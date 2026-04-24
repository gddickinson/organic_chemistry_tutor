# Polymer Chemistry

Polymers are long-chain molecules built from repeating
**monomer** units.  Essentially every plastic, fibre, rubber
and gel in your daily life is a polymer — and so are DNA,
proteins, cellulose and glycogen.  This lesson shows the two
canonical ways chemists stitch monomers together, the maths
that governs chain length, and why tiny mechanistic choices
change the resulting material from flexible cling film to
bullet-proof armour.

## Two mechanistic families

Every synthetic polymer is assembled by **one** of two
mechanisms.  The distinction is not optional — it dictates
every downstream property.

### 1. Step-growth polymerisation

Any two difunctional monomers that can react end-to-end
(diamine + diacid, diol + diacid, diisocyanate + diol) build
chains by condensing one bond at a time.  Every molecule in
the pot can couple with every other — **dimers → tetramers →
octamers** — so high molecular weight is only reached at
~99 %+ conversion.

**Canonical seeded example** (Synthesis tab → *Nylon-6,6*):

    n HOOC–(CH₂)₄–COOH + n H₂N–(CH₂)₆–NH₂
        → [ –OC–(CH₂)₄–CO–NH–(CH₂)₆–NH– ]ₙ  + 2n H₂O

**Carothers's equation** gives the degree of polymerisation
as a function of reaction extent p:

    DP = 1 / (1 − p)

Some worked numbers:

    p = 0.90  → DP =  10   (oligomer, crumbly)
    p = 0.99  → DP = 100   (plastic, MW ~12 kDa for nylon-6,6)
    p = 0.995 → DP = 200   (fibre-grade)
    p = 0.999 → DP = 1000  (research-grade, difficult to hit)

This is why **stoichiometric control matters**: a 1 % excess
of one monomer caps the chain ends and puts a hard ceiling on
DP.  Carothers's trick — crystallise the 1:1 AH salt (the
seeded nylon-6,6 pathway step 1) — is the industrial answer.

Step-growth polymers that show up in the seeded synthesis
catalogue:

| Polymer | Monomers |
|---------|----------|
| Nylon-6,6 | adipic acid + hexamethylenediamine |
| Nylon-6  | ε-caprolactam (ring-opened) |
| Polyester (PET)  | terephthalic acid + ethylene glycol |
| Polyurethane | diisocyanate + diol |
| Polycarbonate | bisphenol-A + phosgene (or DPC) |

### 2. Chain-growth (addition) polymerisation

One active chain end adds monomers one at a time.  The chain
grows to high MW *immediately* and monomer concentration
drops linearly over time.  Molecular weight does *not* depend
on extent of reaction — it depends on initiator / monomer
ratio and on the balance of propagation vs termination.

    I• + n CH₂=CHR → I–CH₂–CHR(–CH₂–CHR–)ₙ₋₁–•

Most commodity plastics are chain-growth:

| Polymer | Monomer | Initiator |
|---------|---------|-----------|
| Polyethylene (HDPE / LDPE) | CH₂=CH₂ | Ziegler-Natta / radical |
| Polypropylene | CH₂=CHCH₃ | Ziegler-Natta metallocene |
| Polystyrene | CH₂=CHPh | radical (AIBN, peroxide) |
| PVC | CH₂=CHCl | radical |
| Teflon (PTFE) | CF₂=CF₂ | radical |
| Polyacrylonitrile | CH₂=CHCN | radical |
| Polymethyl methacrylate | CH₂=C(CH₃)CO₂Me | radical |

Three subclasses by the kind of active end:

- **Radical** — described fully in intermediate lesson 08.
  Starts with a thermolysed peroxide or AIBN; chain ends are
  carbon radicals.  Insensitive to trace water and oxygen at
  low conversion — the reason PE/PS/PVC are made this way.
- **Cationic** — isobutylene → polyisobutylene (butyl rubber).
  BF₃ or H₂SO₄ initiates; very fast, hard to control.
- **Anionic** — styrene + *n*-BuLi gives "living" polystyrene
  with narrow MW distribution.  Used for block copolymers
  (e.g. SBS thermoplastic elastomers in shoe soles).

## Tacticity — the missing dimension

Vinyl polymers have a stereocentre at every repeat unit.
The *relative* configuration along the chain controls
crystallinity, and therefore melting point and mechanical
strength.

    Isotactic     — all stereocentres same (R, R, R, R, ...)
    Syndiotactic  — strictly alternating (R, S, R, S, ...)
    Atactic       — random

**Atactic PP** is a sticky amorphous goo — useless.  **Isotactic
PP**, the one Ziegler and Natta won the 1963 Nobel Prize for,
is a crystalline engineering plastic (M_p 165 °C, tensile
~35 MPa) that feeds the yogurt-container industry.  Same
monomer, same backbone, totally different material.

