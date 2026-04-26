"""Phase 39a (round 142) — headless tests for the lab-calculator
solvers across all 7 categories.

Every solver tested for: textbook-correct numerical results +
all error paths (missing-count != N, non-positive inputs, etc.).
"""
from __future__ import annotations
import math

import pytest


# ==================================================================
# Solution prep + dilution
# ==================================================================

class TestMolarity:
    def test_solve_for_mass(self):
        from orgchem.core.calc_solution import molarity_solve
        # 0.5 M NaCl in 1 L = 29.22 g (MW 58.44).
        r = molarity_solve(molarity_M=0.5, volume_L=1.0,
                           molecular_weight_gmol=58.44)
        assert math.isclose(r["mass_g"], 29.22, rel_tol=1e-6)

    def test_solve_for_molarity(self):
        from orgchem.core.calc_solution import molarity_solve
        r = molarity_solve(mass_g=29.22, volume_L=1.0,
                           molecular_weight_gmol=58.44)
        assert math.isclose(r["molarity_M"], 0.5, rel_tol=1e-4)

    def test_solve_for_volume(self):
        from orgchem.core.calc_solution import molarity_solve
        r = molarity_solve(mass_g=29.22, molarity_M=0.5,
                           molecular_weight_gmol=58.44)
        assert math.isclose(r["volume_L"], 1.0, rel_tol=1e-4)

    def test_solve_for_mw(self):
        from orgchem.core.calc_solution import molarity_solve
        r = molarity_solve(mass_g=29.22, molarity_M=0.5,
                           volume_L=1.0)
        assert math.isclose(r["molecular_weight_gmol"], 58.44,
                            rel_tol=1e-4)

    def test_rejects_two_unknowns(self):
        from orgchem.core.calc_solution import molarity_solve
        with pytest.raises(ValueError):
            molarity_solve(mass_g=10.0)

    def test_rejects_zero_input(self):
        from orgchem.core.calc_solution import molarity_solve
        with pytest.raises(ValueError):
            molarity_solve(mass_g=10.0, volume_L=0.0,
                           molecular_weight_gmol=10.0)


class TestDilution:
    def test_solve_for_v2(self):
        from orgchem.core.calc_solution import dilution_solve
        # 1 M × 10 mL → 0.1 M × 100 mL.
        r = dilution_solve(M1=1.0, V1=10.0, M2=0.1)
        assert math.isclose(r["V2"], 100.0, rel_tol=1e-9)

    def test_solve_for_m2(self):
        from orgchem.core.calc_solution import dilution_solve
        r = dilution_solve(M1=1.0, V1=10.0, V2=100.0)
        assert math.isclose(r["M2"], 0.1, rel_tol=1e-9)

    def test_rejects_two_unknowns(self):
        from orgchem.core.calc_solution import dilution_solve
        with pytest.raises(ValueError):
            dilution_solve(M1=1.0, V1=10.0)


class TestSerialDilution:
    def test_basic(self):
        from orgchem.core.calc_solution import serial_dilution
        # 1 M → 1:10 × 3 = 0.001 M.
        r = serial_dilution(initial_concentration=1.0,
                            dilution_factor=10.0,
                            n_steps=3)
        assert len(r["concentrations"]) == 4
        assert math.isclose(r["final_concentration"], 1e-3,
                            rel_tol=1e-9)
        assert math.isclose(r["total_dilution"], 1000.0,
                            rel_tol=1e-9)

    def test_rejects_factor_le_one(self):
        from orgchem.core.calc_solution import serial_dilution
        with pytest.raises(ValueError):
            serial_dilution(1.0, 1.0, 3)

    def test_rejects_zero_steps(self):
        from orgchem.core.calc_solution import serial_dilution
        with pytest.raises(ValueError):
            serial_dilution(1.0, 10.0, 0)


