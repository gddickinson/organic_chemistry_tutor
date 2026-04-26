# Asymmetric hydrogenation — the original asymmetric catalysis success

The 2001 Nobel Prize (Knowles + Noyori + Sharpless)
recognised three pillars of asymmetric catalysis. Knowles +
Noyori shared half the prize for **asymmetric
hydrogenation** — adding H₂ across a prochiral C=C, C=N, or
C=O to give one enantiomer with > 95 % ee.

## The L-DOPA breakthrough (Knowles, 1968)

Monsanto's industrial L-DOPA synthesis (Parkinson's drug):

```
prochiral acrylate + H₂ + Rh(I)/(S,S)-DIPAMP → L-DOPA
                                                 ee > 95 %
```

DIPAMP — a chiral diphosphine with two stereogenic P atoms —
biases H₂ delivery to one face of the C=C.

This was the **first asymmetric catalysis used at industrial
scale** (kg / yr → multi-tonne / yr).

## The mechanism

For Rh-catalysed asymmetric hydrogenation of a dehydroamino
acid:

1. Substrate binds Rh through the C=C + the carbonyl
   directing group → square-planar Rh(I) complex.
2. Oxidative addition of H₂ → Rh(III) dihydride.
3. **Migratory insertion** — H migrates to one face of the
   bound C=C. Stereochemistry set here.
4. **Reductive elimination** — second H + alkyl → product,
   regenerating Rh(I).

Key insight: the **less reactive diastereomeric Rh-substrate
complex** delivers product faster (Halpern's anti-lock-and-
key principle). The dominant pre-equilibrium intermediate
isn't the productive one.

## Noyori's BINAP / Ru chemistry

**BINAP** — 2,2'-bis(diphenylphosphino)-1,1'-binaphthyl —
Noyori (1980). Atropisomeric chirality (axial, no
stereogenic atom). Combined with Ru:

- **Ru(BINAP)** — hydrogenates β-ketoesters, β-ketoamides,
  α,β-unsaturated acids → > 99 % ee with 0.001-0.01 mol %
  loading.
- **Ru(BINAP)/diamine** — hydrogenates aryl ketones (a
  "non-functionalised" substrate that lacks a directing
  group) by an **outer-sphere bifunctional** mechanism: H⁺
  + H⁻ deliver from Ru-H + N-H simultaneously.

## Industrial applications

- **L-Menthol** (Takasago, 100 + tonnes / yr): Rh/BINAP
  asymmetric isomerisation of geranylamine.
- **L-DOPA** (Monsanto, ongoing): Rh/DIPAMP.
- **Naproxen, Ibuprofen, Sertraline, Aliskiren, Sitagliptin
  (alternative routes)** — all enabled by Rh / Ru
  asymmetric hydrogenation.

## Iridium-catalysed enantioselective imine reduction

Ir/PHOX + Ir/JosiPhos catalysts (Pfaltz, Buchwald) hydrogenate
imines + heteroaromatic N-containing rings. Industrial
example: **(S)-metolachlor** (Syngenta, 10 000 t/yr
herbicide) — Ir-catalysed imine reduction at TON ~ 1 million.

## Modern frontiers

- **Earth-abundant metals** — Fe, Co, Ni, Mn replacing Ir +
  Rh + Ru. Chirik (Co), Beller (Mn), Milstein (Mn pincer)
  catalysts approach the rates + ee of Rh/Ru, far cheaper.
- **Transfer hydrogenation** — uses iPrOH or HCOOH/Et₃N
  instead of H₂ gas. Noyori's Ru/TsDPEN + Wills' tethered
  variants → outer-sphere mechanism, gentle.
- **Asymmetric C=O hydrogenation of CO₂** → formate /
  methanol; enabling green-chemistry one-carbon feedstocks.
- **Photocatalytic asymmetric hydrogenation** — emerging,
  visible-light-driven proton-coupled electron transfer.

## Comparing asymmetric methods

| Method | TON | Loading | ee typical | Cost |
|--------|-----|---------|-----------|------|
| Asymmetric hydrogenation | 10⁴-10⁶ | 0.01-0.1 % | 95-99 % | $$ (Rh, Ir) |
| Asymmetric organocatalysis | 10²-10³ | 5-20 % | 80-99 % | $ |
| Biocatalysis | 10⁵-10⁷ | 0.1-1 % | > 99 % | $$ enzyme |
| Chiral auxiliary | n/a | 1 eq | 95-99 % | $$$ wasteful |

## Try it in the app

- **Tools → Stereochemistry…** → load any chiral drug
  SMILES, see R/S assignments + enantiomer rendering.
- **Tools → Medicinal chemistry…** → look at sertraline,
  naproxen, ibuprofen — drugs where asymmetric
  hydrogenation matters at scale.
- **Glossary** → search *Asymmetric hydrogenation*,
  *BINAP*, *Chiral catalyst*, *Enantiomeric excess*.

Next: **Computational chemistry deep-dive** (graduate tier).
