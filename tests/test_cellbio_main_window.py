"""Phase CB-1.0 (round 212) — GUI smoke tests for the Cell Bio
Studio main window.

Headless / offscreen — verifies the window + its panels construct
cleanly + the open-from-OrgChem path works end-to-end.
"""
from __future__ import annotations
import os
import pytest


pytest.importorskip("PySide6")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_cellbio_main_window_constructs(app):
    """Window + inner tabs construct without crashing.  CB-2.0
    (round 218) added the Cell-cycle tab, so the count is now
    3 instead of the original 2."""
    from cellbio.gui.windows.cellbio_main_window import (
        CellBioMainWindow,
    )
    win = CellBioMainWindow()
    assert win.tabs.count() >= 3
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Signalling" in labels
    assert "Cell cycle" in labels
    assert "Tutorials" in labels
    win.close()


def test_signalling_panel_lists_pathways(app):
    """The Signalling panel populates from the catalogue on
    construction."""
    from cellbio.gui.panels.signaling_panel import SignalingPanel
    from cellbio.core.cell_signaling import list_pathways
    panel = SignalingPanel()
    # All pathways should be in the list at construction (no
    # filters applied).
    assert panel.list_widget.count() == len(list_pathways())


def test_signalling_panel_select_by_id(app):
    from cellbio.gui.panels.signaling_panel import SignalingPanel
    panel = SignalingPanel()
    assert panel.select_pathway("hippo-yap")
    item = panel.list_widget.currentItem()
    assert item is not None
    from PySide6.QtCore import Qt
    assert item.data(Qt.UserRole) == "hippo-yap"


def test_signalling_panel_filter_by_drug(app):
    from cellbio.gui.panels.signaling_panel import SignalingPanel
    panel = SignalingPanel()
    panel.filter_edit.setText("metformin")
    # AMPK + insulin both reference metformin.
    ids = []
    from PySide6.QtCore import Qt
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "ampk" in ids


def test_open_cellbio_studio_from_main_window(app):
    """The OrgChem MainWindow → open_cellbio_studio_window slot
    returns a real Cell Bio main window + caches it."""
    main = app.window
    win = main.open_cellbio_studio_window()
    assert win is not None
    # Cached for re-use.
    assert main._cellbio_window is win
    # Re-opening returns the same instance.
    win2 = main.open_cellbio_studio_window()
    assert win2 is win
    win.close()


def test_open_cellbio_studio_with_tab_label(app):
    main = app.window
    win = main.open_cellbio_studio_window(tab_label="Tutorials")
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Tutorials"
    win.close()


def test_open_cellbio_studio_agent_action(app):
    """The agent action routes through Qt main-thread dispatch +
    returns a JSON-friendly status dict."""
    from orgchem.agent.actions import invoke
    out = invoke("open_cellbio_studio")
    assert isinstance(out, dict)
    assert out.get("opened") is True


def test_open_cellbio_studio_agent_action_with_tab(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_cellbio_studio", tab="Signalling")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Signalling"
