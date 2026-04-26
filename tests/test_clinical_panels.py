"""Phase 37b (round 137) — headless tests for the clinical
lab-panel catalogue + agent actions.

Pure data + lookup checks; no Qt event loop required.
"""
from __future__ import annotations
import os

import pytest


# ---- catalogue contents ---------------------------------------

def test_three_primary_panels_present():
    from orgchem.core.clinical_panels import list_panels
    ids = {p.id for p in list_panels()}
    for must in ("bmp", "cmp", "lipid"):
        assert must in ids


def test_extended_panels_present():
    from orgchem.core.clinical_panels import list_panels
    ids = {p.id for p in list_panels()}
    for must in ("diabetes_followup", "thyroid"):
        assert must in ids


def test_bmp_has_eight_analytes():
    """BMP = Chem 8 (or Chem 7 + Ca) — 8 analytes."""
    from orgchem.core.clinical_panels import get_panel
    p = get_panel("bmp")
    assert p is not None
    assert len(p.analytes) == 8


def test_cmp_extends_bmp_with_six_more():
    """CMP = BMP + 6 liver / protein analytes = 14 total."""
    from orgchem.core.clinical_panels import get_panel
    bmp = get_panel("bmp")
    cmp = get_panel("cmp")
    assert len(cmp.analytes) == 14
    bmp_ids = {a.id for a in bmp.analytes}
    cmp_ids = {a.id for a in cmp.analytes}
    assert bmp_ids.issubset(cmp_ids), \
        "CMP should be a superset of BMP"
    extra = cmp_ids - bmp_ids
    assert len(extra) == 6


def test_lipid_panel_has_four_analytes():
    from orgchem.core.clinical_panels import get_panel
    p = get_panel("lipid")
    assert len(p.analytes) == 4
    ids = {a.id for a in p.analytes}
    assert ids == {"total_chol", "ldl_chol",
                   "hdl_chol", "triglycerides"}


def test_each_analyte_has_required_fields():
    from orgchem.core.clinical_panels import list_analytes
    for a in list_analytes():
        assert a.id, f"missing id"
        assert a.name, f"missing name on {a.id}"
        assert a.abbreviation, f"missing abbrev on {a.id}"
        assert a.units, f"missing units on {a.id}"
        assert a.normal_range, f"missing range on {a.id}"
        assert a.clinical_significance, \
            f"missing significance on {a.id}"


def test_each_panel_has_required_meta():
    from orgchem.core.clinical_panels import list_panels
    for p in list_panels():
        assert p.id and p.name and p.short_name
        assert p.purpose
        assert p.sample
        assert p.procedure
        assert p.fasting
        assert len(p.analytes) > 0


def test_known_clinical_landmarks_in_descriptions():
    """A handful of teaching invariants on the analyte clinical-
    significance text — ensures future copy-edits don't lose
    the things students MUST learn from each row."""
    from orgchem.core.clinical_panels import get_analyte
    bun = get_analyte("bun")
    assert "kidney" in bun.clinical_significance.lower() \
        or "renal" in bun.clinical_significance.lower()
    cr = get_analyte("creatinine")
    assert "gfr" in cr.clinical_significance.lower() \
        or "filtration" in cr.clinical_significance.lower()
    hba1c = get_analyte("hba1c")
    assert "3 month" in hba1c.clinical_significance.lower() \
        or "long-term" in hba1c.clinical_significance.lower()
    tsh = get_analyte("tsh")
    assert "thyroid" in tsh.clinical_significance.lower()


# ---- analyte category coverage --------------------------------

def test_analyte_categories_present():
    """All 7 analyte categories should be represented."""
    from orgchem.core.clinical_panels import (
        list_analytes, VALID_CATEGORIES,
    )
    seen = {a.category for a in list_analytes()}
    assert seen == set(VALID_CATEGORIES), \
        f"missing: {set(VALID_CATEGORIES) - seen}"


def test_list_analytes_filtered_by_category():
    from orgchem.core.clinical_panels import list_analytes
    lipids = list_analytes(category="lipid")
    assert len(lipids) == 4
    assert all(a.category == "lipid" for a in lipids)
    elec = list_analytes(category="electrolyte")
    assert len(elec) >= 4   # Na / K / Cl / HCO₃
    for a in elec:
        assert a.category == "electrolyte"


