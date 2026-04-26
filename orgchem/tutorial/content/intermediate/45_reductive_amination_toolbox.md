# Reductive amination toolbox

**Reductive amination** is the dominant amine-installation
method in modern medicinal chemistry. It cleanly mono-
alkylates an amine + a carbonyl in one pot.

## The base reaction

```
R₂C=O + R'-NH₂ → R₂C=N-R' (imine) → R₂CH-NH-R' (amine)
                  + reductant
```

The imine (or iminium) is reduced in situ to the saturated
amine.

## Common reductant choice

| Reductant | pKa range | Substrate scope |
|-----------|-----------|------------------|
| **NaBH₃CN** (sodium cyanoborohydride) | pH 6-8 | Mild; selective for iminium over carbonyl; reduces only the protonated species. WORKHORSE. |
| **NaBH(OAc)₃** (STAB) | pH 4-7, mostly DCM | Even milder; cheaper than NaBH₃CN; pharma standard. |
| **NaBH₄** | pH > 8 | Reduces the carbonyl, NOT the iminium; only works if imine pre-formed (or Schiff base). |
| **H₂ / Pd-C** | catalytic | Industrial scale; H₂ pressure + cat. Reduces other things too. |
| **H₂ / Raney Ni** | catalytic | Cheap; less selective. |
| **Hantzsch ester** | mild, organic | Photoredox-friendly; biomimetic. |
| **Borane / BH₃-THF** | mild | Not selective; over-reduces. |

NaBH(OAc)₃ in DCM with a drop of AcOH is the modern
default — selective, cheap, predictable.

## Why one-pot beats imine isolation

Forming + isolating an imine is annoying:

- Hygroscopic or oily.
- Often needs azeotropic water removal (Dean-Stark,
  4 Å sieves).
- Imine can hydrolyse during workup.

In situ reductive amination skips the isolation +
typically gives higher yield + cleaner product.

## Substrate scope

Acceptable carbonyls:

- **Aldehydes** — easy; iminium forms fast + reduces
  cleanly.
- **Ketones** — slower; need acid catalysis; α,β-unsat
  ketones tend to also reduce the alkene (use NaBH(OAc)₃
  to spare the alkene).
- **Aryl aldehydes** + benzaldehyde derivatives — easy.

Acceptable amines:

- **Primary alkylamines** — most common.
- **Secondary amines** (R₂NH) — gives R₃N tertiary amine.
- **Anilines** — slower (electron-poor N).
- **Hydrazines** — give hydrazines (different chemistry).
- **Hydroxylamines** — give hydroxylamines.

NOT directly compatible:

- **Tertiary amines** (R₃N) — no N-H to lose.
- **Amides** — too poor as nucleophile; need a different
  approach.

## Asymmetric reductive amination

For chiral amine synthesis:

- **Hantzsch ester + chiral phosphoric acid** (List, MacMillan
  organocatalysis, 2010s) — > 95 % ee.
- **Ir-catalysed asymmetric reductive amination** — H₂ +
  chiral Ir-phosphine.
- **Enzyme-catalysed (transaminase)** — KRED + transaminase
  cascade for industrial chiral amine synthesis (Codexis;
  sitagliptin process is the famous case).

## Practical recipe (NaBH(OAc)₃)

```
1. Combine R₂C=O (1.0 eq) + R'-NH₂ (1.05 eq) in DCM at rt.
2. Stir 5-15 min.
3. Add NaBH(OAc)₃ (1.4 eq) and AcOH (1.0 eq).
4. Stir 1-12 h at rt.
5. Quench with sat. NaHCO₃; extract with DCM.
6. Concentrate; chromatograph if needed.
```

Yield typically 60-90 %.

## Common gotchas

- **Carbonyl with α-H + base** can do aldol before
  reductive amination → side products.
- **Sterically hindered ketones** (t-Bu next to C=O)
  → very slow; switch to STAB + AcOH at higher T or
  Pd/H₂.
- **Aniline + electron-poor carbonyl** → slow; needs
  excess aldehyde + acid.
- **Diethanolamine adducts** → unwanted with formaldehyde +
  amines (Eschweiler-Clarke variant — uses HCOOH as
  reductant + Δ → N-methylation).

## Eschweiler-Clarke methylation

```
R-NH₂ + HCHO + HCOOH → R-N(CH₃)₂  (N,N-dimethylation)
```

A reductive-amination variant where formaldehyde + formic
acid drive the system to mono- or di-methylation.

## Try it in the app

- **Reactions tab** → load *Reductive amination* (if
  seeded).
- **Tools → Lab reagents…** → look up STAB, NaBH₃CN,
  Hantzsch ester for hazards + storage.
- **Glossary** → search *Reductive amination*,
  *Iminium ion*, *NaBH(OAc)₃*, *Hantzsch ester*.

Next: **Reformatsky reaction**.
