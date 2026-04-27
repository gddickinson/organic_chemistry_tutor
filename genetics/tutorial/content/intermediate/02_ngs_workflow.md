# NGS workflow + bioinformatics

The NGS pipeline turns raw sequencing data into
biological + clinical insight.  This lesson walks
through the canonical short-read workflow + introduces
the major tools, decision points, and quality gates
at each stage.

## Stage 1 — sample + library

### Input requirements

- **Genomic DNA** — 1 ng-1 µg (depends on protocol).
- **RNA** — 100 ng-5 µg total RNA; integrity
  matters (RIN > 7 ideal; Bioanalyzer / TapeStation
  / Fragment Analyzer).
- **FFPE** — degraded; use FFPE-tolerant kits
  (Twist, Roche, KAPA HyperPlus); expect lower
  library complexity.
- **cfDNA** — typically 2-8 ng / mL plasma; use
  Streck cfDNA tubes + low-input library prep.

### Library-prep paths

- **PCR-based amplicon panels** (AmpliSeq,
  multiplex PCR + sequencing) — small, targeted.
- **Hybrid capture** (Twist, IDT xGen, Agilent
  SureSelect, Roche KAPA HyperCap) — exome / panel
  / WGS-add-on.
- **Whole-genome shotgun** — fragmentation +
  end-repair + A-tailing + adaptor ligation +
  PCR-free or low-cycle PCR.
- **PCR-free** — preferred for variant calling
  + GC-balanced coverage; needs ≥ 100 ng input.
- **Tagmentation-based** (Nextera) — Tn5 fragments +
  adapts in one step; lower input but higher
  duplication.

### Quality control before sequencing

- **Bioanalyzer / TapeStation** — fragment-size
  distribution; library size 200-800 bp typical.
- **Qubit / Picogreen** — dsDNA concentration.
- **qPCR (KAPA library quantification)** —
  flowcell-loadable library quantification (gold
  standard).
- **Real-time qPCR molarity** + size → effective
  concentration for cluster generation.

## Stage 2 — sequencing

Covered in detail in the GM-1.0 Techniques tab
(`illumina-short-read`, `pacbio-hifi`, `ont-nanopore`).
Key short-read parameters:

- **Read length** — 75 bp (legacy / cheap) → 150
  bp (workhorse) → 250-300 bp (long-amplicon /
  16S).
- **Single-end vs paired-end** — paired
  significantly improves alignment + variant
  calling; standard for most applications.
- **Coverage** — 30× WGS standard for germline; 60-
  100× somatic; 100-200× clinical exome; 500-1000×
  ctDNA.
- **Index hopping** (patterned flowcells) — use
  unique dual indexes (UDI) to mitigate.

## Stage 3 — primary processing

### Quality control

- **FastQC** — per-file metrics (per-base quality,
  per-base GC, adapter content, sequence
  duplication, overrepresented sequences).
- **MultiQC** — aggregates QC across multiple
  samples + tools into one HTML report.
- **NanoPlot + NanoStat** — long-read QC.

### Adapter + quality trimming

- **fastp** — fast all-in-one (trim + filter + QC).
- **Trimmomatic** — older standard; still common.
- **cutadapt** — targeted adapter removal.
- **bbduk** — BBTools.

Trim adaptors + low-quality 3' bases (Q < 20) before
alignment.  Discard reads < 30 bp post-trim.

### Optional UMI processing

- For ctDNA + low-input + duplex sequencing: PCR
  duplicates are deduplicated by UMI (Unique
  Molecular Identifier) tags rather than start
  position alone.
- Tools: fgbio (fulcrumgenomics), umi-tools, Picard
  MarkDuplicatesWithUMIs.

## Stage 4 — alignment

### Choice of aligner

- **BWA-MEM / BWA-MEM2** — the workhorse for short-
  read DNA alignment; gapped alignment to a single
  linear reference.
- **Bowtie2** — older but reliable; sometimes used
  for ChIP-seq + ATAC-seq.
- **STAR** — splice-aware; standard for bulk RNA-seq.
- **HISAT2** — splice-aware; smaller index +
  multi-genome graphs.
