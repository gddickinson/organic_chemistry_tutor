"""Phase 38d.1 (round 192) — process-simulator state machine.

Locks in the headless data + state-machine layer for the
upcoming Phase-38d.2 canvas-animation work.
"""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# ==================================================================
# Stage dataclass
# ==================================================================

def test_stage_is_immutable():
    """``Stage`` is a frozen dataclass — safe to share between
    simulator instances."""
    from orgchem.core.process_simulator import Stage
    s = Stage(id="x", label="X", description="…")
    with pytest.raises(Exception):
        s.id = "y"   # frozen


def test_stage_has_default_duration_and_parameters():
    from orgchem.core.process_simulator import Stage
    s = Stage(id="x", label="X", description="…")
    assert s.duration_seconds > 0
    assert isinstance(s.parameters, dict)
    assert s.parameters == {}


# ==================================================================
# ProcessSimulator state machine
# ==================================================================

def test_simulator_starts_at_first_stage():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("simple_distillation")
    assert sim is not None
    assert sim.current_index() == 0
    assert sim.current_stage() is not None
    assert sim.current_stage().id == "charge"
    assert sim.is_complete() is False


def test_simulator_advance_steps_through_stages():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("simple_distillation")
    n = sim.total_stages
    for i in range(n):
        assert sim.advance() is True
    # After n advances we're past the end → complete.
    assert sim.is_complete() is True
    assert sim.current_stage() is None
    # Further advances are no-ops.
    assert sim.advance() is False


def test_simulator_reset_returns_to_start():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("reflux")
    sim.advance()
    sim.advance()
    assert sim.current_index() == 2
    sim.reset()
    assert sim.current_index() == 0
    assert sim.is_complete() is False


def test_simulator_jump_to_named_stage():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("simple_distillation")
    assert sim.jump_to("condense") is True
    assert sim.current_stage().id == "condense"
    # Unknown id returns False, doesn't move.
    before = sim.current_index()
    assert sim.jump_to("not-a-real-stage") is False
    assert sim.current_index() == before


def test_simulator_progress_is_bounded():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("vacuum_filtration")
    assert sim.progress() == 0.0
    while not sim.is_complete():
        sim.advance()
    assert sim.progress() == 1.0


def test_empty_script_simulator_is_immediately_complete():
    from orgchem.core.process_simulator import ProcessSimulator
    sim = ProcessSimulator(setup_id="x", stages=())
    assert sim.is_complete() is True
    assert sim.current_stage() is None
    assert sim.progress() == 0.0


# ==================================================================
# Lookup
# ==================================================================

def test_simulator_for_unknown_setup_returns_none():
    from orgchem.core.process_simulator import simulator_for_setup
    assert simulator_for_setup("not-a-real-setup") is None


def test_available_setups_lists_seeded_scripts():
    """At least 5 of the 8 Phase-38b setups have a simulator
    script (the rest are added in 38d.2 follow-ups)."""
    from orgchem.core.process_simulator import available_setups
    setups = available_setups()
    assert len(setups) >= 5
    # Sanity: well-known names are present.
    for sid in ("simple_distillation", "reflux",
                "vacuum_filtration"):
        assert sid in setups


def test_each_seeded_script_has_well_formed_stages():
    """Every shipped simulator has ≥ 3 stages, each with
    non-empty id / label / description."""
    from orgchem.core.process_simulator import (
        available_setups, simulator_for_setup,
    )
    for sid in available_setups():
        sim = simulator_for_setup(sid)
        assert sim is not None
        assert sim.total_stages >= 3, \
            f"setup {sid} has only {sim.total_stages} stages"
        ids: set = set()
        for s in sim.stages:
            assert s.id, f"empty stage id in {sid}"
            assert s.label, f"empty label in {sid}.{s.id}"
            assert s.description, \
                f"empty description in {sid}.{s.id}"
            assert s.duration_seconds > 0, \
                f"non-positive duration in {sid}.{s.id}"
            assert s.id not in ids, \
                f"duplicate stage id {s.id!r} in {sid}"
            ids.add(s.id)


def test_fractional_distillation_has_extra_column_stage():
    """Phase-38b fractional distillation is "simple + Vigreux";
    the simulator script reflects this with an extra
    `column-equilibration` stage that simple distillation
    doesn't have."""
    from orgchem.core.process_simulator import simulator_for_setup
    simple = simulator_for_setup("simple_distillation")
    frac = simulator_for_setup("fractional_distillation")
    simple_ids = {s.id for s in simple.stages}
    frac_ids = {s.id for s in frac.stages}
    assert "column-equilibration" in frac_ids
    assert "column-equilibration" not in simple_ids
    assert frac.total_stages == simple.total_stages + 1


# ==================================================================
# Serialisation
# ==================================================================

def test_stage_to_dict_round_trip():
    from orgchem.core.process_simulator import (
        Stage, stage_to_dict,
    )
    s = Stage(
        id="x", label="X", description="…",
        duration_seconds=2.5, parameters={"a": 1, "b": "z"},
    )
    d = stage_to_dict(s)
    assert d["id"] == "x"
    assert d["label"] == "X"
    assert d["duration_seconds"] == 2.5
    assert d["parameters"] == {"a": 1, "b": "z"}


def test_simulator_to_dict_round_trip():
    from orgchem.core.process_simulator import (
        simulator_for_setup, simulator_to_dict,
    )
    sim = simulator_for_setup("reflux")
    sim.advance()
    d = simulator_to_dict(sim)
    assert d["setup_id"] == "reflux"
    assert d["total_stages"] == sim.total_stages
    assert d["current_index"] == 1
    assert d["is_complete"] is False
    assert isinstance(d["stages"], list)
    assert len(d["stages"]) == sim.total_stages


# ==================================================================
# Headless guarantee
# ==================================================================

def test_no_qt_import():
    """The simulator module is pure-data — must not pull in Qt."""
    import sys
    pre = {m for m in sys.modules if m.startswith("PySide6")}
    import orgchem.core.process_simulator   # noqa: F401
    post = {m for m in sys.modules if m.startswith("PySide6")}
    assert post == pre
