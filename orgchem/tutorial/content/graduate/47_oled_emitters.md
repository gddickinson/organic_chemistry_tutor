# OLEDs + emitter design

**Organic light-emitting diodes (OLEDs)** are the dominant
display technology in modern smartphones + TVs. Each pixel
emits light from electrically excited organic molecules.
Emitter design is a multi-million-dollar industry.

## OLED basics

A typical OLED stack:

```
Cathode (Al, Mg-Ag)
↓
Electron transport layer (ETL): TPBi, BPhen
↓
Emitter layer (EML): host + guest emitter
↓
Hole transport layer (HTL): NPB, TPD, TAPC
↓
Hole injection layer (HIL): MoO₃, PEDOT:PSS
↓
ITO anode (transparent conducting oxide)
↓
Glass substrate
```

When voltage applied:

1. Holes injected from anode + electrons from cathode.
2. Both drift through transport layers to EML.
3. Form bound exciton in emitter.
4. Decay → photon emitted.

Quantum yield = efficiency of step 4.

## The 25/75 rule + triplet harvesting

In electrical excitation, spin statistics:

- **25 %** singlet excitons (S₁).
- **75 %** triplet excitons (T₁).

Pure organic fluorescent emitters use only S₁ → max IQE
(internal quantum efficiency) = 25 %. Triplet excitons
quenched as heat.

To use triplets:

- **Phosphorescent emitters** (heavy metal: Ir, Pt) — fast
  ISC + triplet emission.
- **TADF (thermally-activated delayed fluorescence)** —
  small ΔE_ST allows reverse ISC at room T → 100 % IQE.
- **Hyperfluorescence** — TADF host + fluorescent dopant
  → narrow emission + 100 % IQE.

## Emitter classes

### Fluorescent (1st generation)

Pure organic. Low IQE (25 %) but cheap + stable.

- Small-molecule emitters: Alq₃ (green), DCM, DCJTB (red).
- Polymer emitters: PPV, F8BT.

### Phosphorescent (2nd generation)

Iridium + platinum complexes:

- **Ir(ppy)₃** — green, 100 % IQE (1998 introduction).
- **FIrpic** — sky blue.
- **Ir(piq)₃** — red.
- **PtOEP** — red phosphor.

Issue: blue phosphors are unstable. Industry uses
fluorescent blue + phosphorescent red/green for now.

### TADF (3rd generation, MR-TADF)

Small molecule with very small singlet-triplet gap (ΔE_ST
< 100 meV):

- **4CzIPN** — green; original TADF compound.
- **DABNA** — narrow-band blue (multi-resonance TADF).
- Various carbazole + diphenylamine donors + quinone
  acceptors.

Pure organic → no precious metals. Industry actively
moving from Ir to TADF for sustainability + cost.

### Hyperfluorescence

TADF host (pumps triplets into singlets) + fluorescent
emitter dopant (narrow emission). Best of both worlds.
Used in Samsung's latest displays.

## Design rules for emitters

### Colour

```
HOMO-LUMO gap → emission wavelength
Large gap → blue; small gap → red
λ ≈ 1240 / Eg(eV) nm
```

### Bandgap tuning

- Add donor groups → narrower gap → red shift.
- Add acceptor groups → narrower gap → red shift.
- Increase conjugation length → red shift.
- Twist molecule out of plane → blue shift.

### Quantum yield

- Reduce non-radiative decay (vibrational coupling).
- Rigid skeleton → less vibrational quenching.
- Heavy atom on emitter → ISC accelerated (good for
  phosphors, bad for fluorophores).

### Electron mobility (host)

- π-stacking helps hole / electron transport.
- Wide-gap host (CBP, TPBi) → energy-transfer to guest.

## Industrial production

Major OLED manufacturers:

- **Samsung Display** — dominant smartphone + TV OLED.
- **LG Display** — large-area TV (WOLED with white sub-
  pixels).
- **BOE, JDI, Visionox** — Chinese + Japanese makers.

Material suppliers:

- **Universal Display Corp (UDC)** — patents on Ir
  phosphors + TADF materials. Royalty-based business.
- **Merck KGaA** — display materials.
- **Idemitsu Kosan, Hodogaya** — host materials.

## OLEDs vs LCDs

- OLEDs: per-pixel emission → infinite contrast, fast
  refresh, thin.
- LCDs: backlight + filter → cheaper, brighter, longer-
  lifetime.

Both coexist; OLED dominates smartphones + premium TVs.

## Emerging: micro-LED + mini-LED

Direct-emission inorganic LED arrays (one LED per pixel)
challenging OLED for high-brightness displays. Different
chemistry; pixel pitch limits remain.

## Try it in the app

- **Reactions tab** → look at conjugated polymer chemistry
  if seeded.
- **Glossary** → search *OLED*, *Phosphorescence*, *TADF*,
  *Hyperfluorescence*, *Excited state*, *Singlet*,
  *Triplet*.

Next: **Battery electrolytes — chemistry frontiers**.
