# Spectroscopy: IR, NMR, and MS

A synthesis delivers something. Spectroscopy tells you **what**. In
modern organic chemistry, a claimed structure without four spectra (¹H
NMR, ¹³C NMR, IR, HRMS) doesn't get past peer review — and rightly so.
Each technique measures a different property; together they over-
determine the answer.

This lesson covers the four workhorse techniques and the order you use
them in practice. We'll lean on the app's **Phase 4 IR predictor**
(`predict_ir_bands(smiles)`) throughout.

## The structure-determination workflow

Given a product of unknown structure:

1. **Mass spectrum (MS)** — molecular formula from the M⁺ peak and
   isotope pattern. Fixes the atom count.
2. **IR** — functional groups present. ~1-minute scan.
3. **¹³C NMR** — carbon skeleton (count of distinct carbons, rough
   type).
4. **¹H NMR** — hydrogen environments, coupling patterns, integrations
   → connectivity.
5. **2D NMR** (COSY, HSQC, HMBC, NOESY) — through-bond and through-
   space connectivity to nail down ambiguities.

You rarely need all five — spectra are often over-determined. The goal
is just **enough** to rule out every alternative structure.

## Infrared (IR) — "what functional groups are here?"

IR measures vibrational transitions. Different bonds vibrate at different
frequencies, and different **functional groups** sit in predictable
**wavenumber** regions.

Open the tutor and ask:

> Predict the IR spectrum of acetic acid.

Under the hood this calls `predict_ir_bands(smiles="CC(=O)O")` — returns
the characteristic broad H-bonded O–H (2500–3300 cm⁻¹) and the sharp
C=O (1705–1720 cm⁻¹). You can also call `export_ir_spectrum` to save a
schematic PNG for a handout.

### Four bands worth memorising

| Wavenumber | Group | Diagnostic use |
|-----------|-------|----------------|
| 3200–3600 | O–H (alcohol, broad) | Sharp dilute / broad H-bonded |
| 2500–3300 | O–H (COOH dimer) | Unmistakable broad envelope |
| 1700 ± 30 | C=O | Very strong; split by class (aldehyde / ketone / ester / acid / amide) |
| 2200–2260 | C≡N | Sharp singleton, rare — diagnostic for nitrile |

### Things that rarely matter for teaching

- The "fingerprint region" (<1500 cm⁻¹) is where per-molecule vibrations
  live. Pattern-matching against a known library can identify a specific
  compound, but a student won't parse it manually.

## ¹H NMR — "how many kinds of H, in what environments?"

Three pieces of information per peak:

1. **Chemical shift** δ (ppm, relative to TMS). Set by the local
   electronic environment. Rule of thumb:
   - 0.5–1.5: alkyl (CH₃ / CH₂ / CH).
   - 1.5–3: allyl, benzyl, α-to-carbonyl.
   - 3–5: X-CH₂ where X = O / N / Cl / Br.
   - 5–7: alkene H.
   - 6.5–8.5: aromatic H.
   - 9–10: aldehyde H (only!).
   - 10–13: carboxylic acid O-H (exchangeable).
2. **Integration** — area under the peak ∝ number of H. Always given
   relative (2:3:1 etc.), never absolute.
3. **Coupling** — J (Hz) — interaction with neighbouring H. A peak with
   `n` neighbouring H splits into `n+1` lines (the n+1 rule). Aromatic
   H-H coupling: 7–9 Hz ortho, 2–3 Hz meta, ~0 para. Alkene: 16–18 Hz
   trans, 7–10 Hz cis.

### Worked example — ethyl acetate (`CCOC(=O)C`)

Predict the spectrum:

- 2.0 ppm, 3H, singlet — CH₃ attached to C=O (no neighbours with H).
- 1.3 ppm, 3H, triplet — CH₃ of ethyl (2 neighbours from CH₂).
- 4.1 ppm, 2H, quartet — OCH₂ (3 neighbours from CH₃, plus deshielded
  by adjacent O).

Three signals, ratio 3:3:2, two of them split — classic "ethyl ester"
fingerprint. When you see this on an exam, it's ethyl ester or
ethoxide.

### Worked example — the tutor can predict it too

Ask the tutor:

> What's the ¹H NMR of methyl benzoate?

Expected: four peaks. Aromatic-H region integrating to 5 (for the
monosubstituted benzene ring — ortho-H 7.95 ppm dd 2H, meta-H 7.45 ppm
t 2H, para-H 7.55 ppm t 1H), plus 3.90 ppm singlet 3H for the OMe.

(The prediction tool is a future Phase-4 extension; for now manual
analysis or commercial software.)

## ¹³C NMR — "how many different carbons?"

¹³C NMR is simpler (usually). Key features:

