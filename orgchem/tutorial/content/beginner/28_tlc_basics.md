# TLC for beginners

**Thin-layer chromatography (TLC)** is the fastest, cheapest,
most-used analytical technique in any organic-chemistry lab.
A drop of crude reaction mixture, a small silica plate, a
solvent system, and 5 minutes give you an instant answer: did
my reaction work? did all the starting material get consumed?
how many products are there?

## What TLC is

A TLC plate is a thin layer of **silica gel** (or alumina)
coated onto a flat backing of glass or aluminium foil. You
**spot** your sample near the bottom, **develop** the plate by
standing it in a shallow pool of solvent (the *eluent*), and
the solvent **rises by capillary action** carrying compounds
upward at different rates. After 2-5 minutes, you pull the
plate, **mark** the solvent front, **dry** it, **visualise**
under UV / stain, and read the spots.

## The Rf value

For each spot, measure:

```
Rf = (distance from origin to spot)
   / (distance from origin to solvent front)
```

Rf is dimensionless, between 0 (didn't move) and 1 (ran with
the solvent front). Two compounds with the same Rf in the
same eluent are likely the same molecule (but not certainly;
TLC alone never proves identity, only consistency).

## How TLC discriminates

Silica is **polar** — it retains polar compounds via H-bonding
+ dipole-dipole interactions. The eluent is usually an
**EtOAc / hexane mix** of tunable polarity:

- **More EtOAc → more polar eluent → higher Rf** for everything.
- **More hexane → less polar eluent → lower Rf** for everything.

Aim for your most-important spot at Rf 0.3-0.5 — not too low
(can't see clearly), not too high (can't separate from
neighbours).

## Visualisation

Most organic compounds are colourless, so you need a
visualisation method:

- **UV (254 nm)** — fluorescent silica + UV-absorbing
  compounds shows as dark spots on a green background. Works
  for most aromatics + carbonyls. Standard first check.
- **Iodine vapour** — most organic compounds show as brown
  spots. General + reversible.
- **Charring stains** — sulfuric acid spray + heat. Universal
  but destructive.
- **KMnO₄ stain** — yellow stain on a pink background;
  oxidisable groups (alkenes, alcohols, aldehydes) show as
  yellow spots.
- **Ninhydrin** — purple stain for amines + amino acids.
- **Anisaldehyde** — colourful stain for aldehydes / ketones /
  alcohols / carbohydrates.

## Reading a reaction TLC

Spot the reaction mixture in three lanes:

1. **Lane A** — pure starting material.
2. **Lane B** — reaction mixture (or "co-spot" of A+B in a
   single lane near A).
3. **Lane C** — pure product (if available).

After developing:
- If **lane B has spots only at A's Rf** → no reaction
  happened.
- If **lane B has new spots not in A** → product is forming.
- If **A's spot is gone from B** → starting material consumed.
- If **B has multiple new spots** → multiple products
  (impurity / over-reaction / decomposition).

## Optimising the eluent

Start with **20 % EtOAc / 80 % hexane** as a default. Adjust:

- All spots at Rf 0 → too non-polar. Increase EtOAc.
- All spots at Rf 1 → too polar. Decrease EtOAc.
- Spots overlap → swap to a different solvent system (DCM /
  MeOH for very polar, toluene / EtOAc for aromatics).

## Try it in the app

- **Tools → Lab techniques → TLC / Rf simulator** — input
  several SMILES + an eluent; the simulator predicts where
  each compound runs based on its logP + solvent polarity.
  Save the predicted plate as PNG.
- **Tools → Chromatography techniques…** — full reference
  card for TLC, paper chromatography, gravity column, flash,
  HPLC, etc.
- **Glossary** → search for *Rf value* + *polar adsorbent* for
  the formal definitions.

Congratulations — you've reached the end of the beginner tier!
The intermediate tier picks up with **Stereochemistry (R/S, E/Z,
chirality)** + the substitution / elimination / aromatic /
carbonyl / energetics ladder.
