# Vibrational circular dichroism + chiroptical methods

Beyond NMR + X-ray, **chiroptical spectroscopy** measures
how chiral molecules interact with circularly polarised
light. Several techniques each give different views of
chirality:

- **ORD (Optical Rotatory Dispersion)** — rotation vs λ.
- **CD (Circular Dichroism)** — Δε vs λ.
- **VCD (Vibrational CD)** — CD in IR region.
- **ROA (Raman Optical Activity)** — same idea for Raman.

## Specific rotation [α]_D

The classical measure:

```
[α] = (observed rotation in degrees) / (concentration × path length)
[α]_D = at 589 nm (sodium D line), ° dm⁻¹ g⁻¹ mL
```

Reported for chiral compounds:

```
(R)-(+)-glyceraldehyde:    [α]_D = +14°
(R)-(+)-camphor:           [α]_D = +44°
(S)-(-)-naproxen:          [α]_D = -65°
(R)-(+)-CSA-OH:            [α]_D = +21°
```

Sign + magnitude depend on solvent + concentration; report
both.

## ORD vs CD

**ORD** is rotation vs wavelength; CD is the differential
absorption of left vs right circularly polarised light.
CD is more diagnostic.

A CD signal appears in the same UV-Vis region as the
chromophore's absorption — protein α-helix gives a
characteristic positive CD at 195 nm + negative CD at
208 + 222 nm.

## CD applications

- **Protein secondary-structure** — CD spectra distinguish
  α-helix, β-sheet, random coil; quantify by
  curve-fitting.
- **Drug-DNA binding** — induced CD when achiral drug binds
  chiral DNA.
- **Liquid-crystal helix sense** — cholesteryl liquid
  crystals.
- **Enantiomeric excess** — CD intensity ∝ ee for known
  reference; rapid screening.

## VCD — vibrational fingerprint of chirality

Combines IR (vibrational) + CD (chiral discrimination):

- Each functional group has a characteristic VCD signature.
- Doesn't require single-crystal X-ray to assign absolute
  configuration.
- Computationally predictable — DFT calculation of VCD
  spectra confirms assignment.

Workflow:

1. Measure VCD of unknown.
2. Compute VCD of (R)- + (S)-candidate enantiomers.
3. Match to assign absolute configuration.

By 2025, this is the **non-X-ray gold standard** for
absolute configuration of low-MW natural products.

## Equipment + practice

- **Bruker Vertex70 + PMA50** — VCD module add-on.
- **JASCO J series** — combined CD + VCD.
- **Sample**: 50-100 mg in CDCl₃ or d⁶-DMSO; path 50-100
  µm; ~ 4 hours acquisition.

VCD signals are 10⁻⁴-10⁻⁵ of the parent IR signal —
need long acquisition, high-quality sample.

## ROA — Raman optical activity

Same chirality discrimination but in Raman spectrum.
Advantages over VCD:

- Aqueous samples (no D₂O needed).
- Lower wavenumber range (200-2000 cm⁻¹) — captures
  skeletal modes.
- Sensitive to backbone conformation in proteins +
  carbohydrates.

ROA was a niche field until ~ 2010; now a mainstream tool
for biomolecule characterisation alongside CD + VCD.

## Choosing the right method

| Goal | Method |
|------|--------|
| Quick check chiral / racemic | [α]_D (cheap, fast) |
| Protein 2° structure | CD (UV-Vis) |
| Absolute config of small molecule | VCD + DFT |
| ee determination | chiral HPLC + CD detector |
| Aqueous biomolecule | ROA |
| High-throughput SAR ee | CD plate reader |

## Modern uses

- **Amino acid + sugar enantiomer purity** for SPPS or
  glycoprotein synthesis.
- **Asymmetric synthesis** — assign new chiral catalysts'
  selectivity by chiral product CD.
- **Drug enantiomer** quality control (ee specs in API
  must be > 99 %).
- **Liquid-crystal chirality** — helical-pitch
  measurements.

## Try it in the app

- **Tools → Lab analysers…** → look up JASCO / Bruker
  CD / VCD spectrometers.
- **Tools → Spectrophotometry methods → CD section**.
- **Glossary** → search *Specific rotation*, *Optical
  rotation*, *Circular dichroism*, *VCD*, *ROA*,
  *Chiroptical*.

Next: **Absolute configuration determination methods**.
