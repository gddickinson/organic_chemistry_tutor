"""Seed textbook reaction-coordinate energy profiles — Phase 13b.

Numbers are *pedagogical estimates* in kJ/mol. They reproduce the
qualitative shape of each profile (barrier heights, intermediate-well
depth, net ΔH sign) drawn from canonical textbook sources
(Clayden 2nd ed., Carey & Sundberg 5th ed.). They are **not** intended
for kinetic prediction — a real study needs DFT, not a teaching figure.

Profiles are stored in ``Reaction.energy_profile_json`` with a
``seed_version`` stamp so upgrades roll out without a DB migration.
"""
from __future__ import annotations
import json
import logging
from typing import Callable, Dict

from sqlalchemy import select

from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
from orgchem.db.models import Reaction as DBRxn
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


#: Bump whenever seed data changes. Existing rows with a lower embedded
#: ``seed_version`` are overwritten on next app launch.
SEED_VERSION = 11


# ------------------------------------------------------------------
# Profile definitions — keyed by substring match against reaction name.

def _sn2_profile() -> ReactionEnergyProfile:
    """SN2 methyl bromide + hydroxide: single concerted barrier."""
    return ReactionEnergyProfile(
        title="SN2: hydroxide + methyl bromide",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §15)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="CH₃Br + OH⁻"),
            StationaryPoint(label="TS", energy=95.0, is_ts=True,
                            note="pentacoordinate C"),
            StationaryPoint(label="Products", energy=-65.0,
                            note="CH₃OH + Br⁻"),
        ],
    )


def _sn1_profile() -> ReactionEnergyProfile:
    """SN1 tert-butyl bromide in water: two barriers with a carbocation well."""
    return ReactionEnergyProfile(
        title="SN1: tert-butyl bromide in water",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §15)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="t-BuBr + H₂O"),
            StationaryPoint(label="TS ionisation", energy=105.0, is_ts=True,
                            note="rate-limiting"),
            StationaryPoint(label="Carbocation", energy=70.0,
                            note="t-Bu⁺ + Br⁻"),
            StationaryPoint(label="TS capture", energy=85.0, is_ts=True),
            StationaryPoint(label="Products", energy=-20.0,
                            note="t-BuOH + HBr"),
        ],
    )


def _e1_profile() -> ReactionEnergyProfile:
    """E1 from tert-butyl bromide: ionisation then rapid deprotonation."""
    return ReactionEnergyProfile(
        title="E1: tert-butyl bromide",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Carey-Sundberg 5e §5)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="t-BuBr"),
            StationaryPoint(label="TS ionisation", energy=105.0, is_ts=True,
                            note="rate-limiting"),
            StationaryPoint(label="Carbocation", energy=70.0,
                            note="t-Bu⁺ + Br⁻"),
            StationaryPoint(label="TS deprotonation", energy=80.0, is_ts=True),
            StationaryPoint(label="Products", energy=-10.0,
                            note="isobutylene + HBr"),
        ],
    )


def _diels_alder_profile() -> ReactionEnergyProfile:
    """Concerted Diels-Alder: single aromatic-TS barrier, strongly exothermic."""
    return ReactionEnergyProfile(
        title="Diels-Alder: butadiene + ethylene",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §35)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="butadiene + ethylene"),
            StationaryPoint(label="TS", energy=115.0, is_ts=True,
                            note="concerted, aromatic-like"),
            StationaryPoint(label="Products", energy=-165.0,
                            note="cyclohexene"),
        ],
    )


def _e2_profile() -> ReactionEnergyProfile:
    """E2 elimination: concerted, single TS, mildly exothermic."""
    return ReactionEnergyProfile(
        title="E2: base + 2-bromobutane",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §17)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="2-BrBu + EtO⁻"),
            StationaryPoint(label="TS", energy=80.0, is_ts=True,
                            note="anti-periplanar H–C–C–Br"),
            StationaryPoint(label="Products", energy=-35.0,
                            note="2-butene + EtOH + Br⁻"),
        ],
    )


