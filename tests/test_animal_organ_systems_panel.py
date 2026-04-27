"""Phase AB-2.0 (round 223) — GUI smoke tests for the new
Organ-systems panel + the extended AnimalMainWindow.  FINAL
deep-phase round.
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


def test_organ_systems_panel_constructs(app):
    from animal.gui.panels.organ_systems_panel import (
        OrganSystemsPanel,
    )
    from animal.core.organ_systems import list_organ_systems
    panel = OrganSystemsPanel()
    assert panel.list_widget.count() == \
        len(list_organ_systems())


def test_organ_systems_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.organ_systems_panel import (
        OrganSystemsPanel,
    )
    panel = OrganSystemsPanel()
    assert panel.select_system("nervous-mammalian")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "nervous-mammalian"


def test_organ_systems_panel_filter_by_text(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.organ_systems_panel import (
        OrganSystemsPanel,
    )
    panel = OrganSystemsPanel()
    panel.filter_edit.setText("Parkinson")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "nervous-mammalian" in ids


def test_organ_systems_panel_filter_by_category(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.organ_systems_panel import (
        OrganSystemsPanel,
    )
    panel = OrganSystemsPanel()
    for i in range(panel.category_combo.count()):
        if panel.category_combo.itemData(i) == \
                "comparative-anatomy":
            panel.category_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "regeneration-comparative" in ids
    assert "nervous-mammalian" not in ids


def test_animal_main_window_has_organ_systems_tab(app):
    from animal.gui.windows.animal_main_window import (
        AnimalMainWindow,
    )
    win = AnimalMainWindow()
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Animal taxa" in labels
    assert "Organ systems" in labels
    assert "Cell signalling bridge" in labels
    assert "Tutorials" in labels
    assert win.tabs.count() >= 4
    win.close()


def test_animal_main_window_switch_to_organ_systems(app):
    from animal.gui.windows.animal_main_window import (
        AnimalMainWindow,
    )
    win = AnimalMainWindow()
    assert win.switch_to(AnimalMainWindow.TAB_ORGAN_SYSTEMS)
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Organ systems"
    win.close()


def test_open_animal_organ_systems_tab_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_animal_organ_systems_tab")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Organ systems"
