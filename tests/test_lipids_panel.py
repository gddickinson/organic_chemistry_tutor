"""Tests for Phase 29b Lipids tab panel."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_tab_exists(app):
    """Phase 30 moved the Lipids panel into the Macromolecules window.
    It should no longer be on the main-window tabbar but must appear
    as an inner tab of the secondary window."""
    win = app.window
    main_labels = [win.tabs.tabText(i) for i in range(win.tabs.count())]
    assert "Lipids" not in main_labels, main_labels
    mw = win.open_macromolecules_window()
    inner = [mw.tabs.tabText(i) for i in range(mw.tabs.count())]
    assert "Lipids" in inner, inner


def test_panel_populates_full_catalogue(app):
    from orgchem.core.lipids import LIPIDS
    panel = app.window.lipids
    assert panel.entry_list.count() == len(LIPIDS)


def test_family_filter_fatty_acids(app):
    panel = app.window.lipids
    for i in range(panel.family_combo.count()):
        if panel.family_combo.itemData(i) == "fatty-acid":
            panel.family_combo.setCurrentIndex(i)
            break
    from orgchem.core.lipids import LIPIDS
    expected = sum(1 for l in LIPIDS if l.family == "fatty-acid")
    assert panel.entry_list.count() == expected
    panel.family_combo.setCurrentIndex(0)


def test_free_text_filter(app):
    panel = app.window.lipids
    panel.filter.setText("cholesterol")
    # At least one direct cholesterol entry (may also match notes that
    # mention cholesterol, so use >= 1).
    assert panel.entry_list.count() >= 1
    panel.filter.clear()


def test_selection_populates_meta_and_svg(app):
    panel = app.window.lipids
    panel.entry_list.setCurrentRow(0)
    html = panel.meta.toHtml()
    assert "Family" in html
    assert panel.svg.renderer().isValid()


def test_copy_smiles_writes_to_clipboard(app):
    from PySide6.QtGui import QGuiApplication
    panel = app.window.lipids
    panel.entry_list.setCurrentRow(0)
    entry = panel._current_entry()
    assert entry is not None
    panel._on_copy_smiles()
    cb = QGuiApplication.clipboard().text()
    assert cb == entry.smiles


def test_audit_entries_point_at_panel(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("list_lipids", "get_lipid", "lipid_families"):
        entry = GUI_ENTRY_POINTS.get(name, "")
        assert "Macromolecules" in entry and "Lipids" in entry, entry


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
