# Green chemistry — the 12 principles + atom economy

**Green chemistry** is the design of chemical processes to
reduce or eliminate hazardous substances. It is a *design
philosophy*, not a separate field — every reaction can be
made greener by attention to atoms, energy, solvent, and
waste.

## The 12 principles (Anastas + Warner, 1998)

1. **Prevention** — better to prevent waste than to treat or
   clean it up.
2. **Atom economy** — synthetic methods should maximise
   incorporation of all materials into the final product.
3. **Less hazardous syntheses** — use + generate substances
   with little or no toxicity.
4. **Safer chemicals** — design products to preserve efficacy
   while reducing toxicity.
5. **Safer solvents + auxiliaries** — avoid where possible;
   when needed, use innocuous ones.
6. **Energy efficiency** — run at ambient T + P where
   possible.
7. **Renewable feedstocks** — biomass + CO₂ over petroleum.
8. **Reduce derivatives** — protecting groups + temporary
   modifications add steps + waste.
9. **Catalysis** — catalytic reagents are superior to
   stoichiometric ones.
10. **Design for degradation** — products should break down
    to innocuous substances at end-of-life.
11. **Real-time analysis** — in-process monitoring to
    prevent pollution before it forms.
12. **Inherently safer chemistry** — reduce accident potential
    (explosions, fires, toxic releases) by design.

## Atom economy (Trost, 1991)

```
Atom Economy = (MW of product / Σ MW of all reactants) × 100 %
```

Counts atoms, not moles. A reaction with 100 % atom economy
incorporates every reactant atom into the product:

- **Diels-Alder cycloaddition**: 100 % AE — diene + dienophile
  → cyclohexene with no by-product.
- **Click chemistry (CuAAC)**: 100 % AE — alkyne + azide →
  triazole, all atoms preserved.
- **Wittig reaction**: ~ 20 % AE — generates triphenylphosphine
  oxide as a stoichiometric by-product (~ 280 g/mol of waste
  per mole of alkene).
- **Grignard + aldehyde**: ~ 70 % AE depending on the R group
  — magnesium salts are stoichiometric waste.

## E-factor (Sheldon, 1992)

```
E-factor = (mass of waste / mass of product)
```

Industry benchmarks:

- **Bulk petrochemicals**: E ~ 0.1 (very lean — large scale,
  high atom economy).
- **Fine chemicals**: E ~ 5-50.
- **Pharmaceuticals**: E ~ 25-100+ (complex multistep
  synthesis with protecting groups + chromatography).

The pharmaceutical industry produces ~ 100 kg of waste per kg
of API — driven mostly by solvents (filtration, work-up,
recrystallisation, chromatography).

## PMI (Process Mass Intensity)

```
PMI = (total mass of all materials in / mass of product)
    = E-factor + 1
```

PMI now preferred over E-factor in industry: it includes the
product mass, so PMI = 1 means a perfect process. ACS Green
Chemistry Pharmaceutical Roundtable tracks PMI for ~ 50 top
APIs as the headline green-process metric.

## Beyond AE/E-factor: holistic metrics

- **Carbon footprint** (kg CO₂-equivalent per kg product) —
  includes solvent recovery, energy use, transport.
- **Water consumption** — process water + cooling water + waste
  treatment.
- **EcoScale** (Van Aken, 2006) — penalty-points calculator
  combining yield + cost + safety + waste.
- **CHEM21 metrics toolkit** — open-source PMI-based dashboard
  used by AstraZeneca + GSK + Pfizer.

## Famous green wins

- **Ibuprofen** — Boots' 6-step synthesis (1960s, AE ~ 40 %)
  → BHC's 3-step Friedel-Crafts + carbonylation route (1991,
  AE ~ 77 %, won the 1997 Presidential Green Chemistry Award).
- **Sertraline (Zoloft)** — Pfizer cut PMI ~ 60 % by switching
  ethanol for the dichloromethane / hexane / THF cocktail in
  the original route.
- **Sitagliptin (Januvia)** — Codexis + Merck developed an
  enzyme-catalysed transaminase route that replaced an Rh +
  high-pressure-H₂ asymmetric hydrogenation. Doubled yield,
  cut waste 19 %, won the 2010 Presidential Green Chemistry
  Award.

## Try it in the app

- **Tools → Green metrics (atom economy)…** → load any seeded
  reaction → see calculated AE; load any seeded pathway → see
  per-step + overall AE breakdown.
- **Reactions tab** → check seeded *Diels-Alder*, *CuAAC* —
  100 % AE class; *Wittig*, *Aldol* — by-product class.
- **Glossary** → search for *Atom economy*, *E-factor*,
  *Green chemistry*.

Next: **Beginner curriculum complete — explore intermediate +
advanced tiers**.
