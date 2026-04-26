"""Phase 39b (round 143) + 39c (round 145) — agent actions
for the lab calculator.

39b shipped the single dialog-opener action.  39c (this
round) wraps every Phase-39a solver in a thin `@action`
under the `calc` category, so each solver becomes a direct
tool-use target for the tutor / scripts / stdio bridge.

Wrapping convention
-------------------
Every wrapper has the same kwargs as the underlying solver
and returns:

- The solver's result dict on success.
- ``{"error": str(e)}`` when the solver raises ``ValueError``
  (bad input) — never a Python traceback.

Spin-box "0 = unknown" semantics from the dialog don't apply
here — the agent caller passes ``None`` explicitly for the
unknown.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


def _wrap(solver, **kwargs) -> Dict[str, Any]:
    """Common wrapper — call the solver, convert ValueError to
    ``{"error": str}``."""
    try:
        return solver(**kwargs)
    except ValueError as e:
        return {"error": str(e)}


@action(category="calc")
def open_lab_calculator(tab: str = "") -> Dict[str, Any]:
    """Open the *Tools → Lab calculator…* dialog and optionally
    focus a specific tab (one of ``Solution`` / ``Stoichiometry``
    / ``Acid-base`` / ``Gas law`` / ``Colligative`` /
    ``Thermo + kinetics`` / ``Equilibrium``).

    Returns ``{"opened": True, "selected": <bool>, "tab": str}``
    on success or ``{"error": ...}`` when the GUI isn't reachable.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.lab_calculator import (
            LabCalculatorDialog,
        )
        dlg = LabCalculatorDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if tab:
            selected = dlg.select_tab(tab)
        return {
            "opened": True,
            "selected": selected,
            "tab": tab or None,
            "available_tabs": dlg.tab_labels(),
        }

    return run_on_main_thread_sync(_open)


# ==================================================================
# Phase 39c — per-solver wrappers
# ==================================================================

# ---- Solution prep + dilution ------------------------------------

