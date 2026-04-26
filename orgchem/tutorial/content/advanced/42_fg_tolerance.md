# Functional group tolerance — design rules

Modern reactions must tolerate the dozens of functional
groups already present on a complex substrate. Knowing
each method's tolerance + incompatibilities is critical
for synthesis design + late-stage functionalisation.

## The basic question

Before applying a method to a complex substrate, ask:

- **What FGs are present** that could react under the
  conditions?
- **What active species** does the method generate?
- **Will those species attack other parts** of my
  substrate?

This is part of "**chemoselectivity**" — selecting one
reactive site over others.

## Tolerance matrix (selected methods)

| Method | OH | NH₂ | COOH | Ester | Ketone | Aldehyde | Alkene | Alkyne | Nitro |
|--------|----|----|------|-------|--------|----------|--------|--------|-------|
| Suzuki (Pd, base) | ok | ok | ok | ok | ok | sometimes | ok | ok | ok |
| Buchwald-Hartwig (Pd) | ok* | maybe | ok | ok | ok | ok | ok | ok | ok |
| Heck | ok | ok | ok | ok | ok | ok | (target) | ok | ok |
| Sonogashira (Pd, Cu) | ok | ok | ok | ok | ok | ok | ok | (target) | ok |
| H₂ / Pd-C | ok | ok | ok | ok | ok | ok | reduce | reduce | reduce |
| H₂ / Lindlar | ok | ok | ok | ok | ok | ok | ok | reduce | ok |
| LiAlH₄ | reduce | ok | reduce | reduce | reduce | reduce | ok | ok | reduce |
| NaBH₄ | ok | ok | ok | ok | reduce | reduce | ok | ok | ok |
| DIBAL (-78°C) | ok | ok | ok | reduce | ok | ok | ok | ok | ok |
| mCPBA | ok | reduce† | ok | ok | reduce† | ok | epoxide | reduce† | ok |
| OsO₄ | ok | ok | ok | ok | ok | ok | dihydroxylate | ok | ok |
| Grignard | reduce | reduce | reduce | reduce | reduce | reduce | ok | ok | reduce |
| LDA / -78 °C | reduce H+ | reduce H+ | reduce H+ | (selective) | reduce H+ | reduce H+ | ok | ok | reduce H+ |
| TBAF | ok | ok | ok | ok | ok | ok | ok | ok | ok |
| KOH (aq) | ok | ok | salt | hydrolyse | sometimes | sometimes | ok | ok | ok |

*Buchwald-Hartwig: some α-OH amines don't survive (β-
hydride elimination of substrate).
†mCPBA: amines and ketones can be over-oxidised
(N-oxides; Baeyer-Villiger).

## Common pitfalls

### "Why did my Grignard fail?"

Grignards react with: NH₂, OH, COOH, COOR, CONR₂, CN,
CHO, C=O, RX, NO₂. If your substrate has any of these,
you need to either:

- **Protect** the offending group (silyl ether for OH,
  Boc for amine, etc.).
- **Use organozinc** (Negishi) instead — much more tolerant.
- **Use organocopper** (Gilman) for soft 1,4-addition.

### "Why did my Suzuki give low yield?"

Common issues:

- **Free OH or NH** — Pd binds → catalyst inhibition;
  protect first.
- **Free α-CHO** — ester-like reactivity at boronate;
  reduce or protect.
- **Multiple aryl bromides** in substrate → run sequential.
- **Base too strong** — K₂CO₃ usually fine; Cs₂CO₃ stronger;
  for sensitive substrates use K₃PO₄ or KOAc.

### "Why did my hydrogenation over-reduce?"

H₂ / Pd-C reduces alkene, alkyne, NO₂, ArOBn, ArO. Use:

- **Lindlar** (poisoned Pd) for alkyne → cis alkene.
- **Pearlman's** (Pd(OH)₂) for chemoselective benzyl
  cleavage with alkene present.
- **Adams' Pt + H₂** for difficult olefins; survives
  ester / amide.

## Designing tolerance

Strategies:

1. **Choose the mildest method** that does the job.
2. **Protecting groups** to mask sensitive groups; remove
   later.
3. **Order of operations** — do harsh chemistry first,
   then install sensitive FGs late.
4. **Late-stage diversification** — react C-H or aryl Br
   late so most of the molecule is built before the
   sensitive step.

## Modern late-stage functionalisation toolbox

- **Yu / Sanford C-H activation** — install F, OH, OMe,
  NHR on a near-final API.
- **Doyle / Davies Rh-carbene C-H insertion** — install
  CR₂ on an inert C-H.
- **Photoredox metallaphotoredox** — install α-amino
  groups, carboxylic acids, fluorides.
- **Biocatalytic oxidation** (Arnold, Codexis) — install
  OH at specific C-H sites with ee > 99 %.

These dramatically reduce the number of protecting groups
needed in modern medicinal-chemistry SAR work.

## Try it in the app

- **Tools → Drug-likeness…** → check Lipinski + PAINS for
  a SMILES; PAINS flags reactive substructures.
- **Tools → Lab reagents…** → look up specific reagents
  for hazards + selectivity notes.
- **Glossary** → search *Chemoselectivity*, *Functional
  group tolerance*, *Protecting group*, *Late-stage
  functionalisation*.

Next: **Catalyst poisoning + sulfur tolerance**.
