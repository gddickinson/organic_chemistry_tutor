"""Phase 39a (round 142) — stoichiometry calculators.

- Limiting reagent finder.
- Theoretical yield from limiting reagent + product MW.
- Percent yield (actual / theoretical × 100).
- Percent purity (mass-known / mass-sample × 100).
"""
from __future__ import annotations
from typing import Dict, List, Optional


def limiting_reagent(
    reagents: List[Dict[str, float]],
) -> Dict[str, object]:
    """Find the limiting reagent in a multi-reagent reaction.

    Each entry in *reagents* is a dict with:
    - ``"name"``: free-text label.
    - ``"moles"``: moles available (or compute from
      ``"mass_g"`` + ``"molecular_weight_gmol"`` outside this
      call).
    - ``"stoich_coeff"``: stoichiometric coefficient from the
      balanced equation (``1`` for the simplest 1:1 case).

    Returns ``{"limiting_index", "limiting_name",
    "available_eq_units": [n / coeff per reagent]}``.  The
    reagent with the smallest ``moles / stoich_coeff`` quotient
    is the limiting one.
    """
    if not reagents:
        raise ValueError("Need ≥ 1 reagent.")
    eq_units = []
    for i, r in enumerate(reagents):
        for k in ("moles", "stoich_coeff"):
            if k not in r:
                raise ValueError(
                    f"reagent[{i}]: missing key {k!r}")
            if r[k] <= 0:
                raise ValueError(
                    f"reagent[{i}].{k} must be > 0; got {r[k]!r}")
        eq_units.append(r["moles"] / r["stoich_coeff"])
    limiting_idx = min(range(len(reagents)),
                       key=lambda i: eq_units[i])
    limiting_name = reagents[limiting_idx].get(
        "name", f"reagent_{limiting_idx}")
    return {
        "limiting_index": limiting_idx,
        "limiting_name": limiting_name,
        "available_eq_units": eq_units,
        "limiting_eq_units": eq_units[limiting_idx],
    }


def theoretical_yield_g(
    limiting_moles: float,
    limiting_stoich_coeff: float,
    product_stoich_coeff: float,
    product_mw_gmol: float,
) -> Dict[str, float]:
    """Theoretical mass of product (g) from limiting-reagent
    moles + stoichiometric coefficients + product MW.

    moles_product = (limiting_moles / limiting_stoich_coeff)
                  · product_stoich_coeff
    mass_product = moles_product · product_mw_gmol
    """
    for name, val in (("limiting_moles", limiting_moles),
                      ("limiting_stoich_coeff",
                       limiting_stoich_coeff),
                      ("product_stoich_coeff",
                       product_stoich_coeff),
                      ("product_mw_gmol", product_mw_gmol)):
        if val <= 0:
            raise ValueError(f"{name} must be positive; got {val!r}.")
    moles_product = (
        limiting_moles / limiting_stoich_coeff
        * product_stoich_coeff)
    return {
        "moles_product": moles_product,
        "theoretical_yield_g": moles_product * product_mw_gmol,
    }


def percent_yield(
    actual_yield_g: Optional[float] = None,
    theoretical_yield_g: Optional[float] = None,
    percent: Optional[float] = None,
) -> Dict[str, float]:
    """Solve percent = 100 · actual / theoretical.  Pass any 2
    of 3."""
    given = {
        "actual_yield_g": actual_yield_g,
        "theoretical_yield_g": theoretical_yield_g,
        "percent": percent,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 2 of 3 quantities; got "
            f"{len(missing)} missing.")
    for k, v in given.items():
        if v is not None and v <= 0:
            raise ValueError(f"{k} must be positive; got {v!r}.")
    if missing == ["percent"]:
        given["percent"] = 100 * actual_yield_g / theoretical_yield_g
    elif missing == ["actual_yield_g"]:
        given["actual_yield_g"] = (
            theoretical_yield_g * percent / 100)
    else:
        given["theoretical_yield_g"] = (
            actual_yield_g * 100 / percent)
    return given


def percent_purity(
    pure_mass_g: float,
    sample_mass_g: float,
) -> Dict[str, float]:
    """Percent purity = 100 · pure mass / sample mass."""
    if pure_mass_g <= 0 or sample_mass_g <= 0:
        raise ValueError("masses must be positive")
    if pure_mass_g > sample_mass_g:
        raise ValueError(
            "pure_mass_g > sample_mass_g — purity > 100 % is "
            "impossible.")
    return {
        "pure_mass_g": pure_mass_g,
        "sample_mass_g": sample_mass_g,
        "percent_purity": 100 * pure_mass_g / sample_mass_g,
    }
