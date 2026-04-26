# Molecular electronics

**Molecular electronics** uses single molecules — or
small molecular ensembles — as functional electronic
components: wires, switches, rectifiers, transistors,
memory cells. Goal: replace silicon transistors with
molecules at the ultimate (sub-nm) scale.

## The vision

Modern silicon CMOS has reached the angstrom scale (3-5
nm gate length, ~ 50 atoms across). Pushing further
requires fundamentally different platforms — molecular
electronics is one candidate.

A single molecule could:

- Be a wire (~ 1 nm long).
- Switch on/off via chemistry.
- Store information by tautomerising or redox.
- Compute via electron-flow logic gates.

## Building blocks

### Molecular wires

A π-conjugated rod with metal-binding endpoints (e.g.
thiols for Au):

```
HS — (π conjugated chain) — SH
        ↑                       ↑
        Au electrode         Au electrode
```

Examples:

- **Oligothiophene rods** — 10-15 monomers; conductive at
  ~ 10⁻⁸ S.
- **Oligo(phenyleneethynylene) (OPE)** — modular,
  versatile.
- **Carotenoid rods** — natural conjugated chain.
- **DNA + dsDNA** — π-stacking gives some conduction.

### Molecular switches

Photo-switchable groups embedded in a wire:

- **Diarylethenes (dithienylethene)** — open / closed
  forms; UV to close, vis to open. > 10⁴ switching
  cycles.
- **Azobenzene** — E/Z isomerisation by UV / heat.
- **Spiropyran ↔ merocyanine** — photochromic.

### Molecular rectifiers (diodes)

Aviram-Ratner (1974) proposed: donor-acceptor molecule
(e.g. TTF-σ-TCNQ) between two electrodes → asymmetric
I-V curve.

Modern: realised in 2009 (Au electrode + ferrocene-tetra-
phenyl-quinone-Au).

### Molecular transistors

Three-terminal device where a "gate" molecule modulates
current through a "channel". Demonstrated in single-
molecule transistors with cobalt-coordination chemistry
+ electrostatic gating.

## Measurement methods

### Mechanically controllable break junction (MCBJ)

A metallic wire fractured under a piezo to a single-atom
contact, then a molecule trapped between the broken ends.
Conductance measured.

### Conductive AFM (cAFM)

AFM tip pressed against a self-assembled monolayer (SAM)
of molecules; current flows through one or few molecules.

### STM-BJ (Scanning Tunnelling Microscope Break Junction)

Tap the STM tip onto a substrate to form a junction; pull
back gradually; molecules trap between tip + substrate.
Histogram of conductance plateaus identifies molecular
conductance.

### Single-molecule transistor (SMT)

Lithographically defined source + drain on a substrate
with nanogap; molecule deposited from solution; gate
electrode underneath. Multiple groups (Reed, Park,
Tao, Venkataraman) demonstrated.

## Conductance ranges

Molecular conductance G measured in S (Siemens):

| System | G (S) |
|--------|-------|
| Single Au atom (Au-Au quantum point contact) | G₀ = 7.7 × 10⁻⁵ |
| Single CO₂ molecule | < 10⁻¹² |
| Single benzene-1,4-dithiol | ~ 10⁻⁵ |
| Oligo-thiophene (10-mer) | ~ 10⁻⁸ |
| dsDNA 10-bp | 10⁻⁹ |
| Ferrocene-Au | ~ 10⁻⁴ |

## Interpretation: tunnelling vs hopping

Two regimes:

- **Tunnelling** (short molecules, < 3 nm): exponential
  decay of conductance with length: G ∝ e^(-βL).
- **Hopping** (long molecules, > 5 nm): linear decay; G ∝
  1/L (ohmic).

Determines which molecular wire designs scale.

## Single-molecule chemistry tools

Beyond electronics, molecular junctions enable:

- **Single-molecule reaction studies** — observe one
  reaction event at a time.
- **Single-molecule force spectroscopy** (AFM, optical
  trap) — measure bond rupture forces (~ 100-500 pN).
- **Single-molecule fluorescence + plasmonics** — combine
  optical + electrical readout.

## Industrial uses

Limited as of 2025:

- **DNA computing prototypes** — academic research.
- **Memristor + organic memory** — emerging in some
  niche applications.
- **Single-molecule biosensors** — Biological Dynamics +
  others working on cancer-diagnostic platforms.

## Limits

- **Reproducibility** — molecule-by-molecule variability
  makes scaling hard.
- **Stability** — most molecules degrade within days at
  rt; not viable for commercial devices yet.
- **Fabrication** — placing molecules in defined
  positions over a chip = unsolved at scale.
- **Comparison to Si CMOS** — 50-year head-start;
  molecular electronics not ready to replace.

## Try it in the app

- **Glossary** → search *Molecular electronics*, *Single-
  molecule junction*, *STM break junction*, *AFM*,
  *Photoswitch*, *Diarylethene*.

Next: **Spintronic molecules**.