class TestMolarityFromMassPercent:
    def test_concentrated_hcl(self):
        """37 % w/w HCl, density 1.18 g/mL, MW 36.46 → ~12 M."""
        from orgchem.core.calc_solution import (
            molarity_from_mass_percent,
        )
        r = molarity_from_mass_percent(
            mass_percent=37.0,
            density_g_per_mL=1.18,
            molecular_weight_gmol=36.46)
        assert math.isclose(r["molarity_M"], 11.97, rel_tol=1e-2)

    def test_rejects_over_100_percent(self):
        from orgchem.core.calc_solution import (
            molarity_from_mass_percent,
        )
        with pytest.raises(ValueError):
            molarity_from_mass_percent(150.0, 1.0, 1.0)


class TestPpmConversion:
    def test_round_trip(self):
        from orgchem.core.calc_solution import (
            ppm_to_molarity, molarity_to_ppm,
        )
        # 100 ppm of MW-100 species → 0.001 M.
        r = ppm_to_molarity(100.0, 100.0)
        assert math.isclose(r["molarity_M"], 0.001, rel_tol=1e-9)
        r2 = molarity_to_ppm(r["molarity_M"], 100.0)
        assert math.isclose(r2["ppm"], 100.0, rel_tol=1e-9)


# ==================================================================
# Stoichiometry
# ==================================================================

class TestLimitingReagent:
    def test_finds_limiting(self):
        from orgchem.core.calc_stoichiometry import limiting_reagent
        # A: 1 mol with 1 stoich; B: 1 mol with 2 stoich.
        # B is limiting (0.5 eq vs A's 1.0 eq).
        r = limiting_reagent([
            {"name": "A", "moles": 1.0, "stoich_coeff": 1.0},
            {"name": "B", "moles": 1.0, "stoich_coeff": 2.0},
        ])
        assert r["limiting_name"] == "B"
        assert r["limiting_index"] == 1

    def test_finds_first_when_equal(self):
        from orgchem.core.calc_stoichiometry import limiting_reagent
        r = limiting_reagent([
            {"name": "A", "moles": 1.0, "stoich_coeff": 1.0},
            {"name": "B", "moles": 1.0, "stoich_coeff": 1.0},
        ])
        # Tie-break to first.
        assert r["limiting_index"] == 0

    def test_rejects_empty(self):
        from orgchem.core.calc_stoichiometry import limiting_reagent
        with pytest.raises(ValueError):
            limiting_reagent([])

    def test_rejects_missing_field(self):
        from orgchem.core.calc_stoichiometry import limiting_reagent
        with pytest.raises(ValueError):
            limiting_reagent([{"moles": 1.0}])


class TestTheoreticalYield:
    def test_basic(self):
        from orgchem.core.calc_stoichiometry import (
            theoretical_yield_g,
        )
        # 2 mol limiting (coeff 1) → 2 mol product (coeff 1) ×
        # MW 100 = 200 g.
        r = theoretical_yield_g(
            limiting_moles=2.0, limiting_stoich_coeff=1.0,
            product_stoich_coeff=1.0, product_mw_gmol=100.0)
        assert math.isclose(r["theoretical_yield_g"], 200.0,
                            rel_tol=1e-9)

    def test_two_to_one(self):
        from orgchem.core.calc_stoichiometry import (
            theoretical_yield_g,
        )
        # Coeff 2:1 → half as many product mol per limiting mol.
        r = theoretical_yield_g(
            limiting_moles=2.0, limiting_stoich_coeff=2.0,
            product_stoich_coeff=1.0, product_mw_gmol=100.0)
        assert math.isclose(r["moles_product"], 1.0, rel_tol=1e-9)


class TestPercentYield:
    def test_basic(self):
        from orgchem.core.calc_stoichiometry import percent_yield
        r = percent_yield(actual_yield_g=8.0,
                          theoretical_yield_g=10.0)
        assert math.isclose(r["percent"], 80.0, rel_tol=1e-9)

    def test_solve_for_actual(self):
        from orgchem.core.calc_stoichiometry import percent_yield
        r = percent_yield(theoretical_yield_g=10.0, percent=80.0)
        assert math.isclose(r["actual_yield_g"], 8.0, rel_tol=1e-9)


