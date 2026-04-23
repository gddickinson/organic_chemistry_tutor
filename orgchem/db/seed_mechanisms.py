"""Seed textbook mechanisms into the ``Reaction.mechanism_json`` column.

Atom indices below were verified against RDKit's canonical SMILES parse
order (see :mod:`orgchem.core.formats.mol_from_smiles`). Changing a SMILES
string here will silently reshuffle indices — re-verify after any edit.
"""
from __future__ import annotations
import logging
from typing import Dict, List

from sqlalchemy import select

from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep
from orgchem.db.models import Reaction as DBRxn
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Mechanism definitions. Keyed by substring match against reaction name.

def _sn2() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Concerted backside attack",
            description=(
                "Hydroxide's lone pair attacks the carbon from the face "
                "opposite bromine. Simultaneously the C–Br σ bond breaks, "
                "with both electrons going to Br. The transition state is "
                "pentacoordinate at carbon."
            ),
            smiles="C[Br].[OH-]",   # 0=C, 1=Br, 2=O⁻
            arrows=[
                Arrow(from_atom=2, to_atom=0, kind="curly"),   # OH⁻ lone pair → C
                Arrow(from_atom=0, to_atom=1, kind="curly"),   # C–Br → Br
            ],
        ),
        MechanismStep(
            title="Products",
            description=(
                "Methanol and bromide ion. The carbon has undergone "
                "inversion of configuration (not visible for achiral CH₃Br, "
                "but the textbook signature of SN2)."
            ),
            smiles="CO.[Br-]",   # 0=C, 1=O, 2=Br⁻
        ),
    ])


def _sn1() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Ionisation (slow, rate-determining)",
            description=(
                "The C–Br σ bond heterolyses. Both bonding electrons leave "
                "with Br, generating a tertiary carbocation. Rate depends "
                "only on the substrate."
            ),
            smiles="CC(C)(C)Br",   # 0,2,3=CH₃, 1=C(br), 4=Br
            arrows=[
                Arrow(from_atom=1, to_atom=4, kind="curly"),   # C–Br → Br
            ],
        ),
        MechanismStep(
            title="Step 2: Nucleophilic capture (fast)",
            description=(
                "Water attacks the planar carbocation. Attack from either "
                "face is equally likely, which is why SN1 racemises a "
                "chiral centre."
            ),
            smiles="C[C+](C)C.O.[Br-]",   # 0=C, 1=C⁺, 2,3=C, 4=O, 5=Br⁻
            arrows=[
                Arrow(from_atom=4, to_atom=1, kind="curly"),   # water O → C⁺
            ],
        ),
        MechanismStep(
            title="Step 3: Deprotonation",
            description=(
                "The oxonium intermediate loses a proton to solvent, "
                "giving the neutral alcohol."
            ),
            smiles="CC(C)(C)[OH2+].[Br-]",   # 0,2,3=C, 1=C(br), 4=O⁺, 5=Br⁻
        ),
        MechanismStep(
            title="Products",
            description=(
                "tert-Butanol and bromide. The tertiary carbocation "
                "intermediate is why tertiary substrates favour SN1."
            ),
            smiles="CC(C)(C)O.[Br-]",
        ),
    ])


def _e2() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Concerted anti-periplanar elimination",
            description=(
                "Three arrows move in concert: the base takes the β-hydrogen, "
                "its C–H bonding pair becomes the new pi bond, and the C–Br "
                "σ bond leaves with Br. The β-H and Br must be "
                "antiperiplanar across the C–C bond."
            ),
            smiles="CCC(Br)C.[OH-]",   # 0=CH₃, 1=β-C, 2=α-C, 3=Br, 4=CH₃, 5=OH⁻
            arrows=[
                # Base reaches for a β-H (shown atom-to-atom as O → β-C).
                Arrow(from_atom=5, to_atom=1, kind="curly",
                      label="base takes beta-H"),
                # β-C–H bond pair becomes the new pi bond to α-C.
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="new pi"),
                # α-C–Br bond breaks, electrons leave with Br.
                Arrow(from_atom=2, to_atom=3, kind="curly",
                      label="C-Br to Br"),
            ],
        ),
        MechanismStep(
            title="Products",
            description=(
                "trans-2-butene (Zaitsev — the more substituted alkene) "
                "plus bromide and water."
            ),
            smiles="CC=CC.[Br-].O",
        ),
    ])


