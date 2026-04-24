"""Phase 36g round 126 — tests for the *Tools → Drawing tool…* dialog.

The dialog wraps the Phase-36b :class:`DrawingPanel` and adds the
workspace-integration bits (export to PNG/SVG/MOL + send-to-Molecule-
Workspace via the ``add_molecule`` authoring action).  These tests
drive the dialog headlessly, monkey-patching file-save + authoring
calls so we never touch the real DB or disk-prompt UI.
"""
from __future__ import annotations
import os

import pytest
from PySide6.QtCore import QPointF

pytest.importorskip("rdkit")
pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def _reset_singleton():
    """Drop the module-level singleton between tests so each
    test gets a fresh canvas + a fresh panel."""
    from orgchem.gui.dialogs import drawing_tool as mod
    mod.DrawingToolDialog._instance = None
    yield
    mod.DrawingToolDialog._instance = None


# ---- construction + singleton -----------------------------------

def test_dialog_instantiates_with_panel_and_buttons(app, qtbot):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.panel is not None
    assert d.export_btn.isEnabled()
    assert d.send_btn.isEnabled()
    assert not d.isModal()


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    a = DrawingToolDialog.singleton(parent=app.window)
    b = DrawingToolDialog.singleton(parent=app.window)
    assert a is b


def test_singleton_preserves_canvas_across_reopens(app):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    d = DrawingToolDialog.singleton(parent=app.window)
    d.panel.handle_canvas_press(QPointF(0, 0))
    assert d.panel.current_smiles() == "C"
    d2 = DrawingToolDialog.singleton(parent=app.window)
    # Same instance → same structure.
    assert d2 is d
    assert d2.panel.current_smiles() == "C"


def test_seed_smiles_loads_structure(app):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from rdkit import Chem
    d = DrawingToolDialog.singleton(
        parent=app.window, seed_smiles="c1ccccc1")
    s = d.panel.get_structure()
    assert s.n_atoms == 6 and s.n_bonds == 6
    assert Chem.CanonSmiles(d.panel.current_smiles()) == \
           Chem.CanonSmiles("c1ccccc1")


# ---- export path ------------------------------------------------

def test_export_warns_when_canvas_empty(app, qtbot, monkeypatch):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from PySide6.QtWidgets import QMessageBox, QFileDialog
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    messages = []
    monkeypatch.setattr(
        QMessageBox, "information",
        lambda *a, **k: messages.append(a))
    called = {"saveFile": False}

    def _no_save(*a, **k):
        called["saveFile"] = True
        return ("", "")

    monkeypatch.setattr(QFileDialog, "getSaveFileName", _no_save)
    d._on_export()
    assert messages, "expected info dialog when canvas is empty"
    assert not called["saveFile"], \
        "file dialog must not open for empty canvas"


def test_export_mol_writes_v2000_block(app, qtbot, monkeypatch, tmp_path):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from PySide6.QtWidgets import QFileDialog
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    d.panel.set_structure_from_smiles("CCO")

    out = tmp_path / "drawing.mol"
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName",
        lambda *a, **k: (str(out), "MOL V2000 (*.mol)"))
    d._on_export()
    assert out.exists()
    text = out.read_text()
    # V2000 mol-block canonical tokens.
    assert "V2000" in text
    assert "M  END" in text


def test_export_png_writes_image(app, qtbot, monkeypatch, tmp_path):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from PySide6.QtWidgets import QFileDialog
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    d.panel.set_structure_from_smiles("CCO")

    out = tmp_path / "drawing.png"
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName",
        lambda *a, **k: (str(out), "PNG image (*.png)"))
    d._on_export()
    assert out.exists() and out.stat().st_size > 0


# ---- send-to-workspace path -------------------------------------

def test_send_to_workspace_warns_when_empty(app, qtbot, monkeypatch):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from PySide6.QtWidgets import QMessageBox
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    messages = []
    monkeypatch.setattr(
        QMessageBox, "information",
        lambda *a, **k: messages.append(a))
    d._on_send_to_workspace()
    assert messages, "expected info dialog when canvas is empty"


def test_send_to_workspace_invokes_add_molecule(
        app, qtbot, monkeypatch):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from PySide6.QtWidgets import QMessageBox
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    d.panel.set_structure_from_smiles("CCO")

    invocations = []

    def _fake_invoke(name, **kw):
        invocations.append((name, kw))
        return {"status": "accepted", "id": 4242}

    import orgchem.agent.actions as actions_mod
    monkeypatch.setattr(actions_mod, "invoke", _fake_invoke)
    # Silence the success info box.
    monkeypatch.setattr(QMessageBox, "information",
                        lambda *a, **k: None)

    selected = []
    monkeypatch.setattr(
        d, "_select_molecule",
        lambda mid: selected.append(mid))

    d._on_send_to_workspace()
    assert invocations, "expected add_molecule invocation"
    name, kw = invocations[0]
    assert name == "add_molecule"
    assert kw["smiles"] == "CCO"
    assert kw["mol_name"].startswith("Drawn-")
    assert kw["source_tags"] == ["drawn"]
    assert selected == [4242]


def test_send_to_workspace_handles_duplicate(
        app, qtbot, monkeypatch):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from PySide6.QtWidgets import QMessageBox
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    d.panel.set_structure_from_smiles("CCO")

    import orgchem.agent.actions as actions_mod
    monkeypatch.setattr(
        actions_mod, "invoke",
        lambda *a, **k: {
            "status": "rejected",
            "reason": "duplicate InChIKey",
            "existing_id": 17,
        })
    monkeypatch.setattr(QMessageBox, "information",
                        lambda *a, **k: None)
    selected = []
    monkeypatch.setattr(
        d, "_select_molecule",
        lambda mid: selected.append(mid))

    d._on_send_to_workspace()
    # Duplicate path should still select the existing row.
    assert selected == [17]


def test_send_to_workspace_surfaces_invocation_error(
        app, qtbot, monkeypatch):
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    from PySide6.QtWidgets import QMessageBox
    d = DrawingToolDialog(parent=app.window)
    qtbot.addWidget(d)
    d.panel.set_structure_from_smiles("CCO")

    import orgchem.agent.actions as actions_mod

    def _boom(*a, **k):
        raise RuntimeError("DB offline")

    monkeypatch.setattr(actions_mod, "invoke", _boom)
    warnings = []
    monkeypatch.setattr(
        QMessageBox, "warning",
        lambda *a, **k: warnings.append(a))
    d._on_send_to_workspace()
    assert warnings, "expected warning dialog when invoke raises"
