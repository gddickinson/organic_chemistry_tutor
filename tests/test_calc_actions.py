"""Phase 39c (round 145) — agent-action tests for the
per-solver lab-calculator wrappers.

For each registered ``calc`` action: at least one happy-path
(textbook-value verification) and one error-path (bad input
returns ``{"error": ...}`` rather than raising).
"""
from __future__ import annotations
import math
import os

import pytest


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


# ---- registry sanity ------------------------------------------

def test_calc_category_has_thirty_one_solver_actions():
    """31 per-solver wrappers + 1 dialog opener = 32 total."""
    from orgchem.agent.actions import registry
    calc_names = {n for n, s in registry().items()
                  if s.category == "calc"}
    expected_solvers = {
        # Solution
        "molarity", "dilution", "serial_dilution",
        "molarity_from_mass_percent",
        "ppm_to_molarity", "molarity_to_ppm",
        # Stoichiometry
        "limiting_reagent", "theoretical_yield",
        "percent_yield", "percent_purity",
        # Acid-base
        "ph_from_h", "h_from_ph",
        "pka_to_ka", "ka_to_pka",
        "henderson_hasselbalch",
        # Gas law
        "ideal_gas", "combined_gas_law", "gas_density",
        # Colligative
        "boiling_point_elevation", "freezing_point_depression",
        "osmotic_pressure",
        # Thermo + kinetics
        "heat_capacity", "hess_law_sum",
        "first_order_half_life", "first_order_integrated",
        "arrhenius", "eyring_rate_constant",
        # Equilibrium
        "equilibrium_constant", "ksp_from_solubility",
        "solubility_from_ksp", "ice_solve_a_plus_b",
        # Dialog opener
        "open_lab_calculator",
    }
    missing = expected_solvers - calc_names
    assert not missing, f"missing actions: {missing}"


# ---- Solution / dilution --------------------------------------

def test_action_molarity_solves_for_mass(app):
    """0.5 M × 1 L × 58.44 g/mol → 29.22 g (NaCl)."""
    r = app.call("molarity",
                 molarity_M=0.5, volume_L=1.0,
                 molecular_weight_gmol=58.44)
    assert math.isclose(r["mass_g"], 29.22, rel_tol=1e-3)


def test_action_molarity_error_path(app):
    r = app.call("molarity", molarity_M=0.5)  # 3 missing
    assert "error" in r


def test_action_dilution(app):
    r = app.call("dilution", M1=1.0, V1=10.0, M2=0.1)
    assert math.isclose(r["V2"], 100.0, rel_tol=1e-9)


def test_action_serial_dilution(app):
    r = app.call("serial_dilution",
                 initial_concentration=1.0,
                 dilution_factor=10.0, n_steps=3)
    assert math.isclose(r["final_concentration"], 1e-3,
                        rel_tol=1e-9)
    assert len(r["concentrations"]) == 4


def test_action_molarity_from_mass_percent(app):
    """Concentrated HCl: 37 % w/w · 1.18 g/mL ÷ 36.46 ≈ 12 M."""
    r = app.call("molarity_from_mass_percent",
                 mass_percent=37.0,
                 density_g_per_mL=1.18,
                 molecular_weight_gmol=36.46)
    assert math.isclose(r["molarity_M"], 11.97, rel_tol=1e-2)


def test_action_ppm_round_trip(app):
    """100 ppm of MW 100 → 0.001 M → 100 ppm."""
    a = app.call("ppm_to_molarity", ppm=100.0,
                 molecular_weight_gmol=100.0)
    assert math.isclose(a["molarity_M"], 0.001, rel_tol=1e-9)
    b = app.call("molarity_to_ppm",
                 molarity_M=a["molarity_M"],
                 molecular_weight_gmol=100.0)
    assert math.isclose(b["ppm"], 100.0, rel_tol=1e-9)


# ---- Stoichiometry --------------------------------------------

def test_action_limiting_reagent(app):
    r = app.call("limiting_reagent", reagents=[
        {"name": "A", "moles": 1.0, "stoich_coeff": 1.0},
        {"name": "B", "moles": 1.0, "stoich_coeff": 2.0},
    ])
    assert r["limiting_name"] == "B"


