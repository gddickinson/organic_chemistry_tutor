"""Phase 39a (round 142) — solution-preparation + dilution +
concentration-unit calculations.

Every solver follows the Phase-37d ``beer_lambert_solve``
pattern: pass any N-1 of N quantities (use ``None`` for the
unknown), get the full set back with the Nth filled in.
``ValueError`` on missing-count != 1 or non-positive input.
"""
from __future__ import annotations
from typing import Dict, Optional


# ------------------------------------------------------------------
# Molarity ↔ mass / volume / MW
#   m = M · V · MW
# ------------------------------------------------------------------

def molarity_solve(
    mass_g: Optional[float] = None,
    molarity_M: Optional[float] = None,
    volume_L: Optional[float] = None,
    molecular_weight_gmol: Optional[float] = None,
) -> Dict[str, float]:
    """Solve ``mass_g = molarity_M · volume_L ·
    molecular_weight_gmol``.  Pass any 3 of 4; the fourth is
    computed."""
    given = {
        "mass_g": mass_g,
        "molarity_M": molarity_M,
        "volume_L": volume_L,
        "molecular_weight_gmol": molecular_weight_gmol,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be positive; got {v!r}.")
    if missing == ["mass_g"]:
        given["mass_g"] = (
            molarity_M * volume_L * molecular_weight_gmol)
    elif missing == ["molarity_M"]:
        given["molarity_M"] = (
            mass_g / (volume_L * molecular_weight_gmol))
    elif missing == ["volume_L"]:
        given["volume_L"] = (
            mass_g / (molarity_M * molecular_weight_gmol))
    else:
        given["molecular_weight_gmol"] = (
            mass_g / (molarity_M * volume_L))
    return given


# ------------------------------------------------------------------
# Dilution: M₁V₁ = M₂V₂
# ------------------------------------------------------------------

def dilution_solve(
    M1: Optional[float] = None,
    V1: Optional[float] = None,
    M2: Optional[float] = None,
    V2: Optional[float] = None,
) -> Dict[str, float]:
    """Solve M₁·V₁ = M₂·V₂.  Pass any 3 of 4."""
    given = {"M1": M1, "V1": V1, "M2": M2, "V2": V2}
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 3 of 4 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be positive; got {v!r}.")
    if missing == ["M1"]:
        given["M1"] = M2 * V2 / V1
    elif missing == ["V1"]:
        given["V1"] = M2 * V2 / M1
    elif missing == ["M2"]:
        given["M2"] = M1 * V1 / V2
    else:
        given["V2"] = M1 * V1 / M2
    return given


def serial_dilution(
    initial_concentration: float,
    dilution_factor: float,
    n_steps: int,
) -> Dict[str, object]:
    """Compute the concentration at each step of a serial
    dilution.  Each step divides the previous concentration by
    ``dilution_factor``.  Returns
    ``{"concentrations": [c0, c1, ..., c_n]}`` (length n_steps + 1)."""
    if initial_concentration <= 0:
        raise ValueError("initial_concentration must be > 0")
    if dilution_factor <= 1:
        raise ValueError(
            "dilution_factor must be > 1 (a dilution increases "
            "volume / decreases concentration)")
    if n_steps < 1:
        raise ValueError("n_steps must be ≥ 1")
    concentrations = [initial_concentration]
    c = initial_concentration
    for _ in range(n_steps):
        c = c / dilution_factor
        concentrations.append(c)
    return {
        "concentrations": concentrations,
        "final_concentration": concentrations[-1],
        "total_dilution": dilution_factor ** n_steps,
    }


# ------------------------------------------------------------------
# Mass-percent + density → molarity
#   M = (% w/w · ρ · 10) / MW    [ρ in g/mL]
# ------------------------------------------------------------------

def molarity_from_mass_percent(
    mass_percent: float,
    density_g_per_mL: float,
    molecular_weight_gmol: float,
) -> Dict[str, float]:
    """Compute molarity of a w/w% solution given density.

    Example: concentrated HCl is 37 % w/w, density 1.18 g/mL,
    MW 36.46 → molarity ≈ 12.0 M.
    """
    for name, val in (("mass_percent", mass_percent),
                      ("density_g_per_mL", density_g_per_mL),
                      ("molecular_weight_gmol",
                       molecular_weight_gmol)):
        if val <= 0:
            raise ValueError(f"{name} must be positive; got {val!r}.")
    if mass_percent > 100:
        raise ValueError(
            "mass_percent > 100 — pass a percentage, not a "
            "mass fraction.")
    molarity = (mass_percent * density_g_per_mL * 10
                ) / molecular_weight_gmol
    return {
        "molarity_M": molarity,
        "mass_percent": mass_percent,
        "density_g_per_mL": density_g_per_mL,
        "molecular_weight_gmol": molecular_weight_gmol,
    }


# ------------------------------------------------------------------
# ppm / ppb / mg/L conversions
# ------------------------------------------------------------------

def ppm_to_molarity(ppm: float,
                    molecular_weight_gmol: float
                    ) -> Dict[str, float]:
    """Convert ppm (mg / L for a dilute aqueous solution) to
    molarity.  M = ppm / (1000 · MW)."""
    if ppm < 0:
        raise ValueError(f"ppm must be ≥ 0; got {ppm!r}.")
    if molecular_weight_gmol <= 0:
        raise ValueError(
            f"molecular_weight_gmol must be positive; got "
            f"{molecular_weight_gmol!r}.")
    return {
        "ppm": ppm,
        "molarity_M": ppm / (1000.0 * molecular_weight_gmol),
        "molecular_weight_gmol": molecular_weight_gmol,
    }


def molarity_to_ppm(molarity_M: float,
                    molecular_weight_gmol: float
                    ) -> Dict[str, float]:
    """Reverse of :func:`ppm_to_molarity`."""
    if molarity_M < 0:
        raise ValueError(f"molarity_M must be ≥ 0; got {molarity_M!r}.")
    if molecular_weight_gmol <= 0:
        raise ValueError(
            f"molecular_weight_gmol must be positive; got "
            f"{molecular_weight_gmol!r}.")
    return {
        "molarity_M": molarity_M,
        "ppm": molarity_M * 1000.0 * molecular_weight_gmol,
        "molecular_weight_gmol": molecular_weight_gmol,
    }