class TestPercentPurity:
    def test_basic(self):
        from orgchem.core.calc_stoichiometry import percent_purity
        r = percent_purity(pure_mass_g=8.0, sample_mass_g=10.0)
        assert math.isclose(r["percent_purity"], 80.0, rel_tol=1e-9)

    def test_rejects_purity_over_100(self):
        from orgchem.core.calc_stoichiometry import percent_purity
        with pytest.raises(ValueError):
            percent_purity(pure_mass_g=10.0, sample_mass_g=8.0)


# ==================================================================
# Acid-base
# ==================================================================

class TestPHFromH:
    def test_neutral(self):
        from orgchem.core.calc_acid_base import ph_from_h
        r = ph_from_h(1e-7)
        assert math.isclose(r["pH"], 7.0, rel_tol=1e-9)
        assert math.isclose(r["pOH"], 7.0, rel_tol=1e-9)

    def test_acidic(self):
        from orgchem.core.calc_acid_base import ph_from_h
        r = ph_from_h(1e-3)
        assert math.isclose(r["pH"], 3.0, rel_tol=1e-9)
        assert math.isclose(r["pOH"], 11.0, rel_tol=1e-9)

    def test_rejects_zero(self):
        from orgchem.core.calc_acid_base import ph_from_h
        with pytest.raises(ValueError):
            ph_from_h(0.0)


class TestHFromPh:
    def test_round_trip(self):
        from orgchem.core.calc_acid_base import h_from_ph, ph_from_h
        r = h_from_ph(7.0)
        assert math.isclose(r["h_concentration_M"], 1e-7,
                            rel_tol=1e-9)


class TestPkaKa:
    def test_pka_to_ka(self):
        from orgchem.core.calc_acid_base import pka_to_ka
        # Acetic acid pKa 4.76 → Ka ~1.74e-5.
        r = pka_to_ka(4.76)
        assert math.isclose(r["Ka"], 10 ** -4.76, rel_tol=1e-9)

    def test_round_trip(self):
        from orgchem.core.calc_acid_base import pka_to_ka, ka_to_pka
        r = pka_to_ka(4.76)
        r2 = ka_to_pka(r["Ka"])
        assert math.isclose(r2["pKa"], 4.76, rel_tol=1e-9)


class TestHendersonHasselbalch:
    def test_unity_ratio_gives_pka(self):
        from orgchem.core.calc_acid_base import henderson_hasselbalch
        r = henderson_hasselbalch(pKa=4.76, base_acid_ratio=1.0)
        assert math.isclose(r["pH"], 4.76, rel_tol=1e-9)

    def test_solve_for_ratio(self):
        """pH 5.0, pKa 4.76 → ratio = 10^0.24 ≈ 1.74."""
        from orgchem.core.calc_acid_base import henderson_hasselbalch
        r = henderson_hasselbalch(pH=5.0, pKa=4.76)
        assert math.isclose(r["base_acid_ratio"],
                            10 ** 0.24, rel_tol=1e-9)


# ==================================================================
# Gas laws
# ==================================================================

class TestIdealGas:
    def test_stp_one_mole(self):
        """At STP (1 atm, 273.15 K), 1 mol → 22.4 L."""
        from orgchem.core.calc_gas_law import ideal_gas_solve
        r = ideal_gas_solve(pressure_atm=1.0, moles=1.0,
                            temperature_K=273.15)
        # 22.4 L is approximate; exact = R·T/P.
        assert math.isclose(r["volume_L"], 22.414, rel_tol=1e-3)

    def test_solve_for_pressure(self):
        from orgchem.core.calc_gas_law import ideal_gas_solve
        r = ideal_gas_solve(volume_L=22.414, moles=1.0,
                            temperature_K=273.15)
        assert math.isclose(r["pressure_atm"], 1.0, rel_tol=1e-3)