Modern **metallocene catalysts** (Kaminsky / Brintzinger,
1980s-90s) let the chemist dial tacticity + MW distribution
at will.  Single-site homogeneous catalysis; see
{term:Activating and deactivating groups} for the EAS
analogue of picking the right ligand, and graduate lesson 05
for the broader catalysis context.

## Structure → property: Tm and Tg

Two thermal transitions every polymer student learns to name:

- **T_g — glass-transition temperature**.  Below T_g, amorphous
  chains are immobile; the polymer is a hard, brittle **glass**.
  Above T_g, chains can wiggle in the disordered regions; the
  polymer is **rubbery**.  Examples: atactic PS T_g ≈ 100 °C
  (hard at room T), polyisoprene T_g ≈ −72 °C (rubber at room T).
- **T_m — crystalline melting point**.  Only exists for
  semi-crystalline polymers.  Above T_m, the crystalline
  domains melt and the whole thing flows.  Isotactic PP
  T_m ≈ 165 °C, HDPE ≈ 135 °C, nylon-6,6 ≈ 265 °C.

Polymers above both T_g and T_m are viscous liquids (processed
by injection moulding).  Between T_g and T_m is the
semi-crystalline useful-article range.

## Crystallinity — why nylon-6,6 beats nylon-6 in cords

Both are polyamides.  But the amide dipoles in nylon-6,6
**alternate** along the chain direction (because each amide
has an HMDA on one side + adipic acid on the other) — so
two adjacent chains can H-bond to each other with *zero* net
register strain.  In nylon-6, every amide points the **same
way** (all chains go N→C→N→C from one end), so chains must
shift by one repeat to get H-bonds to line up.  Nylon-6,6
therefore crystallises better → higher T_m (265 °C vs 220 °C),
higher modulus, better creep resistance.  That's why tyre
cords are nylon-6,6.

## Copolymers + block copolymers

Not every chain is homogeneous.  Putting two different
monomers into the pot gives:

- **Random copolymers** (statistical mix along the chain) —
  SBR (styrene-butadiene rubber, 75 % car tyres).
- **Alternating copolymers** — styrene-maleic anhydride
  (forced alternation by r₁ · r₂ ≈ 0).
- **Block copolymers** — anionic living polymerisation makes
  e.g. SBS (polystyrene-*b*-polybutadiene-*b*-polystyrene),
  the thermoplastic elastomer in sneaker soles.  Self-
  assembles into hard PS domains pinning a rubbery PB
  matrix — hence "rubbery but reprocessable."
- **Graft copolymers** — ABS (acrylonitrile-butadiene-styrene)
  where rubber particles are grafted into a brittle PS matrix.
  Lego bricks.

## Sustainability notes

Polymers are permanent at ambient conditions — that's what
makes them useful, and what makes the trash problem.
Chemistry answers:

- **Mechanical recycling** — melt and reprocess thermoplastics.
  Works well for PET (resin code #1) and HDPE (#2); degrades
  steadily for others.
- **Chemical recycling** — depolymerise back to monomer.
  PET + methanolysis → DMT + ethylene glycol → virgin PET.
  Much more promising for step-growth than for chain-growth
  (C-C bonds of vinyl chains are hard to cut selectively).
- **Biodegradable polymers** — PLA (polylactic acid, from corn-
  derived lactide), PHA (bacterial polyhydroxyalkanoate).
  Both **step-growth** (hydrolysable ester backbone) — the
  common theme.
- **Biosourced monomers** — succinic acid (vs petroleum
  adipic acid) via fermentation is a plausible route to
  bio-nylon-4,4 with lower CO₂ footprint.

## Exercises

1. Using Carothers's equation, how high must p be to get
   DP ≥ 500 for nylon-6,6?
2. Why can't you make high-MW polystyrene by step-growth?
3. Atactic PP is sticky and useless; isotactic PP is a hard
   plastic.  Both have the same empirical formula.  Draw the
   two chains and identify the difference.
4. PET's ester backbone is hydrolysable and recyclable;
   HDPE's C-C backbone is essentially not.  Explain in one
   sentence why this is.
5. Why is nylon-6,6 chosen for tyre cords instead of
   nylon-6, despite both being polyamides from cyclohexanone
   branch points?

## See also

- Glossary: {term:Regioselectivity}, {term:Hyperconjugation}
  (for chain-end stabilisation), {term:Constitutional isomer}
  (tacticity is a stereochemical, not constitutional,
  variation).
- Tutorials: intermediate / 08 Radicals (chain-growth
  mechanism details); graduate / 05 Catalysis (Ziegler-Natta
  / metallocene context).
- Synthesis tab: **Nylon-6** (Beckmann / caprolactam route),
  **Nylon-6,6** (Carothers polycondensation with the DP
  equation inline), **Adipic acid** (upstream monomer).
