"""Seed the glossary of organic-chemistry terms — Phase 11a.

Short (2-4 sentence) definitions with cross-references to other terms.
Categories roll up to the four syllabus sections from the curriculum
matrix (``fundamentals``, ``reactions``, ``spectroscopy``, ``synthesis``)
plus ``mechanism`` and ``lab-technique`` for entries that span them.

Versioned via :data:`SEED_VERSION` so upgrading the app rewrites stale
definitions without a manual migration.
"""
from __future__ import annotations
import json
import logging
from typing import Any, Dict, List

from sqlalchemy import select

from orgchem.db.models import GlossaryTerm
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)

SEED_VERSION = 7


# (term, aliases, category, see_also, definition_md)
_GLOSSARY: List[Dict[str, Any]] = [
    # ---- Fundamentals: bonding & structure -------------------------
    {"term": "Covalent bond", "aliases": [],
     "category": "fundamentals",
     "see_also": ["Sigma bond", "Pi bond", "Lone pair"],
     "definition_md":
        "A chemical bond formed by a **shared pair of electrons** between "
        "two atoms. Most organic bonds are covalent. Strength depends on "
        "orbital overlap and atomic electronegativity."},
    {"term": "Sigma bond", "aliases": ["σ bond"],
     "category": "fundamentals",
     "see_also": ["Pi bond", "Hybridisation"],
     "definition_md":
        "A covalent bond with **cylindrical symmetry about the internuclear "
        "axis**. Every single bond is a σ bond; double and triple bonds "
        "contain one σ plus one or two π components."},
    {"term": "Pi bond", "aliases": ["π bond"],
     "category": "fundamentals",
     "see_also": ["Sigma bond", "Conjugation", "Aromaticity"],
     "definition_md":
        "A covalent bond formed by **side-on overlap of p orbitals**, with "
        "the electron density in two lobes above and below the internuclear "
        "axis. Weaker than σ; responsible for alkene reactivity."},
    {"term": "Hybridisation", "aliases": ["hybridization"],
     "category": "fundamentals",
     "see_also": ["Sigma bond", "VSEPR"],
     "definition_md":
        "Mixing of atomic orbitals (s and p; sometimes d) on one atom to "
        "produce degenerate hybrid orbitals. sp³ → tetrahedral; sp² → "
        "trigonal planar; sp → linear."},
    {"term": "VSEPR", "aliases": ["Valence-Shell Electron-Pair Repulsion"],
     "category": "fundamentals",
     "see_also": ["Hybridisation"],
     "definition_md":
        "A predictive model: electron pairs (bonding and lone) arrange so as "
        "to minimise mutual repulsion. Yields predicted bond angles (109.5°, "
        "120°, 180°) from the electron-domain count."},
    {"term": "Resonance", "aliases": ["mesomerism", "delocalisation"],
     "category": "fundamentals",
     "see_also": ["Conjugation", "Aromaticity"],
     "definition_md":
        "The delocalisation of electrons across multiple equivalent "
        "Lewis structures. The real molecule is a weighted average of all "
        "contributors (not an equilibrium between them)."},
    {"term": "Formal charge", "aliases": [],
     "category": "fundamentals",
     "see_also": ["Resonance"],
     "definition_md":
        "A bookkeeping charge assigned to an atom = valence electrons − "
        "lone-pair electrons − (bonding electrons / 2). Used to track "
        "electron flow in mechanisms and to identify the best resonance "
        "contributors."},
    {"term": "Lone pair", "aliases": ["non-bonding pair"],
     "category": "fundamentals",
     "see_also": ["Formal charge", "Nucleophile"],
     "definition_md":
        "A pair of valence electrons not shared with another atom. Lone "
        "pairs make atoms nucleophilic / basic and contribute to VSEPR "
        "geometry and dipole moment."},
    {"term": "Electronegativity", "aliases": [],
     "category": "fundamentals",
     "see_also": ["Dipole moment"],
     "definition_md":
        "The tendency of an atom to pull bonding electrons toward itself. "
        "On the Pauling scale F > O > N ≈ Cl > Br > C ≈ H. Differences "
        "drive bond polarity and inductive effects."},

    # ---- Fundamentals: stereochemistry -----------------------------
    {"term": "Stereocentre", "aliases": ["stereogenic centre", "chiral centre"],
     "category": "stereochemistry",
     "see_also": ["R/S configuration", "Enantiomer"],
     "definition_md":
        "An atom (usually sp³ carbon) bearing **four different** substituents. "
        "Interchanging any two gives a non-superimposable stereoisomer. The "
        "CIP R/S rules assign a descriptor to each stereocentre."},
    {"term": "R/S configuration", "aliases": ["CIP descriptor"],
     "category": "stereochemistry",
     "see_also": ["Stereocentre", "Enantiomer"],
     "definition_md":
        "Cahn-Ingold-Prelog system: rank the four substituents by atomic "
        "number; view with the lowest-priority group pointing away; "
        "1→2→3 clockwise is **R** (rectus), anticlockwise is **S** (sinister)."},
    {"term": "Enantiomer", "aliases": [],
     "category": "stereochemistry",
     "see_also": ["Diastereomer", "Racemic mixture", "R/S configuration"],
     "definition_md":
        "Non-superimposable mirror-image isomers. They have identical "
        "physical properties except for rotation of plane-polarised light "
        "and interaction with other chiral systems (e.g. receptors, enzymes)."},
    {"term": "Diastereomer", "aliases": [],
     "category": "stereochemistry",
     "see_also": ["Enantiomer", "Meso compound"],
     "definition_md":
        "Stereoisomers that are **not** mirror images. Molecules with ≥2 "
        "stereocentres have 2ⁿ stereoisomers; any pair that isn't an "
        "enantiomer is a diastereomer. Have distinct physical properties."},
    {"term": "Meso compound", "aliases": [],
     "category": "stereochemistry",
     "see_also": ["Diastereomer", "Enantiomer"],
     "definition_md":
        "A molecule with stereocentres but an **internal plane of symmetry** — "
        "so the 'enantiomer' is actually identical (superimposable). Meso "
        "tartaric acid is the textbook case."},
    {"term": "E/Z configuration", "aliases": ["cis/trans alkene"],
     "category": "stereochemistry",
     "see_also": ["R/S configuration", "Pi bond"],
     "definition_md":
        "For disubstituted alkenes: rank the two substituents on each "
        "carbon by CIP; **E** (entgegen, 'opposite') has higher-priority "
        "groups on opposite sides; **Z** (zusammen, 'together') on the same "
        "side. Extends the older cis/trans nomenclature."},
    {"term": "Newman projection", "aliases": [],
     "category": "stereochemistry",
     "see_also": ["Conformation", "Dihedral angle"],
     "definition_md":
        "A view along a C-C bond: the front carbon is a dot, the back is a "
        "circle; each bears three substituents at 120°. Used to visualise "
        "eclipsed vs. staggered conformations."},

    # ---- Mechanism ----------------------------------------------------
    {"term": "Nucleophile", "aliases": ["Nu"],
     "category": "mechanism",
     "see_also": ["Electrophile", "Lone pair", "SN1", "SN2"],
     "definition_md":
        "A species that donates an electron pair to form a new covalent "
        "bond — 'nucleus-loving'. Usually has a lone pair or a π-bond "
        "HOMO. Examples: OH⁻, NH₃, CN⁻, carbanions."},
    {"term": "Electrophile", "aliases": ["E"],
     "category": "mechanism",
     "see_also": ["Nucleophile", "Carbocation", "SN1", "SN2"],
     "definition_md":
        "A species that accepts an electron pair — 'electron-loving'. "
        "Usually has a low-lying LUMO or an empty orbital. Examples: "
        "H⁺, R⁺ (carbocations), R-X (alkyl halides), C=O (carbonyl)."},
    {"term": "SN1", "aliases": ["unimolecular nucleophilic substitution"], "example_smiles": "CC(C)(C)Br.O>>CC(C)(C)O.[H]Br",
     "category": "mechanism",
     "see_also": ["SN2", "Carbocation", "E1"],
     "definition_md":
        "Nucleophilic substitution via a **two-step** mechanism: slow "
        "ionisation to a carbocation, then fast nucleophile capture. "
        "Rate = k[substrate]. Favoured by 3° substrates, polar protic "
        "solvents, and weak nucleophiles. Racemises chiral centres."},
    {"term": "SN2", "aliases": ["bimolecular nucleophilic substitution"], "example_smiles": "CBr.[OH-]>>CO.[Br-]",
     "category": "mechanism",
     "see_also": ["SN1", "Nucleophile"],
     "definition_md":
        "**Concerted** backside attack: the nucleophile hits the C opposite "
        "the leaving group as the C–LG bond breaks. Rate = k[substrate][Nu]. "
        "Favoured by 1° substrates, polar aprotic solvents, strong "
        "nucleophiles. **Inverts** configuration at the stereocentre."},
    {"term": "E1", "aliases": ["unimolecular elimination"], "example_smiles": "CC(C)(C)Br>>C=C(C)C.[H]Br",
     "category": "mechanism",
     "see_also": ["SN1", "E2", "Carbocation"],
     "definition_md":
        "**Two-step** elimination: ionisation to a carbocation, then loss "
        "of a β-proton. Follows Zaitsev (the more-substituted alkene "
        "dominates). Often competes with SN1."},
    {"term": "E2", "aliases": ["bimolecular elimination"], "example_smiles": "CCC(Br)C.[OH-]>>CC=CC.[Br-].O",
     "category": "mechanism",
     "see_also": ["E1", "SN2"],
     "definition_md":
        "**Concerted** elimination: the base removes a β-proton as the "
        "C–LG bond breaks, forming the π bond in one step. Requires "
        "**anti-periplanar** geometry between H and LG."},
    {"term": "Carbocation", "aliases": ["carbenium ion"],
     "example_smiles": "C[C+](C)C",
     "category": "mechanism",
     "see_also": ["SN1", "E1", "Rearrangement"],
     "definition_md":
        "A carbon atom bearing a **formal +1 charge** and only 6 valence "
        "electrons. Planar sp², empty p orbital. Stability: 3° > 2° > 1° > "
        "methyl, stabilised by hyperconjugation and adjacent π/lone pairs."},
    {"term": "Carbanion", "aliases": [], "example_smiles": "[CH3-]",
     "category": "mechanism",
     "see_also": ["Enolate", "Grignard reagent"],
     "definition_md":
        "A carbon atom bearing a **formal −1 charge** and a lone pair. "
        "Tetrahedral sp³. Basicity / nucleophilicity drops with "
        "s-character: sp³ > sp² > sp. Often generated from organolithiums "
        "or by deprotonation α to a carbonyl."},
    {"term": "Curved arrow", "aliases": ["arrow pushing", "electron-flow arrow"],
     "category": "mechanism",
     "see_also": ["Nucleophile", "Electrophile"],
     "definition_md":
        "The notation for **electron flow** in a mechanism: a full curved "
        "arrow moves a **pair** of electrons (from source → destination); "
        "a fishhook moves **one** electron (radical mechanisms)."},
    {"term": "Transition state", "aliases": ["TS", "activated complex"],
     "category": "mechanism",
     "see_also": ["Activation energy", "Reaction coordinate"],
     "definition_md":
        "The highest-energy point along a reaction coordinate — a maximum "
        "in energy but a saddle point in configuration space. Lasts ~10⁻¹⁴ s; "
        "cannot be isolated. Marked ‡ in diagrams."},
    {"term": "Activation energy", "aliases": ["Ea", "Ea‡"],
     "category": "mechanism",
     "see_also": ["Transition state", "Reaction coordinate"],
     "definition_md":
        "The energy barrier between reactants and the transition state. "
        "Determines reaction rate via the Arrhenius equation "
        "k = A·exp(−Ea/RT)."},

    # ---- Reactions ---------------------------------------------------
    {"term": "Aldol reaction", "aliases": ["aldol addition"],
     "category": "reactions",
     "see_also": ["Enolate", "Claisen condensation"],
     "example_smiles": "CC(=O)C.CC=O>>CC(=O)CC(O)C",
     "definition_md":
        "Addition of an enolate to an aldehyde / ketone to give a β-hydroxy "
        "carbonyl. Under basic + warm conditions the product dehydrates "
        "(aldol *condensation*) to an α,β-unsaturated enone."},
    {"term": "Diels-Alder reaction", "aliases": ["[4+2] cycloaddition"],
     "category": "reactions",
     "see_also": ["Pericyclic", "Conjugation"],
     "example_smiles": "C=CC=C.C=C",
     "definition_md":
        "Concerted [4+2] cycloaddition of a conjugated diene and a "
        "dienophile to give a cyclohexene. Thermally allowed (Woodward-"
        "Hoffmann), suprafacial-suprafacial, stereospecific."},
    {"term": "Friedel-Crafts alkylation", "aliases": ["FC alkylation"], "example_smiles": "c1ccccc1.CCBr>>CCc1ccccc1.[H]Br",
     "category": "reactions",
     "see_also": ["EAS", "Carbocation"],
     "definition_md":
        "Alkylation of an aromatic ring via an R⁺ equivalent (from R-X + "
        "Lewis acid). Prone to carbocation rearrangement and over-"
        "alkylation; doesn't work with deactivated rings."},
    {"term": "EAS", "aliases": ["electrophilic aromatic substitution"], "example_smiles": "c1ccccc1.O=[N+]([O-])O>>[O-][N+](=O)c1ccccc1.O",
     "category": "reactions",
     "see_also": ["Friedel-Crafts alkylation", "Aromaticity"],
     "definition_md":
        "Reaction class in which an aromatic ring attacks an electrophile, "
        "giving a cationic arenium intermediate that deprotonates back to "
        "the aromatic. Nitration, halogenation, sulfonation, FC alkylation/"
        "acylation are all EAS."},
    {"term": "Aromaticity", "aliases": ["Hückel aromaticity"],
     "category": "reactions",
     "see_also": ["Pi bond", "Resonance", "EAS"],
     "example_smiles": "c1ccccc1",
     "definition_md":
        "A cyclic, fully conjugated, planar π-system with **4n+2** π "
        "electrons (Hückel's rule) is aromatic — dramatically stabilised "
        "relative to the open-chain reference. Antiaromatic = 4n electrons."},

    # ---- Synthesis ---------------------------------------------------
    {"term": "Retrosynthesis", "aliases": ["retrosynthetic analysis"], "example_smiles": "CC(=O)Oc1ccccc1C(=O)O>>CC(=O)O.O=C(O)c1ccccc1O",
     "category": "synthesis",
     "see_also": ["Synthon", "Disconnection"],
     "definition_md":
        "A design strategy introduced by Corey: work **backwards** from "
        "the target molecule, breaking it into simpler precursors at each "
        "step until commercially available starting materials remain. "
        "Uses ⟹ (open arrow) to denote a disconnection."},
    {"term": "Atom economy", "aliases": ["AE"],
     "category": "synthesis",
     "see_also": ["E-factor", "Green chemistry"],
     "definition_md":
        "The mass fraction of the reactants that ends up in the desired "
        "product (Trost 1991). AE = MW(product) / Σ MW(reactants) × 100 %. "
        "Independent of yield — a feature of the balanced equation."},
    {"term": "E-factor", "aliases": [],
     "category": "synthesis",
     "see_also": ["Atom economy", "Green chemistry"],
     "definition_md":
        "Sheldon's metric: mass of waste per mass of product. Fine "
        "chemicals 25–100; pharma 25+; petrochemicals <0.1. Lower is "
        "better. Includes solvents and water."},
    {"term": "Green chemistry", "aliases": ["sustainable chemistry"],
     "category": "synthesis",
     "see_also": ["Atom economy", "E-factor"],
     "definition_md":
        "A design philosophy (Anastas + Warner, 1998) minimising "
        "environmental impact — atom economy, benign solvents, catalysis, "
        "renewable feedstocks, biodegradability."},

    # ---- Spectroscopy ------------------------------------------------
    {"term": "NMR spectroscopy", "aliases": ["nuclear magnetic resonance"],
     "category": "spectroscopy",
     "see_also": ["Chemical shift", "Coupling constant"],
     "definition_md":
        "Technique that detects atoms with nuclear spin (¹H, ¹³C, …) via "
        "their resonance frequency in a magnetic field. Reveals the carbon "
        "skeleton, functional groups, and stereochemistry."},
    {"term": "Chemical shift", "aliases": ["δ", "ppm"],
     "category": "spectroscopy",
     "see_also": ["NMR spectroscopy"],
     "definition_md":
        "NMR resonance frequency relative to a reference (TMS), normalised "
        "by the spectrometer frequency, reported in ppm. Reflects the "
        "local electronic environment of the nucleus."},
    {"term": "IR spectroscopy", "aliases": ["infrared spectroscopy"],
     "category": "spectroscopy",
     "see_also": ["NMR spectroscopy"],
     "definition_md":
        "Absorption of IR photons by vibrational modes. Characteristic "
        "bands (C=O 1700, O-H 3400, C-H 2900 cm⁻¹) identify functional "
        "groups; the 'fingerprint region' (<1500) uniquely identifies the "
        "molecule."},

    # ---- Lab techniques ----------------------------------------------
    {"term": "Chromatography", "aliases": [],
     "category": "lab-technique",
     "see_also": ["TLC", "Extraction"],
     "definition_md":
        "Any separation based on differential partitioning between a "
        "mobile and a stationary phase. Organic-chem variants: TLC, "
        "column, HPLC, GC. Polar stationary + polar mobile moves polar "
        "compounds faster (normal phase)."},
    {"term": "TLC", "aliases": ["thin-layer chromatography"],
     "category": "lab-technique",
     "see_also": ["Chromatography"],
     "definition_md":
        "Silica-coated plate dipped in a mobile-phase solvent; compounds "
        "move up by capillary action. Rf = distance moved / solvent front. "
        "Used to monitor reactions and test column fractions."},
    {"term": "Recrystallisation", "aliases": ["recrystallization"],
     "category": "lab-technique",
     "see_also": ["Extraction"],
     "definition_md":
        "Purification by dissolving the crude in a hot solvent in which "
        "the product is sparingly soluble, filtering while hot, then "
        "letting the solution cool so pure product crystallises out while "
        "impurities stay in solution."},
    {"term": "Extraction", "aliases": ["liquid-liquid extraction"],
     "category": "lab-technique",
     "see_also": ["Chromatography"],
     "definition_md":
        "Separation of a compound from a mixture by differential solubility "
        "between two immiscible phases (usually organic + aqueous), shaken "
        "in a separatory funnel. Acid-base extractions exploit pKa to "
        "partition ionisable species."},

    # ---- Enzyme mechanisms (round 31) --------------------------------
    {"term": "Catalytic triad", "aliases": ["Ser-His-Asp triad"],
     "category": "enzyme-mechanism",
     "see_also": ["Serine protease", "General base catalysis",
                  "Chymotrypsin"],
     "definition_md":
        "Three active-site residues acting in concert, classically "
        "**Ser-His-Asp** in the serine proteases. Asp orients and "
        "stabilises His; His acts as a general base to deprotonate the "
        "Ser hydroxyl; the resulting Ser alkoxide is the nucleophile. "
        "Same logic with Cys-His-Asn in cysteine proteases."},
    {"term": "General acid-base catalysis",
     "aliases": ["general acid catalysis", "general base catalysis"],
     "category": "enzyme-mechanism",
     "see_also": ["Catalytic triad", "pKa"],
     "definition_md":
        "A proton is transferred to / from the substrate by a *specific* "
        "functional group (often a His side chain at physiological pH, "
        "pKa ≈ 6–7) in the rate-determining step. Distinct from *specific* "
        "acid/base catalysis, where the proton comes from bulk H⁺ or OH⁻."},
    {"term": "Aspartic protease", "aliases": ["acid protease"],
     "category": "enzyme-mechanism",
     "see_also": ["HIV protease", "Water-mediated catalysis",
                  "General acid-base catalysis"],
     "definition_md":
        "Protease family using two active-site aspartates to activate a "
        "bound water for attack on the scissile peptide carbonyl. One Asp "
        "acts as a general base (deprotonates water), the other as a "
        "general acid (protonates the leaving amine). HIV protease, "
        "pepsin, renin are canonical examples."},
    {"term": "Oxyanion hole", "aliases": [],
     "category": "enzyme-mechanism",
     "see_also": ["Tetrahedral intermediate", "Serine protease"],
     "definition_md":
        "A pocket of backbone N-H groups positioned to hydrogen-bond to "
        "the developing negative charge on the carbonyl oxygen during the "
        "tetrahedral intermediate of protease catalysis. Lowers the "
        "transition-state energy by stabilising the oxyanion."},
    {"term": "In-line phosphoryl transfer",
     "aliases": ["SN2 at phosphorus", "in-line attack"],
     "category": "enzyme-mechanism",
     "see_also": ["RNase A", "Transition state",
                  "General acid-base catalysis"],
     "definition_md":
        "An SN2-like mechanism at a phosphorus centre: the nucleophile "
        "attacks opposite to the leaving group, so the phosphorus passes "
        "through a trigonal-bipyramidal transition state with inversion. "
        "RNase A, ribozymes, and most kinases operate this way."},
    {"term": "Covalent intermediate", "aliases": ["acyl-enzyme"], "example_smiles": "CC(=O)OCC",
     "category": "enzyme-mechanism",
     "see_also": ["Serine protease", "Chymotrypsin",
                  "Tetrahedral intermediate"],
     "definition_md":
        "A short-lived covalent adduct between enzyme and substrate, "
        "formed en route to product. In serine proteases the covalent "
        "intermediate is an **acyl-enzyme** (Ser-O-C(=O)R), hydrolysed "
        "in a second cycle. Diagnostic of double-displacement kinetics."},
    {"term": "Schiff base", "aliases": ["imine", "enamine form"], "example_smiles": "CC(C)=NC",
     "category": "enzyme-mechanism",
     "see_also": ["Aldolase class I", "Enamine"],
     "definition_md":
        "The C=N formed when a primary amine attacks a carbonyl and "
        "dehydrates. Class-I aldolases use the ε-amino of an active-site "
        "lysine to form a Schiff base with DHAP; tautomerisation to the "
        "enamine provides the nucleophile that attacks the aldehyde "
        "substrate."},
    {"term": "Tetrahedral intermediate", "aliases": [], "example_smiles": "CC(O)([O-])C",
     "category": "enzyme-mechanism",
     "see_also": ["Oxyanion hole", "Chymotrypsin", "Aldol reaction"],
     "definition_md":
        "The sp³ addition adduct formed when a nucleophile attacks an "
        "sp² carbonyl carbon but before the C=O is re-formed and a "
        "leaving group departs. Often the rate-determining step in "
        "carbonyl chemistry; stabilised by the oxyanion hole in protease "
        "active sites."},

    # ---- Phase 31f content expansion (2026-04-23) ------------------
    {"term": "Kinetic vs thermodynamic control", "aliases": [],
     "category": "mechanism",
     "see_also": ["Hammond postulate", "Reaction coordinate"],
     "definition_md":
        "When a reaction can give more than one product, **kinetic** "
        "control favours the product with the lowest activation barrier "
        "(formed fastest) — usually at low temperature / short time. "
        "**Thermodynamic** control favours the most stable product "
        "(lowest ΔG) — usually at high temperature / long time (allowing "
        "equilibration). Classic example: 1,2- vs 1,4-addition of HBr "
        "to butadiene (1,2 kinetic, 1,4 thermodynamic)."},
    {"term": "Hammond postulate", "aliases": [],
     "category": "mechanism",
     "see_also": ["Kinetic vs thermodynamic control", "Transition state",
                  "Reaction coordinate"],
     "definition_md":
        "The transition state of a step resembles the species (reactant "
        "or product) **closer to it in energy**. So endothermic steps "
        "have *late* (product-like) TS's; exothermic steps have *early* "
        "(reactant-like) TS's. Lets you predict selectivity and "
        "structure–reactivity trends from thermodynamic data alone."},
    {"term": "Markovnikov's rule", "aliases": ["Markovnikov",
                                                "anti-Markovnikov"],
     "category": "reactions",
     "example_smiles": "CC=C.[H]Br>>CC(Br)C",
     "see_also": ["Carbocation stability", "Hyperconjugation",
                  "Radical addition"],
     "definition_md":
        "In H–X addition to an unsymmetrical alkene, the hydrogen goes "
        "to the carbon **bearing more hydrogens**, and X goes to the "
        "more-substituted carbon — because that route proceeds through "
        "the more stable carbocation. **Anti-Markovnikov** addition "
        "(e.g. HBr with peroxides via radicals; hydroboration / "
        "oxidation) inverts the regiochemistry."},
    {"term": "Zaitsev's rule", "aliases": ["Saytzeff", "Zaitsev"],
     "category": "reactions",
     "example_smiles": "CCC(Br)C>>CC=CC",
     "see_also": ["E2", "E1", "Hofmann elimination"],
     "definition_md":
        "In elimination reactions, the **most substituted (most stable) "
        "alkene** is the major product. Stabilisation comes from "
        "hyperconjugation and alkyl-donor effects. **Hofmann's rule** "
        "(opposite regiochemistry: less substituted alkene) kicks in "
        "with bulky bases (e.g. potassium *tert*-butoxide) or when the "
        "leaving group is a quaternary ammonium — steric / stereochem "
        "constraints override the thermodynamic preference."},
    {"term": "Anti-periplanar", "aliases": [],
     "category": "stereochemistry",
     "see_also": ["E2", "Newman projection", "Staggered",
                  "Dihedral angle"],
     "definition_md":
        "A dihedral angle of **180°** — the H and the leaving group lie "
        "on opposite sides of the C–C axis in a Newman projection. E2 "
        "eliminations require this geometry because the breaking C–H σ "
        "must align with the breaking C–LG σ* to form the new π bond. "
        "Explains why *meso*- and *dl*- diastereomers can give different "
        "alkene geometries under E2."},
    {"term": "Baldwin's rules", "aliases": [],
     "category": "mechanism",
     "see_also": ["Ring closure", "Cyclisation", "Hybridisation"],
     "definition_md":
        "Empirical rules for predicting the **feasibility of ring-closing "
        "reactions**, coded as *n-endo-X* vs *n-exo-X* where `n` is the "
        "ring size, *exo*/*endo* tells which side of the breaking bond "
        "is in the ring, and X = tet/trig/dig for the hybridisation of "
        "the attacked atom. Key predictions: **3-7-exo-tet, 3-7-exo-trig, "
        "5-7-endo-dig are favoured**; **5-endo-trig, 3-5-endo-dig are "
        "disfavoured**. Based on whether the nucleophile can approach at "
        "the required Bürgi-Dunitz angle."},
    {"term": "Chemoselectivity", "aliases": [],
     "category": "synthesis",
     "see_also": ["Regioselectivity", "Stereoselectivity",
                  "Protecting group"],
     "definition_md":
        "Preferential reaction at **one functional group in the "
        "presence of others**. E.g. NaBH₄ reduces aldehydes / ketones "
        "but leaves esters / amides untouched — chemoselective for the "
        "most reactive carbonyl. Achieving chemoselectivity without a "
        "protecting-group strategy is a hallmark of elegant synthesis."},
    {"term": "Bioisostere", "aliases": [],
     "category": "medicinal-chemistry",
     "example_smiles": "c1ccc(C(=O)O)cc1",
     "see_also": ["Pharmacophore", "SAR", "Drug-likeness"],
     "definition_md":
        "A group that **replaces another with similar biological "
        "properties** but different chemistry — letting medicinal "
        "chemists tune potency, metabolism, or permeability without "
        "losing binding. Classical examples: carboxylic acid ↔ "
        "tetrazole, methyl ↔ trifluoromethyl, phenyl ↔ thiophene, "
        "amide ↔ sulfonamide. See the *Tools → Medicinal chemistry → "
        "Bioisosteres* dialog for the full catalogue."},
]


