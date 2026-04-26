"""Phase 39a (round 142) — acid-base calculators.

- pH ↔ [H⁺] / pOH ↔ [OH⁻].
- pKa ↔ Ka.
- Henderson-Hasselbalch (pH ↔ pKa + log [A⁻]/[HA]).
"""
from __future__ import annotations
import math
from typing import Dict, Optional


def ph_from_h(h_concentration_M: float) -> Dict[str, float]:
    """pH = -log10([H⁺]).  Returns the full {pH, pOH, [H⁺],
    [OH⁻]} set assuming aqueous + 25 °C (pH + pOH = 14)."""
    if h_concentration_M <= 0:
        raise ValueError(
            "h_concentration_M must be > 0 (use ≥ 1e-15 for "
            "very dilute strong acid).")
    pH = -math.log10(h_concentration_M)
    pOH = 14.0 - pH
    return {
        "pH": pH,
        "pOH": pOH,
        "h_concentration_M": h_concentration_M,
        "oh_concentration_M": 10 ** (-pOH),
    }


def h_from_ph(pH: float) -> Dict[str, float]:
    """[H⁺] = 10^-pH.  Same return shape as :func:`ph_from_h`."""
    if not (0 <= pH <= 14):
        # Not strictly an error (super-acids / super-bases
        # exist) but flag for the user.
        raise ValueError(
            f"pH outside [0, 14] aqueous range; got {pH!r}.")
    return ph_from_h(10 ** (-pH))


def pka_to_ka(pKa: float) -> Dict[str, float]:
    if pKa < -10 or pKa > 50:
        raise ValueError(
            f"pKa outside reasonable range; got {pKa!r}.")
    return {"pKa": pKa, "Ka": 10 ** (-pKa)}


def ka_to_pka(Ka: float) -> Dict[str, float]:
    if Ka <= 0:
        raise ValueError(f"Ka must be > 0; got {Ka!r}.")
    return {"Ka": Ka, "pKa": -math.log10(Ka)}


def henderson_hasselbalch(
    pH: Optional[float] = None,
    pKa: Optional[float] = None,
    base_acid_ratio: Optional[float] = None,
) -> Dict[str, float]:
    """Solve pH = pKa + log10([A⁻]/[HA]).  Pass any 2 of 3.

    The buffer-design entry point for *"how much A⁻ + HA do I
    mix to get a buffer at pH X with weak-acid pKa Y?"*.
    """
    given = {
        "pH": pH, "pKa": pKa, "base_acid_ratio": base_acid_ratio,
    }
    missing = [k for k, v in given.items() if v is None]
    if len(missing) != 1:
        raise ValueError(
            f"Pass exactly 2 of 3 quantities; got "
            f"{len(missing)} missing.")
    if base_acid_ratio is not None and base_acid_ratio <= 0:
        raise ValueError(
            "base_acid_ratio must be > 0; got "
            f"{base_acid_ratio!r}.")
    if missing == ["pH"]:
        given["pH"] = pKa + math.log10(base_acid_ratio)
    elif missing == ["pKa"]:
        given["pKa"] = pH - math.log10(base_acid_ratio)
    else:
        given["base_acid_ratio"] = 10 ** (pH - pKa)
    return given
