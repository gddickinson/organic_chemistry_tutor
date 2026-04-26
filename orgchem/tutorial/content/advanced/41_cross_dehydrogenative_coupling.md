# Cross-dehydrogenative coupling (CDC)

**Cross-dehydrogenative coupling** forms a new C-C (or
C-X) bond between two C-H partners + an oxidant — the
"dehydrogenative" part is the loss of 2 H atoms as
H₂O / oxidised by-product. Atom-economical because no
pre-functionalisation is needed.

## The reaction

```
R-H  +  R'-H  +  oxidant  +  catalyst  →  R-R'  +  H₂O (or 2 H₂O)
```

Compared to traditional cross-coupling:

```
R-X + R'-M + Pd cat. → R-R' + M-X (Pd waste, salt waste)
                    (Suzuki / Negishi / etc. — needs pre-func.)
```

CDC skips the pre-functionalisation: directly join two
C-H partners.

## Three flavours

### CDC-α-amino C-H (Li, Doyle; 2008+)

```
N-Boc amine (α-CH) + R-H (acidic; e.g. malonate, indole)
                  + oxidant (DDQ, Cu/peroxide) + cat. →
                  α-arylated or α-alkylated amine
```

Mechanism:

1. Amine + oxidant → iminium ion (loss of α-H).
2. Iminium + nucleophile → α-functionalised amine.

### Aryl–aryl CDC (Buchwald, Glorius)

```
ArH + ArH' + Pd cat. + oxidant (Ag, Cu, peroxide) →
                                          Ar-Ar'
```

Direct biaryl coupling — both arenes from C-H. Slower +
more challenging than Suzuki; needs an electron-rich +
electron-poor pair for selectivity.

### α-Acyl CDC

```
ketone (α-CH) + arene (CH) + oxidant + Pd / Cu cat. →
                                         α-aryl ketone
```

Same as α-arylation of carbonyls but starting from C-H
not pre-arylated.

## Photoredox CDC

Visible-light photoredox + HAT catalyst → CDC at
benzylic, α-amino, α-O C-H bonds:

```
benzylic-H + RCHO + Ir(ppy)₃ + decatungstate-HAT + light
                                    → α-aryl alcohol
```

Mild, selective, often complementary to traditional CDC.

## Asymmetric CDC

Several systems combine CDC with chiral catalysis:

- **Chiral Cu / chiral phosphate** + α-amino CDC →
  chiral α-aryl amine.
- **Chiral Ni / Ir-photoredox** → chiral α-arylated
  carbonyls.
- **Chiral Pd** + asymmetric C-H functionalisation →
  chiral α-aryl ketones.

By 2025, asymmetric CDC is a major frontier; ~ 50 papers
per year.

## Limits

- **Lower yields** typical (40-70 %) vs traditional cross-
  coupling (70-95 %).
- **Stoichiometric oxidant waste** — atom-economical only
  for the C-H bonds, but the oxidant (DDQ, Cu(OAc)₂,
  PhI(OAc)₂, Selectfluor) is consumed.
- **Selectivity** — multiple C-H sites compete.

## Industrial uses

CDC remains mostly academic, but:

- **Late-stage functionalisation** in pharma drug
  development.
- **Photoredox CDC at SK Bioscience, Pfizer, AbbVie**
  for SAR exploration.
- **GSK's flow CDC** for kg-scale α-arylation.

## Compared to other modern methods

| Method | Inputs | Pros | Cons |
|--------|--------|------|------|
| Suzuki | ArX + ArB(OH)₂ | clean, robust | pre-fn ArX |
| C-H borylation + Suzuki | ArH → ArBpin → Ar-Ar' | flexible | 2 steps |
| CDC | ArH + ArH | step-economy | yield, oxidant waste |
| Photoredox CDC | ArH + ArH + light | mild | substrate scope |

## Try it in the app

- **Reactions tab** → look at any CDC-style reaction (if
  seeded; α-arylation of indole + aldehyde is the classic).
- **Glossary** → search *CDC*, *Cross-dehydrogenative
  coupling*, *α-Amino C-H functionalisation*, *Photoredox
  CDC*.

Next: **Functional group tolerance design**.
