"""Phase 38c.5 (round 190) — agent actions for the lab-setup
canvas.

Closes the multi-round Phase 38c by exposing the canvas to the
LLM-driven agent surface.  Five actions in the new ``lab-canvas``
category:

- :func:`open_lab_setup_canvas` — open the dialog, optionally
  pre-populating with a seeded Phase-38b setup
- :func:`place_equipment_on_canvas` — drop an equipment glyph
  programmatically (no real drag needed)
- :func:`connect_canvas_equipment` — connect two placed glyphs at
  named ports, with the same `validate_port_pair` validation the
  GUI runs
- :func:`clear_lab_setup_canvas` — wipe the canvas
- :func:`lab_setup_canvas_state` — JSON dump for tutor
  introspection

All five actions marshal onto the Qt main thread via
``_gui_dispatch.run_on_main_thread_sync`` and gracefully handle
the "main window not available" / "dialog not open" / "unknown
equipment id" paths with ``{"error": ...}`` responses rather
than raising.
"""
from __future__ import annotations
from typing import Any, Dict, List

from orgchem.agent.actions import action


# ----------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------
def _get_dialog():
    """Return the canvas dialog instance if it's been opened
    this session, or ``None`` (so the caller can return an
    error)."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    return LabSetupCanvasDialog._instance


def _require_main_window() -> Dict[str, Any]:
    """Return ``{}`` if the main window is reachable, else
    a ``{"error": ...}`` dict."""
    from orgchem.agent import controller
    if controller.main_window() is None:
        return {"error": "Main window not available — run the "
                         "app interactively or via HeadlessApp "
                         "first."}
    return {}


# ----------------------------------------------------------------
# Actions
# ----------------------------------------------------------------
@action(category="lab-canvas")
def open_lab_setup_canvas(setup_id: str = "") -> Dict[str, Any]:
    """Open the *Lab setup canvas* dialog.  If ``setup_id`` is
    given, pre-populate the canvas with that seeded Phase-38b
    setup's equipment + connections.  Returns ``{"opened": True,
    "populated": <bool>}`` or ``{"error": ...}``."""
    err = _require_main_window()
    if err:
        return err
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.lab_setup_canvas import (
            LabSetupCanvasDialog,
        )
        dlg = LabSetupCanvasDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        result: Dict[str, Any] = {
            "opened": True, "populated": False,
        }
        sid = (setup_id or "").strip()
        if sid:
            result["populated"] = dlg.populate_from_setup(sid)
        return result

    return run_on_main_thread_sync(_open)


@action(category="lab-canvas")
def place_equipment_on_canvas(equipment_id: str,
                              x: float = 200.0,
                              y: float = 200.0
                              ) -> Dict[str, Any]:
    """Place an equipment glyph on the canvas at scene
    coordinates ``(x, y)``.  Equivalent to dragging the item
    from the palette + dropping it.  Requires the canvas dialog
    to be open already (call :func:`open_lab_setup_canvas` first
    if needed)."""
    err = _require_main_window()
    if err:
        return err
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _place() -> Dict[str, Any]:
        dlg = _get_dialog()
        if dlg is None:
            return {"error": "Canvas dialog not open — call "
                             "open_lab_setup_canvas first."}
        glyph = dlg.canvas().place_equipment(
            equipment_id, float(x), float(y))
        if glyph is None:
            return {"error":
                    f"Unknown equipment id {equipment_id!r}"}
        return {
            "placed": True,
            "equipment_id": equipment_id,
            "x": float(x), "y": float(y),
            "total_items": dlg.canvas().item_count(),
        }

    return run_on_main_thread_sync(_place)


@action(category="lab-canvas")
def connect_canvas_equipment(equipment_a_id: str,
                             port_a: str,
                             equipment_b_id: str,
                             port_b: str
                             ) -> Dict[str, Any]:
    """Connect two glyphs already placed on the canvas at the
    named ports.  Looks up the **first** glyph carrying each
    equipment id (so for setups that place the same equipment
    twice you should disambiguate via direct GUI interaction).
    Returns ``{"connected": True, "valid": <bool>, "error":
    <str>}`` — ``valid`` reflects whether the port pair passes
    the Phase-38a snap-validation."""
    err = _require_main_window()
    if err:
        return err
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _connect() -> Dict[str, Any]:
        dlg = _get_dialog()
        if dlg is None:
            return {"error": "Canvas dialog not open — call "
                             "open_lab_setup_canvas first."}
        glyphs = dlg.canvas().equipment_glyphs()
        g_a = next((g for g in glyphs
                    if g.equipment_id() == equipment_a_id),
                   None)
        g_b = next((g for g in glyphs
                    if g.equipment_id() == equipment_b_id
                    and g is not g_a),
                   None)
        if g_a is None:
            return {"error":
                    f"No placed glyph for {equipment_a_id!r}"}
        if g_b is None:
            return {"error":
                    f"No second placed glyph for "
                    f"{equipment_b_id!r}"}
        line = dlg.canvas().connect_glyphs(
            g_a, port_a, g_b, port_b)
        if line is None:
            return {"error": "connect_glyphs returned None — "
                             "check equipment ids"}
        return {
            "connected": True,
            "valid": line.is_valid(),
            "error_message": line.error() or "",
            "total_connections":
                len(dlg.canvas().connection_lines()),
        }

    return run_on_main_thread_sync(_connect)


@action(category="lab-canvas")
def clear_lab_setup_canvas() -> Dict[str, Any]:
    """Remove every placed glyph + connection line from the
    canvas."""
    err = _require_main_window()
    if err:
        return err
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _clear() -> Dict[str, Any]:
        dlg = _get_dialog()
        if dlg is None:
            return {"error": "Canvas dialog not open."}
        dlg.canvas().clear_canvas()
        return {"cleared": True}

    return run_on_main_thread_sync(_clear)


@action(category="lab-canvas")
def lab_setup_canvas_state() -> Dict[str, Any]:
    """Return a JSON snapshot of the current canvas — every
    placed glyph (with equipment id + position) and every
    connection (with port pair + validity)."""
    err = _require_main_window()
    if err:
        return err
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    def _state() -> Dict[str, Any]:
        dlg = _get_dialog()
        if dlg is None:
            return {"error": "Canvas dialog not open."}
        glyphs = dlg.canvas().equipment_glyphs()
        lines = dlg.canvas().connection_lines()
        return {
            "glyphs": [
                {
                    "equipment_id": g.equipment_id(),
                    "label": g.label(),
                    "x": float(g.scenePos().x()),
                    "y": float(g.scenePos().y()),
                }
                for g in glyphs
            ],
            "connections": [
                {
                    "equipment_a": ln.equipment_a_id(),
                    "port_a": ln.port_a(),
                    "equipment_b": ln.equipment_b_id(),
                    "port_b": ln.port_b(),
                    "valid": ln.is_valid(),
                    "error": ln.error() or "",
                }
                for ln in lines
            ],
        }

    return run_on_main_thread_sync(_state)
