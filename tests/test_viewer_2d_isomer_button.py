"""Phase 48d (round 173) — tests for the inline 'View
isomers' button on the molecule 2D viewer.
"""
from __future__ import annotations
import os

import pytest


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def _reset_isomer_dialog():
    from orgchem.gui.dialogs import isomer_explorer as mod
    mod.IsomerExplorerDialog._instance = None
    yield
    mod.IsomerExplorerDialog._instance = None


# ==================================================================
# Button presence + initial state
# ==================================================================

def test_viewer_2d_carries_view_isomers_button(app, qtbot):
    """The Phase-48d button must be present on the Viewer2DPanel."""
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    assert hasattr(p, "_isomers_btn")
    assert p._isomers_btn.text() == "View isomers…"


def test_viewer_2d_button_disabled_before_selection(app, qtbot):
    """Before any molecule is selected, the button must be
    disabled — no SMILES to send to the dialog."""
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    assert p._isomers_btn.isEnabled() is False


def test_viewer_2d_button_enabled_after_smiles_set(app, qtbot):
    """After receiving a molecule_selected signal carrying a
    real SMILES, the button must enable."""
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    # Simulate a molecule selection by directly calling
    # _on_mol with a known seeded molecule id.
    from orgchem.db.queries import list_molecules
    rows = list_molecules()
    cholesterol = next(
        (m for m in rows if m.name == "Cholesterol"), None)
    if cholesterol is None:
        pytest.skip("Cholesterol not seeded in this DB run")
    p._on_mol(cholesterol.id)
    assert p._isomers_btn.isEnabled() is True
    assert p._current_smiles == cholesterol.smiles


# ==================================================================
# Click → opens dialog with pre-filled SMILES
# ==================================================================

def test_view_isomers_click_opens_dialog(app, qtbot):
    """Clicking the View isomers button opens the singleton
    dialog AND pre-fills the SMILES inputs."""
    from orgchem.gui.dialogs import isomer_explorer as iso_mod
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    p._current_smiles = "CC(O)C(O)CO"
    p._isomers_btn.setEnabled(True)
    p._on_view_isomers()
    dlg = iso_mod.IsomerExplorerDialog._instance
    assert dlg is not None
    # All three SMILES inputs should be pre-filled.
    assert dlg._stereo_smiles.text() == "CC(O)C(O)CO"
    assert dlg._taut_smiles.text() == "CC(O)C(O)CO"
    assert dlg._cls_a.text() == "CC(O)C(O)CO"


def test_view_isomers_click_focuses_stereoisomers_tab(app, qtbot):
    """Click should land the user on the Stereoisomers tab —
    that's the most natural starting view for 'show me this
    molecule's isomers'."""
    from orgchem.gui.dialogs import isomer_explorer as iso_mod
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    p._current_smiles = "CC(O)C(O)CO"
    p._on_view_isomers()
    dlg = iso_mod.IsomerExplorerDialog._instance
    assert dlg.tab_labels()[
        dlg._tabs.currentIndex()] == "Stereoisomers"


def test_view_isomers_click_auto_runs_enumeration(app, qtbot):
    """Click should auto-run the stereoisomer enumeration so
    the user sees results immediately — no extra Enumerate
    click needed."""
    from orgchem.gui.dialogs import isomer_explorer as iso_mod
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    # 2-stereocentre input → 4 isomers.
    p._current_smiles = "CC(O)C(O)CO"
    p._on_view_isomers()
    dlg = iso_mod.IsomerExplorerDialog._instance
    assert dlg._stereo_list.count() == 4


def test_view_isomers_click_with_no_smiles_is_noop(app, qtbot):
    """If somehow the button is clicked without a current
    SMILES (e.g. signal race), it should silently no-op
    instead of opening an empty dialog."""
    from orgchem.gui.dialogs import isomer_explorer as iso_mod
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    p._current_smiles = None
    p._on_view_isomers()
    assert iso_mod.IsomerExplorerDialog._instance is None


def test_view_isomers_singleton_pattern(app, qtbot):
    """Clicking twice from the same panel reuses the same
    dialog instance (singleton)."""
    from orgchem.gui.dialogs import isomer_explorer as iso_mod
    from orgchem.gui.panels.viewer_2d import Viewer2DPanel
    p = Viewer2DPanel()
    qtbot.addWidget(p)
    p._current_smiles = "CCO"
    p._on_view_isomers()
    first = iso_mod.IsomerExplorerDialog._instance
    p._current_smiles = "CC(C)O"
    p._on_view_isomers()
    second = iso_mod.IsomerExplorerDialog._instance
    assert first is second
    # Second click should have updated the SMILES inputs.
    assert second._stereo_smiles.text() == "CC(C)O"
