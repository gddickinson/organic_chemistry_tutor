# Dose-response in practice

How clinicians + pharmacologists use the
dose-response concept to guide dosing, predict
toxicity, and quantify drug interactions.

## The three classical curves

### Quantal dose-response

Measures the FRACTION of a population producing a
specified all-or-nothing response at each dose.  The
curve looks sigmoidal because individuals vary in
sensitivity.

- **ED50** — dose effective in 50 % of population.
- **TD50** — dose toxic in 50 %.
- **LD50** — dose lethal in 50 % (animal studies; not
  measured in humans).

Quantal curves underlie regulatory dose-finding +
population dosing.

### Graded dose-response

Measures the MAGNITUDE of a continuous response (BP,
heart rate, blood glucose, FEV1) in a single
individual / preparation across doses.

The Emax model of the previous lesson applies.
EC50 is a graded-curve concept; ED50 is a quantal-curve
concept — easy to confuse.

### Time-action

Plots effect vs time after a single dose.  Captures:
- Onset of action.
- Peak effect.
- Duration of action.
- Time to baseline.

For PK-driven drugs, the curve mirrors the plasma
concentration profile; for drugs with hysteresis or
covalent action it doesn't (warfarin's anticoagulant
effect lags concentration by 24-72 h because clotting
factors must turn over).

## Therapeutic index — clinical vs preclinical

- **Preclinical**: TI = LD50 / ED50 in animals.
- **Clinical**: TI = TD50 / ED50 in patients (or
  TD1 / ED99 for a more conservative "margin of
  safety").

Useful clinical thresholds:
- TI > 100 — wide window, safe.
- TI 10-100 — moderate; routine clinical use without
  TDM.
- TI 2-10 — narrow; consider TDM, individualised
  dosing.
- TI < 2 — extreme caution; mandatory TDM.

Examples of narrow-TI drugs requiring TDM:
- Warfarin (INR).
- Phenytoin (10-20 mg/L).
- Lithium (0.6-1.2 mEq/L).
- Digoxin (0.5-2.0 ng/mL).
- Aminoglycosides (peak + trough).
- Vancomycin (AUC24/MIC or trough).
- Cyclosporine, tacrolimus, sirolimus (immunosuppressants).
- Methotrexate (high-dose with leucovorin rescue).
- Theophylline (5-15 mg/L).

## Parallel-shift competitive antagonism

A competitive antagonist right-shifts the agonist
dose-response curve in parallel — Emax preserved,
EC50 increased.

This is the **classical signature of competitive
antagonism**.  It assumes:
- Antagonist + agonist compete for the same site.
- Equilibrium is achieved at each concentration.
- Both bind reversibly.

Real-world deviations:
- **Slow-binding antagonists** — kinetics don't reach
  equilibrium → curves don't perfectly parallel-shift.
- **Hemi-equilibrium** — fast agonist + slow
  antagonist gives intermediate behaviour.
- **Operational receptor reserve** changes the
  relationship between occupancy + effect →
  shifts may not be purely "parallel".

## Schild analysis — the practical pK_B method

Procedure:
1. Measure agonist EC50 in absence of antagonist
   (control).
2. Measure agonist EC50 in presence of multiple
   concentrations of antagonist.
3. Compute dose ratios (DR) at each antagonist
   concentration.
4. Plot log(DR - 1) vs log[B].
5. Slope should be 1.0 (significantly different from
   1.0 indicates non-competitive behaviour).
6. X-intercept gives pA2 = -log K_B (the negative log
   of the antagonist's dissociation constant).

pA2 values are tabulated for many drug-receptor pairs
+ used to compare competitive antagonists across
laboratories.

## Operational model (Black + Leff)

A more general model than Schild that handles partial
agonists + receptor reserve:

E = (Emax × [A]^n × τ^n) / ((K_A + [A])^n + [A]^n × τ^n)

where τ = transducer ratio (intrinsic efficacy +
receptor density), K_A = agonist dissociation constant.

Used in modern pharmacology to:
- Quantify intrinsic efficacy.
- Calculate equiactive concentrations across tissues.
- Assess biased agonism (compute τ for each downstream
  pathway separately).

## Dose-titration in clinical practice

Most drugs are dose-titrated to clinical effect rather
than fixed-dose:

- **Antihypertensives** — titrate to BP target.
- **Antidiabetics** — titrate to HbA1c target.
- **Anticoagulants** — titrate to INR (warfarin) or
  fixed for DOACs.
- **Anti-epileptics** — titrate to seizure freedom +
  drug levels.
- **Opioids** — titrate to pain relief, watching
  respiratory rate + sedation.
- **Levothyroxine** — titrate to TSH.

Titration philosophy:
- **Start low, go slow** in elderly + frail.
- **Wait 4-5 half-lives** between dose changes for
  steady-state assessment.
- **Therapeutic drug monitoring** for narrow-TI drugs.
- **Symptom diary** + **patient-reported outcomes** as
  part of titration.

## Population PK + Bayesian dose individualisation

Modern dosing increasingly uses **population PK
models** (NONMEM-fitted) + **Bayesian forecasting**:

1. Historical data fit a population PK model with
   covariate effects (age, weight, GFR, genotype).
2. Initial dose chosen from population priors +
   patient-specific covariates.
3. Measure concentration after dose.
4. Bayesian update produces posterior estimate of
   individual PK parameters.
5. Refine dose using individualised model.

Standard for vancomycin AUC-targeted dosing,
aminoglycosides, anti-rejection drugs.

## Combination therapy — synergy + isobolograms

When two drugs are combined, three patterns:
- **Additive** — combined effect = sum of individual.
- **Synergistic** — combined > additive.
- **Antagonistic** — combined < additive.

Quantification:
- **Isobologram** — plot iso-effect contours in 2-drug
  concentration space.  A straight line = additive;
  bowed toward origin = synergistic; bowed away =
  antagonistic.
- **Bliss independence** — assumes drugs act on
  independent targets.
- **Loewe additivity** — assumes drugs are
  pharmacologically equivalent at the target.
- **Chou-Talalay combination index (CI)** —
  quantitative metric where CI < 1 = synergy,
  CI = 1 additive, CI > 1 antagonism.

Clinically harnessed:
- **β-lactam + aminoglycoside** for endocarditis
  (additive cell-wall inhibition + protein synthesis
  blockade with synergy).
- **Sulfamethoxazole + trimethoprim (Bactrim)** —
  sequential block of folate synthesis.
- **HAART** — 3-drug combination delays HIV resistance.
- **Cancer combinations** — most regimens designed
  for non-overlapping toxicities + presumed synergy.

## Drug-target engagement biomarkers

Modern PD includes target-engagement readouts:
- **Functional biomarker** — INR for warfarin, glucose
  for insulin, PR interval for digoxin.
- **Target-occupancy biomarker** — PET imaging of
  receptor occupancy (SSRIs at SERT; antipsychotics at
  D2; anti-amyloid mAbs).
- **Pathway biomarker** — ERK phosphorylation for MEK
  inhibitors; HbA1c for chronic glycaemic control.
- **Disease biomarker** — viral load for antivirals,
  CRP for biologics.

A drug development programme often demands
target-engagement evidence in early-phase trials before
proceeding to costlier efficacy studies.

## Try it in the app

- **Window → Pharmacology Studio → Drug classes** —
  per-class therapeutic index + monitoring notes.
- **Window → Pharmacology Studio → Receptors** —
  drug-target engagement context.
- **OrgChem → Tools → Drug-likeness** — predicted PK
  properties as input for PD considerations.

Next: **Drug-drug interactions**.
