# Carboxylic acid derivatives + acyl substitution

The five carboxylic acid derivatives (acid chloride, anhydride,
ester, carboxylic acid, amide) all share the same reactivity
mechanism — **nucleophilic acyl substitution** — but at very
different rates. Understanding this hierarchy lets you plan
sequences of acyl interconversions cleanly.

## The reactivity hierarchy

```
acid chloride > anhydride > ester ≈ acid > amide
   most                              least
   reactive                          reactive
```

The order tracks two effects:

1. **Inductive electron withdrawal** by the leaving group — Cl
   is most EW, NR₂ least.
2. **Resonance donation** from the leaving group's lone pair
   into the C=O — NR₂ donates strongly (~ 40% double-bond
   character C–N), Cl donates weakly. Strong donation
   stabilises the substrate + slows reaction.

## The mechanism — addition then elimination

Nucleophilic acyl substitution always follows the same two-step
**tetrahedral intermediate** path (NOT direct displacement like
SN2):

```
   O                 O⁻                  O
   ‖                 |                   ‖
   C–LG  + Nu⁻ →   Nu–C–LG    →   Nu–C   + LG⁻
                     |
                  (tetrahedral
                  intermediate)
```

Step 1: nucleophile attacks the C=O carbon → tetrahedral
alkoxide intermediate.
Step 2: leaving group departs, regenerating the C=O.

The tetrahedral intermediate is the **rate-limiting** transition
state. More electrophilic carbonyl + better leaving group =
faster reaction.

## Down the hierarchy — easy

Going from a more-reactive to a less-reactive derivative is
straightforward:

- **Acid chloride + amine** → amide (room-temperature, fast).
- **Anhydride + alcohol** → ester + carboxylic acid byproduct.
- **Ester + amine** → amide (heating; slower).

## Up the hierarchy — needs activation

Going from less-reactive to more-reactive needs a
"coupling reagent" or forcing conditions:

- **Carboxylic acid → ester** (Fischer esterification) — needs
  H⁺ catalysis + alcohol in excess; the acid + Lewis-acid-
  activated carbonyl shifts equilibrium.
- **Carboxylic acid → amide** — needs a coupling reagent
  (DCC, EDC, HATU, T3P) that converts the COOH to a
  high-energy active ester first.
- **Ester → acid chloride** — usually go via the carboxylic
  acid first (saponify, then SOCl₂ or oxalyl chloride).

## Key named reactions

The **Reactions** tab seeds:

- **Fischer esterification** — acid + alcohol → ester
  (5-step mechanism).
- **Amide formation** (carboxylic acid + amine) — direct
  thermal coupling.
- **Claisen condensation** — ester enolate + ester → β-keto
  ester.
- **Mitsunobu reaction** — alcohol + carboxylic acid → ester
  with INVERSION (PPh₃ + DEAD).
- **Cannizzaro reaction** — disproportionation of an
  α-non-protic aldehyde.

## Try it in the app

- **Reactions tab** → load *Fischer esterification* +
  *Claisen condensation* — both are textbook acyl-substitution
  mechanisms with numbered curly arrows.
- **Glossary** → search for *Leaving group* + *Activating
  and deactivating groups* — these tie the inductive +
  resonance arguments to a quantitative framework.
- **Tools → Lab reagents…** — look up DCC, EDC, HATU, T3P
  for amide-coupling-reagent reference cards.

Next: **Enolates + α-functionalisation**.
