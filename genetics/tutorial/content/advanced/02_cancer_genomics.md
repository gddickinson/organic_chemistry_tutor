# Cancer genomics

Cancer is fundamentally a disease of somatic-cell
genome evolution.  Cancer genomics has produced one of
biology's most-detailed disease catalogues + has
transformed clinical oncology over the past 15 years.

## Cancer as somatic evolution

Every cancer:
- Acquires somatic mutations during life.
- Selects on those that confer growth advantage.
- Evolves clonal + subclonal architecture under
  selection (treatment + immune + microenvironmental).
- Maintains the ancestral cell's tissue-of-origin
  signature plus added drivers + passengers.

Hanahan + Weinberg 2000 + 2011 + 2022 hallmarks:
- Sustained proliferation.
- Evading growth suppressors.
- Resisting cell death.
- Enabling replicative immortality.
- Inducing angiogenesis.
- Activating invasion + metastasis.
- Reprogramming energy metabolism.
- Avoiding immune destruction.
- Genome instability + mutation (enabling).
- Tumour-promoting inflammation (enabling).
- (2022 additions) Phenotypic plasticity, non-mutational
  epigenetic reprogramming, polymorphic microbiomes,
  senescent cells.

## Drivers vs passengers

- **Drivers** — variants that confer selective
  growth advantage; recurrent across many tumours;
  enriched in known cancer genes.
- **Passengers** — variants neutral or near-neutral
  for fitness; the vast majority of mutations.

Identifying drivers:
- **Recurrence** — same gene hit in many tumours
  beyond background.
- **Mutational hotspots** — same residue (eg
  KRAS G12, BRAF V600, IDH1 R132).
- **Pattern-recognition** — gain-of-function (oncogenes:
  KRAS, EGFR, MYC, BCL2) vs loss-of-function (tumour
  suppressors: TP53, RB1, PTEN, BRCA1/2, APC, CDKN2A).
- **Computational drivers** — MutSigCV, OncoDriveCLUST,
  20/20+, MutPanning.

Reference catalogues:
- **COSMIC** — catalogue of somatic mutations in
  cancer (Sanger).
- **OncoKB** — therapeutic levels of evidence (MSKCC).
- **CIViC** — community-curated.
- **JAX CKB** — clinical knowledgebase.
- **CGI** — Cancer Genome Interpreter.

## Major cancer-genomics consortia

- **TCGA** (The Cancer Genome Atlas, 2006-2018) —
  > 11 000 tumours across 33 cancer types; multi-omic
  (WES, WGS, methylation, proteomics, RNA-seq).
- **ICGC** (International Cancer Genome Consortium) +
  **PCAWG** (Pan-Cancer Analysis of Whole Genomes) —
  > 2 600 WGS pan-cancer.
- **GENIE** (AACR) — > 100 K clinical-sequencing
  records.
- **MSK-IMPACT + Foundation Medicine + Caris**
  panels — clinical sequencing at scale.

## Mutational signatures

Mutational processes leave characteristic patterns
in 96-trinucleotide-context space:

- **SBS1 + SBS5** — clock-like; accumulate with
  age.
- **SBS2 + SBS13** — APOBEC family activity;
  C→T + C→G in TCW context.
- **SBS3** — homologous-recombination deficiency
  (HRD); BRCA1 / BRCA2 LOF.
- **SBS4** — tobacco smoking.
- **SBS6 + SBS15 + SBS20 + SBS26 + SBS44** —
  mismatch-repair deficiency (MSI / MMR).
- **SBS7a-d** — UV exposure (CC > TT skin cancers).
- **SBS22** — aristolochic acid.
- **SBS25** — chemotherapy alkylating agents.

Reference: **Alexandrov / COSMIC mutational
signatures** (v3.3 has 78 SBS + 11 DBS + 17 ID
signatures).

These signatures are clinically actionable:
- HRD signature → PARP inhibitor sensitivity.
- MMR / MSI signature → checkpoint-inhibitor
  sensitivity.
- Tobacco signature → confirm smoking history.

## Tumour-mutational burden (TMB)

