# Quantitative signalling — kinetics, dynamics, and the
modern frontier

Cell signalling has moved from "X activates Y" cartoons to
quantitative dynamic models with measurable rate
constants. This shift — driven by single-cell imaging,
mass cytometry, and computational modelling — is the
modern frontier of the field.

## Why dynamics matter

The classical signalling literature is full of dose-
response curves at fixed time points. Real biology is
time-dependent + heterogeneous + context-sensitive:

- ERK can be either pulsatile or sustained — and the
  same input can give different outputs in different
  cells.
- p53 oscillates with damage intensity; sustained p53 →
  apoptosis, pulsatile p53 → cell-cycle arrest +
  recovery.
- NF-κB oscillates with cytokine stimulus; the
  oscillation frequency encodes information about the
  stimulus identity.

Time + cell-to-cell heterogeneity carry information that
the static "active vs inactive" picture loses.

## Signalling motifs as engineering primitives

Network motifs that recur across pathways:

- **Negative feedback** — fast termination + adaptation.
  EGFR → ERK → DUSP6 → ERK off. Drives oscillation when
  combined with delay.
- **Positive feedback** — bistability + memory. CDK1 +
  Cdc25 + Wee1 in mitotic entry; the Goldbeter-Koshland
  zero-order ultrasensitivity gives switch-like
  behaviour.
- **Coherent feed-forward** — noise filtering. Persists
  through transient input drops.
- **Incoherent feed-forward** — pulse generation,
  perfect adaptation. Bacterial chemotaxis is the
  paradigm (Yi-Huang-Simon-Doyle 2000).
- **Coupled positive + negative feedback** — sustained
  oscillation. Cell cycle, circadian rhythm, NF-κB.

Uri Alon's book *An Introduction to Systems Biology*
(2007, 2nd ed 2019) is the canonical text.

## Quantitative single-cell methods

The data revolution that made dynamic signalling
tractable:

- **Live-cell biosensor imaging** — FRET-based reporters
  for cAMP (Epac), Ca²⁺ (cameleon, GCaMP), kinase
  activity (KARs — kinase activity reporters); single-
  cell + sub-cellular spatial resolution.
- **Mass cytometry (CyTOF)** — heavy-metal isotope-
  tagged antibodies, ~ 50 simultaneous markers per
  single cell, drug-perturbation studies at population
  scale.
- **scRNA-seq + scATAC-seq** — single-cell transcriptome
  + chromatin accessibility; expressing-cell
  heterogeneity uncovered.
- **High-content imaging** — automated microscopy +
  cell segmentation + multi-marker quantification +
  multi-perturbation screens.
- **Optogenetics + chemical induction systems** —
  precise, reversible signalling perturbations
  (CRY2-CIB1, FRB-FKBP, opto-Raf, opto-Akt, opto-
  receptors).

## Mathematical modelling

Two main flavours:

### Deterministic ODE models

- Each protein's concentration as a continuous
  variable evolving by reaction-rate equations.
- Tools: COPASI, MATLAB SimBiology, BioNetGen.
- Examples: Goldbeter's mitotic-oscillator model
  (1991); Tyson's cell-cycle switch (2002); Lev Bar-Or
  + Lahav's p53-MDM2 oscillator (2000).

Limitations: assumes large numbers of molecules + well-
mixed cytoplasm. Single-molecule + low-copy-number
species need stochastic treatment.

### Stochastic / agent-based models

- Gillespie algorithm for chemical-master-equation
  simulation.
- Capture intrinsic noise — the kind that comes from
  small molecule numbers + discrete reaction events.
- Predict cell-to-cell variability from single-cell
  data.

Elowitz + Leibler's repressilator (2000) — synthetic
gene-circuit that *should* oscillate but actually shows
substantial cell-to-cell phase variability — was a
landmark in stochastic modelling.

## Information theory + signalling

Cheong et al (2011, Science) measured the information
capacity of TNF → NF-κB signalling at the single-cell
level: ~ 1 bit per cell. Single cells can barely
distinguish "TNF on" from "TNF off"; populations average
out the noise to encode more.

This raised the question: how do tissues make reliable
collective decisions from noisy single-cell channels?

Answers in active research:

- **Population averaging** — many cells reduce noise.
- **Temporal integration** — noisy channel sampled over
  time gains information.
- **Multi-pathway integration** — multiple noisy inputs
  combined increase information capacity.
- **Cell-cell coupling** — gap-junction or
  electrotonic coupling shares state across cells.

## Synthetic biology + circuit engineering

Once you understand signalling quantitatively, you can
engineer it:

- **CARs (chimeric antigen receptors)** — engineered
  T-cell receptors with extracellular antibody scFv +
  CD3ζ + costimulatory CD28/4-1BB intracellular
  domains.
- **synNotch + SUPRA** — modular synthetic receptor +
  effector platforms.
- **Tet-on / Tet-off + Cre-loxP** — small-molecule-
  inducible genetic switches.
- **Auxin-inducible degron (AID)** — rapid protein
  degradation in seconds-minutes.
- **dTAG + ARV-PROTAC** — chemical-genetic protein
  degraders for any target.

CAR-T cells (tisagenlecleucel, axicabtagene ciloleucel)
delivered the first approved engineered-cell-therapy in
2017 for ALL + DLBCL. Currently > 7 approved CAR-T
products.

## Key open questions

- How do single cells make accurate fate decisions from
  noisy molecular channels?
- What sets the timescale of biological responses? Why
  do some pathways oscillate + others adapt?
- How do signalling cross-talk + non-genetic
  heterogeneity drive drug resistance?
- Can we engineer synthetic signalling circuits
  reliably enough for therapy?

## Try it in the app

- **Cell Bio → Signalling** — every entry's "key
  components" + "regulators" + "disease associations"
  fields are the substrate for quantitative-modelling
  exercises.
- Future Phase CB-3.x will add interactive ODE-
  simulation tools for canonical motifs.

Next: **Synthetic biology + cell engineering**.
