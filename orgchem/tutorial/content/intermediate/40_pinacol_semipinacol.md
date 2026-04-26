# Pinacol + semipinacol rearrangements

The **pinacol rearrangement** (Fittig, 1860) converts a
1,2-diol into a 1,2-shifted ketone via 1,2-cation
migration.

## The classic pinacol → pinacolone

```
(CH₃)₂C(OH)-C(OH)(CH₃)₂  + H⁺  →  (CH₃)₃C-CO-CH₃ + H₂O
   pinacol                          pinacolone
```

Mechanism:

1. Protonate one OH → -OH₂⁺.
2. Loss of H₂O → tertiary carbocation.
3. **1,2-methyl migration** from the adjacent carbon →
   carbocation now adjacent to the remaining OH.
4. Loss of H⁺ from the OH → ketone.

The migration is the key step. **Migratory aptitude** for
1,2 shifts:

```
H > Ar > tertiary alkyl > secondary alkyl > primary alkyl > methyl
```

So aryl groups migrate preferentially over methyl.

## Predicting the product

Start by identifying which OH protonates → which carbocation
forms. Then the more-stable carbocation forms (more
substituted). Finally, the migration direction is set by
which group can migrate to make the most-stable
intermediate.

Worked example: phenylpinacol → phenacol:

```
PhC(OH)(CH₃)-C(OH)(CH₃)₂
+ H⁺ → PhC(OH)(CH₃)-C⁺(CH₃)₂  (tertiary cation more stable)
+ phenyl migrates: PhC(OH)(CH₃) → C(CH₃)₂Ph  → Me-Ph⁺ → ...
                                + Me migrates → final
```

## Semipinacol rearrangement

A 1,2-shift driven by something OTHER than diol hydrolysis:

- **Epoxide ring-opening** + 1,2-shift = semipinacol.
- **Tosylate** (or other LG) + 1,2-shift.
- **Diazo compound** + 1,2-shift.

```
β-hydroxy tosylate (or epoxide) + Lewis acid →
                 → 1,2-shift → ketone + LG ⁻
```

The OH retains; the LG departs; an adjacent group migrates.
Common in steroid + terpenoid biosynthesis (cation
rearrangements during enzymatic cyclisation).

### Asymmetric semipinacol

Tu, Liu groups + others used chiral Brønsted acid catalysts
(BINOL phosphates) to do asymmetric semipinacol on
prochiral epoxy alcohols → > 90 % ee tertiary alcohols.

## Related rearrangements

### Tiffeneau-Demjanov (ring expansion)

```
β-amino alcohol + HNO₂ → diazonium → loss of N₂ → carbocation
                                  → 1,2-alkyl migration → ring expansion
```

5-mem ring + NH₂ + HNO₂ → 6-mem ring ketone. Used in
steroid synthesis.

### Wagner-Meerwein (general 1,2-shift in carbocations)

Any carbocation + adjacent H or alkyl → 1,2-migration to
form a more-stable carbocation. Pervasive in:

- E1 reactions giving "wrong" alkene.
- SN1 product mixtures.
- Terpene biosynthesis (squalene → cholesterol; numerous
  shifts).

### Beckmann rearrangement (oxime)

```
R₂C=N-OH + H⁺ → R-CO-NHR' (group anti to OH migrates)
```

Industrial: cyclohexanone oxime → caprolactam (Nylon-6
monomer).

### Schmidt reaction

```
R₂C=O + HN₃ + H⁺ → R-CO-NHR' (acyl insertion of N)
```

The Beckmann's N-H source is HN₃.

### Curtius rearrangement

```
R-C(=O)-N₃ → R-N=C=O + N₂  (acyl nitrene → isocyanate)
+ ROH → R-NH-CO-OR (carbamate)
```

Used to convert RCOOH → RNH₂ (with shorter chain).

### Hofmann rearrangement

```
R-CO-NH₂ + Br₂/NaOH → R-NH₂ + CO₂↑
```

Amide → primary amine with one less C. Mechanism through
acyl nitrene similar to Curtius.

## All these rearrangements share a core mechanism

A migrating group moves from one atom to an adjacent atom
that's electron-poor (cation, nitrene, carbene). The
cyclic 3-centre TS allows the migration with retention
of stereochemistry at the migrating C.

## Try it in the app

- **Reactions tab** → load *Pinacol rearrangement* (seeded
  for round 62), *Beckmann rearrangement* (if seeded).
- **Glossary** → search *Pinacol rearrangement*,
  *Wagner-Meerwein rearrangement*, *Migratory aptitude*,
  *Beckmann rearrangement*.

Next: **Beckmann + Schmidt + Curtius deep**.
