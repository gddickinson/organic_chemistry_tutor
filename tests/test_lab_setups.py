"""Phase 38b (round 141) — headless tests for the lab-setup
catalogue + validator + agent actions.
"""
from __future__ import annotations
import os

import pytest


# ---- catalogue contents ---------------------------------------

def test_catalogue_size_at_least_eight():
    from orgchem.core.lab_setups import list_setups
    assert len(list_setups()) >= 8


def test_canonical_setups_present():
    from orgchem.core.lab_setups import get_setup
    for must in ("simple_distillation", "fractional_distillation",
                 "reflux", "reflux_with_addition",
                 "soxhlet_extraction", "vacuum_filtration",
                 "liquid_liquid_extraction",
                 "recrystallisation"):
        assert get_setup(must) is not None, \
            f"missing setup {must}"


def test_every_setup_has_required_fields():
    from orgchem.core.lab_setups import list_setups
    for s in list_setups():
        assert s.id, f"missing id"
        assert s.name, f"missing name on {s.id}"
        assert s.purpose, f"missing purpose on {s.id}"
        assert s.equipment, f"empty equipment on {s.id}"
        assert s.procedure, f"missing procedure on {s.id}"


def test_every_setup_id_unique():
    from orgchem.core.lab_setups import list_setups
    ids = [s.id for s in list_setups()]
    assert len(ids) == len(set(ids)), "duplicate id"


# ---- validation ------------------------------------------------

def test_every_seeded_setup_validates_clean():
    """The headline regression test: every catalogued setup
    must validate against the Phase-38a equipment / port
    catalogue with zero errors.  Catches port-renames,
    sex-mismatch typos, and equipment-id typos at test time
    rather than at canvas-build time."""
    from orgchem.core.lab_setups import list_setups, validate_setup
    failures = []
    for s in list_setups():
        errs = validate_setup(s)
        if errs:
            failures.append((s.id, errs))
    assert not failures, \
        f"setups failed validation: {failures}"


def test_validator_catches_unknown_equipment_id():
    from orgchem.core.lab_setups import (
        Setup, SetupConnection, validate_setup,
    )
    bad = Setup(
        id="bogus", name="bogus", purpose="bogus",
        equipment=("bogus_equipment_id",),
        connections=(),
    )
    errs = validate_setup(bad)
    assert errs
    assert any("unknown id" in e for e in errs)


def test_validator_catches_out_of_range_index():
    from orgchem.core.lab_setups import (
        Setup, SetupConnection, validate_setup,
    )
    bad = Setup(
        id="bogus", name="bogus", purpose="bogus",
        equipment=("rbf",),
        connections=(SetupConnection(0, "neck", 99, "x"),),
    )
    errs = validate_setup(bad)
    assert any("out of range" in e for e in errs)


def test_validator_catches_self_loop():
    from orgchem.core.lab_setups import (
        Setup, SetupConnection, validate_setup,
    )
    bad = Setup(
        id="bogus", name="bogus", purpose="bogus",
        equipment=("rbf",),
        connections=(SetupConnection(0, "neck", 0, "neck"),),
    )
    errs = validate_setup(bad)
    assert any("self-loop" in e for e in errs)


def test_validator_catches_unknown_port():
    from orgchem.core.lab_setups import (
        Setup, SetupConnection, validate_setup,
    )
    bad = Setup(
        id="bogus", name="bogus", purpose="bogus",
        equipment=("rbf", "rbf"),
        connections=(
            SetupConnection(0, "no_such_port", 1, "neck"),
        ),
    )
    errs = validate_setup(bad)
    assert any("not on" in e for e in errs)


def test_validator_catches_joint_mismatch():
    from orgchem.core.lab_setups import (
        Setup, SetupConnection, validate_setup,
    )
    # rbf neck is 24/29; vacuum_pump vacuum-in is hose.
    bad = Setup(
        id="bogus", name="bogus", purpose="bogus",
        equipment=("rbf", "vacuum_pump"),
        connections=(
            SetupConnection(0, "neck", 1, "vacuum-in"),
        ),
    )
    errs = validate_setup(bad)
    assert any("joint mismatch" in e for e in errs)


def test_validator_catches_port_sex_mismatch():
    from orgchem.core.lab_setups import (
        Setup, SetupConnection, validate_setup,
    )
    # Two RBFs both have female necks.
    bad = Setup(
        id="bogus", name="bogus", purpose="bogus",
        equipment=("rbf", "rbf"),
        connections=(SetupConnection(0, "neck", 1, "neck"),),
    )
    errs = validate_setup(bad)
    assert any("port-sex mismatch" in e for e in errs)


def test_validator_relaxes_on_open_joint_type():
    """Joint type `open` accepts anything (clamp grip,
    hot-plate top, vessel-on-bench)."""
    from orgchem.core.lab_setups import (
        Setup, SetupConnection, validate_setup,
    )
    # erlenmeyer mouth = open; hotplate_stirrer top = open.
    s = Setup(
        id="bogus", name="bogus", purpose="bogus",
        equipment=("erlenmeyer", "hotplate_stirrer"),
        connections=(SetupConnection(0, "mouth", 1, "top"),),
    )
    assert validate_setup(s) == []


