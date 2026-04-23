# Pericyclic Reactions

Pericyclic reactions are the "third family" of organic mechanisms,
distinct from polar (ionic) and radical chemistry. They share three
defining features:

1. **Concerted.** Bonds break and form in one step — there's no
   intermediate sitting in the middle.
2. **Cyclic transition state.** Electrons shift around a closed loop
   of interacting orbitals.
3. **Governed by orbital symmetry.** Whether a given pericyclic step
   is thermally allowed, photochemically allowed, or forbidden follows
   from the phase relationships of the frontier orbitals — not from
   steric or electronic arguments alone.

The canonical three families are **cycloadditions**, **electrocyclic
reactions**, and **sigmatropic rearrangements**. A fourth family,
**group-transfer reactions** (ene, retro-ene, dyotropic), is usually
treated as a footnote.

## Cycloadditions: `[m + n]`

Two π systems with m and n electrons combine to form two new σ bonds
and a new ring. The most famous is the **Diels-Alder** `[4 + 2]`
(butadiene + ethene → cyclohexene).

Open **Diels-Alder: butadiene + ethene** in the Reactions tab. Then
click **"Energy profile…"** — the profile has a single transition
state ~115 kJ/mol above the reactants, falling steeply to cyclohexene
at −165 kJ/mol. One barrier, one concerted step, no intermediate.

The **Woodward-Hoffmann rule** for cycloadditions:

    Thermal, suprafacial-suprafacial: allowed if (m+n) / 2 is odd
    Photochemical, suprafacial-suprafacial: allowed if (m+n) / 2 is even

For `[4+2]`: (4+2)/2 = 3 is odd → thermally allowed. That's why
Diels-Alder happens under heat alone.

For `[2+2]` (ethene + ethene → cyclobutane): (2+2)/2 = 2 is even →
thermally **forbidden**. Which is why cyclobutane isn't made by just
heating ethylene. `[2+2]`s happen photochemically (UV light promotes
one π electron, flipping the orbital phase), or via metal catalysis
that effectively inverts the symmetry rule.

### Stereochemistry: endo vs. exo

The Diels-Alder of cyclopentadiene with maleic anhydride can give two
stereoisomers of the bicyclic product:

- **Endo** — the electron-withdrawing groups sit *under* the
  cyclopentene fold. **Kinetic product** (secondary orbital interactions
  lower the TS energy).
- **Exo** — those groups sit *outside* the fold. Less steric strain,
  thermodynamic product.

At 25 °C, endo dominates. At higher T with a reversible DA, exo wins.
Classic kinetic-vs-thermodynamic story — see the **Reaction energetics**
lesson for the underlying energy-profile logic.

## Electrocyclic reactions

A linear π system with 2n π electrons closes to a cyclic π system with
(2n − 2) π electrons + one new σ bond. The reverse (**retro-electro-
cyclisation**) breaks the σ bond to reopen the ring.

Seeded example: **6π electrocyclic: hexatriene → cyclohexadiene**
(Reactions tab). A 1,3,5-hexatriene (6 π electrons) closes to a
1,3-cyclohexadiene (4 π electrons + one new C-C σ bond).

### The Woodward-Hoffmann rule for electrocyclic reactions

For a 4n-electron ring closure:
- Thermal → **conrotatory** (the two ends rotate the same direction).
- Photochemical → **disrotatory** (opposite directions).

For a (4n+2)-electron ring closure:
- Thermal → **disrotatory**.
- Photochemical → **conrotatory**.

For our 6π hexatriene case: 6 = 4n+2 (n=1), thermal → disrotatory.
Orbital-symmetry argument: the HOMO of the hexatriene has C₂-symmetric
end-orbital phases; disrotation preserves bonding overlap in the TS.

Compare the picture to the Hückel diagram. Open the tutor and run:

> Compute MO diagrams for 1,3,5-hexatriene (`C=CC=CC=C`) and tell me
> which is the HOMO.

Under the hood, `huckel_mos(smiles="C=CC=CC=C")` returns the 6 π
eigenvalues; the 3rd (HOMO) has a specific symmetry pattern along the
chain. Disrotation connects the endpoints with like-phase lobes.

## Sigmatropic rearrangements: `[i,j]`

A σ bond migrates along a π system. Labels `[i,j]` mean: a σ bond
anchored between atoms i–1 and j–1 of the two π fragments breaks; a new
σ bond forms between atoms i and j.

The two classic examples are both `[3,3]`:

- **Cope rearrangement**: 1,5-hexadiene → 1,5-hexadiene (degenerate).
- **Claisen rearrangement**: allyl vinyl ether →
  4-pentenal (γ,δ-unsaturated carbonyl). Widely used in synthesis.

Woodward-Hoffmann rule: for `[3,3]` thermal, suprafacial-suprafacial
is allowed (6 electrons, like the DA). Low barriers are typical
(~100 kJ/mol for Cope), and temperatures of 150–250 °C usually suffice.

## Orbital-symmetry analysis — the two key tools

Two equivalent frameworks agree on every prediction:

**1. Frontier Molecular Orbital (FMO) theory** — Fukui + Woodward.
Analyse the interaction of the HOMO of one component with the LUMO of
the other (or, for intramolecular, HOMO-HOMO if symmetry demands).
Bonding overlap at both ends of the reacting π system means *allowed*;
opposite-phase overlap means *forbidden*.

**2. Orbital-correlation diagrams** — Woodward + Hoffmann.
Classify each MO by its symmetry element (mirror plane, rotation axis).
Connect reactant MOs to product MOs preserving symmetry. If an occupied
reactant MO correlates with an unoccupied product MO, the ground-state
process is forbidden.

For a quick shortcut, use the **electron-count rule** — the number of
(4q+2)ₛ + (4r)ₐ components in the TS, where s = suprafacial and a =
antarafacial. Thermally allowed if odd, photochemically allowed if even.

## Why this all matters

Pericyclic reactions are:

- **Stereospecific**. The TS's orbital-phase requirement forces a
  specific geometric outcome (endo, disrotatory, etc.). Unlike polar
  mechanisms where stereochemistry can be scrambled by ionisation,
  pericyclic TSs *preserve* stereochemistry deterministically.
- **Predictable**. Once you know the orbital-symmetry rule, you can
  predict whether a reaction happens without running it.
- **Widely deployed**. Diels-Alder is the bedrock of polymer synthesis
  (hexamethylenediamine → nylon-6,6 via ring-opening), natural-product
  synthesis, and Lego-block assembly of polycyclic scaffolds.

## Practice

1. In the Reactions tab, open **Diels-Alder** and **6π electrocyclic**.
   Render their energy profiles. Both have one-barrier profiles — the
   hallmark of concerted pericyclic chemistry.
2. Ask the tutor: "Is the `[2+2]` cycloaddition of two ethenes thermally
   allowed?" (Answer: no — 4 π electrons, thermal, suprafacial-
   suprafacial → forbidden. Photochemical promotion to 3 + 1 = 4
   changes things.)
3. Use `huckel_mos` on butadiene and cyclobutadiene; compare HOMOs.
   Why is the 4-electron thermal `[2+2]` forbidden while the 6-electron
   thermal `[4+2]` works?
4. Read the **Reaction energetics** lesson for the thermodynamic-vs-
   kinetic story that explains endo/exo Diels-Alder selectivity.

Next: **Organometallic chemistry** — the other major family of modern
C-C bond-forming reactions, driven by oxidative addition and
reductive elimination rather than concerted orbital symmetry.
