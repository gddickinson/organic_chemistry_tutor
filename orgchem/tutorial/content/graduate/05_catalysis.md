# Catalysis — a Unified Survey

Catalysis is the quiet protagonist of modern organic chemistry. The
Haber-Bosch process feeds half the world's population; asymmetric
hydrogenation earned a Nobel Prize; DNA polymerase writes the
instructions for every living cell. What they share is the same
formal definition:

> A **catalyst** accelerates a reaction without being consumed,
> by offering an alternative pathway with lower activation
> energy — and does *not* shift the position of equilibrium.

This lesson synthesises the five catalysis families you'll meet
across the seeded pathways + reactions into one cross-referenced
table. Open *View → Command palette…* (Ctrl+K) and jump to any
Synthesis / Reactions entry mentioned below to see the mechanism
in context.

## 1. Homogeneous catalysis (soluble metal complex)

The catalyst is a single molecular species dissolved in the same
phase as the substrate. Rational ligand design lets the chemist
tune electronic and steric demands on the metal with pharmacist-
level precision.

**Canonical seeded example: Knowles Rh-DIPAMP asymmetric hydrogenation**
(Synthesis → *L-DOPA — Knowles Rh-DIPAMP asymmetric route*, step 2).

    (Z)-dehydroamino acid + H₂ / [Rh((R,R)-DIPAMP)]⁺
       → (S)-N-acetyl-3,4-dimethoxyphenylalanine    (≥ 95 % ee)

The chiral-at-phosphorus bisphosphine differentiates the two
prochiral faces of the olefin. Nobel Prize 2001, shared with
Noyori and Sharpless. Turnover number > 10 000; industrial ton-
scale at Monsanto.

Other homogeneous catalysts in the seeded reactions:
- **Suzuki coupling** (Pd(PPh₃)₄ in aryl halide + aryl boronic acid)
- **Buchwald-Hartwig amination** (Pd / XPhos)
- **Sonogashira coupling** (Pd / Cu co-catalysis)
- **Mitsunobu reaction** (DIAD / PPh₃ as stoichiometric
  "co-catalyst" pair — pushes the boundary of the term).

## 2. Heterogeneous catalysis (solid surface)

The catalyst is a solid; the substrate is a liquid or gas.
Active sites live on the surface. Less selectivity control than
a tailored ligand, but hugely practical: filter it off, reuse it,
no metal leaching into the product.

**Canonical seeded example: Pd-C hydrogenolysis of a Cbz group**
(Synthesis → *Aspartame — Z-protected peptide coupling*, step 2).

    Z-aspartame + H₂ / 10 % Pd-C → aspartame + PhCH₃ + CO₂

The Pd surface dissociates H₂ into two Pd-H species; the
benzylic C-O bond of the Cbz adsorbs onto the surface and is
cleaved via concerted addition of surface H + reductive
elimination. Mild, neutral, no epimerisation at α-stereocentres.

Other heterogeneous examples in the seeded content:
- **Cyclohexane air oxidation** (Co / Mn naphthenate, Adipic-acid
  step 1) — a *supported metal* rather than a polished surface.
- **Vapour-phase Beckmann rearrangement** mentioned in the
  Nylon-6 description as the greener alternative to oleum;
  zeolite ZSM-5 catalyst.
- Historical: Sabatier hydrogenation over Ni (1912 Nobel) — the
  ancestor of modern Pd-C / Pt-C workhorses.

## 3. Enzymatic catalysis (nature's rate enhancements)

Enzymes are protein catalysts that routinely accelerate
reactions by factors of 10¹⁰–10¹⁷ — orders of magnitude beyond
anything a chemist builds from scratch. They achieve this via
preorganised active sites, ground-state destabilisation,
transition-state stabilisation, and proximity / orientation
effects.

Three seeded enzyme mechanisms exemplify the three mechanistic
strategies (Reactions tab, has-mechanism rows):

| Enzyme | Strategy |
|--------|----------|
| Chymotrypsin (catalytic triad) | **Nucleophilic catalysis** — Ser hydroxyl as the attacker, His as general base |
| Class-I aldolase (Schiff base) | **Covalent intermediate** — Lys forms a Schiff base, lowering the α-pKa |
| HIV protease (Asp₂) | **Acid-base catalysis** — paired Asp residues activate water |
| RNase A (2× His) | **General acid + base** flanking an in-line phosphoryl transfer |

Beyond the arrow-pushing view, the {term:Pharmacophore} entry in
the Glossary explains why the same catalytic-feature *pattern*
can be built into small-molecule drugs that mimic enzyme
transition states (e.g. statins → HMG-CoA reductase TS
mimics).

And one industrial crossover in the seeded pathways:

- **Thermolysin in aspartame synthesis** — the enzyme is α-
  regioselective for the aspartyl α-COOH coupling to Phe-OMe,
  eliminating the need for Cbz protection.  Ajinomoto ran this
  at 15 000 t / yr in the 1990s.
