"""Phase 38c.1 (round 186) — lab-equipment palette data layer.

Headless data core for the upcoming Phase-38c canvas's drag-source
toolbar.  Groups Phase-38a equipment by category in a stable
display order so the GUI can render category sections (Glassware /
Adapter / Condenser / …) with the equipment items inside each.

This module is **pure data** — no Qt imports, no rendering.  The
canvas, drop targets, snap-validation, and connection-drawing all
ship in subsequent sub-phases (38c.2-38c.5).

Public API:
- :class:`PaletteCategory` frozen dataclass
- :class:`Palette` aggregate
- :func:`default_palette()` — every catalogue equipment, ordered
- :func:`palette_for_setup(setup_id)` — filtered to one seeded
  setup's equipment list (powers the future "Build on canvas"
  button on the Phase-38b *Lab setups…* dialog)
- :func:`categories_in_display_order()` — canonical category order
- :func:`category_label(category_id)` — human-readable label
- :func:`palette_to_dict(palette)` — JSON-friendly serialisation
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Display ordering — canonical sequence for the palette toolbar.
# Drives the visual grouping in the future canvas.  Items inside
# each category use catalogue insertion order.
# ----------------------------------------------------------------
_CATEGORY_DISPLAY_ORDER: Tuple[str, ...] = (
    "glassware",
    "adapter",
    "condenser",
    "separation",
    "filtration",
    "heating",
    "cooling",
    "stirring",
    "vacuum",
    "support",
    "safety",
    "analytical",
)

_CATEGORY_LABELS: Dict[str, str] = {
    "glassware": "Glassware",
    "adapter": "Adapters",
    "condenser": "Condensers",
    "separation": "Separation",
    "filtration": "Filtration",
    "heating": "Heating",
    "cooling": "Cooling",
    "stirring": "Stirring",
    "vacuum": "Vacuum",
    "support": "Support",
    "safety": "Safety",
    "analytical": "Analytical",
}


@dataclass(frozen=True)
class PaletteCategory:
    """One category in the palette toolbar.

    ``equipment_ids`` is an immutable tuple ordered for the GUI's
    grid / list display."""
    category_id: str
    label: str
    equipment_ids: Tuple[str, ...]

    def __len__(self) -> int:
        return len(self.equipment_ids)


@dataclass
class Palette:
    """Ordered palette for the Phase-38c canvas toolbar.

    ``categories`` is a list of :class:`PaletteCategory` in display
    order.  Empty categories are stripped — the GUI never has to
    render an empty section."""
    categories: List[PaletteCategory] = field(default_factory=list)

    def __len__(self) -> int:
        return sum(len(c) for c in self.categories)

    def category(self, category_id: str) -> Optional[PaletteCategory]:
        return next(
            (c for c in self.categories
             if c.category_id == category_id),
            None,
        )

    def all_equipment_ids(self) -> List[str]:
        out: List[str] = []
        for c in self.categories:
            out.extend(c.equipment_ids)
        return out


# ----------------------------------------------------------------
# Public API
# ----------------------------------------------------------------
def categories_in_display_order() -> Tuple[str, ...]:
    """Return the canonical display-order tuple of category ids."""
    return _CATEGORY_DISPLAY_ORDER


def category_label(category_id: str) -> str:
    """Human-readable label for a category id.  Falls back to the
    category id with the first letter capitalised if unknown."""
    return _CATEGORY_LABELS.get(
        category_id, category_id.replace("-", " ").title())


def default_palette() -> Palette:
    """Build the default palette covering every Phase-38a
    equipment item, grouped + ordered by category."""
    from orgchem.core.lab_equipment import list_equipment
    palette = Palette()
    for cat_id in _CATEGORY_DISPLAY_ORDER:
        items = list_equipment(cat_id) or []
        if not items:
            continue
        palette.categories.append(PaletteCategory(
            category_id=cat_id,
            label=category_label(cat_id),
            equipment_ids=tuple(e.id for e in items),
        ))
    return palette


def palette_for_setup(setup_id: str) -> Optional[Palette]:
    """Return a palette pre-populated with just the equipment a
    seeded Phase-38b setup uses.  Returns ``None`` if the setup
    id is unknown.  Useful for the future *Build on canvas*
    button — the user gets a focused toolbar showing only the
    pieces that participate in the chosen setup."""
    from orgchem.core.lab_equipment import get_equipment
    from orgchem.core.lab_setups import get_setup
    setup = get_setup(setup_id)
    if setup is None:
        return None
    # Group the setup's equipment ids by category, preserving
    # display order.  Deduplicate (e.g. two RBFs in distillation).
    seen: set = set()
    by_cat: Dict[str, List[str]] = {}
    for eid in setup.equipment:
        if eid in seen:
            continue
        seen.add(eid)
        eq = get_equipment(eid)
        if eq is None:
            continue
        by_cat.setdefault(eq.category, []).append(eid)
    palette = Palette()
    for cat_id in _CATEGORY_DISPLAY_ORDER:
        ids = by_cat.get(cat_id) or []
        if not ids:
            continue
        palette.categories.append(PaletteCategory(
            category_id=cat_id,
            label=category_label(cat_id),
            equipment_ids=tuple(ids),
        ))
    return palette


def palette_to_dict(palette: Palette) -> Dict[str, object]:
    """JSON-friendly serialisation for the agent action surface
    (Phase 38c.5)."""
    return {
        "total_equipment": len(palette),
        "categories": [
            {
                "category_id": c.category_id,
                "label": c.label,
                "equipment_ids": list(c.equipment_ids),
            }
            for c in palette.categories
        ],
    }
