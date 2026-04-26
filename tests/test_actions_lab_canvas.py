"""Phase 38c.5 (round 190) — agent actions for the lab-setup
canvas.

Tests the 5 actions in the new ``lab-canvas`` category +
verifies the *Build on canvas* integration on the Phase-38b
setup dialog.  Closes Phase 38c.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")
pytest.importorskip("PySide6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="module")
def app():
    """Full HeadlessApp — needed because the agent actions all
    go through `controller.main_window()` and dispatch onto the
    Qt main thread."""
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
    LabSetupCanvasDialog._instance = None


# ==================================================================
# Registration
# ==================================================================

def test_actions_registered(app):
    """All 5 actions are in the registry under ``lab-canvas``."""
    from orgchem.agent.actions import registry
    expected = {
        "open_lab_setup_canvas",
        "place_equipment_on_canvas",
        "connect_canvas_equipment",
        "clear_lab_setup_canvas",
        "lab_setup_canvas_state",
    }
    r = registry()
    for n in expected:
        assert n in r, f"action {n} not registered"
        assert r[n].category == "lab-canvas", \
            f"{n} category != 'lab-canvas'"


# ==================================================================
# open_lab_setup_canvas
# ==================================================================

def test_open_canvas_no_setup(app):
    """Opening with no setup id just shows the empty dialog."""
    res = app.call("open_lab_setup_canvas")
    assert res["opened"] is True
    assert res["populated"] is False


def test_open_canvas_with_setup_populates(app):
    """Opening with a setup id pre-populates the canvas with
    that setup's equipment + connections."""
    res = app.call(
        "open_lab_setup_canvas", setup_id="simple_distillation")
    assert res["opened"] is True
    assert res["populated"] is True


def test_open_canvas_unknown_setup_id(app):
    """Unknown setup id opens the dialog but reports populated
    = False (graceful fallback, not an error)."""
    res = app.call(
        "open_lab_setup_canvas", setup_id="not-a-real-setup")
    assert res["opened"] is True
    assert res["populated"] is False


# ==================================================================
# place_equipment_on_canvas
# ==================================================================

def test_place_equipment_requires_open_dialog(app):
    """`place_equipment_on_canvas` errors if the dialog isn't
    open yet."""
    res = app.call(
        "place_equipment_on_canvas",
        equipment_id="rbf", x=200, y=200,
    )
    assert "error" in res
    assert "open_lab_setup_canvas" in res["error"]


def test_place_equipment_happy_path(app):
    """After opening the dialog, place_equipment lands a glyph."""
    app.call("open_lab_setup_canvas")
    res = app.call(
        "place_equipment_on_canvas",
        equipment_id="rbf", x=100, y=150,
    )
    assert res.get("placed") is True
    assert res["equipment_id"] == "rbf"
    assert res["x"] == 100.0
    assert res["y"] == 150.0
    assert res["total_items"] >= 1


def test_place_equipment_unknown_id(app):
    app.call("open_lab_setup_canvas")
    res = app.call(
        "place_equipment_on_canvas",
        equipment_id="not-real", x=0, y=0,
    )
    assert "error" in res


# ==================================================================
# connect_canvas_equipment
# ==================================================================

def test_connect_canvas_equipment_valid_pair(app):
    """Two compatible glyphs (rbf female × distillation_head male)
    connect cleanly; valid=True, error_message=''."""
    app.call("open_lab_setup_canvas")
    app.call("place_equipment_on_canvas",
             equipment_id="rbf", x=100, y=100)
    app.call("place_equipment_on_canvas",
             equipment_id="distillation_head", x=300, y=100)
    res = app.call(
        "connect_canvas_equipment",
        equipment_a_id="rbf", port_a="neck",
        equipment_b_id="distillation_head", port_b="bottom",
    )
    assert res.get("connected") is True
    assert res["valid"] is True
    assert res["error_message"] == ""


def test_connect_canvas_equipment_mismatched_pair(app):
    """A two-female-joints pair connects but reports valid=False
    + a port-sex error message."""
    app.call("open_lab_setup_canvas")
    app.call("place_equipment_on_canvas",
             equipment_id="rbf", x=100, y=100)
    app.call("place_equipment_on_canvas",
             equipment_id="rbf", x=300, y=100)
    res = app.call(
        "connect_canvas_equipment",
        equipment_a_id="rbf", port_a="neck",
        equipment_b_id="rbf", port_b="neck",
    )
    assert res["connected"] is True
    assert res["valid"] is False
    assert res["error_message"]


