"""Phase 39a (round 142) — thermochemistry + kinetics
calculators.

- Heat capacity: q = m · c · ΔT
- Hess's-law accumulator (sum of step ΔH).
- First-order half-life: t½ = ln 2 / k
- First-order integrated rate: [A]_t = [A]_0 · exp(-kt)
- Arrhenius: k = A · exp(-Ea/RT)
- Eyring (transition-state theory):
  k = (k_B·T / h) · exp(-ΔG‡/RT)
"""
from __future__ import annotations
import math
from typing import Dict, List, Optional


#: Universal gas constant in J·K⁻¹·mol⁻¹ (Arrhenius / Eyring).
R_J_PER_MOL_K: float = 8.314462618

#: Boltzmann constant (J/K).
K_B: float = 1.380649e-23

#: Planck constant (J·s).
H_PLANCK: float = 6.62607015e-34


# ------------------------------------------------------------------
# Thermochemistry
# ------------------------------------------------------------------

def heat_capacity_solve(
    heat_q_J: Optional[float] = None,
    mass_g: Optional[float] = None,
    specific_heat_J_per_g_K: Optional[float] = None,
    delta_T_K: Optional[float] = None,
) -> Dict[str, float]:
    """Solve q = m · c · ΔT.  Pass any 3 of 4."""
    given = {
        "heat_q_J": heat_q_J,
        "mass_g": mass_g,
        "specific_heat_J_per_g_K": specific_heat_J_per_g_K,
        "delta_T_K": delta_T_K,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities; got "
            f"{len(missing)} missing.")
    # Heat + ΔT can be negative (exothermic, cooling).  Mass +
    # specific heat must be positive.
    for k in ("mass_g", "specific_heat_J_per_g_K"):
        v = given[k]
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be > 0; got {v!r}.")
    if missing == ["heat_q_J"]:
        given["heat_q_J"] = (
            mass_g * specific_heat_J_per_g_K * delta_T_K)
    elif missing == ["mass_g"]:
        if specific_heat_J_per_g_K * delta_T_K == 0:
            raise ValueError("Cannot divide by zero ΔT.")
        given["mass_g"] = heat_q_J / (
            specific_heat_J_per_g_K * delta_T_K)
    elif missing == ["specific_heat_J_per_g_K"]:
        if mass_g * delta_T_K == 0:
            raise ValueError("Cannot divide by zero mass·ΔT.")
        given["specific_heat_J_per_g_K"] = heat_q_J / (
            mass_g * delta_T_K)
    else:
        if mass_g * specific_heat_J_per_g_K == 0:
            raise ValueError("Cannot divide by zero m·c.")
        given["delta_T_K"] = heat_q_J / (
            mass_g * specific_heat_J_per_g_K)
    return given


def hess_law_sum(step_delta_H_kJ: List[float]) -> Dict[str, float]:
    """Sum a list of step ΔH values (any sign) to get the
    overall ΔH for a multi-step reaction.  Trivial but
    useful as a single-call agent action."""
    if not step_delta_H_kJ:
        raise ValueError("Need ≥ 1 step ΔH value.")
    total = sum(step_delta_H_kJ)
    return {
        "total_delta_H_kJ": total,
        "n_steps": len(step_delta_H_kJ),
        "step_values": list(step_delta_H_kJ),
    }


# ------------------------------------------------------------------
# Kinetics
# ------------------------------------------------------------------

def first_order_half_life(
    rate_constant_per_s: Optional[float] = None,
    half_life_s: Optional[float] = None,
) -> Dict[str, float]:
    """Solve t½ = ln 2 / k.  Pass either k or t½."""
    if (rate_constant_per_s is None) == (half_life_s is None):
        raise ValueError(
            "Pass exactly one of rate_constant_per_s / "
            "half_life_s; both or neither is invalid.")
    if rate_constant_per_s is not None:
        if rate_constant_per_s <= 0:
            raise ValueError(
                f"rate_constant_per_s must be > 0; "
                f"got {rate_constant_per_s!r}.")
        return {
            "rate_constant_per_s": rate_constant_per_s,
            "half_life_s": math.log(2) / rate_constant_per_s,
        }
    if half_life_s <= 0:
        raise ValueError(
            f"half_life_s must be > 0; got {half_life_s!r}.")
    return {
        "rate_constant_per_s": math.log(2) / half_life_s,
        "half_life_s": half_life_s,
    }


