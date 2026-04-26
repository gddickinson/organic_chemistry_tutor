# Computational catalyst design

The ML + computational-chemistry lessons covered the
foundations. This lesson focuses on how to apply DFT + ML
specifically to **discover or improve a catalyst**.

## Why compute catalysts

Discovering a new catalyst experimentally takes 6-24 months
+ thousands of substrate-screening experiments.
Computational pre-screening reduces this to weeks.

## Three computational strategies

### 1. Mechanism-driven catalyst design

For a known mechanism, identify the rate-determining step.
Compute ΔG‡ for variants of the catalyst → predict best.

```
Step 1: define proposed mechanism + intermediates.
Step 2: DFT-optimise each TS + intermediate.
Step 3: compute ΔG‡ + ΔG_rxn for each step.
Step 4: vary catalyst's electronic / steric features →
   re-optimise + re-compute.
Step 5: pick the variant with lowest ΔG‡_rds.
```

Famous example: **Doyle Rh-carbene chemistry** — DFT
guided design of new chiral Rh dimers for asymmetric C-H
insertion.

### 2. Linear free-energy relationships (LFER)

Often a simple parameter (Tolman cone angle, Hammett σ,
ligand pKa) predicts catalyst performance:

```
log(k) = m × σ + c        (Hammett-like)
log(k) = m × CA + c        (cone angle)
```

Compute σ + CA + pKa for hundreds of candidate ligands
→ rank by predicted activity → synthesise top 5.

### 3. ML-assisted screening

Train ML model on existing catalyst-performance data:

- **Features**: ligand properties (size, electronics,
  conformation), substrate features.
- **Target**: TON, ee, yield.
- **Model**: random forest, GP regression, GNN.
- **Active learning**: model picks the most informative
  next experiment.

EDBO+ (Doyle), CHEMOS (Sigman), BOSS (Aalto) are
chemistry-tuned Bayesian optimisation platforms.

## Tools

| Tool | Use |
|------|-----|
| **Gaussian, ORCA, Q-Chem, Psi4** | DFT optimisation + frequencies |
| **NWChem, CP2K** | Periodic + materials catalysts |
| **AutoDE, Gaussview, ORCA-SHARK** | TS searching + IRC |
| **Materials Project** | Pre-computed catalyst surfaces |
| **PyMOL, ChemDraw 3D** | Visualisation |
| **EDBO+, BOSS** | Bayesian optimisation |
| **DFT-DRD (Distortion-Interaction)** | Decompose ΔG‡ into distortion + interaction |
| **Multiwfn, NCIplot** | Energy decomposition + non-covalent interactions |

## Distortion-Interaction (D-I) analysis

DFT-decompose the activation barrier into:

- **Distortion energy**: deformation of fragments to TS
  geometry.
- **Interaction energy**: bonding between fragments at TS.

```
ΔG‡ = ΔG_distortion + ΔG_interaction
```

Then optimise:

- Reduce distortion → use a more flexible / pre-organised
  fragment.
- Increase interaction → tune electronics for stronger
  bonding.

Used heavily in Houk's predictive selectivity papers.

## Example: heterogeneous catalyst screening

For a CO₂ → fuel reduction electrocatalyst:

1. Pre-compute binding energies of CO + COOH + H + OH on
   100s of metal surfaces (Materials Project /
   Catalysis-Hub).
2. Rank by **Sabatier principle** — best binding ~ 0.5
   eV; too strong / weak both bad.
3. Identify Cu, Au, single-atom Ni-N₄, etc., as
   candidates.
4. Synthesise + test.

Examples: Nørskov's "computational catalyst design" paradigm
discovered MoS₂ as an HER catalyst (2007), now
commercialised.

## Example: ligand design

For a Pd cross-coupling target:

1. Enumerate 200 ligand variants (vary R groups, substitution).
2. Compute Tolman cone angle + σ-donating + π-accepting via
   DFT.
3. Train ML on existing Buchwald data: σ + CA → predicted
   activity for ArCl coupling.
4. Top-10 predictions → synthesise + test.

Hartwig + Buchwald + Doyle have published this kind of
campaign, sometimes finding > 100× rate improvements.

## Pitfalls

- **Wrong mechanism assumed** → all the DFT is wrong.
- **Model error** of 1-2 kcal/mol → 10-100× rate
  uncertainty.
- **Sampling**: many TS found are not the true minimum-
  energy path. Use multiple starting structures.
- **Implicit solvent** misses specific solvent effects;
  explicit-water-shell hybrids better but slower.
- **Distortion-interaction** can mislead if the wrong
  fragmentation is chosen.

## Industrial impact

- **Pfizer + Genentech + GSK** routinely include
  computational pre-screening in catalyst discovery.
- **Schrödinger Material Science Suite + BioVia Materials
  Studio** — commercial platforms.
- **DOE National Labs + UC Berkeley + Stanford** — open-
  data on catalyst surfaces for ML training.

## Try it in the app

- **Tools → Orbitals (Hückel/W-H)** → simple MO theory
  intuition for ligand design.
- **Reactions tab** → energy profiles for seeded reactions
  reflect DFT computations.
- **Glossary** → search *DFT*, *Hammett equation*, *Cone
  angle*, *Distortion-interaction analysis*, *Sabatier
  principle*, *Ligand design*.

Next: **ML for retrosynthesis (Aizynth, ASKCOS, Synthia)**.
