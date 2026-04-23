"""Tests for Phase 25b MedChem + Naming dialogs and Phase 27c Periodic-table
dialog (round 36)."""
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


# ----------------------- MedChem dialog ------------------------------


def test_medchem_dialog_has_two_tabs(app):
    from orgchem.gui.dialogs.medchem import MedChemDialog
    d = MedChemDialog(app.window)
    assert d.tabs.count() == 2


def test_medchem_sar_populates_from_seed(app):
    from orgchem.gui.dialogs.medchem import MedChemDialog
    from orgchem.core.sar import SAR_LIBRARY
    d = MedChemDialog(app.window)
    # First seeded series should populate the table.
    assert d.sar_combo.count() == len(SAR_LIBRARY)
    assert d.sar_table.rowCount() > 0
    assert "target" in d.sar_meta.text().lower()


def test_medchem_bioisosteres_suggest(app):
    from orgchem.gui.dialogs.medchem import MedChemDialog
    d = MedChemDialog(app.window)
    d.bio_smiles.setText("CC(=O)O")   # acetic acid → COOH→tetrazole, etc.
    d._on_bio_run()
    # Variants may be empty on some seeds; at minimum no crash and
    # status text updates.
    assert "variants" in d.bio_status.text() or \
        "template" in d.bio_status.text()


def test_audit_coverage_medchem(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("list_sar_series", "get_sar_series",
                 "export_sar_matrix", "list_bioisosteres",
                 "suggest_bioisosteres"):
        assert GUI_ENTRY_POINTS.get(name), \
            f"{name} should be wired via the MedChem dialog"


# ----------------------- Naming dialog -------------------------------


def test_naming_dialog_lists_all_rules(app):
    from orgchem.gui.dialogs.naming_rules import NamingRulesDialog
    from orgchem.naming.rules import RULES
    d = NamingRulesDialog(app.window)
    assert d.rule_list.count() == len(RULES)


def test_naming_dialog_category_filter(app):
    from orgchem.gui.dialogs.naming_rules import NamingRulesDialog
    from orgchem.naming.rules import RULES
    d = NamingRulesDialog(app.window)
    # Pick the first non-"(all)" category and confirm the list shrinks.
    for i in range(d.cat_combo.count()):
        cat = d.cat_combo.itemData(i)
        if cat:
            d.cat_combo.setCurrentIndex(i)
            break
    expected = sum(1 for r in RULES if r.category == cat)
    assert d.rule_list.count() == expected


def test_naming_dialog_selection_populates_body(app):
    from orgchem.gui.dialogs.naming_rules import NamingRulesDialog
    from orgchem.naming.rules import RULES
    d = NamingRulesDialog(app.window)
    # Default-selected first rule should have populated the body —
    # check the first rule's title appears.
    assert RULES[0].title in d.body_browser.toPlainText()


def test_audit_coverage_naming(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("list_naming_rules", "get_naming_rule",
                 "naming_rule_categories"):
        assert GUI_ENTRY_POINTS.get(name)


# ----------------------- Periodic-table dialog -----------------------


def test_periodic_dialog_builds(app):
    from orgchem.gui.dialogs.periodic_table import PeriodicTableDialog
    d = PeriodicTableDialog(app.window)
    # 118 cells laid out in the grid (plus legend / sidepane).
    # Count the PushButton cells we added to the grid.
    cells = [d._grid.itemAt(i).widget() for i in range(d._grid.count())]
    from PySide6.QtWidgets import QPushButton
    btn_count = sum(1 for c in cells if isinstance(c, QPushButton))
    assert btn_count == 118


def test_periodic_dialog_shows_element_on_click(app):
    from orgchem.gui.dialogs.periodic_table import PeriodicTableDialog
    from orgchem.core.periodic_table import get_element
    d = PeriodicTableDialog(app.window)
    d._show_element(get_element("Fe"))
    html = d.info.toHtml()
    assert "Iron" in html
    assert "Fe" in html
    assert "3d" in html    # electron config hint


def test_audit_coverage_periodic(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("list_elements", "get_element", "elements_by_category"):
        assert GUI_ENTRY_POINTS.get(name)