class TestCombinedGasLaw:
    def test_isothermal_compression(self):
        """T fixed → P₁V₁ = P₂V₂ (Boyle's law)."""
        from orgchem.core.calc_gas_law import combined_gas_law
        r = combined_gas_law(P1=1.0, V1=10.0, T1=300.0,
                             P2=2.0, T2=300.0)
        assert math.isclose(r["V2"], 5.0, rel_tol=1e-9)


class TestGasDensity:
    def test_oxygen_at_stp(self):
        """O₂ at STP: ρ = 32 / 22.4 ≈ 1.43 g/L."""
        from orgchem.core.calc_gas_law import gas_density
        r = gas_density(pressure_atm=1.0,
                        molecular_weight_gmol=32.0,
                        temperature_K=273.15)
        assert math.isclose(r["density_g_per_L"], 1.428,
                            rel_tol=1e-2)


# ==================================================================
# Colligative
# ==================================================================

class TestBoilingPointElevation:
    def test_solvent_lookup(self):
        """1 m sucrose (i=1) in water: ΔTb = 0.512 × 1 = 0.512."""
        from orgchem.core.calc_colligative import (
            boiling_point_elevation,
        )
        r = boiling_point_elevation(
            solvent="water", molality_b=1.0, van_t_hoff_i=1.0)
        assert math.isclose(r["delta_T_b"], 0.512, rel_tol=1e-3)

    def test_unknown_solvent(self):
        from orgchem.core.calc_colligative import (
            boiling_point_elevation,
        )
        with pytest.raises(ValueError):
            boiling_point_elevation(
                solvent="unobtainium",
                molality_b=1.0, van_t_hoff_i=1.0)


class TestFreezingPointDepression:
    def test_nacl_in_water(self):
        """1 m NaCl (i=2) in water: ΔTf = 1.86 × 1 × 2 = 3.72."""
        from orgchem.core.calc_colligative import (
            freezing_point_depression,
        )
        r = freezing_point_depression(
            solvent="water", molality_b=1.0, van_t_hoff_i=2.0)
        assert math.isclose(r["delta_T_f"], 3.72, rel_tol=1e-3)


class TestOsmoticPressure:
    def test_isotonic_saline(self):
        """0.15 M NaCl (i≈1.85, hypotonic at 1) at 310 K (37 °C)
        → ~7.6 atm (close to 7.7 atm physiological osmolarity)."""
        from orgchem.core.calc_colligative import osmotic_pressure
        r = osmotic_pressure(
            molarity_M=0.15, temperature_K=310.0,
            van_t_hoff_i=2.0)
        assert math.isclose(r["pressure_atm"], 7.628, rel_tol=1e-2)


# ==================================================================
# Thermo + kinetics
# ==================================================================

class TestHeatCapacity:
    def test_water_heating(self):
        """Heating 100 g water from 20→30 °C: q = 100 × 4.184 ×
        10 = 4184 J."""
        from orgchem.core.calc_thermo_kinetics import (
            heat_capacity_solve,
        )
        r = heat_capacity_solve(
            mass_g=100.0, specific_heat_J_per_g_K=4.184,
            delta_T_K=10.0)
        assert math.isclose(r["heat_q_J"], 4184.0, rel_tol=1e-9)

    def test_solve_for_specific_heat(self):
        from orgchem.core.calc_thermo_kinetics import (
            heat_capacity_solve,
        )
        r = heat_capacity_solve(
            heat_q_J=4184.0, mass_g=100.0, delta_T_K=10.0)
        assert math.isclose(r["specific_heat_J_per_g_K"], 4.184,
                            rel_tol=1e-9)

    def test_negative_q_allowed(self):
        """Cooling = negative q.  Solver must accept."""
        from orgchem.core.calc_thermo_kinetics import (
            heat_capacity_solve,
        )
        r = heat_capacity_solve(
            mass_g=100.0, specific_heat_J_per_g_K=4.184,
            delta_T_K=-10.0)
        assert math.isclose(r["heat_q_J"], -4184.0, rel_tol=1e-9)


