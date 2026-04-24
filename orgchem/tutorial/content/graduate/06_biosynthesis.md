# Biosynthesis & Natural Products

A human liver cell runs ~10 000 enzymes and turns glucose into
pyruvate (glycolysis) in ten steps, pumping out ATP along the
way.  In the same room, a *Streptomyces* bacterium assembles a
30-carbon macrolide antibiotic from a pool of acetyl-CoA and
malonyl-CoA using a modular polyketide synthase — and it does
the whole job in minutes, at room temperature, in water, with
near-perfect stereocontrol.

Nature is the ultimate organic chemist.  This lesson maps the
biological strategies onto the chemical equivalents we've been
building up over the seeded catalogue — so when you read a
paper that mentions AADC, thermolysin, PKS, or shikimate you
recognise the chemistry, not just the name.

## Biosynthesis as catalysis, four at once

Every cell runs the **five catalysis families** from graduate/05
in parallel.  A single metabolic reaction can layer several at
once; that's how enzymes get to rate accelerations of 10¹⁰ –
10¹⁷.

| Family (graduate/05) | Enzyme example | Seeded mechanism |
|----------------------|----------------|------------------|
| **Nucleophilic catalysis** | chymotrypsin Ser-195 hydroxyl | *Chymotrypsin: peptide bond hydrolysis* |
| **Covalent intermediate** | class-I aldolase Lys-Schiff base | *Aldolase class I: DHAP + G3P → F1,6BP* |
| **Acid-base catalysis** | HIV protease paired Asp₂ | *HIV protease: peptide bond hydrolysis* |
| **General acid + base** | RNase A paired His₁₂ / His₁₁₉ | *RNase A: phosphoryl transfer on RNA* |
| **Cofactor (PLP electron sink)** | AADC decarboxylation of L-DOPA | (mechanism described in the *Dopamine* pathway step 1) |

All four seeded enzyme mechanisms are viewable via *Reactions
tab → Open mechanism…*.  They're the canonical illustrations
of what enzymes do that chemists routinely can't.

## Primary vs secondary metabolism

**Primary metabolism** is the universal toolkit — glycolysis,
TCA cycle, fatty-acid synthesis, amino-acid biosynthesis.
Every cell runs most of this; it's the house-keeping.

**Secondary metabolism** is what makes each organism
*interesting* to chemists: alkaloids, terpenoids, polyketides,
non-ribosomal peptides, shikimate-derived aromatics.  These
are the *natural products* that decorate half the drugs on
the WHO Essential Medicines List and the other half of the
pharmacology textbook.

The same starting materials feed both: acetyl-CoA (C2), PEP +
erythrose-4-P (shikimate pathway), glucose-6-P (carbohydrate
branch).  Secondary metabolism just runs longer, weirder
enzymatic cascades on those starting blocks.

## Four superfamilies to know

### 1. Shikimate pathway — aromatic rings from sugars

Seven enzymatic steps turn PEP + erythrose-4-phosphate into
**chorismate** — the branch-point metabolite that feeds into
phenylalanine, tyrosine, tryptophan, and the precursors for
most plant polyphenols.

Chemist cross-reference: Draths-Frost's biosynthetic route to
adipic acid (green chemistry round 87 case 1) exits the
shikimate pathway at *cis,cis*-muconic acid.  That's the
plant-derived alternative to DuPont's N₂O-heavy KA-oil
process.  Same target; chemistry vs biology.

### 2. Polyketides — iterative Claisen condensations

Acetyl-CoA + (n−1) × malonyl-CoA → a C-2n β-ketoacyl chain.
The PKS machine is the seeded *Claisen condensation* mechanism
(Reactions tab) running in a loop, with optional ketoreductase
/ dehydratase / enoyl-reductase modules at each cycle to
elaborate the β-carbon.

Products:
- **Type I (modular)** — erythromycin, rapamycin, lovastatin.
  One multi-module enzyme per cycle, like an assembly line.
- **Type II (iterative)** — aromatic polyketides like
  tetracyclines, doxorubicin.  One small module used over
  and over.
- **Type III (chalcone synthase)** — single-enzyme, makes
  flavonoids, stilbenes, polyphenols.

