# Molecular dynamics simulations

A **molecular dynamics (MD) simulation** propagates a system
of atoms forward in time by integrating Newton's equations
of motion under a chosen force field. MD reveals the time-
dependent + ensemble-average behaviour of molecules:
folding, binding, conformational change, transport.

## The basic algorithm

For each atom *i*:

```
F_i = -∇_i V(r_1, ..., r_N)         (force from potential)
m_i a_i = F_i                       (Newton's 2nd law)
r_i(t + dt) = r_i(t) + v_i(t) dt + ½ a_i(t) dt²   (Verlet)
v_i(t + dt) = v_i(t) + ½ (a_i(t) + a_i(t+dt)) dt
```

Time step `dt` is typically **1-2 fs** (so light atoms don't
move beyond a fraction of a bond length).

## Force fields

The potential V is a sum of empirical terms:

```
V = V_bond + V_angle + V_torsion + V_LJ + V_Coulomb
```

Bonds, angles, torsions are harmonic (or Fourier series for
torsions). Non-bonded uses **Lennard-Jones** + **Coulomb**.
Force-field parameters fit to experiment + QM data.

### Common force fields

| Field | Best for |
|-------|----------|
| **AMBER (ff14SB, ff19SB, ff99SB)** | Proteins, nucleic acids |
| **CHARMM (CHARMM36)** | Proteins, lipids, carbohydrates |
| **GROMOS** | Proteins, small molecules |
| **OPLS-AA / OPLS3** | Small molecules, drug discovery |
| **GAFF / GAFF2** | General organic small molecules (paired with AMBER) |
| **CGenFF** | Small molecules in CHARMM environment |
| **MARTINI** | Coarse-grained (lipids, proteins, polymers; 4-1 atom mapping) |
| **ReaxFF** | Reactive (allows bond breaking; combustion + catalysis) |
| **AIMD (ab initio MD)** | DFT-level forces, < 100 atoms, < 100 ps |

## Solvent + ensemble

- **Explicit water models**: TIP3P (3-site, classic),
  TIP4P-Ew, OPC (3 + 4-site, more accurate), SPC/E.
- **Implicit solvent**: GBSA, PBSA — fast but loses
  H-bond network.
- **Periodic boundary conditions** to avoid surface
  artifacts.

Ensembles:

- **NVE** (microcanonical) — energy conserved.
- **NVT** (canonical) — Berendsen / Nose-Hoover thermostat
  for temperature control.
- **NPT** (isothermal-isobaric) — Parrinello-Rahman
  barostat for pressure control. Most common for
  biological simulations at 300 K, 1 atm.

## Software

- **GROMACS** — fast on GPUs; biological + small-molecule.
- **AMBER** — historic protein-focused suite; pmemd /
  sander engines.
- **NAMD** — scales well on supercomputers; CHARMM-style.
- **OpenMM** — Python-friendly engine; popular for ML
  + automation.
- **LAMMPS** — material science; reactive force fields,
  coarse-grained, polymer.
- **Schrödinger Desmond** — commercial pharma standard.
- **CP2K + Quickstep** — DFT-based ab initio MD.

## Length + time scales

The unsolved problem: biological events span widely
different timescales.

| Process | Timescale | MD feasible? |
|---------|-----------|--------------|
| Bond vibration | fs | yes (resolved) |
| Side-chain rotation | ps-ns | yes |
| Backbone fluctuation | ns | yes |
| Loop motion | ns-μs | yes (with care) |
| Side-chain rotamer flip | ns-μs | sometimes |
| Allosteric switch | μs-ms | enhanced sampling |
| Protein folding | μs-s | enhanced sampling + special hardware |
| Enzyme catalysis cycle | ms-s | requires QM/MM + enhanced |
| Drug binding (residence time) | s-min | requires Markov state models |

A 1-μs simulation of a 500 000-atom system on modern GPUs
takes ~ 1-2 weeks. Anton 2/3 (D. E. Shaw Research's
custom MD supercomputer) reaches ms timescale for proteins.

## Enhanced sampling

To reach long-time events without brute-force MD:

- **Replica exchange (REMD / T-REMD / H-REMD)** — run
  many copies at different T or Hamiltonian; swap
  configurations to escape local minima.
- **Metadynamics** (Parrinello, Laio) — build up
  history-dependent bias along chosen collective variables
  → flatten the FES.
- **Umbrella sampling** — biased simulations along a
  reaction coordinate → unbias to recover free energy
  profile (WHAM / MBAR).
- **Steered MD** — pull a substrate along a path → estimate
  binding free energy (Jarzynski equality).
- **Markov State Models (MSM)** — collect short MD
  trajectories, cluster, build a transition matrix → infer
  long-timescale kinetics.

## QM/MM

For reactions in the active site of an enzyme: treat the
small reactive region with QM (DFT or post-HF), the rest
with MM force field. Boundary handled by link atoms +
electrostatic embedding.

Used to compute Eₐ for enzyme-catalysed reactions, predict
KIEs, model unusual catalytic mechanisms.

## ML potentials — closing the gap

Force-field accuracy ≈ 1-3 kcal/mol per bond on
relative energies. DFT ≈ 0.5-1 kcal/mol but slow (N⁵ for
hybrid functionals).

**Machine-learned potentials** (ANI-2x, AIMNet2, MACE-OFF23,
SchNet) train neural networks on millions of QM
configurations → DFT-level accuracy at force-field cost.
By 2025, ML potentials run kg-scale industrial drug
binding-affinity simulations + materials simulations.

## Use cases

- **Drug discovery**: predict ligand binding affinity (FEP+,
  TIES) within ~ 1 kcal/mol → guide medicinal chem.
- **Lipid bilayer studies**: cholesterol effect, lipid
  rafts, transmembrane protein insertion.
- **Channel + pump dynamics**: K⁺ channel, ABC transporter,
  ATP synthase rotation.
- **Allostery**: how a distant binding event propagates
  through the protein.
- **Protein-protein assembly**: tau aggregation, amyloid
  formation.
- **Materials**: ion conduction in batteries, polymer
  membranes, MOF gas adsorption.

## Limits

- **Force field limitations** — point charges, no
  polarisation; AMOEBA + Drude polarisable models address
  this but slower.
- **Sampling** — even μs MD doesn't sample every relevant
  state; "the trajectory you ran" ≠ "the equilibrium
  ensemble".
- **Initial conditions matter** — start from a realistic
  configuration; equilibrate properly.
- **Reproducibility** — random number seed differences →
  diverging trajectories after ~ 100 ps. Run multiple
  replicas.

## Try it in the app

- **Tools → Conformer generation** → produces 3D conformers
  by MMFF or RDKit ETKDG; minimum-energy conformer often
  matches MD-equilibrated structure.
- **Glossary** → search *Molecular dynamics*, *Force
  field*, *Ensemble*, *Free energy perturbation*, *QM/MM*.

Next: **Free-energy methods (FEP, TI, umbrella sampling)**.