- **Minimap2** — long-read (PacBio + ONT) +
  splice-aware (-ax splice).
- **Salmon / Kallisto** — pseudo-alignment; very
  fast for transcript quantification (no full
  alignment).

### Reference genome choice

- Match your reference to the data:
  - **GRCh38** + **decoy + alt** — current human
    standard.
  - **T2T-CHM13** — increasingly used for
    structural-variant analysis + repetitive-region
    mapping.
  - **HPRC pangenome** — GRAFimo, vg, Giraffe for
    pangenome alignment.

### Post-alignment processing

```
samtools sort  →  Picard MarkDuplicates  →
GATK BQSR (legacy)  →  Picard CollectMetrics
```

- **Sort** — BAM by coordinate.
- **MarkDuplicates** — flag PCR + optical
  duplicates (~ 5-15 % typical for PCR-free; 20-
  40 % for amplicon).
- **BQSR (Base Quality Score Recalibration)** —
  GATK; corrects systematic Q-score biases.
  Optional in newer pipelines (DeepVariant doesn't
  benefit).
- **Coverage metrics** — Picard
  CollectWgsMetrics + CollectHsMetrics + Mosdepth.

## Stage 5 — variant calling

### SNV + indel callers

- **GATK HaplotypeCaller** — long-standing reference
  standard (germline + somatic via Mutect2).
- **DeepVariant** (Google) — CNN-based; often
  outperforms HaplotypeCaller at SNV + small indel
  precision.
- **Strelka2** (Illumina) — both germline + somatic;
  fast + accurate.
- **Octopus** — flexible Bayesian framework; growing.
- **NVIDIA Parabricks** + **Sentieon** — accelerated
  GPU implementations; same algorithms, ~ 30-100×
  faster.

### Joint vs single-sample calling

- **gVCF + joint genotyping** (GATK GVCF workflow)
  — recommended for cohorts; allows incremental
  re-genotyping as samples are added.
- **Single-sample** — for one-off clinical cases.

### Filtering

- **VQSR** (GATK Variant Quality Score
  Recalibration) — for large cohorts.
- **Hard filters** (gnomAD-style or ExAC-style
  thresholds) — for smaller cohorts where VQSR
  doesn't have enough variants to train.
- **gnomAD allele frequency** — filter common
  variants (MAF > 0.01) for rare-disease
  workups.

### Structural variants

- **Manta** + **Delly** + **Lumpy** + **GRIDSS** —
  short-read SV callers; complementary; ensemble
  improves performance.
- **Sniffles** + **cuteSV** + **dysgu** + **SVision**
  — long-read SV; significantly better than
  short-read for many SV classes.
- **Pangenome-graph methods** (vg, GraphTyper) —
  improving rapidly.

### Copy-number variants

- **CNVkit** + **Control-FREEC** + **PureCN** for
  short-read panels + WES + WGS.
- **GATK gCNV** for WES.
- **Manta + dCNV from long-read** for
  high-resolution CNV.

### Somatic / tumour-only

- **Mutect2** + **Strelka2 somatic** + **VarScan2
  somatic** — tumour-normal pairs.
- **Tumor-only** — harder; requires PoN + gnomAD
  for filtering.
- **TMB calculation** — tumour mutational burden
  (mutations / Mb of coding sequence) — predicts
  immune-checkpoint-inhibitor response.

## Stage 6 — annotation + interpretation

### Functional annotation

- **VEP (Ensembl Variant Effect Predictor)** — most
  popular open-source; fast + comprehensive.
- **SnpEff** — older; good for non-human + bacterial
  genomes.
- **ANNOVAR** — Asian + Indian population
  databases; commercial.

### Population databases

- **gnomAD** v4.x — > 800 K exomes + > 75 K WGS;
  the de-facto standard.
- **TOPMed BRAVO** — 132 K diverse cohort.
- **UK Biobank** — > 500 K WGS released 2023.

### Clinical databases

- **ClinVar** — clinical variant assertions
  (NCBI).
- **OMIM** — Mendelian disease catalogue.
- **HGMD (paid)** — Human Gene Mutation
  Database.
- **DECIPHER** — paediatric variants + phenotypes.
- **PanelApp** — Genomics England gene panels with
  evidence levels.

