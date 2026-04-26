# Lab notebook templates

A clean, consistent lab notebook is the difference between
reproducible chemistry + lost time. Three reusable
templates for routine entries.

## Template 1 — Reaction setup

```
Date: 2026-04-26
Notebook page: 142
Initials: JD
Project: SAR-1234 series
Target compound: 5b

REACTION:
[draw scheme with structures + reagents above arrow]

STOICHIOMETRY TABLE:
Reagent          MW       Mass    Vol     Mol    Eq   Source
SM (4-bromobenzoic) 201.0   100 mg  -       0.498  1.0  Sigma 11-2025
PhB(OH)₂            122.0   72 mg   -       0.589  1.18 Sigma
Pd(PPh₃)₄           1156    29 mg   -       0.025  0.05 Aldrich (degassed)
K₂CO₃ (anhyd)       138.2   137 mg  -       0.99   2.0  
DME (degassed)      -       -       3 mL    -      -    Anhyd Sigma
H₂O (degassed)      -       -       0.5 mL  -      -

PROCEDURE:
A 10-mL round-bottom flask with magnetic stir bar was
charged with 4-bromobenzoic acid (100 mg, 0.498 mmol, 1
eq), PhB(OH)₂ (72 mg, 0.589 mmol, 1.18 eq), Pd(PPh₃)₄ (29
mg, 0.025 mmol, 5 mol %), K₂CO₃ (137 mg, 0.99 mmol, 2 eq).
The flask was evacuated + backfilled with N₂ (× 3).
DME (3 mL) and degassed water (0.5 mL) were added. The
mixture was heated to 85 °C overnight (16 h) under N₂.

WORKUP:
Quenched with sat. NH₄Cl (10 mL); extracted with EtOAc
(3 × 10 mL); washed combined organics with brine;
dried over Na₂SO₄; concentrated.

PURIFICATION:
Flash silica column, hexane / EtOAc 95:5 → 80:20.

YIELD:
75 mg (74 %), white solid.

CHARACTERISATION:
TLC (Hex/EtOAc 4:1): Rf 0.35 (single spot, UV).
¹H NMR (400 MHz, CDCl₃): δ 8.16 (d, 2H), 7.65 (d, 2H),
7.62 (d, 2H), 7.46 (t, 2H), 7.40 (t, 1H).
HRMS: calcd 198.0681, found 198.0683.

NOTES:
- Used reagent-grade B(OH)₂; could try PinB version next time.
- Flask was glass with weak Al residue from earlier; wash next time.
- 16 h was overkill — tlc clean by 4 h.

NEXT STEP:
Try same protocol with 4-bromo-3-fluorobenzoic acid
(SAR-1234 series).
```

## Template 2 — Failed reaction debrief

```
Date: …
Page: …
Project + target: SAR-1234 / 5c

REACTION TRIED: [draw scheme]

CONDITIONS: [as above stoichiometry table]

OBSERVATIONS:
- T1 (15 min after addition): clear yellow solution.
- T2 (1 h): solution darkened to brown.
- T3 (overnight): dark heterogeneous mass.
- TLC at 4 h: streaky, multiple spots.

INTERPRETATION:
Pd black was visible by 1 h, suggesting catalyst death. 
Possible causes:
1. Substrate is electron-poor enough to coordinate Pd
   strongly + decompose it.
2. Insufficient ligand — go to Pd(OAc)₂ + 4 mol % Xphos
   instead.
3. Trace H₂O too much for the boronic ester variant —
   try anhydrous only.

NEXT TIME:
- Switch to Pd(OAc)₂ + XPhos (a la Buchwald table).
- Check substrate stability under base conditions
  (heat with K₂CO₃ alone — does it decompose?).
- Lower T to 65 °C.

LESSON FOR THE GROUP:
Add this substrate class to the "fragile substrates"
list. Check the lab Slack archive for prior issues.
```

## Template 3 — Spectra interpretation

```
Compound 5b
Date: 2026-04-26
Page: 142

¹H NMR (CDCl₃, 400 MHz):
- 8.16 (d, J = 8.4, 2H) → Ar-H ortho to COOH (downfield)
- 7.65 (d, J = 8.4, 2H) → Ar-H meta to COOH
- 7.62 (d, J = 7.6, 2H) → other ring's ortho-H
- 7.46 (t, J = 7.4, 2H) → meta-H
- 7.40 (t, J = 7.4, 1H) → para-H

Total H integration: 9H aromatic. COOH proton missing
(broad, exchanges in CDCl₃).

¹³C NMR (CDCl₃, 101 MHz):
- 172.4 (COOH)
- 145.7, 140.0, 129.4, 128.7, 128.4, 127.6, 127.1, 127.0
  (aromatic C's; 8 distinct signals consistent with
  unsymmetric biaryl)

IR (neat): 3100 br (COOH O-H), 1690 (C=O), 1610 (Ar
C=C), 1435.

HRMS (ESI): [M+H]+ calcd 199.0759, found 199.0761
(Δ = 1 ppm) C₁₃H₁₁O₂

INTERPRETATION:
Confirms 4-phenylbenzoic acid. All peaks accounted for;
no impurities visible.
```

## Other practical templates

- **Stock-solution log** — date prepared, concentration,
  storage, reagent batch.
- **Compound-tracking spreadsheet** — molecule ID,
  structure, mass, location (shelf, freezer, hood),
  hazard.
- **Failure log** — recurring issues to avoid.
- **Ordering log** — what's been ordered + when (avoids
  duplicate orders).

## Try it in the app

- **Tools → Drawing tool…** → sketch a reaction scheme
  to paste into your notebook.
- **Tools → Spectroscopy (IR / NMR / MS)…** → predict
  spectra to compare against your isolated compound.
- **Glossary** → search *Yield*, *Equivalents*,
  *Limiting reagent*, *NMR multiplicity*, *HRMS*,
  *pKa*, *Retrosynthesis*, *Imine*.

Next: **Career paths in organic chemistry**.
