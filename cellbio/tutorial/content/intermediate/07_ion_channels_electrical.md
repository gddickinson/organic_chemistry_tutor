# Ion channels + electrical signalling

Cells maintain ionic gradients across membranes,
and they exploit those gradients via ion channels
to generate + transmit electrical signals.  This
underlies neuronal firing, cardiac contraction,
muscle physiology, sensory transduction,
endocrine secretion, and many cellular signalling
events.

## The ionic environment

Typical mammalian cell:

| Ion | Inside (mM) | Outside (mM) | Equilibrium potential (E_X) |
|-----|-------------|--------------|------------------------------|
| K⁺ | 140 | 5 | ~ -90 mV |
| Na⁺ | 12 | 145 | ~ +66 mV |
| Cl⁻ | 5-10 | 100 | ~ -80 to -65 mV |
| Ca²⁺ | 0.0001 (cytosol; mM in ER) | 1-2 | ~ +120 mV |
| Mg²⁺ | 0.5 | 1.5 | small |
| H⁺ | pH 7.2 (cytosol) | pH 7.4 | ~ -10 mV |

Resting membrane potential ~ -60 to -90 mV (mostly
K⁺-dominated due to high resting K⁺ permeability
via leak channels).

## Channel categories

### By gating mechanism

- **Voltage-gated** — open / close in response to
  membrane potential.
- **Ligand-gated** — open in response to
  neurotransmitter or other small-molecule
  binding (extra- or intracellular).
- **Mechanically-gated** — respond to membrane
  stretch / tension (Piezo, TRPC, K2P).
- **Temperature-gated** — TRPV1 (heat / capsaicin),
  TRPM8 (cold / menthol).
- **Constitutively open (leak)** — set baseline
  permeability.

### By selectivity

- **K⁺-selective** — selectivity filter (TVGYG)
  permits K⁺ but not Na⁺ via dehydration energetics.
- **Na⁺-selective** — DEKA selectivity filter; smaller
  pore.
- **Ca²⁺-selective** — TVGD or EEEE filters; high
  Ca²⁺ selectivity.
- **Cl⁻-selective** — different topology + filter
  geometry (CLC family).
- **Non-selective cation channels** — TRP, CNG,
  HCN.

## Voltage-gated channels

### Voltage sensing

- All Cav, Nav, Kv channels share a 6-transmembrane-
  segment (S1-S6) architecture.
- S4 carries positive charges (Arg / Lys) +
  moves outward in response to depolarisation
  → opens the channel via S4-S5 linker
  coupling to the gate (S6 bundle crossing).

### Sodium channels (Nav)

- Nav1.1-1.9; tissue-specific:
  - Nav1.1, 1.2, 1.6 — CNS.
  - Nav1.4 — skeletal muscle.
  - Nav1.5 — cardiac.
  - Nav1.7, 1.8, 1.9 — peripheral / pain neurons.
- Fast inactivation via "hinge-lid" IFM motif on
  intracellular linker between domains III + IV.
- Targeted by:
  - Local anaesthetics (lidocaine, bupivacaine,
    ropivacaine, prilocaine, mepivacaine).
  - Class IB / IC antiarrhythmics (flecainide,
    propafenone, lidocaine IV).
  - Anticonvulsants (phenytoin, carbamazepine,
    lamotrigine, lacosamide).
  - Tetrodotoxin (TTX) — TTX-sensitive vs
    TTX-resistant subtype distinction.
- Channelopathies: SCN1A mutations cause Dravet
  + GEFS+; SCN5A → Brugada / Long QT 3 / SSS;
  SCN9A → erythromelalgia (gain-of-fxn) or pain
  insensitivity (loss-of-fxn).

### Calcium channels (Cav)

- L-type (Cav1.1-1.4) — long-lasting; cardiac +
  skeletal muscle excitation-contraction coupling
  + endocrine.  DHP receptors (nifedipine,
  amlodipine target).
- N-type (Cav2.2) + P/Q-type (Cav2.1) + R-type
  (Cav2.3) — neuronal; neurotransmitter release.
  Ziconotide (cone-snail-derived) blocks N-type
  for chronic pain.
- T-type (Cav3.1-3.3) — transient, low-voltage-
  activated; pacemaker activity.  Ethosuximide
  for absence seizures.
- Channelopathies: CACNA1A (familial hemiplegic
  migraine + episodic ataxia type 2 + SCA6);
  CACNA1S (hypokalaemic periodic paralysis);
  CACNA1C (Long QT 8 / Timothy syndrome).

### Potassium channels (Kv)

- Largest channel family; > 80 K⁺ channel genes
  in humans.
- Kv1-12 voltage-gated; many roles in
  repolarisation.
