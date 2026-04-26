# Reading mass spectra for the beginner

Mass spectrometry (MS) measures the mass-to-charge ratio (m/z)
of ions. For organic chemistry, the most common variant is
**electron-impact (EI) MS** — the molecule is hit with a beam
of high-energy electrons, ionising it and frequently breaking it
into fragments. The resulting **fragment pattern** is a
diagnostic fingerprint.

## Anatomy of a mass spectrum

A bar chart of intensity (y-axis, % of largest peak called the
**base peak** = 100 %) vs **m/z** (x-axis). Three key
features:

1. **Molecular ion (M⁺)** — the intact, ionised molecule.
   m/z = molecular weight. Sometimes weak or absent if the
   molecule fragments easily.
2. **Fragment ions** — pieces resulting from bond cleavages.
   The strongest fragments correspond to the most stable
   cations (3° > 2° > 1°, allyl, benzyl).
3. **Isotope peaks (M+1, M+2)** — natural abundance of ¹³C
   (1.1 %), ³⁷Cl (24 %), ⁸¹Br (49 %) shows up as small +1 /
   +2 peaks. The M / M+2 intensity ratio is diagnostic for
   halogens.

## The nitrogen rule

A molecule with an **odd number of nitrogen atoms** has an
**odd molecular weight**. Useful for confirming N-content:
caffeine (C₈H₁₀N₄O₂, MW 194 — even, 4 N's) vs nicotine
(C₁₀H₁₄N₂, MW 162 — even, 2 N's) vs amphetamine (C₉H₁₃N,
MW 135 — odd, 1 N).

## Common neutral losses

| ΔM | Loss | Source |
|----|------|--------|
| -1 | H | aldehyde α-cleavage |
| -15 | CH₃ | methyl loss (common) |
| -17 | OH | alcohol, carboxylic acid |
| -18 | H₂O | alcohol dehydration |
| -27 | HCN | nitrile, aromatic amine |
| -28 | CO or C₂H₄ | aldehyde / ketone retro-Diels |
| -29 | CHO or C₂H₅ | aldehyde, ethyl loss |
| -31 | OCH₃ | methyl ester |
| -43 | CH₃CO or C₃H₇ | acetyl, propyl |
| -44 | CO₂ | carboxylic acid decarbonyl |
| -45 | COOH or OEt | carboxylic acid |
| -57 | C₄H₉ | tert-butyl |
| -77 | C₆H₅ | phenyl |

## Halogen patterns

The **M / M+2 intensity ratio** distinguishes halogens:

| Halogen | M : M+2 |
|---------|---------|
| Cl | 3 : 1 |
| Br | 1 : 1 |
| I | M only (no significant +2) |
| 2 × Cl | 9 : 6 : 1 (M : M+2 : M+4) |
| 2 × Br | 1 : 2 : 1 |

Spotting a 1:1 doublet ~ 2 mass units apart = strong evidence
for one Br.

## High-resolution MS (HRMS)

Modern instruments report m/z to 4-5 decimal places — the
**exact mass** of an ion. Comparing the measured exact mass to
all possible CHNOP / CHNOPS formulas within ± 5 ppm narrows
the molecular formula to typically 1-3 candidates.

## Worked example: acetone (CH₃COCH₃, MW 58)

Expected peaks:
- **m/z 58** — molecular ion (M⁺), often the base peak in
  small ketones.
- **m/z 43** — loss of CH₃ (M-15), gives acylium CH₃C≡O⁺
  (very stable, often base peak).
- **m/z 15** — methyl cation CH₃⁺.

The 43 / 58 ratio is so diagnostic that "acetone EI-MS" is one
of the textbook student-exercise spectra.

## Try it in the app

- **Tools → Spectroscopy → MS tab** → paste any SMILES → see
  predicted molecular ion + isotope pattern + common
  fragments. Try caffeine + acetone to compare a stable
  vs fragment-prone molecule.
- **Tools → HRMS guesser…** → enter a measured exact mass +
  ppm tolerance → ranked candidate molecular-formula table.
- **Glossary** → search for *Monoisotopic mass* +
  *Fragment ion*.

Next: **Lab safety basics**.
