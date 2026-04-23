"""Tests for round 38 — final 5 audit gaps closed → 100 % GUI coverage."""
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


# ----------------------- Green-metrics dialog ------------------------


def test_green_metrics_dialog_instantiates(app):
    from orgchem.gui.dialogs.green_metrics import GreenMetricsDialog
    d = GreenMetricsDialog(app.window)
    # Round 50 added a third "Compare pathways" tab (Phase 18a orphan).
    assert d.tabs.count() == 3
    labels = {d.tabs.tabText(i) for i in range(d.tabs.count())}
    assert labels == {"Reaction AE", "Pathway AE", "Compare pathways"}
    # Both original combo-lists still populated from the seeded DB.
    assert d.rxn_combo.count() > 0
    assert d.path_combo.count() > 0
    assert d.cmp_list.count() > 0


def test_green_metrics_reaction_computes(app):
    from orgchem.gui.dialogs.green_metrics import GreenMetricsDialog
    d = GreenMetricsDialog(app.window)
    d._on_reaction_run()
    # At minimum, the summary label gained content about the reaction.
    assert d.rxn_combo.currentText() in d.rxn_summary.text() or \
        "reaction" in d.rxn_summary.text().lower()


def test_green_metrics_pathway_computes(app):
    from orgchem.gui.dialogs.green_metrics import GreenMetricsDialog
    d = GreenMetricsDialog(app.window)
    d._on_pathway_run()
    # Summary should mention atom economy.
    assert "atom economy" in d.path_summary.text().lower() or \
        "%" in d.path_summary.text()


# ----------------------- PPI per-pair + chain sequence ---------------


def test_ppi_per_pair_controls_exist(app):
    """Proteins tab → PPI sub-tab should expose chain A / chain B
    combos + 'Analyse pair' button."""
    p = app.window.proteins
    assert hasattr(p, "ppi_chain_a")
    assert hasattr(p, "ppi_chain_b")
    assert hasattr(p, "ppi_pair_btn")


def test_summary_sequence_controls_exist(app):
    """Proteins tab → Summary sub-tab should expose a chain combo +
    Copy sequence button."""
    p = app.window.proteins
    assert hasattr(p, "summary_chain_combo")
    assert hasattr(p, "summary_copy_btn")


# ----------------------- Glossary figure button ---------------------


def test_glossary_view_figure_button_starts_disabled(app):
    """With no term selected, the View-figure button should start
    disabled (it enables once a term with example_smiles is shown)."""
    from orgchem.gui.panels.glossary_panel import GlossaryPanel
    g = GlossaryPanel()
    assert not g.view_figure_btn.isEnabled()


# ----------------------- Coverage gate --------------------------------


def test_gui_audit_hits_100_percent(app):
    """Round 38 goal: no agent action should be agent-only."""
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0, (
        f"Expected 100% GUI coverage; missing: "
        f"{[r['name'] for r in s['missing_actions']]}"
    )
