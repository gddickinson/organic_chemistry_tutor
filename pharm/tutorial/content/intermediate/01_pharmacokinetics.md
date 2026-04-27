# Pharmacokinetics

Pharmacokinetics (PK) describes the time course of
drug concentrations in the body — what the BODY does to
the DRUG.  Four processes — Absorption, Distribution,
Metabolism, Excretion — collectively **ADME**.  PK
links a dosing regimen to the concentration that
actually reaches the drug's target.

## Absorption

How drug crosses biological membranes from the
administration site into systemic circulation.

Key determinants:
- **Lipophilicity** (logP) — higher lipophilicity =
  better passive transcellular crossing.
- **Ionisation** at the relevant pH — only the unionised
  form crosses membranes (Henderson-Hasselbalch).
- **Molecular size** — < 500 Da passes more readily.
- **Hydrogen-bond donor / acceptor counts** — Lipinski's
  rule of 5 set practical thresholds.
- **Active transport** — drugs that hijack OATP / OCT /
  PEPT1 / etc. (e.g. valacyclovir uses PEPT1, gabapentin
  uses LAT1).
- **First-pass metabolism** — covered in the
  Routes-of-administration lesson.

The fraction reaching systemic circulation is the
**bioavailability F**.  F = 1.0 IV; usually 0.05-1.0 for
oral.

## Distribution

How drug spreads from blood into tissues.  Determined
by:

- **Plasma protein binding** — bound drug is
  pharmacologically inactive.  Albumin binds acids;
  α1-acid glycoprotein binds bases.  Highly-bound
  drugs include warfarin (99 % bound), phenytoin
  (90 %), valproate (90 %), ibuprofen (99 %), naproxen
  (99 %).
- **Tissue binding** — some drugs concentrate in
  specific tissues (chloroquine 1 000× in lysosomes;
  amiodarone in lung + adipose; aminoglycosides in
  renal cortex).
- **Blood-brain barrier** — restricts CNS access;
  P-gp + BCRP actively pump drugs OUT.
- **Placental crossing** — small lipophilic drugs cross
  freely (alcohol, opioids, valproate).  Most teratogens
  are placentally accessible.
- **Body composition** — total body water (TBW),
  extracellular fluid (ECF), fat content.  Lithium
  distributes only in TBW; warfarin in ECF; digoxin
  in muscle + Na+/K+-ATPase pool; benzodiazepines in
  fat.

### Volume of distribution (Vd)

A theoretical concept: the volume of a single
homogeneous compartment that would contain the total
body drug at the plasma concentration.

Vd = Total body amount of drug / Plasma concentration

| Drug | Vd | Compartment proxy |
|------|----|-------------------|
| Warfarin | 8 L | Plasma + albumin-bound |
| Aminoglycosides | 18 L | Extracellular fluid |
| Phenytoin | 50 L | Total body water |
| Digoxin | 500 L | Tissue-bound (Na+/K+-ATPase) |
| Chloroquine | 13 000 L | Concentrated in lysosomes |
| Amiodarone | 5 000 L | Adipose + lung |

A 70-kg adult has only ~ 42 L of total body water +
~ 5 L of plasma — large Vd values (digoxin 500 L;
chloroquine 13 000 L) reflect intense tissue binding,
not volumetric reality.

Loading-dose calculation: Loading dose = Vd × target
plasma concentration.

## Metabolism

Covered in detail in the BC-3.0 advanced lesson "Drug
metabolism enzymology".  Briefly:

- **Phase I** (functionalisation) — CYP P450s
  introduce / unmask -OH, -NH2, -COOH.
- **Phase II** (conjugation) — UGT, SULT, GST, NAT
  attach hydrophilic conjugates.
- **Phase III** (efflux) — P-gp, BCRP, OATPs move
  drugs + metabolites.

### Hepatic clearance

CL_hepatic = Q_H · E_H

where Q_H = hepatic blood flow (~ 1.5 L/min) and E_H =
extraction ratio (0-1).

- **High-extraction** (E > 0.7) — clearance is
  flow-limited.  Propranolol, lidocaine, morphine,
  verapamil.  Liver disease + reduced flow → big
  changes; enzyme inhibition has small marginal effect.
- **Low-extraction** (E < 0.3) — clearance is enzyme-
  limited.  Diazepam, phenytoin, warfarin.  Enzyme
  induction / inhibition matters most; flow changes
  matter little.

## Excretion

Routes:
- **Renal** — most drugs + metabolites; glomerular
  filtration + active tubular secretion.
- **Biliary / fecal** — bulky lipophilic drugs +
  conjugates (statins, oral contraceptives, doxorubicin).
- **Pulmonary** — volatile anaesthetics, alcohol.
- **Sweat / saliva / breast milk** — minor for most
  drugs.

### Renal clearance

CL_renal = (GFR × f_u) + tubular secretion - tubular reabsorption

