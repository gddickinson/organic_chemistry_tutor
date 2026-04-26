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

    # ---- Phase 31b round 134 — CuAAC click chemistry ---------------
    ("Click chemistry: CuAAC (phenylacetylene + benzyl azide)",
     "Cycloaddition (Cu-catalysed)",
     "Sharpless / Meldal / Bertozzi 2022 Nobel Prize in Chemistry. "
     "Copper(I)-catalysed azide-alkyne cycloaddition (CuAAC) — "
     "the canonical 'click' reaction.  Thermal Huisgen "
     "1,3-dipolar cycloaddition of an azide and a terminal "
     "alkyne is sluggish at room temperature and gives a ~1:1 "
     "mixture of 1,4- and 1,5-disubstituted 1,2,3-triazole "
     "regioisomers; the Cu(I) catalyst (from CuSO₄ / sodium "
     "ascorbate, or from CuI directly) accelerates the reaction "
     "~10⁷-fold AND drives complete 1,4-regioselectivity.  "
     "Mechanism (Fokin / Finn 2005 + Worrell 2013): Cu(I) "
     "deprotonates the alkyne to form a copper acetylide; "
     "a second Cu(I) coordinates the azide α-N; ladder cycle "
     "with stepwise C–N bond formation through a six-membered "
     "metallacycle gives the 1,4-triazole + regenerates Cu(I).  "
     "The reaction is bioorthogonal (azides + alkynes don't "
     "exist in living cells) and proceeds in water — the "
     "conditions that put it at the centre of chemical-biology "
     "labelling, drug-discovery fragment assembly, and polymer "
     "/ materials cross-linking.  Strain-promoted SPAAC "
     "(cyclooctyne + azide, no Cu) is the bio-friendly variant "
     "that earned Bertozzi her share of the Nobel.",
     "C#Cc1ccccc1.[N-]=[N+]=NCc1ccccc1"
     ">>c1ccc(Cn2cc(-c3ccccc3)nn2)cc1"),

    # ---- Phase 31b round 152 — Birch reduction ---------------------
    ("Birch reduction (benzene → 1,4-cyclohexadiene)",
     "Reduction (single-electron transfer)",
     "Birch 1944 — dissolving-metal reduction of an aromatic "
     "ring with Na (or Li, or K) in liquid ammonia (~ −33 °C) "
     "and a proton source (EtOH, t-BuOH, MeOH).  The *only* "
     "seeded reaction in the catalogue that goes through "
     "single-electron-transfer (SET) chemistry rather than "
     "concerted / two-electron polar bonds.  Mechanism is a "
     "4-step ladder: (1) Na donates one electron to benzene to "
     "give a radical anion; (2) EtOH protonates the radical "
     "anion at one of the carbons that bears the highest "
     "electron density to give a cyclohexadienyl radical; "
     "(3) a second Na donates an electron to give a "
     "pentadienyl-stabilised carbanion; (4) EtOH protonates "
     "again at the central carbon of the pentadienyl anion to "
     "give the **non-conjugated** 1,4-cyclohexadiene.  "
     "Critical regioselectivity: 1,4 (not 1,3) because the "
     "second protonation lands at the central carbon of the "
     "5-atom pentadienyl anion — protonation at the ends "
     "would give an unstable cross-conjugated diene.  "
     "Substituent rule: electron-donating groups (OMe, NR₂) "
     "land on sp²-carbon of the product (un-reduced ring "
     "position); electron-withdrawing groups (COOH, CO-R) "
     "land on sp³.  Workhorse for setting up enol ethers from "
     "anisole + chiral cyclohexenones from ortho-substituted "
     "benzoic acids in total synthesis.",
     "c1ccccc1.[Na].[Na].CCO.CCO"
     ">>C1=CCC=CC1.[Na+].[Na+].[O-]CC.[O-]CC"),

    # ---- Phase 31b round 152 — Dess-Martin periodinane oxidation ---
    ("Dess-Martin oxidation (1-octanol → octanal)",
     "Oxidation",
     "Dess + Martin 1983 — modern, mild, hyper-valent-iodine(V) "
     "oxidation of a 1° alcohol to an aldehyde (or 2° alcohol "
     "to a ketone) using Dess-Martin periodinane (DMP, "
     "1,1,1-tris(acetyloxy)-1,1-dihydro-1,2-benziodoxol-3-(1H)-"
     "one).  Run in CH₂Cl₂ at room temperature, complete in "
     "minutes; aqueous bicarbonate / thiosulfate workup.  "
     "Mechanism: alcohol exchange replaces one of the three "
     "acetate ligands at the I(V) centre with the alkoxide; "
     "intramolecular β-acetate-assisted hydride / proton "
     "removal (cyclic TS) reduces I(V) → I(III) and produces "
     "the carbonyl + 2 AcOH + the o-iodoxybenzoic-acid "
     "by-product (IBX after workup).  Critical advantage over "
     "Swern: no cryogenic temperature, no foul-smelling "
     "Me₂S by-product, and the reagent is bench-stable as a "
     "white powder.  Critical advantage over Jones / KMnO₄: "
     "does NOT over-oxidise to carboxylic acid (just like "
     "Swern + PCC).  Now the default 1° → aldehyde oxidation "
     "in modern total-synthesis labs.",
     "CCCCCCCCO>>CCCCCCCC=O"),

    # ---- Phase 31b round 153 — Sharpless asymmetric epoxidation ----
    ("Sharpless asymmetric epoxidation (trans-crotyl "
     "alcohol → 2,3-epoxybutan-1-ol)",
     "Asymmetric catalysis (oxidation)",
     "K. B. Sharpless 1980 (Nobel 2001, shared with Knowles + "
     "Noyori) — the first practical asymmetric oxidation, and "
     "the first asymmetric-catalysis entry in the catalogue.  "
     "Reagents: catalytic Ti(OiPr)₄ + a chiral diethyl "
     "tartrate (DET) ligand + tert-butyl hydroperoxide (TBHP) "
     "in CH₂Cl₂ with 4 Å molecular sieves at −20 °C.  "
     "Mechanism (highly schematic): two Ti(OiPr)₄ + two DET "
     "self-assemble into a dimeric Ti₂(tartrate)₂ complex; "
     "the allylic alcohol coordinates one Ti through its OH, "
     "TBHP coordinates the same Ti as a peroxide, and "
     "intramolecular oxygen transfer from the η²-peroxide to "
     "the alkene face dictated by the (R,R)- or (S,S)-tartrate "
     "ligand delivers the 2,3-epoxide.  **Substrate "
     "requirement: the alcohol MUST be allylic** (i.e. -OH on "
     "the carbon next to the C=C) — the OH is the anchor that "
     "binds the substrate to the Ti centre.  Face-selectivity "
     "predicted by the Sharpless mnemonic: with the allylic "
     "alcohol drawn with the OH at lower right, (R,R)-(+)-DET "
     "delivers the oxygen from below; (S,S)-(−)-DET from "
     "above.  Routinely > 90 % ee with simple substrates.  "
     "Game-changing for total synthesis — opened the era of "
     "predictable enantioselective C-O bond formation.",
     "C/C=C/CO.CC(C)(C)OO>>C[C@@H]1O[C@H]1CO.CC(C)(C)O"),

    # ---- Phase 31b round 153 — CBS reduction ------------------------
    ("CBS reduction (acetophenone → (R)-1-phenylethanol)",
     "Asymmetric catalysis (reduction)",
     "Corey + Bakshi + Shibata 1987 — catalytic enantioselective "
     "reduction of a prochiral ketone to the corresponding "
     "secondary alcohol, using a sub-stoichiometric chiral "
     "oxazaborolidine catalyst (the *CBS catalyst*, derived "
     "from (S)- or (R)-α,α-diphenylprolinol + a borane) plus "
     "stoichiometric BH₃·THF / BH₃·SMe₂ / catecholborane as the "
     "hydride source.  Mechanism: the CBS catalyst's nitrogen "
     "Lewis-binds borane while its boron Lewis-binds the "
     "ketone oxygen; this brings hydride + carbonyl into a "
     "rigid cis-fused six-membered chair-like TS where the "
     "*larger* ketone substituent points *away* from the "
     "endo-face of the catalyst, so hydride delivery is "
     "stereo-electronically dictated.  With (S)-CBS catalyst, "
     "ArC(=O)R (Ar bigger than R) gives the (R)-alcohol; "
     "swap to (R)-CBS for the (S)-alcohol.  Routinely > 95 % "
     "ee for aryl-alkyl ketones; tolerates esters, halides, "
     "alkenes that NaBH₄ would touch.  Workhorse asymmetric "
     "ketone reduction in modern total synthesis (e.g. "
     "Corey's prostaglandin, Taxol, ginkgolide routes).  "
     "Pedagogically distinct from the seeded NaBH₄ entry: "
     "same overall transformation (C=O → C-OH), but with "
     "a chiral catalyst that controls the new stereocentre's "
     "absolute configuration.",
     "CC(=O)c1ccccc1.B>>O[C@@H](C)c1ccccc1"),

    # ---- Phase 31b round 154 — Sharpless asymmetric dihydroxylation
    ("Sharpless asymmetric dihydroxylation (trans-stilbene "
     "→ (R,R)-1,2-diphenylethane-1,2-diol)",
     "Asymmetric catalysis (oxidation)",
     "K. B. Sharpless 1988-1996 (the Nobel-2001 oxidation half "
     "of the prize, alongside the asymmetric epoxidation).  "
     "Catalytic K₂OsO₄·2H₂O + a bis-cinchona-alkaloid chiral "
     "ligand ((DHQ)₂PHAL or (DHQD)₂PHAL — the two ligand "
     "enantiomers commercially pre-mixed as **AD-mix-α** "
     "(DHQ)₂PHAL and **AD-mix-β** (DHQD)₂PHAL respectively) + "
     "stoichiometric K₃Fe(CN)₆ as the terminal oxidant + "
     "K₂CO₃ + tBuOH/H₂O at 0 °C.  Mechanism: OsO₄ undergoes a "
     "[3+2] cycloaddition with the alkene face dictated by the "
     "chiral ligand to give an osmate ester; hydrolysis liberates "
     "the *cis*-1,2-diol AND reduced Os(VI), which is "
     "re-oxidised by ferricyanide back to OsO₄ to close the "
     "catalytic cycle.  **The Sharpless mnemonic for face "
     "selectivity:** with the alkene drawn left-to-right and "
     "the larger substituent at upper-left, AD-mix-β attacks "
     "from below to give the *(R,R)* diol; AD-mix-α from "
     "above to give *(S,S)*.  Pedagogically distinct from the "
     "round-153 Sharpless asymmetric epoxidation: works on "
     "any alkene (no allylic-OH substrate restriction), and "
     "delivers a *syn*-diol rather than an epoxide.  Highly "
     "general — trans-, cis-, mono-, di-, tri-substituted "
     "alkenes all reactive — and routinely > 90 % ee.",
     "c1ccc(/C=C/c2ccccc2)cc1.O=[Os](=O)(=O)=O.O"
     ">>O[C@@H](c1ccccc1)[C@H](O)c1ccccc1.O=[Os]=O"),

    # ---- Phase 31b round 154 — Jacobsen-Katsuki epoxidation --------
    ("Jacobsen-Katsuki epoxidation (cis-β-methylstyrene → "
     "(2R,3S)-2-methyl-3-phenyloxirane)",
     "Asymmetric catalysis (oxidation)",
     "Jacobsen 1990 + Katsuki 1990 (independent reports) — "
     "asymmetric epoxidation of unfunctionalised cis- (and "
     "tri-substituted) alkenes using a chiral Mn(III)(salen) "
     "complex catalyst + a stoichiometric terminal oxidant "
     "(NaOCl bleach is the cheapest; PhIO, NMO, mCPBA also "
     "used).  The **(R,R)- or (S,S)-N,N'-bis(3,5-di-tert-"
     "butylsalicylidene)-1,2-cyclohexanediamine-Mn(III)Cl** "
     "catalyst is the canonical 'Jacobsen catalyst'.  "
     "Mechanism: NaOCl oxidises Mn(III) → Mn(V)=O oxo-"
     "intermediate; the alkene approaches over the chiral "
     "salen ligand from the less-hindered face; concerted "
     "(or radical, depending on substrate) oxygen transfer "
     "gives the epoxide and regenerates Mn(III).  Critical "
     "complement to Sharpless: **does NOT require an allylic "
     "OH** (Mn coordinates the oxidant, not the substrate), "
     "making cis-disubstituted aryl alkenes (cis-β-"
     "methylstyrene, cis-stilbene, indene, dihydronaphthalene) "
     "the sweet-spot substrates that Sharpless cannot touch.  "
     "Together with Sharpless asymmetric epoxidation + "
     "Sharpless asymmetric dihydroxylation, completes the "
     "asymmetric-oxygen-installation toolkit.  Routinely "
     "80-95 % ee.",
     "C/C=C\\c1ccccc1.[Na+].[O-]Cl"
     ">>C[C@H]1O[C@@H]1c1ccccc1.[Na+].[Cl-]"),

    # ---- Phase 31b round 155 — Mukaiyama aldol ---------------------
    ("Mukaiyama aldol (TMS enol ether of acetone + "
     "benzaldehyde → 4-hydroxy-4-phenyl-2-butanone)",
     "Asymmetric catalysis (C-C bond formation)",
     "Mukaiyama 1973 — Lewis-acid-catalysed crossed aldol "
     "between a pre-formed silyl enol ether (or silyl ketene "
     "acetal) and an aldehyde / ketone.  Run at −78 °C in "
     "CH₂Cl₂ with TiCl₄ or BF₃·OEt₂ as the Lewis-acid "
     "activator (or, for the asymmetric variant — Mukaiyama "
     "1990, Carreira 1994 — a chiral Ti-BINOL, Cu-BOX, or "
     "oxazaborolidinone Lewis acid).  Mechanism: Lewis acid "
     "binds the aldehyde carbonyl, activating it for "
     "nucleophilic attack; the silyl enol ether attacks via an "
     "**open** TS (not a Zimmerman-Traxler chair) — the silyl "
     "group blocks the aldehyde-ene cyclic geometry — to give "
     "a TMS-protected aldol; aqueous workup desilylates to the "
     "β-hydroxy carbonyl.  Critical pedagogical advantages "
     "over the classic acid- or base-catalysed aldol: pre-"
     "formation of the enol ether sets the regiochemistry "
     "(no α-proton ambiguity), the open TS gives the "
     "**anti**-aldol with simple aldehyde + ketone substrates, "
     "and the Mukaiyama protocol tolerates many Lewis-basic "
     "functional groups that would deprotonate or coordinate "
     "to a strong base.  Workhorse first C-C bond-formation "
     "asymmetric-catalysis entry — opens the asymmetric C-C "
     "bond-formation teaching surface alongside the C-O / "
     "C=O entries (Sharpless AE / AD + Jacobsen + CBS).",
     "C=C(O[Si](C)(C)C)C.O=Cc1ccccc1"
     ">>O[C@H](c1ccccc1)CC(=O)C.O[Si](C)(C)C"),

    # ---- Phase 31b round 155 — Evans aldol -------------------------
    ("Evans aldol (N-propionyl-(S)-4-benzyloxazolidinone + "
     "propanal → syn-(2S,3R)-aldol)",
     "Asymmetric catalysis (C-C bond formation)",
     "D. A. Evans 1981 — diastereoselective aldol via a chiral "
     "**oxazolidinone auxiliary** + Bu₂BOTf + i-Pr₂NEt (or "
     "Et₃N) at −78 °C in CH₂Cl₂.  The (S)-4-benzyl-2-"
     "oxazolidinone auxiliary is acylated onto the carboxylic "
     "acid via mixed-anhydride or DCC chemistry; soft "
     "enolisation with Bu₂BOTf forms the (Z)-boron enolate; "
     "addition to an aldehyde proceeds through a tightly "
     "constrained **Zimmerman-Traxler chair TS** in which "
     "(a) the aldehyde's R group adopts the equatorial "
     "position, (b) the boron's two butyl ligands shield one "
     "enolate face, and (c) the auxiliary's benzyl group "
     "shields the other face — leaving exactly one geometry "
     "open and giving the *Evans syn* aldol with > 95:5 dr.  "
     "Auxiliary cleavage (LiOH / H₂O₂) then liberates the "
     "carboxylic-acid product without epimerisation, and the "
     "auxiliary recycles cleanly.  Pedagogically distinct "
     "from the round-155 Mukaiyama aldol: Evans uses a "
     "stoichiometric chiral *auxiliary* + a closed Zimmerman-"
     "Traxler TS (gives *syn*-aldol), whereas Mukaiyama uses "
     "a sub-stoichiometric Lewis-acid *catalyst* + an open TS "
     "(gives *anti*-aldol when uncatalysed; many "
     "stereo-outcomes possible with chiral catalysts).  "
     "Together they cover the two main paradigms of "
     "asymmetric aldol: chiral auxiliary vs chiral catalyst.",
     "CCC(=O)N1[C@@H](Cc2ccccc2)COC1=O.CCC=O"
     ">>CC[C@H](O)[C@@H](C)C(=O)N1[C@@H](Cc2ccccc2)COC1=O"),

    # ---- Phase 31b round 156 — Stille coupling ---------------------
    ("Stille coupling (bromobenzene + tributyl(vinyl)stannane "
     "→ styrene)",
     "Cross-coupling (Pd-catalysed)",
     "Stille 1978 (Migita-Kosugi-Stille; Nobel 2010 was Negishi "
     "+ Suzuki + Heck — Stille is the famous one that didn't "
     "share the prize, JKS having died in 1989).  Pd(0)-"
     "catalysed C(sp²)–C(sp²) (or C(sp²)–C(sp³)) coupling "
     "between an aryl / vinyl halide (or pseudohalide — "
     "triflate, iodonium, etc.) and an organostannane R₃Sn-R'.  "
     "Catalytic cycle: oxidative addition of Ar–X to Pd(0); "
     "transmetalation in which the R' group migrates from Sn "
     "to Pd (typically Bu₃Sn–X is the by-product); reductive "
     "elimination forms the C-C bond and regenerates Pd(0).  "
     "Distinctive from Suzuki / Sonogashira / Negishi: the Sn "
     "reagent is **air-, moisture-, and pH-stable** — Stille "
     "couplings tolerate water, acidic and basic conditions, "
     "and a huge range of polar functional groups.  Trade-off: "
     "tributyltin is **toxic and environmentally persistent**, "
     "so Stille has been largely replaced by Suzuki for "
     "commercial work; still used in total synthesis where "
     "the stannane's exquisite functional-group tolerance + "
     "ability to make C(sp²)-C(sp³) bonds is irreplaceable.  "
     "Closes the Pd-coupling family in the catalogue at "
     "5/5 textbook canon entries (Suzuki + Negishi + Heck + "
     "Sonogashira + Stille).",
     "Brc1ccccc1.C=C[Sn](CCCC)(CCCC)CCCC"
     ">>C=Cc1ccccc1.CCCC[Sn](CCCC)(CCCC)Br"),

    # ---- Phase 31b round 156 — Corey-Chaykovsky epoxidation --------
    ("Corey-Chaykovsky epoxidation (benzaldehyde + dimethyl"
     "sulfonium methylide → styrene oxide)",
     "Methylene transfer (sulfur ylide)",
     "E. J. Corey + M. Chaykovsky 1965 — single-CH₂ transfer "
     "from a sulfur ylide onto a carbonyl to give an epoxide.  "
     "Two flavours: (a) the **dimethylsulfonium methylide** "
     "(Me₂S=CH₂, generated in situ from trimethylsulfonium "
     "iodide + n-BuLi or NaH) — kinetic, irreversible, "
     "delivers CH₂ to **aldehydes + ketones** to give the "
     "terminal epoxide and dimethyl sulfide as the by-product; "
     "(b) the **dimethylsulfoxonium methylide** (Me₂S(O)=CH₂, "
     "generated from trimethylsulfoxonium iodide + NaH) — "
     "thermodynamic, reversible, prefers 1,4-addition to "
     "α,β-unsaturated carbonyls (giving cyclopropanes from "
     "enones).  Mechanism for (a): nucleophilic ylide carbon "
     "attacks the carbonyl C → betaine; the alkoxide displaces "
     "Me₂S in an intramolecular SN2 → epoxide.  Critical "
     "pedagogical complement to **Wittig** (same overall C=O → "
     "C-X transformation, but Wittig gives an alkene via "
     "R₃P=CR₂ ylide + O ends up on phosphorus, while Corey-"
     "Chaykovsky gives an epoxide via R₂S=CR₂ ylide + S "
     "leaves intact).  Also complements **Sharpless asymmetric "
     "epoxidation** + **Jacobsen** by being a *non-asymmetric* "
     "+ *non-allylic-OH-required* epoxidation that comes from "
     "a ketone substrate not an alkene — the only catalogue "
     "entry that builds a brand-new oxirane CH₂ ring atom from "
     "scratch (Sharpless / Jacobsen oxidise a pre-existing "
     "C=C to an epoxide; Corey-Chaykovsky converts a C=O to "
     "an epoxide that gains a new CH₂).",
     "O=Cc1ccccc1.C[S+](C)[CH2-]>>C1OC1c1ccccc1.CSC"),

    # ---- Phase 31b round 157 — Appel reaction ----------------------
    ("Appel reaction (1-octanol → 1-chlorooctane)",
     "Functional-group interconversion",
     "Appel 1975 — alcohol → alkyl halide via PPh₃ + a "
     "tetrahalomethane (CCl₄ for chloride, CBr₄ for bromide, "
     "CI₄ for iodide).  Run in CH₂Cl₂ or DMF at 0 °C → rt.  "
     "Mechanism: PPh₃ attacks one of the chlorines of CCl₄ "
     "displacing trichloromethanide (CCl₃⁻) → "
     "chlorotriphenylphosphonium chloride [Ph₃PCl]⁺ Cl⁻; the "
     "alcohol substitutes one Cl on phosphorus to give an "
     "alkoxytriphenylphosphonium intermediate "
     "(R-O-P⁺Ph₃) plus HCCl₃ + Cl⁻; chloride then performs "
     "an **SN2 displacement** of the excellent OPPh₃ leaving "
     "group, delivering R-Cl with **inversion of "
     "configuration** at the carbon and Ph₃P=O as the second "
     "by-product.  **Pedagogical pairing with the seeded "
     "Mitsunobu reaction**: both Appel and Mitsunobu activate "
     "an alcohol's OH as a phosphonium leaving group via PPh₃ "
     "and both deliver SN2 inversion at the carbon — but "
     "Appel uses CCl₄/CBr₄/CI₄ as the halide-source "
     "co-reagent (gives R-X), while Mitsunobu uses "
     "DIAD/DEAD + a soft nucleophile pronucleophile (gives "
     "R-O-CO-R', R-N-CO-R', R-O-Ar, etc.).  Workhorse for "
     "halogenation of alcohols where harsher SOCl₂ / PCl₃ "
     "conditions would touch other functional groups.",
     "CCCCCCCCO.c1ccc(P(c2ccccc2)c2ccccc2)cc1.ClC(Cl)(Cl)Cl"
     ">>CCCCCCCCCl.O=P(c1ccccc1)(c1ccccc1)c1ccccc1.ClC(Cl)Cl"),

    # ---- Phase 31b round 157 — Jones oxidation ---------------------
    ("Jones oxidation (1-octanol → octanoic acid)",
     "Oxidation",
     "Jones 1946 — Cr(VI) oxidation of a 1° alcohol all the "
     "way to a **carboxylic acid** (or 2° alcohol → ketone) "
     "using Jones reagent (CrO₃ + dilute H₂SO₄ in acetone, "
     "added drop-wise to the substrate at 0–25 °C until the "
     "characteristic orange-red Cr(VI) colour persists).  "
     "Mechanism: alcohol forms the chromate ester R-O-CrO₃H; "
     "α-H is removed in a cyclic E2-like TS to give the "
     "carbonyl + reduced Cr(IV); for 1° alcohols the resulting "
     "aldehyde is hydrated by aqueous acetone to a gem-diol, "
     "which gets oxidised again by Cr(VI) to the carboxylic "
     "acid — **the over-oxidation step that defines Jones**.  "
     "Critical pedagogical role in the catalogue: every other "
     "seeded oxidation (PCC + Swern + Dess-Martin) was "
     "specifically designed to STOP at the aldehyde — Jones "
     "is the **counterpoint** that shows what happens when "
     "you don't.  Distinct from Sharpless / Jacobsen "
     "asymmetric oxidations: substrate-driven, no chirality "
     "transfer, just bulk Cr(VI)-mediated dehydrogenation.  "
     "Modern green-chemistry trend is to replace Jones with "
     "TEMPO / NaOCl / KBr or NaIO₄ / RuCl₃ to avoid the "
     "Cr(VI) carcinogen + heavy-metal waste — but Jones is "
     "still teaching-essential as the historical default + "
     "the over-oxidation example.  Closes Phase 31b "
     "named-reaction catalogue at the **50/50 milestone** "
     "alongside the Appel reaction shipped this round.",
     "CCCCCCCCO.O=[Cr](=O)=O>>CCCCCCCC(=O)O.O=[Cr]=O.O"),

    # ---- Phase 31b round 164 — Wacker oxidation --------------------
    ("Wacker oxidation (styrene → acetophenone)",
     "Oxidation (Pd-catalysed)",
     "Smidt et al. 1959 — first Pd-catalysed industrial "
     "process; canonical Pd(II)/Cu(II)/O₂ catalytic system "
     "that converts a terminal alkene to a methyl ketone "
     "with **Markovnikov regioselectivity** (the oxygen ends "
     "up on the more-substituted carbon).  Catalytic cycle: "
     "(1) PdCl₂ activates the alkene as an η²-π-complex; "
     "(2) external water attacks the internal carbon (Wacker "
     "syn-/anti- mechanism debated for decades — modern "
     "consensus is anti-hydroxypalladation for terminal "
     "alkenes, syn for chelating substrates); (3) β-hydride "
     "elimination + reductive elimination releases the "
     "methyl ketone and Pd(0); (4) Pd(0) is re-oxidised to "
     "Pd(II) by Cu(II); (5) Cu(I) is re-oxidised to Cu(II) "
     "by O₂ — Cu acts as the electron-shuttle that closes "
     "the catalytic cycle.  **The Tsuji-Wacker variant** "
     "(stoichiometric PdCl₂ in DMF / H₂O without Cu / O₂) "
     "is the lab-scale benchtop version.  Industrial "
     "application: ethylene → acetaldehyde (Wacker process, "
     "still ~ 2 Mt/yr globally).  Pedagogically: opens the "
     "alkene-to-methyl-ketone disconnection AND illustrates "
     "the redox-relay mechanism (Pd ↔ Cu ↔ O₂) that is the "
     "template for many modern aerobic oxidations.",
     "C=Cc1ccccc1.O.O=O>>CC(=O)c1ccccc1.O"),

    # ---- Phase 31b round 164 — Brown hydroboration-oxidation -------
    ("Brown hydroboration-oxidation (1-methylcyclohexene → "
     "trans-2-methylcyclohexanol)",
     "Addition (anti-Markovnikov, syn-addition)",
     "H. C. Brown 1956-1959 (Nobel 1979, shared with G. "
     "Wittig).  **Two-step alkene → alcohol** via (1) "
     "concerted 4-centre hydroboration with BH₃·THF (or "
     "9-BBN, disiamylborane for tighter selectivity) "
     "delivering H and BR₂ across the alkene **syn** with "
     "B going to the **less-substituted** carbon (steric "
     "control over an empty B 2p orbital — opposite "
     "regiochemistry to acid-catalysed hydration's "
     "Markovnikov + opposite stereochemistry to Br₂ "
     "addition's anti); then (2) oxidative work-up with "
     "alkaline H₂O₂ converts the trialkylborane to the "
     "alcohol via [1,2]-alkyl-shift to oxygen with "
     "**retention of configuration** at the migrating "
     "carbon.  Net result: anti-Markovnikov + syn-addition "
     "OH on the alkene (Markovnikov OH would come from "
     "acid-catalysed hydration; anti-Markovnikov from "
     "radical HBr addition — but only Brown's reaction is "
     "BOTH anti-Markovnikov AND stereo-controlled).  The "
     "trans-2-methylcyclohexanol product locks in both "
     "selectivity arguments at once: anti-Markovnikov puts "
     "OH on the un-substituted carbon, syn-addition puts "
     "OH and CH₃ trans across the ring.  Together with the "
     "round-164 Wacker oxidation (Markovnikov methyl "
     "ketone), Brown opens the **alkene functionalisation "
     "regio-/stereo-selectivity teaching surface** that "
     "the original 50-entry catalogue underserved.",
     "CC1=CCCCC1.B.OO.[Na+].[OH-]"
     ">>O[C@@H]1CCCC[C@H]1C.[Na+].O.B(O)(O)O"),

    # ---- Phase 31b round 165 — Robinson annulation -----------------
    ("Robinson annulation (cyclohexanone + methyl vinyl "
     "ketone → Δ1,9-octalin-2-one)",
     "Annulation (C-C ring formation cascade)",
     "Sir Robert Robinson 1935 (Nobel 1947 for alkaloid + "
     "morphine structure work) — **three-step cascade in "
     "one pot**: (1) Michael addition of an enolate (from "
     "the parent ketone, deprotonated by base — KOH, NaOEt, "
     "or proline for the asymmetric Hajos-Parrish-Eder-"
     "Sauer-Wiechert variant) onto an α,β-unsaturated "
     "ketone (canonically methyl vinyl ketone, MVK, "
     "CC(=O)C=C), giving a 1,5-diketone; (2) intramolecular "
     "**aldol condensation** of the 1,5-diketone — the new "
     "α-carbon of the MVK fragment enolises and attacks the "
     "original ketone carbonyl, forming a new 6-membered "
     "ring; (3) acid- or base-catalysed **dehydration** of "
     "the β-hydroxy intermediate to give the **cyclohexenone "
     "ring fused to the original ring**.  Net result: two "
     "C-C bonds formed + one C-O bond cleaved + a new "
     "α,β-unsaturated ring annulated onto the substrate "
     "ketone.  **The canonical ring-construction reaction in "
     "textbook total synthesis** — the steroid-numbering "
     "Wieland-Miescher ketone (precursor for cortisone, "
     "testosterone, oestrone, etc.) is built from "
     "2-methylcyclohexan-1,3-dione + MVK by exactly this "
     "cascade, and the asymmetric Hajos-Parrish proline-"
     "catalysed variant (1971) is regarded as the "
     "intellectual ancestor of modern enamine-catalysis "
     "(List + Barbas + MacMillan, Nobel 2021).  Opens the "
     "**ring-construction teaching surface** that the "
     "round-152-157 catalogue extension didn't cover.",
     "O=C1CCCCC1.CC(=O)C=C>>O=C1C=C2CCCCC2CC1.O"),

    # ---- Phase 31b round 165 — Knoevenagel condensation ------------
    ("Knoevenagel condensation (benzaldehyde + diethyl "
     "malonate → diethyl benzylidene malonate)",
     "Condensation (active-methylene C-C bond formation)",
     "Emil Knoevenagel 1894 — variant of the aldol "
     "condensation in which the nucleophile is an "
     "**active-methylene compound** (between two electron-"
     "withdrawing groups) rather than a simple ketone "
     "enolate.  Pedagogically distinct from the seeded "
     "aldol because the active-methylene C-H is far more "
     "acidic (pKa ~ 11-13 for malonate / ~ 11 for "
     "cyanoacetate / ~ 10 for nitromethane) than a simple "
     "ketone α-C-H (pKa ~ 20) — so a **mild secondary-amine "
     "base** (piperidine, pyridine, or — Doebner variant — "
     "an amino acid like proline / glycine in pyridine "
     "solvent) is sufficient.  Mechanism: (1) amine "
     "deprotonates the active methylene; (2) resulting "
     "carbanion attacks the aldehyde carbonyl; (3) E1cb "
     "dehydration of the β-hydroxy intermediate gives the "
     "**α,β-unsaturated** product; in the **Doebner "
     "modification** (with monoacids like cyanoacetic acid "
     "or malonic acid + pyridine), spontaneous "
     "decarboxylation of one of the COOH / COOR groups "
     "follows the dehydration → α,β-unsaturated mono-acid "
     "/ mono-ester.  Workhorse for cinnamic-acid + α,β-"
     "unsaturated-ester / nitrile syntheses; foundational "
     "to materials chemistry (push-pull chromophores), "
     "drug discovery (Michael acceptor warheads), and "
     "the seeded **knoevenagel-doebner** route to "
     "fluorescent dyes.  Pedagogically pairs with the "
     "round-152 / 165 ring-construction theme via the "
     "Hantzsch dihydropyridine synthesis (a one-pot "
     "Knoevenagel-cum-Michael-cum-cyclisation cascade).",
     "O=Cc1ccccc1.CCOC(=O)CC(=O)OCC"
     ">>CCOC(=O)/C(=C\\c1ccccc1)C(=O)OCC.O"),

    # ---- Phase 31b round 175 — Henry reaction (nitroaldol) ---------
    ("Henry reaction (nitromethane + benzaldehyde → "
     "2-nitro-1-phenylethanol)",
     "Condensation (nitroaldol)",
     "Louis Henry 1895 — base-catalysed addition of a "
     "**nitroalkane** to an aldehyde or ketone, giving a "
     "**β-nitro alcohol** (the 'nitroaldol' product).  "
     "Functionally analogous to the aldol condensation but "
     "with a nitroalkane as the nucleophile instead of a "
     "ketone enolate; the α-CH of a nitroalkane has pKa "
     "~ 10 (vs ~ 20 for a ketone α-H) thanks to the "
     "extraordinary -NO₂ acidifying group, so a mild base "
     "(amine, NaOH, KF, fluoride / phosphazene catalysts) "
     "is sufficient.  Mechanism: base deprotonates the "
     "nitroalkane to form the **aci-nitro carbanion**; "
     "carbanion attacks the carbonyl carbon; protonation "
     "gives the β-nitro alcohol.  Critically the product "
     "is then a **valuable synthetic intermediate**: "
     "(a) hydrogenation of the nitro group gives a 1,2-"
     "amino-alcohol (β-blocker / chloramphenicol "
     "scaffold); (b) Nef reaction converts -NO₂ to a "
     "carbonyl (giving an α,β-dihydroxyketone or aldehyde); "
     "(c) dehydration gives a nitroalkene / Michael "
     "acceptor.  Asymmetric variants (Shibasaki Ln-BINOL "
     "1992; Trost Zn-ProPhenol 2002) deliver the β-nitro "
     "alcohol with > 90 % ee — workhorse of synthesis of "
     "chiral 1,2-amino alcohols.",
     "C[N+](=O)[O-].O=Cc1ccccc1"
     ">>OC(c1ccccc1)C[N+](=O)[O-]"),

    # ---- Phase 31b round 175 — Hantzsch dihydropyridine MCR --------
    ("Hantzsch dihydropyridine synthesis (benzaldehyde + 2 "
     "ethyl acetoacetate + NH₃ → diethyl 4-phenyl-2,6-"
     "dimethyl-1,4-dihydropyridine-3,5-dicarboxylate)",
     "Multi-component reaction (heterocycle synthesis)",
     "Arthur R. Hantzsch 1881 — **the textbook multi-"
     "component reaction (MCR)** that builds a 1,4-"
     "dihydropyridine ring in one pot from an aldehyde + "
     "two equivalents of a β-ketoester + ammonia (or "
     "ammonium acetate).  Mechanism walk: (1) Knoevenagel "
     "condensation of one β-ketoester with the aldehyde "
     "→ unsaturated diketoester (Phase 31b's seeded "
     "Knoevenagel reaction!); (2) the second β-ketoester "
     "condenses with NH₃ → β-enaminone; (3) Michael "
     "addition of the enaminone onto the unsaturated "
     "Knoevenagel adduct closes the ring; (4) dehydration "
     "gives the symmetric 1,4-dihydropyridine.  Three new "
     "C-N + C-C bonds + four bond-rearrangements in one "
     "pot — quintessential MCR efficiency.  **Pharmaceutical "
     "significance**: the 1,4-dihydropyridine scaffold is "
     "the core of the **calcium-channel-blocker antihypertensive "
     "class** (nifedipine 1975, amlodipine 1990, felodipine, "
     "nicardipine, isradipine, lacidipine).  Atom economy is "
     "high (3 H₂O are the only by-products).  Sets up "
     "Phase 31b's first explicit MCR teaching surface — "
     "complements the existing Knoevenagel + Robinson "
     "annulation cascade entries by going one step further "
     "into the multi-component territory.",
     "O=Cc1ccccc1.CCOC(=O)CC(C)=O.CCOC(=O)CC(C)=O.N"
     ">>CCOC(=O)C1=C(C)NC(C)=C(C(=O)OCC)C1c1ccccc1.O.O.O"),

    # ---- Phase 31b round 182 — Grubbs olefin metathesis ----------
    ("Grubbs olefin metathesis (cross-metathesis of styrene + "
     "1-hexene → 1-phenyl-1-hexene)",
     "Olefin metathesis (Ru-catalysed)",
     "Robert H. Grubbs 1995 (Nobel 2005, with Schrock + "
     "Chauvin) — the **C=C bond shuffling** reaction that "
     "transformed total synthesis.  Two olefins exchange their "
     "alkylidene halves via a metallacyclobutane intermediate "
     "on a ruthenium-carbene catalyst (Grubbs I = "
     "RuCl₂(PCy₃)₂(=CHPh); Grubbs II uses a "
     "dihydroimidazolylidene NHC ligand for higher TON + "
     "wider substrate scope).  Three productive variants: "
     "**cross-metathesis (CM)** between two different alkenes "
     "(this entry), **ring-closing metathesis (RCM)** of a "
     "diene to a cyclic alkene (workhorse of macrocyclisation), "
     "**ring-opening metathesis polymerisation (ROMP)** of a "
     "strained cyclic olefin to a linear polymer.  Functional-"
     "group tolerance is exceptional: alcohols, ethers, esters, "
     "ketones, amines all survive.  Total syntheses driven by "
     "metathesis include Eribulin (Halichondrin B), the "
     "Schreiber Sphingofungin, and most modern macrocyclic "
     "natural-product routes.  **Phase 31b round 182 — fills "
     "the olefin-metathesis gap**, complementing the Pd-"
     "cross-coupling cluster (Suzuki / Heck / Negishi / Stille / "
     "Buchwald-Hartwig / Sonogashira) with Ru-catalysed C=C "
     "bond formation.",
     "C=Cc1ccccc1.CCCCC=C>>CCCCC=Cc1ccccc1.C=C"),

    # ---- Phase 31b round 182 — Wolff-Kishner reduction -----------
    ("Wolff-Kishner reduction (acetophenone → ethylbenzene)",
     "Reduction (carbonyl → methylene)",
     "Ludwig Wolff 1912 + N. M. Kishner 1911 (independently) — "
     "the **strongly basic** route to remove a carbonyl oxygen "
     "and replace C=O with CH₂.  Two-stage mechanism: "
     "(1) hydrazone formation from the ketone + hydrazine "
     "(N₂H₄); (2) base-promoted (KOH) loss of N₂ via a "
     "tautomer / diazene intermediate, with concerted protonation "
     "of carbon, gives the alkane.  Originally a sealed-tube "
     "high-temperature procedure; the Huang-Minlon modification "
     "(diethylene glycol solvent, atmospheric pressure) made it "
     "practical.  **Complementary to Clemmensen reduction** "
     "(Zn(Hg) / HCl, strongly acidic) which targets the same "
     "transformation but in molecules incompatible with strong "
     "base; the Wolff-Kishner is the canonical choice for "
     "acid-sensitive substrates.  Both methods together let "
     "students see how mechanistic context (acid vs base) "
     "drives reagent selection for the same overall functional-"
     "group interconversion.  **Phase 31b round 182 — fills the "
     "non-hydride-reduction gap** (existing reductions are "
     "NaBH4 + Birch + CBS — all hydride or SET).",
     "CC(=O)c1ccccc1>>CCc1ccccc1"),

    # ---- Phase 31b round 182 — Hofmann elimination ---------------
    ("Hofmann elimination (2-pentyltrimethylammonium hydroxide "
     "→ 1-pentene + trimethylamine)",
     "Elimination (anti-Zaitsev / Hofmann's rule)",
     "August Wilhelm Hofmann 1851 — the **anti-Zaitsev** "
     "β-elimination from a quaternary ammonium hydroxide that "
     "preferentially gives the **less-substituted (Hofmann) "
     "alkene** rather than the thermodynamically more-stable "
     "Zaitsev product.  Bulky leaving group (NMe₃) + concerted "
     "syn-periplanar transition state biases the deprotonation "
     "toward the **less hindered β-hydrogen**, so the kinetic "
     "product is the terminal alkene.  Standard procedure: "
     "exhaustive methylation of the amine with MeI (3 ×) gives "
     "the quaternary ammonium iodide; ion exchange to the "
     "hydroxide + thermolysis (~ 100 °C) drives the syn-"
     "elimination.  Diagnostic for amine structure determination "
     "in the pre-NMR era (e.g. alkaloid skeleton mapping).  "
     "**Pedagogical value**: pairs naturally with the existing "
     "E1 + E2 entries to show that elimination regioselectivity "
     "depends on leaving-group bulk + base bulk — Zaitsev for "
     "small leaving groups (Br⁻ in E2), Hofmann for bulky NR₃⁺.  "
     "**Phase 31b round 182 — fills the Hofmann-elimination gap** "
     "and rounds out the elimination subcategory to 3 entries.",
     "CCCC(C)[N+](C)(C)C.[OH-]>>C=CCCC.CN(C)C.O"),

    # ---- Phase 31b round 182 — Ozonolysis ------------------------
    ("Ozonolysis with reductive workup (cis-2-butene + O₃ / "
     "Me₂S → 2 acetaldehyde)",
     "Oxidative cleavage (alkene → carbonyls)",
     "Christian Friedrich Schönbein 1840 (O₃ discovery) + "
     "Carl Harries 1903 (synthetic application) — the "
     "**oxidative cleavage** of a C=C double bond to two "
     "carbonyl fragments.  Two-stage mechanism: (1) [3+2] "
     "cycloaddition of ozone (1,3-dipole) onto the alkene gives "
     "the unstable **molozonide** (primary ozonide); it "
     "rearranges via retro-[3+2] / re-cycloaddition to the "
     "**Criegee ozonide** (1,2,4-trioxolane); (2) workup "
     "determines product oxidation state.  **Reductive workup** "
     "(this entry — Me₂S / Zn-AcOH / PPh₃) gives **aldehydes + "
     "ketones**; **oxidative workup** (H₂O₂) overoxidises "
     "aldehydes to carboxylic acids; **reductive-amination "
     "workup** (NaBH₄) gives alcohols directly.  **Diagnostic "
     "value**: pre-NMR-era structure determination — count the "
     "number of carbonyl fragments to map the position of every "
     "C=C bond in a complex natural product (used to determine "
     "the structure of cholesterol, pyrethrins, and many "
     "terpenes).  **Modern use**: late-stage diversification "
     "in total synthesis, atmospheric chemistry of biogenic VOCs.  "
     "**Phase 31b round 182 — fills the oxidative-cleavage gap** "
     "and rounds out the alkene-reaction cluster (addition-"
     "halogenation + addition-hydrogenation + hydroboration + "
     "now cleavage).",
     "C/C=C\\C.O=[O+][O-]>>CC=O.CC=O"),
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