def test_connect_canvas_equipment_glyph_not_present(app):
    """Trying to connect an equipment id that hasn't been placed
    errors (not raises)."""
    app.call("open_lab_setup_canvas")
    res = app.call(
        "connect_canvas_equipment",
        equipment_a_id="rbf", port_a="neck",
        equipment_b_id="beaker", port_b="lip",
    )
    assert "error" in res


# ==================================================================
# clear_lab_setup_canvas
# ==================================================================

def test_clear_canvas_drops_everything(app):
    app.call("open_lab_setup_canvas")
    app.call("place_equipment_on_canvas",
             equipment_id="rbf", x=0, y=0)
    res = app.call("clear_lab_setup_canvas")
    assert res.get("cleared") is True
    state = app.call("lab_setup_canvas_state")
    assert state["glyphs"] == []
    assert state["connections"] == []


# ==================================================================
# lab_setup_canvas_state
# ==================================================================

def test_state_dump_after_populate(app):
    """A canvas built from a seeded setup serialises every
    glyph + every connection."""
    res = app.call(
        "open_lab_setup_canvas", setup_id="simple_distillation")
    assert res["populated"] is True
    state = app.call("lab_setup_canvas_state")
    assert len(state["glyphs"]) >= 4
    assert len(state["connections"]) >= 1
    # Each glyph carries equipment_id + label + x + y.
    sample = state["glyphs"][0]
    assert "equipment_id" in sample
    assert "label" in sample
    assert "x" in sample and "y" in sample
    # Each connection carries port pair + validity + error.
    if state["connections"]:
        c = state["connections"][0]
        assert "equipment_a" in c and "equipment_b" in c
        assert "port_a" in c and "port_b" in c
        assert "valid" in c and "error" in c


def test_state_dump_when_dialog_not_open(app):
    """Calling state when the dialog isn't open errors."""
    res = app.call("lab_setup_canvas_state")
    assert "error" in res


# ==================================================================
# Phase 38c.5 — populate_from_setup helper
# ==================================================================

def test_populate_from_setup_clears_prior_state(app):
    """`populate_from_setup` wipes any prior canvas content
    before placing the seeded setup's equipment."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    app.call("open_lab_setup_canvas")
    app.call("place_equipment_on_canvas",
             equipment_id="rbf", x=500, y=500)
    dlg = LabSetupCanvasDialog._instance
    assert len(dlg.canvas().equipment_glyphs()) == 1
    ok = dlg.populate_from_setup("simple_distillation")
    assert ok is True
    glyphs = dlg.canvas().equipment_glyphs()
    # The lone "rbf" placed above should be gone (not at 500/500).
    assert all(g.scenePos().x() != 500 or g.scenePos().y() != 500
               for g in glyphs)


def test_populate_from_setup_unknown_returns_false(app):
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    app.call("open_lab_setup_canvas")
    dlg = LabSetupCanvasDialog._instance
    assert dlg.populate_from_setup("not-a-real-setup") is False


# ==================================================================
# Phase 38c.5 — LabSetupsDialog "Build on canvas" button
# ==================================================================

def test_build_on_canvas_button_exists(app):
    """The Phase-38b *Lab setups…* dialog gained a *Build on
    canvas* button.  The dialog auto-selects the first setup
    on construction so the button is enabled by default; it
    only disables when no setup is in focus."""
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    LabSetupsDialog._instance = None
    dlg = LabSetupsDialog()
    assert hasattr(dlg, "_build_btn")
    # Force the no-setup state via the public _show_blank slot.
    dlg._show_blank("test")
    assert dlg._build_btn.isEnabled() is False
    # Re-show a setup → button enables.  Calling `_show_setup`
    # directly bypasses the QListWidget signal plumbing in the
    # offscreen-Qt test environment (which doesn't fire
    # `currentRowChanged` reliably for `setCurrentRow(0)` no-ops).
    from orgchem.core.lab_setups import get_setup
    dlg._show_setup(get_setup("simple_distillation"))
    assert dlg._build_btn.isEnabled() is True
    dlg.deleteLater()
    LabSetupsDialog._instance = None


def test_build_on_canvas_button_triggers_canvas_populate(app):
    """Clicking *Build on canvas* opens the canvas dialog +
    populates it with the displayed setup."""
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    LabSetupsDialog._instance = None
    dlg = LabSetupsDialog()
    # Manually display a setup so the button enables.
    dlg.select_setup("simple_distillation")
    assert dlg._build_btn.isEnabled() is True
    dlg._on_build_on_canvas()
    canvas = LabSetupCanvasDialog._instance
    assert canvas is not None
    assert len(canvas.canvas().equipment_glyphs()) >= 4
    dlg.deleteLater()
    LabSetupsDialog._instance = None
