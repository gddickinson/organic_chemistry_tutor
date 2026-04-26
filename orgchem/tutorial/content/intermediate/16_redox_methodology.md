# Reduction + oxidation methodology

Half of synthesis is bond-making; the other half is **oxidation
state adjustment**. This lesson surveys the named reagents you
need to recognise + know when to use.

## The redox ladder for one carbon

```
CH₄ → CH₃OH → HCHO → HCOOH → CO₂
−4    −2     0      +2     +4   (oxidation state of C)
```

Each step up is **oxidation** (electron loss); each step down is
**reduction** (electron gain). Synthetic chemistry is mostly
walking this ladder for specific carbons within bigger molecules.

## Reduction reagents

### Hydride donors

Reagent | Strength | Selectivity
---|---|---
NaBH₄ | mild | aldehydes, ketones; survives water + alcohols
LiAlH₄ | strong | reduces almost everything (esters, amides, nitriles, epoxides)
DIBAL-H | tunable | esters → aldehydes (1 eq, low T) or alcohols (excess)
LiBH₄ | mid | esters → primary alcohols selectively
L-Selectride | bulky | hindered ketones; equatorial alcohol from cyclohexanones
NaBH(OAc)₃ | mild | reductive amination (selective for iminium over ketone)
NaCNBH₃ | very mild | reductive amination at neutral pH

### Catalytic hydrogenation (H₂ + metal)

- **Pd/C** + H₂ → reduces alkenes, alkynes, benzyl ethers,
  Cbz groups; spares aromatic rings + most carbonyls.
- **Pt/C** + H₂ → similar to Pd but reduces some aromatics.
- **Lindlar's catalyst** (Pd/CaCO₃ poisoned with Pb) → alkyne
  → cis-alkene (stops at the alkene).
- **Na/NH₃ (Birch reduction)** → alkyne → trans-alkene; also
  reduces aromatic rings to 1,4-cyclohexadienes.

### Stereoselective reductions

- **CBS reduction** (Corey-Bakshi-Shibata) — chiral
  oxazaborolidine + BH₃; ketones → enantiopure alcohols.
- **Ru-BINAP** asymmetric hydrogenation (Noyori, 2001 Nobel)
  — β-keto esters → β-hydroxy esters with > 99% ee.

The seeded **NaBH₄ reduction**, **CBS reduction**, **Birch
reduction** entries walk the mechanisms.

## Oxidation reagents

### Alcohol → aldehyde (1°) / ketone (2°)

Reagent | Selectivity
---|---
PCC (pyridinium chlorochromate) | 1° → aldehyde (NOT acid); 2° → ketone
Swern (DMSO + (COCl)₂ + Et₃N) | mild, neutral; great for sensitive substrates
Dess-Martin periodinane (DMP) | mild, neutral, fast; current workhorse
Jones (CrO₃ + H₂SO₄ in acetone) | 1° → carboxylic acid; 2° → ketone
TPAP (tetrapropylammonium perruthenate) | catalytic Ru, mild

### Alkene → diol or epoxide

- **OsO₄ + NMO** (Upjohn) → cis-diol.
- **mCPBA** (peracid) → epoxide.
- **Sharpless asymmetric epoxidation** (Ti / DET) — allylic
  alcohol → enantiopure epoxide.
- **Sharpless asymmetric dihydroxylation** (OsO₄ + chiral
  ligand AD-mix-α / β) — alkene → enantiopure diol.

### Alkene → carbonyl (cleavage)

- **Ozonolysis** (O₃ + Me₂S) → 2 carbonyls (lesson on
  ozonolysis in the named-reactions tab).
- **OsO₄ + NaIO₄** → same cleavage, two-step.

### Wacker oxidation

Pd(II)-catalysed alkene → methyl ketone (Markovnikov-like
oxygen addition). Industrially huge for converting ethylene
to acetaldehyde.

## Oxidation-state manipulation strategy

When planning a synthesis, count the **oxidation state of each
target carbon** and compare to your starting material. Every
ladder step needs a reagent. Build the count into your
retrosynthesis to avoid surprise dead-ends late in a route.

## Try it in the app

- **Reactions tab** → load PCC oxidation, NaBH₄ reduction,
  Swern oxidation, Dess-Martin oxidation, Jones oxidation,
  Wacker oxidation, Birch reduction, CBS reduction, Sharpless
  asymmetric epoxidation, Sharpless asymmetric dihydroxylation.
- **Glossary** → *Homolysis vs heterolysis*, *Oxidation state*.
- **Tools → Lab reagents…** — reference cards for all
  catalysts + reagents above.

Next: **Amines + their chemistry**.
