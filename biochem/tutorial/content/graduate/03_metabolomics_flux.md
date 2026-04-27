# Metabolomics + flux analysis

The fourth great omics — after genomics, transcriptomics,
proteomics — is **metabolomics**: the systematic
measurement + interpretation of small-molecule
metabolites in cells, tissues, blood, urine.  Adjacent +
complementary is **fluxomics** — measuring the RATES at
which metabolites flow through pathways.

## Why metabolomics is hard

Unlike DNA / RNA / proteins, metabolites are
chemically heterogeneous:

- ~ 5 000-20 000 putative human endogenous metabolites
  (HMDB count growing).
- Concentrations span ~ 12 orders of magnitude (ATP
  ~ mM; thyroid hormones ~ pM).
- Half-lives span ms-decades.
- Common scaffolds + isomers + stereoisomers blur
  identification.
- Compartmentalisation (mt vs cytosol vs lysosome) is
  invisible to bulk extraction.

There is no metabolomics PCR — every measurement is
analytical chemistry.

## Analytical platforms

### Mass spectrometry — the workhorse

- **LC-MS** (liquid chromatography + MS) — covers most
  polar + semi-polar metabolites.  Reverse-phase C18
  for non-polar, HILIC for polar, ion-pairing for
  phosphorylated metabolites.
- **GC-MS** — small-molecule volatiles + derivatised
  (TMS, MeOX) primary metabolites.  Older + reproducible
  EI fragmentation libraries (NIST).
