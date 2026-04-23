"""Headless smoke test: app launches, seeds, and reacts to an agent action.

This test exercises the same code path a Claude Code / external LLM session
uses when driving the app as a subprocess. If it passes, the end-to-end
"LLM drives the GUI" pipeline works.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("PySide6")


@pytest.fixture(scope="module")
def app():
    # Force offscreen before any Qt import.
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        yield h


def test_database_seeded_with_reference_compounds(app):
    rows = app.call("list_all_molecules")
    names = {r["name"] for r in rows}
    # A sample from the Verma et al. reference set
    for expected in ("Caffeine", "Nicotine", "D-Glucose", "Cholesterol"):
        assert expected in names, f"seed missing {expected!r}"


def test_database_seeded_with_phase6_content(app):
    """Phase 6 content expansion: amino acids, drugs, solvents, natural products."""
    rows = app.call("list_all_molecules")
    names = {r["name"] for r in rows}
    for category in (
        ("Glycine", "L-Alanine", "L-Tryptophan"),        # amino acids
        ("Aspirin", "Ibuprofen", "Acetaminophen"),       # drugs
        ("DMSO", "DMF", "THF"),                          # solvents
        ("Menthol", "Salicylic acid", "Vanillin"),       # natural products
    ):
        for name in category:
            assert name in names, f"Phase-6 seed missing {name!r}"
    assert len(rows) >= 40   # 20 original + 20 Phase-6


def test_database_seeded_with_extended_molecules(app):
    """Phase 6a molecule expansion: 20 amino acids, reagents, drugs,
    biomolecules, dyes, PAHs, heterocycles, and functional-group ladder."""
    rows = app.call("list_all_molecules")
    names = {r["name"] for r in rows}
    # Spot-check one canonical molecule from each major category
    for expected in (
        "L-Valine", "L-Lysine", "L-Arginine", "L-Histidine",   # amino acids
        "LDA", "DBU", "Acetic anhydride",                      # reagents
        "Penicillin G", "Atorvastatin", "Sildenafil",          # drugs
        "Adenosine", "Palmitic acid", "Testosterone",          # biomolecules
        "Indigo", "Crystal violet",                            # dyes
        "Naphthalene", "Pyrene",                               # PAHs
        "Pyridine", "Indole", "Piperidine",                    # heterocycles
        "Pentane", "Phenol", "Benzoic acid",                   # ladder
    ):
        assert expected in names, f"extended-seed missing {expected!r}"
    assert len(rows) >= 200, f"expected ≥200 molecules, got {len(rows)}"


def test_show_molecule_emits_selection(app):
    calls: list[int] = []
    from orgchem.messaging.bus import bus
    bus().molecule_selected.connect(lambda mid: calls.append(int(mid)))

    result = app.call("show_molecule", name_or_id="Caffeine")
    assert "id" in result
    assert calls, "molecule_selected signal never fired"
    assert calls[-1] == result["id"]


def test_formula_tool_roundtrip(app):
    r = app.call(
        "calculate_empirical_formula",
        percentages={"C": 74.00, "H": 8.70, "N": 17.27},
        molar_mass=162.0,
    )
    assert r["empirical_formula"] == "C5H7N"
    assert r["molecular_formula"] == "C10H14N2"
