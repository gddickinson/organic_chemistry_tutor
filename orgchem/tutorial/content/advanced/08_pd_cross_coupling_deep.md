# Pd cross-coupling deep-dive — beyond Suzuki

The 2010 Nobel Prize (Heck + Negishi + Suzuki) put Pd cross-
coupling at the centre of organic synthesis. This lesson goes
past the textbook Suzuki + walks the modern landscape: ligand
design, mechanism details, the named-reaction zoo, and where
the field is going.

## The catalytic cycle (general)

Every Pd(0) / Pd(II) cross-coupling cycles through:

1. **Oxidative addition (OA)** — Pd(0) inserts into Ar-X bond
   → Ar-Pd(II)-X. Rate-limiting for aryl chlorides.
2. **Transmetalation** — second organometallic (R-B, R-Zn,
   R-Sn, R-Si, R-MgX) transfers R to Pd, displacing X⁻.
3. **Reductive elimination (RE)** — Ar-Pd(II)-R → Ar-R +
   Pd(0). Often the trickiest step for sterically congested
   couplings.

**Backbone reactions by transmetalating partner:**

| Reaction | R-M | Year |
|----------|-----|------|
| Suzuki-Miyaura | R-B(OR)₂ | 1979 |
| Negishi | R-ZnX | 1977 |
| Stille | R-SnR'₃ | 1977 |
| Hiyama | R-SiR'₃ | 1988 |
| Kumada | R-MgX | 1972 |
| Sonogashira | R-C≡C-H + Cu | 1975 |
| Heck | R-CH=CH₂ (no transmetalation) | 1972 |
| Buchwald-Hartwig | R-NH₂ + base | 1994 |

## Ligand revolution

Early couplings used PPh₃ — limited to electron-poor aryl
iodides + bromides. Modern bulky electron-rich phosphines
made aryl chlorides + room-temperature couplings + low
loadings routine:

- **SPhos, XPhos, RuPhos, BrettPhos** (Buchwald) —
  biaryl-monodentate, electron-rich phosphines.
  XPhos is the Hartwig-Buchwald amination workhorse.
- **JackiePhos, RockPhos, AdBrettPhos** — second-generation
  for fluorination + heteroaryl couplings.
- **NHC ligands** (PEPPSI, IPr, IMes) — strong σ-donors,
  rival the Buchwald phosphines, air-stable.
- **TPPTS, TXPTS** — water-soluble for green chemistry +
  biological media.

## C–N + C–O couplings (Buchwald-Hartwig)

Aryl-amine bond formation via:

- ArX + R₂NH + Pd / XPhos / NaOtBu → ArNR₂.
- Tolerates 1° + 2° amines + heterocycles (pyrazole,
  imidazole, indole) + amides + sulfonamides.
- Now dominates pharma SAR — most aniline-containing drugs
  use Buchwald.

C-O variant: Ar-OR via Pd/RockPhos. Slower than C-N due to
β-hydride elimination of alkoxides.

## Direct C–H activation

Beyond pre-functionalised C-X: the modern frontier is
catalytic C-H functionalisation.

- **Fagnou's C-H arylation** (2006) — Pd / pivalate base /
  bulky phosphine arylates electron-poor heteroarenes
  directly via concerted metalation-deprotonation (CMD).
- **Yu's Pd / amino acid systems** — directed C-H activation
  using a directing group (CO₂H, CONHAr, pyridine) to bring
  Pd into an ortho or meta position.
- **Sanford** — Pd(II)/Pd(IV) cycles for C-H acetoxylation +
  halogenation.

## Photoredox-Pd dual catalysis

**MacMillan + Doyle** (2014-) combined Pd cross-coupling with
visible-light photoredox:

- Decarboxylative arylation: ArX + RCO₂H + Pd / Ir-photocat /
  light → ArR. Replaces stoichiometric organometallics with
  carboxylic acids.
- α-arylation of amines via radical relay.
- Spurred a rethink of cross-coupling under mild conditions.

## Industrial scale

**Atorvastatin** (Pfizer's Lipitor — peak $13B/yr) — Negishi
on the pyrrole core.
**Losartan** (Merck) — Suzuki + Negishi steps in the
biphenyl-tetrazole sidearm.
**Imatinib** (Novartis Gleevec) — Buchwald-Hartwig in the
piperazine arm.

> Half of all medicinal-chemistry C-C and C-N bond
> disconnections in 2025 trace back to a Pd-catalysed step.

## Try it in the app

- **Reactions tab** → load *Suzuki coupling*, *Heck*,
  *Buchwald-Hartwig amination* — see explicit catalyst-cycle
  mechanism rendering.
- **Tools → Retrosynthesis…** → target SMILES with biaryl /
  C-N bonds → see Suzuki + Buchwald disconnections appear in
  the top-K results.
- **Glossary** → search *Suzuki coupling*, *Oxidative
  addition*, *Reductive elimination*, *Transmetalation*,
  *Buchwald-Hartwig amination*.

Next: **C–H activation — the modern functionalisation
toolbox**.
