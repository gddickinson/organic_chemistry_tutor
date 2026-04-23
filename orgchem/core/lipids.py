"""Lipids data module — Phase 29 (lipids sibling).

Teaching-scale catalogue of the main lipid families:

- **Fatty acids** — saturated, mono- and polyunsaturated, with
  ω-designation and melting-point estimates.
- **Triglycerides** — mono/di/tri-acyl glycerols.
- **Glycerophospholipids** — phosphatidylcholine, phosphatidyl-
  ethanolamine, phosphatidic acid.
- **Sphingolipids** — sphingomyelin, ceramide.
- **Sterols** — cholesterol, vitamin D₃, testosterone.

Pure data module, headless. The accompanying GUI tab mirrors the
Phase 29b Carbohydrates panel pattern.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Lipid:
    """One seeded lipid entry."""
    name: str
    family: str                # "fatty-acid" / "triglyceride" / "phospholipid"
                               # / "sphingolipid" / "sterol" / "vitamin"
    smiles: str
    chain_length: Optional[int] = None        # carbons in the acyl chain
    unsaturations: Optional[int] = None       # number of C=C
    omega_designation: str = ""               # "ω-3" / "ω-6" / "ω-9" / ""
    melting_point_c: Optional[float] = None   # °C, approximate literature value
    notes: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name, "family": self.family,
            "smiles": self.smiles,
            "chain_length": self.chain_length,
            "unsaturations": self.unsaturations,
            "omega_designation": self.omega_designation,
            "melting_point_c": self.melting_point_c,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------

LIPIDS: List[Lipid] = [
    # ---- Saturated fatty acids ------------------------------------
    Lipid(name="Lauric acid (C12:0)", family="fatty-acid",
          smiles="CCCCCCCCCCCC(=O)O",
          chain_length=12, unsaturations=0, melting_point_c=44.0,
          notes="Medium-chain saturated fatty acid. Major component of "
                "coconut + palm-kernel oils."),
    Lipid(name="Palmitic acid (C16:0)", family="fatty-acid",
          smiles="CCCCCCCCCCCCCCCC(=O)O",
          chain_length=16, unsaturations=0, melting_point_c=63.1,
          notes="Most abundant saturated fatty acid in plants + animals."),
    Lipid(name="Stearic acid (C18:0)", family="fatty-acid",
          smiles="CCCCCCCCCCCCCCCCCC(=O)O",
          chain_length=18, unsaturations=0, melting_point_c=69.6,
          notes="Long-chain saturated fat. Solid at room temperature."),
    # ---- Monounsaturated ------------------------------------------
    Lipid(name="Oleic acid (C18:1, ω-9)", family="fatty-acid",
          smiles="CCCCCCCC/C=C\\CCCCCCCC(=O)O",
          chain_length=18, unsaturations=1, omega_designation="ω-9",
          melting_point_c=13.4,
          notes="cis-Δ9. Dominant fatty acid in olive oil; liquid at RT."),
    # ---- Polyunsaturated ------------------------------------------
    Lipid(name="Linoleic acid (C18:2, ω-6)", family="fatty-acid",
          smiles="CCCCC/C=C\\C/C=C\\CCCCCCCC(=O)O",
          chain_length=18, unsaturations=2, omega_designation="ω-6",
          melting_point_c=-5.0,
          notes="Essential fatty acid; precursor to arachidonate."),
    Lipid(name="α-Linolenic acid (C18:3, ω-3)", family="fatty-acid",
          smiles="CC/C=C\\C/C=C\\C/C=C\\CCCCCCCC(=O)O",
          chain_length=18, unsaturations=3, omega_designation="ω-3",
          melting_point_c=-11.0,
          notes="Plant-derived essential ω-3; flax and chia."),
    Lipid(name="Arachidonic acid (C20:4, ω-6)", family="fatty-acid",
          smiles="CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O",
          chain_length=20, unsaturations=4, omega_designation="ω-6",
          melting_point_c=-49.5,
          notes="Precursor to prostaglandins + leukotrienes — "
                "COX/LOX substrates."),
    Lipid(name="EPA (C20:5, ω-3)", family="fatty-acid",
          smiles="CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O",
          chain_length=20, unsaturations=5, omega_designation="ω-3",
          melting_point_c=-54.0,
          notes="Eicosapentaenoic acid. Fish-oil; cardioprotective."),
    Lipid(name="DHA (C22:6, ω-3)", family="fatty-acid",
          smiles="CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCC(=O)O",
          chain_length=22, unsaturations=6, omega_designation="ω-3",
          melting_point_c=-44.0,
          notes="Docosahexaenoic acid. Dominant fatty acid in neural + "
                "retinal phospholipids."),
    # ---- Triglycerides --------------------------------------------
    Lipid(name="Tripalmitin", family="triglyceride",
          smiles="CCCCCCCCCCCCCCCC(=O)OCC(OC(=O)CCCCCCCCCCCCCCC)"
                 "COC(=O)CCCCCCCCCCCCCCC",
          notes="Fully saturated triacylglycerol of palmitic acid."),
    Lipid(name="Triolein", family="triglyceride",
          smiles="CCCCCCCC/C=C\\CCCCCCCC(=O)OCC(OC(=O)CCCCCCC/C=C\\"
                 "CCCCCCCC)COC(=O)CCCCCCC/C=C\\CCCCCCCC",
          notes="Tri-oleoyl glycerol. Principal triacylglycerol in "
                "olive oil."),
    # ---- Phospholipids --------------------------------------------
    Lipid(name="Phosphatidylcholine (POPC-like)",
          family="phospholipid",
          smiles="CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)([O-])OCC"
                 "[N+](C)(C)C)OC(=O)CCCCCCC/C=C\\CCCCCCCC",
          notes="Palmitoyl-oleoyl-PC. Predominant mammalian membrane "
                "phospholipid."),
    Lipid(name="Phosphatidylethanolamine (POPE-like)",
          family="phospholipid",
          smiles="CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)(O)OCCN)"
                 "OC(=O)CCCCCCC/C=C\\CCCCCCCC",
          notes="Cone-shaped lipid — promotes negative curvature."),
    Lipid(name="Phosphatidic acid",
          family="phospholipid",
          smiles="CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(=O)(O)O)"
                 "OC(=O)CCCCCCCCCCCCCCC",
          notes="Central biosynthetic precursor to all "
                "glycerophospholipids."),
    # ---- Sphingolipids --------------------------------------------
    Lipid(name="Ceramide (C18)", family="sphingolipid",
          smiles="CCCCCCCCCCCCCCCCCC(=O)N[C@@H](CO)[C@@H](O)"
                 "/C=C/CCCCCCCCCCCCC",
          notes="Base sphingolipid — sphingosine + fatty-acid amide."),
    Lipid(name="Sphingomyelin (C18)", family="sphingolipid",
          smiles="CCCCCCCCCCCCCCCCCC(=O)N[C@@H](COP(=O)([O-])"
                 "OCC[N+](C)(C)C)[C@@H](O)/C=C/CCCCCCCCCCCCC",
          notes="Myelin-sheath lipid. Phosphocholine head-group on a "
                "ceramide backbone."),
    # ---- Sterols / steroids ---------------------------------------
    Lipid(name="Cholesterol", family="sterol",
          smiles="CC(C)CCC[C@@H](C)[C@H]1CC[C@@H]2[C@@]1(C)CC[C@H]3"
                 "[C@H]2CC=C4[C@@]3(C)CC[C@@H](O)C4",
          notes="Major membrane sterol in animal cells; precursor "
                "to steroid hormones + bile acids."),
    Lipid(name="Ergosterol", family="sterol",
          smiles="CC(C)C(C)[C@H]1CC[C@H]2C3=CC=C4CC(O)CC[C@]4(C)"
                 "C3CC[C@]12C",
          notes="Fungal sterol; target of azole antifungals."),
    Lipid(name="Vitamin D3 (cholecalciferol)", family="vitamin",
          smiles="CC(C)CCC[C@@H](C)[C@H]1CC[C@@H]2/C(=C\\C=C3\\C[C@@H]"
                 "(O)CCC3=C)/CCC[C@]12C",
          notes="Secosteroid; photochemical isomerisation product of "
                "7-dehydrocholesterol in skin."),
    Lipid(name="Testosterone", family="sterol",
          smiles="C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@@]34C)"
                 "[C@@H]1CC[C@@H]2O",
          notes="Androgen — primary male sex hormone. Steroid scaffold."),
    Lipid(name="Estradiol", family="sterol",
          smiles="C[C@]12CCC3c4ccc(O)cc4CC[C@H]3[C@@H]1CC[C@@H]2O",
          notes="Estrogen. Aromatic A-ring is its structural signature."),

    # ---- Phase 31i content expansion (2026-04-23) ----------------
    # Medium-chain saturated fatty acids (MCT oil components)
    Lipid(name="Caprylic acid (C8:0)", family="fatty-acid",
          smiles="CCCCCCCC(=O)O",
          chain_length=8, unsaturations=0, melting_point_c=16.5,
          notes="Medium-chain fatty acid — liquid at room temperature. "
                "MCT oil component; rapidly oxidised in liver for "
                "ketogenic energy supply."),
    Lipid(name="Capric acid (C10:0)", family="fatty-acid",
          smiles="CCCCCCCCCC(=O)O",
          chain_length=10, unsaturations=0, melting_point_c=31.6,
          notes="Medium-chain fatty acid. Coconut / palm-kernel oils; "
                "goat-milk caprylate triglyceride backbone."),
    # Eicosanoids (signalling)
    Lipid(name="Prostaglandin E2 (PGE2)", family="fatty-acid",
          smiles="CCCCC[C@H](O)/C=C/[C@H]1[C@H](O)CC(=O)[C@@H]1"
                 "C/C=C\\CCCC(=O)O",
          chain_length=20, unsaturations=2,
          notes="Arachidonic-acid-derived eicosanoid. Cyclopentane ring "
                "+ α / ω side chains. COX-2 target; mediates fever, "
                "pain, inflammation, parturition."),
    Lipid(name="Thromboxane A2 (TXA2)", family="fatty-acid",
          smiles="CCCCC[C@H](O)/C=C/[C@H]1O[C@@H]2C[C@H]1"
                 "[C@@H](C/C=C\\CCCC(=O)O)O2",
          chain_length=20, unsaturations=2,
          notes="Oxetane-bearing eicosanoid — platelet aggregator "
                "and vasoconstrictor. Target of low-dose aspirin (COX-1 "
                "acetylation in platelets)."),
    # Bile acids
    Lipid(name="Cholic acid", family="sterol",
          smiles="C[C@H](CCC(=O)O)[C@H]1CC[C@@H]2[C@@]1(C)"
                 "[C@@H](O)C[C@H]1[C@H]2[C@@H](O)C[C@@H]2C[C@H](O)"
                 "CC[C@]12C",
          notes="Primary bile acid — synthesised in liver from "
                "cholesterol. Emulsifies dietary fat. 3α, 7α, 12α-"
                "trihydroxy-5β-cholan-24-oic acid."),
    Lipid(name="Taurocholic acid", family="sterol",
          smiles="C[C@H](CCC(=O)NCCS(=O)(=O)O)[C@H]1CC[C@@H]2"
                 "[C@@]1(C)[C@@H](O)C[C@H]1[C@H]2[C@@H](O)C"
                 "[C@@H]2C[C@H](O)CC[C@]12C",
          notes="Taurine-conjugated bile salt. Deprotonated at "
                "intestinal pH — potent detergent for micelle "
                "formation with dietary fats."),
    # Steroid hormones
    Lipid(name="Progesterone", family="sterol",
          smiles="C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@@]34C)"
                 "[C@@H]1CC[C@@H]2C(=O)C",
          notes="C21 steroid hormone. Uterine lining maintenance; "
                "pregnancy. Precursor to cortisol + aldosterone."),
    Lipid(name="Cortisol", family="sterol",
          smiles="OC[C@@]12[C@@](O)([C@@H](O)C[C@@H]1[C@@H]1CC"
                 "[C@H]3CC(=O)CC[C@]3(C)[C@H]1C[C@@H]2O)C(=O)CO",
          notes="Glucocorticoid — stress hormone. Anti-inflammatory "
                "and gluconeogenic. Clinical analogue: prednisolone "
                "(Δ¹-dehydrocortisol)."),
    # Fat-soluble vitamins
    Lipid(name="Retinol (vitamin A)", family="vitamin",
          smiles="CC1=C(/C=C/C(C)=C/C=C/C(C)=C/CO)C(C)(C)CCC1",
          chain_length=20, unsaturations=5,
          notes="All-trans retinol — precursor to retinal (vision) "
                "and retinoic acid (transcriptional regulator, "
                "RAR/RXR)."),
    Lipid(name="α-Tocopherol (vitamin E)", family="vitamin",
          smiles="Cc1c(C)c2c(c(C)c1O)CC[C@@](C)(CCC[C@H](C)CCC"
                 "[C@H](C)CCCC(C)C)O2",
          notes="Main circulating form of vitamin E. Chain-breaking "
                "antioxidant in cell membranes — phenolic H-atom "
                "donor to lipid peroxyl radicals."),
]


# ---------------------------------------------------------------------
# Lookup helpers

def list_lipids(family: str = "") -> List[Dict[str, object]]:
    """Summary-dict list, optionally filtered by family."""
    fam = family.strip().lower()
    return [l.to_dict() for l in LIPIDS
            if not fam or l.family == fam]


def get_lipid(name: str) -> Optional[Lipid]:
    """Exact-or-case-insensitive name lookup."""
    name = name.strip()
    for l in LIPIDS:
        if l.name.lower() == name.lower():
            return l
    return None


def lipid_families() -> List[str]:
    seen: List[str] = []
    for l in LIPIDS:
        if l.family not in seen:
            seen.append(l.family)
    return seen
