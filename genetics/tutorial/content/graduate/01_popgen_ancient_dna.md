# Population genetics + ancient DNA

Population genetics is the study of allele
frequencies + their evolutionary dynamics in
populations.  Ancient DNA (aDNA) extends the analysis
back through tens of thousands of years, transforming
both anthropology + medical genetics.

## Foundational concepts

### Allele frequencies

For a biallelic locus with alleles A + a:
- **p** = frequency of A.
- **q** = frequency of a (p + q = 1).
- **Genotype frequencies** under Hardy-Weinberg
  equilibrium (HWE): p² (AA) + 2pq (Aa) + q² (aa).

HWE assumptions:
- Random mating.
- No selection.
- No mutation.
- No migration.
- Infinite population size.

In practice no population satisfies all assumptions,
but HWE is the null model against which
deviations identify interesting biology.

### Effective population size (Ne)

The size of an idealised Wright-Fisher population
that would produce the same genetic variation as the
actual population.  Ne is usually much smaller than
census N due to:
- Sex ratio imbalance.
- Variance in offspring number.
- Population fluctuations / bottlenecks.
- Subdivided populations.

Human Ne is ~ 10 000 over much of history; lower
during bottlenecks (out-of-Africa ~ 70 000 ya).

### Genetic drift

Random fluctuation in allele frequencies due to
finite population sampling.  Effect is stronger in
small populations:
- Var(Δp) ≈ p(1-p) / 2Ne per generation.
- Time to fixation / loss ~ 4Ne generations.
- Drives loss of variation; founder effects;
  founder-related disease enrichment (Ashkenazi BRCA1
  founder, Finnish IEM enrichment).

### Mutation rate

- **Germline mutation rate** in humans:
  ~ 1.2 × 10⁻⁸ per base per generation (each child
  carries ~ 70 de novo mutations).
- **Father age** is dominant contributor (sperm
  divisions accumulate over life).
- **Substitution rate** at neutral sites approx
  equals mutation rate (Kimura).
- Selection alters substitution rate at functional
  sites (negative selection slows; positive
  selection accelerates).

### Selection coefficients

- **s = 0** — neutral.
- **s > 0** — positive selection (advantageous).
- **s < 0** — negative selection (deleterious).
- **Balancing selection** — heterozygote advantage
  (HbS in malarial regions; HLA in immune defence).

### Coalescents

Looking BACKWARD in time, lineages merge
("coalesce").  Coalescent theory provides a
statistical framework for inferring demographic
+ selective history from sequence data.

Tools: msprime, SLiM (forward + backward), tskit
ecosystem.

## Major population-scale datasets

- **1000 Genomes Project** (1KGP, 2008-2015) — 2 504
  WGS across 26 populations; foundational reference.
- **gnomAD** (Genome Aggregation Database) — > 800 K
  exomes + > 75 K WGS aggregated; the de-facto
  variant-frequency reference.
- **UK Biobank** — > 500 K genotyped + WGS; deeply
  phenotyped.
- **All of Us** — > 1 M planned; diverse-ancestry
  emphasis.
- **TOPMed** — 132 K diverse-ancestry WGS.
- **Estonian Biobank, FinnGen, Million Veteran
  Program, Generations + Generation Scotland** —
  national / regional cohorts.
- **Genome Asia 100K, H3Africa** — non-European
  ancestry programmes.

## Inferring population structure

### Principal component analysis (PCA)

Reduces high-dimensional genotype data to 2-D
visualisation.  Top PCs typically reflect ancestry
(geographic gradients).

### Admixture analysis

- **STRUCTURE / ADMIXTURE / fastSTRUCTURE** —
  Bayesian / ML estimation of admixture proportions
  per individual.
- Outputs ancestral-population proportions; assumes
  K populations contributed.

### F-statistics

- **F-st** — fraction of total genetic variation
  due to population differentiation.
- **f3 + f4 + D-statistics** — admixture +
  treeness tests.
- **Patterson + ancient-DNA toolkits** — qpAdm /
  qpGraph for inferring admixture histories.