### Cancer-specific

- **COSMIC** — somatic mutations.
- **OncoKB** — therapeutic levels of evidence.
- **CIViC** — community-curated cancer-variant
  interpretation.
- **TCGA / GDC** — primary cancer-genomics data.

### Variant prioritisation

For Mendelian rare disease:
- Filter by gnomAD frequency (MAF cutoffs).
- Restrict to coding + splice variants.
- Apply ACMG/AMP classification (path / likely-path
  / VUS / likely-benign / benign).
- Use Exomiser / GADO / LIRICAL for phenotype-driven
  ranking (HPO terms).

For somatic cancer:
- Filter germline + benign.
- Prioritise oncogenic drivers per OncoKB / CIViC.
- Annotate actionable variants per FDA-approved +
  off-label evidence.

## Stage 7 — reporting + storage

### Variant reports

- **MAF / MAF-like** — TCGA-style mutation tables.
- **VCF + tabular outputs** — for downstream
  analysis.
- **PDF clinical reports** — variant + phenotype
  + actionable findings + literature; templating
  via Jinja / Knitr / Quarto.

### Data lifecycle

- Raw FASTQ archived (cold storage; AWS Glacier /
  Tape).
- BAM + VCF live for active analysis (warm
  storage).
- Aggregated cohorts in cloud data warehouses
  (BigQuery / Snowflake / Hail).

## Workflow management

### Workflow languages

- **Nextflow** — Groovy DSL; the most popular
  bioinformatics workflow engine in 2026; nf-core
  ecosystem provides 100+ curated pipelines.
- **Snakemake** — Python; especially popular in
  academic + smaller-scale labs.
- **WDL** — Broad Institute; runs on Cromwell +
  Terra + DNAnexus.
- **CWL** — Common Workflow Language; cross-
  platform open standard.

### Reference pipelines

- **nf-core / sarek** — germline + somatic variant
  calling.
- **nf-core / rnaseq** — bulk transcriptomics.
- **nf-core / scrnaseq** — single-cell.
- **GATK Best Practices** — Broad's reference
  workflows.
- **Sentieon / Parabricks** — accelerated commercial
  pipelines.

## Cloud platforms

- **Terra (Broad / Microsoft)** — WDL + Cromwell;
  AWS + GCP + Azure.
- **DNAnexus** — clinical-grade compliance;
  AWS-based.
- **Seven Bridges (Velsera)** — multi-cloud.
- **AWS HealthOmics** — AWS-native managed service.
- **Azure Genomics** — Azure-native.

## Reproducibility

- Containerise (Docker / Singularity / Apptainer).
- Pin tool versions + reference-genome versions.
- Use workflow-language version control + CI.
- Document parameter choices + rationale.
- Adhere to FAIR principles (Findable, Accessible,
  Interoperable, Reusable).

## What goes wrong + how to detect it

| Issue | Symptom | Detection |
|-------|---------|-----------|
| Index hopping | Sample cross-contamination | Unique dual indexes; barcode-rate auditing |
| GC bias | Coverage troughs at GC extremes | Picard CollectGcBiasMetrics |
| Adapter retention | Spurious soft-clipping | FastQC adapter content; trimming verification |
| Allelic dropout | Het call missed | Coverage analysis; balanced reads-per-allele |
| Reference bias | Variants undercalled at unique loci | Long-read or pangenome alignment validation |
| Duplicates | Inflated coverage; PCR artefacts | Picard MarkDuplicates + low-input UMI workflow |
| Contamination | Spurious variants | VerifyBamID + somatic-vs-germline AF analysis |

## Cross-link

The GM-1.0 catalogue's `illumina-short-read`,
`pacbio-hifi`, `ont-nanopore`, `bulk-rna-seq`,
`scrna-seq`, `snrna-seq`, `chip-seq`, `atac-seq`, +
`hi-c` entries provide technology context.  This
lesson is the workflow + tooling layer.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques** — review NGS-related entries.
- **OrgChem → Tools → Lab analysers** — Illumina +
  PacBio + ONT instruments.

Next: **CRISPR experimental design**.
