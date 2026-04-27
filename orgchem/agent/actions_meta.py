"""Meta-actions — the tutor's self-introspection tools.

Round 55 bug-fix: users reported the tutor refusing to visualise
ligand binding despite the app having a full protein-binding stack.
Root cause: the LLM's training data doesn't know what OrgChem Studio
can do, and a long system prompt is easy to lose in a crowded
context. These meta-actions give the tutor a way to *ask the app*
what's available mid-conversation, grouped by topic.
"""
from __future__ import annotations
from typing import Any, Dict, List

from orgchem.agent.actions import action, registry


# Curated category summary. Keys match the ``category`` string the
# @action decorator uses; values are the one-line description the
# tutor should see when deciding whether to recurse into that area.
_CATEGORY_SUMMARIES: Dict[str, str] = {
    "molecule": "Browse / display / compare molecules from the seeded DB.",
    "tools": "Empirical-formula, IUPAC-formula, hand calculators.",
    "online": "PubChem search + download.",
    "tutorial": "Curriculum lessons (beginner → graduate).",
    "reaction": "Named reactions, 2D / 3D schemes, energy profiles, trajectories.",
    "mechanism": "Step-by-step curly-arrow playback + SVG export.",
    "synthesis": "Multi-step pathways, atom economy, green metrics, retrosynthesis.",
    "dynamics": "Conformer morphs + dihedral scans (interactive 3D HTML).",
    "orbitals": "Hückel MOs + Woodward-Hoffmann rule checks.",
    "stereo": "R/S + E/Z descriptors, wedge/dash 2D, enantiomer flip.",
    "glossary": "Searchable term dictionary (~61 entries).",
    "medchem": "Drug-likeness, SAR series, bioisostere suggestions.",
    "lab": "TLC / Rf, recrystallisation, distillation, acid-base extraction.",
    "naming": "IUPAC naming rule catalogue.",
    "spectroscopy": "IR / ¹H / ¹³C NMR / MS prediction + stick-spectrum export.",
    "session": "Save / load the user's workspace state.",
    "periodic": "118-element interactive periodic table.",
    "carbohydrate": "25-entry carbohydrates catalogue (macromolecule tab).",
    "lipid": "31-entry lipids catalogue (macromolecule tab).",
    "nucleic-acid": "33-entry nucleic-acids catalogue (macromolecule tab).",
    "protein": "PDB + AlphaFold ingestion, binding contacts, PPI, 3D viewer.",
    "export": "2D / 3D image export + screenshots.",
    "window": "Secondary-window management (Macromolecules window).",
    "meta": "Self-introspection actions (this category).",
    # Round 180 (Phase 49e) backfill — categories that shipped
    # after the round-55 baseline but never got a summary entry.
    "authoring": "Add new molecules / reactions / glossary terms / "
                 "tutorial lessons / molecule synonyms to the DB.",
    "biochem": "Major metabolic pathways (glycolysis, TCA, "
               "ox-phos, β-oxidation, …) with per-step substrates / "
               "enzymes / EC numbers / ΔG / regulators.",
    "calc": "Lab calculator solvers — molarity, dilution, "
            "stoichiometry, pH, gas law, colligative, thermo / "
            "kinetics, equilibrium (~ 30 routine bench calcs).",
    "cell": "Cell-component explorer (eukarya / bacteria / "
            "archaea — organelles, membranes, cytoskeleton, "
            "envelopes, ribosomes).",
    "centrifugation": "Centrifuge / rotor catalogue + g↔RPM "
                      "calculator + recommended-protocol lookup.",
    "chromatography": "Chromatography-method reference (TLC, "
                      "HPLC, GC-MS, FPLC, SEC, IC, SFC, …).",
    "clinical": "Clinical chemistry lab panels (BMP / CMP / "
                "Lipid / Diabetes / Thyroid / Vitamin D) with "
                "per-analyte normal ranges + clinical "
                "significance.",
    "drawing": "Headless ChemDraw-equivalent: structure ↔ SMILES, "
               "PNG / SVG / MOL export, reaction-scheme builder.",
    "instrumentation": "Major lab analyser reference catalogue "
                       "(clinical chemistry, hematology, "
                       "molecular, mass-spec, microscopy, "
                       "automation, storage).",
    "isomer": "Stereoisomer + tautomer enumeration + "
              "pairwise-relationship classifier (identical / "
              "enantiomer / diastereomer / meso / tautomer / "
              "constitutional).",
    "kingdom": "Biochemistry-by-Kingdom topics (Eukarya / "
               "Bacteria / Archaea / Viruses × Structure / "
               "Physiology / Genetics).",
    "microscopy": "Microscopy-method reference across resolution "
                  "scales (whole-organism → single-molecule), "
                  "with cross-references to lab analysers.",
    "ph": "pH + buffer explorer — pKa lookup, buffer designer "
          "(Henderson-Hasselbalch), buffer capacity, titration "
          "curve simulator.",
    "phys-org": "Physical organic chemistry — Hammett ρ-σ fits, "
                "primary kinetic isotope effects.",
    "qualitative": "Qualitative inorganic ion / gas tests (flame, "
                   "hydroxide, halide, sulfate, carbonate, NH₄⁺, "
                   "and gas tests).",
    "reagent": "Lab reagents reference (buffers, acids / bases, "
               "detergents, solvents, cell-culture media, "
               "molecular-biology enzymes).",
    "scripting": "Python script editor + 3D scene composer "
                 "workbench window.",
    "search": "Full-text search across every text-bearing column "
              "in the seeded DB (molecules, reactions, "
              "pathways, glossary, mechanism steps).",
    "spectrophotometry": "Spectrophotometry-method reference + "
                         "Beer-Lambert solver (UV-Vis, "
                         "fluorescence, IR / FTIR, NIR, Raman, "
                         "CD, AAS, ICP, NMR).",
    "lab-canvas": "Interactive lab-setup canvas — place "
                  "equipment, snap connection ports, build "
                  "apparatus from seeded Phase-38b setups.",
    "simulator": "Process simulator — animate a seeded lab "
                 "setup through its teaching stages "
                 "(distillation / reflux / extraction / "
                 "filtration / recrystallisation) with "
                 "play/pause/step controls + commentary track.",
    # Phase CB-1.0 — Cell Bio Studio sibling (round 212).  First
    # cellbio category; future Cell Bio sub-domains (cell-cycle,
    # cytoskeleton, transporters, …) will land as sibling
    # `cellbio-*` categories.
    # Phase CB-2.0 — Cell-cycle deep-phase catalogue (round 218).
    "cellbio-cell-cycle": "Cell-cycle catalogue (Cell Bio Studio "
                          "— Phase CB-2.0).  30 entries spanning "
                          "all 5 cycle phases (G1 / S / G2 / M / "
                          "G0), all 4 checkpoints (G1/S "
                          "restriction, intra-S, G2/M, spindle "
                          "assembly), the 4 canonical cyclin-CDK "
                          "pairs (D-CDK4/6, E-CDK2, A-CDK2/1, "
                          "B-CDK1), CIP/KIP + INK4 inhibitors, "
                          "the Rb/E2F axis, mitotic regulators "
                          "(APC/C, separase/securin, Aurora, "
                          "Plk1, SAC components, condensin/"
                          "cohesin), and the DNA-damage-response "
                          "kinases (ATM, ATR, Chk1/Chk2, "
                          "BRCA1/2, p53).  Cross-references to "
                          "CB-1.0 signalling pathways + Pharm "
                          "drug classes.",
    "cellbio-signaling": "Cell-signalling pathway catalogue "
                         "(Cell Bio Studio) — 25 canonical "
                         "pathways (MAPK, PI3K-Akt-mTOR, JAK-"
                         "STAT, Wnt, Notch, Hedgehog, NF-κB, "
                         "TGF-β, GPCR-second-messengers, "
                         "AMPK, p53, apoptosis, TCR, …) with "
                         "receptor class + key components + "
                         "drug targets + cross-references to "
                         "OrgChem molecules.",
    # Phase BC-2.0 — Cofactors deep-phase catalogue (round 219).
    "biochem-cofactors": "Cofactors / coenzymes catalogue "
                         "(Biochem Studio — Phase BC-2.0).  27 "
                         "entries spanning all the canonical "
                         "biochem cofactor classes: nicotinamide "
                         "(NAD+/H, NADP+/H), flavin (FAD/H₂, "
                         "FMN), acyl-carrier (CoA, acetyl-CoA), "
                         "methyl-donor (SAM), phosphate-energy "
                         "currency (ATP, ADP, cAMP, GTP), "
                         "vitamin-derived prosthetic groups "
                         "(biotin / TPP / PLP / lipoate / "
                         "cobalamin / tetrahydrofolate), metal "
                         "cofactors (heme / Mg²⁺ / Zn²⁺), "
                         "quinone electron carriers (CoQ10 / "
                         "plastoquinone), and redox-buffer small "
                         "molecules (glutathione / ascorbate). "
                         " Cross-references to BC-1.0 enzymes "
                         "+ OrgChem metabolic pathways + "
                         "OrgChem molecule rows.",
    # Phase BC-1.0 — Biochem Studio sibling (round 213).
    "biochem-enzymes": "Enzyme catalogue (Biochem Studio) — "
                       "30 enzymes spanning all 7 IUBMB EC "
                       "classes (oxidoreductase, transferase, "
                       "hydrolase, lyase, isomerase, ligase, "
                       "translocase) with mechanism class, "
                       "substrates / products / cofactors, "
                       "regulators, disease associations, "
                       "drug targets, structural family, and "
                       "typed cross-references to OrgChem "
                       "molecules + OrgChem metabolic-pathway "
                       "ids + Cell Bio signalling-pathway ids.",
    # Phase PH-2.0 — Receptor pharmacology deep-phase catalogue
    # (round 220).
    "pharm-receptors": "Receptor pharmacology catalogue "
                       "(Pharmacology Studio — Phase PH-2.0).  "
                       "32 entries spanning all major drug-"
                       "target receptor superfamilies: GPCRs "
                       "(aminergic — β/α adrenergic, muscarinic, "
                       "dopamine; peptide — opioid, angiotensin, "
                       "GLP-1, histamine; cannabinoid), nuclear "
                       "hormone receptors (steroid — GR/ER/AR/PR; "
                       "non-steroid — TR/VDR/PPARγ), receptor "
                       "tyrosine kinases (EGFR, HER2, VEGFR2, "
                       "insulin), voltage-gated ion channels "
                       "(Nav1.7, hERG, Cav1.2), ligand-gated "
                       "(nAChR, GABA-A, NMDA), monoamine "
                       "transporters (SERT, NET, DAT), and "
                       "other transporters (SGLT2, P-gp).  "
                       "Each entry: structural summary, "
                       "endogenous ligands, signalling output, "
                       "tissue distribution, clinical relevance, "
                       "+ 4-way cross-references to PH-1.0 drug "
                       "classes + CB-1.0 signalling pathways + "
                       "BC-1.0 enzymes + OrgChem molecules.",
    # Phase PH-1.0 — Pharmacology Studio sibling (round 214).
    "pharm-drugs": "Drug-class catalogue (Pharmacology Studio) "
                   "— 30 classes across 11 therapeutic areas "
                   "(cardiovascular, metabolic, neurology-"
                   "psychiatry, oncology, infectious, "
                   "inflammation-immunology, pulmonology, "
                   "endocrinology, haematology, GI, pain) "
                   "with mechanism, target, typical agents, "
                   "clinical use, side effects, "
                   "contraindications, monitoring, and typed "
                   "cross-references to OrgChem molecules + "
                   "Biochem enzyme ids + Cell Bio signalling-"
                   "pathway ids.",
    # Phase MB-2.0 — Virulence-factor deep-phase catalogue
    # (round 221).
    "microbio-virulence": "Virulence-factor + toxin catalogue "
                          "(Microbiology Studio — Phase MB-2.0). "
                          " 30 entries spanning the canonical "
                          "bacterial virulence-mechanism classes: "
                          "8 AB-toxins (diphtheria, cholera, "
                          "pertussis, Shiga, anthrax LF + EF, "
                          "tetanus, botulinum), 5 pore-forming "
                          "cytolysins (α-toxin, streptolysin O, "
                          "pneumolysin, PVL, listeriolysin O), 3 "
                          "superantigens (TSST-1, SEA-SEE, SpeA), "
                          "3 adhesins (UPEC fimbriae, M protein, "
                          "Yersinia YadA/Invasin), 3 capsules "
                          "(GAS hyaluronate, pneumococcal "
                          "polysaccharide, anthrax poly-γ-D-"
                          "glutamate), 3 secretion systems "
                          "(T3SS / T4SS-CagA / T6SS), 3 immune-"
                          "evasion factors (IgA1 protease, "
                          "Protein A, Neisseria Opa antigenic "
                          "variation), 1 biofilm + quorum-"
                          "sensing entry, 1 LPS / lipid-A "
                          "endotoxin entry.  Cross-references to "
                          "MB-1.0 microbe ids + BC-1.0 enzymes "
                          "+ CB-1.0 signalling pathways.",
    # Phase MB-1.0 — Microbiology Studio sibling (round 215).
    "microbio-microbes": "Microbe catalogue (Microbiology Studio) "
                         "— 30 organisms across the 5 microbial "
                         "kingdoms (17 bacteria split into gram-"
                         "positive / gram-negative / atypical / "
                         "acid-fast, 2 archaea, 3 fungi, 6 viruses "
                         "covering Baltimore I → VII, 2 protists) "
                         "with morphology, key metabolism / "
                         "replication, pathogenesis, antimicrobial "
                         "susceptibility, genome size, "
                         "Bergey / ICTV reference, and typed "
                         "cross-references to OrgChem cell "
                         "components + Pharm drug-class ids + "
                         "Biochem enzyme ids.",
    # Phase BT-2.0 — Plant-hormones deep-phase catalogue (round 222).
    "botany-hormones": "Plant-hormones catalogue (Botany Studio "
                       "— Phase BT-2.0).  21 entries spanning "
                       "all 10 canonical phytohormone classes: "
                       "auxins (IAA, 2,4-D, NAA, IBA), "
                       "cytokinins (trans-zeatin, kinetin, BAP), "
                       "gibberellins (GA3, GA4), abscisic acid "
                       "(ABA), ethylene, brassinosteroids "
                       "(brassinolide, castasterone), "
                       "jasmonates (JA, MeJA), salicylic acid "
                       "(SA), strigolactones (strigol, "
                       "orobanchol), peptide hormones (CLE, "
                       "systemin, RALF).  Each entry: "
                       "structural class, biosynthesis "
                       "precursor, perception mechanism (TIR1, "
                       "AHK, GID1, PYR/PYL/RCAR, ETR1, BRI1, "
                       "COI1, NPR1, D14, FERONIA…), primary "
                       "physiological effect, antagonisms, "
                       "model plants where signalling was "
                       "characterised, and cross-references to "
                       "OrgChem Molecule rows + BT-1.0 plant-"
                       "taxon ids.",
    # Phase BT-1.0 — Botany Studio sibling (round 216).
    "botany-taxa": "Plant-taxa catalogue (Botany Studio) — 30 "
                   "species spanning all 6 major plant divisions "
                   "(bryophytes, lycophytes, ferns, gymnosperms, "
                   "angiosperm-monocots, angiosperm-eudicots) + "
                   "all 4 photosynthetic strategies (C3 / C4 / "
                   "CAM / not-applicable for the holoparasite "
                   "Rafflesia) with full taxonomic name, life "
                   "cycle, reproductive strategy, ecological "
                   "role, economic importance, model-organism "
                   "flag, genome size, and typed cross-"
                   "references to OrgChem molecules (plant "
                   "natural products like Morphine, Caffeine, "
                   "Salicylic acid, Lycopene) + OrgChem "
                   "metabolic-pathway ids (Calvin cycle is "
                   "universal) + Pharm drug-class ids (poppy → "
                   "opioids; willow → NSAIDs; yew → taxanes).",
    # Phase AB-2.0 — Organ-systems deep-phase catalogue
    # (round 223) — FINAL -2 round, closes the chain.
    "animal-organ-systems": "Animal organ-systems catalogue "
                            "(Animal Biology Studio — Phase "
                            "AB-2.0).  25 entries: the 11 "
                            "canonical mammalian systems "
                            "(cardiovascular, respiratory, "
                            "digestive, urinary, nervous, "
                            "endocrine, immune, musculoskeletal, "
                            "integumentary, reproductive-female "
                            "+ -male, lymphatic) PLUS 13 "
                            "comparative-anatomy entries "
                            "covering open vs closed circulation, "
                            "gills + tracheae + air sacs, "
                            "ruminant + avian + hindgut "
                            "digestion, nerve-net + cephalopod "
                            "brain, protonephridia + Malpighian "
                            "tubules, regeneration outliers "
                            "(planarian + axolotl + hydra), "
                            "eye-evolution convergence, fish "
                            "single-circuit hearts, invertebrate "
                            "innate immunity, insect ecdysone "
                            "signalling, muscle-type evolution, "
                            "hermaphroditism + parthenogenesis, "
                            "ectothermy vs endothermy.  Each "
                            "entry: representative organs, key "
                            "cell types, functional anatomy, "
                            "evolutionary origin, characteristic "
                            "disorders, + 4-way cross-references "
                            "to OrgChem molecules + CB-1.0 "
                            "signalling pathways + BC-1.0 "
                            "enzymes + AB-1.0 animal-taxon ids.",
    # Phase AB-1.0 — Animal Biology Studio sibling (round 217)
    # — sixth + FINAL sibling, completes the platform.
    "animal-taxa": "Animal-taxa catalogue (Animal Biology "
                   "Studio) — 30 species spanning all 9 major "
                   "animal phyla (porifera → cnidaria → "
                   "platyhelminthes → nematoda → mollusca → "
                   "annelida → arthropoda → echinodermata → "
                   "chordata).  Includes the canonical model "
                   "organisms (*C. elegans*, *Drosophila*, "
                   "zebrafish, *Xenopus*, mouse, *Homo "
                   "sapiens*).  Each entry: phylum, class, "
                   "body plan (asymmetric / radial / "
                   "bilateral), germ layers, coelom type, "
                   "reproductive strategy, ecological role, "
                   "model-organism flag, genome size, and "
                   "typed cross-references to OrgChem "
                   "molecules (animal hormones / "
                   "neurotransmitters / metabolites) + Cell "
                   "Bio signalling-pathway ids (developmental, "
                   "apoptosis, immune) + Biochem enzyme ids "
                   "(animal-source enzymes).",
    # Phase GM-1.0 — Genetics + Molecular Biology Studio
    # sibling (round 230) — seventh sibling, post -3 chain.
    "genetics-techniques": "Molecular-biology-techniques "
                           "catalogue (Genetics + Molecular "
                           "Biology Studio) — 40 entries "
                           "spanning all 14 categories (PCR "
                           "/ sequencing / cloning / CRISPR "
                           "/ blots / in-situ hybridisation "
                           "/ chromatin profiling / "
                           "transcriptomics / spatial "
                           "transcriptomics / proteomics / "
                           "interactions / structural + "
                           "3D-genome / epigenetics / "
                           "delivery).  Each entry: "
                           "principle, sample types, "
                           "throughput, key reagents, "
                           "typical readouts, limitations, "
                           "representative platforms, year "
                           "of introduction, key references, "
                           "and 5-way typed cross-references "
                           "to BC-1.0 enzymes + CB-2.0 "
                           "cell-cycle ids + CB-1.0 "
                           "signalling pathways + AB-1.0 "
                           "animal-taxon ids + OrgChem "
                           "molecule names.",
}


