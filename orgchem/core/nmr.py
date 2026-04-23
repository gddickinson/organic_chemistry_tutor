"""Teaching-grade NMR shift predictor — Phase 4 extension.

Follows the IR-predictor design pattern: a table of SMARTS patterns
that match functional-group environments, each annotated with a
**canonical chemical-shift range** (in ppm) and — for ¹H — an expected
multiplicity / integration hint. Given a SMILES, scan every H-bearing
(for ¹H) or every non-H (for ¹³C) atom and emit the predicted peak
list.

The approach is equivalent to what a student does with the Pretsch or
Silverstein shift charts: map the atom to the right environment row,
look up the ppm range, and note the expected coupling partners. It's
**not** an ab-initio shift calculation — real NMR data comes from
experiment or GIAO/DFT.

Calibration: shift ranges approximated to the canonical Silverstein /
Pretsch values. This teaching model trades precision for scope —
every major functional group covered, each with one line of code.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from rdkit import Chem


@dataclass(frozen=True)
class NMRPattern:
    """One row of a chemical-shift correlation table."""
    environment: str
    #: SMARTS pattern. The **first mapped atom** is the reporter
    #: (``[C:1]`` or ``[H:1]``). We enumerate every match and emit one
    #: peak per match.
    smarts: str
    #: (low_ppm, high_ppm) inclusive range
    range_ppm: Tuple[float, float]
    #: "H" or "C" — which nucleus this row predicts
    nucleus: str
    #: Multiplicity hint for ¹H (``"s"`` / ``"d"`` / ``"t"`` / ``"q"`` /
    #: ``"m"``). Ignored for ¹³C.
    multiplicity: str = ""
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment": self.environment, "smarts": self.smarts,
            "range_ppm": list(self.range_ppm), "nucleus": self.nucleus,
            "multiplicity": self.multiplicity, "note": self.note,
        }


# ---------------------------------------------------------------------
# ¹H chemical-shift patterns. Ordered low-to-high ppm.

H_PATTERNS: List[NMRPattern] = [
    NMRPattern("CH₃ (alkyl)", "[CX4H3][#6]", (0.7, 1.3), "H", "t/m",
               note="Triplet if on CH₂, singlet if on quaternary C."),
    NMRPattern("CH₂ (alkyl chain)", "[CX4H2]([#6])[#6]", (1.2, 1.7), "H",
               "m", note="Two sets of neighbours → multiplet."),
    NMRPattern("CH (alkyl)", "[CX4H1]([#6])([#6])[#6]", (1.5, 2.0), "H",
               "m"),
    NMRPattern("=CH (allylic / α to C=O)", "[CX4H][#6]=[#6]",
               (2.0, 2.6), "H", "m"),
    NMRPattern("CH₃ α to carbonyl", "[CH3][CX3](=O)",
               (2.0, 2.6), "H", "s",
               note="Acetyl methyl: ~2.1 ppm; ketone α-methyl ~2.1–2.6."),
    NMRPattern("=CH (benzylic)", "[CX4H][c]", (2.3, 2.9), "H", "m"),
    NMRPattern("CH₂ α to aryl", "[CX4H2]([c])[#6]", (2.3, 2.9), "H", "m"),
    NMRPattern("CH₃ on N (amine)", "[CH3][NX3]", (2.2, 3.0), "H", "s"),
    NMRPattern("CH₃ on O (methoxy)", "[CH3][OX2]", (3.3, 3.9), "H", "s",
               note="Classic methoxy singlet near 3.8 ppm."),
    NMRPattern("CH₂ next to O", "[CX4H2][OX2]", (3.3, 4.1), "H", "q/m"),
    NMRPattern("CH α to O (ester / ether)", "[CX4H][OX2]",
               (3.5, 4.5), "H", "m"),
    NMRPattern("Vinyl CH (alkene)", "[CX3H]=[CX3]", (5.0, 6.5), "H",
               "m", note="cis/trans affect J (cis ~10 Hz, trans ~17 Hz)."),
    NMRPattern("Aromatic CH (benzene-like)", "[cH]", (6.8, 7.8), "H",
               "m", note="Ortho coupling ~7–8 Hz; para ~0; meta ~2–3 Hz."),
    NMRPattern("Aldehyde CH", "[CX3H1](=O)", (9.0, 10.2), "H", "s",
               note="Diagnostic downfield singlet at 9-10 ppm."),
    NMRPattern("Carboxylic acid OH", "C(=O)[OX2H]", (10.0, 13.0), "H",
               "s-br", note="Very broad; exchanges with D₂O."),
    NMRPattern("Amide NH", "[NX3H][CX3](=O)", (6.0, 8.5), "H", "br",
               note="Broad; H-bonding shifts up to 9 ppm."),
    NMRPattern("Amine NH", "[NX3;H1,H2][CX4]", (0.5, 3.5), "H", "br",
               note="Very variable — concentration + solvent sensitive."),
    NMRPattern("Alcohol / phenol OH", "[OX2H1][#6]", (0.5, 5.5), "H",
               "br", note="Sharp in dilute CDCl₃; broad when H-bonded."),
]


# ---------------------------------------------------------------------
# ¹³C chemical-shift patterns. Ordered low-to-high ppm.

C_PATTERNS: List[NMRPattern] = [
    NMRPattern("CH₃ (alkyl)", "[CX4H3][#6]", (8, 30), "C"),
    NMRPattern("CH₂ (alkyl chain)", "[CX4H2]([#6])[#6]", (20, 40), "C"),
    NMRPattern("CH (alkyl)", "[CX4H1]([#6])([#6])[#6]", (25, 50), "C"),
    NMRPattern("Quaternary sp3 C", "[CX4;H0]([#6])([#6])([#6])[#6]",
               (30, 45), "C"),
    NMRPattern("C α to carbonyl", "[CX4][CX3](=O)", (20, 50), "C"),
    NMRPattern("C on N (amine)", "[CX4][NX3]", (30, 55), "C"),
    NMRPattern("C on O (alcohol / ether)", "[CX4][OX2]", (50, 75), "C"),
    NMRPattern("Alkyne C", "[CX2]#[CX2]", (65, 95), "C"),
    NMRPattern("Vinyl C (alkene sp2)", "[CX3]=[CX3]", (100, 150), "C"),
    NMRPattern("Aromatic C–H", "[cH]", (110, 135), "C"),
    NMRPattern("Aromatic C (substituted, ipso)", "[c;!H0]",
               (115, 150), "C"),
    NMRPattern("Amide C=O", "[CX3](=O)[NX3]", (165, 175), "C"),
    NMRPattern("Ester C=O", "[CX3](=O)[OX2]", (165, 175), "C"),
    NMRPattern("Acid C=O", "[CX3](=O)[OX2H1]", (170, 185), "C"),
    NMRPattern("Aldehyde C=O", "[CX3H](=O)", (190, 205), "C"),
    NMRPattern("Ketone C=O", "[#6][CX3](=O)[#6]", (195, 220), "C"),
]


# ---------------------------------------------------------------------
# Prediction engine

def predict_shifts(smiles: str, nucleus: str = "H") -> Dict[str, Any]:
    """Return predicted NMR peaks for ``smiles`` on the selected nucleus.

    Output::

        {"smiles": canonical,
         "nucleus": "H" | "C",
         "peaks": [ {"environment", "atom_indices", "range_ppm",
                     "multiplicity" (if H), "note"}, ... ]}

    Peaks are sorted high-to-low ppm (conventional NMR display).
    """
    nucleus = nucleus.upper().strip()
    if nucleus not in ("H", "C"):
        return {"error": f"nucleus must be 'H' or 'C', got {nucleus!r}"}

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"error": f"Unparseable SMILES: {smiles!r}"}

    patterns = H_PATTERNS if nucleus == "H" else C_PATTERNS
    peaks: List[Dict[str, Any]] = []
    for p in patterns:
        patt = Chem.MolFromSmarts(p.smarts)
        if patt is None:
            continue
        matches = mol.GetSubstructMatches(patt)
        if not matches:
            continue
        peak = p.to_dict()
        peak["atom_indices"] = [list(m) for m in matches]
        peak["n_matches"] = len(matches)
        peaks.append(peak)

    # Sort by descending upper ppm so peaks read left-to-right on a
    # traditional NMR axis.
    peaks.sort(key=lambda e: -max(e["range_ppm"]))

    return {
        "smiles": Chem.MolToSmiles(mol),
        "nucleus": nucleus,
        "peaks": peaks,
        "n_peaks": len(peaks),
    }


def describe_prediction(smiles: str, nucleus: str = "H") -> str:
    """Markdown summary of the prediction for the LLM tutor."""
    res = predict_shifts(smiles, nucleus)
    if "error" in res:
        return f"**Error**: {res['error']}"
    if not res["peaks"]:
        return (f"No {res['nucleus']}NMR environments matched for "
                f"{smiles!r} — molecule is outside the teaching-model's "
                "SMARTS coverage.")
    lines = [f"### Predicted {res['nucleus']} NMR — `{res['smiles']}`\n"]
    for pk in res["peaks"]:
        lo, hi = pk["range_ppm"]
        mult = f", {pk['multiplicity']}" if pk.get("multiplicity") else ""
        note = f" — {pk['note']}" if pk.get("note") else ""
        lines.append(
            f"- **{pk['environment']}**: {lo}–{hi} ppm{mult} "
            f"(×{pk['n_matches']}){note}"
        )
    return "\n".join(lines)
