# Single-molecule fluorescence + super-resolution microscopy

For most of optical microscopy's history the **diffraction
limit** (λ/2NA ~ 200 nm for visible light) was an absolute
ceiling. Modern fluorescence techniques broke that limit +
opened single-molecule sensitivity, enabling biology to be
observed one molecule at a time. The 2014 Nobel Prize
(Betzig + Hell + Moerner) recognised the breakthroughs.

## Single-molecule fluorescence

A single fluorophore emits ~ 10⁵-10⁶ photons before
photobleaching. With a sensitive detector (EM-CCD, sCMOS,
single-photon avalanche diode SPAD) you can detect
individual events.

### TIRF (Total Internal Reflection Fluorescence)

Light enters a coverslip at > critical angle → total
reflection → only an evanescent wave (~ 100 nm) penetrates
into the sample → only fluorophores at the interface
fluoresce → high signal-to-background.

Used for:

- **Single-molecule tracking** of membrane receptors.
- **DNA polymerase / single-molecule kinetics**.
- **Immunological synapse formation**.

### smFRET (single-molecule FRET)

Two fluorophores attached to the same molecule (donor +
acceptor) → distance between them → FRET efficiency.

```
E_FRET = 1 / (1 + (r/R₀)⁶)         R₀ ≈ 5-10 nm
```

Sensitivity: 1-10 nm range. Watch single-molecule
conformational changes:

- Protein folding transitions.
- Ribosome translocation.
- DNA-polymerase fidelity.
- Riboswitch ligand binding.

### MINFLUX (Hell, 2017)

Single-molecule localisation with **< 1 nm precision** —
near the size of a small molecule. Uses a doughnut-shaped
excitation beam; localisation precision improves with
proximity to zero-intensity centre. Cutting-edge.

## Super-resolution microscopy — three families

The diffraction limit was bypassed by three broad
strategies:

### 1. Stimulated emission depletion (STED, Hell 1994)

Two laser beams: an excitation Gaussian + a depletion
doughnut. The doughnut **stimulates emission back to
ground state** for fluorophores at the periphery, leaving
only those at the doughnut's hole to fluoresce → effective
PSF shrinks.

Resolution: ~ 30-50 nm in xy; live-cell compatible.

### 2. Single-molecule localisation microscopy (SMLM): PALM / STORM (Betzig + Hess + Zhuang)

**PALM (photoactivated localisation microscopy)** uses
photoactivatable fluorescent proteins (PA-GFP, PA-mCherry).
Activate a sparse subset → image individual molecules →
localise each to ~ 10 nm (the centroid is much sharper
than the PSF) → bleach + repeat → reconstruct image from
millions of localisations.

**STORM (stochastic optical reconstruction microscopy)**
same idea but uses small-molecule dyes (Alexa, Cy) that
blink between dark + emissive states under chemical
buffer + laser.

Resolution: ~ 10-20 nm xy; multiple wavelengths
(2-colour, 3-colour for protein-protein co-localisation).

### 3. Structured illumination microscopy (SIM, Gustafsson)

Project a **stripe pattern** onto the sample at multiple
orientations. Sample's high-frequency information aliases
into the imaging-band → recover by FT processing. Resolution:
~ 100 nm; live-cell compatible; no special fluorophores.

## Specialised platforms

- **Lattice light-sheet** — illuminate a thin sheet from the
  side → fast 3D imaging with low photo-toxicity. Live
  embryo development at sub-cellular resolution.
- **Expansion microscopy** (Boyden) — embed sample in
  swelling polymer gel → physically expand 4-10× → image
  on a regular confocal as if it had super-resolution.
- **Adaptive optics** — correct for sample-induced
  aberrations → routine sub-100-nm in tissue.
- **FCS / FCCS (fluorescence correlation spectroscopy)** —
  diffusion + binding kinetics from intensity fluctuations
  in a small focal volume.

## Fluorophore design

The fluorophore IS the experiment in many cases:

- **Photoactivatable / photoswitchable** — PA-GFP,
  Dronpa, mEos.
- **Bright + photostable** — Alexa Fluor, Atto, Janelia
  Fluor (JF dyes — Lavis, photoacid system).
- **Self-labelling tags** — SNAP-tag, Halo-tag, CLIP-tag
  → genetic targeting + small-molecule fluorophore choice.
- **Voltage / Ca²⁺ / pH-sensitive** — GCaMP family for Ca²⁺
  imaging in neurons; ASAP / Ace2N for voltage.
- **Bioorthogonal labelling** — click chemistry (azide /
  tetrazine) attaches fluorophore via genetically encoded
  bioorthogonal handle.

## Single-molecule sequencing

Beyond optical:

- **Nanopore sequencing** (Oxford Nanopore PromethION) —
  single DNA / RNA / protein molecule threaded through a
  protein nanopore; current changes encode the sequence.
- **Nanopore protein sequencing** — emerging; needs better
  AA discrimination + reduces translation steps.
- **Zero-mode waveguides + PacBio** — single-molecule
  DNA polymerase + zeptolitre well + fluorescent
  nucleotides → real-time sequencing.

## Applications

- **Synaptic structure** — STORM revealed the active zone
  + post-synaptic density at 20-nm resolution.
- **Mitochondrial cristae** — STED + 3D-SIM mapped the
  cristae architecture in living cells.
- **DNA repair complexes** — assembly + disassembly tracked
  in live cells.
- **Drug receptor interactions** — single-molecule binding
  + dissociation of GPCRs on neurons (Drug screening at
  single-molecule resolution).

## Try it in the app

- **Microscopy tab** (if seeded) → look at STORM / PALM /
  STED / MINFLUX entries — resolution + sample types +
  representative instruments.
- **Tools → Lab analysers…** → look up Zeiss Lattice
  Lightsheet 7, Zeiss LSM 980, Bruker / Vutara STORM.
- **Glossary** → search *Super-resolution microscopy*,
  *STED*, *STORM*, *PALM*, *FRET*, *Single-molecule
  fluorescence*.

Next: **Crystallography of small molecules — CSD,
polymorphs, ChemDraw**.