def _e1() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Ionisation (slow)",
            description=(
                "Same first step as SN1 — the C–Br bond breaks to give a "
                "tertiary carbocation. SN1 and E1 compete from this "
                "intermediate."
            ),
            smiles="CC(C)(C)Br",
            arrows=[
                Arrow(from_atom=1, to_atom=4, kind="curly"),
            ],
        ),
        MechanismStep(
            title="Step 2: Loss of β-hydrogen",
            description=(
                "Solvent (or a weak base) removes a β-proton; the C–H "
                "bonding pair becomes the new pi bond of the alkene."
            ),
            smiles="C[C+](C)C.[Br-]",   # 0=β-C, 1=C⁺, 2,3=C, 4=Br⁻
            arrows=[
                Arrow(from_atom=0, to_atom=1, kind="curly",
                      label="new pi"),
            ],
        ),
        MechanismStep(
            title="Products",
            description=(
                "Isobutylene (2-methylpropene) plus HBr. With tertiary "
                "substrates, E1 competes strongly with SN1 — heat drives "
                "toward elimination."
            ),
            smiles="C=C(C)C.[Br-]",
        ),
    ])


def _aldol() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Enolate formation",
            description=(
                "Hydroxide (a base) removes an alpha proton from acetone. "
                "The carbonyl stabilises the resulting carbanion through "
                "resonance — this is the enolate. The acidity of alpha-CH "
                "(pKa ≈ 20) is why such dilute base works at all."
            ),
            smiles="CC(=O)C.[OH-]",   # 0=CH3, 1=C=O carbon, 2=O, 3=alpha-CH3, 4=OH-
            arrows=[
                Arrow(from_atom=4, to_atom=3, kind="curly",
                      label="base takes alpha-H"),
                Arrow(from_atom=3, to_atom=1, kind="curly",
                      label="e- into C=O"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O to O-"),
            ],
        ),
        MechanismStep(
            title="Step 2: Enolate attacks the second carbonyl",
            description=(
                "The nucleophilic alpha-carbon of the enolate attacks the "
                "electrophilic carbonyl carbon of a second acetone. The C=O pi "
                "electrons move onto the oxygen, giving an alkoxide intermediate."
            ),
            # Atoms: 0,1,2,3 = first acetone (unchanged), 4=alpha-C of enolate,
            # 5=C-carbonyl of enolate, 6=O of enolate, 7=CH3 of enolate
            smiles="CC(=O)C.[CH2-]C(=O)C",
            arrows=[
                Arrow(from_atom=4, to_atom=1, kind="curly",
                      label="alpha-C to C=O"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O to O"),
            ],
        ),
        MechanismStep(
            title="Step 3: Protonation + dehydration",
            description=(
                "Protonation of the alkoxide gives the beta-hydroxy ketone "
                "(aldol adduct). Further acid / base / heat promotes loss of "
                "water to give the alpha,beta-unsaturated ketone (the "
                "condensation product)."
            ),
            smiles="CC(=CC(=O)C)C.O",   # the conjugated product + water
        ),
    ])


def _grignard() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Nucleophilic addition",
            description=(
                "The polarised C-Mg bond puts a carbanion-like methyl group "
                "at the Mg. That nucleophilic carbon attacks the electrophilic "
                "carbonyl carbon of acetone; the C=O pi electrons go onto the "
                "oxygen as an alkoxide."
            ),
            # 0=C of MeMgBr, 1=Mg, 2=Br, 3=CH3 of acetone, 4=C=O carbon,
            # 5=O of acetone, 6=other CH3
            smiles="C[Mg]Br.CC(=O)C",
            arrows=[
                Arrow(from_atom=0, to_atom=4, kind="curly",
                      label="Me- attacks C=O"),
                Arrow(from_atom=4, to_atom=5, kind="curly",
                      label="C=O to O-"),
            ],
        ),
        MechanismStep(
            title="Step 2: Aqueous workup",
            description=(
                "Aqueous acid (or water) protonates the alkoxide, giving the "
                "neutral tertiary alcohol. Magnesium salts wash away. Grignards "
                "are the textbook way to install a tertiary alcohol with "
                "predictable regiochemistry."
            ),
            smiles="CC([O-])(C)C.[Mg+]Br",
        ),
        MechanismStep(
            title="Products",
            description="tert-Butanol (the 3° alcohol) plus MgBrOH.",
            smiles="CC(C)(C)O.Br[Mg]O",
        ),
    ])


