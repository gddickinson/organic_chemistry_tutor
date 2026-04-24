# Reading SMILES — a Practical Primer

Open almost anywhere in this app and you'll find strings like

    CC(=O)Oc1ccccc1C(=O)O

That's **aspirin**, written in **SMILES** — *Simplified
Molecular-Input Line-Entry System*.  SMILES is how chemists
pass structures to computers: one line of text that a machine
can parse unambiguously into a 2D (or 3D) model.  This lesson
teaches you to read it at the level a beginner organic-
chemistry student needs.

The related lesson [03 Lewis & skeletal structures] taught you
to read and draw the skeletal form by hand.  SMILES is the
same information **written as a string** — same connectivity,
same atoms, same hydrogens, just a different notation system.

## Quick worked example — ethanol

Paste **`CCO`** into the Molecule Workspace search box
(or use Ctrl+K → "ethanol").  You get:

    H   H   H
     \ | / |
      C-C-O-H
     / | \
    H  H  H

Three characters.  The rules are:

1. **Each letter is an atom.**  `C`, `O`, `N`, `S`, `P`, `F`,
   `Cl`, `Br`, `I`, `B` — those are the "organic subset"
   atoms you write **without brackets**.  Anything else, or
   any atom with an unusual charge / isotope / H-count, must
   go inside `[ ]`.
2. **Adjacent atoms are bonded.**  `CCO` = C bonded to C
   bonded to O.  The bonds are **implicitly single**.
3. **Hydrogens are implicit.**  SMILES auto-fills enough H's
   to complete the valence (C = 4, N = 3, O = 2, …).  You
   don't write them.

So `CCO` is **CH₃-CH₂-OH** — ethanol.

## Bonds explicitly

| Symbol | Bond |
|--------|------|
| (nothing) | single |
| `=` | double |
| `#` | triple |
| `:` | aromatic (rarely written; lowercase atom is equivalent) |

Examples:

- `CC` — ethane (two sp³ carbons, single bond)
- `C=C` — ethene (double bond; sp² each carbon gets 2 H)
- `C#C` — ethyne / acetylene (triple bond; 1 H each)
- `C=O` — formaldehyde (1 C, 1 O, 2 H on C)
- `C#N` — hydrogen cyanide (HCN; the H is on the C)

Tip — you only *write* the single-bond dash in SMILES if you
really need to (e.g. inside brackets).  `CC` is much more
common than `C-C`.

## Branches

Parentheses `(` and `)` mark a **branch off the main chain**.
The atoms inside the parens hang off whatever atom is to
their left.

    CC(C)C          → isobutane (central C has 3 methyl branches)
    CC(=O)C         → acetone (central C has a =O branch)
    CC(=O)OC        → methyl acetate
    CC(Cl)C         → 2-chloropropane

The central pattern `C(=O)O` is a carboxylic acid.  Reading
aspirin now:

    CC(=O)Oc1ccccc1C(=O)O
    └──┬──┘│└──┬──┘│└──┬──┘
       acetyl  ring  -COOH
       ester   (benzene)
       -OAc

Three pieces: acetyl ester, benzene ring, carboxylic acid.

## Rings

Rings use **matching digits** as ring-closure markers.  The
digit appears twice — both instances identify atoms that are
bonded to each other, but the bond isn't written explicitly
anywhere else in the string.

- `C1CCCCC1` — cyclohexane.  The first `1` says "open a
  ring-close marker on this C", the second `1` says "close
  it here."  The atoms between them (CCCCC) fill the ring.
- `c1ccccc1` — benzene (lowercase `c` means aromatic).
- `C1CCNCC1` — piperidine (6-ring with one N).
- `C1=CC=CC=C1` — **Kekulé-form benzene**, with explicit
  alternating double bonds.  Valid SMILES but non-canonical;
  RDKit normalises this to `c1ccccc1`.

For digits > 9, use `%nn` — e.g. `%10` is ring-closure 10.
You'll see this in very large natural products.

## Aromatic = lowercase

Atoms participating in an aromatic ring are written
**lowercase**: `c`, `n`, `o`, `s`.  Benzene is `c1ccccc1`;
pyridine is `c1ccncc1`; furan is `c1ccoc1`.

RDKit (and most toolkits) do the aromaticity perception for
you: you can write a Kekulé form with `C` + `=` and the
parser will normalise.  Lowercase is faster to read, so it's
the **canonical** form the Molecule browser shows you.

## Brackets — when to use them

Any atom that isn't in the organic subset **must** go in
`[ ]`.  Also:

- Charged atoms: `[NH4+]` (ammonium), `[O-]` (oxide anion),
  `[OH-]` (hydroxide).
