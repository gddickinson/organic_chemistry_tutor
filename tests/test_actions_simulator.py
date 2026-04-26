"""Phase 38d.4 (round 194) — agent actions for the process
simulator.

Tests the 7 agent actions in the new ``simulator`` category +
verifies the 3 round-194 setup scripts (Soxhlet / liquid-liquid /
reflux-with-addition) are now available.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")
pytest.importorskip("PySide6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="module")
def app():
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def reset_canvas_dialog(app):
    """Reset the singleton between tests so they don't bleed."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    LabSetupCanvasDialog._instance = None
    yield
    # Pause any running timer to avoid leaking into the next test.
    if LabSetupCanvasDialog._instance is not None:
        LabSetupCanvasDialog._instance.simulation_dock().pause()
    LabSetupCanvasDialog._instance = None


# ==================================================================
# Registration
# ==================================================================

def test_simulator_actions_registered(app):
    """All 7 actions are in the registry under ``simulator``."""
    from orgchem.agent.actions import registry
    expected = {
        "start_process_simulation",
        "simulator_state",
        "simulator_step",
        "simulator_reset",
        "simulator_play",
        "simulator_pause",
        "set_simulator_speed",
    }
    r = registry()
    for n in expected:
        assert n in r, f"action {n} not registered"
        assert r[n].category == "simulator"


# ==================================================================
# Phase 38d.4 — 3 new setup scripts
# ==================================================================

def test_all_eight_phase_38b_setups_have_scripts():
    from orgchem.core.process_simulator import available_setups
    from orgchem.core.lab_setups import list_setups
    setups = {s.id for s in list_setups()}
    scripts = set(available_setups())
    assert setups == scripts, (
        f"setups without scripts: {setups - scripts}"
    )


def test_soxhlet_script_well_formed():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("soxhlet_extraction")
    assert sim is not None
    ids = {s.id for s in sim.stages}
    assert "siphon" in ids   # canonical Soxhlet step


def test_liquid_liquid_script_well_formed():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("liquid_liquid_extraction")
    assert sim is not None
    ids = {s.id for s in sim.stages}
    # Venting + settling are canonical L/L steps.
    assert "invert" in ids
    assert "settle" in ids


def test_reflux_with_addition_script_well_formed():
    from orgchem.core.process_simulator import simulator_for_setup
    sim = simulator_for_setup("reflux_with_addition")
    assert sim is not None
    ids = {s.id for s in sim.stages}
    assert "dropwise" in ids   # the defining feature


# ==================================================================
# start_process_simulation
# ==================================================================

def test_start_simulation_happy_path(app):
    res = app.call(
        "start_process_simulation",
        setup_id="simple_distillation",
    )
    assert res.get("started") is True
    assert res["setup_id"] == "simple_distillation"
    assert res["total_stages"] >= 5


def test_start_simulation_unknown_setup(app):
    res = app.call(
        "start_process_simulation",
        setup_id="not-a-real-setup",
    )
    assert "error" in res


# ==================================================================
# simulator_state
# ==================================================================

def test_simulator_state_when_no_dialog_yet(app):
    """Before the dialog is opened the state reports
    ``loaded: False`` rather than erroring."""
    res = app.call("simulator_state")
    assert res.get("loaded") is False


def test_simulator_state_after_start(app):
    app.call(
        "start_process_simulation",
        setup_id="vacuum_filtration",
    )
    res = app.call("simulator_state")
    assert res["loaded"] is True
    assert res["setup_id"] == "vacuum_filtration"
    assert res["total_stages"] >= 4
    assert res["current_index"] == 0
    assert res["is_complete"] is False
    assert "current_stage" in res
    assert res["current_stage"]["id"]
    assert res["current_stage"]["label"]
    assert res["current_stage"]["description"]
    assert "is_playing" in res
    assert "progress" in res
    assert res["speed"] == 1.0


# ==================================================================
# Playback controls (step / reset / play / pause)
# ==================================================================

def test_simulator_step_advances(app):
    app.call("start_process_simulation",
             setup_id="recrystallisation")
    app.call("simulator_pause")   # avoid timer interference
    app.call("simulator_reset")
    res = app.call("simulator_step")
    assert res.get("stepped") is True
    state = app.call("simulator_state")
    assert state["current_index"] == 1


def test_simulator_step_no_simulator(app):
    """Calling step before start returns an error."""
    res = app.call("simulator_step")
    assert "error" in res


def test_simulator_reset_goes_back_to_zero(app):
    app.call("start_process_simulation", setup_id="reflux")
    app.call("simulator_pause")
    app.call("simulator_step")
    app.call("simulator_step")
    app.call("simulator_reset")
    state = app.call("simulator_state")
    assert state["current_index"] == 0


def test_simulator_play_pause_toggle(app):
    app.call("start_process_simulation", setup_id="reflux")
    app.call("simulator_pause")
    play_res = app.call("simulator_play")
    assert play_res["playing"] is True
    pause_res = app.call("simulator_pause")
    assert pause_res["playing"] is False


# ==================================================================
# set_simulator_speed
# ==================================================================

def test_set_speed_within_bounds(app):
    app.call("start_process_simulation", setup_id="reflux")
    app.call("simulator_pause")
    res = app.call("set_simulator_speed", speed=2.5)
    assert res["speed"] == 2.5
    state = app.call("simulator_state")
    assert state["speed"] == 2.5


def test_set_speed_clamps(app):
    app.call("start_process_simulation", setup_id="reflux")
    app.call("simulator_pause")
    # Below floor → clamps to 0.5.
    res = app.call("set_simulator_speed", speed=0.1)
    assert res["speed"] == 0.5
    # Above ceiling → clamps to 4.0.
    res = app.call("set_simulator_speed", speed=10.0)
    assert res["speed"] == 4.0
