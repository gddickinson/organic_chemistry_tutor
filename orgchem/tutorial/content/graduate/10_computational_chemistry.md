# Computational chemistry & DFT essentials

A modern organic-chemistry paper without a calculated transition-
state energy is increasingly rare.  Computational chemistry no
longer lives in the theory department; it's a routine bench tool
that complements NMR, IR, and X-ray crystallography in ranking
mechanistic hypotheses + predicting reaction outcomes.

## Two paradigms: wavefunction vs density

**Wavefunction methods** (Hartree-Fock, MP2, CCSD(T)) solve for
the many-electron wavefunction Ψ.  The exact Ψ for an N-electron
molecule is a 3N-dimensional object — computationally
prohibitive past ~ 20 atoms.  Hartree-Fock approximates Ψ as a
single Slater determinant of one-electron orbitals + ignores
electron correlation; post-HF methods (MP2, CCSD(T)) systematically
re-introduce correlation but scale brutally (CCSD(T) is O(N⁷)).

**Density-functional theory (DFT)** sidesteps the wavefunction by
working with the electron density ρ(r) — a 3D object regardless
of N.  The **Hohenberg-Kohn theorems** (1964, Nobel 1998 to Kohn)
prove that ρ(r) uniquely determines the system's ground-state
energy + every observable.  The **Kohn-Sham equations** then
turn the many-body problem into a set of one-body problems on
non-interacting electrons + a magic **exchange-correlation
functional** that absorbs all the many-body physics.

DFT scales O(N³) — about 100 × cheaper than CCSD(T) for the same
system size — making it the default workhorse for organic
chemistry.

## The functional zoo

The exchange-correlation functional E_xc[ρ] is exact in
principle but unknown in practice.  Approximations form a
**Jacob's ladder** of accuracy + cost:

1. **LDA** (local density approximation) — uses ρ(r) only.
   Crude; overbinds bonds, underestimates barriers.  Almost
   never used for organic molecules.
2. **GGA** (generalised gradient approximation) — adds ∇ρ(r).
   PBE, BLYP.  Reasonable geometry, moderate energetics.
3. **meta-GGA** — adds ∇²ρ + kinetic-energy density τ.  M06-L,
   r²SCAN.
4. **Hybrid** — mixes a fraction of exact HF exchange with the
   DFT functional.  **B3LYP** (20% HF + Becke 88 + LYP, 1993)
   is the most-cited functional in chemistry — > 100 000
   citations as of writing.  Modern hybrids: ωB97X-D, M06-2X.
5. **Double hybrid** — adds an MP2-style correlation term.
   B2PLYP, ωB97M(2).  Approaches CCSD(T) accuracy at GGA cost
   for many systems.

**Practical default for organic chemistry**: **ωB97X-D / def2-TZVP**
or **M06-2X / 6-31+G(d,p)** for thermochemistry + barriers;
**B3LYP / 6-31G(d)** as a fast first pass.  **r²SCAN** is the
2020s rising-star meta-GGA — nearly hybrid accuracy without the
HF-exchange cost.

## Basis sets

A **basis set** is a finite set of atom-centred functions used
to represent the molecular orbitals.  Bigger = better but more
expensive.  Two main families:

- **Pople** (e.g. **6-31G(d,p)**) — split-valence; the workhorse
  of the 1990s + 2000s.  Naming: `[core]-[valence-split](polarisation)`
  → 6-31G(d) = 6 inner-shell GTOs, valence split 3+1, d-polarisation
  on heavy atoms; (d,p) adds p-polarisation on H.
- **Dunning** correlation-consistent (e.g. **cc-pVDZ**, **cc-pVTZ**,
  **cc-pVQZ**) — designed for systematic convergence to the
  basis-set limit.  cc-pVTZ is the modern default for accurate
  energetics; cc-pVDZ is the cheap-and-acceptable fallback.
- **Karlsruhe** (e.g. **def2-SVP**, **def2-TZVP**, **def2-QZVP**) —
  designed for DFT.  **def2-TZVP** is the modern default for
  ωB97X-D / r²SCAN calculations on organic molecules.

For anionic species or **diffuse-electron problems** (e.g.
hydrogen-bond + excited-state work), add **diffuse functions** —
6-31+G(d,p) or aug-cc-pVTZ.  For radicals + open-shell systems,
add diffuse functions + use UHF / UKS.

## What we use computational chemistry for

- **Geometry optimisation** — relax to a local minimum on the
  potential-energy surface.  Output: bond lengths, angles,
  dihedrals.  Useful for confirming a tentative structure +
  for the input geometry to higher-level single-point energies.
