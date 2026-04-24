"""Seed the Reactions table with 15 textbook named reactions.

Each entry is a tuple of (name, category, description, reaction SMILES).
The SMILES strings are simple canonical forms — good enough for RDKit to
render clean left→right schemes. Atom-mapped SMARTS for mechanism step
playback lives in a separate ``mechanism_json`` column (populated in
Phase 2b).
"""
from __future__ import annotations
import logging
from typing import List, Tuple

from orgchem.db.models import Reaction as DBRxn
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


# (name, category, description, reaction_smiles)
_STARTER: List[Tuple[str, str, str, str]] = [
    # ---- Substitution ----
    ("SN2: methyl bromide + hydroxide",
     "Substitution",
     "Backside attack of hydroxide on methyl bromide. Single step, concerted — "
     "rate depends on both [CH3Br] and [OH⁻]. Inverts stereochemistry at the "
     "carbon.",
     "CBr.[OH-]>>CO.[Br-]"),
    ("SN1: tert-butyl bromide hydrolysis",
     "Substitution",
     "Stepwise: ionisation to a tertiary carbocation, then water capture. "
     "Rate depends only on the substrate; gives racemic product at a chiral "
     "centre.",
     "CC(C)(C)Br.O>>CC(C)(C)O.[H]Br"),

    # ---- Elimination ----
    ("E2: 2-bromobutane + hydroxide",
     "Elimination",
     "Concerted anti-periplanar loss of H⁺ and Br⁻, giving the more "
     "substituted (Zaitsev) alkene.",
     "CCC(Br)C.[OH-]>>CC=CC.[Br-].O"),
    ("E1: tert-butyl bromide in ethanol",
     "Elimination",
     "Carbocation forms first (slow), then β-H is removed (fast). Competes "
     "with SN1 under the same conditions.",
     "CC(C)(C)Br>>C=C(C)C.[H]Br"),

    # ---- Addition to alkenes ----
    ("Bromination of ethene",
     "Addition",
     "Electrophilic anti-addition of Br₂ across the π bond, via a bromonium "
     "ion intermediate.",
     "C=C.BrBr>>BrCCBr"),
    ("Catalytic hydrogenation of ethene",
     "Addition",
     "Syn addition of H₂ across a C=C bond on a Pd, Pt, or Ni surface.",
     "C=C.[H][H]>>CC"),

    # ---- Pericyclic ----
    ("Diels-Alder: butadiene + ethene",
     "Pericyclic",
     "[4+2] concerted cycloaddition: a diene and a dienophile form a "
     "cyclohexene ring in one step.",
     "C=CC=C.C=C>>C1=CCCCC1"),

    # ---- Carbonyl additions / condensations ----
    ("Fischer esterification",
     "Substitution (acyl)",
     "Carboxylic acid + alcohol → ester + water. Acid-catalysed, reversible. "
     "Drive to products by excess alcohol or by removing water.",
     "CC(=O)O.CCO>>CC(=O)OCC.O"),
    ("Amide formation (carboxylic acid + amine)",
     "Substitution (acyl)",
     "Direct coupling requires activation (here shown as the overall "
     "transformation); real syntheses use DCC / HATU / acyl chlorides.",
     "CC(=O)O.CN>>CC(=O)NC.O"),
    ("Aldol condensation (acetone self-coupling)",
     "Addition / condensation",
     "Base generates an enolate of acetone; it attacks a second carbonyl, "
     "then dehydrates to the α,β-unsaturated ketone.",
     "CC(=O)C.CC(=O)C>>CC(=CC(=O)C)C.O"),
    ("Grignard addition to acetone",
     "Addition",
     "MeMgBr attacks the electrophilic carbonyl carbon; aqueous workup gives "
     "the tertiary alcohol.",
     "C[Mg]Br.CC(=O)C>>CC(C)(C)O.Br[Mg]O"),

    # ---- Aromatic substitution ----
    ("Friedel-Crafts alkylation of benzene",
     "Electrophilic aromatic substitution",
     "AlCl₃ activates an alkyl halide; the resulting carbocation attacks "
     "benzene. Prone to rearrangements and polyalkylation.",
     "c1ccccc1.CCCl>>CCc1ccccc1.Cl"),
    ("Friedel-Crafts acylation of benzene",
     "Electrophilic aromatic substitution",
     "AlCl₃ activates an acid chloride to the acylium ion, which "
     "substitutes onto benzene giving an aryl ketone (no rearrangement).",
     "c1ccccc1.CC(=O)Cl>>CC(=O)c1ccccc1.Cl"),
    ("Nitration of benzene",
     "Electrophilic aromatic substitution",
     "H₂SO₄ + HNO₃ generates NO₂⁺, which substitutes onto the ring.",
     "c1ccccc1.O=N(=O)O>>O=[N+]([O-])c1ccccc1.O"),

    # ---- Redox ----
    ("PCC oxidation of 2-propanol",
     "Oxidation",
     "Pyridinium chlorochromate cleanly oxidises a secondary alcohol to the "
     "ketone (stops before over-oxidation).",
     "CC(O)C>>CC(=O)C"),
    ("NaBH4 reduction of acetone",
     "Reduction",
     "Hydride delivery from NaBH₄ turns a ketone into a secondary alcohol "
     "(without touching esters or acids).",
     "CC(=O)C>>CC(O)C"),

    # ---- +10 content expansion, Phase 6 (2026-04-22) ----
    ("Wittig reaction (propanal + methylidene ylide)",
     "Addition (olefination)",
     "Phosphorus ylide attacks the carbonyl carbon, forming a betaine that "
     "collapses to an alkene and triphenylphosphine oxide. The E/Z ratio "
     "depends on ylide stabilisation.",
     "CCC=O.[CH2-][P+](c1ccccc1)(c1ccccc1)c1ccccc1"
     ">>CCC=C.O=P(c1ccccc1)(c1ccccc1)c1ccccc1"),
    ("Claisen condensation (ethyl acetate)",
     "Condensation",
     "Enolate of one ester attacks the carbonyl of a second, giving a "
     "β-ketoester (ethyl acetoacetate). Requires a full equivalent of base "
     "because the α-proton of the product is more acidic than the starting ester.",
     "CCOC(=O)C.CCOC(=O)C>>CCOC(=O)CC(=O)C.CCO"),
    ("Cannizzaro reaction (benzaldehyde)",
     "Disproportionation",
     "Aldehydes with no α-H undergo base-catalysed disproportionation: one "
     "is reduced to the alcohol, another oxidised to the carboxylate. "
     "Benzaldehyde is the textbook substrate.",
     "O=Cc1ccccc1.O=Cc1ccccc1.[OH-]"
     ">>OCc1ccccc1.[O-]C(=O)c1ccccc1"),
    ("Michael addition (acetone enolate + methyl vinyl ketone)",
     "Addition (conjugate)",
     "A soft nucleophile (stabilised enolate) adds to the β-carbon of an "
     "α,β-unsaturated carbonyl. Gives 1,4-addition products (Michael adducts) "
     "with high regioselectivity.",
     "CC(=O)C=C.[CH2-]C(=O)C>>CC(=O)CCC(=O)C"),
    ("Baeyer-Villiger oxidation (acetone + peracid)",
     "Oxidation (insertion)",
     "Peracid inserts an oxygen next to the carbonyl, turning a ketone into "
     "an ester. Migratory aptitude: H > 3° > 2°ar > 2° > 1° > CH₃.",
     "CC(=O)C.CC(=O)OO>>CC(=O)OC.CC(=O)O"),
    ("Suzuki coupling (bromobenzene + phenylboronic acid)",
     "Cross-coupling",
     "Pd-catalysed biaryl coupling. ArX + Ar'B(OH)₂ → Ar–Ar'. Mild "
     "conditions, tolerant of most functional groups. One of the most "
     "widely-used reactions in the pharma industry.",
     "Brc1ccccc1.OB(O)c1ccccc1>>c1ccc(-c2ccccc2)cc1.OB(O)O.[Br-]"),
    ("Radical halogenation of methane",
     "Radical (substitution)",
     "hv or heat initiates Cl–Cl homolysis. The Cl• radical abstracts an "
     "H from methane, giving CH₃•, which in turn abstracts Cl from Cl₂. "
     "Poor selectivity; over-chlorination is common.",
     "C.ClCl>>CCl.[H]Cl"),
    ("Hell-Volhard-Zelinsky (propanoic acid α-bromination)",
     "Substitution (acyl α)",
     "PBr₃ (or trace) converts the carboxylic acid to the acyl bromide, which "
     "enolises and brominates. Net: α-H is swapped for Br. Used to make "
     "α-amino acids by subsequent SN2 with ammonia.",
     "CCC(=O)O.BrBr>>CC(Br)C(=O)O.[H]Br"),
    ("Pinacol rearrangement (pinacol → pinacolone)",
     "Rearrangement",
     "Acid protonates one OH, which leaves as water, giving a 3° carbocation. "
     "A methyl migrates with its bonding pair, giving an oxocarbenium, which "
     "loses H⁺ to yield the ketone. Textbook 1,2-shift.",
     "CC(O)(C)C(O)(C)C>>CC(=O)C(C)(C)C.O"),
    ("6π electrocyclic: hexatriene → cyclohexadiene",
     "Pericyclic",
     "Thermal disrotatory closure of a 1,3,5-hexatriene to a cyclohexadiene. "
     "Woodward-Hoffmann rules predict disrotatory for 6-electron thermal "
     "reactions (conrotatory for photochemical).",
     "C=CC=CC=C>>C1=CC=CCC1"),
    # ---- Enzyme chemistry (Phase 16d) ----
    ("Chymotrypsin: peptide bond hydrolysis",
     "Enzyme (catalytic triad)",
     "The classic catalytic triad (Ser-195, His-57, Asp-102) hydrolyses a "
     "peptide bond via an acyl-enzyme intermediate. His acts as a general "
     "base (deprotonates Ser), Ser-OH attacks the peptide C=O, collapsing "
     "to the tetrahedral intermediate; the amine leaves, giving an "
     "acyl-serine. Water then repeats the attack, hydrolysing the "
     "acyl-enzyme back to free enzyme + carboxylic acid. Canonical example "
     "of how nature speeds up amide hydrolysis by ~10⁹×.",
     "CC(=O)NCC(=O)O.O>>CC(=O)O.NCC(=O)O"),
    ("Aldolase class I: DHAP + G3P → F1,6BP",
     "Enzyme (Schiff-base aldol)",
     "Class I fructose-bisphosphate aldolase uses an active-site lysine to "
     "form a Schiff base with dihydroxyacetone phosphate (DHAP); the "
     "resulting enamine attacks glyceraldehyde-3-phosphate (G3P) in an "
     "aldol step. After Schiff-base hydrolysis the product is "
     "fructose-1,6-bisphosphate — central reaction of "
     "glycolysis / gluconeogenesis (reversible in vivo).",
     "OCC(=O)COP(=O)(O)O.O=C[C@@H](O)COP(=O)(O)O"
     ">>OCC(=O)[C@@H](O)[C@H](O)[C@@H](O)COP(=O)(O)O"),
    ("HIV protease: peptide bond hydrolysis",
     "Enzyme (aspartic protease)",
     "HIV-1 protease cleaves Gag / Gag-Pol polyproteins — its inhibition is "
     "the foundation of first-generation antiretrovirals (saquinavir, "
     "ritonavir, etc.). Two catalytic Asp residues (Asp-25 on each monomer, "
     "at the homodimer interface) activate a water molecule that attacks "
     "the scissile peptide carbonyl. This makes HIV protease the canonical "
     "'active site IS the dimer interface' teaching example.",
     "CC(=O)NCC.O>>CC(=O)O.NCC"),

    # ---- Phase 31b content expansion (2026-04-23) ----------------
    ("Buchwald-Hartwig amination (bromobenzene + morpholine)",
     "Cross-coupling (Pd-catalysed)",
     "Pd/phosphine-catalysed C–N bond formation between an aryl "
     "halide and a secondary amine. Tolerant of many functional "
     "groups; widely used in medicinal chemistry to decorate "
     "drug-like scaffolds. Key steps: oxidative addition of ArBr, "
     "amine coordination, deprotonation by base (NaOtBu / Cs₂CO₃), "
     "reductive elimination to deliver Ar-NR₂.",
     "Brc1ccccc1.C1COCCN1>>c1ccc(N2CCOCC2)cc1.[H]Br"),
    ("Sonogashira coupling (iodobenzene + phenylacetylene)",
     "Cross-coupling (Pd/Cu-catalysed)",
     "Pd(0) + Cu(I) dual-catalysed C(sp²)–C(sp) coupling between "
     "an aryl/vinyl halide and a terminal alkyne. The copper "
     "co-catalyst makes an acetylide intermediate that transmetalates "
     "onto Pd; amine base (Et₃N / iPr₂NH) deprotonates the alkyne. "
     "One of the workhorses for building conjugated aryl-alkyne "
     "scaffolds (liquid crystals, OLEDs, drug SAR).",
     "Ic1ccccc1.C#Cc1ccccc1>>c1ccc(C#Cc2ccccc2)cc1.[H]I"),
    ("Mitsunobu reaction (alcohol + carboxylic acid)",
     "Functional-group interconversion",
     "Converts a 1° or 2° alcohol into an ester, ether, or amine "
     "with inversion of configuration. Reagents: PPh₃ + DIAD "
     "(or DEAD). PPh₃ activates the alcohol's OH as an oxyphosphonium, "
     "the acidic pronucleophile (pKa ≤ ~13) is deprotonated by the "
     "hydrazide anion, then SN2 displacement of OPPh₃ delivers the "
     "product. Workhorse for installing oxygen nucleophiles with "
     "stereochemical inversion.",
     "CC(O)C.CC(=O)O>>CC(OC(C)=O)C.O"),
    ("Swern oxidation (1-octanol → octanal)",
     "Oxidation",
     "Mild, chromium-free oxidation of a 1° alcohol to an aldehyde "
     "(or 2° alcohol to a ketone) using DMSO activated by oxalyl "
     "chloride at −78 °C, followed by triethylamine. The activated "
     "DMSO (chloromethyleneketene dimethyl ammonium) forms an "
     "alkoxysulfonium, which is deprotonated at a methyl, ejects "
     "Me₂S, and the resulting alkoxide furnishes the carbonyl. "
     "Does NOT over-oxidise to carboxylic acid — a major advantage "
     "over Jones / KMnO₄.",
     "CCCCCCCCO>>CCCCCCCC=O"),
    ("Horner-Wadsworth-Emmons olefination (benzaldehyde + "
     "triethyl phosphonoacetate)",
     "Olefination",
     "Stabilised phosphonate-carbanion analogue of the Wittig "
     "reaction. Strong preference for the E-alkene (thermodynamic "
     "betaine opens via retro-[2+2] to the trans product). "
     "Phosphate by-product is water-soluble, so workup is cleaner "
     "than Wittig. Use: install α,β-unsaturated esters / ketones / "
     "nitriles from aldehydes.",
     "O=Cc1ccccc1.CCOC(=O)CP(=O)(OCC)OCC"
     ">>CCOC(=O)/C=C/c1ccccc1.O=P(OCC)(OCC)O"),

    ("RNase A: phosphoryl transfer on RNA",
     "Enzyme (phosphodiesterase)",
     "Bovine pancreatic ribonuclease A cleaves RNA in two chemically "
     "distinct steps. His-12 and His-119 act as general acid/base in "
     "concert: step 1 (transphosphorylation) uses the ribose 2'-OH as "
     "the nucleophile — an intramolecular SN2-at-P that ejects the "
     "5'-oxygen of the downstream nucleotide and leaves a 2',3'-cyclic "
     "phosphate. Step 2 (hydrolysis) opens the cyclic phosphate with "
     "water to give a 3'-phosphate terminus. Canonical textbook example "
     "of two-step phosphodiester hydrolysis with general acid/base "
     "catalysis.",
     "OC1COP(=O)(O)OC1.O>>OC1COP(=O)(O)OC1.O"),

    # ---- Phase 31b round 123 — Negishi coupling --------------------
    ("Negishi coupling (bromobenzene + phenylzinc chloride)",
     "Cross-coupling (Pd-catalysed)",
     "Negishi 1977 (Nobel 2010, shared with Suzuki + Heck) — "
     "Pd(0)-catalysed cross-coupling between an aryl / vinyl "
     "halide and an organozinc reagent.  Catalytic cycle: "
     "oxidative addition of Ar-X to Pd(0) → transmetalation "
     "of the aryl group from Zn to Pd (the Zn-halide by-"
     "product `Cl[Zn]Br` picks up the halide) → reductive "
     "elimination to form the Ar-Ar' bond + regenerate Pd(0).  "
     "Distinctive from Suzuki / Sonogashira: the Zn reagent is "
     "milder than a Grignard, tolerant of carbonyl "
     "functionality, and transmetalates cleanly without a "
     "base.  Excellent for C(sp²)-C(sp²) + C(sp²)-C(sp³) + "
     "C(sp³)-C(sp³) couplings.  Workhorse in total-synthesis "
     "+ drug discovery where Pd-tolerant functional groups "
     "rule out Suzuki.",
     "Brc1ccccc1.c1ccc([Zn]Cl)cc1>>c1ccc(-c2ccccc2)cc1.Cl[Zn]Br"),

    # ---- Phase 31b round 121 — Heck reaction -----------------------
    ("Heck reaction (iodobenzene + methyl acrylate)",
     "Cross-coupling (Pd-catalysed)",
     "Heck 1972 (Nobel 2010, shared with Negishi + Suzuki) — "
     "Pd(0)-catalysed C(sp²)–C(sp²) coupling between an aryl / "
     "vinyl halide and an alkene.  Catalytic cycle: oxidative "
     "addition of Ar–I to Pd(0), olefin insertion (syn), "
     "β-hydride elimination to regenerate the C=C (now "
     "conjugated to the aryl group), and HX reductive "
     "elimination off Pd–H.  Unlike Suzuki / Sonogashira there "
     "is **no transmetalation** — the new σ bond forms directly "
     "during olefin insertion.  Rate-determining step is usually "
     "oxidative addition for ArI, β-H elimination for ArBr / "
     "electron-rich substrates.  Net: stereoselective E-product "
     "(trans-methyl cinnamate from iodobenzene + methyl "
     "acrylate, as drawn here).  Ubiquitous in pharma +"
     " materials synthesis; Heck-Matsuda and asymmetric variants "
     "are active research areas.",
     "Ic1ccccc1.C=CC(=O)OC>>COC(=O)/C=C/c1ccccc1.[H]I"),
]


