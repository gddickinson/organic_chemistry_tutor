"""Tests for Phase 25b — Orbitals (Hückel + W-H) dialog (round 34)."""
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


def test_dialog_instantiates_with_three_tabs(app):
    from orgchem.gui.dialogs.orbitals import OrbitalsDialog
    d = OrbitalsDialog(app.window)
    assert d.tabs.count() == 3
    labels = [d.tabs.tabText(i) for i in range(d.tabs.count())]
    assert "Hückel MOs" in labels
    assert any("Woodward" in lbl for lbl in labels)
    assert any("allowed" in lbl.lower() for lbl in labels)


def test_huckel_tab_populates_for_benzene(app):
    from orgchem.gui.dialogs.orbitals import OrbitalsDialog
    d = OrbitalsDialog(app.window)
    d.huckel_smiles.setText("c1ccccc1")
    d._on_huckel_run()
    # Benzene has 6 π-MOs.
    assert d.huckel_table.rowCount() == 6
    assert d.huckel_save.isEnabled()
    summary = d.huckel_summary.text()
    assert "HOMO" in summary and "LUMO" in summary


def test_huckel_tab_bad_smiles_warns(app, monkeypatch):
    from orgchem.gui.dialogs.orbitals import OrbitalsDialog
    from PySide6.QtWidgets import QMessageBox
    shown = []
    monkeypatch.setattr(QMessageBox, "warning",
                        lambda *a, **kw: shown.append(a[2]) or 0)
    monkeypatch.setattr(QMessageBox, "information",
                        lambda *a, **kw: shown.append(a[2]) or 0)
    d = OrbitalsDialog(app.window)
    d.huckel_smiles.setText("not_a_real_smiles")
    d._on_huckel_run()
    assert shown, "Expected a dialog on bad SMILES"


def test_wh_tab_lists_rules(app):
    from orgchem.gui.dialogs.orbitals import OrbitalsDialog
    from orgchem.core.wh_rules import RULES
    d = OrbitalsDialog(app.window)
    # Default filter "(all)" → every rule in the list.
    assert d.wh_list.count() == len(RULES)
    # Switching to a family shrinks the list.
    for i in range(d.wh_family.count()):
        if d.wh_family.itemData(i) == "cycloaddition":
            d.wh_family.setCurrentIndex(i)
            break
    assert 0 < d.wh_list.count() < len(RULES)


def test_allowed_predicate_thermal_diels_alder(app):
    """Classic teaching case: thermal [4+2] cycloaddition is
    suprafacial-suprafacial allowed."""
    from orgchem.gui.dialogs.orbitals import OrbitalsDialog
    d = OrbitalsDialog(app.window)
    d.pred_kind.setCurrentText("cycloaddition")
    d.pred_electrons.setValue(6)
    d.pred_regime.setCurrentText("thermal")
    d._on_predicate_run()
    text = d.pred_result.text()
    assert "ALLOWED" in text


def test_allowed_predicate_thermal_2plus2_is_forbidden(app):
    from orgchem.gui.dialogs.orbitals import OrbitalsDialog
    d = OrbitalsDialog(app.window)
    d.pred_kind.setCurrentText("cycloaddition")
    d.pred_electrons.setValue(4)
    d.pred_regime.setCurrentText("thermal")
    d._on_predicate_run()
    assert "FORBIDDEN" in d.pred_result.text()


def test_audit_coverage_grew_round_34(app):
    """Five orbitals actions now have GUI entry points."""
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("huckel_mos", "export_mo_diagram",
                 "list_wh_rules", "get_wh_rule",
                 "check_wh_allowed"):
        assert GUI_ENTRY_POINTS.get(name), \
            f"{name} should be wired via the Orbitals dialog"
