# Free-energy methods for enzymes (EVB, QM/MM, MD-FEP)

The free-energy lesson covered general FEP. This lesson
focuses on **enzyme catalysis** — calculating Eₐ + ΔG‡
+ binding affinity for catalytic + protein-ligand systems.

## Why enzymes are hard

Enzyme reactions in vivo span:

- **Bond breaking + making** (electronic structure
  required → DFT or post-HF).
- **Conformational changes** (10⁻⁹ to 10⁻³ s timescales).
- **Solvent + ions** that affect electrostatics.

Pure DFT is too small (~ 100 atoms); pure MD with
classical force field can't break bonds. **Hybrid
methods** combine the best of both.

## QM/MM

The dominant approach:

```
QM region: ~ 50-200 atoms (active site + substrate);
           treated by DFT or HF or DLPNO-CCSD(T).
MM region: rest of protein + solvent; treated by classical
           force field (CHARMM, AMBER).
boundary: link atoms (H caps QM atoms cut from C-C bond),
          electrostatic embedding (MM charges polarise QM).
```

Compute energy + force at each step → use for MD or
optimisation.

## Major workflows

### Energy minimisation in QM/MM

```
Optimise QM coordinates + a buffer of MM atoms →
                    enzyme-substrate complex.
Identify TS (eigenvector following → saddle point).
Compute ΔG‡ + IRC.
```

Used by Warshel + Hammes-Schiffer + others to compute
catalytic Eₐ for hundreds of enzymes.

### Empirical Valence Bond (EVB)

Warshel's method (1980+):

- Two valence-bond states (reactant + product) are
  treated explicitly.
- Their interaction matrix element is parameterised from
  reference data (gas phase + solution).
- Linear combination of MM force fields with EVB coupling
  gives a smooth FES.

Cheap (force-field cost) + reliable (calibrated to
experiment). Used for thousands of enzyme + solution-
chemistry FES calculations.

### QM/MM-FEP

Combine QM/MM with FEP:

```
λ = 0: substrate
λ = 1: TS (or product)
Run MD at multiple λ values → integrate to get ΔG_QM/MM.
```

Used to compute binding free energies of inhibitors with
near-DFT accuracy in the active-site region.

### Markov state models for enzyme dynamics

Long-timescale (μs-ms) conformational changes that trigger
catalysis tracked by:

- Many short MD trajectories.
- Cluster snapshots into microstates.
- Build Markov transition matrix.
- Identify rare events + their kinetics.

Bowman + Pande pioneered for enzyme conformational
sampling.

## Famous applications

### TIM (triose phosphate isomerase) — catalytic perfection

Knowles' classic enzyme; catalyses DHAP ↔ G3P. QM/MM
calculations explained the > 10¹⁰-fold rate enhancement
via:

- Substrate orientation in active site.
- Glu-165 acts as general base.
- His-95 stabilises the enediol intermediate.

### KSI (ketosteroid isomerase) — proton-shuttle dynamics

QM/MM showed Tyr-16 and Asp-103 form a low-barrier
H-bond that stabilises the dienol intermediate.

### Cytochrome P450s — H-atom abstraction

DFT-cluster + QM/MM showed the iron-oxo Fe(IV)=O species
abstracts H from substrate; Eₐ ~ 15 kcal/mol; KIE ~ 7
predicted, matches experiment.

### HIV protease — drug binding

QM/MM-FEP for protease + lopinavir → predicts binding
affinity within 1 kcal/mol of experiment.

### Chorismate mutase — pericyclic enzyme

Single substrate, no catalytic residues making bonds; pure
electrostatic preorganisation.

## Schrödinger FEP+

Industrial tool:

- Combines QM-derived ligand parameters + classical force
  field for protein.
- λ-windowed FEP simulations for binding free energy.
- Standard accuracy: ± 1 kcal/mol RMS on diverse pharma
  benchmarks.
- Used in over 50 published drug-discovery campaigns.

## Open problems

- **Multi-state catalysis** — many enzymes have multiple
  conformational states; computing each one's Eₐ +
  ranking by population is hard.
- **Allostery** — distant binding events change active-site
  Eₐ; QM/MM needs careful sampling.
- **Cofactor changes** — NADH/NAD+, ATP/ADP, FAD/FADH₂
  redox; require state-specific simulations.
- **Quantum effects** — H tunnelling, zero-point energy;
  need explicit quantum nuclear treatment in QM/MM.

## ML acceleration

Modern: replace DFT with ML potentials (MACE, AIMNet) in
QM/MM → 100-1000× speedup with comparable accuracy.

NN-FEP simulations approaching ms scale + handling
hundreds of ligands per day.

## Try it in the app

- **Reactions tab** → seeded enzyme mechanisms (chymotrypsin,
  HIV protease, RNase A) — see the active-site arrows.
- **Proteins tab** → fetch any seeded PDB + view 3D
  structure.
- **Glossary** → search *QM/MM*, *EVB (empirical valence
  bond)*, *FEP*, *Free energy*, *Enzyme catalysis*.

Next: **Molecular electronics**.
