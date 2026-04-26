"""Phase 36c (round 129) — pytest-qt cases for the template
palette wired into :class:`DrawingPanel`.

Verifies (a) every template tool key has a toolbar button; (b)
clicking with a template tool either places free-standing or
fuses with the clicked atom; (c) template placement participates
in the Phase 36d undo / redo stack as one logical step;
(d) the structure_changed signal fires with the correct SMILES.
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


# ---- toolbar wiring --------------------------------------------

def test_template_buttons_registered(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from orgchem.core.drawing_templates import list_template_names
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    for name in list_template_names():
        key = f"template-{name}"
        assert key in panel._tool_buttons, f"missing button for {name}"


def test_set_template_tool_checks_only_that_button(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("template-benzene")
    assert panel.tool() == "template-benzene"
    assert panel._tool_buttons["template-benzene"].isChecked()
    assert not panel._tool_buttons["template-cooh"].isChecked()
    assert not panel._tool_buttons["atom-C"].isChecked()


# ---- empty-canvas ring placement -------------------------------

def test_benzene_template_on_empty_canvas(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("template-benzene")
    panel.handle_canvas_press(QPointF(0, 0))
    s = panel.get_structure()
    assert s.n_atoms == 6
    assert s.n_bonds == 6
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("c1ccccc1")


def test_cyclohexane_template_on_empty_canvas(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("template-cyclohexane")
    panel.handle_canvas_press(QPointF(0, 0))
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("C1CCCCC1")


# ---- ring fusion onto existing atom ----------------------------

def test_benzene_fuses_onto_existing_carbon(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # Place a single carbon first.
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().n_atoms == 1
    # Switch to benzene template and click the carbon — fuses.
    panel.set_tool("template-benzene")
    panel.handle_canvas_press(QPointF(0, 0))
    s = panel.get_structure()
    assert s.n_atoms == 6     # 1 + 5 new
    assert s.n_bonds == 6
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("c1ccccc1")


# ---- FG attachment ---------------------------------------------

def test_oh_on_existing_atom_makes_methanol(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))   # methyl C
    panel.set_tool("template-oh")
    panel.handle_canvas_press(QPointF(0, 0))   # attach OH to it
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("CO")


def test_cooh_on_existing_atom_makes_acetic_acid(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel.set_tool("template-cooh")
    panel.handle_canvas_press(QPointF(0, 0))
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("CC(=O)O")


def test_no2_on_existing_atom_makes_nitromethane(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel.set_tool("template-no2")
    panel.handle_canvas_press(QPointF(0, 0))
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("C[N+](=O)[O-]")


# ---- undo / redo round-trip ------------------------------------

def test_undo_reverses_template_placement(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("template-benzene")
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.get_structure().n_atoms == 6
    panel.undo()
    assert panel.get_structure().is_empty
    assert panel.can_redo()


def test_redo_replays_template_placement(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("template-cyclopentane")
    panel.handle_canvas_press(QPointF(0, 0))
    panel.undo()
    panel.redo()
    assert panel.get_structure().n_atoms == 5
    assert Chem.CanonSmiles(panel.current_smiles()) == \
           Chem.CanonSmiles("C1CCCC1")


def test_template_then_atom_modify_then_undo_chain(_app, qtbot):
    """One benzene + one element swap should be two undo steps."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("template-benzene")
    panel.handle_canvas_press(QPointF(0, 0))
    bz_smi = panel.current_smiles()
    # Now turn one ring carbon into an N — it'll un-aromatise but
    # the test only cares about undo bookkeeping.
    panel.set_tool("atom-N")
    panel.handle_canvas_press(QPointF(0, 0))
    after_swap = panel.get_structure()
    assert any(a.element == "N" for a in after_swap.atoms)
    # Undo: drop N back to C.
    panel.undo()
    assert all(a.element == "C" for a in panel.get_structure().atoms)
    # Undo again: ring vanishes.
    panel.undo()
    assert panel.get_structure().is_empty


# ---- signal emission -------------------------------------------

def test_template_placement_emits_structure_changed(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    received = []
    panel.structure_changed.connect(lambda smi: received.append(smi))
    panel.set_tool("template-furan")
    panel.handle_canvas_press(QPointF(0, 0))
    assert len(received) == 1
    assert Chem.CanonSmiles(received[0]) == \
           Chem.CanonSmiles("c1ccoc1")


# ---- scene-item bookkeeping ------------------------------------

def test_template_creates_scene_items_for_every_atom(_app, qtbot):
    """`_atom_items` must stay in lock-step with the structure's
    atom list — the scene items are how the canvas draws + how
    hit-testing finds atoms."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("template-pyridine")
    panel.handle_canvas_press(QPointF(0, 0))
    s = panel.get_structure()
    assert len(panel._atom_items) == s.n_atoms
    assert len(panel._bond_items) == s.n_bonds
