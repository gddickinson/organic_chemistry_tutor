"""Phase 38c.1 (round 186) — lab-equipment palette data layer.

Locks in the headless palette structure that the upcoming Phase-
38c canvas's drag-source toolbar will render.  Pure-data layer:
no Qt imports.
"""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# ==================================================================
# Default palette
# ==================================================================

def test_default_palette_covers_every_category():
    """Every non-empty Phase-38a equipment category appears in
    the default palette."""
    from orgchem.core.lab_equipment import categories as eq_cats
    from orgchem.core.lab_palette import default_palette
    palette = default_palette()
    palette_cats = {c.category_id for c in palette.categories}
    # Every catalogue category with ≥ 1 entry should be present.
    for cat in eq_cats():
        from orgchem.core.lab_equipment import list_equipment
        if list_equipment(cat):
            assert cat in palette_cats, \
                f"category {cat!r} missing from default palette"


def test_default_palette_total_matches_catalogue():
    """The default palette enumerates every catalogued
    equipment item exactly once."""
    from orgchem.core.lab_equipment import list_equipment
    from orgchem.core.lab_palette import default_palette
    palette = default_palette()
    total_in_catalogue = len(list_equipment(None))
    assert len(palette) == total_in_catalogue, (
        f"palette has {len(palette)} items; catalogue has "
        f"{total_in_catalogue}"
    )
    # No duplicates.
    ids = palette.all_equipment_ids()
    assert len(ids) == len(set(ids))


def test_default_palette_categories_in_display_order():
    """Categories appear in the canonical display order
    (glassware first, analytical last)."""
    from orgchem.core.lab_palette import (
        default_palette, categories_in_display_order,
    )
    palette = default_palette()
    palette_order = [c.category_id for c in palette.categories]
    canonical = list(categories_in_display_order())
    # palette_order is the canonical order with empties stripped
    canonical_present = [c for c in canonical
                         if c in palette_order]
    assert palette_order == canonical_present


# ==================================================================
# Per-setup palette
# ==================================================================

def test_palette_for_setup_only_includes_setup_equipment():
    """A per-setup palette is filtered down to just the
    equipment IDs that appear in that setup's equipment tuple."""
    from orgchem.core.lab_setups import get_setup
    from orgchem.core.lab_palette import palette_for_setup
    setup = get_setup("simple_distillation")
    palette = palette_for_setup("simple_distillation")
    assert palette is not None
    # Every palette entry must be in the setup's equipment list
    setup_eids = set(setup.equipment)
    for c in palette.categories:
        for eid in c.equipment_ids:
            assert eid in setup_eids


def test_palette_for_setup_returns_none_for_unknown_setup():
    from orgchem.core.lab_palette import palette_for_setup
    assert palette_for_setup("not-a-real-setup") is None


def test_palette_for_setup_deduplicates_repeated_equipment():
    """Setups can list the same equipment id twice (e.g. two RBFs
    in distillation: pot + receiver).  The palette deduplicates."""
    from orgchem.core.lab_palette import palette_for_setup
    palette = palette_for_setup("simple_distillation")
    ids = palette.all_equipment_ids()
    assert len(ids) == len(set(ids)), \
        "palette_for_setup did not deduplicate"


# ==================================================================
# Helpers + serialisation
# ==================================================================

def test_categories_in_display_order_is_immutable_tuple():
    from orgchem.core.lab_palette import (
        categories_in_display_order,
    )
    out = categories_in_display_order()
    assert isinstance(out, tuple)
    assert "glassware" in out
    assert "analytical" in out


def test_category_label_returns_human_readable_string():
    from orgchem.core.lab_palette import category_label
    assert category_label("glassware") == "Glassware"
    assert category_label("adapter") == "Adapters"
    assert category_label("safety") == "Safety"
    # Unknown id falls back to a Title-Cased version.
    assert category_label("not-a-cat") == "Not A Cat"


def test_palette_category_lookup_helper():
    from orgchem.core.lab_palette import default_palette
    p = default_palette()
    cat = p.category("glassware")
    assert cat is not None
    assert cat.category_id == "glassware"
    assert cat.label == "Glassware"
    assert "rbf" in cat.equipment_ids
    # Unknown
    assert p.category("nope") is None


def test_palette_to_dict_round_trip():
    from orgchem.core.lab_palette import (
        default_palette, palette_to_dict,
    )
    p = default_palette()
    d = palette_to_dict(p)
    assert d["total_equipment"] == len(p)
    assert isinstance(d["categories"], list)
    assert all("category_id" in c for c in d["categories"])
    assert all(isinstance(c["equipment_ids"], list)
               for c in d["categories"])


def test_no_qt_import():
    """The palette module is pure-data — must not pull in Qt."""
    import sys
    # Re-import fresh and ensure no PySide6 module appears as a
    # side-effect of loading lab_palette.
    pre = {m for m in sys.modules if m.startswith("PySide6")}
    import orgchem.core.lab_palette  # noqa: F401
    post = {m for m in sys.modules if m.startswith("PySide6")}
    assert post == pre, "lab_palette pulled in Qt"
