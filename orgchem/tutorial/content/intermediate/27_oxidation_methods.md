# Oxidation methods — comparing the toolbox

Oxidation removes electrons from a substrate or adds O.
Modern oxidising reagents range from cheap + harsh (CrO₃)
to mild + selective (DMP, Swern, TEMPO). Choose by
substrate, scale, and what other groups need to survive.

## The reagent ladder

### Alcohol → aldehyde / ketone (controlled)

| Reagent | Notes |
|---------|-------|
| **PCC** (pyridinium chlorochromate) | 1° → CHO (stops there). Mild. Cr waste. |
| **PDC** (pyridinium dichromate) | Similar to PCC; can over-oxidise in DMF. |
| **DMP** (Dess-Martin periodinane) | Modern workhorse: room T, neutral, no over-ox. Iodine-V. |
| **Swern** ((COCl)₂ / DMSO / Et₃N) | -60 °C; smelly Me₂S byproduct; gentle. |
| **Pfitzner-Moffatt** (DMSO + DCC) | Mild; HMPA-free Swern alternative. |
| **TPAP / NMO** (Ley) | Catalytic Ru; cleaner than chromium. |
| **TEMPO / NaOCl / KBr** (Anelli) | Catalytic; aqueous; scalable; works for unhindered 1° + 2° alcohols. |
| **Oppenauer** (Al(OiPr)₃ + acetone) | 2° → ketone via hydride transfer; complementary to MPV reduction. |

### Alcohol → carboxylic acid (over-oxidise 1°)

| Reagent | Notes |
|---------|-------|
| **Jones** (CrO₃ / H₂SO₄ / acetone) | Strong + cheap; goes COOH from 1°. |
| **KMnO₄** | Hot aqueous; cleaves at the same time. |
| **Pinnick / Lindgren** (NaClO₂ / NaH₂PO₄ / 2-methyl-2-butene) | Aldehyde → COOH selectively; doesn't touch alcohols. |
| **TEMPO / NaOCl₂ / NaOCl** | Catalytic; modern green-friendly. |

### Aldehyde → carboxylic acid

| Reagent | Notes |
|---------|-------|
| **Pinnick** | Most selective + safest — leaves alcohols / alkenes. |
| **Tollens** (Ag(NH₃)₂⁺) | Diagnostic + mild ("silver mirror" test). |
| **Fehling / Benedict** | Cu(II) → Cu₂O test for reducing sugars. |

### Alkene functionalisation

| Reagent | Product |
|---------|---------|
| **mCPBA** | epoxide |
| **DMDO** | epoxide; clean (Me₂CO byproduct) |
| **OsO₄ (cat.) / NMO** | syn 1,2-diol |
| **AD-mix-α / AD-mix-β** (Sharpless) | enantioselective syn diol |
| **OsO₄ + NaIO₄** (Lemieux-Johnson) | cleaves to two C=O via diol intermediate |
| **O₃ / Zn / AcOH** | oxidative cleavage to aldehydes |
| **O₃ / H₂O₂** | oxidative cleavage to COOH |
| **KMnO₄ (hot)** | oxidative cleavage to COOH |
| **PdCl₂ / CuCl₂ / O₂** (Wacker) | terminal alkene → methyl ketone |
| **mCPBA** then ROH | epoxide → trans diol or trans alkoxyalcohol |
| **Sharpless AE** (Ti(OiPr)₄ + DET + tBuOOH) | enantioselective epoxidation of allylic alcohols |
| **Jacobsen / Katsuki** (Mn(salen) + NaOCl) | enantioselective epoxidation of cis-alkenes |
| **Shi epoxidation** (chiral fructose-derived ketone + Oxone) | enantioselective epoxidation of trans + tri-substituted alkenes |

### Sulfur oxidation

| Reagent | Sulfide → ? |
|---------|-------------|
| **NaIO₄** | sulfoxide (1 oxidation) |
| **mCPBA** | sulfoxide or sulfone (control eq.) |
| **H₂O₂ / cat.** | sulfoxide |
| **OsO₄ / NMO** | sulfoxide |
| **Sharpless AS** (Ti / DET / tBuOOH) | enantioselective sulfoxide |

### Aromatic activation

| Reagent | Product |
|---------|---------|
| **DDQ / Chloranil** | dehydrogenation (cyclohexadiene → benzene) |
| **MnO₂** | benzylic alcohol → benzaldehyde |

### α-Oxidation of carbonyls

| Reagent | Product |
|---------|---------|
| **Br₂ / AcOH** (HVZ-like) | α-bromo |
| **NBS** | α-bromo / allylic bromo |
| **Davis' oxaziridine** | α-hydroxy |
| **MoOPH** (MoO₅·py·HMPA) | α-hydroxy |
| **Saegusa-Ito** (PdOAc₂ from TMS-enol ether) | α,β-unsat carbonyl |

### Baeyer-Villiger oxidation

```
R-CO-R' + RCO₃H → R-O-CO-R' (or R-CO-O-R')
```

Migratory aptitude: H > tert-C > sec-C > prim-C > Me. Use
mCPBA, peracids, or H₂O₂ + cat.

## Choosing chromium vs. modern oxidants

Chromium-based (PCC, PDC, Jones, CrO₃) reagents are:

- **Cheap + scalable** — historically dominant.
- **Toxic + carcinogenic + heavy-metal waste** — environmental
  + worker-safety concerns.

Modern alternatives (DMP, Swern, TEMPO, TPAP) replaced
chromium in pharma + academic labs since ~ 2000.

## Choosing Swern vs DMP vs TEMPO

| Method | Pros | Cons |
|--------|------|------|
| **Swern** | Cheap reagents, very mild, broad scope | -78 °C, smelly Me₂S |
| **DMP** | Room T, very clean, no foul smell | DMP itself is shock-sensitive (mild explosion risk if dry) |
| **TEMPO/NaOCl** | Cheapest catalytic, aqueous, scalable | Tends to go to COOH if not stopped |

For tonnes-scale process chemistry: TEMPO. Gram-scale lab:
DMP. Sensitive substrates with esters / amides / silyl
ethers: Swern.

## Try it in the app

- **Reactions tab** → load Wacker oxidation (if seeded),
  ozonolysis (if seeded), Baeyer-Villiger (if seeded).
- **Tools → Lab reagents…** → look up CrO₃ / DMP / Swern /
  mCPBA / OsO₄ — hazards + storage + standard procedures.
- **Glossary** → search *Oxidation*, *DMP (Dess-Martin
  periodinane)*, *Swern oxidation*, *Baeyer-Villiger*,
  *Sharpless asymmetric epoxidation*.

Next: **Alkene + alkyne addition reactions deeper**.
