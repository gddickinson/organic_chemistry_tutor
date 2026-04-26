# Pericyclic reactions intro — concerted, Woodward-Hoffmann allowed

A **pericyclic reaction** has a cyclic transition state with
no intermediates: bonds break + form simultaneously around a
ring. Three big families:

- **Cycloadditions** — two π systems → one σ + one π.
- **Electrocyclic** — open-chain π → cyclic σ (or reverse).
- **Sigmatropic** — σ bond migrates across a π system.

The 1981 Nobel Prize (Fukui + Hoffmann) recognised the
quantum-mechanical foundations + the Woodward-Hoffmann
rules.

## What "concerted" means

In a stepwise reaction (e.g. SN1, E1) you can in principle
isolate the intermediate. In a concerted reaction the bonds
all change in one elementary step — you can't intercept any
intermediate, only the transition state.

Diagnostics:

- **Stereospecific** — geometry of starting material
  uniquely determines geometry of product.
- **No solvent / catalyst dependence** typically.
- **Negative ΔS‡** — TS more ordered than reactants.
- **Often heat- or photo-driven**.

## Cycloadditions

Notation: `[a + b]` = sum of π electrons from each
component. The famous one: **[4 + 2] = Diels-Alder**.

### Diels-Alder reaction (heat, [4+2])

```
diene + dienophile → cyclohexene
4 π e⁻ + 2 π e⁻ = 6 π e⁻
```

- s-cis diene preferred (s-trans can't reach the
  dienophile).
- **endo rule** (Alder-Stein) — the substituent on the
  dienophile prefers the *endo* face of the developing ring
  due to secondary orbital overlap.
- **Stereospecific** — cis dienophile → cis product;
  retention of double-bond geometry.
- Inverse electron demand: electron-poor diene + electron-
  rich dienophile (tetrazine + TCO bioorthogonal example).

Allowed **thermally** because 4 + 2 = 4n + 2 (n = 1).

### [2+2] cycloaddition (light, [2+2])

```
2 alkenes + hν → cyclobutane
2 π e⁻ + 2 π e⁻ = 4 π e⁻
```

Forbidden thermally (4n electrons) but allowed
photochemically — the excited state has different orbital
symmetry.

### 1,3-Dipolar cycloaddition (heat, [4+2] over 3 atoms + 2 atoms)

```
azide + alkyne → triazole         (Huisgen)
nitrile oxide + alkene → isoxazoline
ozone + alkene → ozonide
diazomethane + alkene → pyrazoline
```

Sharpless's CuAAC click chemistry is a Cu-accelerated
1,3-dipolar (regioselective for 1,4-triazole; uncatalysed
gives ~ 1:1 1,4 / 1,5 mixtures).

## Electrocyclic reactions

A linear conjugated π system closes to a ring (or vice
versa):

```
butadiene  ⇌  cyclobutene        (4 π e⁻)
hexatriene ⇌  1,3-cyclohexadiene (6 π e⁻)
octatetraene ⇌ 1,3,5-cyclooctatriene (8 π e⁻)
```

The terminal carbons rotate during ring closure. Under
**thermal** conditions:

- **(4n)** π e⁻ system (4, 8, ...) → **conrotatory**
  closure (both ends rotate same direction).
- **(4n + 2)** π e⁻ system (2, 6, ...) → **disrotatory**
  closure (opposite directions).

Photochemical reverses the selectivity.

Stereochemical consequence: the product's substituents end
up cis or trans depending on rotation mode → predict by
W-H rules.

## Sigmatropic rearrangements

Notation: `[i, j]` = a σ bond migrates from one end to a
new position i atoms one direction and j atoms the other.

### [3,3]-sigmatropic

The two big ones:

- **Cope rearrangement** — 1,5-hexadiene ⇌ 1,5-hexadiene
  (migrates an all-carbon σ bond).
- **Claisen rearrangement** — allyl vinyl ether → γ,δ-
  unsaturated carbonyl. Powerful C-O → C-C transformation.

```
CH₂=CH-CH₂-O-CH=CH₂  →  CH₂=CH-CH₂-CH₂-CHO
                          (γ,δ-unsaturated)
```

Variants: **Aromatic Claisen** (allyl phenyl ether → ortho-
allyl phenol), **Ireland-Claisen** (silyl ketene acetal),
**Johnson-Claisen** (orthoester).

Allowed thermally (6 π e⁻ in chair TS, 4n + 2).

### [2,3]-sigmatropic

- **Wittig rearrangement** of allyl ethers (carbanion
  variant).
- **Meisenheimer** of allyl ammonium oxides.
- **Mislow-Evans** of allyl sulfoxides.

### [1,5]-sigmatropic H shifts

```
CH₃-CH=CH-CH=CH-D  ⇌  CH₂=CH-CH=CH-CHD-H
                       (D migrates from C1 to C5)
```

Allowed thermally for [1,5] H shifts. Cyclopentadiene
scrambles its H's via this.

## The Woodward-Hoffmann rules in one line

For a thermal pericyclic reaction with **q** electrons in
the cyclic TS:

- Allowed if **q = 4n + 2** with **suprafacial** components
  on both sides.
- Allowed if **q = 4n** with **antarafacial** on one side,
  suprafacial on the other.

Photo-flip the suprafacial/antarafacial requirement.

In practice, you remember:

- [4+2] is thermally allowed (Diels-Alder).
- [2+2] needs photons (or strain; ene, ene-yne).
- 6-electron electrocyclic = disrotatory (heat) or
  conrotatory (light).
- [3,3]-sigmatropic = thermally allowed (Cope, Claisen).

## Try it in the app

- **Reactions tab** → load *Diels-Alder*, *Claisen
  rearrangement* (if seeded), *Aldol*, *Wittig*.
- **Tools → Orbitals (Hückel/W-H)…** → *W-H* tab → pick a
  pericyclic family + electron count → see the rule.
- **Glossary** → search *Pericyclic*, *Diels-Alder
  reaction*, *Cope rearrangement*, *Claisen rearrangement*,
  *Conrotatory*, *Disrotatory*.

Next: **Reduction methods — comparing the toolbox**.
