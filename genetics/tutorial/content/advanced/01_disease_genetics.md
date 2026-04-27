# Mendelian + polygenic disease genetics

The genetics of human disease spans the spectrum
from single-gene Mendelian disorders (rare, high-
penetrance) through oligogenic conditions to common
polygenic disease (high prevalence, many small-
effect variants).  Modern molecular genetics
quantitatively dissects all three.

## Mendelian disease — the catalogue

OMIM (Online Mendelian Inheritance in Man) catalogues
> 17 K Mendelian phenotypes with > 5 K genetically
defined.  These include:

- **Cystic fibrosis** (CFTR) — most-common AR in
  Europeans (1 / 2 500 births).
- **Sickle-cell disease** (HBB Glu6Val) — high
  prevalence in malaria-endemic ancestries.
- **Huntington's** (HTT, CAG repeat) — autosomal
  dominant; full penetrance > 40 repeats.
- **Duchenne muscular dystrophy** (DMD) — X-linked
  recessive.
- **Familial hypercholesterolaemia** (LDLR / APOB
  / PCSK9 / LDLRAP1) — autosomal-dominant heart-
  disease risk.
- **Hereditary breast + ovarian cancer** (BRCA1 /
  BRCA2) — autosomal dominant; lifetime risk
  60-80 %.
- **Fragile X** (FMR1, CGG repeat) — X-linked;
  most-common inherited cause of intellectual
  disability.
- **Tay-Sachs disease** (HEXA) — AR;
  enriched in Ashkenazi Jewish + Cajun + French-
  Canadian populations.
- **β-thalassaemia + α-thalassaemia** (HBB / HBA1 /
  HBA2) — globin chain imbalance.
- **Hereditary haemochromatosis** (HFE C282Y) —
  most-common Mendelian disorder in Northern
  Europeans (~ 1 / 200 homozygotes).
- **Hereditary Long QT syndrome** (KCNQ1 / KCNH2 /
  SCN5A + others).

## Diagnosis — the molecular workup

### Single-gene testing
- Sanger sequencing of candidate genes.
- MLPA for CNV-prone genes (DMD, BRCA1/2, SMN).
- Targeted-panel NGS — 5-50 genes for syndrome-
  specific workups.

### Whole-exome sequencing (WES)
- ~ 1.5 % of genome (the protein-coding portion).
- Captures > 80 % of known disease-causing variants.
- Cost ~ $300-1000 in 2026 clinically.
- Diagnostic yield in undiagnosed-disease cohorts:
  25-50 % depending on phenotype + family history.

### Whole-genome sequencing (WGS)
- Catches variants in non-coding regions, structural
  variants, mitochondrial variants more reliably
  than WES.
- Increasingly first-line for paediatric rare disease
  (NHS Genomic Medicine Service has shifted from WES
  → WGS for many indications).

### Newborn screening
- Tandem-MS metabolite panels (PKU, MCAD, CAH, CF,
  congenital hypothyroidism).
- Genomic newborn screening pilots (BabySeq, NIH
  Newborn Sequencing in Genomic Medicine + Public
  Health) explore WES / WGS at birth.

### Carrier + reproductive genetics
- Expanded carrier screening — pre-conception
  panels test for ~ 100-500 recessive conditions.
- NIPT — circulating cell-free fetal DNA.
- PGT — pre-implantation genetic testing of IVF
  embryos (PGT-A aneuploidy, PGT-M monogenic, PGT-
  SR structural).

## Variant interpretation — ACMG/AMP framework

The 2015 ACMG/AMP guidelines (Richards et al.) +
ClinGen refinements provide a structured 5-tier
classification:

- **Pathogenic** — high-confidence disease-causing.
- **Likely pathogenic** — > 90 % chance.
- **Variant of uncertain significance (VUS)** —
  insufficient evidence either way.
- **Likely benign** — > 90 % chance benign.
- **Benign** — confidently benign.

Evidence categories:
- **Population data** (gnomAD frequency, ethnic
  background).
- **Functional data** (in-vitro / in-vivo
  experiments).
- **In-silico predictions** (CADD, REVEL, AlphaMissense
  for missense; SpliceAI for splicing).
- **Computational + literature evidence**.
- **Segregation in families**.
- **De novo + somatic vs germline**.

Tools: VarSome + Franklin (Genoox) + Mastermind +
ClinGen Allele Registry.

## Polygenic disease

Common diseases (T2DM, CAD, schizophrenia, depression,
common cancers, IBD, asthma) have:
- > 50-95 % heritability (twin + sib studies).
- Hundreds-thousands of contributing loci.
- Most variants of small effect (OR 1.05-1.20).
- Plus rare-variant + monogenic-form contributions.

### Genome-wide association studies (GWAS)

- Test millions of variants for association with
  phenotype.
- Logistic / linear regression with covariate
  adjustment (age, sex, PCs for ancestry).
- Genome-wide significance threshold: P < 5×10⁻⁸
  (Bonferroni for ~ 10⁶ independent SNPs).
- Output: Manhattan plot showing -log10(P) per
  position.

### Major resources

- **UK Biobank** — > 500 K participants; deeply
  phenotyped + WES + WGS released.
- **All of Us** — > 1 M planned; focused on
  diversity.
