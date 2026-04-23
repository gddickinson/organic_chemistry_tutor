"""Classic textbook mechanisms (substitution, elimination, pericyclic,
addition).  Imported by :mod:`orgchem.db.seed_mechanisms`.

Atom indices below were verified against RDKit's canonical SMILES parse
order.  Changing a SMILES string here will silently reshuffle indices —
re-verify after any edit.
"""
from __future__ import annotations

from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep


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
                Arrow(from_atom=2, to_atom=0, kind="curly"),
                Arrow(from_atom=0, to_atom=1, kind="curly"),
            ],
        ),
        MechanismStep(
            title="Products",
            description=(
                "Methanol and bromide ion. The carbon has undergone "
                "inversion of configuration (not visible for achiral CH₃Br, "
                "but the textbook signature of SN2)."
            ),
            smiles="CO.[Br-]",
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
            smiles="CC(C)(C)Br",
            arrows=[Arrow(from_atom=1, to_atom=4, kind="curly")],
        ),
        MechanismStep(
            title="Step 2: Nucleophilic capture (fast)",
            description=(
                "Water attacks the planar carbocation. Attack from either "
                "face is equally likely, which is why SN1 racemises a "
                "chiral centre."
            ),
            smiles="C[C+](C)C.O.[Br-]",
            arrows=[Arrow(from_atom=4, to_atom=1, kind="curly")],
        ),
        MechanismStep(
            title="Step 3: Deprotonation",
            description=(
                "The oxonium intermediate loses a proton to solvent, "
                "giving the neutral alcohol."
            ),
            smiles="CC(C)(C)[OH2+].[Br-]",
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
            smiles="CCC(Br)C.[OH-]",
            arrows=[
                Arrow(from_atom=5, to_atom=1, kind="curly",
                      label="base takes beta-H"),
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="new pi"),
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
            arrows=[Arrow(from_atom=1, to_atom=4, kind="curly")],
        ),
        MechanismStep(
            title="Step 2: Loss of β-hydrogen",
            description=(
                "Solvent (or a weak base) removes a β-proton; the C–H "
                "bonding pair becomes the new pi bond of the alkene."
            ),
            smiles="C[C+](C)C.[Br-]",
            arrows=[Arrow(from_atom=0, to_atom=1, kind="curly",
                          label="new pi")],
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
            smiles="CC(=O)C.[OH-]",
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
            smiles="CC(=CC(=O)C)C.O",
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
            smiles="C=CC=C.C=C",
            arrows=[
                Arrow(from_atom=0, to_atom=5, kind="curly", label="new bond"),
                Arrow(from_atom=4, to_atom=3, kind="curly", label="new bond"),
                Arrow(from_atom=2, to_atom=1, kind="curly", label="pi shift"),
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


BUILDERS = {
    "SN2: methyl bromide":  _sn2,
    "SN1: tert-butyl":      _sn1,
    "E2: 2-bromobutane":    _e2,
    "E1: tert-butyl":       _e1,
    "Diels-Alder":          _diels_alder,
    "Aldol condensation":   _aldol,
    "Grignard addition":    _grignard,
    "Wittig reaction":      _wittig,
    "Michael addition":     _michael,
}
