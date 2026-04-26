# Diazo + nitrene chemistry

**Carbenes** + **nitrenes** are 6-electron neutral species
with a lone pair and an empty orbital — dangerous + reactive
+ surprisingly versatile. Diazo + azide compounds are the
canonical precursors.

## Diazo compounds

A **diazo compound** has a terminal `=N⁺=N⁻` group (or
equivalent resonance):

```
R-CH=N⁺=N⁻   ↔   R-CH⁻-N≡N⁺
```

The most famous: **diazomethane (CH₂N₂)** — yellow gas,
intensely toxic + explosive; used for:

- **Methylation of carboxylic acids** (R-COOH + CH₂N₂ →
  R-COOMe + N₂↑) — selective vs alcohols + amines.
- **Carbene generation** (CH₂N₂ → :CH₂ + N₂; needs UV or
  Cu / Rh).
- **Ring expansion** of cyclic ketones (Tiffeneau-Demjanov).

Modern surrogate: **TMSCHN₂** (trimethylsilyl-
diazomethane) — same chemistry, much safer. Works in
flow reactors at scale.

## Carbenes

A carbene `:CR₂` has 2 non-bonding electrons. Two spin
states:

- **Singlet carbene** — two electrons paired in one
  orbital (the empty p remains empty). Concerted reactions,
  stereospecific.
- **Triplet carbene** — two electrons unpaired (diradical-
  like). Stepwise via diradical, can lose stereochemistry.

Singlet vs triplet ground state depends on the substituents
+ environment.

## Carbene reactions

### Cyclopropanation

```
CH₂=CHR + :CH₂ → cyclopropane-CH₂R
```

- **Simmons-Smith** — Zn / CH₂I₂ → carbenoid (not free
  carbene); syn cyclopropanation, retention of alkene
  geometry.
- **Cu / Rh / diazo** — catalytic asymmetric cyclopropanation.
  Doyle Rh(II)-carboxylates → > 90 % ee.
- **Bamford-Stevens** + **Shapiro** — generate carbene from
  tosylhydrazone via in-situ-generated diazo.

### C–H insertion

Carbenes insert into C–H bonds — direct functionalisation
without prior halogenation:

```
:CR₂ + R'-H → R'-CR₂-H
```

Rh(II)(perfluorocarboxylate)₂ catalysts (Doyle, Davies)
insert into selected C-H bonds with high regio- + stereo-
selectivity. Pharma uses this for late-stage C-H
functionalisation.

### Ylide formation

A carbene captures a lone pair to form a zwitterionic
ylide (C-O, C-N, C-S). Subsequent rearrangement gives
useful products:

- **Stevens** + **Meisenheimer** rearrangements.
- **Wittig-style** olefination from sulfur ylides.
- **Doyle's** C-H insertion via ylide intermediates.

### Wolff rearrangement

```
α-diazoketone + hν → ketene + N₂
R-CO-CHN₂ → R-CH=C=O
```

Retains the carbonyl C → useful in the **Arndt-Eistert
homologation**: R-COOH → R-COCl → R-CO-CHN₂ → R-CH₂-COOH
(one-carbon extension).

## Nitrenes

The nitrogen analogue: `R-N:` with 6 valence electrons.
Same singlet / triplet spin chemistry.

### Generation

- **Acyl azides** + heat → acyl nitrene → Curtius
  rearrangement to isocyanate.
- **Sulfonyl azides** + Rh(II) → sulfonyl nitrene → C-H
  amination.
- **Sulfonimidoylimino-N-source** (PhI=NTs, etc.) →
  hypervalent iodine + nitrene.

### Curtius rearrangement

```
R-C(=O)-N₃ → R-N=C=O (isocyanate) + N₂
            → R-NH-CO-OR' (carbamate) + R'OH
```

Net: carboxylic acid → primary amine with one fewer carbon.

### Schmidt reaction

```
R-CO-R' + HN₃ + H⁺ → R-N=C=R' (rearranges) → amide → cleaves
```

Migration of the larger group to N. Used to convert
ketones to N-substituted amides.

### Asymmetric C–H amination

```
R-H + PhI=NSO₂Ar + Rh₂(esp)₂ → R-NHSO₂Ar
```

DuBois (Stanford) + Davies (Emory) chiral Rh dimers →
intramolecular C-H amination with selectivity for tertiary
+ benzylic + α-heteroatom positions.

## Azide chemistry

Beyond nitrene precursors, azides have their own reactivity:

- **CuAAC click** — azide + terminal alkyne + Cu → 1,4-
  triazole (Sharpless / Meldal click chemistry, 2001).
- **Staudinger reduction** — RN₃ + PPh₃ → R-N=P-Ph₃ →
  H₂O → R-NH₂ + Ph₃P=O. Mild + chemoselective for amine
  generation.
- **Staudinger ligation** — modified Staudinger with
  intramolecular ester delivers an amide bond → first
  bioorthogonal chemistry.
- **Azide-alkyne CuAAC bioconjugation** — every modern
  bioconjugation toolkit.

## Safety + handling

- **Diazomethane** is shock + heat sensitive. Use only with
  Teflon (no ground glass, scratches initiate detonation).
  Modern flow generators consume it as it forms.
- **Sulfonyl + acyl azides** — heat sensitive; > 50 % azide-
  by-mass is over the limit for routine handling.
- **Heavy-metal azides** (NaN₃ + Cu pipes) — primary
  explosives. Don't dispose of NaN₃ down a copper drain.

## Try it in the app

- **Reactions tab** → load *Click chemistry CuAAC* (1,3-
  dipolar cycloaddition); look for Wolff / Curtius if
  seeded.
- **Tools → Lab reagents…** → look up diazomethane,
  TMSCHN₂, NaN₃ for hazards.
- **Glossary** → search *Carbene*, *Nitrene*, *Diazomethane*,
  *Wolff rearrangement*, *Curtius rearrangement*,
  *Staudinger reaction*, *Click chemistry*.

Next: **Steroids + terpenoids — biosynthesis + structure**.