@action(category="calc")
def molarity(
    mass_g: Optional[float] = None,
    molarity_M: Optional[float] = None,
    volume_L: Optional[float] = None,
    molecular_weight_gmol: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve ``mass_g = molarity_M · volume_L ·
    molecular_weight_gmol``.  Pass any 3 of 4 quantities;
    the fourth is computed."""
    from orgchem.core.calc_solution import molarity_solve
    return _wrap(molarity_solve,
                 mass_g=mass_g, molarity_M=molarity_M,
                 volume_L=volume_L,
                 molecular_weight_gmol=molecular_weight_gmol)


@action(category="calc")
def dilution(
    M1: Optional[float] = None,
    V1: Optional[float] = None,
    M2: Optional[float] = None,
    V2: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve M₁·V₁ = M₂·V₂.  Pass any 3 of 4."""
    from orgchem.core.calc_solution import dilution_solve
    return _wrap(dilution_solve,
                 M1=M1, V1=V1, M2=M2, V2=V2)


@action(category="calc")
def serial_dilution(
    initial_concentration: float,
    dilution_factor: float,
    n_steps: int,
) -> Dict[str, Any]:
    """Walk a serial dilution: each step divides the previous
    concentration by ``dilution_factor``.  Returns the full
    concentration list (length ``n_steps + 1``) +
    final_concentration + total_dilution."""
    from orgchem.core.calc_solution import (
        serial_dilution as _serial,
    )
    return _wrap(
        _serial,
        initial_concentration=initial_concentration,
        dilution_factor=dilution_factor,
        n_steps=n_steps)


@action(category="calc")
def molarity_from_mass_percent(
    mass_percent: float,
    density_g_per_mL: float,
    molecular_weight_gmol: float,
) -> Dict[str, Any]:
    """Compute molarity of a w/w% solution given density.
    Example: HCl 37 % w/w · 1.18 g/mL ÷ 36.46 → ~12 M."""
    from orgchem.core.calc_solution import (
        molarity_from_mass_percent as _mfm,
    )
    return _wrap(
        _mfm,
        mass_percent=mass_percent,
        density_g_per_mL=density_g_per_mL,
        molecular_weight_gmol=molecular_weight_gmol)


@action(category="calc")
def ppm_to_molarity(
    ppm: float,
    molecular_weight_gmol: float,
) -> Dict[str, Any]:
    """Convert ppm (mg/L for dilute aqueous) to molarity:
    M = ppm / (1000 · MW)."""
    from orgchem.core.calc_solution import (
        ppm_to_molarity as _pm,
    )
    return _wrap(_pm, ppm=ppm,
                 molecular_weight_gmol=molecular_weight_gmol)


@action(category="calc")
def molarity_to_ppm(
    molarity_M: float,
    molecular_weight_gmol: float,
) -> Dict[str, Any]:
    """Inverse of :func:`ppm_to_molarity`."""
    from orgchem.core.calc_solution import (
        molarity_to_ppm as _mp,
    )
    return _wrap(_mp, molarity_M=molarity_M,
                 molecular_weight_gmol=molecular_weight_gmol)


# ---- Stoichiometry ---------------------------------------------

@action(category="calc")
def limiting_reagent(
    reagents: List[Dict[str, float]],
) -> Dict[str, Any]:
    """Find the limiting reagent.  ``reagents`` is a list of
    ``{name, moles, stoich_coeff}`` dicts.  Returns
    ``{limiting_index, limiting_name, available_eq_units,
    limiting_eq_units}``."""
    from orgchem.core.calc_stoichiometry import (
        limiting_reagent as _lr,
    )
    return _wrap(_lr, reagents=reagents)


@action(category="calc")
def theoretical_yield(
    limiting_moles: float,
    limiting_stoich_coeff: float,
    product_stoich_coeff: float,
    product_mw_gmol: float,
) -> Dict[str, Any]:
    """Theoretical product mass (g) from limiting-reagent
    moles + stoichiometric coefficients + product MW."""
    from orgchem.core.calc_stoichiometry import (
        theoretical_yield_g as _ty,
    )
    return _wrap(
        _ty,
        limiting_moles=limiting_moles,
        limiting_stoich_coeff=limiting_stoich_coeff,
        product_stoich_coeff=product_stoich_coeff,
        product_mw_gmol=product_mw_gmol)


@action(category="calc")
def percent_yield(
    actual_yield_g: Optional[float] = None,
    theoretical_yield_g: Optional[float] = None,
    percent: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve percent = 100 · actual / theoretical.  Pass any
    2 of 3."""
    from orgchem.core.calc_stoichiometry import (
        percent_yield as _py,
    )
    return _wrap(_py, actual_yield_g=actual_yield_g,
                 theoretical_yield_g=theoretical_yield_g,
                 percent=percent)


@action(category="calc")
def percent_purity(
    pure_mass_g: float,
    sample_mass_g: float,
) -> Dict[str, Any]:
    """Percent purity = 100 · pure mass / sample mass."""
    from orgchem.core.calc_stoichiometry import (
        percent_purity as _pp,
    )
    return _wrap(_pp, pure_mass_g=pure_mass_g,
                 sample_mass_g=sample_mass_g)


# ---- Acid-base ---------------------------------------------------

@action(category="calc")
def ph_from_h(h_concentration_M: float) -> Dict[str, Any]:
    """pH = -log10([H⁺]).  Returns {pH, pOH, [H⁺], [OH⁻]}."""
    from orgchem.core.calc_acid_base import (
        ph_from_h as _phfh,
    )
    return _wrap(_phfh, h_concentration_M=h_concentration_M)


@action(category="calc")
def h_from_ph(pH: float) -> Dict[str, Any]:
    """[H⁺] = 10⁻ᵖᴴ.  Same return shape as :func:`ph_from_h`."""
    from orgchem.core.calc_acid_base import (
        h_from_ph as _hfph,
    )
    return _wrap(_hfph, pH=pH)


@action(category="calc")
def pka_to_ka(pKa: float) -> Dict[str, Any]:
    """pKa → Ka (Ka = 10⁻ᵖᴷᵃ)."""
    from orgchem.core.calc_acid_base import (
        pka_to_ka as _pk,
    )
    return _wrap(_pk, pKa=pKa)


@action(category="calc")
def ka_to_pka(Ka: float) -> Dict[str, Any]:
    """Ka → pKa (pKa = -log10(Ka))."""
    from orgchem.core.calc_acid_base import (
        ka_to_pka as _kp,
    )
    return _wrap(_kp, Ka=Ka)


@action(category="calc")
def henderson_hasselbalch(
    pH: Optional[float] = None,
    pKa: Optional[float] = None,
    base_acid_ratio: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve pH = pKa + log10([A⁻]/[HA]).  Pass any 2 of 3.
    Buffer-design entry point."""
    from orgchem.core.calc_acid_base import (
        henderson_hasselbalch as _hh,
    )
    return _wrap(_hh, pH=pH, pKa=pKa,
                 base_acid_ratio=base_acid_ratio)


# ---- Gas laws ----------------------------------------------------

@action(category="calc")
def ideal_gas(
    pressure_atm: Optional[float] = None,
    volume_L: Optional[float] = None,
    moles: Optional[float] = None,
    temperature_K: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve PV = nRT.  Pass any 3 of 4."""
    from orgchem.core.calc_gas_law import ideal_gas_solve
    return _wrap(ideal_gas_solve,
                 pressure_atm=pressure_atm, volume_L=volume_L,
                 moles=moles, temperature_K=temperature_K)


@action(category="calc")
def combined_gas_law(
    P1: Optional[float] = None,
    V1: Optional[float] = None,
    T1: Optional[float] = None,
    P2: Optional[float] = None,
    V2: Optional[float] = None,
    T2: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve P₁V₁/T₁ = P₂V₂/T₂.  Pass any 5 of 6."""
    from orgchem.core.calc_gas_law import (
        combined_gas_law as _cgl,
    )
    return _wrap(_cgl, P1=P1, V1=V1, T1=T1,
                 P2=P2, V2=V2, T2=T2)


@action(category="calc")
def gas_density(
    pressure_atm: float,
    molecular_weight_gmol: float,
    temperature_K: float,
) -> Dict[str, Any]:
    """Density of an ideal gas: ρ = PM / RT."""
    from orgchem.core.calc_gas_law import (
        gas_density as _gd,
    )
    return _wrap(_gd, pressure_atm=pressure_atm,
                 molecular_weight_gmol=molecular_weight_gmol,
                 temperature_K=temperature_K)


# ---- Colligative properties --------------------------------------

@action(category="calc")
def boiling_point_elevation(
    K_b: Optional[float] = None,
    molality_b: Optional[float] = None,
    van_t_hoff_i: Optional[float] = None,
    delta_T_b: Optional[float] = None,
    solvent: Optional[str] = None,
) -> Dict[str, Any]:
    """Solve ΔT_b = K_b · b · i.  Pass any 3 of 4 quantities,
    or pass ``solvent`` (e.g. ``"water"``) to auto-fill K_b."""
    from orgchem.core.calc_colligative import (
        boiling_point_elevation as _bpe,
    )
    return _wrap(_bpe, K_b=K_b, molality_b=molality_b,
                 van_t_hoff_i=van_t_hoff_i,
                 delta_T_b=delta_T_b, solvent=solvent)


@action(category="calc")
def freezing_point_depression(
    K_f: Optional[float] = None,
    molality_b: Optional[float] = None,
    van_t_hoff_i: Optional[float] = None,
    delta_T_f: Optional[float] = None,
    solvent: Optional[str] = None,
) -> Dict[str, Any]:
    """Solve ΔT_f = K_f · b · i.  Pass any 3 of 4 quantities,
    or pass ``solvent`` to auto-fill K_f."""
    from orgchem.core.calc_colligative import (
        freezing_point_depression as _fpd,
    )
    return _wrap(_fpd, K_f=K_f, molality_b=molality_b,
                 van_t_hoff_i=van_t_hoff_i,
                 delta_T_f=delta_T_f, solvent=solvent)


@action(category="calc")
def osmotic_pressure(
    molarity_M: Optional[float] = None,
    temperature_K: Optional[float] = None,
    van_t_hoff_i: Optional[float] = None,
    pressure_atm: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve Π = M·R·T·i.  Pass any 3 of 4."""
    from orgchem.core.calc_colligative import (
        osmotic_pressure as _op,
    )
    return _wrap(_op, molarity_M=molarity_M,
                 temperature_K=temperature_K,
                 van_t_hoff_i=van_t_hoff_i,
                 pressure_atm=pressure_atm)


# ---- Thermo + kinetics -------------------------------------------

@action(category="calc")
def heat_capacity(
    heat_q_J: Optional[float] = None,
    mass_g: Optional[float] = None,
    specific_heat_J_per_g_K: Optional[float] = None,
    delta_T_K: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve q = m · c · ΔT.  Pass any 3 of 4.  Heat + ΔT
    can be negative (exothermic / cooling); mass + specific
    heat must be positive."""
    from orgchem.core.calc_thermo_kinetics import (
        heat_capacity_solve,
    )
    return _wrap(heat_capacity_solve,
                 heat_q_J=heat_q_J, mass_g=mass_g,
                 specific_heat_J_per_g_K=specific_heat_J_per_g_K,
                 delta_T_K=delta_T_K)


@action(category="calc")
def hess_law_sum(step_delta_H_kJ: List[float]) -> Dict[str, Any]:
    """Sum a list of step ΔH values to get the overall ΔH for
    a multi-step reaction."""
    from orgchem.core.calc_thermo_kinetics import (
        hess_law_sum as _hl,
    )
    return _wrap(_hl, step_delta_H_kJ=step_delta_H_kJ)


@action(category="calc")
def first_order_half_life(
    rate_constant_per_s: Optional[float] = None,
    half_life_s: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve t½ = ln 2 / k.  Pass either k or t½ — exactly
    one."""
    from orgchem.core.calc_thermo_kinetics import (
        first_order_half_life as _fohl,
    )
    return _wrap(_fohl, rate_constant_per_s=rate_constant_per_s,
                 half_life_s=half_life_s)


@action(category="calc")
def first_order_integrated(
    initial_concentration: Optional[float] = None,
    final_concentration: Optional[float] = None,
    rate_constant_per_s: Optional[float] = None,
    time_s: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve [A]_t = [A]_0 · exp(-kt).  Pass any 3 of 4."""
    from orgchem.core.calc_thermo_kinetics import (
        first_order_integrated as _foi,
    )
    return _wrap(
        _foi,
        initial_concentration=initial_concentration,
        final_concentration=final_concentration,
        rate_constant_per_s=rate_constant_per_s,
        time_s=time_s)


@action(category="calc")
def arrhenius(
    rate_constant: Optional[float] = None,
    pre_exponential_A: Optional[float] = None,
    activation_energy_J_per_mol: Optional[float] = None,
    temperature_K: Optional[float] = None,
) -> Dict[str, Any]:
    """Solve k = A · exp(-Ea / RT).  Pass any 3 of 4."""
    from orgchem.core.calc_thermo_kinetics import (
        arrhenius_solve,
    )
    return _wrap(
        arrhenius_solve,
        rate_constant=rate_constant,
        pre_exponential_A=pre_exponential_A,
        activation_energy_J_per_mol=activation_energy_J_per_mol,
        temperature_K=temperature_K)


@action(category="calc")
def eyring_rate_constant(
    delta_G_double_dagger_J_per_mol: float,
    temperature_K: float,
) -> Dict[str, Any]:
    """Eyring forward solve: k = (k_B·T / h) · exp(-ΔG‡ / RT).
    Returns the rate constant + pre-factor."""
    from orgchem.core.calc_thermo_kinetics import (
        eyring_rate_constant as _ey,
    )
    return _wrap(
        _ey,
        delta_G_double_dagger_J_per_mol=
            delta_G_double_dagger_J_per_mol,
        temperature_K=temperature_K)


# ---- Equilibrium -------------------------------------------------

@action(category="calc")
def equilibrium_constant(
    species: List[Dict[str, object]],
) -> Dict[str, Any]:
    """K_eq = Π[product]^coeff / Π[reactant]^coeff.

    Each species: ``{name, concentration_M, stoich_coeff,
    side}`` where side ∈ {``product``, ``reactant``}."""
    from orgchem.core.calc_equilibrium import (
        equilibrium_constant_from_concentrations as _ec,
    )
    return _wrap(_ec, species=species)


@action(category="calc")
def ksp_from_solubility(
    molar_solubility: float,
    n: int,
    m: int,
) -> Dict[str, Any]:
    """K_sp = (n·s)ⁿ · (m·s)ᵐ for a simple AₙBₘ salt."""
    from orgchem.core.calc_equilibrium import (
        ksp_from_solubility as _ks,
    )
    return _wrap(_ks, molar_solubility=molar_solubility,
                 n=n, m=m)


@action(category="calc")
def solubility_from_ksp(
    K_sp: float,
    n: int,
    m: int,
) -> Dict[str, Any]:
    """Inverse of :func:`ksp_from_solubility`.  Closed-form:
    s = (K_sp / (nⁿ · mᵐ))^(1 / (n + m))."""
    from orgchem.core.calc_equilibrium import (
        solubility_from_ksp as _sk,
    )
    return _wrap(_sk, K_sp=K_sp, n=n, m=m)


@action(category="calc")
def ice_solve_a_plus_b(
    K: float,
    initial_A: float,
    initial_B: float,
    initial_C: float = 0.0,
    initial_D: float = 0.0,
) -> Dict[str, Any]:
    """Closed-form quadratic ICE solver for A + B ⇌ C + D
    (1:1:1:1 stoichiometry).  Returns the extent of reaction
    + all four equilibrium concentrations."""
    from orgchem.core.calc_equilibrium import (
        ice_solve_a_plus_b as _ice,
    )
    return _wrap(_ice, K=K, initial_A=initial_A,
                 initial_B=initial_B,
                 initial_C=initial_C,
                 initial_D=initial_D)