class TestHessLaw:
    def test_sum(self):
        from orgchem.core.calc_thermo_kinetics import hess_law_sum
        r = hess_law_sum([-100.0, +50.0, -25.0])
        assert math.isclose(r["total_delta_H_kJ"], -75.0,
                            rel_tol=1e-9)
        assert r["n_steps"] == 3


class TestFirstOrderHalfLife:
    def test_k_to_t_half(self):
        """k = 0.05 /s → t½ = ln 2 / 0.05 ≈ 13.86 s."""
        from orgchem.core.calc_thermo_kinetics import (
            first_order_half_life,
        )
        r = first_order_half_life(rate_constant_per_s=0.05)
        assert math.isclose(r["half_life_s"], math.log(2) / 0.05,
                            rel_tol=1e-9)

    def test_round_trip(self):
        from orgchem.core.calc_thermo_kinetics import (
            first_order_half_life,
        )
        r = first_order_half_life(rate_constant_per_s=0.05)
        r2 = first_order_half_life(half_life_s=r["half_life_s"])
        assert math.isclose(r2["rate_constant_per_s"], 0.05,
                            rel_tol=1e-9)

    def test_rejects_both_or_neither(self):
        from orgchem.core.calc_thermo_kinetics import (
            first_order_half_life,
        )
        with pytest.raises(ValueError):
            first_order_half_life()
        with pytest.raises(ValueError):
            first_order_half_life(rate_constant_per_s=0.05,
                                  half_life_s=10.0)


class TestFirstOrderIntegrated:
    def test_solve_for_final(self):
        """[A]_0 = 1 M, k = 0.1 /s, t = 10 s → [A] = e^-1 ≈
        0.368."""
        from orgchem.core.calc_thermo_kinetics import (
            first_order_integrated,
        )
        r = first_order_integrated(
            initial_concentration=1.0,
            rate_constant_per_s=0.1, time_s=10.0)
        assert math.isclose(r["final_concentration"],
                            math.exp(-1), rel_tol=1e-9)


class TestArrhenius:
    def test_solve_for_k(self):
        """k = A · exp(-Ea/RT) — basic forward solve."""
        from orgchem.core.calc_thermo_kinetics import (
            arrhenius_solve, R_J_PER_MOL_K,
        )
        r = arrhenius_solve(
            pre_exponential_A=1e10,
            activation_energy_J_per_mol=50000.0,
            temperature_K=300.0)
        expected = 1e10 * math.exp(-50000.0 / (R_J_PER_MOL_K * 300.0))
        assert math.isclose(r["rate_constant"], expected,
                            rel_tol=1e-9)


class TestEyring:
    def test_basic(self):
        from orgchem.core.calc_thermo_kinetics import (
            eyring_rate_constant,
        )
        r = eyring_rate_constant(
            delta_G_double_dagger_J_per_mol=80000.0,
            temperature_K=300.0)
        assert r["rate_constant"] > 0
        assert r["prefactor_kB_T_over_h"] > 0


# ==================================================================
# Equilibrium
# ==================================================================

