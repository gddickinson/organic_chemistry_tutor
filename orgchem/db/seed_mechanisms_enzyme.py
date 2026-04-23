"""Enzyme-active-site mechanisms. Imported by
:mod:`orgchem.db.seed_mechanisms`.

Covers chymotrypsin (serine-protease triad), class-I aldolase
(Schiff-base aldol), HIV protease (aspartic-protease peptide
hydrolysis), and RNase A (two-step phosphoryl transfer).  The HIV
and RNase entries exercise the Phase 13c lone-pair dot + bond-midpoint
arrow features.
"""
from __future__ import annotations

from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep


def _chymotrypsin() -> Mechanism:
    """Serine-protease catalytic-triad mechanism, teaching-level.

    Pedagogically simplified: we draw the scissile peptide as
    ``CC(=O)NCC(=O)O`` (N-acetylglycine) and spell out the four
    textbook events on the substrate's atoms. The enzyme residues
    (His-57 / Ser-195 / Asp-102) are described in the captions but
    not drawn — a full enzyme drawing would overwhelm the 2D view.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Ser-OH attacks the scissile C=O",
            description=(
                "His-57 acts as a general base (deprotonates Ser-195). "
                "The activated Ser alkoxide attacks the carbonyl C of the "
                "peptide substrate, giving a tetrahedral intermediate. "
                "Asp-102 electrostatically stabilises the His-57+."
            ),
            smiles="CC(=O)NCC(=O)O",
            arrows=[Arrow(from_atom=1, to_atom=2, kind="curly",
                          label="C=O pi to O")],
        ),
        MechanismStep(
            title="Step 2: Collapse of tetrahedral intermediate — amine leaves",
            description=(
                "The tetrahedral oxide collapses back to C=O, ejecting "
                "the amine portion (which picks up a proton from "
                "His-57+). The remaining acyl-enzyme has replaced the "
                "amide N with a Ser ester."
            ),
            smiles="CC(=O)O.NCC(=O)O",
            arrows=[],
        ),
        MechanismStep(
            title="Step 3: Water attacks the acyl-enzyme",
            description=(
                "A second cycle — His-57 now deprotonates water; the "
                "hydroxide attacks the acyl-serine carbonyl, giving a "
                "new tetrahedral intermediate. Symmetry-identical to "
                "step 1 with water in place of Ser."
            ),
            smiles="CC(=O)O.O",
            arrows=[Arrow(from_atom=3, to_atom=1, kind="curly",
                          label="H2O attacks")],
        ),
        MechanismStep(
            title="Step 4: Release of the free carboxylic acid",
            description=(
                "Tetrahedral collapse regenerates free enzyme and "
                "releases the carboxylic acid half of the original "
                "substrate. Overall: one amide bond hydrolysed, enzyme "
                "returned to resting state."
            ),
            smiles="CC(=O)O",
            arrows=[],
        ),
    ])


def _aldolase_class_I() -> Mechanism:
    """Class-I fructose-bisphosphate aldolase (Schiff-base aldol).

    Simplified to the C-C bond-forming step: an enzyme-bound enamine
    (drawn as a simple enamine CH₂=C(OH)-O for pedagogical clarity)
    attacks the aldehyde carbon of glyceraldehyde-3-phosphate. The
    resulting aldol product is released after Schiff-base hydrolysis.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Schiff base with DHAP",
            description=(
                "Active-site Lys-229 (E. coli numbering) attacks the "
                "ketone C of DHAP, giving a carbinolamine that loses "
                "water to form an imine (Schiff base). The α-CH₂ next "
                "to the imine acidifies — the enamine form dominates "
                "in the active site."
            ),
            smiles="OCC(=O)C.NC",
            arrows=[Arrow(from_atom=5, to_atom=2, kind="curly",
                          label="Lys-N attacks C=O")],
        ),
        MechanismStep(
            title="Step 2: Enamine attacks G3P",
            description=(
                "The enamine (α-C nucleophilic) attacks the aldehyde "
                "C of G3P in an aldol-like step. A new C-C bond forms "
                "between what will become C3 and C4 of fructose."
            ),
            smiles="OCC(=NC)C.O=C[C@@H](O)CO",
            arrows=[
                Arrow(from_atom=3, to_atom=6, kind="curly",
                      label="enamine to aldehyde C"),
                Arrow(from_atom=6, to_atom=7, kind="curly",
                      label="C=O pi to O-"),
            ],
        ),
        MechanismStep(
            title="Step 3: Hydrolysis releases fructose-1,6-BP",
            description=(
                "Water hydrolyses the iminium-form Schiff base: "
                "carbinolamine → free amine + ketone. The active-site "
                "Lys is regenerated and the product F1,6BP is released."
            ),
            smiles="OCC(=O)[C@@H](O)[C@H](O)[C@@H](O)CO",
            arrows=[],
        ),
    ])


