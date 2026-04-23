# Asymmetric Synthesis: Making One Hand at a Time

A chiral molecule made without chiral induction is **racemic** — a
50:50 mixture of enantiomers. That's fine for the bench in a teaching
lab. It is **not** fine for a drug, a flavour, or a fragrance: biology
is chiral and usually cares which enantiomer you deliver. Thalidomide,
propranolol, ibuprofen, and dozens of others showed the hard way that
"sell the racemate" isn't safe as a default.

The field that solves this — **asymmetric synthesis** — has three
Nobel Prizes behind it (Sharpless/Knowles/Noyori 2001, List/MacMillan
2021), an industrial footprint exceeding $30 B/year, and a graduate-
level vocabulary students need to command fluently. This lesson lays
out the canon.

## The metric: enantiomeric excess (ee)

If a reaction produces R in excess of S (or vice versa), the **ee** is:

    ee (%) = |R − S| / (R + S)  ×  100

- 0 %  — racemic.
- 50 %  — 75:25 (dominant:minor).
- 90 %  — 95:5.
- 99 %  — 99.5:0.5. The bar for a publishable "asymmetric" method.
- 99.9 % — the bar for a drug intermediate today.

An equivalent measure is **er** (enantiomeric ratio), reported as
"95:5" or "99.5:0.5". Journals use either; know both.

Call `assign_stereodescriptors(smiles=…)` in the app to confirm which
enantiomer you have. `enantiomer_of(…)` computes the other. Together
they're enough to walk through every example below.

## The three strategic approaches

Every asymmetric method falls into one of:

1. **Chiral substrate / auxiliary**. The substrate itself is already
   chiral (from the chiral pool: amino acids, sugars, terpenes) or
   has a removable chiral auxiliary attached. The new stereocentre
   forms diastereoselectively. Example: **Evans' oxazolidinones**.
2. **Chiral reagent**. A stoichiometric chiral source. Example: **CBS
   reduction** uses a chiral oxazaborolidine + BH₃; 1 eq of chiral
   material per stereocentre formed.
3. **Chiral catalyst**. A substoichiometric chiral source that cycles
   through many substrates. Atom-economic and cost-efficient;
   the methodology is **dominant** in modern synthesis. Examples:
   **Sharpless**, **Noyori**, **List-MacMillan**, **Grubbs**.

Category 3 is the Nobel field and the bulk of this lesson.

## Transition-metal asymmetric catalysis

### Knowles hydrogenation (1968; Nobel 2001)

The trigger for the whole field. Knowles at Monsanto took Wilkinson's
Rh catalyst, swapped triphenylphosphine for a **chiral phosphine**
(DIPAMP), and hydrogenated a dehydro-amino-acid precursor of **L-DOPA**
at industrial scale in >95 % ee. First-ever kg-scale asymmetric
synthesis.

### Noyori asymmetric hydrogenation (1980; Nobel 2001)

**Ru-BINAP** reduces prochiral β-ketoesters → chiral β-hydroxyesters.
99 % ee on most substrates. The BINAP ligand (1,1'-binaphthyl-2,2'-
diyl-bis-diphenylphosphine) is **atropisomeric** — the axial chirality
of the binaphthyl framework transmits to the metal's coordination
geometry.

BINAP is the single most-cited chiral ligand in the literature. (R)-
and (S)-BINAP deliver opposite enantiomers of product; both are
commercial.

### Sharpless asymmetric epoxidation (1980; Nobel 2001)

    Allylic alcohol + Ti(OiPr)₄ + (+)-DET + t-BuOOH  →  2,3-epoxy alcohol

The mnemonic: "(+)-DET delivers O to the *bottom* face when the
allylic alcohol is drawn as a hockey stick with the OH in the lower-
right corner." Works on most allylic alcohols with 90–95 % ee. Set
the tone for "chiral metal + chiral additive + prochiral substrate" as
a universal formula.

### Sharpless asymmetric dihydroxylation (AD) — 1988; Nobel 2001

    Alkene + OsO₄ (cat.) + K₃Fe(CN)₆ / K₂CO₃ / (DHQD)₂-PHAL  →  syn-diol

**AD-mix-α** and **AD-mix-β** (pre-formulated reagents containing the
chiral ligand) cover most alkenes. Can hit 99 % ee on styrenes.

### Jacobsen epoxidation (1990)

Mn(salen) complex + oxidant → epoxide from **non-allylic** alkenes.
Fills the gap that Sharpless AE couldn't reach.

### Jacobsen HKR (hydrolytic kinetic resolution, 1997)

Racemic epoxide + H₂O + chiral Co(salen) → fast reaction on one
enantiomer → recovered epoxide in high ee. A clever use of **kinetic
resolution** — the catalyst doesn't set the centre, it just discards
the wrong hand.

### Grubbs / Schrock metathesis (1990s; Nobel 2005)

Asymmetric Mo / Ru carbene catalysts construct alkenes with high ee
(when a ring is being closed and the two alkene substituents differ).
Foundation of modern ring-closing metathesis in complex synthesis.

## Organocatalysis

