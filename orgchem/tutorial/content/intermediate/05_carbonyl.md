# Carbonyl Chemistry

The C=O double bond is arguably the most important functional group
in organic chemistry. Aldehydes, ketones, carboxylic acids, esters,
amides, acid chlorides, anhydrides — all share the same electronic
DNA: a strongly polarised C(δ⁺)=O(δ⁻) that acts as the electrophilic
workhorse for nucleophilic addition, acyl substitution, and enolate
chemistry. This lesson unifies the whole family.

## Why C=O is so reactive

Two pieces of physics:

1. **Polarisation**. Oxygen's electronegativity (3.44) pulls the
   C–O π and σ electrons toward itself. The carbon is electron-
   deficient — the classic electrophilic site.
2. **Geometry**. The sp² carbon is planar and accessible from both
   faces. No steric shielding like a tetrahedral C already bonded
   to four groups.

Nucleophiles attack from either face at ~107° (the "Bürgi-Dunitz
angle" — experimentally derived from scanning thousands of crystal
structures). The product is a **tetrahedral intermediate** — a key
branching point.

## The canonical branching: addition vs substitution

After nucleophile attack, the tetrahedral intermediate either:

- **Kicks out a new group** → substitution (acyl substitution). Happens
  when the carbonyl carbon started with a leaving group (OR in esters,
  Cl in acyl chlorides, NR₂ in amides).
- **Stays tetrahedral + protonates** → addition. Happens when the
  starting carbonyl had no leaving group (aldehyde, ketone).

This single fork explains why:

- Aldehydes + Grignard → alcohol (addition).
- Esters + Grignard → tertiary alcohol (two additions: the ester
  first loses OR to become a ketone, which then undergoes a second
  attack).
- Carboxylic acid + alcohol + H⁺ → ester + water (Fischer esterification,
  acid-catalysed substitution).

## The reactivity ladder

Not all carbonyls are equal. The order of **electrophilicity** is:

    Acid chloride > Anhydride > Aldehyde > Ketone > Ester > Amide > Carboxylate

Why? Two effects acting on the carbonyl carbon's LUMO energy:

- **Inductive**: Cl > OR > NR₂ is the order of σ-withdrawal. Chloride
  pulls electron density away, lowering the π* LUMO → more reactive.
- **Resonance**: N has the best lone-pair donation into the C=O π*
  (raising the LUMO) → amides least reactive. O is intermediate
  (esters moderate). Cl has poor p-orbital overlap with C=O → doesn't
  counteract its σ-withdrawal → acid chlorides stay reactive.

You can convert **up** the ladder (acid → acid chloride via SOCl₂)
but never **down** (amide → aldehyde is not a direct step; you'd
have to cleave the amide first).

## The Grignard and organolithium — workhorses

Strong nucleophilic carbanion equivalents. Attack once:

    R-MgBr + R'CHO  →  [R'-CH(O⁻MgBr)R]  →(H₃O⁺)→  R'-CH(OH)R    (2° alcohol)
    R-MgBr + R'CO-R'' → [R'-C(O⁻MgBr)(R)R'']  →(H₃O⁺)→ R'-C(OH)(R)R''   (3°)

Attack twice (ester → via ketone → tertiary alcohol):

    R-MgBr + R'CO₂R''  →  R'-CO-R (ketone; loses R''O⁻)
       + second eq R-MgBr  →  R'-C(R)₂-OH (3° alcohol)

Open the **Grignard addition to acetone** entry in the Reactions tab.
The seeded mechanism shows the magnesium-coordinated oxygen → proton
transfer → free alcohol sequence.

## Enolates — the α carbon as a nucleophile

The **α-hydrogen** of a carbonyl (the H on the C adjacent to C=O) is
acidic (pKa ~20 for ketones, ~25 for esters). Deprotonation gives an
**enolate** — a stabilised carbanion where negative charge sits on
both the α-C and the carbonyl O.

Enolates are the **nucleophilic twin** of the carbonyl — they attack
other electrophiles (C=O, C=C-E, alkyl halides). That's the whole
foundation of aldol, Claisen, Michael, Mannich chemistry.

