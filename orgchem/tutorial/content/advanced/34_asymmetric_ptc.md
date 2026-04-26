# Asymmetric phase-transfer catalysis — Maruoka catalysts

The intermediate-tier lesson covered classical phase-
transfer catalysis (PTC). The asymmetric version uses a
chiral cation to deliver an anionic nucleophile to a
prochiral substrate with high ee.

## The chiral PTC model

```
PROCHIRAL substrate (in organic phase)
         + ANION (e.g. enolate, fluoride, hypochlorite) (in aq. phase)
         + CHIRAL ammonium cation (transports anion across phase boundary)
         → ENANTIOENRICHED product
```

Compared to homogeneous chiral catalysis:

- **No need for elaborate ligand design** — chiral cation
  is the entire chiral environment.
- **Catalyst loading typically 5-10 mol %** — high but
  acceptable.
- **Cheap + air-stable** chiral cinchona alkaloids work
  well.
- **Room temperature** + biphasic conditions → green
  + scalable.

## Cinchona alkaloid quaternary salts

Cheap chirality from natural products:

```
Cinchonidine (left-handed) →  benzyl cinchonidinium chloride
Cinchonine (right-handed)  →  benzyl cinchoninium chloride
Quinine                    →  benzyl quininium chloride
Quinidine                  →  benzyl quinidinium chloride
```

The quaternary N is the cation that pairs with the anion;
the chiral framework does the asymmetric induction.

### Famous applications

- **Cinchona PTC + glycine alkylation** — early example
  (~ 50 % ee).
- **MIBK-glycinate alkylation** with benzyl cinchoninium
  → unnatural amino acids.

## Maruoka catalysts (1999, modern workhorse)

Maruoka (Kyoto) designed **C₂-symmetric chiral binaphthyl-
ammonium salts** with bulky aromatic substituents:

- Modified BINOL-derived quaternary cations.
- **Two enantiomerically pure binaphthyl rings** flank the
  N, creating a deep chiral pocket.
- Anionic nucleophile binds in a chiral environment.

Maruoka catalysts achieve **> 99 % ee** for many
asymmetric alkylations + Mannichs + epoxidations.

### Industrial example

Synthesis of unnatural α-amino acids — alkyl, aryl, Cα-
substituted, highly hindered analogues used in peptide
chemistry. Bachem + others use Maruoka PTC to make
non-natural building blocks at multi-kilogram scale.

## Key reactions catalysed

### Asymmetric alkylation of glycine equivalent

```
N-(diphenylmethylene)glycine tert-butyl ester (CH₂=NCPh₂-CO₂tBu)
         + RX + base + chiral PTC
         → α-substituted amino acid (alpha-AA)
                                       ee > 95 %
```

The masked glycine has no αH problem; the alkylation
installs R with chirality control.

### Asymmetric Michael addition

```
glycine schiff base + α,β-unsat ester / nitro compound +
                   chiral PTC + base → β-substituted amino acid
```

### Asymmetric Mannich

```
schiff base + N-Boc imine + chiral PTC + base → β-amino-α-amino ester
```

### Asymmetric epoxidation (Hou's variant)

Chiral PTC + NaOCl + α,β-unsat ketone → enantioenriched
epoxide.

### Asymmetric fluorination

Chiral PTC + Selectfluor + α-substrate → enantioselective
α-F installation.

## Mechanism

The chiral cation pairs with the enolate / alkoxide /
fluoride / etc. + brings it into the organic phase. The
chiral cavity around the cation orients the anion's
electrophile-attacking trajectory.

Computational studies (Houk, Maruoka) suggest the
substrate H-bonds to the cation's quaternary N + acyl
group, with the prochiral face of attack determined by
the binaphthyl wall.

## Limits

- Catalyst is expensive (Maruoka catalyst ~ $300/g for
  the simpler version, more for advanced).
- Substrate scope: best for activated nucleophiles +
  acidic substrates (pKa < ~ 30).
- High catalyst loading (5-10 mol %) compared to metal
  asymmetric catalysis (0.1-1 %).

## Try it in the app

- **Reactions tab** → look for asymmetric alkylation
  reactions if seeded.
- **Tools → Stereochemistry…** → input chiral product
  SMILES → see R/S assignments.
- **Glossary** → search *Phase-transfer catalysis*,
  *Maruoka catalyst*, *Cinchona alkaloid*, *Asymmetric
  alkylation*.

Next: **Enamine + iminium catalysis (List/MacMillan
deeper)**.
