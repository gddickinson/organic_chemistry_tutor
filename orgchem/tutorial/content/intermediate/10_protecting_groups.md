# Protecting Groups

Most synthesis targets carry **two or more reactive functional
groups**.  You want to transform one while leaving the others
untouched — but a good reagent rarely discriminates on its own.
The standard answer: temporarily **mask** the groups you don't
want to touch, run your reaction, then peel the masks off.

This lesson walks the protecting-group toolkit that underpins
most of the seeded pharmaceutical syntheses — *and* the modern
philosophy that prefers to avoid protection entirely via
regioselective enzymes or catalysts (Anastas principle 8).

## Why protect? — the chemoselectivity problem

Concrete example from the seeded Aspartame pathway
(Synthesis tab → *Aspartame — Z-protected peptide coupling*):

    L-aspartic acid has TWO carboxyl groups (α and β)
    L-phenylalanine has ONE carboxyl (α) and ONE amine (α)

If you throw all four groups into a DCC coupling, the diacid's
β-COOH would compete with its α-COOH to form the amide — and
you'd lose α-α regioselectivity.  The aspartame you want
(α-α dipeptide) is sweet; the β-α isomer is bitter.  One
regio-wrong amide bond changes a food additive into an unsold
failure.

The industrial fix of the 1970s: mask the aspartate α-NH₂ with
**Cbz** (benzyloxycarbonyl, Z).  That turns the α-amine into a
carbamate — not nucleophilic enough to compete with the
α-carboxyl — so the coupling goes cleanly α-α.

## The three properties every protecting group needs

1. **Installable selectively.**  You need a way to put the
   mask on only the target group.
2. **Stable to the reactions you're running.**  Otherwise it
   falls off in the middle.
3. **Removable selectively at the end** — crucially, without
   disturbing the other protecting groups or the new bond
   you just made.

Property 3 is what makes **orthogonality** the key design
idea.  Two protecting groups are "orthogonal" when you can
remove either one **without** touching the other.

## Orthogonal amine protection — the three you'll meet

| Group | Install | Deprotect | Stable to… | Not stable to… |
|-------|---------|-----------|-----------|-----------------|
| **Cbz (Z)**  | Cbz-Cl + base | H₂ / Pd-C | acid, base | hydrogenolysis |
| **Boc** | Boc₂O + base | TFA or dilute HCl | base, nucleophiles, hydrogenolysis | strong acid |
| **Fmoc** | Fmoc-Cl + base | piperidine / DMF | acid, hydrogenolysis | base (β-elimination) |

The magic:

- Cbz and Boc are orthogonal — H₂/Pd drops the Cbz but leaves
  the Boc; TFA drops the Boc but doesn't touch the Cbz.
- Fmoc and Boc are orthogonal — base drops Fmoc but not Boc;
  acid drops Boc but not Fmoc.
- Fmoc and Cbz are **partially** orthogonal — piperidine
  doesn't touch Cbz, but H₂/Pd drops the Cbz and also cleaves
  some Fmocs through side reactions.

This is why **solid-phase peptide synthesis (SPPS)** uses
Fmoc/tBu chemistry: Fmoc on the growing chain's α-NH₂ (pop
off with base) + tBu-based side-chain protection (pop off at
the end with TFA).  Orthogonal cleavage between chain-
extension and final-cleavage steps.  Seeded example: Synthesis
tab → *Met-enkephalin via Fmoc SPPS 5-step*.

### Cbz hydrogenolysis — mechanism

    Ph-CH₂-O-CO-NR₂  + H₂ / Pd  →  Ph-CH₃ + CO₂ + HNR₂

The Pd surface dissociates H₂ into two adsorbed H atoms.  The
benzylic C-O bond of the Cbz adsorbs + the H migrates,
cleaving to give toluene + a carbamic acid (HO-CO-NR₂).  The
carbamic acid spontaneously loses CO₂ to give the free amine
plus H₂O.  Neutral, mild, no epimerisation at α-carbons —
which is why it's the SPPS-era workhorse for solution-phase
work.  (Full mechanism in the Aspartame pathway step 2 notes.)

### Fmoc deprotection — mechanism (E1cb)

    Fluorenyl-CH₂-O-CO-NR₂  + piperidine  →
      dibenzofulvene (trapped by piperidine) + CO₂ + HNR₂

Piperidine (a 2° amine) abstracts the **acidic C-H** on the
fluorenyl CH (pKa ~22 — unusually acidic because the resulting
carbanion is aromatic cyclopentadienyl-stabilised).  The
carbanion kicks out the carbamate through an E1cb β-elimination,
giving dibenzofulvene + carbamic acid (→ CO₂ + free amine).
The dibenzofulvene is then Michael-trapped by the same
piperidine; that piperidine-adduct byproduct is why SPPS
washes need excess piperidine.

### Boc deprotection — mechanism (SN1)

    Me₃C-O-CO-NR₂  + H⁺  →  Me₃C⁺ + HO-CO-NR₂
    Me₃C⁺ → Me₂C=CH₂ (+ H⁺)
    HO-CO-NR₂ → CO₂ + HNR₂

