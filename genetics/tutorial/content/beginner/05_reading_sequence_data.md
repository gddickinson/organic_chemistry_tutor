# Reading sequence data

Modern molecular biology generates terabytes of
sequence data daily.  Knowing how to read + work with
the standard file formats is the entry point to
practical bioinformatics.

## The major formats

### FASTA — sequences only

Simplest format.  Each entry is a single-line header
starting with ``>`` followed by sequence (any number
of lines):

```
>chr1
NNNNNNTACGTAACGTAACGTAACGTACGT
ACGTAACGTAACGTAACGTAACGTAACGTA
>chr2
ACGTACGTACGTACGT...
```

Used for:
- Reference genomes (UCSC + Ensembl + GENCODE).
- Transcript sequences.
- Protein sequences (with single-letter amino-acid
  codes).
- Custom test sequences.

### FASTQ — reads + quality

NGS instrument output.  Four lines per read:

```
@read_id
ACGTACGTACGT
+
IIIIIIIIIIII
```

- Line 1: ``@`` + identifier + optional comment.
- Line 2: sequence.
- Line 3: ``+`` (separator).
- Line 4: per-base quality scores (Phred-encoded
  ASCII; Q33 offset means ``!`` = Q0, ``I`` = Q40).

Quality scores indicate base-call confidence:
- Q10 = 1 / 10 error rate.
- Q20 = 1 / 100 (the "trim threshold").
- Q30 = 1 / 1 000 (the "high-quality threshold").
- Q40 = 1 / 10 000 (PacBio HiFi + late-cycle Illumina
  reach this).

FASTQ files are usually gzip-compressed (``.fastq.gz``);
illumina convention names paired-end reads ``_R1`` /
``_R2``.

### SAM / BAM / CRAM — aligned reads

After mapping reads to a reference:

- **SAM** (Sequence Alignment / Map) — text format;
  one alignment per line; columns include read name,
  flags, reference, position, MAPQ, CIGAR,
  sequence, quality, and tags.
- **BAM** — binary compressed SAM (typical
  intermediate file).
- **CRAM** — reference-based compression; ~ 30-50 %
  smaller than BAM.

Crucial flags:
- 0x4 = unmapped.
- 0x10 = reverse strand.
- 0x40 = first in pair.
- 0x80 = second in pair.
- 0x100 = secondary alignment.
- 0x400 = PCR / optical duplicate.

CIGAR string encodes the alignment operations:
- ``M`` — match / mismatch.
- ``=`` — exact match (newer).
- ``X`` — mismatch (newer).
- ``I`` — insertion.
- ``D`` — deletion.
- ``S`` — soft clip (sequence kept but unaligned).
- ``H`` — hard clip.
- ``N`` — skipped region (RNA-seq splicing).
- ``P`` — padding.

Tools: ``samtools`` (the standard CLI), pysam
(Python bindings), htslib (the underlying C library).

### VCF — variants

Variant Call Format; the standard for SNVs + indels +
SVs:

```
##fileformat=VCFv4.2
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total depth">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT SAMPLE1
chr1 12345 . A G 100 PASS DP=50 GT:DP 0/1:25
```

Genotype codes:
- ``0/0`` — homozygous reference.
- ``0/1`` (or ``0|1`` phased) — heterozygous.
- ``1/1`` — homozygous alternate.
- ``./. `` — no call.

VCF + BCF (binary) widely supported.  Tools: ``bcftools``,
``vcftools``, ``rtg-tools``, ``hail``, ``pysam``.

### GFF / GTF — annotations

Tab-separated annotations of genes, transcripts, exons,
CDSs, UTRs:

```
chr1 ENSEMBL gene 11869 14409 . + . ID=ENSG00000223972;gene_name=DDX11L1
chr1 ENSEMBL transcript 11869 14409 . + . Parent=ENSG00000223972
chr1 ENSEMBL exon 11869 12227 . + . Parent=ENST00000456328
```

GFF3 + GTF differ subtly in attribute syntax; most
tools accept both.

### BED — regions

Simpler than GFF; 3 + optional columns:

```
chr1 100 200 region1 0 +
chr1 500 600 region2 0 -
```

Columns: chrom + start (0-based) + end (1-based) +
optional name + score + strand + thickStart + thickEnd
+ rgb + blockCount + blockSizes + blockStarts.

Used for: ChIP-seq peaks, ATAC-seq peaks, exome
capture targets, annotation tracks.

### BedGraph + bigWig + bigBed

- **BedGraph** — text; chrom + start + end + value
  (signal track).
