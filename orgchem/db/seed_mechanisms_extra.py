"""Phase 31c mechanism-expansion batch (rounds 59-62).

Fischer esterification, NaBH₄ reduction, nitration of benzene,
Claisen condensation, pinacol rearrangement, bromination of ethene
(bromonium), Friedel-Crafts alkylation of benzene.  Imported by
:mod:`orgchem.db.seed_mechanisms`.
"""
from __future__ import annotations

from orgchem.core.mechanism import Arrow, Mechanism, MechanismStep


def _fischer_esterification() -> Mechanism:
    """Acid-catalysed ester synthesis: AcOH + EtOH → EtOAc + H₂O."""
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
            smiles="CC(=O)O.[H+]",
            arrows=[Arrow(from_atom=2, to_atom=4, kind="curly",
                          label="C=O lone pair → H⁺")],
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
                "acid OHs.  The net effect is to give the "
                "tetrahedral intermediate with a good leaving "
                "group — H₂O."
            ),
            smiles="CC(O)(O)[OH+]CC",
            arrows=[Arrow(from_atom=4, to_atom=2, kind="curly",
                          label="proton hops via solvent")],
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
                "the acid catalyst."
            ),
            smiles="CC(=O)OCC.O",
        ),
    ])


def _nabh4_reduction() -> Mechanism:
    """Single-step hydride transfer from NaBH₄ to acetone."""
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
                "workup.  Net transformation: acetone + H⁻ + H⁺ → "
                "isopropanol."
            ),
            smiles="CC(O)C.[BH3]",
        ),
    ])


def _nitration_benzene() -> Mechanism:
    """EAS — HNO₃ / H₂SO₄ nitrating benzene to nitrobenzene."""
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Generation of the nitronium electrophile",
            description=(
                "H₂SO₄ protonates HNO₃, and the protonated species "
                "loses water to give the nitronium ion NO₂⁺ — the "
                "true electrophile in aromatic nitration."
            ),
            smiles="O=[N+]=O.O",
            arrows=[Arrow(from_atom=0, to_atom=1, kind="curly",
                          label="N=O (electrophile)")],
        ),
        MechanismStep(
            title="Step 2: Benzene attacks NO₂⁺ → arenium ion",
            description=(
                "A π bond of benzene attacks the electrophilic "
                "nitrogen of NO₂⁺. One ring carbon becomes sp³ "
                "(tetrahedral — now carries the incoming NO₂ + an "
                "H); the remaining four π electrons are delocalised "
                "across the other five carbons — the classic "
                "cyclohexadienyl-cation / Wheland intermediate."
            ),
            smiles="c1ccccc1.O=[N+]=O",
            arrows=[Arrow(from_atom=0, to_atom=7, kind="curly",
                          label="ring π → N⁺")],
        ),
        MechanismStep(
            title="Step 3: Rearomatisation by loss of H⁺",
            description=(
                "HSO₄⁻ (or any available base) removes the proton "
                "from the sp³ carbon of the Wheland intermediate. "
                "The two electrons from the C–H bond restore the "
                "ring π system — aromaticity comes back and the "
                "product is nitrobenzene."
            ),
            smiles="c1ccc(cc1)[N+](=O)[O-].OS(=O)(=O)O",
        ),
    ])


def _claisen_condensation() -> Mechanism:
    """2× ethyl acetate + NaOEt → ethyl acetoacetate + EtOH."""
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Ester enolate formation",
            description=(
                "Ethoxide (a base) removes an α-H from ethyl acetate. "
                "The α-pKa is ~25 — higher than ketone α-H (~20) — "
                "so the equilibrium lies against enolate, but the "
                "overall reaction is pulled forward by the very "
                "acidic (pKa ~11) β-keto-ester product in step 4."
            ),
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
                "tetrahedral alkoxide intermediate."
            ),
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
                "(OEt⁻) as the leaving group.  This is the "
                "addition-elimination pattern unique to carboxylic "
                "acid derivatives."
            ),
            smiles="CC(=O)CC(=O)OCC.[O-]CC",
            arrows=[Arrow(from_atom=3, to_atom=1, kind="curly",
                          label="alkoxide collapses to C=O")],
        ),
        MechanismStep(
            title="Step 4: Deprotonation of the β-keto ester",
            description=(
                "The β-keto ester's α-H sits between two carbonyls "
                "and has pKa ≈ 11 — far more acidic than any "
                "starting material. Ethoxide deprotonates it, and "
                "the doubly-stabilised enolate is trapped.  This is "
                "the thermodynamic sink that makes Claisen "
                "condensations viable."
            ),
            smiles="CC(=O)[CH-]C(=O)OCC.CCO",
        ),
    ])


