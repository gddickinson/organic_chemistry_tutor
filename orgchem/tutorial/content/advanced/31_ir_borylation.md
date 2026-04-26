# Ir-catalysed C-H borylation (Ishiyama)

The Hartwig-Ishiyama C-H borylation (2002) installs a Bpin
group directly on an aromatic C-H without prior
halogenation or directing group. The product Ar-Bpin then
undergoes Suzuki coupling for the next step.

## The reaction

```
ArH + B₂pin₂ + Ir(cod)(OMe) / 4,4'-di-tBu-bpy → Ar-Bpin + HBpin (or pinacol-borane)
                                              (catalyst: ~ 0.5 mol % Ir)
```

Conditions:

- **Substrate**: simple arene (no DMG required).
- **Boron source**: B₂pin₂ (pinacol diborane; HBpin works
  too).
- **Catalyst**: [Ir(cod)(OMe)]₂ + 4,4'-di-tBu-2,2'-
  bipyridine (or dmpe).
- **Solvent**: hexane, THF, octane, or neat.
- **T**: 80-120 °C (or rt for simple substrates).

## Selectivity — sterics, NOT electronics

The most distinctive feature: Ir-borylation goes for the
**most-accessible** C-H bond. **Steric, not electronic**
control:

```
toluene → meta + para borylation (NOT ortho; ortho is hindered by Me)
1,3-disubstituted benzene → C5 borylation (between two subs.; least hindered)
naphthalene → 2-borylation (β-position; less hindered than α)
```

This is **complementary to electrophilic aromatic
substitution** (which is electronics-controlled, ortho /
para → activator) + Pd C-H functionalisation (DMG
directs).

## Substrate scope

- Most arenes work; ortho-directed-by-Me restriction can
  be useful + a limit.
- Heteroarenes (pyridine, thiophene, furan, indole) work
  with selectivity that depends on electronics + sterics.
- Polycyclic + naphthyl substrates work cleanly.

Excludes:

- Substrates that strongly bind Ir (sulfides, free amines)
  → catalyst poisoning.
- Highly electron-rich (aniline, phenol) → over-borylation.

## After-borylation chemistry

The Ar-Bpin is the Suzuki partner par excellence:

```
ArBpin + Ar'X + Pd / phosphine + base → Ar-Ar'  (Suzuki)
ArBpin + R-X (alkyl halide) + Ni / Pd cat. → Ar-R
ArBpin + R'COOH + Cu cat. + air → Ar-O-COR'  (oxidation to ester via Chan-Lam-like)
ArBpin + Pd / Cu / oxidant → ArOH (oxidation to phenol)
ArBpin + RNHR' + Cu cat. → ArNRR' (Chan-Lam amination)
```

Effectively gives you a "universal handle" to install
almost anything at any unhindered arene C-H.

## Practical recipe

```
1. Combine arene (1 eq) + B₂pin₂ (1.1 eq) + [Ir(cod)(OMe)]₂
   (0.5 mol %) + dtbpy (1 mol %) in hexane (or no solvent).
2. Heat to 80 °C, stir 4-12 h.
3. Concentrate; column or recrystallise to get Ar-Bpin.
```

Purification can be tricky — Ar-Bpin sometimes co-elutes
with HBpin byproduct.

## Asymmetric C-H borylation

For prochiral substrates, chiral phosphine ligands
(P,N-pyridyl) → enantioselective borylation. Hartwig +
others have demonstrated > 95 % ee.

## Late-stage functionalisation in pharma

Pfizer, Genentech, AstraZeneca + others use Ir-borylation
to install Bpin on advanced drug intermediates:

- **Late-stage SAR** — install Bpin → couple with various
  Ar-X to explore SAR around an arene without redoing the
  whole synthesis.
- **Process scale-up** — Ir-borylation has been scaled to
  100 kg+ (e.g. Pfizer pirtobrutinib).
- **Tritium / deuterium labelling** — Ir-D borylation
  installs DBpin → swap for D-labelled product.

## Limits

- **Cost** — Ir is ~ $200/g; even 0.5 mol % adds up at
  scale.
- **Removal** — sub-ppm Ir spec for APIs requires careful
  work-up.
- **Regioselectivity** — sterics-driven means para +
  meta only on 1,2-disubstituted arenes; can't get ortho.
- **Heteroatoms** — sulfur + free amines are catalyst
  poisons.

## Try it in the app

- **Reactions tab** → look at *Suzuki coupling* (seeded)
  for the downstream step after C-H borylation.
- **Tools → Retrosynthesis…** → for late-stage Ar
  functionalisation, C-H borylation is the modern entry
  point.
- **Glossary** → search *C-H activation*, *Ir-catalysed
  borylation*, *Hartwig-Ishiyama*, *Bpin*, *Late-stage
  functionalisation*.

Next: **Lithium chemistry — directed ortho-metalation**.
