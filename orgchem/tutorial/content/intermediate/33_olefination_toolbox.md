# Olefination toolbox — Wittig, HWE, Julia, Peterson

To install a C=C double bond from a carbonyl, you have a
zoo of olefination methods. Each gives different
selectivity, scale, + functional-group tolerance.

## Wittig reaction (1954, Nobel 1979)

```
R₂C=O + Ph₃P=CHR'  →  R₂C=CHR' + Ph₃P=O
```

The phosphorus ylide attacks the carbonyl → 4-membered
oxaphosphetane → retro-[2+2] → alkene + Ph₃P=O.

### Stereoselectivity

- **Stabilised ylide** (Ph₃P=CH-CO₂R, Ph₃P=CHCN) → mostly
  E-alkene.
- **Non-stabilised ylide** (Ph₃P=CH-R alkyl, salt-free
  conditions) → mostly Z-alkene.
- **Semi-stabilised** (Ph₃P=CHPh) → mixture, biased E.

### Pros + cons

- **Pros**: very general; mild; tolerates many FGs.
- **Cons**: Ph₃P=O is stoichiometric waste (~ 280 g per mol
  alkene; ~ 20 % atom economy for simple cases); slow with
  bulky aldehydes; no asymmetric variant on substrate
  control.

## Horner-Wadsworth-Emmons (HWE)

```
(RO)₂P(O)-CH₂-CO₂R' + base → ylide
ylide + R₂C=O → R₂C=CH-CO₂R' + (RO)₂P(O)O⁻
```

- **Strongly E-selective** (> 90 % E for most substrates).
- The phosphonate by-product is water-soluble → easy
  aqueous workup → no chromatography of Ph₃P=O.
- Reagents commercial; cheap.

Variants:

- **Still-Gennari** ((CF₃CH₂O)₂P(O)CH₂CO₂R + KHMDS / 18-c-6)
  → strongly Z-selective.
- **Ando** (Ph(CO)O ester variant) → also Z-selective.
- **Masamune-Roush** (LiCl + iPr₂NEt) → mild conditions
  for sensitive substrates.

## Julia olefination

```
RCH(SO₂Ar)-CHR'OH + Na/Hg → RCH=CHR'
```

Old Julia: aryl sulfone + aldehyde → β-hydroxy sulfone →
sodium-amalgam reduction → alkene (E-selective).

**Julia-Kocienski / modified Julia** (1991, 2000):

- Replace aryl sulfone with benzothiazolyl or pyridyl
  sulfone.
- One-pot: sulfone + base + aldehyde → alkene + ArSO₂⁻
  (no separate reduction).
- Strong E-selectivity for most substrates.

Common with sensitive substrates (no Ph₃P=O to remove).

## Peterson olefination

```
RCH(SiMe₃)-CHR'OH + base or acid → RCH=CHR'
```

- **Acid conditions** (HF, BF₃) → anti elimination → E
  alkene.
- **Basic conditions** (KH) → syn elimination → Z alkene.

So Peterson is **stereoselectable by reagent** — both E
and Z accessible from the same intermediate.

Drawback: sensitive substrate (Si group + α-OH); silyl
species are moisture-sensitive.

## Tebbe olefination + Petasis methylenation

For methylenation (CH₂ installation, not general alkene):

```
R₂C=O → R₂C=CH₂
```

- **Tebbe reagent** (Cp₂TiCH₂·AlMe₂Cl) — methylenates esters
  (won't reduce them; useful when LAH would over-reduce).
- **Petasis reagent** (Cp₂TiMe₂) — gentler; tolerates more
  FGs.
- **Lombardo reagent** (Zn/CH₂Br₂/TiCl₄) — even gentler.
- **Takai olefination** (CrCl₂ + CHX₃) — installs vinyl
  halides (CHCl=CR vs CHBr=CR).

## Olefin metathesis

The modern Wittig replacement for many target alkenes:

```
R-CH=CH₂ + R'-CH=CH₂ + Grubbs cat. → R-CH=CH-R' + CH₂=CH₂
```

- Atom-economical (only ethene is the by-product).
- Can do Z-selective with custom Ru catalysts (Grubbs Z-
  selective).
- Substrate must be a non-conjugated terminal alkene
  typically.

Covered separately in the advanced lesson 10.

## Choice matrix

| Need | Best method |
|------|-------------|
| Z-alkene from a non-stabilised ylide | Wittig (salt-free) |
| E-α,β-unsat ester | HWE |
| Z-α,β-unsat ester | Still-Gennari (HWE variant) |
| E-alkene from a sensitive substrate | Julia-Kocienski |
| Z OR E from same intermediate | Peterson |
| Methylenate an ester | Tebbe / Petasis |
| Install vinyl-Cl or vinyl-Br | Takai olefination |
| Internal alkene from two pieces | metathesis |

## Try it in the app

- **Reactions tab** → load *Wittig reaction* (seeded) for
  mechanism walkthrough.
- **Tools → Retrosynthesis…** → input a target alkene →
  Wittig + HWE disconnections often show up.
- **Glossary** → search *Wittig reaction*, *HWE
  (Horner-Wadsworth-Emmons)*, *Julia olefination*,
  *Peterson olefination*.

Next: **Friedel-Crafts deeper — alkylation, acylation,
limitations**.