- Unusual H-counts: `[CH3]` (methyl cation, if the
  surrounding context doesn't make `C` get 3 H).
- Isotopes: `[13C]` (carbon-13).

Inside brackets, H is explicit — you write it out.  `[NH4+]`
has 4 H.  `[Mg+2]` (magnesium with a +2 charge) has 0 H.

## Stereochemistry — brief

SMILES encodes 3D stereochemistry with two markers:

- **`@` / `@@`** on a stereogenic atom means "looking from
  the first-listed substituent, the remaining three run
  counter-clockwise (@) or clockwise (@@)."  This is
  mechanical — you rarely *read* these, but you see them
  on every chiral amino acid and sugar.
- **`/` / `\`** on a double bond record the *E*/*Z*
  arrangement.

Examples:

- `C[C@H](N)C(=O)O` — L-alanine ((*S*)-2-aminopropanoic acid)
- `C[C@@H](N)C(=O)O` — D-alanine, the enantiomer
- `C/C=C/C` — (*E*)-2-butene (trans)
- `C/C=C\C` — (*Z*)-2-butene (cis)

Full treatment in *beginner / 07 Stereochemistry 101* and
*intermediate / 01 Stereochemistry*.

## Reading three real seeded SMILES

### Caffeine — `Cn1c(=O)c2c(ncn2C)n(C)c1=O`

Break it down:

    C n1 c(=O) c2 c(ncn2 C) n(C) c1 =O

Two fused rings (markers `1` and `2`), the larger a 6-
pyrimidinedione, the smaller a 5-imidazole.  Three methyls
(`C`) decorate nitrogens; two `=O` are the carbonyls.
Classic xanthine heterocycle.

### Aspirin — `CC(=O)Oc1ccccc1C(=O)O`

Reading left to right: `CC(=O)O` is an acetyl ester (-OAc);
`c1ccccc1` is a benzene ring; `C(=O)O` is a carboxylic acid.
Put together: 2-acetoxybenzoic acid — the IUPAC name you
already know from *beginner / 05 Nomenclature*.

### Benzocaine — `CCOC(=O)c1ccc(N)cc1`

`CCO` is an ethoxy; `C(=O)` is a carbonyl; the combination
`CCOC(=O)` is an **ethyl ester**.  Then `c1ccc(N)cc1` — a
benzene ring with a primary amine (`N`) on one para position.
4-aminoethylbenzoate — the local-anaesthetic ethyl ester
of PABA.

## Five-step reading recipe

Every time you meet a SMILES, do this:

1. **Split the string at the outer branches**.  Identify the
   backbone (the longest unbracketed chain).
2. **Find the rings** — count matching digits.
3. **Find the functional groups** — watch for `C(=O)O`
   (acid), `C(=O)N` (amide), `OC(=O)` (ester), `c1ccccc1`
   (benzene), `[OH]` (alcohol), `N` (amine).
4. **Check the stereo** — any `@` / `@@` / `/` / `\`?
5. **Eyeball the H count** — count implicit H on every
   non-bracketed atom.  C needs 4 total, N needs 3, O needs
   2.

With practice, you'll read `CC(=O)Oc1ccccc1C(=O)O` in under
a second as "aspirin."

## Paste and explore

Open Tools → Stereochemistry… or Tools → Orbitals (Hückel /
W-H) and paste SMILES strings to see them rendered and
analysed.  The Molecule Workspace search box accepts SMILES
directly too (type `CCO` and hit Enter — ethanol appears).
The Molecule browser also supports drag-and-drop from
external sources.

## Things SMILES **doesn't** say

- **3D conformation** — SMILES tells the connectivity and
  the *R*/*S* / *E*/*Z* labels, not the current ring
  pucker or dihedral angles.  Use the 3D viewer for that.
- **Protonation state in solution** — the SMILES gives the
  drawn form; physiological charge state is inferred
  separately (pKa lookups).
- **Tautomer** — keto vs enol of a β-ketoester looks
  different; most databases store one canonical tautomer
  and flag the others as search synonyms.

## Exercises

1. Draw the skeletal structure for `CCN(CC)CCOC(=O)c1ccc(N)cc1`.
   (Hint: this is Procaine — seeded in the Synthesis tab.)
2. Predict the SMILES of 2-methylpropanal (isobutyraldehyde).
3. Is `c1ccccc1O` the same as `Oc1ccccc1`?  Explain.
4. What does `[C@H]` tell you that plain `C` doesn't?
5. Read aloud: `CC(=O)NC1=CC=CC=C1`.  (Acetanilide — seeded
   in the Synthesis tab and used as a precursor for
   phenacetin and sulfanilamide.)

## See also

- Beginner / 03 Lewis & skeletal structures — the hand-
  drawn equivalent.
- Beginner / 07 Stereochemistry 101 — the `@` / `@@` / `/` /
  `\` story.
- Intermediate / 01 Stereochemistry — full CIP rules.
- Glossary: {term:SMILES}, {term:Covalent bond},
  {term:Hybridisation}, {term:Aromaticity},
  {term:Carbonyl}.
