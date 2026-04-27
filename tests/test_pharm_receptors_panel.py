"""Phase PH-2.0 (round 220) — GUI smoke tests for the new
Receptors panel + the extended PharmMainWindow.
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


def test_receptors_panel_constructs(app):
    from pharm.gui.panels.receptors_panel import (
        ReceptorsPanel,
    )
    from pharm.core.receptors import list_receptors
    panel = ReceptorsPanel()
    assert panel.list_widget.count() == len(list_receptors())


def test_receptors_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.receptors_panel import (
        ReceptorsPanel,
    )
    panel = ReceptorsPanel()
    assert panel.select_receptor("egfr")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "egfr"


def test_receptors_panel_filter_by_text(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.receptors_panel import (
        ReceptorsPanel,
    )
    panel = ReceptorsPanel()
    panel.filter_edit.setText("morphine")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "opioid-mu" in ids


def test_receptors_panel_filter_by_family(app):
    from PySide6.QtCore import Qt
    from pharm.gui.panels.receptors_panel import (
        ReceptorsPanel,
    )
    panel = ReceptorsPanel()
    for i in range(panel.family_combo.count()):
        if panel.family_combo.itemData(i) == "nhr-steroid":
            panel.family_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "glucocorticoid-receptor" in ids
    assert "egfr" not in ids  # rtk family


def test_pharm_main_window_has_receptors_tab(app):
    """The PH-2.0 Receptors tab must appear on
    PharmMainWindow without breaking the existing PH-1.0
    tabs."""
    from pharm.gui.windows.pharm_main_window import (
        PharmMainWindow,
    )
    win = PharmMainWindow()
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Drug classes" in labels
    assert "Receptors" in labels
    assert "Bridges" in labels
    assert "Tutorials" in labels
    assert win.tabs.count() >= 4
    win.close()


def test_pharm_main_window_switch_to_receptors(app):
    from pharm.gui.windows.pharm_main_window import (
        PharmMainWindow,
    )
    win = PharmMainWindow()
    assert win.switch_to(PharmMainWindow.TAB_RECEPTORS)
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Receptors"
    win.close()


def test_open_pharm_receptors_tab_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_pharm_receptors_tab")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Receptors"