### Identity-by-descent (IBD)

- **IBD segments** — long stretches of identical
  haplotype shared by descent (vs identity-by-state).
- Used for relatedness inference (KING, hapibd,
  iLASH).
- Detects cryptic relatedness in cohorts; identifies
  founder effects.

## Detecting selection

### Within-species

- **Tajima's D** — neutral vs selection.
- **Fay + Wu's H**.
- **iHS (integrated Haplotype Score)** — recent
  positive selection (haplotype sharing).
- **XP-EHH + nSL** — population-comparative
  haplotype-based.
- **Composite Likelihood Ratio (CLR)** — sweep
  detection.
- **PBS (Population Branch Statistic)** — three-
  population.

### Between-species

- **dN / dS** ratio of non-synonymous : synonymous
  substitutions.
  - dN/dS < 1 → purifying selection.
  - dN/dS = 1 → neutral.
  - dN/dS > 1 → positive selection.
- **HKA test** — divergence-vs-polymorphism
  inconsistency.
- **MK test** — McDonald-Kreitman; selection on
  amino-acid changes.

### Famous examples

- **Lactase persistence (LCT / MCM6 enhancer)** —
  multiple independent origins linked to dairying
  (Europe ~ 7 K ya; East Africa later; Arabia
  later).
- **EPAS1 + EGLN1** — high-altitude adaptation in
  Tibetans (Denisovan-introgressed).
- **EDAR V370A** — East-Asian hair + sweat-gland
  morphology.
- **SLC24A5 + SLC45A2 + MC1R + OCA2 + HERC2** —
  pigmentation across ancestries.
- **AMY1 copy number** — starch consumption.
- **HbS + HbC + G6PD + DARC** — malaria
  resistance.
- **CCR5-Δ32** — partial protection against
  plague + smallpox + HIV.
- **APOL1** G1 / G2 — kidney disease in African-
  ancestry; trypanosomal-resistance balancing.

## Ancient DNA — the methods

### Recovery + extraction

- DNA highly fragmented (typical fragments ~ 30-
  150 bp).
- Cytosine deamination accumulates → C→T at 5'
  ends + G→A at 3' ends (signature damage
  pattern).
- Petrous bone (cochlea) yields highest % endogenous
  DNA in mammals; teeth + dentine also good.
- Special clean rooms + protocols to avoid modern
  contamination.

### Library prep

- **Single-stranded library prep** (Meyer +
  Kircher 2010) — captures damaged + short
  fragments.
- **UDG treatment** — removes deaminated cytosines
  + reduces damage (but also removes endogenous
  base modifications).
- **Hybridisation capture** — enriches for human /
  mitochondrial / target-locus DNA.

### Authentication

- **DNA damage pattern** — verifies endogenous
  ancient origin.
- **Read length distribution** — short reads
  consistent with ancient DNA.
- **Contamination tests** — schmutzi
  (mitochondrial), ANGSD (X-chromosome), nuclear.

## Ancient DNA achievements

### Pääbo Nobel 2022

Svante Pääbo + colleagues:

- **Mitochondrial Neanderthal genome** (2008) — first
  ancient hominin genome.
- **Nuclear Neanderthal genome** (2010) — revealed
  Neanderthal-modern-human interbreeding; ~ 2 % of
  modern non-African genomes are Neanderthal-derived.
- **Denisovan genome** (2010, from a Siberian cave
  pinky bone) — distinct hominin; introgressed into
  modern humans, particularly in Melanesians +
  Tibetans (EPAS1).

Pääbo received the 2022 Nobel Prize in Physiology
or Medicine for "his discoveries concerning the
genomes of extinct hominins and human evolution."

### Other landmark aDNA studies

- **Ötzi the Iceman** (2012 genome) — South-Tyrolean
  5 300-year-old.
- **Mungo Lady + Man** (Australian Pleistocene).
- **Cheddar Man** (Mesolithic Britain) — surprised
  the public with dark skin + blue eye genotype.
