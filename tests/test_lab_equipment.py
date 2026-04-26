"""Phase 38a (round 140) — headless tests for the lab-equipment
catalogue + agent actions.
"""
from __future__ import annotations
import os

import pytest


# ---- catalogue contents ---------------------------------------

def test_catalogue_size_at_least_thirty_five():
    from orgchem.core.lab_equipment import list_equipment
    assert len(list_equipment()) >= 35


def test_twelve_categories_all_represented():
    from orgchem.core.lab_equipment import (
        VALID_CATEGORIES, list_equipment,
    )
    seen = {e.category for e in list_equipment()}
    assert seen == set(VALID_CATEGORIES), \
        f"missing: {set(VALID_CATEGORIES) - seen}"


def test_every_entry_has_required_fields():
    from orgchem.core.lab_equipment import list_equipment
    for e in list_equipment():
        assert e.id, f"missing id"
        assert e.name, f"missing name on {e.id}"
        assert e.category, f"missing category on {e.id}"
        assert e.description, f"missing description on {e.id}"
        assert e.typical_uses, f"missing typical_uses on {e.id}"


def test_each_entry_id_unique():
    from orgchem.core.lab_equipment import list_equipment
    ids = [e.id for e in list_equipment()]
    assert len(ids) == len(set(ids)), \
        f"duplicate id: {[i for i in ids if ids.count(i) > 1]}"


def test_canonical_apparatus_present():
    """The pieces that appear in EVERY undergraduate lab —
    these MUST be in the catalogue or any setup story breaks."""
    from orgchem.core.lab_equipment import get_equipment
    for must in ("rbf", "rbf_3neck", "erlenmeyer", "beaker",
                 "distillation_head", "claisen_adapter",
                 "vacuum_adapter", "stopper",
                 "liebig_condenser", "allihn_condenser",
                 "heating_mantle", "variac", "hotplate_stirrer",
                 "sep_funnel", "vigreux_column",
                 "buchner_funnel", "filter_flask",
                 "vacuum_pump", "stir_bar",
                 "ring_stand", "clamp_3prong",
                 "fume_hood", "thermometer"):
        assert get_equipment(must) is not None, \
            f"missing apparatus: {must}"


# ---- teaching-invariant content checks ------------------------

def test_rbf_safety_mentions_cork_or_clamp():
    """Round-bottom flask must call out the support requirement
    — it's the most common safety pitfall for beginners."""
    from orgchem.core.lab_equipment import get_equipment
    body = get_equipment("rbf").safety_notes.lower()
    assert "cork" in body or "clamp" in body


def test_three_neck_flask_lists_three_ports():
    from orgchem.core.lab_equipment import get_equipment
    e = get_equipment("rbf_3neck")
    assert len(e.connection_ports) == 3
    names = {p.name for p in e.connection_ports}
    assert {"center", "left", "right"} == names


def test_distillation_head_has_three_ports():
    """Bottom (joins distillation pot), top (thermometer),
    side (joins condenser)."""
    from orgchem.core.lab_equipment import get_equipment
    e = get_equipment("distillation_head")
    assert len(e.connection_ports) == 3


def test_liebig_has_water_in_and_out_hoses():
    from orgchem.core.lab_equipment import get_equipment
    e = get_equipment("liebig_condenser")
    hose_names = {p.name for p in e.connection_ports
                  if p.joint_type == "hose"}
    assert {"water-in", "water-out"} <= hose_names


def test_separatory_funnel_safety_mentions_venting():
    from orgchem.core.lab_equipment import get_equipment
    body = get_equipment("sep_funnel").safety_notes.lower()
    assert "vent" in body or "pressure" in body


def test_dry_ice_bath_in_cooling_category():
    from orgchem.core.lab_equipment import get_equipment
    e = get_equipment("dry_ice_bath")
    assert e.category == "cooling"
    assert "-78" in e.description


def test_bunsen_burner_safety_notes_open_flame_risk():
    from orgchem.core.lab_equipment import get_equipment
    body = get_equipment("bunsen_burner").safety_notes.lower()
    assert "flammable" in body or "flame" in body


def test_keck_clip_size_table_in_variants():
    from orgchem.core.lab_equipment import get_equipment
    body = get_equipment("keck_clip").variants
    # Must mention at least the common 24/29 mapping (#22).
    assert "24/29" in body


# ---- connection-port shape ------------------------------------

def test_every_port_has_required_fields():
    from orgchem.core.lab_equipment import list_equipment
    for e in list_equipment():
        for p in e.connection_ports:
            assert p.name, f"unnamed port on {e.id}"
            assert p.location, f"missing port location on {e.id}"
            assert p.joint_type, f"missing joint_type on {e.id}"
            assert isinstance(p.is_male, bool)


# ---- filter / lookup ------------------------------------------

def test_list_filtered_by_category():
    from orgchem.core.lab_equipment import list_equipment
    glassware = list_equipment(category="glassware")
    assert all(e.category == "glassware" for e in glassware)
    assert len(glassware) >= 4   # rbf + 3neck + erlenmeyer + beaker
    cond = list_equipment(category="condenser")
    assert len(cond) >= 5   # liebig + allihn + graham + friedrichs + dimroth + air


def test_list_unknown_category_returns_empty():
    from orgchem.core.lab_equipment import list_equipment
    assert list_equipment(category="not-a-real-category") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.lab_equipment import get_equipment
    assert get_equipment("does-not-exist") is None


def test_find_equipment_substring_case_insensitive():
    from orgchem.core.lab_equipment import find_equipment
    a = {e.id for e in find_equipment("CONDENSER")}
    b = {e.id for e in find_equipment("condenser")}
    assert a == b
    assert len(a) >= 5    # all 6 condensers should match


def test_find_equipment_empty_returns_empty():
    from orgchem.core.lab_equipment import find_equipment
    assert find_equipment("") == []


# ---- to_dict serialisation ------------------------------------

def test_to_dict_keys_and_ports_serialise():
    from orgchem.core.lab_equipment import get_equipment, to_dict
    d = to_dict(get_equipment("rbf"))
    expected = {
        "id", "name", "category", "description",
        "typical_uses", "variants", "safety_notes",
        "icon_id", "connection_ports",
    }
    assert set(d.keys()) == expected
    # Ports come out as a list of dicts.
    assert isinstance(d["connection_ports"], list)
    for p in d["connection_ports"]:
        assert {"name", "location", "joint_type",
                "is_male"} <= set(p.keys())


# ---- agent actions --------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_equipment(app):
    rows = app.call("list_lab_equipment")
    assert len(rows) >= 35


def test_action_list_equipment_filtered(app):
    rows = app.call("list_lab_equipment", category="condenser")
    assert all(r["category"] == "condenser" for r in rows)
    assert len(rows) >= 5


def test_action_list_equipment_unknown_category_errors(app):
    rows = app.call("list_lab_equipment", category="bogus")
    assert len(rows) == 1
    assert "error" in rows[0]


def test_action_get_equipment(app):
    r = app.call("get_lab_equipment", equipment_id="rbf")
    assert "error" not in r
    assert r["category"] == "glassware"
    assert r["name"] == "Round-bottom flask"
    assert r["connection_ports"]


def test_action_get_unknown_equipment(app):
    r = app.call("get_lab_equipment", equipment_id="bogus")
    assert "error" in r


def test_action_find_equipment(app):
    rows = app.call("find_lab_equipment", needle="vacuum")
    ids = {r["id"] for r in rows}
    assert "vacuum_pump" in ids
    assert "vacuum_adapter" in ids
    assert "vacuum_trap" in ids
