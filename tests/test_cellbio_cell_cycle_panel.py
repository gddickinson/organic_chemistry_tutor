"""Phase CB-2.0 (round 218) — GUI smoke tests for the new
Cell-cycle panel + the extended CellBioMainWindow.
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


def test_cell_cycle_panel_constructs(app):
    from cellbio.gui.panels.cell_cycle_panel import (
        CellCyclePanel,
    )
    from cellbio.core.cell_cycle import list_cell_cycle_entries
    panel = CellCyclePanel()
    assert panel.list_widget.count() == \
        len(list_cell_cycle_entries())


def test_cell_cycle_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from cellbio.gui.panels.cell_cycle_panel import (
        CellCyclePanel,
    )
    panel = CellCyclePanel()
    assert panel.select_entry("rb-e2f-axis")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "rb-e2f-axis"


def test_cell_cycle_panel_filter_by_text(app):
    from PySide6.QtCore import Qt
    from cellbio.gui.panels.cell_cycle_panel import (
        CellCyclePanel,
    )
    panel = CellCyclePanel()
    panel.filter_edit.setText("aurora")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "aurora-kinases" in ids


def test_cell_cycle_panel_filter_by_category(app):
    from PySide6.QtCore import Qt
    from cellbio.gui.panels.cell_cycle_panel import (
        CellCyclePanel,
    )
    panel = CellCyclePanel()
    for i in range(panel.category_combo.count()):
        if panel.category_combo.itemData(i) == "cyclin-cdk":
            panel.category_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "cyclin-d-cdk4-cdk6" in ids
    assert "rb-e2f-axis" not in ids  # pocket-protein category


def test_cellbio_main_window_has_cell_cycle_tab(app):
    """The CB-2.0 Cell-cycle tab must appear on
    CellBioMainWindow without breaking the existing CB-1.0
    tabs."""
    from cellbio.gui.windows.cellbio_main_window import (
        CellBioMainWindow,
    )
    win = CellBioMainWindow()
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Signalling" in labels
    assert "Cell cycle" in labels
    assert "Tutorials" in labels
    assert win.tabs.count() >= 3
    win.close()


def test_cellbio_main_window_switch_to_cell_cycle(app):
    from cellbio.gui.windows.cellbio_main_window import (
        CellBioMainWindow,
    )
    win = CellBioMainWindow()
    assert win.switch_to(CellBioMainWindow.TAB_CELL_CYCLE)
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Cell cycle"
    win.close()


def test_open_cellbio_cell_cycle_tab_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_cellbio_cell_cycle_tab")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Cell cycle"
