# Nucleophilic Substitution: SN1 vs SN2

Nucleophilic substitution is the single most-taught reaction mechanism
in organic chemistry because it's:
- simple (two arrows, sometimes three),
- everywhere (biochemistry, drug synthesis, industrial processes),
- and cleanly stratified into exactly two archetypes that behave very
  differently.

Open the **Reactions** tab (top bar) and load the two reactions
**"SN2: methyl bromide + hydroxide"** and **"SN1: tert-butyl bromide
hydrolysis"** side-by-side in your head as you read.

## The common story

Both reactions replace a leaving group (the thing that walks away with
the bonding pair) with a nucleophile (the thing that donates its pair to
form the new bond). On paper:

    Nu⁻ + R–LG  →  Nu–R + LG⁻

Everything interesting is in *how* this substitution happens.

## SN2 — "bimolecular, concerted"

**Rate law:** first order in substrate, first order in nucleophile.
`rate = k [R-LG][Nu⁻]`

One step. The nucleophile attacks the carbon at 180° from the leaving
group (**backside attack**), and as the new bond forms, the old bond
breaks — in one flowing motion.

Consequences:

- **Stereochemistry**: the carbon inverts, like an umbrella in a
  windstorm. A chiral R-bromide gives the opposite-handed R-alcohol.
- **Substrate preference**: methyl > primary > secondary ≫ tertiary.
  Tertiary carbons are too crowded — the nucleophile can't reach.
- **Nucleophile preference**: strong, unhindered anions. OH⁻, CH₃O⁻, CN⁻.
- **Solvent preference**: polar aprotic (DMSO, DMF, acetone) — doesn't
  tie up the nucleophile with hydrogen bonds.
- **Leaving group**: must be stable as the anion (weak conjugate base).
  I⁻ > Br⁻ > Cl⁻ ≫ F⁻, OH⁻, NH₂⁻.

## SN1 — "unimolecular, stepwise"

**Rate law:** first order in substrate *only*.
`rate = k [R-LG]`

Two steps. First the substrate ionises (slow), giving a carbocation.
Then the nucleophile captures the cation (fast).

Consequences:

- **Stereochemistry**: the intermediate cation is flat (sp²), so the
  nucleophile can attack from either face — racemisation. Starting
  chiral → ending 50:50 mixture.
- **Substrate preference**: tertiary > secondary ≫ primary ≫ methyl.
  The cation must be stable enough to form (hyperconjugation +
  inductive donation from alkyl groups).
- **Nucleophile preference**: doesn't appear in the rate law, so weak
  neutral nucleophiles work fine. Water, ethanol.
- **Solvent preference**: polar protic (water, alcohols) — stabilises
  the cation and anion.
- **Leaving group**: same hierarchy as SN2.

## The decision tree

A substrate handed to you, and you want to predict which mechanism wins:

1. **Primary?** → SN2. (Methyl and primary substrates can't support the
   cation that SN1 would need.)
2. **Tertiary?** → SN1 (with neutral nucleophile) or E1 elimination
   (with heat, weak base). SN2 is blocked by steric bulk.
3. **Secondary?** → It depends on the nucleophile and solvent:
   - Strong nucleophile + polar aprotic → SN2.
   - Weak nucleophile + polar protic + heat → SN1 / E1.

## Things that confuse students (and examiners)

- **"Polar aprotic" ≠ "non-polar"**. DMSO is *very* polar; it just can't
  donate a hydrogen bond. That's what makes it the SN2 solvent of choice.
- **Leaving-group ability is about the anion, not the atom**. Triflate
  (CF₃SO₃⁻) is an extraordinary leaving group because the anion is
  delocalised; F⁻ is a terrible one because the anion is destabilised.
- **E1 / E2 always lurk.** If the substrate has a β-hydrogen, elimination
  competes. Strong bulky bases (tert-butoxide) push toward elimination;
  heat pushes toward elimination. If you need the alcohol, keep it cold.
- **Allyl and benzyl substrates cheat.** They stabilise the SN1 cation
  through π-donation, so primary allyl / benzyl halides can go SN1 —
  often faster than you'd expect from "primary → SN2."

## Try it

In the **Reactions** tab, select the SN2 entry. Read the description.
Try the SN1 entry and compare — the reaction SMILES is almost identical
(same bonds formed/broken), but the mechanism class and category are
different. In the Reaction panel you can also see the category column
(Substitution for both).

Now go to the **Molecule Workspace** and load **Cocaine**. Its structure
contains two ester groups — each of which would hydrolyse via *acyl*
substitution, a cousin of SN1/SN2 that we'll reach in the carbonyl
lesson.

Next lesson: **Elimination (E1 / E2)** — same substrates, different
outcome.