def _aldol_profile() -> ReactionEnergyProfile:
    """Base-catalysed aldol addition: fast enolate formation + slow addition."""
    return ReactionEnergyProfile(
        title="Aldol addition: acetaldehyde (base-catalysed)",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §26)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="aldehyde + base"),
            StationaryPoint(label="TS enolisation", energy=65.0, is_ts=True,
                            note="α-proton removal"),
            StationaryPoint(label="Enolate", energy=35.0,
                            note="resonance-stabilised"),
            StationaryPoint(label="TS addition", energy=75.0, is_ts=True,
                            note="rate-limiting C–C bond forming"),
            StationaryPoint(label="Alkoxide", energy=5.0,
                            note="β-alkoxy aldehyde"),
            StationaryPoint(label="Products", energy=-10.0,
                            note="β-hydroxy aldehyde + base"),
        ],
    )


def _grignard_profile() -> ReactionEnergyProfile:
    """Grignard addition: strongly exothermic, irreversible, one TS + workup."""
    return ReactionEnergyProfile(
        title="Grignard addition: MeMgBr + acetaldehyde",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §9)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="RMgX + R'CHO"),
            StationaryPoint(label="TS addition", energy=40.0, is_ts=True,
                            note="Mg coordinates O; C–C forms"),
            StationaryPoint(label="Alkoxide", energy=-85.0,
                            note="magnesium alkoxide"),
            StationaryPoint(label="TS protonation", energy=-60.0, is_ts=True,
                            note="aqueous workup"),
            StationaryPoint(label="Products", energy=-140.0,
                            note="2° alcohol"),
        ],
    )


def _wittig_profile() -> ReactionEnergyProfile:
    """Wittig olefination: via betaine + oxaphosphetane intermediates."""
    return ReactionEnergyProfile(
        title="Wittig: ylide + acetaldehyde",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §14)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="Ph₃P=CHR + R'CHO"),
            StationaryPoint(label="TS 1", energy=55.0, is_ts=True,
                            note="C–C forming"),
            StationaryPoint(label="Oxaphosphetane", energy=-20.0,
                            note="4-membered ring intermediate"),
            StationaryPoint(label="TS 2", energy=10.0, is_ts=True,
                            note="fragmentation, C=O forming"),
            StationaryPoint(label="Products", energy=-120.0,
                            note="alkene + Ph₃P=O"),
        ],
    )


def _michael_profile() -> ReactionEnergyProfile:
    """Michael addition: single concerted TS from stabilised carbanion + enone."""
    return ReactionEnergyProfile(
        title="Michael addition: enolate + α,β-unsaturated ketone",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Carey-Sundberg 5e §10)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="stabilised Nu⁻ + enone"),
            StationaryPoint(label="TS", energy=55.0, is_ts=True,
                            note="1,4-addition to β-C"),
            StationaryPoint(label="Enolate", energy=-15.0,
                            note="resonance-stabilised"),
            StationaryPoint(label="Products", energy=-50.0,
                            note="1,5-dicarbonyl"),
        ],
    )


# ---- Phase 31e content expansion (2026-04-23) -----------------------

def _sonogashira_profile() -> ReactionEnergyProfile:
    """Sonogashira catalytic cycle: OA of ArI (RDS) → Cu-acetylide
    transmetalation → reductive elimination. Energies are qualitative
    estimates in the palladium-catalysed regime."""
    return ReactionEnergyProfile(
        title="Sonogashira coupling: Pd(0) / CuI dual catalysis",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Hartwig OTM §18)",
        points=[
            StationaryPoint(label="Ar-I + Pd(0)", energy=0.0,
                            note="plus Cu-acetylide (formed on Cu cycle)"),
            StationaryPoint(label="TS OA", energy=85.0, is_ts=True,
                            note="rate-determining oxidative addition"),
            StationaryPoint(label="Ar-Pd-I", energy=-10.0,
                            note="Pd(II) intermediate"),
            StationaryPoint(label="TS transmetalation", energy=40.0,
                            is_ts=True,
                            note="Cu-C ↔ Pd-C swap"),
            StationaryPoint(label="Ar-Pd-C≡C-Ar'", energy=-35.0,
                            note="diaryl Pd(II) complex"),
            StationaryPoint(label="TS red. elim.", energy=15.0,
                            is_ts=True,
                            note="C(sp²)–C(sp) bond forms"),
            StationaryPoint(label="Ar-C≡C-Ar' + Pd(0)", energy=-130.0,
                            note="product + regenerated catalyst"),
        ],
    )