def _diels_alder() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Concerted [4+2] cycloaddition",
            description=(
                "Three arrows chase each other in a cyclic 6-electron flow: "
                "one diene terminus attacks one end of the dienophile, the "
                "dienophile π bond becomes the other new bond bond, and the "
                "internal diene π shifts from 2,3 to 1,2. All in a single "
                "pericyclic transition state."
            ),
            # 0=1 (diene π), 1-2 single, 2=3 (diene π); 4=5 (dienophile π)
            smiles="C=CC=C.C=C",
            arrows=[
                Arrow(from_atom=0, to_atom=5, kind="curly",
                      label="new bond"),
                Arrow(from_atom=4, to_atom=3, kind="curly",
                      label="new bond"),
                Arrow(from_atom=2, to_atom=1, kind="curly",
                      label="pi shift"),
            ],
        ),
        MechanismStep(
            title="Cyclohexene product",
            description=(
                "The new six-membered ring has the dienophile's σ bonds "
                "in place, and the former internal σ bond of the diene is "
                "now the ring π bond."
            ),
            smiles="C1=CCCCC1",
        ),
    ])


# ------------------------------------------------------------------
# Matcher: name substring → mechanism builder.

def _wittig() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Ylide attacks the carbonyl",
            description=(
                "The negatively-polarised ylide carbon attacks the "
                "electrophilic carbonyl carbon of the aldehyde. The C=O pi "
                "electrons shift onto the oxygen, giving a zwitterionic "
                "betaine. Two arrows in concert — a classic addition "
                "across a π bond."
            ),
            # 0=CH3, 1=C=O carbon, 2=O, 3=ylide C (nucleophile), 4=P
            smiles="CC=O.[CH2-][P+](c1ccccc1)(c1ccccc1)c1ccccc1",
            arrows=[
                Arrow(from_atom=3, to_atom=1, kind="curly",
                      label="ylide attacks C=O"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O pi to O-"),
            ],
        ),
        MechanismStep(
            title="Step 2: Betaine → oxaphosphetane",
            description=(
                "The betaine (a 1,2-zwitterion with O- on one carbon and "
                "P+ on the adjacent one) cyclises: the alkoxide oxygen "
                "attacks the positively-charged phosphorus, forming a "
                "four-membered oxaphosphetane ring. This step is usually "
                "fast and proceeds without arrow-pushing notation."
            ),
            # Betaine: 0=CH3, 1=C-O-, 2=O, 3=CH2 bridge, 4=P
            smiles="CC([O-])C[P+](c1ccccc1)(c1ccccc1)c1ccccc1",
            arrows=[],
        ),
        MechanismStep(
            title="Step 3: Fragmentation → alkene + O=PPh3",
            description=(
                "The four-membered oxaphosphetane collapses in a retro-[2+2] "
                "fashion: the C-C bond and the P-O bond of the ring both "
                "break, forming the new C=C double bond of the product "
                "alkene and the very stable P=O double bond of "
                "triphenylphosphine oxide. The P=O bond is the "
                "thermodynamic sink that makes Wittig irreversible."
            ),
            # Products: 0=CH3, 1=CH=, 2=CH2, 3=O, 4=P
            smiles="CC=C.O=P(c1ccccc1)(c1ccccc1)c1ccccc1",
            arrows=[],
        ),
    ])


