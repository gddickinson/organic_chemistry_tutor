# Photoelectron spectroscopy — XPS + UPS

Photoelectron spectroscopy uses high-energy photons to
**eject electrons from a sample**; the kinetic energies of
the ejected electrons report the binding energies of the
electronic levels they came from.

## Two main flavours

| | XPS | UPS |
|----|-----|-----|
| Photon source | X-ray (Al-Kα 1486 eV; Mg-Kα 1254 eV) | UV (He-I 21.2 eV; He-II 40.8 eV) |
| Electrons ejected | core electrons (1s, 2p, etc.) | valence electrons |
| Information | composition + oxidation state | molecular orbital structure |
| Resolution | ~ 0.5 eV | < 0.05 eV (best) |

## XPS — composition + chemistry

Each element has characteristic core-level binding
energies. Some examples:

| Element | Core line | BE (eV) |
|---------|-----------|---------|
| C | 1s | 285 |
| N | 1s | 400 |
| O | 1s | 532 |
| F | 1s | 685 |
| Na | 1s | 1071 |
| S | 2p | 168 |
| Cl | 2p | 199 |
| Si | 2p | 99 |
| Ti | 2p | 458 |
| Fe | 2p₃/₂ | 707 |
| Cu | 2p₃/₂ | 933 |
| Au | 4f₇/₂ | 84 |

Beyond identification, **chemical shifts** report
oxidation state + bonding environment:

```
C 1s: graphite        285.0 eV
      C-C / C-H        285.0 eV
      C-O              286.5 eV
      C=O              287.5 eV
      O-C=O (ester)    289.0 eV
      C-F              ~ 290 eV
      CF₃             ~ 293 eV
```

Resolves carbons in different chemical environments — often
1-2 eV apart for distinct functional groups.

## UPS — frontier MOs

UPS measures valence-electron binding energies →
direct access to MO structure:

- HOMO position relative to vacuum.
- Workfunction of metals + semiconductors.
- LUMO from inverse photoemission.

In conjugated polymers (semiconductor electronics +
solar cells) UPS is key for measuring HOMO-LUMO gap +
band offsets at interfaces.

## Surface sensitivity

XPS detects only the top **5-10 nm** of a sample (electron
escape depth). Useful for:

- **Thin-film characterisation** — ALD, MBE, CVD layer
  composition.
- **Catalyst surface chemistry** — adsorbed species,
  oxidation state of active sites.
- **Corrosion** — passive-layer composition on metal
  surface.
- **Polymer + biomaterial surfaces** — protein adsorption,
  contact angle correlation.

## Modern variants

### NAP-XPS (near-ambient pressure XPS)

Conventional XPS needs ultra-high vacuum (UHV ~ 10⁻⁹
mbar). NAP-XPS works at up to 25 mbar — enables study
of catalysts under reaction conditions.

### HAXPES (hard X-ray PES)

Higher energy X-rays (5-15 keV) → deeper electrons
ejected → bulk-sensitive (~ 50 nm depth) instead of just
surface. Used for buried interfaces.

### ARPES (angle-resolved PES)

Measures the photoelectron's emission angle → resolves
band structure k-vector by k-vector. Used for studying
graphene, topological insulators, superconductors.

### Synchrotron PES

Variable photon energy → tunable depth + selectivity.
Best resolution + sensitivity. Done at large facilities
(SLAC, ESRF, MAX-IV, Diamond).

## XPS in catalysis research

Standard procedure for any new heterogeneous catalyst:

1. **Composition** — confirm element ratios (Pd, Pt, Co,
   Ni).
2. **Oxidation state** — Fe(II) vs Fe(III); Cu(0) vs
   Cu(I) vs Cu(II).
3. **Active site** — identify supported nanoparticles vs
   single atoms.
4. **Coverage / loading** — quantify wt%.

Single-atom catalysis (lesson 23) leans heavily on XPS
for confirming M-Nₓ vs M-M nanocluster character.

## XPS in batteries

Solid-electrolyte interphase (SEI) layer characterisation:

- Li 1s binding energy → distinguishes Li₂O, Li₂CO₃, LiF,
  LiOH species in SEI.
- Identifies salt decomposition products (LiPF₆ → LiF +
  POₓFᵧ).
- Tracks SEI evolution during cycling.

## XPS limits

- **Surface only** (5-10 nm).
- **Vacuum required** (NAP-XPS partially solves).
- **No H detection** (1s of H ~ 0 eV; below detection).
- **Quantification ~ 5 % accuracy** for most elements.
- **Insulating samples** charge up; need flood gun.

## Try it in the app

- **Tools → Lab analysers…** → look up Thermo Scientific /
  Kratos / SPECS XPS systems (if seeded).
- **Tools → Spectrophotometry methods** → see PES section.
- **Glossary** → search *XPS*, *UPS*, *Photoelectron
  spectroscopy*, *Binding energy*, *Surface sensitivity*,
  *NAP-XPS*.

Next: **Vibrational circular dichroism**.
