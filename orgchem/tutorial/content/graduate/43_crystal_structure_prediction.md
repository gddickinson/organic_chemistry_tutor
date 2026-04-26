# Crystal structure prediction (CSP)

Given a chemical formula or 2D structure, can we
**computationally predict** its crystal structure +
polymorphs? CSP has matured from a research curiosity to
a routine tool in pharma + materials.

## The CSP pipeline

```
1. Generate candidate packings (millions per molecule).
2. Score each by force-field energy.
3. Re-rank top hits by DFT or DFT+D.
4. Identify the most-stable predicted polymorph.
5. Compare to experimental form (if known) or guide search
   for new forms.
```

## Why CSP matters

### Pharma — polymorph risk

Drug efficacy + bioavailability depend on crystal form.
Famous failures (Cefdinir, Ritonavir's Form II) cost
hundreds of millions when an unexpected form appeared.

CSP **predicts** all energetically accessible forms
before scale-up + helps mitigate polymorph risk.

### Materials — design

For high-performance materials (hydrogen-storage MOFs,
photovoltaic perovskites, OLED emitters):

- Predict if a target molecular packing is stable.
- Rank candidates before synthesis.
- Identify packing motifs that maximise function.

### Ferromagnetism, conductivity, mechanical strength

All depend on crystal structure. CSP enables targeted
materials discovery.

## Algorithms

### USPEX (Oganov)

Genetic-algorithm-based CSP. Random initial population +
crossover + mutation + DFT scoring → evolve toward
low-energy structures. Used heavily in extreme-T,P
materials prediction.

### CALYPSO

Particle-swarm optimisation. Used for high-pressure +
exotic stoichiometries.

### ChemicalLandscape (Schrödinger)

Conformational + packing search → DFT re-ranking.
Commercial pharma platform.

### CSP@CCDC

Cambridge Crystallographic Data Centre's CSP suite.
Industry standard for pharmaceutical polymorph prediction.

### Pedone / Crystals.NET (academic)

Academic packages.

## Energy ranking accuracy

Modern CSP achieves:

- **Top-10 hit rate**: > 90 % for small organics; the
  experimental form is among the top 10 predicted.
- **Energy ranking**: ± 1 kcal/mol.
- **Failures** common when:
  - Hydrogen bonding is intricate.
  - Non-covalent interactions (CH-π, halogen bonds) are
    mis-modelled.
  - The molecule is highly flexible (many conformers).

DFT+D corrections (D3, D4 dispersion) are essential for
organic crystals — most accuracy comes from getting
dispersion right.

## Famous CSP campaigns

- **CCDC CSP Blind Test (2007-2017)** — anonymous
  benchmark; teams submit predictions for unreleased
  crystal structures. Modern teams identify top-1 form
  ~ 80 % of the time.
- **Pfizer + Schrödinger** — apply CSP routinely in early
  development; flag risky polymorphs.
- **Vertex's Trikafta (cystic-fibrosis drug)** — CSP-
  guided polymorph screening before launch.
- **GSK + Eli Lilly** — internal CSP groups.

## Beyond polymorphs — CSP for solvates + cocrystals

CSP can also predict:

- **Hydrates** — drug + water co-crystals.
- **Solvate forms** — DCM-, MeOH-, DMSO-solvated forms.
- **Cocrystals** — drug + coformer combinations (e.g.
  carbamazepine + saccharin).

The cocrystal-screening problem now usually starts with
CSP: predict which coformers + ratios give stable
cocrystals → focused experimental screen.

## Challenges remaining

- **Conformational flexibility** — many torsional angles
  → exponentially many candidate packings.
- **Disorder + partial occupancy** — modern CSP starts
  including this.
- **Long-range electrostatics + dispersion** — DFT+D3 /
  D4 + many-body dispersion improving accuracy.
- **Kinetics** — CSP predicts thermodynamic structure;
  the kinetically preferred form during crystallisation
  may differ.

## Modern ML in CSP

ML potentials (MACE, NequIP, AIMNet) replace DFT in
CSP scoring → 10-100× speedup with similar accuracy.

Generative models (CDVAE, DiffCSP) propose candidate
packings from chemistry input → reduces search space
massively.

## Try it in the app

- **Tools → Lab analysers…** → look up XRD instruments
  (Bruker D8, Rigaku XtaLAB).
- **Glossary** → search *Crystal structure prediction*,
  *Polymorphism*, *USPEX*, *CCDC*, *DFT+D*, *Cocrystal*.

Next: **Free-energy methods for enzymes (FEP, EVB,
QM/MM)**.
