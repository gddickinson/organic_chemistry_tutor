# Tautomerism intro

**Tautomers** are constitutional isomers that interconvert
rapidly by migration of a hydrogen atom (or sometimes
heavier groups). They share the same molecular formula but
differ in connectivity.

Tautomers are NOT resonance structures (resonance is
electron movement only, no atom motion).

## Keto-enol tautomerism

The most common case. A carbonyl compound + its enol form:

```
      O                   OH
      ||                  |
R-C-CH₂-R'   ⇌   R-C=CH-R'
   keto                enol
```

For acetone: 99.99 % keto / 0.0001 % enol at equilibrium.
But the enol matters because:

- It's the reactive species in α-halogenation, aldol,
  Mannich.
- Keto/enol equilibria can be acid- or base-catalysed.

## When the enol wins

For β-dicarbonyl compounds, the enol is stabilised by
intramolecular H-bond + extended conjugation:

| Compound | % enol |
|----------|--------|
| Acetone | 0.0001 |
| Cyclopentanone | 0.001 |
| Cyclohexanone | 0.0001 |
| Acetaldehyde | 0.000001 |
| Acetylacetone (pentane-2,4-dione) | 85 (in CCl₄) |
| Acetoacetic ester | 8 (in CCl₄) |
| Phenol | 100 (no keto form possible without losing aromaticity) |

## Enol + enolate

The conjugate base of the enol is the **enolate** —
nucleophile in many C-C bond-forming reactions:

```
enol ⇌ enolate + H⁺          pKa ~ 10-12 for enol O-H
keto ⇌ enolate + H⁺          pKa ~ 20-25 for α-C-H
```

Acidity of α-C-H is enhanced by adjacent EWGs (esters,
nitro, sulfone). A 1,3-dicarbonyl compound has α-pKa ~ 9
(deprotonatable by NaH or even K₂CO₃).

## Imine-enamine tautomerism

```
R₂N-CHR'-CHR''₂  ⇌  R₂N=CR'-CHR''₂  + H₂O ↔  R₂N-CR'=CR''₂
                       (iminium)                 (enamine)
```

Used in iminium organocatalysis (MacMillan) + enamine
organocatalysis (List).

## Lactam-lactim tautomerism

Important in nucleobases:

```
guanine: 2-amino-6-oxo-purine    ⇌    2-amino-6-hydroxy-purine
         (lactam, dominant)            (lactim, minor)
```

Wrong tautomer pairing in DNA → mutation. The **dominant**
tautomer at physiological pH determines correct base pairing.

## Pyridone-hydroxypyridine

```
2-hydroxypyridine ⇌ 2-pyridone
```

The keto form (pyridone) dominates by > 99:1 in water; in
DMSO ~ 1000:1. Often catches students off guard because
the OH form looks more aromatic.

## Tautomers in spectroscopy

- **NMR**: rapid tautomerisation gives averaged signals;
  slow → distinct sets.
- **IR**: keto C=O ~ 1715 cm⁻¹; enol O-H ~ 3300 cm⁻¹
  (broad).
- **MS**: same molecular ion; same molecular formula. No
  way to distinguish without follow-up tests.

## Drug discovery + tautomers

A drug's "real" structure for binding is sometimes a minor
tautomer. Computational tautomer enumeration (RDKit
TautomerEnumerator, SkeletonKey) is now standard for
docking + ML model training.

## Try it in the app

- **Tools → Isomer relationships…** → *Tautomers* tab —
  enter SMILES → get all reasonable tautomers.
- **Reactions tab** → load *Aldol condensation* — see the
  enolate/enol step explicitly.
- **Glossary** → search *Tautomer*, *Keto-enol
  tautomerism*, *Enol*, *Enolate*.

Next: **Acid-base titrations + indicators**.
