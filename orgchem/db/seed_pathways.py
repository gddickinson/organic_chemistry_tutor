"""Seed the Synthesis Pathways tables with 6 classic textbook syntheses.

Each pathway is a tuple of (name, target_name, target_smiles, description,
category, source, steps). Each step is a dict with reaction_smiles and
(optionally) reagents / conditions / yield_pct / notes.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Tuple

from orgchem.db.models import SynthesisPathway, SynthesisStep
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


# (name, target_name, target_smiles, description, category, source, [steps])
_STARTER: List[Tuple[str, str, str, str, str, str, List[Dict[str, Any]]]] = [
    (
        "Wöhler urea synthesis (1828)",
        "Urea",
        "NC(=O)N",
        "The reaction that dissolved the vitalism doctrine — Friedrich Wöhler "
        "showed that an organic compound (urea) could be made from inorganic "
        "starting materials (silver cyanate + ammonium chloride). Triggered by "
        "gentle heating; the reactive species is ammonium cyanate, which "
        "isomerises spontaneously to urea.",
        "Historic",
        "Wöhler, F. (1828) Ann. Phys. Chem. 12, 253.",
        [
            {"reaction_smiles": "[Ag+].[O-]C#N.[NH4+].[Cl-]>>NC(=O)N.[Ag+].[Cl-]",
             "reagents": "heat",
             "conditions": "aqueous, gentle warming",
             "notes": "Via ammonium cyanate [NH4+][NCO-]. The cyanate oxygen "
                      "attacks an ammonium proton, then tautomerises.",
             "yield_pct": None},
        ],
    ),

    (
        "Aspirin (acetylsalicylic acid)",
        "Aspirin",
        "CC(=O)Oc1ccccc1C(=O)O",
        "Classic industrial acetylation — salicylic acid's phenol oxygen is "
        "acylated by acetic anhydride. Trace sulfuric acid catalyses the "
        "addition-elimination sequence at the anhydride carbonyl.",
        "Industrial",
        "Hoffmann / Bayer, 1897.",
        [
            {"reaction_smiles": "OC(=O)c1ccccc1O.CC(=O)OC(=O)C"
                                ">>CC(=O)Oc1ccccc1C(=O)O.CC(=O)O",
             "reagents": "Ac₂O, cat. H₂SO₄",
             "conditions": "85 °C, ~15 min",
             "yield_pct": 85.0,
             "notes": "Phenol oxygen of salicylic acid attacks acetic "
                      "anhydride; acetate leaves. By-product: acetic acid."},
        ],
    ),

    (
        "Paracetamol (acetaminophen)",
        "Acetaminophen",
        "CC(=O)Nc1ccc(O)cc1",
        "Industrial synthesis — p-aminophenol is selectively N-acetylated "
        "(amine is more nucleophilic than phenol) by acetic anhydride in "
        "aqueous conditions.",
        "Industrial",
        "Morse, H.N. (1878) Ber. 11, 232. Commercialised mid-20th century.",
        [
            {"reaction_smiles": "Nc1ccc(O)cc1.CC(=O)OC(=O)C"
                                ">>CC(=O)Nc1ccc(O)cc1.CC(=O)O",
             "reagents": "Ac₂O",
             "conditions": "H₂O, 80 °C",
             "yield_pct": 90.0,
             "notes": "N-acetylation is selective because the aromatic "
                      "amine is a better nucleophile than the phenol."},
        ],
    ),

    (
        "Ibuprofen — BHC green-chemistry process",
        "Ibuprofen",
        "CC(C(=O)O)c1ccc(CC(C)C)cc1",
        "The BHC (Boots-Hoechst-Celanese) process is a 3-step synthesis "
        "that replaced the 6-step Boots route in 1991. 99 % atom "
        "efficiency and recyclable HF catalyst — it won the 1997 "
        "Presidential Green Chemistry Challenge Award.",
        "Green chemistry",
        "BHC Co. (1991). Presidential Green Chemistry Award, 1997.",
        [
            {"reaction_smiles": "CC(C)Cc1ccccc1.CC(=O)OC(=O)C"
                                ">>CC(=O)c1ccc(CC(C)C)cc1.CC(=O)O",
             "reagents": "Ac₂O, HF (catalyst)",
             "conditions": "liquid HF, 20 °C",
             "notes": "Step 1: Friedel-Crafts acylation. Para selectivity "
                      "from the isobutyl ortho/para-director."},
            {"reaction_smiles": "CC(=O)c1ccc(CC(C)C)cc1.[H][H]"
                                ">>CC(O)c1ccc(CC(C)C)cc1",
             "reagents": "H₂, Raney Ni",
             "conditions": "50 bar, 80 °C",
             "notes": "Step 2: catalytic reduction of the aryl ketone to "
                      "the secondary alcohol."},
            {"reaction_smiles": "CC(O)c1ccc(CC(C)C)cc1.[C]=O"
                                ">>CC(C(=O)O)c1ccc(CC(C)C)cc1",
             "reagents": "CO, Pd catalyst",
             "conditions": "140 °C, 35 bar",
             "notes": "Step 3: carbonylation replaces the OH with CO₂H, "
                      "giving the α-methyl arylacetic acid directly."},
        ],
    ),

    (
        "Caffeine by N-methylation of theobromine",
        "Caffeine",
        "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
        "Commercial preparation from theobromine (a natural product from "
        "cacao). The remaining N1–H is selectively methylated by MeI "
        "under mild base. Historically also done by exhaustive methylation "
        "of xanthine.",
        "Natural product",
        "",
        [
            {"reaction_smiles": "Cn1cnc2c1c(=O)[nH]c(=O)n2C.CI"
                                ">>Cn1cnc2c1c(=O)n(C)c(=O)n2C.[I-]",
             "reagents": "MeI, K₂CO₃",
             "conditions": "DMF, 80 °C",
             "yield_pct": 88.0,
             "notes": "Theobromine (3,7-dimethylxanthine) → caffeine "
                      "(1,3,7-trimethylxanthine). N1 is the last remaining "
                      "N-H; deprotonation + SN2 on methyl iodide."},
        ],
    ),

    (
        "Paracetamol from phenol (Hoechst 3-step)",
        "Acetaminophen",
        "CC(=O)Nc1ccc(O)cc1",
        "Industrial synthesis: phenol is nitrated at the para position, "
        "the nitro is hydrogenated to an amine (catalytic, Pd/C), and the "
        "amine is selectively N-acetylated by acetic anhydride. Three "
        "clean steps with ~99 % para selectivity in the nitration.",
        "Industrial",
        "Hoechst (1878); still an active industrial route today.",
        [
            {"reaction_smiles":
             "Oc1ccccc1.O=N(=O)O>>Oc1ccc([N+](=O)[O-])cc1.O",
             "reagents": "HNO₃, H₂SO₄",
             "conditions": "0 °C",
             "notes": "Step 1: electrophilic aromatic nitration. The "
                      "OH directs ortho/para; para dominates on sterics."},
            {"reaction_smiles":
             "Oc1ccc([N+](=O)[O-])cc1.[H][H]>>Oc1ccc(N)cc1.O",
             "reagents": "H₂, Pd/C",
             "conditions": "1 atm, 25 °C",
             "notes": "Step 2: catalytic reduction of the nitro group "
                      "to the primary aromatic amine (p-aminophenol)."},
            {"reaction_smiles":
             "Oc1ccc(N)cc1.CC(=O)OC(=O)C>>CC(=O)Nc1ccc(O)cc1.CC(=O)O",
             "reagents": "Ac₂O",
             "conditions": "H₂O, 80 °C",
             "notes": "Step 3: selective N-acetylation — the aromatic "
                      "amine is more nucleophilic than the phenol."},
        ],
    ),

    (
        "Aspirin from phenol (Kolbe-Schmitt + acetylation)",
        "Aspirin",
        "CC(=O)Oc1ccccc1C(=O)O",
        "Two-step industrial route: phenol is carboxylated ortho to the "
        "hydroxyl with NaOH + CO₂ under pressure (Kolbe-Schmitt), giving "
        "salicylic acid; this is then acetylated with acetic anhydride to "
        "give aspirin.",
        "Industrial",
        "Kolbe (1860); Schmitt (1885); Bayer (1897).",
        [
            {"reaction_smiles":
             "Oc1ccccc1.O=C=O>>OC(=O)c1ccccc1O",
             "reagents": "NaOH, CO₂",
             "conditions": "125 °C, 100 bar",
             "notes": "Step 1: Kolbe-Schmitt carboxylation. Sodium "
                      "phenoxide attacks CO₂; proton shift gives ortho "
                      "hydroxybenzoate, acidic workup gives salicylic acid."},
            {"reaction_smiles":
             "OC(=O)c1ccccc1O.CC(=O)OC(=O)C"
             ">>CC(=O)Oc1ccccc1C(=O)O.CC(=O)O",
             "reagents": "Ac₂O, cat. H₂SO₄",
             "conditions": "85 °C, 15 min",
             "yield_pct": 85.0,
             "notes": "Step 2: O-acetylation of the phenol with acetic "
                      "anhydride. By-product is acetic acid."},
        ],
    ),

    (
        "Vanillin from eugenol (2-step via isoeugenol)",
        "Vanillin",
        "COc1cc(C=O)ccc1O",
        "Classic semisynthesis from eugenol (clove oil). KOH isomerises "
        "the allyl group to the more-stable propenyl group, then oxidative "
        "cleavage of that alkene (O₃ or KMnO₄) gives vanillin plus "
        "acetaldehyde.",
        "Natural product",
        "Tiemann & Haarmann (1874).",
        [
            {"reaction_smiles":
             "C=Cc1ccc(O)c(OC)c1>>CC=Cc1ccc(O)c(OC)c1",
             "reagents": "KOH",
             "conditions": "EtOH, 150 °C, 4 h",
             "notes": "Step 1: base-catalysed isomerisation of the allyl "
                      "group to the propenyl (conjugates with the ring)."},
            {"reaction_smiles":
             "CC=Cc1ccc(O)c(OC)c1.[O]>>COc1cc(C=O)ccc1O.CC=O",
             "reagents": "O₃, then Zn / H₂O (or KMnO₄)",
             "conditions": "CH₂Cl₂, −78 °C (ozonolysis)",
             "notes": "Step 2: oxidative cleavage of the C=C giving "
                      "vanillin and acetaldehyde as the two fragments."},
        ],
    ),

    (
        "Aniline from benzene (2-step: nitration + reduction)",
        "Aniline",
        "Nc1ccccc1",
        "Classic 2-step industrial amination of benzene. Step 1 is the "
        "canonical mixed-acid nitration (HNO₃/H₂SO₄); step 2 is catalytic "
        "reduction of the nitro group to the primary arylamine. This is "
        "the opening move for a huge fraction of aromatic chemistry — "
        "aniline is the starting point for azo dyes, sulfonamides, and "
        "nitrogen-heterocycle synthesis.",
        "Industrial",
        "Hofmann 1843 (aniline from nitrobenzene); mixed-acid nitration is textbook.",
        [
            {"reaction_smiles":
             "c1ccccc1.O=N(=O)O>>[O-][N+](=O)c1ccccc1.O",
             "reagents": "HNO₃, H₂SO₄",
             "conditions": "50 °C, controlled addition",
             "notes": "Step 1: electrophilic aromatic nitration. "
                      "H₂SO₄ generates NO₂⁺ from HNO₃. Selectivity for "
                      "mononitration by keeping the temperature low."},
            {"reaction_smiles":
             "[O-][N+](=O)c1ccccc1.[H][H]>>Nc1ccccc1.O",
             "reagents": "H₂, Pd/C (or Sn / HCl historically)",
             "conditions": "1 atm, 25 °C",
             "notes": "Step 2: the nitro group is reduced stepwise "
                      "(nitroso → hydroxylamine → amine) and "
                      "dehydration on the catalyst surface gives aniline."},
        ],
    ),

    (
        "2-Methyl-2-butanol via Grignard (2-step)",
        "2-Methyl-2-butanol",
        "CCC(C)(O)C",
        "Textbook Grignard synthesis of a tertiary alcohol. Ethyl bromide "
        "is activated by Mg insertion to give ethylmagnesium bromide, "
        "which then attacks the carbonyl carbon of acetone. Aqueous "
        "workup protonates the magnesium alkoxide intermediate, giving "
        "the 3° alcohol. Classic undergraduate two-step transformation.",
        "Textbook",
        "Grignard 1900 (Nobel Prize 1912).",
        [
            {"reaction_smiles":
             "CCBr.[Mg]>>CC[Mg]Br",
             "reagents": "Mg turnings",
             "conditions": "anhydrous Et₂O or THF",
             "notes": "Step 1: oxidative insertion of Mg into the C–Br "
                      "bond gives the Grignard reagent. Strictly "
                      "anhydrous solvent — any water kills the reagent."},
            {"reaction_smiles":
             "CC[Mg]Br.CC(=O)C.O>>CCC(C)(O)C.Br[Mg]O",
             "reagents": "acetone, then H₃O⁺",
             "conditions": "Et₂O, 0 °C → rt, aqueous workup",
             "notes": "Step 2: nucleophilic addition of the Grignard "
                      "carbanion to the carbonyl gives a magnesium "
                      "alkoxide; aqueous workup protonates to the "
                      "tertiary alcohol (2-methyl-2-butanol)."},
        ],
    ),

    (
        "Met-enkephalin via Fmoc SPPS (solid-phase peptide synthesis)",
        "Met-enkephalin (YGGFM)",
        "N[C@@H](Cc1ccc(O)cc1)C(=O)NCC(=O)NCC(=O)N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCSC)C(=O)O",
        "Teaching example of Merrifield-style solid-phase peptide "
        "synthesis using the Fmoc strategy. Chain is built C→N on a "
        "resin: each cycle is (a) Fmoc deprotection with 20 % "
        "piperidine/DMF, then (b) coupling the next Fmoc-amino acid "
        "with HBTU/DIPEA (activated ester). After the final residue, "
        "TFA cleavage releases the peptide and removes side-chain "
        "protecting groups. Demonstrates five such cycles — one per "
        "residue of the pentapeptide YGGFM.",
        "Peptide / classroom",
        "Merrifield, R.B. 1963 J. Am. Chem. Soc. 85:2149",
        [
            {"reaction_smiles":
                "O=C(OCC1c2ccccc2-c2ccccc21)N[C@@H](CCSC)C(=O)O.[OH]"
                ">>N[C@@H](CCSC)C(=O)O.O=C(O)OCC1c2ccccc2-c2ccccc21",
             "reagents": "20 % piperidine in DMF",
             "conditions": "5 min, rt",
             "notes": "Fmoc removal on resin-bound Met; the Fmoc "
                      "leaves as dibenzofulvene trapped by piperidine. "
                      "Exposes the free α-amine ready for coupling."},
            {"reaction_smiles":
                "N[C@@H](CCSC)C(=O)O."
                "O=C(OCC1c2ccccc2-c2ccccc21)N[C@@H](Cc1ccccc1)C(=O)O"
                ">>O=C(OCC1c2ccccc2-c2ccccc21)N[C@@H](Cc1ccccc1)"
                "C(=O)N[C@@H](CCSC)C(=O)O.O",
             "reagents": "Fmoc-Phe-OH, HBTU, DIPEA, DMF",
             "conditions": "30 min, rt",
             "notes": "HBTU activates the incoming Fmoc-Phe as an "
                      "OBt ester; DIPEA buffers the liberated acid. "
                      "The activated ester aminolyses in minutes."},
            {"reaction_smiles":
                "O=C(OCC1c2ccccc2-c2ccccc21)N[C@@H](Cc1ccccc1)"
                "C(=O)N[C@@H](CCSC)C(=O)O.NCC(=O)O"
                ">>O=C(OCC1c2ccccc2-c2ccccc21)NCC(=O)"
                "N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCSC)C(=O)O.O",
             "reagents": "Fmoc-Gly-OH, HBTU, DIPEA, DMF (after Fmoc removal)",
             "conditions": "30 min, rt",
             "notes": "Repeat deprotect/couple cycle for Gly-4."},
            {"reaction_smiles":
                "O=C(OCC1c2ccccc2-c2ccccc21)NCC(=O)N[C@@H](Cc1ccccc1)"
                "C(=O)N[C@@H](CCSC)C(=O)O.NCC(=O)O"
                ">>O=C(OCC1c2ccccc2-c2ccccc21)NCC(=O)NCC(=O)"
                "N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCSC)C(=O)O.O",
             "reagents": "Fmoc-Gly-OH, HBTU, DIPEA, DMF (after Fmoc removal)",
             "conditions": "30 min, rt",
             "notes": "Repeat deprotect/couple for Gly-3."},
            {"reaction_smiles":
                "O=C(OCC1c2ccccc2-c2ccccc21)NCC(=O)NCC(=O)"
                "N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCSC)C(=O)O."
                "N[C@@H](Cc1ccc(O)cc1)C(=O)O"
                ">>N[C@@H](Cc1ccc(O)cc1)C(=O)NCC(=O)NCC(=O)"
                "N[C@@H](Cc1ccccc1)C(=O)N[C@@H](CCSC)C(=O)O."
                "O=C(O)OCC1c2ccccc2-c2ccccc21",
             "reagents": "Fmoc-Tyr(OtBu)-OH then 95 % TFA cleavage",
             "conditions": "2 h coupling, then 2 h TFA",
             "notes": "Final residue coupled; then TFA cleaves the "
                      "peptide from the Wang resin and removes the "
                      "tert-butyl ether from tyrosine in one step. "
                      "Product is free Met-enkephalin."},
        ],
    ),

    (
        "Phenacetin → Acetaminophen (O-dealkylation)",
        "Acetaminophen",
        "CC(=O)Nc1ccc(O)cc1",
        "Historic: phenacetin was withdrawn in the 1980s after links to "
        "kidney failure and cancer, but its active metabolite — "
        "acetaminophen, produced by CYP-mediated O-deethylation in the "
        "liver — is the paracetamol we still use. This transformation "
        "can also be achieved chemically with HBr.",
        "Metabolic / semisynthetic",
        "Morse, H.N. (1878). Phenacetin withdrawn 1983.",
        [
            {"reaction_smiles": "CCOc1ccc(NC(=O)C)cc1.[H+]"
                                ">>CC(=O)Nc1ccc(O)cc1.CC",
             "reagents": "48 % HBr, Δ",
             "conditions": "reflux, 3 h",
             "notes": "Acid-catalysed cleavage of the aryl ethyl ether. "
                      "In vivo the same transformation is performed by "
                      "CYP1A2 (O-deethylation)."},
        ],
    ),
]


def seed_pathways_if_empty() -> int:
    """Additively seed pathways — insert any missing by name."""
    with session_scope() as s:
        existing_names = {p.name for p in s.query(SynthesisPathway.name).all()}

    to_add = [p for p in _STARTER if p[0] not in existing_names]
    if not to_add:
        log.info("Synthesis pathways table has all %d starter entries",
                 len(_STARTER))
        return 0

    added = 0
    with session_scope() as s:
        for (name, target_name, target_smiles, description, category,
             source, steps) in to_add:
            pathway = SynthesisPathway(
                name=name,
                target_name=target_name,
                target_smiles=target_smiles,
                description=description,
                category=category,
                source=source,
            )
            s.add(pathway)
            s.flush()   # assign pathway.id
            for idx, step in enumerate(steps):
                s.add(SynthesisStep(
                    pathway_id=pathway.id,
                    step_index=idx,
                    reaction_smiles=step["reaction_smiles"],
                    reagents=step.get("reagents"),
                    conditions=step.get("conditions"),
                    yield_pct=step.get("yield_pct"),
                    notes=step.get("notes"),
                ))
            added += 1
    log.info("Seeded %d synthesis pathways", added)
    return added
