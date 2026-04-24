"""Phase 36b round 125 — tests for the drawing canvas widget.

Drives the widget headlessly via pytest-qt — click + drag
events simulated directly rather than through the QGraphicsView
event pipeline.
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


# ---- tool bookkeeping -----------------------------------------

def test_drawing_panel_starts_empty_with_carbon_tool(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    assert panel.tool() == "atom-C"
    assert panel.current_smiles() == ""
    assert panel.get_structure().is_empty


def test_set_tool_updates_button_state(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("atom-N")
    assert panel.tool() == "atom-N"
    assert panel._tool_buttons["atom-N"].isChecked()
    assert not panel._tool_buttons["atom-C"].isChecked()


# ---- atom placement -------------------------------------------

def test_click_places_carbon(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().n_atoms == 1
    assert panel.get_structure().atoms[0].element == "C"
    assert panel.current_smiles() == "C"


def test_click_with_atom_tool_changes_element(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().atoms[0].element == "C"
    panel.set_tool("atom-N")
    # Click near the existing atom.
    panel.handle_canvas_press(QPointF(2, 0))
    assert panel.get_structure().atoms[0].element == "N"


# ---- bond drawing ---------------------------------------------

def test_bond_tool_connects_two_atoms(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().n_atoms == 2
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    s = panel.get_structure()
    assert s.n_bonds == 1
    assert {s.bonds[0].begin_idx, s.bonds[0].end_idx} == {0, 1}
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("CC")


def test_bond_tool_cycles_order_on_repeat_clicks(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # 1st bond → single.
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().bonds[0].order == 1
    # 2nd cycle → double.
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().bonds[0].order == 2
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("C=C")
    # 3rd cycle → triple.
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().bonds[0].order == 3
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("C#C")


def test_bond_tool_auto_places_endpoints(_app, qtbot):
    """Clicking empty canvas with the bond tool should place a
    carbon at each end — matches ChemDraw's default behaviour."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    s = panel.get_structure()
    assert s.n_atoms == 2 and s.n_bonds == 1
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("CC")


# ---- erase tool -----------------------------------------------

def test_erase_deletes_atom_and_its_bonds(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.handle_canvas_press(QPointF(60, 0))   # C-C-C chain
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.handle_canvas_press(QPointF(60, 0))
    assert panel.get_structure().n_bonds == 2
    panel.set_tool("erase")
    # Erase middle atom — both bonds should vanish.
    panel.handle_canvas_press(QPointF(20, 0))
    s = panel.get_structure()
    assert s.n_atoms == 2
    assert s.n_bonds == 0


def test_erase_reindexes_remaining_bonds(_app, qtbot):
    """Deleting an atom in the middle of a longer chain must
    re-index every higher-numbered atom reference in the bond
    list so RDKit doesn't crash."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # Build C0-C1-C2-C3 linear chain.
    for x in (-30, 0, 30, 60):
        panel.handle_canvas_press(QPointF(x, 0))
    panel.set_tool("bond")
    for i in range(3):
        x0, x1 = (-30 + 30 * i, 0 + 30 * i)
        panel.handle_canvas_press(QPointF(x0, 0))
        panel.handle_canvas_press(QPointF(x1, 0))
    panel.set_tool("erase")
    panel.handle_canvas_press(QPointF(0, 0))   # wipe atom #1
    s = panel.get_structure()
    assert s.n_atoms == 3
    # Remaining bond should still reference valid atom indices.
    for b in s.bonds:
        assert 0 <= b.begin_idx < s.n_atoms
        assert 0 <= b.end_idx < s.n_atoms
    # SMILES must round-trip without crashing.
    assert Chem.MolFromSmiles(panel.current_smiles() or "X") is not None


# ---- SMILES ribbon --------------------------------------------

def test_smiles_entry_builds_canvas(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel._smiles_edit.setText("c1ccccc1")
    panel._on_smiles_entered()
    s = panel.get_structure()
    assert s.n_atoms == 6
    assert s.n_bonds == 6
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("c1ccccc1")


def test_smiles_entry_rejects_garbage(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel._smiles_edit.setText("!!not a smiles!!")
    panel._on_smiles_entered()
    assert panel.get_structure().is_empty


# ---- structure_changed signal + clear --------------------------

def test_structure_changed_signal_fires_on_add(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    received = []
    panel.structure_changed.connect(lambda smi: received.append(smi))
    panel.handle_canvas_press(QPointF(0, 0))
    assert received == ["C"]
    panel.set_tool("atom-O")
    panel.handle_canvas_press(QPointF(40, 0))
    assert received[-1] in ("C.O", "O.C")


def test_clear_empties_structure_and_fires_signal(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().n_atoms == 1
    received = []
    panel.structure_changed.connect(lambda smi: received.append(smi))
    panel.clear()
    assert panel.get_structure().is_empty
    assert received == [""]
