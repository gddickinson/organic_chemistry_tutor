# Common organic synthons

A **synthon** is an idealised reactive species used during
retrosynthetic analysis. It might be a cation, anion, or
radical that doesn't actually exist in solution but maps
onto a real **synthetic equivalent** (a stable reagent that
behaves like it).

## Common synthons + their equivalents

| Synthon | Synthetic equivalent (real reagent) |
|---------|-------------------------------------|
| **CH₃⁻** (methyl anion) | MeMgBr, MeLi, MeCu, Me₂CuLi |
| **CH₃⁺** (methyl cation) | MeI, MeOTf, Me₂SO₄ |
| **CH₃·** (methyl radical) | (Me)₂Hg + hν or AIBN-style |
| **R-C≡C⁻** (acetylide) | RC≡CH + n-BuLi or NaNH₂ |
| **PhCH₂⁻** (benzyl anion) | PhCH₂MgCl, BnLi |
| **PhCH₂⁺** (benzyl cation) | BnBr, BnOTs |
| **HC≡C⁻** (acetylide H) | HC≡CH + n-BuLi |
| **CN⁻** | NaCN, KCN, TMSCN |
| **CHO⁻** (formyl anion) | DMF + n-BuLi (formyl trapping) |
| **CO₃²⁻** (carbonate dianion) | Cs₂CO₃, K₂CO₃ |
| **CO₂⁻** (carboxylate) | CO₂ in THF after Grignard / acetylide attack |
| **CO+** (acylium) | acid chloride / anhydride + Lewis acid |
| **R₂C=CH⁻** (vinyl anion) | vinyl Grignard, vinyl lithium |
| **R-CH=CH₂ → α-anion (allyl⁻)** | allyl-MgBr, allyl-Sn(R)₃ |

## d¹ + a¹ synthons

Notation:

- **d** = donor (nucleophilic) site.
- **a** = acceptor (electrophilic) site.
- Number = atom from the heteroatom.

Examples for an aldehyde RCHO:

- **a¹** synthon — RCHO is electrophile at C1; reacts with
  any nucleophile (Grignard, hydride, enolate).
- **d¹** synthon — RCHO would be a nucleophile at C1 —
  unnatural. Solution: **dithiane umpolung** (Corey-Seebach).

## Umpolung (polarity inversion)

A natural d¹ aldehyde becomes a d¹ anion via an alkyl
dithiane:

```
RCHO + HS-CH₂-CH₂-SH → 1,3-dithiane (C1 sp³, two S at
                                     2,2)
1,3-dithiane + n-BuLi → 1,3-dithiane Li (C1 carbanion!)
+ R'X → 1,3-dithiane R-R' → (HgCl₂ or Hg(ClO₄)₂)
                          → R-CO-R'
```

Net: turned an electrophilic aldehyde C into a nucleophilic
C — formed a new C-C bond.

Other umpolung tools:

- **Cyanide + acid (Stetter)** — α-keto C as nucleophile.
- **NHC catalysis** (benzoin condensation) — same.
- **TMS-cyanide** + Lewis acid — add CN to a carbonyl,
  reverse polarity.
- **Vinyl epoxides** — open to allyl anion equivalent.

## Frequent retrosynthetic disconnections

For a target T, identify:

- **C-C bond between EWG-α and adjacent C** → aldol /
  Mannich / Michael disconnection.
- **C-C between aryl + sp²** → Suzuki / Negishi.
- **C-C-O linker** → Williamson / Mitsunobu.
- **C-N to amine** → reductive amination / Buchwald.
- **C-CO-O** → ester formation / acyl chloride coupling.
- **C-C in α-arylation / α-alkylation** → enolate +
  electrophile.

## Working through a real target

Target: ibuprofen (2-(4-isobutylphenyl)propanoic acid).

```
PhC(CH₃)(H)COOH retro-disconnect at α-carbon:
     PhCH(CH₃)X synthon (where X = good LG)
         + carbonate/CO₂ as the COOH source
   
Or: aryl Grignard attack on a 2-bromopropanoate?
Or: BHC's modern route — Friedel-Crafts of isobutylbenzene
    with 2-chloropropanoyl chloride, then carbonylation.
```

Synthons aren't a shortcut to thinking — they ARE the
thinking, made formal.

## Try it in the app

- **Tools → Retrosynthesis…** → input a target SMILES →
  see template-based disconnection suggestions, often
  reflecting the synthons described here.
- **Glossary** → search *Synthon*, *Synthetic equivalent*,
  *Umpolung*, *Retrosynthesis*.

Next: **Functional group interconversions table**.
