# Amino acid + peptide chemistry

The 20 standard amino acids are the alphabet of proteins.
This lesson covers their chemistry: structures + side-chain
classes + zwitterions + isoelectric points + how to make a
peptide bond.

## Structure + the 20 standard amino acids

Each amino acid has a central α-carbon bonded to:

- An amino group (-NH₂)
- A carboxyl group (-COOH)
- A hydrogen (-H)
- A variable side chain (-R)

All except glycine (R = H) are chiral; in nature only the
**L-isomer** (S configuration except cysteine) is
incorporated into proteins.

### Side-chain classes

| Class | Members | Property |
|-------|---------|----------|
| **Non-polar aliphatic** | Gly, Ala, Val, Leu, Ile, Pro, Met | Hydrophobic; protein interior |
| **Aromatic** | Phe, Tyr, Trp | Hydrophobic + UV-active (280 nm absorbance for protein quantification) |
| **Polar uncharged** | Ser, Thr, Cys, Asn, Gln | Form H-bonds; surface; Cys can disulfide-bridge |
| **Positively charged (basic)** | Lys, Arg, His | Salt bridges; binding to anions, DNA, RNA |
| **Negatively charged (acidic)** | Asp, Glu | Salt bridges; metal coordination; catalysis |

### Three-letter + one-letter codes

| Name | 3-letter | 1-letter | Notes |
|------|----------|----------|-------|
| Glycine | Gly | G | smallest |
| Alanine | Ala | A | |
| Valine | Val | V | branched |
| Leucine | Leu | L | branched |
| Isoleucine | Ile | I | branched, two stereocentres |
| Proline | Pro | P | imino acid; rigid Φ angle |
| Phenylalanine | Phe | F | aromatic |
| Tyrosine | Tyr | Y | aromatic + OH |
| Tryptophan | Trp | W | indole; fluorescent |
| Methionine | Met | M | thioether; S-CH₃ |
| Serine | Ser | S | OH; phosphorylation site |
| Threonine | Thr | T | OH + Me; phosphorylation site |
| Cysteine | Cys | C | SH; forms disulfides |
| Asparagine | Asn | N | amide |
| Glutamine | Gln | Q | amide |
| Lysine | Lys | K | terminal NH₃⁺; pKa 10.5 |
| Arginine | Arg | R | guanidinium; pKa ~ 12 |
| Histidine | His | H | imidazole; pKa 6 |
| Aspartate | Asp | D | COO⁻; pKa 3.7 |
| Glutamate | Glu | E | COO⁻; pKa 4.1 |

## Zwitterions + isoelectric point

At physiological pH (~ 7.4) every standard amino acid is a
**zwitterion** — both NH₃⁺ + COO⁻ ionised. Net charge
depends on side-chain ionisations + the pH.

The **isoelectric point (pI)** is the pH where the molecule
has zero net charge:

```
For a non-ionic side chain:   pI = (pKa(COOH) + pKa(NH₃⁺)) / 2
For an acidic side chain:     pI = (pKa(COOH) + pKa(side R)) / 2
For a basic side chain:       pI = (pKa(side R) + pKa(NH₃⁺)) / 2

Glycine: pKa(COOH) = 2.34, pKa(NH₃⁺) = 9.60 → pI = 5.97
Aspartate: pI = 2.77 (acidic side chain)
Lysine: pI = 9.74 (basic side chain)
```

pI matters in chromatography: at pH = pI, an amino acid /
protein is least soluble + doesn't migrate in an electric
field (used in isoelectric focusing).

## Synthesis of amino acids

### Strecker synthesis

```
RCHO + NH₃ + HCN → R-CH(NH₂)-CN → (hydrolysis) → R-CH(NH₂)-COOH
```

Gives racemic amino acids. Modern asymmetric variants use
chiral auxiliaries (Ellman, Davis sulfinamides) or
asymmetric catalysis.

### Gabriel + diethyl aminomalonate routes

Phthalimide alkylation gives masked amino groups; diethyl
aminomalonate chemistry (Sorensen) builds AAs from alkyl
halides + condensation.

### Asymmetric hydrogenation of dehydroamino acids

```
Ph-CH=C(NHAc)-COOH + H₂ + Rh-DIPAMP → (S)-Phenylalanine derivatives
                                     ee > 95 %
```

Knowles's L-DOPA process. Industrial scale for unnatural
+ deuterated AAs.

### Biocatalytic / fermentation

L-amino acids made commercially (kt/yr) by bacterial
fermentation: L-glutamate, L-lysine. Most cost-effective.

## Peptide bond formation — the synthesis problem

A peptide bond is an amide between α-COOH of one AA and
α-NH₂ of the next. The challenge:

- Each AA has a reactive COOH AND NH₂.
- Coupling them indiscriminately gives polymers.
- Solution: **protect** the NH₂ of one AA, the COOH of the
  other, **activate** the free COOH, couple, then
  deprotect for next coupling.

The basic cycle:

```
Boc-AA₁-OH + HCl·H₂N-AA₂-OBn  +  EDC / HOBt
              → Boc-AA₁-AA₂-OBn  → (TFA) → H₂N-AA₁-AA₂-OBn → repeat
```

For long peptides, use **solid-phase peptide synthesis
(SPPS)** — covered in the advanced curriculum.

## Common modifications

- **Phosphorylation** — Ser / Thr / Tyr OH → phosphate by
  kinases. Reversible by phosphatases.
- **Acetylation** — Lys NH₂ → acetamide by HATs. Removed by
  HDACs.
- **Methylation** — Lys NH₂ → mono / di / tri-methyl. Marks
  histones for chromatin states.
- **Glycosylation** — Asn (N-linked) or Ser/Thr (O-linked)
  + sugar.
- **Disulfide bridges** — Cys-SH + Cys-SH → Cys-S-S-Cys.
  Stabilise extracellular proteins (insulin, antibodies).

## Try it in the app

- **Proteins tab** → fetch any seeded PDB → see the AA
  sequence + 3D fold.
- **Reactions tab** → load *Met-enkephalin via Fmoc SPPS
  5-step* — see a full peptide synthesis.
- **Carbohydrates tab** → glucose for context (sugar +
  amino sugar like GlcNAc).
- **Glossary** → search *Amino acid*, *Zwitterion*,
  *Isoelectric point*, *Peptide bond*, *SPPS*.

Next: **Lipid chemistry — fatty acids, glycerides,
phospholipids**.
