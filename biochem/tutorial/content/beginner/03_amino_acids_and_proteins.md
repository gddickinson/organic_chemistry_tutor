# Amino acids and proteins

Proteins are the workhorses of biology.  Almost everything
a cell does — catalyse reactions, build structures,
generate movement, transmit signals, defend against
pathogens — is done by proteins.

## The 20 standard amino acids

Every protein is a chain of amino acids drawn from a
20-residue alphabet:

| Class | Examples |
|-------|----------|
| Hydrophobic aliphatic | Gly, Ala, Val, Leu, Ile, Met, Pro |
| Hydrophobic aromatic | Phe, Trp, Tyr |
| Polar uncharged | Ser, Thr, Cys, Asn, Gln |
| Acidic (-) | Asp, Glu |
| Basic (+) | Lys, Arg, His |

Each amino acid has the same backbone:

```
      H   R    O
       \  |   ‖
   H₂N — Cα — C — OH
            |
            H
```

with a unique side chain (R group) at the α-carbon.  The
side chain determines:

- **Hydrophobicity** — drives folding (hydrophobic core,
  hydrophilic surface).
- **Charge** — at physiological pH, Asp/Glu are
  negative, Lys/Arg/His positive.
- **Reactivity** — Cys thiols form disulfide bonds; Ser/
  Thr/Tyr hydroxyls are phosphorylation targets.

20 standard + 2 occasional (selenocysteine, pyrrolysine)
= 22.  Plus dozens of post-translationally modified
variants (phosphorylated, methylated, acetylated,
ubiquitinated, glycosylated, hydroxylated).

## The peptide bond

Amino acids polymerise via dehydration condensation: the
α-carboxyl of one + the α-amino of the next → peptide
bond + water.

The peptide bond is **planar** + has partial double-bond
character (resonance between C=O lone pair on N + C-N
bond).  This planarity restricts the protein backbone to
two adjustable dihedral angles per residue: φ (phi, N-Cα)
and ψ (psi, Cα-C).

The Ramachandran plot shows the allowed φ-ψ combinations.
α-helix + β-sheet conformations occupy the densely-
populated regions.

## The four levels of protein structure

### Primary

The amino-acid sequence: a string of one-letter codes
(MAGEDFG…) read N-terminus → C-terminus.

Sequence determines structure (Anfinsen 1973 Nobel —
ribonuclease A refolds spontaneously to its native state
in vitro).

### Secondary

Local backbone-hydrogen-bond patterns:

- **α-helix** — right-handed helix, 3.6 residues per
  turn, ~ 5.4 Å pitch.  Backbone H-bond from C=O of
  residue *i* to N-H of residue *i+4*.
- **β-sheet** — extended strands held together by inter-
  strand H-bonds; can be parallel or antiparallel.
- **Turns** — short (3-5 residue) segments connecting
  helices + strands.
- **Loops** — longer connecting segments without regular
  H-bonding.

Pauling + Corey predicted the α-helix + β-sheet from
peptide-bond geometry in 1951 — before any experimental
protein structure was known.

### Tertiary

The overall 3D fold of a single polypeptide chain.
Stabilised by:

- **Hydrophobic effect** — the dominant driving force.
  Burial of hydrophobic side chains away from water.
- **Hydrogen bonds** — between polar side chains.
- **Salt bridges** — between oppositely-charged side
  chains.
- **Disulfide bonds** — covalent S-S between two Cys
  residues; common in secreted proteins.
- **Van der Waals contacts** — short-range packing.

Folds are catalogued in databases (CATH, SCOP, ECOD)
into ~ 1000 distinct topology classes.

### Quaternary

Assembly of multiple subunits.  Examples:

- Hemoglobin: α₂β₂ tetramer.
- Insulin receptor: α₂β₂ heterotetramer (disulfide-
  linked).
- 20S proteasome: α₇β₇β₇α₇.
- Bacterial ribosome: 50S + 30S → 70S.
- Viral capsids: massive icosahedral assemblies.

## How proteins fold

Folding is fast (microseconds-seconds) + reproducible.
Anfinsen's principle: the native state is the
thermodynamic minimum of the polypeptide's free-energy
landscape.

In cells, **chaperones** help difficult folds:

- **Hsp70** family (HSPA1, BiP) — bind nascent +
  unfolded polypeptides via hydrophobic patches; ATP-
  dependent.
- **Hsp60 / GroEL-GroES** — barrel-shaped chaperonin
  that encloses unfolded protein in a hydrophilic
  cavity for folding.
- **Hsp90** — folds signalling clients (kinases, steroid
  receptors).
- **Calnexin / calreticulin** — ER glycoprotein-folding
  quality control.

Misfolding causes disease: α-synuclein in Parkinson's,
amyloid-β in Alzheimer's, prion proteins, CFTR-ΔF508 in
cystic fibrosis.  AlphaFold (DeepMind, 2020-2024) +
RoseTTAFold solved the protein-structure-prediction
problem for nearly all known sequences — see the graduate
"Enzyme engineering" lesson.

## Try it in the app

- **Window → Macromolecules → Proteins** (Ctrl+Shift+M) —
  the seeded protein-structure catalogue.
- **Window → Biochem Studio → Enzymes** — every enzyme
  entry is itself a protein with primary → quaternary
  structure.

Next: **Enzymes — the basics**.
