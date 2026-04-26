# Hydrogen production + fuel cells

Hydrogen is a candidate carbon-free fuel. Producing it
sustainably + using it in fuel cells are two of the major
chemistry challenges of the energy transition.

## Hydrogen production

### Steam methane reforming (SMR; current)

```
CH₄ + H₂O → CO + 3 H₂           (high T, Ni catalyst)
CO + H₂O → CO₂ + H₂              (water-gas shift)
```

~ 95 % of industrial H₂ today (~ 70 Mt / yr globally).
Generates ~ 9 kg CO₂ per kg H₂. **"Grey hydrogen"**.

With CCS (carbon capture + storage) → **"blue
hydrogen"** — partly decarbonised.

### Water electrolysis (clean, scaling)

```
2 H₂O → 2 H₂ + O₂         (powered by electricity)
```

If electricity from renewables (solar, wind), this is
**"green hydrogen"** — fully zero-carbon.

Three electrolyser technologies:

| Type | Electrolyte | Efficiency | Cost |
|------|-------------|-----------|------|
| **Alkaline (AEC)** | KOH | 60-70 % | low ($/kW) |
| **PEM (proton exchange membrane)** | Nafion | 65-75 % | moderate |
| **SOEC (solid-oxide electrolysis)** | YSZ | 80-90 % at 700-800 °C | high but high efficiency |

Active materials:

- **Pt cathode (HER)** — best for HER; replaceable by Ni-
  based catalysts in alkaline conditions.
- **Ir / Ru oxide anode (OER)** — most active; expensive.
  Ni-based replacements emerging (NiFe layered double
  hydroxide).

### Photocatalytic water splitting

Use sunlight directly:

```
TiO₂ + hν → e⁻ + h⁺ → H₂ + O₂
```

Honda + Fujishima 1972. STH (solar-to-hydrogen) efficiency
~ 5-15 % achieved in lab; scale-up ongoing.

### Photoelectrochemical (PEC)

Combine semiconductor + electrochemistry. III-V tandem
cells reach > 30 % STH efficiency in lab.

## Fuel cells

### PEM fuel cell

```
Anode: H₂ → 2 H⁺ + 2 e⁻
Cathode: ½ O₂ + 2 H⁺ + 2 e⁻ → H₂O
```

Pt catalyst + Nafion membrane. Operates ~ 80 °C.

Cathode is the slow step (ORR — oxygen reduction
reaction). Pt-content reduction is the dominant cost
problem.

Modern: Pt loading dropped from 1 mg/cm² (2000) to ~ 0.05
mg/cm² (2025). Single-atom Fe-N₄ cathodes (lesson 23) are
the modern Pt-free target.

### SOFC (solid-oxide fuel cell)

```
Anode (700-1000 °C): fuel + O²⁻ → e⁻ + product
Cathode: ½ O₂ + 2 e⁻ → O²⁻
```

Ceramic electrolyte (YSZ); operates at high T → high
efficiency + fuel flexibility (H₂, CH₄, CO, ammonia all
work).

### AFC (alkaline fuel cell)

KOH electrolyte; first commercial fuel cell (Apollo
spacecraft). Pure H₂ + O₂ only (CO₂-poisoned).

### DMFC (direct methanol)

Direct CH₃OH oxidation. Lower energy density than H₂ but
liquid fuel = easier handling. Used in portable power.

## Hydrogen storage

H₂ is hard to store at atmospheric T:

- **Compressed gas** (700 bar) — current automotive
  standard (Toyota Mirai, Hyundai Nexo). 5 wt% H₂.
- **Liquid (-253 °C)** — for trucks + ships; expensive
  cryogenic.
- **Metal hydrides** (LaNi₅, Mg₂Ni) — slow uptake; weight
  heavy.
- **MOFs + nanoporous materials** — under research; ~ 5 %
  capacity at 77 K.
- **Liquid organic hydrogen carriers (LOHC)** — N-ethyl
  carbazole, dibenzyltoluene → reversibly absorbed +
  desorbed H₂ at 200-300 °C.
- **Ammonia (NH₃)** — H storage at ~ 17 wt% H; transported
  + cracked to H₂ at point of use.

Ammonia is currently the leading large-scale H carrier
(IEA + Australia + Japan + Singapore investing).

## Cost trajectory

```
Green hydrogen cost ($/kg):
2010: ~ $10
2020: ~ $5
2025: ~ $3-5
2030 target: $2 (DOE Hydrogen Shot)
2050: $1-2
```

Drivers: cheaper electrolysers + cheaper renewables +
scale.

## Industrial uses

Today (~ 95 Mt H₂/yr):

- 50 % ammonia (Haber-Bosch).
- 25 % petroleum refining (HDS).
- 10 % methanol production.
- 15 % other (electronics, food hydrogenation).

Future:

- Steel (replace coke with H₂ in DRI).
- Heavy transport (trucks, buses, trains, ships).
- Fertiliser (decarbonise NH₃).
- Backup grid storage.
- Aviation (H₂ aircraft + e-fuels).

## Try it in the app

- **Tools → Lab analysers…** → look up GC-TCD analysers
  for H₂ detection (if seeded).
- **Glossary** → search *Hydrogen*, *Electrolysis*, *PEM
  fuel cell*, *SOFC*, *Green hydrogen*, *LOHC*, *Steam
  methane reforming*, *Catalytic triad*, *pH*.

Next: **Carbon capture chemistry**.
