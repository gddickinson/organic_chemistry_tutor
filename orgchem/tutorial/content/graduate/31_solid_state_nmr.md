# Solid-state NMR

For most NMR, samples are dissolved in a solvent — molecular
motion averages out anisotropic interactions. **Solid-state
NMR (ssNMR)** measures samples that don't dissolve:
polymers, MOFs, pharmaceuticals (polymorphs), bones, wood.

## What's different in solids

In solution, free tumbling averages:

- **Chemical-shift anisotropy (CSA)** — the chemical shift
  is direction-dependent in a rigid molecule.
- **Dipolar coupling** — through-space H-H, ¹H-¹³C
  coupling sums to zero only if isotropic motion.
- **Quadrupolar interaction** (for nuclei with I > ½) —
  large, direction-dependent.

In a solid, none of these average out → spectra are very
broad (kHz–MHz line widths instead of Hz).

## Magic-angle spinning (MAS)

The big trick: spin the sample at the **magic angle**
(54.74° from the magnetic field) at high speed (10-150
kHz). At this angle:

```
3 cos²θ - 1 = 0
```

Average dipolar + CSA contributions to zero. Recovers
narrow lines (~ 100 Hz for ¹³C, similar to solution).

## Key experiments

### Cross-polarisation (CP) MAS

Transfer ¹H magnetisation to dilute spins (¹³C, ¹⁵N) →
boost signal 4× (γ_H / γ_C ratio); also avoid waiting for
slow ¹³C T₁ recovery.

Standard for organic solids: CP-MAS ¹³C spectrum gives
chemical-shift assignments + quantification of crystalline
forms.

### MAS NMR for ³¹P, ²⁹Si, ²⁷Al, ⁵¹V

- ³¹P (100 % natural abundance, I = ½) — phosphate
  rocks + bone + pharmaceuticals + RNA / DNA.
- ²⁹Si — zeolites, silica gels, surfaces.
- ²⁷Al — zeolites, alumina, MAS clay.
- ⁵¹V — vanadium-containing materials.

### Quadrupolar NMR (³⁵Cl, ⁷⁹Br, ¹⁴N, ²H, ²³Na)

Difficult; requires very fast MAS or DOR (double-rotation)
or QCPMG (Carr-Purcell variant for I > ½).

¹⁴N (99.6 % natural abundance, I = 1) — most common N
isotope but quadrupolar. ²H labelling sometimes used as
alternative.

### Solid-state 2D experiments

- **HETCOR** (heteronuclear correlation) — ¹H-¹³C 2D in
  solids; need fast MAS or homonuclear decoupling on ¹H.
- **DARR** (¹³C-¹³C dipolar-assisted rotational resonance)
  — ¹³C connectivity; protein backbone assignment in
  membrane proteins.
- **DNP** (dynamic nuclear polarisation) — pre-polarise
  electrons; transfer to nuclei → 100-1000× signal boost
  for ssNMR.

## Applications

### Pharmaceutical polymorphs

Different crystal forms of an API have different ¹³C shifts
(crystal-environment-dependent). ssNMR is **THE** technique
for distinguishing:

- Form I vs Form II (Cefdinir, ritonavir, ...).
- Anhydrate vs hydrate.
- Cocrystal vs salt.
- Amorphous vs crystalline.

USP sets ssNMR as the gold standard for polymorph
identification.

### Membrane protein structure

When the protein doesn't crystallise + is too large for
solution NMR (> 30 kDa):

- Solid-state NMR with fast MAS + DNP (Aix-Marseille,
  ETH).
- Membrane-embedded GPCRs, ion channels, mechanosensitive
  proteins solved.
- Complementary to cryo-EM.

### Cellulose + biopolymers

Cellulose I (native) vs cellulose II (regenerated)
distinguished by ¹³C ssNMR. Lignin chemistry mapped by
solid-state ¹³C + ²H NMR.

### Battery materials

- ⁷Li ssNMR for Li-ion battery cathode + electrolyte
  characterisation.
- ²⁹Si ssNMR for Si-anode evolution during charge cycle.
- ¹⁹F ssNMR for SEI (solid-electrolyte interphase) layer.

## Software + facilities

- **Bruker TopSpin** — instrument control + processing.
- **NMRPipe + Sparky** — analysis.
- **CASTEP / VASP / Quantum ESPRESSO** — DFT-computed
  ssNMR shifts (compare to experiment for assignment).

Major facilities: Lyon (France), DOE national labs,
ETH Zürich, MIT-Harvard CMR. NHMFL in Tallahassee,
Florida (US national high-field facility) — > 1 GHz NMR.

## Try it in the app

- **Tools → Lab analysers…** → look up Bruker / JEOL ssNMR
  systems (if seeded).
- **Tools → Spectroscopy methods (techniques tab)** → see
  NMR section.
- **Glossary** → search *Solid-state NMR*, *Magic-angle
  spinning*, *Cross-polarisation*, *DNP*, *Polymorph*.

Next: **Hyperpolarised NMR (DNP, PHIP, SABRE)**.
