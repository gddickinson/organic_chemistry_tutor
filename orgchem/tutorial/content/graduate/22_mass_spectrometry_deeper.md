# Mass spectrometry deeper — ionisation, analysers, ion mobility

The beginner MS lesson covered EI fragmentation + the
molecular ion. This lesson goes into modern MS: how
different ionisation methods open different applications,
how analyser physics determines mass accuracy, and what
ion mobility adds to the toolkit.

## Ionisation methods

### Electron ionisation (EI)

70 eV electron beam knocks off an electron from the
neutral analyte → radical cation M⁺•. **Hard** (lots of
fragmentation). Used for small organic molecules + GC-MS
because the spectra are reproducible enough for library
matching (NIST EI library: > 350 000 spectra).

### Chemical ionisation (CI)

Reagent gas (CH₄, NH₃, isobutane) → CH₅⁺ → proton-
transfer to analyte → soft ionisation, [M+H]⁺ with little
fragmentation. Often run as a complement to EI on the
same sample.

### Electrospray ionisation (ESI; Fenn, 2002 Nobel)

Liquid stream + high voltage → spray of charged droplets
→ desolvation → gas-phase ions. Soft; multiple charging
of large molecules (proteins → +20, +30, ...). Open standard
for LC-MS, proteomics, drug-metabolite analysis.

### MALDI (Matrix-Assisted Laser Desorption/Ionisation; Tanaka, 2002 Nobel)

Sample co-crystallised with UV-absorbing matrix (CHCA, DHB,
SA) on a metal target → laser pulse → matrix absorbs +
desorbs analyte → ionisation. Singly charged dominant.

Key applications:

- **Protein + peptide MS** — fast (0.5 s per spot, 96 wells).
- **Microbial identification** (Bruker MALDI Biotyper) —
  clinical pathogen ID by ribosomal protein fingerprint.
- **MALDI imaging** — rastering laser across a tissue
  section maps where each m/z occurs.

### Modern soft ionisation

- **APCI (atmospheric pressure CI)** — for low-polarity
  molecules + steroids that ESI doesn't ionise well.
- **APPI (atmospheric pressure photo-ionisation)** — for
  PAHs + lipids.
- **ICP-MS (inductively coupled plasma)** — for elemental
  analysis (heavy metals, isotope ratios).
- **DESI / DART** — open-air desorption ionisation; analyte
  on a surface gets ionised by spray / plasma stream.
  No sample prep.
- **PaperSpray, LESA, REIMS** — point-of-care MS for
  surgery (intraoperative tumour-margin identification)
  + forensics.

## Mass analysers

The analyser separates ions by m/z. Each technology has its
own resolution + accuracy + mass range trade-off.

### Quadrupole

Four parallel rods with RF + DC fields → only ions in a
narrow m/z window pass through. Cheap + robust; resolution
~ 1000-2000; mass accuracy ~ 100 ppm. Used in LC-MS
(triple-quad for SRM quantitation).

### Ion trap

3D Paul trap or 2D linear trap — ions captured in a small
volume + selectively ejected by m/z. Good for MSⁿ
sequential fragmentation experiments. Resolution ~ 10 000.

### Time-of-flight (TOF)

Ions accelerated to fixed kinetic energy → drift through a
field-free flight tube → time-of-flight ∝ √(m/z). Good
mass range (no upper limit), resolution 10 000-100 000
with reflector + multi-pass.

### FT-ICR (Fourier transform ion cyclotron resonance)

Ions trapped in a cell at high B field → orbit at cyclotron
frequency ω = qB/m → induced image current → FT to spectrum.

Resolution **> 1 000 000** at high field (15 T, 21 T).
Mass accuracy < 1 ppm. Slow; used when resolution + accuracy
trump speed (deep proteomics, oil chemistry, lipidomics).

### Orbitrap (Makarov, 2005)

Ions orbit a central spindle electrode + oscillate axially
at frequency ∝ √(1/m) → image current → FT. Resolution
~ 100 000-1 000 000; mass accuracy < 5 ppm. Fast (sub-
second). Now the dominant high-resolution analyser
(Thermo Q Exactive, Orbitrap Eclipse).

## Quadrupole-Orbitrap + Q-TOF

Hybrid analysers combine quadrupole pre-selection with TOF
or Orbitrap measurement → MS² (parent → fragment) +
ultra-high resolution. The workhorse for modern LC-MS
proteomics + drug-metabolite analysis.

## Tandem MS (MS/MS)

Select a parent ion (m/z), fragment it, measure the
products:

- **CID (collision-induced dissociation)** — collide with
  inert gas (Ar, N₂); standard for peptide sequencing.
- **HCD (higher-energy collisional dissociation)** —
  Orbitrap variant; cleaner backbone fragments.
- **ETD (electron transfer dissociation)** — softer; keeps
  PTMs intact; used for phospho/glyco-peptide mapping.
- **UVPD (ultraviolet photo-dissociation)** — 193 nm
  photons; backbone fragmentation of protein at any
  position.

## Ion mobility (IM-MS)

Add a drift cell between source + analyser. Ions drift
through buffer gas under a gentle E field → drift time
correlates with **collision cross-section (CCS)** —
related to ion shape + size.

Applications:

- **Isomer separation** — structural isomers with the same
  m/z but different shapes (linear vs branched, cis vs
  trans, conformers of the same protein).
- **Glycan + lipid isomer characterisation** — same mass,
  different structure → different drift time.
- **Native MS** — protein complexes preserved; CCS
  reports overall shape + assembly state.

Common IMs: **DTIMS** (drift tube), **TWIMS** (Waters
Synapt traveling wave), **TIMS** (Bruker timsTOF), **FAIMS**
(differential mobility, Thermo).

## Mass accuracy + isotope envelopes

For HRMS: report theoretical mass ("calcd C₁₈H₁₆O₃ =
296.1043") + measured mass ("found 296.1041, Δ = 0.7 ppm").
< 5 ppm is publication standard.

The isotope envelope (M / M+1 / M+2 / ...) gives
**molecular formula constraints** — characteristic 3:1
Cl, 1:1 Br, etc.

## Modern frontiers

- **Single-cell MS** — micro-pipette + nano-ESI; metabolite
  + lipid profiles of single tumour cells.
- **Native MS of MDa complexes** — ribosome, viral
  capsids; structural insight without crystals or cryo-EM.
- **Top-down proteomics** — fragment the intact protein
  (no proteolysis) → preserves PTM-stripped patterns.
- **Imaging MS at sub-µm resolution** (MALDI 2 + atomic
  force MS) — drug distribution in tissue, lipid maps in
  membranes.

## Try it in the app

- **Tools → Spectroscopy (IR / NMR / MS)…** → MS tab — see
  monoisotopic mass + M / M+1 / M+2 envelope + EI
  fragments.
- **Tools → HRMS Guesser…** → enter measured mass + ppm
  tolerance → ranked candidate molecular formulas.
- **Tools → Lab analysers…** → look up SCIEX QTRAP 7500,
  Bruker MALDI Biotyper, Thermo Orbitrap Eclipse,
  Bruker timsTOF.
- **Glossary** → search *Mass spectrometry*, *Electrospray
  ionisation (ESI)*, *MALDI*, *FT-ICR*, *Orbitrap*, *Ion
  mobility*.

Next: **Single-molecule fluorescence + super-resolution
microscopy**.
