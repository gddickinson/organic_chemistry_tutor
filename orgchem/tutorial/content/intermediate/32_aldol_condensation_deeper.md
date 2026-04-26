# Aldol condensation deeper — cross + intramolecular

The aldol covered in lesson 14 was the simplified version.
This lesson handles the practical complications: crossed
aldols, intramolecular cyclisations, and modern asymmetric
versions.

## The base reaction (recap)

```
2 RCHO + base → R-CH(OH)-CHR-CHO    (β-hydroxy aldehyde)
                ↓ Δ + H₂O
              R-CH=CR-CHO            (α,β-unsat aldehyde, "aldol cond.")
```

A simple aldol with one component gives a self-condensation:
acetaldehyde → 3-hydroxybutanal → crotonaldehyde.

## Cross aldol — the selectivity problem

If you mix two different carbonyls + base, you typically
get **four** products:

```
A-A, A-B, B-A, B-B
```

To get clean cross-aldol you need a controlled regime:

### 1. Use a non-enolisable acceptor

```
RCHO (acceptor, no α-H) + R'CH₂CHO (donor, has α-H)
→ R-CH(OH)-CHR'-CHO
```

Examples: benzaldehyde + acetone → benzalacetone (after
dehydration).

### 2. Pre-form the enolate kinetically

```
R'CH₂COR'' + LDA, -78 °C → R'C⁻=COLi (kinetic enolate)
                          + RCHO
                       → R'C(R-CHOH)-COR''
```

LDA at -78 °C in THF cleanly deprotonates the most-
accessible α-H without equilibrating to the more-stable
thermodynamic enolate.

### 3. Mukaiyama variant

```
silyl enol ether + RCHO + Lewis acid (TiCl₄, BF₃) →
                 → β-silyloxy ketone (then desilylate)
```

Silyl enol ether is non-basic, stable, isolable; Lewis
acid activates aldehyde; works at -78 °C → 0 °C.

### 4. Aldol via boron enolate (Evans)

Boron enolates form selectively with chiral diisocamphenyl
borate triflates (Evans 1981). Z-enolate gives syn-aldol
preferentially. Combined with an Oppolzer/Evans chiral
auxiliary → > 95 % de.

## Kinetic vs thermodynamic enolate

For an unsymmetric ketone (e.g. methyl phenyl ketone):

```
Ph-CO-CH₂CH₃    + LDA at -78 °C → Ph-C(O⁻)=CHCH₃    (kinetic, less subs.)
                + NaOR at reflux → Ph-CO-CH=CHCH₂Me  (thermo, more subs.)
```

LDA is bulky + kinetic + irreversible — kinetic enolate
trapped before equilibration.

NaOR is small + reversible — thermo enolate dominates.

## Intramolecular aldol (annulation)

For a diketone, base attack on one ketone enolate that
attacks the other carbonyl in the same molecule → 5- or
6-membered ring:

```
   O        O
   ||       ||
   C        C
  / \  + base
 R   R'  → enolate → attack other C=O →
   ↓ closure
   ring
```

Famous example: Robinson annulation:

```
methyl vinyl ketone (MVK) + cyclohexanone + base →
   conjugate addition → intermediate → intramolecular aldol →
   bicyclic product (steroid building block)
```

## Mannich reaction (related, with N)

```
amine + RCHO + R'COR'' → R'C(NR₂)CH-COR''-R
```

Iminium ion (from amine + aldehyde) is attacked by an
enolate. Stork's enamine + List's organocatalysis are
modern variants.

## Asymmetric versions

| Method | Gives | ee |
|--------|-------|-----|
| Evans aldol (chiral aux.) | syn-aldol | > 95 % de |
| Oppolzer (sultam) | syn-aldol | > 95 % de |
| Myers pseudoephedrine | both syn + anti | > 95 % de |
| Proline organocatalysis (List 2000) | aldol on non-enolisable acceptor | 50-90 % ee |
| MacMillan organocat | iminium catalysis | > 90 % ee |
| Mukaiyama / chiral Lewis acid (Carreira, Evans, Trost) | crossed aldol | > 95 % ee |

## Aldol step in biology

Almost every biochemical pathway has an aldol step:

- **Glycolysis** (aldolase enzyme: F1,6BP → DHAP + GAP).
- **Calvin cycle** (transketolase + aldolase).
- **Nucleotide biosynthesis** (ATCase + aldolase).
- **Lysine biosynthesis** (DAP synthase).

Class I aldolases (animals + plants) use Schiff-base
chemistry (Lys + carbonyl → imine → enamine → attack).
Class II aldolases (bacteria + fungi) use a Zn²⁺
coordinated to the substrate carbonyl.

## Try it in the app

- **Reactions tab** → load *Aldol condensation* (seeded) +
  *Claisen condensation* (seeded).
- **Mechanism player** → step through the aldol +
  condensation steps.
- **Glossary** → search *Aldol reaction*, *Aldol
  condensation*, *Mukaiyama aldol*, *Robinson annulation*,
  *Mannich reaction*.

Next: **Wittig + HWE + Julia + Peterson — olefination
toolbox**.
