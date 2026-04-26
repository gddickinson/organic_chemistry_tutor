"""Phase 39a (round 142) — gas-law calculators.

- Ideal-gas-law solver (PV = nRT).
- Combined gas law (P₁V₁/T₁ = P₂V₂/T₂).
- Density of an ideal gas (ρ = PM / RT).
"""
from __future__ import annotations
from typing import Dict, Optional


#: Ideal-gas constant.  Chosen units: pressure in atm, volume
#: in L, temperature in K, moles in mol → R = 0.082057 L·atm·
#: K⁻¹·mol⁻¹.  All ideal-gas helpers here use this convention.
R_L_ATM_PER_MOL_K: float = 0.0820573661


def ideal_gas_solve(
    pressure_atm: Optional[float] = None,
    volume_L: Optional[float] = None,
    moles: Optional[float] = None,
    temperature_K: Optional[float] = None,
) -> Dict[str, float]:
    """Solve PV = nRT.  Pass any 3 of 4."""
    given = {
        "pressure_atm": pressure_atm,
        "volume_L": volume_L,
        "moles": moles,
        "temperature_K": temperature_K,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be positive; got {v!r}.")
    R = R_L_ATM_PER_MOL_K
    if missing == ["pressure_atm"]:
        given["pressure_atm"] = (
            moles * R * temperature_K / volume_L)
    elif missing == ["volume_L"]:
        given["volume_L"] = (
            moles * R * temperature_K / pressure_atm)
    elif missing == ["moles"]:
        given["moles"] = (
            pressure_atm * volume_L / (R * temperature_K))
    else:
        given["temperature_K"] = (
            pressure_atm * volume_L / (moles * R))
    return given


def combined_gas_law(
    P1: Optional[float] = None,
    V1: Optional[float] = None,
    T1: Optional[float] = None,
    P2: Optional[float] = None,
    V2: Optional[float] = None,
    T2: Optional[float] = None,
) -> Dict[str, float]:
    """Solve P₁V₁/T₁ = P₂V₂/T₂.  Pass any 5 of 6."""
    given = {"P1": P1, "V1": V1, "T1": T1,
             "P2": P2, "V2": V2, "T2": T2}
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 5 of 6 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be positive; got {v!r}.")
    if missing == ["P1"]:
        given["P1"] = P2 * V2 * T1 / (V1 * T2)
    elif missing == ["V1"]:
        given["V1"] = P2 * V2 * T1 / (P1 * T2)
    elif missing == ["T1"]:
        given["T1"] = P1 * V1 * T2 / (P2 * V2)
    elif missing == ["P2"]:
        given["P2"] = P1 * V1 * T2 / (V2 * T1)
    elif missing == ["V2"]:
        given["V2"] = P1 * V1 * T2 / (P2 * T1)
    else:
        given["T2"] = P2 * V2 * T1 / (P1 * V1)
    return given


def gas_density(
    pressure_atm: float,
    molecular_weight_gmol: float,
    temperature_K: float,
) -> Dict[str, float]:
    """Density of an ideal gas: ρ = PM / RT (g/L when P in atm,
    M in g/mol, T in K)."""
    for name, val in (("pressure_atm", pressure_atm),
                      ("molecular_weight_gmol",
                       molecular_weight_gmol),
                      ("temperature_K", temperature_K)):
        if val <= 0:
            raise ValueError(f"{name} must be positive; got {val!r}.")
    rho = (pressure_atm * molecular_weight_gmol
           ) / (R_L_ATM_PER_MOL_K * temperature_K)
    return {
        "density_g_per_L": rho,
        "pressure_atm": pressure_atm,
        "molecular_weight_gmol": molecular_weight_gmol,
        "temperature_K": temperature_K,
    }
