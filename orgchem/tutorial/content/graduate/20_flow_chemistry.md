# Flow chemistry — leaving the round-bottom flask

In **flow chemistry**, reagents are pumped continuously
through a reactor (tube, packed bed, microfluidic chip)
instead of being mixed batch-wise in a flask. Residence
time replaces reaction time; concentration profile is
spatial instead of temporal.

By 2025 flow is the default for hazardous + scale-sensitive
chemistry in pharma + speciality chemicals manufacturing.

## Why flow?

- **Heat + mass transfer** — small channels (μm-mm) give
  short diffusion paths + huge surface-area-to-volume.
  Exothermic + cryogenic reactions become safe.
- **Pressure** — sealed tubes routinely run at 30-100 bar
  (water above its bp, supercritical CO₂, gases dissolved
  at high concentration).
- **Hazardous intermediates** — make + consume in the same
  steady-state stream, never accumulating dangerous
  amounts (azides, diazomethane, ozonides, nitro alkanes).
- **Reproducibility** — steady-state operation; second-by-
  second control.
- **Scale-up by numbering up** — same reactor scales by
  duplication or by extending residence time, not by
  rebuilding.
- **Inline analytics** — UV, IR, NMR, MS sensors monitor
  the stream in real time → automatic feedback.

## Hardware

### Pumps

- **HPLC pumps** ($10k-30k) — standard for organic
  chemistry. Stainless or PTFE wetted parts.
- **Syringe pumps** — best for small-volume + variable
  rates (Harvard Apparatus, kdScientific).
- **Peristaltic** — gentle on sensitive samples but
  pulsatile; good for biological flows.

### Reactors

- **PFA tube reactors** (1/16" or 1/8" OD, 0.5-1.5 mm ID)
  — workhorse; cheap; transparent for visual / photo
  reactions.
- **Stainless steel coils** — high T + high P.
- **Microfluidic chips** (Vapourtec, Syrris, Chemtrix) —
  glass or silicon channels with mixing structures
  (interdigital, slit, T-mixer).
- **Packed-bed reactors** — solid catalyst (Pd/C, Lindlar,
  H-Cube cartridges) in a column; substrate pumped
  through. Workhorse for hydrogenation.
- **Tube-in-tube** (Ley) — gas + liquid stream separated by
  a Teflon AF membrane that lets gas dissolve into liquid
  at controlled rates (CO, H₂, O₂, NH₃).

### Back-pressure regulators (BPR)

Maintain constant pressure (10-100 bar) so:

- Solvents stay liquid above their bp.
- Gases stay dissolved.
- Pumps don't cavitate.

### In-line analytics

- **FlowIR** — Mettler ReactIR; tracks functional-group
  appearance / disappearance.
- **Inline UV-Vis** — Avantes / Ocean Optics fibre
  spectrometers.
- **HPLC sampling valve** — automated split → online HPLC.
- **Benchtop NMR** — Magritek Spinsolve picks up reaction
  end-point.
- **MS** — Advion expression, Waters QDa direct-coupled.

## Famous flow processes

### Hazardous-intermediate chemistry

- **Diazomethane** (Ley, others) — Aldrich's TMSCHN₂
  remains for batch; flow generates CH₂N₂ inline + uses
  it before the flask sees the danger.
- **Azides + acyl azides** — controlled in flow via
  membrane-separated reagent streams (MIT, Asymchem).
- **Nitration / sulfonation** — Lonza, Sandoz scale-up
  with flow microreactors.
- **Lithiation** — Pfizer + Genentech use flow to do
  RLi / cryogenic deprotonation at -78 °C → -10 °C with
  μs-resolved residence times to control selectivity.

### Photochemistry

Photochemistry scales linearly with surface area + badly
with volume. Flow turns this into a feature: thin tube,
high light flux, high throughput. Visible-light flow photo-
reactors are now standard (Vapourtec UV-150, Syrris
Asia-FFP) for kg-scale photoredox.

### Multi-step + telescoping

- Connect 2-5 reactors in series → full synthesis without
  isolating intermediates.
- **Plug-flow + back-pressure cascade** lets each step run
  at its own optimal T + P.
- Famous example: **artemisinin total synthesis** in flow
  (Seeberger 2012); **ibuprofen 3-step continuous** (Jamison
  2014); **insulin in 4 hours** (Pentelute 2020).

### Manufacturing scale

- **Lonza / Pfizer / Genentech** — flow API plants in
  Switzerland + China.
- **DARPA's Battlefield Medicine program** — portable
  on-demand drug manufacturing.
- **Snapdragon Chemistry / Asymchem** — CRO services for
  flow process development.

## Flow ≠ always better

Batch chemistry remains dominant for:

- **Slow reactions** (> 24 h) — need impractically long
  reactors or tiny flow rates.
- **Slurries + heterogeneous mixtures** — clog tubes.
- **Crystallisations + workup** — flow doesn't replace the
  unit operations after the reaction.
- **Small one-off batches** — overhead of setting up flow
  doesn't pay off for 1-mmol exploratory chemistry.

## Modern frontiers

- **Self-optimising flow reactors** — feedback from inline
  analytics + Bayesian optimisation tunes T, residence
  time, stoichiometry on-the-fly. Jensen, Bourne, Cronin
  publishing actively.
- **3D-printed reactors** — custom geometries (static
  mixers, static heat exchangers) printed in PEEK or
  Hastelloy.
- **Electrochemical flow cells** — Asynt FlowSyn-Electro,
  Ammonite, IKA flow accessories.
- **Continuous biocatalysis** — immobilised enzymes in
  packed beds; works for transaminases, lipases,
  carbohydrate-active enzymes.

## Try it in the app

- **Tools → Lab analysers…** → look up Mettler-Toledo
  ReactIR, Magritek Spinsolve — inline analytics for
  flow.
- **Glossary** → search *Flow chemistry*, *Continuous
  manufacturing*, *Microreactor*, *Plug flow*, *Residence
  time*.

Next: **Curriculum complete — explore the catalogues +
specialised tools**.
