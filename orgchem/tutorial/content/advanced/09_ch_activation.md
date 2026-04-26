# C–H activation — the modern functionalisation toolbox

A C–H bond is the most abundant + least reactive bond in
organic molecules. **C–H activation** breaks one of these
bonds + functionalises the carbon — without prior
halogenation or other "directing" pre-step. This is one of
the major ongoing revolutions in synthetic methodology.

## Why it matters

Traditional cross-coupling needs Ar–X (X = Br, I, OTf). To
get Ar–X, you typically do an electrophilic aromatic
substitution. C–H activation replaces:

```
Ar-H → Ar-Br → Ar-X coupling product   (3 steps, X = waste)
Ar-H → Ar-X coupling product             (1 step)
```

This is **step-economy** in action — cuts route length, atom
economy, + waste in one move.

## Mechanistic classes

### 1. Concerted metalation-deprotonation (CMD)

Pd(II)/Cu(I)/Rh(I)/Ir(I) carboxylate clusters cleave Ar-H
via a 6-membered TS where the metal-bound carboxylate
abstracts H⁺ as the metal binds C. **Key insight (Fagnou,
2006)**: pivalate is a much better proton shuttle than
acetate. Modern Pd / Cu / pivalate systems arylate
heteroarenes (thiophenes, furans, pyrroles) directly.

### 2. Electrophilic metalation (SEAr-like)

Pd(II), Pt(II), Ir(III) act as electrophiles + attack
electron-rich arenes. Substrate selectivity follows EAS
trends.

### 3. Oxidative addition into C–H

Pt(0), Ir(I), Rh(I) insert directly into a C-H bond
(Bergman, Goldman, Hartwig). Rare but spectacular — enables
non-aromatic sp³ C-H functionalisation.

### 4. Concerted radical mechanisms

Recent: photoredox-generated radicals + HAT (hydrogen-atom
transfer) catalysts (decatungstate, quinuclidine, AIBN-style
initiators). Doyle, Knowles, MacMillan deeply explored.

## Directing groups

C–H activation needs *selectivity*. A pendant heteroatom
that coordinates the metal first delivers it to a specific
C-H bond (usually ortho via 5-membered metallacycle):

- **Pyridine, quinoline, pyrazole** — strong σ-donors.
- **Amides, carbamates** — modulated electronics.
- **Carboxylic acids** (Yu) — removable + native.
- **8-Aminoquinoline** (Daugulis, 2005) — bidentate, super
  selective.
- **Native functional groups** — ketone, alcohol, amine —
  modern frontier.

## Yu's meta-C–H activation

Most directing groups place the metal at *ortho*. Yu used
**templating directing groups** (norbornene as a relay,
cyclopalladation past ortho) to functionalise *meta* C–H
bonds — landmark in regiocontrol.

Para is even harder; only a few approaches work.

## sp³ C–H activation

Aliphatic C–H bonds (~ 100 kcal/mol BDE) are tougher than
aromatic ones (~ 110 kcal/mol — but more accessible due to
metal π-binding). Recent advances:

- **White-Chen catalysts** — Fe/PDP for site-selective
  oxidation of aliphatic C-H bonds. Predicts which C-H
  oxidises by sterics + electronics.
- **Sanford Pd(II)/(IV)** — δ-C-H activation via
  palladacycles.
- **Hartwig Ir-borylation** — sp³ borylation of methyl C-H,
  enables further coupling of any methyl-bearing molecule.

## Halogenation, borylation, fluorination

C–H activation lets you install a coupling handle without
prior halogenation:

- **Ir-borylation** (Hartwig, Ishiyama) — Bpin installs at
  the most accessible position; product Ar-Bpin → Suzuki.
- **Pd halogenation** — Pd(II) + N-halosuccinimide installs
  Ar-Cl, Ar-Br, Ar-I directly.
- **Pd fluorination** (Sanford, Ritter) — Pd(II)/Pd(IV) +
  Selectfluor installs Ar-F.

## Industrial impact

Adoption is slower than cross-coupling because directing-
group strategies need design. But:

- **Late-stage functionalisation** of advanced
  pharmaceuticals — install F, OH, NHR on a near-final API
  to explore SAR without redoing the whole synthesis. Genentech
  + Merck use Yu / Sanford chemistry routinely.
- **Boron-installation routes** — Pfizer's pirtobrutinib
  (BTK inhibitor) used Hartwig-Ishiyama borylation in
  process development.

## Try it in the app

- **Tools → Retrosynthesis…** → look for templated
  C-H-activation disconnections (8-aminoquinoline directing
  group, Yu meta).
- **Glossary** → search *C-H activation*, *Concerted
  metalation-deprotonation (CMD)*, *Directing group*,
  *Late-stage functionalisation*.

Next: **Olefin metathesis — Grubbs + Schrock + everything
since**.
