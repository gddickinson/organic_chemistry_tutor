# How to read a chemistry paper + ELN best practices

Two of the most under-taught skills for beginning organic
chemists: efficiently reading the literature, and keeping a
notebook that someone else can follow.

## Reading a chemistry paper

The literature has its own grammar. A typical methodology /
total-synthesis paper has:

```
Title → Abstract → Graphical abstract → Introduction →
Results & Discussion → Conclusion → SI (procedures + spectra)
```

### Don't read linearly

Skim in this order:

1. **Title + abstract** (30 sec) — what's the punchline?
2. **Graphical abstract** + first scheme (1 min) — what
   transformation? what catalyst?
3. **First page of results** + Table 1 — substrate scope?
4. **Conclusion** — what is the author's big claim?
5. **SI experimental section** for the specific compound /
   reaction you care about.
6. **Introduction** last — context + motivation, only when
   you're hooked.

### Reading the SI

The Supporting Information is where the real chemistry
lives. For each compound:

```
General procedure: …
Compound 5: 1H NMR (400 MHz, CDCl3) δ 7.42 (m, 5H), 5.18
(s, 2H), 3.65 (s, 3H); 13C NMR (101 MHz, CDCl3) δ 170.2,
138.5, 128.7, 128.3, 128.0, 67.0, 51.9; HRMS (ESI) m/z
[M+H]+ calcd for C9H11O3 167.0708, found 167.0710.
```

Decode:

- **400 MHz** — proton frequency of the NMR magnet.
- **CDCl₃** — deuterated solvent (chloroform-d).
- **δ 7.42 (m, 5H)** — chemical shift in ppm, multiplicity,
  integration. m = multiplet, s = singlet, d = doublet, t
  = triplet, q = quartet, dd = doublet of doublets.
- **HRMS (ESI)** — high-resolution mass spec, electrospray
  ionisation. `Calcd` is the theoretical exact mass.
  `Found` should match within 5 ppm.

### Critical reading questions

- **Yield reported on what scale?** (1 mg vs 1 g matters.)
- **Number of substrates?** A scope table of 30 successful
  + 0 failed substrates is suspicious — papers omit failed
  scope.
- **Catalyst loading?** 5 mol % beats 30 mol %; 0.05 mol %
  beats 5 mol %.
- **Selectivity reported as ee or de?** What method (chiral
  HPLC, NMR with shift reagent)?
- **Solvent + temperature** — ambient is great, -78 °C is
  scary, > 100 °C suggests slow reaction.
- **Mechanistic claims** vs experimental evidence — DFT-only
  proposals are weaker than KIE or labelling experiments.

## ELN (electronic notebook) best practices

The notebook records what actually happened. Future-you (and
PIs / collaborators / patent attorneys / safety officers)
read it years later. **Write for them.**

### What every entry needs

1. **Date** + **your initials** + **page number**.
2. **Reaction scheme** drawn out — substrate, reagents,
   product structure with stereo.
3. **Stoichiometry table**: limiting reagent, mass, mmol,
   equivalents, MW. Even if you don't use it, write it.
4. **Procedure** — step-by-step, in past tense:
   "Salicylic acid (1.0 g, 7.2 mmol, 1.0 eq) was dissolved
    in CH₂Cl₂ (20 mL) at 0 °C; acetic anhydride (0.74 g,
    7.2 mmol, 1.0 eq) was added dropwise over 5 min;
    DMAP (90 mg, 0.7 mmol, 0.1 eq) was added and the
    reaction was stirred at 0 → rt over 4 h."
5. **Workup** — quench, extraction, drying, concentration.
6. **Purification** — column? Crystallisation? Solvent?
7. **Result** — yield (mg + mmol + %), TLC Rf, NMR
   highlights ("clean by ¹H NMR; matches lit").
8. **Observations** — colour change, exotherm, gas
   evolution, anything weird.
9. **Hazards** — note pyrophorics (n-BuLi), peroxide
   formers (THF), water-reactive (NaH), carcinogens.

### What kills lab books

- **No mass — only "added a spatula tip"** — irreproducible.
- **No mention of what failed** — you'll repeat the failed
  attempt.
- **Stale entries with no follow-up** ("ran a column,
  couldn't separate; took an NMR, weird peaks; → set aside")
  — finish the entry with a decision (re-do, abandon,
  characterise differently).
- **Hand-drawn structures only** — agree on a digital
  drawing standard (ChemDraw, ChemAxon, OrgChem Studio
  drawing tool).

### Modern ELN platforms

- **Benchling** — cloud, real-time collaboration, free for
  academia.
- **LabArchives** — biology-leaning, popular in
  universities.
- **IDBS E-WorkBook** — pharma-grade, audit-trail.
- **Signals** + **Dotmatics** — drug-discovery focused.
- **OneNote / Notion / paper notebook + scanner** — works
  if disciplined.

Whatever you use, **back it up**. A laptop dying with 6
months of unbacked notes happens. Sync to cloud daily.

## Try it in the app

- **Tools → Drawing tool…** → sketch a reaction scheme to
  paste into your notebook.
- **Tools → Spectroscopy…** → predict NMR shifts to compare
  against your isolated compound.
- **Glossary** → search *Yield*, *Equivalents*, *NMR
  multiplicity*, *HRMS*.

Next: **Common transformations cheat-sheet — synthesis at a
glance**.
