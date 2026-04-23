"""Tests for Phase 17e physical-organic helpers (round 55)."""
from __future__ import annotations
import math

import pytest

pytest.importorskip("rdkit")


# ---- hammett_fit --------------------------------------------------

def test_hammett_fit_positive_rho():
    """Benzoic-acid ionisation — the canonical positive-ρ reaction
    (electron-withdrawing groups stabilise the carboxylate).
    Textbook ρ ≈ +1 for ionisation in water at 25 °C."""
    from orgchem.core.physical_organic import hammett_fit
    # Synthetic: log(K/K₀) = 1.0·σ_p (exact, so r² = 1).
    data = {"H": 0.00, "CH3": -0.17, "Cl": 0.23, "NO2": 0.78,
            "OH": -0.37, "OCH3": -0.27}
    res = hammett_fit(data, sigma_type="sigma_p")
    assert "error" not in res, res
    assert abs(res["rho"] - 1.0) < 0.02
    assert res["r_squared"] > 0.99
    assert "ρ > 0" in res["interpretation"]


def test_hammett_fit_negative_rho():
    """SN1 on benzhydryl chlorides — EDGs *accelerate* ionisation
    (ρ ≈ −4). Synthetic data with slope −4."""
    from orgchem.core.physical_organic import hammett_fit
    data = {"H": 0.00, "CH3": 1.24, "OCH3": 3.12,
            "CF3": -2.16, "NO2": -3.12}
    res = hammett_fit(data, sigma_type="sigma_p_plus")
    assert res["rho"] < 0
    assert "ρ < 0" in res["interpretation"]


def test_hammett_fit_rejects_too_few_points():
    from orgchem.core.physical_organic import hammett_fit
    res = hammett_fit({"H": 0.0}, sigma_type="sigma_p")
    assert "error" in res


def test_hammett_fit_skips_unknown_substituent():
    from orgchem.core.physical_organic import hammett_fit
    data = {"H": 0.0, "NO2": 0.78, "CH3": -0.17,
            "bogus-group": 5.5}
    res = hammett_fit(data, sigma_type="sigma_p")
    assert "error" not in res
    # Only 3 known rows survived the filter.
    assert res["n_points"] == 3


def test_list_hammett_substituents_includes_classical_EDG_EWG():
    from orgchem.core.physical_organic import list_hammett_substituents
    cat = list_hammett_substituents()
    for must in ("NO2", "NH2", "CH3", "OH", "Cl", "CF3", "H"):
        assert must in cat
        for key in ("sigma_m", "sigma_p",
                    "sigma_p_minus", "sigma_p_plus"):
            assert key in cat[must]


# ---- predict_kie --------------------------------------------------

def test_predict_kie_HD_298K_in_textbook_range():
    """Textbook primary C–H/C–D KIE at 298 K is ~6.5–7.0 for a
    C–H stretch at 3000 cm⁻¹. Bigeleisen formula + light carbon
    partner should land in that window."""
    from orgchem.core.physical_organic import predict_kie
    res = predict_kie(isotope_pair="H/D", partner_element="C",
                      nu_H_cm1=3000.0, temperature_K=298.15)
    assert "error" not in res
    assert 5.0 <= res["kie"] <= 9.0, res["kie"]
    assert "primary" in res["interpretation"].lower()


def test_predict_kie_HT_larger_than_HD():
    """H/T KIE is bigger than H/D at the same T and ν."""
    from orgchem.core.physical_organic import predict_kie
    r_hd = predict_kie(isotope_pair="H/D")
    r_ht = predict_kie(isotope_pair="H/T")
    assert r_ht["kie"] > r_hd["kie"]


def test_predict_kie_higher_temperature_smaller_kie():
    """Raising the temperature damps the ZPE advantage — KIE
    shrinks (Eyring intuition)."""
    from orgchem.core.physical_organic import predict_kie
    cold = predict_kie(temperature_K=250.0)
    hot = predict_kie(temperature_K=400.0)
    assert cold["kie"] > hot["kie"]


def test_predict_kie_unknown_pair_errors():
    from orgchem.core.physical_organic import predict_kie
    res = predict_kie(isotope_pair="bogus")
    assert "error" in res


# ---- agent-action integration ------------------------------------

def test_hammett_fit_agent_action():
    from orgchem.agent.actions import invoke
    res = invoke("hammett_fit",
                 data={"H": 0.0, "NO2": 0.78, "OCH3": -0.27,
                       "CH3": -0.17, "Cl": 0.23})
    assert "rho" in res
    assert math.isfinite(res["rho"])


def test_predict_kie_agent_action():
    from orgchem.agent.actions import invoke
    res = invoke("predict_kie", isotope_pair="H/D")
    assert 5.0 <= res["kie"] <= 9.0


def test_list_hammett_substituents_agent_action():
    from orgchem.agent.actions import invoke
    res = invoke("list_hammett_substituents")
    assert "substituents" in res
    assert "NO2" in res["substituents"]


def test_hammett_kie_in_list_capabilities_under_phys_org():
    from orgchem.agent.actions import invoke
    res = invoke("list_capabilities", category="phys-org")
    assert "error" not in res
    names = [a["name"] for a in res["actions"]]
    assert "hammett_fit" in names
    assert "predict_kie" in names


def test_phys_org_audit_entries_present():
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("hammett_fit", "predict_kie",
                 "list_hammett_substituents"):
        assert GUI_ENTRY_POINTS.get(name, ""), name


def test_gui_coverage_still_100():
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
