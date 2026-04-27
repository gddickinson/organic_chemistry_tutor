# AI for genomics

The 2020s saw deep learning transform multiple
sub-fields of genomics — protein structure
prediction, regulatory-sequence interpretation,
generative protein design, single-cell analysis, and
clinical genomics.  This lesson surveys the major
technical breakthroughs + their practical impact.

## The breakthrough — AlphaFold + ESM

### AlphaFold2 (DeepMind, 2020-2021)

- Predicts protein 3D structures from sequence at
  near-experimental accuracy.
- Architecture: Evoformer (MSA + pair representation
  attention) + structure module (invariant point
  attention).
- CASP14 (2020) results crashed the structure-
  prediction problem (median GDT-TS 92 vs prior
  state-of-art ~ 70).
- AlphaFold DB (2022): structures for ~ 200 M
  proteins (UniProt + species genomes) — open
  + free.
- Transformed structural biology + drug discovery.

### AlphaFold3 (DeepMind, 2024)

- Extends to protein-ligand + protein-DNA / RNA +
  protein-protein complexes.
- Diffusion-based structure module replaces
  AlphaFold2's IPA.
- Predicts modified residues + glycosylation +
  ions.
- Closed source initially; open weights released
  with restrictions.

### ESMFold (Meta AI, 2022)

- Single-sequence (no MSA) → structure via
  pretrained protein language model (ESM-2).
- ~ 60× faster than AlphaFold2 at modest accuracy
  trade-off.
- Enabled metagenomic-scale prediction (ESM
  Metagenomic Atlas — 700 M+ structures).

### Open + commercial follow-ons

- **OmegaFold + RoseTTAFold + RoseTTAFold2** —
  alternative architectures.
- **OpenFold + ColabFold** — open-source AlphaFold
  reimplementations + interactive notebooks.
- **HelixFold + IgFold + AbLang2** — antibody-
  specific.
- **Boltz-1** — new generation diffusion-based
  predictor.

## Protein language models (PLMs)

Models trained on millions of protein sequences as
text:

- **ESM-1b / ESM-2 / ESM-3** — Meta's series; ESM-3
  (2024) is multimodal (sequence + structure +
  function).
- **ProtBert / ProtT5** — older Rostlab.
- **AntiBERTy + IgLM** — antibody-specific.
- **AlphaMissense** (DeepMind 2023) — missense-
  pathogenicity prediction at scale (ESM-style
  variant scoring across ~ 70 M coding variants;
  19 % rated likely pathogenic).

Applications:
- Variant-effect prediction (zero-shot from sequence
  likelihood).
- Protein-function annotation (BLAST-free).
- Engineering candidate identification.
- Embedding for downstream classifiers.

## Generative protein design

### RFdiffusion (Baker lab + Meta, 2023)

- Diffusion-based protein-backbone generator.
- Conditioned on binding-site geometry, motif, or
  scaffold.
- Designs novel proteins binding chosen targets
  (TGFβ inhibitors, cancer-target binders, etc.).
- Open-source.

### ProteinMPNN (Baker lab, 2022)

- Inverse-folding: backbone → sequence.
- Designs sequences that fold into a given
  3D structure.
- High experimental success rates (~ 50-90 %) for
  designed binders.

### Generative + functional design pipelines

- **Designed enzymes** for organophosphate
  hydrolysis, Diels-Alderase, retro-aldolase
  (Baker lab classics, now supercharged with
  RFdiffusion + ProteinMPNN).
- **Designed binders** for SARS-CoV-2 spike, IL-2,
  influenza HA, GLP-1R, cancer antigens.
- **De-novo enzymes** for industrial chemistry +
  bioremediation.

## Regulatory + genomic-sequence models

### Enformer (DeepMind 2021)

- Transformer for sequence-to-function regulatory
  prediction.
- Input: 200-kb sequence; output: cell-type-
  specific RNA + chromatin signal predictions
  across thousands of tracks.
- Outperformed Basenji + DeepSEA on benchmarks.

### Basenji + Borzoi (Calico / Kelley)

- CNN-based regulatory predictors.
- Borzoi: gene-expression prediction across human
  + mouse tissues.

### Sequence-to-expression / regulatory ML

- **Enformer + Borzoi** — bulk regulation.
- **Aleph** + **Lyra** — chromatin + 3D contacts.
- **scBasset + scGPT + Geneformer** — single-cell
  modelling.
- **Variant interpretation** — predict effect of
  non-coding SNPs by comparing reference vs alt
  predictions.

## Single-cell ML

- **scVI / scANVI / TotalVI / MultiVI / scArches**
  (Theis lab) — VAE-based single-cell normalization
  + integration + transfer learning + reference-
  to-query mapping.
- **Geneformer + scGPT + UCE + CellPLM** —
  pretrained transformers for single-cell;
  zero-shot cell-type annotation + perturbation
  prediction.
- **Tangram + cell2location + RCTD + CARD** —
  spatial transcriptomic deconvolution.

## Clinical genomics ML

### Variant-effect prediction

- **CADD + REVEL + MetaSVM + AlphaMissense + EVE +
  PrimateAI** — coding variant pathogenicity.
- **SpliceAI + Pangolin + SpliceTransformer** —
  splice-disrupting variants.
- **Enformer-derived non-coding scoring** — for
  regulatory variants.

### Diagnostic + prognostic

