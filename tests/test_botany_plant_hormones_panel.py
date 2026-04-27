"""Phase BT-2.0 (round 222) — GUI smoke tests for the new
Plant-hormones panel + the extended BotanyMainWindow.
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


def test_plant_hormones_panel_constructs(app):
    from botany.gui.panels.plant_hormones_panel import (
        PlantHormonesPanel,
    )
    from botany.core.plant_hormones import list_plant_hormones
    panel = PlantHormonesPanel()
    assert panel.list_widget.count() == \
        len(list_plant_hormones())


def test_plant_hormones_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_hormones_panel import (
        PlantHormonesPanel,
    )
    panel = PlantHormonesPanel()
    assert panel.select_hormone("ethylene")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "ethylene"


def test_plant_hormones_panel_filter_by_text(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_hormones_panel import (
        PlantHormonesPanel,
    )
    panel = PlantHormonesPanel()
    panel.filter_edit.setText("FERONIA")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "ralf-peptides" in ids


def test_plant_hormones_panel_filter_by_class(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_hormones_panel import (
        PlantHormonesPanel,
    )
    panel = PlantHormonesPanel()
    for i in range(panel.class_combo.count()):
        if panel.class_combo.itemData(i) == "auxin":
            panel.class_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "iaa" in ids
    assert "ethylene" not in ids


def test_botany_main_window_has_plant_hormones_tab(app):
    from botany.gui.windows.botany_main_window import (
        BotanyMainWindow,
    )
    win = BotanyMainWindow()
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Plant taxa" in labels
    assert "Plant hormones" in labels
    assert "Plant secondary metabolites" in labels
    assert "Tutorials" in labels
    assert win.tabs.count() >= 4
    win.close()


def test_botany_main_window_switch_to_plant_hormones(app):
    from botany.gui.windows.botany_main_window import (
        BotanyMainWindow,
    )
    win = BotanyMainWindow()
    assert win.switch_to(BotanyMainWindow.TAB_PLANT_HORMONES)
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Plant hormones"
    win.close()


def test_open_botany_plant_hormones_tab_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_botany_plant_hormones_tab")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Plant hormones"
