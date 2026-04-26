# Battery electrolytes — chemistry frontiers

The electrolyte is the often-overlooked component of a Li-
ion battery, but it determines safety, cycle life,
voltage window, and rate capability. Modern battery
chemistry is mostly electrolyte chemistry.

## What an electrolyte does

```
Electrolyte: ionic conductor + electronic insulator
   → carries Li⁺ between cathode + anode
   → must be stable across the voltage window
   → forms SEI (solid electrolyte interphase) on anode
   → forms CEI on cathode
```

## Standard Li-ion electrolyte

```
1 M LiPF₆ in EC : DMC (or EC : EMC : DEC)
                 (3:7 v/v)
+ ~ 2 % vinyl carbonate (additive)
+ ~ 1 % FEC (fluoroethylene carbonate)
```

Components:

- **LiPF₆** — salt; forms LiF + POₓFᵧ in SEI.
- **Ethylene carbonate (EC)** — high dielectric, freezes at
  36 °C; needs liquid co-solvent.
- **Dimethyl carbonate (DMC) + EMC + DEC** — low-viscosity
  carbonates; lower dielectric.
- **VC (vinyl carbonate) + FEC (fluoroethylene carbonate)
  + LiBOB + LiDFOB** — additives that polymerise on
  anode → improved SEI.

This formulation works from 1.5 V to ~ 4.3 V (graphite
anode + LCO/NMC cathode).

## Why "more voltage" is hard

To increase energy density, we want higher cathode
voltage (5+ V). Standard EC + DMC oxidise above 4.5 V →
electrolyte decomposes → cell dies.

### Solutions being developed

- **Fluorinated solvents**: FEC, FEMC, F-EC; oxidatively
  stable.
- **Sulfones, nitriles**: glutaronitrile (GN) +
  succinonitrile work to 5+ V.
- **Ionic liquids**: imidazolium / pyrrolidinium /
  piperidinium salts; very wide voltage windows.
- **Solid-state electrolytes** — completely sidestep
  liquid stability.

## Solid-state electrolytes (SSEs)

Replace liquid with a Li⁺-conducting ceramic or polymer:

| SSE | Type | σ (S/cm at 25 °C) |
|-----|------|---------------------|
| LIPON | thin-film amorphous | 10⁻⁶ |
| LLZO (Li₇La₃Zr₂O₁₂) | garnet ceramic | 10⁻³ |
| Li₆PS₅Cl | argyrodite sulfide | 10⁻³ |
| Li₁₀GeP₂S₁₂ (LGPS) | thiophosphate | 10⁻² |
| PEO + LiTFSI | polymer | 10⁻⁴ at 60 °C |
| Composite (LLZO + PEO) | hybrid | 10⁻⁴ |

Targets:

- σ ~ 10⁻³-10⁻² S/cm at room T.
- Stable against Li metal anode (key for energy density).
- Mechanical strength to suppress dendrites.

Companies: **QuantumScape, Solid Power, Toyota,
Samsung, Nio, Mercedes**.

## Beyond Li-ion

### Na-ion

Replace Li with Na (~ 1000× more abundant). Lower energy
density but cheaper. CATL + BYD launching Na-ion EVs in
2024-2026 for grid storage + low-cost cars.

Electrolyte: NaPF₆ in EC/PC/DMC; similar formulations to
Li-ion.

### Multivalent (Mg²⁺, Ca²⁺, Al³⁺, Zn²⁺)

Higher theoretical energy density (multi-electron per
ion). Challenges: slow ion mobility, electrolyte
decomposition, anode passivation.

Most lab-scale; commercialisation 5-10 years out.

### Lithium-sulphur

Cathode: S₈ → Li₂S (theoretical capacity ~ 1670 mAh/g, 5 ×
LCO).
Issues: polysulphide shuttle (Li₂S_n dissolves +
diffuses); short lifetime.
Electrolyte additives + interlayers mitigate. OXIS Energy
+ Sion Power working on commercial.

### Lithium-air (Li-O₂)

Theoretical highest energy density (Li + O₂ → Li₂O₂);
limited by high overpotential + carbonate-electrolyte
side reactions. Mostly research; commercial timeline
~ 10+ years.

## Anode chemistry

The negative electrode often dictates electrolyte:

| Anode | Common formulation |
|-------|---------------------|
| Graphite (intercalation) | LiPF₆ in carbonates + 2 % VC |
| Si (alloy) | LiPF₆ + FEC (much higher SEI volume change) |
| Li metal | sulfide / garnet SSE; or LiPF₆ + special additives |
| Hard carbon (Na-ion) | NaPF₆ in carbonates + DTD additive |

## SEI characterisation

Battery chemists routinely study SEI by:

- **XPS** (Li 1s, F 1s, P 2p) — Li₂O, LiF, Li₂CO₃, Li_xPOyFz.
- **Cryo-TEM** — atomic structure of SEI layers.
- **Raman** — carbon phase + polymorph.
- **In-operando GC-MS** of headspace — gas evolution
  identifies decomposition.

## Modern frontiers

- **High-concentration electrolytes (HCEs)** — > 4 M LiTFSI
  → no free solvent → wider voltage stability.
- **Localized HCEs** — HCE + diluent → still wide voltage
  but lower viscosity.
- **Ionic-liquid electrolytes** — pyrrolidinium-TFSI; > 5 V
  stability.
- **Self-forming SEI** — additive design via ML screening
  (e.g., Carbon Pioneer / NextSilicon / others).

## Try it in the app

- **Tools → Lab analysers…** → look up Li battery cyclers
  (Arbin, Maccor) + cryo-EM (for SEI characterisation).
- **Glossary** → search *Battery*, *Electrolyte*, *SEI
  (solid electrolyte interphase)*, *LiPF₆*, *Solid-state
  battery*, *Ionic liquid*, *EC (ethylene carbonate)*,
  *Photoredox catalysis*, *pKa*.

Next: **Hydrogen production + fuel cells**.
