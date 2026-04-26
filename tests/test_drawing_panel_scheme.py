"""Phase 36f.2 (round 132) — pytest-qt cases for the canvas
reaction arrow + Scheme extraction wiring.

Drives the panel's public API to verify (a) arrow placement
flows through the tool dispatcher, (b) `current_scheme()`
partitions atoms by x-coord vs arrow position, (c) the
arrow participates in the round-128 undo / redo stack, and
(d) `clear()` resets the arrow.
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

def test_arrow_tools_registered(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    assert "arrow-forward" in panel._tool_buttons
    assert "arrow-reversible" in panel._tool_buttons


# ---- arrow placement -------------------------------------------

def test_arrow_tool_places_arrow_on_canvas(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.has_arrow()
    state = panel.arrow_state()
    assert state == (0.0, 0.0, "forward")


def test_reversible_arrow_state(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-reversible")
    panel.handle_canvas_press(QPointF(50, 10))
    assert panel.arrow_state() == (50.0, 10.0, "reversible")


def test_second_arrow_replaces_first(_app, qtbot):
    """Only one arrow per canvas — placing again replaces."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    panel.handle_canvas_press(QPointF(80, 0))
    assert panel.arrow_state() == (80.0, 0.0, "forward")


def test_repeat_arrow_at_same_point_is_noop(_app, qtbot):
    """Same kind + same position = no undo snapshot."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    n = len(panel._undo_stack)
    panel.handle_canvas_press(QPointF(0, 0))   # same point
    assert len(panel._undo_stack) == n


def test_remove_arrow_clears_state(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.has_arrow()
    panel.remove_arrow()
    assert not panel.has_arrow()


# ---- undo / redo -----------------------------------------------

def test_undo_reverses_arrow_placement(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    panel.undo()
    assert not panel.has_arrow()
    panel.redo()
    assert panel.arrow_state() == (0.0, 0.0, "forward")


def test_undo_after_arrow_replacement(_app, qtbot):
    """Two arrow placements + undo restores the first arrow,
    not 'no arrow at all'."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    panel.handle_canvas_press(QPointF(80, 0))
    assert panel.arrow_state()[0] == 80.0
    panel.undo()
    assert panel.arrow_state() == (0.0, 0.0, "forward")


def test_clear_drops_arrow(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    panel.clear()
    assert not panel.has_arrow()
    assert panel.get_structure().is_empty


# ---- scheme extraction ------------------------------------------

def test_current_scheme_is_none_without_arrow(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(0, 0))
    assert panel.current_scheme() is None


def test_current_scheme_partitions_atoms_by_x(_app, qtbot):
    """Two atoms left of the arrow + two right → 2-atom LHS,
    2-atom RHS."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # LHS atoms at x = -50, -30; RHS atoms at x = 30, 50.
    for x in (-50, -30, 30, 50):
        panel.handle_canvas_press(QPointF(x, 0))
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))   # arrow at x=0
    scheme = panel.current_scheme()
    assert scheme is not None
    assert scheme.n_lhs_atoms == 2
    assert scheme.n_rhs_atoms == 2


def test_scheme_drops_bonds_crossing_arrow(_app, qtbot):
    """A C-C bond whose endpoints span the arrow shouldn't survive
    into either half of the extracted scheme."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # Two atoms separated wide.
    panel.handle_canvas_press(QPointF(-50, 0))   # atom 0 (LHS)
    panel.handle_canvas_press(QPointF(50, 0))    # atom 1 (RHS)
    # Bond them.
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-50, 0))
    panel.handle_canvas_press(QPointF(50, 0))
    assert panel.get_structure().n_bonds == 1
    # Arrow at x=0 splits them.
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    scheme = panel.current_scheme()
    assert scheme is not None
    # Each side has one atom, no bonds (bond crossed the arrow).
    assert scheme.n_lhs_atoms == 1
    assert scheme.n_rhs_atoms == 1
    for s in scheme.lhs:
        assert s.n_bonds == 0
    for s in scheme.rhs:
        assert s.n_bonds == 0


def test_scheme_preserves_intra_side_bonds(_app, qtbot):
    """A C-C bond entirely on one side of the arrow survives."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    from rdkit import Chem
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    # LHS C-C dimer.
    panel.handle_canvas_press(QPointF(-60, 0))
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.set_tool("bond")
    panel.handle_canvas_press(QPointF(-60, 0))
    panel.handle_canvas_press(QPointF(-30, 0))
    # RHS single carbon.
    panel.set_tool("atom-C")
    panel.handle_canvas_press(QPointF(40, 0))
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    scheme = panel.current_scheme()
    assert scheme is not None
    assert scheme.n_lhs_atoms == 2
    assert scheme.lhs[0].n_bonds == 1
    rxn = scheme.to_reaction_smiles()
    # LHS canonical = ethane "CC", RHS canonical = methane "C".
    assert rxn is not None
    lhs_str, _, rhs_str = rxn.split(">")
    assert Chem.CanonSmiles(lhs_str) == Chem.CanonSmiles("CC")
    assert Chem.CanonSmiles(rhs_str) == Chem.CanonSmiles("C")


def test_scheme_arrow_kind_propagates(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.set_tool("atom-N")
    panel.handle_canvas_press(QPointF(30, 0))
    panel.set_tool("arrow-reversible")
    panel.handle_canvas_press(QPointF(0, 0))
    scheme = panel.current_scheme()
    assert scheme is not None
    assert scheme.arrow == "reversible"


def test_scheme_with_one_empty_side(_app, qtbot):
    """RHS empty (no atoms past the arrow) → empty rhs list."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(40, 0))   # arrow far right
    scheme = panel.current_scheme()
    assert scheme is not None
    assert scheme.n_lhs_atoms == 1
    assert scheme.n_rhs_atoms == 0
    # Reaction-SMILES round-trip should serialise as "C>>".
    rxn = scheme.to_reaction_smiles()
    assert rxn is not None
    assert rxn.endswith(">")


# ---- stereo / charge survive partitioning ----------------------

def test_charge_survives_partitioning(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.set_tool("atom-N")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel._set_atom_charge(0, +1)
    panel._set_atom_h_count(0, 4)
    panel.set_tool("atom-C")
    panel.handle_canvas_press(QPointF(30, 0))
    panel.set_tool("arrow-forward")
    panel.handle_canvas_press(QPointF(0, 0))
    scheme = panel.current_scheme()
    assert scheme is not None
    assert scheme.lhs[0].atoms[0].charge == 1
    assert scheme.lhs[0].atoms[0].h_count == 4
