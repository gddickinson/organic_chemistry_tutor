# Pharmacodynamics

Pharmacodynamics (PD) is the quantitative description
of how drug concentration relates to drug effect.  It's
the mathematical bridge from molecule to clinical
outcome.

## The Emax model

The simplest + most-used PD model:

E = (Emax × C) / (EC50 + C)

where:
- E = effect at concentration C.
- Emax = maximal achievable effect.
- EC50 = concentration producing 50 % of Emax.

Mathematically identical to Michaelis-Menten.  Plot
E vs log(C) gives the classic sigmoidal log-dose-
response curve.

## The Hill equation

When the curve is steeper than the simple Emax model,
add a Hill coefficient n:

E = (Emax × C^n) / (EC50^n + C^n)

- **n = 1** — simple Emax / hyperbolic.
- **n > 1** — positive cooperativity (steep curve).
  Hemoglobin O2 binding n ≈ 2.7-3.
- **n < 1** — negative cooperativity (flat curve).

Steep dose-response (n > 4-5) often indicates
amplification through a downstream cascade or multiple
binding sites.

## Full vs partial agonism

In a tissue with receptor reserve:

- **Full agonist** — generates the maximal achievable
  response (Emax).  EC50 < K_d (occupies a fraction of
  receptors at maximal effect).
- **Partial agonist** — Emax less than the system
  maximum even at saturating concentration.  Tells you
  the drug has lower **intrinsic efficacy** at that
  receptor.

A partial agonist's effect depends on the system:
- Low agonist tone → partial agonist behaves AGONISTICALLY
  (contributes some response).
- High agonist tone → partial agonist behaves as a
  functional ANTAGONIST (it occupies receptors that
  would otherwise be activated by the full endogenous
  agonist).

Examples:
- **Buprenorphine** — partial μ-opioid; ceiling effect
  on respiratory depression; precipitates withdrawal in
  full-opioid-tolerant patients.
- **Aripiprazole** — partial D2 + 5-HT1A; "stabiliser"
  for bipolar / schizophrenia.
- **Pindolol** — β-adrenergic with intrinsic
  sympathomimetic activity (ISA).

## Occupancy theory + receptor reserve

Classic occupancy theory (Clark) assumed effect
proportional to fractional receptor occupancy.  Stephenson
(1956) + Furchgott (1966) extended it: many tissues
have **spare receptors**, so maximal effect occurs at
sub-saturating occupancy.

Implications:
- A fully-efficacious drug only needs to occupy a small
  fraction of receptors.
- Partial agonists' deficit is much more visible in
  tissues with low reserve.
- Receptor down-regulation (chronic agonist exposure)
  reduces reserve → partial agonists become less
  effective.

## Schild analysis — measuring competitive antagonism

Add a competitive antagonist + the agonist
dose-response curve right-shifts in parallel (Emax
unchanged, EC50 increases).

The **dose ratio (DR)** = EC50 with antagonist / EC50
without.

Schild equation: log(DR - 1) = log[B] - log K_B

A Schild plot of log(DR-1) vs log[B] gives:
- **Slope = 1** confirms simple competitive
  antagonism.
- **X-intercept = log K_B** is the dissociation
  constant of the antagonist (pK_B = -log K_B).

Slope ≠ 1 indicates non-competitive or allosteric
antagonism.

## Insurmountable + non-competitive antagonism

Non-competitive antagonists DEPRESS the agonist Emax —
no amount of agonist can restore the maximal response.
The dose-response curve flattens vertically rather
than right-shifting.

Causes:
- **Covalent binding** (phenoxybenzamine at α-adrenergic;
  aspirin at COX).
- **Allosteric inhibition** that prevents activation
  conformational change.
- **Channel-pore block** (ketamine in NMDA; QX-314 in
  Nav).
- **Cooperative dis-inhibition** of downstream amplifier.

## Inverse agonism

In systems with constitutive receptor activity, an
inverse agonist STABILISES THE INACTIVE STATE → reduces
basal signalling below the agonist-free baseline.

Many drugs originally classified as "antagonists" are
inverse agonists when measured carefully.  Clinical
relevance:
- Up-regulated β-adrenergic receptors in heart failure
  show constitutive activity; inverse agonists like
  bisoprolol may reduce the basal hyperactivity better
  than neutral antagonists.
