# Elimination: E1 vs E2

Elimination is the other reaction that happens to the same substrates
that undergo substitution. Where SN1/SN2 replaces a leaving group with a
nucleophile, E1/E2 removes the leaving group *and* a neighbouring
hydrogen, forming a new π bond. The decision between substitution and
elimination lives inside the same reaction flask, and which one wins
depends on heat, solvent, base strength, and substrate structure.

Load the **Reactions** tab and pick the two mechanisms **"E2: 2-bromobutane
+ hydroxide"** and **"E1: tert-butyl bromide in ethanol"** — press the
**Play mechanism** button to step through the arrows.

## E2 — "bimolecular, concerted"

**Rate law:** `rate = k [R-LG][base]`. Both must collide productively.

One step. Three things happen in concert:

1. The base takes a β-hydrogen (the H on the carbon next to the one
   bearing the leaving group).
2. The C–H bonding pair becomes the new π bond between the α- and β-
   carbons.
3. The α-C–LG bond breaks with electrons leaving to LG.

For this to work the β-H and the leaving group must be **antiperiplanar** —
on opposite faces of the α-β bond so the four-atom σ/σ system can line up
into a planar six-electron transition state. In cyclohexanes this means
both groups must be axial; it's what sets the stereochemistry of E2
products.

Consequences:

- **Zaitsev's rule**: the more substituted alkene dominates (more
  stable). Small bases lead to Zaitsev.
- **Hofmann product**: bulky bases (like *tert*-butoxide) prefer the
  less hindered β-H and give the less substituted alkene.
- **Stereochemistry**: syn eliminations (where β-H and LG are on the
  same face) are very slow — the antiperiplanar geometry is required.

## E1 — "unimolecular, stepwise"

**Rate law:** `rate = k [R-LG]` — same as SN1.

Two steps:

1. C–LG ionises to give a carbocation. **Slow, rate-determining.**
2. A base (often just solvent) removes a β-proton; the C–H electrons form
   the π bond. **Fast.**

Consequences:

- Same substrate preferences as SN1: tertiary > secondary ≫ primary.
- Always competes with SN1 at the carbocation stage. **Heat pushes
  toward E1** (elimination has a positive ΔS; substitution doesn't).
- Scrambled stereochemistry because the carbocation is flat.
- Can rearrange via hydride or methyl shifts before elimination.

## The four-way decision tree

You have an alkyl halide in a flask. Four products fight:

| Substrate | Cold + strong unhindered nu. | Cold + weak nu. | Hot + weak nu./base | Hot + strong bulky base |
|-----------|------------------------------|-----------------|---------------------|-------------------------|
| primary   | SN2                          | SN2 (slow)      | E2                  | E2 (Hofmann)            |
| secondary | SN2                          | SN1/E1 mix      | E1/E2               | E2 (Hofmann)            |
| tertiary  | E2 only                      | SN1/E1 mix      | E1                  | E2 (Hofmann)            |

*Methyl halides never eliminate — no β-hydrogens to lose.*

## The mechanism panel

Click **Play mechanism** on the E2 reaction. You'll see three red arrows
overlaid on 2-bromobutane + hydroxide:

- One from hydroxide's oxygen toward the β-carbon (representing "base
  takes β-H").
- One from the β-carbon toward the α-carbon ("new π bond forms").
- One from the α-carbon toward bromine ("C–Br breaks, electrons to Br").

Advance to step 2 and the arrows are gone — the products (2-butene,
bromide, water) are shown.

Click **Play mechanism** on E1 and you'll see *two* separate steps —
exactly matching the kinetic signature of the stepwise mechanism.

## Try it

1. Step through the **SN2** and **E2** mechanisms back-to-back. Both
   have a strong base and a substrate with a leaving group — but the
   arrow count (2 vs 3) and what's attacked (α-C vs β-H) differ.
2. Step through **SN1** and **E1**. Notice the first step is identical —
   the carbocation is the common intermediate. It's the *second* step
   that chooses between the two outcomes.
3. Open **Cholesterol** in the molecule browser. If we were to
   dehydrate its 3β-hydroxyl (E1 under acid), which alkene position
   would we expect via Zaitsev? Draw it on paper, then verify by
   comparing with the known dehydration product.

Next lesson: **Aromaticity and electrophilic aromatic substitution.**