- **bigWig** — indexed binary version; faster random
  access; standard for genome-browser tracks.
- **bigBed** — indexed binary BED.

Tools: ``bedtools``, ``bigWigToBedGraph``,
``deepTools``, ``UCSC tools``.

### Other essentials

- **GFA** — genome graphs (pangenomes); used by
  minigraph + pangenome-graph projects.
- **MAF** — multi-species alignment.
- **HDF5 / Zarr** — single-cell + spatial
  transcriptomic / proteomic data containers (10x,
  Scanpy, Seurat .h5ad / .h5seurat).
- **Mzml + mgf** — mass-spectrometry data.
- **PDB / mmCIF** — protein structures.

## Coordinates — 0-based vs 1-based

A subtle but clinically-painful distinction:
- **0-based, half-open** ([start, end)) — UCSC, BED,
  pysam, htslib, bcftools.
- **1-based, fully closed** ([start, end]) — VCF,
  GFF, SAM, samtools text view, Ensembl.

Mismatch between formats is a common source of bugs.
Always sanity-check coordinate systems when crossing
file types.

## Reference genome assemblies

For human:
- **GRCh37 / hg19** — released 2009; still in
  clinical use because much legacy data + many
  databases.
- **GRCh38 / hg38** — released 2013; current
  reference for most new work.
- **T2T-CHM13** — first complete telomere-to-
  telomere human reference (2022); resolves repeats
  + centromeres + Y chromosome.
- **HPRC pangenome** — multiple haplotype-resolved
  assemblies released 2023+; capturing structural-
  variant + ancestral diversity.

Cross-build coordinate translation: use ``CrossMap``,
``LiftOver``, or ``picard LiftoverVcf``.

## Common pipelines in 5 stages

A canonical short-read variant-calling pipeline:

1. **QC** — FastQC + MultiQC + trimming (fastp,
   trimmomatic).
2. **Alignment** — BWA-MEM or BWA-MEM2 (bwa-mem 1
   has been benchmark since 2013); for transcripts:
   STAR + HISAT2 + Salmon / Kallisto for
   pseudo-alignment.
3. **Post-processing** — Sort + dedup (samtools +
   Picard MarkDuplicates); BQSR (GATK).
4. **Variant calling** — GATK HaplotypeCaller +
   DeepVariant + Strelka2 + VarScan + bcftools
   mpileup; structural variants: Manta + Delly +
   Lumpy + dysgu.
5. **Annotation + interpretation** — VEP + SnpEff +
   Annovar; clinical annotation: ClinVar + gnomAD +
   COSMIC + OncoKB.

A full long-read pipeline differs (minimap2 +
Clair3 + Sniffles + cuteSV).

## Public databases

- **NCBI** — GenBank, RefSeq, dbSNP, ClinVar, GEO,
  SRA, PubMed.
- **EMBL-EBI** — Ensembl, UniProt, ChEMBL, OpenTargets,
  BioStudies, EuropePMC.
- **UCSC** — genome browser, table browser.
- **gnomAD** — population allele frequencies.
- **TCGA / GDC** — cancer genomics data (NCI's
  legacy + current portals).
- **HCA** — Human Cell Atlas (single-cell).
- **GTEx** — tissue-specific expression + eQTLs.
- **ENCODE** — regulatory annotations.
- **PDB** — protein structures.
- **AlphaFold DB** — predicted structures.

## Cloud + workflow infrastructure

Pipelines are increasingly cloud-native:
- **Workflow languages**: WDL, Nextflow, Snakemake,
  CWL.
- **Cloud platforms**: AWS, GCP, Azure; Terra,
  DNAnexus, Seven Bridges, Cromwell.
- **Reproducibility**: Singularity / Docker
  containers + GitHub Actions / CI.
- **Standards**: GA4GH (Global Alliance for Genomics +
  Health) + DRS (Data Repository Service) + WES
  (Workflow Execution Service).

## What to learn next

- **Linux / shell basics** — pipes, awk, grep, sed,
  redirects.
- **Python or R** — pysam / pyranges / scanpy /
  Bioconductor.
- **Git / GitHub** — version control.
- **A workflow language** — Nextflow most popular
  in 2026.
- **Containers** — Docker + Singularity.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques** — see how each technology generates
  these file formats (Illumina → FASTQ; aligned →
  BAM; variants → VCF; etc.).
- **OrgChem → Tools → Lab analysers** — sequencing
  instruments + their typical output volumes.

This concludes the GM-3.0 beginner tier.  Next:
**PCR + qPCR + diagnostics** (intermediate).
