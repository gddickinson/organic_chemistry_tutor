# Continuous-flow process design

The advanced flow-chemistry lesson covered the basics. This
lesson goes into **process design** — what to think about
when scaling a batch reaction to flow + then to industrial
manufacturing.

## When to choose flow over batch

Flow wins when one of these is true:

- **Hazardous intermediate** — generated + consumed
  continuously, never accumulated (azides, diazomethane,
  ozone, peroxides).
- **Cryogenic chemistry** (e.g. -78 °C lithiation) — flow
  reactor's small heat capacity allows fast cooling.
- **Photoreaction** — surface-area-to-volume scaling
  favours flow.
- **Multi-step telescope** — connect 2-5 reactions in
  series without isolating intermediates.
- **Steady-state need** — pharmaceutical manufacturing
  requires reproducibility per lot.
- **Safety** — fugitive emissions of toxic gas, etc.,
  contained.

Flow loses when:

- Reaction takes > 24 h (huge tube needed).
- Substrate forms slurries (clogs).
- Crystallisation / precipitation step.
- Workup involves multiple liquid-liquid extractions.
- You only need 1 mmol once.

## Key design parameters

### Residence time τ

```
τ = reactor volume / flow rate
```

For a 10 mL reactor at 1 mL/min, τ = 10 min.

τ should match the reaction time required at the chosen
temperature. For an SN2 that takes 60 min in batch,
τ = 60 min in flow.

### Flow rate

Determines **throughput** + relates to mixing + Reynolds
number:

- Slow flow → laminar flow, slow mixing (need static
  mixer).
- Fast flow → turbulent flow, fast mixing.

For reactions with fast bimolecular kinetics (lithiation,
acid chloride coupling), you NEED fast mixing → use static
mixers (Comet, IMM, interdigital).

### Reactor materials

- **PFA tubing** — chemically inert; transparent for
  photochemistry; cheap.
- **Stainless steel** — high T + P; durable; opaque.
- **Hastelloy** — corrosion-resistant; for HF, conc. acid,
  bromine.
- **PEEK** — chemically inert; mid-T (max 250 °C).
- **Glass capillaries** — transparent, fragile; for special
  cases.

### Back-pressure regulator (BPR)

Maintains pressure in the reactor:

- Allows high-T solvent (water, ethanol above bp).
- Keeps gas dissolved (CO, H₂, gases via tube-in-tube).
- Prevents pump cavitation.

## Multi-step flow design

Example: a 3-step API synthesis in flow:

```
Step 1: Diazotisation in PFA coil at 0 °C, τ = 30 s.
Step 2: Trap with Cu / amine in second coil at 25 °C,
        τ = 5 min.
Step 3: Reductive amination in third coil at 50 °C,
        τ = 30 min.
        Output: API in solution → BPR → collection.
```

Total residence time ~ 35 min. Compared to batch (3
isolations + 3 reactions): 3-5 days → ~ 35 min flow.

## Inline analytics + feedback

- **FlowIR** (Mettler ReactIR) — real-time IR; tracks
  conversion + intermediate identity.
- **Inline UV-Vis** (Avantes) — colorimetric tracking.
- **Online HPLC** (split + autosampler) — quantitative.
- **Inline NMR** (Magritek Spinsolve) — slow but
  quantitative.
- **Inline MS** — Advion / Waters QDa for MS detection.

Combined with **Bayesian optimisation** (Doyle, Jensen) →
self-optimising flow reactor that finds optimal T + τ +
stoichiometry without human intervention.

## Famous flow processes

- **Anti-malarial artemisinin** — Sanofi continuous flow
  photoreactor.
- **Insulin in 4 hours** — MIT Pentelute lab.
- **Ibuprofen** in 3 minutes — Jamison + Snapdragon
  Chemistry.
- **Continuous manufacturing API** — FDA-approved Vertex's
  Orkambi (lumacaftor + ivacaftor).
- **Eli Lilly Tirzepatide** — flow synthesis steps.

## Scale-up "numbering up"

Unlike batch where you build a 1000× bigger flask, flow
scales by:

- **Numbering up** — duplicate identical small reactors in
  parallel.
- **Slight scale-up** — increase tube diameter; doesn't
  scale beyond ~ 5-10 mm without losing heat / mass
  transfer.

## Flow + biocatalysis

Immobilised enzymes in packed-bed flow reactors:

- KRED / transaminase / lipase reactions in enzymes-on-
  resin column.
- Enzyme retains activity for months in flow.
- Used for chiral building-block manufacturing at kg
  scale.

## Try it in the app

- **Tools → Lab analysers…** → look up Mettler ReactIR,
  Magritek Spinsolve, Vapourtec / Syrris flow systems.
- **Tools → Lab equipment…** → flow reactor entries (if
  seeded).
- **Glossary** → search *Flow chemistry*, *Continuous
  manufacturing*, *Microreactor*, *Residence time*,
  *Tube-in-tube*.

Next: **Process safety in pharma**.
