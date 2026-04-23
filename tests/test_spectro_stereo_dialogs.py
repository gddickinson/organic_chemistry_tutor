"""Tests for Phase 25b — Spectroscopy + Stereo dialogs (round 37)."""
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


# ---- Spectroscopy ---------------------------------------------------


def test_spectro_dialog_three_tabs(app):
    from orgchem.gui.dialogs.spectroscopy import SpectroscopyDialog
    d = SpectroscopyDialog(app.window)
    assert d.tabs.count() == 3
    labels = [d.tabs.tabText(i) for i in range(d.tabs.count())]
    assert labels == ["IR", "NMR", "MS"]


def test_ir_tab_populates_for_acetic_acid(app):
    from orgchem.gui.dialogs.spectroscopy import SpectroscopyDialog
    d = SpectroscopyDialog(app.window)
    d.ir_smiles.setText("CC(=O)O")
    d._on_ir_run()
    # Acetic acid → carboxylic acid C=O, O-H, C-O bands expected.
    assert d.ir_table.rowCount() > 0


def test_nmr_tab_populates_for_ethyl_acetate(app):
    from orgchem.gui.dialogs.spectroscopy import SpectroscopyDialog
    d = SpectroscopyDialog(app.window)
    d.nmr_smiles.setText("CC(=O)OCC")
    d._on_nmr_run()
    assert d.nmr_table.rowCount() > 0


def test_ms_tab_populates_for_chlorobenzene(app):
    from orgchem.gui.dialogs.spectroscopy import SpectroscopyDialog
    d = SpectroscopyDialog(app.window)
    d.ms_smiles.setText("Clc1ccccc1")
    d._on_ms_run()
    assert d.ms_table.rowCount() > 0
    # Classic chlorine 3:1 isotope signature — at least M and M+2 present.
    assert "monoisotopic" in d.ms_summary.text().lower()


def test_audit_coverage_spectroscopy(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("predict_ir_bands", "export_ir_spectrum",
                 "predict_nmr_shifts", "export_nmr_spectrum",
                 "predict_ms", "export_ms_spectrum"):
        assert GUI_ENTRY_POINTS.get(name), name


# ---- Stereochemistry dialog ---------------------------------------


def test_stereo_dialog_initial_lactate(app):
    from orgchem.gui.dialogs.stereo import StereoDialog
    d = StereoDialog(app.window)
    # Default SMILES is (S)-lactic acid — should have at least one R/S row.
    assert d.table.rowCount() >= 1


def test_stereo_dialog_mirror_changes_smiles(app):
    from orgchem.gui.dialogs.stereo import StereoDialog
    d = StereoDialog(app.window)
    original = d.smiles.text()
    d._on_mirror()
    # For a single stereocentre the enantiomer has a different canonical
    # SMILES.
    assert d.smiles.text() != original


def test_audit_coverage_stereo(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("flip_stereocentre", "enantiomer_of"):
        assert GUI_ENTRY_POINTS.get(name), name