def _michael() -> Mechanism:
    return Mechanism(steps=[
        MechanismStep(
            title="Concerted 1,4-addition",
            description=(
                "The stabilised enolate attacks the beta-carbon of methyl "
                "vinyl ketone (Michael acceptor). Three arrows move in "
                "concert: the enolate delivers its electron pair to the "
                "beta-C; the alpha-beta pi bond shifts into a new pi bond "
                "toward the carbonyl carbon (forming the enolate of the "
                "product); and the C=O pi bond moves onto oxygen, giving "
                "the enolate oxide. 'Soft nucleophile on soft "
                "electrophile' — the MO story that defines Michael "
                "additions."
            ),
            # 0=CH3 (MVK), 1=C(=O) of MVK, 2=O, 3=alpha-C (sp2), 4=beta-C (sp2),
            # 5=nucleophile C- (acetone enolate), 6=C=O of enolate, 7=O, 8=CH3
            smiles="CC(=O)C=C.[CH2-]C(=O)C",
            arrows=[
                Arrow(from_atom=5, to_atom=4, kind="curly",
                      label="Nu to beta-C"),
                Arrow(from_atom=3, to_atom=1, kind="curly",
                      label="pi shift alpha->C=O"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O to O-"),
            ],
        ),
        MechanismStep(
            title="Protonation gives the 1,5-diketone",
            description=(
                "The enolate intermediate is protonated (by solvent or "
                "added acid) at the alpha-carbon, giving the neutral "
                "Michael adduct — a 1,5-diketone, here 2,5-hexanedione "
                "(acetonylacetone)."
            ),
            smiles="CC(=O)CCCC(=O)C",
            arrows=[],
        ),
    ])


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
            # 0=CH3, 1=C(=O), 2=O, 3=N, 4=CH2, 5=C(=O) (new acid), 6=O, 7=O
            smiles="CC(=O)NCC(=O)O",
            arrows=[
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O pi to O"),
            ],
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
            arrows=[
                Arrow(from_atom=3, to_atom=1, kind="curly",
                      label="H2O attacks"),
            ],
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
            # Simplified DHAP + Lys as CC(=NC)CO for teaching
            smiles="OCC(=O)C.NC",
            arrows=[
                Arrow(from_atom=5, to_atom=2, kind="curly",
                      label="Lys-N attacks C=O"),
            ],
        ),
        MechanismStep(
            title="Step 2: Enamine attacks G3P",
            description=(
                "The enamine (α-C nucleophilic) attacks the aldehyde "
                "C of G3P in an aldol-like step. A new C-C bond forms "
                "between what will become C3 and C4 of fructose."
            ),
            # enamine of DHAP-Lys + glyceraldehyde; simplified atoms
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

    Step 1 (transphosphorylation): His-12 deprotonates the 2'-OH
    of the substrate ribose; the 2'-oxygen attacks the phosphorus
    (SN2-at-P); the 5'-oxygen of the downstream nucleotide leaves,
    cleaving the RNA strand. A 2',3'-cyclic phosphate forms.

    Step 2 (hydrolysis): the roles reverse. His-12 now protonates
    to deliver a proton to the departing 3'-oxygen; His-119
    deprotonates a water, which attacks the cyclic phosphate
    in-line. Net: 3'-phosphate + free 2'-OH on the ribose.

    Further exercises Phase 13c: both steps have ``lone_pairs`` on
    the attacking oxygen, and both use a bond-midpoint arrow to
    show cleavage of the P-O σ bond to the leaving group.
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
            # Substrate atoms (simplified): 0=C3', 1=O3', 2=P, 3=O5',
            # 4=C5' of the leaving nucleotide, 5=O2' (attacker), 6=C2'.
            smiles="OC1COP(=O)(O)OC1",
            arrows=[
                # 2'-oxide attacks P (attacker → P)
                Arrow(from_atom=0, to_atom=3, kind="curly",
                      label="O2' → P"),
                # P-O(5') σ bond breaks — arrow exits the bond midpoint
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
                # Water attacks P
                Arrow(from_atom=8, to_atom=3, kind="curly",
                      label="H2O → P"),
                # P-O(2') σ bond breaks from the bond midpoint
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
    peptide carbonyl. Pedagogically simplified to the substrate
    atoms only; the two Asp side chains are described in the
    captions. This mechanism is why HIV protease is the canonical
    PPI-vs-ligand teaching example (Phase 24j: the active site *is*
    the dimer interface).

    Phase 13c follow-up exercised here: ``lone_pairs`` mark the water
    oxygen in step 1, and an arrow targets the bond **midpoint** of
    the scissile C-N peptide bond to illustrate σ-bond cleavage in
    step 2.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Asp-activated water attacks scissile C=O",
            description=(
                "Asp-25 (protonated) H-bonds to the scissile peptide "
                "oxygen; Asp-25' (deprotonated) removes a proton from a "
                "bound water. The nucleophilic hydroxide attacks the "
                "peptide carbonyl carbon, giving a tetrahedral gem-diol "
                "intermediate. Substrate atoms: 0=N-term side, 1=C(=O), "
                "2=O, 3=N, 4=C-term side; 5/6=bound water O/H pair."
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
                "onto the departing nitrogen to give the neutral amine. "
                "The arrow exits the midpoint of the C-N bond to show "
                "σ-bond heterolysis."
            ),
            smiles="CC(=O)O.NCC",
            arrows=[
                # Arrow runs from the C-N bond midpoint onto the amine N.
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


def _fischer_esterification() -> Mechanism:
    """Round-59 addition: the canonical acid-catalysed ester
    synthesis. Six teaching-grade steps walking through
    carbonyl protonation, nucleophilic addition, proton
    shuffling, water departure, and deprotonation.

    Reaction shown in the seeded DB: acetic acid + ethanol →
    ethyl acetate + water (H⁺ catalysed).
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Protonation of the carbonyl oxygen",
            description=(
                "A proton from the acid catalyst (H₃O⁺ in the "
                "reaction flask) adds to the acetic-acid carbonyl "
                "oxygen. This makes the carbonyl carbon much more "
                "electrophilic (positive charge on the oxygen "
                "pulls electron density away from the adjacent C)."
            ),
            # Atoms: 0=CH3, 1=C(=O)OH, 2=O(=), 3=O-H, 4=H (from H+)
            smiles="CC(=O)O.[H+]",
            arrows=[
                Arrow(from_atom=2, to_atom=4, kind="curly",
                      label="C=O lone pair → H⁺"),
            ],
            lone_pairs=[2],
        ),
        MechanismStep(
            title="Step 2: Ethanol attacks the activated carbonyl",
            description=(
                "Ethanol's oxygen lone pair attacks the now-"
                "electrophilic carbonyl carbon. The C=O+ π bond "
                "collapses onto the oxygen, giving a tetrahedral "
                "intermediate with the C now sp³."
            ),
            # Atoms: 0=CH3(acid), 1=C(of acid), 2=O+, 3=O-H,
            # 4=O(of ethanol), 5=CH2, 6=CH3
            smiles="CC(=[OH+])O.OCC",
            arrows=[
                Arrow(from_atom=4, to_atom=1, kind="curly",
                      label="EtOH lone pair → C"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O⁺ → O"),
            ],
            lone_pairs=[4],
        ),
        MechanismStep(
            title="Step 3: Proton transfer (EtOH⁺ → OH)",
            description=(
                "A proton from the attacking ethanol (now a "
                "positively-charged oxonium on the tetrahedral "
                "carbon) is transferred to one of the acetic-"
                "acid OHs. In practice the solvent shuttles the "
                "proton; the net effect is to give the tetrahedral "
                "intermediate with a good leaving group — H₂O."
            ),
            # Atoms: 0=CH3, 1=C(sp3 tetrahedral), 2=OH, 3=OH,
            # 4=OH+(Et still attached), 5=Et. Simplified shorthand.
            smiles="CC(O)(O)[OH+]CC",
            arrows=[
                Arrow(from_atom=4, to_atom=2, kind="curly",
                      label="proton hops via solvent"),
            ],
            lone_pairs=[2, 3],
        ),
        MechanismStep(
            title="Step 4: Water leaves as a good leaving group",
            description=(
                "With the oxonium now on one of the original-"
                "carboxylate oxygens, the C–OH₂⁺ bond breaks. "
                "The two electrons leave with the water; the "
                "adjacent oxygen's lone pair collapses into a "
                "new π bond to restore the sp² carbonyl."
            ),
            # 0=CH3, 1=C, 2=O(becoming C=O), 3=O-Et, 4=O-H+(leaving)
            smiles="CC(O)(OCC)[OH2+]",
            arrows=[
                Arrow(from_atom=2, to_atom=1, kind="curly",
                      label="O lone pair → C"),
                Arrow(from_atom=1, to_atom=4, kind="curly",
                      label="C–OH₂⁺ → O+ leaves as H₂O"),
            ],
            lone_pairs=[2],
        ),
        MechanismStep(
            title="Step 5: Deprotonation → neutral ester",
            description=(
                "A final base (another ethanol or water) removes "
                "the proton from the remaining oxonium, giving "
                "the neutral ethyl acetate product and regenerating "
                "the acid catalyst. The reaction is reversible — "
                "driven forward by excess ethanol or by removing "
                "water (Dean-Stark, molecular sieves)."
            ),
            smiles="CC(=O)OCC.O",
        ),
    ])


def _nabh4_reduction() -> Mechanism:
    """Single-step hydride transfer from NaBH₄ to acetone.

    The canonical "metal hydride reduces carbonyl" demonstration —
    short, clean, high-value for teaching. Works the same way for
    aldehydes, ketones, and (slowly) esters.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Hydride delivery to the carbonyl carbon",
            description=(
                "The B–H bond of BH₄⁻ carries two bonding electrons. "
                "Those electrons attack the electrophilic carbonyl "
                "carbon of acetone — with B becoming trivalent BH₃ "
                "as the hydride hops across. Simultaneously the C=O "
                "π bond collapses onto the oxygen, giving an "
                "alkoxide. Water or alcohol workup protonates the "
                "alkoxide to the final 2-propanol."
            ),
            # Atoms: 0,3=CH3, 1=C(sp2 carbonyl), 2=O, 4=B, 5-8=H on B
            smiles="CC(=O)C.[BH4-]",
            arrows=[
                Arrow(from_atom=4, to_atom=1, kind="curly",
                      label="B–H bond → C"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O → O⁻"),
            ],
        ),
        MechanismStep(
            title="Aqueous workup → 2-propanol",
            description=(
                "The alkoxide is protonated by water / methanol on "
                "workup. Net transformation: acetone + H⁻ + H⁺ → "
                "isopropanol. NaBH₄ delivers one hydride per B; the "
                "other three are less reactive but eventually "
                "consumed as BH₃ → B(OH)₃ in water."
            ),
            smiles="CC(O)C.[BH3]",
        ),
    ])


def _nitration_benzene() -> Mechanism:
    """Canonical EAS mechanism — HNO₃ / H₂SO₄ nitrating benzene to
    nitrobenzene. Three teaching-grade steps through the Wheland
    (arenium) intermediate.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Generation of the nitronium electrophile",
            description=(
                "H₂SO₄ protonates HNO₃, and the protonated species "
                "loses water to give the nitronium ion NO₂⁺ — the "
                "true electrophile in aromatic nitration. Net "
                "stoichiometry: HNO₃ + H₂SO₄ → NO₂⁺ + HSO₄⁻ + H₂O."
            ),
            # Atoms (cartoon): 0=O, 1=N+, 2=O of NO2+ (linear)
            smiles="O=[N+]=O.O",
            arrows=[
                Arrow(from_atom=0, to_atom=1, kind="curly",
                      label="N=O (electrophile)"),
            ],
        ),
        MechanismStep(
            title="Step 2: Benzene attacks NO₂⁺ → arenium ion",
            description=(
                "A π bond of benzene attacks the electrophilic "
                "nitrogen of NO₂⁺. One ring carbon becomes sp³ "
                "(tetrahedral — now carries the incoming NO₂ + an "
                "H); the remaining four π electrons are delocalised "
                "across the other five carbons — the classic "
                "cyclohexadienyl-cation / Wheland intermediate. "
                "Aromaticity is temporarily lost."
            ),
            # Atoms: 0..5 = benzene ring, 6 = N+ of NO2+, 7,8 = O's
            smiles="c1ccccc1.O=[N+]=O",
            arrows=[
                Arrow(from_atom=0, to_atom=7, kind="curly",
                      label="ring π → N⁺"),
            ],
        ),
        MechanismStep(
            title="Step 3: Rearomatisation by loss of H⁺",
            description=(
                "HSO₄⁻ (or any available base) removes the proton "
                "from the sp³ carbon of the Wheland intermediate. "
                "The two electrons from the C–H bond restore the "
                "ring π system — aromaticity comes back and the "
                "product is nitrobenzene. Fast and irreversible "
                "because aromatic stabilisation (~150 kJ/mol) is "
                "the driving force."
            ),
            # Simpler cartoon: show the product (nitrobenzene) plus
            # the base byproduct (H2SO4 regenerated).
            smiles="c1ccc(cc1)[N+](=O)[O-].OS(=O)(=O)O",
        ),
    ])


def _claisen_condensation() -> Mechanism:
    """Ester self-condensation: 2× ethyl acetate + NaOEt → ethyl
    acetoacetate + EtOH. Sibling of the aldol but driven by the
    ester's ability to kick out an alkoxide leaving group.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Ester enolate formation",
            description=(
                "Ethoxide (a base) removes an α-H from ethyl acetate. "
                "The α-pKa is ~25 — higher than ketone α-H (~20) — "
                "so the equilibrium lies against enolate, but the "
                "overall reaction is pulled forward by the very "
                "acidic (pKa ~11) β-keto-ester product in step 4. "
                "The enolate is resonance-stabilised by the ester "
                "carbonyl."
            ),
            # Atoms: 0=CH3 α, 1=C=O, 2=O(=), 3=O(–Et), 4,5=Et,
            # 6=O of EtO⁻, 7,8=Et
            smiles="CC(=O)OCC.[O-]CC",
            arrows=[
                Arrow(from_atom=6, to_atom=0, kind="curly",
                      label="EtO⁻ takes α-H"),
                Arrow(from_atom=0, to_atom=1, kind="curly",
                      label="e⁻ into C=O"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="C=O → O⁻"),
            ],
        ),
        MechanismStep(
            title="Step 2: Enolate attacks the second ester",
            description=(
                "The nucleophilic α-carbon of the enolate attacks "
                "the carbonyl C of a second ester molecule. The C=O "
                "π bond collapses onto the oxygen, giving a "
                "tetrahedral alkoxide intermediate. This is exactly "
                "the aldol step — except with an ester, not a ketone."
            ),
            # 0=α-C of enolate, 1=C=O of enolate-side, 2=O(−),
            # 3..5=OEt, 6=C-carbonyl of second ester, 7=O(=), 8=O-Et,
            # 9,10=Et
            smiles="[CH2-]C(=O)OCC.CC(=O)OCC",
            arrows=[
                Arrow(from_atom=0, to_atom=6, kind="curly",
                      label="α-C → C=O"),
                Arrow(from_atom=6, to_atom=7, kind="curly",
                      label="C=O → O⁻"),
            ],
        ),
        MechanismStep(
            title="Step 3: Ethoxide leaves — restoring C=O",
            description=(
                "The alkoxide on the tetrahedral intermediate "
                "reforms the C=O π bond while kicking out ethoxide "
                "(OEt⁻) as the leaving group. This is the "
                "addition-elimination pattern unique to carboxylic "
                "acid derivatives (ketones can't do this — no good "
                "leaving group)."
            ),
            # Simplified: show the β-keto ester product with EtO⁻
            # already separated off.
            smiles="CC(=O)CC(=O)OCC.[O-]CC",
            arrows=[
                Arrow(from_atom=3, to_atom=1, kind="curly",
                      label="alkoxide collapses to C=O"),
            ],
        ),
        MechanismStep(
            title="Step 4: Deprotonation of the β-keto ester (drives equilibrium)",
            description=(
                "The β-keto ester's α-H sits between two carbonyls "
                "and has pKa ≈ 11 — far more acidic than any "
                "starting material. Ethoxide deprotonates it, and "
                "the doubly-stabilised enolate is trapped. This is "
                "the thermodynamic sink that makes Claisen "
                "condensations viable despite the unfavourable "
                "enolate equilibrium in step 1."
            ),
            smiles="CC(=O)[CH-]C(=O)OCC.CCO",
        ),
    ])


