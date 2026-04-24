# Green Chemistry — Case Studies From the Seeded Catalogue

Paul Anastas and John Warner published *Green Chemistry:
Theory and Practice* in 1998 with **12 Principles** that, put
together, turn "make the product" into "make the product
cheaply, safely, and without trashing the planet."  This
lesson uses the 12 principles as an **audit checklist** and
maps each one onto already-seeded pathways and reactions —
so you can see where the seeded chemistry passes the test,
where it flunks, and where a redesign was actually deployed
at plant scale.

The 12 principles (Anastas & Warner 1998):

1. **Prevent waste** (rather than treat it after the fact).
2. **Atom economy** — incorporate every starting-material
   atom into the product.
3. **Less hazardous syntheses** — design reagents to be less
   toxic.
4. **Safer products** — design molecules to do their job then
   degrade.
5. **Safer solvents + auxiliaries**.
6. **Energy efficiency** — room temperature / pressure beats
   hot / high-pressure.
7. **Renewable feedstocks** — biomass > petroleum.
8. **Reduce derivatisation** — protecting groups, blocking
   groups, temporary modifications add waste.
9. **Catalysis > stoichiometry**.
10. **Design for degradation** — don't leave persistent
    pollutants.
11. **Real-time monitoring** — catch problems before the
    waste stream leaves the plant.
12. **Inherently safer chemistry** — choose routes whose
    accidents are tolerable.

## Metrics

Two quantitative metrics sit underneath everything.  Both
live in the **Tools → Green metrics…** dialog you've already
met.

**Atom economy** — the mass fraction of starting-material
atoms that ends up in the product.

    AE = MW(desired product) / Σ MW(stoichiometric inputs)  × 100 %

**E-factor** (Sheldon, 1992) — kg of waste per kg of product.
Industrial benchmarks: bulk chemicals E ≈ 1-5; fine chemicals
5-50; pharmaceuticals 25-100+.