- **Transition-state finding** — locate the saddle point
  between reactant + product.  Two main techniques:
  **eigenvector following** (start near a TS guess, climb the
  Hessian's lowest mode) + **nudged elastic band (NEB)**
  (interpolate intermediate images + relax them all jointly).
  Verify with an **IRC** (intrinsic reaction coordinate) walk
  that the TS connects the right reactant + product.
- **Thermochemistry** — vibrational analysis at a stationary
  point gives ZPE, thermal corrections, and an estimate of S°
  (enthalpy + entropy at 298 K).  Combine with single-point
  energies to get ΔG° = ΔH° - TΔS°.  An Eyring-equation rate
  constant follows: k = (k_B T / h) · exp(−ΔG‡ / RT).
- **NMR prediction** — **GIAO** (gauge-including atomic
  orbitals) DFT predicts ¹H + ¹³C chemical shifts to ± 0.2-0.4
  ppm + 1-3 ppm respectively; sufficient to distinguish
  structural isomers.  See the seeded `core/nmr.py` for the
  rule-based teaching version.
- **IR prediction** — harmonic vibrational frequencies (scaled
  by ~ 0.96 for B3LYP) match experiment to ± 30 cm⁻¹.
- **Excited-state work** — TDDFT predicts UV-Vis transitions +
  fluorescence wavelengths.  Critical for photoredox catalysis
  (round-198 lesson) + photoswitch design.
- **pKa prediction** — thermodynamic-cycle approach: ΔG_aq for
  the deprotonation (computed via gas-phase ΔG + solvation
  ΔG_solv) → pKa = ΔG_aq / (RT ln 10).  Accurate to ± 1 pKa
  unit with explicit-solvent corrections.

## Implicit solvent

For solution-phase work, embed the solute in a **polarisable
continuum model (PCM)** that treats the solvent as a dielectric
continuum (water ε = 80).  Variants: **C-PCM** (default for most
codes), **SMD** (a more sophisticated parameterisation that
accounts for non-electrostatic effects — preferred for pKa +
solvation-energy work).  The molecule sits in a cavity carved
from atomic radii; the surrounding dielectric polarises in
response.

For **explicit solvation** of specific hydrogen bonds, add 1-5
explicit waters around hydrogen-bond donors + acceptors before
adding the PCM continuum — gives ~ 0.5 pKa unit improvement on
acid-base + many transition states.

## Software ecosystem

- **Gaussian** — the commercial standard since the 1980s.
  Excellent algorithms; expensive licence.
- **ORCA** — free for academia, fast, modern algorithms,
  excellent for DFT + DLPNO-CCSD(T).  Modern preferred default
  for academic work.
- **Q-Chem** — fast, modern, commercial.
- **Psi4** — open-source, Python-driven, growing ecosystem.
- **CP2K** — solid-state + condensed-phase periodic DFT.
- **TeraChem** — GPU-accelerated, fastest for large molecules.

## Modern ML potentials

The 2020s brought **ML potentials** that approximate the
DFT potential-energy surface with neural networks trained on
millions of DFT calculations.  **ANI-2x** (Smith et al.),
**AIMNet2**, **MACE-OFF23** all give DFT-level accuracy at
forcefield-level cost (~ 10⁵ × speed-up).  Suitable for routine
geometry optimisation + conformer generation; less reliable
near transition states.

These are starting to displace classical force fields for
medium-accuracy work + accelerating the reaction-discovery loop.

## How computational chemistry connects to the rest of the
curriculum

Computational chemistry is the **quantitative complement** to
classical mechanism analysis:

- The Phase-13 reaction-coordinate diagrams + Phase-14a Hückel
  MOs + Phase-14b Woodward-Hoffmann rules are all **qualitative
  versions** of what DFT computes quantitatively.
- The Phase-198 photoredox lesson's "excited-state redox
  potentials" are TDDFT outputs.
- The Phase-204 enzyme-catalysis transition-state-mimic
  drug-design strategy works because we can now compute the
  TS structure + design molecules that resemble it.

The right modern workflow is **iterative**: a chemist sketches
mechanisms with arrows + classical reasoning, then asks the
computer to confirm (or refute) by computing the predicted ΔG‡
of the proposed pathway.  When experiment and computation agree,
confidence in the mechanism is high; when they disagree, you
have a paper to write.

## Try it in the app

- **Tools → Spectroscopy** — predict ¹H + ¹³C NMR shifts via
  rule-based tables.  The DFT GIAO approach would give better
  numbers but is out of scope for a teaching tool.
- **Tools → Orbitals** — Hückel MOs for π-systems are a
  textbook taste of what DFT does for any molecule.
- **Reactions tab** — every seeded reaction has an energy
  profile (ΔG‡ + ΔG_rxn) calculated at standard DFT levels;
  the *Energy profile…* dialog renders these as Bezier-smoothed
  reaction-coordinate diagrams.

## Further reading

- Cramer, C. J. *Essentials of Computational Chemistry*
  (2nd ed., 2004) — the textbook.
- Bursch, M.; Mewes, J.-M.; Hansen, A.; Grimme, S. (2022)
  "Best-practice DFT protocols for basic molecular
  computational chemistry" *Angew. Chem. Int. Ed.* **61**,
  e202205735.  The 2022 modern-defaults paper — read this
  before running ANY new DFT calculation.
- Smith, J. S. et al. (2017) "ANI-1: an extensible neural
  network potential…" *Chem. Sci.* **8**, 3192.  The
  founding ML-potential paper.

Next: The graduate-tier curriculum is now wide-ranging
(photoredox / click chemistry / enzyme catalysis /
computational chemistry).  The intermediate tier still has
gaps — supramolecular chemistry + organocatalysis + heterocyclic
chemistry would all benefit from dedicated lessons.
