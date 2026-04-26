# Olefin metathesis — Grubbs + Schrock + everything since

**Olefin metathesis** swaps the substituents on two alkenes:

```
R₁CH=CHR₂ + R₃CH=CHR₄  ⇌  R₁CH=CHR₃ + R₂CH=CHR₄
```

The 2005 Nobel Prize (Chauvin + Grubbs + Schrock) recognised
the discovery + understanding + utility of metathesis.

## The Chauvin mechanism

A metal carbene M=CHR₁ reacts with alkene R₂CH=CHR₃:

1. **[2+2] cycloaddition** → metallacyclobutane.
2. **Retro-[2+2]** in the *productive* direction — opens to
   give a new metal carbene M=CHR₂ + a new alkene R₁CH=CHR₃.
3. New M=CHR₂ enters next cycle.

The alkene + the carbene swap halves. Total bond reorganisation
is two C=C bonds in, two C=C bonds out — atom-economical.

## Catalyst families

### Schrock molybdenum + tungsten

`Mo(=NAr)(=CHR)(OR')₂` — first well-defined, well-behaved
metathesis catalyst (1990). High activity, exquisite selectivity,
but air-sensitive — needs glovebox.

### Grubbs ruthenium

The breakthrough for everyday lab use:

- **Grubbs G1** (1995) — `RuCl₂(=CHPh)(PCy₃)₂`. Air-stable.
- **Grubbs G2** (1999) — replaces one PCy₃ with a NHC (H₂IMes).
  Higher activity, broader scope.
- **Hoveyda-Grubbs HG2** — replaces the other PCy₃ with an
  ortho-isopropoxy-styrene chelate. Recyclable.
- **Stewart-Grubbs** + **Grela** + **Buchmeiser** — modern
  variants for Z-selectivity, stereoretention, low loading.

Ru tolerates more functional groups than Mo (esters, amines,
ketones) but is slower for sterically hindered alkenes.

## Variant reactions

| Reaction | Substrate | Product |
|----------|-----------|---------|
| **Cross metathesis (CM)** | A=B + C=D | A=C + B=D |
| **Ring-closing metathesis (RCM)** | diene tethered | ring + ethylene |
| **Ring-opening metathesis (ROM)** | strained ring | acyclic diene |
| **Ring-opening metathesis polymerisation (ROMP)** | strained ring | polymer |
| **Acyclic diene metathesis (ADMET)** | α,ω-diene | polymer + ethylene |
| **Ene-yne metathesis** | alkene + alkyne | conjugated diene |

## RCM — the workhorse for ring synthesis

5- to 8-membered + macrocyclic rings via:

```
diene + Grubbs → ring + CH₂=CH₂↑
```

Driven by entropy (ethylene escapes the flask). Now the
default macrocyclisation method — replaced challenging
intramolecular alkylation / acylation routes for medium and
large rings.

Famous targets: Eribulin, vancomycin, epothilones.

## Z- vs E-selective metathesis

Default Grubbs gives the E-alkene (more stable). **Z-selective
Ru catalysts** (Grubbs, 2011) place a bulky pyridine + adamantyl
N-aryl on Ru — the Z-alkene fits the metallacycle's narrow
pocket. Z-Hoveyda + **W oxo-alkylidenes** (Schrock) achieve >
95 % Z.

## ROMP — polymer chemistry

Norbornene + cyclooctadiene + cyclooctene + dicyclopentadiene
→ functionalised polymers via ROMP. Living polymerisation —
narrow PDI, controlled MW, block-copolymer access.

Industrial uses: **Vestenamer** (polyoctenamer rubber),
**Telene/Pentam** (poly-DCPD reaction injection moulding —
turbine blade housings, structural polymers).

## Limits + workarounds

- **Terminal alkenes preferred** — internal alkenes slower.
- **Trisubstituted alkenes** — slow; need higher loadings.
- **Tetrasubstituted** — generally inaccessible.
- **Styrene + 1,1-disubstituted** — challenging.
- **N-H amines, free thiols, alkynes** — kill catalysts;
  protect first.

## Try it in the app

- **Reactions tab** → load *Grubbs metathesis* (if seeded;
  if not, use the *Add reaction* dialog).
- **Tools → Retrosynthesis…** → for ring-containing targets,
  RCM disconnections appear in seeded retro templates.
- **Glossary** → search *Metathesis*, *Grubbs catalyst*,
  *Ring-closing metathesis*, *ROMP*.

Next: **Photochemistry deeper — modern photoredox + EnT
catalysis**.