- H2 inverse agonists (cimetidine, ranitidine) reduce
  basal acid secretion below stomach baseline.

## Allosteric modulation

Binding to a site distinct from the orthosteric ligand
binding site:

- **PAM (positive allosteric modulator)** — increases
  agonist affinity AND/OR efficacy.  No agonist = no
  PAM effect.  Examples:
  - **Benzodiazepines** at GABA_A — increase channel-
    opening frequency in response to GABA; ceiling on
    effect (vs barbiturates which directly open the
    channel + can produce respiratory arrest).
  - **Cinacalcet** at CaSR — sensitises parathyroid
    cells to extracellular Ca²⁺.
  - **Ivacaftor** at CFTR — restores gating in G551D
    mutant CFTR.
  - **Mavacamten** at cardiac myosin — for HCM.
- **NAM (negative allosteric modulator)** — reduces
  agonist effect.
- **Probe-dependent modulation** — some allosteric
  drugs modulate one orthosteric ligand differently
  from another (so PAM at one agonist, no effect at
  another; relevant for biased signalling).

## Therapeutic index + safety margins

Two metrics describe drug safety:

- **Therapeutic Index (TI)** = LD50 / ED50 (or TD50 / ED50
  in clinical use).
- **Therapeutic Window** — concentration range that's
  effective without toxicity.

Narrow-TI drugs (TI < 10):
- Warfarin, digoxin, lithium, phenytoin, carbamazepine,
  cyclosporine, tacrolimus, methotrexate, theophylline,
  aminoglycosides, vancomycin.

Wide-TI drugs (TI > 100):
- Most penicillins, amoxicillin, paracetamol (within
  therapeutic doses), most NSAIDs (within indication),
  most SSRIs.

Narrow-TI drugs typically warrant therapeutic drug
monitoring (TDM).

## Biased agonism + functional selectivity

A single receptor can engage multiple downstream
pathways (e.g. GPCR → G-protein vs β-arrestin).  Some
ligands preferentially activate one over the other —
"biased agonism".

Examples:
- **TRV130 (oliceridine)** — μ-opioid G-protein-biased;
  approved for IV pain with claimed reduced respiratory
  depression vs morphine (clinical magnitude debated).
- **β-arrestin-biased angiotensin** ligands explored
  for heart failure.
- **D2 partial-agonist + β-arrestin profile** matters
  for atypical antipsychotic effects vs side effects.

The field is mechanistically rich + clinically still
maturing.

## Drug synergy + antagonism (combinations)

Combination drug effects:
- **Additive** — combined effect = sum of individual.
- **Synergistic** — combined > sum (1 + 1 > 2).  Often
  exploited in antibiotics (β-lactam + aminoglycoside),
  anti-tuberculosis (RIPE), anti-cancer combinations.
- **Antagonistic** — combined < sum.  Sometimes
  harnessed therapeutically (naloxone reversal of
  opioids).

Quantitative methods: **isobolograms**, **Loewe
additivity**, **Bliss independence**, **Chou-Talalay
combination index**.

## How PK + PD combine

Clinical effect depends on whether the PK delivers a
concentration in the PD effect window for long enough.

- **PK/PD efficacy index** for antibiotics:
  - Time > MIC for β-lactams (= dosing-interval design).
  - Cmax/MIC for aminoglycosides (high peak, long
    interval).
  - AUC/MIC for vancomycin + fluoroquinolones (24-h
    exposure matters).
- **Hysteresis** — when effect peaks AFTER concentration
  due to delayed equilibration into effect compartment
  (digoxin, warfarin, β-blockers in heart failure).
- **Tolerance / desensitisation** — chronic exposure
  reduces effect for the same concentration.

## Try it in the app

- **Window → Pharmacology Studio → Receptors** —
  per-receptor agonist + antagonist + allosteric
  modulator examples.
- **Window → Cell Biology Studio → Signalling** —
  downstream pathway context for receptor activation.
- **OrgChem → Tools → Drug-likeness** — physicochemical
  properties drive PK that supports a PD profile.

Next: **Dose-response in practice**.
