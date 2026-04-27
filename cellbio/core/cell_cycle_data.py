"""Phase CB-2.0 (round 218) — 28-entry cell-cycle catalogue.

Each entry carries typed cross-references into:
- ``cellbio.core.cell_signaling`` ids (the CB-1.0 catalogue
  — many cell-cycle regulators sit downstream of growth-
  factor / mitogen pathways).
- ``pharm.core.drug_classes`` ids (PH-1.0 — kinase
  inhibitors are the dominant cell-cycle drug class;
  taxanes hit mitotic spindle / Aurora indirectly).
- OrgChem ``Molecule`` rows by name (left empty for v0.1 —
  cyclins / kinases are proteins, not in the small-molecule
  DB; future round may backfill specific drug molecules).

All cross-reference ids verified against destination
catalogues at write time; the round-218 catalogue tests gate
re-validation at every test run.
"""
from __future__ import annotations
from typing import Tuple

from cellbio.core.cell_cycle import CellCycleEntry


CELL_CYCLE_ENTRIES: Tuple[CellCycleEntry, ...] = (
    # ============================================================
    # Phases (5)
    # ============================================================
    CellCycleEntry(
        id="g1-phase",
        name="G1 phase",
        category="phase",
        phase_or_role="G1",
        summary=(
            "First gap phase between cytokinesis and S-phase "
            "DNA replication.  Cell biosynthesis is at maximum "
            "rate; cell grows + decides whether to commit to "
            "another division round at the G1/S restriction "
            "point.  Length is the most variable of any cycle "
            "phase — minutes (early embryo) to years "
            "(differentiated tissue)."),
        key_components=(
            "Cyclin D-CDK4/6", "Cyclin E-CDK2",
            "Rb (hypophosphorylated → hyperphosphorylated)",
            "E2F transcription factors", "Myc",
        ),
        function=(
            "Mitogen integration + cell-size sensing → "
            "decision to enter or skip S-phase."),
        activated_by=(
            "Mitogenic growth factors via MAPK / ERK + "
            "PI3K / Akt", "Wnt / β-catenin (in regenerative "
            "epithelia)", "Cyclin D induction",
        ),
        inhibited_by=(
            "TGF-β / Smad → p15 INK4b → blocks Cyclin D-CDK4/6",
            "p21 / p27 / p57 (CIP/KIP family)", "Contact "
            "inhibition (Hippo / YAP repression)",
        ),
        disease_associations=(
            "Loss of G1/S checkpoint is the universal hallmark "
            "of cancer; ~ 100 % of tumours disable Rb directly "
            "or indirectly via Cyclin D / CDK4/6 / p16 axis.",
        ),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pi3k-akt-mtor", "wnt-beta-catenin",
            "tgf-beta-smad", "hippo-yap",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Cells in G0 (quiescence) are G1-derived but have "
            "exited the cycle entirely; re-entry requires "
            "fresh mitogen exposure."),
    ),
    CellCycleEntry(
        id="s-phase",
        name="S phase (DNA synthesis)",
        category="phase",
        phase_or_role="S",
        summary=(
            "DNA-replication phase.  Every chromosome is "
            "duplicated exactly once.  Origins fire in a "
            "regulated temporal program; replication forks "
            "proceed bidirectionally; pre-replication "
            "complexes (pre-RC) cannot reload until next M-"
            "phase exit, ensuring once-and-only-once "
            "replication."),
        key_components=(
            "Cyclin A-CDK2 (drives origin firing)",
            "ORC + Cdc6 + Cdt1 (pre-RC)",
            "MCM2-7 helicase complex", "PCNA + DNA polymerase "
            "δ / ε", "Geminin (Cdt1 inhibitor)",
        ),
        function=(
            "Faithful duplication of the entire genome."),
        activated_by=(
            "Cyclin E-CDK2 (start)", "Cyclin A-CDK2 (sustain)",
            "Dbf4-Cdc7 (DDK)",
        ),
        inhibited_by=(
            "Intra-S checkpoint (ATR-Chk1) under fork stress",
            "Geminin sequestering Cdt1",
        ),
        disease_associations=(
            "Replication stress drives genome instability + "
            "tumorigenesis; defective MCM licensing causes "
            "Meier-Gorlin syndrome.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "platinum-chemotherapy",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "S-phase is the substrate of platinum-based DNA-"
            "damaging chemotherapy + nucleoside analogues "
            "(gemcitabine / cytarabine)."),
    ),
    CellCycleEntry(
        id="g2-phase",
        name="G2 phase",
        category="phase",
        phase_or_role="G2",
        summary=(
            "Second gap phase between S-phase completion and "
            "mitosis.  Cell completes biosynthesis, checks "
            "that DNA replication finished cleanly + repaired "
            "any damage, accumulates Cyclin B-CDK1 (MPF) in an "
            "inactive Tyr15-phosphorylated form."),
        key_components=(
            "Cyclin B-CDK1 (MPF, accumulating + inhibited)",
            "Wee1 / Myt1 (Tyr15 phosphorylation)",
            "Cdc25 family (Tyr15 dephosphorylation activator)",
        ),
        function=(
            "Integrate completion of S-phase with permission "
            "to enter mitosis at the G2/M checkpoint."),
        activated_by=(
            "Cdc25 dephosphorylation of CDK1",
            "Auto-amplification loop (CDK1 inhibits Wee1 + "
            "activates Cdc25)",
        ),
        inhibited_by=(
            "G2/M checkpoint via ATR / ATM → Chk1 / Chk2 → "
            "Cdc25 inhibition", "Wee1 / Myt1",
        ),
        disease_associations=(
            "G2/M checkpoint failure with damaged DNA → "
            "mitotic catastrophe + chromosomal instability.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Wee1 inhibitors (adavosertib) are in clinical "
            "trials — block the brake → tumour cells with "
            "broken G1/S checkpoint enter mitosis with damage "
            "→ mitotic catastrophe."),
    ),
    CellCycleEntry(
        id="m-phase",
        name="M phase (mitosis + cytokinesis)",
        category="phase",
        phase_or_role="M",
        summary=(
            "Chromosome segregation + cell division.  Five "
            "morphological subphases: prophase (chromosome "
            "condensation, nuclear envelope breakdown) → "
            "prometaphase (kinetochore-microtubule capture) → "
            "metaphase (chromosome alignment at metaphase "
            "plate) → anaphase (sister chromatid separation) → "
            "telophase (nuclear envelope reformation) + "
            "cytokinesis (actomyosin contractile-ring "
            "constriction)."),
        key_components=(
            "Cyclin B-CDK1 (active MPF)", "Aurora kinases A/B",
            "Polo-like kinase 1", "Condensin (chromosome "
            "compaction)", "Cohesin (sister-chromatid linkage)",
            "Spindle microtubules + kinetochores",
            "APC/C E3 ligase (anaphase trigger)",
        ),
        function=(
            "Faithful segregation of the duplicated genome "
            "into two daughter cells."),
        activated_by=(
            "Cyclin B-CDK1 activation (MPF)",
            "APC/C-Cdc20 → Securin destruction → Separase "
            "cleaves Cohesin → anaphase",
        ),
        inhibited_by=(
            "Spindle-assembly checkpoint (SAC) holds APC/C-"
            "Cdc20 in check until every kinetochore is "
            "bipolar-attached",
        ),
        disease_associations=(
            "Chromosomal instability + aneuploidy are "
            "hallmarks of most solid tumours.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "taxanes", "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Taxanes (paclitaxel / docetaxel) stabilise "
            "microtubules → freeze the spindle → SAC stays "
            "engaged → prolonged mitotic arrest → apoptosis."),
    ),
    CellCycleEntry(
        id="g0-phase",
        name="G0 (quiescence)",
        category="phase",
        phase_or_role="G0",
        summary=(
            "Reversible exit from the cell cycle.  Most adult "
            "differentiated cells (neurons, hepatocytes, "
            "lymphocytes at rest) are G0.  Re-entry requires "
            "fresh mitogen exposure + Cyclin D upregulation; "
            "some lineages (terminally-differentiated "
            "neurons, cardiomyocytes) cannot re-enter."),
        key_components=(
            "Hypo-phosphorylated Rb sequestering E2F",
            "High p21 / p27 levels", "Low Cyclin D",
        ),
        function=(
            "Tissue-architecture preservation + metabolic "
            "energy savings between divisions."),
        activated_by=(
            "Mitogen withdrawal", "Contact inhibition",
            "Differentiation cues",
        ),
        inhibited_by=(
            "Mitogen exposure → Cyclin D induction → re-entry",
        ),
        disease_associations=(
            "Loss of G0 maintenance → pre-cancerous hyper"
            "plasia.  Cancer stem cells survive chemotherapy "
            "by dwelling in G0 then re-entering after "
            "treatment.",
        ),
        cross_reference_signaling_pathway_ids=(
            "ampk", "hippo-yap",
        ),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Distinguished from senescence (irreversible exit "
            "with SASP secretory phenotype).  AMPK activation "
            "promotes G0 entry under energy stress."),
    ),

    # ============================================================
    # Checkpoints (4)
    # ============================================================
    CellCycleEntry(
        id="g1-s-restriction-point",
        name="G1/S restriction point",
        category="checkpoint",
        phase_or_role="late G1",
        summary=(
            "The fundamental commitment point of the cell "
            "cycle.  Until the restriction point (R-point) a "
            "cell still requires continuous mitogen exposure; "
            "once past R-point it commits to S-phase + "
            "completes the cycle even if mitogens are "
            "withdrawn.  Mediated by hyperphosphorylation of "
            "Rb → release of E2F → transcription of S-phase "
            "genes (Cyclin E, Cyclin A, dihydrofolate "
            "reductase, etc.)."),
        key_components=(
            "Cyclin D-CDK4/6", "Rb", "E2F", "p16 INK4a",
        ),
        function=(
            "Integrate mitogen signal + DNA-damage status + "
            "cell size into a single binary commitment "
            "decision."),
        activated_by=(
            "Mitogenic growth factors → Cyclin D → CDK4/6 "
            "phosphorylation of Rb",
        ),
        inhibited_by=(
            "p16 INK4a (Cyclin D-CDK4/6 inhibitor)",
            "p21 / p27 / p57", "DNA damage via p53 → p21",
        ),
        disease_associations=(
            "Loss-of-function in p16 INK4a, Rb, or upstream "
            "p53 axis is found in nearly every human cancer.",
        ),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pi3k-akt-mtor", "p53",
            "wnt-beta-catenin", "tgf-beta-smad",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Palbociclib / ribociclib / abemaciclib (CDK4/6 "
            "inhibitors) hold ER+ breast cancer cells before "
            "the R-point.  Combination with endocrine therapy "
            "doubled PFS in the PALOMA / MONALEESA / MONARCH "
            "trial series."),
    ),
    CellCycleEntry(
        id="intra-s-checkpoint",
        name="Intra-S checkpoint",
        category="checkpoint",
        phase_or_role="S",
        summary=(
            "Slows replication-fork progression + suppresses "
            "late-origin firing in response to replication "
            "stress (stalled forks, depleted dNTP pools, UV / "
            "alkylation damage, nucleotide-analogue exposure). "
            " Centrally driven by ATR + Chk1 — the master "
            "kinase pair of the replication-stress response."),
        key_components=(
            "ATR (sensor)", "Claspin (mediator)",
            "Chk1 (effector)", "Cdc25A (degraded → CDK2 "
            "inhibition)",
        ),
        function=(
            "Prevent fork collapse + chromosome breaks during "
            "S-phase by pausing replication until stress "
            "resolves."),
        activated_by=(
            "ssDNA exposure at stalled forks → RPA coating → "
            "ATR-ATRIP recruitment",
        ),
        inhibited_by=(
            "Successful fork restart → checkpoint adaptation "
            "+ resumption of replication",
        ),
        disease_associations=(
            "ATR loss is embryonic lethal; ATR-Seckel syndrome "
            "(hypomorphic alleles) → microcephaly + dwarfism.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "ATR inhibitors (berzosertib / ceralasertib) + "
            "Chk1 inhibitors are in clinical trials for cancers "
            "with high replication stress (especially MYC-"
            "driven or ATM-deficient tumours)."),
    ),
    CellCycleEntry(
        id="g2-m-checkpoint",
        name="G2/M checkpoint",
        category="checkpoint",
        phase_or_role="G2/M",
        summary=(
            "Last opportunity before mitosis to detect + "
            "repair DNA damage.  Holds Cyclin B-CDK1 (MPF) in "
            "the inactive Tyr15-phosphorylated form by "
            "inhibiting Cdc25 phosphatase + activating Wee1 "
            "kinase.  Controlled by ATM/ATR → Chk1/Chk2 → "
            "Cdc25 axis."),
        key_components=(
            "ATM / ATR (sensors)", "Chk1 / Chk2 (effectors)",
            "Wee1 / Myt1", "Cdc25A/B/C", "p53 → 14-3-3σ "
            "(Cyclin B-CDK1 cytoplasmic sequestration)",
        ),
        function=(
            "Prevent entry into mitosis with unrepaired DNA "
            "damage."),
        activated_by=(
            "DNA double-strand breaks via ATM",
            "Replication stress carry-over via ATR",
        ),
        inhibited_by=(
            "Damage repair completion → Cdc25 reactivation + "
            "Wee1 degradation",
        ),
        disease_associations=(
            "Tumour cells with disabled G1/S checkpoint (~ "
            "all cancers) become uniquely dependent on the "
            "G2/M checkpoint for survival — synthetic "
            "lethality opportunity.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Wee1 inhibitor adavosertib (AZD1775) exploits "
            "this dependency in p53-mutant tumours."),
    ),
    CellCycleEntry(
        id="spindle-assembly-checkpoint",
        name="Spindle-assembly checkpoint (SAC)",
        category="checkpoint",
        phase_or_role="prometaphase / metaphase",
        summary=(
            "Holds anaphase onset until every kinetochore is "
            "stably bipolar-attached to spindle microtubules. "
            "Unattached kinetochores generate the mitotic "
            "checkpoint complex (MCC = Mad2-BubR1-Bub3-Cdc20) "
            "which sequesters Cdc20 + inhibits APC/C, "
            "preventing Securin + Cyclin B destruction."),
        key_components=(
            "Mad2", "BubR1", "Bub1", "Bub3", "Mps1 (kinase)",
            "Aurora B (error correction)", "MCC = Mad2-BubR1-"
            "Bub3-Cdc20",
        ),
        function=(
            "Prevent aneuploidy by ensuring no chromosome "
            "segregates before correct bipolar attachment."),
        activated_by=(
            "Unattached kinetochore (Mps1 + Aurora B "
            "phosphorylation cascade)",
        ),
        inhibited_by=(
            "Bipolar tension across all kinetochores → Mps1 "
            "leaves → MCC silenced → APC/C activates",
        ),
        disease_associations=(
            "Mosaic-variegated-aneuploidy syndrome (BUB1B "
            "mutations); SAC weakening drives chromosomal "
            "instability + tumour heterogeneity.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "taxanes", "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Taxanes + vinca alkaloids work by chronically "
            "engaging the SAC.  Mps1 inhibitors (BAY 1217389, "
            "BOS172722) are in trials as next-generation anti-"
            "mitotics."),
    ),

    # ============================================================
    # Cyclin-CDK pairs (4)
    # ============================================================
    CellCycleEntry(
        id="cyclin-d-cdk4-cdk6",
        name="Cyclin D + CDK4 / CDK6",
        category="cyclin-cdk",
        phase_or_role="G1",
        summary=(
            "Mitogen-responsive G1 cyclin-CDK complex.  Three "
            "D-cyclins (D1 / D2 / D3) pair with CDK4 or CDK6.  "
            "Hyperphosphorylates Rb → releases E2F → drives "
            "G1/S transition.  Activity inhibited by INK4 "
            "family (p16 / p15 / p18 / p19)."),
        key_components=(
            "Cyclin D1 (CCND1)", "Cyclin D2", "Cyclin D3",
            "CDK4", "CDK6", "Rb", "p16 INK4a",
        ),
        function=(
            "Convert mitogen signals into Rb hyper"
            "phosphorylation + commitment past R-point."),
        activated_by=(
            "MAPK / ERK", "PI3K / Akt → Cyclin D translation",
            "Wnt / β-catenin → Cyclin D1 transcription",
        ),
        inhibited_by=(
            "p16 INK4a (locks the kinase ATP cleft)",
            "TGF-β → p15 INK4b",
        ),
        disease_associations=(
            "CCND1 amplification drives mantle-cell lymphoma + "
            "ER+ breast cancer; CDK4 amplification in well-"
            "differentiated liposarcoma + glioblastoma.",
        ),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pi3k-akt-mtor", "wnt-beta-catenin",
            "tgf-beta-smad",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Palbociclib (Pfizer, 2015), ribociclib (Novartis, "
            "2017), abemaciclib (Lilly, 2017) — first three "
            "CDK4/6 inhibitors approved for HR+/HER2- breast "
            "cancer.  All three induce G1 arrest + downstream "
            "senescence."),
    ),
    CellCycleEntry(
        id="cyclin-e-cdk2",
        name="Cyclin E + CDK2",
        category="cyclin-cdk",
        phase_or_role="G1/S",
        summary=(
            "Driver of S-phase entry.  E2F-induced; "
            "self-amplifies its own transcription (positive "
            "feedback that creates the bistable switch at "
            "R-point).  Phosphorylates Rb (sustaining its "
            "hyperphosphorylation), p27 (driving its "
            "ubiquitin-mediated degradation), Cdc6 + NPAT + "
            "histones (initiating S-phase gene expression)."),
        key_components=(
            "Cyclin E1 (CCNE1)", "Cyclin E2", "CDK2", "p27",
        ),
        function=(
            "Commit to S-phase + initiate origin firing."),
        activated_by=(
            "E2F transcription factors (Rb-released)",
        ),
        inhibited_by=(
            "p21 / p27 / p57 (CIP/KIP family)",
        ),
        disease_associations=(
            "CCNE1 amplification drives ovarian + uterine "
            "carcinosarcoma (~ 20 % of high-grade serous "
            "ovarian); marker of poor prognosis.",
        ),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pi3k-akt-mtor",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "PKMYT1 inhibitors (lunresertib) target CCNE1-"
            "amplified tumours via synthetic lethality."),
    ),
    CellCycleEntry(
        id="cyclin-a-cdk2-cdk1",
        name="Cyclin A + CDK2 / CDK1",
        category="cyclin-cdk",
        phase_or_role="S → G2",
        summary=(
            "Cyclin A1 (germline-restricted) + Cyclin A2 "
            "(somatic).  Pairs with CDK2 in S-phase + CDK1 in "
            "G2.  Sustains DNA replication + prevents origin "
            "re-firing within the same cycle by phosphorylating "
            "ORC + Cdc6."),
        key_components=(
            "Cyclin A2 (CCNA2)", "CDK2", "CDK1",
        ),
        function=(
            "Sustain S-phase progression + suppress re-"
            "replication.  Hand off CDK1 activity to Cyclin B "
            "as G2 progresses."),
        activated_by=(
            "E2F at the G1/S transition", "Stable through S + "
            "G2",
        ),
        inhibited_by=(
            "APC/C-Cdc20 destruction in early mitosis",
        ),
        disease_associations=(
            "Cyclin A2 overexpression marker in HCC + "
            "lymphoma; rarely a primary driver.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Cyclin A1 (CCNA1) is germ-cell-restricted + a "
            "cancer-testis antigen — explored as immuno-"
            "therapy target."),
    ),
    CellCycleEntry(
        id="cyclin-b-cdk1",
        name="Cyclin B + CDK1 (MPF)",
        category="cyclin-cdk",
        phase_or_role="G2 → M",
        summary=(
            "Mitosis-promoting factor (MPF).  The master "
            "kinase of mitotic entry.  Accumulates in G2, "
            "held inactive by Wee1/Myt1-mediated Tyr15 "
            "phosphorylation, then explosively activated by "
            "Cdc25 dephosphorylation in a positive-feedback "
            "switch.  Phosphorylates hundreds of mitotic "
            "substrates (lamins, condensins, golgi proteins, "
            "myosin, etc.)."),
        key_components=(
            "Cyclin B1 (CCNB1)", "Cyclin B2", "CDK1 (CDC2)",
            "Wee1", "Cdc25A/B/C",
        ),
        function=(
            "Drive nuclear envelope breakdown + chromosome "
            "condensation + spindle assembly + Golgi "
            "fragmentation; the global mitotic-state inducer."),
        activated_by=(
            "Cdc25 dephosphorylation of CDK1 Tyr15",
            "Auto-amplification (CDK1 inhibits Wee1 + "
            "activates Cdc25)",
        ),
        inhibited_by=(
            "Wee1 / Myt1 (Tyr15 + Thr14 phosphorylation)",
            "APC/C-Cdc20 destruction at metaphase / anaphase "
            "transition",
        ),
        disease_associations=(
            "Premature MPF activation → mitotic catastrophe "
            "of damaged cells (an intentional therapeutic "
            "target with Wee1 inhibitors).",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Hartwell + Hunt + Nurse won the 2001 Nobel for "
            "discovering the cyclin / CDK system + the M-phase-"
            "promoting factor.  Hunt's experiments on sea-"
            "urchin egg extracts showed Cyclin B oscillates."),
    ),

    # ============================================================
    # CDK inhibitors (3 — CIP/KIP + INK4)
    # ============================================================
    CellCycleEntry(
        id="p21-cdkn1a",
        name="p21 (CDKN1A / WAF1 / CIP1)",
        category="cdk-inhibitor",
        phase_or_role="G1, G2, S (universal)",
        summary=(
            "Universal CDK inhibitor of the CIP/KIP family.  "
            "Direct p53 transcriptional target — the dominant "
            "downstream effector of p53-mediated cell-cycle "
            "arrest.  Binds + inhibits Cyclin E-CDK2, Cyclin "
            "A-CDK2, and Cyclin B-CDK1.  Also blocks PCNA → "
            "halts DNA replication."),
        key_components=(
            "p21 protein (CDKN1A gene)",
        ),
        function=(
            "Stoichiometric CDK inhibition + PCNA blockade → "
            "G1 / G2 arrest in response to DNA damage, "
            "senescence, or differentiation cues."),
        activated_by=(
            "p53 (canonical)", "TGF-β / Smad",
            "Differentiation cues (Myo D in muscle)",
        ),
        inhibited_by=(
            "Mitogenic Ras signalling (transcriptional "
            "repression)",
        ),
        disease_associations=(
            "Loss-of-expression amplifies the effects of p53 "
            "mutation; over-expression in some chemo-resistant "
            "tumours.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53", "tgf-beta-smad",
        ),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "p21 was the first cyclin-dependent kinase "
            "inhibitor cloned (1993, Bert Vogelstein lab, as "
            "a p53 target)."),
    ),
    CellCycleEntry(
        id="p27-cdkn1b",
        name="p27 (CDKN1B / KIP1)",
        category="cdk-inhibitor",
        phase_or_role="G1",
        summary=(
            "CIP/KIP-family CDK inhibitor whose abundance is "
            "controlled post-translationally by SCF-Skp2 "
            "ubiquitination + Cyclin E-CDK2 phosphorylation. "
            "Holds cells in G0 / quiescence; degraded as "
            "cells re-enter the cycle."),
        key_components=(
            "p27 protein (CDKN1B gene)", "Skp2 E3 ligase",
        ),
        function=(
            "Quiescence maintenance + G1 progression brake."),
        activated_by=(
            "Mitogen withdrawal", "Contact inhibition",
            "TGF-β",
        ),
        inhibited_by=(
            "Cyclin E-CDK2 phosphorylation → SCF-Skp2 "
            "ubiquitination → proteasome", "PI3K / Akt → "
            "cytoplasmic sequestration",
        ),
        disease_associations=(
            "Reduced p27 expression is independently "
            "prognostic of poor outcome in many carcinomas; "
            "Cushing syndrome from MEN4 (germline CDKN1B "
            "mutation).",
        ),
        cross_reference_signaling_pathway_ids=(
            "tgf-beta-smad", "pi3k-akt-mtor",
        ),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "p27 is a haploinsufficient tumour suppressor — "
            "loss of one allele is enough to predispose to "
            "tumours in mouse models."),
    ),
    CellCycleEntry(
        id="p16-ink4a-cdkn2a",
        name="p16 INK4a (CDKN2A)",
        category="cdk-inhibitor",
        phase_or_role="G1",
        summary=(
            "Founding member of the INK4 family.  Specifically "
            "inhibits CDK4 + CDK6 (binds the kinase ATP cleft "
            "+ allosterically prevents Cyclin D binding).  The "
            "CDKN2A locus encodes both p16 INK4a (G1/S brake) "
            "+ p14 ARF (p53 stabiliser via MDM2 inhibition) "
            "from alternative reading frames."),
        key_components=(
            "p16 INK4a (CDKN2A α-transcript)",
            "p14 ARF (CDKN2A β-transcript)",
        ),
        function=(
            "Specific CDK4/6 inhibition + indirect p53 "
            "stabilisation via the ARF arm.  Marker of "
            "cellular senescence."),
        activated_by=(
            "Oncogenic stress (Ras / Myc) → p16 induction",
            "Aging + senescence",
        ),
        inhibited_by=(
            "Promoter hypermethylation in cancer (one of the "
            "most commonly silenced tumour-suppressor loci)",
        ),
        disease_associations=(
            "CDKN2A is the most-frequently inactivated tumour "
            "suppressor in human cancer (melanoma, "
            "glioblastoma, pancreatic, mesothelioma).  "
            "Familial atypical mole-melanoma syndrome (FAMMM) "
            "from germline CDKN2A loss.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "CDK4/6 inhibitors (palbociclib etc.) "
            "pharmacologically replace lost p16 function."),
    ),

    # ============================================================
    # Pocket-protein axis (1)
    # ============================================================
    CellCycleEntry(
        id="rb-e2f-axis",
        name="Rb / E2F axis",
        category="pocket-protein",
        phase_or_role="G1/S transition",
        summary=(
            "The master G1/S transcriptional switch.  Hypo"
            "phosphorylated Rb binds E2F + recruits histone "
            "deacetylases → represses S-phase gene expression. "
            " Cyclin D-CDK4/6 + Cyclin E-CDK2 sequentially "
            "hyperphosphorylate Rb (~ 14 sites) → release E2F "
            "→ transcription of S-phase genes (Cyclin E, "
            "Cyclin A, dihydrofolate reductase, thymidylate "
            "synthase, MCM2-7, …)."),
        key_components=(
            "Rb (RB1)", "p107 (RBL1)", "p130 (RBL2)",
            "E2F1-8", "DP1/2",
        ),
        function=(
            "Bistable on/off switch for S-phase commitment."),
        activated_by=(
            "(Rb tumour-suppressive function) — INK4 + CIP/KIP "
            "inhibition of Cyclin-CDK keeps Rb hypo"
            "phosphorylated",
        ),
        inhibited_by=(
            "Cyclin D-CDK4/6 + Cyclin E-CDK2 hyper"
            "phosphorylation", "HPV E7 / SV40 Large T / "
            "adenovirus E1A oncoprotein binding",
        ),
        disease_associations=(
            "Bilateral retinoblastoma (Knudson two-hit "
            "discovery) → RB1 founded the tumour-suppressor "
            "concept.  Functional Rb loss is universal in "
            "HPV-driven cervical cancer (E7 sequestration).",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Knudson's 1971 two-hit hypothesis explained the "
            "epidemiology of inherited vs sporadic "
            "retinoblastoma + launched the field of cancer "
            "genetics."),
    ),

    # ============================================================
    # Mitotic regulators (8)
    # ============================================================
    CellCycleEntry(
        id="wee1-myt1",
        name="Wee1 / Myt1 (CDK1 inhibitory kinases)",
        category="mitotic-regulator",
        phase_or_role="G2/M",
        summary=(
            "Tyrosine kinases that hold Cyclin B-CDK1 (MPF) "
            "inactive by phosphorylating CDK1 on Tyr15 (Wee1, "
            "nuclear) + Thr14 (Myt1, cytoplasmic / membrane).  "
            "Removed by Cdc25 phosphatase action when entry "
            "into mitosis is permitted."),
        key_components=(
            "Wee1 kinase", "Myt1 (PKMYT1)",
        ),
        function=(
            "Restrain mitotic entry until S-phase complete + "
            "DNA damage repaired."),
        activated_by=(
            "G2/M checkpoint (Chk1 stabilises Wee1)",
        ),
        inhibited_by=(
            "Cyclin B-CDK1 auto-amplification (CDK1 "
            "phosphorylates + inactivates Wee1)",
        ),
        disease_associations=(
            "Pharmacological Wee1 inhibition in p53-mutant "
            "tumours forces them into mitosis with damaged "
            "DNA → mitotic catastrophe.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Wee1 inhibitor adavosertib (AZD1775) reached "
            "Phase 2 trials.  PKMYT1 inhibitor lunresertib "
            "(RP-6306) targets CCNE1-amplified tumours."),
    ),
    CellCycleEntry(
        id="cdc25-family",
        name="Cdc25 phosphatase family",
        category="mitotic-regulator",
        phase_or_role="G1/S, G2/M",
        summary=(
            "Three dual-specificity protein phosphatases "
            "(Cdc25A / B / C) that dephosphorylate the Tyr15 + "
            "Thr14 inhibitory marks on CDKs, activating them. "
            " Cdc25A drives G1/S; Cdc25B+C drive G2/M.  Major "
            "nodes of checkpoint convergence — Chk1 + Chk2 "
            "phosphorylate Cdc25 → 14-3-3 binding → "
            "cytoplasmic sequestration + degradation."),
        key_components=(
            "Cdc25A", "Cdc25B", "Cdc25C", "14-3-3",
        ),
        function=(
            "Remove inhibitory phosphates from CDKs to drive "
            "cell-cycle transitions."),
        activated_by=(
            "Polo-like kinase 1 phosphorylation", "Cyclin B-"
            "CDK1 positive feedback at G2/M",
        ),
        inhibited_by=(
            "Chk1 / Chk2 phosphorylation → 14-3-3 "
            "sequestration + SCF-βTrCP degradation",
        ),
        disease_associations=(
            "Cdc25A overexpression in many carcinomas drives "
            "premature S-phase entry + genome instability.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Named for the Schizosaccharomyces pombe cdc25 "
            "gene — Paul Nurse's foundational 1976 mutant."),
    ),
    CellCycleEntry(
        id="apc-c",
        name="Anaphase-promoting complex / cyclosome (APC/C)",
        category="mitotic-regulator",
        phase_or_role="metaphase / anaphase + G1",
        summary=(
            "Multi-subunit RING-type E3 ubiquitin ligase that "
            "triggers anaphase + sustains G1.  Two activator "
            "switches: Cdc20 (active metaphase → anaphase) + "
            "Cdh1 / Fzr1 (active anaphase → end of G1).  "
            "Substrates include Securin, Cyclin B, Geminin, "
            "Cdc20 itself, Aurora, Plk1.  Inhibited by the "
            "spindle-assembly checkpoint via the MCC."),
        key_components=(
            "APC2 + APC11 (RING module)", "Cdc20 (early "
            "activator)", "Cdh1 / Fzr1 (late activator)",
            "Mitotic checkpoint complex",
        ),
        function=(
            "Trigger sister-chromatid separation by "
            "ubiquitinating Securin → release of Separase → "
            "Cohesin cleavage."),
        activated_by=(
            "Cyclin B-CDK1 phosphorylation (Cdc20 binding)",
            "SAC silencing on full kinetochore tension",
        ),
        inhibited_by=(
            "Mitotic checkpoint complex (Mad2-BubR1-Bub3 + "
            "Cdc20)",
        ),
        disease_associations=(
            "APC/C dysfunction → chromosomal instability "
            "(CIN+) tumours.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Discovered ~ 1995 in Xenopus egg extract / yeast "
            "via the cyclin-destruction box.  Awarded "
            "extensively in Rose / Hershko / Ciechanover's "
            "2004 Nobel for ubiquitin-mediated proteolysis."),
    ),
    CellCycleEntry(
        id="separase-securin",
        name="Separase / Securin",
        category="mitotic-regulator",
        phase_or_role="metaphase → anaphase",
        summary=(
            "Separase is a cysteine protease that cleaves the "
            "Scc1 / Rad21 subunit of cohesin → physically "
            "separates sister chromatids.  Securin binds + "
            "inhibits Separase until APC/C-Cdc20 ubiquitinates "
            "Securin for proteasomal destruction at the "
            "metaphase → anaphase transition."),
        key_components=(
            "Separase (ESPL1)", "Securin (PTTG1)", "Cohesin "
            "(Scc1 / Rad21 subunit)",
        ),
        function=(
            "Execute the irreversible step of sister-chromatid "
            "separation."),
        activated_by=(
            "APC/C-Cdc20-mediated Securin destruction",
            "Cyclin B-CDK1 destruction (relieves CDK-mediated "
            "Separase inhibition)",
        ),
        inhibited_by=(
            "Securin (default state)",
        ),
        disease_associations=(
            "Securin (PTTG1) overexpression in pituitary "
            "adenoma; aneuploidy in separase-dysregulated "
            "tumours.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Separase activation is the irreversible "
            "commitment step of mitosis — the cell-cycle "
            "equivalent of ‘crossing the Rubicon’."),
    ),
    CellCycleEntry(
        id="aurora-kinases",
        name="Aurora kinases A + B",
        category="mitotic-regulator",
        phase_or_role="prophase → cytokinesis",
        summary=(
            "Conserved serine/threonine kinases with non-"
            "redundant mitotic functions.  Aurora A regulates "
            "centrosome maturation + spindle assembly + Cdc25 "
            "activation.  Aurora B is the catalytic core of "
            "the chromosomal passenger complex (CPC = Aurora B "
            "+ INCENP + Survivin + Borealin), correcting "
            "merotelic + syntelic kinetochore-microtubule "
            "attachments."),
        key_components=(
            "Aurora A (AURKA)", "Aurora B (AURKB)", "INCENP",
            "Survivin", "Borealin", "TPX2 (Aurora A "
            "activator)",
        ),
        function=(
            "Centrosome maturation, spindle assembly, error "
            "correction of kinetochore-microtubule attachment, "
            "cytokinetic furrow positioning."),
        activated_by=(
            "TPX2 (Aurora A)", "Auto-phosphorylation in "
            "trans on activation loop",
        ),
        inhibited_by=(
            "Phosphatase PP1 + PP2A counteraction",
            "Specific small-molecule inhibitors (alisertib, "
            "AZD2811)",
        ),
        disease_associations=(
            "Aurora A amplification in 12 % of breast cancers "
            "+ many solid tumours; survivin overexpression "
            "near-universal in cancer.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Alisertib (Aurora A) + AZD2811 (Aurora B) reached "
            "Phase II trials.  Aurora B inhibitors uniquely "
            "induce polyploidy + mitotic slippage."),
    ),
    CellCycleEntry(
        id="polo-like-kinase-1",
        name="Polo-like kinase 1 (Plk1)",
        category="mitotic-regulator",
        phase_or_role="late G2 → mitosis",
        summary=(
            "Master regulator of mitotic entry + progression. "
            "Required for centrosome maturation, mitotic "
            "spindle assembly, kinetochore-microtubule "
            "attachment, sister-chromatid separation, + "
            "cytokinesis.  Activates Cdc25 (driving CDK1 "
            "activation) + Cyclin B nuclear translocation; "
            "phosphorylates APC/C subunits."),
        key_components=(
            "Plk1", "Bora (Plk1 activator)",
        ),
        function=(
            "Multifunctional mitotic kinase + mitotic-entry "
            "trigger."),
        activated_by=(
            "Aurora A + Bora-mediated activation-loop "
            "phosphorylation",
        ),
        inhibited_by=(
            "Specific small-molecule inhibitors (volasertib / "
            "BI 6727, onvansertib)",
        ),
        disease_associations=(
            "Plk1 overexpression in many carcinomas + "
            "haematological malignancies; marker of poor "
            "prognosis.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Onvansertib (PCM-075, Cardiff Oncology) is in "
            "Phase 2 for KRAS-mutant CRC + AML."),
    ),
    CellCycleEntry(
        id="mad2-bubr1-sac-components",
        name="Mad2 / BubR1 / Bub1 / Mps1 (SAC components)",
        category="mitotic-regulator",
        phase_or_role="prometaphase",
        summary=(
            "The molecular core of the spindle-assembly "
            "checkpoint.  Mps1 kinase senses unattached "
            "kinetochores + recruits Bub1 / BubR1 + Mad1 / "
            "Mad2 — forming the mitotic checkpoint complex "
            "(MCC = Mad2-BubR1-Bub3-Cdc20) that sequesters "
            "Cdc20 + inhibits APC/C until every kinetochore "
            "has bipolar tension."),
        key_components=(
            "Mad1", "Mad2", "Bub1 (kinase)", "BubR1 (BUB1B, "
            "pseudokinase)", "Bub3", "Mps1 (TTK kinase)",
            "Aurora B (error-correction interplay)",
        ),
        function=(
            "Delay anaphase onset until every kinetochore is "
            "bipolar-attached → prevent aneuploidy."),
        activated_by=(
            "Unattached kinetochore (high Mps1 activity, "
            "phosphorylates KNL1 → Bub3-Bub1 recruitment)",
        ),
        inhibited_by=(
            "Bipolar tension across all kinetochores (Mps1 "
            "leaves, MCC dissociates, APC/C-Cdc20 activates)",
        ),
        disease_associations=(
            "Mosaic-variegated-aneuploidy syndrome (homozygous "
            "BUB1B mutations); SAC-weakening polymorphisms "
            "drive tumour aneuploidy.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors", "taxanes",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Mps1 / TTK inhibitors (BAY 1217389, BOS172722) "
            "in early trials as next-gen anti-mitotics with "
            "less neuropathy than taxanes."),
    ),
    CellCycleEntry(
        id="condensin-cohesin",
        name="Condensin + Cohesin",
        category="mitotic-regulator",
        phase_or_role="S-phase loading → mitosis",
        summary=(
            "Two SMC-family multi-subunit complexes that "
            "shape mitotic chromosomes.  Cohesin holds sister "
            "chromatids together from S-phase replication "
            "until separase cleavage at anaphase.  Condensin "
            "I + II compact chromosomes ~ 100-fold for "
            "mitotic segregation."),
        key_components=(
            "Cohesin: Smc1 / Smc3 / Scc1 (Rad21) / SA1/SA2",
            "Condensin I: Smc2 / Smc4 / CAP-D2 / CAP-G / "
            "CAP-H", "Condensin II: Smc2 / Smc4 / CAP-D3 / "
            "CAP-G2 / CAP-H2",
        ),
        function=(
            "Sister-chromatid cohesion + mitotic chromosome "
            "compaction."),
        activated_by=(
            "Cyclin B-CDK1 phosphorylation (condensin)",
            "Acetylation of Smc3 by ESCO2 (cohesin "
            "establishment)",
        ),
        inhibited_by=(
            "WAPL (cohesin removal during prophase)",
            "Separase cleavage (cohesin Scc1 destruction at "
            "anaphase)",
        ),
        disease_associations=(
            "Cornelia de Lange syndrome (NIPBL mutations); "
            "Roberts syndrome (ESCO2); cohesinopathies "
            "broadly affect development.  Cohesin mutations "
            "(STAG2, RAD21) common in AML + bladder cancer.",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Cohesin also organises 3D genome architecture in "
            "interphase via loop extrusion — a recent + "
            "rapidly-developing field (Mirny / Dekker)."),
    ),

    # ============================================================
    # DNA-damage-response (5)
    # ============================================================
    CellCycleEntry(
        id="atm-kinase",
        name="ATM kinase",
        category="dna-damage-response",
        phase_or_role="all phases (DSB sensor)",
        summary=(
            "Ataxia-telangiectasia-mutated kinase.  PIKK-"
            "family serine/threonine kinase that senses DNA "
            "double-strand breaks via the MRN complex (Mre11-"
            "Rad50-Nbs1).  Activates Chk2, p53, BRCA1, H2AX, "
            "53BP1 — orchestrating cell-cycle arrest, DNA "
            "repair, or apoptosis depending on damage extent."),
        key_components=(
            "ATM kinase", "MRN complex (Mre11-Rad50-Nbs1)",
        ),
        function=(
            "Master sensor + transducer of double-strand "
            "break signals."),
        activated_by=(
            "DNA double-strand breaks via MRN recruitment",
            "Auto-phosphorylation in trans",
        ),
        inhibited_by=(
            "Specific inhibitors (KU-55933, KU-60019; clinical "
            "candidate AZD0156)",
        ),
        disease_associations=(
            "Ataxia-telangiectasia (homozygous ATM loss): "
            "cerebellar ataxia, immunodeficiency, radio-"
            "sensitivity, lymphoma predisposition.  ATM "
            "heterozygotes have increased breast-cancer risk.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "ATM-inhibitor + radiotherapy combinations are an "
            "active clinical area (e.g. AZD1390 in glioma)."),
    ),
    CellCycleEntry(
        id="atr-kinase",
        name="ATR kinase",
        category="dna-damage-response",
        phase_or_role="S, intra-S checkpoint",
        summary=(
            "ATR (Ataxia-telangiectasia + Rad3-related) is the "
            "master kinase of the replication-stress response. "
            "Sensed by RPA-coated ssDNA at stalled replication "
            "forks; recruited via ATRIP.  Activates Chk1 → "
            "cell-cycle arrest + fork stabilisation."),
        key_components=(
            "ATR kinase", "ATRIP", "TopBP1 (activator)",
            "9-1-1 clamp", "Claspin (Chk1 mediator)",
        ),
        function=(
            "Sense + respond to replication stress + ssDNA."),
        activated_by=(
            "ssDNA exposure at stalled forks → RPA → ATR-"
            "ATRIP loading → TopBP1 + Ewing sarcoma protein"
            "-mediated activation",
        ),
        inhibited_by=(
            "Specific inhibitors (berzosertib / VX-970, "
            "ceralasertib / AZD6738)",
        ),
        disease_associations=(
            "ATR-Seckel syndrome (hypomorphic): microcephaly + "
            "dwarfism.  Complete ATR loss is embryonic "
            "lethal.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "ATR inhibitors show synthetic lethality with "
            "ATM loss + with high replication stress (MYC-"
            "driven, CCNE1-amplified, BRCA-mutant tumours)."),
    ),
    CellCycleEntry(
        id="chk1-chk2",
        name="Chk1 / Chk2 effector kinases",
        category="dna-damage-response",
        phase_or_role="all phases",
        summary=(
            "Effector kinases of the DNA-damage response.  "
            "Chk1 is the major effector downstream of ATR "
            "(replication stress); Chk2 sits downstream of "
            "ATM (DSBs).  Both phosphorylate Cdc25 family → "
            "14-3-3 binding + degradation → CDK inhibition + "
            "cell-cycle arrest.  Chk2 also stabilises p53."),
        key_components=(
            "Chk1 kinase (CHEK1)", "Chk2 kinase (CHEK2)",
        ),
        function=(
            "Convert ATM/ATR damage signal into cell-cycle "
            "arrest by inactivating Cdc25 + activating p53."),
        activated_by=(
            "ATR phosphorylation (Chk1)",
            "ATM phosphorylation (Chk2)",
        ),
        inhibited_by=(
            "Specific inhibitors (prexasertib, MK-8776 — Chk1)",
        ),
        disease_associations=(
            "Germline CHEK2 mutations (Li-Fraumeni-like, "
            "increased breast + colorectal cancer risk).  "
            "Chk1 is essential — no germline LOF tolerated.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Chk1 inhibitors (prexasertib) sensitise tumours "
            "to chemotherapy in trials but Hb / neutropenia "
            "have been dose-limiting."),
    ),
    CellCycleEntry(
        id="brca1-brca2",
        name="BRCA1 / BRCA2",
        category="dna-damage-response",
        phase_or_role="S/G2 (homologous recombination)",
        summary=(
            "Tumour suppressors essential for high-fidelity "
            "homologous-recombination DNA repair.  BRCA1 "
            "functions in damage signalling + Rad51 loading "
            "regulation; BRCA2 directly loads Rad51 onto "
            "ssDNA at resected DSB ends.  Loss-of-function "
            "shifts repair to error-prone non-homologous end "
            "joining → genome instability."),
        key_components=(
            "BRCA1", "BRCA2", "PALB2", "Rad51", "53BP1 "
            "(opposing factor)",
        ),
        function=(
            "Drive faithful homologous-recombination repair "
            "of double-strand breaks during S/G2."),
        activated_by=(
            "ATM-mediated phosphorylation of BRCA1",
            "Resection of DSB ends by MRN + CtIP",
        ),
        inhibited_by=(
            "53BP1 + Shieldin (push toward NHEJ)",
        ),
        disease_associations=(
            "Hereditary breast + ovarian cancer syndrome "
            "(germline BRCA1/2 mutations); ~ 70 % lifetime "
            "breast cancer risk for BRCA1 carriers.  "
            "Synthetic lethality with PARP inhibition is one "
            "of oncology's biggest precision-medicine wins.",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Olaparib (2014, AstraZeneca) — first PARP "
            "inhibitor approved.  Olaparib + niraparib + "
            "rucaparib + talazoparib now standard for "
            "BRCA1/2-mutant ovarian + breast + prostate + "
            "pancreatic cancer."),
    ),
    CellCycleEntry(
        id="p53-master-tumour-suppressor",
        name="p53 master tumour suppressor (cell-cycle role)",
        category="dna-damage-response",
        phase_or_role="all phases",
        summary=(
            "Sequence-specific transcription factor stabilised "
            "by ATM / ATR / Chk1 / Chk2 phosphorylation in "
            "response to DNA damage, oncogenic stress, "
            "ribosomal stress, or hypoxia.  Drives a "
            "transcriptional program of cell-cycle arrest "
            "(p21), DNA repair (DDB2 / GADD45), apoptosis "
            "(PUMA / Bax / Noxa), or senescence depending on "
            "damage extent + cellular context."),
        key_components=(
            "p53 (TP53)", "MDM2 (negative regulator)",
            "p21 (CDKN1A)", "PUMA / Bax / Noxa (apoptosis)",
        ),
        function=(
            "Integrate stress signals into a binary cell-fate "
            "decision: arrest + repair vs apoptosis vs "
            "senescence."),
        activated_by=(
            "ATM / ATR / Chk1 / Chk2 phosphorylation → "
            "blocks MDM2 binding → p53 stabilisation",
            "p14 ARF (oncogenic-stress arm)",
        ),
        inhibited_by=(
            "MDM2 ubiquitination + proteasomal degradation "
            "(default state)", "MDMX (binds p53 transactivation "
            "domain)",
        ),
        disease_associations=(
            "Most-mutated tumour suppressor in human cancer "
            "(~ 50 % of all tumours carry TP53 mutation).  "
            "Li-Fraumeni syndrome (germline TP53).",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53", "intrinsic-apoptosis",
        ),
        cross_reference_pharm_drug_class_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "MDM2 inhibitors (idasanutlin, milademetan) "
            "stabilise wild-type p53 in TP53-WT tumours.  "
            "p53-mutant restoration drugs (PRIMA-1 / APR-246 "
            "/ eprenetapopt) reactivate Y220C + R175H mutants "
            "in vitro."),
    ),
)
