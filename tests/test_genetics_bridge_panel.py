"""Phase GM-1.0 (round 230) — GUI smoke tests for
``MolecularBiologyBridgePanel``.
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


def test_panel_constructs(app):
    from genetics.gui.panels.molecular_biology_bridge_panel import (
        MolecularBiologyBridgePanel,
    )
    panel = MolecularBiologyBridgePanel()
    # BC-1.0 currently catalogues only ``dna-ligase-i`` as a
    # nucleic-acid enzyme; the panel must populate with at
    # least that one entry.
    assert panel.list_widget.count() >= 1


def test_filter_helper_returns_only_nucleic_acid_enzymes():
    """The ``filtered_nucleic_acid_enzymes`` helper must
    return enzymes whose id, name, or related fields contain
    a nucleic-acid keyword (polymerase / ligase / restriction
    / nuclease / etc.)."""
    from genetics.gui.panels.molecular_biology_bridge_panel import (
        filtered_nucleic_acid_enzymes,
    )
    es = filtered_nucleic_acid_enzymes()
    assert len(es) >= 1
    keywords = (
        "polymerase", "ligase", "restriction",
        "endonuclease", "exonuclease", "nuclease",
        "topoisomerase", "helicase", "transcriptase",
        "primase", "telomerase", "integrase",
        "recombinase",
    )
    for e in es:
        haystack = " ".join([
            e.id, e.name, e.ec_number, str(e.ec_class),
            e.mechanism_class, e.notes,
        ] + list(e.substrates) + list(e.products)).lower()
        assert any(k in haystack for k in keywords), \
            f"Enzyme {e.id!r} doesn't match any nucleic-acid keyword"


def test_dna_ligase_in_filtered_list():
    """DNA ligase I (the canonical BC-1.0 nucleic-acid enzyme)
    must always appear in the bridge panel."""
    from genetics.gui.panels.molecular_biology_bridge_panel import (
        filtered_nucleic_acid_enzymes,
    )
    ids = {e.id for e in filtered_nucleic_acid_enzymes()}
    assert "dna-ligase-i" in ids


def test_select_enzyme_focuses_row(app):
    from genetics.gui.panels.molecular_biology_bridge_panel import (
        MolecularBiologyBridgePanel,
    )
    panel = MolecularBiologyBridgePanel()
    assert panel.select_enzyme("dna-ligase-i") is True


def test_select_unknown_returns_false(app):
    from genetics.gui.panels.molecular_biology_bridge_panel import (
        MolecularBiologyBridgePanel,
    )
    panel = MolecularBiologyBridgePanel()
    assert panel.select_enzyme("not-an-enzyme") is False


def test_detail_card_renders(app):
    from genetics.gui.panels.molecular_biology_bridge_panel import (
        MolecularBiologyBridgePanel,
    )
    panel = MolecularBiologyBridgePanel()
    panel.select_enzyme("dna-ligase-i")
    html = panel.detail.toHtml()
    assert "DNA ligase" in html
