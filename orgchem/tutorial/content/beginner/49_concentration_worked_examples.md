# Concentration calculations — worked examples

The mass+moles lesson covered the formulas. This lesson works
through real-world concentration problems from the bench.

## Problem 1 — Diluting a stock

You have 100 mL of 0.5 M HCl. How do you make 50 mL of 0.05 M HCl?

```
M₁V₁ = M₂V₂
0.5 × V₁ = 0.05 × 50
V₁ = 5 mL of stock
```

Take 5 mL stock + add water to 50 mL final.

## Problem 2 — Buffer recipe

Make 100 mL of 50 mM phosphate buffer pH 7.0.

```
H₂PO₄⁻ ⇌ HPO₄²⁻         pKa₂ = 7.2
pH = pKa + log([A⁻]/[HA])
7.0 = 7.2 + log(R)
R = 0.63 → [HPO₄²⁻]/[H₂PO₄⁻] = 0.63

Total = 50 mM = [HA] + [A⁻]
[HA] (acid) = 50 / 1.63 = 30.7 mM
[A⁻] (base) = 19.3 mM

In 100 mL: 3.07 mmol NaH₂PO₄ + 1.93 mmol Na₂HPO₄
        = 0.41 g NaH₂PO₄·H₂O + 0.27 g Na₂HPO₄
```

## Problem 3 — Theoretical yield

Esterify 5.0 g of acetic acid (MW 60.05) with excess EtOH.

```
n(AcOH) = 5.0 / 60.05 = 0.0833 mol  (limiting)
1:1 stoichiometry → 0.0833 mol ester
m(EtOAc) = 0.0833 × 88.11 = 7.34 g (theoretical)
```

Isolated 5.5 g → % yield = 5.5 / 7.34 × 100 = **74.9 %**.

## Problem 4 — ppm conversion

Drinking water has [Pb²⁺] = 15 ppb. What's that in mol/L?

```
15 ppb = 15 µg / kg ≈ 15 µg / L (water density ≈ 1)
       = 15 × 10⁻⁶ g / L / 207 g·mol⁻¹
       = 7.2 × 10⁻⁸ M = 72 nM
```

EPA action level is 15 ppb — calibrated to be detectable
+ harmful at chronic exposure.

## Problem 5 — Equivalents in a reaction

Run a Suzuki coupling: 100 mg of aryl bromide (MW 235), 1.5
eq boronic acid (MW 162), 5 mol % Pd(PPh₃)₄ (MW 1156),
2.0 eq K₂CO₃ (MW 138).

```
n(ArBr) = 0.1 / 235 = 0.426 mmol  (limiting reagent)
n(B(OH)₂) = 0.426 × 1.5 = 0.638 mmol → m = 0.103 g
n(Pd) = 0.426 × 0.05 = 0.021 mmol → m = 24 mg
n(K₂CO₃) = 0.426 × 2.0 = 0.852 mmol → m = 0.118 g
```

That's a typical 100 mg-scale screening reaction.

## Try it in the app

- **Tools → Lab calculator…** → *Solution* + *Stoichiometry*
  + *Acid-base* tabs solve all of the above.
- **Glossary** → search *Molarity*, *Buffer*, *ppm*,
  *Equivalents*, *Yield*.

Next: **Aqueous chemistry intro**.
