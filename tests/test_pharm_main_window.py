"""Phase PH-1.0 (round 214) — GUI smoke tests for the
Pharmacology Studio main window + multi-hop bridge panels.
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


def test_pharm_main_window_constructs(app):
    """Main window + inner tabs construct without crashing.
    PH-2.0 (round 220) added the Receptors tab, so the tab
    count is now 4 instead of the original 3."""
    from pharm.gui.windows.pharm_main_window import (
        PharmMainWindow,
    )
    win = PharmMainWindow()
    assert win.tabs.count() >= 4
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Drug classes" in labels
    assert "Receptors" in labels
    assert "Bridges" in labels
    assert "Tutorials" in labels
    win.close()


def test_drug_classes_panel_lists_all(app):
    from pharm.gui.panels.drug_classes_panel import (
        DrugClassesPanel,
    )
    from pharm.core.drug_classes import list_drug_classes
    panel = DrugClassesPanel()
    assert panel.list_widget.count() == len(list_drug_classes())


def test_drug_classes_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.drug_classes_panel import (
        DrugClassesPanel,
    )
    panel = DrugClassesPanel()
    assert panel.select_drug_class("statins")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "statins"


def test_drug_classes_panel_filter_by_agent(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.drug_classes_panel import (
        DrugClassesPanel,
    )
    panel = DrugClassesPanel()
    panel.filter_edit.setText("propranolol")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "beta-blockers" in ids


def test_drug_classes_panel_filter_by_target_class(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.drug_classes_panel import (
        DrugClassesPanel,
    )
    panel = DrugClassesPanel()
    # Set target combo to GPCR.
    for i in range(panel.target_combo.count()):
        if panel.target_combo.itemData(i) == "GPCR":
            panel.target_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "beta-blockers" in ids
    assert "statins" not in ids  # enzyme target


def test_biochem_bridge_panel_constructs(app):
    """The bridge reads biochem.core.enzymes directly."""
    from pharm.gui.panels.biochem_bridge_panel import (
        BiochemBridgePanel,
    )
    from biochem.core.enzymes import list_enzymes
    panel = BiochemBridgePanel()
    # Should list only drug-targetable enzymes (drug_targets
    # non-empty).  Sanity check: count ≥ 1, ≤ total.
    drug_targetable = sum(
        1 for e in list_enzymes() if e.drug_targets)
    assert panel.list_widget.count() == drug_targetable
    assert panel.list_widget.count() >= 1


def test_biochem_bridge_select_enzyme(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.biochem_bridge_panel import (
        BiochemBridgePanel,
    )
    panel = BiochemBridgePanel()
    assert panel.select_enzyme("ace")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "ace"


def test_cellbio_bridge_panel_constructs(app):
    """The bridge reads cellbio.core.cell_signaling directly —
    multi-hop data sharing."""
    from pharm.gui.panels.cellbio_bridge_panel import (
        CellBioBridgePanel,
    )
    from cellbio.core.cell_signaling import list_pathways
    panel = CellBioBridgePanel()
    drug_targeted = sum(
        1 for p in list_pathways() if p.drug_targets)
    assert panel.list_widget.count() == drug_targeted
    assert panel.list_widget.count() >= 1


def test_cellbio_bridge_select_pathway(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.cellbio_bridge_panel import (
        CellBioBridgePanel,
    )
    panel = CellBioBridgePanel()
    # Pick a pathway we know is drug-targeted (e.g. mapk-erk
    # has Vemurafenib + Trametinib).
    assert panel.select_pathway("mapk-erk")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "mapk-erk"


def test_open_pharm_studio_from_main_window(app):
    main = app.window
    win = main.open_pharm_studio_window()
    assert win is not None
    assert main._pharm_window is win
    win2 = main.open_pharm_studio_window()
    assert win2 is win
    win.close()


def test_open_pharm_studio_with_tab(app):
    main = app.window
    win = main.open_pharm_studio_window(tab_label="Bridges")
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Bridges"
    win.close()


def test_open_pharm_studio_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_pharm_studio")
    assert isinstance(out, dict)
    assert out.get("opened") is True


def test_open_pharm_studio_agent_action_with_tab(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_pharm_studio", tab="Drug classes")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Drug classes"
