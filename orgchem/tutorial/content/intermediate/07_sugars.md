# Sugars and carbohydrates

Sugars are polyhydroxy aldehydes or ketones — the name *carbohydrate*
comes from the empirical formula (CH₂O)ₙ. They're the first
biomolecule you meet that combines stereochemistry, tautomerism,
ring-chain equilibria, and stereoselective ring formation in a
single class of compound.

> Open the **Macromolecules window** (*Window → Macromolecules…* or
> Ctrl+Shift+M) and switch to the **Carbohydrates** tab to see the
> seeded catalogue of 25 sugars while you read. Click any entry to
> view its 2D structure + family, form, anomer, and glycosidic-bond
> metadata.

## D vs L: the Fischer projection trick

In the open-chain Fischer projection of a sugar, write the highest-
priority end (the aldehyde or ketone) at the top. Look at the
**bottom** stereocentre (the one farthest from the carbonyl):

- OH on the **right** → D sugar.
- OH on the **left**  → L sugar.

Almost every naturally occurring sugar is D. Your glucose, ribose,
fructose, galactose — all D. L-sugars are rare in biology but
crucial for certain antibiotics and deoxy sugars (L-fucose,
L-rhamnose).

The D/L labels are **not** about optical rotation (+/−). A sugar
can be D and yet rotate plane-polarised light left — e.g. D-fructose
is levorotatory. That's why the convention is anchored to
configuration, not to rotation.

## Chain ↔ ring (the real action)

Glucose in dilute solution is **< 1 % open-chain** at any instant.
The rest is pyranose (6-membered ring) or furanose (5-membered
ring) — the aldehyde / ketone has been attacked intramolecularly
by a hydroxyl, giving a hemiacetal / hemiketal.

### Pyranose closure

For an aldohexose like glucose, the C5 hydroxyl attacks C1. This is
a **5-exo-trig** cyclisation — favoured by Baldwin's rules. The new
stereocentre at C1 is called the **anomeric carbon**, and its two
configurations (α, OH axial in the chair; β, OH equatorial) are
called **anomers**.

In water, glucose equilibrates to **~37 % α / 63 % β / ~0.003 %
open chain / trace furanose**. The β preference is thermodynamic
(all substituents equatorial in the chair). The equilibration is
called **mutarotation** and you can watch it happen with a
polarimeter:

- Dissolve pure α-D-glucose (α = +112°) and the rotation drifts
  toward +53°.
- Dissolve pure β-D-glucose (α = +19°) and the rotation drifts
  toward the same +53°.

### Furanose closure

For ribose (an aldopentose), both 4-exo-trig (too strained) and
5-exo-trig (pyranose) and the alternative 4-OH → C1 attack (the
furanose) are accessible (a neat application of {term:Baldwin's rules}).
Ribose in water is **~76 % pyranose / 24 % furanose**. Biology
selects the **furanose** form when locking ribose into nucleosides
(ATP, RNA) — the five-membered ring has more pucker flexibility,
which matters for the phosphodiester backbone.

## Anomeric effect

Despite the "all equatorial = most stable" rule of thumb, the
anomeric OR group in a pyranose prefers **axial** orientation — the
α anomer is more stable for a purely electronegative OR
substituent. This is the **anomeric effect**.

Origin: the axial OR has a lone pair on the ring oxygen anti-
periplanar to the C–OR σ\* orbital, so there's a favourable n → σ\*
hyperconjugation. In the equatorial anomer that alignment is lost.
The stabilisation is ~4 kJ/mol — enough to flip the normal steric
preference.

The effect **gets stronger with more electronegative substituents**
(F > OR > Cl) and with non-polar solvents. It explains why
methyl-α-D-glucoside predominates over methyl-β-D-glucoside in
non-aqueous solvent.

## Glycosidic bonds: how sugars are joined

A glycosidic bond is an acetal C–O–C formed between the anomeric
OH of one sugar and a hydroxyl of another. The stereochemistry at
the anomeric carbon is frozen by the glycosylation step.

| Linkage  | Example                 | Biology          |
|----------|-------------------------|------------------|
| α-1,4    | Amylose (starch), glycogen | Energy storage — coiled helices, easily hydrolysed |
| β-1,4    | Cellulose                | Structural — linear ribbons, H-bond mats, indigestible by mammals |
| α-1,6    | Glycogen branch points   | Compact branching, enzymatic shortcut |
| β-1,2    | Sucrose                 | Non-reducing (both anomeric centres locked) |
| α,α-1,1  | Trehalose               | Non-reducing, protects against desiccation |

**Reducing sugars** still have a free hemiacetal (unlocked anomeric
OH) and can open back to the aldehyde — so they reduce Fehling's
solution, Tollens' reagent, and give positive Benedict's test.
Sucrose and trehalose are **non-reducing** because both anomeric
centres are engaged in the glycosidic bond.

## Modified sugars you'll recognise

The Carbohydrates tab ships examples of several **chemically
modified sugars** that show up in biology and medicine:

- **Aminosugars** — D-glucosamine (OH at C2 → NH₂) and its
  *N*-acetyl derivative GlcNAc. Backbone of chitin (arthropod
  exoskeleton) and bacterial peptidoglycan.
- **Uronic acids** — C6 OH oxidised to carboxylic acid
  (glucuronic acid). Phase-II liver metabolism glucuronidates
  drugs for excretion.
- **Deoxy sugars** — L-fucose and L-rhamnose (6-deoxy) appear on
  blood-group antigens and in plant glycosides.
- **Sugar alcohols** — sorbitol / mannitol / xylitol are reduced
  aldoses / ketoses. Non-cariogenic sweeteners.

## How this connects to the rest of the app

- **Glossary** — *Anomeric effect*, *Glycosidic bond*, *Mutarotation*
  are searchable from the Glossary tab.
- **Retrosynthesis** — the *Tools → Retrosynthesis…* dialog can
  disconnect glycosidic bonds via the Williamson-ether template
  (α / β stereospecificity is handled by the template SMARTS).
- **Chromatography** — *Tools → Lab techniques → TLC Rf
  simulator* lets you compare Rf of glucose vs sucrose in
  EtOAc / iPrOH / H₂O — instructive because sugars tail badly on
  silica and you usually switch to reverse-phase.

## Practice

Open the Carbohydrates tab and compare:

1. α-D-glucopyranose vs β-D-glucopyranose — spot the
   axial / equatorial difference at C1.
2. Glucose vs galactose — single stereocentre flip at C4.
3. Amylose (α-1,4) vs cellulose (β-1,4) — same monomer, different
   anomeric configuration, completely different biology.

Then try *Copy SMILES* on sucrose, paste into the *Tools →
Spectroscopy* IR dialog, and confirm the broad 3400 cm⁻¹ O–H
stretch + 1050 cm⁻¹ C–O region that identifies polyols.
