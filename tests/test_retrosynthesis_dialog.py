"""Tests for Phase 25b — Retrosynthesis dialog wiring (round 33)."""
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


def test_dialog_instantiates(app):
    from orgchem.gui.dialogs.retrosynthesis import RetrosynthesisDialog
    d = RetrosynthesisDialog(app.window)
    assert d.windowTitle().startswith("Retrosynthesis")
    # Two result tabs: single-step / multi-step.
    assert d.tabs.count() == 2


def test_single_step_populates_table(app):
    from orgchem.gui.dialogs.retrosynthesis import RetrosynthesisDialog
    d = RetrosynthesisDialog(app.window)
    d.smiles.setText("CC(=O)Oc1ccccc1C(=O)O")  # aspirin
    d._on_single()
    # At least one ester / acid disconnection expected.
    assert d.single_table.rowCount() >= 1
    assert "disconnection" in d.status.text().lower() or \
        "step" in d.status.text().lower()


def test_multi_step_populates_tree(app):
    from orgchem.gui.dialogs.retrosynthesis import RetrosynthesisDialog
    d = RetrosynthesisDialog(app.window)
    d.smiles.setText("CC(=O)Oc1ccccc1C(=O)O")
    d.max_depth.setValue(2)
    d._on_multi()
    assert d.multi_tree.topLevelItemCount() == 1
    root = d.multi_tree.topLevelItem(0)
    assert root.text(0)   # some label was set


def test_bad_smiles_warns_not_crashes(app, monkeypatch):
    """An invalid SMILES pops a warning dialog but doesn't crash."""
    from orgchem.gui.dialogs.retrosynthesis import RetrosynthesisDialog
    from PySide6.QtWidgets import QMessageBox
    d = RetrosynthesisDialog(app.window)
    d.smiles.setText("not_a_molecule")
    shown = []
    monkeypatch.setattr(QMessageBox, "warning",
                        lambda *a, **kw: shown.append(a[2]) or 0)
    d._on_single()
    assert shown, "Expected a warning dialog for bad SMILES"


def test_audit_coverage_grew_round_33(app):
    """Three retrosynthesis actions now have GUI entry points."""
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("find_retrosynthesis",
                 "list_retro_templates",
                 "find_multi_step_retrosynthesis"):
        assert GUI_ENTRY_POINTS.get(name), \
            f"{name} should now be wired via the Retrosynthesis dialog"
