# Stereochemistry 101 — Why 3D Matters

Every molecule you've drawn so far has been flat on the page.
That flat drawing is a **2D projection** — a compressed summary
of a real, 3D, tetrahedral arrangement of atoms in space.
Usually this compression is fine.  Sometimes it loses
information that completely changes how the molecule behaves.

This lesson is your first look at the lost information.  The
deep-dive — *R*/*S* assignment, *E*/*Z* bond priorities, the
Cahn-Ingold-Prelog rules — waits in the intermediate lesson
[*Stereochemistry (R/S, E/Z, chirality)*](intermediate/01_stereochemistry.md).
Start here.

## A tale of two pills

In 1957 the German company Chemie Grünenthal sold thalidomide
as a morning-sickness remedy for pregnant women.  It worked.
It also — devastatingly — caused severe limb deformities in
more than 10 000 babies before being withdrawn in 1961.

The physical thalidomide pill contained an equal mix of two
molecules that are **mirror images of each other**:

    (R)-thalidomide  →  sedative, effective antinausea
    (S)-thalidomide  →  teratogenic, causes birth defects

Same formula.  Same bonds.  Same connectivity.  Different
arrangements in 3D.  One helps; the other harms.

This is **stereochemistry** — the study of how molecules are
arranged in three dimensions and what happens when that
arrangement changes.

## Your hands are chiral

Hold your hands out in front of you, palms facing away.
Rotate them.  Try to overlay one on the other: palm-to-palm
works if you flip the orientation, but back-to-back doesn't
without a mirror.  Your left hand and right hand are
**non-superimposable mirror images** of each other.

A molecule with this same property is called **chiral** (from
the Greek χείρ, "hand").  The two mirror-image forms are
called **enantiomers**.

Here's the single easiest way to build your intuition.  Any
carbon that has **four different substituents** attached is a
**stereocentre** (or "chiral centre").  For each stereocentre,
there are exactly two mirror-image arrangements — imagine
swapping any two of the four substituents, and you flip to
the enantiomer.

    Cl   Cl
     \   \        ← these two molecules are mirror images
      C   C       (one is the enantiomer of the other)
     / \ / \
    F   Br       (bear with the ASCII — real 3D has the
                  sticks pointing out of the page too)

## Why your nose notices

Most biological receptors are themselves chiral — made of
L-amino acids folded into chiral pockets.  An enantiomer fits
into the pocket one way but not the mirror-image way.  So
your body routinely tells enantiomers apart:

| Molecule | (R)-enantiomer smells like | (S)-enantiomer smells like |
|----------|----------------------------|----------------------------|
| Carvone  | caraway seed               | spearmint                  |
| Limonene | oranges                    | lemons                     |

Same molecular formula, same bond list, same everything
except the 3D layout at one stereocentre.  Your olfactory
receptors spot the difference — in the case of carvone, they
place you in either a rye-bread bakery or a chewing-gum aisle.

## "R or S?" — a thumbnail

Chemists label the two enantiomers with **R** (*rectus*,
Latin for "right") and **S** (*sinister*, "left") using the
*Cahn-Ingold-Prelog* priority rules.  The procedure in
thumbnail:

1. Look at the four substituents on the stereocentre.
2. Rank them 1 → 4 by atomic number (higher-Z wins).
3. Point the lowest-priority substituent (usually H)
   *away* from you.
4. Trace 1 → 2 → 3.  Clockwise = **R**.  Counter-clockwise
   = **S**.

The intermediate lesson walks every rule case + tie-break
properly; for now, just remember that the descriptor is a
**conventional label**, not a physical property.  (*R*)-
thalidomide and (*S*)-thalidomide still react with acids and
bases identically — only their interaction with other chiral
things (receptors, enzymes, drug targets) differs.

## Cis / trans and E / Z — when bonds are double

Stereocentres only happen at tetrahedral carbons.  Double
bonds introduce a different kind of fixed-in-space
arrangement because the π bond blocks rotation:

    H   H         H   Br
     \ /           \ /
      C==C    vs    C==C
     / \           / \
    Br  Br        Br   H

    "cis" or Z       "trans" or E
    (same-side Brs)  (across-the-bond Brs)

The old-fashioned labels are **cis** (same side) and
**trans** (across).  The modern, unambiguous labels are
**Z** (*zusammen*, "together") and **E** (*entgegen*,
"opposite") assigned by CIP priorities — same rule system as
*R*/*S*.  Full treatment: intermediate lesson 01.

## Meso and diastereomers — a preview

If a molecule has **two or more** stereocentres, more things
happen:

- With n stereocentres you get up to 2ⁿ distinct stereoisomers
  (fewer if the molecule has internal symmetry).
- A **meso compound** has stereocentres that cancel —
  e.g. (R,S)-tartaric acid is superimposable on its mirror
  image and is therefore achiral as a whole.
- Two stereoisomers that are *not* mirror images are called
  **diastereomers** — unlike enantiomers, they have
  different physical properties (melting point, solubility,
  spectra).

Again, detail lives in intermediate/01.  The point of this
primer is to *see* that the flat drawing is not the whole
story.

## Practice your eye

Open the Stereochemistry dialog: **Tools → Stereochemistry…**
Type a SMILES string and the dialog prints every assigned
stereocentre with its descriptor.  Try these:

| SMILES | Result |
|--------|--------|
| `C[C@H](N)C(=O)O` | L-alanine — one (*S*) stereocentre |
| `C[C@@H](N)C(=O)O` | D-alanine — same bond list, flipped to (*R*) |
| `C/C=C/C` | *trans* / *E*-2-butene |
| `C/C=C\C` | *cis* / *Z*-2-butene |
| `O[C@@H](CO)[C@@H](O)[C@H](O)[C@H](O)C=O` | D-glucose (4 stereocentres, all assigned) |

The `@` and `@@` marks are SMILES's way of writing the 3D
information that the flat drawing can't.  Look at them as
"the direction the wedge points."  Flipping a single `@` to
`@@` flips one stereocentre — which may be a perfectly
reasonable compound (the enantiomer or a diastereomer), a
meso form, or nothing at all depending on the rest of the
molecule.

## Three takeaways to remember

1. A **stereocentre** is a carbon (or other sp³ atom) with
   four different substituents.  Each one adds a factor of
   two to the possible 3D arrangements.
2. Two molecules that are **non-superimposable mirror
   images** are **enantiomers**.  They share every scalar
   physical property (melting point, density, logP) *except*
   the direction they rotate plane-polarised light and their
   behaviour toward other chiral partners.
3. The 2D drawing tells you the **connectivity**; the 3D
   label (wedges, *R*/*S*, *cis*/*trans*, `@`/`@@`) tells you
   the **arrangement**.  Both matter.

## See also

- Intermediate / 01 *Stereochemistry (R/S, E/Z, chirality)* —
  the full CIP priority-rules walkthrough, diastereomers,
  meso, conformational vs configurational stereochemistry.
- Intermediate / 07 *Sugars and carbohydrates* — every
  sugar is a multi-stereocentre compound; anomers in
  particular are paired diastereomers at the hemiacetal
  carbon.
- Advanced / 02 *Organometallics* — asymmetric catalysis
  (Knowles Rh-DIPAMP, Nobel 2001) is all about making one
  enantiomer in preference to the other.
- Glossary: {term:Enantiomer}, {term:Diastereomer},
  {term:Stereocentre}, {term:R/S configuration},
  {term:E/Z configuration}, {term:Meso compound},
  {term:Enantiomeric excess}, {term:Anomer},
  {term:Walden inversion}.
