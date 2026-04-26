# X-ray crystallography for chemists

X-ray crystallography is the gold standard for atomic-
resolution 3D structure of small molecules + macromolecules.
The Cambridge Structural Database (CSD) holds > 1.2 million
small-molecule structures + the PDB > 220 000 protein
structures, almost all from X-ray diffraction.

## How it works (intuition)

A crystal is a 3D periodic lattice of identical molecules.
Shoot it with X-rays (λ ~ 1 Å, comparable to bond lengths)
+ measure the diffraction pattern. Each diffracted spot
corresponds to a Fourier component of the electron-density
map. With enough spots + the right phases, you Fourier-
transform back to get the electron density → atomic positions.

## The phase problem

You measure spot **intensities** — but you need the
**complex amplitudes** (intensity + phase) to do the
inverse Fourier transform. Recovering phases is the hard
part.

Solutions:

- **Direct methods** (Hauptman + Karle, 1985 Nobel) —
  statistical relationships between spot intensities give
  approximate phases. Works for small molecules + rare
  proteins.
- **Heavy atom / isomorphous replacement (MIR)** —
  derivatise the protein with a heavy atom (Hg, Au, Pt,
  Se) → its position derivable from intensity differences →
  starting phase set.
- **Anomalous scattering (MAD / SAD)** — selenomethionine-
  labelled proteins; Se K-edge inflection point reveals
  Se positions from anomalous scattering → phases. Now the
  workhorse for protein crystallography.
- **Molecular replacement (MR)** — start from a homologous
  known structure, place it in the unit cell, refine. Most
  PDB depositions use MR + AlphaFold predictions seed the
  search.

## Crystallisation

The bottleneck for proteins. Approaches:

- **Vapour diffusion** — sitting drop / hanging drop
  against a precipitant reservoir. Slow concentration
  drives nucleation.
- **Microbatch under oil** — robot-friendly, smaller
  drops.
- **Counter-diffusion in capillaries** — fine gradient
  control.
- **High-throughput screens** — Hampton / Molecular
  Dimensions / Qiagen plates with 96-1500 conditions.
  Robotic imaging.
- **Lipidic cubic phase (LCP)** — crystallise membrane
  proteins (GPCRs!) in a viscous lipid mesophase. Cherezov
  + Stevens revolutionised GPCR crystallography ~ 2007.

## Resolution + quality metrics

- **Resolution** (Å) — d-spacing of the highest-resolution
  spot used. Atomic resolution: < 1.2 Å. Pharma-quality:
  1.5-2.5 Å. Lower-resolution: 3-4 Å (still locates ligands
  + side chains).
- **R / R_free** — fit of model to data; R_free is the
  cross-validation R for a held-out 5 % of reflections.
  Acceptable: R_free < 0.3, ideally R_free - R < 0.05.
- **Rmsd from ideal geometry** — bond lengths < 0.02 Å,
  angles < 2°.
- **Ramachandran outliers** — < 0.5 % outliers for high-
  quality structures.
- **MolProbity score** — combined geometry quality
  indicator.

## Small-molecule X-ray

For drug discovery + natural-product structure
determination:

- **Single-crystal X-ray** — needs a crystal ~ 0.1 mm.
- **Microcrystal electron diffraction (MicroED)** — works
  on µm-sized crystals (sometimes a powder)! Gonen +
  Nannenga. Now routine for natural-product
  characterisation.
- **Powder XRD** — for polymorphs + amorphous phases. Drug
  forms (Form I vs Form II vs amorphous) matter for
  bioavailability — Cefdinir, Ritonavir's polymorph II
  disaster (1998 — half their stockpile crystallised as
  insoluble Form II overnight).

## Synchrotrons + free-electron lasers

- **Synchrotron beamlines** (Diamond, ESRF, NSLS-II, APS)
  — 10-100 ng of crystal, sub-second exposure, sub-µm
  beam size. Most modern PDB depositions.
- **X-ray free-electron lasers (XFEL)** — femtosecond
  pulses; serial femtosecond crystallography (SFX)
  destroys each crystal but captures diffraction before
  damage. Studies radiation-sensitive species + time-
  resolved chemistry on µs timescales.

## Time-resolved crystallography

**Pump-probe** at XFEL: laser-flash a photoactive substrate
+ collect diffraction at varying delays after the flash.
Movie-of-a-reaction frame-by-frame.

Famous wins: photolyase DNA repair, photosystem II water-
oxidation S-states, bacteriorhodopsin photocycle.

## Limits

- **Crystals are unphysiological** — packing + buffer +
  cryoprotectant differ from cytosol. Conformations may be
  trapped.
- **Disorder** — mobile residues + ligands without clear
  density appear as diffuse blobs.
- **Hydrogens** — only at sub-Å resolution (< 0.8 Å) +
  neutron diffraction.
- **Single conformation** — crystal averages 10²⁰ molecules
  into a static snapshot.

## Try it in the app

- **Proteins tab** → fetch any PDB (1OS6, 5FM7, 4HHB) → 3D
  structure tab; the high-resolution PDBs come from X-ray.
- **Glossary** → search *X-ray crystallography*, *Resolution
  (Å)*, *Phase problem*, *Molecular replacement*, *MicroED*.

Next: **Cryo-EM — atomic resolution without crystals**.
