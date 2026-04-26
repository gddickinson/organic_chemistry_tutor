"""Phase 36e (round 130) — wedge / dash + charge / isotope /
radical / explicit-H tests for `DrawingPanel`.

Drives the canvas through its public + tool-mode API; exercises
the round-128 undo stack to verify Phase-36e mutations
participate as one logical step each.
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

def test_wedge_and_dash_tools_registered(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    assert "bond-wedge" in panel._tool_buttons
    assert "bond-dash" in panel._tool_buttons


# ---- wedge bond placement --------------------------------------

def test_wedge_tool_creates_wedge_bond(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))   # C0
    panel.handle_canvas_press(QPointF(20, 0))    # C1
    panel.set_tool("bond-wedge")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    s = panel.get_structure()
    assert s.n_bonds == 1
    assert s.bonds[0].stereo == "wedge"
    assert s.bonds[0].order == 1


def test_dash_tool_creates_dash_bond(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond-dash")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    s = panel.get_structure()
    assert s.bonds[0].stereo == "dash"


def test_wedge_tool_toggles_stereo_on_existing_bond(_app, qtbot):
    """Clicking wedge on a bond that already IS wedge clears
    the stereo back to ``"none"``."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond-wedge")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().bonds[0].stereo == "wedge"
    # Click again — toggles off.
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().bonds[0].stereo == "none"


def test_wedge_replaces_dash_on_same_bond(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond-dash")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond-wedge")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().bonds[0].stereo == "wedge"


def test_wedge_auto_places_endpoints(_app, qtbot):
    """Empty-canvas wedge clicks should place fresh carbons,
    matching the plain bond tool's behaviour."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("bond-wedge")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    s = panel.get_structure()
    assert s.n_atoms == 2
    assert s.n_bonds == 1
    assert s.bonds[0].stereo == "wedge"


def test_undo_reverses_wedge_creation(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond-wedge")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    assert panel.get_structure().n_bonds == 1
    panel.undo()
    assert panel.get_structure().n_bonds == 0


# ---- charge property -------------------------------------------

def test_set_atom_charge_updates_structure(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("atom-N")
    panel.handle_canvas_press(QPointF(0, 0))
    panel._set_atom_charge(0, +1)
    assert panel.get_structure().atoms[0].charge == +1


def test_set_atom_charge_pushes_undo(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("atom-N")
    panel.handle_canvas_press(QPointF(0, 0))
    # One undo step from atom placement.
    assert len(panel._undo_stack) == 1
    panel._set_atom_charge(0, +1)
    assert len(panel._undo_stack) == 2
    panel.undo()
    assert panel.get_structure().atoms[0].charge == 0


def test_set_atom_charge_no_op_when_unchanged(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    n_before = len(panel._undo_stack)
    panel._set_atom_charge(0, 0)   # same as default
    assert len(panel._undo_stack) == n_before


def test_charged_nitrogen_round_trips_via_smiles(_app, qtbot):
    """Charge must survive the live SMILES round-trip."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("atom-N")
    panel.handle_canvas_press(QPointF(0, 0))
    panel._set_atom_charge(0, +1)
    panel._set_atom_h_count(0, 4)   # NH4+
    smi = panel.current_smiles()
    assert Chem.CanonSmiles(smi) == Chem.CanonSmiles("[NH4+]")


# ---- isotope --------------------------------------------------

def test_set_atom_isotope(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel._set_atom_isotope(0, 13)
    assert panel.get_structure().atoms[0].isotope == 13


def test_isotope_round_trips_in_smiles(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel._set_atom_isotope(0, 13)
    smi = panel.current_smiles()
    assert "13" in smi
    # Round-trip via RDKit canonical form.
    mol = Chem.MolFromSmiles(smi)
    assert mol is not None
    assert mol.GetAtomWithIdx(0).GetIsotope() == 13


# ---- radical electrons ----------------------------------------

def test_set_atom_radical(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel._set_atom_radical(0, 1)
    assert panel.get_structure().atoms[0].radical == 1


# ---- explicit H count -----------------------------------------

def test_set_atom_h_count(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    panel._set_atom_h_count(0, 3)
    assert panel.get_structure().atoms[0].h_count == 3
    # Undo restores default sentinel -1.
    panel.undo()
    assert panel.get_structure().atoms[0].h_count == -1


# ---- right-click hit-test guard -------------------------------

def test_right_click_on_empty_canvas_is_noop(_app, qtbot):
    """Right-click misses any atom → no menu, no exception."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from PySide6.QtCore import QPoint
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_right_click(QPointF(999, 999), QPoint(0, 0))
    assert panel.get_structure().is_empty


# ---- bond stereo round-trip via RDKit -------------------------

def test_wedge_bond_emits_stereo_flag_in_molblock(_app, qtbot):
    """Wedge stereo must be encoded in the V2000 mol-block bond
    line.  RDKit's reader drops the direction on non-stereocenter
    bonds, so we verify the *writer* output rather than the
    round-trip."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from orgchem.core.drawing import structure_to_molblock
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # Build C-C with wedge.
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    panel.set_tool("bond-wedge")
    panel.handle_canvas_press(QPointF(-20, 0))
    panel.handle_canvas_press(QPointF(20, 0))
    block = structure_to_molblock(panel.get_structure())
    assert block is not None
    # V2000 bond line: "atom1 atom2 type stereo". For C-C with
    # wedge the line should be "  1  2  1  1" (last 1 = wedge).
    # Whitespace-tokenise to be field-width tolerant.
    tokens = [ln.split() for ln in block.splitlines()
              if ln.strip().startswith(("1 2", "2 1"))
              or (len(ln.split()) >= 4
                  and ln.split()[0] in ("1", "2")
                  and ln.split()[1] in ("1", "2")
                  and ln.split()[0] != ln.split()[1])]
    bond_tokens = [t for t in tokens if len(t) >= 4
                   and t[0] in ("1", "2") and t[1] in ("1", "2")]
    assert any(t[3] == "1" for t in bond_tokens), \
        f"No wedge stereo flag in molblock:\n{block}"
