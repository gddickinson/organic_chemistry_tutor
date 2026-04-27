# Drug development pipeline

The journey from a biological hypothesis to an approved
drug spans 12-15 years, costs ~ $2.6 B (Tufts CSDD
2020 estimate, capitalised), and sees ~ 90 % attrition
between Phase 1 entry and approval.  Understanding the
pipeline is foundational to industrial pharmacology.

## Stage 1 — Target identification + validation

Where biology + medicinal chemistry meet.

**Target ID** sources:
- Disease genetics (GWAS, exome / whole-genome
  sequencing, Mendelian disorders).
- Functional genomics (CRISPR screens — knock-out,
  knock-in, base editing, prime editing; siRNA;
  shRNA libraries).
- Pathway analysis from omics (transcriptomics,
  proteomics, metabolomics, single-cell).
- Reverse / forward chemical genetics — phenotypic
  screens of compound libraries identify the target
  later.
- Comparative biology — successful drugs reveal new
  targets (e.g. SSRIs led to NET / DAT modulators).

**Target validation** evidence:
- Genetic evidence — loss-of-function variants
  protect from disease (PCSK9 → evolocumab).
- Animal model phenocopy — KO mouse mimics the desired
  pharmacological phenotype.
- Tool compounds — small molecules + antibodies that
  modulate the target reproduce the phenotype.
- Tractability — protein has a druggable site
  (cryptic pockets, kinase ATP site, GPCR
  orthosteric pocket, allosteric vulnerabilities).

Genetically-validated targets have ~ 2-3× higher
clinical success rate (Nelson 2015 + later studies).

## Stage 2 — Hit identification

Find chemical matter that engages the target.

**High-throughput screening (HTS)** — screen 10⁵-10⁷
compounds in a target-specific assay.  Hit rate
typically 0.1-1 %.  Industrial scale.

**Fragment-based drug discovery (FBDD)** — screen
~ 1 000-10 000 small (< 250 Da) "fragments" by SPR /
ITC / NMR / X-ray; merge / grow / link to lead-like
molecules.  Pioneered by Astex; the BCL-2 inhibitor
**venetoclax** is the canonical FBDD success.

**DNA-encoded libraries (DELs)** — chemistry encoded by
DNA tags allows pooling 10⁹-10¹² compounds in a single
selection.  GSK + X-Chem.  Widely used since ~ 2010.

**Virtual screening** — computational docking +
pharmacophore + ligand-based ML to rank compounds
before any wet-lab test.  Increasingly hybridised with
ML potential / generative models.

**Phenotypic screening** — assay a complex phenotype
(cell viability, organism behaviour, organoid response)
and identify hits agnostic to mechanism.  Resurgent
since 2010 (Swinney + Anthony 2011 Nature Reviews
showed phenotypic screens yielded most first-in-class
drugs 1999-2008).

**Natural products** — still produce ~ 30 % of new
small-molecule drugs.

## Stage 3 — Hit-to-lead

Take a screening hit + improve potency, selectivity,
solubility, ADME by ~ 100-1 000-fold.

Multi-parameter optimisation (MPO):
- **Potency** — IC50 / EC50 / K_d at target.
- **Selectivity** — vs related off-targets +
  anti-target panel (CYPs, hERG, kinome).
- **Solubility** + **permeability** (PAMPA, Caco-2).
- **Metabolic stability** (microsomes, hepatocytes).
- **CYP inhibition / induction** (DDI risk).
- **hERG inhibition** (cardiac safety).
- **Ames / micronucleus / chromosomal aberration**
  (genotoxicity).
- **In vivo PK** (rat + dog + monkey).
- **Behavioural / safety pharm** (CNS, cardiovascular,
  respiratory).

A typical hit-to-lead programme synthesises 100-1 000
analogues over 12-24 months.

## Stage 4 — Lead optimisation

