# Modern photoredox + energy-transfer catalysis

Visible-light photochemistry has been the most active area
of methodology development since 2010. The toolkit: a few
microgrammes of a coloured photocatalyst, a $30 blue LED,
a stir bar, room temperature.

## Why visible light is special

UV light (< 400 nm) was the historical photochemistry
medium but is destructive — most molecules absorb UV, so
selectivity is poor. **Visible-light photocatalysts** (Ir,
Ru, organic dyes) absorb where the substrate doesn't, then
shuttle the photon's energy to a chosen reaction partner.

## Two activation modes

### 1. Photoredox (single-electron transfer, SET)

The excited photocatalyst is a **stronger oxidant + reductant**
than its ground state — it can do both directions:

```
*PC + R-X  →  PC⁺ + R-X⁻  →  R•  +  X⁻         (reductive quenching)
*PC + R-H  →  PC⁻ + R-H⁺  →  PC⁻ + H⁺ + R•     (oxidative quenching)
```

Generated radicals add to alkenes, abstract H, couple with
metals, etc. The catalyst returns to ground state by
swapping an electron with a sacrificial donor / acceptor.

**Workhorse photocatalysts**:

- **[Ru(bpy)₃]²⁺** — orange light, modest E*.
- **[Ir(ppy)₃], [Ir(dF(CF₃)ppy)₂(dtbbpy)]⁺** — strongest +
  most-tuned.
- **Organic dyes** — eosin Y, rose bengal, acridinium
  (Fukuzumi, Nicewicz). Cheaper, metal-free.
- **4CzIPN** — donor-acceptor organic, balances cost +
  performance.

### 2. Energy transfer (EnT, sensitisation)

The excited photocatalyst transfers its triplet energy
*without* electron transfer:

```
*PC (T₁) + Substrate (S₀) → PC (S₀) + *Substrate (T₁)
```

Useful for triplet sensitisation: [2+2] cycloadditions,
E→Z isomerisation, di-π-methane rearrangements, certain
strained-ring openings. Glorius + Bach + Yoon have driven
this resurgence.

## Famous reaction classes

- **Photoredox decarboxylative coupling** (MacMillan, Doyle)
  — RCO₂H + ArX → R-Ar via Pd / Ir / light. Replaces
  organozinc / boron with carboxylic acids.
- **Photoredox C-H functionalisation** — HAT catalysts
  (decatungstate, quinuclidine) abstract sp³ H; resulting
  radical couples with vinyl arenes / Michael acceptors.
- **Photoredox alkene hydrofunctionalisation** —
  hydroamination, hydroetherification, hydrothiolation by
  radical chain.
- **Visible-light [2+2]** — Bach's chiral templates +
  Yoon's chiral Lewis acid + Ru photocat → enantioselective
  cyclobutanes.
- **Metallaphotoredox** (MacMillan, Doyle, Molander) —
  combines photoredox with Ni catalysis to do otherwise-
  difficult cross-couplings.

## Triplet energy transfer in pharma

EnT [2+2] enables 4-membered carbocycle synthesis without
strained substrates. Pfizer + AstraZeneca routinely use
photoredox in process chemistry → kg-scale flow reactors
with custom blue-LED arrays.

## Apparatus

A typical setup:

- **Light source** — Kessil PR160L (440 nm or 427 nm), $300.
  Replaces fluorescent CFLs that dominated 2009-2014.
- **Reactor** — round-bottom flask + rare-earth magnet
  stirrer + ice bath (LEDs are surprisingly hot).
- **Flow** — for scale-up. Photochemistry scales linearly
  with surface area, badly with volume → flow > batch above
  ~ 10 g.

## Mechanistic toolkit

- **Stern-Volmer quenching** — plot 1/Φ vs [Q] gives the
  bimolecular quenching rate; tells you which reagent
  quenches the photocatalyst.
- **Cyclic voltammetry** — measure E_red, E_ox of
  photocatalysts; compare to substrate redox potentials.
- **Transient absorption spectroscopy** — femtosecond /
  microsecond TA traces the photocatalyst's excited-state
  decay.
- **Quantum yield Φ** — ratio of products formed per
  photon absorbed; Φ > 1 implies a chain mechanism.

## Try it in the app

- **Reactions tab** → look for photoredox-tagged reactions
  (decarboxylative coupling, [2+2], minisci-type).
- **Tools → Spectroscopy…** → estimate UV-vis bands of a
  photocatalyst; absorbance edge tells you what wavelength
  to use.
- **Glossary** → search *Photoredox*, *Energy transfer
  (sensitisation)*, *HAT (hydrogen atom transfer)*,
  *Stern-Volmer*.

Next: **Bioorthogonal chemistry — labelling biology in real
time**.
