# Process safety in pharma

A reaction that works at 100 mg in a fume hood may be
catastrophic at 100 kg in a plant. **Process safety** is
the discipline of keeping people + facilities safe at
manufacturing scale.

## Why scale changes the rules

- **Heat transfer** — surface-area-to-volume falls as the
  third power of size. A 1 g flask cools in seconds; a
  100 kg reactor takes minutes.
- **Mass transfer** — mixing slower at scale; bigger
  concentration gradients.
- **Pressure build-up** — 1 mol of gas at 1 atm fills 24 L.
  In a sealed reactor, that's ~ 2 bar/mol/L of solvent.
- **Residence time** — substrates may sit hours at scale-
  up vs minutes in lab.

A reaction with mild exotherm at small scale can be a
runaway at scale.

## Hazards to assess

### Reactivity

- **Heat of reaction (ΔH)** — measure by reaction
  calorimetry (RC1, EasyMax).
- **Adiabatic temperature rise** — what's the worst case
  if cooling fails?
- **Self-accelerating decomposition temperature (SADT)**
  — runaway-onset temperature.
- **Onset temperature** — when does decomposition start?

### Acute toxicity

- LD50 / LC50 in animal models.
- OEL (occupational exposure limit) for workers.
- ALOHA model for emergency dispersion.

### Flammability

- Flash point (lowest T to ignite vapour).
- Auto-ignition temperature.
- LEL / UEL (lower / upper explosion limits in air).
- Class I (flammable liquids: bp < 38 °C, FP < 38 °C)
  needs explosion-proof equipment.

### Pressure

- Maximum pressure rise during reaction.
- Maximum pressure during decomposition.
- Reactor relief valve sized for both.

### Static electricity

- Conductive solvents (THF, MeCN, DCM): low risk.
- Insulating solvents (hexane, toluene, ether): high risk
  with metal vessels → ground everything; nitrogen
  blanket.

## Calorimetry methods

### DSC (Differential Scanning Calorimetry)

Heats a small sample (mg) at controlled rate; measures
ΔH(T). Quick screen for heat of decomposition + onset
temperature.

### Reaction calorimetry (RC1, EasyMax)

Measures heat output of a reaction at lab scale (10-
500 mL); gives ΔH_rxn + heat output rate over time.

### ARC (accelerating rate calorimetry)

Mimics adiabatic conditions; gives self-heat rate vs T;
identifies SADT.

### TSu (Thermal Screening Unit)

Quick decomposition screen; safer + cheaper than DSC for
some samples.

## Common process-safety pitfalls

### "Isothermal" reactions become exothermic at scale

A reaction labelled "isothermal" in lab may have a 5 °C
exotherm at 1 g — but a 50 °C exotherm at 100 kg if
heat transfer fails.

Mitigation: dose feed; use jacketed reactor with rapid
cooling; emergency cooling plan.

### Acid-water mixing rule

ALWAYS add acid to water (not water to acid). The other
way generates concentrated layer with massive exotherm.

### Lithiations + air-sensitive

n-BuLi + acetone → fast violent. Keep ketones away from
RLi unless intended.

### Scale-up of azides + diazo

A reaction that's safe at 1 mmol of NaN₃ in DMF
(0.1 mol / L) is dangerous at 1 mol scale (concentrate +
heat → detonation). Modern flow chemistry mitigates this
by never accumulating a large pool.

### Pyrophorics on transfer

n-BuLi + air → fire. Use cannula transfer; flush with
inert gas; never expose pump tubing.

### Pressure relief sizing

Standard rule: relief valve must vent the worst-case
exothermic gas + vapour generation rate. Sized using
DIERS methodology (Design Institute for Emergency Relief
Systems).

## Hazard analysis methods

### HAZOP (Hazard + Operability)

Brainstorm "what if" deviations: more flow, less flow,
high T, low T, etc., for each unit operation. Identify
hazards + safeguards.

### What-If

Less structured than HAZOP; quick-and-dirty.

### LOPA (Layer of Protection Analysis)

Quantitative — assigns probability of failure to each
safeguard layer, sums to risk per year.

### Bowtie

Visual representation of cause-consequence chains for
high-severity events.

## Documents required

For an FDA-regulated drug API:

- **Process Safety Information (PSI)** — chemical hazards,
  process limits, PFD/P&ID diagrams.
- **Reactivity profile** — full calorimetry data.
- **PHA (process hazard analysis)** — HAZOP / What-If
  documented.
- **Operating procedure** — written step-by-step.
- **Emergency response plan** — what to do if cooling
  fails, etc.

## ICH Q7 (FDA / EMA / PMDA)

Manufacturing standards for APIs:

- Equipment qualification (IQ/OQ/PQ).
- Cleaning validation between batches.
- Process validation (PPQ batches).
- Continuous monitoring (CGMP).
- Change control.

## Try it in the app

- **Tools → Lab analysers…** → look up DSC + RC1 + ARC for
  calorimetry instruments (if seeded).
- **Tools → Lab reagents…** → check hazards on each
  reagent + storage notes.
- **Glossary** → search *Process safety*, *DSC
  (differential scanning calorimetry)*, *ARC*, *HAZOP*,
  *Runaway reaction*, *Activation energy*, *pKa*.

Next: **Cost of goods + green metrics for process**.
