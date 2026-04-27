# Plant single-cell + spatial transcriptomics

The single-cell + spatial-omics revolution that
transformed animal cell biology in 2015-2025 is
now being applied to plant tissues — with some
plant-specific twists.  This lesson surveys methods
+ findings + remaining challenges.

## Why single-cell biology is hard in plants

Plant cells present unique technical challenges:
- **Cell wall** — must be removed for protoplasting
  + droplet-based scRNA-seq, but enzymatic
  digestion stresses cells + alters transcriptomes.
- **Diversity in size** — cells range from < 10 µm
  guard cells to giant > 1 mm sieve elements →
  no one droplet system works for all.
- **High vacuole content** — most cytoplasm is
  vacuole; RNA per cell varies wildly.
- **Phenolic + polysaccharide compounds** can
  interfere with library prep.
- **Cell types are positionally defined** — annotation
  needs spatial information; pure cluster-based
  analysis is harder than in animals.

## Method overview

### Protoplast-based scRNA-seq

The dominant approach (most published plant scRNA-seq).

1. Enzymatic cell-wall digestion (cellulase,
   pectinase, macerozyme) → protoplast suspension.
2. Cell sorting / droplet capture (10x Genomics
   Chromium, Drop-seq, in-house microfluidics).
3. Standard library prep + sequencing.
4. Computational analysis with stress-response
   gene filtering to handle protoplasting artefacts.

Caveats:
- Cell-wall removal triggers wound response → genes
  like **WRKY40 + JAZ + PAD3** spike.
- Filter these "protoplasting genes" before
  clustering.
- Some cell types resist protoplasting (xylem
  fibres, sclereids).

Iconic plant scRNA-seq atlases:
- **Arabidopsis root** — multiple papers from 2019;
  cell-type annotation maps to known marker genes
  (cortex, endodermis, pericycle, stele, root cap,
  trichoblast / atrichoblast, root-hair specification).
- **Arabidopsis shoot apical meristem + leaves**.
- **Maize ear + tassel + leaf**.
- **Rice + tomato + cotton + soybean** atlases.

### Single-nucleus RNA-seq (snRNA-seq)

Avoids protoplasting:
1. Tissue cryosectioned + nuclei isolated by
   detergent + sucrose gradient or FACS.
2. Droplet-based capture (10x Multiome works on
   nuclei).
3. Lower transcript counts per cell vs scRNA-seq
   but no protoplasting artefacts.
4. Can multiplex with snATAC-seq for chromatin
   accessibility.

Increasingly preferred for plant studies; works
with hard tissues + frozen samples + diverse
species without optimisation.

### Spatial transcriptomics

Preserves location information.

**Spot-based**:
- **10x Visium** — 55-µm spots over a slide;
  ~ 5 K spots per slide; species-agnostic.  Used
  for several plant tissue atlases.
- **Slide-seq + Slide-seqV2** — DNA-barcoded
  beads at higher resolution (~ 10 µm); used in
  Arabidopsis root + shoot.

**Image-based**:
- **MERFISH + smFISH-like** — multi-round
  single-molecule FISH; 100-1 000 genes; sub-cellular
  resolution.  Demanding workflow.
- **ISS (in situ sequencing)** — hundreds of genes
  via padlock probes + rolling-circle amplification.
- **CosMx + Xenium** — commercial multi-gene
  in-situ.
- **Stereo-seq** (BGI) — DNA-nanoball arrays at
  500-nm resolution; used in *Arabidopsis* +
  rice atlases.

### Spatial proteomics + metabolomics

- **MALDI-MSI** — mass-spec imaging at 10-50 µm;
  metabolites + lipids; powerful for natural-
  product distribution mapping.
- **DESI-MSI** — softer ionisation alternative.
- **Imaging mass cytometry** + **multiplexed IF** —
  protein-level spatial analysis; less common in
  plant biology than animal.

## Plant-specific findings

### Root cell-type atlases

*Arabidopsis* root scRNA-seq has resolved:
- Quiescent centre (QC) signatures.
- Cortex / endodermis differentiation trajectory.
- Stele cell-types (xylem precursors → vessel
  elements; phloem precursors).
- Root hair cell trajectory (atrichoblast → trichoblast
  decision).
- Lateral-root primordium initiation.
- Stress-responsive subpopulations.

### Shoot apical meristem dynamics