def _hwe_profile() -> ReactionEnergyProfile:
    """Horner-Wadsworth-Emmons: stabilised carbanion + aldehyde → E-alkene.
    Oxaphosphetane collapse via retro-[2+2] is the selectivity-setting step."""
    return ReactionEnergyProfile(
        title="Horner-Wadsworth-Emmons: β-ketoester phosphonate + aldehyde",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §27)",
        points=[
            StationaryPoint(label="Reactants + base", energy=0.0,
                            note="phosphonate, aldehyde, NaH"),
            StationaryPoint(label="Phosphonate carbanion", energy=-25.0,
                            note="resonance-stabilised"),
            StationaryPoint(label="TS C-C bond", energy=30.0, is_ts=True,
                            note="carbanion attacks C=O"),
            StationaryPoint(label="Betaine / oxaphosphetane",
                            energy=-15.0,
                            note="4-membered P–C–C–O ring"),
            StationaryPoint(label="TS retro-[2+2]", energy=10.0,
                            is_ts=True,
                            note="E-selective fragmentation"),
            StationaryPoint(label="E-alkene + phosphate", energy=-120.0,
                            note="thermodynamic sink (P=O strength)"),
        ],
    )


def _claisen_profile() -> ReactionEnergyProfile:
    """Claisen condensation (two esters + ethoxide): pedagogically
    the classic case where the **final** step — deprotonation of
    the doubly α-acidic β-ketoester proton (pKa ≈ 11) by alkoxide
    (pKa ≈ 17) — drives an otherwise marginal equilibrium.
    Without that last step, net ΔG is roughly zero; with it, the
    stabilised β-ketoester enolate sits well downhill."""
    return ReactionEnergyProfile(
        title="Claisen condensation: ethyl acetate + NaOEt",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §26; Carey-Sundberg 5e §7)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="2 EtOAc + NaOEt"),
            StationaryPoint(label="TS enolisation", energy=50.0,
                            is_ts=True,
                            note="α-H removal by EtO⁻; unfavourable"),
            StationaryPoint(label="Ester enolate", energy=30.0,
                            note="+ EtOH; endergonic intermediate"),
            StationaryPoint(label="TS C–C addition", energy=70.0,
                            is_ts=True,
                            note="rate-limiting attack on 2nd ester C=O"),
            StationaryPoint(label="Tetrahedral alkoxide", energy=10.0,
                            note="sp³ at former carbonyl C"),
            StationaryPoint(label="TS alkoxide collapse",
                            energy=35.0, is_ts=True,
                            note="EtO⁻ departs; C=O re-forms"),
            StationaryPoint(label="Neutral β-ketoester",
                            energy=-5.0,
                            note="ΔG near zero — equilibrium would "
                                 "sit here without step 4"),
            StationaryPoint(label="TS final deprotonation",
                            energy=15.0, is_ts=True,
                            note="EtO⁻ removes α-H between two C=O "
                                 "(pKa ≈ 11)"),
            StationaryPoint(label="Products", energy=-40.0,
                            note="doubly-stabilised β-ketoester "
                                 "enolate + EtOH — the step that "
                                 "DRIVES the Claisen"),
        ],
    )


def _nabh4_profile() -> ReactionEnergyProfile:
    """NaBH₄ reduction of a ketone (acetone → 2-propanol): the
    simplest irreversible addition shape in the catalogue.
    Hydride transfer from B–H to the carbonyl C is the only
    TS; a stabilised alkoxide intermediate follows; aqueous
    workup is a trivial proton grab.  The teaching point is
    that the reaction is kinetically demanding (Ea ~55 kJ/mol)
    but strongly exergonic downstream — the alkoxide sits
    ~80 kJ/mol below the reactants because C–O(R) + B–H is
    far more stable than C=O + B–H was."""
    return ReactionEnergyProfile(
        title="NaBH₄ reduction: acetone → 2-propanol",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §6; Brown 1972 "
               "*Organic Syntheses via Boranes*)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="acetone + NaBH₄ in MeOH"),
            StationaryPoint(label="TS hydride transfer",
                            energy=55.0, is_ts=True,
                            note="B–H···C=O alignment; 4-centre "
                                 "TS with partial B-O bond"),
            StationaryPoint(label="Borate alkoxide",
                            energy=-80.0,
                            note="R₂CHO-BH₃⁻ Na⁺; further hydride "
                                 "transfers possible (NaBH₄ can do "
                                 "4 reductions per equivalent)"),
            StationaryPoint(label="TS workup", energy=-65.0,
                            is_ts=True,
                            note="aqueous proton grab; low barrier"),
            StationaryPoint(label="Products", energy=-115.0,
                            note="2-propanol + B(OH)₃ + NaOH"),
        ],
    )


