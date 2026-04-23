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

    # ---- Phase 31h content expansion (2026-04-23) ----------------
    # Aminosugars
    Carbohydrate(
        name="D-Glucosamine", family="monosaccharide",
        form="pyranose", carbonyl_type="aldose", anomer="β",
        smiles="N[C@H]1[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O",
        notes="2-amino-2-deoxy-D-glucose. Precursor to GlcNAc; building "
              "block of chitin and glycosaminoglycans. Dietary "
              "supplement in OA.",
    ),
    Carbohydrate(
        name="N-Acetylglucosamine (GlcNAc)", family="monosaccharide",
        form="pyranose", carbonyl_type="aldose", anomer="β",
        smiles="CC(=O)N[C@H]1[C@@H](O)O[C@H](CO)[C@@H](O)[C@@H]1O",
        notes="Core monomer of chitin, peptidoglycan, and hyaluronic "
              "acid. Lysozyme hydrolyses β-1,4 GlcNAc–MurNAc bonds.",
    ),
    # Uronic acids
    Carbohydrate(
        name="D-Glucuronic acid", family="monosaccharide",
        form="pyranose", carbonyl_type="aldose", anomer="β",
        smiles="O=C(O)[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Liver phase-II drug conjugation (glucuronidation) "
              "solubilises xenobiotics for excretion. Component of "
              "hyaluronic acid, heparin, proteoglycans.",
    ),
    # Deoxy sugars beyond 2-deoxyribose
    Carbohydrate(
        name="L-Fucose (6-deoxy-L-galactose)",
        family="monosaccharide",
        form="pyranose", carbonyl_type="aldose", anomer="α",
        smiles="C[C@@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Terminal sugar on many N-glycans and blood-group "
              "antigens (H antigen). Fucosylation is a major "
              "cancer-biomarker axis.",
    ),
    Carbohydrate(
        name="L-Rhamnose (6-deoxy-L-mannose)",
        family="monosaccharide",
        form="pyranose", carbonyl_type="aldose", anomer="α",
        smiles="C[C@@H]1O[C@H](O)[C@@H](O)[C@H](O)[C@H]1O",
        notes="Common plant sugar; part of pectin side-chains, "
              "flavonoid and saponin glycosides. Also caps the "
              "O-antigen of many Gram-negative bacteria.",
    ),
    # Sugar alcohols
    Carbohydrate(
        name="D-Sorbitol", family="monosaccharide",
        form="open-chain", carbonyl_type="",
        smiles="OC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO",
        notes="Reduced form of glucose (aldehyde → 1° alcohol). "
              "Non-cariogenic sweetener; also an osmolyte — "
              "accumulation drives diabetic cataract formation.",
    ),
    Carbohydrate(
        name="D-Mannitol", family="monosaccharide",
        form="open-chain", carbonyl_type="",
        smiles="OC[C@@H](O)[C@@H](O)[C@H](O)[C@H](O)CO",
        notes="Reduced form of mannose. Clinical osmotic diuretic; "
              "used to reduce intracranial pressure. Differs from "
              "sorbitol only at C2.",
    ),
    Carbohydrate(
        name="Xylitol", family="monosaccharide",
        form="open-chain", carbonyl_type="",
        smiles="OC[C@@H](O)C(O)[C@H](O)CO",
        notes="5-carbon sugar alcohol. Anticariogenic sweetener "
              "(oral bacteria can't metabolise it). Same sweetness "
              "as sucrose with ⅔ the calories.",
    ),
    # Rare aldoses
    Carbohydrate(
        name="D-Tagatose", family="monosaccharide",
        form="pyranose", carbonyl_type="ketose", anomer="α",
        smiles="OC[C@H]1O[C@](O)(CO)[C@H](O)[C@@H]1O",
        notes="C4 epimer of fructose — a rare hexulose. "
              "Low-glycaemic sweetener; isomerised from lactose-"
              "derived galactose industrially.",
    ),
    # Disaccharide biology extras
    Carbohydrate(
        name="Trehalose (α,α-1,1 glucose dimer)",
        family="disaccharide", form="pyranose–pyranose",
        carbonyl_type="non-reducing",
        glycosidic="α,α-1,1",
        smiles="OC[C@H]1O[C@H](O[C@@H]2O[C@H](CO)[C@@H](O)"
               "[C@H](O)[C@H]2O)[C@H](O)[C@@H](O)[C@@H]1O",
        notes="Non-reducing sugar in insects, fungi, yeasts. "
              "Protects proteins / membranes against desiccation "
              "(anhydrobiosis). Both anomeric carbons are locked.",
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
