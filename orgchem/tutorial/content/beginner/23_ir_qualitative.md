# Reading IR spectra for the beginner

Infrared spectroscopy probes molecular vibrations. Each
**functional group** absorbs IR light at a characteristic
frequency, so an IR spectrum is essentially a **fingerprint of
which functional groups are present** in your molecule. Cheap,
fast, and a great first-pass check after running a reaction.

## What an IR spectrum is

A plot of % transmittance (y-axis) vs **wavenumber** (x-axis,
usually 4000-400 cm⁻¹, plotted **right-to-left** so high cm⁻¹
sits on the left). Each absorption shows up as a **dip** —
percent transmittance drops where the molecule absorbs IR
photons matching a vibrational frequency.

## The four IR regions

| Region (cm⁻¹) | What's there |
|---------------|--------------|
| 4000-2500 | **X–H stretches** (O–H, N–H, C–H sp/sp²/sp³) |
| 2500-2000 | **triple-bond stretches** (C≡C, C≡N) |
| 2000-1500 | **double-bond stretches** (C=O, C=C, C=N) |
| 1500-400 | **fingerprint region** — single-bond stretches, bends, rings |

The **C=O stretch** in the double-bond region is the single
most diagnostic IR band — different carbonyl types absorb at
different wavenumbers (see table below).

## Diagnostic bands — the short version

| Functional group | Stretch (cm⁻¹) | Notes |
|------------------|----------------|-------|
| Free O–H (alcohol, phenol) | 3550-3650 (sharp) | dilute solution |
| H-bonded O–H | 3200-3550 (broad) | concentrated, neat |
| O–H of carboxylic acid | 2500-3300 (very broad) | acid-dimer pattern |
| N–H amine (1°) | 3300-3500 (two peaks) | symmetric + asymmetric |
| N–H amine (2°) | 3300-3500 (one peak) | |
| Amide N–H | 3100-3500 | broader |
| C–H sp³ | 2850-3000 (medium) | the alkane fingerprint |
| C–H sp² | 3000-3100 (medium) | aromatic + vinyl |
| C–H sp (alkyne) | 3300 (sharp) | terminal alkyne only |
| C≡C alkyne | 2100-2260 (weak) | terminal stronger than internal |
| C≡N nitrile | 2200-2260 (sharp, medium) | |
| C=O carbonyl | 1650-1820 | sub-ranges below |
| C=C alkene | 1620-1680 (weak) | |
| C=C aromatic | 1450-1620 (multiple) | |

## Carbonyl sub-ranges (memorise these)

| Carbonyl type | Stretch (cm⁻¹) |
|---------------|----------------|
| Acid chloride | 1790-1815 |
| Anhydride | 1750 + 1820 (two peaks) |
| Ester | 1735-1750 |
| Aldehyde | 1720-1740 |
| Ketone | 1705-1720 |
| Carboxylic acid | 1700-1725 |
| Amide | 1630-1690 |
| α,β-unsaturated carbonyl | drop ~ 30 cm⁻¹ from saturated |

The order **acid chloride > anhydride > ester > aldehyde >
ketone > acid > amide** comes from a tug-of-war between
inductive electron withdrawal (raises stretch) and resonance
donation (lowers stretch).

## Worked example: acetone (CH₃COCH₃)

Expected major bands:
- **C=O ketone** at ~ 1715 cm⁻¹ (strong, sharp).
- **C–H sp³** at 2900-3000 cm⁻¹ (medium, methyl groups).
- **fingerprint** at 1200-1400 cm⁻¹ (C–C, C=O bends).

What you would NOT see:
- Any O–H or N–H peaks (no protic groups).
- Any C=C or aromatic peaks (no double bonds beyond carbonyl).
- Any sp² or sp C–H (no alkenes or alkynes).

## Try it in the app

- **Tools → Spectroscopy** → IR tab → paste any SMILES + click
  *Predict bands* → see a labelled IR sketch with the
  diagnostic stretches identified.
- Compare **acetone** (CC(=O)C) vs **acetic acid** (CC(=O)O) —
  the C=O is at slightly different wavenumber + the acid has
  a huge broad O–H peak the ketone lacks.
- **Tools → Lab reagents…** → most reagent reference cards
  list the molecule's diagnostic IR bands in the *notes*
  field.

Next: **Reading mass spectra for the beginner**.