def test_action_theoretical_yield(app):
    """2 mol limiting (coeff 1) → 2 mol product (coeff 1) ×
    MW 100 = 200 g."""
    r = app.call("theoretical_yield",
                 limiting_moles=2.0,
                 limiting_stoich_coeff=1.0,
                 product_stoich_coeff=1.0,
                 product_mw_gmol=100.0)
    assert math.isclose(r["theoretical_yield_g"], 200.0,
                        rel_tol=1e-9)


def test_action_percent_yield(app):
    r = app.call("percent_yield",
                 actual_yield_g=8.0,
                 theoretical_yield_g=10.0)
    assert math.isclose(r["percent"], 80.0, rel_tol=1e-9)


def test_action_percent_purity_error_over_100(app):
    r = app.call("percent_purity",
                 pure_mass_g=10.0, sample_mass_g=8.0)
    assert "error" in r


# ---- Acid-base ------------------------------------------------

def test_action_ph_from_h_neutral(app):
    r = app.call("ph_from_h", h_concentration_M=1e-7)
    assert math.isclose(r["pH"], 7.0, rel_tol=1e-9)


def test_action_h_from_ph(app):
    r = app.call("h_from_ph", pH=3.0)
    assert math.isclose(r["h_concentration_M"], 1e-3,
                        rel_tol=1e-9)


def test_action_pka_ka_round_trip(app):
    a = app.call("pka_to_ka", pKa=4.76)
    b = app.call("ka_to_pka", Ka=a["Ka"])
    assert math.isclose(b["pKa"], 4.76, rel_tol=1e-9)


def test_action_henderson_hasselbalch(app):
    """At [A⁻]/[HA] = 1, pH = pKa."""
    r = app.call("henderson_hasselbalch",
                 pKa=4.76, base_acid_ratio=1.0)
    assert math.isclose(r["pH"], 4.76, rel_tol=1e-9)


# ---- Gas laws -------------------------------------------------

def test_action_ideal_gas_stp(app):
    """1 mol at STP → 22.414 L."""
    r = app.call("ideal_gas", pressure_atm=1.0,
                 moles=1.0, temperature_K=273.15)
    assert math.isclose(r["volume_L"], 22.414, rel_tol=1e-3)


def test_action_combined_gas_law(app):
    """Boyle's law: P1V1=P2V2 (T fixed)."""
    r = app.call("combined_gas_law",
                 P1=1.0, V1=10.0, T1=300.0,
                 P2=2.0, T2=300.0)
    assert math.isclose(r["V2"], 5.0, rel_tol=1e-9)


def test_action_gas_density(app):
    """O₂ at STP: 32 / 22.4 ≈ 1.428 g/L."""
    r = app.call("gas_density", pressure_atm=1.0,
                 molecular_weight_gmol=32.0,
                 temperature_K=273.15)
    assert math.isclose(r["density_g_per_L"], 1.428,
                        rel_tol=1e-2)


# ---- Colligative ----------------------------------------------

def test_action_boiling_point_elevation_solvent(app):
    """1 m sucrose (i=1) in water → ΔTb = 0.512 °C."""
    r = app.call("boiling_point_elevation",
                 solvent="water", molality_b=1.0,
                 van_t_hoff_i=1.0)
    assert math.isclose(r["delta_T_b"], 0.512, rel_tol=1e-3)


def test_action_freezing_point_nacl(app):
    """1 m NaCl (i=2) in water → ΔTf = 3.72 °C."""
    r = app.call("freezing_point_depression",
                 solvent="water", molality_b=1.0,
                 van_t_hoff_i=2.0)
    assert math.isclose(r["delta_T_f"], 3.72, rel_tol=1e-3)


def test_action_osmotic_pressure(app):
    """0.15 M NaCl (i=2) at 310 K → ~7.63 atm (isotonic)."""
    r = app.call("osmotic_pressure",
                 molarity_M=0.15, temperature_K=310.0,
                 van_t_hoff_i=2.0)
    assert math.isclose(r["pressure_atm"], 7.628, rel_tol=1e-2)


def test_action_freezing_point_unknown_solvent(app):
    r = app.call("freezing_point_depression",
                 solvent="unobtainium",
                 molality_b=1.0, van_t_hoff_i=1.0)
    assert "error" in r