Fatty-acid synthase (FAS) is mechanistically identical to
type-I PKS with all three reduction modules turned on every
cycle.  That's why fatty-acid biosynthesis is nicknamed
"fully reducing polyketide."

### 3. Terpenoids — isoprene units + prenyltransferases

Isoprene (C₅) units (isopentenyl-PP + dimethylallyl-PP,
from the MVA or MEP pathway) couple head-to-tail to give
C₁₀ (monoterpenes — menthol, limonene — Glossary cross-ref
{term:Regioselectivity}), C₁₅ (sesquiterpenes —
farnesene), C₂₀ (diterpenes — taxol core), C₃₀
(triterpenes — steroids via lanosterol), and C₄₀
(carotenoids).

Key enzyme class: **terpene cyclases**, which take a flexible
isoprenoid chain and flash it into a polycyclic skeleton
through a cascade of carbocation rearrangements — the same
arrow-pushing you meet in the *Pinacol rearrangement*
mechanism, but daisy-chained.  This is how a single enzyme
(oxidosqualene cyclase) turns a linear C₃₀ alkene into
lanosterol's four-ring steroid scaffold in one step.

Seeded cross-refs: every sterol in the Lipids panel
(cholesterol, testosterone, estradiol, cortisol, …) is a
terpene-cyclase product.

### 4. Alkaloids + amines — PLP decarboxylation

Pyridoxal-5'-phosphate (PLP) is the cofactor whose
**quinonoid intermediate** accepts the electron pair from a
decarboxylating amino acid, giving an achiral product.  You
already met the mechanism in the *Dopamine* pathway step 1:
L-DOPA → dopamine + CO₂, AADC-catalysed.

PLP also powers transaminations (Asp + α-KG ↔ OAA + Glu),
β-eliminations, and α,β-eliminations across amino-acid
scaffolds.  One cofactor, five reaction classes — a
pharmacist-level pattern match on the same
electron-sink principle.

Secondary-metabolite alkaloids (morphine, caffeine,
nicotine, cocaine, quinine, strychnine, …) mostly start
from a PLP-decarboxylated aromatic amino acid and elaborate
through iminium-ion cyclisations that again look exactly
like *Pinacol rearrangement* arrow-pushing.

## Industrial biosynthesis — when biology out-competes chemistry

Three seeded examples already show this in action:

| Product | Chemical route | Biosynthetic alternative |
|---------|----------------|--------------------------|
| **Aspartame** | Z-DCC coupling (round 80 pathway) | Thermolysin enzymatic coupling at Ajinomoto, 15 000 t/yr — no protection needed |
| **Adipic acid** | DuPont KA-oil + HNO₃ (N₂O pollution) | Draths-Frost *E. coli* shikimate pathway → *cis,cis*-muconic acid + H₂ |
| **Dopamine** | (not industrial) | AADC decarboxylation of L-DOPA at CNS site (pro-drug rationale) |

Several more in the pipeline (not seeded but worth knowing):
- **1,3-propanediol** (PDO, nylon precursor) — DuPont + Tate &
  Lyle fermentation from corn glucose.
- **Artemisinin** — Keasling's synthetic-biology *Saccharomyces*
  route to artemisinic acid; one plant-saving win of the 2010s.
- **Farnesene** (jet-fuel precursor / vitamin-E intermediate)
  — Amyris.
- **Insulin, growth hormone, monoclonal antibodies** — all
  recombinant; can't be made by chemistry at all.

## When chemistry beats biology

Biology is better at:
- Long enzymatic cascades at physiological conditions.
- Reactions with strict regio / stereo constraints on
  multi-substituted scaffolds.
