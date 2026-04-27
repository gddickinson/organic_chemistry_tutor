"""Phase BC-2.0 (round 219) — GUI smoke tests for the new
Cofactors panel + the extended BiochemMainWindow.
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


def test_cofactors_panel_constructs(app):
    from biochem.gui.panels.cofactors_panel import (
        CofactorsPanel,
    )
    from biochem.core.cofactors import list_cofactors
    panel = CofactorsPanel()
    assert panel.list_widget.count() == len(list_cofactors())


def test_cofactors_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from biochem.gui.panels.cofactors_panel import (
        CofactorsPanel,
    )
    panel = CofactorsPanel()
    assert panel.select_cofactor("atp")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "atp"


def test_cofactors_panel_filter_by_text(app):
    from PySide6.QtCore import Qt
    from biochem.gui.panels.cofactors_panel import (
        CofactorsPanel,
    )
    panel = CofactorsPanel()
    panel.filter_edit.setText("heme")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "heme" in ids


def test_cofactors_panel_filter_by_class(app):
    from PySide6.QtCore import Qt
    from biochem.gui.panels.cofactors_panel import (
        CofactorsPanel,
    )
    panel = CofactorsPanel()
    for i in range(panel.class_combo.count()):
        if panel.class_combo.itemData(i) == "nicotinamide":
            panel.class_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "nad-plus" in ids
    assert "atp" not in ids  # phosphate-energy class


def test_biochem_main_window_has_cofactors_tab(app):
    """The BC-2.0 Cofactors tab must appear on
    BiochemMainWindow without breaking the existing BC-1.0
    tabs."""
    from biochem.gui.windows.biochem_main_window import (
        BiochemMainWindow,
    )
    win = BiochemMainWindow()
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Enzymes" in labels
    assert "Cofactors" in labels
    assert "Metabolic pathways" in labels
    assert "Tutorials" in labels
    assert win.tabs.count() >= 4
    win.close()


def test_biochem_main_window_switch_to_cofactors(app):
    from biochem.gui.windows.biochem_main_window import (
        BiochemMainWindow,
    )
    win = BiochemMainWindow()
    assert win.switch_to(BiochemMainWindow.TAB_COFACTORS)
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Cofactors"
    win.close()


def test_open_biochem_cofactors_tab_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_biochem_cofactors_tab")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Cofactors"
