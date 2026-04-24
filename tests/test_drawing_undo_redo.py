"""Phase 36d round 128 — undo/redo regression tests for `DrawingPanel`.

Covers the snapshot-based undo/redo stack added on top of the
round-125 canvas: every mutation should produce one undo step, and
Ctrl+Z / Ctrl+Shift+Z must round-trip SMILES exactly.
"""
from __future__ import annotations
import os

import pytest
from PySide6.QtCore import QPointF

pytest.importorskip("rdkit")
pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as app:
        yield app


# ---- initial state ---------------------------------------------

def test_undo_stack_empty_on_construction(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    assert not panel.can_undo()
    assert not panel.can_redo()
    assert not panel._undo_btn.isEnabled()
    assert not panel._redo_btn.isEnabled()


def test_undo_noop_on_empty_stack(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.undo()  # must not raise / change anything
    panel.redo()
    assert panel.get_structure().is_empty


# ---- atom placement --------------------------------------------

def test_undo_reverses_atom_placement(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().n_atoms == 1
    assert panel.can_undo()
    panel.undo()
    assert panel.get_structure().n_atoms == 0
    assert panel.current_smiles() == ""
    assert not panel.can_undo()
    assert panel.can_redo()


def test_redo_replays_atom_placement(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel.undo()
    panel.redo()
    assert panel.get_structure().n_atoms == 1
    assert panel.current_smiles() == "C"
    assert not panel.can_redo()


def test_undo_chain_of_atom_placements(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    for x in (0, 40, 80):
        panel.handle_canvas_press(QPointF(x, 0))
    assert panel.get_structure().n_atoms == 3
    panel.undo()
    panel.undo()
    assert panel.get_structure().n_atoms == 1
    panel.undo()
    assert panel.get_structure().n_atoms == 0


# ---- element swap ----------------------------------------------

def test_undo_reverses_element_change(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel.set_tool("atom-N")
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().atoms[0].element == "N"
    panel.undo()
    assert panel.get_structure().atoms[0].element == "C"


def test_same_element_click_is_noop_for_undo(_app, qtbot):
    """Re-clicking the same atom with the same element shouldn't
    pile identical snapshots onto the undo stack."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    depth = len(panel._undo_stack)
    panel.handle_canvas_press(QPointF(0, 0))  # same C, same spot
    assert len(panel._undo_stack) == depth


# ---- bonds -----------------------------------------------------

def test_undo_reverses_bond_creation(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().n_bonds == 1
    panel.undo()
    assert panel.get_structure().n_bonds == 0
    assert panel.get_structure().n_atoms == 2


def test_undo_reverses_bond_order_cycle(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))   # single
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))   # → double
    assert panel.get_structure().bonds[0].order == 2
    panel.undo()
    assert panel.get_structure().bonds[0].order == 1
    # Another undo drops the bond itself.
    panel.undo()
    assert panel.get_structure().n_bonds == 0


def test_bond_tool_cancel_does_not_pollute_undo(_app, qtbot):
    """Clicking the same atom twice with the bond tool is a cancel;
    it must not appear as an undo step."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))    # place atom
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(0, 0))    # first bond click
    depth = len(panel._undo_stack)
    panel.handle_canvas_press(QPointF(0, 0))    # cancel (same atom)
    # No extra undo step.
    assert len(panel._undo_stack) == depth


# ---- erase -----------------------------------------------------

def test_undo_restores_erased_atom_and_bonds(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # C-C-C chain.
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(0, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(0, 0))
    panel.handle_canvas_press(QPointF(0, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    assert panel.get_structure().n_atoms == 3
    assert panel.get_structure().n_bonds == 2
    panel.set_tool("erase")
    panel.handle_canvas_press(QPointF(0, 0))    # erase middle atom
    assert panel.get_structure().n_atoms == 2
    assert panel.get_structure().n_bonds == 0
    panel.undo()
    assert panel.get_structure().n_atoms == 3
    assert panel.get_structure().n_bonds == 2


# ---- clear -----------------------------------------------------

def test_undo_reverses_clear(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel.handle_canvas_press(QPointF(40, 0))
    assert panel.get_structure().n_atoms == 2
    panel.clear()
    assert panel.get_structure().is_empty
    panel.undo()
    assert panel.get_structure().n_atoms == 2


def test_clear_empty_canvas_does_not_push_snapshot(_app, qtbot):
    """Calling clear() on an already-empty canvas is a no-op;
    it shouldn't inflate the undo stack."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    assert not panel.can_undo()
    panel.clear()
    assert not panel.can_undo()


# ---- SMILES rebuild --------------------------------------------

def test_undo_reverses_smiles_rebuild(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().n_atoms == 1
    panel.set_structure_from_smiles("c1ccccc1")
    assert panel.get_structure().n_atoms == 6
    panel.undo()
    assert panel.get_structure().n_atoms == 1
    assert panel.current_smiles() == "C"


# ---- stack management + redo invalidation ----------------------

def test_new_mutation_clears_redo_stack(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel.undo()
    assert panel.can_redo()
    panel.handle_canvas_press(QPointF(40, 0))
    assert not panel.can_redo()


def test_undo_stack_bounded_at_100(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from orgchem.gui.panels.drawing_panel import _UNDO_STACK_MAX
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # Space clicks further apart than `_HIT_RADIUS_PX` so each
    # one lands as a fresh atom rather than re-clicking a prior
    # one (which would be a no-op element-change).
    for i in range(_UNDO_STACK_MAX + 10):
        panel.handle_canvas_press(QPointF(i * 25, 0))
    assert len(panel._undo_stack) == _UNDO_STACK_MAX


# ---- button enabled state --------------------------------------

def test_buttons_reflect_stack_state(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    assert not panel._undo_btn.isEnabled()
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel._undo_btn.isEnabled()
    assert not panel._redo_btn.isEnabled()
    panel.undo()
    assert not panel._undo_btn.isEnabled()
    assert panel._redo_btn.isEnabled()


# ---- full round trip -------------------------------------------

def test_full_build_undo_redo_roundtrip(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # Build C=C.
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))   # single
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))   # double
    smi_after = panel.current_smiles()
    assert Chem.CanonSmiles(smi_after) == Chem.CanonSmiles("C=C")
    # Full unwind.
    while panel.can_undo():
        panel.undo()
    assert panel.get_structure().is_empty
    # Full rewind.
    while panel.can_redo():
        panel.redo()
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("C=C")
