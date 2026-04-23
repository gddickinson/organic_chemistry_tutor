"""Teaching-grade mass-spectrum predictor — Phase 4.

Two outputs that matter for interpreting a teaching MS spectrum:

1. **Monoisotopic mass** (M⁺ peak position). Computed from the most-
   abundant isotope of each element — matches HRMS to ~10⁻³ Da.
2. **Isotope pattern** (M, M+1, M+2, M+3 … relative heights). Computed
   by polynomial convolution of per-element isotope distributions.
   Diagnostic for halogens (one Cl → M+2 at 33 %; one Br → M+2 at 98 %)
   and sulfur.

Covered elements: H, C, N, O, F, P, S, Cl, Br, I. These account for
>99 % of organic-chem teaching content; exotic heteroatoms (B, Si, Sn,
…) use the IUPAC abundances but are not individually tabulated here —
they fall through to a single-isotope approximation.

Numbers from the 2021 IUPAC Technical Report on isotopic abundances
(Meija et al., Pure Appl. Chem. 2022). Values round to the same
digits students see in the Silverstein table.
"""
from __future__ import annotations
import logging
from typing import Dict, List, Tuple

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

log = logging.getLogger(__name__)


# (mass, abundance) per isotope, most-abundant first.
ISOTOPES: Dict[str, List[Tuple[float, float]]] = {
    "H":  [(1.00783, 0.999885),  (2.01410, 0.000115)],
    "C":  [(12.00000, 0.9893),   (13.00336, 0.0107)],
    "N":  [(14.00307, 0.99636),  (15.00011, 0.00364)],
    "O":  [(15.99491, 0.99757),  (16.99913, 0.00038), (17.99916, 0.00205)],
    "F":  [(18.99840, 1.0)],
    "P":  [(30.97376, 1.0)],
    "S":  [(31.97207, 0.9499),   (32.97146, 0.0075),  (33.96787, 0.0425)],
    "Cl": [(34.96885, 0.7576),   (36.96590, 0.2424)],
    "Br": [(78.91834, 0.5069),   (80.91629, 0.4931)],
    "I":  [(126.90447, 1.0)],
}


# ---------------------------------------------------------------------

def _element_counts(smiles: str) -> Dict[str, int]:
    """Return an element → count dict (hydrogens inferred)."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {}
    mol_h = Chem.AddHs(mol)
    counts: Dict[str, int] = {}
    for atom in mol_h.GetAtoms():
        sym = atom.GetSymbol()
        counts[sym] = counts.get(sym, 0) + 1
    return counts


def monoisotopic_mass(smiles: str) -> float:
    """Exact mass using the most-abundant isotope of every element.

    Returns 0.0 on parse failure.
    """
    counts = _element_counts(smiles)
    if not counts:
        return 0.0
    total = 0.0
    for sym, n in counts.items():
        if sym in ISOTOPES:
            total += n * ISOTOPES[sym][0][0]
        else:
            # Unknown element: fall back to RDKit's table for safety.
            try:
                pt = Chem.GetPeriodicTable()
                total += n * pt.GetMostCommonIsotopeMass(pt.GetAtomicNumber(sym))
            except Exception:
                pass
    return total


def _convolve(a: List[Tuple[float, float]],
              b: List[Tuple[float, float]],
              mass_tolerance: float = 0.5,
              min_abundance: float = 1e-6,
              max_peaks: int = 20) -> List[Tuple[float, float]]:
    """Merge two peak lists (mass, abundance) into a combined distribution.

    Merges peaks whose masses differ by less than ``mass_tolerance`` (Da).
    Prunes peaks below ``min_abundance`` and truncates to ``max_peaks``.
    """
    out: List[Tuple[float, float]] = []
    for (m1, a1) in a:
        for (m2, a2) in b:
            out.append((m1 + m2, a1 * a2))
    # Sort, then merge adjacent peaks.
    out.sort(key=lambda p: p[0])
    merged: List[Tuple[float, float]] = []
    for m, a in out:
        if merged and abs(m - merged[-1][0]) < mass_tolerance:
            prev_m, prev_a = merged[-1]
            total_a = prev_a + a
            # Weighted average mass.
            new_m = (prev_m * prev_a + m * a) / total_a if total_a else m
            merged[-1] = (new_m, total_a)
        else:
            merged.append((m, a))
    # Prune + truncate.
    merged = [(m, a) for m, a in merged if a >= min_abundance]
    merged.sort(key=lambda p: -p[1])
    return merged[:max_peaks]


def isotope_pattern(smiles: str, normalise: bool = True,
                    max_peaks: int = 8) -> Dict[str, object]:
    """Compute the isotope envelope around M⁺.

    Returns ``{"monoisotopic_mass": float, "formula": str,
    "peaks": [ {"mz": m, "intensity": rel_abundance_0_to_1,
    "label": "M"/"M+1"/... }, ... ]}``. Peaks are sorted by ``mz`` and
    (if ``normalise=True``) intensities are scaled so the most intense
    peak = 1.0.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"error": f"Unparseable SMILES: {smiles!r}"}
    mol_h = Chem.AddHs(mol)
    counts = _element_counts(smiles)
    if not counts:
        return {"error": f"Empty molecule for {smiles!r}"}

    # Start with a unit peak; convolve in each element's contribution
    # once per atom.
    dist: List[Tuple[float, float]] = [(0.0, 1.0)]
    for sym, n in counts.items():
        iso = ISOTOPES.get(sym)
        if iso is None:
            # Single-isotope fallback: add mass once.
            try:
                pt = Chem.GetPeriodicTable()
                m = pt.GetMostCommonIsotopeMass(pt.GetAtomicNumber(sym))
                dist = [(mm + n * m, aa) for mm, aa in dist]
            except Exception:
                pass
            continue
        for _ in range(n):
            dist = _convolve(dist, iso)

    # Sort by mass for the envelope, keep the top ``max_peaks`` most
    # intense, re-sort by mass.
    dist.sort(key=lambda p: -p[1])
    dist = dist[:max_peaks]
    dist.sort(key=lambda p: p[0])

    if not dist:
        return {"error": "empty isotope distribution"}

    mono_mass = dist[0][0]
    peaks: List[Dict[str, object]] = []
    max_a = max(a for _, a in dist)
    for i, (m, a) in enumerate(dist):
        rel = a / max_a if normalise else a
        # Label: integer mass shift from the monoisotopic.
        shift = int(round(m - mono_mass))
        label = "M" if shift == 0 else f"M+{shift}"
        peaks.append({
            "mz": round(m, 4),
            "intensity": round(rel, 4),
            "label": label,
        })

    formula = rdMolDescriptors.CalcMolFormula(mol)

    return {
        "smiles": Chem.MolToSmiles(mol),
        "formula": formula,
        "monoisotopic_mass": round(monoisotopic_mass(smiles), 4),
        "peaks": peaks,
    }


def describe_ms(smiles: str) -> str:
    """Markdown MS summary for the tutor layer."""
    r = isotope_pattern(smiles)
    if "error" in r:
        return f"**Error**: {r['error']}"
    lines = [
        f"### Predicted MS — `{r['smiles']}`",
        "",
        f"- **Formula**: {r['formula']}",
        f"- **Monoisotopic mass**: {r['monoisotopic_mass']:.4f} Da",
        "",
        "| Peak | m/z | Relative intensity |",
        "|------|------|--------------------|",
    ]
    for p in r["peaks"]:
        lines.append(f"| {p['label']} | {p['mz']:.4f} | "
                     f"{p['intensity']*100:.1f}% |")
    return "\n".join(lines)
