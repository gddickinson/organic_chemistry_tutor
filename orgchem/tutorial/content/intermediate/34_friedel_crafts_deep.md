# Friedel-Crafts deeper — alkylation, acylation, limitations

The simplest electrophilic aromatic substitutions: install
an alkyl or acyl group on an electron-rich arene with a
Lewis-acid catalyst.

## Friedel-Crafts alkylation

```
ArH + RCl + AlCl₃ → ArR + HCl
```

Mechanism:

1. AlCl₃ + RCl → R⁺ + [AlCl₄]⁻ (carbocation generation).
2. R⁺ attacks Ar π-system → Wheland intermediate
   (cyclohexadienyl cation).
3. Loss of H⁺ → ArR + Lewis-acid recovery.

### Limitations of FC alkylation

1. **Carbocation rearrangement** — primary R⁺ is unstable;
   rearranges to 2° / 3° → wrong product:
   ```
   PhH + n-PrCl + AlCl₃ → PhCH(CH₃)CH₃ (iso-propyl), NOT n-propyl
   ```

2. **Polyalkylation** — alkyl group is activating (more
   electron-donating than H) → product more reactive than
   substrate → multiple alkylations.

3. **Deactivated rings** — strongly deactivated arenes
   (nitrobenzene, benzoic acid) → alkylation fails. Pyridine
   is too poor too.

4. **No vinyl, no aryl R groups** — need sp³ carbocation.

## Friedel-Crafts acylation

```
ArH + RCOCl + AlCl₃ → ArCOR + HCl
```

The acylium cation R-C≡O⁺ is the electrophile (stable +
non-rearranging). Mechanism mirrors alkylation.

### Pros over alkylation

- **No carbocation rearrangement** (acylium is resonance-
  stabilised, no migration to a more-stable form).
- **No polyacylation** — the ketone product is deactivating
  (-M from C=O), so it's slower than the substrate; mono-
  acylation dominates.
- **Reduces to FC alkyl** — Wolff-Kishner or Clemmensen on
  the ketone gives the same final product as FC alkylation
  but cleanly.

### Limitations

- **Deactivated rings** still don't work (nitrobenzene,
  pyridine).
- **Catalyst is consumed** — AlCl₃ binds the C=O of
  product; need ≥ 1 eq AlCl₃ per acyl group, not catalytic.

## Modern Friedel-Crafts

### Triflate-activated

```
ArH + R-OTf + Sc(OTf)₃ → ArR
```

Lanthanide triflates (Sc, Yb, Sm) work as catalytic Lewis
acids. Avoid the AlCl₃ workup mess.

### Lewis-acid free

- **PhI(OAc)₂ + alkene** → arene alkylation.
- **Photoredox** routes from carboxylic acids (decarboxylative
  arylation; lesson 11).

### Bismuth (BiCl₃, Bi(OTf)₃)

Mild Lewis acids that tolerate nitro + ester + halide
substituents. Replacing AlCl₃ in process chemistry.

## Substrate scope

What works as the arene (decreasing reactivity):

```
ArOR > ArOH > Ar (alkyl) > Ar (H) > ArX (halide) > Ar (deactivated)
```

Deactivating + meta-directing groups stop FC entirely.
Strongly activated arenes (anilines, phenol ethers) over-
react + polyalkylate.

## Famous applications

- **BHC ibuprofen synthesis** — FC acylation of
  isobutylbenzene with acetic anhydride (in HF) installs
  the acetyl group; then Pd-catalysed carbonylation
  installs the COOH.
- **Industrial bisphenol A** — acetone + 2 phenols + acid
  catalyst (sulfonic acid resin) → BPA.
- **Aspirin precursor** — phenol + sodium hydroxide + CO₂
  + heat (Kolbe-Schmitt; an EAS-related carboxylation).

## Try it in the app

- **Reactions tab** → load *Friedel-Crafts alkylation*
  (seeded — methyl cation EAS) for full mechanism.
- **Mechanism player** → step through the Wheland
  intermediate.
- **Glossary** → search *Friedel-Crafts alkylation*,
  *Friedel-Crafts acylation*, *Acylium ion*, *Wheland
  intermediate*, *Lewis acid catalysis*.

Next: **Aromatic substitution patterns — DMG + ortho
lithiation**.
