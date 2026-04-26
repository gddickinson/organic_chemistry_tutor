# Reaction kinetics intro — rate laws + the rate equation

Thermodynamics tells you whether a reaction CAN run; kinetics
tells you HOW FAST. Two reactions with similar ΔG can have
rates differing by a factor of 10⁹ — kinetics is the
practical lab-bench question.

## The rate of a reaction

For a reaction `A + B → P`, the **rate** is the change in any
concentration per unit time:

```
rate = −d[A]/dt = −d[B]/dt = +d[P]/dt
```

(Negative for consumed; positive for formed.) Units:
mol·L⁻¹·s⁻¹.

## The rate law

Experiments measure the **rate law** — an empirical equation
relating rate to concentrations:

```
rate = k [A]^m [B]^n
```

- **k** is the rate constant (temperature-dependent; units
  depend on the overall order).
- **m + n** is the **overall order**. For the example above,
  if m = 1 and n = 1, the reaction is "second order overall,
  first order in each component".
- The exponents are NOT in general the stoichiometric
  coefficients — they're determined by the rate-limiting
  step's mechanism.

## SN1 vs SN2 — kinetics distinguishes them

The classical mechanistic discrimination:

- **SN2** mechanism: rate = k [substrate][nucleophile]
  (second-order overall, first in each).
- **SN1** mechanism: rate = k [substrate] (first-order
  overall; nucleophile concentration doesn't matter because
  rate-limiting step is unimolecular ionisation to a
  carbocation).

Hughes + Ingold won this argument in the 1930s by simply
varying nucleophile concentration + watching the rate. SN2
rates double when [Nu] doubles; SN1 rates don't.

## Half-life

For a first-order reaction:

```
t½ = ln 2 / k = 0.693 / k
```

Independent of starting concentration. A reaction with k = 1
s⁻¹ halves every 0.69 seconds; with k = 10⁻⁴ s⁻¹ (slow), every
~ 2 hours.

## Pseudo-first-order

If one reactant is in large excess, its concentration barely
changes during the reaction. The rate law collapses to
pseudo-first-order:

```
rate = k [A][B]   if [B] >> [A]
     ≈ k_obs [A]   where k_obs = k [B]
```

This is the standard simplification for kinetic analysis —
swamp the variable you don't want to vary.

## Try it in the app

- **Tools → Lab calculator…** → *Thermo + kinetics* tab →
  solve first-order half-life, integrated rate-law
  problems, Arrhenius + Eyring rate constants.
- **Reactions tab** → load *SN1* + *SN2* reactions; the
  *Energy profile…* dialog renders the activation barriers
  for both mechanism classes.
- **Glossary** → search for *Rate-determining step*, *Half-
  life*, *Activation energy*.

Next: **Activation energy + the Arrhenius equation**.
