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

    # ---- Phase 31d content expansion (2026-04-23) --------------------
    (
        "Benzocaine — 3-step nitrotoluene route",
        "Benzocaine",
        "CCOC(=O)c1ccc(N)cc1",
        "Classic teaching synthesis of the topical local anaesthetic: "
        "p-nitrotoluene → p-nitrobenzoic acid via KMnO₄ oxidation of "
        "the methyl → reduction of the nitro group to the amine with "
        "Fe/HCl → Fischer esterification with ethanol. Illustrates "
        "chemoselective oxidation (no touching of the aromatic ring), "
        "a classical nitro reduction, and the equilibrium-driven "
        "esterification reinforcing Le Chatelier thinking.",
        "Pedagogical (3-step)",
        "Clayden *Organic Chemistry* 2e §23 (undergrad lab synthesis).",
        [
            {"reaction_smiles": "Cc1ccc([N+](=O)[O-])cc1"
                                ">>O=C(O)c1ccc([N+](=O)[O-])cc1",
             "reagents": "KMnO₄, H₂O",
             "conditions": "reflux, 4 h, then H₃O⁺ workup",
             "yield_pct": 70.0,
             "notes": "Strong oxidation burns the methyl all the way "
                      "to the carboxylic acid. NO₂ is inert under "
                      "these conditions; ring oxidation (Baeyer-"
                      "Villiger-style) is not competitive."},
            {"reaction_smiles": "O=C(O)c1ccc([N+](=O)[O-])cc1"
                                ">>O=C(O)c1ccc(N)cc1",
             "reagents": "Fe, HCl",
             "conditions": "reflux, 2 h; then base workup",
             "yield_pct": 85.0,
             "notes": "Classical Béchamp reduction — the Fe(0) donates "
                      "6e⁻ total to reduce NO₂ through ArNO / ArNHOH "
                      "→ ArNH₂. Modern labs often substitute H₂/Pd-C."},
            {"reaction_smiles": "O=C(O)c1ccc(N)cc1.CCO"
                                ">>CCOC(=O)c1ccc(N)cc1.O",
             "reagents": "EtOH (excess), cat. H₂SO₄",
             "conditions": "reflux, 6 h",
             "yield_pct": 75.0,
             "notes": "Fischer esterification. Excess ethanol drives "
                      "the equilibrium right; the aromatic amine is "
                      "not acylated because NH₂ is a worse nucleophile "
                      "than EtOH under the H₃O⁺ / protonation regime."},
        ],
    ),

    (
        "Lidocaine — 2-step amide + amine-alkylation route",
        "Lidocaine",
        "CCN(CC)CC(=O)Nc1c(C)cccc1C",
        "Industrial 2-step synthesis of the amide-class local "
        "anaesthetic / class-Ib antiarrhythmic. 2,6-dimethylaniline "
        "reacts with chloroacetyl chloride to give an α-chloroamide, "
        "then SN2 displacement of the α-Cl by diethylamine delivers "
        "lidocaine. The 2,6-methyl substitution on the aniline is "
        "what blocks N-acylation-to-amide hydrolysis and gives "
        "lidocaine its long in-vivo half-life.",
        "Pharmaceutical (2-step)",
        "Löfgren & Lundqvist, *Svensk Kem. Tidskr.* 58:206 (1946).",
        [
            {"reaction_smiles": "Nc1c(C)cccc1C.ClCC(=O)Cl"
                                ">>ClCC(=O)Nc1c(C)cccc1C.[H]Cl",
             "reagents": "ClCH₂COCl, Et₃N (base / HCl scavenger)",
             "conditions": "CH₂Cl₂, 0 °C → rt, 1 h",
             "yield_pct": 90.0,
             "notes": "Schotten-Baumann-style acylation. The 2,6-"
                      "methyls on the aniline create steric shielding "
                      "around the amide C=O — this is the whole point, "
                      "because it's what blocks esterase hydrolysis "
                      "(unlike procaine, an ester)."},
            {"reaction_smiles": "ClCC(=O)Nc1c(C)cccc1C.CCNCC"
                                ">>CCN(CC)CC(=O)Nc1c(C)cccc1C.[H]Cl",
             "reagents": "Et₂NH (excess, 2 eq.)",
             "conditions": "toluene or benzene reflux, 3 h",
             "yield_pct": 80.0,
             "notes": "SN2 on the α-chloroamide. Diethylamine is the "
                      "nucleophile; the α-carbonyl activates the C–Cl. "
                      "Second eq. of Et₂NH scavenges HCl. Product is "
                      "a tertiary amine that is readily protonated at "
                      "physiological pH — hence the clinical "
                      "lidocaine hydrochloride salt."},
        ],
    ),

    (
        "Procaine — 2-step acyl chloride route (Einhorn)",
        "Procaine",
        "CCN(CC)CCOC(=O)c1ccc(N)cc1",
        "Teaching-grade 2-step synthesis of the ester-class local "
        "anaesthetic that completes the seeded anaesthetic triad "
        "(Benzocaine, Lidocaine, Procaine). PABA is first activated "
        "as the acyl chloride with SOCl₂ — a textbook "
        "carboxylic-acid-to-acyl-chloride activation that kicks out "
        "SO₂ and HCl. The acyl chloride then undergoes a "
        "Schotten-Baumann-style esterification with "
        "2-(diethylamino)ethanol, delivering procaine directly. "
        "Note the design contrast with lidocaine: procaine carries "
        "an **ester** linker (hydrolysed in plasma by butyryl-"
        "cholinesterase → short duration of action), while lidocaine's "
        "**amide** linker + 2,6-xylidine flanking methyls block "
        "esterase hydrolysis → long duration. Same pharmacophore, "
        "very different PK.",
        "Pharmaceutical (2-step)",
        "Einhorn, A. (1905) Justus Liebigs Ann. Chem. 371:125-161.",
        [
            {"reaction_smiles": "Nc1ccc(C(=O)O)cc1.ClS(=O)Cl"
                                ">>Nc1ccc(C(=O)Cl)cc1.O=S=O.[H]Cl",
             "reagents": "SOCl₂ (1.2 eq.)",
             "conditions": "neat or CH₂Cl₂, reflux, 2 h",
             "yield_pct": 92.0,
             "notes": "Classic carboxylic-acid → acyl chloride "
                      "activation. The S centre is attacked by the "
                      "carboxylate oxygen; a chloride ion is then "
                      "delivered to the carbonyl carbon and the "
                      "chlorosulphite leaving group collapses to "
                      "SO₂ + Cl⁻. The aniline nitrogen is not "
                      "protected because the carboxylic-acid OH "
                      "is far more nucleophilic towards SOCl₂ — "
                      "no side-reaction in practice."},
            {"reaction_smiles": "Nc1ccc(C(=O)Cl)cc1.OCCN(CC)CC"
                                ">>CCN(CC)CCOC(=O)c1ccc(N)cc1.[H]Cl",
             "reagents": "HOCH₂CH₂NEt₂ (1.1 eq.), Et₃N (HCl scavenger)",
             "conditions": "toluene, 0 °C → rt, 4 h",
             "yield_pct": 85.0,
             "notes": "Schotten-Baumann-style esterification: the "
                      "primary alcohol of 2-(diethylamino)ethanol "
                      "attacks the acyl chloride; chloride leaves; "
                      "Et₃N mops up HCl. The tertiary-amine nitrogen "
                      "of the aminoethanol is the clinically "
                      "important protonation site — procaine is "
                      "dispensed as the hydrochloride salt "
                      "(formed in situ here, or by treatment with "
                      "HCl/Et₂O). Keeping the reaction cold + "
                      "anhydrous prevents hydrolysis of the "
                      "acyl chloride back to PABA."},
        ],
    ),

    (
        "Sulfanilamide — 3-step chlorosulfonation route",
        "Sulfanilamide",
        "Nc1ccc(S(=O)(=O)N)cc1",
        "The first clinically useful sulfa drug (Prontosil's active "
        "metabolite).  Industrial route starts from acetanilide — "
        "cheap, commercial, with the amine already masked as the "
        "acetamide so it doesn't compete during chlorosulfonation. "
        "Three textbook steps: **EAS chlorosulfonation** installs a "
        "sulfonyl chloride para to the acetamido directing group; "
        "**amination** with NH₃ converts the -SO₂Cl to the "
        "sulfonamide; **acidic hydrolysis** then deprotects the "
        "aniline.  Sulfanilamide launched antibacterial chemotherapy "
        "(Domagk, Nobel 1939).",
        "Pharmaceutical (3-step)",
        "Northey, E.H. (1948) *Sulfonamides & allied compounds*.",
        [
            {"reaction_smiles": "CC(=O)Nc1ccccc1.OS(=O)(=O)Cl"
                                ">>CC(=O)Nc1ccc(S(=O)(=O)Cl)cc1.O",
             "reagents": "ClSO₃H (chlorosulfonic acid, 4 eq.)",
             "conditions": "neat, 60 °C, 2 h",
             "yield_pct": 70.0,
             "notes": "Electrophilic aromatic substitution; the "
                      "acetamide group is a para-director + activator, "
                      "so the sulfonyl chloride lands almost "
                      "exclusively at the 4-position.  Water is the "
                      "nominal byproduct of the overall reaction."},
            {"reaction_smiles": "CC(=O)Nc1ccc(S(=O)(=O)Cl)cc1.N"
                                ">>CC(=O)Nc1ccc(S(=O)(=O)N)cc1.[H]Cl",
             "reagents": "NH₃ (aq. or conc. NH₄OH, 4 eq.)",
             "conditions": "0 °C → rt, 30 min",
             "yield_pct": 90.0,
             "notes": "Nucleophilic substitution at sulfur: the "
                      "sulfonyl chloride is attacked by ammonia, "
                      "chloride leaves as HCl.  Excess NH₃ scavenges "
                      "the proton.  Classic mild Schotten-Baumann-"
                      "style amidation at S rather than C."},
            {"reaction_smiles": "CC(=O)Nc1ccc(S(=O)(=O)N)cc1.O"
                                ">>Nc1ccc(S(=O)(=O)N)cc1.CC(=O)O",
             "reagents": "10 % HCl (aq.)",
             "conditions": "reflux, 1 h",
             "yield_pct": 85.0,
             "notes": "Acid-catalysed hydrolysis of the acetamide "
                      "deprotecting group.  The sulfonamide is "
                      "hydrolytically stable, so selectivity is "
                      "easy.  Acetic acid drifts off; crystallise "
                      "the free aniline from the cooled mixture."},
        ],
    ),

    (
        "Phenolphthalein — Friedel-Crafts condensation",
        "Phenolphthalein",
        "OC1=CC=C(C=C1)C1(c2ccc(O)cc2)OC(=O)c2ccccc21",
        "Classical 1-step dye / indicator synthesis: phthalic "
        "anhydride condenses with **two** equivalents of phenol "
        "under Brønsted-acid catalysis (conc. H₂SO₄ or ZnCl₂).  "
        "Both C–C bonds form at the para position of each phenol "
        "via a Friedel-Crafts-like acylation / dehydration "
        "cascade through a lactone-hemiketal intermediate.  "
        "Phenolphthalein is colourless below pH ~8.3 (closed "
        "lactone) and pink above (open quinoid dianion) — the "
        "textbook acid-base indicator.  Also widely used in "
        "industrial-scale laxative manufacture until the 1990s.",
        "Dye / indicator",
        "Baeyer, A. (1871) *Ann. Chem. Pharm.* 160: 325.",
        [
            {"reaction_smiles":
             "O=C1OC(=O)c2ccccc12.Oc1ccccc1.Oc1ccccc1"
             ">>OC1=CC=C(C=C1)C1(c2ccc(O)cc2)OC(=O)c2ccccc21.O",
             "reagents": "conc. H₂SO₄ (catalyst, 1-2 eq.) or ZnCl₂ "
                         "(melt, no solvent)",
             "conditions": "120 °C, 2-4 h",
             "yield_pct": 80.0,
             "notes": "Stepwise mechanism inside the flask: "
                      "(i) phenol attacks a protonated anhydride "
                      "carbonyl (C-acylation para to OH), opening "
                      "the anhydride to a diaryl-ketone carboxylic "
                      "acid.  (ii) The remaining carboxylic acid "
                      "dehydrates onto the new ketone carbon, "
                      "closing a 5-ring lactone.  (iii) A second "
                      "phenol adds to the lactol carbon "
                      "(Friedel-Crafts on the carbinol carbocation) "
                      "and water leaves, delivering the "
                      "characteristic sp³ spiro-lactone.  "
                      "Net: anhydride + 2 PhOH → phenolphthalein "
                      "+ H₂O."},
        ],
    ),

    (
        "Saccharin — 3-step Remsen-Fahlberg route",
        "Saccharin",
        "O=C1NS(=O)(=O)c2ccccc21",
        "The first artificial sweetener, discovered accidentally by "
        "Remsen & Fahlberg in 1879 while studying the oxidation of "
        "o-toluenesulfonamide.  Three textbook transforms from cheap "
        "toluene: **chlorosulfonation** (para + ortho; the ortho "
        "isomer carries the lesson), **ammonolysis** of the sulfonyl "
        "chloride, and **side-chain oxidation** of the methyl group.  "
        "The freshly-formed o-carboxylic acid spontaneously condenses "
        "with the adjacent sulfonamide N-H to close the 5-membered "
        "1,1-dioxo-benzothiazolinone (sulfimide) ring — that "
        "cyclisation is what gives saccharin its unusual structure.",
        "Food / consumer",
        "Remsen, I. & Fahlberg, C. (1879) Am. Chem. J. 1: 426.",
        [
            {"reaction_smiles": "Cc1ccccc1.OS(=O)(=O)Cl"
                                ">>Cc1ccccc1S(=O)(=O)Cl.O",
             "reagents": "ClSO₃H (chlorosulfonic acid, 3 eq.)",
             "conditions": "neat, 0 → 40 °C, 1 h",
             "yield_pct": 65.0,
             "notes": "EAS: the methyl group directs ortho + para, "
                      "so the crude mixture carries both sulfonyl "
                      "chlorides.  Industrially the isomers are "
                      "separated by fractional crystallisation of "
                      "the product sulfonamide (next step) — the "
                      "ortho isomer is the valuable precursor here."},
            {"reaction_smiles": "Cc1ccccc1S(=O)(=O)Cl.N"
                                ">>Cc1ccccc1S(=O)(=O)N.[H]Cl",
             "reagents": "aq. NH₃ (4 eq., excess)",
             "conditions": "0 °C → rt, 30 min",
             "yield_pct": 90.0,
             "notes": "Ammonolysis at sulfur: the chloride leaves "
                      "as HCl (scavenged by excess NH₃).  At this "
                      "stage the para isomer is removed by selective "
                      "crystallisation — only the ortho "
                      "sulfonamide cyclises cleanly in step 3."},
            {"reaction_smiles":
             "Cc1ccccc1S(=O)(=O)N.O=[Mn](=O)(=O)[O-].[K+]"
             ">>O=C1NS(=O)(=O)c2ccccc21.O=[Mn]=O.O.[K+].[OH-]",
             "reagents": "KMnO₄ (3 eq., aq.)",
             "conditions": "reflux, 4 h; acidify, crystallise",
             "yield_pct": 70.0,
             "notes": "Side-chain oxidation CH₃ → COOH, then "
                      "intramolecular dehydration: the ortho -COOH "
                      "carbonyl is attacked by the -SO₂NH₂ nitrogen, "
                      "closing the 5-ring sulfimide lactam.  The "
                      "product is saccharin's neutral form; "
                      "technical-grade material is the sodium salt "
                      "(sodium saccharinate).  MnO₂ + KOH are the "
                      "oxidation byproducts."},
        ],
    ),

    (
        "Acetanilide — 1-step acetylation of aniline",
        "Acetanilide",
        "CC(=O)Nc1ccccc1",
        "Trivial but pedagogically rich: aniline + acetic anhydride "
        "→ acetanilide + acetic acid, a one-step N-acetylation that "
        "masks the basic amine as a deactivated amide.  Acetanilide "
        "is the common starting material for **two** already-seeded "
        "industrial routes: phenacetin (alkylate the N, then Frost "
        "reduction) and sulfanilamide (chlorosulfonation → amination "
        "→ hydrolysis).  It's also historically the first aniline-"
        "based antipyretic (1886 — withdrawn by the 1940s after "
        "methaemoglobinaemia reports; replaced by acetaminophen, "
        "its N-deacylated hepatic metabolite).",
        "Teaching / precursor",
        "Friedländer & Taussig (1896); Kalle chemische Fabrik.",
        [
            {"reaction_smiles": "Nc1ccccc1.CC(=O)OC(=O)C"
                                ">>CC(=O)Nc1ccccc1.CC(=O)O",
             "reagents": "acetic anhydride (1.1 eq.)",
             "conditions": "glacial AcOH as solvent, 60 °C, 15 min; "
                           "quench on ice → crystallise",
             "yield_pct": 95.0,
             "notes": "Textbook nucleophilic acyl substitution at "
                      "the more electrophilic anhydride carbonyl.  "
                      "The aniline N attacks, the tetrahedral "
                      "intermediate collapses kicking out acetate "
                      "(which picks up the proton to give acetic "
                      "acid).  The reaction is fast and selective "
                      "even in acetic-acid solvent because the "
                      "amide C=O is much less electrophilic than "
                      "the anhydride — no di-acylation."},
        ],
    ),

    (
        "L-DOPA — Knowles Rh-DIPAMP asymmetric route (3-step)",
        "L-DOPA",
        "N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O",
        "Monsanto's industrial route to (S)-levodopa — the first "
        "**asymmetric catalytic hydrogenation** to reach industrial "
        "scale and the centrepiece of William Knowles's 2001 Nobel "
        "Prize.  Three steps from the cheap aromatic aldehyde "
        "veratraldehyde (3,4-dimethoxybenzaldehyde):\n\n"
        "  1. Erlenmeyer-type condensation with N-acetylglycine gives "
        "a (Z)-dehydroamino-acid intermediate.\n"
        "  2. Asymmetric hydrogenation over Rh / (R,R)-DIPAMP "
        "delivers H₂ to a single enantioface, giving the (S)-"
        "configured N-acetyl-3,4-dimethoxyphenylalanine in "
        "≥ 95 % ee — the industrial proof that a chiral phosphine "
        "ligand could replace a resolution.\n"
        "  3. HBr / AcOH simultaneously demethylates both methyl "
        "aryl ethers and hydrolyses the acetamide, giving "
        "L-DOPA directly.\n\n"
        "L-DOPA itself is a **pro-drug for dopamine**: it crosses "
        "the blood-brain barrier via the LAT1 amino-acid "
        "transporter (dopamine cannot), then aromatic-amino-acid "
        "decarboxylase (AADC) strips the -COOH in situ inside the "
        "CNS.  Gold-standard Parkinson's treatment since 1970 "
        "(Cotzias, Yahr, Duvoisin).",
        "Pharmaceutical (3-step, asymmetric)",
        "Knowles, W.S. (2002) *Angew. Chem. Int. Ed.* 41: 1998 "
        "(Nobel lecture).",
        [
            {"reaction_smiles":
             "O=Cc1ccc(OC)c(OC)c1.CC(=O)NCC(=O)O"
             ">>CC(=O)N/C(=C\\c1ccc(OC)c(OC)c1)/C(=O)O.O",
             "reagents": "N-acetylglycine (1.05 eq.), Ac₂O (4 eq.), "
                         "NaOAc (1 eq.)",
             "conditions": "reflux, 2 h; hydrolyse the intermediate "
                           "azlactone with aq. acetone",
             "yield_pct": 75.0,
             "notes": "The N-acetylglycine goes first through a "
                      "5-membered azlactone (Erlenmeyer) that "
                      "deprotonates to a strongly nucleophilic "
                      "enolate — this attacks the aldehyde in an "
                      "aldol-style C-C bond formation.  Aqueous "
                      "work-up opens the azlactone back to the "
                      "(Z)-dehydroamino acid (Z preferred by "
                      "intramolecular H-bonding with the NH)."},
            {"reaction_smiles":
             "CC(=O)N/C(=C\\c1ccc(OC)c(OC)c1)/C(=O)O.[H][H]"
             ">>CC(=O)N[C@@H](Cc1ccc(OC)c(OC)c1)C(=O)O",
             "reagents": "H₂ (3 atm), [Rh((R,R)-DIPAMP)]⁺ (0.01 eq.)",
             "conditions": "MeOH, 25 °C, 12 h",
             "yield_pct": 95.0,
             "notes": "The Knowles keystone.  DIPAMP = (R,R)-"
                      "bis(2-methoxyphenyl)(phenyl)phosphine, the "
                      "chiral-at-phosphorus bisphosphine that "
                      "differentiates the two prochiral faces of "
                      "the substrate via a dihydride-intermediate "
                      "'minor pathway' that actually delivers the "
                      "product.  Gives (S)-amino acid in ≥ 95 % ee "
                      "at industrial ton scale — a milestone for "
                      "asymmetric catalysis."},
            {"reaction_smiles":
             "CC(=O)N[C@@H](Cc1ccc(OC)c(OC)c1)C(=O)O.[H]Br.[H]Br.[H]Br.O"
             ">>N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O.CC(=O)O.CBr.CBr",
             "reagents": "48 % HBr / AcOH (excess)",
             "conditions": "reflux, 4 h; crystallise from EtOH/H₂O",
             "yield_pct": 85.0,
             "notes": "One-pot triple deprotection: both methyl "
                      "aryl ethers are cleaved by HBr (SN2 at "
                      "methyl → CH₃Br byproduct; phenol is "
                      "regenerated), and the acetamide is "
                      "hydrolysed by the hot aqueous acid.  No "
                      "epimerisation at the α-stereocentre despite "
                      "the acidic conditions — the stereocentre is "
                      "protected by the zwitterion form of the "
                      "amino acid."},
        ],
    ),

    (
        "Dopamine — decarboxylation of L-DOPA (1-step)",
        "Dopamine",
        "NCCc1ccc(O)c(O)c1",
        "Companion single-step to the L-DOPA route.  Decarboxylation "
        "of the α-amino acid removes CO₂ and gives the catecholamine "
        "neurotransmitter directly.  *In vivo* this is the AADC-"
        "catalysed reaction that activates L-DOPA inside the CNS — "
        "which is why L-DOPA (not dopamine) is dispensed: dopamine "
        "itself can't cross the blood-brain barrier, but its amino-"
        "acid precursor rides LAT1 and is decarboxylated on "
        "arrival.  Chemically, the same net transform can be driven "
        "with heat + Brønsted acid (Ba(OH)₂ gives a cleaner lab-"
        "scale variant).",
        "Pharmacology / biosynthesis",
        "Blaschko, H. (1939) *J. Physiol.* 96: 50 (first "
        "observation in mammalian tissue).",
        [
            {"reaction_smiles":
             "N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O"
             ">>NCCc1ccc(O)c(O)c1.O=C=O",
             "reagents": "AADC (aromatic-L-amino-acid "
                         "decarboxylase, PLP cofactor) — **or** "
                         "Ba(OH)₂, heat (chemical)",
             "conditions": "aqueous, pH 7, 37 °C (enzymatic) or "
                           "~200 °C (thermal Ba(OH)₂)",
             "yield_pct": 90.0,
             "notes": "Mechanism (enzymatic): the α-NH₂ forms an "
                      "imine with pyridoxal phosphate (PLP); the "
                      "carboxylate leaves as CO₂ with the bond-"
                      "breaking electrons moving onto the PLP π "
                      "system (quinonoid intermediate, "
                      "electron-sink stabilisation is PLP's "
                      "specialty); the resulting planar carbanion "
                      "is reprotonated on the same face by a "
                      "conserved active-site residue — hence the "
                      "reaction is stereospecific but the "
                      "α-stereocentre is destroyed (product is "
                      "achiral; no chirality to preserve).  Net: "
                      "loss of CO₂, replacement of the α-COOH "
                      "with α-H."},
        ],
    ),

    (
        "Adipic acid — DuPont cyclohexane route (2-step)",
        "Adipic acid",
        "OC(=O)CCCCC(=O)O",
        "The industrial route that feeds ~90 % of world adipic "
        "acid production (~2.8 Mt/yr), most of which goes into "
        "nylon-6,6 via the companion pathway below.  Two steps "
        "from cheap cyclohexane (distilled from petroleum naphtha "
        "or made by benzene hydrogenation):\n\n"
        "  1. **Air oxidation** of cyclohexane with a Co/Mn "
        "naphthenate catalyst at 150 °C / 15 atm gives a ~1:1 "
        "mixture of cyclohexanol + cyclohexanone — the industrial "
        "**KA oil** (K = ketone, A = alcohol).  Selectivity to KA "
        "oil is held ≲ 10 % conversion to avoid radical "
        "overoxidation of the C-H-rich cycle.\n"
        "  2. **Nitric-acid oxidation** of KA oil with 50 % HNO₃ / "
        "V + Cu catalyst cleaves the C-C bond to give adipic acid "
        "quantitatively.  The well-known environmental wart: "
        "~1 mol N₂O escapes per mol adipic acid, making it one of "
        "the largest industrial sources of this potent greenhouse "
        "gas.  Modern plants install catalytic N₂O abatement "
        "downstream.",
        "Industrial / commodity",
        "Draths, K.M. & Frost, J.W. (1994) *J. Am. Chem. Soc.* "
        "116: 399 (greener biosynthetic alternative).",
        [
            {"reaction_smiles":
             "C1CCCCC1.O=O>>OC1CCCCC1.O=C1CCCCC1.O",
             "reagents": "O₂ (4 bar), Co / Mn naphthenate (0.01 eq.)",
             "conditions": "150 °C, 15 atm, ~8 % conversion (kinetic "
                           "quench)",
             "yield_pct": 85.0,
             "notes": "Radical autoxidation: cyclohexyl peroxyl "
                      "intermediates decompose to give KA oil. "
                      "Held at low conversion because the "
                      "alcohol/ketone are much easier to over-"
                      "oxidise than cyclohexane itself."},
            {"reaction_smiles":
             "OC1CCCCC1.O=C1CCCCC1.O[N+](=O)[O-].O[N+](=O)[O-]"
             ">>OC(=O)CCCCC(=O)O.[N-]=[N+]=O.O.O",
             "reagents": "50 % aq. HNO₃ (2-4 eq.), V₂O₅ / Cu(NO₃)₂ "
                         "(catalytic)",
             "conditions": "80-100 °C, ~1 atm, 1 h",
             "yield_pct": 95.0,
             "notes": "Mechanism is a mix of V-mediated C-C "
                      "cleavage on the α-diketone oxidation "
                      "intermediate and direct HNO₃ cleavage.  "
                      "N₂O is the major nitrogen byproduct "
                      "(~1 mol/mol adipic) — a major industrial "
                      "climate-footprint issue addressed by "
                      "thermal-catalytic abatement at plant "
                      "scale."},
        ],
    ),

    (
        "Nylon-6,6 — adipic acid + HMDA polycondensation (2-step)",
        "Nylon-6,6",
        "NCCCCCCNC(=O)CCCCC(=O)NCCCCCCN",
        "The Carothers polyamide that launched synthetic-fibre "
        "industry in 1938.  Two discrete industrial stages:\n\n"
        "  1. **Nylon salt formation** — equimolar adipic acid + "
        "hexamethylenediamine (HMDA) in methanol crystallise as "
        "the 1:1 diammonium di-carboxylate salt "
        "(*AH salt*, mp 190 °C).  Making the salt first gives "
        "exact 1:1 stoichiometry — critical for high-MW polymer, "
        "because Carothers's equation says MW rockets only as "
        "the ratio approaches 1:1 exactly.\n"
        "  2. **Melt polycondensation** — heat the dry salt at "
        "270 °C under N₂ with vacuum to drive off water; the "
        "ammonium salts liberate HMDA and adipic acid in the "
        "melt, which condense sequentially to give the long-chain "
        "polyamide.  Typical commercial MW ~15-30 kDa (n ~ 50 "
        "repeat units).  The SMILES below is a 2-amide 'model "
        "dimer' showing one complete HMDA-AA-HMDA segment (the "
        "polymer chain is just this unit repeated).",
        "Industrial polymer",
        "Carothers, W.H. (1938) US Patent 2,130,523; du Pont "
        "commercial launch 1939 as nylon stockings.",
        [
            {"reaction_smiles":
             "NCCCCCCN.OC(=O)CCCCC(=O)O"
             ">>[NH3+]CCCCCC[NH3+].[O-]C(=O)CCCCC(=O)[O-]",
             "reagents": "adipic acid (1.0 eq.), HMDA (1.0 eq.)",
             "conditions": "MeOH, 25 °C; salt crystallises",
             "yield_pct": 95.0,
             "notes": "Acid-base neutralisation: both amine ends "
                      "grab a proton from the diacid.  The "
                      "diammonium di-carboxylate is a crystalline "
                      "solid, easy to purify, and provides the "
                      "exact 1:1 stoichiometry that Carothers's "
                      "equation demands for high-MW polymer.  "
                      "Called **AH salt** in plant jargon."},
            {"reaction_smiles":
             "[NH3+]CCCCCC[NH3+].[O-]C(=O)CCCCC(=O)[O-].NCCCCCCN"
             ">>NCCCCCCNC(=O)CCCCC(=O)NCCCCCCN.O.O",
             "reagents": "(nylon salt melt, dry)",
             "conditions": "270 °C, N₂ purge → vacuum, 4 h",
             "yield_pct": 90.0,
             "notes": "Step-growth polycondensation: the "
                      "ammonium-carboxylate liberates free amine "
                      "+ free acid in the hot melt; the pair "
                      "then dehydrates through a tetrahedral "
                      "intermediate to give an amide + H₂O.  "
                      "Chain length grows by Carothers's formula "
                      "DP = 1/(1-p) with p = extent of "
                      "reaction — so 99 % conversion gives "
                      "DP = 100 (MW ~ 12-15 kDa), 99.5 % gives "
                      "DP = 200.  Water removal drives the "
                      "equilibrium forward.  The 'model dimer' "
                      "in the product SMILES is one complete "
                      "HMDA-AA-HMDA repeat; real polymer is this "
                      "× 50-150."},
        ],
    ),

    (
        "Nylon-6 — Beckmann / caprolactam route (3-step)",
        "Nylon-6",
        "NCCCCCC(=O)NCCCCCC(=O)O",
        "The other big commodity polyamide — Paul Schlack's 1938 "
        "answer to Carothers's nylon-6,6.  Three steps from the "
        "same cyclohexanone that feeds the adipic-acid route, "
        "showing how one C₆ cycloketone branches into the two "
        "world-scale nylon markets:\n\n"
        "  1. **Oxime formation** — cyclohexanone + NH₂OH (from "
        "hydroxylammonium sulfate) → cyclohexanone oxime.\n"
        "  2. **Beckmann rearrangement** — oxime + conc. H₂SO₄ "
        "(or oleum) → ε-caprolactam.  The ring *expands by one* "
        "because the C-C bond anti to the leaving –OH migrates "
        "to nitrogen; the stereospecificity of that migration "
        "is the textbook pedagogical payload.\n"
        "  3. **Ring-opening polycondensation** — caprolactam + "
        "trace water, 260 °C → nylon-6.  Each repeat unit is "
        "one caprolactam with the lactam opened to an amide + "
        "free amine / acid ends that feed the next monomer.  "
        "The product SMILES is a 2-residue dimer model "
        "(amino-terminus → amide bond → carboxylic-acid "
        "terminus) — real nylon-6 is this × 100-200 repeats.\n\n"
        "Properties differ from nylon-6,6 because **all amide "
        "bonds point the same way** along the chain (versus "
        "alternating in nylon-6,6) — giving slightly lower "
        "melting point, softer hand, and different dye uptake.  "
        "Still the dominant polyamide for tyre-cord and textile.",
        "Industrial polymer",
        "Schlack, P. (1938) IG Farben Patent DE 748,253; later "
        "BASF / DSM commercial routes.",
        [
            {"reaction_smiles":
             "O=C1CCCCC1.ON>>ON=C1CCCCC1.O",
             "reagents": "hydroxylammonium sulfate (0.5 eq. = 1 "
                         "eq. NH₂OH), NaOH buffer",
             "conditions": "aq., 60 °C, 1 h",
             "yield_pct": 95.0,
             "notes": "Standard oxime formation: NH₂OH attacks "
                      "the ketone carbonyl, eliminates water "
                      "through a carbinolamine intermediate.  "
                      "Buffered at pH 5-6 — acid catalyses the "
                      "dehydration step, but strong acid "
                      "suppresses NH₂OH nucleophilicity by "
                      "protonation."},
            {"reaction_smiles":
             "ON=C1CCCCC1.OS(=O)(=O)O>>O=C1CCCCCN1.OS(=O)(=O)O",
             "reagents": "oleum / conc. H₂SO₄ (>3 eq., or SO₃-"
                         "modified)",
             "conditions": "80-130 °C, 30 min; then neutralise "
                           "with aq. NH₃ (generates (NH₄)₂SO₄ "
                           "byproduct — valuable fertiliser!)",
             "yield_pct": 90.0,
             "notes": "Beckmann mechanism: protonation of the "
                      "oxime O turns it into a leaving group; "
                      "the C-C bond *anti* to the O migrates to "
                      "N in concert with -OH₂⁺ departure; the "
                      "resulting nitrilium ion is attacked by "
                      "water and tautomerises to the amide.  "
                      "Stereospecific: only the anti C-C bond "
                      "migrates.  (NH₄)₂SO₄ coproduction is "
                      "huge at plant scale — the ratio is a "
                      "classical industrial sustainability "
                      "concern addressed by newer vapour-phase "
                      "zeolite Beckmann catalysts."},
            {"reaction_smiles":
             "O=C1CCCCCN1.O=C1CCCCCN1.O>>NCCCCCC(=O)NCCCCCC(=O)O",
             "reagents": "H₂O (~2 % w/w as ring-opening "
                         "initiator)",
             "conditions": "260 °C, N₂ blanket, 6 h; draw fibre "
                           "from melt",
             "yield_pct": 95.0,
             "notes": "Ring-opening polycondensation: trace "
                      "water hydrolyses one lactam to give a "
                      "linear amino acid (6-aminohexanoic acid) "
                      "that then propagates by adding more "
                      "lactam monomers through its amine end, "
                      "each opening the C-N of the next lactam "
                      "(same net transformation as hydrolysis "
                      "+ re-condensation).  Equilibrium "
                      "polymerisation — product equilibrates "
                      "with ~10 % unreacted lactam that is "
                      "washed out of the finished pellets.  The "
                      "model dimer in the SMILES shows one full "
                      "HN-CH₂-CH₂-CH₂-CH₂-CH₂-CO- repeat × 2."},
        ],
    ),

    (
        "Aspartame — Z-protected peptide-coupling route (2-step)",
        "Aspartame",
        "COC(=O)[C@@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O",
        "The artificial sweetener discovered serendipitously by "
        "Schlatter in 1965 while assembling a peptide drug — he "
        "licked his finger to turn a page and noticed the "
        "sweetness.  Aspartame is simply **L-Asp-L-Phe-OMe** "
        "(a dipeptide methyl ester), ~200× sweeter than sucrose "
        "per gram.  Must be the **α-linked** regioisomer from "
        "the aspartate side — β-linkage (Asp side-chain "
        "carboxyl → Phe) is bitter.\n\n"
        "Two steps using standard orthogonal protection:\n\n"
        "  1. Peptide coupling of **Z-L-Asp** (α-NH₂ protected "
        "as the benzyloxycarbonyl carbamate, β-COOH free) with "
        "**L-Phe-OMe** via DCC / HOBt → Z-aspartame.  The "
        "Z-group prevents the α-amine from self-acylating; "
        "the β-COOH stays free (harmless spectator under DCC "
        "because it's more sterically hindered + less "
        "activated).\n"
        "  2. **Z hydrogenolysis** (H₂ / Pd-C, MeOH) cleaves "
        "the benzylic C-O bond; the resulting carbamic acid "
        "spontaneously decarboxylates to give the free amine "
        "(+ toluene byproduct + CO₂).  Mild, neutral, does not "
        "epimerise.",
        "Pharmaceutical / food",
        "Mazur, R.H.; Schlatter, J.M.; Goldkamp, A.H. (1969) "
        "*J. Am. Chem. Soc.* 91: 2684.",
        [
            {"reaction_smiles":
             "O=C(OCc1ccccc1)N[C@@H](CC(=O)O)C(=O)O"
             ".COC(=O)[C@@H](N)Cc1ccccc1"
             ">>O=C(OCc1ccccc1)N[C@@H](CC(=O)O)C(=O)N[C@@H]"
             "(Cc1ccccc1)C(=O)OC.O",
             "reagents": "DCC (1.1 eq.), HOBt (1 eq.)",
             "conditions": "DMF, 0 °C → rt, 4 h",
             "yield_pct": 75.0,
             "notes": "Classic DCC / HOBt coupling: DCC "
                      "activates the α-COOH of Z-Asp through "
                      "the O-acylisourea, HOBt shuttles it "
                      "through a less-reactive benzotriazole "
                      "ester to suppress racemisation.  The "
                      "α-amine of Phe-OMe then attacks the "
                      "activated carbonyl, giving the amide.  "
                      "The β-COOH of aspartate sits quietly on "
                      "the side — it's both sterically "
                      "disfavoured and poorly activated under "
                      "DCC compared to the α.  Industrial "
                      "plants use the enzyme thermolysin as an "
                      "alternative, which is absolutely α-"
                      "regioselective (no protection needed on "
                      "the β)."},
            {"reaction_smiles":
             "O=C(OCc1ccccc1)N[C@@H](CC(=O)O)C(=O)N[C@@H]"
             "(Cc1ccccc1)C(=O)OC.[H][H].[H][H]"
             ">>COC(=O)[C@@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O"
             ".Cc1ccccc1.O=C=O",
             "reagents": "H₂ (1 atm), 10 % Pd-C (cat.)",
             "conditions": "MeOH, rt, 1 h",
             "yield_pct": 95.0,
             "notes": "Z (carbobenzoxy) hydrogenolysis: Pd "
                      "cleaves the benzylic C-O bond to give "
                      "toluene + a carbamic acid intermediate, "
                      "which spontaneously loses CO₂ to leave "
                      "the free amine.  Mild, neutral, no "
                      "epimerisation — one of the key reasons "
                      "Z remains a go-to Nα protecting group "
                      "in peptide chemistry.  Fmoc (9-fluorenyl"
                      "methyloxycarbonyl) is the base-labile "
                      "alternative when acid- or H₂-sensitive "
                      "side chains are also present."},
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
