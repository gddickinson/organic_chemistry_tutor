# Cryo-EM — atomic resolution without crystals

**Cryo-electron microscopy** (cryo-EM) reconstructs 3D
biomolecular structures from millions of 2D projection
images of single molecules embedded in vitreous ice. The
2017 Nobel Prize (Henderson + Frank + Dubochet) recognised
the field; the *resolution revolution* of 2013-2017
transformed cryo-EM from a "blob-ology" into the dominant
structural-biology technique for large complexes.

## Workflow

1. **Sample preparation** — purified protein in buffer,
   blot a 3-µL drop on a holey-carbon grid, plunge into
   liquid ethane (-180 °C). Water vitrifies (no crystal
   ice) so individual molecules are trapped in random
   orientations in a thin film.
2. **Imaging** — load grid into a TEM at 300 keV (FEI /
   Thermo Krios, JEOL CRYO ARM). Defocus + low-dose
   exposure (~ 50 e⁻ / Å²) to spread radiation damage
   over the dataset.
3. **Direct electron detector** — Falcon, K2/K3 cameras
   record 30-60 frame movies → align frames + correct
   beam-induced motion.
4. **Particle picking** — software (cryoSPARC, RELION,
   crYOLO) finds individual particles in the
   micrographs.
5. **2D classification** — group + average particles to
   get clean projection classes.
6. **3D ab initio** — generate initial 3D model from a few
   classes.
7. **3D refinement** — iteratively refine particle poses
   + 3D map. Modern: > 1 M particles → 2-3 Å maps.
8. **Model building** — fit atoms into the density.

## Resolution today

- **Routine (2025)**: 2.5-3.5 Å for ≥ 100 kDa complexes.
  Side chains + water + ligands resolved.
- **Best**: ~ 1.2 Å (apoferritin benchmark, 2020) — atomic
  resolution comparable to X-ray.
- **Membrane proteins**: 2.5-4 Å routine, even for hard
  GPCRs in nanodiscs.
- **Megacomplexes** (ribosome, spliceosome,
  proteasome): 2.5-4 Å for 500 kDa - 5 MDa.

## Why cryo-EM took over

- **No crystals** — works on heterogeneous, conformationally
  flexible samples that won't crystallise.
- **Multiple conformations** in one dataset — 3D
  classification splits an ensemble. You see *the protein
  doing its job* across states.
- **Membrane proteins in near-native lipid environments**
  (nanodiscs, peptidiscs).
- **Big complexes** that crack X-ray (ribosomes,
  spliceosomes, viruses).

## Negative cases

- **Small proteins (< 50 kDa)** — low SNR; X-ray still
  better. AlphaFold + X-ray fragment screening usually
  preferred.
- **Highly flexible samples without obvious classes**
  — 3D classification fails to converge.
- **Need for ligand-induced kinetics** — better caught by
  time-resolved X-ray crystallography or NMR.

## Cryo-electron tomography (cryo-ET)

Same concept but for unique objects (cells, sub-cellular
volumes):

1. Tilt the stage from -60° → +60° in 1-3° steps,
   collecting one image per tilt.
2. Reconstruct a 3D tomogram by inverse Radon transform.
3. **Subtomogram averaging** — pick repeating particles
   within the tomogram + average → resolution to 5-10 Å on
   particles inside cells.

Famous examples: in-cell ribosome structures, COVID-19 spike
in situ on the virion surface, axonal microtubule arrays.

## Microsymposia: software you should know

- **RELION** (Scheres, MRC) — Bayesian inference framework;
  open + reference implementation.
- **cryoSPARC** (Punjani, Toronto) — GPU-accelerated;
  industry-favourite for speed.
- **EMAN2, SPHIRE** — alternative open suites.
- **ChimeraX** — visualisation + interactive map fitting.
- **PHENIX, ISOLDE** — atomic refinement against cryo-EM
  density.

## Validation metrics

- **FSC (Fourier Shell Correlation)** — split data in half,
  reconstruct independently, compare. Resolution defined
  at FSC = 0.143.
- **Map sharpness (B-factor)** — how flat the high-resolution
  signal is.
- **Atomic-model fit**: real-space correlation, EMRinger
  validation, MolProbity.

## Modern frontiers

- **Single-particle resolution < 2 Å** — needs perfect
  vitrification + cold-FEG sources + Selectris energy
  filter; common at top facilities by 2024.
- **Time-resolved cryo-EM** — mix-and-spray devices freeze
  reactions in milliseconds → movie of a conformational
  change.
- **Drug-discovery cryo-EM** — fragment screening + co-
  structures replace X-ray for big targets (NMDA receptors,
  ion channels, ribosomal antibiotics).
- **AI-driven map interpretation** — ModelAngelo, ParticleSeg
  automate model-building.

## Try it in the app

- **Proteins tab** → many seeded PDB entries (HIV protease,
  ribosome) come from cryo-EM. Look at maps + check
  resolution metadata.
- **Glossary** → search *Cryo-EM*, *Cryo-ET*, *Resolution
  revolution*, *FSC (Fourier shell correlation)*,
  *Vitrification*.

Next: **Controlled radical polymerisation (RAFT, ATRP,
NMP)**.