scRNA-seq + snRNA-seq + spatial work has mapped:
- Stem-cell pool (CLV3-expressing) vs organising
  centre (WUS-expressing) vs peripheral / rib
  zones.
- Leaf-primordium initiation + auxin / cytokinin
  feedback.
- Floral-meristem identity transition (LFY,
  AP1-mediated).
- Position-dependent gene expression patterns.

### Vascular development

- Pre-procambium → procambium → cambium → secondary
  xylem / phloem trajectories now resolved at
  single-cell + spatial resolution.
- Hardwood (vessel-bearing) vs softwood (tracheid-
  only) cambial-cell types being mapped.

### Reproductive cells

- Pollen development — microspore → bi-cellular →
  tri-cellular pollen trajectories.
- Embryo sac formation (megasporogenesis +
  megagametogenesis).
- Fertilisation + early embryogenesis.

### Stress responses + cell-type-specific responses

- Cell-types respond differently to drought / heat /
  pathogen — ABA-responsive genes spike differently
  in mesophyll vs guard cells vs phloem cells.
- Pathogen attack maps differentially across cell
  types (epidermal vs mesophyll vs vascular
  cell responses).

### Plant-microbe interfaces

- Symbiotic interaction at the root-mycorrhiza
  interface mapped at single-cell resolution.
- N-fixing nodules (legume root) — colonising
  rhizobia trigger specific cortical cell-type
  programmes.

### Crop applications

- Maize ear development atlas.
- Rice meiosis + grain-filling single-cell
  programmes.
- Tomato fruit-development cell-type maps (pericarp,
  locule, seed coat).
- Cotton fibre development (single-cell extending
  ovule epidermal cell).

## Multi-modal + integrative approaches

- **scATAC-seq + scRNA-seq** — match transcription +
  chromatin accessibility per cell.
- **CUT&Tag / CUT&RUN** in plants — chromatin
  profiling at single-cell resolution emerging.
- **Multi-omics integration** — Seurat WNN, MOFA+,
  Harmony, Liger.
- **Trajectory + RNA-velocity** — infer
  developmental trajectories from snapshot data
  (scVelo, Cellrank, Monocle3).
- **Cell-cell communication inference** — CellChat,
  NicheNet, NATMI for ligand-receptor signalling.

## Computational tools

Plant single-cell analysis uses generic single-cell
tools + plant-specific resources:
- **Scanpy + Seurat** — backbone analysis frameworks.
- **PlantPhoneDB + PlantSCRNADB** — plant-specific
  databases.
- **PCMDB** — Plant cell marker DB.
- **SpaceMarkers + spatial-deconvolution** for
  Visium-resolution cell-type assignment.
- **Saturn + species-aware integrations** — handle
  cross-species comparisons.

## A future Genetics + Molecular Biology Studio

Single-cell + spatial sequencing techniques will be
covered in technique-level depth in the upcoming
**Genetics + Molecular Biology Studio** sibling.

## Open challenges

- **Stress-induced expression artefacts** in
  protoplasting + nuclei isolation.
- **Reference annotations** lag behind raw data —
  cell-type definitions still being refined.
- **Long-read single-cell** — emerging (PacBio /
  ONT) but limited throughput.
- **Spatial resolution vs throughput** trade-off —
  no single technology covers entire-tissue at
  sub-cellular resolution yet.
- **3D / tissue-level reconstruction** — spatial
  data is mostly 2D sections.
- **Computational cost + reproducibility** — large
  datasets, evolving algorithms, version
  sensitivity.

## Outlook

By 2030, expect:
- Single-cell atlases of every major crop species.
- Routine pre-clinical + clinical-trial plant
  phenotyping at single-cell resolution.
- Integration of spatial + temporal (developmental
  time-course) + multi-omics (transcriptomic +
  epigenomic + proteomic + metabolomic) at
  single-cell scale.
- AI-driven cell-type discovery + annotation.
- Cross-species cell-type comparative analysis
  driving evo-devo insights.

## Try it in the app

- **OrgChem → Tools → Cell components** — plant
  cell-component entries provide the foundational
  cell-type vocabulary.
- **Window → Botany Studio → Plant taxa** — model
  + crop species used in single-cell studies.
- **Window → Cell Biology Studio → Signalling** —
  shared signalling pathways resolved at single-cell
  scale across plant + animal systems.

Next: **Synthetic biology + plant engineering**.
