"""Agent actions for Phase 29a — carbohydrates."""
from __future__ import annotations
from typing import Any, Dict, List

from orgchem.agent.actions import action


@action(category="carbohydrate")
def list_carbohydrates(family: str = "") -> List[Dict[str, Any]]:
    """Enumerate seeded sugars, optionally filtered by family
    (``monosaccharide`` / ``disaccharide`` / ``polysaccharide``)."""
    from orgchem.core.carbohydrates import list_carbohydrates as _list
    return _list(family)


@action(category="carbohydrate")
def get_carbohydrate(carb_name: str) -> Dict[str, Any]:
    """Full entry by name (case-insensitive)."""
    from orgchem.core.carbohydrates import get_carbohydrate as _get
    c = _get(carb_name)
    if c is None:
        return {"error": f"Unknown carbohydrate: {carb_name!r}"}
    return c.to_dict()


@action(category="carbohydrate")
def carbohydrate_families() -> List[str]:
    """The family taxonomy (ordered)."""
    from orgchem.core.carbohydrates import families as _fams
    return _fams()
