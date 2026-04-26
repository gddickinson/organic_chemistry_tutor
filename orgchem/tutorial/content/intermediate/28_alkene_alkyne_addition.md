# Alkene + alkyne addition reactions deeper

The intermediate alkene chemistry covered hydration +
hydrogenation. This lesson goes through the full menu of
addition reactions, with explicit attention to
regiochemistry + stereochemistry.

## Electrophilic addition: HX

```
R-CH=CH-R' + H-X  →  R-CHX-CH₂-R'   (Markovnikov)
                  or R-CH₂-CHX-R'   (anti-Markov.)
```

Markovnikov rule: the H ends up on the carbon with more H's
already (the less-substituted end), the X on the more-
substituted end. Mechanism: H⁺ adds first → forms the more-
stable carbocation → X⁻ attacks.

**Anti-Markovnikov** with HBr happens with peroxides
(initiator → Br•), via a free-radical chain. The Br• adds
first to the less-substituted end → more-stable carbon
radical → H• abstraction.

## Hydration

### Markovnikov: dilute acid

```
RCH=CH₂ + H₂O / H₂SO₄ →  R-CH(OH)-CH₃
```

Mechanism: H⁺ adds to less-substituted C → 2° carbocation →
H₂O adds → loss of H⁺.

### Anti-Markovnikov: hydroboration-oxidation

```
RCH=CH₂ + BH₃ → R-CH₂-CH₂-BH₂ → (H₂O₂ / NaOH) → R-CH₂-CH₂-OH
```

Two steps:

1. **Hydroboration** — concerted syn addition; B adds to
   less-hindered (less-substituted) carbon.
2. **Oxidation** — H₂O₂ / NaOH retains stereochemistry,
   replaces B with OH.

Net: **anti-Markov + syn** addition of H + OH.

### Oxymercuration-demercuration

```
RCH=CH₂ + Hg(OAc)₂ / H₂O → R-CH(OH)-CH₂-HgOAc → (NaBH₄) → R-CH(OH)-CH₃
```

Markovnikov; no carbocation (mercurinium intermediate so
no rearrangement).

## Halogenation

```
RCH=CHR' + Br₂ → R-CHBr-CHBr-R'
```

- **Anti** addition (bromonium ion intermediate).
- Stereospecific: cis alkene → meso dibromide; trans alkene
  → racemic dl pair.

In water: → bromohydrin (Markovnikov OH, anti to Br).

## Epoxidation

```
RCH=CHR' + mCPBA  →  trans-epoxide + ArCO₂H
```

Concerted [2+1] addition; **syn**. Stereospecific.

Ring-opening of epoxides:

- **Acidic conditions**: nucleophile attacks **more-substituted** C
  (Markovnikov-like; protonated epoxide has carbocation
  character).
- **Basic conditions**: Nu attacks **less-substituted** C
  (SN2 on less-hindered C).

## Dihydroxylation

### Syn diol: OsO₄

```
RCH=CHR' + OsO₄ + NMO → R-CH(OH)-CH(OH)-R' (syn)
```

Catalytic in OsO₄ with NMO co-oxidant.

**Sharpless asymmetric dihydroxylation (AD)**: same
chemistry + a chiral DHQ / DHQD ligand → > 90 % ee.
Available as AD-mix-α + AD-mix-β kits.

### Anti diol: epoxide → SN2-open

```
RCH=CHR' + mCPBA → trans-epoxide → H₂O / H⁺ → R-CH(OH)-CH(OH)-R' (anti)
```

## Oxidative cleavage

- **O₃ / Zn / AcOH** → 2 × C=O (aldehyde end).
- **O₃ / H₂O₂** → 2 × COOH end (over-ox).
- **OsO₄ / NaIO₄** (Lemieux-Johnson) → diol then cleavage;
  one-pot.
- **KMnO₄ (hot)** → COOH + ketones; messy.

Useful for structure elucidation (degrade a complex alkene
+ identify the fragments) + total synthesis.

## Alkyne reactions

### Hydration

- **Markov**: HgSO₄ / H₂SO₄ / H₂O → terminal alkyne →
  methyl ketone (enol tautomerises).
- **Anti-Markov**: hydroboration with bulky borane
  (disiamylborane) + oxidation → terminal alkyne →
  aldehyde.

### Reduction

- **H₂ / Lindlar** → cis alkene only (poisoned Pd).
- **Na / NH₃ (Birch)** → trans alkene.
- **H₂ / Pd-C (no poison)** → over-reduces to alkane.

### Acetylide alkylation

```
RC≡CH + NaNH₂ → RC≡C⁻Na⁺
RC≡C⁻ + R'X → RC≡C-R'
```

Terminal alkyne pKa ~ 25, deprotonated by NaNH₂ in NH₃ or
by n-BuLi. The acetylide is a strong nucleophile that does
SN2 on primary alkyl halides (3° → E2).

### Sonogashira coupling

```
RC≡CH + ArX + Pd(0) / CuI / amine → RC≡C-Ar
```

The Pd cross-coupling for sp-sp² C-C bonds. Workhorse for
arylacetylene synthesis.

## Stereochemistry summary

| Reaction | Add mode | Selectivity |
|----------|----------|-------------|
| Hydrogenation | syn | both H from metal surface |
| Halogenation | anti | bromonium intermediate |
| Hydration / acid | random | carbocation intermediate |
| Hydroboration | syn | concerted |
| OsO₄ dihydroxylation | syn | osmate ester |
| Epoxidation | syn | concerted [2+1] |
| Acid-opened epoxide → diol | anti | net acid-catalysed Markov SN1 |
| HX | random | carbocation |
| HBr / peroxides | random | radical chain |

## Try it in the app

- **Reactions tab** → load *Bromination of ethene* (seeded)
  for the bromonium mechanism.
- **Tools → Stereochemistry…** → input alkene products to
  see R/S assignments + the meso vs dl distinction.
- **Glossary** → search *Markovnikov*, *Anti-Markovnikov*,
  *Hydroboration-oxidation*, *Bromonium ion*, *Lindlar
  catalyst*.

Next: **Carbocation chemistry deeper — rearrangements +
neighbouring group participation**.