def _friedel_crafts_profile() -> ReactionEnergyProfile:
    """Friedel-Crafts alkylation (benzene + CH₃Cl / AlCl₃):
    second EAS profile in the catalogue, pairs with the
    round-101 nitration curve.  Distinctive from nitration:
    an **extra pre-equilibrium TS** for alkyl-cation
    generation (AlCl₃ pulls Cl⁻ from CH₃Cl) before the
    standard Wheland-intermediate cycle.  The free methyl
    cation is genuinely unstable — +25 kJ/mol above reactants
    — which is *why* FC alkylation suffers from rearrangement
    (1° → 2° / 3° via H-shift) and from poly-alkylation (the
    alkylated product is more reactive than benzene itself).
    Nitronium, by contrast, is a stable / isolable cation
    and doesn't rearrange."""
    return ReactionEnergyProfile(
        title="Friedel-Crafts alkylation: benzene + CH₃Cl / AlCl₃",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §22; Olah 1964 "
               "*JACS* 86:1039 — superacid C⁺ characterisation)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="benzene + CH₃Cl + AlCl₃ "
                                 "(Lewis-acid catalyst)"),
            StationaryPoint(label="TS cation generation",
                            energy=60.0, is_ts=True,
                            note="AlCl₃ abstracts Cl⁻ from CH₃Cl; "
                                 "ion pair forming"),
            StationaryPoint(label="Methyl cation + AlCl₄⁻",
                            energy=25.0,
                            note="unstable 1° C⁺ — rearranges to "
                                 "more stable cations if possible; "
                                 "this is why FC fails for 1° RX"),
            StationaryPoint(label="TS EAS attack",
                            energy=70.0, is_ts=True,
                            note="rate-limiting CH₃⁺ attack on "
                                 "benzene π-electrons; commits to "
                                 "Wheland formation"),
            StationaryPoint(label="Wheland (arenium) intermediate",
                            energy=30.0,
                            note="sp³ C–CH₃ + H; positive charge "
                                 "delocalised over 5 ring carbons"),
            StationaryPoint(label="TS deprotonation",
                            energy=45.0, is_ts=True,
                            note="AlCl₄⁻ grabs sp³ proton; "
                                 "aromaticity restored"),
            StationaryPoint(label="Products", energy=-20.0,
                            note="toluene + HCl + regenerated "
                                 "AlCl₃; net mildly exergonic — but "
                                 "toluene is *more* nucleophilic than "
                                 "benzene → poly-alkylation"),
        ],
    )