A chiral catalyst that is **not** a metal complex — usually a small
organic molecule that activates the substrate via an iminium, enamine,
or H-bonding interaction.

### List's proline aldol (2000) & MacMillan's imidazolidinone (2000)

Simultaneously introduced by Benjamin List (Max Planck) and David
MacMillan (Princeton) — Nobel 2021. The breakthrough: **L-proline**,
a $1/g amino acid, catalyses asymmetric intermolecular aldol reactions
at 20-30 mol % loading with ≥ 90 % ee. MacMillan's **imidazolidinone**
catalysts do the same via iminium activation for Diels-Alder, 1,4-
addition, α-functionalisation.

The 15-year explosion of "organocatalysis" methodology papers in the
2000s-2010s derives from these two seminal 2000 reports.

### Jacobsen thiourea catalysis (2000s)

Chiral bis-thioureas that template H-bonding to prochiral electrophiles.
Particularly effective for Strecker amino-acid synthesis (aldehyde +
HCN + chiral thiourea + amine → chiral α-amino-nitrile → amino acid).

### MacMillan SOMO catalysis (2007)

One-electron oxidation of an enamine to a radical cation that couples
with electron-rich arenes or alkenes. Unlocks transformations that
classical two-electron mechanisms can't do.

## Chiral-pool / auxiliary methods

### Evans' oxazolidinone aldol (1981)

Attach a chiral oxazolidinone (from valine, norephedrine, or
phenylalanine) to a carboxylic acid → enolise → attack aldehyde →
cleave the auxiliary. Predictable syn-selectivity. Delivered into
natural-product synthesis like no method before; still taught as the
gold-standard way to do a stereoselective aldol by hand.

### CBS reduction (Corey-Bakshi-Shibata, 1987)

Chiral oxazaborolidine catalyst + BH₃. Prochiral ketone → chiral
alcohol, 95-99 % ee, substrate-general. The go-to method when
Noyori hydrogenation is inconvenient.

## Chiral drugs and why the economics favour single enantiomers

Until ~1990 most chiral drugs were sold as racemates. FDA guidance
since then asks sponsors to **justify** marketing a racemate if the
enantiomers can be separated cheaply. The reasons:

- **Thalidomide** (1957) — R-sedative, S-teratogen. Racemic sale
  caused ~10 000 birth defects in Europe. A cautionary tale even
  though thalidomide itself **racemises in vivo**.
- **Propranolol** — only the S-(-) enantiomer is the β-blocker; the
  R-(+) is inactive. Sold racemic for 40 years.
- **Ibuprofen** — only the S enantiomer is the COX inhibitor. The R
  enantiomer is slowly converted to S in vivo (~60 %), so the racemate
  still works clinically — but pure S (dexibuprofen) has faster onset.
- **Esomeprazole** — the S enantiomer of omeprazole (proton-pump
  inhibitor). AstraZeneca's "chiral switch": sold the single-enantiomer
  version when the racemic patent expired, extending effective patent
  life.

Half of new small-molecule drugs are single enantiomers today. For a
pharma chemist, asymmetric methodology is not optional — it's the
daily job.

## Seeding priorities for this project

From the above, the highest-ROI reactions to seed next (Phase 6b):

1. **Noyori Ru-BINAP hydrogenation** — a single representative step.
2. **Sharpless epoxidation** of geraniol or allyl alcohol.
3. **List proline aldol** — acetone + benzaldehyde; L-proline
   catalyst.
4. **MacMillan imidazolidinone Diels-Alder** — classic 2000 JACS
   paper.
5. **Evans oxazolidinone aldol** — 1-step with the (S)-Bn auxiliary.

Each would be a seeded reaction with an energy profile + mechanism and
a paragraph of context. Content-expansion queue updated in
`ROADMAP.md`.

## Practice

1. Load **L-Alanine** and **L-Phenylalanine** in the Molecule Workspace.
   Compute `enantiomer_of` on each — you get D-Alanine and
   D-Phenylalanine, the naturally-rare forms. Ask: *why* do ribosomes
   only use L?
2. The Compare tab lets you drop **Ibuprofen** (racemic seeded SMILES)
   next to **its enantiomer** (flip with `enantiomer_of`). Compare
   descriptors — identical except for 3D stereo indicators.
3. Ask the tutor: "What is ee? Compute the ee of a 95:5 mixture."
4. Read the **Glossary** entries for **Stereocentre**, **Enantiomer**,
   **Diastereomer**, **Meso compound**.

## Further reading

- Noyori, R. *Asymmetric Catalysis in Organic Synthesis* (1994).
- Ojima, I. (ed.) *Catalytic Asymmetric Synthesis* (3rd ed., 2010).
- List, B. & MacMillan, D. W. C. (2022) Nobel lectures, *Angew. Chem.
  Int. Ed.* 61, e202112086, e202113088.
- Jacobsen, E. N., Pfaltz, A., Yamamoto, H. (eds.) *Comprehensive
  Asymmetric Catalysis* (1999, 3 vols). The definitive reference.

Next (graduate tier): **Molecular-orbital theory & reactivity** —
builds on the Hückel backend and ties FMO theory to the periselective
stories seen in pericyclic and cross-coupling lessons.
