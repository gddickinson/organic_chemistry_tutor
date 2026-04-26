# Free-energy methods — FEP, TI, umbrella sampling

Computing **free energies** quantitatively — binding
affinities, solvation, conformational equilibria — is the
holy grail of computational chemistry. Several flavours
of method, each with strengths.

## Why free energy is hard

Energy E(r) is a number at each configuration r. Free
energy is an integral over all configurations:

```
A = -kT ln Z         where  Z = ∫ exp(-V(r)/kT) dr
```

Z spans 3N-dimensional configuration space. Direct
integration is exponentially expensive for N > 5.

The trick: never compute Z directly. Compute **free-energy
differences** between two states by sampling.

## Free-energy perturbation (Zwanzig, 1954)

Two systems with potentials V_A and V_B (both contain the
same atoms, but in different states like "ligand X bound"
vs "ligand X' bound"). Free energy difference:

```
ΔA_AB = -kT ln <exp(-(V_B - V_A)/kT)>_A
```

"Run MD on system A, average exp(-ΔV/kT) over the
ensemble." Works only when A and B overlap significantly
in configuration space — otherwise the average is dominated
by rare events.

In practice:

- Split the A → B perturbation into **multiple windows**
  (intermediate λ values: 0, 0.1, ..., 1).
- Run MD at each λ; compute incremental free energies
  between adjacent windows; sum.

This is **multi-window FEP** — the workhorse method.

## Thermodynamic integration (TI)

Equivalent reformulation:

```
ΔA_AB = ∫₀¹ <∂V/∂λ>_λ dλ
```

Same result; sample at each λ. TI + FEP give identical
answers in principle; differ in numerical noise.

## Bennett acceptance ratio (BAR)

Combines forward + backward FEP estimates → minimum-
variance estimator of ΔA. Standard in modern packages
(GROMACS, AMBER, Schrödinger FEP+).

**MBAR (multi-state BAR)** extends to many windows
simultaneously → optimal estimate from all data.

## FEP+ for relative ligand binding

Flagship application: predict **relative binding affinity**
of two ligands to the same protein.

Thermodynamic cycle:

```
Ligand A bound  ──ΔG_bind(A)──  Ligand A free
       │                              │
   ΔG_perturb(P)                ΔG_perturb(W)
       │                              │
Ligand B bound  ──ΔG_bind(B)──  Ligand B free

ΔΔG_bind = ΔG_bind(B) - ΔG_bind(A) = ΔG_perturb(W) - ΔG_perturb(P)
```

Compute ΔG_perturb in protein + water by alchemical FEP →
ΔΔG without ever simulating the binding event itself.

Schrödinger's **FEP+** is the dominant pharma
implementation. Accuracy: ~ 1 kcal/mol RMSD vs
experiment for diverse benchmarks (Wang et al. 2015,
*JACS*).

## Umbrella sampling

For **physical** (not alchemical) free-energy profiles —
what's the free energy along a coordinate ξ (distance,
angle, dihedral, RMSD, ...)?

Technique:

1. Apply biasing potential w(ξ) = ½ k (ξ - ξ_i)² centred
   at multiple values of ξ_i.
2. Run MD in each window; record distribution of ξ.
3. Combine via WHAM (weighted histogram analysis method)
   or MBAR → unbiased free-energy profile.

Produces a **PMF (potential of mean force)** — the free
energy along the chosen coordinate.

Examples:

- Membrane permeation of a small molecule (ξ = depth in
  bilayer).
- Substrate dissociation from an enzyme (ξ = ligand-protein
  distance).
- Conformational change of a molecule (ξ = dihedral angle).

## Metadynamics

Adds bias **dynamically** during simulation. Each time the
trajectory visits a region of CV space, deposit a small
Gaussian "hill" → discourages return. Over time the bias
fills basins → flat (free-)energy surface.

Variants:

- **Standard MetaD** — biased trajectory; recover free
  energy by removing the bias.
- **Well-tempered MetaD** (Barducci, 2008) — hills shrink
  over time → guaranteed convergence.
- **Bias-exchange MetaD** — multiple replicas with
  different CVs → swap configurations.

PLUMED is the standard plugin for MetaD across MD packages.

## Steered MD + Jarzynski equality

Pull the system along a coordinate at constant velocity →
record the work done. Average over many runs; Jarzynski's
equality:

```
exp(-ΔA/kT) = <exp(-W/kT)>     (over forward pulls)
```

In practice this is noisy because rare low-W trajectories
dominate. Useful as a sanity check or for fast PMF
estimation.

## Replica exchange thermodynamic integration (REUS)

Combine umbrella sampling with replica exchange — exchange
configurations between adjacent windows → faster
equilibration. Default in many modern protocols.

## Markov state models (MSM)

Different philosophy: don't compute free energies directly,
infer them from many short MD trajectories.

1. Run hundreds-thousands of short trajectories (10-100
   ns each).
2. Cluster snapshots into ~ 100-1000 microstates.
3. Estimate transition matrix from short-time observations.
4. Build a Markov model → recover **kinetics + steady-state
   populations + free energy** of each state.

Pros: parallelisable; reaches ms timescale; gives kinetics
+ thermodynamics.

Cons: needs careful clustering + lag-time validation.

## ML-accelerated FEP

Recent: train a neural network to predict free-energy
correction from short MD or single-point QM → drastically
faster FEP. Boltzmann generators (Noé, 2019) directly
sample the equilibrium distribution by inverse-flow neural
nets.

## Use cases

- **Drug binding affinity** (FEP+, TIES) — design ligand
  variants with predicted ΔΔG ~ 1 kcal/mol.
- **Solvation free energy** — for log P + log D
  prediction.
- **pKa shift in proteins** — ionisation state of titratable
  residues.
- **Membrane permeation** — log Perm prediction for drug
  PK.
- **Catalytic mechanism free energy** (QM/MM + umbrella) —
  enzyme catalysis Eₐ.
- **Polymorph thermodynamics** (Newman, Pascal) — relative
  stability of crystal forms.

## Limits

- **Force field accuracy** — 1-2 kcal/mol systematic error
  per molecule; ML potentials closing the gap.
- **Sampling** — sluggish degrees of freedom (slow
  conformational change in protein loops) need enhanced
  sampling.
- **Convergence** — must demonstrate by hysteresis tests
  (forward vs backward perturbation should agree).
- **Cost** — pharma-grade FEP+ on a protein-ligand system
  needs ~ 100 GPU-hours per ligand pair.

## Try it in the app

- **Tools → Lab calculator…** → *Thermo + kinetics* tab —
  compute Eyring rates from ΔG‡; useful intuition for
  FEP-derived barriers.
- **Glossary** → search *Free energy*, *FEP (free energy
  perturbation)*, *Umbrella sampling*, *Metadynamics*,
  *Markov state model*, *PMF*.

Next: **Microbiome chemistry — gut metabolites + microbial
natural products**.
