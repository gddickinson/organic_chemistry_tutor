# Isomerism: a unified hierarchy

You've already met **stereochemistry** in lesson 1.  This lesson zooms
out to the wider question that stereochemistry is one branch of:
**when do two molecules count as the same compound, and when don't
they?**  The answer organises into a hierarchy that's worth memorising
because it underpins everything that follows — drug discovery,
spectroscopy, retrosynthesis, biochemistry.

Try it: in the **Tools** menu, open **Isomer relationships…**
(`Ctrl+Shift+B`).  We'll come back to this dialog with worked
examples through the lesson.

## The five-tier hierarchy

| Level | Same molecular formula? | Same connectivity? | Same 3D? |
|-------|-------------------------|--------------------|----------|
| **Identical** | yes | yes | yes |
| **Conformer** | yes | yes | rotation around single bonds only |
| **Enantiomer** | yes | yes | mirror images |
| **Diastereomer** | yes | yes | NOT mirror images |
| **Tautomer** | yes | no (proton shift) | — |
| **Constitutional isomer** | yes | no | — |
| **Different molecule** | no | — | — |

Notice that **isomerism only applies when the molecular formula
matches** — toluene and benzene aren't isomers of each other because
toluene has an extra CH₂.  **All isomers share a formula.**

## Constitutional / structural isomers — different bonds

The simplest case.  Same atoms, wired up differently.  Most of the
worked examples in introductory organic chemistry are constitutional:

- **n-butanol** (`CCCCO`), **sec-butanol** (`CCC(O)C`), **isobutanol**
  (`CC(C)CO`), and **tert-butanol** (`CC(C)(C)O`) are all C₄H₁₀O.
- **Propanal** (`CCC=O`) and **acetone** (`CC(C)=O`) are both C₃H₆O —
  same formula, completely different functional groups.

Try it: open **Tools → Isomer relationships…**, switch to the
**Classify pair** tab, paste `CCC=O` and `CC(C)=O`, click *Classify
relationship*.  You should get the green-coloured `constitutional`
verdict + a 2-row table confirming both have molecular formula C₃H₆O.

Constitutional isomers usually have **different physical properties**
(boiling point, melting point, NMR spectra, logP) — which is why
distillation and chromatography work as separation techniques.

## Stereoisomers — different 3D arrangements

When two molecules share **both** the molecular formula AND the bond
connectivity, they're stereoisomers.  Two sub-types:

### Enantiomers — mirror images

**Lactic acid** has one stereocentre.  The (R) enantiomer
`C[C@H](O)C(=O)O` and the (S) enantiomer `C[C@@H](O)C(=O)O` are
non-superimposable mirror images.  Try it in the **Classify pair**
tab — you'll get the purple-coloured `enantiomer` verdict.

Enantiomers have **identical** physical properties EXCEPT for two
things:

1. **Opposite optical rotation** — equal magnitude, opposite sign.
   Pasteur measured this in 1848 with tartaric acid crystals.  See
   the glossary entry for **Optical activity**.
2. **Opposite biological activity** at chiral receptors.  One
   enantiomer of carvone smells like spearmint, the other like
   caraway.  L-DOPA treats Parkinson's; D-DOPA does nothing.  This is
   why the FDA increasingly approves single-enantiomer drugs (the
   "chiral switch" — see lesson 1's thalidomide history + the
   Phase-31k SSRI series with citalopram → escitalopram).

### Diastereomers — NOT mirror images

A molecule with **two or more stereocentres** has up to 2ⁿ
stereoisomers.  Pairs that aren't mirror images of each other are
diastereomers.  Try `C[C@H](O)[C@H](O)C(=O)O` and
`C[C@H](O)[C@@H](O)C(=O)O` (2,3-dihydroxybutanoic acid) — same
connectivity, different stereo at one centre, NOT mirror images →
purple `diastereomer` verdict.

The crucial pedagogical point: **diastereomers have different
physical properties** (unlike enantiomers).  This means you can
**separate** them by ordinary, non-chiral chromatography or
crystallisation — exploited heavily in classical resolution
strategies.

### Meso compounds — chiral atoms, achiral overall

**meso-tartaric acid** has two stereocentres but is superimposable on
its own mirror image because of an internal symmetry plane.  It's
optically inactive even though it contains stereocentres.  The
classifier dialog catches this in its `identical` branch: a meso
compound's mirror image canonicalises to the SAME SMILES as the
original.

## Conformers — single-bond rotation

**Conformers** are different 3D shapes a molecule adopts by rotating
around single bonds — no bonds break, so they interconvert freely
(milliseconds to picoseconds at room temperature).

Classic examples:

- **Butane** has anti / gauche / eclipsed conformers around the
  central C-C bond.
- **Cyclohexane** flips between two equivalent chair forms (and
  accessible boat / twist-boat states).
- **Proteins** continuously sample conformer ensembles around their
  backbone φ/ψ angles + side-chain χ angles.