def _pinacol_rearrangement() -> Mechanism:
    """Pinacol (2,3-dimethyl-2,3-butanediol) → pinacolone
    (3,3-dimethyl-2-butanone) via 1,2-methyl shift."""
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Protonation of one hydroxyl",
            description=(
                "Acid catalyst (H₃O⁺) protonates one of the two "
                "hydroxyls.  The product — a hydroxyl-oxonium — is "
                "now primed to lose water as a neutral leaving "
                "group."
            ),
            smiles="CC(C)(O)C(C)(C)O.[H+]",
            arrows=[Arrow(from_atom=3, to_atom=7, kind="curly",
                          label="OH lone pair → H⁺")],
            lone_pairs=[3, 8],
        ),
        MechanismStep(
            title="Step 2: Loss of water → tertiary carbocation",
            description=(
                "The C–OH₂⁺ bond heterolyses — both bonding "
                "electrons leave with water. The resulting carbon "
                "is a tertiary carbocation (three alkyl substituents)."
            ),
            smiles="CC(C)(O)C(C)(C)[OH2+]",
            arrows=[Arrow(from_atom=4, to_atom=7, kind="curly",
                          label="C–O bond → OH₂⁺ leaves")],
        ),
        MechanismStep(
            title="Step 3: 1,2-methyl migration",
            description=(
                "A methyl group from the adjacent sp³ carbon (which "
                "still carries the OH) migrates to the cation with "
                "its bonding electrons. The migration target is "
                "better stabilised — the new carbocation is "
                "resonance-stabilised by the adjacent OH "
                "(oxocarbenium character)."
            ),
            smiles="CC(O)(C)[C+](C)C",
            arrows=[Arrow(from_atom=3, to_atom=4, kind="curly",
                          label="C–Me bond → migrates")],
            lone_pairs=[2],
        ),
        MechanismStep(
            title="Step 4: Deprotonation → ketone (pinacolone)",
            description=(
                "The oxocarbenium loses the O–H proton to water "
                "(or any base in solution), giving the neutral "
                "C=O ketone — pinacolone. The C=O bond is "
                "~80 kJ/mol stronger than the equivalent C⁺–O "
                "single + O–H bonds combined."
            ),
            smiles="CC(=O)C(C)(C)C.O",
        ),
    ])


def _bromination_ethene() -> Mechanism:
    """Anti addition of Br₂ to ethene via a bromonium ion.

    Classic example of electrophilic addition going through a
    bridged halonium — the stereochemistry signature (anti,
    trans-1,2-dihalide) is the textbook fingerprint.
    """
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: Bromonium ion formation",
            description=(
                "The π electrons of the C=C bond polarise the Br–Br "
                "bond as they approach.  The alkene π pair attacks "
                "one Br; simultaneously the Br–Br σ bond heterolyses, "
                "pushing Br⁻ off as the leaving group.  The departing "
                "Br⁺ does NOT form an open carbocation — its lone pair "
                "forms a second C–Br bond on the back face, giving a "
                "3-membered bromonium ion."
            ),
            smiles="C=C.BrBr",   # 0,1 = C; 2,3 = Br-Br
            arrows=[
                Arrow(from_atom=0, to_atom=2, kind="curly",
                      label="π → Br"),
                Arrow(from_atom=2, to_atom=3, kind="curly",
                      label="Br–Br → Br⁻"),
            ],
        ),
        MechanismStep(
            title="Step 2: Backside attack by Br⁻ opens the ring",
            description=(
                "Br⁻ attacks one of the bromonium carbons from the "
                "face opposite the bridging Br⁺ — an SN2-like step "
                "at carbon.  The C–Br⁺ bond on that carbon breaks "
                "heterolytically, returning Br to its neutral form "
                "on the other carbon.  Because attack is backside, "
                "the two Br atoms end up on opposite faces — this "
                "is why alkene halogenation gives the anti (trans) "
                "dihalide stereospecifically."
            ),
            smiles="[Br+]1CC1.[Br-]",   # 0=Br+, 1,2=C, 3=Br-
            arrows=[
                Arrow(from_atom=3, to_atom=1, kind="curly",
                      label="Br⁻ → C"),
                Arrow(from_atom=1, to_atom=0, kind="curly",
                      label="C–Br⁺ → Br"),
            ],
            lone_pairs=[3],
        ),
        MechanismStep(
            title="Product: 1,2-dibromoethane (anti addition)",
            description=(
                "The product is vicinal dibromide (1,2-dibromo-"
                "ethane).  For acyclic substrates the two stereo-"
                "centres come out anti (trans), which for a "
                "symmetric alkene like ethene is invisible — but "
                "for cyclohexene the anti-addition signature is "
                "the trans-1,2-dibromocyclohexane product."
            ),
            smiles="BrCCBr",
        ),
    ])