def _chymotrypsin_profile() -> ReactionEnergyProfile:
    """Chymotrypsin peptide-bond hydrolysis: the first **enzyme
    catalytic mechanism** profile in the catalogue.  The shape
    is distinctive — two tetrahedral intermediates bracketing a
    covalent **acyl-enzyme** well that no solution-phase profile
    shows.  Catalytic triad (Ser195-His57-Asp102) + oxyanion
    hole lower both tetrahedral-intermediate energies; covalent
    catalysis splits one 20-kcal/mol solution barrier into two
    10-kcal/mol enzyme barriers (kcat/Km enhancement ≈ 10¹⁰).
    The "double hump" is the teaching point."""
    return ReactionEnergyProfile(
        title="Chymotrypsin: catalytic triad peptide hydrolysis",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Fersht 1999 §13; Hedstrom "
               "2002 *Chem. Rev.* 102:4501)",
        points=[
            StationaryPoint(label="Michaelis complex", energy=0.0,
                            note="E·S; substrate bound in S1 pocket; "
                                 "Ser-195 primed by H-bond to His-57"),
            StationaryPoint(label="TS acylation",
                            energy=65.0, is_ts=True,
                            note="Ser-O attacks scissile C=O; "
                                 "His-57 acts as general base; "
                                 "oxyanion developing"),
            StationaryPoint(label="Tetrahedral intermediate 1",
                            energy=25.0,
                            note="sp³ alkoxide stabilised by "
                                 "oxyanion-hole H-bonds (Gly-193, "
                                 "Ser-195 backbone NH)"),
            StationaryPoint(label="TS amine leaves",
                            energy=40.0, is_ts=True,
                            note="collapse of T1; His-57 protonates "
                                 "departing amine"),
            StationaryPoint(label="Acyl-enzyme intermediate",
                            energy=-15.0,
                            note="covalent Ser195-O-C(=O)-R; peptide "
                                 "C-terminal half has diffused away; "
                                 "real isolable intermediate"),
            StationaryPoint(label="TS deacylation",
                            energy=50.0, is_ts=True,
                            note="water attacks acyl-enzyme; "
                                 "His-57 now deprotonates water"),
            StationaryPoint(label="Tetrahedral intermediate 2",
                            energy=15.0,
                            note="mirror of T1; oxyanion-hole again "
                                 "stabilising"),
            StationaryPoint(label="TS Ser-O leaves",
                            energy=30.0, is_ts=True,
                            note="collapse; carboxylic acid forms; "
                                 "Ser-OH regenerated"),
            StationaryPoint(label="E + 2 products",
                            energy=-80.0,
                            note="free enzyme + both peptide halves; "
                                 "strongly exergonic"),
        ],
    )


def _pinacol_profile() -> ReactionEnergyProfile:
    """Pinacol rearrangement (pinacol → pinacolone, H⁺-cat.):
    the textbook **1,2-methyl-shift** profile.  The pedagogical
    point is that the migration TS is *lower* than the ionisation
    TS (rate-determining), and the post-shift oxocarbenium is
    *more* stable than the pre-shift tertiary carbocation because
    the oxygen lone pair donates into the empty p-orbital.
    The shape — "carbocation high, oxocarbenium low" — is why
    1,2-shifts run forward to the ketone, not backward to the
    diol."""
    return ReactionEnergyProfile(
        title="Pinacol rearrangement: pinacol → pinacolone (H⁺-cat.)",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §37; Carey-Sundberg "
               "5e §10)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="pinacol + H⁺ (aqueous)"),
            StationaryPoint(label="TS ionisation", energy=100.0,
                            is_ts=True,
                            note="rate-limiting; H₂O leaves as "
                                 "C–O bond breaks"),
            StationaryPoint(label="Tertiary carbocation",
                            energy=40.0,
                            note="R₃C⁺; β-hydroxyl still present"),
            StationaryPoint(label="TS 1,2-methyl shift",
                            energy=50.0, is_ts=True,
                            note="migratory aptitude: alkyl > H; "
                                 "hyperconjugation assists"),
            StationaryPoint(label="Protonated ketone",
                            energy=-20.0,
                            note="oxocarbenium C=O⁺–H; O lone pair "
                                 "stabilises the cation — more "
                                 "stable than the tertiary C⁺"),
            StationaryPoint(label="TS deprotonation",
                            energy=-10.0, is_ts=True,
                            note="water grabs sp² proton; fast"),
            StationaryPoint(label="Products", energy=-70.0,
                            note="pinacolone + H₃O⁺; overall "
                                 "dehydration is exergonic"),
        ],
    )