- **Stuttgart + Loschbour** (early-Neolithic +
  Mesolithic European).
- **Yamnaya steppe pastoralists** — ~ 5 000 ya;
  Bronze Age expansion across Europe + South Asia.
- **Newgrange + Megalithic populations** — kinship
  + social structure inference.
- **Human pathogen aDNA** — Black Death *Y. pestis*,
  ancient TB (in Andean mummies pre-Columbus),
  Salmonella in pre-Columbian Americas, ancient
  HBV / variola / leprosy.

### Plant + animal aDNA

- **Cave bear, mammoth, sabre-tooth cat genomes** —
  Pleistocene megafauna.
- **Mungo lake aboriginal sediments + bog
  preservation**.
- **Ancient maize + wheat domestication
  histories**.
- **Ancient horse + cattle + dog + pig domestication
  histories**.

### Sediment aDNA + iceberg-DNA

- Recently: aDNA recovered from cave + lake
  sediments + ice cores + air without bone (Slon
  + Meyer; Willerslev).
- Detected fauna + flora + microbes that left no
  bones / pollen.

## Modern human history insights

aDNA + modern-population genomics together have
rewritten:

- **The peopling of Europe** — three major waves
  (Mesolithic hunter-gatherers, Neolithic Anatolian
  farmers, Bronze Age Yamnaya steppe pastoralists).
- **Bronze-Age Indo-European expansion** —
  Yamnaya-related ancestry expanded across Europe
  + Central Asia + South Asia.
- **Peopling of the Americas** — earlier than
  thought (~ 16-23 K ya); multiple Beringian
  populations.
- **Africa's deep diversity** — much greater than
  outside Africa; Khoisan + pygmy + Bantu
  expansions.
- **Out of Africa migration** — 50-70 K ya; with
  multiple smaller earlier dispersals + back-
  migrations.
- **South + Southeast Asian complexity** — Indus
  Valley Civilisation continuity + Bronze-Age
  steppe admixture + indigenous deep ancestry.
- **Pacific peopling** — Lapita expansion + later
  Polynesian voyaging.

## Pan-genome + reference shifts

The classical single-reference-genome paradigm is
giving way to **pan-genomes**:
- HPRC (Human Pangenome Reference Consortium) — 47
  haplotype-resolved genomes published 2023; ~ 350
  planned.
- Captures structural-variant + ancestral diversity
  systematically.
- Pangenome alignment (Giraffe, vg, minigraph) +
  variant calling improving rapidly.

## Selection at single-base resolution + Mendelian
randomisation

A modern intersection of population genetics +
disease genetics:
- Common variants under recent selection often
  modulate disease risk (LCT for lactose,
  EPAS1 for hypoxia tolerance, sickle-cell for
  malaria).
- Mendelian randomisation uses these natural
  experiments to test causality of biomarkers vs
  diseases (LDL → CAD: yes; CRP → CAD: no; HDL →
  CAD: controversial).

## Forensic + investigative genetic genealogy

- **Standard STR profiles** (CODIS markers, 13-20
  loci) — used by law enforcement for matching
  + paternity.
- **Investigative genetic genealogy (IGG)** —
  upload SNP data to GEDmatch / FamilyTreeDNA →
  identify distant relatives → reconstruct family
  tree → narrow suspect identity.  Golden State
  Killer (2018) brought IGG into public
  consciousness.
- Privacy + consent debates ongoing; FBI + DOJ
  guidelines emerged 2019.

## Cross-link

The GM-1.0 catalogue's `pacbio-hifi`, `ont-
nanopore`, `illumina-short-read`, and `ap-ms`
entries provide technology-card context.  See also
**AB-3.0 graduate "Comparative genomics + animal
evolution"** for paleogenomic + comparative-
evolution context.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques → sequencing** — Illumina + PacBio +
  ONT for population-scale + aDNA work.
- **Window → Animal Biology Studio → Animal taxa** —
  human + extinct hominins + ancient-DNA-recovered
  megafauna.

Next: **Comparative + functional genomics**.
