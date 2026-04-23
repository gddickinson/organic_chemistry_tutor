"""Teaching-grade lab-technique helpers — Phase 15a-lite.

Three small utilities bridging physical-property data to practical
benchwork decisions:

- **Recrystallisation**: an idealised solubility-vs-temperature curve
  and a "recrystallisation yield" calculator.
- **Distillation**: pick up the boiling-point list for a mixture of
  seeded molecules and estimate which pair can be cleanly separated
  (ΔT_b > 25 °C ≈ simple distillation; 5–25 °C ≈ fractional;
  <5 °C ≈ not distinct; use another technique).
- **Acid-base extraction**: predict partitioning between an organic
  layer and an aqueous pH given a molecule's pKa (Henderson-Hasselbalch).

None of these replace real-world judgement — they're teaching models.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp
from typing import Any, Dict, List, Optional, Tuple

from rdkit import Chem
from rdkit.Chem import Descriptors


# ---- Recrystallisation ----------------------------------------------

def solubility_curve(s_hot_g_per_100ml: float, s_cold_g_per_100ml: float,
                     t_hot_c: float = 80.0, t_cold_c: float = 5.0,
                     n_points: int = 20) -> List[Tuple[float, float]]:
    """A monotonic solubility curve fit to two anchor points.

    Many solid-organic solubilities follow an Arrhenius-ish exponential
    in T. Given the hot / cold anchors, fit ``s(T) = A · exp(B · T)`` and
    sample ``n_points`` evenly between ``t_cold_c`` and ``t_hot_c``.
    Returns a list of ``(T °C, solubility g/100 mL)`` pairs.
    """
    if t_hot_c <= t_cold_c:
        raise ValueError("t_hot_c must be greater than t_cold_c")
    if s_hot_g_per_100ml <= 0 or s_cold_g_per_100ml <= 0:
        raise ValueError("solubilities must be positive")
    # s(T) = A * exp(B * T); solve for A, B from the two anchors.
    import math
    B = math.log(s_hot_g_per_100ml / s_cold_g_per_100ml) / (t_hot_c - t_cold_c)
    A = s_cold_g_per_100ml / math.exp(B * t_cold_c)
    out: List[Tuple[float, float]] = []
    for i in range(n_points + 1):
        t = t_cold_c + (t_hot_c - t_cold_c) * i / n_points
        out.append((t, A * exp(B * t)))
    return out


def recrystallisation_yield(s_hot: float, s_cold: float,
                            m_crude_g: float, solvent_volume_ml: float,
                            purity_hot: float = 1.0) -> Dict[str, Any]:
    """How much crude product recrystallises, in grams and percent.

    Assumes the crude dissolves fully in the hot solvent volume at
    solubility ``s_hot`` (g/100 mL); on cooling the saturated solution
    sheds ``m_crude − (s_cold × volume / 100)`` grams as crystals.

    ``purity_hot`` (0–1) is the assumed mass fraction of the desired
    compound in the crude; impurities are assumed to stay in the mother
    liquor.
    """
    if solvent_volume_ml <= 0 or m_crude_g <= 0:
        return {"error": "mass and solvent volume must be positive"}
    m_desired = m_crude_g * purity_hot
    # max dissolved at hot T:
    max_hot = s_hot * solvent_volume_ml / 100.0
    if m_desired > max_hot:
        return {"error": "crude doesn't fully dissolve at hot T — "
                         "increase solvent volume or pick a better solvent"}
    retained_in_liquor = s_cold * solvent_volume_ml / 100.0
    crystals = m_desired - retained_in_liquor
    if crystals <= 0:
        return {"error": "product is too soluble even cold — won't crystallise"}
    yield_pct = 100.0 * crystals / m_desired
    return {
        "crystals_g": crystals,
        "retained_g": retained_in_liquor,
        "yield_pct": yield_pct,
        "m_desired_g": m_desired,
        "s_hot": s_hot, "s_cold": s_cold,
        "solvent_volume_ml": solvent_volume_ml,
    }


# ---- Distillation ---------------------------------------------------

@dataclass
class DistillationRow:
    name: str
    smiles: str
    bp_celsius: Optional[float]


#: Textbook boiling points (°C at 1 atm) for the molecules a teaching
#: distillation demo is likely to touch. Missing entries fall back to the
#: Joback estimate; we only ship empirical values where we've verified them.
_BP_TABLE_C: Dict[str, float] = {
    "Water":            100.0,
    "Methanol":         64.7,
    "Ethanol":          78.4,
    "Propan-1-ol":      97.2,
    "Propan-2-ol":      82.5,
    "Butan-1-ol":       117.7,
    "tert-Butanol":     82.4,
    "Acetone":          56.0,
    "2-Butanone":       79.6,
    "DMSO":             189.0,
    "DMF":              153.0,
    "THF":              66.0,
    "Diethyl ether":    34.6,
    "Acetonitrile":     81.6,
    "Acetic acid":      118.1,
    "Formic acid":      100.8,
    "Benzene":          80.1,
    "Toluene":          110.6,
    "Hexane":           68.7,
    "Pentane":          36.1,
    "Heptane":          98.4,
    "Octane":           125.7,
    "Chloroform":       61.2,
    "Methanol":         64.7,
    "Formaldehyde":     -19.0,
    "Acetaldehyde":     20.0,
    "Propanal":         48.0,
    "Benzaldehyde":     178.1,
    "Acetic anhydride": 139.8,
    "Dimethyl ether":   -24.0,
    "Ethylene oxide":   10.7,
    "Propylene oxide":  34.0,
}


def boiling_point(name: str) -> Optional[float]:
    """Return tabulated bp (°C) for a seeded molecule, or None if unknown."""
    return _BP_TABLE_C.get(name)


def distillation_plan(pair: Tuple[str, str]) -> Dict[str, Any]:
    """Recommend a distillation technique for a two-component mixture."""
    a, b = pair
    bp_a = boiling_point(a)
    bp_b = boiling_point(b)
    if bp_a is None or bp_b is None:
        return {"error": f"no bp data for {a if bp_a is None else b}"}
    lo_name, lo_bp = (a, bp_a) if bp_a <= bp_b else (b, bp_b)
    hi_name, hi_bp = (b, bp_b) if bp_a <= bp_b else (a, bp_a)
    delta = hi_bp - lo_bp
    if delta >= 25:
        technique = "simple distillation"
        rationale = "ΔTb ≥ 25 °C — one theoretical plate usually suffices."
    elif delta >= 5:
        technique = "fractional distillation"
        rationale = "5 °C ≤ ΔTb < 25 °C — needs a packed column."
    else:
        technique = "not distillable — use chromatography or extraction"
        rationale = "ΔTb < 5 °C — azeotrope risk; distillation won't resolve."
    return {
        "lower_bp_component": lo_name, "lower_bp_c": lo_bp,
        "higher_bp_component": hi_name, "higher_bp_c": hi_bp,
        "delta_c": delta,
        "technique": technique,
        "rationale": rationale,
    }


# ---- Acid-base extraction -------------------------------------------

def fraction_ionised(pka: float, ph: float, is_acid: bool) -> float:
    """Henderson-Hasselbalch: fraction of species in the **ionised** form.

    Acid  HA ⇌ H⁺ + A⁻:  fraction A⁻ = 1 / (1 + 10^(pKa − pH))
    Base  B + H⁺ ⇌ BH⁺:   fraction BH⁺ = 1 / (1 + 10^(pH − pKa))
    """
    if is_acid:
        return 1.0 / (1.0 + 10 ** (pka - ph))
    return 1.0 / (1.0 + 10 ** (ph - pka))


def extraction_plan(pka: float, ph: float, is_acid: bool,
                    logp_neutral: Optional[float] = None) -> Dict[str, Any]:
    """Predict where a molecule partitions in an acid-base extraction.

    The neutral form partitions into the organic layer (logP applies);
    the ionised form (A⁻ or BH⁺) strongly prefers water. We report both
    fractions and a 'goes to organic' boolean for the common teaching case.
    """
    f_ion = fraction_ionised(pka, ph, is_acid)
    f_neut = 1.0 - f_ion
    destination = "organic" if f_neut > 0.5 else "aqueous"
    tip = ""
    if is_acid and ph > pka + 2:
        tip = "aqueous: acidify the water layer to extract back"
    elif is_acid and ph < pka - 2:
        tip = "organic: protonated form; will cross into the organic layer"
    elif not is_acid and ph < pka - 2:
        tip = "aqueous: basify the water layer to extract back"
    elif not is_acid and ph > pka + 2:
        tip = "organic: unprotonated; will cross into the organic layer"
    return {
        "fraction_neutral": f_neut,
        "fraction_ionised": f_ion,
        "preferred_phase": destination,
        "logp_neutral": logp_neutral,
        "note": tip,
    }


def logp_of(smiles: str) -> float:
    """Crippen logP of a SMILES; useful in conjunction with extraction_plan."""
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        raise ValueError(f"Unparseable SMILES: {smiles!r}")
    from rdkit.Chem import Crippen
    return float(Crippen.MolLogP(m))
