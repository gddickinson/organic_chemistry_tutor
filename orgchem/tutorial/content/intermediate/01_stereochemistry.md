# Stereochemistry: R/S, E/Z, Chirality

Two molecules can have the **same atoms**, the **same bonds**, and still
be different. That's the heart of stereochemistry — and it matters
enormously in organic chemistry because biology is chiral. One enantiomer
of thalidomide is a sedative; the other is a teratogen. One enantiomer
of carvone smells like spearmint; the other smells like caraway.

## Why carbon can be chiral

An sp³ carbon with **four different substituents** has no internal
mirror plane, no rotation axis, nothing that superimposes it onto its
mirror image. Try it with one of your hands — left and right hands are
mirror images but no amount of rotation makes them equivalent. That's
chirality.

Such a carbon is called a **stereocentre** (older texts: "chiral
centre"). The CIP rules then assign it an **R** or **S** descriptor.

Try it: in the **Molecule Workspace** load **L-Alanine** (its SMILES is
`N[C@@H](C)C(=O)O`). The `@@` encodes the stereochemistry. The
descriptors panel on the right should list one stereocentre. You can ask
the LLM tutor:

> Show me the enantiomer of L-alanine and tell me its R/S descriptor.

Under the hood this triggers the `enantiomer_of` agent action, flipping
every `@` to `@@` and vice versa, and returns `D-alanine` — the R
enantiomer.

## Assigning R/S: the CIP rules

Cahn-Ingold-Prelog (CIP) priority is "atomic number wins, with a
series of tie-breakers". Practically:

1. Rank the four substituents at the stereocentre by **atomic number**.
   Higher Z → higher priority. `I > Br > Cl > F > O > N > C > H`.
2. If two substituents tie at the first atom, look at the **next shell
   out**. `-CH₂OH` beats `-CH₂CH₃` because O beats C at the second
   shell.
3. Double bonds count as **duplicate atoms**. `-CH=O` is treated as
   `-CH(O)(O)` for the ranking.
4. **View the molecule** with the lowest-priority group pointing
   **away** from you.
5. Walk 1 → 2 → 3. Clockwise is **R** (rectus, Latin for "right"),
   anticlockwise is **S** (sinister, Latin for "left").

## Wedge and dash bonds

On paper we use wedge/dash bonds to show the 3D arrangement:

- **Solid wedge** — coming toward you, out of the page.
- **Dashed wedge** — going away from you, into the page.
- Plain line — in the plane of the page.

The app renders these automatically when you select a chiral molecule.
Every 2D render with `show_stereo_labels=True` also overlays the
CIP descriptor in parentheses, e.g. `(R)` right on the stereocentre.

## E and Z for double bonds

Disubstituted alkenes are the other common stereoisomer family. A C=C
can't rotate, so the two arrangements of substituents are distinct
compounds.

- **E** (entgegen, "opposite") — the higher-CIP-priority substituents on
  each carbon are on **opposite** sides of the double bond.
- **Z** (zusammen, "together") — on the **same** side.

The older `cis / trans` labels still show up in textbooks; they line up
with Z / E most of the time but can disagree when the priorities are
unusual. **E / Z always work.**

Open the tutor and ask:

> What's the E/Z descriptor of (2E,4E)-hexa-2,4-dienal?

The answer comes from RDKit's `AssignStereochemistry`, wrapped by
`core/stereo.py`.

## Stereoisomerism families

Molecules with n stereocentres can have up to 2ⁿ stereoisomers. The
relationships:

- **Enantiomers**: non-superimposable mirror images. Identical physical
  properties except for optical rotation and chiral-environment
  interactions (enzymes, receptors).
- **Diastereomers**: stereoisomers that *aren't* mirror images. Distinct
  melting points, solubilities, spectra.
- **Meso compounds**: have stereocentres but also an internal mirror
  plane — so the "enantiomer" is the same molecule. Meso tartaric acid
  (R,S) vs. D-tartaric (R,R) vs. L-tartaric (S,S).

## Why biology cares

Nearly every natural amino acid is **L** (S). Nearly every natural sugar
is **D** (R in the canonical carbon). This isn't chance — it's a
consequence of enzyme active sites being chiral, so they evolved to bind
one hand but not the other.

Drugs often exploit this. **Ibuprofen** is sold as a racemate, but only
the S enantiomer is pharmacologically active (the R is slowly
epimerised in vivo, which is why the racemate still works). Modern
practice is to market the pure single enantiomer when the two behave
differently enough to matter.

## Stereochemistry shows up in mechanisms

- **SN2** gives **inversion** of configuration — the nucleophile attacks
  from the opposite face of the leaving group. See the SN2 3D
  trajectory in the Reactions tab.
- **SN1** gives **racemisation** — the flat carbocation intermediate
  can be attacked from either face.
- **E2** is **anti-periplanar** — H and leaving group must be on opposite
  sides of the C-C bond that becomes the π bond.
- **Diels-Alder** is **stereospecific** — cis dienophiles give cis
  products, trans give trans. The reaction conserves relative
  stereochemistry.

## Practice

1. In the **Glossary tab**, search "stereo" and read the entries for
   **Stereocentre**, **Enantiomer**, **Diastereomer**, **Meso
   compound**, and **R/S configuration**.
2. Load **D-Glucose** into the viewer. How many stereocentres does it
   have? How many stereoisomers does that imply?
3. Use the agent: `enantiomer_of(smiles="CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O")`.
   Compare the two canonical SMILES. Can you see which atom flipped?
4. Try the **flip_stereocentre** action on a known chiral molecule and
   verify the descriptor flips.

Next: **Aromaticity and electrophilic aromatic substitution**, where
resonance + orbital symmetry meet.
