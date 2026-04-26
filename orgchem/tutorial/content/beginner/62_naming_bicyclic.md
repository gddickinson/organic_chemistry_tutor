# Naming bicyclic compounds

A **bicyclic** compound has two rings sharing atoms. The
IUPAC convention names them by counting carbons + bridging
atoms.

## Three classes by ring fusion

- **Spiro** — two rings share ONE atom (the spiro centre).
- **Fused** — two rings share TWO adjacent atoms (one
  bond).
- **Bridged** — two rings share TWO non-adjacent atoms
  (two bridgehead atoms with a connecting bridge).

## Naming spiro compounds

Format: `spiro[a.b]xxxxane`, with a + b = number of carbons
in each ring excluding the spiro centre, in size order.

```
spiro[4.5]decane   (cyclopentane fused at a single C with cyclohexane,
                    total 10 C: 4 + 5 + 1 spiro)
```

## Naming fused bicyclic

Format: `bicyclo[a.b.c]xxxxxane`, a ≥ b ≥ c, where a/b/c
are the number of carbons between the two **bridgeheads**.

For fused bicyclic, c = 0 (no bridge between the
bridgeheads, just a direct bond).

```
bicyclo[4.4.0]decane   = decalin (cis or trans)
                        (4 + 4 + 0 = 8 + 2 bridgeheads = 10 C)
bicyclo[3.4.0]nonane   = hydrindane
bicyclo[2.2.0]hexane   = bicyclohexane (rare)
```

## Naming bridged bicyclic

Same `bicyclo[a.b.c]xxxxane` format but c > 0 means a
non-zero bridge between bridgeheads.

```
bicyclo[2.2.1]heptane  = norbornane (3 bridges: 2C, 2C, 1C between bridgeheads)
                                                   total = 2+2+1+2 = 7 C
bicyclo[1.1.0]butane   = bicyclobutane (highly strained)
bicyclo[2.2.2]octane   = like norbornane with a longer bridge
```

## Numbering

Start at one bridgehead, go around the longest bridge first
(highest a), then the second-longest, finally the shortest:

```
norbornane C1 = top bridgehead
1 → 2 → 3 → 4 (other bridgehead) → 5 → 6 → 7 (1-C bridge)
```

Substituents get lowest locants by this canonical numbering.

## Famous bicyclic systems

| Compound | Bicyclic name |
|----------|---------------|
| Norbornane | bicyclo[2.2.1]heptane |
| Norbornene | bicyclo[2.2.1]hept-2-ene |
| α-Pinene | (1S,5S)-2,6,6-trimethylbicyclo[3.1.1]hept-2-ene |
| Camphor | (1R,4R)-1,7,7-trimethylbicyclo[2.2.1]heptan-2-one |
| Decalin | bicyclo[4.4.0]decane |
| Adamantane | tricyclo[3.3.1.1³,⁷]decane |
| Cubane | pentacyclo[4.2.0.0²,⁵.0³,⁸.0⁴,⁷]octane |

## Common name vs IUPAC

For famous structures, common names are still preferred in
practice:

- camphor (not "1,7,7-trimethyl-bicyclo[2.2.1]heptan-2-one").
- adamantane.
- norbornane / norbornene.
- pinene (α + β).

But IUPAC names are unambiguous + needed for new structures.

## Stereochemistry in bicyclics

- **endo** — substituent on the side of the larger
  bridge.
- **exo** — substituent on the side of the smaller bridge.

For Diels-Alder products: endo-rule (Alder-Stein)
predicts kinetic preference for endo isomer.

## Try it in the app

- **Tools → IUPAC naming rules…** → look up bicyclic
  naming rules.
- **2D viewer** → load camphor, norbornene, decalin —
  see how the bicyclic skeleton is drawn.
- **Glossary** → search *Bicyclic*, *Bridgehead*,
  *Spiro centre*, *Norbornane*, *Endo*, *Exo*.

Next: **Naming heterocycles**.