- **Decoupled spectra** (the default) — each carbon gives a singlet.
- Chemical-shift ranges roughly 10× bigger than ¹H:
  - 0–50 ppm: sp³ alkyl.
  - 50–100 ppm: sp³ next to O / N.
  - 100–150 ppm: alkene, aromatic.
  - 150–210 ppm: carbonyl (C=O).
- Integrations are **not reliable** — T₁ relaxation differs per carbon.
  Use ¹³C to count *kinds* of C, not quantities.

### How it confirms structure

The number of ¹³C peaks tells you how many *non-equivalent* carbons
the molecule has. Symmetric molecules show fewer peaks than atoms:

- Benzene has 6 carbons, **1** ¹³C peak (all equivalent, C₆ symmetry).
- Para-xylene has 8 C, **3** peaks (by symmetry: CH₃, quaternary-C,
  ring-CH).
- A chiral molecule shows **every** carbon — good counting check.

## Mass spectrometry — "what's the molecular formula?"

Mass spec ionises the molecule and weighs it. Three pieces of info:

1. **M⁺** — molecular ion peak. Gives the molecular weight.
2. **Isotope pattern** — relative heights of M⁺, M+1, M+2. Diagnostic
   for halogens (Cl: 3:1 M/M+2; Br: 1:1 M/M+2; S: M+2 contribution),
   and for C-count (M+1 is ~1.1% × n_carbons from ¹³C).
3. **Fragmentation** — M⁺ breaks at weak bonds. Each fragment is a
   substructure clue.

### HRMS — high-resolution mass spec

A normal MS reports nominal mass (integer); HRMS reports to 3 decimal
places (10⁻⁴ Da). That resolution distinguishes `C₆H₁₂O`
(mass 100.0888) from `C₅H₈O₂` (100.0524). The **molecular formula is
uniquely determined** by a matched HRMS.

## Putting it together: a worked problem

Suppose you ran an unknown and collected:

- MS: M⁺ = 102, no Cl/Br isotope pattern.
- IR: strong at 1735 cm⁻¹, moderate at 1150 cm⁻¹.
- ¹H NMR: singlet 3H at 2.0 ppm, triplet 3H at 1.3 ppm, quartet 2H at
  4.1 ppm.
- ¹³C NMR: 4 peaks.

Working through:

1. M⁺ 102. Likely formula: C₄H₁₀O, C₄H₆O₂, C₅H₁₀O₂. Compute degrees of
   unsaturation = (2×4 − 10 + 2)/2 = 0 (if C₄H₁₀O₂) vs 1 (for C₄H₆O₂)
   vs 1 (for C₅H₁₀O₂). IR 1735 → has C=O, so ≥ 1 unsaturation.
2. IR 1735: ester C=O. IR 1150: C–O stretch.
3. ¹H NMR: 3-signal ratio 3:3:2 with quartet/triplet pair — ethyl
   group. Singlet 3H 2.0 ppm — CH₃-CO-. Put them together: CH₃-CO-O-
   CH₂-CH₃ = ethyl acetate. Molecular formula C₄H₈O₂, MW 88.
4. But MW 88 ≠ 102! Re-check: could it be methyl propionate (MW 88)?
   No, that's also 88. Methyl butanoate is 102. Butyric acid is 88.
   Hmm — the IR + NMR evidence points to ethyl acetate (MW 88),
   but the MS says 102. **The MS is wrong**: the given M⁺ = 102 is
   inconsistent with the other data. In a real experiment, check for
   M-CH₃ losses (common), or an M+H adduct (ethyl acetate + NH₄⁺ ≈ 106).

That final reality check is the whole point: each technique over-
determines the answer. If IR + NMR agree on ethyl acetate, the MS
reading is an artefact; don't trust a single spectrum that contradicts
three others.

## Practice

1. In the Molecule Workspace load **Aspirin**, **Caffeine**, **Ethyl
   acetate**, and **Benzonitrile**. Ask the tutor to predict the IR
   for each — or call `predict_ir_bands(smiles=...)` directly.
2. Load **Methyl benzoate** (`COC(=O)c1ccccc1`) and predict its ¹H NMR
   mentally. Check against a spectral database.
3. Read the **Glossary** entries for NMR spectroscopy, Chemical shift,
   and IR spectroscopy (Glossary tab).
4. A Phase 4 extension will ship NMR and MS predictors in future
   sessions — check `PROJECT_STATUS.md` for progress.

## Further reading

- Silverstein, Webster, Kiemle, *Spectrometric Identification of
  Organic Compounds* (8th ed.). The standard undergraduate text.
- Pretsch, Bühlmann, Badertscher, *Structure Determination of Organic
  Compounds* (5th ed.). Tabulated shift / coupling data.
- NIST Chemistry WebBook — free IR, MS, and UV-Vis spectra for
  >70,000 compounds (https://webbook.nist.gov/chemistry).

Next: the **Graduate** tier begins with **Named reactions library** —
a curated tour of the 50-ish named reactions every postdoc knows by
heart.