- **FinnGen** — Finnish founder population; high
  power for rare-variant analysis.
- **Million Veteran Program (MVP)** — > 1 M US
  veterans.
- **GWAS Catalog (EBI)** — curated published
  associations.
- **PGC** (Psychiatric Genomics Consortium) —
  schizophrenia + bipolar + ADHD + autism + MDD
  meta-analyses.

### Polygenic risk scores (PRS)

- Sum of variant effects weighted by GWAS β-coefficients.
- Predicts disease risk (continuous or
  dichotomised).
- Increasingly clinically deployed for CAD, breast
  cancer, T2DM.
- Major equity issue: most GWAS in European-
  ancestry populations → PRS less accurate in non-
  European populations.

### Heritability + missing heritability

- **Twin-based heritability** — high (50-95 %) for
  many traits.
- **GWAS-identified heritability** — typically
  10-30 % from significant SNPs.
- The "missing heritability" — likely from rare +
  structural + non-additive variants + GxE +
  epigenetics.

## Key analytical concepts

### Linkage disequilibrium (LD)

- Non-random association of alleles at nearby loci.
- LD blocks span ~ kb-100s of kb in humans (varies by
  population).
- GWAS hits identify a region, not a causal variant.
- Fine-mapping uses statistical methods (CAVIAR,
  SuSiE, FINEMAP) + functional annotation to pin
  down candidate causal variants.

### Burden + collapsing tests

- For rare variants: collapse all variants within a
  gene + test as a unit.
- **SKAT / SKAT-O** — robust to mixed effect
  directions.
- **Burden tests** — assume same direction.
- **REGENIE** — modern fast linear / logistic
  mixed-model regression with whole-genome support.

### Mendelian randomisation

- Use genetic variants as instrumental variables
  to test causality.
- Variants that influence an exposure can be tested
  for downstream effect on outcome.
- Avoids confounding (variant assignment is
  random at conception).
- Examples: LDL → CAD (yes), CRP → CAD (no), HDL →
  CAD (controversial).

## Pharmacogenomics

A specialised application of disease genetics
covered in detail in **PH-3.0 advanced
"Pharmacogenomics" lesson**.  Briefly, key gene-drug
pairs:

- CYP2D6 → codeine, tamoxifen, β-blockers.
- CYP2C19 → clopidogrel.
- CYP2C9 + VKORC1 → warfarin.
- TPMT + NUDT15 → thiopurines.
- DPYD → 5-FU.
- HLA-B*57:01 → abacavir.
- HLA-B*15:02 → carbamazepine.
- SLCO1B1 → simvastatin.
- UGT1A1 → irinotecan.

Implementation: CPIC guidelines + EHR-integrated
clinical decision support.

## Therapeutic implications

### Existing approaches

- **Replace the missing protein** — enzyme
  replacement therapy (Cerezyme for Gaucher,
  Aldurazyme for MPS-I).
- **Bypass the deficient pathway** — vitamin
  cofactor supplementation (B6 for cystathionine-β-
  synthase deficiency).
- **Substrate restriction** — phenylalanine-
  restricted diet for PKU.
- **Transplantation** — bone marrow for SCID,
  liver for OTC deficiency.

### Modern approaches

- **Gene therapy (AAV)** — Luxturna (RPE65),
  Zolgensma (SMN1), Hemgenix (FIX), Roctavian
  (FVIII), Elevidys (DMD), Upstaza (AADC).
- **CRISPR therapeutics** — Casgevy (BCL11A
  enhancer in HSCs for SCD + β-thal).
- **Base + prime editors** — Verve (PCSK9),
  Beam (HBG1/2), Prime Medicine (CYBB CGD).
- **mRNA-LNP genome editing** — Intellia (TTR for
  hATTR; KLKB1 for HAE).
- **ASO + siRNA** — nusinersen (SMN2), patisiran +
  vutrisiran (TTR), inclisiran (PCSK9), milasen
  (Batten n=1).
- **Selective splicing modulators** — risdiplam
  (SMA, oral SMN2 splicing).
- **n=1 personalised therapeutics** — milasen +
  follow-on programmes (n-Lorem) for individual
  patients.

## Equity + ancestry

A major emerging issue:
- 80 % of GWAS subjects + most reference panels
  + most variant-curation evidence is European
  ancestry.
- Variant calling, PRS, and ACMG classification all
  perform less well for non-European populations.
- ClinGen + CPIC + gnomAD v4 + Pan-ancestry T2D-GENES
  are working to expand coverage.
- Equity-aware bioinformatic tools (LDpred-funct,
  Polygenic Score Catalog) help calibrate.

## Cross-link

For molecular techniques used in disease genetics
(WES + WGS + targeted-panel + pharmacogenomic
genotyping), see GM-1.0 sequencing entries +
**MB-3.0 advanced microbiome / metagenomics** +
**PH-3.0 advanced "Pharmacogenomics"**.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques → sequencing** — Illumina + PacBio +
  ONT entries.
- **Window → Pharmacology Studio → Drug classes** —
  pharmacogenomically-actionable drugs.
- **Window → Microbiology Studio → Microbes** —
  microbial pathogens diagnosed by molecular
  testing.

Next: **Cancer genomics**.
