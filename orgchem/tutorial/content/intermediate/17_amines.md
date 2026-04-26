# Amines and their chemistry

Amines are the **second-most-common functional group in drugs**
(after the carbonyl). 60% of small-molecule pharmaceuticals
contain at least one amine. The chemistry that makes amines is
therefore one of the most-asked questions in pharma synthesis.

## Classification

- **Primary (1°)** — RNH₂. Methylamine, aniline.
- **Secondary (2°)** — R₂NH. Diethylamine, piperidine.
- **Tertiary (3°)** — R₃N. Triethylamine, DMAP.
- **Quaternary (4°)** — R₄N⁺. Acetylcholine, betaine —
  always charged + non-basic (no lone pair on N).

## Basicity + pKa(BH⁺)

Amines are **basic** because the lone pair on N picks up a
proton. The pKa of the **conjugate acid** (RNH₃⁺) measures
basicity:

Amine | pKa(BH⁺) | Notes
---|---|---
methylamine | 10.7 | typical sp³ amine
diethylamine | 11.0 | slightly more basic (more inductive donation)
piperidine | 11.3 | cyclic 2°
triethylamine | 10.7 | typical 3°
DBU (1,8-diazabicycloundec-7-ene) | 12.5 | superbase, non-nucleophilic
DMAP | 9.7 | hugely nucleophilic on N1
aniline (PhNH₂) | 4.6 | weak — N lone pair into the ring
pyridine | 5.2 | sp² N, weaker
imidazole | 7.0 | N1, biological pH range

## Three ways to make an amine

### 1. Reductive amination

Most common in pharma. Carbonyl + amine → imine → reduction
to the substituted amine:

```
R-CHO + R'NH₂ → R-CH=NR' (imine) → R-CH₂-NHR' (amine)
   reductant: NaBH(OAc)₃ or NaCNBH₃ (selective for iminium)
```

The single-step protocol with NaBH(OAc)₃ in DCE is the
**workhorse method**.

### 2. Direct alkylation (often messy)

```
R-Br + R'NH₂ → R-NHR' + R-NR'₂ + R-NR'₃⁺ Br⁻
                (multiple alkylations — hard to stop at the
                 mono-alkyl product unless you use excess amine)
```

The Hofmann ammonolysis route — historically common, now
mostly replaced by reductive amination.

### 3. Reduction of amides / nitriles / nitro / azides

- **Amide → amine** (LiAlH₄ or BH₃·THF).
- **Nitrile → primary amine** (LiAlH₄ or H₂ + Pd).
- **Nitro → primary amine** (H₂ + Pd, or Sn + HCl, or Fe +
  HCl).
- **Azide → primary amine** (H₂ + Pd, or Staudinger reduction
  with PPh₃ + H₂O — bioorthogonal).

## Reactivity of amines

- **Acylation** with acid chlorides + anhydrides → amides.
  See lesson 12 on acyl substitution.
- **Sulfonylation** with sulfonyl chlorides → sulfonamides.
- **Buchwald-Hartwig amination** — Pd-catalysed cross-
  coupling of aryl halide + amine → arylamine. The standard
  modern way to make Ar–N bonds.
- **Reductive amination** as above.

The seeded **Buchwald-Hartwig amination** entry walks the
Pd cycle.

## Aromatic amines + the Sandmeyer reaction

Aryl amines (anilines) → diazonium salts (NaNO₂ + HCl, 0 °C):

```
Ar-NH₂ → Ar-N₂⁺ Cl⁻
```

The diazonium + various nucleophiles → Ar-Cl, Ar-Br, Ar-CN
(Sandmeyer, with Cu catalysis), Ar-OH (warm water), Ar-H
(H₃PO₂), Ar-Ar (azo coupling for dyes).

## Try it in the app

- **Reactions tab** → load *Buchwald-Hartwig amination* +
  *Mitsunobu reaction* (alcohol → amine via inversion).
- **Glossary** → *pKa*, *Henderson-Hasselbalch*, *Reductive
  amination*.
- **Molecule Workspace** → load drug examples (Caffeine, 4
  N's; Diazepam; Ibuprofen — wait that has no N) to see how
  amines integrate into pharmaceutical scaffolds.

Next: **Heterocyclic chemistry intro**.
