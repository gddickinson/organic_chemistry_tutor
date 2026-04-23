# Lewis and Skeletal Structures

There are several ways to draw an organic molecule. You need to read
them all fluently, because every textbook, paper, and lecture will mix
them without warning.

## Four representations of the same molecule

Take **ethanol** (CH₃CH₂OH). Select it in the browser — the app shows
it as the *skeletal* form. Here's what else it can look like:

| Form | What's drawn | When you'll see it |
|------|--------------|--------------------|
| **Molecular formula** | `C2H6O` | First-line identification. Hides structure. |
| **Condensed structure** | `CH3CH2OH` | Tight one-line depiction, common in text. |
| **Lewis structure** | Every atom, every bond, all lone pairs | Homework, first-year courses. |
| **Kekulé structure** | Every atom + bond, no lone pairs | Common in published schemes. |
| **Skeletal ("line-bond")** | Carbons implicit at line ends/corners, hydrogens implicit | The working language of organic chemistry. |

Flip the **Style** selector on the 2D viewer between *Skeletal*, *Kekulé*,
*Atom indices*, and *Explicit hydrogens* — notice how the same molecule
looks radically different, but the atoms and bonds are identical.

## Reading skeletal structures

The convention is dense — once mastered, a whole reaction scheme fits on
a postcard.

- **Every line endpoint or corner is a carbon** unless labelled
  otherwise.
- **Hydrogens on carbon are implicit** — count them to give each carbon
  4 bonds total.
- **Heteroatoms are always labelled** — O, N, S, halogens appear as
  their symbol.
- **Double bonds** are drawn as two parallel lines; **triple**, three.
- **Wedges and dashes** show 3D orientation — solid wedge comes toward
  you, dashed recedes.

Try it: open **D-Glucose** and count the explicit hydrogens in the 2D
view. Now switch to *Explicit hydrogens* mode — the app draws every H.
The hydroxyl Hs were already visible because they're on oxygen; the CH
and CH₂ protons now appear on the ring carbons.

## Stereochemistry cues in 2D

Three molecules that look identical in SMILES can differ by **which
side of the plane** a group sits on:

- A plain line = either side, unspecified.
- A solid wedge `↟` = that bond comes forward (out of the page).
- A dashed wedge `╴╴╴` = that bond goes back (into the page).

Load **Cholesterol** and look at the fused ring system — you'll see
wedges on the methyl groups at positions 10 and 13, and on the
3β-hydroxyl. These are what make cholesterol's specific stereochemistry
*the* stereochemistry (there are 2⁸ = 256 possible diastereomers; only
one is biologically active).

## Skeletal → 3D in your head

When you see a skeletal drawing, mentally expand it:

1. Add a hydrogen to every carbon until its valence is 4.
2. Sort the carbons by hybridisation (sp³ / sp² / sp — lesson 2).
3. Place the bonds at the canonical angles (109.5° / 120° / 180°).
4. Wedges and dashes pin the out-of-plane atoms.

The 3D viewer does this for you in seconds; but your ability to do it on
paper is what distinguishes fluent from novice organic chemists.

## Exercise

1. Click **Benzene** — count the carbons and hydrogens in the skeletal
   form. Verify it's C₆H₆ via the Properties panel.
2. Click **Cocaine** — which atoms in its skeletal form are stereo-
   assigned? Which bond is drawn with a wedge? Which atoms form the
   tropane ring system?
3. Click **Porphyrin** — why does the app render it as a macrocycle
   rather than as four separate pyrroles?

Next lesson: functional groups — the reactivity vocabulary of organic
chemistry.
