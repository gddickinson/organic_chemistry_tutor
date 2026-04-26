"""Phase 37a (round 136) — headless tests for the qualitative
inorganic-test catalogue + agent actions.

Pure data + lookup checks; no Qt event loop required.
"""
from __future__ import annotations
import os

import pytest


# ---- catalogue contents ---------------------------------------

def test_catalogue_has_all_seven_categories():
    from orgchem.core.qualitative_tests import (
        VALID_CATEGORIES, list_tests,
    )
    seen_cats = {t.category for t in list_tests()}
    assert seen_cats == set(VALID_CATEGORIES), \
        f"missing categories: {set(VALID_CATEGORIES) - seen_cats}"


def test_catalogue_size_at_least_thirty():
    from orgchem.core.qualitative_tests import list_tests
    assert len(list_tests()) >= 30


def test_each_test_has_required_fields():
    from orgchem.core.qualitative_tests import list_tests
    for t in list_tests():
        assert t.id, f"missing id on {t}"
        assert t.name, f"missing name on {t.id}"
        assert t.target, f"missing target on {t.id}"
        assert t.target_class in ("cation", "anion", "gas"), \
            f"bad target_class on {t.id}: {t.target_class}"
        assert t.reagents, f"missing reagents on {t.id}"
        assert t.procedure, f"missing procedure on {t.id}"
        assert t.positive_observation, \
            f"missing positive_observation on {t.id}"
        assert t.colour_hex.startswith("#") \
            and len(t.colour_hex) == 7, \
            f"bad colour_hex on {t.id}: {t.colour_hex}"


def test_canonical_flame_tests_present():
    from orgchem.core.qualitative_tests import find_tests_for
    # The four canonical undergraduate flame tests.
    assert len(find_tests_for("Na+")) >= 1
    assert len(find_tests_for("K+")) >= 1
    assert len(find_tests_for("Ca2+")) >= 1
    assert len(find_tests_for("Cu2+")) >= 1


def test_canonical_halide_tests_present():
    from orgchem.core.qualitative_tests import find_tests_for
    for ion in ("Cl-", "Br-", "I-"):
        rows = find_tests_for(ion)
        assert any(r.category == "halide" for r in rows), \
            f"no halide test entry for {ion}"


def test_canonical_gas_tests_present():
    from orgchem.core.qualitative_tests import find_tests_for
    for gas in ("H2", "O2", "CO2", "Cl2", "NH3"):
        rows = find_tests_for(gas)
        assert any(r.category == "gas" for r in rows), \
            f"no gas test entry for {gas}"


# ---- filter / lookup ------------------------------------------

def test_list_filtered_by_category():
    from orgchem.core.qualitative_tests import list_tests
    flame = list_tests(category="flame")
    assert all(t.category == "flame" for t in flame)
    assert len(flame) >= 4


def test_list_unknown_category_returns_empty():
    from orgchem.core.qualitative_tests import list_tests
    assert list_tests(category="not-a-real-category") == []


def test_get_test_returns_none_for_unknown_id():
    from orgchem.core.qualitative_tests import get_test
    assert get_test("does-not-exist") is None


def test_get_test_returns_full_record():
    from orgchem.core.qualitative_tests import get_test
    t = get_test("flame-na")
    assert t is not None
    assert t.target == "Na⁺"
    assert "yellow" in t.positive_observation.lower()


# ---- ASCII / unicode-tolerant lookup -------------------------

def test_find_tolerates_ascii_charge_format():
    """`Cu2+` should hit the same record as `Cu²⁺`."""
    from orgchem.core.qualitative_tests import find_tests_for
    unicode_hits = {t.id for t in find_tests_for("Cu²⁺")}
    ascii_hits = {t.id for t in find_tests_for("Cu2+")}
    assert unicode_hits == ascii_hits
    assert len(ascii_hits) >= 2  # flame + hydroxide


def test_find_tolerates_lowercase():
    from orgchem.core.qualitative_tests import find_tests_for
    upper = {t.id for t in find_tests_for("Cl-")}
    lower = {t.id for t in find_tests_for("cl-")}
    assert upper == lower


def test_find_tolerates_whitespace():
    from orgchem.core.qualitative_tests import find_tests_for
    a = {t.id for t in find_tests_for("Cu2+")}
    b = {t.id for t in find_tests_for("Cu  2  +")}
    assert a == b


def test_find_returns_empty_for_unknown_target():
    from orgchem.core.qualitative_tests import find_tests_for
    assert find_tests_for("Xx7+") == []


def test_find_returns_empty_for_empty_string():
    from orgchem.core.qualitative_tests import find_tests_for
    assert find_tests_for("") == []


# ---- amphoteric note ------------------------------------------

def test_aluminium_hydroxide_amphoteric_flag_in_notes():
    """The Al³⁺ hydroxide entry MUST mention amphoteric / "
    "excess NaOH dissolution — that's the discriminating feature
    vs Mg²⁺ / Ca²⁺ teaching point."""
    from orgchem.core.qualitative_tests import get_test
    al = get_test("hydroxide-al3")
    assert al is not None
    notes_lower = al.notes.lower()
    assert "amphoteric" in notes_lower or "excess" in notes_lower
    assert "aluminate" in notes_lower or "[al(oh)" in notes_lower


# ---- to_dict serialisation ------------------------------------

def test_to_dict_round_trip_keys():
    from orgchem.core.qualitative_tests import get_test, to_dict
    t = get_test("hydroxide-cu2")
    d = to_dict(t)
    expected_keys = {
        "id", "name", "category", "target", "target_class",
        "reagents", "procedure", "positive_observation",
        "colour_hex", "notes",
    }
    assert set(d.keys()) == expected_keys
    assert d["id"] == "hydroxide-cu2"


# ---- agent actions --------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_inorganic_tests(app):
    rows = app.call("list_inorganic_tests")
    assert isinstance(rows, list)
    assert len(rows) >= 30
    assert "id" in rows[0]


def test_action_list_filtered_by_category(app):
    rows = app.call("list_inorganic_tests", category="halide")
    assert all(r["category"] == "halide" for r in rows)


def test_action_list_unknown_category_errors(app):
    rows = app.call("list_inorganic_tests",
                    category="not-a-real-cat")
    assert len(rows) == 1
    assert "error" in rows[0]


def test_action_get_inorganic_test(app):
    r = app.call("get_inorganic_test", test_id="flame-cu")
    assert "error" not in r
    assert r["target"] == "Cu²⁺"
    assert r["category"] == "flame"


def test_action_get_unknown_id_returns_error(app):
    r = app.call("get_inorganic_test", test_id="bogus")
    assert "error" in r


def test_action_find_for_target_works_with_ascii(app):
    rows = app.call("find_inorganic_tests_for", target="Cu2+")
    assert len(rows) >= 2
    cats = {r["category"] for r in rows}
    assert "flame" in cats
    assert "hydroxide" in cats
