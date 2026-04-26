# Common spectroscopy unit conversions

Spectroscopists use different units for different methods.
Memorise the conversions to avoid embarrassing factor-of-100
mistakes.

## Wavelength + frequency + wavenumber

```
ν = c / λ            (frequency = speed of light / wavelength)
ν̃ = 1 / λ           (wavenumber)
E = h ν = h c / λ = h c ν̃
```

| What | Symbol | Unit | Domain |
|------|--------|------|--------|
| Wavelength | λ | nm or µm | UV-Vis, IR |
| Frequency | ν | Hz | NMR, microwave |
| Wavenumber | ν̃ | cm⁻¹ | IR, Raman |
| Energy | E | eV, kJ/mol, kcal/mol | photochemistry |

### Conversions

```
1 µm = 1000 nm
1 µm wavelength → 10 000 cm⁻¹ wavenumber (1 / 0.0001 cm)
500 nm wavelength → 20 000 cm⁻¹ → 2.48 eV → 240 kJ/mol
```

Quick numbers:

- **UV** 200-400 nm = 50 000-25 000 cm⁻¹ = 6.2-3.1 eV
- **Visible** 400-700 nm = 25 000-14 000 cm⁻¹ = 3.1-1.8 eV
- **IR** 4000-400 cm⁻¹ = 2.5-25 µm = 0.5-0.05 eV

## NMR — chemical shift

```
δ (ppm) = (ν_sample - ν_reference) / ν_spectrometer × 10⁶
```

Reference: TMS at 0 ppm for ¹H + ¹³C; CFCl₃ at 0 ppm for
¹⁹F; H₃PO₄ at 0 ppm for ³¹P.

A 500 MHz spectrometer means proton Larmor frequency at
500 MHz at the field used (11.74 T). At higher field
(800 MHz, 18.8 T), absolute frequency separations grow but
δ in ppm stays the same — that's the whole point of ppm.

## NMR — coupling constant

J in **Hz**, NOT ppm. Independent of B₀ — same J value at
500 MHz + 800 MHz spectrometer. Typical:

- ³J(H-H) vicinal: 0-12 Hz.
- ²J(H-H) geminal: -10 to -18 Hz.
- ³J(H-C-O-H): 4-8 Hz.
- ¹J(C-H): 125-250 Hz.
- ¹J(¹⁹F-¹H): 40-50 Hz.

## IR — transmittance + absorbance

- **% Transmittance** = I / I_0 × 100. The y-axis on most
  IR spectra. Bands point DOWN.
- **Absorbance** A = log₁₀ (I_0 / I). Linear in
  concentration (Beer-Lambert).

Convert: A = log₁₀ (100 / %T). %T = 10 → A = 1.

## UV-Vis — extinction coefficient

```
A = ε × l × c            (Beer-Lambert)
```

ε in L mol⁻¹ cm⁻¹ (M⁻¹ cm⁻¹). Units of c in mol/L; l in cm.

Typical π → π* in conjugated dye: ε ~ 10⁴-10⁵ M⁻¹ cm⁻¹.
Typical n → π* in carbonyl: ε ~ 100 M⁻¹ cm⁻¹ (forbidden,
weak).

For protein quantitation: A_280 / 1.0 = ~ 1 mg/mL of typical
protein (varies with Trp + Tyr content).

## Mass spec — m/z + ppm error

```
ppm error = (m_observed - m_calculated) / m_calculated × 10⁶
```

Routine HRMS quotes < 5 ppm. So at m/z = 200, ± 0.001 Da.
At m/z = 1000, ± 0.005 Da.

Resolving power R = m / Δm at FWHM. R = 100 000 means
distinguishing two peaks 0.001 Da apart at m/z = 100.

## Try it in the app

- **Tools → Spectroscopy (IR / NMR / MS)…** → all three
  panels show predicted spectra in standard units.
- **Tools → HRMS Guesser…** → input mass + ppm tolerance
  → ranked formula candidates.
- **Glossary** → search *Wavenumber*, *Chemical shift*,
  *Coupling constant*, *Beer-Lambert*, *Extinction
  coefficient*, *ppm*.

Next: **Electronic structure of atoms (Aufbau in detail)**.
