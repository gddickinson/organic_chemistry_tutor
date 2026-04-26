"""Phase 31f continued-expansion glossary terms.

Kept out of `seed_glossary.py` so the main seed file stays at a
manageable size (it was already pushing the project's 500-line soft
cap). The main module imports ``EXTRA_TERMS`` from here and appends
them to its ``_GLOSSARY`` list before seeding, so the additive
upgrade path and SEED_VERSION rewrite semantics are unchanged.

Each entry uses the same schema as `_GLOSSARY`: a dict with
``term`` / ``aliases`` / ``category`` / ``see_also`` /
``definition_md`` keys, plus optional ``example_smiles`` for the
Phase 26a figure pipeline.
"""
from __future__ import annotations
from typing import Any, Dict, List


EXTRA_TERMS: List[Dict[str, Any]] = [
    # ---- Mechanism / stereochemistry follow-ups (round 46) ----------
    {"term": "Saytzeff / Hofmann product",
     "aliases": ["Zaitsev product", "Hofmann product"],
     "category": "reactions",
     "see_also": ["Zaitsev's rule", "E2", "E1"],
     "definition_md":
        "The **Saytzeff (Zaitsev) product** is the most-substituted "
        "alkene in an elimination — thermodynamically favoured. The "
        "**Hofmann product** is the least-substituted alkene — "
        "kinetically favoured when the base or leaving group is bulky "
        "(*tert*-butoxide, quaternary ammonium). Framing helps predict "
        "regiochemistry from reagent choice alone."},
    {"term": "Bürgi-Dunitz angle",
     "aliases": [],
     "category": "mechanism",
     "see_also": ["Nucleophilic addition", "Baldwin's rules"],
     "definition_md":
        "The **107° trajectory** at which a nucleophile optimally "
        "attacks a C=O carbonyl — aligned with the π* orbital's "
        "backside lobe. Not 90°, because the carbonyl oxygen's lone "
        "pairs occupy the in-plane region. Explains the stereochemistry "
        "of 1,2-additions and underpins Baldwin's rules for ring closure."},
    {"term": "Kinetic isotope effect",
     "aliases": ["KIE", "primary KIE", "secondary KIE"],
     "category": "mechanism",
     "see_also": ["Transition state", "Rate-determining step"],
     "definition_md":
        "The **rate ratio k_H/k_D** when a C–H bond is replaced by C–D. "
        "Primary KIE (2–8) diagnoses C–H cleavage in the RDS — the "
        "deuterium's heavier mass lowers the zero-point energy more for "
        "the ground state than for the TS. Secondary KIE (1.0–1.3) is "
        "a finer probe of hybridisation change adjacent to the reacting "
        "centre."},
    # ---- Pericyclic & frontier MO language --------------------------
    {"term": "HOMO / LUMO",
     "aliases": ["frontier molecular orbitals", "FMO"],
     "category": "mechanism",
     "see_also": ["Woodward-Hoffmann", "Diels-Alder",
                  "Orbital symmetry"],
     "definition_md":
        "**HOMO** = highest occupied, **LUMO** = lowest unoccupied. "
        "In Fukui's frontier-MO theory, the dominant interaction in a "
        "concerted reaction is HOMO(Nu) ↔ LUMO(E). Tighter energy match "
        "→ faster reaction. Explains why electron-rich dienes react "
        "faster with electron-poor dienophiles (normal-demand Diels-"
        "Alder)."},
    {"term": "Endo rule (Alder endo rule)",
     "aliases": ["endo rule", "secondary orbital interaction"],
     "category": "reactions",
     "see_also": ["Diels-Alder", "HOMO / LUMO"],
     "definition_md":
        "In Diels-Alder cycloadditions, the *endo* product — where the "
        "dienophile's EWG points **under** the diene — is kinetically "
        "favoured despite being more sterically strained. Traditionally "
        "explained by secondary orbital interactions (additional "
        "HOMO-LUMO overlap between the EWG π* and diene HOMO); modern "
        "analyses also invoke dispersion forces. *Exo* may dominate at "
        "higher temperatures (thermodynamic control)."},
    # ---- Conformational analysis ------------------------------------
    {"term": "Gauche interaction",
     "aliases": ["gauche"],
     "category": "stereochemistry",
     "see_also": ["Anti-periplanar", "Newman projection",
                  "Staggered"],
     "definition_md":
        "A **60° dihedral** between two substituents on adjacent sp³ "
        "carbons — staggered but destabilised relative to *anti* (180°) "
        "by ~3.8 kJ/mol in butane. Gauche pentane / gauche penalty drives "
        "conformational preferences in flexible chains. The *gauche "
        "effect* — where electronegative substituents prefer gauche over "
        "anti — is a hyperconjugation-driven exception (e.g. 1,2-"
        "difluoroethane)."},
    {"term": "A-value (axial-equatorial preference)",
     "aliases": ["A value", "conformational free energy"],
     "category": "stereochemistry",
     "see_also": ["Cyclohexane chair", "Gauche interaction"],
     "definition_md":
        "The **ΔG° (kJ/mol) penalty for placing a substituent axial "
        "on cyclohexane**, relative to equatorial. Big groups → big A "
        "values: H = 0, Me ≈ 7, Et ≈ 7.5, iPr ≈ 9, tBu ≈ 20 (ring flip "
        "essentially locked). Ph ≈ 12, OH ≈ 2.2. Summing A values "
        "predicts the dominant chair of a polysubstituted ring."},
    # ---- Medicinal chemistry ----------------------------------------
    {"term": "Pharmacophore",
     "aliases": [],
     "category": "medicinal-chemistry",
     "see_also": ["Bioisostere", "SAR", "Drug-likeness"],
     "definition_md":
        "The **abstract 3D arrangement of features** — H-bond donors / "
        "acceptors, aromatic rings, hydrophobes, ionisable centres — "
        "that a ligand needs to bind a given target. Pharmacophores are "
        "chemistry-agnostic: many different scaffolds can hit the same "
        "pharmacophore. Used to cluster a SAR series and to seed "
        "virtual-screening queries."},
    {"term": "Prodrug",
     "aliases": [],
     "category": "medicinal-chemistry",
     "see_also": ["Bioisostere", "Pharmacokinetics"],
     "definition_md":
        "An inactive compound that is metabolised into the active drug "
        "in vivo. Used to fix problems the final drug can't solve on "
        "its own — poor solubility (fosphenytoin → phenytoin), poor "
        "oral absorption (enalapril → enalaprilat), CNS penetration "
        "(L-DOPA → dopamine), or selective tissue targeting (oseltamivir "
        "phosphate → oseltamivir carboxylate)."},
    # ---- Spectroscopy / data analysis -------------------------------
    {"term": "Coupling constant (J)",
     "aliases": ["J value", "NMR coupling"],
     "category": "spectroscopy",
     "see_also": ["Chemical shift", "NMR"],
     "definition_md":
        "The **through-bond splitting (Hz)** of an NMR signal by a "
        "neighbouring magnetic nucleus. Vicinal ³J_HH depends on "
        "dihedral via the **Karplus equation**: 0° → ~9 Hz, 90° → ~0 "
        "Hz, 180° → ~12 Hz. Diagnostic values: cis-alkene ³J ≈ 6-12, "
        "trans-alkene ³J ≈ 12-18, axial-axial cyclohexane ~8-10, "
        "axial-equatorial ~2-3 Hz. Lets NMR fingerprint stereo + "
        "conformation without a crystal."},
    # ---- Round 63 gap-closers: mechanism / stereo fundamentals ------
    {"term": "Hyperconjugation",
     "aliases": ["σ-conjugation", "no-bond resonance"],
     "category": "mechanism",
     "see_also": ["Carbocation", "Resonance", "Gauche interaction",
                  "Inductive effect"],
     "definition_md":
        "Stabilisation by **donation of σ(C–H) or σ(C–C) electrons into "
        "an adjacent empty (or partially filled) π* / p orbital.** The "
        "canonical case: a β-C–H σ pair stabilises a carbocation by "
        "donating into the empty p orbital, drawn as a *no-bond* "
        "resonance structure (H⁺ / C=C). Hyperconjugation explains why "
        "tertiary cations > secondary > primary, why more-substituted "
        "alkenes are thermodynamically favoured (Zaitsev), and the "
        "anomeric effect in sugars. Distinct from π-resonance — the "
        "donor orbital is a σ bond, not a lone pair or π.",
     "example_smiles": "CC(C)(C)[CH2+]"},
    {"term": "Inductive effect",
     "aliases": ["σ-induction", "electron-withdrawing group",
                 "electron-donating group", "EWG", "EDG"],
     "category": "mechanism",
     "see_also": ["Hyperconjugation", "Resonance", "Electronegativity",
                  "Hammett postulate"],
     "definition_md":
        "**Propagation of bond polarity through σ bonds**, falling off "
        "rapidly with distance (~½ per bond). Fluorine and -NO₂ pull "
        "electron density toward themselves (−I, electron-withdrawing); "
        "alkyl groups push density away (+I, electron-donating). "
        "Inductive effects rationalise pKa trends — acetic acid "
        "(pKa 4.76) vs trifluoroacetic acid (pKa 0.23) vs fluoroacetic "
        "(2.6), chloroacetic (2.9) — and work alongside resonance to "
        "explain substituent impact on aromatic rings (σₘ vs σₚ in the "
        "Hammett correlation)."},
    {"term": "Leaving group",
     "aliases": ["LG", "nucleofuge"],
     "category": "mechanism",
     "see_also": ["SN1", "SN2", "E1", "E2", "pKa"],
     "definition_md":
        "The atom or group that **departs with the bonding electron "
        "pair** when a C–X σ bond breaks in a substitution or "
        "elimination. Good leaving groups are **stable as anions** — "
        "usually the conjugate bases of strong acids (I⁻ > Br⁻ > Cl⁻ > "
        "TsO⁻ ≈ MsO⁻ ≈ TfO⁻ >> F⁻; H₂O (from protonated –OH) >> HO⁻; "
        "N₂ from a diazonium is effectively irreversible). Rule of "
        "thumb: *LG ability tracks the pKa of its conjugate acid* — "
        "lower pKa ⇒ better LG. Hydroxide and alkoxide are poor LGs "
        "directly; they must be activated (protonation, tosylation, "
        "Appel / Mitsunobu conditions) first."},
    {"term": "Enantiomeric excess",
     "aliases": ["ee", "optical purity", "enantiopurity"],
     "category": "stereochemistry",
     "see_also": ["Enantiomer", "Racemate",
                  "Asymmetric synthesis", "R/S configuration"],
     "definition_md":
        "**ee (%) = 100 × (|R − S|) / (R + S)** — the scalar measure "
        "of how asymmetric a chiral sample is. 0 % ee is a racemate; "
        "100 % ee is enantiopure. A sample with 90 % ee is 95 % of one "
        "enantiomer and 5 % of the other (mixture is 95:5). ee is the "
        "canonical metric for asymmetric catalysis (e.g. Sharpless AD, "
        "CBS reduction — both target ≥ 95 % ee for pharmaceutical use). "
        "Measured by chiral HPLC, chiral-shift NMR, or specific "
        "rotation relative to the pure enantiomer. Related: "
        "diastereomeric excess (de) for diastereomer mixtures."},
    {"term": "Keto-enol tautomerism",
     "aliases": ["tautomer", "enol form", "keto form",
                 "tautomerisation"],
     "category": "mechanism",
     "see_also": ["Aldol reaction", "Enolate", "Schiff base",
                  "Michael addition"],
     "definition_md":
        "Rapid **proton-transfer equilibrium** between a carbonyl "
        "(keto form, C=O + α-CH) and its enol (C(OH)=C) constitutional "
        "isomer. Simple ketones sit ~10⁻⁶ toward enol (acetone's enol "
        "content is ~0.0001 %), but 1,3-diketones (acetylacetone) are "
        "~85 % enol because the enol is stabilised by conjugation + "
        "intramolecular H-bonding. The α-H ⇌ enol-OH swap underlies "
        "α-halogenation, aldol / Claisen, enamine chemistry, and the "
        "reactivity of enolates. Acid- or base-catalysed — neither "
        "route goes through a carbocation.",
     "example_smiles": "CC(=O)C>>C=C(O)C"},
    {"term": "Homolysis vs heterolysis",
     "aliases": ["bond cleavage", "radical cleavage",
                 "ionic cleavage"],
     "category": "mechanism",
     "see_also": ["Free radical", "Fishhook arrow", "Curved arrow",
                  "Carbocation", "Carbanion"],
     "definition_md":
        "Two modes of breaking a covalent bond. **Homolysis**: the "
        "bond splits evenly — each fragment takes one electron, "
        "giving two **radicals**. Shown with *fishhook* (single-"
        "barbed) arrows. Favoured by weak, nonpolar bonds under heat "
        "/ UV / radical initiators (Cl₂ → 2 Cl• under hν). "
        "**Heterolysis**: both electrons leave with one fragment, "
        "giving a **cation + anion** pair. Shown with full curly "
        "arrows. Favoured by polar bonds in polar / ionising media "
        "(t-BuCl → t-Bu⁺ + Cl⁻ in water). The arrow notation tells "
        "the reader which regime is being invoked."},
    {"term": "Walden inversion",
     "aliases": ["inversion of configuration",
                 "umbrella flip"],
     "category": "stereochemistry",
     "see_also": ["SN2", "Stereocentre", "R/S configuration"],
     "definition_md":
        "The **umbrella-style inversion** of an sp³ carbon's geometry "
        "when a nucleophile attacks opposite the leaving group in an "
        "SN2. Incoming Nu forms its bond 180° from the departing LG; "
        "the three other substituents flip from one face of the "
        "carbon to the other — like an umbrella in a gust. If the "
        "carbon was a stereocentre, the CIP descriptor typically "
        "switches (R ↔ S, though not always — it depends on CIP "
        "priority rankings of Nu vs LG). The stereo-signature of SN2 "
        "(vs racemisation in SN1) and the reason 2° alkyl halides "
        "with a chiral α-carbon invert cleanly under azide / cyanide "
        "/ hydroxide."},
    {"term": "Anomer",
     "aliases": ["α-anomer", "β-anomer", "anomeric centre",
                 "anomeric carbon"],
     "category": "stereochemistry",
     "see_also": ["Diastereomer", "Carbohydrate",
                  "Mutarotation", "Pyranose", "Furanose"],
     "definition_md":
        "The pair of **cyclic sugar diastereomers that differ only "
        "at the hemiacetal (anomeric) carbon** — C1 of an aldose, C2 "
        "of a ketose. The anomeric OH is **axial in α**, "
        "**equatorial in β** for a D-pyranose drawn in the standard "
        "chair. α-D-glucopyranose (36 %) ⇌ β-D-glucopyranose (64 %) "
        "in aqueous solution via the open-chain aldehyde — the "
        "phenomenon of **mutarotation**. The **anomeric effect** "
        "(preference for electronegative axial substituents at the "
        "anomeric C) is explained by n_O → σ*_{C-X} hyperconjugation, "
        "not by simple sterics."},
    # ---- Round 77: EAS + selectivity (close Phase 31f at 80) ---
    {"term": "Activating and deactivating groups",
     "aliases": ["EAS directing effects", "ortho-para director",
                 "meta director", "directing group",
                 "-EDG", "-EWG"],
     "category": "reactions",
     "see_also": ["EAS", "Friedel-Crafts alkylation", "Nitration",
                  "Inductive effect", "Resonance", "Hyperconjugation",
                  "Hammett postulate"],
     "definition_md":
        "Substituents on an aromatic ring classified by how they "
        "**bias electrophilic aromatic substitution** — both the "
        "*rate* (activation vs deactivation) and the *regiochemistry* "
        "(ortho/para vs meta).\n\n"
        "**Activators** (π-donors): –NH₂, –NHR, –OH, –OR, –NHCOR, "
        "–alkyl.  They raise the ring's HOMO, push electrons onto "
        "ortho + para positions via resonance, and speed EAS up by "
        "orders of magnitude.  Regio: **ortho/para directors**.\n\n"
        "**Deactivators** (σ-withdrawers or π-acceptors): –NO₂, "
        "–CN, –COR, –COOH, –SO₃H, –CF₃, –NR₃⁺.  They lower the "
        "HOMO, make EAS slower, and *deactivate every position* — "
        "but the ortho + para sites suffer the biggest energy "
        "penalty (direct conjugation with the EWG), so attack "
        "sneaks in **meta**.  Regio: **meta directors**.\n\n"
        "Halogens (–F, –Cl, –Br, –I) are the famous exception: "
        "σ-withdrawing (so slightly *deactivating*) but π-donating "
        "by resonance with lone pairs (so still **ortho/para "
        "directors**).  The Hammett σₚ constants quantify this: "
        "positive σ = deactivating, negative σ = activating."},
    {"term": "Regioselectivity",
     "aliases": ["regioselective", "regiochemistry",
                 "positional selectivity"],
     "category": "reactions",
     "see_also": ["Markovnikov's rule", "Saytzeff / Hofmann product",
                  "Activating and deactivating groups",
                  "Chemoselectivity", "Kinetic vs thermodynamic control"],
     "definition_md":
        "When a reaction could form **two or more constitutional "
        "isomers** that differ in *where* the new bond lands, the "
        "preference for one is its **regioselectivity**.  Distinct "
        "from:\n\n"
        "* **Chemoselectivity** — choice between different *functional "
        "  groups* on the same molecule (e.g. a reducing agent that "
        "  hits the ketone but leaves the ester alone).\n"
        "* **Stereoselectivity** — choice between *stereoisomers* "
        "  (R vs S, cis vs trans).\n\n"
        "Canonical regiochemistry-driven rules in the seeded "
        "content: Markovnikov (H adds to the carbon with more H's "
        "already on it in alkene hydration), Saytzeff / Zaitsev "
        "(most-substituted alkene in E1 / E2), ortho/para vs meta "
        "directing in EAS, and the 1,2- vs 1,4-addition split in "
        "conjugated dienes (Diels-Alder / Michael).  A reaction is "
        "**regiospecific** only when a single regioisomer is "
        "obtained mechanistically (e.g. Diels-Alder endo-orbital "
        "alignment pinning ortho + para products)."},
    {"term": "Constitutional isomer",
     "aliases": ["structural isomer", "constitutional isomers"],
     "category": "stereochemistry",
     "see_also": ["Isomerism", "Stereoisomer", "Regiochemistry",
                  "Tautomer", "Enantiomer", "Diastereomer"],
     "definition_md":
        "Molecules with the **same molecular formula but different "
        "atom connectivity**.  The most fundamental flavour of "
        "isomerism — everything else (stereoisomers, tautomers, "
        "rotamers) assumes connectivity is already fixed.\n\n"
        "Four sub-types to keep straight:\n\n"
        "1. **Chain / skeletal isomers** — n-butane vs isobutane "
        "   (C4H10): same atoms, different carbon skeleton.\n"
        "2. **Positional isomers** — 1-propanol vs 2-propanol "
        "   (C3H8O): same skeleton, functional group on a "
        "   different carbon.\n"
        "3. **Functional-group isomers** — ethanol vs dimethyl "
        "   ether (C2H6O): different functional groups entirely.\n"
        "4. **Tautomers** — keto vs enol "
        "   (CH₃-CO-CH₃ ⇌ CH₂=C(OH)-CH₃): constitutional isomers "
        "   that interconvert rapidly via a proton shift "
        "   (distinguished from the others because they are in "
        "   dynamic equilibrium at ambient conditions).\n\n"
        "Contrast with **stereoisomers** (same connectivity, "
        "different 3D arrangement — enantiomers + diastereomers). "
        "Constitutional isomers usually have *different physical "
        "properties* (bp, mp, logP, spectra); stereoisomers often "
        "don't (with the notable exception of enantiomer optical "
        "activity)."},

    # ---- Phase 48a (round 170) — isomerism vocabulary --------------
    {"term": "Isomerism",
     "aliases": ["isomers"],
     "category": "stereochemistry",
     "see_also": ["Constitutional isomer", "Stereoisomer",
                  "Enantiomer", "Diastereomer", "Tautomer",
                  "Conformer", "Atropisomer",
                  "Cis-trans isomerism"],
     "definition_md":
        "**Isomerism** is the umbrella term for molecules that "
        "share a molecular formula but differ in some other "
        "respect.  The hierarchy: (a) **constitutional / "
        "structural isomers** differ in connectivity (n-butanol "
        "vs sec-butanol vs tert-butanol — same C₄H₁₀O); (b) "
        "**stereoisomers** share connectivity but differ in 3D "
        "arrangement — split into **enantiomers** (mirror "
        "images, non-superimposable, same physical properties "
        "except optical rotation) and **diastereomers** (NOT "
        "mirror images — different physical properties); (c) "
        "**conformational isomers / conformers** differ only "
        "in single-bond rotation, freely interconverting at "
        "room temperature; (d) **tautomers** are "
        "constitutional isomers in dynamic proton-transfer "
        "equilibrium (keto / enol; amide / iminol); (e) "
        "**atropisomers** are stereoisomers arising from "
        "restricted rotation about a single bond."},

    {"term": "Stereoisomer",
     "aliases": ["stereochemistry"],
     "category": "stereochemistry",
     "see_also": ["Enantiomer", "Diastereomer", "Meso compound",
                  "Conformer", "Atropisomer",
                  "Cis-trans isomerism", "R/S configuration"],
     "definition_md":
        "**Stereoisomers** share the same molecular formula AND "
        "connectivity but differ in their 3D spatial "
        "arrangement.  Two main classes: (a) **enantiomers** — "
        "mirror-image stereoisomers that cannot be superimposed; "
        "have identical physical properties except for opposite "
        "optical rotation + opposite biological activity at "
        "chiral receptors (the **chirality** of life); (b) "
        "**diastereomers** — stereoisomers that are NOT mirror "
        "images; have *different* physical properties (mp, bp, "
        "solubility) AND different biological activity.  A "
        "molecule with *n* stereocentres has at most 2ⁿ "
        "stereoisomers (less when symmetry creates meso "
        "compounds).  Distinguish from **constitutional "
        "isomers** (different connectivity) and **conformers** "
        "(different rotational state, no bond-breaking required "
        "to interconvert)."},

    {"term": "Conformer",
     "aliases": ["conformational isomer", "rotamer",
                 "conformational analysis"],
     "category": "stereochemistry",
     "see_also": ["Stereoisomer", "Anti / gauche / eclipsed",
                  "Newman projection", "Ring flip"],
     "definition_md":
        "**Conformers** (or *conformational isomers*) are "
        "different 3D shapes a molecule adopts by **single-bond "
        "rotation alone** — no bonds are broken, so they "
        "interconvert freely (typically ~ kJ/mol barriers, "
        "milliseconds to picoseconds at room temperature).  "
        "Classic examples: **butane** has anti / gauche / "
        "eclipsed conformers around the central C-C bond; "
        "**cyclohexane** flips between two equivalent chair "
        "forms (and accessible boat / twist-boat states); "
        "**proteins** continuously sample conformer ensembles "
        "around their backbone φ/ψ angles + side-chain χ "
        "angles.  Distinguish from **stereoisomers** (different "
        "configuration — bond-breaking required to "
        "interconvert).  In drug discovery, the **bioactive "
        "conformer** is often a higher-energy conformer that "
        "the receptor selectively binds — driving conformational "
        "constraint as a potency-improvement strategy."},

    {"term": "Tautomer",
     "aliases": ["tautomerism", "tautomerisation"],
     "category": "stereochemistry",
     "see_also": ["Keto-enol tautomerism", "Constitutional isomer",
                  "Stereoisomer"],
     "definition_md":
        "**Tautomers** are constitutional isomers in **dynamic "
        "proton-transfer equilibrium** at ambient conditions — "
        "proton + double-bond shift between adjacent atoms, "
        "with no other bond breaking.  Major classes: "
        "(a) **keto / enol** (CH₃COCH₃ ⇌ CH₂=C(OH)CH₃ — "
        "acetone is > 99.9999% keto at equilibrium); (b) "
        "**amide / iminol** (R-CO-NHR' ⇌ R-C(OH)=NR'); (c) "
        "**lactam / lactim** (cyclic amide / iminol — drives "
        "uracil / cytosine / guanine base-pairing geometry); "
        "(d) **nitroso / oxime** (R-N=O ⇌ R-NH-OH); (e) "
        "**ring-chain** in sugars (open-chain aldehyde ⇌ "
        "cyclic hemiacetal — the α/β anomers of glucose).  "
        "Tautomeric ratio is **environment-dependent** "
        "(solvent, pH, hydrogen-bond partners) — a major "
        "complication in computational drug discovery + "
        "spectral interpretation."},

    {"term": "Atropisomer",
     "aliases": ["atropisomerism", "axial chirality"],
     "category": "stereochemistry",
     "see_also": ["Enantiomer", "Stereoisomer",
                  "BINAP",
                  "Restricted rotation"],
     "definition_md":
        "**Atropisomers** are stereoisomers that arise from "
        "**restricted rotation about a single bond** — usually "
        "a biaryl C-C bond with bulky ortho substituents that "
        "raise the rotation barrier so high (≥ ~ 20 kcal/mol) "
        "that the two rotamers can be isolated as discrete "
        "compounds.  Classic example: **BINAP** "
        "(2,2'-bis(diphenylphosphino)-1,1'-binaphthyl) — the "
        "(R) + (S) atropisomers are stable enantiomers used "
        "as the chiral ligand for Noyori asymmetric "
        "hydrogenation (Nobel 2001).  The FDA classifies "
        "atropisomers as separate molecules requiring separate "
        "regulatory approval — atropisomerism is a "
        "**pharmaceutical-development gotcha** for biaryl drugs "
        "(telmisartan, lesinurad, gefitinib all carry "
        "atropisomeric centres that had to be characterised + "
        "controlled in manufacturing)."},

    {"term": "Cis-trans isomerism",
     "aliases": ["geometric isomerism", "E/Z isomerism",
                 "cis isomer", "trans isomer"],
     "category": "stereochemistry",
     "see_also": ["Diastereomer", "Stereoisomer",
                  "E/Z designation"],
     "definition_md":
        "**Cis-trans isomerism** (more formally **E/Z "
        "isomerism** under the CIP priority system) is the "
        "diastereomeric relationship between two molecules that "
        "differ in the relative position of substituents around "
        "a **non-rotating bond** — typically a C=C double bond "
        "or a ring.  *Cis* / *Z* = higher-priority substituents "
        "on the same side; *trans* / *E* = on opposite sides.  "
        "Different physical + biological properties: "
        "*cis*-2-butene boils at 4 °C, *trans*-2-butene at "
        "1 °C; *cis*-platin is a frontline chemotherapy, "
        "*trans*-platin is therapeutically inactive; *cis* + "
        "*trans* fatty acids in food have dramatically "
        "different cardiovascular profiles (industrial trans "
        "fats from partial hydrogenation are now banned in "
        "many countries).  Replaced 'cis/trans' with 'E/Z' for "
        "polysubstituted alkenes where 'same side' is "
        "ambiguous."},

    {"term": "Optical activity",
     "aliases": ["specific rotation", "optical rotation",
                 "polarimetry"],
     "category": "stereochemistry",
     "see_also": ["Enantiomer", "Chirality",
                  "Enantiomeric excess", "Racemic mixture"],
     "definition_md":
        "**Optical activity** is the rotation of plane-"
        "polarised light by a chiral molecule in solution — "
        "the macroscopic signature of molecular chirality, "
        "discovered by Biot 1815 + Pasteur's tartaric-acid "
        "crystals 1848.  Measured as **specific rotation** "
        "[α]ᴅ²⁰ = α / (l × c), where α = observed rotation in "
        "degrees, l = path length in dm, c = concentration in "
        "g/mL, the D subscript = sodium D-line (589 nm), and "
        "20 = temperature in °C.  The two enantiomers of a "
        "chiral molecule give **equal-magnitude opposite-"
        "sign** rotations: (R)-(+)-glucose has [α]ᴅ²⁰ = "
        "+52.7°, (S)-(–)-glucose −52.7°.  A 1:1 racemic "
        "mixture is optically inactive ([α] = 0); intermediate "
        "compositions give intermediate rotations, which is "
        "how **enantiomeric excess (ee)** can be measured by "
        "polarimetry: ee = (observed [α]) / (pure-enantiomer "
        "[α]) × 100%."},

    # ---- Phase 49a (round 176) — cross-module integration sweep ----
    # Foundational chemistry terms referenced by many catalogues
    # but not previously in the glossary.
    {"term": "pH",
     "aliases": ["acidity"],
     "category": "physical chemistry",
     "see_also": ["pKa", "Buffer", "Henderson-Hasselbalch",
                  "Buffer capacity"],
     "definition_md":
        "**pH** = −log₁₀[H₃O⁺].  Quantifies the acidity / "
        "basicity of an aqueous solution on a 0-14 scale "
        "(at 25 °C; the upper limit shifts with temperature "
        "since K_w varies).  Pure water has [H⁺] = "
        "10⁻⁷ M → pH 7 (neutral).  Strong acids (HCl, "
        "H₂SO₄, HNO₃) give pH 0-3; strong bases (NaOH, KOH) "
        "give pH 11-14.  Biological systems are **tightly "
        "buffered near pH 7.4** (blood) — the bicarbonate / "
        "phosphate / protein buffers in the body resist "
        "pH change against the 100 mEq/day acid load from "
        "metabolism.  Measured with a glass pH electrode + "
        "Ag/AgCl reference, calibrated against 2-3 "
        "standard buffer solutions."},

    {"term": "pKa",
     "aliases": ["acid dissociation constant", "Ka"],
     "category": "physical chemistry",
     "see_also": ["pH", "Buffer", "Henderson-Hasselbalch"],
     "definition_md":
        "**pKa** = −log₁₀(Kₐ), where Kₐ is the acid "
        "dissociation constant for HA ⇌ H⁺ + A⁻.  Lower "
        "pKa = stronger acid.  Useful pKa anchors: HCl "
        "−7, H₂SO₄ −3 (first), AcOH 4.76, H₂CO₃ 6.35, H₂S "
        "7.0, NH₄⁺ 9.25, methanol 15.5, water 15.7, "
        "alkanes ~ 50.  At **pH = pKa**, the acid is half-"
        "dissociated — the inflection point on a titration "
        "curve and the maximum-buffer-capacity point.  See "
        "the Phase-46 pH explorer for the seeded 46-acid "
        "catalogue + the buffer-designer + titration-curve "
        "simulator that exploit this principle."},

    {"term": "Buffer",
     "aliases": ["buffer solution"],
     "category": "physical chemistry",
     "see_also": ["pH", "pKa", "Buffer capacity",
                  "Henderson-Hasselbalch"],
     "definition_md":
        "A **buffer** is a solution that resists pH change "
        "when small amounts of acid or base are added.  "
        "Composed of a **weak acid + its conjugate base** "
        "(or weak base + conjugate acid) at comparable "
        "concentrations.  Common biological buffers include "
        "phosphate (pKa₂ 7.20 — perfect for physiological "
        "pH 7.4), bicarbonate (the major plasma buffer), "
        "Tris (pKa 8.10), HEPES (pKa 7.55).  Best buffering "
        "**within ±1 pH unit** of the buffer's pKa; outside "
        "that window the capacity drops to ~ 30 % of "
        "maximum (see **Buffer capacity**).  See the "
        "Phase-46 pH explorer's buffer-designer tab + the "
        "Phase-45 lab-reagents catalogue's 11 seeded "
        "buffers."},

    {"term": "Buffer capacity",
     "aliases": ["β", "buffering capacity"],
     "category": "physical chemistry",
     "see_also": ["Buffer", "pH", "pKa",
                  "Henderson-Hasselbalch"],
     "definition_md":
        "The **buffer capacity β** = 2.303 · C_total · α · "
        "(1 − α), where C_total is the sum of acid + "
        "conjugate-base concentrations and α = [A⁻] / "
        "C_total is the fraction in the deprotonated form.  "
        "β has units of mol·L⁻¹ per pH unit — the moles of "
        "strong base needed to shift the buffer's pH by 1.  "
        "Maximum at **pH = pKa** where α = 0.5 and β = "
        "0.576 · C_total.  Drops to ~ 30 % of max at |ΔpH| "
        "= 1, ~ 4 % at |ΔpH| = 2.  Drives the **'pick a "
        "buffer with a pKa within ±1 of your target pH'** "
        "rule of thumb."},

    {"term": "Henderson-Hasselbalch",
     "aliases": ["Henderson-Hasselbalch equation",
                 "HH equation"],
     "category": "physical chemistry",
     "see_also": ["pH", "pKa", "Buffer", "Buffer capacity"],
     "definition_md":
        "The **Henderson-Hasselbalch equation** is the "
        "log-form of the acid-dissociation equilibrium: "
        "**pH = pKa + log₁₀([A⁻] / [HA])**.  Lawrence J. "
        "Henderson 1908; Karl A. Hasselbalch 1916 (logged "
        "version).  At pH = pKa, log = 0 → [A⁻] = [HA] "
        "(half-dissociated).  Practical use: design a "
        "buffer at any target pH within ±1 of a chosen "
        "pKa by choosing the [A⁻]/[HA] ratio.  See the "
        "Phase-46 pH explorer's buffer-designer tab — "
        "enter target pH + pKa + total concentration, get "
        "back the [HA]/[A⁻] split + the moles of each "
        "needed."},

    {"term": "Hydrogen bonding",
     "aliases": ["H-bond", "hydrogen bond", "hydrogen bonds"],
     "category": "bonding",
     "see_also": ["Polarity", "Hydrophobic effect",
                  "Solvation"],
     "definition_md":
        "**Hydrogen bonding** is the directional, partially-"
        "covalent attractive interaction between an H atom "
        "covalently bonded to a strongly electronegative "
        "atom (O, N, F) and a lone pair on another "
        "electronegative atom.  Strength typically 5-30 "
        "kJ/mol — much weaker than a covalent bond (~ 350-"
        "400 kJ/mol) but stronger than dispersion.  Drives "
        "water's anomalously high boiling point (100 °C "
        "vs ~ −60 °C predicted from group trends), the "
        "α-helix + β-sheet of protein secondary structure, "
        "the Watson-Crick base-pairing of DNA + RNA, and "
        "the recognition geometry of every drug-target "
        "binding pocket.  Often shown as dotted lines in "
        "structural diagrams + chemical drawings."},

    {"term": "Hydrophobic effect",
     "aliases": ["hydrophobicity", "hydrophobic interaction"],
     "category": "bonding",
     "see_also": ["Hydrogen bonding", "Solvation",
                  "logP"],
     "definition_md":
        "The **hydrophobic effect** is the entropic driving "
        "force that makes non-polar molecules cluster "
        "together in water.  Origin: water molecules around "
        "a non-polar solute lose orientational freedom "
        "(forming a 'clathrate' cage of H-bonded waters) — "
        "an entropic penalty.  Aggregating non-polar solutes "
        "minimises the surface area that has to be "
        "clathrate-coated, releasing structured water back "
        "to bulk → entropy gain.  **Drives** protein "
        "folding (hydrophobic core), lipid-bilayer "
        "self-assembly, micelle / detergent action, drug-"
        "binding-pocket selectivity, and the high "
        "solubility of polar drugs vs the low solubility of "
        "lipophilic drugs."},

    {"term": "Lithium diisopropylamide",
     "aliases": ["LDA"],
     "category": "reagents",
     "see_also": ["Strong base", "Enolate", "Aldol reaction"],
     "definition_md":
        "**LDA** (lithium diisopropylamide, "
        "[(CH₃)₂CH]₂NLi) is a **strong, non-nucleophilic "
        "base** used to quantitatively deprotonate ketone / "
        "ester / amide α-CH (pKa ~ 20-30) to the lithium "
        "enolate without competing nucleophilic addition.  "
        "Generated in situ from diisopropylamine + n-BuLi "
        "in THF at −78 °C; pKa of the conjugate acid ~ 36, "
        "so deprotonation is essentially irreversible.  "
        "**Kinetic vs thermodynamic enolate control**: "
        "LDA at −78 °C gives the **kinetic enolate** (less-"
        "hindered side); equilibration at higher T gives "
        "the **thermodynamic enolate** (more-substituted "
        "= more-stable conjugation).  The standard base for "
        "directed aldol + alkylation chemistry."},

    {"term": "Multi-component reaction",
     "aliases": ["MCR", "multicomponent reaction"],
     "category": "synthesis",
     "see_also": ["Hantzsch dihydropyridine synthesis",
                  "Atom economy", "Step economy"],
     "definition_md":
        "A **multi-component reaction (MCR)** combines "
        "**three or more starting materials in a single "
        "pot** to give a product that incorporates "
        "essentially all of their atoms — high atom "
        "economy + step economy.  Classics: **Hantzsch "
        "dihydropyridine synthesis** (1881; aldehyde + 2 "
        "β-ketoester + NH₃ → 1,4-DHP, the calcium-channel-"
        "blocker scaffold); **Strecker amino-acid synthesis** "
        "(1850; aldehyde + NH₃ + HCN → α-aminonitrile → "
        "α-amino acid); **Mannich reaction** (1912; "
        "aldehyde + amine + ketone → β-amino ketone); "
        "**Ugi 4-component reaction** (1959; aldehyde + "
        "amine + isocyanide + carboxylic acid → α-acylamino "
        "amide).  Workhorses in combinatorial library "
        "synthesis + medicinal-chem fragment growth."},

    {"term": "Active-methylene compound",
     "aliases": ["active methylene", "acidic methylene"],
     "category": "synthesis",
     "see_also": ["pKa", "Knoevenagel condensation",
                  "Aldol reaction"],
     "definition_md":
        "An **active-methylene compound** has a CH₂ flanked "
        "by **two electron-withdrawing groups**, typically "
        "carbonyls or nitro / nitrile.  Examples: malonate "
        "esters (CH₂(COOR)₂, pKa ~ 13), β-ketoesters "
        "(R-CO-CH₂-COOR', pKa ~ 11), 1,3-diketones (R-CO-"
        "CH₂-CO-R', pKa ~ 9), nitroalkanes (R-CH₂-NO₂, "
        "pKa ~ 10), cyanoacetate (NC-CH₂-COOR, pKa ~ 11).  "
        "The two EWGs **dramatically acidify** the α-CH (vs "
        "pKa ~ 20 for a simple ketone α-CH), so a mild "
        "secondary-amine base (piperidine, pyridine) is "
        "sufficient to generate the stabilised carbanion — "
        "drives the **Knoevenagel condensation** + "
        "**Hantzsch dihydropyridine synthesis** cascades."},

    {"term": "Endosymbiotic theory",
     "aliases": ["endosymbiosis"],
     "category": "biology",
     "see_also": ["Mitochondrion", "Chloroplast"],
     "definition_md":
        "The **endosymbiotic theory** (Lynn Margulis 1967) "
        "holds that eukaryotic mitochondria descended from "
        "an α-proteobacterium engulfed by an archaeal host, "
        "and chloroplasts descended from a cyanobacterium "
        "engulfed by a primordial photosynthetic eukaryote.  "
        "Evidence: (a) mitochondrial + chloroplast genomes "
        "are **circular** like bacterial chromosomes; (b) "
        "their ribosomes are **70S** like bacteria, "
        "sensitive to macrolides + tetracyclines that don't "
        "touch the cytoplasmic 80S; (c) their inner "
        "membranes lack cholesterol; (d) phylogenetic "
        "placement of mitochondrial 16S rRNA within "
        "α-proteobacteria; (e) **double membranes** "
        "(engulfment signature).  See the Phase-47 "
        "biochemistry-by-kingdom catalogue's eukarya-"
        "genetics topic."},

    {"term": "Horizontal gene transfer",
     "aliases": ["HGT", "lateral gene transfer", "LGT"],
     "category": "biology",
     "see_also": ["CRISPR-Cas", "Plasmid"],
     "definition_md":
        "**Horizontal gene transfer (HGT)** — between "
        "non-parental cells, contrasted with vertical "
        "Darwinian descent — dominates bacterial + "
        "archaeal evolution.  Three mechanisms: (a) "
        "**transformation** = uptake of naked environmental "
        "DNA via competence machinery (*S. pneumoniae*, "
        "*B. subtilis*, *N. gonorrhoeae*); (b) "
        "**transduction** = DNA transfer via bacteriophage "
        "particles (generalised + specialised); (c) "
        "**conjugation** = direct cell-to-cell DNA transfer "
        "via a sex pilus + Type-IV secretion system, "
        "encoded by conjugative plasmids (F-factor) or "
        "integrative + conjugative elements (ICEs).  HGT is "
        "the engine of **antibiotic-resistance spread** — "
        "β-lactamases, NDM-1 carbapenem-resistance, mcr-1 "
        "colistin-resistance all dispersed globally on "
        "plasmids in < 5 years."},

    {"term": "CRISPR-Cas",
     "aliases": ["CRISPR", "CRISPR-Cas9", "Cas9",
                 "Cas12", "Cas13"],
     "category": "biology",
     "see_also": ["Horizontal gene transfer",
                  "Restriction-modification"],
     "definition_md":
        "**CRISPR-Cas** (Clustered Regularly Interspaced "
        "Short Palindromic Repeats + CRISPR-associated "
        "nucleases) is the **adaptive immune system of "
        "bacteria + archaea against bacteriophages + "
        "plasmid invasion**.  Short fragments (~ 30 bp "
        "'spacers') of invading DNA are integrated into "
        "the host's CRISPR locus, transcribed into guide "
        "RNAs, and used by Cas nucleases (Cas9 / Cas12 / "
        "Cas13) to cleave any future invader carrying a "
        "matching protospacer + PAM motif.  **Repurposed "
        "for genome editing** by Doudna + Charpentier 2012 "
        "(Nobel 2020) — Cas9 + a programmed guide RNA can "
        "introduce a double-strand break at any genomic "
        "locus carrying a matching 20 bp + PAM.  In 2023 "
        "the FDA approved **Casgevy** for sickle-cell "
        "disease — the first CRISPR therapy."},

    {"term": "Chirality",
     "aliases": ["chiral", "achiral"],
     "category": "stereochemistry",
     "see_also": ["Stereocentre", "Enantiomer",
                  "Optical activity"],
     "definition_md":
        "A molecule is **chiral** if it is not superimposable "
        "on its mirror image — like a left vs right hand.  "
        "Most commonly arises from an **sp³ carbon with 4 "
        "different substituents** (a stereocentre).  Chiral "
        "molecules are **optically active** (rotate plane-"
        "polarised light) and often have stereo-specific "
        "biological activity (one enantiomer of carvone "
        "smells like spearmint, the other like caraway; "
        "L-DOPA treats Parkinson's, D-DOPA does nothing).  "
        "Most biological molecules — amino acids, sugars, "
        "lipids — are chiral and biology uses essentially "
        "one enantiomer of each.  Distinguish from "
        "**achiral** molecules (superimposable on mirror "
        "image — most simple alkanes, water, CO₂).  See "
        "the Phase-48 isomer explorer's enantiomer "
        "classifier."},

    {"term": "Chiral switch",
     "aliases": [],
     "category": "medicinal chemistry",
     "see_also": ["Enantiomer", "Chirality",
                  "Enantiomeric excess"],
     "definition_md":
        "A **chiral switch** is a pharmaceutical-development "
        "strategy where a marketed **racemic drug** is "
        "re-developed as the **single more-active "
        "enantiomer** to extend patent life + reduce "
        "off-target effects from the inactive enantiomer.  "
        "Two textbook examples: (a) **citalopram → "
        "escitalopram** — Lundbeck took racemic citalopram "
        "off-patent, then released the (S)-enantiomer "
        "(escitalopram, 2002) as a new product with fresh "
        "patent life — (R)-citalopram contributes only ~ "
        "1% of the SERT-inhibition activity AND blocks the "
        "histamine H1 receptor as the source of sedation "
        "side effect; (b) **omeprazole → esomeprazole** — "
        "AstraZeneca's (S)-omeprazole (Nexium 2001) "
        "eliminated the inter-patient CYP2C19-polymorphism "
        "variability of the racemate.  See the Phase-31k "
        "SSRI + PPI SAR series."},
]