# ---- Thermo + kinetics -----------------------------------------

def test_action_heat_capacity(app):
    """100 g water 20→30 °C: q = 100·4.184·10 = 4184 J."""
    r = app.call("heat_capacity",
                 mass_g=100.0,
                 specific_heat_J_per_g_K=4.184,
                 delta_T_K=10.0)
    assert math.isclose(r["heat_q_J"], 4184.0, rel_tol=1e-9)


def test_action_hess_law_sum(app):
    r = app.call("hess_law_sum",
                 step_delta_H_kJ=[-100.0, +50.0, -25.0])
    assert math.isclose(r["total_delta_H_kJ"], -75.0,
                        rel_tol=1e-9)


def test_action_first_order_half_life(app):
    """k = 0.05 /s → t½ = ln 2 / 0.05 ≈ 13.86 s."""
    r = app.call("first_order_half_life",
                 rate_constant_per_s=0.05)
    assert math.isclose(r["half_life_s"], math.log(2) / 0.05,
                        rel_tol=1e-9)


def test_action_first_order_integrated(app):
    """[A]_0 = 1, k = 0.1, t = 10 → [A] = e^-1."""
    r = app.call("first_order_integrated",
                 initial_concentration=1.0,
                 rate_constant_per_s=0.1, time_s=10.0)
    assert math.isclose(r["final_concentration"],
                        math.exp(-1), rel_tol=1e-9)


def test_action_arrhenius(app):
    """k = 1e10 · exp(-50000 / (8.314 · 300))."""
    r = app.call("arrhenius",
                 pre_exponential_A=1e10,
                 activation_energy_J_per_mol=50000.0,
                 temperature_K=300.0)
    expected = 1e10 * math.exp(-50000.0 / (8.314462618 * 300.0))
    assert math.isclose(r["rate_constant"], expected,
                        rel_tol=1e-9)


def test_action_eyring_rate_constant(app):
    r = app.call("eyring_rate_constant",
                 delta_G_double_dagger_J_per_mol=80000.0,
                 temperature_K=300.0)
    assert r["rate_constant"] > 0
    assert r["prefactor_kB_T_over_h"] > 0


# ---- Equilibrium ----------------------------------------------

def test_action_equilibrium_constant(app):
    """A ⇌ B, [A] = 1, [B] = 2 → K = 2.0."""
    r = app.call("equilibrium_constant", species=[
        {"name": "A", "concentration_M": 1.0,
         "stoich_coeff": 1.0, "side": "reactant"},
        {"name": "B", "concentration_M": 2.0,
         "stoich_coeff": 1.0, "side": "product"},
    ])
    assert math.isclose(r["K_eq"], 2.0, rel_tol=1e-9)


def test_action_ksp_round_trip_agcl(app):
    """AgCl: s = 1.3e-5 → K_sp = 1.69e-10 → s = 1.3e-5."""
    a = app.call("ksp_from_solubility",
                 molar_solubility=1.3e-5, n=1, m=1)
    assert math.isclose(a["K_sp"], 1.69e-10, rel_tol=1e-6)
    b = app.call("solubility_from_ksp",
                 K_sp=a["K_sp"], n=1, m=1)
    assert math.isclose(b["molar_solubility"], 1.3e-5,
                        rel_tol=1e-3)


def test_action_ksp_pbi2(app):
    """PbI₂: K_sp = 4·s³."""
    s = 1.5e-3
    r = app.call("ksp_from_solubility",
                 molar_solubility=s, n=1, m=2)
    expected = 4 * s ** 3
    assert math.isclose(r["K_sp"], expected, rel_tol=1e-9)


def test_action_ice_solve_basic(app):
    """A + B ⇌ C + D with K = 1, A₀ = B₀ = 1 → x = 0.5."""
    r = app.call("ice_solve_a_plus_b",
                 K=1.0, initial_A=1.0, initial_B=1.0)
    assert math.isclose(r["extent_x"], 0.5, rel_tol=1e-6)


def test_action_ice_solve_error_path(app):
    """Both reactants at zero → error."""
    r = app.call("ice_solve_a_plus_b",
                 K=1.0, initial_A=0.0, initial_B=0.0)
    assert "error" in r
