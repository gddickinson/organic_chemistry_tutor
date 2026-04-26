# Activation energy + the Arrhenius equation

A reaction's rate depends not just on what's there, but on
what fraction of molecular collisions has enough energy to get
over the **activation barrier** — the energy peak between
reactants and products.

## The reaction-coordinate diagram

Plot energy on the y-axis vs reaction progress on the x-axis:

- **Reactant valley** — starting energy.
- **Transition state (TS)** — the highest point along the
  minimum-energy path. Its energy above the reactant valley
  is the **activation energy E_a** (or in modern notation,
  ΔG‡, the activation free energy).
- **Product valley** — final energy. The vertical drop from
  reactant to product is ΔG (overall thermodynamics).

For a **multi-step reaction**, you get multiple peaks. The
**rate-limiting (rate-determining) step** is the one with the
highest TS — it dominates the overall rate.

## The Arrhenius equation

```
k = A exp(−E_a / RT)
```

- **k** — rate constant.
- **A** — pre-exponential factor (frequency of collisions,
  steric factor; ~ 10¹³ s⁻¹ for unimolecular reactions in
  solution).
- **E_a** — activation energy (kJ/mol or kcal/mol).
- **R** — gas constant (8.314 J/mol·K).
- **T** — absolute temperature (K).

The exponential makes rate **enormously sensitive to T**:

- A reaction with E_a = 50 kJ/mol roughly **doubles** for
  every 10 K increase near room temperature.
- Reactions with E_a > 100 kJ/mol need substantial heating
  (reflux temperatures) to run on a reasonable lab timescale.

## Catalysts lower E_a

A catalyst provides an alternate reaction path with a lower
activation energy. ΔG (thermodynamics) doesn't change; only
the kinetic rate does.

The Eyring equation is the modern reformulation of Arrhenius:

```
k = (k_B T / h) exp(−ΔG‡ / RT)
```

Same physics, different parameterisation. Use Eyring when
talking about computational chemistry; use Arrhenius when
fitting experimental data.

## Worked example

A reaction with E_a = 80 kJ/mol at 298 K has:

```
k₁ = A · exp(−80000 / (8.314 × 298))
   = A · exp(−32.3)
   = A · 9.4 × 10⁻¹⁵
```

Heat to 348 K (75 °C):

```
k₂ = A · exp(−80000 / (8.314 × 348))
   = A · exp(−27.7)
   = A · 9.4 × 10⁻¹³
```

Ratio k₂/k₁ ≈ 100 — the reaction is **100 times faster** at 75
°C than at 25 °C. This is why reflux is so often the standard
operating temperature.

## Try it in the app

- **Tools → Lab calculator…** → *Thermo + kinetics* tab →
  *Arrhenius* solver (any 3 of 4 quantities k / A / E_a / T).
- **Reactions tab** → click any seeded reaction → *Energy
  profile…* dialog → see the ΔG‡ value used in the
  Bezier-smoothed reaction-coordinate diagram.
- **Glossary** → search for *Activation energy*, *Eyring
  equation*, *Rate-determining step*.

Next: **Catalysis intro — what catalysts do**.
