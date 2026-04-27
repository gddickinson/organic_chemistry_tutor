"""Phase BC-1.0 (round 213) — GUI smoke tests for the Biochem
Studio main window + the metabolic-pathways bridge panel.
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


def test_biochem_main_window_constructs(app):
    """Window + inner tabs construct without crashing.  BC-2.0
    (round 219) added the Cofactors tab, so the tab count is
    now 4 instead of the original 3."""
    from biochem.gui.windows.biochem_main_window import (
        BiochemMainWindow,
    )
    win = BiochemMainWindow()
    assert win.tabs.count() >= 4
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Enzymes" in labels
    assert "Cofactors" in labels
    assert "Metabolic pathways" in labels
    assert "Tutorials" in labels
    win.close()


def test_enzymes_panel_lists_all_entries(app):
    from biochem.gui.panels.enzymes_panel import EnzymesPanel
    from biochem.core.enzymes import list_enzymes
    panel = EnzymesPanel()
    assert panel.list_widget.count() == len(list_enzymes())


def test_enzymes_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from biochem.gui.panels.enzymes_panel import EnzymesPanel
    panel = EnzymesPanel()
    assert panel.select_enzyme("hiv-protease")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "hiv-protease"


def test_enzymes_panel_filter_by_drug(app):
    from PySide6.QtCore import Qt
    from biochem.gui.panels.enzymes_panel import EnzymesPanel
    panel = EnzymesPanel()
    panel.filter_edit.setText("captopril")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "ace" in ids


def test_enzymes_panel_filter_by_ec_class(app):
    from PySide6.QtCore import Qt
    from biochem.gui.panels.enzymes_panel import EnzymesPanel
    panel = EnzymesPanel()
    # Set the EC-class combo to Hydrolases (3); should show only
    # class 3 enzymes.
    for i in range(panel.ec_combo.count()):
        if panel.ec_combo.itemData(i) == 3:
            panel.ec_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "chymotrypsin" in ids
    assert "hexokinase" not in ids  # class 2


def test_metabolic_bridge_panel_constructs(app):
    """The bridge panel reads orgchem.core.metabolic_pathways
    directly — proves the cross-studio data-sharing pattern."""
    from biochem.gui.panels.metabolic_bridge_panel import (
        MetabolicBridgePanel,
    )
    from orgchem.core.metabolic_pathways import list_pathways
    panel = MetabolicBridgePanel()
    # All seeded orgchem pathways appear in the bridge.
    assert panel.list_widget.count() == len(list_pathways())


def test_metabolic_bridge_panel_select(app):
    from PySide6.QtCore import Qt
    from biochem.gui.panels.metabolic_bridge_panel import (
        MetabolicBridgePanel,
    )
    panel = MetabolicBridgePanel()
    assert panel.select_pathway("glycolysis")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "glycolysis"


def test_open_biochem_studio_from_main_window(app):
    main = app.window
    win = main.open_biochem_studio_window()
    assert win is not None
    assert main._biochem_window is win
    # Cached:
    win2 = main.open_biochem_studio_window()
    assert win2 is win
    win.close()


def test_open_biochem_studio_with_tab(app):
    main = app.window
    win = main.open_biochem_studio_window(
        tab_label="Metabolic pathways")
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Metabolic pathways"
    win.close()


def test_open_biochem_studio_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_biochem_studio")
    assert isinstance(out, dict)
    assert out.get("opened") is True


def test_open_biochem_studio_agent_action_with_tab(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_biochem_studio", tab="Enzymes")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Enzymes"
