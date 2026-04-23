"""Ollama backend — local LLM inference via the Ollama HTTP server.

Default endpoint: ``http://localhost:11434``. Tool-use is supported by
Ollama for models that expose a ``tools`` field (llama3.1+, qwen2.5+, etc.).

If the user doesn't pass an explicit ``model``, the backend probes
``/api/tags`` to pick one of the models that is actually installed —
preferring known-good tool-use families (``llama3.1`` / ``llama3.2`` /
``qwen2.5`` / ``mistral``) over plain ``llama3`` (which is tool-use-
unaware), and finally falling back to the first installed entry.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

import requests

from orgchem.agent.llm.base import LLMBackend, ChatMessage, ToolCall
from orgchem.messaging.errors import NetworkError


_TOOL_USE_PREFERENCE = (
    # Known tool-use-capable families, best first.
    # NOTE: variants like `llama3.2-vision` or `codellama` are
    # excluded separately via ``_TOOL_USE_EXCLUDE_SUFFIXES`` below.
    "llama3.1", "llama3.2", "llama3.3", "qwen2.5", "qwen3",
    "mistral-nemo", "mixtral", "command-r", "firefunction-v2",
    "granite3.1-dense", "nemotron",
)

# Stem suffixes that disqualify a tag from the tool-use allowlist,
# even if its base name matches a family above. These models either
# don't support tools at all (vision) or weren't trained for them
# (code specialists).
_TOOL_USE_EXCLUDE_SUFFIXES = (
    "-vision", "-code", "-coder", "-coder-lite", "-instruct",
)
# Bare model stems that are *not* tool-use-capable even though the
# family is. Plain ``llama3`` (the original 8B) predates Meta's
# tool-use training; Ollama returns HTTP 500 "does not support
# tools" if we send it a ``tools`` list.
_TOOL_USE_DISALLOW_EXACT = (
    "llama3", "llama2", "llama",
)


def model_supports_tools(tag: str) -> bool:
    """Heuristic: does this Ollama model tag accept a ``tools``
    field in ``/api/chat`` without erroring? Uses an explicit
    allowlist of families plus suffix-based exclusion for the
    known non-tool-use variants (vision, code)."""
    stem = tag.split(":", 1)[0].lower()
    if stem in _TOOL_USE_DISALLOW_EXACT:
        return False
    for bad in _TOOL_USE_EXCLUDE_SUFFIXES:
        if bad in stem:
            return False
    for family in _TOOL_USE_PREFERENCE:
        if stem == family or stem.startswith(family + "-"):
            # But re-apply the exclude check so e.g.
            # ``llama3.2-vision`` doesn't slip through the prefix test.
            if any(bad in stem for bad in _TOOL_USE_EXCLUDE_SUFFIXES):
                return False
            return True
    return False


def ollama_list_models(host: str = "http://localhost:11434",
                       timeout: float = 3.0) -> List[str]:
    """Return the list of model tags installed on a reachable Ollama
    server. Raises :class:`NetworkError` if the server can't be
    contacted — that's the explicit signal the tutor panel uses to
    tell the user "Ollama isn't running"."""
    host = host.rstrip("/")
    try:
        r = requests.get(f"{host}/api/tags", timeout=timeout)
        r.raise_for_status()
    except requests.RequestException as e:
        raise NetworkError(
            f"Could not reach Ollama at {host}: {e}. Is the server "
            f"running? (`ollama serve` or run the Ollama desktop app.)"
        ) from e
    payload = r.json() or {}
    models = payload.get("models") or []
    return [m.get("name", "") for m in models if m.get("name")]


def _is_text_chat_friendly(tag: str) -> bool:
    """Is this tag likely to work for text-only chat? Filters out
    specialist variants (vision models need images, code models
    drift off-topic for general tutoring) so the picker doesn't
    land on one of them as a "fallback"."""
    stem = tag.split(":", 1)[0].lower()
    for bad in _TOOL_USE_EXCLUDE_SUFFIXES:
        if bad in stem:
            return False
    return True


def _pick_best_model(installed: List[str]) -> Optional[str]:
    """From the models a user has actually pulled, prefer tool-use-
    capable tags (as judged by :func:`model_supports_tools`),
    ordered by the :data:`_TOOL_USE_PREFERENCE` list. Fall back to
    the first *text-chat-friendly* installed tag if nothing
    tool-capable is available — so general chat still works even
    without tool support, and we never pick a vision-only or code-
    only specialist by default."""
    if not installed:
        return None
    # First pass: by preference family, only accept tool-capable tags.
    for family in _TOOL_USE_PREFERENCE:
        for name in installed:
            stem = name.split(":", 1)[0].lower()
            if (stem == family or stem.startswith(family + "-")) \
                    and model_supports_tools(name):
                return name
    # Second pass: any tool-capable tag (covers exotics).
    for name in installed:
        if model_supports_tools(name):
            return name
    # Third pass: nothing tool-capable, but avoid landing on vision /
    # code specialists — they rarely work for plain-text tutoring
    # chat and are often broken when out-of-sync with Ollama's
    # runtime (reported 2026-04-23).
    for name in installed:
        if _is_text_chat_friendly(name):
            return name
    # Absolute last resort: nothing matched any of the above.
    return installed[0]


class OllamaBackend(LLMBackend):
    name = "ollama"
    # Placeholder default — the constructor replaces it with a real
    # installed model the first time probing succeeds.
    default_model = "llama3.1"

    def __init__(self, model: str = "",
                 host: str = "http://localhost:11434",
                 auto_select: bool = True, **cfg: Any):
        super().__init__(model=model, **cfg)
        self.host = host.rstrip("/")
        self.available_models: List[str] = []
        # Populate ``available_models`` whenever ``auto_select`` is
        # on, regardless of whether ``model`` was explicitly supplied
        # — the tutor panel's status line uses this to tell the user
        # how many Ollama tags are visible.
        if auto_select:
            try:
                self.available_models = ollama_list_models(self.host)
            except NetworkError:
                # Stay constructible even without a server so the agent
                # action registry and unit tests work offline.
                self.available_models = []
            if not model:
                picked = _pick_best_model(self.available_models)
                if picked:
                    self.model = picked

    def chat(self, history: List[ChatMessage], tools: List[Dict[str, Any]],
             system: str = "") -> ChatMessage:
        model_tag = self.model or self.default_model
        body: Dict[str, Any] = {
            "model": model_tag,
            "messages": _history_to_ollama(history, system),
            "stream": False,
        }
        # Only attach `tools` when the selected model is known to
        # support them. Otherwise Ollama returns HTTP 500 with
        # "<tag> does not support tools" and the whole turn dies.
        send_tools = bool(tools) and model_supports_tools(model_tag)
        if send_tools:
            body["tools"] = [_tool_to_ollama(t) for t in tools]

        try:
            r = requests.post(f"{self.host}/api/chat", json=body,
                              timeout=180)
            # Graceful fallback: if a model we *thought* supported
            # tools actually rejects the `tools` field (Ollama's
            # allowlist evolves), strip it and retry once.
            if (r.status_code == 500 and send_tools
                    and "does not support tools" in (r.text or "")):
                body.pop("tools", None)
                r = requests.post(f"{self.host}/api/chat", json=body,
                                  timeout=180)
            r.raise_for_status()
        except requests.RequestException as e:
            msg = str(e)
            # Surface the Ollama-side error body when present — more
            # useful than a bare "500 Server Error" in the tutor UI.
            try:
                body_text = e.response.text if getattr(
                    e, "response", None) is not None else ""
            except Exception:  # noqa: BLE001
                body_text = ""
            if body_text:
                msg = f"{msg}\n{body_text.strip()[:500]}"
            raise NetworkError(f"Ollama request failed: {msg}") from e

        payload = r.json()
        msg = payload.get("message", {}) or {}
        tool_calls: List[ToolCall] = []
        for i, tc in enumerate(msg.get("tool_calls") or []):
            fn = tc.get("function", {}) or {}
            args = fn.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            tool_calls.append(ToolCall(
                name=fn.get("name", ""),
                id=f"ollama-{i}",
                arguments=args,
            ))
        return ChatMessage(role="assistant", text=msg.get("content", "") or "",
                           tool_calls=tool_calls)


def _history_to_ollama(history: List[ChatMessage], system: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if system:
        out.append({"role": "system", "content": system})
    for m in history:
        if m.role == "user":
            out.append({"role": "user", "content": m.text})
            for tr in m.tool_results:
                out.append({"role": "tool", "content": json.dumps(tr.content, default=str)})
        elif m.role == "assistant":
            entry: Dict[str, Any] = {"role": "assistant", "content": m.text}
            if m.tool_calls:
                entry["tool_calls"] = [{
                    "function": {"name": tc.name, "arguments": tc.arguments},
                } for tc in m.tool_calls]
            out.append(entry)
    return out


def _tool_to_ollama(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema.get("description", ""),
            "parameters": schema.get("input_schema", {"type": "object", "properties": {}}),
        },
    }
