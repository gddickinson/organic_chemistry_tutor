# Phosphine chemistry intro

Phosphorus is below nitrogen in the periodic table —
similar 5-electron valence shell, but bigger, softer, more
nucleophilic. **Phosphines** (PR₃) are versatile in
synthesis + catalysis.

## Phosphines as ligands

The dominant use: as **σ-donor / π-acceptor ligands** for
transition metals.

| Ligand | Substituents | σ-donor | π-acceptor | Use |
|--------|--------------|---------|------------|-----|
| PMe₃ | small alkyl | strong | weak | small-Pd Suzuki |
| PEt₃ | small alkyl | strong | weak | mostly historic |
| PCy₃ | bulky alkyl | very strong | weak | bulky → favours mono-coordination |
| PtBu₃ | very bulky | strong | weak | high-T couplings |
| PPh₃ | aryl | medium | medium | classic Heck / Suzuki |
| P(o-Tol)₃ | bulky aryl | medium | medium | improves Heck rate |
| BINAP | chiral biaryl | medium | medium | Noyori asymmetric H₂ |
| dppe / dppp / dppf | bidentate | medium | medium | Pd / Ni |
| XPhos / SPhos / RuPhos | bulky biaryl | strong | medium | Buchwald amination |
| PtBu₂(o-biphenyl) | very bulky | strong | medium | difficult ArCl couplings |
| TPPTS | sulfonated aryl | medium | medium | water-soluble (Suzuki + Wittig) |

## Phosphines as reagents

### Wittig

PPh₃ + RX → phosphonium salt → base → ylide →
olefination (lesson 33).

### Mitsunobu

PPh₃ + DIAD + R-OH + Nu-H → R-Nu (lesson 43).

### Appel halogenation

PPh₃ + CX₄ + ROH → RX (lesson 44).

### Staudinger reduction

```
RN₃ + PPh₃ → R-N=PPh₃ → + H₂O → R-NH₂ + Ph₃P=O
```

Mild, chemoselective azide → amine. Tolerates many FGs.

### Aza-Wittig

```
R-N=PPh₃ + R'CHO → R-N=CHR' + Ph₃P=O
```

Imines from azides + carbonyls; useful when direct
condensation fails.

## Phosphine oxidation states

- **R₃P** — phosphine (P(III)).
- **R₃P=O** — phosphine oxide (P(V)).
- **R₃P=CR'R''** — ylide (P(V), formally).
- **R₃P=NR'** — phosphinimide / phosphazene.
- **R₃P-X⁺ X⁻** — phosphonium salt (P(V)).
- **R₂P-PR₂** — diphosphine (P(II)).
- **PR₅** — pentavalent phosphorus (rare; ylids, halides).

Most reactions cycle phosphine ↔ phosphine oxide. Recycling
phosphines back from oxides is hard (industry largely
discards).

## Air sensitivity

Most phosphines (PMe₃, PEt₃, PCy₃, PtBu₃) **oxidise in air**
to the phosphine oxide. Store under N₂ / Ar.

PPh₃ + bulky aryl phosphines (XPhos etc.) are usually
**bench-stable** for short periods.

Buchwald 2nd-generation pre-catalysts (XPhos-Pd-G2,
SPhos-Pd-G3) are air-stable Pd-phosphine complexes —
just-add-substrate.

## Phosphine basicity

```
Tolman cone angle θ
PMe₃:   118°
PEt₃:   132°
PPh₃:   145°
PCy₃:   170°
PtBu₃:  182°
P(C₆F₅)₃: 184° (electron-poor aryl)
```

Larger cone angle → more steric bulk → favours mono-
coordination + active species in catalysis.

## Phosphine pKa (conjugate acid)

```
PH₃:    -14    (very weak base!)
PMe₃:    8.65
PEt₃:    8.69
PCy₃:    9.7
PtBu₃:  11.4
PPh₃:    2.7   (much weaker than alkyl phosphines)
```

Aryl phosphines are weaker bases (resonance stabilises
the lone pair into the aromatic ring).

## Phosphazene superbases (Schwesinger)

```
P1 = (Me₂N)₃P=NR     pKa(MeCN) ~ 27
P2 = ...             pKa ~ 33
P3 = ...             pKa ~ 38
P4 = ...             pKa ~ 42
```

Phosphazene bases (P1-P4) are organic, non-nucleophilic,
super-strong bases. Used in cases where DBU or LDA
aren't strong enough but you don't want a metal alkoxide.

## Phosphate + phosphonate chemistry (related)

Beyond phosphines:

- **Phosphate esters** (PO₄) — DNA, RNA, ATP, phospholipid.
- **Phosphonates** (R-PO(OR')₂) — HWE reagents (lesson 33).
- **Phosphites** ((RO)₃P) — antioxidants, ligands, Michaelis-
  Arbuzov reaction.
- **Bisphosphonates** (HOOP(R)PO(OH)₂) — osteoporosis drugs
  (alendronate, zoledronate).

## Try it in the app

- **Tools → Lab reagents…** → look up PPh₃, PCy₃, BINAP,
  XPhos for hazards + storage + use cases.
- **Reactions tab** → Suzuki + Wittig + Mitsunobu all
  involve phosphines.
- **Glossary** → search *Phosphine*, *Triphenylphosphine*,
  *BINAP*, *Tolman cone angle*, *Buchwald ligand*.

Next: **Sulfur ylide (Corey-Chaykovsky) chemistry**.
