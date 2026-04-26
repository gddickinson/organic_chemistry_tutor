# Allylation reactions — Tsuji-Trost, Mukaiyama, allyl-B

Adding an allyl group (CH₂=CH-CH₂-) to an electrophile is
a workhorse C-C bond-formation strategy. Three main
approaches: Pd-catalysed (Tsuji-Trost), Lewis-acid +
silane (Sakurai-Hosomi), and Grignard-like boron-allyl
(Brown).

## Tsuji-Trost allylation

```
allyl-X (X = OAc, OCO₂R, OPh, halide) + Nu-H + Pd(0) cat. →
                                          Nu-allyl + LG⁻
```

Pd(0) forms a **π-allyl Pd** intermediate that's
electrophilic. Nucleophile attacks at either end of the
allyl (regiochemistry-controllable).

### Mechanism

1. Pd(0) + allyl-OAc → π-allyl Pd + OAc⁻.
2. Nu attacks the less-substituted end (anti to Pd) →
   regenerates Pd(0) + allyl-Nu.

### Common nucleophiles

- Soft enolates (β-ketoester, malonate, β-cyanoester) —
  classical.
- Indoles (Nazarov-Trost variant).
- Amines (allyl amination).
- Phenoxides (allyl ether).

### Asymmetric Tsuji-Trost (Trost / Helmchen)

```
allyl-OAc + Nu-H + Pd(0) + chiral phosphine ligand →
                       chiral Nu-allyl with > 95 % ee
```

Trost ligands (BPI; bis(diphenylphosphino)indane) +
Helmchen ligands (PHOX) → industrial chiral building-block
synthesis.

### Stoltz decarboxylative allylation

```
allyl β-ketoester + Pd cat. → Pd loses CO₂ → enolate +
                              allyl Pd → α-allylated ketone
```

Builds quaternary carbon stereocentres in one step. Used
in alkaloid + terpene total synthesis (Stoltz 2007).

## Sakurai-Hosomi allylation

```
allyl-SiMe₃ + RCHO (or R₂C=O) + Lewis acid → R-CR'(OH)-CH₂CH=CH₂
                                              (β-hydroxy + γ-alkene)
```

Allyl silane is a soft nucleophile that adds to the
activated carbonyl. Lewis acid (TiCl₄, BF₃·OEt₂, Sc(OTf)₃)
activates the carbonyl.

### Variants

- **Allyl-Sn** (Brown allylation precursor for Sn);
  toxicity issues.
- **Allyl-Bpin** (modern; Brown-style boron).

### Asymmetric Sakurai

Chiral Lewis acid (BINOL-Ti, BINOL-Sc) → enantioselective
allylation. Used in Roush's chiral-allylboration camp.

## Brown allylation

```
(R)-(+)-α-pinene + 9-BBN → (R)-(Ipc)₂B-allyl
+ RCHO → (R)-homoallyl alcohol (> 90 % ee)
```

(Ipc)₂B-allyl is the workhorse chiral allylborane; α-pinene
is the chiral source. Alternative chiral sources for
Brown:

- (R)- or (S)-2-pinanyl-9-BBN.
- Chiral 1,3,2-dioxaborolanes.

Roush's tartrate allylborate gives different selectivity.

## Asymmetric allyl-Sn (Keck, Yamamoto)

```
allyl-Sn(Bu)₃ + RCHO + chiral Lewis acid (BINOL-Ti) →
                          chiral homoallyl alcohol
```

Less common today (Sn toxicity); replaced by allyl-B.

## Crotylation + prenylation

For more-substituted allyls:

```
crotyl-Bpin + RCHO + chiral Lewis acid → (E)-crotyl product
```

Crotyl-Bpin gives γ-methyl-β-hydroxy aldehyde with control
of:

- α/γ regiochemistry (E vs Z crotyl-B → different products).
- syn/anti diastereomer (Z-crotyl-B → syn; E-crotyl-B →
  anti).

Burke's MIDA boronate variants: more stable, slower
release, useful for iterative allylation.

## Comparison

| Method | Nucleophile | LG | ee available |
|--------|-------------|-----|--------------|
| Tsuji-Trost | enolate + N + O | OAc / Cl | yes (Trost ligands) |
| Sakurai-Hosomi | allyl-Si + Lewis acid | – (no LG) | yes (chiral Lewis acid) |
| Brown allylation | allyl-B | – | yes (chiral borane) |
| Negishi | allyl-Zn + Pd | OAc | with chiral Pd |
| Yamamoto / Roush | allyl-Sn or B | – | yes (chiral Lewis acid) |

## Industrial uses

- **Asymmetric allylation in API synthesis** for
  hydroxypiperidines + chiral homoallyl alcohols.
- **Stoltz decarboxylative allylation** in vinblastine +
  aspirin-related syntheses.
- **Trost asymmetric allylation** in vitamin E +
  prostaglandin work.

## Try it in the app

- **Reactions tab** → look at allylation reactions if
  seeded.
- **Glossary** → search *Tsuji-Trost*, *π-allyl Pd*,
  *Sakurai-Hosomi*, *Brown allylation*, *Crotylation*.

Next: **Aldol with chiral auxiliaries (Evans, Oppolzer,
Myers)**.