# Phase 31f follow-up: additional terms live in a sibling module to
# keep this file near the project's 500-line soft cap. Extend in place
# so the seeding logic below doesn't have to care.
from orgchem.db.seed_glossary_extra import EXTRA_TERMS
_GLOSSARY.extend(EXTRA_TERMS)


def seed_glossary_if_empty(force: bool = False) -> int:
    """Populate / update glossary terms additively.

    Each row is keyed by ``term``; an existing term is overwritten only if
    its stored ``definition_md`` differs or ``force=True``. New terms are
    always inserted.
    """
    updated = 0
    with session_scope() as s:
        existing_rows = {r.term: r for r in s.scalars(
            select(GlossaryTerm)).all()}
        for entry in _GLOSSARY:
            term = entry["term"]
            row = existing_rows.get(term)
            example_smiles = entry.get("example_smiles") or None
            example_figure_path = entry.get("example_figure_path") or None
            if row is None:
                s.add(GlossaryTerm(
                    term=term,
                    aliases_json=json.dumps(entry.get("aliases", [])),
                    definition_md=entry["definition_md"],
                    category=entry.get("category"),
                    see_also_json=json.dumps(entry.get("see_also", [])),
                    example_ids_json=None,
                    example_smiles=example_smiles,
                    example_figure_path=example_figure_path,
                ))
                updated += 1
                continue
            needs_update = (
                force
                or row.definition_md != entry["definition_md"]
                or (row.category or "") != (entry.get("category") or "")
                or (row.example_smiles or "") != (example_smiles or "")
                or (row.example_figure_path or "")
                   != (example_figure_path or "")
            )
            if needs_update:
                row.aliases_json = json.dumps(entry.get("aliases", []))
                row.definition_md = entry["definition_md"]
                row.category = entry.get("category")
                row.see_also_json = json.dumps(entry.get("see_also", []))
                row.example_smiles = example_smiles
                row.example_figure_path = example_figure_path
                updated += 1
    log.info("Seeded / updated %d glossary terms (version %d)",
             updated, SEED_VERSION)
    return updated