- Any target where a well-known metabolite already exists
  (harvest it, don't synthesise it).

Chemistry is better at:
- Unnatural scaffolds enzymes don't have a template for
  (fluorinated drugs, biaryl cross-couplings).
- Single-step reactions at high concentration / high
  temperature / non-aqueous conditions.
- Any bond-formation the enzyme toolbox doesn't know
  (e.g. C-B bonds, Suzuki, Pd catalysis in general).
- Deep-seated scaffold modifications (skeletal
  rearrangements).

A modern process route often runs **chemoenzymatic**:
enzyme for the stereocentre, chemistry for the scaffold.
Sitagliptin (Merck / Codexis 2010) is the classic
chemoenzymatic success — an engineered transaminase
installs the amine stereocentre, rest of the route is
chemistry.

## Retrobiosynthesis — a useful design exercise

When you retro-analyse a natural product (review advanced/03
Retrosynthesis), ask at each disconnection:

1. Does this bond correspond to a **known enzyme class**?
   (acyltransferase, cyclase, reductase, oxidase, glycosyl-
   transferase, methyltransferase, halogenase, …)
2. Could an **iterative building block** (C2 acetyl for PKS,
   C5 isoprene for terpenes, C₂-C₃ glycine-equivalent for
   alkaloids) replace an ad-hoc disconnection?
3. Is this stereocentre **set by the backbone fold**
   (PKS ketoreductase stereochem, terpene-cyclase
   stereochem) rather than by a chiral auxiliary?

These are the questions a biosynthetic chemist like Floss
(stereochemistry), Cane (terpenes), or Walsh (enzyme
modification) trained their students to ask.

## Cofactor cheat-sheet

Every biosynthesis student eventually memorises which
cofactor does what.  Here's the short version:

| Cofactor | Role | Seeded relevance |
|----------|------|------------------|
| ATP / GTP | phosphoryl transfer, activation | RNase A phosphoryl transfer |
| NAD(P)H | hydride donor (reduction) | PKS ketoreductase module |
| FAD | 2-electron oxidation | flavoenzymes |
| Biotin | CO₂ carrier | fatty-acid synthase |
| Coenzyme A | activates acyl groups as thioesters | PKS, FAS |
| **PLP** | electron-sink for α-carbanion reactions | AADC / decarboxylations |
| Tetrahydrofolate | 1-C transfer (methyl) | nucleotide + aromatic-amino-acid biosynthesis |
| **SAM** | methyl-group donor | methyltransferases |
| Thiamin-PP | α-carbanion stabilisation | pyruvate dehydrogenase |
| Heme | O₂ binding / P450 hydroxylation | phenacetin → acetaminophen O-deethylation (seeded) |

The bolded rows are directly relevant to the seeded
pathways (L-DOPA → dopamine via PLP/AADC; SAM is the
archetypal methyl donor that would run the SAH → SAM
cycle on any methylation step in a natural-product
biosynthesis).

## Exercises

1. The *Caffeine from theobromine* pathway in the seeded
   Synthesis tab is a methylation step.  Which cofactor
   does the biological analogue use?
2. Which of the four biosynthetic superfamilies would you
   assign **ibuprofen** to?  (Trick question.)
3. The seeded Nylon-6,6 pathway uses HMDA from petroleum.
   Sketch a fictional biosynthetic route from glucose.
   Which superfamily would supply the C₆ diamine
   intermediate?
4. The *Aldolase class I* enzyme uses a **Schiff-base
   covalent intermediate** (seeded mechanism).  Which of
   the five catalysis families is this, and what's the
   non-enzymatic chemical equivalent?
5. Why is **recombinant insulin** the canonical example of
   a target that chemistry can't reach but biology can?

## See also

- Graduate / 05 Catalysis — five catalysis families framed
  without the biology context.
- Advanced / 05 Green chemistry — Draths-Frost biosynthetic
  adipic acid; PLA from lactide fermentation.
- Intermediate / 07 Sugars and carbohydrates — glucose as
  the carbon-feedstock root.
- Intermediate / 10 Protecting groups — thermolysin as the
  PG-avoidance flagship.
- Synthesis tab: L-DOPA → Dopamine; Aspartame thermolysin;
  Met-enkephalin Fmoc SPPS.
- Reactions tab: the four seeded enzyme mechanisms
  (chymotrypsin, class-I aldolase, HIV protease, RNase A).
- Glossary: {term:Catalytic triad}, {term:Schiff base},
  {term:Oxyanion hole}, {term:In-line phosphoryl transfer},
  {term:Covalent intermediate}, {term:Pharmacophore}.
