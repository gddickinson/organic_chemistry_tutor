# Single-cell + spatial omics workflows

The single-cell + spatial-omics revolution has
transformed biology in the late 2010s + 2020s.  This
lesson covers the practical experimental + analytical
workflow for the dominant platforms, plus the
emerging multi-modal + spatial integration layer.

## When to use single-cell

- **Cell-type discovery** in heterogeneous tissue
  (tumour, immune, brain, developing embryo).
- **Trajectory analysis** of differentiation +
  development.
- **Transcriptional response** of specific cell
  types to perturbation (drug, genetic, infection).
- **Rare-cell-population characterisation** (cancer
  stem cells, lymphocyte subsets, neural progenitors).
- **Cell-cell communication** inference (ligand-
  receptor mapping).
- **Reference-atlas building** (HCA, BICCN,
  HuBMAP).

When NOT to use single-cell:
- Bulk + low-cell-type-heterogeneity work where
  bulk RNA-seq is cheaper + more sensitive.
- When tissue-dissociation will damage signal of
  interest (some immune-cell-state changes occur
  during dissociation).

## Choice of platform

| Platform | Read-out | Cells / channel | Notes |
|----------|----------|-----------------|-------|
| 10x Chromium | 3' RNA-seq | 10K-100K | The dominant droplet-based; integrated CITE-seq + ATAC + Multiome |
| BD Rhapsody | 3' RNA-seq | 10K | Cartridge-based; targeted-panel options |
| Parse Bio Evercode | 3' RNA-seq | 10K-1M | Combinatorial barcoding; very large experiments |
| Singleron GEXSCOPE | 3' RNA-seq | 10K | Cost-competitive |
| Smart-seq3 + Smart-seq3xpress | Full-length RNA-seq | 100s-1000s | Higher per-cell detection; lower throughput |
| Plate-based MARS-seq + CEL-Seq2 | 3' RNA-seq | 100s-1000s | Targeted; combinable with FACS sorting |
| 10x Multiome | RNA + ATAC | 10K | Same nucleus, two modalities |
| 10x Visium | Spatial spot-RNA-seq | 5K spots / slide | Original spatial workhorse |
| 10x Xenium | Spatial in-situ | 100s-1000s of genes | Sub-cellular resolution |
| Vizgen MERSCOPE | Spatial in-situ MERFISH | 500-1000 genes | Sub-cellular resolution |
| Nanostring CosMx | Spatial in-situ | 1000+ genes / 64+ proteins | Multi-omic |
| BGI Stereo-seq | Spatial sequencing | 500 nm bins | Highest-resolution sequencing-based |
| Curio Seeker (Slide-seqV2) | Spatial sequencing | ~ 10 µm beads | Whole-transcriptome, single-cell-like |

## Stage 1 — sample preparation

### Single-cell RNA-seq

Two paths:

- **Fresh dissociation** — enzymatic (collagenase /
  papain / trypsin / TrypLE / dispase) + mechanical;
  yields living cells; risks dissociation-induced
  expression changes (immediate-early genes spike).
- **Single-nucleus** — flash-freeze tissue + isolate
  nuclei via Triton / NP-40 / sucrose gradient or
  FACS; preserves frozen samples; lower transcript
  count per nucleus but no dissociation stress.

For brain + cardiac + adipose + muscle + kidney +
plant (cell-wall makes dissociation hard):
**snRNA-seq is increasingly preferred**.

For tumour + immune + cultured cells:
**scRNA-seq still standard**.

### Quality control before encapsulation

- **Cell count** — Countess / Cellometer / TC20.
- **Viability** — > 80 % typical; trypan blue or
  PI exclusion.
- **Aggregate-free** — pass through 35-40 µm strainer.
- **Singlet purity** — FACS sort if available.

## Stage 2 — library prep + sequencing

10x Chromium Single Cell 3' workflow (typical
parameters):
- Loading: ~ 8 000-10 000 cells per channel for
  ~ 5 000-7 000 captured cells (Poisson-driven
  doublet rate ~ 4-5 %).
- GEM (Gel-bead in EMulsion) generation: ~ 7 min on
  a Chromium controller.
- RT + bead release + cDNA amplification:
  overnight.
- Library construction: 1-2 days.
- Sequencing: Illumina; ~ 50 K-100 K reads per cell
  for 3' gene-expression library.

## Stage 3 — primary processing

### Cell Ranger (10x Chromium standard)

```
cellranger count --id=$SAMPLE --transcriptome=$REF
                 --fastqs=$FASTQ_DIR
                 --sample=$SAMPLE_NAME
```

