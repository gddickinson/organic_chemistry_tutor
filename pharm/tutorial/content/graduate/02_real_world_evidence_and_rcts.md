# Real-world evidence + RCTs

The randomised controlled trial (RCT) remains the
gold standard for establishing efficacy + safety.
Real-world evidence (RWE) — from EHRs, claims,
registries, wearables, patient-reported outcomes —
is increasingly accepted by regulators alongside RCT
data.  Modern pharmacology must navigate both.

## Why RCTs

The randomisation guarantees:
- Treatment + control groups balanced on observed +
  unobserved confounders (in expectation).
- Causal inference is valid without strong modelling
  assumptions.

Blinding (single, double, triple) controls for
placebo + nocebo effects + observer bias.  Pre-
specified primary endpoint + power analysis prevent
post-hoc cherry-picking.

The hierarchy of evidence (informally):
1. Systematic review + meta-analysis of RCTs.
2. Single well-powered RCT.
3. Observational cohort.
4. Case-control.
5. Case series + case reports.
6. Expert opinion.

## RCT design vocabulary

### Phase classifications

Already covered in the development-pipeline lesson.
Phase 4 = post-marketing surveillance + label
expansion + comparative effectiveness.

### Randomisation strategies

- **Simple randomisation** — coin flip.  Risk of
  imbalance in small trials.
- **Block randomisation** — e.g. blocks of 4 (AABB,
  ABAB, ABBA, BABA, BAAB, BBAA).  Maintains
  approximately equal arm sizes.
- **Stratified randomisation** — randomise within
  pre-specified strata (centre, age band, biomarker
  status).  Improves power + balance for important
  prognostic factors.
- **Adaptive randomisation** — allocation ratio shifts
  during trial in response to interim results
  (response-adaptive, covariate-adaptive).
  Controversial — preserves valid inference only with
  careful design.

### Blinding

- **Open-label** — both parties know the assignment.
  Survival oncology trials are sometimes open-label
  for ethical reasons.
- **Single-blind** — patient blinded.
- **Double-blind** — patient + investigator blinded.
- **Triple-blind** — patient + investigator + outcome
  assessor blinded.

Blinding becomes harder with biologics (subcutaneous
sites, infusion reactions) — sham injections + active
comparators help.

### Endpoint hierarchy

- **Hard clinical endpoints** — all-cause mortality,
  hospitalisation, MACE (major adverse cardiovascular
  events).  Largest, longest, most-expensive trials;
  most-credible.
- **Composite endpoints** — combinations (MACE = CV
  death + MI + stroke + revascularisation).  Smaller
  trials but interpretation needs care.
- **Surrogate endpoints** — biomarkers (HbA1c,
  LDL, BP, viral load, tumour response).  Faster +
  smaller trials but require validation that surrogate
  changes track clinical-outcome changes.
- **Patient-reported outcomes (PROs)** — symptoms,
  HRQoL, function.  Increasingly required by
  regulators + payers.

### Trial designs

- **Parallel groups** — most common; randomise to
  one of N arms, follow forward.
- **Crossover** — each patient receives all
  treatments in randomised sequence.  Powerful
  (each patient is own control) but only valid for
  conditions that don't change between periods +
  drugs without carry-over.
- **Factorial** — 2 × 2 (or larger) — test multiple
  interventions in one trial.  PHS (aspirin × β-
  carotene), HOPE (ramipril × vitamin E).
- **Cluster** — randomise groups (clinics, schools,
  villages) instead of individuals.  Used for
  vaccines (RTS,S malaria), infection-control
  interventions, public-health programmes.
- **Adaptive** — interim analyses + pre-specified
  modifications (drop arms, add arms, sample-size
  reassessment).
- **Platform / basket / umbrella** —
  - **Platform** trials test multiple agents against
    a control over time, with arms added + dropped
    (RECOVERY for COVID-19, GBM AGILE, I-SPY).
  - **Basket** — one biomarker, multiple cancer types
    (e.g. larotrectinib for NTRK-fusion across all
    histologies).
  - **Umbrella** — one cancer type, multiple
    biomarker-defined arms (Lung-MAP, BATTLE).
- **N-of-1** — single-patient crossover; growing for
  rare diseases + personalised therapeutics.

### Statistical analysis

- **Intention-to-treat (ITT)** — analyse all
  randomised participants in their assigned arm,
  regardless of compliance.  Preserves randomisation;
  conservative.
- **Per-protocol** — only those completing assigned
  treatment.  Risks bias from non-random drop-out.
- **As-treated** — analyse by what was actually
  received.  Useful for safety analyses.

ITT for primary efficacy + per-protocol as
sensitivity analysis is standard.

- **Multiplicity adjustment** — for multiple primary
  endpoints, secondary endpoints, interim analyses.
  Bonferroni, Holm, Hochberg, gatekeeping
  hierarchies.
- **Pre-specification** — protocol locked + filed
  before unblinding.  Critical to avoid HARKing
  (hypothesising after results known).
- **Bayesian methods** — increasingly used in early-
  phase + adaptive designs.  Posterior probabilities
  of efficacy + futility decisions.

## Real-world evidence (RWE)

The 21st Century Cures Act (2016) + FDA RWE Framework
(2018) explicitly included RWE in regulatory
decision-making.  Sources:

- **Electronic health records (EHRs)** — Optum, IQVIA,
  Truveta.
- **Claims data** — Medicare, Medicaid, commercial
  payers (Marketscan, Optum Clinformatics).