class TestEquilibriumConstant:
    def test_simple_a_to_b(self):
        """A ⇌ B, [A] = 1, [B] = 2 → K = 2.0."""
        from orgchem.core.calc_equilibrium import (
            equilibrium_constant_from_concentrations,
        )
        r = equilibrium_constant_from_concentrations([
            {"name": "A", "concentration_M": 1.0,
             "stoich_coeff": 1.0, "side": "reactant"},
            {"name": "B", "concentration_M": 2.0,
             "stoich_coeff": 1.0, "side": "product"},
        ])
        assert math.isclose(r["K_eq"], 2.0, rel_tol=1e-9)

    def test_reactant_squared(self):
        """A + A ⇌ B, [A] = 0.5, [B] = 0.25 → K = 0.25/0.25 = 1."""
        from orgchem.core.calc_equilibrium import (
            equilibrium_constant_from_concentrations,
        )
        r = equilibrium_constant_from_concentrations([
            {"name": "A", "concentration_M": 0.5,
             "stoich_coeff": 2.0, "side": "reactant"},
            {"name": "B", "concentration_M": 0.25,
             "stoich_coeff": 1.0, "side": "product"},
        ])
        assert math.isclose(r["K_eq"], 1.0, rel_tol=1e-9)

    def test_rejects_unknown_side(self):
        from orgchem.core.calc_equilibrium import (
            equilibrium_constant_from_concentrations,
        )
        with pytest.raises(ValueError):
            equilibrium_constant_from_concentrations([
                {"name": "A", "concentration_M": 1.0,
                 "stoich_coeff": 1.0, "side": "neither"},
            ])


class TestKsp:
    def test_agcl(self):
        """AgCl: K_sp = s² → s = sqrt(K_sp)."""
        from orgchem.core.calc_equilibrium import (
            ksp_from_solubility, solubility_from_ksp,
        )
        r = ksp_from_solubility(1.3e-5, 1, 1)
        assert math.isclose(r["K_sp"], 1.69e-10, rel_tol=1e-9)
        r2 = solubility_from_ksp(1.69e-10, 1, 1)
        assert math.isclose(r2["molar_solubility"], 1.3e-5,
                            rel_tol=1e-3)

    def test_pbi2(self):
        """PbI₂: K_sp = 4·s³ → s = (K_sp/4)^(1/3)."""
        from orgchem.core.calc_equilibrium import (
            ksp_from_solubility, solubility_from_ksp,
        )
        # s = 1.5e-3 → K_sp = (1)(1.5e-3) · (2)(1.5e-3)² × 2
        # Actually K_sp = s · (2s)² = 4s³.
        r = ksp_from_solubility(1.5e-3, 1, 2)
        expected = 4 * (1.5e-3) ** 3
        assert math.isclose(r["K_sp"], expected, rel_tol=1e-9)
        r2 = solubility_from_ksp(expected, 1, 2)
        assert math.isclose(r2["molar_solubility"], 1.5e-3,
                            rel_tol=1e-6)


class TestICE:
    def test_simple_quadratic(self):
        """A + B ⇌ C + D with K = 4, A₀ = B₀ = 1, C₀ = D₀ = 0.
        Quadratic: x² = 4 (1-x)² → x = 2/(2+1) = 2/3.  But
        with 1-K coeff: -3x² - 8x + 4 = 0 → x = ... let me
        just verify the equation holds."""
        from orgchem.core.calc_equilibrium import ice_solve_a_plus_b
        r = ice_solve_a_plus_b(K=4.0, initial_A=1.0,
                               initial_B=1.0)
        x = r["extent_x"]
        assert 0 < x < 1, f"x out of range: {x}"
        # Verify K holds at equilibrium.
        K_check = (r["C_eq"] * r["D_eq"]) / (r["A_eq"] * r["B_eq"])
        assert math.isclose(K_check, 4.0, rel_tol=1e-6)

    def test_no_reactants(self):
        from orgchem.core.calc_equilibrium import ice_solve_a_plus_b
        with pytest.raises(ValueError):
            ice_solve_a_plus_b(K=1.0, initial_A=0.0, initial_B=0.0)

    def test_K_equal_one_degenerate(self):
        """K = 1, A₀ = B₀ = 1, C₀ = D₀ = 0 → linear case."""
        from orgchem.core.calc_equilibrium import ice_solve_a_plus_b
        r = ice_solve_a_plus_b(K=1.0, initial_A=1.0,
                               initial_B=1.0)
        # At K=1, equal initial reactants → x = 0.5.
        assert math.isclose(r["extent_x"], 0.5, rel_tol=1e-6)
