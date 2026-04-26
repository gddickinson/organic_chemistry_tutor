# Absolute configuration determination

For a chiral molecule, the **absolute configuration** is
the actual 3D arrangement of substituents around the
stereocentre — not just the relative stereochemistry of
adjacent centres. Several techniques can answer "is this
the (R)- or (S)-enantiomer?"

## Methods

### 1. Single-crystal X-ray with anomalous scattering (Bijvoet)

The gold standard when applicable:

- Friedel's law: |F(hkl)| = |F(h̄k̄l̄)| for centro-symmetric
  cases.
- **Anomalous scattering** by heavier atoms (S, Br, Se,
  ...) breaks Friedel's law → one enantiomer is
  preferentially absorbing → distinguishable.
- **Flack parameter** quantifies absolute configuration:
  - 0 → correct enantiomer.
  - 1 → inverted (need to invert space group).
  - ~ 0.5 → indeterminate (twinned crystal).
- Modern Cu-Kα radiation gives Flack uncertainty < 0.05 for
  typical organics.

For all-light-atom (only H/C/N/O) compounds, Flack
uncertainty is too high → use Cu radiation or chiral HPLC
+ correlate to a known reference.

### 2. VCD + DFT (chiroptical, no X-ray)

Detailed in lesson 36. Best for compounds without heavy
atoms or that don't crystallise.

Workflow:

1. Measure VCD spectrum.
2. DFT-calculate VCD for both candidate enantiomers
   (cheap; B3LYP / def2-TZVP).
3. Compare; assign matching enantiomer.

### 3. Mosher's method

```
chiral alcohol + (R)- or (S)-MTPA-Cl + base → diastereomeric esters
                                        + ¹H NMR shifts compared
```

(R)-MTPA = α-methoxy-α-trifluoromethyl-α-phenylacetic acid
("Mosher acid"). A small chiral perturbation introduced;
the protons of the alcohol's substituents shift differently
depending on the alcohol's chirality.

```
For Δδ(R - S) > 0 → group is in front of MTPA's plane
For Δδ(R - S) < 0 → group is behind
```

Read off the absolute configuration from the sign pattern.

Variants: **MPA (methoxyphenylacetic acid)** — simpler, less
problematic anisotropy than MTPA.

### 4. ECD + DFT

Electronic CD spectrum (UV-Vis region) calculated by TD-DFT
+ compared to experiment. Easier than VCD — most
spectrometers do CD already.

Cytochrome P450-style chromophores + steroid +
flavonoid + alkaloid molecules use ECD routinely.

### 5. Microcrystal electron diffraction (MicroED)

For substrates that don't form macroscopic crystals (lesson
24). Bijvoet-like analysis on micro-crystals.

### 6. Chiral chromatography + correlation

```
chiral HPLC: (R)-eluting at 5 min; (S)-eluting at 7 min
```

Order on a known column (Chiralpak AD-H, etc.) is
reproducible. Run the unknown + a synthesised
reference of known config; identical retention →
same enantiomer.

### 7. Optical rotation correlation

[α]_D vs literature value. Sign + magnitude:

- (R)-(+)-camphor [α]_D = +44° (lit.)
- Your synthesised compound: [α]_D = +42° → likely (R).

Caution: solvent + concentration affect [α]_D; use the
same solvent + closely matched [α]_D.

### 8. Synthesis from known reference

Build the chiral compound from a chiral starting material
of known config. The synthetic route should preserve or
controllably invert; final config follows.

This is the historical basis for many natural-product
absolute-config assignments.

### 9. Enzymatic resolution + correlation

Some enzymes prefer one enantiomer (lipases for one
hand of a secondary alcohol). Use enzyme + monitor → the
slow-reacting enantiomer is the (R)- or (S)-form by
literature precedent.

## Integration

Often multiple methods used together:

- **Final**: X-ray (heavy-atom or MicroED).
- **Quick**: chiral HPLC + correlation.
- **No crystal**: VCD or ECD + DFT.
- **Standard**: Mosher's for alcohols + amines.

## When absolute config matters

- **API filings** — FDA requires > 99 % ee + assigned
  absolute config.
- **Natural product structure** — most journals require
  absolute-config assignment (X-ray, VCD, or chemical
  correlation).
- **Asymmetric methodology** — every new asymmetric reaction
  needs ee + absolute config.
- **Chiral receptor binding** — different enantiomers may
  have very different bio activity (thalidomide; the
  classic).

## Try it in the app

- **Tools → Stereochemistry…** → input chiral SMILES → see
  R/S assignment + flip enantiomer.
- **Tools → Isomer relationships → Classify pair** → check
  R vs S relationship.
- **Glossary** → search *Absolute configuration*, *Bijvoet
  method*, *Flack parameter*, *Mosher's method*, *VCD*,
  *Chiral HPLC*.

Next: **Computational catalyst design**.