Open the seeded **Aldol condensation** mechanism in the Reactions tab.
The 3-step pattern (enolisation → C-C bond → dehydration) is the
template for hundreds of real reactions.

## Addition to C=O: the patterns worth memorising

### 1. Acetal formation (aldehyde + 2 × alcohol + H⁺)

    R-CHO + HOR' ⇌ R-CH(OR')(OH) ⇌ R-CH(OR')₂ + H₂O

Two rounds of addition with water elimination in between. Reversible;
used as a **protecting group** for carbonyls (the acetal survives base,
Grignard, and many other things that would attack a free C=O).

### 2. Imine / enamine formation (ald/ket + 1° amine / 2° amine)

    R-CHO + H₂N-R' ⇌ R-CH(OH)(NHR') ⇌ R-CH=N-R' + H₂O   (imine, 1° amine)
    R-CHO + HN(R')₂ ⇌ R-CH=N⁺(R')₂ →  R-CH=C<...  (enamine, 2° amine)

Imines are key in **reductive amination** and **enzyme catalysis**
(aldolase class I — see the seeded enzyme mechanism for this exact
Schiff-base intermediate).

### 3. Cyanohydrin formation (ald/ket + HCN)

    R-CHO + HCN → R-CH(OH)(CN)

A cyanohydrin is one chiral-centre-closer to being an α-hydroxy acid
(hydrolyse the nitrile) or a 1,2-amino alcohol (reduce the nitrile).
A classical C-C bond-forming step.

### 4. Wittig — carbonyl → alkene

Phosphorus ylide + C=O → C=C + Ph₃P=O. The seeded **Wittig reaction**
mechanism walks through the betaine → oxaphosphetane → fragmentation
pathway.

## Acyl substitution: the three key examples

1. **Ester ↔ carboxylic acid** (Fischer esterification / saponification).
   Acid- or base-catalysed. Reversible in acid, driven forward by
   removing water.
2. **Acid chloride → amide** (Schotten-Baumann). Fast, irreversible
   under aqueous-base conditions.
3. **Ester → amide** (aminolysis). Slow but practical for protecting
   amines during peptide synthesis (see the seeded SPPS pathway).

## The α-C reactivity patterns

Beyond aldol / Claisen / Michael:

- **α-halogenation**: ketones + X₂ + acid → α-halo ketone. Base
  version (haloform reaction) gives carboxylate + HCX₃.
- **Mannich reaction**: enolate + iminium → β-amino carbonyl. The
  "proline organocatalysis" version (List 2000) made it asymmetric.
- **HVZ**: carboxylic acid + Br₂ + PBr₃ → α-brominated acid. Seeded
  as **Hell-Volhard-Zelinsky** in the Reactions tab.

## Why this matters

A survey of named reactions in modern synthesis shows **>60%** use
at least one carbonyl addition or acyl substitution. Asymmetric
synthesis (Phase 21b tutorial) largely *is* asymmetric carbonyl
chemistry — Evans, List, MacMillan, Noyori all work on some flavour
of this scaffold.

## Practice

1. In the **Reactions tab**, step through the seeded mechanism of
   **Grignard addition** (3 steps including workup) and **Aldol
   condensation** (3 steps — enolise, attack, dehydrate).
2. Ask the tutor: *"What's the difference between an aldol
   *addition* and an aldol *condensation*?"* (Hint: water loss in
   the latter.)
3. Look up **Acetaldehyde** in the Molecule Workspace. The ¹H NMR
   predictor (Phase 4) shows the diagnostic 9-10 ppm aldehyde singlet
   + methyl doublet at 2.2 ppm.
4. In the Reactions tab, look at **NaBH4 reduction of acetone** and
   **PCC oxidation of 2-propanol** side-by-side. Same C=O ↔ C(OH)
   fork, opposite directions.

Next: **Reaction energetics** (already landed) — now that you
understand carbonyl mechanisms, you can reason about why some steps
are fast and others aren't.
