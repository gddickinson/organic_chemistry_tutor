# Signalling-related enzymes

Cells use enzymes not just for metabolism but as the
fundamental units of information processing.  Kinases,
phosphatases, and ATPases together form the molecular
language of intracellular signalling.

## Protein kinases — the writers

Protein kinases transfer the γ-phosphate of ATP to a
Ser / Thr / Tyr (or in some cases His) on a substrate
protein.  The human genome encodes ~ 518 kinases (the
"kinome") + ~ 200 pseudo-kinases — a substantial fraction
of all protein-coding genes.

### The kinase fold

Every eukaryotic protein kinase shares the bilobal Hanks
fold (Susan Taylor's PKA crystal structure 1991 was the
template).

- **N-lobe** — small, β-sheet rich; binds ATP via the
  glycine-rich P-loop (GxGxxG motif).
- **C-lobe** — larger, α-helical; binds substrate +
  carries the catalytic loop.
- **ATP-binding cleft** sits at the lobe interface +
  contains the gatekeeper residue that drug designers
  exploit for selectivity.
- **Activation loop** — flexible segment whose
  phosphorylation flips the kinase between active +
  inactive conformations (DFG-in vs DFG-out).
- **αC-helix** position controls catalytic competence
  ("αC-in" = active).

### Major kinase families

The kinome divides into ~ 10 groups:

- **AGC kinases** — PKA, PKC, PKG, Akt/PKB, S6K.
- **CMGC** — CDKs, MAPKs (ERK, JNK, p38), GSK-3.
- **TK** — receptor tyrosine kinases (EGFR, FGFR, VEGFR,
  insulin R) + non-receptor (Src, Abl, JAK).
- **CAMK** — Ca²⁺/calmodulin-dependent (CaMKII).
- **STE** — MAP-kinase kinase kinases.
- **CK1** — casein kinase 1 family.
- **TKL** — tyrosine-kinase-like (RAF, BRAF).

### PKA — the textbook example

cAMP-dependent protein kinase A is the classical
allosteric kinase + signalling terminus of the GPCR / Gs
/ adenylate-cyclase / cAMP cascade.

Inactive state: R₂C₂ tetramer (regulatory dimer + 2
catalytic subunits).  cAMP binds the R subunits → 4 cAMP
per tetramer → C subunits release + active.

Substrate motif: **Arg-Arg-X-Ser/Thr-Φ** (Φ = bulky
hydrophobe).  Hundreds of substrates, organised into
distinct PKA-anchoring populations by AKAPs (A-kinase
anchoring proteins) for spatial specificity.

### Receptor tyrosine kinases (RTKs)

EGFR / HER2 / FGFR / VEGFR / insulin-R / KIT / PDGFR / c-
MET are all single-pass transmembrane proteins that
dimerise upon ligand binding → trans-autophosphorylation
of activation-loop Tyr → recruitment of SH2-domain
adaptors (Grb2, Shc, PLCγ, PI3K p85) → MAPK + PI3K
cascades.

Cancers frequently activate RTK signalling:
- EGFR-mutant NSCLC (T790M gatekeeper, exon-19 del,
  L858R).
- HER2-amplified breast cancer.
- BCR-ABL fusion (Philadelphia chromosome) drives CML.
- ALK / ROS1 / RET / NTRK fusions in NSCLC + thyroid +
  paediatric cancers.

### Kinase inhibitor drug class

The biggest pharmacological success story of the past
two decades:

- **Imatinib** (Gleevec, 2001) — BCR-ABL → cured CML.
  Lead drug of the kinase-inhibitor era; binds DFG-out
  inactive state.
- **Erlotinib / Gefitinib** — EGFR (NSCLC).
- **Osimertinib** — covalent, T790M-active EGFR (3rd-gen
  NSCLC).
- **Dabrafenib + Trametinib** — BRAF V600E + MEK in
  melanoma (combination).
- **Ibrutinib** — covalent BTK in CLL / MCL.
- **Palbociclib** — CDK4/6 in HR+ breast cancer.
- **Ruxolitinib** — JAK1/2 in myelofibrosis + atopic
  dermatitis.
- **Tofacitinib + baricitinib** — JAK in RA + COVID.

> 80 small-molecule kinase inhibitors are FDA-approved
(2026) — a testament to the druggability of the ATP
pocket + the value of kinase signalling targets.

## Protein phosphatases — the erasers

Phosphorylation is reversible — phosphatases remove the
phosphate.

### Ser/Thr phosphatases

- **PP1** — most abundant; ~ 200 regulatory subunits
  define substrate + localisation.
- **PP2A** — heterotrimeric (A + B + C); broad substrate
  set; tumour suppressor (B subunits).  Inhibited by
  okadaic acid (research tool + a marine toxin).
