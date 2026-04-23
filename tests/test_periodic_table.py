"""Tests for Phase 27a — periodic-table data module."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


def test_all_118_elements_present():
    from orgchem.core.periodic_table import ELEMENTS
    assert len(ELEMENTS) == 118


def test_elements_indexed_by_z():
    from orgchem.core.periodic_table import ELEMENTS
    for i, e in enumerate(ELEMENTS, start=1):
        assert e.z == i, f"index {i-1} has z={e.z}"


def test_hydrogen_and_oganesson_endpoints():
    from orgchem.core.periodic_table import get_element
    h = get_element("H")
    og = get_element(118)
    assert h is not None and h.name == "Hydrogen" and h.period == 1
    assert og is not None and og.symbol == "Og" and og.period == 7


def test_category_palette_covers_every_element():
    from orgchem.core.periodic_table import ELEMENTS, CATEGORY_COLOURS
    for e in ELEMENTS:
        assert e.category in CATEGORY_COLOURS, e.symbol
        assert e.colour().startswith("#")


def test_atomic_mass_from_rdkit():
    """Masses should be populated (non-zero) for the full set."""
    from orgchem.core.periodic_table import ELEMENTS
    # At least the first 94 are naturally occurring; RDKit may return
    # 0 for some super-heavy synthetic elements.
    natural = [e for e in ELEMENTS if e.z <= 94]
    for e in natural:
        assert e.atomic_mass > 0.0, e.symbol


def test_get_element_accepts_multiple_forms():
    from orgchem.core.periodic_table import get_element
    assert get_element("Fe").z == 26
    assert get_element("fe").z == 26            # case insensitive
    assert get_element("iron").z == 26          # by name
    assert get_element(26).symbol == "Fe"
    assert get_element("26").symbol == "Fe"
    assert get_element("Zzz") is None


def test_elements_by_category_halogens():
    from orgchem.core.periodic_table import elements_by_category
    halogens = elements_by_category("halogen")
    symbols = {e.symbol for e in halogens}
    # F/Cl/Br/I are always halogens; At + Ts also categorised here.
    for s in ("F", "Cl", "Br", "I"):
        assert s in symbols


def test_categories_enumeration_is_stable():
    from orgchem.core.periodic_table import categories
    cats = categories()
    # Canonical families.
    for key in ("alkali-metal", "noble-gas", "halogen",
                "transition-metal", "lanthanide", "actinide"):
        assert key in cats


def test_element_to_dict_shape():
    from orgchem.core.periodic_table import get_element
    d = get_element("O").to_dict()
    for key in ("symbol", "name", "z", "group", "period",
                "block", "category", "atomic_mass",
                "electronegativity", "common_oxidation_states",
                "electron_configuration", "colour"):
        assert key in d


# ---- Agent actions ----------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_elements_action(app):
    rows = app.call("list_elements")
    assert len(rows) == 118


def test_get_element_action(app):
    r = app.call("get_element", symbol_or_z="N")
    assert r["symbol"] == "N"
    assert r["z"] == 7


def test_get_element_action_unknown(app):
    r = app.call("get_element", symbol_or_z="Qx")
    assert "error" in r


def test_elements_by_category_action(app):
    rows = app.call("elements_by_category", category="noble-gas")
    symbols = {r["symbol"] for r in rows}
    for s in ("He", "Ne", "Ar", "Kr", "Xe", "Rn"):
        assert s in symbols
