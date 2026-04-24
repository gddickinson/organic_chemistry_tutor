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
]
