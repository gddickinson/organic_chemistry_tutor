# Enthalpy, entropy, and free energy in organic reactions

Three thermodynamic state functions decide whether a reaction
can run + how thermodynamically favourable it is. Knowing how
to estimate each lets you predict equilibrium positions
without doing any kinetics.

## The Gibbs equation

```
ΔG = ΔH − T ΔS
```

- **ΔG** (Gibbs free energy) — the thermodynamic driving
  force. Negative = spontaneous (products favoured).
- **ΔH** (enthalpy) — heat absorbed or released. Negative =
  exothermic.
- **T** (temperature, K) — multiplies the entropy term.
- **ΔS** (entropy) — change in molecular disorder. Positive =
  more disorder in products.

ΔG ties to the equilibrium constant by `ΔG = −RT ln K`. A 
reaction with ΔG = −10 kJ/mol at room temperature has K ≈ 60
(strongly product-favoured); ΔG = +10 kJ/mol has K ≈ 0.018
(reactant-favoured).

## Estimating ΔH

Use bond dissociation energies (lesson 30):

```
ΔH ≈ Σ BDE(broken) − Σ BDE(formed)
```

Most exothermic organic reactions form C=O, C–C, or O–H bonds.
Combustion is the most exothermic (ΔH ~ −200 kcal/mol per CH₂).

## Estimating ΔS

Sign rules:

- **Increase in moles of gas** → ΔS > 0.
- **One molecule splits into two** → ΔS > 0.
- **Two molecules combine into one** → ΔS < 0 (a Diels-Alder
  cycloaddition, an aldol condensation).
- **Going from solid to liquid to gas** → ΔS > 0.
- **Conformational restriction** (chelation, ring closure) →
  ΔS < 0.

Magnitudes are harder to estimate from inspection alone — for
simple reactions, ΔS is often small (< 50 J/mol·K) so the
TΔS term is < 15 kJ/mol at room temperature.

## When entropy wins

For high-temperature reactions, the TΔS term dominates. The
reaction:

```
2 NH₃ → N₂ + 3 H₂        ΔH = +92 kJ/mol  (endothermic)
                          ΔS = +199 J/mol·K (favourable)
```

is impossible at room temperature (ΔG = +33 kJ/mol) but
spontaneous above ~ 460 K.

The **Eyring equation** for kinetic rates:

```
k = (k_B T / h) × exp(−ΔG‡ / RT)
```

links ΔG‡ (activation free energy) to the rate constant.
Doubling the rate at room temp = lowering ΔG‡ by ~ 1.7 kJ/mol.

## Try it in the app

- **Reactions tab** → click any seeded reaction → click *Energy
  profile…* to see the calculated ΔG, ΔH, and Eₐ for the
  step.
- **Tools → Lab calculator…** (Ctrl+Shift+C) → *Thermo +
  kinetics* tab → solve heat-capacity equations, Eyring rate
  constants, Arrhenius parameters.
- **Glossary** → search for *Endothermic*, *Activation
  energy*, *Eyring equation*, *Kinetic vs thermodynamic
  control* (the most stable product isn't always the one that
  forms fastest), *Transition state*.

Next: **Reaction kinetics intro — rate laws + the rate
equation**.
