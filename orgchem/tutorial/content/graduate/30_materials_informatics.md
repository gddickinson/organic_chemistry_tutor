# Materials informatics — batteries, photovoltaics, catalyst design

**Materials informatics** applies the cheminformatics + ML
toolkit to materials discovery: batteries, photovoltaics,
heterogeneous catalysts, magnets, superconductors, alloys.
The Materials Genome Initiative (US, 2011) catalysed the
field; by 2025 ML-discovered materials reach commercialisation.

## Why ML for materials?

- **Combinatorial chemical space** — composition + crystal
  structure + processing all matter.
- **Slow + expensive synthesis** — single-crystal growth +
  battery cycling test takes weeks.
- **Need "needle in a haystack"** — among 10⁵-10⁸
  candidate compositions, the best one might be unique.

ML reduces the search by orders of magnitude.

## Open materials databases

- **Materials Project** (Berkeley, ~ 130 000 entries) —
  DFT-computed properties of inorganic crystals + their
  band gaps + stabilities + elastic moduli.
- **AFLOWlib** (Duke) — competing comprehensive DFT
  database.
- **OQMD (Open Quantum Materials Database)** — Wolverton
  group; ~ 1 M entries.
- **NOMAD** — European multi-platform repository.
- **Crystallography Open Database (COD)** — > 500 000
  experimental crystal structures, free.
- **ICSD** — Inorganic Crystal Structure Database
  (subscription).
- **Battery Archive** — NASA-curated cycling data for Li-ion.

## Property prediction

### Band gap

DFT (PBE) predicts band gaps poorly (underestimates by
40-50 %); HSE / GW corrects but expensive. ML models
trained on DFT or experimental data give chemical-
accuracy predictions in milliseconds:

- **Crystal Graph CNN (CGCNN)** + **MEGNet** — graph
  neural networks treating crystals as graphs.
- **CrystalNet, MatBert** — modern transformers.

### Formation energy + stability

Predict whether a hypothetical compound is on the convex
hull (synthesisable) — within ~ 30 meV/atom is the typical
threshold.

### Mechanical properties

Bulk modulus, shear modulus, hardness from elastic
constants. Useful for screening structural materials,
ceramics, alloys.

## Battery materials

Li-ion cathode discovery — finding the next better than
LiCoO₂ / LiFePO₄ / NMC811:

- Constraints: high capacity (mAh/g), high voltage (V),
  cycling stability, no Co (cobalt is expensive +
  conflict-mineral).
- ML screens 100 k Li-Mn-O / Li-Fe-Si-O / Li-Mg-Mn-O
  compositions for predicted properties.
- Wang et al. (2020, *Nature*) — discovered LiCoMnO4 +
  related cathodes by ML + DFT.

Also active: solid-electrolytes for solid-state Li
batteries (Li₆PS₅Cl, Li₁₀GeP₂S₁₂ family); Na-ion + K-ion +
multivalent (Mg, Ca, Zn, Al) chemistries.

## Photovoltaics

### Conventional Si

ML helps with defect engineering + dopant placement +
contact materials.

### Perovskites (organic-inorganic hybrid)

CH₃NH₃PbI₃ + many variants. ML screens for:

- Stable composition (mixed-cation Cs/MA/FA, mixed-halide
  I/Br/Cl).
- Tandem-cell partner band gap (1.1 eV Si bottom + 1.6 eV
  perovskite top → > 30 % efficiency target).
- Lead-free alternatives (Sn-based, Bi-based, Ag-Bi-Br
  double perovskites).

The University of Toronto + Oxford PV groups have used
ML-driven HTE to find > 10 high-efficiency perovskite
recipes.

### Organic photovoltaics

Acceptor + donor polymer / small molecule discovery; HTP
(high-throughput polymer) synthesis robots.

## Catalyst design

### Heterogeneous catalysts

- **Sabatier principle** — best catalyst binds intermediate
  with optimal strength (not too weak, not too strong).
- **Volcano plot** — activity vs binding energy is a
  parabola peaked at ideal Δ.
- **ML** screens binary + ternary alloys (high-throughput
  DFT of CO + CO₂ + H₂ + N₂ adsorption energies on every
  surface facet + alloy composition).

### Single-atom catalyst design

Predict M-Nₓ environments + dopant choice for selective
electrocatalysis (CO₂ reduction, ORR, NRR).

## Modern frontiers

### Active learning + Bayesian optimisation

Don't pre-screen 1 M materials randomly — let an
acquisition function pick the most-informative next
candidate. Convergence to the optimum in 100-500
experiments instead of millions.

Successful case studies:

- **Aldol catalyst optimisation** (Doyle 2018) — 100
  experiments to discover top performer in 100 k chemical
  space.
- **OLED emitter design** (Soshi, Aspuru-Guzik 2020) —
  ML-guided synthesis of new green emitters.
- **High-temperature superconductor candidates** (Konno,
  Nature 2020) — ML predicts Tc.

### Generative materials models

VAE / Diffusion / Transformer models that propose **new
hypothetical structures** (not just rank existing ones):

- **CDVAE** (Xie, MIT) — diffusion model for crystal
  structures.
- **Quasi-random crystal generation** (Tian, Berkeley) —
  exploration of chemical-space corners.

### Self-driving labs

Fully autonomous labs combining ML + robotics to discover
materials with no human intervention:

- **Ada (UBC, Berlinguette)** — first fully autonomous
  thin-film optimisation.
- **A-Lab (Berkeley, Ceder + Persson 2023, Nature)** —
  17 days, 41 inorganic compounds synthesised + verified
  autonomously; 71 % success rate on novel targets.
- **NeurIPS workshops on AI for science** + **MEET (Materials
  Genome Initiative)** track community progress.

## Limits + critiques

- **Distribution shift** — most ML models trained on
  databases biased toward known materials; novel chemistry
  (multivalent ions, exotic structures) underperforms.
- **Synthesisability** — predicting formation energy ≠
  predicting which lab procedure succeeds. Synthesis-
  prediction models still primitive.
- **Property prediction ≠ device performance** — battery
  cycling depends on grain boundaries + electrolyte
  interface + manufacturing scale, not just bulk
  properties.
- **Reproducibility crisis** — many published ML-
  materials results don't replicate; community demands
  open data + benchmark splits.

## Try it in the app

- **Tools → Lab analysers…** → look up XRD + DSC + battery
  cyclers used in materials characterisation.
- **Glossary** → search *Materials informatics*, *Density
  functional theory (DFT)*, *Basis set*, *ML potential*,
  *Band gap*, *Sabatier principle*, *Active learning*.

Next: **Curriculum complete — explore all tabs + tools**.