- **HERG (Kv11.1, encoded by KCNH2)** — cardiac
  rapid delayed-rectifier; mutations cause
  Long QT 2; off-target binding by many
  drugs causes acquired Long QT (a major drug-
  development concern).
- **KCNQ family** — slow delayed-rectifier;
  KCNQ1 (Long QT 1), KCNQ2/3 (BFNS).
- **Inward-rectifier Kir** — including KATP
  (β-cell insulin secretion target — sulfonyl-
  ureas; cardiac-protection target).
- **Two-pore domain K2P (TASK, TREK, TWIK,
  TRAAK)** — set resting membrane potential;
  modulated by stretch + pH + temperature +
  anaesthetics.

### Pacemaker (HCN) channels

- HCN1-4 — hyperpolarisation-activated,
  cyclic-nucleotide-gated.
- "Funny current (If)" in cardiac SA node →
  rate setter.  Ivabradine — selective HCN
  blocker, reduces heart rate without
  inotropic effect (heart failure +
  inappropriate sinus tachycardia).

## Action potentials

### Neuronal (HH model)

1. **Resting** ~ -70 mV; K⁺ leaks set baseline.
2. **Depolarisation** to threshold (~ -55 mV)
   triggers Nav opening.
3. **Upstroke** — Nav opens fully → Na⁺ influx
   → depolarisation toward E_Na (+30 to +40 mV).
4. **Repolarisation** — Nav rapidly inactivates;
   Kv opens → K⁺ efflux → membrane returns to
   negative.
5. **Hyperpolarisation** — slow K⁺ closure +
   continued K⁺ flow → undershoot below resting.
6. **Refractory period** — Nav must recover from
   inactivation before another AP can fire.

Hodgkin-Huxley 1952 model + Nobel 1963.

### Cardiac action potential

Multiple specialised flavours:

- **Ventricular myocyte (rapid response)**:
  - Phase 0 — Na⁺ upstroke (Nav1.5).
  - Phase 1 — early repol (Ito, transient outward
    K⁺).
  - Phase 2 — plateau (L-type Ca²⁺ in vs
    delayed-rectifier K⁺ out balance).
  - Phase 3 — repol (IKr — HERG, IKs — KCNQ1,
    IK1 — Kir2).
  - Phase 4 — diastolic (IK1 stable resting).

- **SA node + AV node (slow response)**:
  - Phase 4 — funny current (HCN, If) drives
    spontaneous depolarisation.
  - Phase 0 — slow upstroke via L-type Ca²⁺.
  - Phase 3 — repol via delayed rectifier.

Drugs (Vaughan Williams classification):
- Class I — Na⁺ channel blockers (Ia: quinidine,
  procainamide; Ib: lidocaine, mexiletine; Ic:
  flecainide, propafenone).
- Class II — β-blockers (atenolol, metoprolol,
  propranolol).
- Class III — K⁺ channel blockers (amiodarone,
  sotalol, dofetilide, ibutilide).
- Class IV — Ca²⁺ channel blockers
  (verapamil, diltiazem).

### Skeletal muscle excitation-contraction coupling

- Muscle AP → T-tubule → Cav1.1 (DHP receptor)
  → mechanically coupled to RyR1 in SR
  membrane → Ca²⁺ release → troponin C → actin-
  myosin contraction.

### Cardiac excitation-contraction coupling

- AP → Cav1.2 (LTCC) → small Ca²⁺ influx → triggers
  RyR2 in SR membrane (Ca²⁺-induced Ca²⁺ release)
  → larger Ca²⁺ release → contraction.
- SERCA pumps Ca²⁺ back into SR; NCX (Na⁺/Ca²⁺
  exchanger) extrudes across PM.
- RyR2 mutations cause CPVT (catecholaminergic
  polymorphic ventricular tachycardia).

## Ligand-gated channels

### nAChR (nicotinic acetylcholine receptor)

- Cation-selective; pentameric (α, β, γ, δ,
  ε subunits in muscle; α + β subunits only in
  many neuronal subtypes).
- Neuromuscular junction muscle-type: 2 α + β +
  γ (fetal) or ε (adult) + δ.
- Targeted by:
  - Tubocurarine + atracurium (NMJ blockers,
    muscle relaxants).
  - Succinylcholine (depolarising blocker; rapid-
    sequence intubation).
  - Nicotine (smoking cessation receptor).
  - Varenicline + cytisine (partial agonists for
    smoking cessation).

### GABA_A receptor

- Cl⁻-selective; pentameric (most common α1β2γ2).
- Activation hyperpolarises → inhibitory.
- Targeted by:
  - Benzodiazepines (diazepam, lorazepam,
    alprazolam) — PAM at αβγ-containing receptors.
  - Barbiturates — PAM (high doses also direct
    activator).
  - General anaesthetics (propofol, etomidate,
    isoflurane, sevoflurane, desflurane) — PAMs.
  - Alcohol (ethanol) — modulator.
  - Z-drugs (zolpidem, zopiclone, eszopiclone) —
    α1-selective BZD-site PAMs.