# ---- per-setup teaching invariants ----------------------------

def test_simple_distillation_has_pot_and_receiver():
    """Simple distillation must include TWO RBFs (pot +
    receiver) — the canonical teaching configuration."""
    from orgchem.core.lab_setups import get_setup
    s = get_setup("simple_distillation")
    rbf_count = sum(1 for eid in s.equipment if eid == "rbf")
    assert rbf_count >= 2, \
        f"expected ≥2 RBFs, got {rbf_count}"


def test_simple_distillation_includes_thermometer_and_condenser():
    from orgchem.core.lab_setups import get_setup
    s = get_setup("simple_distillation")
    eq_ids = set(s.equipment)
    assert "thermometer" in eq_ids
    assert "liebig_condenser" in eq_ids
    assert "distillation_head" in eq_ids
    assert "vacuum_adapter" in eq_ids


def test_fractional_distillation_adds_vigreux_to_simple():
    from orgchem.core.lab_setups import get_setup
    simple = set(get_setup("simple_distillation").equipment)
    frac = set(get_setup("fractional_distillation").equipment)
    assert "vigreux_column" in frac
    assert "vigreux_column" not in simple
    # Fractional should have everything simple has (super-set).
    assert simple <= frac


def test_reflux_uses_allihn_not_liebig():
    """Reflux pedagogy: Allihn (bulb) > Liebig (straight tube)
    because bulbs increase residence time + vapour recovery
    for sustained reflux."""
    from orgchem.core.lab_setups import get_setup
    s = get_setup("reflux")
    assert "allihn_condenser" in s.equipment
    assert "liebig_condenser" not in s.equipment


def test_soxhlet_includes_extractor_and_condenser():
    from orgchem.core.lab_setups import get_setup
    s = get_setup("soxhlet_extraction")
    assert "soxhlet_extractor" in s.equipment
    assert "allihn_condenser" in s.equipment
    assert "rbf" in s.equipment


def test_vacuum_filtration_includes_buchner_filter_flask_and_trap():
    from orgchem.core.lab_setups import get_setup
    s = get_setup("vacuum_filtration")
    eq_ids = set(s.equipment)
    assert "buchner_funnel" in eq_ids
    assert "filter_flask" in eq_ids
    assert "vacuum_trap" in eq_ids


def test_lle_centers_on_separatory_funnel():
    from orgchem.core.lab_setups import get_setup
    s = get_setup("liquid_liquid_extraction")
    assert "sep_funnel" in s.equipment
    assert "ring_stand" in s.equipment


def test_recrystallisation_has_collection_filtration():
    """Recrystallisation pedagogy includes the collection
    step — Büchner + filter flask + vacuum."""
    from orgchem.core.lab_setups import get_setup
    s = get_setup("recrystallisation")
    eq_ids = set(s.equipment)
    assert "buchner_funnel" in eq_ids
    assert "filter_flask" in eq_ids


# ---- lookup helpers -------------------------------------------

def test_get_unknown_setup_returns_none():
    from orgchem.core.lab_setups import get_setup
    assert get_setup("does-not-exist") is None


def test_find_setups_substring_case_insensitive():
    from orgchem.core.lab_setups import find_setups
    a = {s.id for s in find_setups("DISTILL")}
    b = {s.id for s in find_setups("distill")}
    assert a == b
    assert "simple_distillation" in a
    assert "fractional_distillation" in a


def test_find_setups_empty_returns_empty():
    from orgchem.core.lab_setups import find_setups
    assert find_setups("") == []


# ---- to_dict serialisation ------------------------------------

def test_to_dict_keys_and_connections_serialise():
    from orgchem.core.lab_setups import get_setup, to_dict
    d = to_dict(get_setup("simple_distillation"))
    expected = {
        "id", "name", "purpose", "equipment", "connections",
        "procedure", "safety_notes", "pedagogical_notes",
        "typical_reactions", "icon_id",
    }
    assert set(d.keys()) == expected
    assert isinstance(d["equipment"], list)
    assert isinstance(d["connections"], list)
    for c in d["connections"]:
        assert {"from_equipment_idx", "from_port",
                "to_equipment_idx", "to_port",
                "note"} <= set(c.keys())


# ---- agent actions --------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_action_list_setups(app):
    rows = app.call("list_lab_setups")
    assert len(rows) >= 8
    assert "id" in rows[0]


def test_action_get_setup(app):
    r = app.call("get_lab_setup", setup_id="reflux")
    assert "error" not in r
    assert r["name"] == "Standard reflux"


def test_action_get_unknown_setup(app):
    r = app.call("get_lab_setup", setup_id="bogus")
    assert "error" in r


def test_action_find_setups(app):
    rows = app.call("find_lab_setups", needle="reflux")
    ids = {r["id"] for r in rows}
    assert "reflux" in ids
    assert "reflux_with_addition" in ids


def test_action_validate_setup_clean(app):
    r = app.call("validate_lab_setup", setup_id="simple_distillation")
    assert r["valid"] is True
    assert r["errors"] == []


def test_action_validate_setup_unknown(app):
    r = app.call("validate_lab_setup", setup_id="bogus")
    assert "error" in r
