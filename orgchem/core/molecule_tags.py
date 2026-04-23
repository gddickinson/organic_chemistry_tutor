"""Auto-tagger for molecule-browser multi-category filters — Phase 28c.

Given an RDKit ``Mol`` (or a SMILES), return a tag dictionary that
the GUI filter bar can AND together:

- ``functional_groups`` — SMARTS-matched groups like
  ``"carboxylic_acid"``, ``"alcohol"``, ``"amine"`` …
- ``composition_flags`` — coarse element-presence flags
  (``"contains_halogen"``, ``"contains_phosphorus"``, …).
- ``charge_category`` — ``"neutral"`` / ``"cation"`` / ``"anion"``
  / ``"zwitterion"``.
- ``size_band`` — ``"small"`` (≤ 12 heavy atoms) / ``"medium"``
  (13-30) / ``"large"`` (≥ 31).
- ``ring_band`` — ``"acyclic"`` / ``"one_to_two"`` /
  ``"three_plus"``.

Everything is hand-curated and SMARTS-based so the result is
deterministic and testable. No external deps beyond RDKit.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from rdkit import Chem

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Functional-group SMARTS library.
# Order matters a little — more-specific groups should come before
# their generalisations (e.g. carboxylic acid before alcohol).
FUNCTIONAL_GROUPS: List[tuple] = [
    ("carboxylic_acid",   "[CX3](=O)[OX2H1]"),
    ("ester",             "[CX3](=O)[OX2][#6]"),
    ("amide",             "[CX3](=O)[NX3]"),
    ("acyl_halide",       "[CX3](=O)[F,Cl,Br,I]"),
    ("anhydride",         "[CX3](=O)[OX2][CX3](=O)"),
    ("nitrile",           "[C]#[N]"),
    ("aldehyde",          "[CX3H1](=O)[#6]"),
    ("ketone",            "[#6][CX3](=O)[#6]"),
    ("ether",             "[OD2]([#6])[#6]"),
    ("alcohol",           "[OX2H][CX4;!$(C=[O,N,S])]"),
    ("phenol",            "[OX2H][c]"),
    ("primary_amine",     "[NX3;H2;!$(NC=O)]"),
    ("secondary_amine",   "[NX3;H1;!$(NC=O)]"),
    ("tertiary_amine",    "[NX3;H0;!$(NC=O);!$(N=*)]"),
    ("aromatic",          "c1ccccc1"),
    ("heterocycle_N",     "[n]"),
    ("heterocycle_O",     "[o]"),
    ("heterocycle_S",     "[s]"),
    ("sulfonate",         "[SX4](=O)(=O)[OX2H,OX1-]"),
    ("sulfonamide",       "[SX4](=O)(=O)[NX3]"),
    ("thioether",         "[SX2]([#6])[#6]"),
    ("thiol",             "[SX2H]"),
    ("phosphate",         "[P](=O)([OH])([OH])[OX2]"),
    ("nitro",             "[NX3+](=O)[O-]"),
    ("alkene",            "[CX3]=[CX3]"),
    ("alkyne",            "[CX2]#[CX2]"),
    ("halide",            "[F,Cl,Br,I]"),
]


#: Flat map from element symbol → composition flag.
_ELEMENT_FLAGS = {
    "F": "contains_halogen", "Cl": "contains_halogen",
    "Br": "contains_halogen", "I": "contains_halogen",
    "P": "contains_phosphorus",
    "S": "contains_sulfur",
    "B": "contains_boron",
    "Si": "contains_silicon",
}

#: "Organic only" element set for the "pure organic" composition flag.
_ORGANIC_ELEMENTS = {"C", "H", "N", "O", "S", "P",
                     "F", "Cl", "Br", "I"}


# ---------------------------------------------------------------------

@dataclass
class TagResult:
    functional_groups: List[str] = field(default_factory=list)
    composition_flags: List[str] = field(default_factory=list)
    charge_category: str = "neutral"
    size_band: str = "small"
    ring_band: str = "acyclic"
    heavy_atom_count: int = 0
    formal_charge: int = 0
    n_rings: int = 0
    has_stereo: bool = False

    def to_dict(self) -> Dict[str, object]:
        return {
            "functional_groups": list(self.functional_groups),
            "composition_flags": list(self.composition_flags),
            "charge_category": self.charge_category,
            "size_band": self.size_band,
            "ring_band": self.ring_band,
            "heavy_atom_count": self.heavy_atom_count,
            "formal_charge": self.formal_charge,
            "n_rings": self.n_rings,
            "has_stereo": self.has_stereo,
        }


# ---------------------------------------------------------------------

def auto_tag(mol_or_smiles: Union[Chem.Mol, str]) -> TagResult:
    """Return a :class:`TagResult` with all derived tags populated."""
    if isinstance(mol_or_smiles, str):
        mol = Chem.MolFromSmiles(mol_or_smiles)
    else:
        mol = mol_or_smiles
    if mol is None:
        return TagResult()

    # ----- Functional groups ----------------------------------------
    groups: List[str] = []
    for name, smarts in FUNCTIONAL_GROUPS:
        patt = Chem.MolFromSmarts(smarts)
        if patt is None:
            continue
        if mol.HasSubstructMatch(patt):
            groups.append(name)

    # ----- Composition flags ----------------------------------------
    elements = {atom.GetSymbol() for atom in mol.GetAtoms()}
    flags: List[str] = []
    for el, flag in _ELEMENT_FLAGS.items():
        if el in elements and flag not in flags:
            flags.append(flag)
    # Pure-organic check (C/H/N/O/S/P/halogens only).
    if elements and all(el in _ORGANIC_ELEMENTS for el in elements):
        flags.append("pure_organic")
    has_metal = any(
        atom.GetAtomicNum() > 0
        and Chem.GetPeriodicTable().GetElementSymbol(atom.GetAtomicNum())
        not in _ORGANIC_ELEMENTS
        and atom.GetSymbol() not in ("B", "Si")  # metalloids handled above
        for atom in mol.GetAtoms()
    )
    if has_metal:
        flags.append("has_metal")

    # ----- Charge category ------------------------------------------
    total_charge = Chem.GetFormalCharge(mol)
    pos = any(a.GetFormalCharge() > 0 for a in mol.GetAtoms())
    neg = any(a.GetFormalCharge() < 0 for a in mol.GetAtoms())
    if pos and neg and total_charge == 0:
        charge_cat = "zwitterion"
    elif total_charge > 0:
        charge_cat = "cation"
    elif total_charge < 0:
        charge_cat = "anion"
    else:
        charge_cat = "neutral"

    # ----- Size + rings ---------------------------------------------
    heavy = mol.GetNumHeavyAtoms()
    if heavy <= 12:
        size = "small"
    elif heavy <= 30:
        size = "medium"
    else:
        size = "large"

    n_rings = mol.GetRingInfo().NumRings()
    if n_rings == 0:
        ring_band = "acyclic"
    elif n_rings <= 2:
        ring_band = "one_to_two"
    else:
        ring_band = "three_plus"

    # ----- Stereo ---------------------------------------------------
    has_stereo = any(
        atom.GetChiralTag() != Chem.ChiralType.CHI_UNSPECIFIED
        for atom in mol.GetAtoms()
    ) or any(
        bond.GetStereo() not in (Chem.BondStereo.STEREONONE,)
        for bond in mol.GetBonds()
    )

    return TagResult(
        functional_groups=groups,
        composition_flags=flags,
        charge_category=charge_cat,
        size_band=size,
        ring_band=ring_band,
        heavy_atom_count=heavy,
        formal_charge=total_charge,
        n_rings=n_rings,
        has_stereo=has_stereo,
    )


# ---------------------------------------------------------------------
# Enumerated category taxonomies — surfaced by the GUI filter bar.

FILTER_AXES: Dict[str, List[str]] = {
    "functional_group": [name for name, _ in FUNCTIONAL_GROUPS],
    "composition": [
        "contains_halogen", "contains_phosphorus", "contains_sulfur",
        "contains_boron", "contains_silicon", "pure_organic",
        "has_metal",
    ],
    "source": [
        # Broad bucket labels from the seed files.
        "amino-acid", "reagent", "drug", "biomolecule",
        "dye", "pah", "heterocycle", "intermediate",
        # User-facing fine-grained tags (curated in
        # orgchem/db/seed_source_tags.py).
        "NSAID", "statin", "antibiotic", "beta-lactam",
        "antiviral", "SSRI", "antidepressant", "beta-blocker",
        "ACE-inhibitor", "angiotensin-receptor-blocker",
        "antidiabetic", "anticoagulant", "proton-pump-inhibitor",
        "PDE5-inhibitor", "opioid", "antihistamine",
        "local-anaesthetic", "anticholinergic", "antimalarial",
        "alkaloid", "natural-product",
        "neurotransmitter", "catecholamine",
        "hormone", "steroid", "androgen", "estrogen",
        "nucleoside",
        "sugar", "pentose", "hexose", "disaccharide",
        "fatty-acid", "saturated", "monounsaturated",
        "polyunsaturated", "omega-3", "omega-6", "omega-9",
        "peptide", "antioxidant",
        "pigment", "vat-dye", "indicator", "stain", "fluorophore",
        "hindered-base", "hydride-reductant", "protecting-group",
        "oxidant", "peroxyacid", "activating-group", "base",
        "acylating-agent", "halogenating-agent",
        "HMG-CoA-reductase-inhibitor",
        "prostaglandin-synthesis-inhibitor",
        "analgesic",
    ],
    "charge": ["neutral", "cation", "anion", "zwitterion"],
    "size": ["small", "medium", "large"],
    "ring_count": ["acyclic", "one_to_two", "three_plus"],
    "has_stereo": ["yes", "no"],
}


def list_filter_axes() -> Dict[str, List[str]]:
    """Enumerate the category axes + possible values for the GUI."""
    return {k: list(v) for k, v in FILTER_AXES.items()}
