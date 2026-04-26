"""Phase 38d.4 (round 194) — agent actions for the process
simulator.

Six actions in the new ``simulator`` category that drive the
Phase-38d.2 SimulationDock from the AI tutor:

- :func:`start_process_simulation(setup_id)` — opens the canvas
  dialog (if needed), loads the setup, binds + starts the
  simulator
- :func:`simulator_state` — JSON snapshot
  (`{loaded, setup_id, total_stages, current_index, current_stage,
  is_complete, is_playing, progress, speed}`)
- :func:`simulator_step` — manual advance one stage
- :func:`simulator_reset` — rewind to stage 0
- :func:`simulator_play` / :func:`simulator_pause` — playback
  controls
- :func:`set_simulator_speed(speed)` — speed adjust (clamped
  0.5 to 4.0)

All actions marshal onto the Qt main thread via
``_gui_dispatch.run_on_main_thread_sync`` and gracefully handle
"main window not available" / "no simulator loaded" /
"unknown setup id" with ``{"error": ...}`` responses.
"""
from __future__ import annotations
from typing import Any, Dict

from orgchem.agent.actions import action


def _get_dialog_and_dock():
    """Return ``(dialog, dock)`` if the canvas dialog has been
    opened this session, else ``(None, None)``."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    dlg = LabSetupCanvasDialog._instance
    if dlg is None:
        return None, None
    return dlg, dlg.simulation_dock()


def _require_main_window() -> Dict[str, Any]:
    from orgchem.agent import controller
    if controller.main_window() is None:
        return {"error": "Main window not available — run the "
                         "app interactively or via HeadlessApp "
                         "first."}
    return {}


def _require_dock() -> Dict[str, Any]:
    """Return ``{}`` + a dock instance, or an error dict."""
    err = _require_main_window()
    if err:
        return {"error": err["error"]}
    _, dock = _get_dialog_and_dock()
    if dock is None:
        return {"error": "Canvas dialog not open — call "
                         "start_process_simulation first."}
    return {"_dock": dock}


@action(category="simulator")
def start_process_simulation(setup_id: str) -> Dict[str, Any]:
    """Open the *Lab setup canvas* dialog, populate it with the
    seeded Phase-38b setup, bind a fresh
    :class:`~core.process_simulator.ProcessSimulator`, and start
    auto-playback.  Returns ``{"started": True, "setup_id":
    ..., "total_stages": <n>}`` or ``{"error": ...}`` for
    unknown setups / setups without a simulator script."""
    err = _require_main_window()
    if err:
        return err
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    from orgchem.core.process_simulator import (
        simulator_for_setup,
    )
    win = controller.main_window()

    def _start() -> Dict[str, Any]:
        from orgchem.gui.dialogs.lab_setup_canvas import (
            LabSetupCanvasDialog,
        )
        dlg = LabSetupCanvasDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        # Populate the canvas from the seeded setup so the
        # student sees the apparatus that's about to run.
        populated = dlg.populate_from_setup(setup_id)
        if not populated:
            return {"error":
                    f"Unknown setup id {setup_id!r}"}
        sim = simulator_for_setup(setup_id)
        if sim is None:
            return {"error":
                    f"No simulator script for {setup_id!r}"}
        dock = dlg.simulation_dock()
        dock.set_simulator(sim)
        dock.play()
        return {
            "started": True,
            "setup_id": setup_id,
            "total_stages": sim.total_stages,
        }

    return run_on_main_thread_sync(_start)


@action(category="simulator")
def simulator_state() -> Dict[str, Any]:
    """Return a JSON snapshot of the currently-loaded
    simulator's state.  Useful for the tutor to introspect
    "where in the process are we right now?"."""
    err = _require_main_window()
    if err:
        return err
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _state() -> Dict[str, Any]:
        _, dock = _get_dialog_and_dock()
        if dock is None:
            return {"loaded": False}
        sim = dock.simulator()
        if sim is None:
            return {"loaded": False}
        stage = sim.current_stage()
        return {
            "loaded": True,
            "setup_id": sim.setup_id,
            "total_stages": sim.total_stages,
            "current_index": sim.current_index(),
            "current_stage": (
                {
                    "id": stage.id,
                    "label": stage.label,
                    "description": stage.description,
                }
                if stage is not None else None
            ),
            "is_complete": sim.is_complete(),
            "is_playing": dock.is_playing(),
            "progress": sim.progress(),
            "speed": dock.speed(),
        }

    return run_on_main_thread_sync(_state)


@action(category="simulator")
def simulator_step() -> Dict[str, Any]:
    """Advance the simulator by one stage (manual step-through
    study mode)."""
    res = _require_dock()
    if "error" in res:
        return res
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _step() -> Dict[str, Any]:
        dock = res["_dock"]
        if dock.simulator() is None:
            return {"error": "No simulator loaded — call "
                             "start_process_simulation first."}
        dock.step()
        return {"stepped": True,
                "current_index":
                    dock.simulator().current_index()}

    return run_on_main_thread_sync(_step)


@action(category="simulator")
def simulator_reset() -> Dict[str, Any]:
    """Rewind the simulator to stage 0."""
    res = _require_dock()
    if "error" in res:
        return res
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _reset() -> Dict[str, Any]:
        dock = res["_dock"]
        if dock.simulator() is None:
            return {"error": "No simulator loaded."}
        dock.reset()
        return {"reset": True}

    return run_on_main_thread_sync(_reset)


@action(category="simulator")
def simulator_play() -> Dict[str, Any]:
    """Resume timer-driven auto-playback."""
    res = _require_dock()
    if "error" in res:
        return res
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _play() -> Dict[str, Any]:
        dock = res["_dock"]
        if dock.simulator() is None:
            return {"error": "No simulator loaded."}
        dock.play()
        return {"playing": dock.is_playing()}

    return run_on_main_thread_sync(_play)


@action(category="simulator")
def simulator_pause() -> Dict[str, Any]:
    """Pause timer-driven auto-playback."""
    res = _require_dock()
    if "error" in res:
        return res
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _pause() -> Dict[str, Any]:
        dock = res["_dock"]
        dock.pause()
        return {"playing": dock.is_playing()}

    return run_on_main_thread_sync(_pause)


@action(category="simulator")
def set_simulator_speed(speed: float = 1.0) -> Dict[str, Any]:
    """Set the playback speed multiplier.  Clamped to [0.5, 4.0].
    Returns the actually-applied value."""
    res = _require_dock()
    if "error" in res:
        return res
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _set() -> Dict[str, Any]:
        dock = res["_dock"]
        # The slider is configured for 50 - 400 (= 0.5× to 4×).
        clamped = max(0.5, min(4.0, float(speed)))
        dock._speed_slider.setValue(int(clamped * 100))
        return {"speed": dock.speed()}

    return run_on_main_thread_sync(_set)