def _rnase_a() -> Mechanism:
    """Ribonuclease A: two-step in-line phosphoryl-transfer on RNA.

    Teaching-simplified: the canonical RNase A mechanism has two
    histidines flanking the active site — His-12 acts as a general
    base and His-119 as a general acid (roles swap in step 2).
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Transphosphorylation → 2',3'-cyclic phosphate",
            description=(
                "His-12 deprotonates the 2'-OH of the substrate ribose. "
                "The resulting 2'-oxide attacks the phosphorus in-line "
                "with the P-O(5') bond. The 5'-oxygen of the downstream "
                "nucleotide leaves (protonated by His-119), cleaving "
                "the RNA strand. Product: a 2',3'-cyclic phosphate on "
                "the upstream ribose."
            ),
            smiles="OC1COP(=O)(O)OC1",
            arrows=[
                Arrow(from_atom=0, to_atom=3, kind="curly",
                      label="O2' → P"),
                Arrow(from_atom=3, to_atom=5, from_bond=(3, 4),
                      kind="curly", label="P-O5' breaks"),
            ],
            lone_pairs=[0],
        ),
        MechanismStep(
            title="Step 2: Hydrolysis → 3'-phosphate + free 2'-OH",
            description=(
                "Roles reverse. His-12 is now protonated (from step 1) "
                "and donates a proton to a departing oxygen. His-119 "
                "deprotonates a bound water; the hydroxide attacks the "
                "cyclic phosphate in-line with the P-O(2') bond. The "
                "2'-oxygen leaves, regenerating the 2'-OH on the ribose "
                "and giving the 3'-phosphate terminus."
            ),
            smiles="OC1COP(=O)(O)OC1.O",
            arrows=[
                Arrow(from_atom=8, to_atom=3, kind="curly",
                      label="H2O → P"),
                Arrow(from_atom=3, to_atom=0, from_bond=(3, 6),
                      kind="curly", label="P-O2' breaks"),
            ],
            lone_pairs=[8],
        ),
    ])


def _hiv_protease() -> Mechanism:
    """HIV-1 protease peptide-bond hydrolysis — teaching-level.

    Aspartic-protease mechanism: the two catalytic aspartates
    (Asp-25 on chain A, Asp-25' on chain B, at the homodimer
    interface) activate a water molecule that attacks the scissile
    peptide carbonyl.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Asp-activated water attacks scissile C=O",
            description=(
                "Asp-25 (protonated) H-bonds to the scissile peptide "
                "oxygen; Asp-25' (deprotonated) removes a proton from a "
                "bound water. The nucleophilic hydroxide attacks the "
                "peptide carbonyl carbon, giving a tetrahedral gem-diol "
                "intermediate."
            ),
            smiles="CC(=O)NCC.O",
            arrows=[
                Arrow(from_atom=5, to_atom=1, kind="curly",
                      label="H2O → C(=O)"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O π → O"),
            ],
            lone_pairs=[5],
        ),
        MechanismStep(
            title="Step 2: Tetrahedral collapse — C-N bond breaks",
            description=(
                "The gem-diol tetrahedral intermediate collapses: the "
                "C-N σ bond breaks at the scissile position and electrons "
                "move onto the leaving amine. Asp-25 shuttles a proton "
                "onto the departing nitrogen to give the neutral amine."
            ),
            smiles="CC(=O)O.NCC",
            arrows=[
                Arrow(from_atom=0, to_atom=4, from_bond=(1, 4),
                      kind="curly", label="C-N breaks"),
            ],
            lone_pairs=[4],
        ),
        MechanismStep(
            title="Step 3: Products diffuse away; active site resets",
            description=(
                "The two products (the newly formed carboxylic acid + "
                "the free amine) leave the active site. Asp-25 / Asp-25' "
                "return to their resting protonation states — one acid, "
                "one conjugate base — ready for another substrate."
            ),
            smiles="CC(=O)O.NCC",
            arrows=[],
        ),
    ])


BUILDERS = {
    "Chymotrypsin":     _chymotrypsin,
    "Aldolase class I": _aldolase_class_I,
    "HIV protease":     _hiv_protease,
    "RNase A":          _rnase_a,
}
