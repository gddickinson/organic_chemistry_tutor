# Acylation + asymmetric acylation — Fu's nucleophilic catalysis

Acyl-transfer chemistry is fundamental — esters, amides,
acetate protecting groups all involve transfer of an acyl
group between an electrophile + a nucleophile. Modern
**asymmetric acyl transfer** by chiral nucleophilic catalysts
is one of the cleanest ways to resolve racemic alcohols.

## Classical acylation

```
RCOOH + ROH + DCC + cat. DMAP → RCOOR'
RCOOH + R'NH₂ + DCC / EDC + DMAP → RCOR' (amide)
RCOCl + ROH + Et₃N → RCOOR'
```

DMAP (4-N,N-dimethylaminopyridine) is a famous **acyl-
transfer catalyst** (Steglich, 1969). It accepts the acyl
group from the activated carboxylate + transfers it to
the alcohol → ester + DMAP regenerated.

Mechanism:

1. Anhydride / acyl-EDC + DMAP → DMAP-acyl
   adduct (acyl-pyridinium).
2. Alcohol attacks the activated carbonyl → ester.
3. DMAP regenerated.

Without DMAP, ester yield drops 5-50 % depending on
substrate.

## Catalytic asymmetric acylation

Fu (Caltech / MIT, ~ 1996) designed **planar-chiral DMAP
analogues** that can desymmetrise racemic alcohols + meso
diols + meso epoxides:

```
racemic alcohol + Ac₂O + Fu's chiral DMAP →
                       enantioselective acylation
                  → enantioenriched alcohol + ester
```

The "matched" enantiomer reacts faster than the "mismatched"
one → kinetic resolution (or dynamic kinetic resolution
with racemising substrate).

### Famous Fu catalysts

- **PPY (planar-chiral pyrrolidinopyridine)** — classic.
- **Imide-based** chiral pyridines — newer variants for
  specific resolutions.

## Kinetic resolution principles

For racemic alcohol + acetic anhydride + chiral catalyst:

```
fast: (R)-alcohol + Ac₂O → (R)-acetate
slow: (S)-alcohol + Ac₂O → (S)-acetate
```

After ~ 50 % conversion:

- Product: ~ 95 % (R)-acetate.
- Recovered SM: ~ 95 % (S)-alcohol.

The selectivity factor `s = k_R/k_S` is the kinetic
discrimination. Useful: s > 10 is the textbook target;
s > 100 in modern systems.

## Dynamic kinetic resolution (DKR)

If the substrate racemises faster than reaction:

```
(R)-substrate ⇌ (S)-substrate (fast equilibrium)
fast:    (R) + Ac₂O + chiral cat. → (R)-acetate
        (S) replenished from racemising pool
```

Net: 100 % of substrate becomes single-enantiomer
acetate. Modern DKR uses:

- **Chiral acyl-transfer catalyst** + **racemisation
  catalyst** (often a Ru complex).
- **Bäckvall et al.** combined Fu's PPY with Shvo's Ru
  → DKR of secondary alcohols → > 95 % ee at 100 %
  yield.

Industrial: kg-scale chiral alcohol synthesis for pharma
intermediates.

## Asymmetric ester / amide formation

Beyond just acetate, chiral acyl-transfer catalysts can
do enantioselective:

- Esterification with bulky carboxylic acids.
- Amidation with anhydrides.
- Carbamate formation with chloroformates.

Loadings: typically 5-10 mol % of chiral catalyst.

## Acylating agents — choice matrix

| Reagent | Use | Pros |
|---------|-----|------|
| Ac₂O / Ac-Cl | acetyl protection | cheap, simple |
| (Boc)₂O | Boc protection | water-tolerant |
| TBSCl + imidazole | silyl protection | reliable, common |
| TsCl + pyridine | tosyl ester | activates OH for SN2 |
| MsCl + Et₃N | mesyl ester | better LG than tosyl, cheap |
| Tf₂O + pyridine | triflate | best LG |
| EDC + HOBt + Hünig's base + RNHR' | amide formation | water-tolerant; pharma standard |
| HATU + Hünig's base + RNH₂ | amide formation | clean, standard for SPPS |
| T3P + Et₃N | amide formation | scalable, low racemisation |

## Try it in the app

- **Reactions tab** → load *Fischer esterification* (if
  seeded) for the H⁺ catalysed variant.
- **Tools → Lab reagents…** → look up DMAP, EDC, HATU,
  T3P, Ac₂O.
- **Tools → Stereochemistry…** → input KR product → confirm
  chirality.
- **Glossary** → search *Acyl transfer*, *DMAP*, *Kinetic
  resolution*, *Dynamic kinetic resolution*, *Fu chiral
  DMAP*, *EDC coupling*.

Next: **CDC (cross-dehydrogenative coupling)**.