Don't confuse conformers with stereoisomers — interconverting between
stereoisomers requires **breaking a bond**; interconverting between
conformers does not.  Drug-discovery scientists obsess about the
**bioactive conformer** — often a higher-energy conformer that the
receptor selectively binds — and use **conformational constraint**
(adding a ring, or restricting rotation with bulky groups) to lock
the molecule into the bioactive shape.

You've already met conformer dynamics in the **Tools → Conformational
Dynamics** workflow.  See the glossary entry for **Conformer**.

## Tautomers — proton-transfer isomers

**Tautomers** look like constitutional isomers (different
connectivity) but are special: they interconvert at ambient conditions
via a proton + double-bond shift.  At equilibrium they sit as a
mixture, with the position determined by thermodynamics + the
environment.

The textbook example: **acetone** in equilibrium with its enol form.

```
CH3-CO-CH3  ⇌  CH2=C(OH)-CH3
   (keto)         (enol)
```

Try it: paste `CC(=O)C` (keto acetone) and `CC(O)=C` (enol acetone)
into the **Classify pair** tab.  You'll get the orange `tautomer`
verdict.  At equilibrium acetone is > 99.9999% keto — but the tiny
enol fraction is what reacts in **aldol chemistry**, **alpha-
halogenation**, and the **Hell-Volhard-Zelinsky** reaction (see the
seeded reaction database).

Other classic tautomeric pairs:

- **Amide / iminol** — the amide-N-H and the imino-O-H forms;
  amide dominates massively for proteins.
- **Lactam / lactim** — the cyclic amide / iminol switch that
  drives the Watson-Crick base-pairing geometry of guanine + thymine
  + uracil + cytosine.
- **Ring / chain in sugars** — open-chain glucose ↔ α/β-cyclic
  hemiacetal anomers.  See the **Glossary tab → 'Mutarotation'**.

Try the **Tautomers** tab on `CC(=O)CC(=O)C` (2,4-pentanedione, the
acetylacetonate ligand precursor) — you should see ≥ 5 tautomers
because the central CH₂ is doubly-activated by the two carbonyls.

## Atropisomers — restricted-rotation enantiomers

A late-arriving member of the family: stereoisomers that arise from
**restricted rotation about a single bond**, usually a biaryl C-C
bond with bulky ortho substituents that raise the rotation barrier
high enough (≥ ~ 20 kcal/mol) for the two rotamers to be isolated as
discrete compounds.

The famous example: **BINAP** (2,2'-bis(diphenylphosphino)-1,1'-
binaphthyl).  Both atropisomers are stable; the (R) + (S) forms are
the chiral ligand for **Noyori asymmetric hydrogenation** (Nobel
2001).

The FDA classifies atropisomers as separate molecules requiring
separate regulatory approval — a pharmaceutical-development gotcha
for biaryl drugs (telmisartan, lesinurad, gefitinib all have
atropisomeric centres that had to be characterised + controlled in
manufacturing).

## Worked example: butenes

The C₄H₈ formula has four common isomers — work through them in the
**Classify pair** tab:

- `C=CCC` (1-butene) vs `CC=CC` (2-butene) → `constitutional` (different
  position of the double bond)
- `C/C=C/C` (E-2-butene) vs `C/C=C\C` (Z-2-butene) → `diastereomer`
  (geometric / cis-trans isomerism — see the glossary entry
  **Cis-trans isomerism**)
- `C=CCC` (1-butene) vs `C1CCC1` (cyclobutane) → `constitutional`
  (acyclic alkene vs ring)
- `C1CCC1` (cyclobutane) vs `CC1CC1` (methylcyclopropane) →
  `constitutional` (ring contraction)

Notice that **the same molecular formula is shared across all five**
— C₄H₈.  That's the defining feature of an isomer family.

## Practice

1. Open **Tools → Isomer relationships…** (`Ctrl+Shift+B`).
2. In the **Stereoisomers** tab, paste the SMILES for **D-glucose**
   from the molecule database (search by name with the agent's
   `find_molecule_by_name` action).  How many stereoisomers do you
   expect?  How many does the enumerator return?  Why might the two
   numbers differ (hint: anomers are tautomers, not stereoisomers).
3. In the **Tautomers** tab, paste `OC1=CC=NC=C1` (4-hydroxypyridine)
   and observe the tautomer / 4-pyridone result — a famously
   solvent-dependent tautomer pair.
4. Use the inline **View isomers…** button on the Molecule Workspace
   to jump from a seeded molecule directly into the dialog
   pre-filled.  The Phase-48d round-173 wiring auto-runs the
   stereoisomer enumeration so you see results immediately.
5. Read the Glossary entries for **Isomerism**, **Stereoisomer**,
   **Conformer**, **Tautomer**, **Atropisomer**, **Cis-trans
   isomerism**, and **Optical activity** (all added in round 170 as
   part of Phase 48a).

Next: **Aromaticity and electrophilic aromatic substitution** —
where the symmetry-driven tautomer rules of section 4 meet the
mechanism-driven substitution patterns of lesson 4.
