# Mössbauer spectroscopy

**Mössbauer spectroscopy** measures recoilless nuclear γ-ray
absorption + emission. It reports the nuclear environment
of a few specific isotopes (most importantly **⁵⁷Fe**) +
gives unique fingerprints of oxidation state, spin state,
+ ligand field.

## How it works

The Mössbauer effect: when a γ-ray nucleus is in a solid
matrix, it can absorb / emit photons **without recoiling**
(the whole crystal absorbs the recoil momentum).

```
source: ⁵⁷Co (β-decays to ⁵⁷Fe in excited state) →
        ⁵⁷Fe* + 14.4 keV γ-ray
sample: ⁵⁷Fe (in compound) absorbs γ-ray → resonance
```

Source is moved at velocities mm/s relative to sample;
Doppler shift fine-tunes γ-ray energy across the nuclear
transition. Plot transmission vs velocity → spectrum.

## What's measured

### Isomer shift δ (mm/s)

Reflects s-electron density at the nucleus:

- **Fe(II) high-spin (HS, S=2)**: δ ≈ 1.2-1.5
- **Fe(II) low-spin (LS, S=0)**: δ ≈ 0.4-0.5
- **Fe(III) HS (S=5/2)**: δ ≈ 0.3-0.5
- **Fe(III) LS (S=1/2)**: δ ≈ 0.0-0.3
- **Fe(IV)**: δ ≈ -0.1 to 0.1
- **Fe(V), Fe(VI)** (very rare): δ < -0.5

A single number tells you Fe oxidation + spin state.

### Quadrupole splitting ΔE_Q (mm/s)

Nuclear quadrupole interacts with the electric field
gradient at the nucleus. ΔE_Q ranges ~ 0-3 mm/s.

- Symmetric site → ΔE_Q ≈ 0.
- Asymmetric site → larger ΔE_Q.
- HS Fe(II) shows extreme ΔE_Q (~ 2-3 mm/s).

### Magnetic hyperfine field (B_int)

If the iron centre is in a magnetic environment (Fe-O bond
+ d-electrons unpaired), the nuclear levels split into 6
lines (Zeeman splitting):

```
6-line pattern: ferromagnetic / antiferromagnetic
  (~ 33 T at the nucleus for α-Fe)
```

Used to distinguish:

- α-Fe (metallic) — 33 T.
- Magnetite Fe₃O₄ — 50 T at A-site, 46 T at B-site.
- Hematite α-Fe₂O₃ — 53 T.
- Goethite α-FeOOH — 38 T at low T (paramagnetic above
  Néel T).

Mineralogists + corrosion engineers love Mössbauer for
distinguishing iron oxide phases.

## Other Mössbauer-active nuclei

| Isotope | Energy (keV) | Common use |
|---------|--------------|------------|
| ⁵⁷Fe | 14.4 | most common; iron chemistry |
| ¹¹⁹Sn | 23.9 | tin oxidation states + bonding |
| ¹⁵¹Eu | 21.5 | rare earth chemistry |
| ¹²⁹I | 27.8 | iodine chemistry |
| ¹⁹⁷Au | 77.3 | gold catalysis |
| ⁹⁹Ru | 89.4 | ruthenium |
| ⁶¹Ni | 67.4 | nickel oxidation states |
| ¹⁹³Ir | 73.0 | iridium chemistry |

⁵⁷Fe is by far the most accessible (¹/³⁷ natural
abundance; ⁵⁷Co source readily available, ~ 270-day half-
life).

## Applications

### Iron-containing biomolecules

- **Heme proteins** (haemoglobin, myoglobin, cytochromes)
  — distinguish Fe(II) vs Fe(III) vs HS vs LS.
- **Iron-sulfur clusters** ([2Fe-2S], [4Fe-4S]) — track
  oxidation state changes during catalysis (nitrogenase,
  hydrogenase, photosystem I).
- **Non-heme iron enzymes** (taurine dioxygenase, IPNS) —
  characterise reaction intermediates.

### Industrial catalysis

- **Ammonia synthesis (Haber)** — characterise Fe / FeO /
  iron carbide species.
- **Fischer-Tropsch** — Fe carbides during CO hydrogenation.
- **Iron oxide catalysts** — water-gas-shift, Claus
  process (S removal).

### Materials + minerals

- Phase identification in iron oxides (rust products,
  meteorites).
- Battery electrodes (LiFePO₄ cathode chemistry tracked by
  ⁵⁷Fe Mössbauer).
- Glass + ceramic Fe-containing minerals.

## Limits

- **Specific to a few nuclei** — most elements not
  accessible.
- **Specialised equipment** — γ-source + cryo-cooler;
  facility-scale.
- **Solid-state only** — needs solid sample; frozen
  solutions sometimes work.
- **Linewidth** ~ 0.1 mm/s; can't always resolve closely
  related Fe sites.

## Try it in the app

- **Tools → Lab analysers…** → look up Mössbauer
  spectrometers if seeded.
- **Glossary** → search *Mössbauer spectroscopy*, *Isomer
  shift*, *Quadrupole splitting*, *Iron oxidation state*.

Next: **Photoelectron spectroscopy (XPS, UPS)**.
