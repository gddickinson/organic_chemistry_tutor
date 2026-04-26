"""Decorator-based action registry.

Every app capability an LLM might invoke is registered here. Actions have
typed signatures (so we can auto-emit JSON-schema tool specs) and concise
docstrings (which become the LLM-facing descriptions).

Usage
-----
    from orgchem.agent.actions import action

    @action(category="molecule")
    def show_molecule(name_or_id: str) -> dict:
        '''Display a molecule in the viewers by DB id or name.'''
        ...

An action implementation may be pure Python (no GUI) or it may emit a
bus signal for the GUI to react to. The ``gui/`` package subscribes to these
signals — actions never import from ``orgchem.gui``.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import inspect
from typing import Any, Callable, Dict, List, Optional, get_type_hints


@dataclass
class ActionSpec:
    name: str
    fn: Callable[..., Any]
    description: str
    category: str = "general"
    params: List[Dict[str, Any]] = field(default_factory=list)

    def json_schema(self) -> Dict[str, Any]:
        """Return an Anthropic / OpenAI-style tool schema for this action."""
        props: Dict[str, Any] = {}
        required: List[str] = []
        for p in self.params:
            props[p["name"]] = {"type": p["type"], "description": p.get("description", "")}
            if p["required"]:
                required.append(p["name"])
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": props,
                "required": required,
            },
        }


_PY_TO_JSON = {
    int: "integer",
    float: "number",
    str: "string",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _params_from_signature(fn: Callable[..., Any]) -> List[Dict[str, Any]]:
    sig = inspect.signature(fn)
    hints = get_type_hints(fn)
    out: List[Dict[str, Any]] = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        t = hints.get(name, str)
        out.append({
            "name": name,
            "type": _PY_TO_JSON.get(t, "string"),
            "required": param.default is inspect.Parameter.empty,
            "description": "",
        })
    return out


_REGISTRY: Dict[str, ActionSpec] = {}


def action(name: Optional[str] = None, category: str = "general") -> Callable:
    """Register a function as an LLM-callable action."""
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        spec = ActionSpec(
            name=name or fn.__name__,
            fn=fn,
            description=(fn.__doc__ or "").strip().split("\n")[0],
            category=category,
            params=_params_from_signature(fn),
        )
        _REGISTRY[spec.name] = spec
        return fn
    return deco


def registry() -> Dict[str, ActionSpec]:
    return dict(_REGISTRY)


def invoke(name: str, /, **kwargs: Any) -> Any:
    """Invoke a registered action by name.

    The action-name argument is **positional-only** (the ``/`` after
    it).  This matters because some actions declare a parameter
    literally called ``name`` (e.g. ``import_smiles(name, smiles)``),
    and the agent's tool-loop calls this as
    ``invoke(tool.name, **tool.arguments)``.  Without the
    positional-only marker, ``tool.arguments = {"name": "glucose",
    ...}`` would collide with the registry's own ``name`` parameter
    and raise ``TypeError: invoke() got multiple values for
    argument 'name'``.
    """
    if name not in _REGISTRY:
        raise KeyError(f"Unknown action: {name!r}. Known: {sorted(_REGISTRY)}")
    return _REGISTRY[name].fn(**kwargs)


def tool_schemas() -> List[Dict[str, Any]]:
    """Return Anthropic-style tool schemas for every registered action."""
    return [spec.json_schema() for spec in _REGISTRY.values()]