Iterate to a clinical candidate meeting CCQ (clinical
candidate quality) criteria:
- Target potency low-nM.
- Selectivity > 100× vs off-targets.
- F (oral) > 30 %.
- t1/2 supporting once-daily or BID dosing.
- Clean tox panel.
- Preclinical efficacy in disease model.
- IP position (composition-of-matter patent).

Lead optimisation is the most resource-intensive
discovery stage — 24-48 months, 1 000-10 000
analogues, multiple sub-teams (chem, biology, DMPK,
tox, formulation).

## Stage 5 — Preclinical / IND-enabling

Once a clinical candidate is nominated, the IND
package requires:

- **GLP toxicology** in two species (typically rat +
  dog) — 14-day, 28-day, 90-day, chronic.
- **Reproductive toxicology** (DART — Developmental +
  Reproductive Tox).
- **Genotoxicity battery** (Ames + micronucleus +
  chromosomal aberration).
- **Safety pharmacology** — cardiovascular (hERG,
  telemetry), respiratory, CNS.
- **GLP pharmacokinetics** in tox species.
- **CMC** (chemistry, manufacturing, controls) —
  GMP synthesis route, stability, formulation.
- **Clinical protocol** + investigator brochure.

IND-enabling stage runs ~ 12-18 months, costs
$10-50 M, and ends with FDA / EMA / PMDA filing.

## Stage 6 — Phase 1

First-in-human studies.  Goals:
- **Safety** — adverse events, dose-limiting toxicity.
- **PK** — establish dose-PK relationship, half-life,
  food effect, drug-drug interactions.
- **PD biomarker engagement** when feasible.
- **MTD** (maximum tolerated dose) for cytotoxic
  oncology drugs.

Healthy volunteers for non-oncology drugs (~ 20-100
participants); patients for oncology (3+3 design or
modern model-based escalation like CRM / BOIN).

Duration ~ 1-2 years.  Successful → ~ 60 % advance to
Phase 2.

## Stage 7 — Phase 2

Proof of concept in patients.

- **Phase 2a** — small (~ 50-200) open-label dose-
  ranging in target population.
- **Phase 2b** — larger (~ 200-500) randomised
  controlled trial vs placebo / standard of care.

Goals: efficacy signal, dose-finding, expanded safety,
PK in patients (often very different from healthy
volunteers).

Duration 1-3 years.  Phase 2 → 3 attrition is high
(~ 40-50 % advance) — most clinical-attrition occurs
here on efficacy grounds.

## Stage 8 — Phase 3

Pivotal trials supporting registration.

- **Large** (~ 1 000-10 000+ patients).
- **Randomised, double-blind, controlled** (vs placebo
  or active comparator).
- **Multi-centre, often multi-national**.
- **Pre-specified primary efficacy endpoint** powered
  for statistical significance.
- **Adequate exposure** for safety (~ 1 500 patients
  for chronic-use registration).

Adaptive designs (interim analyses with stopping rules,
seamless Phase 2/3, basket / umbrella / platform trials)
are increasingly common.

Duration 2-5 years.  Phase 3 → approval ~ 60 %
advance.

## Stage 9 — Regulatory submission

Compile all evidence into a:
- **NDA** (New Drug Application — small molecules) or
  **BLA** (Biologics License Application — biologics)
  for FDA.
- **MAA** (Marketing Authorisation Application) for
  EMA.

Standard review ~ 10 months FDA; **Priority Review**
6 months for serious/life-threatening conditions.
Other expedited pathways:
- **Breakthrough Therapy** — substantial improvement
  over existing therapies.
- **Fast Track** — unmet medical need.
- **Accelerated Approval** — surrogate endpoint with
  post-market confirmation.
- **Orphan Drug Designation** — < 200 000 US patients.

## Stage 10 — Phase 4 / post-market

After approval:
- **Pharmacovigilance** — spontaneous adverse-event
  reporting (FAERS, EudraVigilance, Yellow Card).
- **Risk Evaluation + Mitigation Strategies (REMS)** —
  for drugs with serious safety concerns.
