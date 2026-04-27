# Allostery and cooperativity

Allosteric regulation is how cells fine-tune protein
function in real time.  An allosteric protein has at
least two binding sites that talk to each other — binding
at one site changes affinity or activity at the other.

## Hemoglobin — the textbook allosteric protein

Hemoglobin binds 4 oxygens cooperatively.  Plot saturation
vs pO₂ → **sigmoidal** S-shaped curve, not the hyperbolic
binding curve you'd get from independent sites.

Why this matters physiologically:

- In lungs (pO₂ ~ 100 mmHg), hemoglobin is ~ 98 %
  saturated.
- In tissues (pO₂ ~ 40 mmHg), hemoglobin drops to ~ 75 %
  saturation.
- The sigmoidal shape means a **larger fraction of bound
  O₂ is delivered** for a given pressure drop than a
  hyperbolic carrier would deliver.

Hemoglobin's cooperativity gives mammals an O₂-delivery
system optimised for the actual lung-vs-tissue pressure
gradient.

## The Hill coefficient

Quantifies cooperativity:

```
Y = ([L]^n) / (K^n + [L]^n)
```

where **n** is the Hill coefficient.

- **n = 1** — no cooperativity; classic Michaelis-Menten
  hyperbola.
- **n > 1** — positive cooperativity (binding helps
  binding).
- **n < 1** — negative cooperativity (binding hinders
  further binding).

Hemoglobin's n ≈ 2.8 (between 1 + 4, never exactly the
number of subunits).  Phosphofructokinase-1 (the
glycolysis pacemaker) has n ≈ 4.

## Two models of allostery

### MWC — Monod-Wyman-Changeux (1965)

The "concerted" model.  All subunits switch
**simultaneously** between two conformational states:

- **T (tense)** — low-affinity, dominant in absence of
  ligand.
- **R (relaxed)** — high-affinity, stabilised by ligand
  binding.

Cooperativity arises because each ligand binding shifts
the T ↔ R equilibrium toward R, increasing affinity for
the *next* ligand.  Symmetry is preserved — all subunits
in T or all in R, never mixed.

### KNF — Koshland-Némethy-Filmer (1966)

The "sequential" model.  Subunits switch independently;
ligand binding induces a conformational change in the
bound subunit, which propagates through interfaces to
alter neighbouring-subunit affinity.

Reality is a mix.  Hemoglobin fits MWC quite well; many
other allosteric enzymes (ATCase, phosphofructokinase)
are intermediate.

## Allosteric activators + inhibitors

Allosteric ligands at sites separate from the substrate
pocket can:

- **Activate** — stabilise the R state, increase Vmax or
  decrease Km.
- **Inhibit** — stabilise the T state, decrease Vmax or
  increase Km.

Classic examples:

- **2,3-BPG** binds hemoglobin at a site between the β-
  subunits + stabilises T → right-shifts the O₂ binding
  curve → unloads more O₂ in tissues.  Up-regulated at
  altitude + in chronic anaemia.
- **CO₂ + protons (Bohr effect)** — also stabilise T;
  hemoglobin delivers more O₂ to tissues with high
  metabolic activity (acidic + CO₂-rich).
- **CO + carboxyhaemoglobin** — binds with 250× higher
  affinity than O₂ + locks hemoglobin in R → carbon-
  monoxide poisoning.

## Allosteric drug examples

Allosteric drugs offer two big advantages over orthosteric
ones:

- **Subtype selectivity** — allosteric sites are less
  conserved than orthosteric pockets.
- **Ceiling effect** — a positive allosteric modulator
  (PAM) does nothing without endogenous ligand; can't
  over-activate.

Examples:

- **Benzodiazepines** — PAMs of GABA-A receptor at a site
  distinct from GABA itself.
- **Cinacalcet** — PAM of the calcium-sensing receptor;
  treats secondary hyperparathyroidism.
- **Maraviroc** — allosteric antagonist of CCR5 (HIV
  co-receptor).
- **Plasma kallikrein PAM** — under development for
  hereditary angioedema.

## The kinase-cascade ultrasensitivity

Cooperativity isn't just for traditional allosteric
proteins.  The MAPK cascade behaves like a switch because:

- Each kinase has **dual phosphorylation sites** (TXY
  motif in MAP kinases) — both must be phosphorylated for
  activity.  Hill-like cooperativity at each tier.
- Three sequential tiers compound the cooperativity.

Combined effect: input-output ultrasensitivity that
behaves like a sharp threshold (Huang + Ferrell 1996,
*Xenopus* MAPK switch).

This is one example of the broader principle: **biology
uses cooperativity wherever it needs sharp on-off
decisions** rather than smooth analogue responses.

## Try it in the app

- **OrgChem → Macromolecules → Proteins** — hemoglobin +
  ATCase + other allosteric structures (if seeded).
- **Cell Bio → Signalling** — kinase cascades exhibit
  ultrasensitivity through cooperativity.
- **Pharm → Receptors** — `gaba-a` entry (benzodiazepines
  are GABA-A PAMs).
- **Pharm → Drug classes** — `benzodiazepines` entry.

Next: **Glycolysis and the citric-acid cycle**.