Protonation of the carbamate carbonyl; the tert-butyl C-O
bond heterolyses with the stabilised tertiary cation;
t-butyl cation eliminates a proton to give isobutylene (the
driving-off byproduct).  Fast, clean, mild enough to keep
most other protecting groups intact.

## Alcohol + carboxylic-acid protection

Common alcohol protection:

| Group | Install | Deprotect |
|-------|---------|-----------|
| **Ac** (acetate) | Ac₂O / pyridine | K₂CO₃ / MeOH |
| **Bn** (benzyl) | NaH + BnBr | H₂ / Pd-C |
| **TBS** (t-butyldimethylsilyl) | TBS-Cl + imidazole | TBAF or dilute F⁻ |
| **MOM** (methoxymethyl) | MOM-Cl + i-Pr₂NEt | dilute HCl, MeOH |

Carboxylic-acid protection is usually just the ester:

| Group | Install | Deprotect |
|-------|---------|-----------|
| **Me ester** | MeOH, H⁺ or CH₂N₂ | LiOH / H₂O |
| **Bn ester** | BnOH, H⁺ or BnBr, Cs₂CO₃ | H₂ / Pd-C |
| **tBu ester** | isobutylene + H⁺ | TFA |

Note the **pairing orthogonality**: a Bn ester is cleaved by
H₂/Pd, same as Cbz — so don't use both in the same sequence
unless you want to drop them together on purpose.  A tBu
ester pairs with Fmoc (Fmoc: base; tBu: acid) — that's
exactly the combination SPPS uses.

## Carbonyl protection — acetals

Aldehydes and ketones are dramatically more reactive than
most other functional groups.  Two routes to mask them:

    R-CHO + (HOCH₂CH₂OH) + H⁺ → cyclic acetal + H₂O
                                (1,3-dioxolane)

Acetal formation is reversible: mildly acidic aqueous
conditions regenerate the carbonyl.  Stable to everything
basic or reducing that would otherwise hit C=O.  Popular
with diols (ethylene glycol, 2,2-dimethylpropane-1,3-diol).

## Orthogonal protection in action — SPPS

Fmoc-SPPS runs the cycle:

    1. Resin-bound H₂N-Xaa — attach Fmoc-AA via the amide bond.
    2. Pop Fmoc with 20 % piperidine in DMF (bases peptide α-NH₂).
    3. Repeat with the next Fmoc-AA.
    4. …
    N. Final: TFA cocktail cleaves the peptide off the resin AND
       removes every tBu-based side-chain protecting group in
       one step.

Two orthogonal axes (base for chain extension, acid for
global cleavage) make the whole machine work.  Without
orthogonal protecting groups, each coupling would require a
custom deprotection — and peptide synthesis couldn't be
automated.

## When to avoid protecting groups entirely

Every Anastas-principle-8 win (review green-chemistry lesson
*advanced/05*) says: **don't protect if you can get
regioselectivity from the reagent itself.**

- **Thermolysin** catalyses the α-regioselective aspartame
  peptide coupling **with no protection on either partner**.
  Ajinomoto industrial practice since 1982.
- **Suzuki coupling** of an aryl halide + an aryl boronic
  acid ignores amide and ester groups elsewhere on the
  molecule — so biaryl formation rarely needs protection.
- **Knowles asymmetric H₂** hits only C=C bonds, not C=O,
  so you keep acid / ester functionality intact at 3 atm
  H₂ / Rh without protection.

The discipline: every time you add a protecting group, your
route gets two steps longer and your atom economy drops.
Always ask "could a selective catalyst / enzyme replace this
mask?"  Often it can't — but asking is the habit that
separates a clean route from a 12-step one.

## Exercises

1. You are running SPPS.  At step 3 you discover you set
   down an unprotected cysteine thiol — which orthogonal
   protecting group for -SH should you use, and what takes
   it off?  (Hint: look up *Trt* and *Mmt*.)
2. Why is **Boc-on-amine + Me ester on COOH** NOT a good
   choice for a route that ends in a base-catalysed
   saponification of the methyl ester?  (Hint: what is the
   Boc stable to?)
3. The seeded L-DOPA route uses **Ac on the amine + Me
   ether on both catechol OHs**.  Step 3 removes everything
   in one HBr cocktail.  What is the green-chemistry
   objection to this combined deprotection?
4. Design a fictional route that installs a Bn ester,
   then a Cbz on an amine later.  What global deprotection
   step will drop BOTH in one pot?
5. Three amine-protecting groups (Cbz / Boc / Fmoc) sit
   on three different amines in one molecule.  You want to
   reveal just the Fmoc-protected one.  What reagent + why?

## See also

- Synthesis tab: Aspartame (Cbz + DCC + Pd/H₂),
  Met-enkephalin Fmoc SPPS, L-DOPA (Ac + Me ether),
  Procaine (no protection).
- Graduate / 02 Asymmetric synthesis — why Knowles-style
  catalysis sometimes replaces protection entirely.
- Graduate / 05 Catalysis — the five-family view.
- Advanced / 05 Green chemistry — Anastas principle 8.
- Glossary: {term:Chemoselectivity}, {term:Regioselectivity},
  {term:Stereocentre} (why protecting groups rarely
  epimerise α-stereocentres, and when they do).
