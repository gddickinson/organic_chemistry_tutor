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
]
