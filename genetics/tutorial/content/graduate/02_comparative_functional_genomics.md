# Comparative + functional genomics

Comparative genomics asks how genomes evolve across
species; functional genomics asks what each genomic
element does.  The two fields complement each other +
together drive most of modern molecular biology.

## Comparative genomics — methods

### Whole-genome alignment

- **Pairwise** — LASTZ, minimap2, AnchorWave.
- **Multiple-genome** — progressiveCactus (active
  research community).
- **Pangenome alignment** — minigraph, vg, Giraffe.

Output: chains + nets + MAF files; visualised in
genome browsers (UCSC + Ensembl + JBrowse).

### Synteny + orthology

- **Synteny** — conserved gene order across species.
- **Orthologs** — homologous genes diverged by
  speciation.
- **Paralogs** — homologous genes diverged by
  duplication.
- Tools: OrthoFinder, OrthoDB, Compara, OMA, Roary
  (microbial pan-genome).

### Substitution rates

- **dN / dS** — non-synonymous : synonymous;
  measures selection at protein level.
- **dN / dS < 1** — purifying selection (most
  conserved genes).
- **dN / dS > 1** — positive selection (rare).
- **Synonymous-rate (dS) variation** — clock
  variation; codon usage; recombination effects.

### Branch + site models

- **PAML** — codeml branch / site / branch-site
  models for adaptive evolution detection.
- **HyPhy + DataMonkey** — hypothesis-driven
  selection tests.
- **BUSTED + RELAX + aBSREL** — common modern
  models.

### Phylogenetic comparative methods (PCMs)

- Test trait-trait correlations accounting for
  shared ancestry.
- **Felsenstein's independent contrasts**.
- **Phylogenetic generalised least squares (PGLS)**.
- **Brownian motion + Ornstein-Uhlenbeck** models
  for trait evolution.

## Conserved non-coding elements (CNEs)

- Identifiable by deep evolutionary conservation
  + lack of coding-sequence features.
- Most are enhancers; some are insulators or
  ncRNAs.
- ~ 100 K - 500 K CNEs in vertebrates.
- Useful for prioritising regulatory variants in
  WGS analysis.

## Ultra-conserved elements (UCEs)

- 200+ bp regions of perfect identity across
  vertebrates.
- ~ 480 UCEs in vertebrate genomes.
- Surprisingly, many are dispensable (knockouts
  viable in mouse).
- Active research area into their function.

## Pan-genomes

The realisation that a single reference is
insufficient:
- **Core genome** — present in all individuals /
  strains.
- **Accessory genome** — present in some.
- **Singletons** — strain / individual-specific.

For bacteria:
- Many species have core / accessory ratios of
  ~ 30/70.
- **Open** vs **closed** pan-genomes (open keeps
  expanding with new strain sequencing).

For humans:
- HPRC pangenome captures ~ 100 Mb additional
  sequence beyond GRCh38.
- Improves variant calling + structural-variant
  detection in diverse populations.

## Functional genomics — methods

### Transcriptome profiling

- **Bulk RNA-seq** — gene + isoform expression
  across tissues / conditions.
- **scRNA-seq + snRNA-seq** — cell-type-specific.
- **Ribo-seq** — translation snapshot.
- **GRO-seq + PRO-seq + NET-seq** — nascent
  transcription.
- **Direct-RNA-seq** (ONT) — full-length + native
  modifications.

### Chromatin profiling

- **DNase-seq + ATAC-seq** — open chromatin.
- **MNase-seq** — nucleosome positioning.
- **ChIP-seq + CUT&RUN + CUT&Tag** — TF + histone-
  mark binding.
- **Hi-C + Micro-C** — 3D chromatin architecture.
- **Capture Hi-C + 4C-seq** — locus-specific 3D.

### Epigenomic profiling

- **WGBS + RRBS + EM-seq** — DNA methylation.
- **TAB-seq + oxBS-seq** — 5hmC vs 5mC.
- **Methylation EPIC array** — cost-effective CpG
  profiling.

### Cis-regulatory mapping

- **STARR-seq + MPRA** — massively parallel reporter
  assays for enhancer activity.
- **CRISPRi screens** at enhancers.
- **CROP-seq + Perturb-seq** — combines CRISPR
  perturbation + scRNA-seq readout.
- **Saturation mutagenesis** + DMS — variant-effect
  measurement at single-base resolution.

### Protein-DNA + protein-protein

- ChIP-seq + CUT&RUN + Y2H + AP-MS + BioID
  (covered in GM-1.0 catalogue).

## Major reference projects

### ENCODE

The Encyclopedia of DNA Elements:
- Phase 1 (2003-2007) — pilot.
- Phase 2 (2007-2012) — major expansion.
- Phase 3 (2017-2020) — single-cell + 4D.
- Phase 4 (2021-) — ENCODE 4 + cCRE catalogue.
- Outputs: DNase + ATAC + ChIP-seq + RNA-seq across
  hundreds of cell types + tissues.

### Roadmap Epigenomics

Sister project; reference epigenomic profiles for
> 100 human cell types.

### IHEC

International Human Epigenome Consortium —
international coordination of epigenome reference
data.

### GTEx