def _friedel_crafts_alkylation() -> Mechanism:
    """CH₃Cl + benzene + AlCl₃ → toluene + HCl + AlCl₃ (catalyst)."""
    return Mechanism(steps=[
        MechanismStep(
            title="Step 1: AlCl₃ activates the alkyl halide",
            description=(
                "AlCl₃ is a Lewis acid — an empty p-orbital on Al "
                "accepts a lone pair from Cl of CH₃Cl. The C–Cl "
                "bond lengthens as it feels the pull of AlCl₄⁻, "
                "ultimately heterolysing to give a CH₃⁺ ion pair "
                "(tight in solution, drawn here as discrete cation "
                "+ AlCl₄⁻ for clarity)."
            ),
            smiles="CCl.[Al](Cl)(Cl)Cl",   # 0=C, 1=Cl, 2=Al, 3/4/5=Cl
            arrows=[
                Arrow(from_atom=1, to_atom=2, kind="curly",
                      label="Cl lone pair → Al"),
                Arrow(from_atom=0, to_atom=1, kind="curly",
                      label="C–Cl → Cl"),
            ],
            lone_pairs=[1],
        ),
        MechanismStep(
            title="Step 2: Benzene attacks CH₃⁺ → Wheland intermediate",
            description=(
                "A π bond of benzene attacks the methyl cation.  One "
                "ring carbon becomes sp³ (now bears the new methyl + "
                "the original H); the remaining four π electrons "
                "delocalise over the other five carbons — the classic "
                "cyclohexadienyl / arenium / Wheland intermediate. "
                "Aromaticity is temporarily lost (~150 kJ/mol "
                "penalty)."
            ),
            smiles="c1ccccc1.[CH3+]",   # 0..5 = benzene, 6 = CH3+
            arrows=[Arrow(from_atom=0, to_atom=6, kind="curly",
                          label="ring π → CH₃⁺")],
        ),
        MechanismStep(
            title="Step 3: Rearomatisation — AlCl₄⁻ takes the H⁺",
            description=(
                "AlCl₄⁻ (or any weak base present) removes the proton "
                "from the sp³ carbon of the Wheland intermediate. "
                "The C–H bonding electrons restore the ring π system "
                "— aromaticity comes back and toluene is released. "
                "HCl + AlCl₃ come out as byproducts, the catalyst is "
                "regenerated, and the overall reaction is driven "
                "forward by the re-aromatisation."
            ),
            smiles="Cc1ccccc1.Cl.[Al](Cl)(Cl)Cl",
        ),
    ])


BUILDERS = {
    "Fischer esterification":   _fischer_esterification,
    "NaBH4 reduction":          _nabh4_reduction,
    "Nitration of benzene":     _nitration_benzene,
    "Claisen condensation":     _claisen_condensation,
    "Pinacol rearrangement":    _pinacol_rearrangement,
    "Bromination of ethene":    _bromination_ethene,
    "Friedel-Crafts alkylation": _friedel_crafts_alkylation,
}
