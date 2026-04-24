# Radical Reactions

So far the seeded mechanisms have been **polar**: curly arrows move
electron **pairs** from a nucleophile to an electrophile. Radical
chemistry is the "third family" that sits outside the polar /
pericyclic axes — electrons move one at a time, leaving unpaired
spins behind.

The notation switches too: full curly arrows become **fishhook arrows
(single-barbed)**, each tracking a single electron.

Open **{term:Homolysis vs heterolysis}** in the Glossary (*View →
Glossary*, or Ctrl+K → "homolysis") for the short definition.

## Three hallmarks of radical chemistry

1. **Fishhook arrows.** Each electron moves separately. A bond
   breaking homolytically gives two arrows — one to each fragment.
2. **Chain mechanism.** Once started, a single initiator event
   propagates through many turnovers before termination. This is
   what makes radical reactions *catalytic in the initiator*.
3. **Non-ionic, non-polar.** No build-up of charge in the transition
   state; radical reactions often work fine in non-polar solvents
   (hexane, CCl₄) where ionic mechanisms stall.

## The chain: initiation / propagation / termination

Every radical chain has three stages. Using Cl₂ + CH₄ → CH₃Cl + HCl
as the canonical worked example (Reactions tab →
*Radical halogenation of methane*):

**Initiation** — create the first radical.

    Cl-Cl → 2 Cl•              (hν or ~200 °C)

Homolytic cleavage of the weakest bond in the pot. Two fishhook
arrows split the Cl-Cl σ pair evenly.

**Propagation** — consume one radical, produce another. Two steps
that together consume a substrate molecule and release a product:

    Cl• + H-CH₃ → H-Cl + •CH₃    (H-atom abstraction)
    •CH₃ + Cl-Cl → Cl-CH₃ + Cl•  (Cl abstraction)

Each step is an atom transfer — the radical "moves" along the
pathway while staying a radical. The net of the two propagation
steps is the overall stoichiometry:

    Cl-Cl + H-CH₃ → H-Cl + Cl-CH₃

**Termination** — two radicals combine, ending the chain.

    2 Cl•    → Cl-Cl
    Cl• + •CH₃ → CH₃-Cl
    2 •CH₃   → CH₃-CH₃ (trace ethane — classic chain-diagnostic)

Termination products are typically traces (< 1 %) but they are
the fingerprint of a radical mechanism in a GC trace.

## Radical stability: the analogue of carbocation stability

Like carbocations, radicals are stabilised by hyperconjugation and
by resonance. The **3° > 2° > 1° > methyl** order runs in the same
direction for both species, and for the same reason — the radical
π* (or empty p) orbital accepts donation from adjacent σ(C-H)
bonds.

    Radical stability:  3° > 2° > 1° > methyl ≈ 10 kJ/mol per step

Allylic (CH₂=CH-CH₂•) and benzylic (Ph-CH₂•) radicals are even
more stable because the unpaired electron delocalises into the π
system.

## Selectivity — chlorine vs bromine

Chlorine radicals are **reactive but unselective**: Cl• has
−ΔH ≈ −7 kJ/mol for 1° C-H abstraction and −ΔH ≈ −14 kJ/mol for
3° C-H. Ratio of rates ~ 1 : 4 : 5. Result: chlorination of
isobutane gives a messy 2 : 1 mixture of primary vs tertiary
chloride.

Bromine radicals are **sluggish but selective**: Br-H is a weaker
bond, so Br• barely grabs a 1° H but happily grabs a 3° (more-
stable radical → more exothermic → lower Ea via the Hammond
postulate). Ratio ~ 1 : 80 : 1700. Bromination of isobutane gives
> 99 % tertiary.

The **Hammond postulate** (Glossary) explains this: a weakly
exothermic step has a late, product-like transition state where
radical stability matters a lot. A strongly exothermic step has
an early TS where radical stability barely matters.

## Applications you'll meet later

- **Radical polymerisation** — the huge industrial route to
  polyethylene, polystyrene, polyvinyl chloride. Initiator
  (AIBN, di-tert-butyl peroxide) → alkene chain adds one monomer
  at a time → terminate by coupling or disproportionation.
- **Autoxidation** — the rancidity of oils and fats is O₂
  slowly inserting into C-H bonds via a peroxy-radical chain.
  **Antioxidants** (vitamin E, BHT) work by donating an H to the
  chain-carrying peroxyl radical, replacing it with an unreactive
  stabilised radical.
- **Atmospheric chemistry** — ozone-depletion catalytic cycles
  (Cl• from CFCs + ozone) are radical chains in the stratosphere.
- **Biological radicals** — tyrosyl radical in ribonucleotide
  reductase, NO• signalling, oxidative stress.

## Arrow practice — try them in your head

1. The initiation step Cl-Cl → 2 Cl•. Two fishhook arrows where?
2. The first propagation step Cl• + H-CH₃ → HCl + •CH₃. Draw three
   fishhooks: one from each of the C-H σ pair, plus one from Cl•
   to the H it's grabbing.
3. Disproportionation: 2 CH₃CH₂• → CH₂=CH₂ + CH₃-CH₃. What four
   fishhook arrows generate both products in one concerted step?

Answers live in any introductory textbook — or ask the tutor
with *"show me disproportionation as an arrow-pushing diagram"*.

## See also

- Glossary: *Homolysis vs heterolysis*, *Hammond postulate*,
  *Curved arrow*, *Carbocation* (contrast — both 3° > 1° for
  the same hyperconjugation reason).
- Reactions tab: *Radical halogenation of methane* (seeded with
  full chain-step notes).
- Advanced → *Pericyclic reactions* (the "no-charge" third family
  that sits alongside radicals outside the polar axis).
