# Flow & Process Chemistry

Every reaction in this app so far has been implicitly **batch**:
fill a flask with reagents, heat, stir, quench, work up.  It's
how you learn organic chemistry and how most research labs run
today.  It's also how most industrial fine-chemical plants
*used* to run — and it's the regime the Carothers-Sheldon
E-factor numbers were calibrated against.

**Flow chemistry** is the alternative where reagents stream
through tubes and solid-phase cartridges and come out as product
on the other side.  A batch flask becomes a **pipe**.  The
consequences for heat management, safety, mixing, scale-up, and
atom economy are wide enough that most major pharmaceutical
plants built since ~2010 have at least one flow stage.

This lesson is the capstone of the tutorial tier — it pulls
together:

- The Carothers + Anastas + process-scale intuition from
  intermediate/09 Polymers and advanced/05 Green chemistry.
- The enzyme + chemoenzymatic framing from graduate/05
  Catalysis and graduate/06 Biosynthesis.
- The classical batch mechanisms from throughout the
  Reactions tab.

## Two canonical reactor types

**Continuous stirred-tank reactor (CSTR)** — a flask that
never empties.  Reagents enter at the same rate product
leaves.  The contents are one well-mixed composition
(steady-state).  Mathematically:

    τ = V / Q           (mean residence time = volume / flow)

Every volume element stays τ on average; the actual
distribution is exponential (wide spread).

**Plug-flow reactor (PFR)** — a long tube.  Each small volume
element traverses end-to-end without back-mixing.  Residence
time is a **sharp distribution** — every reagent molecule
sees the same t.  Mathematically:

    dC_A / dx = −k · C_A^n / v     (1D steady-state)

Most flow chemistry in fine chemicals is PFR-style (tube-in-
tube, packed-bed, micro-reactor).  CSTR is common for
polymerisation and continuous fermentation.

The practical lesson: **batch** = CSTR-with-τ-approaches-
infinity.  **Flow** = PFR with τ = reactor volume / pump rate.

## Why flow ever wins

### 1. Heat transfer and exotherms

Surface-to-volume ratio scales as **1 / r** for a cylindrical
vessel.  A 10-mL flask has ~5 cm⁻¹ of surface per volume; a
100-L reactor has ~0.05 cm⁻¹.  A mildly exothermic reaction
that's safe in a flask can run away in the plant vessel
(Runaway.  Look up "thermal runaway, Bhopal" as the extreme
example.)

A 1 mm-diameter flow tube has ~40 cm⁻¹ — almost three orders
of magnitude more surface than the flask.  Heat leaves so
efficiently that you can run a *strongly* exothermic reaction
under mild external cooling, no fear of runaway.

Concrete: **nitration** (Reactions tab → Nitration of benzene).
Batch nitration of arenes with fuming HNO₃/H₂SO₄ is a
textbook disaster-risk exothermic cascade.  Flow nitration is
routine at ton-scale — the heat leaves through the tube wall
fast enough to keep ΔT inside the reactor < 10 °C.

### 2. Mixing

In a batch flask, mixing time scales as ~10 s for a typical
stir bar at a typical viscosity.  If your reaction has a
half-life < 10 s, you don't have control — you get
stoichiometric hot spots.

Flow: **microreactor mixing** via T-junction + 100 µm
channel + turbulent flow hits the mixing limit in ~100 µs.
That's 5 orders of magnitude faster than a batch flask.
Reactions that are too fast for batch (Grignard additions
at elevated T, organolithiums, fluorination with F₂) run
fine in flow.

### 3. Reactive-intermediate handling

Any unstable intermediate that has to be generated, used,
and quenched *on the way through the tube* — never stored,
never accumulated.  Examples:

- **Organolithium** generation and use within 5 s before
  it degrades at −30 °C.
- **Diazomethane** (toxic, explosive) made in situ, consumed
  in the next reactor, and never leaving the plant.
- **Ozone** (toxic, explosive) generated from O₂ in-line,
  used for ozonolysis, then catalytically quenched.
- **H₂ under pressure** — flow hydrogenation cartridges
  (H-Cube, ThalesNano) generate H₂ electrolytically at
  plant scale so you never have a high-pressure H₂ vessel
  larger than a coin.

### 4. Process intensification

Temperature and pressure ranges *that can't be reached in
batch*:

- 300-400 °C / 100-300 bar in a 2-mm titanium tube: **super-
  heated water** becomes a near-aprotic solvent that runs
  hydrolyses without acid catalysts.
- 100-300 °C in a microreactor: **Paal-Knorr** pyrrole
  synthesis takes 5 min instead of 12 h.
- Packed-bed heterogeneous catalyst + 10 bar H₂:
  **continuous asymmetric hydrogenation** — the Knowles
  Rh-DIPAMP chemistry (L-DOPA pathway step 2, seeded)
  runs in flow at higher TON than batch.

## The canonical modern process: sitagliptin

Merck's sitagliptin (Januvia) route (2010, Codexis
collaboration) is the industry standard example of a
**modern chemoenzymatic flow process**:

    chloro-diketone + benzyl amine + transaminase enzyme
    + pyridoxal phosphate + iPrNH₂ (amine donor)
        → (R)-sitagliptin + acetone + H₂O

- The engineered transaminase sets the amine stereocentre
  at > 99.5 % ee — no chiral auxiliary, no protection.
