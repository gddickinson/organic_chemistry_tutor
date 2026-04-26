# Solvent selection — picking the right solvent for the job

The solvent is rarely innocent. It can speed up, slow down,
reverse, or stop a reaction altogether. This lesson collects
the practical rules for picking solvents in synthesis,
extraction, recrystallisation, and chromatography.

## Three big solvent properties

### 1. Polarity

Roughly: how well the solvent solvates ions and dipoles.
Measured by the **dielectric constant ε**:

| Solvent | ε | Class |
|---------|---|-------|
| Hexane | 1.9 | non-polar |
| Toluene | 2.4 | non-polar |
| DCM | 8.9 | low-polar |
| THF | 7.5 | low-polar aprotic |
| Acetone | 21 | polar aprotic |
| EtOH | 24 | polar protic |
| MeOH | 33 | polar protic |
| MeCN | 37 | polar aprotic |
| DMF | 37 | polar aprotic |
| DMSO | 47 | polar aprotic |
| Water | 80 | polar protic |

### 2. Hydrogen-bond donor (protic) vs acceptor only (aprotic)

- **Protic**: water, alcohols, carboxylic acids, primary
  amines. Have an O-H, N-H, S-H to donate.
- **Aprotic**: DMSO, DMF, MeCN, acetone, THF, DCM. Accept
  H-bonds (via O, N, S lone pairs) but don't donate.

Critical for nucleophilic substitution:

- **Polar protic** solvents H-bond to anionic nucleophiles
  → less reactive; favour SN1 / E1 (which generate ions
  → solvated transition state).
- **Polar aprotic** solvents don't H-bond to anions →
  "naked" highly nucleophilic anions → favour SN2 / E2.

### 3. Boiling point

Determines reaction temperature for reflux + ease of
removal:

| Solvent | bp (°C) | Notes |
|---------|---------|-------|
| Et₂O | 35 | Easily removed; flash-volatile |
| DCM | 40 | Easily removed |
| Acetone | 56 | Easily removed |
| MeOH | 65 | Hydrogen-bonded; more stubborn |
| Hexane | 69 | OK |
| THF | 66 | OK |
| EtOH | 78 | OK; hard to dry |
| EtOAc | 77 | OK |
| Water | 100 | Hard to remove (lyophilise or extract) |
| Toluene | 111 | Higher T reactions |
| MeCN | 82 | OK |
| DMF | 153 | Very hard to remove (water wash) |
| DMSO | 189 | Very hard to remove (water wash) |
| HMPA | 232 | Very hard + toxic |

## Solvent choice for common situations

### Nucleophilic substitution

- **SN2** → polar aprotic (DMSO, DMF, MeCN, acetone).
- **SN1 / E1** → polar protic (MeOH, EtOH, water). Helps
  ionise R-X.

### Carbanion chemistry (LDA, n-BuLi enolates)

- THF or Et₂O at -78 °C. DCM is incompatible with strong
  bases (deprotonates → CHCl₂⁻ that decomposes).

### Grignard / organolithium formation

- Et₂O or THF only. Coordinates the metal centre.

### Diels-Alder

- Toluene, DCM, or even neat. Polarity has small effect
  unless the dienophile is charged.

### Reductions

- LiAlH₄ → THF, Et₂O.
- NaBH₄ → MeOH, EtOH, water.
- DIBAL → toluene, DCM at -78 °C.
- H₂/Pd-C → MeOH, EtOH, EtOAc.

### Coupling (Pd) reactions

- Suzuki → toluene + EtOH + water; or dioxane / DMF.
- Heck → DMF or NMP (high T).
- Buchwald-Hartwig → toluene or dioxane.

### Photoredox

- MeCN, DMSO, DMF — degassed (sparge with N₂ or Ar).

## Workup considerations

Choose solvents that **separate cleanly from water** for
extraction:

- **Yes** (immiscible): Et₂O, EtOAc, DCM, toluene, hexane,
  CHCl₃.
- **No** (miscible): MeOH, EtOH, THF, MeCN, DMSO, DMF,
  acetone.

If you ran the reaction in DMF, dilute with water → extract
into EtOAc → wash EtOAc with water several times to remove
remaining DMF.

## Chromatography solvents

For silica TLC + flash chromatography, solvents are ranked
by **eluotropic strength** (how strongly they elute):

```
Hexane < Toluene < DCM < EtOAc < Acetone < MeOH < Water
```

Common gradients:

- Non-polar substrates: hexane / EtOAc 9:1 → 1:1.
- Polar substrates: DCM / MeOH 100:0 → 90:10 (then add 1 %
  TEA for amines).
- Free amines often need 1 % TEA or 1 % NH₄OH to suppress
  tailing.

## Greener choices

The CHEM21 solvent guide ranks them:

- **Recommended**: water, EtOH, iPrOH, EtOAc, 2-MeTHF,
  acetone, anisole.
- **Problematic**: DMF, MeCN, DCM (carcinogenic suspicion,
  REACH list).
- **Hazardous**: HMPA (carcinogen), benzene (human
  carcinogen), CCl₄ (ozone-depleting).

Modern process chemistry actively avoids DCM + DMF; 2-MeTHF
+ EtOAc + cyclopentyl methyl ether (CPME) are the "green
THF / DMF" alternatives.

## Try it in the app

- **Tools → Lab reagents…** → look up solvents for hazards,
  dryness, peroxide-formation, freezing points.
- **Tools → Lab techniques → TLC / Rf** → predict an Rf in
  a candidate solvent system.
- **Glossary** → search *Polar protic*, *Polar aprotic*,
  *Eluotropic series*, *Miscibility*.

Next: **You've finished the beginner curriculum — see the
intermediate tier**.
