# Reading ¹H NMR for the beginner

¹H NMR (proton nuclear magnetic resonance) is the **single most-
used analytical technique in organic chemistry**. Every paper
showing a new molecule includes its ¹H NMR. This lesson teaches
you to read one without doing any quantum mechanics.

## What an ¹H NMR spectrum is

A plot of signal intensity vs **chemical shift** (δ, in ppm,
left-to-right axis runs HIGH ppm to LOW ppm — opposite of normal
plots). Every distinct H environment in the molecule gives a
**peak** at a position determined by its electronic surroundings.

You read three things from each peak:

1. **Chemical shift (δ, ppm)** — *what kind of H* it is.
2. **Integration** (area under the peak) — *how many H's*.
3. **Multiplicity** (how the peak is split) — *how many H's*
   on the **adjacent** carbons.

## Chemical shift map

| δ (ppm) | Hydrogen type |
|---------|---------------|
| 0-1 | sp³ CH near nothing (TMS reference at 0) |
| 0.7-1.5 | alkyl CH₃, CH₂ |
| 1.5-2.5 | allylic / α to carbonyl CH |
| 2.5-3.5 | next to electronegative atom (Cl, N) |
| 3.5-4.5 | next to O (alcohols, ethers, esters) |
| 5-7 | vinyl (alkene) H |
| 6.5-8 | aromatic H |
| 9-10 | aldehyde H |
| 10-13 | carboxylic acid H |

Quick mnemonic: **electronegative neighbours pull H's downfield**
(higher ppm). H's near electron-rich groups stay upfield.

## Multiplicity (n+1 rule)

A peak split into **n+1 lines** indicates **n** H's on the
adjacent carbon(s):

- 1 line (singlet, *s*) → no adjacent H
- 2 lines (doublet, *d*) → 1 adjacent H
- 3 lines (triplet, *t*) → 2 adjacent H's
- 4 lines (quartet, *q*) → 3 adjacent H's
- 5 lines (pentet) → 4 adjacent H's
- many lines (multiplet, *m*) → complex coupling

The **coupling constant** *J* (in Hz) tells you how the
adjacent H is connected (3-bond couplings are typical, 6-8 Hz
for sp³–sp³, 10-18 Hz for trans-vinyl, 6-12 Hz for cis-vinyl).

## Worked example: ethanol (CH₃CH₂OH)

Three distinct H environments:
- CH₃ at ~ 1.2 ppm, **triplet** (couples to 2 CH₂ H's), 3H
  integration.
- CH₂ at ~ 3.6 ppm, **quartet** (couples to 3 CH₃ H's), 2H.
- OH at ~ 2.5 ppm (concentration- + temperature-dependent;
  often a broad singlet), 1H.

Total H count = 3 + 2 + 1 = 6, matching C₂H₆O.

## Common pitfalls

- **OH and NH peaks shift with concentration + temperature** —
  often broad + can swap with D₂O when shaken. The **D₂O
  shake** test confirms an exchangeable proton.
- **Aromatic ring para-substituents** give the diagnostic
  AA'BB' pattern (looks like 4 lines but is actually a
  complex spin system).
- **Solvent residual peaks** show up — CDCl₃ at 7.26 ppm,
  DMSO-d₆ at 2.50 ppm, MeOD at 3.31 + 4.87 ppm. Memorise
  the common ones.

## Try it in the app

- **Tools → Spectroscopy** → NMR tab → paste a SMILES + click
  *Predict* → see predicted ¹H peaks with environment labels.
  Try `CCO` (ethanol) first to verify against the worked
  example above.
- Try **Caffeine** + **Aspirin** to see real-drug spectra.
- **Glossary tab** → search for *Coupling constant (J)* +
  *Chemical shift* for the formal definitions.

Next: **Reading IR spectra for the beginner**.