- Total non-synonymous + truncating mutations per Mb
  of coding sequence.
- Predicts immune-checkpoint-inhibitor response (≥ 10
  mut/Mb is a common cut-off; FDA-approved indication
  for pembrolizumab).
- Hyper-mutated tumours: melanoma + NSCLC + bladder +
  MSI-H colorectal.
- Low TMB: HR+ breast, prostate, kidney.

## Microsatellite instability (MSI)

- Indels at short repeat tracts due to mismatch-
  repair (MMR) deficiency (MLH1 / MSH2 / MSH6 /
  PMS2).
- MSI-H tumours: ~ 15 % of colorectal, ~ 30 % of
  endometrial, < 5 % of most others.
- Strong response to anti-PD-1 (FDA tissue-
  agnostic approval — pembrolizumab).
- Detected by MSI-PCR (MSI Analysis System) or
  MSIsensor / MSIcaller from NGS data.

## Liquid biopsy + ctDNA

Cell-free tumour DNA (ctDNA) circulates in blood:

- **Detection** — ctDNA-fraction varies (< 0.01 %
  to > 50 %); deep-sequencing + UMI dedup needed
  for low-fraction.
- **Tumour-informed (MRD)** — sequence tumour to
  identify variants → personalised assay tracks
  those variants in blood.
- **Tumour-naive** — cancer-broad panel detects
  driver mutations without requiring tumour
  tissue.

Use cases:
- **MRD (minimal residual disease)** — post-
  surgery surveillance + adjuvant-treatment
  guidance.  Natera Signatera + Inivata RaDaR +
  ArcherDX PCM-Seq + Roche Avenio.
- **Companion diagnostics** — Foundation Medicine
  CDx + Roche cobas EGFR + Guardant360 CDx.
- **Pan-cancer early detection** — Galleri
  (GRAIL) + DELFI Diagnostics + Bluestar Genomics.
- **Tumour-of-origin classification**.
- **Treatment response monitoring + resistance-
  emergence**.

## Single-cell + spatial cancer genomics

- **scRNA-seq** of tumour + microenvironment maps
  cellular heterogeneity (tumour cells, T cells,
  macrophages, fibroblasts, endothelial cells).
- **scATAC-seq** + **scNanoseq** (long-read) +
  **scWGS** for somatic variant + clonal-architecture
  mapping.
- **Spatial transcriptomics** (Visium, Xenium,
  CosMx) maps the tumour-microenvironment geometry.
- **Multi-modal integration** (CITE-seq, TEA-seq,
  ASAP-seq) combines RNA + protein + chromatin.

Major projects: HTAN (Human Tumor Atlas Network),
HCA Cancer, Tumor Atlas Pilot Projects.

## Clinical-grade NGS panels

In 2026, most large cancer centres use a hybrid-
capture panel covering:

- **300-500 cancer genes** — drivers + actionable
  + germline-cancer-syndrome genes.
- **Targeted introns + UTRs** — for fusion + SV
  detection.
- **Sequencing depth** — typically 500-1000× tumour;
  100× normal; 1000-5000× ctDNA.

Notable platforms:
- **MSK-IMPACT** — 505 genes; > 100 K patients.
- **Foundation Medicine FoundationOne CDx** —
  324 genes; FDA-approved.
- **Tempus xT** + **Caris MI** — comprehensive +
  immune profiling.
- **Guardant360** — > 70-gene ctDNA panel.

## Structural-variant + fusion gene detection

Many cancers driven by structural variants:
- **BCR-ABL** (CML, t(9;22)) — imatinib +
  follow-on TKIs.
- **EML4-ALK** (NSCLC) — crizotinib + alectinib +
  brigatinib + lorlatinib.
- **ROS1, RET, NTRK fusions** — selpercatinib +
  pralsetinib + larotrectinib + entrectinib.
- **TMPRSS2-ERG** (~ 50 % of prostate adenocarcinoma).
- **MYC translocations** — Burkitt + DLBCL.

