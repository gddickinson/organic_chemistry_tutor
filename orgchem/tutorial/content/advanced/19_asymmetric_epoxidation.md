# Catalytic asymmetric epoxidation — Sharpless, Jacobsen, Shi

Three flavours of asymmetric epoxidation cover most
substrates. Pick the right one based on what's in your
alkene.

## Sharpless asymmetric epoxidation (SAE, 1980)

Substrate: **allylic alcohol** (the OH is required — it
coordinates to Ti).

Reagent system:

```
Ti(OiPr)₄ + (+)- or (-)-DET (diethyl tartrate) + tBuOOH
            (chiral auxiliary)              (oxidant)
```

The allylic alcohol coordinates Ti via its OH; tartrate
provides the chiral environment; tBuOOH delivers the O to
one face only.

### Mnemonic for sense of induction

Draw the allylic alcohol with OH pointing toward you
(bottom right in standard orientation); D-(-)-DET delivers
O to **top face**, L-(+)-DET to **bottom face**. Predicts
which enantiomer of epoxide you get from > 99 % of
allylic alcohol substrates.

### Industrial impact

- **Glycidol** synthesis at multi-tonne scale → drug
  intermediates.
- **(R)- + (S)-Propylene oxide** in pharma.
- **Sharpless's 2001 Nobel Prize** (with Knowles +
  Noyori).

### Limitations

- Requires the directing OH (no allylic alcohol → no
  reaction).
- Slow on hindered substrates.
- Catalyst loading 5-25 mol % (compared to modern 0.1-1 %
  catalysts).

## Jacobsen-Katsuki epoxidation (1990-91)

Substrate: **cis-disubstituted + trisubstituted alkenes**;
NO directing group needed.

Reagent system:

```
Mn(salen)Cl + chiral salen + NaOCl (bleach)
              (chiral auxiliary)   (oxidant)
```

Manganese(III) salen complex with a binaphthyl- or
diaminocyclohexane-derived chiral diamine backbone. NaOCl
oxidises Mn(III) → Mn(V)=O (the active oxidant), which
delivers O via a TS where the alkene approaches from the
side; chirality of salen biases face selectivity.

### Best substrates

- cis-styrenes (cis-β-methylstyrene → 90 % ee).
- 2,2-disubstituted alkenes (R₂C=CHR').
- Indenes + chromenes (target: pharmaceutical
  intermediates like (R)-glycidyl ethers).

### Limitations

- Trans-alkenes give modest ee (poor TS geometry).
- Some terminal alkenes give sub-90 % ee.

## Shi epoxidation (1996)

Substrate: **trans-alkenes + trisubstituted + tetrasubstituted
alkenes** (complementary to Jacobsen).

Reagent: **chiral fructose-derived ketone** (cheap natural-
product-derived) + **Oxone** (KHSO₅).

```
Shi ketone + Oxone → dioxirane (active oxidant) → alkene + O delivery
```

Mechanism: ketone + Oxone → dioxirane (3-membered O-O-C
ring); alkene attacks dioxirane on one face only, biased
by ketone chirality.

### Best substrates

- trans-disubstituted alkenes (chalcones, cinnamic
  esters).
- trisubstituted alkenes (90-99 % ee for many).
- 2,2-disubstituted alkenes (some are tough).

### Pros

- Cheap chiral catalyst (fructose-based — Shi
  ketone synthesis is 4 steps from cheap sugar).
- Aqueous compatible.
- Substrate scope complementary to Jacobsen.

### Limitations

- High catalyst loading (20-30 mol %).
- Catalyst decomposes in the reaction; turnover-limited.
- Some sensitive functional groups (silyl ethers, acid-
  sensitive groups) struggle with Oxone's pH ~ 2-3.

## Quick choice matrix

| Substrate | Best method |
|-----------|-------------|
| Allylic alcohol | Sharpless |
| cis-disubstituted alkene without OH | Jacobsen |
| trans-alkene without OH | Shi |
| Trisubstituted alkene (no OH) | Shi |
| Tetrasubstituted alkene | Shi (modest ee), or biocatalysis |

## Other asymmetric epoxidation methods

- **Juliá-Colonna** — chiral poly-Leu peptide + H₂O₂ →
  α,β-unsat carbonyl epoxidation. Cheap + scalable; works
  on chalcones.
- **Manganese / chiral imidazole / H₂O₂** (Beller, Bryliakov)
  — earth-abundant alternatives to Mn(salen).
- **Iron-porphyrin systems** (Klein Gebbink) — biomimetic
  cytochrome P450 mimics.
- **Biocatalytic** — styrene monooxygenases (Codexis,
  Genentech) deliver enantioselective epoxidation at
  industrial scale.

## Epoxide → useful products

A chiral epoxide is a workhorse intermediate:

- **Ring-opening with O nucleophiles** → diols, ethers.
- **Ring-opening with N nucleophiles** → β-amino alcohols
  → β-blockers (propranolol, atenolol).
- **Ring-opening with C nucleophiles** → C-C bond
  formation with stereocontrol.
- **Payne rearrangement** → 2,3-epoxy alcohols ⇌ 1,2-
  epoxy alcohols.

## Try it in the app

- **Reactions tab** → load *Sharpless asymmetric
  epoxidation* (if seeded) — see catalyst-cycle
  mechanism.
- **Tools → Stereochemistry…** → input epoxide SMILES →
  see CIP assignments.
- **Glossary** → search *Sharpless asymmetric
  epoxidation*, *Jacobsen-Katsuki*, *Shi epoxidation*,
  *Asymmetric catalysis*, *Enantiomeric excess*.

Next: **Catalytic asymmetric dihydroxylation + amino-
hydroxylation**.
