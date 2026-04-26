# Enolates and α-functionalisation

The α-carbon of a carbonyl (the C adjacent to C=O) is the
**most-functionalised carbon position in synthesis**. Almost
every named C–C bond-forming reaction in the *Reactions* tab
goes through an **enolate** intermediate at some point.

## What's an enolate?

An α-H of a ketone (pKa ~ 20) or ester (pKa ~ 25) is
removable by a strong base. The conjugate base — the
**enolate** — is a resonance hybrid:

```
   O                    O⁻
   ‖                    |
   C–CH₂–R   ↔   C=CH–R         (carbanion form ↔ enolate form)
```

The negative charge sits partially on **both** the α-carbon
(carbanion-like, nucleophilic at C) and the oxygen
(O-localised, nucleophilic at O).

In practice the C-bound form is the kinetic + nucleophilic
character; the enolate attacks electrophiles **at the α-carbon**
in essentially every named α-functionalisation.

## Choosing your base

Different bases give different selectivity:

- **NaOH, KOH, NaOR** — equilibrium deprotonation. Best for
  reactions where the more-acidic α-H is the one you want.
  Aldol condensation runs here.
- **NaH, KH** — irreversible deprotonation (H₂ gas
  byproduct). Quantitative enolate formation; useful when the
  parent acid is much less acidic than water.
- **LDA (lithium diisopropylamide; pKa(BH⁺) ~ 36)** — the
  workhorse for **kinetic enolate** formation. At −78 °C in
  THF, LDA selectively deprotonates the **less-substituted**
  α-position (the one that's faster to deprotonate, before
  equilibrium can set in). The kinetic enolate is the one
  used for stereoselective alkylation.
- **KHMDS, NaHMDS, LiHMDS** — bulky non-nucleophilic bases
  for kinetic enolate formation; less basic than LDA but
  selective.

## The four α-functionalisation reactions

1. **Aldol condensation** — enolate + carbonyl → β-hydroxy
   carbonyl → (dehydration) → α,β-unsaturated carbonyl.
2. **Claisen condensation** — ester enolate + ester →
   β-keto ester (via tetrahedral intermediate).
3. **Michael addition** — enolate + α,β-unsaturated carbonyl
   → 1,4-conjugate addition product (a 1,5-dicarbonyl).
4. **α-Alkylation** — enolate + alkyl halide → α-substituted
   carbonyl. SN2 on the halide.

Plus the auxiliary tools:

- **Mannich reaction** — enolate + iminium → β-amino carbonyl.
- **α-Halogenation** — enolate + Br₂ or Cl₂ → α-haloketone
  (the Hell-Volhard-Zelinsky reaction is the carboxylic-acid
  variant).

## The Robinson annulation cascade

A classic enolate cascade builds rings in one pot:

1. **Michael addition** — enolate adds to a vinyl ketone
   (often methyl vinyl ketone, MVK).
2. The Michael adduct now has both an enolate site + a
   carbonyl 4 carbons away.
3. **Intramolecular aldol condensation** closes a 6-membered
   ring.
4. **Dehydration** gives the α,β-unsaturated cyclohexenone
   (a "Wieland-Miescher" or "Hagedorn" intermediate).

The seeded **Robinson annulation** entry in the *Reactions*
tab walks the full cascade.

## The Hantzsch + Knoevenagel multi-component reactions

Both lean on **active-methylene compounds** (β-ketoesters,
malonates) that have **two flanking EWGs** + therefore very
acidic α-H (pKa ~ 11). The doubly-acidic α-H means even mild
bases (piperidine, NH₃) generate enough enolate to drive the
reaction.

## Try it in the app

- **Reactions tab** → load *Aldol condensation*, *Claisen
  condensation*, *Michael addition*, *Robinson annulation*,
  *Hantzsch dihydropyridine synthesis*, *Knoevenagel
  condensation*, *Henry reaction* — all walk the enolate-
  formation step explicitly.
- **Glossary** → *Active-methylene compound*, *Multi-
  component reaction*, *Lithium diisopropylamide*.
- **Tools → pH explorer…** → check the pKa of the α-H of any
  carbonyl class.

Next: **Aldol + Claisen condensations — going deeper**.
