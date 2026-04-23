"""Carbohydrates data module — Phase 29a.

Teaching-scale catalogue of sugars across the main families:
monosaccharides (aldoses / ketoses, pyranose / furanose / open-chain),
disaccharides (glycosidic-bond + anomeric configuration), and
polysaccharide fragments (amylose, cellulose).

The accompanying GUI tab (round 42) will render each entry in both
Haworth and chair projections, plus the usual 2D / 3D views via the
existing `draw2d` / 3Dmol pipelines. This module is pure data + small
helpers, kept headless so tests and agent actions can pull from it
without importing Qt.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Carbohydrate:
    """One seeded carbohydrate entry."""
    name: str
    family: str             # "monosaccharide" / "disaccharide" / "polysaccharide"
    form: str               # "pyranose" / "furanose" / "open-chain"
    carbonyl_type: str      # "aldose" / "ketose" / "" (for di/polysaccharides)
    smiles: str
    anomer: str = ""        # "α" / "β" / ""
    glycosidic: str = ""    # e.g. "α-1,4" for glycosidic-linkage teaching
    notes: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name, "family": self.family,
            "form": self.form, "carbonyl_type": self.carbonyl_type,
            "smiles": self.smiles, "anomer": self.anomer,
            "glycosidic": self.glycosidic, "notes": self.notes,
        }


# ---------------------------------------------------------------------

CARBOHYDRATES: List[Carbohydrate] = [
    # ---- D-Glucose ------------------------------------------------
    Carbohydrate(
        name="D-Glucose (open chain)",
        family="monosaccharide", form="open-chain",
        carbonyl_type="aldose",
        smiles="OC[C@@H](O)[C@@H](O)[C@H](O)[C@H](O)C=O",
        notes="The acyclic Fischer-projection form. Shifts into "
              "α/β pyranose forms in aqueous solution.",
    ),
    Carbohydrate(
        name="α-D-Glucopyranose",
        family="monosaccharide", form="pyranose",
        carbonyl_type="aldose", anomer="α",
        smiles="OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Ring form with axial-OH at C1. ~36 % at equilibrium "
              "in water; the remaining ~64 % is the β anomer.",
    ),
    Carbohydrate(
        name="β-D-Glucopyranose",
        family="monosaccharide", form="pyranose",
        carbonyl_type="aldose", anomer="β",
        smiles="OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Ring form with equatorial-OH at C1. Favoured anomer.",
    ),
    # ---- D-Fructose ----------------------------------------------
    Carbohydrate(
        name="D-Fructose (open chain)",
        family="monosaccharide", form="open-chain",
        carbonyl_type="ketose",
        smiles="OC[C@@H](O)[C@@H](O)[C@H](O)C(=O)CO",
        notes="Ketohexose — the only abundant monosaccharide ketose.",
    ),
    Carbohydrate(
        name="β-D-Fructofuranose",
        family="monosaccharide", form="furanose",
        carbonyl_type="ketose", anomer="β",
        smiles="OC[C@H]1O[C@](O)(CO)[C@@H](O)[C@@H]1O",
        notes="Favoured ring form; what sucrose incorporates.",
    ),
    # ---- Pentoses -------------------------------------------------
    Carbohydrate(
        name="D-Ribose (furanose)",
        family="monosaccharide", form="furanose",
        carbonyl_type="aldose",
        smiles="OC[C@H]1O[C@H](O)[C@H](O)[C@@H]1O",
        notes="Found in RNA; 2'-OH distinguishes it from deoxyribose.",
    ),
    Carbohydrate(
        name="2-Deoxy-D-ribose (furanose)",
        family="monosaccharide", form="furanose",
        carbonyl_type="aldose",
        smiles="OC[C@H]1O[C@H](O)C[C@@H]1O",
        notes="The sugar in DNA — missing the 2'-OH.",
    ),
    # ---- Galactose + mannose --------------------------------------
    Carbohydrate(
        name="α-D-Galactopyranose",
        family="monosaccharide", form="pyranose",
        carbonyl_type="aldose", anomer="α",
        smiles="OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@H]1O",
        notes="C-4 epimer of glucose.",
    ),
    Carbohydrate(
        name="α-D-Mannopyranose",
        family="monosaccharide", form="pyranose",
        carbonyl_type="aldose", anomer="α",
        smiles="OC[C@H]1O[C@H](O)[C@@H](O)[C@@H](O)[C@@H]1O",
        notes="C-2 epimer of glucose.",
    ),
    # ---- Disaccharides --------------------------------------------
    Carbohydrate(
        name="Sucrose",
        family="disaccharide", form="pyranose+furanose",
        carbonyl_type="",
        glycosidic="α-1,2",
        smiles="OC[C@H]1O[C@@H](O[C@]2(CO)O[C@H](CO)[C@@H](O)"
               "[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Glucose(α1)–Fructose(β2) disaccharide. Non-reducing "
              "because both anomeric carbons are tied up.",
    ),
    Carbohydrate(
        name="Lactose",
        family="disaccharide", form="pyranose+pyranose",
        carbonyl_type="aldose",
        glycosidic="β-1,4",
        smiles="OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)"
               "[C@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Galactose(β1→4)Glucose. Milk sugar. Hydrolysed by "
              "lactase; absence causes lactose intolerance.",
    ),
    Carbohydrate(
        name="Maltose",
        family="disaccharide", form="pyranose+pyranose",
        carbonyl_type="aldose",
        glycosidic="α-1,4",
        smiles="OC[C@H]1O[C@H](O[C@H]2[C@H](O)[C@@H](O)[C@@H](O)"
               "O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Glucose(α1→4)Glucose. From amylose hydrolysis.",
    ),
    Carbohydrate(
        name="Cellobiose",
        family="disaccharide", form="pyranose+pyranose",
        carbonyl_type="aldose",
        glycosidic="β-1,4",
        smiles="OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)"
               "[C@@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Glucose(β1→4)Glucose. Repeat unit of cellulose.",
    ),
    # ---- Polysaccharide fragments ---------------------------------
    Carbohydrate(
        name="Amylose fragment (3 glucose, α-1,4)",
        family="polysaccharide", form="pyranose chain",
        carbonyl_type="aldose",
        glycosidic="α-1,4",
        smiles="OC[C@H]1O[C@H](O[C@H]2[C@H](O)[C@@H](O)"
               "O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Linear α-1,4 chain — the soluble starch fraction. "
              "Forms a helical structure around I₂ (starch-iodine "
              "test).",
    ),
    Carbohydrate(
        name="Cellulose fragment (3 glucose, β-1,4)",
        family="polysaccharide", form="pyranose chain",
        carbonyl_type="aldose",
        glycosidic="β-1,4",
        smiles="OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)"
               "O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="β-1,4 glycosidic bonds force linear ribbons that "
              "hydrogen-bond into insoluble fibres — plant cell walls.",
    ),
]


# ---------------------------------------------------------------------
# Lookup helpers

def list_carbohydrates(family: str = "") -> List[Dict[str, object]]:
    """Summary-dict list, optionally filtered by family."""
    fam = family.strip().lower()
    return [c.to_dict() for c in CARBOHYDRATES
            if not fam or c.family == fam]


def get_carbohydrate(name: str) -> Optional[Carbohydrate]:
    """Exact-or-case-insensitive name lookup."""
    name = name.strip()
    for c in CARBOHYDRATES:
        if c.name.lower() == name.lower():
            return c
    return None


def families() -> List[str]:
    seen: List[str] = []
    for c in CARBOHYDRATES:
        if c.family not in seen:
            seen.append(c.family)
    return seen
