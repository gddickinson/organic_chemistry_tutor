# Curly arrows — the mechanism alphabet

Every organic reaction can be written as a sequence of **electron
movements**. Curly arrows are the universal notation chemists
use to track those movements. Once you can read them, you can
read any mechanism.

## Two arrow types

- **Double-headed arrow (↶)** — moves a **pair of electrons**
  (a bond or a lone pair). This is the workhorse of polar
  organic chemistry: SN1, SN2, E1, E2, addition, condensation,
  elimination, every named reaction.
- **Single-headed (fishhook) arrow (⇁)** — moves a **single
  electron**. Used for **radical** mechanisms only:
  halogenation of alkanes, polymerisation, photoredox catalysis
  (see Phase-198).

## Arrow conventions

1. **Tail at the source of electrons**, **head at the destination**:
   - From a lone pair on a nucleophile to an electrophilic atom.
   - From a π bond to an empty atom orbital (electrophilic
     addition).
   - From a σ bond to an antibonding orbital (SN2).
2. **The arrow shows where electrons GO, not where atoms move**.
   A common student mistake is drawing arrows like atoms moving;
   atoms follow the electrons.
3. **One arrow per electron pair**. A typical step has 2-4
   arrows.

## Reading an SN2 step

```
HO⁻      ↶ a       ↶ b       Br⁻
   ↘            ↘
    C─Br       C─OH
   /             /
  (substrate)   (product)
```

Two arrows:
- **Arrow a**: lone pair on hydroxide → carbon (forms the new
  C-O bond).
- **Arrow b**: C-Br σ bond → bromide (breaks the old C-Br bond
  + dumps both electrons on Br to make Br⁻).

Electron-rich (HO⁻) attacks electron-poor (δ⁺ C of C–Br); the
leaving group walks away with the bond.

## Reading a Diels-Alder step

```
diene + dienophile  ↶↶↶  cyclohexene
```

Three arrows in concert (a *concerted* mechanism — all bonds
form + break at once):
- π bond of dienophile → new σ bond at one end
- π bond of diene end → other new σ bond
- shifted π bond stays in the new ring

The Diels-Alder is the canonical pericyclic reaction; see the
seeded *Diels-Alder* entry in the **Reactions** tab for the
full mechanism rendering.

## Common patterns

- **Nucleophile attacks electrophile** — arrow from lone pair
  / π bond / σ bond to empty / partially-empty orbital.
- **Bond breaks heterolytically** — arrow from bond to the
  more-electronegative atom.
- **Proton transfer** — arrow from base lone pair to H, second
  arrow from breaking H-X bond to X.
- **E2 elimination** — three concerted arrows: base → H, σ-CH
  → π, σ-CX → X.

## Try it in the app

- **Reactions tab** → click any seeded reaction with a
  *mechanism* (SN1, SN2, E1, E2, Diels-Alder, aldol, Wittig,
  bromination of ethene, …) → press **Play mechanism**. The
  step-by-step viewer renders each electron-movement arrow as
  a numbered curved arrow over the structure.
- **Glossary tab** → search for *Walden inversion* (SN2-
  specific arrow geometry) + *Bürgi-Dunitz angle* (preferred
  arrow trajectory for nucleophilic addition to a carbonyl).

Next: **Nucleophiles vs electrophiles** — recognising the two
roles every arrow connects.
