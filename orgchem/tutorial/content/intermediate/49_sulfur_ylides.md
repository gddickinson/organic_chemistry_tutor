# Sulfur ylide (Corey-Chaykovsky) chemistry

A **sulfur ylide** is a carbanion adjacent to a positively
charged sulfur — a soft nucleophile that's analogous to
phosphorus ylides (Wittig) but with different reactivity.

## The Corey-Chaykovsky reagents

Two main sulfur ylides for synthesis:

### 1. Dimethylsulfonium methylide (DMSM)

```
Me₃S⁺ I⁻  + n-BuLi (or NaH) → CH₂=SMe₂ (ylide; "DMSM")
                              + Me₃SI is precursor
```

DMSM is a **non-stabilised** ylide. Reacts with carbonyls:

```
R₂C=O + DMSM → R₂C(O-CH₂-SMe₂⁺)⁻ → R₂C-CH₂ + SMe₂
                                    (epoxide)
```

Net: ketone → epoxide with one carbon added. The four-
membered alkoxide-ylide intermediate collapses to an
oxirane (epoxide) instead of opening to an olefin (which
is what Wittig does).

### 2. Dimethylsulfoxonium methylide (DMSOM)

```
Me₃S(O)⁺ I⁻ + NaH → CH₂=S(O)Me₂ ("Corey-Chaykovsky reagent",
                              ~ stabilised ylide)
```

DMSOM (more stabilised by S=O) reacts differently:

```
R₂C=CR'-CO-R'' (α,β-unsat) + DMSOM → cyclopropane
                                     (1,4-addition then ring closure)
```

Cyclopropanates **enones** while DMSM epoxidates them.
Mechanism: DMSOM adds 1,4 (Michael), the resulting α-anion
attacks back on the ylide C to close the ring, with loss
of DMSO.

## Comparing — DMSM vs DMSOM at a carbonyl

| Substrate | DMSM (non-stabilised) | DMSOM (stabilised) |
|-----------|------------------------|---------------------|
| Aldehyde / ketone | epoxide | epoxide |
| α,β-Unsaturated carbonyl | epoxide of the C=C | cyclopropane on the α,β-system |

The selectivity is **stabilisation-driven**: less-stabilised
ylide (DMSM) attacks the carbonyl directly; more-stabilised
ylide (DMSOM) adds in a Michael fashion to the C=C of an
enone.

## Other sulfur ylide chemistry

### Stevens rearrangement

```
[2,3]-sigmatropic of an α-substituted ammonium / sulfonium
ylide → N or S leaves, new C-C bond forms.
```

Used in alkaloid synthesis.

### Trost cyclopropanation

Trost developed Pd-catalysed allylation with sulfonyl
ylides → asymmetric cyclopropanation.

### Aggarwal asymmetric sulfur-ylide chemistry

Vary Aggarwal (Bristol) developed chiral sulfur ylides
from chiral sulfides → asymmetric epoxide / aziridine /
cyclopropane synthesis. Catalytic in the chiral
sulfide if regenerated.

## Practical recipe — DMSM epoxidation

```
1. Trimethylsulfonium iodide (Me₃S⁺ I⁻; commercial) +
   NaH (1.1 eq) in DMSO, rt, 30 min → DMSM in situ.
2. Add ketone or aldehyde; stir 1-12 h at rt.
3. Quench with sat. NH₄Cl; extract with Et₂O.
4. Concentrate; column purification → epoxide.
```

Sometimes a one-pot from Me₃SI / KOH in CH₃CN works
without isolating ylide.

## Sulfoxide vs sulfide vs sulfone

Sulfur in different oxidation states behaves differently:

```
R-SH       (thiol)        — nucleophile / acid
R-S-R'     (sulfide)      — soft donor; coordinates to soft metals
R-S(=O)-R' (sulfoxide)    — Lewis basic O; Pummerer reactions
R-S(=O)₂-R' (sulfone)     — α-C is acidic (Julia); EWG
```

Modify oxidation state with mCPBA, NaIO₄, H₂O₂, OsO₄.

## Other sulfur reagents in synthesis

- **DMSO** — Swern / Pfitzner-Moffatt oxidation.
- **DMSO-(COCl)₂** — activated electrophilic S species
  → activate alcohol → eliminate.
- **(CH₃)₂S₂** (dimethyl disulfide) — deactivate Pd
  catalyst; soft thiol source.
- **NaSH / Na₂S** — install -SH or -S-S-.

## Try it in the app

- **Tools → Lab reagents…** → look up Me₃SI, NaH, DMSO,
  Me₃S(O)I.
- **Reactions tab** → look at Corey-Chaykovsky if seeded.
- **Glossary** → search *Sulfur ylide*, *Corey-
  Chaykovsky*, *Sulfoxide*, *Sulfone*.

Next: **Boron chemistry intro**.
