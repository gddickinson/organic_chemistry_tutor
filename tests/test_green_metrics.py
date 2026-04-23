"""Tests for Phase 17a / 18a — green-chemistry metrics."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---- Core module ----------------------------------------------------

def test_mol_weight_basic():
    from orgchem.core.green_metrics import mol_weight
    # Water: 18.010 u
    assert abs(mol_weight("O") - 18.01) < 0.1
    # Ethanol: 46.042
    assert abs(mol_weight("CCO") - 46.04) < 0.1


def test_mol_weight_bad_smiles_returns_zero():
    from orgchem.core.green_metrics import mol_weight
    assert mol_weight("not a molecule") == 0.0


def test_atom_economy_diels_alder_is_100():
    """Concerted DA has no byproducts — textbook AE = 100%."""
    from orgchem.core.green_metrics import atom_economy
    r = atom_economy("C=CC=C.C=C>>C1CCCC=C1")
    assert abs(r["atom_economy"] - 100.0) < 0.1


def test_atom_economy_fischer_esterification():
    """AcOH + EtOH → EtOAc + H2O; AE = 88/(60+46) ≈ 83%."""
    from orgchem.core.green_metrics import atom_economy
    r = atom_economy("CC(=O)O.CCO>>CCOC(=O)C.O")
    assert 80.0 < r["atom_economy"] < 86.0
    # Desired product auto-picked as the heaviest — should be the ester
    assert r["desired_product"] == "CCOC(=O)C"


def test_atom_economy_bromination_benzene_around_66():
    """PhH + Br2 → PhBr + HBr; AE ≈ 66%."""
    from orgchem.core.green_metrics import atom_economy
    r = atom_economy("c1ccccc1.BrBr>>Brc1ccccc1.Br")
    assert 63.0 < r["atom_economy"] < 70.0


def test_atom_economy_no_arrow_is_error():
    from orgchem.core.green_metrics import atom_economy
    r = atom_economy("CCO")
    assert "error" in r


def test_atom_economy_explicit_product_index():
    """Selecting the wrong product fragment (water) gives low AE."""
    from orgchem.core.green_metrics import atom_economy
    # Water is the second product (index 1) in Fischer esterification.
    r = atom_economy("CC(=O)O.CCO>>CCOC(=O)C.O", product_index=1)
    assert r["desired_product"] == "O"
    assert r["atom_economy"] < 25.0


def test_e_factor_basic():
    from orgchem.core.green_metrics import e_factor
    r = e_factor(mass_inputs=100.0, mass_product=40.0)
    assert r["e_factor"] == 1.5
    assert r["pmi"] == 2.5


def test_e_factor_validates_inputs():
    from orgchem.core.green_metrics import e_factor
    assert "error" in e_factor(mass_inputs=100.0, mass_product=0.0)
    assert "error" in e_factor(mass_inputs=10.0, mass_product=50.0)


def test_pathway_atom_economy_multiplies_fractions():
    """Two 50% steps → 25% overall."""
    from orgchem.core.green_metrics import pathway_atom_economy
    # Fabricate two pathways that each have ~50% AE
    # A + B → C + waste  where MW(C) = 50% of MW(A)+MW(B)
    # Hard to construct with real SMILES; instead test by faking via
    # the public helpers — assert the multiplicative property using
    # the Fischer reaction twice (83% × 83% ≈ 69%).
    steps = ["CC(=O)O.CCO>>CCOC(=O)C.O"] * 2
    r = pathway_atom_economy(steps)
    assert 65.0 < r["overall_atom_economy"] < 75.0
    assert len(r["step_atom_economies"]) == 2


def test_pathway_atom_economy_empty_is_error():
    from orgchem.core.green_metrics import pathway_atom_economy
    assert "error" in pathway_atom_economy([])


# ---- Agent actions --------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_reaction_atom_economy_action_diels_alder(app):
    rows = app.call("list_reactions", filter="Diels-Alder")
    assert rows
    r = app.call("reaction_atom_economy", reaction_id=rows[0]["id"])
    assert "error" not in r
    assert abs(r["atom_economy"] - 100.0) < 0.1


def test_reaction_atom_economy_missing_id(app):
    r = app.call("reaction_atom_economy", reaction_id=99_999)
    assert "error" in r


def test_pathway_green_metrics_bhc_is_greenest(app):
    """BHC ibuprofen is specifically designed as a >70% atom-economy route."""
    rows = app.call("list_pathways", filter="BHC")
    assert rows
    r = app.call("pathway_green_metrics", pathway_id=rows[0]["id"])
    assert "error" not in r
    overall = r["overall"]["overall_atom_economy"]
    assert overall > 70.0, f"BHC overall AE should be >70%, got {overall}"
    # 3-step route
    assert len(r["per_step"]) == 3


def test_pathway_green_metrics_missing_id(app):
    r = app.call("pathway_green_metrics", pathway_id=99_999)
    assert "error" in r