def _bromination_ethene_profile() -> ReactionEnergyProfile:
    """Bromination of an alkene (ethene + Br₂ → 1,2-dibromoethane):
    the canonical **bromonium-valley anti-addition** shape that
    explains trans-diaxial stereochemistry.  Step 1 (π-electrons
    attack Br–Br; Br⁻ kicked out) is rate-limiting.  The 3-membered
    bromonium intermediate sits in a real, resonance-stabilised
    valley — deeper than a classical carbocation would be — which
    is *why* Br⁻ attacks from the opposite face (backside SN2-like
    opening) instead of recombining with the now-adjacent bromonium.
    The anti-addition outcome falls out of the shape.
    Teaching complement to the Phase-14b halohydrin formation
    glossary entry + Phase 31c round-62 mechanism JSON."""
    return ReactionEnergyProfile(
        title="Bromination: ethene + Br₂ → 1,2-dibromoethane",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §20; Carey-Sundberg "
               "5e §4)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="ethene (π-HOMO) + Br₂ (σ*-LUMO)"),
            StationaryPoint(label="TS bromonium",
                            energy=80.0, is_ts=True,
                            note="rate-limiting; π-attack + "
                                 "Br-Br heterolysis concerted"),
            StationaryPoint(label="Bromonium ion",
                            energy=40.0,
                            note="3-membered cyclic Br⁺; partial "
                                 "positive charge on both carbons; "
                                 "free Br⁻ outside"),
            StationaryPoint(label="TS anti-attack",
                            energy=50.0, is_ts=True,
                            note="Br⁻ SN2-opens bromonium from "
                                 "opposite face → trans-product"),
            StationaryPoint(label="Products",
                            energy=-100.0,
                            note="anti-1,2-dibromoethane (meso for "
                                 "substituted alkenes)"),
        ],
    )


def _nitration_benzene_profile() -> ReactionEnergyProfile:
    """Nitration of benzene by NO₂⁺ (from HNO₃ / H₂SO₄): the
    canonical **electrophilic aromatic substitution** shape —
    a high first barrier (electrophile attack = RDS) drops
    into a shallow **Wheland (arenium) valley** that's
    resonance-stabilised but still ~45 kJ/mol above the
    reactants, then a *low* second barrier for deprotonation
    (the solvent base grabs the sp³ proton) followed by a
    strongly exothermic re-aromatisation to the product.
    The shallow valley is the textbook point — the arenium
    intermediate is real but fleeting, and the rate-limiting
    step is always the first attack, not the second."""
    return ReactionEnergyProfile(
        title="Nitration of benzene: NO₂⁺ + C₆H₆",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §22; Carey-Sundberg 5e §11)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="benzene + NO₂⁺ (from HNO₃/H₂SO₄)"),
            StationaryPoint(label="TS addition", energy=90.0,
                            is_ts=True,
                            note="rate-limiting NO₂⁺ attack; π-bond"
                                 " commits to σ-bond formation"),
            StationaryPoint(label="Wheland (arenium)",
                            energy=45.0,
                            note="sp³ C bearing NO₂ + H; positive "
                                 "charge delocalised across 5 ring "
                                 "carbons — resonance-stabilised "
                                 "but non-aromatic"),
            StationaryPoint(label="TS deprotonation",
                            energy=55.0, is_ts=True,
                            note="HSO₄⁻ removes sp³ proton; low "
                                 "barrier — aromaticity restored "
                                 "in the product"),
            StationaryPoint(label="Products", energy=-25.0,
                            note="nitrobenzene + H⁺ (→ H₂SO₄); "
                                 "net exergonic by re-aromatisation"),
        ],
    )


def _fischer_profile() -> ReactionEnergyProfile:
    """Fischer esterification (carboxylic acid + alcohol, H⁺-cat.):
    the textbook **thermoneutral equilibrium** — net ΔG ≈ 0, so
    the reaction is driven by Le Chatelier (excess alcohol or
    Dean-Stark water removal), not by thermodynamics.  Three
    minima + two TSs capture the shape: reactants near zero,
    tetrahedral intermediate ~20 kJ/mol uphill, products ~5
    kJ/mol uphill — a shallow roller-coaster with K≈3 rather
    than a deep well."""
    return ReactionEnergyProfile(
        title="Fischer esterification: RCOOH + R'OH (H⁺-catalysed)",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §12; March 7e §16-64)",
        points=[
            StationaryPoint(label="Reactants", energy=0.0,
                            note="RCOOH + R'OH + H⁺ (cat.)"),
            StationaryPoint(label="TS addition", energy=55.0,
                            is_ts=True,
                            note="rate-limiting R'OH attack on "
                                 "protonated C=O"),
            StationaryPoint(label="Tetrahedral intermediate",
                            energy=20.0,
                            note="protonated sp³-carbon with OR' + OH"),
            StationaryPoint(label="TS collapse", energy=35.0,
                            is_ts=True,
                            note="H₂O leaves after proton shuffle"),
            StationaryPoint(label="Products", energy=5.0,
                            note="ester + H₂O — ΔG ≈ 0, so K ≈ 3; "
                                 "drive with excess ROH or "
                                 "Dean-Stark water removal"),
        ],
    )