Genotype-Tissue Expression — tissue-specific
expression + eQTLs across > 50 human tissues.

### FANTOM

Functional Annotation of the Mammalian Genome —
CAGE-based promoter + enhancer atlas.

### 4D Nucleome

Spatial + temporal organisation of the genome.

### Single-cell atlases

- HCA (Human Cell Atlas).
- BICCN (BRAIN Initiative Cell Census Network).
- HuBMAP.
- LungMAP, KidneyMAP, GUTMAP, etc.

## Variant prioritisation

For non-coding variants, integrate:
- Conservation (phyloP, phastCons).
- Chromatin state (chromHMM, ChromImpute).
- Open chromatin (DNase / ATAC).
- TF-binding-site prediction (motif + ChIP-seq).
- 3D contacts (Hi-C).
- eQTL effects (GTEx).
- Direct functional assays (MPRA, CRISPRi).

Tools:
- **CADD + REVEL + PrimateAI** — coding-region
  variant prediction.
- **AlphaMissense** (DeepMind 2023) — missense-
  pathogenicity prediction at scale.
- **SpliceAI + Pangolin** — splice-disrupting
  variants.
- **ENCODE-rE2G** — enhancer-gene linking.
- **Enformer + Borzoi + Aleph** (DeepMind +
  others) — sequence-to-function transformers
  for regulatory predictions.

## Variant-to-function (V2F)

A central challenge: GWAS / WGS identifies variant
+ disease association, but most associated variants
are non-coding + with unclear function.

Approach:
1. **Fine-mapping** — pin down likely causal
   variant within an LD block.
2. **Functional annotation** — chromatin state +
   eQTL + epigenome + Hi-C contacts.
3. **Prioritise candidate gene** — closest gene +
   eQTL effects + Hi-C target + functional
   evidence.
4. **Functional validation** — CRISPRi + MPRA +
   reporter assays + animal models.

A growing literature + tooling around V2F.

## Functional + comparative-genomic insights

### Lineage-specific innovations

- **Vertebrate** — adaptive immunity (RAG / MHC /
  Ig); neural crest; jaw evolution.
- **Mammalian** — placentation (syncytin from
  ERV); milk + lactation (caseins); endothermy.
- **Primate** — colour vision (opsin
  duplication); cognition-related accelerated
  regions (HARs, HACNS1).
- **Human** — vocal learning (FOXP2 evolution);
  speech-related cortical regulatory changes.

### Gene loss

- Cetaceans lost olfactory receptors + many taste
  receptors adapting to aquatic life.
- Snakes lost limb-development regulatory elements.
- Cave fish lost vision + pigmentation pathway
  genes.
- Dietary specialists lose digestive enzymes
  (giant panda lost umami taste receptor TAS1R1).

### Convergent evolution

- **Echolocation** (bats + cetaceans) — Prestin +
  KCNQ4 + Tmc1 amino-acid convergence.
- **Cold tolerance** (Antarctic icefish + Arctic
  cod) — antifreeze glycoprotein convergence.
- **Hypoxia tolerance** (high-altitude humans +
  bar-headed goose) — hemoglobin convergence.

### Intra-species variation

- 1KGP + gnomAD + UK Biobank reveal:
  - ~ 4-5 M variants per individual genome (vs
    GRCh38).
  - ~ 12 K loss-of-function variants per individual.
  - ~ 200-300 deletions + ~ 30-40 duplications per
    individual.
  - Ancestry differences + private variants.

## Methods + software

- **Cactus + ProgressiveCactus** — multi-genome
  alignment.
- **OrthoFinder, OrthoDB, OMA, Compara** —
  orthology.
- **PAML, HyPhy, Datamonkey** — selection inference.
- **MAFFT + MUSCLE5** — multiple sequence alignment.
- **IQ-TREE 2 + RAxML-NG + BEAST 2** — phylogeny.
- **TreeViewer + iTOL + ggtree** — tree
  visualisation.
- **chromHMM + ChromImpute** — chromatin states.
- **Enformer + Basenji** — sequence-to-function ML.
- **scvi-tools + scArches + Tangram + cell2location**
  — single-cell + spatial integration.
- **deepTools + samtools + bedtools** — workhorses.

## What comparative + functional genomics tells us

- Most genome change is REGULATORY, not protein-
  coding.
- Most functional sequence is conserved across
  species at low to moderate stringency.
- Pan-genomes capture diversity invisible to single-
  reference analyses.
- Functional-genomic atlases enable variant
  interpretation in disease + agriculture +
  evolution.
- Increasingly ML-mediated predictions can fill
  gaps in experimental annotation.

## Cross-link

The GM-1.0 catalogue's `chip-seq`, `cut-and-run`,
`atac-seq`, `bulk-rna-seq`, `scrna-seq`, `bisulfite-
seq`, + `hi-c` entries provide the technologies
underlying functional genomics.  See also **AB-3.0
graduate "Comparative genomics + animal evolution"**
+ **CB-3.0 graduate "Quantitative signalling"**.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques → chromatin + transcriptomics** —
  every functional-genomics technology.
- **Window → Animal Biology Studio → Animal taxa** —
  diverse model species for comparative genomics.

Next: **AI for genomics**.
