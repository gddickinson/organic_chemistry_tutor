"""Phase 37c (round 138) — headless tests for the
chromatography-method catalogue + agent actions.
"""
from __future__ import annotations
import os

import pytest


# ---- catalogue contents ---------------------------------------

def test_catalogue_size_at_least_fifteen():
    from orgchem.core.chromatography_methods import list_methods
    assert len(list_methods()) >= 15


def test_seven_categories_all_represented():
    from orgchem.core.chromatography_methods import (
        VALID_CATEGORIES, list_methods,
    )
    seen = {m.category for m in list_methods()}
    assert seen == set(VALID_CATEGORIES), \
        f"missing: {set(VALID_CATEGORIES) - seen}"


def test_each_method_has_required_fields():
    from orgchem.core.chromatography_methods import list_methods
    for m in list_methods():
        assert m.id, f"missing id"
        assert m.name, f"missing name on {m.id}"
        assert m.abbreviation, f"missing abbrev on {m.id}"
        assert m.category, f"missing category on {m.id}"
        assert m.principle, f"missing principle on {m.id}"
        assert m.stationary_phase, f"missing stat phase on {m.id}"
        assert m.mobile_phase, f"missing mobile phase on {m.id}"
        assert m.detectors, f"missing detectors on {m.id}"
        assert m.typical_analytes, \
            f"missing typical_analytes on {m.id}"
        assert m.strengths, f"missing strengths on {m.id}"
        assert m.limitations, f"missing limitations on {m.id}"
        assert m.procedure, f"missing procedure on {m.id}"


def test_canonical_methods_present():
    from orgchem.core.chromatography_methods import get_method
    for must in ("tlc", "column", "flash", "gc", "gc_ms",
                 "hplc", "lc_ms", "hilic", "fplc", "iex",
                 "sec", "affinity", "ion", "sfc"):
        assert get_method(must) is not None, \
            f"missing method {must}"


def test_user_requested_methods_present():
    """The user explicitly requested GC, HPLC, FPLC — verify
    each one is in the catalogue with content."""
    from orgchem.core.chromatography_methods import get_method
    for tid in ("gc", "hplc", "fplc"):
        m = get_method(tid)
        assert m is not None
        # Each must have a non-trivial principle description.
        assert len(m.principle) > 50


# ---- teaching invariants on individual rows -------------------

def test_hplc_describes_reverse_phase():
    """HPLC entry must mention reverse-phase + C18 — the
    workhorse mode 90 % of practitioners use."""
    from orgchem.core.chromatography_methods import get_method
    h = get_method("hplc")
    body = (h.principle + h.stationary_phase).lower()
    assert "reverse" in body or "c18" in body


def test_gc_mentions_volatility_constraint():
    """GC's hard limit — only volatile / thermally stable
    analytes — must be in the limitations text."""
    from orgchem.core.chromatography_methods import get_method
    g = get_method("gc")
    assert "volatil" in g.limitations.lower() \
        or "thermal" in g.limitations.lower()


def test_sec_explains_size_based_separation():
    """SEC's defining feature — separation by size, not affinity
    — must be in the principle text."""
    from orgchem.core.chromatography_methods import get_method
    s = get_method("sec")
    body = s.principle.lower()
    assert "size" in body or "pore" in body
    assert "void" in body or "early" in body


def test_affinity_mentions_his_tag_or_protein_a():
    """Affinity entry must reference at least one canonical
    workhorse system (His-tag/Ni-NTA, Protein A, GST/glutathione)."""
    from orgchem.core.chromatography_methods import get_method
    a = get_method("affinity")
    body = (a.stationary_phase + a.notes
            + a.typical_analytes).lower()
    assert ("his" in body or "ni-nta" in body
            or "protein a" in body or "gst" in body)


def test_sfc_mentions_chiral_separation():
    """SFC is the dominant modern chiral-separation method —
    must be in the strengths or typical_analytes."""
    from orgchem.core.chromatography_methods import get_method
    s = get_method("sfc")
    body = (s.strengths + s.typical_analytes).lower()
    assert "chiral" in body or "enantiomer" in body


# ---- filter / lookup -----------------------------------------

def test_list_filtered_by_category():
    from orgchem.core.chromatography_methods import list_methods
    proteins = list_methods(category="protein")
    assert all(m.category == "protein" for m in proteins)
    assert len(proteins) >= 4   # FPLC + IEX + SEC + affinity


def test_list_unknown_category_returns_empty():
    from orgchem.core.chromatography_methods import list_methods
    assert list_methods(category="not-a-real-category") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.chromatography_methods import get_method
    assert get_method("does-not-exist") is None


def test_find_methods_substring():
    from orgchem.core.chromatography_methods import find_methods
    rows = find_methods("hplc")
    ids = {m.id for m in rows}
    # Should pick up plain HPLC + LC-MS (matches "hplc" in "high-
    # performance liquid"); HILIC also contains "lc"-related
    # terms.
    assert "hplc" in ids


def test_find_methods_case_insensitive():
    from orgchem.core.chromatography_methods import find_methods
    a = {m.id for m in find_methods("GC")}
    b = {m.id for m in find_methods("gc")}
    assert a == b
    assert "gc" in a and "gc_ms" in a


def test_find_methods_empty_returns_empty():
    from orgchem.core.chromatography_methods import find_methods
    assert find_methods("") == []


# ---- to_dict serialisation ------------------------------------

def test_to_dict_keys():
    from orgchem.core.chromatography_methods import (
        get_method, to_dict,
    )
    d = to_dict(get_method("tlc"))
    expected = {
        "id", "name", "abbreviation", "category", "principle",
        "stationary_phase", "mobile_phase", "detectors",
        "typical_analytes", "strengths", "limitations",
        "procedure", "notes",
    }
    assert set(d.keys()) == expected


# ---- agent actions --------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_methods(app):
    rows = app.call("list_chromatography_methods")
    assert len(rows) >= 15


def test_action_list_methods_filtered(app):
    rows = app.call("list_chromatography_methods",
                    category="gas")
    assert all(r["category"] == "gas" for r in rows)


def test_action_list_methods_unknown_category_errors(app):
    rows = app.call("list_chromatography_methods",
                    category="bogus")
    assert len(rows) == 1
    assert "error" in rows[0]


def test_action_get_method(app):
    r = app.call("get_chromatography_method", method_id="hplc")
    assert "error" not in r
    assert r["abbreviation"] == "HPLC"


def test_action_get_unknown_method(app):
    r = app.call("get_chromatography_method", method_id="bogus")
    assert "error" in r


def test_action_find_methods(app):
    rows = app.call("find_chromatography_methods", needle="ion")
    # "ion" should match: ion-exchange + ion chromatography
    ids = {r["id"] for r in rows}
    assert "iex" in ids
    assert "ion" in ids
