# Synthesis design tactics — a checklist

You've learned chemistry. Now you face a new molecule + a
blank piece of paper. How do you design the synthesis?
This lesson collects the heuristics + tactical questions
practising synthetic chemists run through.

## Step 1: Read the target

Write the target structure carefully. Catalogue:

- **Ring count** + ring sizes + bridging.
- **Stereocentres** — count, assign R/S, note adjacencies
  (vicinal stereocentres need different tactics from
  isolated ones).
- **Functional groups** — list every one, ranked from
  *unique* to *ubiquitous*.
- **Symmetry** — fold lines, pseudo-symmetry, possibly
  exploit a desymmetrisation strategy.
- **Polar surface area / log P** — hint at how to handle
  it during synthesis.

## Step 2: Strategic disconnections (Corey)

Apply retrosynthetic logic:

1. **Find the strategic bond** — the one whose
   disconnection simplifies the molecule the most. Often
   the bond that closes the largest ring, or the bond
   between two distinct fragments.
2. **Look for known transforms** — every disconnection
   should map to a real forward reaction.
3. **Iterate** — keep disconnecting until you reach
   commercially available starting materials (Aldrich,
   Sigma, AK Scientific catalogues, Enamine REAL).
4. **Branch the tree** — pursue 2-3 routes in parallel; the
   "best" route may not be the first you find.

## Step 3: Convergence

Plan for **convergent synthesis** — assemble fragments
independently, then join late. Why?

- Yield: 5 linear steps at 70 % each = 17 %; 5-step
  convergent = ~ 30 % (the "long arm" is shorter).
- Risk: a problem in one fragment doesn't halt the whole
  pipeline.
- Parallelism: SAR exploration around a fragment reuses
  the other.

A useful guideline: aim for the **longest linear sequence**
under ~ 12 steps; total step count can be much higher.

## Step 4: Stereochemistry strategy

For each stereocentre, decide:

- **Substrate-controlled** — let the existing chirality
  control the new centre via a chair / Felkin-Anh / chelation
  TS.
- **Catalyst-controlled** — use an asymmetric catalyst
  (Sharpless AE/AD, Noyori H₂, Jacobsen, organocatalysis).
- **Auxiliary-controlled** — temporarily attach a chiral
  group (Evans oxazolidinone, Oppolzer sultam, Myers
  pseudoephedrine).
- **Resolution** — separate enantiomers chromatographically
  (chiral HPLC) or by salt formation.
- **Pool (chiral pool)** — start from a chiral natural
  product (amino acid, sugar, terpene) that already has
  the chirality.

## Step 5: Functional-group strategy

Order operations to:

- **Install functional groups in the order of rising
  reactivity** — protect or defer the most reactive ones.
- **Use protecting groups orthogonally** — choose Boc / Bn
  / TBS / Ac so each removes under different conditions.
- **Avoid pointless interconversions** — don't go COOH →
  CH₂OH → COOH if you can leave the COOH untouched.

## Step 6: Risk assessment

For each step, evaluate:

- **Atom economy** — Wittig vs metathesis vs HWE choice.
- **Toxicity / safety** — replace OsO₄ or HF when possible.
- **Scalability** — chromatography below 1 g; recrystallise
  above 1 g.
- **Robustness** — does the reaction work in your hands +
  with your substrate?
- **Cost of reagents + catalysts** — Pd (~ $80/g) is fine
  at 1 mol % but unsafe at 30 mol %.

## Tactical heuristics

### The "5-membered ring" rule

A 5-membered ring forms 10× faster than a 6-membered ring
(Baldwin's rules notwithstanding). When you have a choice,
plan ring closures to give 5-membered first.

### Baldwin's rules for ring closure

```
3-exo-tet: favoured
3-exo-trig: favoured
3-endo-tet: disfavoured
3-endo-trig: disfavoured
4-exo-tet: favoured
4-endo-tet: disfavoured
5-exo-tet: favoured
5-exo-trig: favoured
5-endo-trig: disfavoured (key!)
6-exo-tet/trig: favoured
6-endo-trig: favoured (5-endo-trig disfavoured)
```

The "endo-trig" cases are the famous trip-ups.

### Late-stage diversification

For SAR exploration, plan a **common penultimate
intermediate** that can branch into 30-100 final analogs in
1-2 steps. Useful disconnections to defer:

- Suzuki coupling on an aryl bromide.
- Reductive amination on a ketone.
- Click chemistry on an azide.
- C-H functionalisation on an arene.

### Telescoping vs isolation

Isolate intermediates:

- **Always** if the intermediate is a critical SM for
  another route.
- **Always** if downstream chemistry needs ultra-high
  purity.

Telescope (carry forward without workup):

- Quench → switch solvent → next step works on the same
  pot. Saves time + solvent + chromatography.
- Common in process chemistry.

## Modern tools

- **Computational retrosynthesis** — ASKCOS, AiZynthFinder,
  Synthia, Manifold. Suggest disconnections + propose
  routes.
- **DFT-guided mechanism** — predict regio + stereo
  outcomes before running the reaction.
- **HTE** — screen 96 conditions in a day to find optimum.
- **Flow chemistry** — turns a difficult reaction (cryogenic
  lithiation, photoredox) into a routine kg-scale process.
- **Biocatalysis** — Codexis enzymes for asymmetric
  reductions, transamination, hydroxylation, KREDs.

## Common failure modes

- **No retrosynthetic backbone** — you start with a vague
  idea, write 30 steps that "should work", run the first
  one, fail. Plan first.
- **Ignore precedent** — you propose a new disconnection
  with no literature support. Often there's a reason no
  one's done it.
- **Late-stage stereocentre** — installing a stereocentre
  in the final step is risky; one bad batch wastes the
  whole route.
- **Untested chiral catalysis** — don't bank on > 90 % ee
  for an untested substrate type; do a small-scale
  validation first.
- **Forget the workup** — a yield-on-paper is irrelevant
  if you can't extract / chromatograph the product.

## Try it in the app

- **Tools → Retrosynthesis…** → input target SMILES; see
  template-based disconnection suggestions.
- **Synthesis tab** → load any seeded multi-step pathway
  for examples of how routes are planned.
- **Glossary** → search *Retrosynthesis*, *Convergent
  synthesis*, *Baldwin's rules*, *Chiral pool*, *Late-stage
  diversification*.

Next: **NMR theory deeper** (graduate tier).
