# NMR theory deeper — relaxation, NOE, coupling, 2D

The beginner NMR lesson covered chemical shift +
multiplicity. This lesson goes into the physics: what NMR
actually measures, how relaxation works, what the NOE +
J-coupling tell you about geometry, and how 2D experiments
(COSY, HSQC, NOESY) decode complex molecules.

## What NMR measures

A nucleus with non-zero spin (¹H, ¹³C, ¹⁵N, ³¹P, ¹⁹F) in a
magnetic field B₀ has a tiny energy splitting between its
spin states:

```
ΔE = γ ℏ B₀
```

where γ is the **gyromagnetic ratio** (nucleus-specific).
For ¹H at 11.7 T (a 500 MHz spectrometer):

- ΔE ~ 10⁻²⁵ J — minuscule.
- Population difference between up + down spins ~ 1 in 10⁵.
- That's the signal you measure.

You apply an RF pulse at the Larmor frequency, tip
magnetisation off-axis, and watch it precess + decay.

## Relaxation — T₁ and T₂

After the pulse, magnetisation returns to equilibrium via
two distinct relaxation channels:

### T₁ — spin-lattice relaxation

How quickly the population difference (longitudinal
magnetisation along B₀) recovers. Driven by molecular
motion at frequencies matching the Larmor frequency.

```
M_z(t) = M_0 [1 − exp(−t / T₁)]
```

T₁ for ¹H in small molecules in solution: 1-10 s. T₁
matters because:

- You must wait ~ 5 × T₁ between pulses for full recovery
  → routine ¹H acquisition needs 5-10 s relaxation delay.
- Tells you about molecular dynamics (large molecules with
  slow tumbling have shorter T₁ at "intermediate" tumbling
  rates).
- Used for **inversion recovery** experiment to measure T₁
  + identify slowly relaxing nuclei.

### T₂ — spin-spin relaxation

How quickly the spin coherence (transverse magnetisation
in the xy plane) decays. Sets the line width:

```
Linewidth (FWHM) = 1 / (π T₂*)
```

T₂* includes T₂ + magnetic-field inhomogeneity. T₂ < T₁
always; for small molecules in solution they're
comparable.

For solids + viscous samples + macromolecules, T₂ is
short (milliseconds) → broad lines. Solid-state NMR uses
magic-angle spinning to narrow them.

## The Nuclear Overhauser Effect (NOE)

When two protons are spatially close (< 5 Å), saturating
one perturbs the other's intensity:

```
NOE intensity ∝ 1 / r⁶
```

So NOE is exquisitely distance-sensitive. Use cases:

- **Stereochemistry of small molecules** — observe NOE
  between specific protons → infer cis vs trans, axial vs
  equatorial.
- **Protein structure determination** — NOESY-derived
  distances + simulated annealing → 3D structure
  (the first NMR structures of proteins were solved this
  way; Wüthrich's 2002 Nobel).

NOE sign depends on tumbling rate:

- **Small molecule (fast tumbling)** — positive NOE
  (peaks gain intensity).
- **Large molecule (slow tumbling, > ~ 1500 Da)** —
  negative NOE.
- **Intermediate (~ 1000 Da)** — NOE crosses zero;
  zero-quantum coherence used (ROESY) to recover signal.

## J-coupling

Through-bond magnetic interaction, transmitted by bonding
electrons. **J** is in Hz, independent of B₀.

### ³J(H-C-C-H) — Karplus equation

```
³J = A cos²(φ) + B cos(φ) + C
```

with empirical constants A ~ 7-10, B ~ -1, C ~ 1. φ is the
H-C-C-H dihedral angle. So:

- φ = 0° → ³J ~ 8 Hz (cis or eclipsed).
- φ = 90° → ³J ~ 1 Hz.
- φ = 180° → ³J ~ 12 Hz (trans or anti-periplanar).

This lets you assign chair conformation in cyclohexane,
proline puckering, glycosidic angles in carbohydrates.

### Larger J for special cases

- ²J(H-C-H) (geminal): -10 to -20 Hz (negative; cancels
  in normal multiplicity).
- ⁴J (W-coupling): 1-3 Hz, observed in rigid systems
  with W-shaped HCCCH path.
- ³J(H-N-H, H-O-H): exchanges away in protic solvents.

## 2D experiments

### COSY (Correlated Spectroscopy)

Maps **scalar coupling**: peaks at (δ_A, δ_B) show H_A and
H_B are coupled (through 1-3 bonds typically).

Walk through a molecule by following the diagonal +
off-diagonal cross-peaks → reconstruct the coupling
network → assign all protons.

### TOCSY (Total Correlation Spectroscopy)

Like COSY but extends to all coupled protons in the same
spin system. Useful for amino acid + sugar identification.

### HSQC (Heteronuclear Single Quantum Correlation)

Maps **¹H-¹³C one-bond connections** (or ¹H-¹⁵N for
proteins). Peak at (δ_H, δ_C) shows the C and the H
attached to it.

The standard ¹³C resolution tool in 2025 — replaces 1D
¹³C in many cases (faster, more sensitive via inverse
detection).

### HMBC (Heteronuclear Multiple Bond Correlation)

¹H-¹³C **two- and three-bond** correlations. Maps which
carbons are 2-3 bonds away from a given proton — connects
quaternary carbons to nearby protons → assign C without
attached H (carbonyl, quaternary aromatic).

### NOESY / ROESY

¹H-¹H **through-space (NOE)** correlations. Cross-peaks
show H_A and H_B are spatially close, regardless of
covalent connectivity. Stereochemistry + 3D structure
determination.

### Modern fast-2D: BIRD, CRINEPT, CYCLOPS

Pulse-sequence improvements that suppress noise + boost
sensitivity. NMR spectroscopy on µg of natural product is
now routine.

## Cryoprobes + DNP — sensitivity

- **Cryoprobes** (cooled to 25 K) — coil + preamplifier
  cold reduces thermal noise → ~ 4× sensitivity gain at
  the cost of a $300 k probe upgrade.
- **DNP (Dynamic Nuclear Polarisation)** — pre-polarise
  electron spins, transfer polarisation to nuclei via μw
  irradiation → 100-1000× signal boost. Bruker's
  HyperSense + Spinsolve DNP-NMR for solid-state +
  metabolomics.
- **Para-hydrogen induced polarisation (PHIP)** + **SABRE**
  — chemical hyperpolarisation for ¹³C metabolic imaging
  in vivo.

## Try it in the app

- **Tools → Spectroscopy (IR / NMR / MS)…** → NMR tab —
  predict ¹H + ¹³C shifts for any SMILES; export stick
  spectrum.
- **Tools → Lab analysers…** → look up Bruker / JEOL /
  Varian NMR + Magritek Spinsolve benchtop systems.
- **Glossary** → search *NMR*, *Chemical shift*,
  *J-coupling*, *NOE (nuclear Overhauser effect)*, *COSY*,
  *HSQC*.

Next: **Mass spectrometry deeper — ionisation, FT-ICR,
Orbitrap, IM-MS**.