@action(category="meta")
def list_capabilities(category: str = "") -> Dict[str, Any]:
    """Return the tutor's capability inventory.

    Without a ``category`` argument, returns the list of known
    categories with a one-line description each plus the count of
    agent actions in each. Pass a category to drill in — you get
    every action in that bucket with its docstring's first line.

    Use this whenever a student asks about a topic you're unsure
    the app supports. It's faster and more reliable than guessing
    from memory.

    Examples of useful drill-ins:
    - ``list_capabilities(category="protein")`` — every PDB /
      binding-contact / interaction-map action.
    - ``list_capabilities(category="spectroscopy")`` — every IR /
      NMR / MS tool.
    - ``list_capabilities(category="synthesis")`` — pathways,
      retrosynthesis, atom economy.
    """
    all_actions = registry()
    by_cat: Dict[str, List[Dict[str, str]]] = {}
    for name, spec in all_actions.items():
        cat = getattr(spec, "category", "") or "(uncategorised)"
        fn = getattr(spec, "fn", None) or getattr(spec, "func", None)
        doc = (fn.__doc__ if fn is not None else "") or ""
        doc = doc.strip()
        first_line = doc.splitlines()[0] if doc else ""
        by_cat.setdefault(cat, []).append({
            "name": name, "summary": first_line,
        })
    if not category:
        return {
            "total_actions": len(all_actions),
            "categories": [
                {
                    "category": c,
                    "description": _CATEGORY_SUMMARIES.get(c, ""),
                    "action_count": len(actions),
                    "example_actions": [a["name"] for a in actions[:3]],
                }
                for c, actions in sorted(by_cat.items())
            ],
        }
    key = category.strip().lower()
    match = next(
        (c for c in by_cat if c.lower() == key), None,
    )
    if match is None:
        return {
            "error": f"Unknown category {category!r}. "
                     f"Known: {sorted(by_cat)}",
        }
    return {
        "category": match,
        "description": _CATEGORY_SUMMARIES.get(match, ""),
        "actions": sorted(by_cat[match], key=lambda a: a["name"]),
    }
