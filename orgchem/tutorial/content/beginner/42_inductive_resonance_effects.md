# Inductive vs resonance effects on reactivity

A substituent on a molecule can donate or withdraw electron
density via two distinct channels: **through bonds (inductive)**
and **through π systems (resonance)**. Knowing which one
dominates lets you predict acidity, basicity, and orientation
of reactions.

## The two effects

### Inductive (σ) effect

Transmitted through σ bonds by polarisation. Falls off
rapidly with distance (~ ε^(−r)). Designated:

- **+I** (electron-donating) — alkyl groups (very weak
  donor, controversial; in modern view their effect is
  hyperconjugation rather than pure induction).
- **−I** (electron-withdrawing) — F, Cl, Br, OH, OR, NR₂,
  NO₂, CN, COR, COOR, SO₂R, NR₃⁺.

### Resonance (mesomeric, π) effect

Transmitted through π systems by overlap of p orbitals.
Acts at distance (1, 3, 5, ... atoms away through a
conjugated chain). Designated:

- **+M** (electron-donating into π) — OH, OR, NH₂, NR₂,
  SH, halogens (lone pair donates into π).
- **−M** (electron-withdrawing from π) — NO₂, CN, CHO,
  COR, COOR, SO₂R (empty π* or π acceptor).

A given substituent often has both effects — sometimes in
opposite directions.

## Substituent effect matrix

| Group | I | M | Net effect on aromatic ring |
|-------|---|---|------------------------------|
| –NH₂, –NR₂ | −I (weak) | +M (strong) | Strongly activating |
| –OH, –OR | −I (moderate) | +M (strong) | Activating |
| –NHCOR (acylamide) | −I | +M (moderate) | Activating |
| –F, –Cl, –Br, –I | −I (strong) | +M (weak) | Slightly deactivating but ortho/para directing |
| –CHO, –COR | −I | −M | Deactivating, meta directing |
| –COOR, –COOH | −I | −M | Deactivating, meta directing |
| –CN | −I | −M | Deactivating, meta directing |
| –NO₂ | −I | −M | Strongly deactivating, meta directing |
| –NR₃⁺ | −I (strong) | none | Deactivating, meta directing |
| –CH₃, –R | +I (weak hyperconjugation) | none | Slightly activating |

## Acidity examples

The more electron-withdrawing the substituent, the more
stable the conjugate base, the lower the pKa.

### Carboxylic acids

| Acid | pKa | Why |
|------|-----|-----|
| Acetic | 4.76 | reference |
| Chloroacetic | 2.86 | −I from Cl |
| Dichloroacetic | 1.29 | 2 × −I |
| Trichloroacetic | 0.65 | 3 × −I |
| Trifluoroacetic | 0.23 | 3 × −I (F stronger than Cl per atom) |

Inductive effect dominates here — F/Cl can't resonance-
donate into the COOH because their lone pairs would have to
go through 2 σ bonds.

### Phenols

| Phenol | pKa |
|--------|-----|
| Phenol | 9.95 |
| 4-Nitrophenol | 7.15 |
| 2,4-Dinitrophenol | 4.09 |
| 2,4,6-Trinitrophenol (picric acid) | 0.38 |

The −M nitro groups stabilise the phenoxide by delocalising
the negative charge onto the nitro oxygens — resonance does
the heavy lifting.

## Basicity examples

The more electron-rich the lone pair, the more basic the
amine.

| Amine | pKaH | Why |
|-------|------|-----|
| Ammonia | 9.25 | reference |
| Methylamine | 10.66 | +I from CH₃ |
| Aniline | 4.62 | N lone pair conjugates into the ring (less available) |
| 4-Nitroaniline | 1.0 | −M nitro pulls lone pair away |
| Diphenylamine | 0.78 | two rings drain the lone pair |

## EAS regiochemistry — why "ortho/para" vs "meta"

For electrophilic aromatic substitution on substituted
benzenes:

- **+M groups** (OH, OR, NR₂) stabilise the Wheland
  intermediate when E⁺ adds **ortho** or **para** because
  the positive charge can be delocalised onto the
  substituent's lone pair.
- **−M groups** (NO₂, CN) destabilise ortho/para attack
  (positive charge ends up on the carbon bearing the
  electron-withdrawing group); meta attack avoids this.

Halogens are an interesting case: −I (deactivating) but
+M (ortho/para directing) — the M effect controls
regiochemistry, the I effect controls overall rate.

## Hammett correlation

A quantitative framework: log(k/k₀) = ρ × σ where σ is the
substituent constant + ρ measures the reaction's
sensitivity to electronic effects. A positive ρ means the
reaction is helped by electron-withdrawing groups (e.g.
ester saponification); negative ρ means helped by donors.

## Try it in the app

- **Reactions tab** → look at *Nitration of benzene* +
  *Friedel-Crafts alkylation* — see the EAS Wheland
  intermediates that resonance arguments predict.
- **Tools → Lab calculator…** → *Acid-base* tab → compute
  pH for carboxylic acids of varying pKa.
- **Glossary** → search *Inductive effect*, *Resonance
  effect*, *Hammett equation*, *Activating group*,
  *Directing group*.

Next: **The Hammond postulate — TS resembles its nearest
endpoint**.
