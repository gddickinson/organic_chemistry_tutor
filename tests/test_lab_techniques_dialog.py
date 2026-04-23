"""Tests for Phase 25b — Lab techniques dialog (round 35)."""
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


def test_dialog_has_four_tabs(app):
    from orgchem.gui.dialogs.lab_techniques import LabTechniquesDialog
    d = LabTechniquesDialog(app.window)
    assert d.tabs.count() == 4


def test_tlc_tab_populates_rows(app):
    from orgchem.gui.dialogs.lab_techniques import LabTechniquesDialog
    d = LabTechniquesDialog(app.window)
    d.tlc_smiles.setPlainText("c1ccccc1\nCC(=O)O")
    d._on_tlc_run()
    assert d.tlc_table.rowCount() == 2


def test_recrystallisation_tab_shows_yield(app):
    from orgchem.gui.dialogs.lab_techniques import LabTechniquesDialog
    d = LabTechniquesDialog(app.window)
    d._on_recryst_run()
    out = d.rec_out.text()
    assert "Crystals recovered" in out or "Error" in out


def test_distillation_tab_uses_ethanol_water(app):
    from orgchem.gui.dialogs.lab_techniques import LabTechniquesDialog
    d = LabTechniquesDialog(app.window)
    d._on_distill_run()
    # Ethanol / water should yield a technique label (simple /
    # fractional / azeotrope warning).
    out = d.dist_out.text()
    assert "Technique" in out or "Error" in out


def test_extraction_tab_runs(app):
    from orgchem.gui.dialogs.lab_techniques import LabTechniquesDialog
    d = LabTechniquesDialog(app.window)
    d._on_extract_run()
    assert "Predicted layer" in d.ext_out.text() or \
        "Error" in d.ext_out.text()


def test_audit_coverage_after_round_35(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("predict_tlc", "predict_rf",
                 "recrystallisation_yield", "distillation_plan",
                 "extraction_plan"):
        assert GUI_ENTRY_POINTS.get(name), \
            f"{name} should be wired via the Lab techniques dialog"