def _mitsunobu_profile() -> ReactionEnergyProfile:
    """Mitsunobu reaction: PPh₃ + DIAD activates the alcohol; SN2 on
    oxyphosphonium inverts configuration. Driving force is P=O
    formation (≈ 580 kJ/mol bond-strength bonus)."""
    return ReactionEnergyProfile(
        title="Mitsunobu: PPh₃ / DIAD esterification with inversion",
        energy_unit="kJ/mol",
        source="pedagogical estimate (Clayden 2e §17)",
        points=[
            StationaryPoint(label="ROH + PPh₃ + DIAD",
                            energy=0.0,
                            note="plus acidic pronucleophile"),
            StationaryPoint(label="Betaine (PPh₃-DIAD adduct)",
                            energy=-15.0,
                            note="hydrazide dianion + P(V) cation"),
            StationaryPoint(label="Alkoxyphosphonium RO-PPh₃⁺",
                            energy=-30.0,
                            note="alcohol activated; Nu⁻ now free"),
            StationaryPoint(label="TS SN2 inversion", energy=55.0,
                            is_ts=True,
                            note="backside attack displaces O-PPh₃"),
            StationaryPoint(label="Products: R′-Nu + O=PPh₃",
                            energy=-115.0,
                            note="inverted at C; driven by P=O"),
        ],
    )


_PROFILE_MAP: Dict[str, Callable[[], ReactionEnergyProfile]] = {
    "SN2: methyl bromide":  _sn2_profile,
    "SN1: tert-butyl":      _sn1_profile,
    "E1: tert-butyl":       _e1_profile,
    "E2: 2-bromobutane":    _e2_profile,
    "Diels-Alder":          _diels_alder_profile,
    "Aldol condensation":   _aldol_profile,
    "Grignard addition":    _grignard_profile,
    "Wittig reaction":      _wittig_profile,
    "Michael addition":     _michael_profile,
    "Sonogashira coupling": _sonogashira_profile,
    "Horner-Wadsworth":     _hwe_profile,
    "Mitsunobu":            _mitsunobu_profile,
    "Claisen condensation": _claisen_profile,
    "Fischer esterification": _fischer_profile,
    "Nitration of benzene": _nitration_benzene_profile,
    "NaBH4 reduction": _nabh4_profile,
    "Bromination of ethene": _bromination_ethene_profile,
    "Pinacol rearrangement": _pinacol_profile,
    "Chymotrypsin":          _chymotrypsin_profile,
    "Friedel-Crafts alkylation": _friedel_crafts_profile,
}


def seed_energy_profiles_if_empty(force: bool = False) -> int:
    """Attach energy-profile JSON to reactions with a matching name substring.

    Idempotent: rows whose stored JSON has a ``seed_version`` at least as new
    as :data:`SEED_VERSION` are left alone. Pass ``force=True`` to rewrite
    unconditionally.
    """
    updated = 0
    with session_scope() as s:
        for name_substr, builder in _PROFILE_MAP.items():
            stmt = select(DBRxn).where(DBRxn.name.like(f"%{name_substr}%"))
            for row in s.scalars(stmt):
                if row.energy_profile_json and not force:
                    try:
                        existing = json.loads(row.energy_profile_json)
                    except Exception:
                        existing = {}
                    if existing.get("seed_version", 0) >= SEED_VERSION:
                        continue
                prof = builder()
                prof.reaction_id = row.id
                payload = prof.to_dict()
                payload["seed_version"] = SEED_VERSION
                row.energy_profile_json = json.dumps(payload, indent=2)
                updated += 1
    log.info("Seeded %d energy profiles (version %d)", updated, SEED_VERSION)
    return updated
