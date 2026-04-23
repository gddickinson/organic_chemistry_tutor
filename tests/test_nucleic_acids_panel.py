"""Tests for Phase 29c Nucleic-acids tab panel."""
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
    """Phase 30 moved the NA panel into the Macromolecules window."""
    win = app.window
    main_labels = [win.tabs.tabText(i) for i in range(win.tabs.count())]
    assert "Nucleic acids" not in main_labels, main_labels
    mw = win.open_macromolecules_window()
    inner = [mw.tabs.tabText(i) for i in range(mw.tabs.count())]
    assert "Nucleic acids" in inner, inner


def test_panel_populates_full_catalogue(app):
    from orgchem.core.nucleic_acids import NUCLEIC_ACIDS
    panel = app.window.nucleic_acids
    assert panel.entry_list.count() == len(NUCLEIC_ACIDS)


def test_family_filter_nucleobases(app):
    panel = app.window.nucleic_acids
    for i in range(panel.family_combo.count()):
        if panel.family_combo.itemData(i) == "nucleobase":
            panel.family_combo.setCurrentIndex(i)
            break
    from orgchem.core.nucleic_acids import NUCLEIC_ACIDS
    expected = sum(1 for n in NUCLEIC_ACIDS if n.family == "nucleobase")
    assert panel.entry_list.count() == expected
    panel.family_combo.setCurrentIndex(0)


def test_free_text_filter_pdb(app):
    panel = app.window.nucleic_acids
    panel.filter.setText("tRNA")
    # At least one tRNA motif in the catalogue.
    assert panel.entry_list.count() >= 1
    panel.filter.clear()


def test_pdb_entry_enables_fetch_button(app):
    """PDB motif entries should turn the fetch button on but disable
    Copy SMILES (no SMILES)."""
    panel = app.window.nucleic_acids
    # Find the first pdb-motif entry by family.
    for i in range(panel.entry_list.count()):
        panel.entry_list.setCurrentRow(i)
        entry = panel._current_entry()
        if entry is not None and entry.family == "pdb-motif":
            assert panel.fetch_btn.isEnabled()
            assert panel.copy_btn.isEnabled() is bool(entry.smiles)
            break
    else:
        pytest.skip("No pdb-motif entry seeded")


def test_smiles_entry_enables_copy(app):
    """Entries with a SMILES render + allow clipboard copy."""
    panel = app.window.nucleic_acids
    # Find first nucleobase (has SMILES).
    for i in range(panel.entry_list.count()):
        panel.entry_list.setCurrentRow(i)
        entry = panel._current_entry()
        if entry is not None and entry.smiles:
            assert panel.copy_btn.isEnabled()
            panel._on_copy_smiles()  # should not raise
            break


def test_audit_entries_point_at_panel(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("list_nucleic_acids", "get_nucleic_acid",
                 "nucleic_acid_families"):
        entry = GUI_ENTRY_POINTS.get(name, "")
        assert "Nucleic acids tab" in entry, entry


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