Open Tools → Green metrics… and pick **Aspirin** to see the
per-step and overall AE for the seeded Kolbe-Schmitt route
(87 %, which is excellent — most of the waste in industrial
aspirin is not mass, it's energy + aqueous workup volume).

## Case 1 — Adipic acid, the N₂O problem (Principles 1, 3, 10)

Synthesis tab → *Adipic acid — DuPont cyclohexane route*.

Step 2 of the route uses 50 % HNO₃ to cleave KA oil to the
diacid — and releases **~1 mole of N₂O per mole of adipic
acid**.  N₂O has ~265× the global-warming potential of CO₂
per mass.  Global adipic acid production is ~2.8 Mt/y; before
plant-scale N₂O abatement (thermal-catalytic decomposition
over Al₂O₃ or CuO catalysts) this reaction alone was responsible
for ~5-8 % of all anthropogenic N₂O emissions.

**Green-chemistry response**:

- **Catalytic N₂O abatement** (most plants post-1997) —
  passes principle 11 (monitor + react) but still fails
  principle 1 (prevent waste at source).
- **Biotech alternative**: Draths & Frost (Michigan State,
  1994) demonstrated a route from D-glucose through *cis,cis*-
  muconic acid + hydrogenation to adipic acid, using an
  engineered *E. coli* shikimate-pathway strain.  Passes
  principles 2, 3, 7 (renewable feedstock), 9 (biocatalysis),
  10 (degradable byproducts).  Scale-up still hampered by
  titer + separation costs.

## Case 2 — Nylon-6 and the ammonium sulfate mountain (Principles 1, 5, 9)

Synthesis tab → *Nylon-6 — Beckmann / caprolactam route*, step 2.

The classical Beckmann rearrangement of cyclohexanone oxime
uses oleum or conc. H₂SO₄.  After the product caprolactam is
neutralised with aq. NH₃, the byproduct is **~5 kg of (NH₄)₂SO₄
per kg of caprolactam**.  Turns out to be valuable as fertiliser
— but the market for fertiliser-grade (NH₄)₂SO₄ is saturated by
the primary-amine industry, and many caprolactam plants have to
pay to dispose of it.

**Green-chemistry response**:

- **Vapour-phase Beckmann over zeolite ZSM-5** (Sumitomo,
  Fukui commercialised 2003).  Solid acid catalyst replaces
  oleum entirely; no aqueous work-up; no sulfate waste.
  Passes principles 5 (solvent), 9 (catalysis), 1 (waste
  prevention).  Now used for ~20 % of global caprolactam.
- Still no route that dodges *all* of the waste: the oxime
  step still consumes hydroxylamine (itself made from NH₃
  + NO via the Raschig process, with its own sulfate issue).

## Case 3 — L-DOPA and the Knowles Nobel (Principles 2, 5, 8, 9)

Synthesis tab → *L-DOPA — Knowles Rh-DIPAMP asymmetric route*.

The route is in many ways a green-chemistry showpiece:

- **Principle 2 (atom economy).**  The asymmetric
  hydrogenation step adds only H₂ — 2 g / mol product. AE
  for step 2 is ~99 %.
- **Principle 8 (reduce derivatisation).**  The alternative
  was **resolution** — make the racemate, react it with a
  chiral auxiliary to form diastereomers, separate them by
  crystallisation, then recover the pure (*S*) by
  hydrolysing the auxiliary.  That classic textbook route
  discards up to 50 % of the material as the wrong
  enantiomer.  Knowles's asymmetric-catalysis route simply
  makes the right one.
- **Principle 9 (catalysis).**  Rh-DIPAMP turnover number is
  well over 10 000 at industrial conditions.
- **Weaknesses**: the HBr/AcOH deprotection step (3) loses
  two CH₃Br equivalents per product molecule.  Not a
  big deal for the small (~100 kg/yr) L-DOPA market, but
  would scale badly for a commodity target.

## Case 4 — Aspartame and the thermolysin shortcut (Principles 8, 9)

Synthesis tab → *Aspartame — Z-protected peptide coupling*.

The classical DCC / Cbz route described in step 1 / 2 of the
seeded pathway is good chemistry but expensive on principles
8 and 9:

- Cbz protection + hydrogenolysis deprotection adds two
  whole steps that just protect-then-unprotect.  Principle 8
  violation by definition.
- DCC stoichiometry (> 1 eq.) → dicyclohexylurea byproduct
  that has to be filtered off (waste).  Principle 1 hit.

**Ajinomoto's green response**: the **thermolysin-catalysed
peptide coupling** mentioned in the step 1 notes.  The enzyme
is absolutely α-regioselective for the aspartyl α-COOH →
Phe-OMe amide, so no protection is needed.  Runs at pH 7,
room temperature, in water.  Passes principles 5, 6, 8, 9
simultaneously.  Scaled to 15 000 t/yr in the 1990s.

## Case 5 — Fischer esterification and Le Chatelier (Principles 2, 6)

Synthesis tab / Reactions tab → *Fischer esterification*
(5-step arrow-pushing mechanism).

The overall stoichiometry is beautifully atom-economical —
water is the only byproduct:

    R-COOH + R'-OH  ⇌  R-CO-O-R' + H₂O

The catch is the equilibrium sits roughly 1:1 at 25 °C.
Industrially, you pull it forward by:

- **Dean-Stark trap** — azeotropic distillation of water
  with an aromatic co-solvent.  Works, but the co-solvent
  (toluene) is itself a principle-5 concern.
- **Molecular sieves** — 3 Å absorbent for H₂O; passes
  principle 5.
- **Excess alcohol** — cheap for small-molecule esters
  (MeOH, EtOH).
- **Vacuum distillation** of water — if the temperature
  window allows.

Atom economy of the overall reaction is usually > 80 %.  The
*real* E-factor is dominated by the catalyst (usually conc.
H₂SO₄ — principle-3 hit) and the workup.  Principle 9 fixes
it: solid acid catalysts (Amberlyst-15, sulfonated silica)
give equivalent selectivity at room temperature with
trivial filtration.

## Case 6 — PLA: designed for degradation (Principles 4, 7, 10)

Polymer chemistry lesson (intermediate/09) mentions PLA
(polylactic acid) as a compostable alternative to polyolefins.
PLA passes a triple of green principles few other plastics can:

- **Principle 7 (renewable feedstocks)** — lactide monomer
  comes from fermentation of corn / sugarcane glucose.
- **Principle 4 (safer products)** — low-toxicity degradation
  products (lactic acid → CO₂ + H₂O in compost).
- **Principle 10 (design for degradation)** — the same
  hydrolysable ester bonds that make PLA step-growth also
  make it biodegradable in industrial compost (50-60 °C,
  ~60-90 days).  Polyolefin C-C bonds don't hydrolyse at all;
  PET ester bonds hydrolyse only slowly without base.

The drawback is that the degradation conditions (elevated
temperature, moisture) aren't common in landfills — so PLA
thrown in regular trash behaves much like PET.  Don't
oversell the "bioplastic" label.

## Scoring your own route

For a synthesis you're designing (or critiquing), run this
five-question checklist:

1. **AE ≥ 80 %?**  If yes, the stoichiometry is clean.  If
   no, look for better-atom-economy alternatives — a
   catalytic path may replace a stoichiometric oxidant.
2. **Any protecting group that's on-then-off in the same
   route?**  Principle-8 violation — look for a
   regioselective enzyme / catalyst (see Aspartame).
3. **Any stoichiometric reagent + > 5 kg / kg waste?**  If
   yes, check the literature for a catalytic alternative;
   if none exists, flag for further R&D.
4. **Any solvent on the EU REACH / EPA "substances of
   concern" list?**  Swap for water, ethanol, scCO₂, or
   ionic liquid.
5. **Does the product biodegrade?**  Many pharmaceuticals
   don't — they bioaccumulate in surface water.  Design for
   metabolism (soft-drug / retrometabolic design) if you
   have latitude.

## Exercises

1. Compute the overall atom economy for the seeded **Aspirin
   Kolbe-Schmitt route** by hand.  Compare against the
   output from Tools → Green metrics…
2. The seeded **Saccharin Remsen-Fahlberg route** uses
   chlorosulfonic acid + KMnO₄.  Assess it against principles
   1, 3, 5, 9 — name one specific green-chemistry upgrade you
   would propose.
3. Why is the **Carothers equation** (DP = 1/(1-p))
   relevant to green chemistry?  Hint: consider the yield
   per step × DP trade-off for step-growth polymers.
4. Open the **Hammett fit** dialog (Tools → Physical organic…)
   and find one reaction in the seeded catalogue where a ρ
   value could help predict a greener substrate.
5. Which of Anastas's 12 principles would be **made
   worse** by Knowles's L-DOPA route?  (Hint: step 3.)

## See also

- Glossary: {term:Atom economy}, {term:E-factor}, {term:Green
  chemistry}, {term:Chemoselectivity}, {term:Regioselectivity}.
- Tutorials: intermediate / 09 Polymer chemistry (PLA +
  recycling framing); graduate / 05 Catalysis — unified
  survey (how catalysis pass-through for principles 2/9).
- Reactions tab: Fischer esterification (mechanism).
  Synthesis tab: Adipic acid, Nylon-6, Nylon-6,6, L-DOPA,
  Aspartame — every case study above has a one-click path.
