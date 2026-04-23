"""Bioisostere toolkit — Phase 19c.

A **bioisostere** is a functional group that replaces another and
preserves the biological activity (usually at a receptor / enzyme),
even though the two groups are not otherwise equivalent. Classical
examples:

- **COOH ↔ tetrazole**: acidity matches, lipophilicity improves.
- **CH₃ ↔ CF₃**: shape similar, metabolic stability rises.
- **C(=O)NH ↔ S(=O)₂NH**: amide → sulfonamide, H-bond acceptor
  survives, proteolysis resistance rises.
- **Phenyl ↔ thiophene**: aromatic ring preserved, metabolic /
  electronic profile shifts.
- **CH₂ ↔ O**: a CH₂ linker → ether linker; similar conformation,
  different polarity.

This module ships a **curated catalogue** of 8 classical pairs (16
directional templates since each pair is reversible) plus a
SMARTS-reaction engine that applies every matching template to a
target SMILES and returns the unique variant set.

Teaching-grade: in real med-chem the "bio" in "bioisostere" requires
retesting each variant's activity. The catalogue here illustrates
the structural moves, not guarantees of biological equivalence.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List

from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem


@dataclass(frozen=True)
class Bioisostere:
    id: str
    label: str
    description: str
    #: SMARTS reaction in `source >> replacement` direction. Each template
    #: is written so that RDKit's `RunReactants` produces a single,
    #: unambiguous product.
    smarts: str


# Apply each template in both directions — i.e., COOH→tetrazole *and*
# tetrazole→COOH — so the engine surfaces the classical substitution
# regardless of which side of the pair the input is.
BIOISOSTERES: List[Bioisostere] = [
    # --- Carboxylic acid <-> tetrazole (classical acid equivalents) ---
    Bioisostere(
        id="cooh-to-tetrazole",
        label="-COOH → 1H-tetrazole",
        description=(
            "Classical acid replacement. Tetrazole pKa (~4.8) matches "
            "carboxylic acid (~4.5); planar π-system similar. Slower "
            "metabolism, often higher lipophilicity — widely used in "
            "AT1 antagonists (losartan family)."
        ),
        smarts="[#6:1]C(=O)[OH]>>[#6:1]c1nnn[nH]1",
    ),
    Bioisostere(
        id="tetrazole-to-cooh",
        label="1H-tetrazole → -COOH",
        description="Reverse of cooh-to-tetrazole.",
        smarts="[#6:1]c1[nH]nnn1>>[#6:1]C(=O)O",
    ),

    # --- Methyl <-> trifluoromethyl ---
    Bioisostere(
        id="me-to-cf3",
        label="-CH₃ → -CF₃",
        description=(
            "Volume-matched non-classical bioisostere. CF₃ is "
            "metabolically inert (no CYP oxidation), more "
            "electron-withdrawing, slightly larger (volume ~45 Å³ vs "
            "24 Å³). Canonical in drug-optimisation campaigns."
        ),
        smarts="[#6:1][CH3]>>[#6:1]C(F)(F)F",
    ),
    Bioisostere(
        id="cf3-to-me",
        label="-CF₃ → -CH₃",
        description="Reverse of me-to-cf3.",
        smarts="[#6:1]C(F)(F)F>>[#6:1][CH3]",
    ),

    # --- Primary amide <-> sulfonamide ---
    Bioisostere(
        id="amide-to-sulfonamide",
        label="-C(=O)NH₂ → -S(=O)₂NH₂",
        description=(
            "Amide → sulfonamide: preserves H-bond donor + acceptor "
            "pattern but adds tetrahedral geometry at S and increases "
            "acidity. Common in CA / PDE inhibitor optimisation."
        ),
        smarts="[#6:1]C(=O)N>>[#6:1]S(=O)(=O)N",
    ),
    Bioisostere(
        id="sulfonamide-to-amide",
        label="-S(=O)₂NH₂ → -C(=O)NH₂",
        description="Reverse of amide-to-sulfonamide.",
        smarts="[#6:1]S(=O)(=O)N>>[#6:1]C(=O)N",
    ),

    # --- Phenyl <-> thiophene (classical aromatic-ring isosteres) ---
    Bioisostere(
        id="phenyl-to-thiophene",
        label="Phenyl → 2-thienyl",
        description=(
            "Canonical aromatic-ring swap. Preserves the π-system but "
            "shrinks the ring by one atom (6 → 5) while keeping "
            "aromaticity intact; widely used to modulate metabolic "
            "stability (thiophene is often slower-metabolised than phenyl "
            "but can generate reactive metabolites — pharm team choice)."
        ),
        smarts="[#6:1]c1ccccc1>>[#6:1]c1ccsc1",
    ),

    # --- Ether <-> CH2 spacer ---
    Bioisostere(
        id="o-to-ch2",
        label="-O- → -CH₂- (ether → methylene spacer)",
        description=(
            "Swap an ether oxygen for a CH₂ linker. Same conformation "
            "family, loses H-bond acceptor + polarity; raises logP. "
            "Classical in CNS-penetration optimisation where H-bond "
            "acceptor count is being trimmed to pass BBB."
        ),
        smarts="[#6:1][OX2][#6:2]>>[#6:1][CH2][#6:2]",
    ),
    Bioisostere(
        id="ch2-to-o",
        label="-CH₂- → -O- (methylene → ether)",
        description="Reverse of o-to-ch2.",
        smarts="[#6:1][CH2][#6:2]>>[#6:1][OX2][#6:2]",
    ),

    # --- Halogen ladder ---
    Bioisostere(
        id="cl-to-f",
        label="Aryl -Cl → -F",
        description=(
            "Cl / F on aromatic rings are classical bioisosteres. F is "
            "smaller, more electronegative, and doesn't leave as a "
            "metabolite. Shifts lipophilicity down (~logP −0.3)."
        ),
        smarts="[c:1][Cl]>>[c:1]F",
    ),
    Bioisostere(
        id="f-to-cl",
        label="Aryl -F → -Cl",
        description="Reverse of cl-to-f.",
        smarts="[c:1][F]>>[c:1]Cl",
    ),

    # --- Hydroxyl <-> NH ---
    Bioisostere(
        id="ar-oh-to-ar-nh2",
        label="Aryl -OH → -NH₂",
        description=(
            "Phenol → aniline. Preserves H-bond donor + π-donation to "
            "the ring. pKa shifts up (10→4-5), metabolism shifts from "
            "glucuronidation to N-acetylation."
        ),
        smarts="[c:1][OH]>>[c:1]N",
    ),
    Bioisostere(
        id="ar-nh2-to-ar-oh",
        label="Aryl -NH₂ → -OH",
        description="Reverse of ar-oh-to-ar-nh2.",
        smarts="[c:1][NH2]>>[c:1]O",
    ),

    # --- Ester <-> amide (serine-ester → amide stability) ---
    Bioisostere(
        id="ester-to-amide",
        label="-C(=O)O- → -C(=O)NH-",
        description=(
            "Ester → amide: preserves H-bond acceptor + approximate "
            "geometry but gains proteolytic stability. Core move in "
            "peptidomimetic drug design."
        ),
        smarts="[#6:1]C(=O)O[#6:2]>>[#6:1]C(=O)N[#6:2]",
    ),
]


# ---------------------------------------------------------------------

def list_bioisosteres() -> List[Dict[str, str]]:
    """Enumerate the bioisostere catalogue."""
    return [
        {"id": b.id, "label": b.label, "description": b.description}
        for b in BIOISOSTERES
    ]


def _dedupe_products(results) -> List[str]:
    """Sanitise + canonicalise + deduplicate RunReactants output."""
    seen: set = set()
    out: List[str] = []
    for prods in results:
        if not prods:
            continue
        m = prods[0]
        try:
            Chem.SanitizeMol(m)
        except Exception:
            continue
        smi = Chem.MolToSmiles(m)
        if smi in seen:
            continue
        seen.add(smi)
        out.append(smi)
    return out


def suggest_bioisosteres(smiles: str,
                         template_ids: List[str] = None) -> Dict[str, Any]:
    """Apply every bioisostere template to ``smiles`` and return the
    unique set of variants.

    Returns ``{"target": canonical, "n_variants": N, "variants": [
    {"template_id", "label", "smiles"}, ...]}`` or ``{"error": ...}``.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"error": f"Unparseable SMILES: {smiles!r}"}
    canon = Chem.MolToSmiles(mol)
    templates = BIOISOSTERES
    if template_ids:
        wanted = set(template_ids)
        templates = [b for b in BIOISOSTERES if b.id in wanted]

    variants: List[Dict[str, Any]] = []
    # Silence the "product has no mapped atoms" warning when templates
    # have unmapped atoms by design.
    RDLogger.DisableLog("rdApp.warning")
    try:
        for b in templates:
            try:
                rxn = AllChem.ReactionFromSmarts(b.smarts)
            except Exception:
                continue
            fresh_mol = Chem.MolFromSmiles(canon)
            new_smiles = _dedupe_products(rxn.RunReactants((fresh_mol,)))
            for v in new_smiles:
                if v == canon:
                    continue  # self-match; not a transformation
                variants.append({
                    "template_id": b.id,
                    "label": b.label,
                    "smiles": v,
                })
    finally:
        RDLogger.EnableLog("rdApp.warning")

    # Deduplicate across templates: same product via 2 templates counts once
    # but we keep the first template's label (usually the classic direction).
    seen: set = set()
    deduped: List[Dict[str, Any]] = []
    for v in variants:
        if v["smiles"] in seen:
            continue
        seen.add(v["smiles"])
        deduped.append(v)

    return {
        "target": canon,
        "n_variants": len(deduped),
        "variants": deduped,
    }