def test_list_analytes_unknown_category_returns_empty():
    from orgchem.core.clinical_panels import list_analytes
    assert list_analytes(category="nonexistent") == []


# ---- lookup helpers -------------------------------------------

def test_get_panel_returns_none_for_unknown_id():
    from orgchem.core.clinical_panels import get_panel
    assert get_panel("does-not-exist") is None


def test_get_analyte_returns_none_for_unknown_id():
    from orgchem.core.clinical_panels import get_analyte
    assert get_analyte("bogus") is None


def test_find_analyte_by_name():
    from orgchem.core.clinical_panels import find_analyte
    rows = find_analyte("sodium")
    assert len(rows) == 1
    assert rows[0].id == "sodium"


def test_find_analyte_by_abbreviation():
    from orgchem.core.clinical_panels import find_analyte
    rows = find_analyte("BUN")
    assert len(rows) == 1
    assert rows[0].id == "bun"


def test_find_analyte_case_insensitive():
    from orgchem.core.clinical_panels import find_analyte
    a = {x.id for x in find_analyte("Glucose")}
    b = {x.id for x in find_analyte("glucose")}
    c = {x.id for x in find_analyte("GLUCOSE")}
    assert a == b == c == {"glucose"}


def test_find_analyte_empty_returns_empty():
    from orgchem.core.clinical_panels import find_analyte
    assert find_analyte("") == []


def test_find_analyte_no_match_returns_empty():
    from orgchem.core.clinical_panels import find_analyte
    assert find_analyte("xyznotreal") == []


# ---- shared analyte instance identity -------------------------

def test_bmp_and_cmp_share_glucose_instance():
    """Frozen-dataclass identity check: CMP's glucose row is
    literally the same object as BMP's glucose row."""
    from orgchem.core.clinical_panels import get_panel
    bmp = get_panel("bmp")
    cmp = get_panel("cmp")
    bmp_glu = next(a for a in bmp.analytes if a.id == "glucose")
    cmp_glu = next(a for a in cmp.analytes if a.id == "glucose")
    assert bmp_glu is cmp_glu


# ---- to_dict serialisation ------------------------------------

def test_analyte_to_dict_keys():
    from orgchem.core.clinical_panels import (
        analyte_to_dict, get_analyte,
    )
    d = analyte_to_dict(get_analyte("creatinine"))
    expected = {
        "id", "name", "abbreviation", "category", "units",
        "normal_range", "clinical_significance", "notes",
    }
    assert set(d.keys()) == expected


def test_panel_to_dict_includes_analytes():
    from orgchem.core.clinical_panels import (
        get_panel, panel_to_dict,
    )
    d = panel_to_dict(get_panel("bmp"))
    assert d["short_name"] == "BMP"
    assert isinstance(d["analytes"], list)
    assert len(d["analytes"]) == 8


# ---- agent actions --------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_lab_panels(app):
    rows = app.call("list_lab_panels")
    ids = {r["id"] for r in rows}
    for must in ("bmp", "cmp", "lipid"):
        assert must in ids


def test_action_get_lab_panel(app):
    r = app.call("get_lab_panel", panel_id="bmp")
    assert "error" not in r
    assert r["short_name"] == "BMP"
    assert len(r["analytes"]) == 8


def test_action_get_lab_panel_unknown_returns_error(app):
    r = app.call("get_lab_panel", panel_id="bogus")
    assert "error" in r


def test_action_list_lab_analytes(app):
    rows = app.call("list_lab_analytes")
    assert isinstance(rows, list)
    assert len(rows) >= 20


def test_action_list_lab_analytes_filtered(app):
    rows = app.call("list_lab_analytes", category="lipid")
    assert all(r["category"] == "lipid" for r in rows)
    assert len(rows) == 4


def test_action_list_lab_analytes_unknown_category(app):
    rows = app.call("list_lab_analytes",
                    category="nonexistent")
    assert len(rows) == 1
    assert "error" in rows[0]


def test_action_find_lab_analyte(app):
    rows = app.call("find_lab_analyte", needle="sodium")
    assert len(rows) == 1
    assert rows[0]["id"] == "sodium"


def test_action_find_lab_analyte_by_abbrev(app):
    rows = app.call("find_lab_analyte", needle="BUN")
    assert any(r["id"] == "bun" for r in rows)
