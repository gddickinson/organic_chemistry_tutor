# Enol ether + dithiane chemistry — umpolung tools

The α-carbon of a carbonyl is normally **electrophilic** at
the C=O + **nucleophilic** at the α-position (after
deprotonation). To reverse this — make the carbonyl C
nucleophilic — chemists use **dithiane umpolung** + related
tricks.

## Enol ethers

```
R-CO-CH₂-R' + R''OH (or RCl) → R-C(OR'')=CH-R'
            silyl ether: R-C(OSiMe₃)=CH-R'
```

Enol ethers are **electron-rich** alkenes (the OR group is
+M):

- React with electrophiles at α-position (C2) — Mukaiyama
  aldol uses this.
- Hydrolyse back to enol → ketone in the presence of mild
  acid.

Uses:

- **Aldol equivalent**: silyl enol ether + Lewis acid +
  RCHO → β-hydroxy ketone (Mukaiyama).
- **C-C bond forming** with Pd, Cu, Sc Lewis acids.
- **Stable enolate** for reactions where free enolate
  would over-react.

## Vinyl ethers + acetals

A vinyl ether is the simplest enol ether (CH₂=CHOR).
Polymerisation gives polyvinyl alcohol after hydrolysis.

Acetals are stable masked carbonyls:

```
R₂C=O + 2 ROH + H⁺ → R₂C(OR)₂ + H₂O   (acetal)
R₂C=O + HOCH₂CH₂OH + H⁺ → 1,3-dioxolane
```

Acetals:

- Stable to base, nucleophiles, organometallics.
- Cleaved back to ketone in dilute aqueous acid.
- Standard **carbonyl protecting group** in multi-step
  synthesis.

## Dithianes — the umpolung classic

```
RCHO + HS-CH₂-CH₂-CH₂-SH (1,3-propanedithiol) + acid
   → 1,3-dithiane (cyclic; C is now sp³, has 2 S + 1 R + 1 H)
```

The dithiane C is **acidic** (pKa ~ 31, comparable to
n-BuH) — n-BuLi deprotonates it:

```
1,3-dithiane + n-BuLi → 1,3-dithiane Li (carbanion!)
```

The carbanion is a **nucleophile at the carbon that was
the aldehyde C** — exactly the umpolung effect.

### Use as nucleophile

```
1,3-dithiane Li + R'X → 1,3-dithiane-R' (alkylated)
                or + R'CHO → 1,3-dithiane-CH(OH)-R'
```

### Cleave back to carbonyl

```
2,2-disubstituted dithiane + Hg(ClO₄)₂ / H₂O
                → R-CO-R' + recovered dithiol
```

Other deprotection methods: HgCl₂, AgNO₃, MeI / NaHCO₃,
electrochemical, oxidative (NBS, mCPBA).

## Stork enamine alkylation (umpolung-like)

Enamines are also α-nucleophiles (at the α-C, not the
carbonyl C):

```
R₂CH-CO-R' + R''₂NH → R₂C=CR'-NR''₂ (enamine)
+ R'''X → R₂C(R''')-CR'-NR''₂ (iminium)
+ H₂O → R₂C(R''')-CO-R' (mono α-alkylated ketone)
```

Avoids over-alkylation that plagues direct enolate +
alkyl halide.

## NHC-catalysed acyl anion (Stetter, benzoin)

NHC catalysts (from imidazolium / triazolium salts) +
aldehyde → Breslow intermediate (acyl anion equivalent):

```
RCHO + NHC → R-C(OH)(NHC) (Breslow intermediate)
+ R'CO-R'' → R-CO-CR'(OH)R'' (Stetter, benzoin)
```

NHC-catalysed asymmetric Stetter (Rovis, Bode) gives
enantioenriched 1,4-dicarbonyls.

## Other umpolung surrogates

| Equivalent | Source |
|------------|--------|
| Acyl anion | dithiane, NHC catalyst, alkyne + cat. |
| Allyl anion | allyl-Sn(R)₃ + Lewis acid (Brown allylation) |
| α-amino anion | α-amino dithiane |
| Carbene | diazo + Cu/Rh; tosylhydrazone + base |
| Vinyl anion | tosylhydrazone (Shapiro) |

## Modern umpolung — photoredox

Visible-light photoredox catalysis enables many traditional
umpolung-equivalent reactions without dithianes:

- α-Arylation of amines via SET.
- α-Acylation of imines via NHC + photoredox.
- 1,1-difunctionalisation of alkenes via radical pair
  recombination.

## Try it in the app

- **Reactions tab** → look for *Mukaiyama aldol* (if
  seeded), *Benzoin condensation* (if seeded).
- **Glossary** → search *Umpolung*, *Dithiane*, *Acetal*,
  *Enol ether*, *Stork enamine alkylation*, *Mukaiyama
  aldol*, *NHC catalysis*.

Next: **Ene reaction**.
