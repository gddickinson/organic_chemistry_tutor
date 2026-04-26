# Appel reaction + similar OH-activation tricks

A small family of reagents converts an alcohol into a halide
under mild conditions. Each has its niche.

## Appel reaction (1975)

```
R-OH + CCl₄ + PPh₃ → R-Cl + CHCl₃ + Ph₃P=O
R-OH + CBr₄ + PPh₃ → R-Br + CHBr₃ + Ph₃P=O
R-OH + CI₄  + PPh₃ → R-I  + CHI₃  + Ph₃P=O
R-OH + CCl₃CN + PPh₃ → R-Cl + Cl₂CHCN + Ph₃P=O
```

- Mild (rt or 0 °C); compatible with most FGs.
- Inversion of configuration (SN2-like).
- Workup: filter Ph₃P=O off; column.

Mechanism: PPh₃ + CX₄ → Cl-P(Ph)₃-CX₃ → activates ROH by
forming R-O-PPh₃⁺ → X⁻ does SN2.

## Mitsunobu vs Appel

| | Mitsunobu | Appel |
|----|-----------|-------|
| Reagents | PPh₃ + DIAD + Nu-H | PPh₃ + CX₄ |
| Product | R-Nu (any acidic Nu-H) | R-X (halide) |
| Stereochemistry | inversion | inversion |
| Atom economy | poor | poor (CX₄ partly waste) |
| Cost | $$ | $ |

Use Mitsunobu when you want a specific N / O / S nucleophile;
use Appel when you just want the halide.

## Other OH → halide reagents

### Thionyl chloride (SOCl₂)

```
R-OH + SOCl₂ → R-Cl + SO₂↑ + HCl↑
```

- 1° + 2° alcohols → 1° + 2° chlorides.
- Mechanism through R-OSOCl → SN2 (with retention if
  pyridine present; SNi without).
- Cheap, scalable. Industrial workhorse.
- Pyridine added to neutralise HCl; in pyridine sometimes
  proceeds through SNi → retention.

### Phosphorus tribromide (PBr₃)

```
R-OH + PBr₃ → R-Br + HOPBr₂
```

- Like SOCl₂; for bromides.
- Inversion of configuration.

### Phosphorus pentachloride (PCl₅)

```
R-OH + PCl₅ → R-Cl + POCl₃ + HCl
```

- Harsher; for tough substrates.
- Industrial use.

### HX + ZnX₂ (Lucas reagent)

```
R-OH + HCl/ZnCl₂ → R-Cl + H₂O
```

- Tertiary OH → 3° R-Cl (SN1; very fast at rt).
- Secondary OH → 2° R-Cl (slower; ~ 1-5 min).
- Primary OH → 1° R-Cl (very slow, needs heat).
- Diagnostic test for alcohol class (1° vs 2° vs 3°).

### DAST (and Deoxofluor)

```
R-OH + DAST → R-F + Et₂N-S=O + Et₂N-S(F)-OH
```

- Diethylaminosulfur trifluoride; converts OH → F with
  inversion.
- Also converts C=O → CF₂ (gem-difluoride).
- Classical reagent for mild fluorination.
- Modern Deoxofluor (Deoxo-Fluor) is safer to handle.

## Tosylation + mesylation (related approach)

Convert OH to a leaving-group ester:

```
R-OH + TsCl + pyridine → R-OTs + HCl·py
R-OH + MsCl + Et₃N      → R-OMs + Et₃N·HCl
```

- Tosylate (R-OTs) — moderate LG (~ HOTs LG; pKa -3).
- Mesylate (R-OMs) — better LG; cheaper reagent.
- Triflate (R-OTf, from Tf₂O / pyridine) — superior LG;
  pKa of HOTf -14.

Then SN2 with any nucleophile:

```
R-OTs + NaCl/DMF → R-Cl
R-OMs + NaN₃     → R-N₃
R-OTs + NaCN     → R-CN
```

Inversion at C; the LG is "good enough" for most Nu.

## Why so many alternatives?

Each method's selectivity + tolerance differ:

- **SOCl₂**: tolerates esters + ketones; loses water as
  SO₂ + HCl.
- **PBr₃**: similar; tolerates more.
- **Mitsunobu**: tolerates everything but is expensive +
  waste-heavy.
- **Appel**: tolerates many FGs; mild.
- **DAST**: harsh on adjacent functional groups; for F
  installation.

## Try it in the app

- **Tools → Lab reagents…** → look up SOCl₂, PBr₃, TsCl,
  MsCl, Tf₂O for hazards + procedures.
- **Tools → Stereochemistry…** → confirm inversion of OH
  → halide via Appel.
- **Glossary** → search *Appel reaction*, *Tosylate*,
  *Mesylate*, *Triflate*, *DAST*, *Mitsunobu reaction*.

Next: **Reductive amination toolbox**.
