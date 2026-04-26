# Reduction methods — comparing the toolbox

Reduction is anything that adds H₂ or removes O — formally
adding electrons to a substrate. Modern organic chemistry
has dozens of reducing agents; the trick is choosing the
right one for the right functional group.

## The reagent ladder (mild → strong)

| Reagent | Reduces | Survives |
|---------|---------|----------|
| H₂ / Pd-C | C=C, C≡C, ArNO₂, RN₃, aryl X | C=O, COOR, COOH |
| H₂ / Lindlar | C≡C → cis C=C only | C=C, C=O, COOR |
| H₂ / Pt | All H₂/Pd targets + ArOH | C=O, COOR |
| Na / NH₃ (Birch) | aromatic → 1,4-cyclohexadiene; C≡C → trans C=C | most |
| NaBH₄ | C=O (ald + ket) | COOR, COOH, CN, ArNO₂ |
| NaBH(OAc)₃ | iminium (red. amination) | most |
| NaBH₃CN | iminium at pH 6-8 | most |
| LiBH₄ | C=O + COOR | COOH, CN |
| DIBAL (-78 °C) | COOR → RCHO; CN → RCHO | C=C, ArR |
| LiAlH₄ | C=O, COOR, COOH, CONR₂, CN, RNO₂, RX | C=C |
| Red-Al | similar to LAH but milder | |
| L-Selectride | bulky stereoselective ketone reduction | most |
| Sm I₂ (SmI₂) | ketyl-radical chemistry | wide functional-group tolerance |
| Bouveault-Blanc (Na, EtOH) | COOR | C=C |
| Zn / HCl | ArNO₂ → ArNH₂ | most |
| Sn / HCl | ArNO₂ → ArNH₂ | most |
| Fe / HCl | ArNO₂ → ArNH₂ | most |
| Wolff-Kishner (NH₂NH₂, KOH, Δ) | C=O → CH₂ | basic conditions |
| Clemmensen (Zn-Hg, HCl, Δ) | C=O → CH₂ | acidic conditions |
| Mozingo (HSCH₂CH₂SH; Raney Ni) | C=O → CH₂ | |

## Catalytic hydrogenation

`H₂` + a transition-metal catalyst:

- **Pd-C, PtO₂ (Adams), Rh-C** → most reductions.
- **Lindlar (Pd-CaCO₃-PbO + quinoline)** → poisoned
  catalyst; alkyne stops at cis alkene.
- **Raney Ni** → cheap; works for nitrile + alkene + benzyl
  / Cbz removal.
- **Pearlman's (Pd(OH)₂)** → hindered debenzylation.
- **Crabtree (Ir)** → directed hydrogenation by polar
  group → high diastereoselectivity.
- **Asymmetric H₂** — Rh / DIPAMP, Ru / BINAP (covered in
  the advanced curriculum).

Mechanism: substrate + H₂ → both adsorb to metal → syn
addition → release.

## Hydride reductions — selectivity by reagent

The aluminium / boron hydride family ranks by reactivity:

```
LiAlH₄  >  Red-Al  >  LiBH₄  >  DIBAL  >  NaBH₄  >  NaBH(OAc)₃  >  NaBH₃CN
    ↓ reactivity decreases ↓
    ↑ functional-group tolerance increases ↑
```

NaBH₄ in MeOH at 0 °C reduces aldehydes + ketones cleanly +
leaves esters / amides / nitriles untouched.

LiAlH₄ in dry THF reflux reduces almost everything except
isolated C=C (alkenes survive).

DIBAL is the trick reagent — at -78 °C with **one
equivalent**, an ester only takes one hydride + stops at
the aldehyde. Two equivalents → all the way to alcohol.

## Stereoselective reductions

- **Felkin-Anh model** — for ketones with adjacent
  stereocentres, the largest group goes anti to the
  incoming hydride.
- **CBS reduction** (Corey-Bakshi-Shibata, 1987) — chiral
  oxazaborolidine catalyst + BH₃; > 95 % ee for prochiral
  ketones.
- **Noyori asymmetric H₂** — Ru / BINAP / diamine.
- **Enzymatic** — alcohol dehydrogenases (ADHs) reduce
  ketones to single enantiomer alcohols.

## Functional-group-specific tactics

### C=O → CH₂ (deoxygenate)

- **Wolff-Kishner** (NH₂NH₂, KOH, Δ) — basic conditions;
  works for ketones + aldehydes; mechanism through
  hydrazone → diazo → loss of N₂.
- **Clemmensen** (Zn-Hg / HCl) — acidic; less general but
  works on acid-stable substrates.
- **Mozingo** (form thioacetal + Raney Ni) — neutral; for
  acid + base sensitive substrates.
- **TsNHNH₂ + NaBH₄** (Caglioti) — milder than Wolff.

### COOH → CH₃ (rare)

Usually go via COOH → COOR → RCH₂OH → RCH₃. No direct one-
pot reagent; involves a halogenation + radical reduction
or LiAlH₄ then dehydroxylation.

### ArNO₂ → ArNH₂

Most popular: H₂ / Pd-C in EtOH. Or Sn / HCl, Fe / HCl /
EtOH for cheap scale-up. SnCl₂ / EtOH is the lab favourite
when you can't use H₂.

### C=C → CH-CH (hydrogenate without touching anything)

H₂ / Pd-C is the workhorse. Lindlar for alkynes only. Don't
use LiAlH₄ — it won't reduce isolated alkenes.

### Aromatic ring → cyclohexane

- **Rh-Al₂O₃** at high P + T (most efficient).
- **PtO₂** in AcOH.
- **Birch** does NOT fully reduce — gives 1,4-dihydro.

## Try it in the app

- **Reactions tab** → load *NaBH₄ reduction* (seeded) for
  a 1-step hydride-transfer mechanism.
- **Tools → Lab reagents…** → look up NaBH₄, LiAlH₄,
  DIBAL, Pd/C — see hazards + storage + handling.
- **Glossary** → search *Reduction*, *Hydride*,
  *Hydrogenation*, *Lindlar catalyst*, *Wolff-Kishner
  reduction*, *Clemmensen reduction*.

Next: **Oxidation methods — comparing the toolbox**.
