# Microbiome + metagenomics

The microbiome — the collective community of microbes
living on + in a host — is now one of the most
intensively-studied areas of biology.  Two technological
revolutions enabled it: (1) the recognition that ~ 99 %
of microbes can't be cultured + (2) cheap NGS that
made culture-independent profiling routine.

## What "microbiome" means

Distinct concepts often conflated:
- **Microbiota** — the community of microbes
  themselves (taxa + abundances).
- **Microbiome** — the microbiota PLUS their genomes,
  metabolites, structural elements, environmental
  conditions.
- **Metagenome** — all genomic DNA in a community
  sample.
- **Metatranscriptome** — all RNAs.
- **Metabolome** — small-molecule metabolites.
- **Holobiont** — host + all its microbes treated as
  a functional unit.

Each layer is interrogated by different technologies +
gives different answers.

## Profiling technologies

### 16S rRNA amplicon sequencing

The workhorse of microbiome surveys.

- PCR-amplify a hypervariable region (V3-V4 most
  common) of the bacterial 16S rRNA gene from
  community DNA.
- Sequence on Illumina (~ 20 K-100 K reads / sample).
- Cluster reads into ASVs (amplicon sequence variants)
  via DADA2 / Deblur / Vsearch — ASVs replace OTUs
  for higher taxonomic resolution.
- Assign taxonomy via SILVA, Greengenes2, GTDB.

Strengths: cheap, scalable, tolerates degraded
samples, well-curated databases.
Limitations: bacteria + archaea only (no fungi or
viruses); genus-level resolution typical
(species/strain ambiguous); functional inference
indirect.

### ITS amplicon

For fungi — internal transcribed spacer (ITS1 or
ITS2) of the rRNA operon.  UNITE database for
taxonomy.

### Shotgun metagenomic sequencing

Sequence ALL DNA in the sample, no PCR
amplification.

- Output: 1-10 GB / sample of mixed-origin reads.
- Pipelines:
  - **Kraken2 / Bracken** for taxonomy.
  - **HUMAnN3** for functional pathway abundance.
  - **MetaPhlAn4** for marker-gene-based species ID.
  - **MetaSPAdes / MEGAHIT** for assembly.
  - **MaxBin / MetaBAT / CONCOCT** for binning into
    MAGs (metagenome-assembled genomes).

Strengths: species + strain resolution; functional
gene content; antibiotic-resistance gene + virulence
factor surveys; novel-taxa discovery (~ 200 K
human-gut MAGs catalogued in UHGG / SPIRE).
Limitations: more expensive (~ 5-10× 16S);
computationally demanding; biased toward
high-abundance taxa.

### Long-read metagenomics

PacBio HiFi + ONT for circularised microbial chromosomes
+ near-complete MAGs from single samples.  Increasingly
common.

### Metatranscriptomics

Sequence community RNA → who's expressing what.
Reveals active vs dormant taxa + responsive
functions.

### Metaproteomics

LC-MS/MS of community proteins.  Functional readout
at the protein level.

### Metabolomics

LC/GC-MS or NMR of community metabolites.  Often the
most clinically-actionable read-out (SCFAs,
secondary bile acids, TMAO, indoles).

A future **Genetics + Molecular Biology Studio**
sibling will deepen the technique side of microbiome
profiling.

## Major human microbiomes

### Gut

Dominant + most-studied.  ~ 10¹³-10¹⁴ microbes;
> 1 000 species per individual; 100× more genes than
the human genome.

Compositional signatures:
- **Bacteroidota** (Bacteroidetes) + **Bacillota**
  (Firmicutes) dominate.
- Genus-level diversity: *Bacteroides*, *Prevotella*,
  *Faecalibacterium*, *Roseburia*, *Eubacterium*,
  *Akkermansia*, *Bifidobacterium*, *Lactobacillus*.
- Functional core: SCFA production, bile-acid
  modification, B-vitamin synthesis, polysaccharide
  fermentation.

Disease associations (correlation, not always causal):
- IBD — reduced *F. prausnitzii*, increased
  Enterobacterales.
- Obesity — Firmicutes:Bacteroidetes ratio
  (controversial).
- T2DM — reduced butyrate producers, increased
  inflammatory taxa.
- Colorectal cancer — *F. nucleatum*, *Bacteroides
  fragilis* (toxigenic), *pks+ E. coli*.
- C. difficile recurrence — reduced diversity, loss
  of bile-acid-modifying clades.
- Allergic / autoimmune disease — reduced early-life
  diversity ("hygiene hypothesis"-related).
- Cancer immunotherapy response — *Akkermansia*,
  *Bifidobacterium*, *Faecalibacterium* enriched in
  responders.

### Skin

Site-specific:
- **Sebaceous** (face, back) — *Cutibacterium acnes*
  dominates.
- **Moist** (axilla, groin) — *Corynebacterium*,
  *Staphylococcus*, *Malassezia*.
- **Dry** (forearms, palms) — diverse, low biomass.

Disease associations: atopic dermatitis (*S. aureus*
overgrowth), acne (*C. acnes* phylotypes), psoriasis,
hidradenitis suppurativa.

### Oral

300+ species per person; ~ 10¹⁰ microbes.  Site-
specific (saliva vs subgingival vs supragingival
plaque vs tongue).

Pathogens: *Streptococcus mutans* + *Lactobacillus*
(caries), *Porphyromonas gingivalis* + *Tannerella*
+ *Treponema denticola* (red-complex periodontitis).
*P. gingivalis* now linked to atherosclerosis +
Alzheimer's.

### Vaginal