- **Required post-market trials** — confirmatory,
  paediatric, long-term safety.
- **Real-world evidence (RWE)** — registries, EHR
  studies, claims data.
- **Label expansion** trials for new indications.
- **Generic / biosimilar** competition after patent
  expiry → ~ 80-90 % price drops.

## Attrition data

Approximate clinical-attrition rates (Hay 2014 +
later updates):

- IND → Phase 1 : ~ 100 %.
- Phase 1 → Phase 2 : ~ 60 %.
- Phase 2 → Phase 3 : ~ 30 %.
- Phase 3 → NDA submission : ~ 60 %.
- NDA → approval : ~ 90 %.

Cumulative IND → approval : ~ 10-12 %.

Reasons for failure (BIO 2018 analysis):
- Phase 2 — efficacy ~ 50 %.
- Phase 3 — efficacy ~ 50 %.
- Across all phases — toxicity / safety ~ 25 %.
- Strategy / commercial ~ 15 %.

## Costs + economics

Tufts CSDD 2020:
- Per-approved-drug capitalised cost ~ $2.6 B.
- Includes failures + cost of capital.
- ~ $1.4 B out-of-pocket; ~ $1.2 B time-cost-of-capital
  (10.5 %).

DiMasi/Hansen + Joseph: out-of-pocket per approved
drug $314M (1991) → $802M (2003) → $1.4B (2014) →
expected to keep rising as easier targets are
exhausted + biologics demand expensive manufacturing.

Critics: industry cost numbers include rejected
candidates + cost of capital; actual marginal cost of
producing a new drug is much lower.  The DiMasi
methodology is still standard for industry +
regulatory discussion.

## Modern accelerators

- **AI / ML-driven design** — cuts hit-to-lead +
  lead-optimisation time-cost (Insilico Medicine,
  Recursion, BenevolentAI, Atomwise, Iktos, Cradle).
  First INSILICO-designed clinical candidate
  (INS018_055 for IPF) entered the clinic in 2023.
- **AlphaFold + ESM** for structure-based design
  without wet-lab structural biology.
- **Adaptive / platform trials** (RECOVERY, SOLIDARITY,
  I-SPY, BATTLE, Lung-MAP, GBM AGILE) compress
  Phase 2/3 timelines.
- **Real-world evidence** + **synthetic control arms**
  reduce trial size requirements.
- **Pragmatic trials** (PRECIS-2 framework) measure
  effectiveness in real-world settings.

## Modalities

Beyond traditional small molecules + biologics:
- **PROTACs / molecular glues** — induced protein
  degradation.
- **mRNA vaccines + therapeutics** (Moderna, BioNTech).
- **AAV gene therapy** (Spark Luxturna, Novartis
  Zolgensma, BioMarin Roctavian).
- **Lentiviral CAR-T** (Kymriah, Yescarta, Breyanzi,
  Carvykti).
- **CRISPR therapeutics** (Casgevy / exa-cel for
  sickle cell + β-thalassaemia, the first approved
  CRISPR drug, Dec 2023).
- **Base editors + prime editors** — early clinical
  (Verve VERVE-101 PCSK9 base editor, Beam BEAM-101,
  Prime Medicine PM359).
- **Antisense oligonucleotides** (nusinersen, milasen).
- **siRNA** (patisiran, lumasiran, inclisiran).
- **Engineered cell therapies** beyond CAR-T (TCR-T,
  TIL).

These modalities have different development paths —
shorter discovery (mRNA can be encoded in days), but
manufacturing + delivery + cost remain hurdles.

## Try it in the app

- **Window → Pharmacology Studio → Drug classes** —
  per-class entries note approval history + landmark
  trials.
- **Window → Pharmacology Studio → Receptors** —
  drug-target landscape across superfamilies.
- **Window → Biochem Studio → Enzymes** — many drug
  targets sit here (CYPs, kinases, proteases).

Next: **Biologics**.
