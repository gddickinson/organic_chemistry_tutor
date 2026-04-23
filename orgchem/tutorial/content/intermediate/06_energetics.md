# Reaction Energetics: Profiles and Kinetics

Every reaction can be described on four increasingly abstract axes:

1. **Arrow pushing** — what moves (Chapter: mechanisms).
2. **3D geometry** — how atoms rearrange in space (3D trajectories).
3. **Energy landscape** — how thermodynamics and kinetics compete (this
   lesson).
4. **Orbital interaction** — what orbitals overlap and why (MO theory).

Here we focus on the **energy landscape** — what students traditionally
call the "reaction coordinate diagram."

## The canonical picture

Energy is on the y-axis, "reaction progress" is on the x-axis. The
curve goes from **reactants** up through one or more **transition
states** (TS‡), possibly through **intermediates**, and down (or up) to
the **products**.

Two quantities matter:

- **Activation energy (Ea)** — the height of the first uphill climb.
  Sets the **rate** (Arrhenius: k = A·exp(−Ea/RT)).
- **ΔH / ΔG** — the vertical distance from reactants to products. Sets
  the **equilibrium position**.

They are completely independent. A reaction can be strongly exothermic
(large negative ΔH) yet kinetically sluggish (large Ea) — think of
diamond spontaneously converting to graphite at room temperature.
Thermodynamically downhill, kinetically nowhere.

Open any of the seeded profiles in the **Reactions tab** — select SN1,
SN2, Diels-Alder, aldol, Grignard, E1, E2, Wittig, or Michael, then
click **"Energy profile…"**.

## One barrier vs. two barriers

The profile shape distinguishes concerted vs. stepwise mechanisms.

**One barrier** = **concerted**. SN2, E2, Diels-Alder.

    Reactants ───╱TS‡╲─── Products

The reaction passes through one transition state without ever resting.
This is why SN2 is stereospecific — there's no chance for the chiral
centre to racemise, because there's no intermediate to racemise
*through*.

**Two barriers + intermediate well** = **stepwise**. SN1, E1,
Grignard addition (has a workup protonation), Wittig (oxaphosphetane
intermediate), aldol (enolate intermediate), Michael.

    Reactants ─╱TS1‡╲── Intermediate ─╱TS2‡╲── Products

The intermediate sits in a shallow well. It's a real species — long
enough-lived to have a lifetime, a geometry, a spectrum — just not
stable enough to isolate at room temperature. The carbocation in SN1
is the textbook case.

## Rate-limiting step

When you have two TSs, only one can be the highest. Whatever barrier
leads *to* that highest TS sets the overall rate — the **rate-
determining** (or rate-limiting) **step**.

In the seeded SN1 profile for tert-butyl bromide, the first TS
(ionisation to the carbocation) is the RDS — once the cation is formed,
water captures it quickly. That's why SN1 rate depends only on the
substrate concentration (first order overall) — water doesn't appear in
the rate-limiting step.

## Hammond's postulate

Hammond: "The structure of a transition state resembles the species
nearest it in energy."

Practically:

- **Exothermic step** → TS is close in structure to the **reactants**
  ("early TS"). Small perturbations to the substrate show small changes
  in rate.
- **Endothermic step** → TS is close in structure to the **products /
  intermediate** ("late TS"). Small perturbations can show large
  changes in rate — the TS "feels" the product structure.

This is why carbocation stability controls SN1 rates so strongly —
the ionisation TS looks a lot like the carbocation itself, so anything
that stabilises the cation stabilises the TS. Tertiary substrates react
10⁴ faster than secondary.

## Kinetic vs. thermodynamic product

When two (or more) products can form from the same starting material,
their yields depend on:

- **Which has the lower Ea?** → kinetic product.
- **Which is more stable?** → thermodynamic product.

These are often the same compound but sometimes they aren't. The
canonical case: **Diels-Alder endo vs. exo**. The **endo** adduct
forms faster (lower Ea — secondary orbital interactions) but the
**exo** adduct is more stable (less steric strain). Run at low T →
endo dominates (kinetic). Heat or use reversible DA conditions → the
system equilibrates → exo dominates (thermodynamic).

## Reading a seeded profile

In the Reactions tab, select **"Diels-Alder: butadiene + ethene"** and
click **"Energy profile…"**. You'll see:

- **Three** stationary points (one barrier — concerted).
- Ea ≈ 115 kJ/mol — that's why you need heat.
- ΔH ≈ −165 kJ/mol — strongly exothermic, driven by the new C-C σ bond.
- Source tag at the bottom: "pedagogical estimate (Clayden 2e §35)" —
  so you know the numbers are for teaching, not kinetic prediction.

Compare to **SN1** (5 points, 2 barriers with a carbocation well) and
**Diels-Alder** (3 points, 1 barrier, deep exothermic well). The shapes
**are** the mechanism.

## What the numbers mean, and what they don't

These profiles are **pedagogical**. The Ea values come from canonical
textbooks and reproduce the qualitative shape — a student can read off
"this is a slow reaction (high Ea)" or "this intermediate is pretty
stable (deep well)" — but they are not kinetic predictions. A real
study needs DFT or experimental measurement.

For actual kinetic predictions, the app hooks plug into the `source`
field of `ReactionEnergyProfile` — if you paste DFT-computed numbers,
you mark them with `source="DFT/B3LYP/6-31G*"` instead of the default
"pedagogical estimate" so the distinction is preserved.

## Practice

1. In the Reactions tab, visit every reaction that has an **"Energy
   profile…"** button enabled. Compare shapes: one-barrier vs.
   two-barrier, exo- vs. endo-thermic.
2. Use the `get_energy_profile` agent action for SN1 and read out the
   stationary-point labels and energies.
3. Export the Aldol condensation profile (6 points — two barriers plus
   an enolate well and an alkoxide well). Identify the RDS.
4. Ask the tutor: "What's the Hammond postulate, and how does it apply
   to the second step of SN1?"

Next: **Spectroscopy** (Advanced tier) — once you know how the energy
landscape sets reactivity, you need tools to *characterise* the
products.