Healthy = Lactobacillus-dominant (mostly *L. crispatus*,
*L. iners*, *L. gasseri*, *L. jensenii*); produce
lactic acid → low pH (3.5-4.5) → suppresses
pathogens.  Bacterial vaginosis = polymicrobial
overgrowth (Gardnerella, Atopobium, Sneathia).

### Lung

Once thought sterile; we now know low-biomass
microbiomes exist.  CF + bronchiectasis +
COPD have characteristic dysbiosis (Pseudomonas,
Burkholderia, Stenotrophomonas, anaerobes).

### Other sites

Stomach (H. pylori dominant if positive),
small bowel (variable), urinary (bladder microbiome
recently characterised).

## Dysbiosis + intervention

Dysbiosis = microbiota composition associated with a
disease state.  Re-establishing healthy composition
is therapeutic in some settings.

### Faecal microbiota transplantation (FMT)

- > 90 % cure rate for recurrent *C. difficile*
  (recurrent ≥ 2nd episode).
- Multiple delivery routes — colonoscopy, NG tube,
  capsules.
- Now multiple FDA-approved formulations: Rebyota
  (rectal), Vowst (oral SER-109).

### Defined microbial consortia / live biotherapeutics

Vedanta, Seres, Finch, 4D Pharma developing:
- Defined consortia of cultivated strains.
- Spore-based (oral capsule, easier delivery).
- Indications: rCDI, IBD, cancer-immunotherapy
  augmentation, hepatic encephalopathy.

### Prebiotics + postbiotics

- **Prebiotics** — substrates that selectively
  promote beneficial microbes (FOS, GOS, inulin,
  resistant starch).
- **Probiotics** — live microbes administered for
  health benefit (Lactobacillus, Bifidobacterium,
  *Saccharomyces boulardii*).  Modest evidence for
  most claims.
- **Postbiotics** — microbial metabolites + cell-wall
  components administered as the active therapeutic
  (butyrate, propionate, defined cell-wall components).
- **Synbiotics** — pre + pro combination.

### Microbiome modulation by diet

- **Fibre** strongly increases SCFA-producer abundance.
- **Mediterranean / plant-rich diets** increase
  diversity + SCFA production.
- **High-fat / Western diets** decrease diversity +
  shift toward inflammatory taxa.
- **Fermented foods** (yoghurt, kefir, kimchi,
  sauerkraut, kombucha) modestly modulate composition.

### Pharmacological microbiome interactions

- Antibiotics — broad-spectrum agents disrupt
  microbiomes for months-years; collateral damage
  drives *C. difficile* + AMR + immune dysregulation.
- PPIs — small-bowel bacterial overgrowth (SIBO)
  signal.
- Metformin — partly works via microbiome
  modulation.
- Many drugs metabolised by gut microbes (digoxin
  by *Eggerthella lenta*; sulfasalazine activation;
  irinotecan SN-38 reactivation by β-glucuronidases).

## The virome

The viral component of the microbiome — mostly
phages + some eukaryotic viruses.  Vastly under-
studied because:
- Smaller signal in shotgun sequencing.
- Limited reference databases.
- Large fraction "viral dark matter" — unknown.

Roles:
- Modulate bacterial population structure (top-down
  predation).
- Drive bacterial evolution (transduction).
- Direct host interactions (some eukaryotic viruses
  are commensal — Anelloviridae nearly universal).

## Earth + environmental microbiomes

- **Tara Oceans** — global ocean plankton survey;
  > 100 K MAGs.
- **Earth Microbiome Project** — 30 K samples
  across all biomes.
- **Genomic Standards Consortium MIxS** — metadata
  standards.
- **Soil + plant rhizosphere** — agricultural +
  ecological relevance.
- **Built environment** (homes, hospitals, ISS) —
  HMP-style longitudinal studies.

## Causal inference in microbiome research

A persistent challenge — microbiome composition
COrrelates with countless outcomes; causal links are
much harder to establish.

Strengths of evidence:
1. **Mendelian randomisation** — host-genetic
   instrument variables (*FUT2* + *Bifidobacterium*).
2. **Germ-free + gnotobiotic mouse models** —
   transfer microbiota from cases vs controls.
3. **FMT in humans** — direct clinical-outcome
   change supports causality (rCDI clearest).
4. **Defined-consortium administration** —
   gain-of-function.
5. **Antibiotic ablation** — loss-of-function.

Confounders: diet, age, sex, BMI, geography,
medications, sampling method, storage conditions,
extraction method, sequencing platform.

## The microbiome industry + clinical translation

- **Diagnostic** — microbiome-based diagnostic
  panels for IBD, depression, response prediction
  (early-stage).
- **Therapeutic** — Rebyota, Vowst FDA-approved;
  many others Phase 2/3.
- **Cosmetics + skincare** — microbiome-friendly +
  postbiotic-formulated products.
- **Personalised nutrition** — Day Two, Zoe,
  Viome (evidence base mixed).

## Cross-link

For molecular techniques (16S sequencing, shotgun
metagenomics, metatranscriptomics protocols), the
upcoming **Genetics + Molecular Biology Studio**
will host the technique-level lessons.  For
**SCFA** / bile-acid metabolism cross-references,
see **BC-3.0 graduate "Metabolomics + flux
analysis"**.

## Try it in the app

- **Window → Microbiology Studio → Microbes** —
  per-microbe gut-vs-pathobiont notes.
- **Window → Biochem Studio → Metabolic pathways** —
  microbial-derived SCFA + bile-acid pathways.
- **Window → Cell Biology Studio → Signalling** —
  microbiome-host immune signalling (TLR, NF-κB,
  NLRP3).

Next: **Emerging + zoonotic infections**.
