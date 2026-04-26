# Spintronic molecules + single-molecule magnets

**Spintronics** uses electron **spin** (in addition to or
instead of charge) for computation + memory. Molecular
spintronics + single-molecule magnets (SMMs) extend this
to molecule-sized devices.

## Why spin

Spin has 2 states (up + down) — like binary 0 + 1 — but
with quantum properties (superposition, entanglement) that
make it richer than charge:

- Energy efficient (no current needed to maintain spin
  state).
- Quantum computing (qubit candidate).
- Non-volatile memory (MRAM).

## Single-molecule magnets (SMMs)

A molecule with **slow magnetic relaxation** below a
"blocking temperature" T_B. The classic:

```
Mn₁₂-acetate: [Mn₁₂O₁₂(OAc)₁₆(H₂O)₄]
```

Discovered 1993 (Sessoli, Gatteschi). T_B ~ 4 K. Below T_B,
magnetisation persists for hours-days even after removing
the field — molecular magnet.

### Key SMM family

- **Mn₁₂** — original; eight Mn(III) + four Mn(IV); S = 10
  ground state.
- **Mn₈** — smaller analogue.
- **Fe₈** — Fe(III) cluster; T_B ~ 2 K.
- **Dy(III) + Tb(III) lanthanide SMMs** — single ion
  metallocenes; T_B up to 60 K (Dy-COT).
- **Single-atom SMMs** (Ho, Dy, Tb on substrates) — push
  T_B to 80 K.

### Why high T_B matters

Practical use needs T_B > 77 K (liquid N₂ cooling) for
cheap spinronics; > 300 K (ambient) for room-temperature
devices.

By 2025, lanthanide SMMs reached T_B ~ 80 K → first
practical-temperature SMMs. Goal: 300 K eventually.

## Molecular qubits

A SMM with addressable + coherent spin state =
**molecular qubit**. Requirements:

- **Long coherence time T₂** (microseconds to
  milliseconds).
- **Addressable** by RF or μw pulses.
- **Scalable** (multiple molecules in array).

Examples:

- **Cu(II) phthalocyanine** — T₂ ~ µs at 4 K; spin-1/2.
- **VO(porphyrin)** — V(IV) S = 1/2; T₂ ~ ms at 4 K.
- **Ni(II) complexes** — S = 1; useful for clock-transition
  protection.
- **Vanadium triphenoxide** (VOTPP) — record T₂ for a
  molecular qubit (~ 1 ms at 5 K).

## Photoswitched spin states

Some Fe(II) compounds undergo **spin crossover (SCO)**:

- LS Fe(II) (S = 0) at low T or under high pressure.
- HS Fe(II) (S = 2) at high T.
- Switching by T, P, light, magnetic field, or chemical
  perturbation.

Useful for:

- Display devices (T-induced colour change).
- Pressure sensors.
- Information storage with memory effect.

## Chiral-induced spin selectivity (CISS)

Discovered ~ 2010s: electrons travelling through a chiral
helical molecule (like dsDNA) acquire net spin polarisation
based on the helix sense.

Implications:

- **Spin filtering** at room T using chiral organic
  molecules.
- **Chiral electrochemistry** — measurable spin polarisation
  of redox products.
- **Asymmetric synthesis via spin selection** — emerging
  applications.

## Measurement methods

- **SQUID magnetometry** — measure magnetic moment vs T,
  H. Standard for SMMs.
- **EPR + ENDOR** — characterise spin state + coupling
  (lesson 33).
- **Mössbauer (for Fe SMMs)** — local Fe environment +
  spin state.
- **Inelastic neutron scattering (INS)** — magnetic
  excitations.
- **Pulse EPR** — measure T₁ + T₂ for qubit candidates.

## Industrial relevance

- **MRAM (Magnetoresistive RAM)** — already commercial
  (Everspin, IBM, Samsung); uses metal-MTJs (not SMMs
  yet).
- **Hard-disk read heads** — use spin-valve effect (Nobel
  2007: Fert + Grünberg).
- **Spin-based cell sensors** for cancer + neurodegenerative
  diagnostics.

SMM-based commercial spintronics not yet here — research
phase.

## Limits

- **Low T** for most SMMs (need cooling).
- **Fabrication** — placing single molecules at defined
  positions on a chip is hard.
- **Coherence times** still shorter than atomic qubits
  (NV centres in diamond, trapped ions).
- **Read-out** — single-molecule magnetic measurement
  requires very sensitive detectors.

## Try it in the app

- **Tools → Lab analysers…** → look up SQUID magnetometry
  + EPR systems.
- **Glossary** → search *Spintronics*, *Single-molecule
  magnet*, *Spin crossover*, *Molecular qubit*, *CISS*,
  *Chiral-induced spin selectivity*.

Next: **OLEDs + emitter design**.
