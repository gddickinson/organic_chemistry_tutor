# EPR spectroscopy — for unpaired electrons

**Electron paramagnetic resonance (EPR / ESR)** is the
electron version of NMR — it detects unpaired electrons +
their environments. Used for radicals, transition-metal
complexes, defects in materials, biomolecular cofactors.

## Why EPR

NMR detects nuclear spins; EPR detects electron spins.
Differences:

| | NMR | EPR |
|----|-----|-----|
| Frequency at 1 T | 42.6 MHz (¹H) | 28 GHz |
| Sensitivity | low (~ µM at high field) | very high (~ nM at high field) |
| Common operating field | 7-23 T | 0.34 T (X-band ~ 9 GHz) |
| Linewidth | Hz | MHz - GHz |
| Sample state | liquid + solid | mostly solid / frozen solution |
| Required species | nuclear spin | unpaired electron |

EPR is the only spectroscopic method specifically tuned
to unpaired electrons; lots of unique chemistry visible.

## Operating principle

Electron in B field has 2 spin states (m_s = ±½). RF
absorption at:

```
ν = g μ_B B / h
```

g = the **g-factor**:

- Free electron: g = 2.0023.
- Organic radicals: g ≈ 2.00 (close to free).
- Transition metals: g varies widely (1.9-9 depending on
  geometry + d-electron count).
- Heavy-element radicals: g shifts more from 2.00 (spin-
  orbit coupling).

## Hyperfine coupling

Unpaired electron's interaction with nearby nuclear spins
splits the EPR signal:

```
hyperfine A = electron-nuclear coupling, in MHz or Gauss
```

Common couplings:

- ¹H (I = ½): each H gives 2 lines.
- ¹⁴N (I = 1): each N gives 3 lines.
- ⁵⁵Mn (I = 5/2): 6 lines.
- ⁵⁹Co (I = 7/2): 8 lines.

Pattern + magnitude tells you which nuclei are near the
unpaired electron + how delocalised it is.

## Common EPR experiments

### CW-EPR (continuous wave)

Standard 1D EPR spectrum (g, A); used for routine spin
counting + radical identification.

### Pulse EPR (ENDOR, ESEEM, HYSCORE, DEER)

- **ENDOR** — combines NMR + EPR in one experiment;
  precise nuclear hyperfine measurements.
- **ESEEM** — electron spin echo envelope modulation;
  weak couplings to remote nuclei.
- **HYSCORE** — 2D ESEEM; resolves overlapping couplings.
- **DEER (PELDOR)** — measures distance between two
  spins (3-8 nm) via dipolar coupling. Used for protein
  structure: introduce two nitroxide spin labels,
  measure distance.

### Multi-frequency EPR

X-band (9 GHz) is standard. Also Q-band (35 GHz), W-band
(95 GHz), and high-field (> 263 GHz at 9.4 T).

Higher field → better g-resolution; useful for
distinguishing similar-g species.

## Applications

### Free radicals

- **Persistent organic radicals** (TEMPO, DPPH, galvinoxyl)
  — used as standards + as catalysts (TEMPO oxidation,
  ATRP initiator).
- **Reaction intermediates** — captured at low T or
  trapped (spin-trapping with PBN, DMPO).
- **Photoredox cycles** — directly observe Ir⁺* + radical
  intermediates.

### Transition-metal coordination

- Cu(II), Mn(II), Mo(V), Co(II) all EPR-active in their
  d⁹, d⁵, d¹, d⁷ states.
- Distinguishes oxidation states in catalysts +
  metalloenzymes.

### Metalloenzymes

- **Hydrogenase** — Fe-Fe + Ni-Fe sites; EPR + Mössbauer
  identify oxidation states of intermediates.
- **Photosystem II** — Mn₄CaO₅ cluster cycles through
  S-states, each EPR-active.
- **Cobalamin (B₁₂)** — Co(II) intermediate of methionine
  synthase tracked by EPR.
- **Tyrosyl radicals** in ribonucleotide reductase + class
  I radical SAM enzymes.

### Battery + materials

- Li dendrites — Li⁰ paramagnetic; tracks dendrite growth
  in solid-state Li batteries.
- Defects in semiconductors, MOFs.
- Oxygen radicals on catalyst surfaces.

### Drug-radical interactions

- Spin-trap of reactive oxygen species (ROS) from drug
  metabolism.
- Free-radical bond formation in radical-mediated drugs
  (bleomycin, calicheamicin).

## DEER for protein structure

DEER (double electron-electron resonance) — measures
distance between two nitroxide spin labels (introduced
via cysteine-MTSL labelling) in a protein.

- Distance range: 1.5-8 nm (sometimes 10 nm with
  optimisation).
- Resolution: ± 0.2 nm.
- Used for membrane protein conformation, intrinsically
  disordered protein ensembles, protein-RNA contacts
  → complementary to cryo-EM + X-ray.

## Try it in the app

- **Tools → Lab analysers…** → look up Bruker EPR / EleXsys
  systems (if seeded).
- **Tools → Spectrophotometry methods** → see EPR section
  if surfaced.
- **Glossary** → search *EPR (electron paramagnetic
  resonance)*, *DEER*, *Hyperfine coupling*, *g-factor*,
  *Spin trap*, *TEMPO*.

Next: **Mössbauer spectroscopy**.
