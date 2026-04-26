# The Hammond postulate — TS resembles its nearest endpoint

The transition state (TS) of an elementary step has a fleeting
geometry you can't isolate or directly observe. Yet you need
to reason about its structure to predict reactivity. **Hammond's
postulate** (George S. Hammond, 1955) gives the rule of thumb.

## The statement

> The transition state of an elementary step structurally
> resembles whichever of its endpoints (reactant or product)
> is closer to it in **energy**.

In a reaction-coordinate diagram:

```
Endothermic step (ΔH > 0):    TS resembles PRODUCT (late TS)
Exothermic step (ΔH < 0):     TS resembles REACTANT (early TS)
Thermoneutral (ΔH ≈ 0):       TS is in between
```

## Why it works

For an elementary step, the TS is at the highest point along
the minimum-energy path. If the product is much higher in
energy than the reactant, the TS sits high on the way up the
hill — geometrically closer to the product. The atoms have
mostly already done the bond-making / bond-breaking by the
TS.

## Worked example 1 — SN2 reactions

SN2 is one elementary step:

```
Nu⁻ + R-X → [Nu···R···X]‡ → Nu-R + X⁻
```

For most SN2 reactions, the leaving group has a comparable
nucleophilicity to the entering group → step is roughly
thermoneutral → TS is symmetrical (~ 50 % bond formed +
50 % bond broken).

For an SN2 with a much weaker leaving group (e.g. OH⁻
displacing iodide is unfavourable, the reverse very
favourable) → endothermic in this direction → TS is late
→ Nu-C bond is mostly formed, C-X bond is mostly broken.

## Worked example 2 — Carbocation formation

Step: ionisation R-X → R⁺ + X⁻ is endothermic (positive ΔG;
heat of ionisation positive).

By Hammond, the TS resembles the carbocation product. So
factors that stabilise the carbocation (3° > 2° > 1°,
adjacent oxygen lone pair, allylic, benzylic, …) stabilise
the TS by almost the same amount → faster ionisation.

This is why SN1 + E1 rates correlate with carbocation
stability — the rate-determining step's TS *is* the
carbocation, near enough.

## Worked example 3 — Bromination vs chlorination of methane

Free-radical halogenation step:

```
X• + CH₄ → X-H + CH₃•      ΔH(Cl) = +1 kcal/mol
                            ΔH(Br) = +18 kcal/mol
```

Chlorination is nearly thermoneutral → early TS → little
preference between primary, secondary, tertiary C-H bonds
→ poor selectivity.

Bromination is endothermic → late TS → TS resembles the
alkyl radical → reactivity correlates with radical
stability → strong selectivity for tertiary C-H.

This is why N-bromosuccinimide (NBS) gives clean allylic /
benzylic bromination while Cl₂ + CH₄ gives messy mixtures.

## Worked example 4 — Markovnikov vs anti-Markovnikov

HBr addition to propene proceeds through a carbocation
intermediate. The endothermic step is the protonation:

```
CH₃-CH=CH₂ + HBr → CH₃-CH⁺-CH₃ + Br⁻       (or CH₃-CH₂-CH₂⁺ + Br⁻)
```

The 2° carbocation is much more stable than the 1° → late
TS → preferentially form the 2° → Br⁻ adds → 2-bromopropane
(Markovnikov).

With peroxides, the radical chain mechanism puts the
primary C-Br bond as the rate-controlling step, reversing
the selectivity (anti-Markovnikov).

## Reactivity-selectivity principle

Hammond predicts a general trend: **less reactive species
are more selective**. Because they have higher barriers
→ later TS → bigger discrimination between substrate sites.

Examples:

- Br• > Cl• in selectivity (because Br is less reactive).
- t-Bu cation > Me cation in selectivity (more stable, higher
  barrier to form, more product-like TS).
- LDA (bulky, less basic kinetically) > KOH (smaller, more
  reactive) for selective enolate formation.

## When Hammond fails

- **Multi-step reactions** — Hammond applies to one
  elementary step at a time.
- **Highly asymmetric reaction surfaces** — the energy-vs-
  position picture isn't 1D.
- **Late or weird TS geometries** — Marcus theory + DFT
  computations give a more nuanced picture.

## Try it in the app

- **Reactions tab** → load *SN1*, *SN2*, *E1*, *E2* — see
  the energy profile + Ea values; compare to predict TS
  position.
- **Tools → Lab calculator…** → *Thermo + kinetics* tab →
  *Eyring* solver to compute ΔG‡ from k.
- **Glossary** → search *Hammond postulate*, *Transition
  state*, *Reactivity-selectivity principle*, *Markovnikov*.

Next: **Mass + moles + stoichiometry — the lab arithmetic**.
