"""Phase 38d.2 (round 193) — process-simulator playback dock.

Tests the Qt UI wired in 38d.2: SimulationDock controls drive
the headless `ProcessSimulator` state machine + the dock
binds correctly to the canvas dialog's *Run simulation* button.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")
pytest.importorskip("PySide6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="module")
def qt_app():
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def dock(qt_app):
    from orgchem.gui.dialogs.lab_simulation_dock import (
        SimulationDock,
    )
    d = SimulationDock()
    yield d
    d.deleteLater()


@pytest.fixture
def canvas_dialog(qt_app):
    """Fresh canvas dialog per test (resets the singleton)."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    LabSetupCanvasDialog._instance = None
    dlg = LabSetupCanvasDialog()
    yield dlg
    LabSetupCanvasDialog._instance = None
    dlg.deleteLater()


# ==================================================================
# SimulationDock — empty / no-simulator state
# ==================================================================

def test_dock_initially_has_no_simulator(dock):
    assert dock.simulator() is None
    # Controls should reflect "nothing to do".
    assert dock._play_btn.isEnabled() is False
    assert dock._step_btn.isEnabled() is False
    assert dock._reset_btn.isEnabled() is False


def test_dock_set_simulator_enables_controls(dock):
    from orgchem.core.process_simulator import (
        simulator_for_setup,
    )
    sim = simulator_for_setup("simple_distillation")
    dock.set_simulator(sim)
    assert dock.simulator() is sim
    assert dock._play_btn.isEnabled() is True
    assert dock._step_btn.isEnabled() is True
    assert dock._reset_btn.isEnabled() is True


def test_dock_clear_simulator_disables_controls(dock):
    from orgchem.core.process_simulator import (
        simulator_for_setup,
    )
    dock.set_simulator(simulator_for_setup("reflux"))
    dock.set_simulator(None)
    assert dock.simulator() is None
    assert dock._play_btn.isEnabled() is False


# ==================================================================
# Manual stepping
# ==================================================================

def test_step_advances_simulator_and_emits_signal(dock):
    from orgchem.core.process_simulator import (
        simulator_for_setup,
    )
    sim = simulator_for_setup("vacuum_filtration")
    dock.set_simulator(sim)
    captured: list = []
    dock.stage_changed.connect(
        lambda sid, idx: captured.append((sid, idx)))
    # First emit fires from set_simulator; clear it.
    captured.clear()
    dock.step()
    assert sim.current_index() == 1
    # stage_changed fired for the new stage.
    assert captured, "no stage_changed signal"
    assert captured[-1][1] == 1


def test_step_to_completion_disables_play(dock):
    from orgchem.core.process_simulator import (
        simulator_for_setup,
    )
    sim = simulator_for_setup("recrystallisation")
    dock.set_simulator(sim)
    finished_calls: list = []
    dock.finished.connect(lambda: finished_calls.append(True))
    while not sim.is_complete():
        dock.step()
    assert sim.is_complete()
    assert dock._play_btn.isEnabled() is False
    assert finished_calls == [True]


def test_reset_returns_simulator_to_start(dock):
    from orgchem.core.process_simulator import (
        simulator_for_setup,
    )
    sim = simulator_for_setup("reflux")
    dock.set_simulator(sim)
    dock.step()
    dock.step()
    assert sim.current_index() == 2
    dock.reset()
    assert sim.current_index() == 0


# ==================================================================
# Speed slider
# ==================================================================

def test_speed_default_is_1x(dock):
    assert dock.speed() == 1.0


def test_speed_slider_updates_speed(dock):
    dock._speed_slider.setValue(200)   # 2.0×
    assert dock.speed() == 2.0
    dock._speed_slider.setValue(50)    # 0.5×
    assert dock.speed() == 0.5


# ==================================================================
# Timer-driven playback (smoke test using a 1-stage script)
# ==================================================================

def test_timer_advances_through_short_stage(dock, qt_app):
    """A simulator with a single 0.05s stage advances after a
    single timer tick at high speed.  Tests the auto-advance
    path without waiting for a real wall-clock second."""
    from PySide6.QtCore import QCoreApplication
    from orgchem.core.process_simulator import (
        ProcessSimulator, Stage,
    )
    sim = ProcessSimulator(
        setup_id="test",
        stages=(
            Stage(id="x", label="X", description="x",
                  duration_seconds=0.05),
            Stage(id="y", label="Y", description="y",
                  duration_seconds=0.05),
        ),
    )
    dock.set_simulator(sim)
    # 4× speed → stage_ms = 12 ms; one 100 ms tick will skip
    # past it.
    dock._speed_slider.setValue(400)
    dock.play()
    dock._on_tick()   # synthetic tick (avoid real-time wait)
    # After a tick that exceeds the stage_ms, the simulator
    # should have advanced.
    assert sim.current_index() >= 1


def test_play_pause_toggle(dock):
    from orgchem.core.process_simulator import (
        simulator_for_setup,
    )
    dock.set_simulator(simulator_for_setup("simple_distillation"))
    assert dock.is_playing() is False
    dock.play()
    assert dock.is_playing() is True
    dock.pause()
    assert dock.is_playing() is False


# ==================================================================
# Canvas-dialog integration
# ==================================================================

def test_canvas_has_simulation_dock(canvas_dialog):
    from orgchem.gui.dialogs.lab_simulation_dock import (
        SimulationDock,
    )
    assert isinstance(canvas_dialog.simulation_dock(),
                      SimulationDock)


def test_run_simulation_button_no_setup_loaded(canvas_dialog):
    """Pressing *Run simulation* with no setup loaded reports
    a friendly message + leaves the dock empty."""
    canvas_dialog._on_run_simulation()
    assert canvas_dialog.simulation_dock().simulator() is None


def test_run_simulation_button_with_loaded_setup(canvas_dialog):
    """After `load_setup`, *Run simulation* binds the simulator
    + auto-plays."""
    canvas_dialog.load_setup("simple_distillation")
    canvas_dialog._on_run_simulation()
    sim = canvas_dialog.simulation_dock().simulator()
    assert sim is not None
    assert sim.setup_id == "simple_distillation"
    assert canvas_dialog.simulation_dock().is_playing() is True
    # Cleanup: pause to avoid timer leaking into the next test.
    canvas_dialog.simulation_dock().pause()


def test_run_simulation_with_unscripted_setup(canvas_dialog):
    """Setups without a script leave the dock empty + show a
    status message.  As of round 194 all 8 Phase-38b setups
    have scripts; this test now uses a fictional unknown id
    via direct `simulator_for_setup`-bypassing path to keep
    the no-script branch exercised."""
    # Force the no-script branch by setting a non-existent
    # setup id in `_loaded_setup_id` directly.
    canvas_dialog._loaded_setup_id = "definitely-not-a-real-setup"
    canvas_dialog._on_run_simulation()
    assert canvas_dialog.simulation_dock().simulator() is None
