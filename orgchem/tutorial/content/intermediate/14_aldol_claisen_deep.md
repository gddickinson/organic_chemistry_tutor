# Aldol + Claisen condensations — going deeper

Lesson 13 introduced the enolate. This lesson digs into the two
most-used C–C bond-forming reactions in organic synthesis:
**aldol** + **Claisen** condensations. Mastering them = unlocking
about 30% of all retrosynthesis disconnections.

## The aldol reaction — three flavours

### Direct aldol (kinetic vs thermodynamic control)

A ketone or aldehyde α-deprotonates, then the enolate adds to
another carbonyl:

```
2 acetone → 4-hydroxy-4-methylpentan-2-one (a β-hydroxy ketone)
                 ↓ −H₂O
              "diacetone alcohol"
                 ↓
              mesityl oxide (the α,β-unsat. condensation product)
```

- **Kinetic control** (LDA, low T): the more-substituted
  enolate attacks the less-hindered face. Predictable
  stereo.
- **Thermodynamic control** (NaOH, room T): equilibrium gives
  the more-stable enolate + the more-substituted (Zaitsev-
  like) aldol product.

### Cross-aldol (Mukaiyama variant)

To stop two different carbonyls from cross-condensing
randomly, **pre-form** the silyl enol ether of one partner,
then add it to the other partner under Lewis-acid activation:

```
Me₃SiO–C=CH–R  +  R'CHO  →[BF₃ or TiCl₄]→ aldol product
```

The seeded **Mukaiyama aldol** entry in *Reactions* walks
this case explicitly. Used in nearly every modern asymmetric
aldol (Evans, Carreira, Mukaiyama-Kobayashi auxiliaries).

### Asymmetric aldol — Evans + others

**Evans aldol** uses a chiral oxazolidinone auxiliary on the
nucleophile to control absolute stereochemistry. Boron
triflate generates the boron-enolate; the chiral auxiliary
biases the chair-like Zimmerman-Traxler transition state to
one face. **syn**-product with > 95% de.

The seeded **Evans aldol** entry shows the standard substrate
+ outcome.

## The Claisen condensation

Two ester molecules condense — an ester enolate adds to
another ester, giving a β-keto ester after the alkoxide
leaves:

```
2 EtOAc + NaOEt → CH₃COCH₂COOEt (ethyl acetoacetate) + EtOH
```

Mechanism is acyl substitution on the second ester, with the
enolate of the first as the nucleophile.

The product is exceptionally acidic at the α-position (pKa
~ 11) — both flanking carbonyls stabilise the enolate. It's an
**active methylene compound**, ready for further functionalisation.

### Crossed Claisen: the Dieckmann

A diester intramolecularly cyclises to give a cyclic β-keto
ester. Used to build 5- and 6-membered rings.

## Decarboxylative tricks

β-keto esters + malonates **decarboxylate** on heating after
hydrolysis to give the free α-substituted ketone:

```
RCH₂CH(COOEt)₂ → (saponify) → RCH₂CH(COOH)₂
                → (heat) → RCH₂CH₃ (after −CO₂ × 2 + tautomerisation)
```

The **acetoacetic ester synthesis** + **malonic ester
synthesis** use this trick to install an alkyl group at the
α-carbon of a ketone or carboxylic acid.

## Stereochemistry — the Zimmerman-Traxler model

Aldol transition states adopt a **chair-like 6-membered ring**
(metal + enolate-O + carbonyl C + carbonyl O + α-C + α-C).
Substituents prefer equatorial positions in this chair, giving
the **syn** or **anti** aldol product depending on enolate
geometry:

- **Z-enolate** + chair TS → syn aldol.
- **E-enolate** + chair TS → anti aldol.

The aldol stereochemistry is therefore **controlled by enolate
geometry**, which is controlled by the choice of base + counter-
ion + temperature.

## Try it in the app

- **Reactions tab** → step through *Aldol condensation*,
  *Mukaiyama aldol*, *Evans aldol*, *Claisen condensation*,
  *Robinson annulation* — each rendered with enolate
  formation, transition-state geometry, + product stereo
  outcome.
- **Glossary** → search for *Active-methylene compound*,
  *Bürgi-Dunitz angle*, *Hyperconjugation*.

Next: **Organometallic reagents — Grignards, organolithiums,
cuprates**.
