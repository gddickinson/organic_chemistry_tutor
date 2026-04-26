# Hydroformylation + carbonylation chemistry

CO is a cheap, abundant feedstock (from syngas: H₂ + CO out
of methane reforming or coal gasification). Catalysts that
insert CO into organic substrates power a huge fraction of
the world's chemical industry.

## Hydroformylation (Roelen, 1938; oxo process)

```
RCH=CH₂ + H₂ + CO → RCH₂-CH₂-CHO  +  RCH(CHO)-CH₃
                       (n linear)        (iso branched)
```

Catalysed by Co or Rh + phosphine ligands. The most
practised industrial homogeneous catalysis: **~ 12 million
tonnes / yr** (mostly C₈ aldehydes → C₈ alcohols → DOP
plasticisers; also C₃ aldehydes → n-butanol, 2-ethyl-
hexanol).

### Mechanism (Heck-Breslow cycle)

1. **Activate Rh / Co** → Rh-H or Co-H.
2. **Alkene coordination** → π-complex.
3. **Migratory insertion** of alkene into Rh-H → Rh-alkyl.
4. **CO coordination + insertion** → Rh-acyl.
5. **H₂ oxidative addition** → Rh-acyl-H₂ → reductive
   elimination → aldehyde + Rh.

n / iso ratio depends on the migration step's
regiochemistry (linear vs branched alkyl). Bulky phosphines
favour linear (BiPhePhos, BISBI ligands).

### Catalysts

- **Co₂(CO)₈** (Roelen's original) — high P + T (200 atm,
  150 °C). Cheap but messy.
- **HRh(CO)(PPh₃)₃** + chelating diphosphine (BiPhePhos,
  Xantphos) — milder (10-20 atm, 80-100 °C); 99 % linear
  selectivity. Rh recovery via membrane filtration or two-
  phase liquid-liquid (water-soluble TPPTS).
- **Pt / Sn / phosphine** — niche.

## Asymmetric hydroformylation

Adding chiral diphosphines to Rh:

- **(R,R)-Chiraphos**, **(S,S)-Yanphos**, **(R)-BINAPHOS** —
  > 90 % ee + > 99 % branched selectivity in some cases.
- Industrial example: **(S)-naproxen aldehyde** intermediate
  via asymmetric hydroformylation of vinyl arene.

## Hydroformylation variants

- **Hydrocarbonylation** — alkene + CO → carboxylic acid /
  ester / amide (depending on co-reagent).
- **Hydroamidation** — alkene + CO + amine → amide.
- **Reppe carbonylation** — alkyne + CO + ROH → α,β-
  unsaturated ester (acrylate from acetylene, historic).

## Acid-catalysed carbonylation — Reppe + Koch

- **Koch carbonylation** — alkene + CO + H₂O + strong acid
  (H₂SO₄, HF) → tertiary carboxylic acid via Markov H⁺
  addition + acylium attack of CO.
- Industrial: **Pivalic acid (neopentanoic acid)** from
  isobutene + CO + H₂O.

## Methanol carbonylation — Monsanto + Cativa

The single largest acetic acid manufacturing process:

```
CH₃OH + CO → CH₃COOH
```

- **Monsanto process** (1970s) — Rh + I⁻; ~ 10⁵ tonnes /
  yr per plant.
- **Cativa process** (BP, 1996) — Ir + I⁻; faster, lower
  Ir loading, lower water content (less waste).

Combined: **> 12 million tonnes / yr** of acetic acid
worldwide, vital for vinyl acetate (PVA), terephthalic acid
(PET), cellulose acetate.

## Other Pd carbonylations

### Methoxycarbonylation

```
RX + CO + ROH + Pd cat. → RC(=O)OR'
```

Pharma uses this for ester installation late-stage.

### Aminocarbonylation

```
RX + CO + R'NH₂ + Pd cat. → RC(=O)NR'H
```

Drug-discovery libraries — CO + amine + aryl halide → wide
amide library in one step.

### Beller / Skrydstrup CO surrogates

CO is hazardous (lethal at 400 ppm in 30 min). For lab
scale:

- **Beller's** — Mo(CO)₆ as solid, releases CO slowly on
  heating.
- **Skrydstrup's two-chamber technology** — generate CO ex
  situ from formic acid / oxalyl chloride in chamber A,
  diffuse into chamber B with the Pd-coupling reaction.
- **Carbon monoxide isotopes (¹³CO, ¹⁴CO)** can be
  installed cleanly with these surrogates.

## Hydroxycarbonylation in flow

Modern flow chemistry handles the CO-pressure problem
elegantly: substrate + CO from a high-pressure inlet
delivered through a Teflon-AF-2400 membrane (tube-in-tube)
keeps reagent + gas in the same tube without phase
separation. Allows kg-scale carbonylation without batch
high-pressure reactors.

## Try it in the app

- **Reactions tab** → look for hydroformylation, methanol
  carbonylation, Pd carbonylation entries (if seeded).
- **Tools → Lab analysers…** → look up online IR sensors
  + CO scrubbers used in flow carbonylation.
- **Glossary** → search *Hydroformylation*, *Oxo process*,
  *Monsanto process*, *Carbonylation*, *Migratory
  insertion*.

Next: **Frustrated Lewis pairs — metal-free H₂ activation**.