Outputs:
- `filtered_feature_bc_matrix/` — cells × genes count matrix.
- `raw_feature_bc_matrix/` — all barcodes including empty droplets.
- `web_summary.html` — QC report.
- `cloupe.cloupe` — Loupe Browser file.

### Alternative tools

- **alevin-fry** — fast Salmon-based; lower memory.
- **starsolo** — STAR-based.
- **kb-python** (kallisto + bustools) — fast +
  versatile.
- **alevin / pyroe** — Python ecosystem.

Choice often comes down to lab habit; benchmarks
mostly equivalent within ~ 5 %.

## Stage 4 — quality control

### Per-cell QC metrics

- **Total counts (UMIs)** per cell — typically
  1 000-50 000.
- **Number of detected genes** per cell — 500-
  10 000 typical.
- **% mitochondrial** — high (> 10-20 %) often
  flags dying cells; lower thresholds (5 %) for
  healthy mammalian cells; higher for some lineages
  (cardiac, hepatocyte).
- **% ribosomal** — high in some lineages
  (proliferating cells); not necessarily a defect.
- **% hemoglobin** — high in red-blood-cell or
  blood-tissue contamination; can be regressed
  out.

Filter cells outside outlier ranges.

### Doublet detection

- **Scrublet** — kNN-based simulation.
- **DoubletFinder** — similar simulation approach.
- **scds** — multiple methods.
- **Solo (scvi-tools)** — VAE-based.

Typical doublet rate: 1-10 % depending on
loading.

### Ambient-RNA correction

- **SoupX** — corrects for ambient RNA contamination
  in droplet-based scRNA-seq.
- **DecontX** — Bayesian alternative.
- **CellBender** — neural-network-based denoising.

Critical for tumour + tissue samples with high
extracellular RNA.

## Stage 5 — analysis

### Normalization + transformation

- **CPM / TP10K + log1p** — standard early.
- **SCTransform** (Seurat) — variance-stabilising
  regression with negative binomial.
- **scran deconvolution** + **size factors**.
- **scVI / scANVI** — VAE-based normalization +
  integration.

### Dimensionality reduction

- **PCA** — first 30-50 PCs typical.
- **Harmony** + **scVI / scANVI** — batch-aware
  integration.
- **UMAP** — visualization.
- **t-SNE** — older alternative; supplanted by
  UMAP.
- **PHATE** — preserves trajectory structure.

### Clustering

- **Leiden** (modularity-based; preferred over
  Louvain for stability).
- Multi-resolution (test resolution 0.2-2.0).
- Marker-gene-based annotation per cluster.

### Cell-type annotation

- **Manual marker-gene** — domain expertise; the
  gold standard.
- **Reference-based**:
  - **scmap + scPred** — older but robust.
  - **SingleR** — annotation against bulk references.
  - **scArches** + **scANVI** — transfer learning.
  - **Azimuth** — Seurat-curated PBMC + lung +
    bone marrow + heart + tonsil + kidney atlases.
  - **CellTypist** — ML-based pan-tissue classifier.

### Trajectory + pseudotime

- **Monocle3** — graph-based trajectory.
- **PAGA** + **Scanpy** — partition-based graph
  abstraction.
- **scVelo + scFates** — RNA velocity-based
  trajectories (using spliced + unspliced read
  ratios from velocyto / kb-python output).
- **CellRank** — combines RNA velocity + trajectory
  inference.

### Differential expression

- **wilcoxauc** + **Seurat::FindMarkers** + **scanpy
  rank_genes_groups** for cluster markers.
- **MAST** (zero-inflated lognormal) for
  cell-state DE.
- **Pseudobulk DE** (DESeq2 / edgeR on aggregated
  cell-type counts) — increasingly preferred for
  comparing conditions across cell types.
- **muscat** + **dreamlet** — pseudobulk DE
  workflows.

### Cell-cell communication

- **CellChat** — most popular.
- **NicheNet** — ligand-target signalling
  inference.
- **NATMI** + **CellPhoneDB** + **LIANA** —
  alternatives + meta-analysis.

## Spatial-transcriptomics workflows

### Visium workflow

1. Place tissue cryosection on slide.
2. Permeabilise.
3. mRNA captures on barcoded poly-T spots.
4. Reverse transcription.
5. Library + sequencing.
6. Space Ranger preprocessing → spot × gene
   matrix + tissue image.
7. Analysis with **Seurat** (SpatialFeaturePlot),
   **Scanpy + Squidpy**, or **STUtility**.

Key analyses:
- **Spatially-variable genes** — moranI / SPARK /
  trendsceek / SpatialDE.
- **Cell-type deconvolution per spot** — RCTD,
  SpaceXR, cell2location, stereoscope, CellDART
  (Visium spots ~ 5-10 cells; need deconvolution).
