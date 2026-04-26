# Equilibrium + Le Chatelier's principle

A reversible reaction reaches **equilibrium** when forward
and reverse rates are equal. The thermodynamics is fixed (ΔG
sets K), but the **position of equilibrium can be shifted by
external conditions** — this is what Le Chatelier's principle
tells you, qualitatively, before you do any maths.

## The equilibrium constant

For `aA + bB ⇌ cC + dD`:

```
K = [C]^c [D]^d / [A]^a [B]^b      (at equilibrium)
ΔG° = −RT ln K
```

- K > 1: products favoured at equilibrium (ΔG° < 0).
- K < 1: reactants favoured (ΔG° > 0).
- K = 1: 50/50 mix (ΔG° = 0).

The reaction quotient Q has the same form as K but uses
*current* concentrations; Q < K means the forward direction
runs; Q > K means the reverse runs.

## Le Chatelier's principle

> If you perturb a system at equilibrium, the system shifts
> in the direction that **opposes the perturbation**.

Five common perturbations:

### 1. Adding reactant or removing product

Q drops below K → forward shift → more product.

```
Fischer esterification:
RCOOH + R'OH ⇌ RCOOR' + H₂O
```

Use excess alcohol (or distill off water) to drive the
ester formation. Both work.

### 2. Removing reactant or adding product

Q rises above K → reverse shift.

### 3. Temperature change

For an exothermic reaction (ΔH < 0):

- Heating shifts equilibrium **backward** (reverse is
  endothermic, absorbs heat).
- Cooling shifts equilibrium **forward**.

For endothermic, the reverse: heating helps the forward
reaction.

The van't Hoff equation quantifies it: `d(ln K)/dT = ΔH° /
RT²`.

### 4. Pressure change (gas-phase only)

If product side has fewer moles of gas, increasing pressure
shifts forward. Example: Haber process

```
N₂(g) + 3 H₂(g) ⇌ 2 NH₃(g)     4 mol → 2 mol
```

High P drives ammonia formation. Industrially run at 150-
300 atm.

### 5. Adding inert gas at constant volume

No effect on K or position — partial pressures unchanged.

## Catalysts don't shift equilibrium

A catalyst lowers Ea for both forward + reverse equally —
reaches equilibrium faster but doesn't change where
equilibrium sits.

## Worked example — Haber process

```
N₂ + 3 H₂ ⇌ 2 NH₃        ΔH = −92 kJ/mol
```

At 25 °C, K is huge (~ 10¹⁵), but the reaction is
infinitesimally slow without a catalyst. Industrial
conditions:

- **High P** (150-300 atm) — favours product (4 mol → 2 mol).
- **Moderate T** (400-500 °C) — compromise: lower T helps
  position (exothermic) but kills rate.
- **Iron catalyst** — boosts rate without shifting
  equilibrium.

Equilibrium yield ~ 15 % per pass; unreacted N₂/H₂ are
recycled.

## Coupling equilibria

Two reactions at equilibrium can be coupled by a shared
intermediate:

```
A ⇌ B    K₁
B ⇌ C    K₂
A ⇌ C    K_overall = K₁ × K₂
```

This is how unfavourable steps get pulled along by favourable
ones — biology's whole metabolism is coupled equilibria, with
ATP hydrolysis (very favourable) coupled to thousands of
otherwise-unfavourable biosyntheses.

## Try it in the app

- **Tools → Lab calculator…** → *Equilibrium* tab → solve
  K from concentrations or ICE-table problems.
- **Reactions tab** → load *Fischer esterification* — see
  the Le Chatelier shifts driven by water removal.
- **Glossary** → search for *Le Chatelier*, *Equilibrium
  constant*, *Reaction quotient*, *Kinetic vs thermodynamic
  control*.

Next: **Hydrogen bonding — deeper**.
