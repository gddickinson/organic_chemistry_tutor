# Carbohydrate chemistry — Fischer, Haworth, anomers, glycosides

The Beginner *Sugars and carbohydrates* lesson covered the
big picture. This goes deeper: how chemists draw + name +
manipulate sugars, and the role of the anomeric centre that
makes carbohydrate chemistry hard.

## Open vs cyclic forms

Glucose is a 6-carbon aldose:

```
CHO            HOH₂C-O                  HOH₂C-O
H-C-OH                 OH                       OH
HO-C-H        HO          OH         HO              H
H-C-OH               OH                          OH
H-C-OH       (β-pyranose, OH up)      (α-pyranose, OH down)
CH₂OH
(open chain, < 0.1 %)
```

In water, < 0.1 % is open chain; ~ 64 % β-pyranose and
~ 36 % α-pyranose at equilibrium. The **anomeric carbon**
(C1) is the new stereocentre formed by ring closure.

## Fischer projections

The 19th-century convention:

- Vertical bonds go **back** (away from viewer).
- Horizontal bonds come **forward** (toward viewer).
- Carbon backbone runs vertical, top = most-oxidised end
  (CHO or COOH), bottom = least-oxidised (CH₂OH).

D-sugar: highest-numbered chiral C has its OH on the right.
L-sugar: OH on the left. > 99 % of natural sugars are D.

## Haworth projections

The 6-membered hemiacetal ring drawn flat:

- Atoms drawn in a plane with O at upper right.
- OH/H groups drawn up or down.
- α/β assignment for the anomeric C: opposite face of CH₂OH
  = α; same face as CH₂OH = β.

For D-glucose: C6 (CH₂OH) points up. β = OH up at C1; α =
OH down.

## Chair conformations of pyranoses

Pyranoses adopt chair conformations like cyclohexane.
β-D-Glucopyranose puts every substituent (incl. OH at C1)
**equatorial** — the most stable monosaccharide
configuration possible:

```
β-D-Glc (4C1 chair):
all OH + CH₂OH equatorial → ~ 64 % at equilibrium
```

α-D-Glucose has C1-OH axial (worse), so α/β ratio favours
β.

## Mutarotation

A solution of pure α-D-glucose has [α]_D = +112° initially,
slowly drifting to +52.7° as α + β equilibrate. This
**mutarotation** is acid- + base-catalysed via the open-
chain aldehyde.

## Glycosidic bonds + glycosylation

Two sugars link via a **glycosidic bond** — the anomeric
hydroxyl (hemiacetal OH) condenses with another OH:

```
α-D-Glc-(1→4)-α-D-Glc = maltose
β-D-Gal-(1→4)-β-D-Glc = lactose
α-D-Glc-(1↔2)-β-D-Fru = sucrose
```

Notation: linkage glycoside-anomer (1 → C-of-acceptor).
Sucrose is special: both anomeric carbons are tied up so
neither sugar can mutarotate → non-reducing.

## Reducing vs non-reducing sugars

A **reducing sugar** has a free anomeric OH (hemiacetal),
which can ring-open to the aldehyde + reduce Tollens'
reagent (Ag(NH₃)₂⁺) or Fehling's. Glucose, fructose,
maltose, lactose are reducing. Sucrose, trehalose, methyl
glycosides are non-reducing.

## Glycosylation — the synthesis problem

Forming a glycosidic bond stereoselectively at the anomeric
centre is **the hardest controlled chemistry in
carbohydrate synthesis**. Methods:

- **Koenigs-Knorr** (1901) — glycosyl bromide + Ag₂CO₃ +
  ROH → β-glycoside via SN2-like. Modern: AgOTf, Hg salts.
- **Trichloroacetimidate method** (Schmidt, 1980) — donor:
  glycosyl-O-C(=NH)CCl₃ + ROH + cat. TMSOTf or BF₃·OEt₂.
- **Thioglycosides** (Lönn, Fügedi) — donor: glycosyl-
  SR + activator (NIS, MeOTf) → reactive intermediate.
- **Selenoglycosides** + **glycosyl fluorides** + many
  others.

Stereocontrol depends on a **C-2 protecting group**. A
participating C2-OAc forms an acyloxonium intermediate that
forces β attack (1,2-trans). A non-participating C2-OBn
allows α / β mixtures via SN1.

## Protecting groups in carbohydrate synthesis

A glucose has 4 OH + 1 CH₂OH + 1 anomeric OH — **6
hydroxyls** of similar reactivity. Carbohydrate synthesis
spends most of its time protecting + deprotecting:

- **Benzyl (Bn)** — H₂/Pd-C labile; long-term protection.
- **Acetyl (Ac)** — base labile; short-term + neighbouring-
  group active.
- **Benzoyl (Bz)** — base labile; bulkier, more
  participatory.
- **Benzylidene (PhCH<)** — protects 4,6-OH as a 6-membered
  acetal; opened with NaCNBH₃ + HCl to free 4-OH or 6-OH
  selectively.
- **PMB** — DDQ labile.
- **TBS, TBDPS** — F⁻ labile.

## Naming polysaccharides

| Polymer | Monomer | Linkage |
|---------|---------|---------|
| Starch (amylose) | α-D-Glc | (1→4) linear |
| Starch (amylopectin) | α-D-Glc | (1→4) + (1→6) branches |
| Glycogen | α-D-Glc | (1→4) + dense (1→6) branches |
| Cellulose | β-D-Glc | (1→4) linear, fibrous |
| Chitin | β-D-GlcNAc | (1→4) |

The α vs β linkage is the difference between digestible
starch and indigestible cellulose — humans don't have a
β-1,4-glucanase.

## Try it in the app

- **Carbohydrates tab** → load α-glucose, β-glucose,
  fructose, sucrose, lactose, maltose, cellulose fragment;
  see Haworth + open-chain forms.
- **Reactions tab** → look at Fischer glycosylation seeded
  reactions.
- **Glossary** → search *Anomer*, *Mutarotation*, *Glycoside*,
  *Reducing sugar*, *Pyranose*, *Furanose*.

Next: **Amino acid + peptide chemistry**.