- **AADC (aromatic-L-amino-acid decarboxylase)** activates
  L-DOPA *in vivo* — the seed rationale for why L-DOPA (not
  dopamine) is dispensed. PLP cofactor + an electron-sink
  quinonoid intermediate you can walk through in the
  *Dopamine* synthesis description.

## 4. Lewis-acid catalysis

A Lewis acid accepts a lone pair from a substrate heteroatom,
polarising its neighbouring bonds and making them electrophilic.
The catalyst is regenerated on product release.

**Canonical seeded example: AlCl₃ in Friedel-Crafts**
(Reactions tab → *Friedel-Crafts alkylation of benzene*, 3-step
mechanism).

    CH₃Cl + AlCl₃ → CH₃⁺  AlCl₄⁻   (activation)
    benzene + CH₃⁺ → Wheland        (EAS)
    AlCl₄⁻ + Wheland → toluene + HCl + AlCl₃   (rearomatise)

AlCl₃ shuttles chloride back and forth — nominally catalytic
but usually super-stoichiometric in practice because the
product amide or ketone coordinates to Al and traps it.

Other seeded Lewis-acid catalysts:
- BF₃ in Mukaiyama aldol chemistry
- ZnCl₂ as an alternative to H₂SO₄ in the phenolphthalein melt
  condensation

## 5. Brønsted-acid catalysis

A proton moves. Simple, cheap, ubiquitous — protonating a
carbonyl oxygen makes the carbonyl carbon dramatically more
electrophilic; protonating a leaving group turns -OH into -OH₂⁺
which leaves as water.

**Two seeded mechanisms walk through it step-by-step:**

- **Fischer esterification** (5 steps) — the classical acid-
  catalysed esterification. Each step prints inline how the
  proton shuttles.
- **Pinacol rearrangement** (4 steps) — protonation → water
  departure → 1,2-methyl shift → deprotonation.
- **Beckmann rearrangement** (Nylon-6 synthesis step 2) — conc.
  H₂SO₄ protonates the oxime O; the anti C-C bond migrates to N.

The catalytic turnover: the proton comes in at the first step,
leaves at the last, and the net reaction consumes no acid.

## How to tell them apart

| Feature | Homogeneous | Heterogeneous | Enzyme | Lewis acid | Brønsted acid |
|--------|------------|---------------|--------|-----------|--------------|
| Phase | liquid | solid | aqueous | liquid | liquid |
| Selectivity | tunable via ligands | low → fair | exquisite | moderate | low |
| Recovery | hard | easy | tricky | hard | easy |
| Turnover freq | 10²–10⁶ h⁻¹ | 10¹–10⁴ h⁻¹ | 10⁴–10⁸ h⁻¹ | 10⁰–10³ h⁻¹ | 10⁰–10³ h⁻¹ |
| Classic Nobel | Knowles, Noyori, Sharpless (2001); Grubbs, Schrock (2005) | Sabatier (1912); Ertl (2007) | many — e.g. Sumner's urease crystallisation (1946) | — | — |

## Cross-cutting theme — transition-state stabilisation

All five families do the same thing at the level of the
reaction-coordinate diagram (open *06_energetics* lesson for
the picture). The catalyst opens a *different path* whose TS
is **lower in energy** than the uncatalysed one. The reactants
and products have the same energy on both paths, so ΔG is
unchanged; only Ea drops.

That single sentence is the deepest thing we know about
catalysis.  The five families are just different ways to
implement it — through dative bonds, through surface
adsorption, through preorganised hydrogen bonds, through
protonation.

## Exercises

1. Re-read the Aspartame pathway's step 1 notes. Why would a
   chemist choose thermolysin over DCC coupling?  List three
   concrete advantages in terms of the five families above.
2. Open the *Dopamine* synthesis description.  The step uses
   AADC (an enzyme) or Ba(OH)₂ (a Brønsted base, heat).  Name
   one practical advantage of each route.
3. Suzuki coupling (homogeneous Pd) vs Ni-catalysed cross-
   coupling (supported heterogeneous) — what considerations
   push a process chemist toward one or the other?
4. Explain, in one sentence each, why Ea drops in homogeneous
   vs Brønsted-acid catalysis.  Use the TS-stabilisation
   framing.

## See also

- Glossary: {term:Activation energy}, {term:Hammond postulate},
  {term:Regioselectivity}, {term:Chemoselectivity},
  {term:Pharmacophore}.
- Tutorials: intermediate / 06 Reaction energetics;
  intermediate / 08 Radicals (the non-catalytic third family);
  graduate / 02 Asymmetric synthesis.
- Synthesis tab: L-DOPA (Knowles), Aspartame, Nylon-6
  (Beckmann), Phenolphthalein (Brønsted), Friedel-Crafts
  alkylation (Lewis).
