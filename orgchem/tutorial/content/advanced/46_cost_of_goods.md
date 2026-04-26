# Cost of goods + green metrics for process

For a drug to be commercial, the **cost of goods (COGS)**
matters as much as the chemistry. Process chemists balance
yield, cost, safety, environmental impact, + intellectual
property to optimise the route.

## What COGS includes

```
COGS = raw materials + reagents + solvents + catalyst +
       energy + labour + waste handling + facility +
       quality control + depreciation
```

For a typical small-molecule API:

- **Raw materials**: 10-40 % of COGS.
- **Solvents**: 30-60 % (dwarfing reagent costs).
- **Energy** (heating, cooling, distillation): 10-20 %.
- **Labour + facility**: 20-40 % at smaller scale; 5-10 %
  at very large scale.

The "**80/20 rule**": ~ 80 % of COGS comes from ~ 20 % of
unit operations (typically the chromatography + the
dilute-stoichiometry steps).

## Green metrics

### Atom economy (AE)

```
AE = MW(product) / Σ MW(reactants) × 100 %
```

Target ≥ 50 % for late-stage steps.

### Reaction mass efficiency (RME)

```
RME = mass(product) / mass(all inputs) × 100 %
```

Includes solvent + catalyst — closer to real waste than AE.

### E-factor

```
E = mass(waste) / mass(product)
```

Pharma typical: 25-100. Bulk chem: 0.1-5.

### Process Mass Intensity (PMI)

```
PMI = mass(all materials) / mass(product) = E + 1
```

Industry-preferred since 2010. Pfizer, AstraZeneca, GSK +
others publish PMI for top APIs.

### CO₂ footprint

```
kg CO₂-eq / kg API
```

Includes solvent recovery, energy, transport. Driven by
solvent (often 60-80 % of footprint).

### Solvent intensity

```
mass(solvent) / mass(product)
```

Solvent is the dominant green-metric driver. Reducing
solvent = reducing E-factor + PMI + CO₂.

## Optimising COGS — process chemistry tactics

### 1. Replace expensive reagents

- **Boronic acids → boronic esters** ($2/g vs $20/g for
  some).
- **Pd / XPhos → Ni / NHC** (10× cheaper metal).
- **Hindered TBSCl → TES Cl** if functional protection
  allows.

### 2. Reduce solvent

- Switch from DCM (11 L/kg API typical) to MTBE / 2-MeTHF.
- Use higher concentration (0.1 M → 1 M reduces solvent
  10×).
- Telescope steps (carry forward without isolating).
- Continuous-flow chemistry — uses less solvent per kg.

### 3. Recycle catalyst + solvent

- Polymer-supported Pd → filter + recycle.
- Distill + recycle solvent — most pharma plants do this.
- Process developers measure recovery efficiency in the
  PMI calculation.

### 4. Replace chromatography

- Replace silica column with crystallisation or extraction.
- A single chromatography step adds ~ 10 L solvent / g
  product → kills PMI.
- Modern process: NO chromatography in any step beyond
  early discovery.

### 5. Use biocatalysis

- Enzyme-catalysed steps often have superior selectivity
  + atom economy.
- Sitagliptin (Codexis transaminase) — 19 % less waste,
  60 % less solvent vs Rh / H₂.

### 6. Asymmetric methods late in synthesis

- Install chirality late → don't carry chirality through
  many steps.
- Avoid racemic intermediates needing chiral resolution
  → ~ 50 % yield loss.

## ACS Green Chemistry Pharmaceutical Roundtable

A consortium of pharma + academic chemists tracking PMI
for top APIs since 2005:

- **Top APIs** (sertraline, atorvastatin, sitagliptin,
  etc.) — PMI improvement tracked over time.
- **CHEM21 metrics toolkit** — open-source PMI calculator.
- **IQ Consortium** — collaborative process-development
  group.

## Famous green-process improvements

| API | Original PMI | Improved PMI | How |
|-----|--------------|---------------|-----|
| Sertraline (Zoloft) | ~ 200 | ~ 35 | solvent change DCM → EtOH |
| Sitagliptin (Januvia) | ~ 130 | ~ 40 | Codexis transaminase replaced Rh / H₂ |
| Imatinib (Gleevec) | ~ 80 | ~ 30 | telescoped + crystallised |
| Atorvastatin (Lipitor) | ~ 50 | ~ 15 | replaced Cr-mediated step |
| Lumacaftor / Ivacaftor (Orkambi) | – | continuous manufacturing | Vertex flow process |

## Commercial vs Discovery vs Process — different priorities

| Priority | Discovery | Process | Commercial |
|----------|-----------|---------|------------|
| Yield | mid | high | very high |
| Step count | high (many SAR) | low | very low |
| Cost | low | medium | very low |
| Reproducibility | low | high | very high |
| Safety | medium | high | very high |
| Green metrics | low | high | very high |

A discovery chemist's "great synthesis" often becomes a
process chemist's nightmare, then a commercial chemist's
art form.

## Try it in the app

- **Tools → Green metrics (atom economy)…** → input a
  reaction or a synthesis pathway → see AE + step
  metrics.
- **Tools → Lab calculator…** → *Stoichiometry* tab to
  compute waste from yields.
- **Glossary** → search *Atom economy*, *E-factor*,
  *Process mass intensity*, *Cost of goods*, *Green
  chemistry*.

Next: **Solid-state NMR** (graduate tier).