- **PP2B / calcineurin** — Ca²⁺/CaM-activated.  Drug
  target: cyclosporine + tacrolimus inhibit calcineurin
  via cyclophilin / FKBP12 bridges → block NFAT
  dephosphorylation → block T-cell activation
  (transplant immunosuppression).
- **PP2C** — Mg²⁺-dependent.

### Tyr phosphatases (PTPs)

- **PTP1B** — major insulin-receptor / leptin-receptor
  phosphatase.  Long-pursued obesity / diabetes target;
  catalytic-cysteine + shallow active site = poor
  druggability has limited progress.
- **SHP2 (PTPN11)** — oncogenic + a cancer drug target;
  allosteric SHP2 inhibitors (TNO155) in trials.
- **CD45** — T-cell receptor PTP; required for TCR
  signalling.

### Dual-specificity phosphatases

Hydrolyse both pSer/pThr + pTyr.  Example: **MKPs**
(MAP-kinase phosphatases) terminate ERK / JNK / p38
signalling.

## ATPases — the workhorses

Enzymes that hydrolyse ATP coupled to mechanical or
chemical work:

### P-type ATPases — auto-phosphorylated

Na⁺/K⁺-ATPase, Ca²⁺-ATPase (SERCA + PMCA), H⁺/K⁺-ATPase
(gastric), H⁺-ATPase.  Form a covalent phosphoenzyme
intermediate (Asp-P) during transport cycle.

- **Na⁺/K⁺-ATPase** pumps 3 Na⁺ out + 2 K⁺ in per ATP →
  resting membrane potential, secondary-active
  transport drive.  Inhibited by **digoxin** (heart
  failure, atrial fibrillation) + **ouabain**.
- **SERCA** (sarco/endoplasmic-reticulum Ca²⁺-ATPase)
  re-loads SR Ca²⁺ stores.  Inhibited by **thapsigargin**
  → triggers ER stress / apoptosis (research tool).
- **H⁺/K⁺-ATPase** acidifies stomach.  Inhibited by
  proton-pump inhibitors **omeprazole / pantoprazole**.

### V-type ATPases

Vacuolar; acidify lysosomes / endosomes / secretory
vesicles.  Inhibited by **bafilomycin A1** + **concanamycin**
(research tools).  V-ATPase deregulation contributes to
tumour-microenvironment acidification + osteoporosis.

### F-type ATPases

ATP synthase running in reverse.  Mitochondrial F1F0 was
covered in the previous lesson.

### AAA+ ATPases

Energise diverse remodelling machines:
- **Proteasome** 19S regulatory cap.
- **Dynein** + **kinesin** + **myosin** — cytoskeletal
  motors.
- **DNA helicases** (MCM, RecQ, BLM).
- **Hsp104 / ClpB** — disaggregases.
- **p97 / VCP** — substrate extraction for ERAD.

### ABC transporters

ATP-binding cassette superfamily — > 50 in humans.

- **CFTR** — chloride channel; mutated in cystic
  fibrosis (ΔF508).  Modulators (lumacaftor +
  ivacaftor + tezacaftor + elexacaftor) restore
  trafficking + gating.
- **MDR1 / P-gp** — multidrug-resistance pump; effluxes
  chemotherapy out of tumour cells.
- **BCRP / ABCG2** — secondary multidrug-resistance.

## Other signalling enzymes worth knowing

- **Adenylate cyclase** (ATP → cAMP) — 9 transmembrane
  isoforms + 1 soluble.  Activated by Gαs (Gαs-Q227L
  oncogene drives McCune-Albright + somatotrophinomas).
- **Guanylate cyclase** (GTP → cGMP) — soluble (NO-
  responsive, drug target sildenafil-via-PDE5) +
  particulate (ANP / BNP receptors).
- **Phospholipase C** (PIP₂ → IP₃ + DAG) — Gq + RTK
  effector.
- **Protein arginine methyltransferases (PRMTs) +
  histone methyl/acetyl-transferases** — chromatin
  signalling.

## Why signalling enzymes are evolutionarily ancient

The ATP-driven phosphorylation circuit predates
eukaryotes.  Bacterial **two-component systems** use
sensor histidine kinases + response-regulator aspartate
phosphorylation — a simpler architecture but the same
core idea: a covalent phosphate flag toggles a downstream
state.  Eukaryotic Ser/Thr/Tyr signalling networks
expanded this minimally several hundred-fold.

## Try it in the app

- **Window → Biochem Studio → Enzymes** — `pka` + `egfr-
  kinase` + `na-k-atpase` entries.
- **Window → Biochem Studio → Cofactors** — `atp` for
  the universal phosphoryl donor.
- **Window → Pharmacology Studio → Receptors** — kinase
  inhibitor drug-target context.
- **Window → Cell Biology Studio → Signalling** —
  `gpcr-camp-pka`, `rtk-mapk`, `pi3k-akt` pathways.

Next: **Drug metabolism enzymology**.