def _pinacol_rearrangement() -> Mechanism:
    """Canonical 1,2-methyl shift: pinacol (2,3-dimethyl-2,3-
    butanediol) rearranges under acid to pinacolone
    (3,3-dimethyl-2-butanone). Textbook example of a carbocation
    driving force — a less-stable secondary cation migrates an
    alkyl group to become a more-stable oxocarbenium.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Protonation of one hydroxyl",
            description=(
                "Acid catalyst (H₃O⁺) protonates one of the two "
                "hydroxyls. The product — a hydroxyl-oxonium — is "
                "now primed to lose water as a neutral leaving "
                "group."
            ),
            # 0=CH3, 1=C(OH)(CH3), 2=O(H), 3=CH3, 4=C(OH)(CH3),
            # 5=O(H), 6=CH3, 7=H+ (external); H2O etc. implicit.
            smiles="CC(C)(O)C(C)(C)O.[H+]",
            arrows=[
                Arrow(from_atom=3, to_atom=7, kind="curly",
                      label="OH lone pair → H⁺"),
            ],
            lone_pairs=[3, 8],
        ),
        MechanismStep(
            title="Step 2: Loss of water → tertiary carbocation",
            description=(
                "The C–OH₂⁺ bond heterolyses — both bonding "
                "electrons leave with water. The resulting carbon "
                "is a tertiary carbocation (three alkyl substituents), "
                "relatively stable but not the most stable option "
                "available to the molecule."
            ),
            smiles="CC(C)(O)C(C)(C)[OH2+]",
            arrows=[
                Arrow(from_atom=4, to_atom=7, kind="curly",
                      label="C–O bond → OH₂⁺ leaves"),
            ],
        ),
        MechanismStep(
            title="Step 3: 1,2-methyl migration",
            description=(
                "A methyl group from the adjacent sp³ carbon (which "
                "still carries the OH) migrates to the cation with "
                "its bonding electrons. The migration target is "
                "better stabilised — the new carbocation is "
                "resonance-stabilised by the adjacent OH "
                "(oxocarbenium character), which is much better "
                "than a plain tertiary cation."
            ),
            # 0=CH3, 1=C(OH) becoming C+, 2=O, 3=CH3, 4=[C+],
            # 5,6=CH3 (one will migrate)
            smiles="CC(O)(C)[C+](C)C",
            arrows=[
                Arrow(from_atom=3, to_atom=4, kind="curly",
                      label="C–Me bond → migrates"),
            ],
            lone_pairs=[2],
        ),
        MechanismStep(
            title="Step 4: Deprotonation → ketone (pinacolone)",
            description=(
                "The oxocarbenium loses the O–H proton to water "
                "(or any base in solution), giving the neutral "
                "C=O ketone — pinacolone. Aromatic-stabilisation-"
                "like driving force: the C=O bond is ~80 kJ/mol "
                "stronger than the equivalent C⁺–O single + "
                "O–H bonds combined."
            ),
            smiles="CC(=O)C(C)(C)C.O",
        ),
    ])


_MECH_MAP = {
    "SN2: methyl bromide":  _sn2,
    "SN1: tert-butyl":      _sn1,
    "E2: 2-bromobutane":    _e2,
    "E1: tert-butyl":       _e1,
    "Diels-Alder":          _diels_alder,
    "Aldol condensation":   _aldol,
    "Grignard addition":    _grignard,
    "Wittig reaction":      _wittig,
    "Michael addition":     _michael,
    "Chymotrypsin":         _chymotrypsin,
    "Aldolase class I":     _aldolase_class_I,
    "HIV protease":         _hiv_protease,
    "RNase A":              _rnase_a,
    "Fischer esterification": _fischer_esterification,
    "NaBH4 reduction":        _nabh4_reduction,
    "Nitration of benzene":   _nitration_benzene,
    "Claisen condensation":   _claisen_condensation,
    "Pinacol rearrangement":  _pinacol_rearrangement,
}


#: Current mechanism-seed format version. Bump whenever the seed data
#: changes meaningfully (labels, arrow indices, added/removed steps) so
#: stale JSON on existing databases is overwritten on next startup.
SEED_VERSION = 10


def seed_mechanisms_if_empty(force: bool = False) -> int:
    """Attach mechanism JSON to seeded reactions that match a known pattern.

    Overwrites existing JSON if its embedded ``seed_version`` is older than
    :data:`SEED_VERSION` (so users picking up a new app version get the
    fresh mechanisms without a manual migration). Pass ``force=True`` to
    rewrite unconditionally.
    """
    import json as _json
    updated = 0
    with session_scope() as s:
        for name_substr, builder in _MECH_MAP.items():
            stmt = select(DBRxn).where(DBRxn.name.like(f"%{name_substr}%"))
            for row in s.scalars(stmt):
                if row.mechanism_json and not force:
                    try:
                        existing = _json.loads(row.mechanism_json)
                    except Exception:
                        existing = {}
                    if existing.get("seed_version", 0) >= SEED_VERSION:
                        continue
                mech = builder()
                mech.reaction_id = row.id
                payload = mech.to_dict()
                payload["seed_version"] = SEED_VERSION
                row.mechanism_json = _json.dumps(payload, indent=2)
                updated += 1
    log.info("Seeded %d mechanisms (version %d)", updated, SEED_VERSION)
    return updated
