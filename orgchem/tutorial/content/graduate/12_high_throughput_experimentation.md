# High-throughput experimentation + automation

**High-throughput experimentation (HTE)** miniaturises +
parallelises chemical reactions to test dozens to thousands
of conditions per day. By 2025 every major pharma + many
academic labs run HTE for reaction development.

## Why HTE?

Traditional reaction optimisation is one variable at a time
(OVAT) — change temperature, then catalyst, then solvent, …
Slow + biased + can't find synergistic effects.

HTE allows:

- **Design of Experiments (DoE)** — vary ≥ 3 factors
  simultaneously, fit response surfaces.
- **Catalyst screening** — 96 conditions in one plate.
- **Substrate-scope tables** without months of manual work.
- **Reproducibility audit** — same protocol → same result.

## Hardware

### Reaction block + plate formats

- **96-well plate** (8 × 12, ~ 100-1500 µL) — workhorse.
- **24-well + 384-well** for special use.
- **High-pressure HTE plates** (Symyx → Freeslate) —
  individually sealed wells for H₂, CO, ammonia screens.
- **Photochemistry HTE** — LED-bottom-illuminated plates
  for visible-light methodology screens.

### Liquid handling

Hamilton STAR, Tecan Fluent, Opentrons OT-2 — robotic
arms pipette stock solutions of catalyst + ligand + base +
substrate onto the plate. Sub-µL accuracy, programmable.

### Analysis

- **UPLC-MS** — 1-2 min per well. Quantify product peak
  area + look for correct mass.
- **GC-MS** — for volatile substrates.
- **HRMS imaging** (DESI-MS, MALDI imaging) — direct from
  plate without injection.
- **NMR sleeves** — 384-well NMR rotors enable parallel
  ¹H acquisition; reduced quantification accuracy.

## Software

- **Reaction-design platforms** — Mestrelab Mnova, Inkspot,
  AnalyzeChem, AlphaChem.
- **Statistical packages** — JMP, Minitab, R, Python +
  scikit-learn for DoE + response-surface methods.
- **ELN integration** — Benchling, IDBS E-WorkBook so
  each well's metadata + result are tracked.
- **AI optimisers** — Bayesian optimisation tools
  (BOSS, Edbo+, PhEDOX) suggest the next plate of
  conditions to try.

## Famous HTE wins

- **Doyle's nickel cross-coupling screens** (Princeton, 2014)
  — Ni / photoredox coupling of carboxylic acids with aryl
  halides. 3000 substrate-condition pairs in days.
- **Merck's Buchwald-Hartwig optimisation** — discovered the
  optimal Pd / ligand / base combination for an internal
  intermediate by screening 4000 conditions.
- **AbbVie's flow + HTE for Imbruvica** — process
  development reduced solvent use 50 %.
- **MIT's substrate scope tables** (Doyle, Sigman) — instead
  of 30 cherry-picked substrates in a manuscript, screen
  100s spanning electronic + steric features.

## Automated synthesis platforms

Beyond HTE: full **autonomous** synthesis robots:

- **Burke's Synthia / molecular machine** — couples
  building blocks via repetitive Suzuki couplings; > 1000
  small molecules synthesised autonomously.
- **Cronin's Chemputer / Chemify** — bench-scale flow
  reactor + custom XDL programming language for
  reproducible synthesis recipes.
- **Sames-MERck CATWALK** — automated reaction development
  + scale-up from milligrams → kilograms.
- **Coley + Jensen's IBM RoboRXN** — cloud-controlled
  flow-based synthesis platform; suggests + executes
  reactions remotely.

## Statistical doe

A typical 2-level full-factorial design with k factors needs
2^k experiments. For k = 5 → 32 wells. Higher fractions
(2^(k-p)) screen up to k = 8 in 32 wells with some
confounding.

**Response surface methods** (Box-Behnken, Central
composite) — quadratic fits over 3-5 factors give
optimal-condition prediction.

**Bayesian optimisation** — modern alternative to DoE.
Gaussian-process surrogate model + acquisition function
balances exploration vs exploitation. EDBO+ is the
chemistry-tuned implementation.

## What HTE doesn't fix

- **Mechanistic insight** — 10 000 wells still doesn't tell
  you *why* the reaction works.
- **Substrate scope ≠ generality** — a method that works on
  100 substrates might fail on the 101st (the molecule you
  care about).
- **Scale-up** — milligram-scale results don't always
  translate to kilo lab.
- **Side products** — UPLC-MS catches major peaks, may miss
  trace impurities relevant for API filings.

## Try it in the app

- **Tools → Lab analysers…** → look up FLIPR Penta + Operetta
  CLS — high-throughput screening platforms used for
  primary HTE assays in drug discovery.
- **Glossary** → search *High-throughput experimentation*,
  *Design of Experiments (DoE)*, *Bayesian optimisation*.

Next: **Cheminformatics + ML for chemistry**.
