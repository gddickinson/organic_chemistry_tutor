# Enzyme kinetics — Michaelis-Menten

Enzyme kinetics is the quantitative study of how fast an
enzyme converts substrate to product, and how that rate
depends on substrate concentration.  Two parameters —
**Vmax** and **Km** — capture the essential behaviour of
nearly every enzyme.

## The Michaelis-Menten model

The simplest enzyme model:

```
        k1       k2
E + S ⇌ ES → E + P
        k-1
```

- **E** = free enzyme.
- **S** = substrate.
- **ES** = enzyme-substrate complex.
- **P** = product.

Three rate constants:

- **k1** — substrate binding.
- **k-1** — substrate dissociation (unproductive).
- **k2** (also called **kcat**) — catalytic step;
  product formation + ES dissociation.

## The steady-state assumption

Briggs + Haldane (1925) introduced the **steady-state
approximation**: shortly after the reaction starts,
[ES] reaches a value at which formation = breakdown:

```
k1 [E][S] = k-1 [ES] + k2 [ES]
```

Solving for [ES] + substituting into the rate expression
(v = k2 [ES]) gives the Michaelis-Menten equation:

```
v = (Vmax · [S]) / (Km + [S])
```

where:

- **Vmax = kcat · [E]total** — the maximum rate when
  enzyme is fully saturated with substrate.
- **Km = (k-1 + k2) / k1** — the **Michaelis constant**;
  the substrate concentration at which v = Vmax / 2.

When k2 << k-1 (slow catalysis, fast equilibration), Km
approximates the dissociation constant Kd of the ES
complex.  Otherwise Km is a kinetic parameter, not a
binding constant.

## Interpreting Vmax and Km

**Vmax** is the rate ceiling.  It scales linearly with
total enzyme concentration; doubling [E] doubles Vmax.

**kcat** ("turnover number") is Vmax / [E]total — the
maximum number of substrate molecules processed per
enzyme per unit time.  Typical values:

- Carbonic anhydrase II: kcat ~ 10⁶ s⁻¹ (one of the fastest).
- Catalase: kcat ~ 10⁷ s⁻¹.
- Acetylcholinesterase: kcat ~ 1.4 × 10⁴ s⁻¹.
- Slower enzymes: kcat ~ 1-10⁰ s⁻¹.

**Km** is a measure of "substrate affinity for the
catalytic process".  Low Km = enzyme works at half-max
even at low [S]; high Km = enzyme needs lots of
substrate to be busy.

Typical Km values are µM-mM, comparable to physiological
substrate concentrations.

## kcat / Km — the catalytic efficiency

The single most useful enzyme-kinetic parameter:

```
kcat / Km = (k1 · k2) / (k-1 + k2)
```

When k2 >> k-1, this collapses to k1 — the rate of
substrate binding.  The diffusion-controlled upper limit
is ~ 10⁸-10⁹ M⁻¹s⁻¹ — the **kinetic perfection limit**.

Enzymes operating near this limit:

- Triose phosphate isomerase (TIM) — ~ 10⁸ M⁻¹s⁻¹.
- Acetylcholinesterase — ~ 10⁸ M⁻¹s⁻¹.
- Catalase — ~ 4 × 10⁸ M⁻¹s⁻¹.

These are "kinetically perfect" — every collision between
enzyme + substrate leads to catalysis.  Evolution can't
make them faster.

## Lineweaver-Burk + Eadie-Hofstee plots

Before computers, kineticists linearised Michaelis-Menten
to extract Vmax + Km from data.

**Lineweaver-Burk** (double-reciprocal):

```
1/v = (Km / Vmax) · (1/[S]) + 1/Vmax
```

Plot 1/v vs 1/[S] → straight line; slope = Km/Vmax,
y-intercept = 1/Vmax, x-intercept = -1/Km.

**Eadie-Hofstee**:

```
v = Vmax - Km · (v / [S])
```

Plot v vs v/[S] → slope = -Km, y-intercept = Vmax.

Modern practice: nonlinear least-squares fit to the
Michaelis-Menten equation directly.  Linearised plots
are still useful for visualising deviations from MM
behaviour (allostery, inhibition, multi-substrate).

## Multi-substrate kinetics

Most real enzymes have ≥ 2 substrates.  The kinetic
mechanism distinguishes:

- **Sequential (ordered or random)** — both substrates
  bind before any product is released.  All hexokinase-
  family enzymes use this.
- **Ping-pong** — first substrate binds, modifies the
  enzyme + leaves; second substrate then binds the
  modified enzyme.  Aminotransferases (PLP-dependent)
  + many flavoenzymes use ping-pong.

The diagnostic: secondary plots of slope + intercept
from primary Lineweaver-Burk give different patterns
for sequential vs ping-pong.

## Allosteric departures

Some enzymes don't follow Michaelis-Menten — they show
**sigmoidal** v-vs-[S] curves instead of hyperbolic.
These are usually multi-subunit allosteric enzymes
(hemoglobin O₂ binding, ATCase, PFK-1).

The Hill equation:

```
v = (Vmax · [S]^n) / (K^n + [S]^n)
```

with **n** the Hill coefficient (n > 1 = positive
cooperativity; n < 1 = negative; n = 1 = MM).
Hemoglobin's O₂ binding has n ≈ 2.8-3.

## Why kinetics matters for drug design

Drug-target binding kinetics is increasingly understood
as more important than equilibrium affinity:

- **Residence time** (1/koff) determines duration of
  drug action *in vivo*.
- **Slow off-rate** drugs are often more selective + more
  effective than equipotent fast off-rate drugs.
- **Mechanism-based inhibitors** (covalent or
  irreversible) act by enzyme-driven activation +
  trapping in the active site.

## Try it in the app

- **Window → Biochem Studio → Enzymes** — every entry
  carries the EC number + mechanism class needed to
  predict kinetic behaviour.
- **Tools → Lab calculator** for substrate-concentration
  + rate-constant calculations.

Next: **Enzyme inhibition**.
