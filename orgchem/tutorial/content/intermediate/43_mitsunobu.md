# Mitsunobu reaction — alcohol → almost anything

The **Mitsunobu reaction** (Oyo Mitsunobu, 1967) converts
an alcohol into an SN2 product **with inversion of
configuration**. It uses two stoichiometric reagents that
together activate the alcohol + the nucleophile.

## The reagents + cycle

```
R-OH + Nu-H + PPh₃ + DIAD (or DEAD) → R-Nu + Ph₃P=O + reduced DIAD
                                       (inversion)
```

**Reagents**:

- **PPh₃** (triphenylphosphine) — phosphorus binds the
  alcohol's O.
- **DIAD** (diisopropyl azodicarboxylate) or **DEAD** (diethyl
  azodicarboxylate) — oxidising azodicarboxylate.
- **Nu-H** — the nucleophile, must be acidic enough (pKa
  < ~ 13).

## Mechanism

1. **PPh₃ + DIAD** → betaine intermediate (P-N adduct).
2. Betaine deprotonates Nu-H → Nu⁻ + PPh₃ activated.
3. Activated PPh₃ binds R-OH → alkoxyphosphonium
   intermediate.
4. Nu⁻ does **SN2** on R-OPPh₃⁺ → R-Nu + Ph₃P=O.

The R-OPPh₃⁺ is the key — alcohol O has been activated
into a beautiful leaving group.

## Substrate scope

Substrate must be:

- **1° or 2° alcohol** — 3° alcohols don't work (cation
  formation interferes).
- The alcohol must be unhindered enough for SN2.

Nucleophile must be acidic enough for the betaine to
deprotonate (pKa < ~ 13):

| Nu-H | pKa | Use |
|------|-----|-----|
| Carboxylic acid | 4-5 | esterification (R-OH → R-O-CO-R') |
| Phenol | 10 | ether (R-OH → R-O-Ar) |
| Phthalimide | 8 | amine surrogate (Gabriel) |
| Sulfonamide (TsNHR) | 10 | sulfonamide (R-OH → R-N-SO₂Ar) |
| Hydrazoic acid (HN₃) | 4.7 | azide (R-OH → R-N₃) |
| Thiol (RSH) | 10 | thioether (R-OH → R-S-R') |
| Hydroxamic acid | 9 | hydroxamate |
| Imide (CHCl-imide) | 6 | imide → primary amine |

## Why it's useful

Three combined attractions:

1. **Inversion of configuration** — converts a (R)-alcohol
   to (S)-product. Most useful in chiral synthesis.
2. **One-pot** — no need to isolate the activated alcohol
   intermediate.
3. **Wide nucleophile scope** — covers most "OH → X"
   transformations in a single recipe.

## Limitations + side reactions

- **PPh₃ + DIAD waste** — > 1 eq each, so 2 eq of waste
  per product (Ph₃P=O + reduced hydrazide). Over 50 % of
  Mitsunobu reaction mass is waste — bad atom economy.
- **Difficult workup** — Ph₃P=O + reduced DIAD often
  co-elute with product on silica.
- **Tertiary OH** doesn't work; eliminations dominate.
- **Hindered substrates** are slow.
- **Acidic Nu-H required** — pKa > 13 doesn't work.
- **DIAD is shock + heat sensitive** — handle carefully;
  don't grind the solid; commercial soln in toluene
  preferred.

## Modern variants

### Polymer-bound PPh₃ + DEAD

Solid-phase Mitsunobu: easy filtration removes the
phosphine waste. Argonaut + Aldrich sell PS-PPh₃ +
PS-DEAD beads.

### TMAD + n-Bu₃P (Tsunoda)

Replaces PPh₃ + DIAD with n-Bu₃P (lower-MW phosphine) +
TMAD (azodicarboxamide) — same chemistry, less waste.

### Itoh + Cohen catalytic Mitsunobu

Catalytic in azo + phosphine using oxidative
regeneration. Reduces waste 10-fold.

### Modern non-Mitsunobu alcohol activations

- **TBD-catalysed** OH → N (sulfonamide).
- **MFM-catalysed** OH → ester.
- **Bull's catalytic Mitsunobu** (2019) — completely
  closed cycle, near-stoichiometric scale.

## Famous applications

- **Inverting a stereocentre** — esterify with PNB
  acid, then hydrolyse the ester → net inversion of OH
  with no other changes.
- **Macrolactonisation** — intramolecular Mitsunobu of
  acid + alcohol on the same molecule → ring-closure.
  Common in macrolide synthesis.
- **N-alkylation of sulfonamides + phthalimides** →
  amine alternatives that avoid over-alkylation.

## Try it in the app

- **Tools → Lab reagents…** → look up PPh₃, DIAD, DEAD —
  hazards + storage.
- **Tools → Stereochemistry…** → input alcohol + Mitsunobu
  product → confirm inversion.
- **Glossary** → search *Mitsunobu reaction*, *Inversion
  of configuration*, *Triphenylphosphine*, *DIAD*.

Next: **Appel reaction + similar OH-activation tricks**.