def first_order_integrated(
    initial_concentration: Optional[float] = None,
    final_concentration: Optional[float] = None,
    rate_constant_per_s: Optional[float] = None,
    time_s: Optional[float] = None,
) -> Dict[str, float]:
    """Solve [A]_t = [A]_0 · exp(-kt).  Pass any 3 of 4
    quantities."""
    given = {
        "initial_concentration": initial_concentration,
        "final_concentration": final_concentration,
        "rate_constant_per_s": rate_constant_per_s,
        "time_s": time_s,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be > 0; got {v!r}.")
    if missing == ["final_concentration"]:
        given["final_concentration"] = (
            initial_concentration
            * math.exp(-rate_constant_per_s * time_s))
    elif missing == ["initial_concentration"]:
        given["initial_concentration"] = (
            final_concentration
            / math.exp(-rate_constant_per_s * time_s))
    elif missing == ["rate_constant_per_s"]:
        if final_concentration >= initial_concentration:
            raise ValueError(
                "final_concentration must be < initial; "
                "first-order decay only.")
        given["rate_constant_per_s"] = (
            math.log(initial_concentration / final_concentration)
            / time_s)
    else:
        if final_concentration >= initial_concentration:
            raise ValueError(
                "final_concentration must be < initial; "
                "first-order decay only.")
        given["time_s"] = (
            math.log(initial_concentration / final_concentration)
            / rate_constant_per_s)
    return given


def arrhenius_solve(
    rate_constant: Optional[float] = None,
    pre_exponential_A: Optional[float] = None,
    activation_energy_J_per_mol: Optional[float] = None,
    temperature_K: Optional[float] = None,
) -> Dict[str, float]:
    """Solve k = A · exp(-Ea / RT).  Pass any 3 of 4
    quantities."""
    given = {
        "rate_constant": rate_constant,
        "pre_exponential_A": pre_exponential_A,
        "activation_energy_J_per_mol":
            activation_energy_J_per_mol,
        "temperature_K": temperature_K,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be > 0; got {v!r}.")
    R = R_J_PER_MOL_K
    if missing == ["rate_constant"]:
        given["rate_constant"] = (
            pre_exponential_A
            * math.exp(-activation_energy_J_per_mol
                       / (R * temperature_K)))
    elif missing == ["pre_exponential_A"]:
        given["pre_exponential_A"] = (
            rate_constant
            / math.exp(-activation_energy_J_per_mol
                       / (R * temperature_K)))
    elif missing == ["activation_energy_J_per_mol"]:
        given["activation_energy_J_per_mol"] = (
            -R * temperature_K
            * math.log(rate_constant / pre_exponential_A))
    else:
        ratio = rate_constant / pre_exponential_A
        if ratio <= 0 or ratio >= 1:
            raise ValueError(
                "rate_constant / pre_exponential_A must be "
                "in (0, 1) for the Arrhenius temperature solve.")
        given["temperature_K"] = (
            -activation_energy_J_per_mol
            / (R * math.log(ratio)))
    return given


def eyring_rate_constant(
    delta_G_double_dagger_J_per_mol: float,
    temperature_K: float,
) -> Dict[str, float]:
    """Forward Eyring solve: k = (k_B·T / h) · exp(-ΔG‡ / RT).

    Returns the rate constant k.  No symmetric-solve wrapper —
    the inverse (Ea-from-k at single T) is rarely useful + the
    Arrhenius solver covers the practical case.
    """
    if temperature_K <= 0:
        raise ValueError(
            f"temperature_K must be > 0; got {temperature_K!r}.")
    R = R_J_PER_MOL_K
    pref = (K_B * temperature_K) / H_PLANCK
    rate_constant = pref * math.exp(
        -delta_G_double_dagger_J_per_mol / (R * temperature_K))
    return {
        "rate_constant": rate_constant,
        "delta_G_double_dagger_J_per_mol":
            delta_G_double_dagger_J_per_mol,
        "temperature_K": temperature_K,
        "prefactor_kB_T_over_h": pref,
    }
