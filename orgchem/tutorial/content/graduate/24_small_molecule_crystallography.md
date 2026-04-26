# Small-molecule crystallography — CSD, polymorphs, MicroED

The graduate X-ray-crystallography lesson focused on
proteins. This lesson is the other half: **small-molecule
crystallography**, the workhorse for chemists. The Cambridge
Structural Database (CSD) holds > 1.2 million single-crystal
structures by 2025; almost every published organic compound
gets crystallised + characterised at some point in
methodology + total synthesis work.

## Why small-molecule crystallography matters

- **Confirm structure + connectivity** — 100 % unambiguous
  vs NMR + MS combined.
- **Confirm stereochemistry** — absolute configuration via
  anomalous scattering (Bijvoet method).
- **Polymorph identification** — different crystal forms
  of the same compound have different bioavailability,
  stability, IP coverage.
- **Cocrystal formation** — pharmaceutical formulation +
  drug improvement.
- **Reaction product identification** — final proof for
  natural-product structure + total-synthesis target.

## The crystallisation challenge

Getting a good single crystal is the bottleneck:

- **Slow evaporation** — dissolve in a single solvent,
  cap loosely, evaporate over days to weeks. Most
  reliable.
- **Vapour diffusion** — solute in a beaker inside a
  larger beaker holding poor-solvent vapour (e.g. DCM
  inside hexane).
- **Cooling crystallisation** — heat solution to dissolve,
  let cool slowly.
- **Seeding** — drop in a tiny crystal of the same compound
  to initiate growth.
- **Solvent screening** — an affordable robot screens 96
  conditions in 1 day. Common in pharma polymorph
  screening (cocrystal forms + salt forms count too).

## The data collection

Modern small-molecule diffractometer:

- **Source**: Mo Kα (λ = 0.71 Å), Cu Kα (λ = 1.54 Å),
  rotating anode or microfocus sealed tube.
- **Goniometer**: kappa or Eulerian, 4-circle.
- **Detector**: Pilatus / Bruker Photon CMOS / Hybrid Pixel.
- **Cryo cooler**: 100 K is standard (improves data; freezes
  thermal motion).

A typical structure: 50 000-200 000 reflections collected
in 0.5-12 hours; resolution to 0.7-1.0 Å. R₁ < 5 %, wR₂
< 12 % for well-behaved structures.

## Software

- **APEX 4 / X-DUO** (Bruker) — collection + processing.
- **CrysAlisPro** (Rigaku Oxford Diffraction) — same role.
- **OLEX2** — free GUI; integrates with SHELXL refinement.
- **SHELX suite** (Sheldrick) — gold-standard structure
  solution + refinement; SHELXT for solution, SHELXL for
  refinement.
- **Mercury** (CCDC) — free visualisation + analysis.
- **PLATON** — automated checks; H-bond analysis; void
  detection.

## What gets reported (CIF file)

A Crystallographic Information File (CIF) is the standard
deposition format containing:

- Cell parameters (a, b, c, α, β, γ).
- Space group + symmetry operators.
- Atomic coordinates + displacement parameters.
- Bond lengths + angles (with standard uncertainties).
- Hydrogen-bond table.
- Refinement statistics.

A "publication-quality" CIF passes **CheckCIF / IUCr
validation** with no Level A or B alerts.

## Polymorphism

Different crystal forms of the same chemical entity. The
classic disasters:

- **Ritonavir** (Norvir, Abbott, 1998) — 2 years after
  launch, a previously unseen Form II crystallised globally
  + had ~ 25 % the bioavailability. Half of Abbott's
  inventory was useless. Cost > $250 M to redesign.
- **Cefdinir** (Omnicef) — multiple polymorphs; only
  Form 1 is on the market.
- **Caffeine** — 2 anhydrous + several hydrates known.

Pharma polymorph screening:

- Solvent screen (50-200 solvents).
- Anti-solvent crystallisation.
- Cooling crystallisation at multiple rates.
- Vapour diffusion.
- Slurry conversion.
- Mechanical milling (LAG).

Patent ALL forms found. The "form-of-the-month" race.

## Cocrystals

Two distinct molecular entities held together by H-bonds /
π-stacking + crystallised together:

- **Carbamazepine + saccharin cocrystal** — improves
  carbamazepine solubility 3× while keeping its anti-
  epileptic activity.
- **Ibuprofen + nicotinamide** — better dissolution.
- **Coformer libraries** — pharmacopeia-approved coformers
  used to optimise drug forms.

Cocrystals are NOT salts (no proton transfer). The boundary
is sometimes ambiguous (Δ pKa < 3 → cocrystal; > 3 → salt).
ICH guidelines + FDA recognise cocrystals as a separate
patentable class.

## Absolute configuration

Bijvoet method: **anomalous scattering** by heavier atoms
(S, Br, Se, ...) breaks Friedel's law (|F(hkl)| ≠ |F(h̄k̄l̄)|)
→ direct readout of absolute hand. Reported as **Flack
parameter** (0 = correct enantiomer, 1 = inverted, ~ 0.5 =
indeterminate).

For all-light-atom organic molecules (only H/C/N/O), Flack
uncertainty is too high → use Cu radiation or chiral
HPLC + correlate to a known reference.

## MicroED — micro-crystals

For natural products that don't form macroscopic crystals
(< 1 µm), **MicroED** (microcrystal electron diffraction,
Gonen / Nannenga 2013) uses a TEM operating in diffraction
mode. Single tiny crystal (often a powder) → 1° tilt
series of diffraction patterns → solve like X-ray.

Notable wins (since 2013):

- Multiple natural-product structures from amorphous
  powders.
- Drug-screening fragment hits when only crystallised on
  the protein, not by themselves.
- New polymorphs of common drugs (paracetamol Form III).

## Try it in the app

- **Tools → Lab analysers…** → look up Bruker D8 + Rigaku
  XtaLAB single-crystal diffractometers.
- **Glossary** → search *X-ray crystallography*, *CIF*,
  *Polymorphism*, *Cocrystal*, *Flack parameter*,
  *MicroED*.

Next: **Quantum mechanics primer for chemists**.
