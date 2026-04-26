# Mass + moles + stoichiometry — the lab arithmetic

Every wet-chemistry experiment begins with arithmetic: how
much of each reagent? How big a flask? What yield should I
expect? This lesson covers the basics — the calculations
you'll do hundreds of times before they become reflexive.

## The mole

A mole is **6.022 × 10²³ entities** (Avogadro's number).
For a substance:

```
moles = mass / molar mass
n     = m / M

Aspirin: M = 180.16 g/mol
1.00 g aspirin = 1.00 / 180.16 = 5.55 mmol
```

For a solution:

```
moles = molarity × volume
n     = c × V

10 mL of 1.0 M HCl = 0.010 × 1.0 = 10 mmol
```

## Limiting reagent

In a balanced reaction `aA + bB → cC + dD`, the **limiting
reagent** is the one consumed first based on stoichiometry.
The product yield is set by the limiting reagent.

```
2 aspirin + ?? → ??

Mix 5 mmol salicylic acid + 8 mmol acetic anhydride:
→ ratio 5:8 = 0.625
→ stoichiometric ratio (1:1 in synthesis) = 1.0
→ salicylic acid is limiting → max yield = 5 mmol aspirin
→ acetic anhydride excess: 8 − 5 = 3 mmol left over
```

Always identify the limiting reagent BEFORE calculating
yield.

## Theoretical, actual, percent yield

```
theoretical yield = limiting reagent moles × stoichiometric ratio × MW(product)
actual yield      = mass of pure product isolated
% yield           = (actual / theoretical) × 100 %
```

Example: theoretical aspirin = 5 mmol × 180 = 900 mg.
Isolated 720 mg → 80 % yield.

Reasonable yields by reaction type:

| Reaction type | Typical % yield |
|---------------|-----------------|
| Simple acid-base / salt | 90-100 |
| SN2 with a good nucleophile | 70-90 |
| Diels-Alder | 60-95 |
| Wittig | 50-85 |
| Multistep with chromatography | 30-60 (per step) |
| Total synthesis (15+ steps) | 0.1-5 (overall) |

## Stoichiometric ratios — equivalents (eq)

In the lab we usually express reagent ratios as
**equivalents** relative to the limiting reagent:

```
substrate (1.0 eq) + base (1.5 eq) + catalyst (0.05 eq) + electrophile (1.2 eq)
```

A typical Wittig prep: ylide 1.2 eq, aldehyde 1.0 eq → use
20 % excess ylide to drive the aldehyde to completion.

## Concentration units

| Unit | Definition | Use |
|------|------------|-----|
| **Molarity (M)** | mol / L solution | Most common; varies with T |
| **Molality (m)** | mol / kg solvent | T-independent |
| **% w/w** | g solute / 100 g soln | Concentrated reagents (HCl 37 %) |
| **% w/v** | g solute / 100 mL soln | Some buffers (1 % BSA) |
| **% v/v** | mL solute / 100 mL soln | Mixed solvents (50 % EtOH/H₂O) |
| **ppm** | mg / kg or mg / L | Trace contaminants, drinking water |
| **ppb** | µg / kg or µg / L | Trace impurities |

### Conversion examples

Concentrated HCl is 37 % w/w, density 1.18 g/mL, MW 36.46:

```
12 M HCl: in 1 L of solution there are 12 mol HCl × 36.46 = 437 g HCl
        in 1 L of solution at ρ 1.18: 1180 g total
        → 437 / 1180 = 37 % w/w  ✓
```

## Worked example — making a buffer

Recipe: 100 mL of 50 mM Tris-HCl, pH 7.4.

Tris MW = 121.14 g/mol. Need:

```
n(Tris) = 0.050 mol/L × 0.100 L = 0.0050 mol = 0.606 g
```

Dissolve 0.606 g Tris in ~ 80 mL water, adjust pH to 7.4
with HCl, then top up to 100 mL.

Why "top up after pH adjustment"? Because adding HCl adds
volume + dilutes the buffer. Final volume must be measured
AFTER pH-adjustment is complete.

## Density + molarity from labels

Concentrated reagents come labelled by density + % w/w.
Quick conversion:

```
M = (10 × % × ρ) / MW

Concentrated H₂SO₄: 98 % w/w, ρ 1.84 g/mL, MW 98.08
→ M = (10 × 98 × 1.84) / 98.08 = 18.4 M
```

## Try it in the app

- **Tools → Lab calculator…** → *Solution* tab → solve
  molarity, dilution, ppm, % w/w problems.
- **Tools → Lab calculator…** → *Stoichiometry* tab →
  limiting-reagent + theoretical / percent yield solver.
- **Glossary** → search *Mole*, *Limiting reagent*, *Yield*,
  *Equivalents*, *Molarity*.

Next: **Common reagent abbreviations + what they mean**.