- GABA_B is metabotropic (GPCR); GABA_C is also
  ionotropic (Cl⁻).

### Glycine receptor

- Cl⁻-selective; pentameric.
- Inhibitory; spinal cord + brainstem.
- Strychnine antagonist (lethal disinhibition).

### Glutamate receptors (ionotropic)

- AMPA — non-NMDA; fast EPSCs; tetrameric
  GluA1-4; Ca²⁺-permeable if GluA2-lacking.
- Kainate — neuromodulatory.
- NMDA — slow EPSCs; voltage- + ligand-gated;
  Mg²⁺ block at rest; Ca²⁺-permeable; coincidence
  detector for LTP.
- Targeted by ketamine + memantine + esketamine
  (NMDA antagonists; depression + Alzheimer's
  + anaesthesia).

### 5-HT3

- Cation-selective; pentameric.
- Anti-emetics ondansetron + granisetron + palon-
  osetron block.

### P2X receptors

- ATP-gated cation channels; trimeric.
- P2X3 + P2X2/3 in pain pathways.

## Channelopathies — selected

| Channel | Gene(s) | Disease |
|---------|---------|---------|
| Nav1.1 | SCN1A | Dravet, GEFS+ |
| Nav1.5 | SCN5A | Brugada, Long QT 3, SSS |
| Nav1.7 | SCN9A | Erythromelalgia (GoF) / pain insensitivity (LoF) |
| Cav1.1 | CACNA1S | Hypokalaemic periodic paralysis |
| Cav1.2 | CACNA1C | Timothy syndrome / Long QT 8 |
| HERG | KCNH2 | Long QT 2; SQTS1 |
| KCNQ1 | KCNQ1 | Long QT 1; SQTS2; familial AF |
| RyR1 | RYR1 | Malignant hyperthermia, central-core |
| RyR2 | RYR2 | CPVT |
| CFTR | CFTR | Cystic fibrosis (Cl⁻ channel) |
| CLCN1 | CLCN1 | Myotonia congenita (Thomsen / Becker) |
| AChR α1 | CHRNA1 | Congenital myasthenia |
| KATP (Kir6.2 + SUR1) | KCNJ11 / ABCC8 | Neonatal diabetes / congenital hyperinsulinism |

## Patch clamp + electrophysiology

- **Patch clamp** (Neher + Sakmann Nobel 1991) —
  standard technique for ion-channel
  electrophysiology.  Configurations:
  cell-attached, whole-cell, perforated-patch,
  inside-out, outside-out.
- **Voltage clamp** — control membrane voltage
  + measure current.
- **Current clamp** — fix current + record
  voltage (used for AP recording).
- **Automated patch clamp** — Nanion Patchliner +
  Sophion Qube + Molecular Devices IonWorks +
  IonFlux.  High-throughput drug screening.
- **Multi-electrode arrays (MEAs)** — extracellular
  recording from large cell populations.
- **Voltage-sensitive dyes + indicators** —
  optical alternatives.

## Modulation + drug development

- **Allosteric modulators** — increasingly
  preferred for selectivity (subtype-specific
  PAM / NAM).
- **Use-dependent block** — local anaesthetics +
  Class I antiarrhythmics preferentially block
  open / inactivated channels (target firing
  cells).
- **State-selective drugs** — mexiletine + lacosamide
  (slow-inactivation enhancer; partial-onset
  seizures).
- **Cardiac safety pharmacology** — every drug
  candidate screened for HERG block (in vitro)
  + QT effects (in vivo + clinical) due to
  Torsades-de-pointes risk.
- **Cone-snail toxins (conotoxins)** — rich
  source of channel- + receptor-selective
  ligands.

## Cross-link

For neuroscience-specific channel + neurotransmitter
detail, see **AB-3.0 intermediate "Nervous systems
+ neuroscience essentials"**.  For cardiac
pharmacology + electrophysiology, see future
**PH-4.0 "Cardiovascular pharmacology"**.

## Try it in the app

- **Window → Pharmacology Studio → Receptors** —
  voltage-gated + ligand-gated channel
  superfamilies + drug classes.
- **Window → Pharmacology Studio → Drug
  classes** — every channel-targeting drug class
  above.
- **Window → Biochem Studio → Enzymes** —
  Na/K-ATPase + SERCA + PMCA + V-ATPase entries.

This concludes the new intermediate-tier
additions for CB-4.0.  Next: **Calcium
signalling** (advanced).