#: Atom-mapped reaction SMARTS for the 3D side-by-side renderer
#: (Phase 2c.1). Indexed by a substring of the reaction name; reactions
#: whose name doesn't match stay NULL in the ``reaction_smarts_mapped``
#: column and the 3D renderer will fall back to rdFMCS when added.
#: Atom-mapped SMARTS for the 3D renderer. Implicit-H counts are written
#: explicitly (``[CH3:N]`` rather than ``[C:N]``) so ``Chem.AddHs`` fills
#: the molecule out to its real geometry — otherwise ``[C:1]`` parses as
#: a 0-H carbon and acetone renders as 3 spheres in a row.
_MAPPED: dict = {
    "SN2: methyl bromide":     "[CH3:1][Br:2].[OH:3]>>[CH3:1][O:3][H].[Br:2]",
    "SN1: tert-butyl":         "[C:1]([CH3:5])([CH3:6])([CH3:7])[Br:2].[OH2:3]"
                               ">>[C:1]([CH3:5])([CH3:6])([CH3:7])[OH:3].[Br:2]",
    "Bromination of ethene":   "[CH2:1]=[CH2:2].[Br:3][Br:4]"
                               ">>[Br:3][CH2:1][CH2:2][Br:4]",
    "Catalytic hydrogenation": "[CH2:1]=[CH2:2].[H:3][H:4]"
                               ">>[CH2:1]([H:3])[CH2:2][H:4]",
    "PCC oxidation":           "[CH3:1][CH:2]([OH:3])[CH3:4]"
                               ">>[CH3:1][C:2](=[O:3])[CH3:4]",
    "NaBH4 reduction":         "[CH3:1][C:2](=[O:3])[CH3:4]"
                               ">>[CH3:1][CH:2]([OH:3])[CH3:4]",
}


