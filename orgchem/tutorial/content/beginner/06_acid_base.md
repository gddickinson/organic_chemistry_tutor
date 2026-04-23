# Acid–base chemistry & pKa

Acid–base reactions are everywhere in organic chemistry: catalysis,
buffering, solubility, separation, even drug design. This lesson
covers the two definitions you'll use day-to-day, the pKa concept,
and the rules of thumb that let you predict which way a proton will
move.

## Two definitions, one arrow

| Definition | Acid | Base |
|------------|------|------|
| **Brønsted–Lowry** | proton donor | proton acceptor |
| **Lewis**          | electron-pair acceptor | electron-pair donor |

Every Brønsted acid/base pair is **also** a Lewis acid/base pair —
Brønsted is just the special case where the electron pair being
traded is the O–H (or N–H, S–H) bonding pair. Curly-arrow notation
works identically: the arrow starts at the electron pair on the base
and ends at the acidic hydrogen.

Reagents that are Lewis acids but **not** Brønsted acids — AlCl₃,
BF₃, TiCl₄ — show up constantly in Friedel-Crafts alkylations,
epoxide openings, and ester activation. Learning to spot the empty
orbital (or low-lying σ\*) is the key skill.

## pKa in one paragraph

`pKa = −log₁₀(Ka)`. Small pKa = strong acid = happy to give up its
proton. Big pKa = weak acid = holds on to its proton. The useful
ranges:

| pKa        | Typical family                  | Example (pKa)             |
|------------|---------------------------------|---------------------------|
| –10 to 0   | mineral acids / ArSO₃H           | H₂SO₄ (−3), HCl (−7)      |
| 0 to 5     | carboxylic acids                | acetic acid (4.8)         |
| 5 to 12    | phenols, thiols, β-diketones    | phenol (10), pentanedione (9) |
| 12 to 20   | alcohols, amides, α-H ketones   | ethanol (16), acetone α-H (20) |
| 20 to 35   | sp alkynes, α-H esters          | 1-propyne (25), ester α (25) |
| 35 to 50   | sp² / sp³ C–H                   | NH₃ (38), benzene (43)    |

**ΔpKa ≈ 10 shifts the equilibrium constant by 10¹⁰.** So if you
mix an acid of pKa 5 with the conjugate base of an acid of pKa 15,
the reaction is essentially irreversible toward protonation of the
stronger base.

For more general reasoning about proton-transfer rates and
transition-state geometry, see {term:Hammond postulate} — it
sharpens the "which direction does equilibrium go?" intuition
into "when does the TS look more like the reactants vs the
products?".

## The five factors that stabilise a conjugate base

These let you **predict pKa without memorising it**. Rank potential
acids by how well each factor stabilises the anion that forms
after deprotonation.

1. **Atom identity (electronegativity + size).** Down a group,
   size wins — HI is a stronger acid than HF despite F being more
   electronegative, because I⁻ is much more diffuse / polarisable
   and better stabilises the charge. Across a period,
   electronegativity wins — HF >> CH₄ in acidity.

2. **Resonance delocalisation.** A carboxylate spreads its charge
   across two oxygens; an alkoxide doesn't. That's the 11-pKa-unit
   gap between acetic acid (4.8) and ethanol (16).

3. **Inductive withdrawal.** Electron-withdrawing groups near the
   acid site stabilise the anion. Trichloroacetic acid (pKa 0.7)
   vs acetic acid (4.8) — the three chlorines pull electron
   density away from the carboxylate.

4. **Hybridisation.** sp C–H (pKa ~ 25) > sp² C–H (~ 44) >
   sp³ C–H (~ 50), because s-character holds the negative
   charge closer to the nucleus. The same trick explains why
   terminal alkynes can be deprotonated by amide base and used as
   nucleophiles.

5. **Solvent.** Polar protic solvents stabilise small anions
   (good H-bond acceptor from solvent). Polar aprotic solvents
   (DMSO, DMF) *destabilise* small anions (no H-bond donor) and
   so make them *more* basic and nucleophilic.

## Practical patterns

### Drawing the equilibrium

```
HA  +  B⁻   ⇌   A⁻  +  HB
```

**Equilibrium favours the side with the weaker acid / weaker base
(larger pKa).** So if HA has pKa 5 and HB has pKa 16, the reaction
goes right essentially to completion (ΔpKa = 11).

### Buffers

When you need the pH near a target: pick an acid–base pair whose
pKa matches the target pH within ±1 unit, then use the
Henderson-Hasselbalch equation:

```
pH = pKa + log([A⁻] / [HA])
```

Classic buffers: phosphate (pKa₁ = 2.1, pKa₂ = 7.2, pKa₃ = 12.4)
covers three pH ranges; acetate buffers near pH 5; Tris buffers
near pH 8; HEPES near pH 7.4 (biology).

### Predicting tautomer / protonation state

Given a multi-functional molecule, ask *which site is most acidic?*
Rank candidate pKa values — the site with the lowest pKa is the
one that will deprotonate first. Amino acids are the canonical
example: α-COOH (pKa ~ 2) deprotonates first, then α-NH₃⁺
(pKa ~ 9) — giving the familiar zwitterion at physiological pH.

## Why it matters downstream

Acid–base reasoning is the scaffolding for almost everything:

- **Nucleophile strength** — a stronger base (higher pKa of
  conjugate acid) is typically a better nucleophile in polar
  aprotic solvents.
- **Leaving-group ability** — the lower the pKa of HLG, the
  better LG is a leaving group. Tf⁻ (pKa HTfO = −14) is a
  phenomenal leaving group; F⁻ (pKa HF = 3) is terrible.
- **Catalyst selection** — Fischer esterification needs an acid
  catalyst to protonate the carbonyl; Wittig needs a base strong
  enough to deprotonate a phosphonium salt (pKa ~ 22, so use nBuLi).
- **Extraction / purification** — acid–base extraction sorts
  carboxylic acids, phenols, amines, and neutrals into different
  aqueous layers in one funnel. Covered in *Tools → Lab techniques →
  Acid-base extraction*.

Once you internalise the five-factor anion-stability picture,
you'll find you can predict most pKa values within ±2 units on the
fly — and that's all you need to steer a reaction.

## Practice

Try the *Tools → Lab techniques → Acid-base extraction* dialog
with the following SMILES + pKa pairs to see which layer each
lands in at pH 5 / 7 / 10:

| SMILES       | Name             | Expected pKa |
|--------------|------------------|--------------|
| `CC(=O)O`    | Acetic acid      | 4.8          |
| `Oc1ccccc1`  | Phenol           | 10.0         |
| `CCN`        | Ethylamine       | conj. 10.7   |
| `c1ccccc1`   | Benzene (neutral)| —            |

The dialog returns the % in each layer plus the logP contribution,
so you can see how protonation state flips the partitioning.