- **CE-MS** — high resolution for charged metabolites
  (Soga's group did landmark cancer-tissue work).
- **MALDI-MSI** (mass-spec imaging) — spatial
  distribution at ~ 10-50 µm.
- **DESI-MSI** + **SIMS** — alternative ionisation for
  imaging.

### NMR

- ¹H-NMR less sensitive (mM detection limits) but
  quantitative + reproducible + non-destructive.  Ideal
  for serum / urine clinical metabolomics.  HSQC + HMBC
  + TOCSY for structural ID.
- ¹³C-NMR isotopologue analysis is gold-standard for
  flux work (see below).

### Targeted vs untargeted

- **Untargeted** — measure everything detectable; data-
  analysis challenge of identifying unknown peaks.  ID
  rate ~ 5-30 %.
- **Targeted** — pre-selected ~ 100-500 metabolites with
  authenticated standards + multiple-reaction monitoring
  (MRM) on triple quad → quantitative + reproducible.
- **Semi-targeted** — large pre-defined panels (Biocrates,
  Metabolon) with known IDs but assay-specific
  coverage.

## The annotation crisis

A typical untargeted LC-MS run picks up 5 000-20 000
features (mass + retention time pairs).  Identifying
each requires:

1. **Mass accuracy** (< 5 ppm) → narrow molecular-formula
   candidates.
2. **MS/MS fragmentation** matched against libraries
   (METLIN, MoNA, GNPS, MassBank).
3. **Authenticated standard co-elution** — gold-standard
   identification (Schymanski Level 1).
4. **Isotope-pattern + adduct-pattern analysis** to
   confirm formula.

The MSI Schymanski levels classify confidence (1 =
identified standard, 4 = unequivocal molecular formula,
5 = exact mass only).  Most reported metabolites in
papers are level 2-3.

## Pathway + statistical analysis

Once you have IDs + abundances:

- **Univariate** — t-test, Mann-Whitney, FDR-adjusted
  per metabolite.
- **Multivariate** — PCA, OPLS-DA, random forests.
- **Pathway enrichment** — MetaboAnalyst, Mummichog
  (untargeted-friendly), KEGG / Reactome / Recon3D
  topology.
- **Genome-scale metabolic models (GEMs)** — Recon3D,
  HMR2 — context for which pathways are even possible.

## Fluxomics — the missing fourth dimension

Concentrations alone don't tell you whether a metabolite
is high because production is faster or consumption is
slower.  **Flux** = rate per unit volume.  You measure
flux by tracking labelled atoms.

### Stable-isotope tracing

Feed cells / tissue / animal / patient a ¹³C-labelled
substrate (uniformly ¹³C₆-glucose, [1,2-¹³C]-glucose,
¹³C₅-glutamine, ²H₇-glucose, ¹⁵N-amide-glutamine).  At
quasi-steady-state, measure the **isotopologue
distribution** (M+0, M+1, …, M+n) for each downstream
metabolite by LC-MS or NMR.

The pattern of label scrambling diagnoses pathway
activity:
- ¹³C from glucose appears in lactate (glycolysis vs
  oxidation).
- M+2 vs M+3 citrate distinguishes glucose-via-PDH vs
  glutamine-via-α-KG entry to TCA.
- Pentose-phosphate flux gives ¹³CO₂ from C1-glucose
  (decarboxylation step).
- Reductive carboxylation (cancer hypoxic phenotype)
  shows reverse-IDH labelling.

### Metabolic flux analysis (MFA)

Mathematical inference: given measured isotopologue
distributions + a stoichiometric model, fit the FLUX
through every reaction.

- **Stationary MFA (¹³C-MFA)** — assumes metabolic +
  isotopic steady state.  Mature; INCA + 13CFLUX2 +
  Metran solve the inverse problem.
- **Non-stationary INST-MFA** — measures isotopologues
  before isotopic steady state; needed for
  photosynthesis + most short-half-life pathways.
- **Dynamic flux analysis** — coupled ODEs for
  concentrations + fluxes; fits time-courses of
  perturbations.

### Constraint-based modelling — flux balance analysis (FBA)

For genome-scale models, MFA is intractable but FBA
isn't:

- Stoichiometric matrix S (m × n; m metabolites, n
  reactions).
- Steady-state assumption: S · v = 0.
- Bound each flux: v_min ≤ v ≤ v_max.
- Define an objective (often biomass production for
  microbes, or ATP yield) + linear-programme.

FBA is the engine behind genome-scale metabolic models
(GSMMs):
- **iML1515** for *E. coli* (Monk 2017).
- **Recon3D** + **HMR2** for human.
- **Yeast8 / Yeast-GEM** for *S. cerevisiae*.
- > 6000 published GSMMs in the BiGG database.

Variants — pFBA (parsimonious), eFBA (energy), MOMA +
ROOM (knockout response), dFBA (dynamic), FVA (flux
variability) — each address specific questions.

## Cancer metabolism — the killer app

Otto Warburg's 1924 observation that tumours ferment
glucose to lactate even in O₂ ("aerobic glycolysis")
is now the foundational story.  Modern flux work has
revealed:

- **Glutamine addiction** — many cancers oxidise
  glutamine via α-KG to fuel TCA.  CB-839 (telaglenastat)
  glutaminase inhibitor in trials.
- **Reductive carboxylation** — under hypoxia, IDH1/2
  runs in reverse: α-KG + CO₂ → isocitrate → acetyl-CoA
  for lipid synthesis.
- **One-carbon metabolism** — folate cycle + serine /
  glycine cleavage drives nucleotide + methylation;
  serine starvation slows tumours in mice.
- **Lactate as fuel** — counter-Warburg: some tumour
  cells SHUTTLE lactate for oxidation; MCT1 inhibitors
  in trials.
- **Onco-metabolites** — IDH1/2 R132H mutants produce
  2-HG (2-hydroxyglutarate) → KDM / TET inhibition →
  hypermethylator phenotype.  Ivosidenib + enasidenib
  + olutasidenib FDA-approved for IDH-mutant AML +
  cholangiocarcinoma + glioma.
- **SDH + FH mutations** drive paraganglioma + HLRCC →
  succinate + fumarate accumulation as oncometabolites.

## Clinical metabolomics

- **Inborn errors of metabolism (IEMs)** — > 600
  Mendelian disorders.  Tandem-MS newborn screening
  routinely scans ~ 50 IEMs (PKU, MCAD def, MMA, etc.)
  in a single dried-blood-spot run.
- **Pharmacometabolomics** — predict drug response from
  baseline metabolome.
- **Microbiome-derived metabolites** — TMAO + CVD risk;
  short-chain fatty acids + colon health; bile acid
  remodelling + immunomodulation.
- **Metabolomics-aided diagnostics** — 2-HG NMR for IDH-
  mutant glioma; sphingomyelin profiling for cardiac
  risk; branched-chain AAs for diabetes risk.
- **Polar metabolite cancer signatures** — FDA-cleared
  panels (oncotype-DX-like) emerging.

## Reproducibility + standards

The field has had a reproducibility reckoning:
- **Pre-analytical variation** dwarfs biological signal
  in most untargeted studies.  Sample collection +
  quenching + extraction protocols matter immensely.
- **Metabolomics Standards Initiative (MSI)** + **mwTab
  / mzML** + **Metabolomics Workbench / MetaboLights**
  data deposition.
- **Cross-laboratory harmonisation** programmes
  (NIH-NIST quality-control reference materials).
- **Always run pooled-QC samples** every 5-10 patient
  samples + monitor signal drift + abandon runs that
  drift.

## Open frontiers

- **Spatial metabolomics** (MALDI-MSI + DESI-MSI) at
  cellular resolution.
- **Single-cell metabolomics** — emerging via
  microfluidic coupling.
- **Compartmentalised flux measurements** — separating
  mitochondrial vs cytosolic NADPH (Rabinowitz lab is
  leading).
- **In-vivo human flux measurements** at clinically
  meaningful scale (deuterated-water for proteome /
  glucose flux studies are mature).
- **Combined multi-omics integration** — proteomics +
  transcriptomics + metabolomics + fluxomics through
  unified models (Bayesian + ML approaches).
- **Microbiome co-metabolism** — host + gut-microbe
  metabolic exchange measured via co-occurring labels.

## Try it in the app

- **Window → Biochem Studio → Metabolic pathways** —
  glycolysis, TCA, ox-phos, fatty-acid β-oxidation.
- **Window → Biochem Studio → Cofactors** — `nadph`,
  `acetyl-coa`, `glutathione` are central metabolites
  for many flux signatures.
- **OrgChem → Tools → MS isotope pattern** — preview
  M+1 / M+2 patterns for isotopologue analysis.

Next sibling: **Pharmacology** — your tour through
PK/PD, ADME, and modern drug development.
