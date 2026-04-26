# Conjugate acid-base pairs + the pKa table

The **pKa** of an acid HA is `−log Ka`, where Ka is the
dissociation equilibrium constant `[A⁻][H⁺] / [HA]`. Lower pKa
= stronger acid = greater tendency to release the proton.

The pKa table organises every acid-base reaction in organic
chemistry. Memorising the rough position of common groups is
the most leveraged investment a chemistry student can make.

## A working pKa table

pKa | Acid | Conjugate base
---|---|---
−10 | HI, HBr, HCl (strong inorganic) | I⁻, Br⁻, Cl⁻
−1.7 | H₃O⁺ | H₂O
0 | TFA (CF₃COOH) | CF₃COO⁻
1.3 | CCl₃COOH | CCl₃COO⁻
2.9 | CHCl₂COOH | CHCl₂COO⁻
3.8 | HCOOH (formic) | HCOO⁻
4.8 | CH₃COOH (acetic) | CH₃COO⁻
4.2 | benzoic acid | benzoate
6.4 | H₂CO₃ | HCO₃⁻
7.0 | water (autoionisation) | OH⁻ + H⁺
9.4 | NH₄⁺ | NH₃
10 | phenol | phenoxide
10.7 | (CH₃)₃NH⁺ | (CH₃)₃N
13 | malonic ester (active methylene) | enolate
15.7 | water | OH⁻
16 | ethanol | ethoxide
20 | acetone (α-H) | enolate
24 | acetylene | acetylide
25 | methyl ketone (α-H) | enolate
35 | NH₃ | NH₂⁻
36 | DMSO α-H | dimsyl
44 | benzene C–H | phenyl⁻
50 | alkane C–H (sp³) | carbanion (rare)

## How to use it

The single most important rule: **a base will deprotonate any
acid weaker than the conjugate acid of itself.** In other
words, the equilibrium:

```
HA + B  ⇌  A⁻ + BH⁺
```

lies to the right when **pKa(HA) < pKa(BH⁺)**.

Worked examples:
- **NaOH (conj. acid pKa 15.7) + ethanol (pKa 16)** → only
  partial deprotonation; ethoxide is barely formed.
- **NaH (conj. acid pKa 35) + ethanol (pKa 16)** → quantitative
  deprotonation; H₂ gas evolves; ethoxide forms cleanly.
- **NaH (pKa 35) + acetone α-H (pKa 20)** → quantitative
  enolate formation.
- **LDA (lithium diisopropylamide; conj. acid pKa 36) + ester
  α-H (pKa 25)** → standard "kinetic enolate" generation
  protocol.

## Choosing your base

Match base strength to the substrate's pKa:

- **Carboxylic acids (pKa 3-5)** → NaHCO₃, NaOH, K₂CO₃,
  Et₃N all work.
- **Phenols (pKa 10)** → NaOH works; carbonates (NaHCO₃) are
  too weak.
- **Alcohols (pKa 16)** → need NaH or NaNH₂ for full
  deprotonation; metal hydrides are the workhorse.
- **Ketone α-H (pKa 20)** → use LDA, KHMDS, NaHMDS for
  kinetic enolate; NaOH/NaOR gives only partial conversion.
- **Terminal alkyne (pKa 24)** → NaH or NaNH₂; the resulting
  acetylide is a strong nucleophile.
- **NH₂ of amines (pKa 35)** → use n-BuLi or NaNH₂.

## Try it in the app

- **Tools → pH explorer…** (Ctrl+Alt+H) — full 46-acid pKa
  lookup table organised by category. Use the buffer designer
  + titration-curve tabs for quantitative work.
- **Glossary** → search for *pKa*, *Buffer*, *Henderson-
  Hasselbalch*, *Lithium diisopropylamide* for the formal
  definitions.
- **Reactions tab** → load *Aldol condensation* or *Claisen
  condensation* — the enolate-formation pKa logic is
  rendered in the mechanism.

Next: **Enthalpy, entropy, and free energy in organic
reactions**.
