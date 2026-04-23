"""Tests for Phase 15a-lite — recrystallisation / distillation / extraction."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---- Recrystallisation ------------------------------------------------

def test_solubility_curve_monotonic_in_T():
    from orgchem.core.lab_techniques import solubility_curve
    curve = solubility_curve(s_hot_g_per_100ml=30, s_cold_g_per_100ml=2,
                             t_hot_c=80, t_cold_c=5, n_points=10)
    temps = [t for t, _ in curve]
    sols = [s for _, s in curve]
    # strictly increasing in T
    assert temps == sorted(temps)
    assert sols == sorted(sols)


def test_solubility_curve_anchor_values():
    from orgchem.core.lab_techniques import solubility_curve
    curve = solubility_curve(30, 2, t_hot_c=80, t_cold_c=5, n_points=20)
    # first and last match the anchors (within fitting tolerance)
    assert abs(curve[0][0] - 5) < 0.1
    assert abs(curve[0][1] - 2) < 0.05
    assert abs(curve[-1][0] - 80) < 0.1
    assert abs(curve[-1][1] - 30) < 0.05


def test_recrystallisation_yield_typical():
    """10 g crude in 30 mL; hot s = 50 g/100 mL; cold s = 2 g/100 mL →
    crystals = 10 − (2 × 30 / 100) = 9.4 g → yield ~94%."""
    from orgchem.core.lab_techniques import recrystallisation_yield
    r = recrystallisation_yield(s_hot=50, s_cold=2,
                                m_crude_g=10, solvent_volume_ml=30)
    assert "error" not in r
    assert abs(r["crystals_g"] - 9.4) < 0.1
    assert abs(r["yield_pct"] - 94) < 1.0


def test_recrystallisation_insoluble_at_hot_fails():
    from orgchem.core.lab_techniques import recrystallisation_yield
    r = recrystallisation_yield(s_hot=5, s_cold=1,
                                m_crude_g=100, solvent_volume_ml=10)
    assert "error" in r


def test_recrystallisation_too_soluble_cold_fails():
    from orgchem.core.lab_techniques import recrystallisation_yield
    # cold solubility is so high that nothing crystallises
    r = recrystallisation_yield(s_hot=50, s_cold=40,
                                m_crude_g=10, solvent_volume_ml=100)
    assert "error" in r


# ---- Distillation -----------------------------------------------------

def test_distillation_simple_for_big_delta():
    from orgchem.core.lab_techniques import distillation_plan
    r = distillation_plan(("Water", "Diethyl ether"))
    # ΔTb ≈ 65 °C — simple distillation
    assert "error" not in r
    assert r["technique"] == "simple distillation"
    assert r["delta_c"] > 25


def test_distillation_fractional_for_medium_delta():
    from orgchem.core.lab_techniques import distillation_plan
    r = distillation_plan(("Methanol", "Ethanol"))
    # bps 64.7, 78.4 → Δ ≈ 14 → fractional
    assert "error" not in r
    assert r["technique"] == "fractional distillation"
    assert 5 <= r["delta_c"] < 25


def test_distillation_not_for_small_delta():
    from orgchem.core.lab_techniques import distillation_plan
    # Benzene 80.1 vs Acetonitrile 81.6 — ΔTb ≈ 1.5
    r = distillation_plan(("Benzene", "Acetonitrile"))
    assert "error" not in r
    assert "chromatography" in r["technique"].lower() \
        or "not distillable" in r["technique"].lower()


def test_distillation_missing_bp():
    from orgchem.core.lab_techniques import distillation_plan
    r = distillation_plan(("Morphine", "Ethanol"))
    assert "error" in r


# ---- Acid-base extraction ---------------------------------------------

def test_fraction_ionised_at_pka_is_half():
    from orgchem.core.lab_techniques import fraction_ionised
    # At pH = pKa the acid should be 50% ionised
    assert abs(fraction_ionised(pka=4.76, ph=4.76, is_acid=True) - 0.5) < 1e-6


def test_acidic_drug_partitions_correctly():
    """Aspirin-like carboxylic acid (pKa 3.5): at pH 1 goes organic, at pH 7
    goes aqueous."""
    from orgchem.core.lab_techniques import extraction_plan
    low = extraction_plan(pka=3.5, ph=1.0, is_acid=True)
    high = extraction_plan(pka=3.5, ph=7.0, is_acid=True)
    assert low["preferred_phase"] == "organic"
    assert high["preferred_phase"] == "aqueous"


def test_basic_amine_partitions_correctly():
    """Amine (pKa of conjugate acid 10): at pH 13 goes organic, at pH 3 goes aqueous."""
    from orgchem.core.lab_techniques import extraction_plan
    low = extraction_plan(pka=10.0, ph=3.0, is_acid=False)
    high = extraction_plan(pka=10.0, ph=13.0, is_acid=False)
    assert low["preferred_phase"] == "aqueous"
    assert high["preferred_phase"] == "organic"


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_recrystallisation_yield_action(app):
    r = app.call("recrystallisation_yield",
                 s_hot=50.0, s_cold=2.0,
                 m_crude_g=10.0, solvent_volume_ml=30.0)
    assert "error" not in r
    assert r["yield_pct"] > 80


def test_distillation_plan_action(app):
    r = app.call("distillation_plan",
                 component_a="Water", component_b="Ethanol")
    assert "error" not in r
    # ΔTb ≈ 21.6 → fractional
    assert r["technique"] == "fractional distillation"


def test_extraction_plan_action(app):
    r = app.call("extraction_plan", pka=3.5, ph=1.0, is_acid=True,
                 smiles="CC(=O)Oc1ccccc1C(=O)O")
    assert "error" not in r
    assert r["preferred_phase"] == "organic"
    assert r["logp_neutral"] is not None