def seed_reactions_if_empty() -> int:
    """Additively seed reactions: insert any missing by name, plus backfill
    mapped SMARTS on existing rows that are still NULL. Pre-existing user
    reactions are not touched."""
    with session_scope() as s:
        existing_names = {row.name for row in s.query(DBRxn.name).all()}

    # Insert any starter entries whose name isn't already in the DB.
    to_add = [e for e in _STARTER if e[0] not in existing_names]
    added = 0
    if to_add:
        with session_scope() as s:
            for name, category, description, smiles in to_add:
                s.add(DBRxn(
                    name=name,
                    reaction_smarts=smiles,
                    reaction_smarts_mapped=_lookup_mapped(name),
                    category=category,
                    description=description,
                ))
                added += 1
        log.info("Seeded %d reactions (table size now %d)",
                 added, len(existing_names) + added)
    else:
        log.info("Reactions table has all %d starter entries", len(_STARTER))

    # Backfill / refresh mapped SMARTS: rewrite if current value doesn't
    # match the latest _MAPPED table (handles both NULL and stale-after-
    # upgrade cases).
    patched = 0
    with session_scope() as s:
        for row in s.query(DBRxn).all():
            mapped = _lookup_mapped(row.name)
            if mapped and row.reaction_smarts_mapped != mapped:
                row.reaction_smarts_mapped = mapped
                patched += 1
    if patched:
        log.info("Refreshed mapped SMARTS for %d reactions", patched)
    return added + patched


def _lookup_mapped(reaction_name: str) -> str | None:
    for substr, mapped in _MAPPED.items():
        if substr in reaction_name:
            return mapped
    return None