- **Histopathology image-classification** —
  PathAI + Paige + iCare + Tempus.
- **Radiogenomics** — ML models predicting
  molecular subtypes from imaging.
- **Multi-modal models** — integrating WGS +
  WES + RNA-seq + clinical for diagnosis.

### Polygenic risk scores

- **Bayesian + ML PRS methods** — LDpred-funct,
  PRS-CSx, MegaPRS — improve over standard
  C+T (clumping + thresholding).
- **TL-Multi + JointPRS** — multi-ethnic transfer
  learning to address ancestry bias.

## Drug discovery

### Structure-based AI

- **AlphaFold-Multimer + AlphaFold3** — predict
  protein-ligand + protein-protein complexes.
- **DiffDock + EquiBind + Boltz** — diffusion-
  based docking.
- **Enzyme + binder design** with RFdiffusion +
  ProteinMPNN.

### Generative chemistry

- **Insilico Medicine** — Pharma.AI platform; first
  AI-designed candidate (INS018_055 IPF) entered
  Phase 2 clinical trials.
- **Recursion + Atomwise + BenevolentAI + Cradle +
  Iktos** — generative + search-based discovery.
- **Diffusion + transformer-based small-molecule
  generation** (e.g. MolDiff, GeoDiff, ChemBERTa).

## Single-cell + multi-omic foundation models

A 2023-2026 trend toward "foundation models"
trained on millions of cells:

- **Geneformer** (Theodoris 2023) — transformer
  trained on 30 M cells; zero-shot perturbation
  prediction.
- **scGPT** (Cui 2024) — transformer trained on
  33 M cells; multi-task fine-tuning.
- **scBasset** — sc ATAC-seq.
- **UCE** (Universal Cell Embedding) — cross-
  species single-cell embedding.
- **CellPLM + Cell2Sentence** — alternatives.

Open question: do these models really capture
biology beyond what classical methods do?  Active
benchmarking + critique.

## Multi-omic + multi-modal

Models combining multiple data types per cell:
- **Multi-VI / Multi-MAP** — VAE-based.
- **Cobolt + UnionCom / iNMF** — data-integration
  methods.
- **MOFA+ + MOFA2** — Bayesian factor analysis.

## Real-world impact + caution

### Where AI is genuinely transforming work

- Protein structure prediction → near-zero-cost
  for any new sequence.
- Clinical variant interpretation (AlphaMissense
  + SpliceAI) — expanding actionable variants.
- High-throughput screening triage (ML for hit
  prioritisation).
- Single-cell cell-type annotation (CellTypist +
  Azimuth + Geneformer).

### Where AI's promise has been overstated

- Drug-discovery generative models still need
  extensive medicinal-chemistry follow-up; few
  AI-designed clinical candidates yet.
- Foundation single-cell models often don't
  outperform well-tuned classical methods.
- Variant-interpretation models are well-trained
  on common variants but uncertain on rare /
  non-European-ancestry variants.
- Clinical adoption remains slower than hype
  suggests.

### Where caution is needed

- Training-data bias → ancestry / sex / age
  bias in predictions.
- Hallucination — generative models output
  plausible-but-wrong predictions.
- Reproducibility — version + dependency drift
  in fast-moving codebases.
- Interpretability — black-box predictions in
  clinical contexts raise regulatory concerns.
- Privacy + consent — large genomic datasets
  + ML enable re-identification risks.

## Software + infrastructure

Most of the above ML lives in:
- **PyTorch** + **JAX** + **TensorFlow**.
- **Hugging Face** for model + dataset hosting.
- **Hydra + Lightning + Triton + DeepSpeed** for
  training infrastructure.
- **scvi-tools + scArches** for single-cell ML.
- **Bioconda + conda-forge** for environment
  management.
- **Nextflow + Snakemake + WDL** for pipeline
  orchestration.

## Future directions

- **Foundation models** for genomics (scGPT,
  Enformer-style + larger).
- **AI-designed clinical candidates** entering
  the clinic in numbers.
- **End-to-end genomic-medicine workflows** —
  WGS → variant interpretation → ACMG
  classification → reporting via ML pipelines.
- **Spatial + multi-modal foundation models** at
  whole-tissue scale.
- **Interpretability + explainability** advances
  for clinical trust.
- **Privacy-preserving ML** (federated learning,
  differential privacy) for sensitive genomic
  data.

## Cross-link

The GM-1.0 catalogue's `illumina-short-read`,
`pacbio-hifi`, `ont-nanopore`, `scrna-seq`, +
`bottom-up-proteomics` entries provide the
upstream technology layer.  See also **PH-3.0
graduate "Computational drug discovery"** for
drug-discovery applications + **AB-3.0 graduate
"Neuroscience frontiers"** for the AI-neuroscience
interface.

## Try it in the app

- **OrgChem → Macromolecules → Proteins** — fetch
  AlphaFold-predicted structures.
- **Window → Genetics + Molecular Biology Studio →
  Techniques** — every technology generating data
  for these ML pipelines.
- **Window → Pharmacology Studio → Drug classes** —
  AI-discovered + AI-designed therapeutics.

This concludes the GM-3.0 graduate tier + the
GM-3.0 tutorial expansion as a whole.

The next round will start the **-4 tutorial-
expansion chain** across the existing 6 siblings
(CB-4.0 → AB-4.0), adding ~ 12 more lessons each.