- Runs at 45 °C, atmospheric pressure, aqueous DMSO.
- E-factor halved vs the prior rhodium-asymmetric-H₂ batch
  route (Merck's internal comparison).
- Nobel-ish chemistry prize: 2018 Frances Arnold (directed
  evolution, same toolbox as this transaminase) + George
  Smith + Greg Winter.

The pre-2010 route was **batch** + **stoichiometric chiral
auxiliary** + **rhodium**.  Swapping in a flow-compatible
transaminase replaced a rare-metal stoichiometric step with
a catalytic biological one.  Classic Anastas principles
2 / 8 / 9 wins.

## Scale-up vs numbering-up

A traditional plant scales from 10 mL (med-chem flask) →
1 L (hood) → 10 L (kilo lab) → 100 L (pilot) → 2500 L
(plant).  Each step is a 10× volume jump, so the
surface / volume drops 10⁻¹/³ ≈ 0.46× each time.  Heat
and mixing get progressively harder; every step needs
reoptimization.

Flow plants usually **number up** instead.  You don't make
a 10 cm tube 10× wider; you run 10 identical 1 cm tubes in
parallel.  The kinetics, heat transfer, and mixing are
identical to the lab-scale unit at every stage of scale-
up.  Move from lab → kilo → production by buying more
reactors, not by re-engineering the reactor.

Downside: capital cost.  A batch plant's 2500 L vessel is
one asset; a flow plant's 100 × 25-L tubes is 100 assets
+ pumps + control valves.  Process-chemistry economics
still favour batch when the target is stable + safe and
the downside of going flow isn't huge.

## Real-time analytics (PAT)

Flow has a huge side-effect: the **steady-state stream** is
perfect for inline analysis.

- Inline FT-IR / Raman probe in the product stream — first
  derivative of concentration gives you the rate, in
  seconds, not hours.
- Online HPLC samples every 30 s and triggers an auto-
  reject loop if conversion drifts.
- Thermo-camera over the tube wall spots temperature
  fingerprints that diagnose chemistry issues before
  the product gets quenched.

FDA's **PAT** (Process Analytical Technology, 2004) framework
was essentially a standards push around this — and it's
the regulatory backdrop for why flow is so attractive for
pharma.  A fully-instrumented flow line *is* its own quality-
control system.

## Flow weaknesses — when batch still wins

- **Slow reactions** (τ > 1 h).  A 10 L/h reaction with a
  3 h residence time means a 30 L tube — expensive compared
  to a stirred flask.
- **Solid-phase reactions or slurries** that would clog a
  tube.  Heterogeneous catalysis in packed-bed columns
  works; dispersed insoluble reagents don't.
- **Very long reagent-addition campaigns** (drip 500 mL
  over 4 h, monitor colour).  Batch is still the right
  tool for low-volume, high-supervision operations.
- **R&D / exploratory chemistry** where you change
  conditions every few hours.  Flow rewards a fixed
  protocol; batch rewards flexibility.

## A decision checklist

Before switching a step to flow, run this checklist:

1. **Heat.**  Does a 10× scale-up create a thermal-runaway
   risk?  If yes, flow wins.
2. **Time.**  Is τ < 30 min?  Flow is efficient.  τ > 2 h:
   batch.
3. **Reactive intermediate.**  Any ozone / organolithium /
   diazo / H₂-at-pressure step?  Flow wins on safety.
4. **Mixing kinetics.**  Half-life of the desired step <
   10 s?  Flow wins on mixing control.
5. **Scale vision.**  Will this scale from kilo → 100 kg
   → ton?  Flow wins via numbering-up.
6. **Solids.**  Any suspended particulates, gels, slurries?
   Batch unless engineered around.
7. **Regulatory pathway.**  FDA / EMA PAT requirement?
   Flow lands pre-instrumented.

Most modern med-chem routes hit 2-3 of these on at least one
step, which is why >50 % of plant-new chemistry since 2015
has a flow stage.

## Exercises

1. Pick **one seeded Synthesis pathway** and identify the
   step most likely to benefit from flow.  Justify against
   the checklist.
2. The seeded **Nitration of benzene** reaction is a
   textbook flow candidate.  Name three specific flow
   advantages citing the checklist.
3. The **Knowles asymmetric H₂** step (L-DOPA pathway
   step 2) runs batch under 3 atm H₂.  What checklist
   criterion argues flow, and what argues batch?  Who
   wins?
4. Re-read the **nylon-6 / caprolactam** Beckmann step
   (oleum catalyst).  Propose a flow variant using
   zeolite ZSM-5 (mentioned in the green-chem lesson
   round 87).  What's the key flow design parameter?
5. Why is **PAT** more compatible with flow than with
   batch?  Give two concrete reasons grounded in
   signal / rate sampling.

## See also

- Advanced / 05 Green chemistry (Anastas principle 6,
  process metrics, Sheldon E-factor framing).
- Graduate / 05 Catalysis — homogeneous vs heterogeneous
  kinetics context.
- Graduate / 06 Biosynthesis — thermolysin flow and
  continuous fermentation crossover.
- Intermediate / 09 Polymer chemistry — step-growth vs
  chain-growth in continuous reactors.
- Reactions tab: Nitration of benzene (flow-friendly).
- Synthesis tab: Nylon-6, Nylon-6,6, Aspartame, L-DOPA
  — each with a flow-equivalent retrospective.
- Glossary: {term:Atom economy}, {term:E-factor},
  {term:Activation energy}.
