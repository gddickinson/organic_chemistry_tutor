# CRISPR experimental design

The CRISPR revolution has democratised genome editing,
but a successful experiment depends on a half-dozen
interlocking design decisions: target choice, sgRNA
design, Cas variant, delivery method, screening
strategy, and validation.

## Decision 1 — what to edit + why

Define the biological question first:

- **Knockout (loss-of-function)** — disrupt a gene to
  test its role.  Standard Cas9 + NHEJ → indel.
- **Knockin / point mutation** — install a specific
  change.  HDR (slow, low efficiency) or base /
  prime editor (no DSB).
- **Knockdown (transient suppression)** — CRISPRi
  (dCas9-KRAB) for stable + reversible
  transcriptional repression.
- **Activation** — CRISPRa (dCas9-VPR / SAM) for
  promoter-driven activation.
- **Tag insertion** — fluorescent / epitope /
  degron tag at endogenous locus.  HDR or HDR-
  enhancer chemistry (M3814 / NU7441 i-NHEJ).
- **Pooled screen** — 1 K-100 K perturbations vs a
  selectable phenotype.
- **Diagnostic** — SHERLOCK / DETECTR for
  nucleic-acid detection.
- **Therapeutic** — clinical CRISPR (Casgevy +
  Verve VERVE-101 + Intellia NTLA-2002 etc.).

## Decision 2 — Cas variant

| Cas variant | Use case | PAM | Notes |
|-------------|----------|-----|-------|
| SpCas9 | Workhorse | NGG | High fidelity variants (eSpCas9, HF1, HypaCas9, evoCas9) |
| SpCas9-NG / xCas9 / SpRY | Relaxed PAM | NGN / NRN / NNN | Trade-off: lower activity |
| SaCas9 | Smaller (~ 1 050 aa) | NNGRRT | Fits in single AAV |
| CjCas9 / NmCas9 | Even smaller | NNNVRYM / NNNNGAYW | Niche |
| Cas12a (LbCas12a / AsCas12a) | T-rich PAM, multiplex | TTTV | Self-processes crRNA arrays; ~ 1 300 aa |
| Cas12f / Cas14 | Tiny (400-700 aa) | T-rich | AAV-deliverable; emerging |
| Cas13a-d | RNA targeting | — | Diagnostic + RNA-knockdown |
| dCas9 (catalytically dead) | CRISPRi / CRISPRa / base editors / prime editors / chromatin epigenome editors | NGG | Multi-purpose scaffold |

## Decision 3 — sgRNA design

### Target selection

- **Position** — early-exon for full knockout (NMD
  +early-stop); functional-domain disruption for
  loss-of-function dominant-negative effects.
- **Splice junctions** — conservative knockout
  (intron-retained allele still produces partial
  protein).
- **Allele-specific** — exploit SNPs near PAM for
  haplotype-specific editing.

### Algorithmic design

Use validated sgRNA-design tools:

- **CHOPCHOP** — GUI-friendly; multiple Cas variants;
  extensive PAM options; good off-target prediction.
- **CRISPOR** — comprehensive; benchmarks multiple
  scoring algorithms.
- **Benchling** — commercial; integrated with
  cloning workflows.
- **Synthego CRISPR Design** — cloud + KO-
  validation pipeline.
- **GuideScan2** — fast; precomputed off-targets
  for major species.
- **DeepCRISPR + Azimuth + Rule Set 2** —
  ML-based on-target activity prediction.

### Scoring

- **On-target activity** — Doench Rule Set 2 (the
  benchmark for Cas9); Moreno-Mateos for in-vivo
  zebrafish; CINDEL for Cas12a.
- **Off-target** — CFD (Cutting Frequency
  Determination), MIT score, Cas-OFFinder for
  exhaustive enumeration.

### Practical sgRNA design rules

