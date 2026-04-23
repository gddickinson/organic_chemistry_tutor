"""Tests for Phase 29b Carbohydrates tab panel."""
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
    """Phase 30 moved the Carbohydrates panel into the Macromolecules
    window; confirm it lives there now, not on the main tabbar."""
    win = app.window
    main_labels = [win.tabs.tabText(i) for i in range(win.tabs.count())]
    assert "Carbohydrates" not in main_labels, main_labels
    mw = win.open_macromolecules_window()
    inner = [mw.tabs.tabText(i) for i in range(mw.tabs.count())]
    assert "Carbohydrates" in inner, inner


def test_panel_populates_full_catalogue(app):
    from orgchem.core.carbohydrates import CARBOHYDRATES
    panel = app.window.carbohydrates
    # No family filter, no text filter → every entry.
    assert panel.entry_list.count() == len(CARBOHYDRATES)


def test_family_filter_monosaccharides(app):
    panel = app.window.carbohydrates
    # Find and select the "monosaccharide" family.
    for i in range(panel.family_combo.count()):
        if panel.family_combo.itemData(i) == "monosaccharide":
            panel.family_combo.setCurrentIndex(i)
            break
    from orgchem.core.carbohydrates import CARBOHYDRATES
    expected = sum(1 for c in CARBOHYDRATES
                   if c.family == "monosaccharide")
    assert panel.entry_list.count() == expected
    # Restore.
    panel.family_combo.setCurrentIndex(0)


def test_free_text_filter(app):
    panel = app.window.carbohydrates
    panel.filter.setText("sucrose")
    assert panel.entry_list.count() == 1
    panel.filter.clear()


def test_selection_populates_meta_and_svg(app):
    panel = app.window.carbohydrates
    # Select the first entry explicitly (may already be set by __init__).
    panel.entry_list.setCurrentRow(0)
    html = panel.meta.toHtml()
    # Name tag present in the details pane.
    assert "Family" in html
    # The SVG widget actually loaded something (non-zero size).
    assert panel.svg.renderer().isValid()


def test_copy_smiles_writes_to_clipboard(app, monkeypatch):
    from PySide6.QtGui import QGuiApplication
    panel = app.window.carbohydrates
    panel.entry_list.setCurrentRow(0)
    entry = panel._current_entry()
    assert entry is not None
    # Clipboard may be synthesised under offscreen Qt; the slot
    # should still not raise.
    panel._on_copy_smiles()
    # Assert the string we copied equals the current entry's SMILES
    # (the application clipboard returns what we just set).
    cb = QGuiApplication.clipboard().text()
    assert cb == entry.smiles


def test_show_in_workspace_without_match_is_graceful(app):
    """Sugar names ('α-D-Glucopyranose') typically aren't in the
    molecule DB; the slot must not crash, just post an info message."""
    panel = app.window.carbohydrates
    panel.entry_list.setCurrentRow(0)
    panel._on_show_in_workspace()  # should not raise


def test_audit_entries_point_at_panel(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("list_carbohydrates", "get_carbohydrate",
                 "carbohydrate_families"):
        entry = GUI_ENTRY_POINTS.get(name, "")
        assert "Macromolecules" in entry and "Carbohydrates" in entry, entry


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
