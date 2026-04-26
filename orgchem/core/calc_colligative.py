"""Phase 39a (round 142) — colligative-property calculators.

- Boiling-point elevation: ΔT_b = K_b · b · i
- Freezing-point depression: ΔT_f = K_f · b · i
- Osmotic pressure: Π = M · R · T · i
"""
from __future__ import annotations
from typing import Dict, Optional


#: Cryoscopic / ebullioscopic constants for common solvents
#: (K_b in °C·kg/mol; K_f in °C·kg/mol).  Source:
#: Atkins / de Paula Physical Chemistry (10th ed.).
SOLVENT_CONSTANTS: Dict[str, Dict[str, float]] = {
    "water":         {"K_b": 0.512, "K_f": 1.86},
    "benzene":       {"K_b": 2.53,  "K_f": 5.12},
    "chloroform":    {"K_b": 3.63,  "K_f": 4.68},
    "acetic_acid":   {"K_b": 3.07,  "K_f": 3.90},
    "ethanol":       {"K_b": 1.22,  "K_f": 1.99},
    "carbon_tetrachloride":
                     {"K_b": 5.03,  "K_f": 30.0},
    "cyclohexane":   {"K_b": 2.79,  "K_f": 20.0},
    "camphor":       {"K_b": 5.95,  "K_f": 40.0},
}

#: Universal gas constant in osmotic-pressure-friendly units
#: (L·atm·K⁻¹·mol⁻¹).  Same value as `calc_gas_law.R`.
_R_L_ATM_PER_MOL_K = 0.0820573661


def boiling_point_elevation(
    K_b: Optional[float] = None,
    molality_b: Optional[float] = None,
    van_t_hoff_i: Optional[float] = None,
    delta_T_b: Optional[float] = None,
    solvent: Optional[str] = None,
) -> Dict[str, float]:
    """Solve ΔT_b = K_b · b · i.  Pass any 3 of 4 quantities,
    or pass ``solvent`` (one of :data:`SOLVENT_CONSTANTS`) to
    auto-fill K_b.

    Returns the full {K_b, molality_b, van_t_hoff_i,
    delta_T_b} dict.
    """
    if solvent is not None and K_b is None:
        if solvent not in SOLVENT_CONSTANTS:
            raise ValueError(
                f"Unknown solvent {solvent!r}; valid: "
                f"{', '.join(SOLVENT_CONSTANTS)}.")
        K_b = SOLVENT_CONSTANTS[solvent]["K_b"]
    given = {
        "K_b": K_b, "molality_b": molality_b,
        "van_t_hoff_i": van_t_hoff_i, "delta_T_b": delta_T_b,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities (or solvent + 2 of "
            f"the rest); got {len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be > 0; got {v!r}.")
    if missing == ["delta_T_b"]:
        given["delta_T_b"] = K_b * molality_b * van_t_hoff_i
    elif missing == ["K_b"]:
        given["K_b"] = delta_T_b / (molality_b * van_t_hoff_i)
    elif missing == ["molality_b"]:
        given["molality_b"] = delta_T_b / (K_b * van_t_hoff_i)
    else:
        given["van_t_hoff_i"] = delta_T_b / (K_b * molality_b)
    return given


def freezing_point_depression(
    K_f: Optional[float] = None,
    molality_b: Optional[float] = None,
    van_t_hoff_i: Optional[float] = None,
    delta_T_f: Optional[float] = None,
    solvent: Optional[str] = None,
) -> Dict[str, float]:
    """Mirror of :func:`boiling_point_elevation` for the
    cryoscopic constant K_f."""
    if solvent is not None and K_f is None:
        if solvent not in SOLVENT_CONSTANTS:
            raise ValueError(
                f"Unknown solvent {solvent!r}; valid: "
                f"{', '.join(SOLVENT_CONSTANTS)}.")
        K_f = SOLVENT_CONSTANTS[solvent]["K_f"]
    given = {
        "K_f": K_f, "molality_b": molality_b,
        "van_t_hoff_i": van_t_hoff_i, "delta_T_f": delta_T_f,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities (or solvent + 2 of "
            f"the rest); got {len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be > 0; got {v!r}.")
    if missing == ["delta_T_f"]:
        given["delta_T_f"] = K_f * molality_b * van_t_hoff_i
    elif missing == ["K_f"]:
        given["K_f"] = delta_T_f / (molality_b * van_t_hoff_i)
    elif missing == ["molality_b"]:
        given["molality_b"] = delta_T_f / (K_f * van_t_hoff_i)
    else:
        given["van_t_hoff_i"] = delta_T_f / (K_f * molality_b)
    return given


def osmotic_pressure(
    molarity_M: Optional[float] = None,
    temperature_K: Optional[float] = None,
    van_t_hoff_i: Optional[float] = None,
    pressure_atm: Optional[float] = None,
) -> Dict[str, float]:
    """Solve Π = M·R·T·i.  Pass any 3 of 4 quantities.  Pressure
    in atm, M in mol/L, T in K, i dimensionless."""
    given = {
        "molarity_M": molarity_M,
        "temperature_K": temperature_K,
        "van_t_hoff_i": van_t_hoff_i,
        "pressure_atm": pressure_atm,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be > 0; got {v!r}.")
    R = _R_L_ATM_PER_MOL_K
    if missing == ["pressure_atm"]:
        given["pressure_atm"] = (
            molarity_M * R * temperature_K * van_t_hoff_i)
    elif missing == ["molarity_M"]:
        given["molarity_M"] = pressure_atm / (
            R * temperature_K * van_t_hoff_i)
    elif missing == ["temperature_K"]:
        given["temperature_K"] = pressure_atm / (
            molarity_M * R * van_t_hoff_i)
    else:
        given["van_t_hoff_i"] = pressure_atm / (
            molarity_M * R * temperature_K)
    return given