- **Start with G** — first base of spacer should be
  G (or 5'-Gn if using U6 promoter).
- **GC content** — 40-80 % ideal; extreme content
  may reduce activity.
- **Avoid 4+ T runs** — Pol III termination signal.
- **Multiple guides per target** — pool 3-4 guides
  for KO confidence; single high-quality guide for
  knockin.
- **Avoid SNPs in target** — check gnomAD; SNP can
  disrupt cleavage in heterozygous cell lines.

## Decision 4 — delivery method

| Delivery | Use case | Pros | Cons |
|----------|----------|------|------|
| Lipofection (RNP) | Cell lines, primary cells | High efficiency, transient (no DNA) | Cell-type-dependent |
| Electroporation (RNP / mRNA) | T cells, HSCs, primary cells, embryos | High efficiency, no DNA | Cell viability hit |
| Lentivirus | Stable expression + screens | Stable integration, easy scale | Random insertion site |
| AAV | In-vivo + clinical | Long-term expression in non-dividing tissue | Cargo limit (~ 4.7 kb), neutralising Abs |
| Lipid nanoparticle (LNP) | In-vivo (liver-tropic mostly) | Non-viral, scalable, redoseable | Liver tropism dominant |
| Plasmid transfection | Cell lines (legacy) | Cheap | Insertional + cytotoxic + DNA persistence |

For clinical applications:
- **Casgevy / exa-cel** — ex-vivo electroporation
  of HSCs with Cas9 RNP.
- **Verve VERVE-101 / -102** — in-vivo LNP
  delivery to liver hepatocytes.
- **Intellia NTLA-2002 / -2001** — in-vivo LNP.
- **Editas EDIT-101** — AAV intravitreal.
- **Beam BEAM-101** — ex-vivo HSC base editing.

## Decision 5 — screening + selection

### For single-target experiments

- **Sanger + TIDE / ICE** — quick deconvolution of
  bulk indel frequencies.
- **Amplicon NGS (CRISPResso2)** — quantitative
  per-allele genotype + indel profile.
- **ddPCR drop-off assay** — high-sensitivity
  rare-variant.
- **Phenotypic** — protein knockout (Western /
  IF / FACS) or function (reporter / activity
  assay).

### For pooled screens

- **Library design** — ~ 4-6 guides per gene
  (Brunello, Brie, TKOv3, GeCKO V2 standards).
- **Lentiviral transduction at MOI < 0.3** — one
  guide per cell.
- **Selection** — positive (drug resistance,
  growth) or negative (drug sensitivity, depletion).
- **Sequencing readout** — PCR-amplify guide
  region + Illumina; analyse with MAGeCK / DrugZ /
  CRISPhieRmix.
- **Coverage** — typically 500-1000× cells per
  guide for the initial library; 200-500× per
  time point.

## Decision 6 — validation

A CRISPR experiment isn't done until you've
confirmed:

1. **Editing efficiency at the target locus** —
   amplicon NGS (CRISPResso2) gives indel +
   substitution profile.
2. **Phenotype matches expectation** — protein
   knockdown verified by Western or FACS;
   function lost in functional assay.
3. **Off-target characterisation** — at least the
   top in-silico predictions; for clinical-grade
   work, GUIDE-seq / CIRCLE-seq / DISCOVER-seq /
   amplicon NGS at top sites.
4. **Karyotype / large-deletion check** — DSB
   sometimes induces large deletions / inversions
   / translocations / chromothripsis (especially
   problematic for HSC + iPSC editing).
5. **Allele independence** — bi-allelic vs mono-
   allelic editing matters for autosomal
   dominant / recessive phenotypes.
6. **Clonal vs polyclonal** — clonal isolation +
   re-validation gives clean genotype; pooled is
   faster but heterogeneous.

## Common pitfalls

- **Heterogeneous clones** — pooled edits are a
  mixture; functional assays may show partial
  effects.
- **Off-target effects** — almost always present
  to some degree; their biological impact varies.
- **Compensation** — knocked-out gene's paralog
  upregulates → no phenotype.
- **Dominant negative truncations** — partial-
  knockout fragment may have dominant function.
- **Splice variants** — knocking out exon 1
  doesn't kill all isoforms; some use alternative
  start sites.
- **Heterozygosity** — diploid cell lines may be
  KO/+ → only partial loss of function.
- **PAM-disrupting SNP** — silently prevents
  editing in some patients / strains.
- **Reagent QC** — sgRNA degradation / Cas9
  activity loss; positive controls catch this.

## Special-case design

### Base + prime editing

- **CBE / ABE** — choose to alter exact base; use
  benchTop or web-based PAM-window tools (BE-
  Designer, BE-Hive) for prediction.
- **Bystander edits** — characterise nearby
  cytidines / adenines that may also be edited.
- **Prime editing** — design pegRNA with PBS +
  RT template; multiple iteration of pegRNA
  design + epegRNA optimisation often needed.

### Multiplex CRISPR

- **Cas12a self-processing** — ideal for
  multiplex (single transcript with multiple
  spacers separated by direct repeats).
- **Cas9 multiplex** — Csy4 / tRNA processing /
  ribozyme cassettes; or dual-guide expression
  vectors.

### Knockin via HDR

- **Donor design** — short (90-200 nt) ssODN for
  point mutations + small tags; long (kb-scale)
  dsDNA / AAV / lentivirus for big inserts.
- **HDR enhancers** — small molecules (M3814,
  NU7441, RS-1) to bias toward HDR; cycle-
  arrested cells (G2/S synchronisation) to
  improve HDR.
- **Selection cassette** — eGFP + puro for
  initial enrichment; Cre-loxP excision for
  scarless final.

## Software ecosystem

- **CHOPCHOP**, **CRISPOR** — guide design.
- **CRISPResso2**, **TIDE / ICE** — editing
  outcomes analysis.
- **MAGeCK**, **DrugZ**, **BAGEL2** — pooled-
  screen analysis.
- **GUIDE-seq**, **CIRCLE-seq**, **DISCOVER-seq** —
  unbiased off-target detection.
- **Benchling**, **Geneious** — commercial design
  + cloning environments.
- **CRISPRecso**, **OffSpotter**, **Cas-OFFinder**
  — off-target enumeration.

## Cross-link

The GM-1.0 catalogue's `crispr-cas9`, `crispr-
cas12a`, `base-editor`, `prime-editor`, and
`crispr-diagnostics` entries provide the technology-
card context.  See also **MB-3.0 graduate "CRISPR +
microbial molecular biology"** for the natural-
immunity origin + therapeutic context.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques → CRISPR family** — 5 entries.
- **Window → Pharmacology Studio → Drug classes** —
  CRISPR therapeutics as a modality.
- **Window → Animal Biology Studio → Animal taxa** —
  model-organism options for CRISPR (worm, fly,
  fish, mouse, zebrafish, axolotl).

Next: **Cloning + synthetic biology basics**.
