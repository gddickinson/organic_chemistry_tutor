"""Teaching-grade spectroscopy predictors — Phase 4.

The first sub-feature is an **IR-band** predictor: given a SMILES, find
which functional-group classes it contains (via RDKit SMARTS matching)
and return the characteristic IR absorption bands with canonical wave-
number ranges, intensities, and pedagogical notes.

This is **not** a quantum / ab-initio IR calculation — those need DFT
and days of compute. Real IR data comes from measurement (NIST WebBook,
SDBS). What this module does is the same thing a student does when they
look up the "IR correlation chart" in the back of Pavia/Lampman: match
functional groups to approximate absorption regions.

Calibrated against the canonical undergraduate chart (Silverstein et al.,
*Spectrometric Identification of Organic Compounds*, 8th ed., Ch. 2).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from rdkit import Chem


@dataclass(frozen=True)
class IRBand:
    """A single characteristic IR band."""
    group: str
    #: SMARTS pattern used to detect the functional group
    smarts: str
    #: (low, high) wavenumber range in cm⁻¹
    range_cm1: tuple
    #: "strong" / "medium" / "weak" / "variable"
    intensity: str
    mode: str                    # stretching / bending / etc.
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group": self.group,
            "smarts": self.smarts,
            "range_cm1": list(self.range_cm1),
            "intensity": self.intensity,
            "mode": self.mode,
            "note": self.note,
        }


#: Canonical IR correlation chart — rough values for undergraduate
#: teaching. Ordered roughly by spectrum position (high wavenumber first)
#: so the predictor returns bands in the order a student scans left-to-right.
IR_BANDS: List[IRBand] = [
    # ---- 3700-3200: OH / NH stretches ----
    IRBand(group="O–H (alcohol/phenol, free)",
           # OH on sp3 C or aromatic C that is NOT a carbonyl carbon
           # (that's the separate COOH entry below).
           smarts="[OX2H1][CX4,c;!$([CX3]=[OX1])]",
           range_cm1=(3200, 3600), intensity="strong",
           mode="stretch (broad if H-bonded)",
           note="Very broad when H-bonded; sharp in dilute CCl₄."),
    IRBand(group="O–H (carboxylic acid, H-bonded dimer)",
           smarts="C(=O)[OH]",
           range_cm1=(2500, 3300), intensity="strong",
           mode="stretch (very broad)",
           note="Signature extremely broad envelope sitting on top of C-H; "
                "unmistakable for a carboxylic acid."),
    IRBand(group="N–H (1° amine / 2° amine / amide)",
           smarts="[NX3;H1,H2]",
           range_cm1=(3300, 3500), intensity="medium",
           mode="stretch",
           note="1° amine = 2 peaks (sym/asym), 2° amine = 1 peak, "
                "amide often 2 peaks around 3350/3180."),
    IRBand(group="≡C–H (terminal alkyne)",
           smarts="[CH]#C",
           range_cm1=(3250, 3330), intensity="strong",
           mode="stretch",
           note="Sharp, distinctive — only alkynes have C-H this high."),
    # ---- 3100-3000: =C-H / aromatic C-H stretches ----
    IRBand(group="=C–H (alkene)",
           smarts="[CX3H]=[CX3]",
           range_cm1=(3000, 3100), intensity="medium",
           mode="stretch"),
    IRBand(group="Aromatic C–H",
           smarts="[cH]",
           range_cm1=(3000, 3100), intensity="medium",
           mode="stretch"),
    # ---- 3000-2800: sp3 C-H ----
    IRBand(group="Aliphatic C–H (sp3)",
           smarts="[CX4;H1,H2,H3]",
           range_cm1=(2850, 3000), intensity="strong",
           mode="stretch",
           note="Almost every organic compound shows this — not usually "
                "diagnostic on its own."),
    IRBand(group="Aldehyde C–H (doublet)",
           smarts="[CX3H1](=O)",
           range_cm1=(2720, 2820), intensity="medium",
           mode="stretch (Fermi doublet)",
           note="Two sharp peaks — the diagnostic for aldehyde vs ketone."),
    # ---- 2260-2100: triple-bond stretches ----
    IRBand(group="C≡N (nitrile)",
           smarts="C#N",
           range_cm1=(2200, 2260), intensity="medium",
           mode="stretch",
           note="Sharp; a little lower when conjugated."),
    IRBand(group="C≡C (alkyne)",
           smarts="C#C",
           range_cm1=(2100, 2260), intensity="variable",
           mode="stretch",
           note="Terminal alkynes: medium. Internal symmetric alkynes: "
                "weak or absent."),
    # ---- 1800-1600: C=O, C=C, aromatic ----
    IRBand(group="C=O acid chloride",
           smarts="[CX3](=O)[Cl]",
           range_cm1=(1770, 1820), intensity="strong",
           mode="stretch",
           note="Highest C=O frequency — a dead giveaway for acyl chloride."),
    IRBand(group="C=O anhydride (two bands)",
           smarts="C(=O)OC(=O)",
           range_cm1=(1750, 1820), intensity="strong",
           mode="stretch (two bands ~60 cm⁻¹ apart)",
           note="Two bands: asym ~1820, sym ~1750."),
    IRBand(group="C=O ester",
           smarts="[CX3](=O)[OX2][CX4]",
           range_cm1=(1735, 1750), intensity="strong",
           mode="stretch",
           note="Very sharp; also a C-O stretch near 1200 cm⁻¹."),
    IRBand(group="C=O aldehyde",
           smarts="[CX3H1](=O)",
           range_cm1=(1720, 1740), intensity="strong",
           mode="stretch"),
    IRBand(group="C=O ketone",
           smarts="[#6][CX3](=O)[#6]",
           range_cm1=(1705, 1725), intensity="strong",
           mode="stretch",
           note="Conjugated ketones drop 20–40 cm⁻¹."),
    IRBand(group="C=O carboxylic acid",
           smarts="[CX3](=O)[OX2H]",
           range_cm1=(1705, 1720), intensity="strong",
           mode="stretch"),
    IRBand(group="C=O amide",
           smarts="[CX3](=O)[NX3]",
           range_cm1=(1630, 1695), intensity="strong",
           mode="stretch (amide I)",
           note="Amide I (C=O) ~1650 + amide II (N-H bend) ~1550."),
    IRBand(group="N–H bend (amide II)",
           smarts="[NX3H][CX3](=O)",
           range_cm1=(1510, 1580), intensity="medium",
           mode="bend"),
    IRBand(group="C=C alkene",
           smarts="[CX3]=[CX3]",
           range_cm1=(1620, 1680), intensity="variable",
           mode="stretch",
           note="Weak for symmetric alkenes; stronger when conjugated."),
    IRBand(group="Aromatic C=C (two-to-four bands)",
           smarts="c1ccccc1",
           range_cm1=(1450, 1600), intensity="medium",
           mode="ring stretch",
           note="Characteristic 'four-finger' pattern 1450, 1500, 1580, 1600."),
    # ---- 1600-1200: N-O, C-H bends ----
    IRBand(group="N=O (nitro, asym + sym)",
           smarts="[NX3+](=O)[O-]",
           range_cm1=(1300, 1550), intensity="strong",
           mode="stretch (two bands)",
           note="asym ~1520-1550, sym ~1330-1370."),
    # ---- 1300-1000: C-O ----
    IRBand(group="C–O (alcohol/ether/ester)",
           smarts="[CX4][OX2]",
           range_cm1=(1050, 1260), intensity="strong",
           mode="stretch",
           note="Often splits into multiple bands in this region."),
    # ---- 900-700: C-H bend aromatic / alkene ----
    IRBand(group="=C–H out-of-plane (disubstituted alkene)",
           # Generic disubstituted alkene; cis/trans distinguished by
           # bond-direction flags at the SMILES level, not SMARTS.
           smarts="[CX3H]=[CX3H]",
           range_cm1=(660, 980), intensity="strong",
           mode="bend",
           note="Cis ~680–730, trans ~960–980 — one of the few IR methods "
                "to distinguish cis vs trans double bonds."),
    # ---- ~700-500: C-X ----
    IRBand(group="C–Cl stretch",
           smarts="[CX4][Cl]",
           range_cm1=(600, 800), intensity="strong",
           mode="stretch"),
    IRBand(group="C–Br stretch",
           smarts="[CX4][Br]",
           range_cm1=(500, 600), intensity="strong",
           mode="stretch"),
]


def predict_bands(smiles: str) -> Dict[str, Any]:
    """Return every IR band whose detection SMARTS matches the molecule.

    Output:
        {"smiles": ..., "n_atoms": N, "bands": [ {...}, {...}, ... ]}
    where each band dict is :meth:`IRBand.to_dict` augmented with
    ``match_atoms`` (the RDKit atom indices that triggered the match,
    one-shot per band type).
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"error": f"Unparseable SMILES: {smiles!r}"}
    out: List[Dict[str, Any]] = []
    for band in IR_BANDS:
        patt = Chem.MolFromSmarts(band.smarts)
        if patt is None:
            continue
        matches = mol.GetSubstructMatches(patt)
        if not matches:
            continue
        entry = band.to_dict()
        entry["match_atoms"] = list(matches[0])
        entry["n_matches"] = len(matches)
        out.append(entry)
    # Sort by wavenumber high→low so the predicted spectrum reads left-to-right
    out.sort(key=lambda e: -max(e["range_cm1"]))
    return {"smiles": smiles, "n_atoms": mol.GetNumHeavyAtoms(),
            "bands": out}


def describe_prediction(smiles: str) -> str:
    """Return a markdown bulletised IR prediction for the LLM tutor."""
    res = predict_bands(smiles)
    if "error" in res:
        return f"**Error**: {res['error']}"
    if not res["bands"]:
        return f"No characteristic IR bands identified for {smiles!r} — " \
               "molecule has only sp³ skeleton or pattern SMARTS missed."
    lines = [f"### Predicted IR bands — `{smiles}`\n"]
    for b in res["bands"]:
        lo, hi = b["range_cm1"]
        note = f" ({b['note']})" if b["note"] else ""
        lines.append(
            f"- **{b['group']}**: {lo}–{hi} cm⁻¹, {b['intensity']} "
            f"{b['mode']}{note}"
        )
    return "\n".join(lines)