Detection — RNA-seq fusion callers (STAR-Fusion,
FusionCatcher, Arriba); panel-based DNA capture (intronic
target-tiling); long-read DNA / RNA + optical mapping
for complex SVs.

## Tumour heterogeneity + clonal evolution

Tumours are mosaic populations:
- **Clonal** mutations — present in all cells.
- **Subclonal** mutations — present in fractions.
- **Branched evolution** — multiple subclones with
  shared early drivers + private late mutations.
- **Convergent evolution** — independent subclones
  acquire similar mutations (often resistance).

Tools: PyClone-VI, sciClone, CITUP, Canopy,
SubClonalSelection.

## Cancer immunology + neoantigens

- **Neoantigens** — tumour-specific peptides from
  somatic mutations presented on MHC.
- **HLA typing** + epitope-prediction (NetMHCpan,
  MHCflurry, BigMHC) identifies candidates.
- **Personalised cancer vaccines** — Moderna mRNA-
  4157 + Merck pembrolizumab in melanoma (Phase 3
  KEYNOTE-942 successful 2024).
- **T-cell receptor (TCR) discovery** — single-cell
  + bulk TCR-seq; identifies TCRs targeting tumour
  antigens.
- **TIL therapy** — Iovance lifileucel (FDA 2024,
  melanoma).
- **TCR-T** — Adaptimmune Tecelra (afami-cel, FDA
  2024, synovial sarcoma).
- **CAR-T** — covered in PH-3.0 graduate "Modern
  modalities".

## Cancer-driving epigenetics

- **DNA methylation** — CIMP (CpG island methylator
  phenotype) in MSI colorectal; methylation
  classifiers for CNS tumours (Capper 2018).
- **Chromatin remodellers** — SWI/SNF (ARID1A,
  SMARCB1, SMARCA4); polycomb (EZH2); MLL
  family.
- **Histone mutations** — H3K27M (paediatric DIPG),
  H3G34R (paediatric glioblastoma), H3.3
  oncohistones.

## Pharmacogenomics in oncology

Targeted therapies based on tumour genotype:

- **HER2-amplified** → trastuzumab + T-DM1 + T-DXd
  + pertuzumab.
- **EGFR-mutant NSCLC** → erlotinib / gefitinib /
  osimertinib (T790M-active).
- **KRAS G12C** → sotorasib + adagrasib.
- **BRAF V600E** → dabrafenib + encorafenib +
  trametinib + binimetinib.
- **MEK + ERK** → trametinib, binimetinib, cobimetinib;
  ulixertinib.
- **CDK4/6** in HR+ breast → palbociclib +
  ribociclib + abemaciclib.
- **PI3K + AKT + mTOR** → alpelisib + capivasertib
  + everolimus + sirolimus.
- **PARP inhibitor** for HRD/BRCA → olaparib +
  niraparib + rucaparib + talazoparib.
- **Anti-angiogenic** → bevacizumab + ramucirumab
  + axitinib + sunitinib.
- **Tissue-agnostic** approvals — pembrolizumab
  (MSI-H, TMB ≥ 10), larotrectinib (NTRK fusion),
  selpercatinib (RET fusion), dostarlimab (MSI-H
  endometrial).

## Cross-link

The GM-1.0 catalogue's `illumina-short-read`,
`pacbio-hifi`, `digital-pcr`, `chip-seq`, `bisulfite-
seq`, `methylation-array`, `scrna-seq`, +
`bottom-up-proteomics` entries provide the
technologies underpinning cancer genomics.  See also
**PH-3.0 graduate "Computational drug discovery"**
+ **PH-3.0 graduate "Modern modalities"** + **CB-3.0
advanced "Cancer signalling networks"**.

## Try it in the app

- **Window → Pharmacology Studio → Drug classes** —
  every targeted therapy listed above.
- **Window → Cell Biology Studio → Signalling** —
  pathway-context for drivers (RAS-MAPK, PI3K-Akt,
  cell-cycle, p53).
- **Window → Genetics + Molecular Biology Studio →
  Techniques** — multi-modal cancer-genomics
  workflows.

Next: **Single-cell + spatial omics workflows**.