- **Niche analysis** — proximity-based clustering.
- **Tissue domains** — BANKSY, GraphST, STAGATE.

### Xenium / MERSCOPE / CosMx workflow

1. Prepare tissue sections (FFPE or fresh-frozen).
2. Probe panel design (target 100-1000 genes).
3. Multi-round imaging on instrument.
4. On-instrument decoding → cell × gene matrix
   with spatial coordinates.
5. Analysis with **Squidpy**, **Spatial Seurat**,
   commercial Xenium Explorer / CosMx Analysis
   Suite.

### Slide-seqV2 / Curio Seeker

Whole-transcriptome at ~ 10 µm bead resolution; cell-
type deconvolution + spatial-pattern analysis as for
Visium.

### Stereo-seq

500-nm-bin spatial sequencing; near-cellular but
true spatial; major effort by BGI; analysis via
**spateo** + **Stereopy**.

## Multi-modal integration

### Within-cell multi-modal

- **CITE-seq** — antibody-derived tags (ADT) → RNA
  + cell-surface protein per cell.
- **TEA-seq + ASAP-seq + DOGMA-seq** — RNA + ATAC
  + protein triple-mode.
- **10x Multiome** — RNA + ATAC.
- **Multi-CUT&Tag + sci-CUT&Tag-pro** — multi-
  histone-mark profiling per cell.
- **Patch-seq** — patch-clamp + scRNA-seq from
  single neurons.

### Cross-modal integration

- **WNN (Weighted Nearest Neighbors, Seurat)** —
  multi-modal joint embedding.
- **MOFA+ + MOFA2** — Bayesian multi-omic factor
  analysis.
- **scVI / totalVI / Multi-VI** — VAE-based.
- **Glue / scGen** — integration with reference
  atlases.

### Spatial + scRNA-seq integration

- Use scRNA-seq as reference for spatial cell-type
  deconvolution.
- Tools: **Tangram + Cell2location + RCTD + SpaCET +
  destVI**.

### Spatial + multi-omic

- **DBiT-seq** — spatial multi-omic.
- **Stereo-seq + spatial proteomics**.
- **Spatial CITE-seq + ASAP-seq variants**.
- Active research area.

## Reference atlases

- **Human Cell Atlas** — pan-organ; > 100
  contributing labs.
- **Allen Brain Cell Atlas** — comprehensive
  mouse + human brain.
- **HuBMAP** — multi-omic spatial human atlas.
- **Tabula Sapiens / Tabula Muris / Tabula
  Microcebus** — pan-tissue atlases.
- **CZ CELLxGENE** — Chan-Zuckerberg-curated;
  > 70 M cells deposited as of 2026.
- **Human Lung + Heart + Kidney + Liver + Gut
  + Skin + Tonsil cell atlases** — published
  individual organ references.

## Practical pipeline stack (2026)

A typical workflow:
- **Cell Ranger / kb-python / alevin-fry** — primary processing.
- **Scanpy (Python)** OR **Seurat (R)** — analysis backbone.
- **scVI / scANVI / Harmony** — integration.
- **CellTypist / Azimuth** — annotation.
- **Squidpy + spateo + Giotto** — spatial analysis.
- **CellChat / LIANA / NicheNet** — cell-cell
  communication.
- **scvi-tools + scArches** — large-atlas integration.
- **CZ CELLxGENE Discover** — atlas data discovery.

Cloud: AnnData + Zarr + LaminDB + cellxgene-census
APIs.

## Single-cell challenges (still)

- **Sparsity** — 1-10 K transcripts / cell vs
  ~ 20 K genes → most entries are zero.
- **Doublets** — never zero; filter aggressively.
- **Dissociation artefacts** — IEG + heat-shock
  bias toward dissociation method.
- **Batch effects** — between channels + days +
  sites + chemistries; need integration.
- **Cell-type definition** — clustering choices
  influence "discoveries" of cell types.
- **Compositional analysis** — % cell types is a
  ratio (not independent counts) → need
  compositional-aware DA tools (scCODA, sccomp,
  propeller).

## Cross-link

The GM-1.0 catalogue's `scrna-seq`, `snrna-seq`,
`visium-spatial`, `slide-seq`, `smfish-merfish`, +
`atac-seq` entries provide the technology-card
context.  See also **CB-3.0 graduate "Quantitative
signalling"** + **BT-3.0 graduate "Plant single-
cell + spatial transcriptomics"** for context-
specific applications.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques** — single-cell + spatial entries.
- **Window → Animal Biology Studio → Animal taxa** —
  model organisms used in atlas-scale projects.

This concludes the GM-3.0 advanced tier.  Next:
**Population genetics + ancient DNA** (graduate).
