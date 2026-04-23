# Aromaticity and Electrophilic Aromatic Substitution

Benzene is weird. It has three double bonds written in the Kekulé
structure, but it doesn't behave like an alkene — it doesn't add
bromine across the π bonds, it doesn't hydrogenate under mild
conditions, and its six C-C bond lengths are all identical (1.40 Å,
halfway between single and double). Aromaticity is the name for this
special stability, and it governs an enormous amount of organic
chemistry.

## Hückel's rule

A cyclic, fully conjugated, planar π system is **aromatic** when it has

    4n + 2   π electrons   (n = 0, 1, 2, …)

So 2, 6, 10, 14, … are aromatic magic numbers. 6 is benzene.

A cyclic, fully conjugated, planar π system with **4n** π electrons is
**antiaromatic** — *destabilised* compared to the linear reference.
Cyclobutadiene (4) and cyclooctatetraene-if-forced-flat (8) are the
textbook cases.

Everything else (non-planar, non-cyclic, or incomplete conjugation) is
just **non-aromatic** — behaves like a regular alkene.

## Proving it with Hückel MO theory

The app ships a simple Hückel MO engine (`orgchem/core/huckel.py`) that
computes the π MOs by eigendecomposing the adjacency matrix of the π
subsystem. In the tutor, ask:

> Compute the Hückel MO diagram for benzene.

Under the hood: the action `huckel_mos(smiles="c1ccccc1")` returns
eigenvalues [+2, +1, +1, −1, −1, −2] (in units of β, with α = 0). The
six π electrons fully occupy the three bonding MOs (+2, +1, +1) and
leave the three antibonding MOs empty — that's the aromatic
stabilisation.

Compare to butadiene (`C=CC=C`): four electrons, eigenvalues ±1.618,
±0.618. Still stable, but not specially so — you can add Br₂ across the
diene in the cold, you can hydrogenate it, it's a normal polyene.

Now run the `export_mo_diagram` action on benzene and save a PNG — the
three bonding MOs fill, HOMO / LUMO are labelled, the **zero-net-bonding
gap** jumps out at you.

## 5-rings and 7-rings count too

- **Cyclopentadienide anion (Cp⁻)**: 5 sp² carbons + one extra π
  electron from the negative charge = 6 π electrons. **Aromatic.**
  Super stable; that's why it's ubiquitous as a ligand.
- **Cycloheptatrienyl cation (tropylium)**: 7 sp² carbons − 1 electron
  (positive charge) = 6 π electrons. **Aromatic.** One of the rare
  stable-at-room-temp carbocations.
- **Pyrrole**: 5-ring with N-H. The nitrogen contributes its lone pair
  to the π system, so 4 × C(1) + 1 × N(2) = 6. **Aromatic.**
- **Pyridine**: 6-ring with N. The nitrogen's lone pair sits in an sp²
  orbital **in the ring plane** — it doesn't contribute to the π
  system. So 5 × C(1) + 1 × N(1) = 6. Still **aromatic**, and the lone
  pair makes the ring basic.
- **Furan / Thiophene**: same logic as pyrrole — the heteroatom's lone
  pair is donated to the π system. **Aromatic.**

## Electrophilic aromatic substitution (EAS)

Because benzene is so stable, it prefers to regenerate the aromatic
system rather than add across π bonds. The mechanism is therefore
**substitution**, not addition:

1. The aromatic ring's π electrons attack an electrophile (E⁺), giving
   a **cationic arenium intermediate** (a.k.a. σ-complex, a.k.a.
   Wheland intermediate). This step breaks aromaticity and is the
   **rate-determining step**.
2. A weak base deprotonates the sp³ carbon that picked up E⁺,
   restoring aromaticity.

The seeded reactions **Friedel-Crafts alkylation**, **Friedel-Crafts
acylation**, and **Nitration of benzene** all follow this pattern.
Open any of them in the Reactions tab.

## The five canonical EAS reactions

| Reaction                 | Electrophile              | Catalyst  |
|:-------------------------|:--------------------------|:----------|
| Halogenation             | X⁺ (from X₂ + FeX₃)       | FeX₃      |
| Nitration                | NO₂⁺                      | H₂SO₄     |
| Sulfonation              | SO₃ / HSO₃⁺               | fuming H₂SO₄ |
| Friedel-Crafts alkylation| R⁺                        | AlCl₃     |
| Friedel-Crafts acylation | RCO⁺ (acylium)            | AlCl₃     |

## Directing effects

A substituent already on the ring biases where the next electrophile
goes in.

- **Activating + ortho/para-directing**: electron donors — `-OH`,
  `-OR`, `-NH₂`, `-NR₂`, `-R` (alkyl). They stabilise the cationic
  intermediate at the ortho and para positions (where the (+) can sit
  next to the donor).
- **Deactivating + meta-directing**: electron withdrawers — `-NO₂`,
  `-CN`, `-COR`, `-CO₂H`, `-SO₃H`. They destabilise the ortho/para
  intermediates more than meta, so meta wins by default.
- **Deactivating + ortho/para-directing** (odd ones out): halogens
  (`-F`, `-Cl`, `-Br`, `-I`). They're σ-withdrawing (deactivating) but
  π-donating via lone pair (ortho/para-directing).

## Practice

1. Open the **Glossary tab**, search "aromatic", and read the
   **Aromaticity** and **EAS** entries.
2. In the Molecule Workspace load **Naphthalene**, **Pyridine**,
   **Pyrrole**, and **Furan**. Compute their logPs (Properties panel)
   and notice how the heterocycles with N-H / O / S are more
   water-soluble than the all-C analogue.
3. Ask the tutor to compute Hückel MOs for **cyclobutadiene**
   (`C1=CC=C1`) and confirm it gets an antiaromatic diagnosis
   (4 electrons, two singly-occupied degenerate non-bonding orbitals).
4. Export the MO diagrams for benzene, butadiene, and pyrrole. Compare
   the HOMO-LUMO gaps — benzene's is largest, which correlates with
   its UV spectrum.

Next: **Carbonyl chemistry** — another big family where the π system
matters, but this time it's the C=O that drives everything.
