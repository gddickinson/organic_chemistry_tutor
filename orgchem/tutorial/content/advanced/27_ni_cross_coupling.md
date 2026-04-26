# Ni-catalysed cross-coupling — Negishi, Kumada, photoredox

While Pd dominates the cross-coupling literature, **Ni** has
emerged as an indispensable + complementary metal for
several couplings — cheaper, more reactive toward aryl
chlorides, and the partner of choice in modern
metallaphotoredox chemistry.

## Why Ni vs Pd

| | Pd | Ni |
|----|----|----|
| Cost | $80 / g | $0.70 / g |
| Oxidative addition into ArCl | slow | fast |
| Oxidative addition into ArOTf | medium | medium |
| sp³-sp³ couplings | difficult | excellent |
| Photoredox compatibility | OK | excellent (Ni(I) / Ni(III) accessible) |
| Toxicity | low | medium-high (Ni allergies; carcinogenic) |
| Reactivity scope | broad | broader for aryl Cl, sp³ |

So:

- Aryl bromides + iodides → Pd Suzuki / Heck / Buchwald.
- Aryl chlorides + sp³ couplings → Ni.
- Photoredox cross-couplings → Ni or Cu.

## Kumada coupling (1972)

```
ArX + R-MgX + NiCl₂(dppp) → ArR
```

The original Ni cross-coupling (Kumada + Tamao + Corriu).
Aryl + vinyl halides + Grignards → biaryls / styrenes.

**Pros**:
- Cheap (Grignard reagents widely available).
- Can use ArCl with Ni / NHC catalysts.

**Cons**:
- Grignard intolerant of esters, ketones, nitriles, OH.
- Limited functional-group scope.
- Replaced largely by Suzuki + Negishi for sensitive
  substrates.

## Negishi coupling (1977; 2010 Nobel)

```
ArX + R-ZnX + Pd or Ni cat. → ArR
```

Organozinc partner; tolerates more FGs than Grignard.

- **Pd-cat**: aryl bromides / iodides; standard.
- **Ni-cat**: aryl chlorides + sp³-sp³ couplings (Fu's
  Ni / Pybox systems).

### sp³-sp³ Negishi (Fu)

```
secondary alkyl bromide + alkyl-ZnX + Ni cat. + chiral pybox
→ stereoselective sp³-sp³ coupling
```

Gregory Fu (Caltech) — broke new ground for
enantioselective sp³-sp³ couplings (~ 2010 onward); now
the standard route for many chiral fragment connections.

## Modern Ni cross-coupling

### Reductive cross-coupling (Reisman)

```
R-X + R'-X + Ni cat. + Zn or Mn → R-R'  (no organometallic
                                          partner needed!)
```

Two organohalides + a heterogeneous reductant + Ni →
cross-coupling. Sarah Reisman + Daniel Weix pioneered;
now used routinely in pharma SAR.

### Ni-catalysed C-N coupling (Hartwig variant)

```
ArX + R₂NH + Ni / phosphine + base → ArNR₂
```

Cheaper than Buchwald-Hartwig Pd; works on aryl chlorides
better than Pd.

### Ni-catalysed C-O coupling

```
ArX + R-OH + Ni cat. + base → Ar-OR
```

Buchwald + Hartwig / Doyle / Nakamura developed Ni
versions.

## Metallaphotoredox (MacMillan, Doyle)

Photoredox + Ni acts cooperatively:

- Photoredox catalyst (Ir, Ru, organic dye) generates
  radicals from carboxylic acids, amines, alcohols.
- Ni shuttles between Ni(0) → Ni(I) → Ni(II) → Ni(III) to
  trap the radicals + couple.

```
ArX + R-COOH + Ni / Ir-photocat / blue LED → Ar-R + CO₂↑
```

The 2014 MacMillan/Doyle paper enabled **decarboxylative
arylation** — replacing organozincs / boronates with
carboxylic acids. Saves cost + handles previously
impossible substrates.

## Examples in pharma

- **Decarboxylative arylation** at MIT, Princeton, Pfizer
  → late-stage SAR libraries.
- **Photoredox Ni amination** in drug discovery — install
  alkyl amines on ArX without Pd / Buchwald.
- **Reductive sp³-sp³ couplings** for PROTAC linkers + bRo5
  scaffolds.

## Try it in the app

- **Reactions tab** → load Suzuki coupling for the Pd
  baseline; mentally substitute Ni for cheaper alternative.
- **Tools → Lab reagents…** → look up NiCl₂, Ni(cod)₂,
  NHC ligands.
- **Glossary** → search *Negishi coupling*, *Kumada
  coupling*, *Reductive cross-coupling*,
  *Metallaphotoredox*, *Ni catalysis*.

Next: **Cu chemistry — Ullmann, Glaser, Chan-Lam**.
