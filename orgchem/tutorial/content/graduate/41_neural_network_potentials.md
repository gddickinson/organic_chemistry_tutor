# Neural network potentials deeper — MACE, NequIP, AIMNet

The cheminformatics + MD lessons mentioned **ML potentials**.
This lesson goes into detail: how they work, how they
compare to classical force fields + DFT, and where they're
heading.

## What an ML potential is

A neural network trained to predict **DFT-quality energies +
forces** from atomic coordinates:

```
input: 3D positions r₁, r₂, ..., rₙ + atomic numbers
output: total energy E(r) + forces -∂E/∂r
```

Once trained, used for:

- Molecular dynamics simulation.
- Geometry optimisation.
- Vibrational frequencies.
- Conformer search.
- Free-energy methods (FEP, US, MetaD).

## Why it matters

| Method | Cost (per energy) | Accuracy |
|--------|-------------------|----------|
| Force field (CHARMM, OPLS) | 10⁻⁴ s | 1-3 kcal/mol |
| Neural network potential | 10⁻³ - 10⁻¹ s | 1-2 kcal/mol |
| Semi-empirical (PM7, GFN-xTB) | 10⁻¹ s | 2-5 kcal/mol |
| DFT (PBE) | 10² - 10⁴ s | 0.5-1 kcal/mol |
| CCSD(T)/CBS | 10⁵ - 10⁷ s | < 0.5 kcal/mol |

NN potentials hit DFT-like accuracy at force-field-like
cost — bridging the gap.

## Architecture progression

### Behler-Parrinello (2007)

Original NN potential. Hand-crafted "symmetry functions"
describe atomic environments → feedforward NN predicts
per-atom energy.

### SchNet (Schütt 2018)

Message-passing GNN. First end-to-end learnable
representation; ~ 0.5 kcal/mol on QM9 dataset.

### DimeNet (Klicpera 2020)

Includes 3-body (angle) information explicitly. Improved
accuracy on torsional energies.

### NequIP (Batzner 2022)

**Equivariant** under rotation + translation — uses
spherical-harmonic features → much better
generalisation. Smaller dataset → same accuracy as SchNet.

### MACE (Batatia 2022)

Higher-order equivariant message passing with cluster
expansion → state-of-the-art accuracy with relatively
small training sets.

### AIMNet2 (Outeiral 2024)

Universal NN potential trained on diverse organic +
inorganic chemistry; near-DFT accuracy out-of-the-box.

## ANI series (Smith et al.)

Pre-trained on millions of small organic molecule
configurations:

- **ANI-1** (2017) — first universal ML potential.
- **ANI-2x** (2019) — adds N, S, F, Cl; widely used.
- **ANI-2x-D** — includes dispersion.

ANI-2x is now standard for low-cost organic conformer
search + MD.

## MACE-OFF

**MACE-OFF23** (Kovács 2023) — state-of-the-art NN potential
for organic small molecules. Drop-in replacement for
classical force fields in MD simulations.

Used in **drug-binding free-energy calculations** with
near-DFT accuracy at force-field cost.

## Training datasets

- **QM9** — 134 K small molecules; cheap DFT energies +
  geometries.
- **ANI-1x, ANI-2x dataset** — millions of configurations.
- **OC22, OC25** — open catalysis dataset; surfaces +
  intermediates.
- **SPICE** — solvated proteins + ligands.
- **MD22** — biomolecular MD trajectories.

## Active learning + uncertainty quantification

NN potentials sometimes fail outside their training
distribution. Active learning:

1. Start with seed dataset.
2. Train NN.
3. Run MD → identify configurations where NN is
   uncertain (committee disagreement, ensemble variance).
4. Compute DFT for those → add to training set.
5. Retrain.

Repeat until uncertainty is low everywhere.

## Industrial uses

- **Pharma drug-binding FEP** — Schrödinger + others
  evaluating MACE-OFF for production FEP+.
- **Materials simulation** — battery electrolyte
  decomposition, polymer chemistry, MOF gas adsorption.
- **Protein-ligand interaction** — NN potential + MD →
  binding-affinity ranking.
- **Catalysis** — surface reactions on Pt, Au, Cu modelled
  with NequIP / MACE; replaces explicit DFT MD.

## Limits

- **Out-of-distribution failures** — performance drops on
  exotic chemistry not in training set.
- **Reactive chemistry** — bond-breaking + bond-making
  challenging without specific training data.
- **Cost** — cheaper than DFT but more expensive than
  classical FF; ~ 100-1000× FF cost per energy
  evaluation.
- **GPU-required** — most efficient on modern GPUs (A100,
  H100).

## Try it in the app

- **Tools → Conformer generation** → produces conformers
  via MMFF; equivalent ML-potential results would be
  more accurate.
- **Glossary** → search *Neural network potential*,
  *MACE*, *NequIP*, *ANI*, *AIMNet*, *Equivariant
  neural network*.

Next: **Generative chemistry models (ChemBERTa, MolFormer)**.