- **Disease registries** — SEER (cancer), TriNetX
  (cardiology), AHA Get-With-The-Guidelines.
- **Patient-generated data** — wearables (Apple
  Watch, Fitbit), mobile apps, ePROs.
- **Pragmatic clinical trials** — real-world settings,
  routine care, simpler eligibility.
- **Literature** — systematic review of publications.

### When RWE adds most value

- **Long-term safety** — rare adverse events, late
  effects.
- **Comparative effectiveness** between approved
  drugs.
- **Sub-population effects** under-represented in
  RCTs (elderly, paediatric, multi-morbid).
- **Treatment patterns** + adherence + persistence.
- **Regulatory pathway support** for rare diseases
  (small RCTs supplemented by registry data).
- **Synthetic control arms** — historical / external
  controls instead of randomising new patients (used
  for ultra-rare or ethically-difficult settings).

### When RWE struggles

- **Confounding by indication** — sicker patients get
  different treatments; observational designs need
  causal-inference methods (propensity scores,
  instrumental variables, target trial emulation).
- **Missing data** + measurement error — EHRs ARE
  not designed for research.
- **Selection bias** — patient populations differ
  across data sources.
- **Time-zero ambiguity** — when does follow-up
  start in observational data?

## Causal inference toolkit

For drawing causal conclusions from observational
data:

- **Propensity score matching / weighting** —
  estimate probability of treatment given covariates,
  match or weight to balance arms.
- **Inverse probability of treatment weighting (IPTW)**
  — re-weight observational data to mimic randomisation.
- **Instrumental variables** — exploit a randomly-
  varying determinant of treatment that doesn't
  affect outcome directly.
- **Difference-in-differences** — exploit
  policy / time changes.
- **Regression discontinuity** — exploit threshold-
  based assignment.
- **Target trial emulation** — frame an observational
  analysis to mimic a hypothetical RCT (Hernán +
  Robins).
- **Doubly robust + machine-learning estimators** —
  TMLE, AIPW, double-ML.

## FDA Sentinel + active surveillance

The FDA Sentinel System (launched 2008, fully
operational 2016) is a distributed-data network
monitoring drug safety in > 100 M patients across
US payers + EHRs.

Use cases:
- **Mini-Sentinel** rapid signal evaluation —
  rofecoxib analyses in retrospect, rivaroxaban
  bleeding signal validation, COVID-19 vaccine
  safety.
- **Modular programme** queries — pre-specified
  analytics on standardised data.
- **Active surveillance** of high-impact safety
  questions vs reactive spontaneous-report mining
  (FAERS).

Other systems: EU's EMA-DARWIN, UK's Yellow Card
Centre + CPRD, Sentinel-equivalent national
networks in Asia.

## Pragmatic vs explanatory trials

The PRECIS-2 framework characterises trials along 9
domains from "explanatory" (highly-controlled,
homogeneous, optimised) to "pragmatic" (real-world,
broad eligibility, routine care).

- **Explanatory** — efficacy under ideal conditions.
  Phase 3 registration trials are mostly explanatory.
- **Pragmatic** — effectiveness in real practice.
  Better for payer + clinical-guideline decisions.
- **Hybrid** — explanatory primary + pragmatic
  secondary endpoints.

The SPRINT, RECOVERY, ASPREE, ISCHEMIA, REDUCE-IT,
SCORED, EMPEROR-Preserved trials illustrate large
pragmatic / semi-pragmatic designs that have shaped
recent practice.

## Decentralised + virtual trials

Accelerated by COVID-19:
- **Direct-to-patient drug shipping**.
- **Telemedicine visits**.
- **Wearable + mobile-app data collection**.
- **eConsent**.
- **Local lab / imaging at community providers**.

Reduces patient burden + improves recruitment +
expands geographic reach.  Standard for some studies
now (Apple Heart Study, Walmart Trial Connect).

## Regulatory trends

- **FDA + EMA** publishing guidance on RWE,
  decentralised trials, master protocols.
- **Accelerated approval** based on surrogate
  endpoints (with required confirmatory trials —
  some have failed, e.g. aducanumab; Project Confirm
  is FDA's response).
- **ICH harmonisation** (E6(R3) GCP revision, E20
  Adaptive Designs guideline).
- **Patient-focused drug development (PFDD)** —
  formal patient input into outcomes that matter.
- **Risk-based monitoring** (RBM) replacing 100 %
  source-data verification.

## Worked example — semaglutide

Semaglutide has the canonical post-modern evidence
package:

- **Phase 3 (SUSTAIN, PIONEER series)** — registration
  RCTs for T2DM glycaemic control.
- **Phase 3 (STEP series)** — registration RCTs for
  obesity (semaglutide 2.4 mg).
- **Phase 3 (SELECT)** — large CV-outcomes RCT in
  obesity without diabetes; 20 % MACE reduction;
  underpinned label expansion.
- **Phase 3 (FLOW)** — kidney outcomes in T2DM with
  CKD.
- **Real-world evidence** — TriNetX + Optum studies
  comparing semaglutide vs other GLP-1s + insulin.
- **Pharmacovigilance** — pancreatitis, gallbladder,
  thyroid C-cell signals continuously monitored.

Modern drugs ship with hundreds of thousands of
patient-years of evidence; the line between RCT +
RWE blurs continuously.

## Try it in the app

- **Window → Pharmacology Studio → Drug classes** —
  per-class entries note landmark RCTs +
  comparative-effectiveness data.
- **Window → Pharmacology Studio → Drug development
  / RCT bridges** (per-class).

Next: **Modern modalities**.