GFR ≈ 90-120 mL/min in healthy adults.  f_u = unbound
fraction.  Drugs that are renally cleared are
particularly affected by chronic kidney disease — dose
adjustment by GFR / Cockcroft-Gault / CKD-EPI is
standard.

Drugs requiring renal-impairment dose adjustment:
- Aminoglycosides (gentamicin, vancomycin).
- DOACs (rivaroxaban, apixaban, dabigatran).
- Many antibiotics (β-lactams, fluoroquinolones).
- Lithium.
- Digoxin.
- Opioid metabolites (morphine-6-glucuronide accumulates
  in CKD, prolonged sedation).

## Half-life (t1/2)

Time for plasma concentration to fall by 50 %.

For a one-compartment model with first-order kinetics:

t1/2 = (ln 2 × Vd) / CL = 0.693 × Vd / CL

Half-life governs:
- **Time to steady state** — 4-5 half-lives of regular
  dosing.
- **Dosing interval** — drugs with long t1/2 can be
  dosed less often.
- **Time to washout** — 4-5 half-lives after
  discontinuation.

| Drug | t1/2 | Notes |
|------|------|-------|
| Esmolol | 9 min | Ultra-short β-blocker |
| Adenosine | 10 sec | Diagnostic SVT termination |
| Aspirin | 0.4 h (parent), 2-3 h (salicylate) | Active metabolite |
| Ibuprofen | 2 h | TID dosing |
| Warfarin | 36-42 h | Slow loading; once-daily |
| Diazepam | 20-50 h (parent), > 100 h (active metabolites) | Cumulation in elderly |
| Amiodarone | 25-100 days | Tissue accumulation |
| Fluoxetine | 1-4 days; norfluoxetine 7-15 days | Active metabolite |

## One-compartment model

The simplest PK model: the body is a single
well-mixed volume with first-order elimination.

After IV bolus: C(t) = C_0 · exp(-k_e · t),
where C_0 = Dose / Vd and k_e = CL / Vd = ln 2 / t1/2.

For an infusion at rate R: C(t) = (R / CL) · (1 -
exp(-k_e · t)).  Steady-state C_ss = R / CL —
independent of Vd.

Multi-compartment models (two-compartment, three-
compartment) are needed when drugs distribute slowly
(e.g. lipophilic drugs into peripheral fat) or when
high-frequency sampling reveals biphasic decay.

## Steady-state principle

For repeated dosing with interval τ + dose D:
- C_ss_avg = (F × D / τ) / CL
- C_ss_max ≈ C_ss_avg + (D × F) / (2 × Vd)
- C_ss_min ≈ C_ss_avg - (D × F) / (2 × Vd)

Average steady-state concentration depends on dose,
interval, F + CL — NOT on Vd directly.  Vd determines
peak-trough fluctuation amplitude.

## Loading dose vs maintenance dose

- **Loading dose** rapidly achieves target concentration:
  Loading = Vd × target × (1 / F)
- **Maintenance dose** sustains it:
  Maintenance = CL × target × τ × (1 / F)

Used routinely for amiodarone, digoxin, antibiotics
with narrow therapeutic windows + drugs with long t1/2
where waiting 4-5 half-lives is impractical.

## Linear vs nonlinear PK

Most drugs exhibit linear (first-order) PK at
therapeutic doses — concentration scales with dose.
Some show **saturable** (Michaelis-Menten) kinetics:

- **Phenytoin** — CYP saturation in the therapeutic
  range; small dose changes cause big concentration
  changes.
- **Ethanol** — ADH saturation at ~ 0.1 g/L; zero-order
  elimination at typical intoxication levels.
- **Aspirin** — saturation of conjugation pathways at
  high doses.
- **Theophylline** — Km close to therapeutic range.

Saturable PK is a clinical-monitoring + dose-adjustment
nightmare; therapeutic drug monitoring (TDM) is often
mandatory.

## Special populations

- **Paediatrics** — neonates have immature CYP / UGT;
  CL/kg generally LOW in neonates, HIGH in toddlers
  (relative to adults), then declines.
- **Geriatrics** — declining GFR, reduced lean body
  mass, polypharmacy, pharmacodynamic sensitivity.
- **Pregnancy** — increased Vd, increased GFR (~ 50 %
  by 3rd trimester), induction of some CYPs.
- **Obesity** — Vd increases for lipophilic drugs;
  use ABW or AdjBW for loading-dose calculations.
- **Hepatic / renal impairment** — Child-Pugh +
  estimated GFR drive dose adjustment.

## Try it in the app

- **OrgChem → Tools → Drug-likeness** — Lipinski +
  Veber for absorption potential.
- **Window → Biochem Studio → Enzymes** — the major
  CYPs (`cyp3a4`, `cyp2d6`, `cyp2c9`, `cyp2c19`,
  `cyp1a2`, `cyp2e1`) for hepatic-metabolism context.
- **Window → Pharmacology Studio → Drug classes** —
  per-class entries note typical PK profile.

Next: **Pharmacodynamics**.
