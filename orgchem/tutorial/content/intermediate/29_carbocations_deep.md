# Carbocation chemistry deeper — rearrangements + neighbouring group participation

A **carbocation** is a positively charged carbon with only 6
valence electrons (instead of 8). Modern organic chemistry
fully embraces them: SN1, E1, electrophilic aromatic
substitution, biosynthetic terpenes — all carbocations
under the hood.

## Stability ladder

```
Methyl < 1° < 2° < 3°  <  allyl ≈ benzyl  <  acylium  <  trityl  <  …
   ↑
non-classical: bridged + delocalised carbocations
```

Stabilisation comes from:

- **Hyperconjugation** — adjacent C-H σ bonds donate into
  the empty p orbital. More alkyl groups → more
  hyperconjugation → more stable.
- **Resonance** — allyl, benzyl, oxocarbenium spread the
  positive charge over multiple atoms.
- **Adjacent lone pair donation** — α-O, α-N, α-halogen
  cations are remarkably stable (e.g. acylium R-C≡O⁺).

## Generation

- **Acid + alcohol** — H₃O⁺ + R-OH → R-OH₂⁺ → R⁺ + H₂O.
- **Acid + alkene** — H⁺ adds to less-substituted C → more-
  substituted carbocation.
- **Solvolysis of R-X** — R-X → R⁺ + X⁻ in polar protic
  solvent.
- **Diazonium decomposition** — Ar-N₂⁺ → Ar⁺ + N₂↑ (very
  short-lived).
- **Oxidation** — Pb(OAc)₄, hypervalent iodine, electrochem.

## Rearrangements

A less-stable carbocation can **rearrange to a more stable
one** by 1,2-shift of:

- **H** (1,2-hydride shift) — fastest.
- **Alkyl group** (1,2-alkyl shift) — slower.
- **Aryl** (1,2-aryl shift) — typical of phenonium ions.

```
2° R⁺  →  3° R⁺   (more stable; rearrangement happens)
2° R⁺  →  2° R⁺   (no rearrangement; same stability)
```

### Famous example — Wagner-Meerwein

```
neopentyl substrate (CH₃)₃C-CH₂-X →
   primary CH₂⁺ →  1,2-Me shift  →  3° (CH₃)₂C⁺-CH₂CH₃
                                    → SN1 product
```

Pinacol-pinacolone rearrangement, Beckmann rearrangement,
retro-pinacol — all rely on the same 1,2-shift principle.

## Non-classical (bridged) carbocations

Some 2° carbocations have an adjacent σ bond that donates
into the empty p orbital, forming a **3-centre 2-electron
bond** — the classical / non-classical debate (Winstein vs
Brown, 1950s-1980s).

The **2-norbornyl cation** is the textbook example. The
molecular orbital picture has a single bridged species, NOT
two equilibrating classical cations. NMR + X-ray (in stable
super-acid media) confirm.

## Neighbouring group participation (NGP)

A nearby **donor atom or π system** can attack the cation
internally, forming a 3-, 4-, or 5-membered ring
intermediate that:

- Stabilises the cation (faster reaction → "anchimeric
  assistance", k > 10³ × normal SN1).
- Locks stereochemistry (the bridge attacks from one face).
- Often gives **retention** of configuration (two
  inversions = retention).

### Examples

- **Mustard gas** — sulfide neighbouring group → episulfonium →
  attacked by water; explains its rapid alkylation chemistry.
- **2-bromopropionate → α-acetoxypropionate via carboxylate NGP**
  (acetolysis with carboxylate displacement).
- **Cholesterol tosylate solvolysis** — homoallyl cation
  via 5-membered cyclopropyl participation; rearranges to
  cyclosteroid.
- **Sugar chemistry** — C2-acyloxy NGP enforces 1,2-trans
  glycoside formation (glycosylation chapter, lesson 22).

### Diagnostic of NGP

- **Rate enhancement** — solvolysis k 10²-10⁶ × faster than
  unsubstituted analogue.
- **Stereochemical retention** — net retention of
  configuration (rare for SN1 / SN2).
- **Crossover product** — sometimes nucleophile attacks
  the bridge from the wrong face.

## Carbocation chemistry in biology

### Terpene biosynthesis

Terpene cyclases catalyse cation cascade reactions: an
isoprenyl pyrophosphate ionises to a carbocation → undergoes
multiple 1,2-shifts + cyclisations → final quench by water
or H⁻ loss. **Cholesterol from squalene** runs through
~ 8 sequential cation rearrangements in one enzyme active
site (oxidosqualene cyclase).

### Glycoside hydrolysis

Lysozyme + other glycoside hydrolases protonate the
glycosidic O → forms a glycosyl oxocarbenium → trapped by
water (retaining mechanism) or directly by nucleophile
(inverting). The half-chair oxocarbenium TS is the textbook
glycosidase intermediate.

## Stable carbocations — superacids

George Olah's 1994 Nobel work: in **super-acid** media
(SbF₅·HSO₃F, "magic acid"; SbF₅·HF), even alkyl carbocations
become persistent + isolable + characterisable by NMR + X-
ray. Tert-butyl cation, norbornyl cation, cyclopentadienyl
cation — all observed.

Modern non-coordinating anions (BArF⁻, B(C₆F₅)₄⁻,
[B₁₂H₁₂]²⁻ analogues) crystallise carbocations cleanly.

## Try it in the app

- **Reactions tab** → load *SN1*, *E1* — see the
  carbocation intermediate; *Pinacol rearrangement* (seeded)
  for a 1,2-Me shift; *Friedel-Crafts alkylation* for a
  methyl cation.
- **Tools → Stereochemistry…** → check enantiomeric
  outcome of NGP-controlled reactions (retention).
- **Glossary** → search *Carbocation*, *Hyperconjugation*,
  *1,2-shift*, *Wagner-Meerwein rearrangement*,
  *Neighbouring group participation*, *Non-classical
  carbocation*.

Next: **Diazo + nitrene chemistry**.
