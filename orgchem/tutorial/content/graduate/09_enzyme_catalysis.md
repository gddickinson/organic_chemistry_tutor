# Enzyme catalysis essentials

Enzymes are nature's catalysts: typically **10⁸ to 10²⁰ × faster
than the uncatalysed background reaction**, with rate enhancements
that classical synthetic chemistry can't approach.  Orotidine 5'-
phosphate decarboxylase is the current record-holder at ~ 10¹⁷ ×
acceleration — meaning the half-life of OMP without the enzyme is
~ 78 million years; with it, ~ 18 milliseconds.

The **how** behind these accelerations comes down to one idea
(Linus Pauling, 1948): **enzymes bind the transition state more
tightly than they bind the substrate**.  Everything else —
covalent catalysis, acid-base, metal-ion participation, electrostatic
preorganisation, induced fit — is a means of achieving that
preferential binding.

## Michaelis-Menten kinetics

The canonical kinetic model (Michaelis & Menten 1913, formalised
by Briggs-Haldane 1925) treats enzyme + substrate binding as a
fast equilibrium followed by slow turnover:

```
E + S  ⇌(K_M)  ES  →(k_cat)  E + P
```

Three numbers tell you almost everything about an enzyme:

- **K_M** (Michaelis constant) — the substrate concentration at
  which v = V_max / 2.  Approximates K_d (substrate affinity)
  when k_cat ≪ k_off.  Range: 10⁻⁷ to 10⁻¹ M for biological
  substrates.
- **k_cat** (turnover number) — how many substrate molecules one
  enzyme molecule processes per second at saturation (V_max =
  k_cat × [E]_total).  Range: 10⁰ to 10⁶ s⁻¹.  Carbonic
  anhydrase wins at ~ 10⁶ s⁻¹.
- **k_cat / K_M** (catalytic efficiency, "specificity constant")
  — the second-order rate constant for E + S → E + P at low
  [S].  The diffusion limit (~ 10⁹ M⁻¹ s⁻¹) is reached by
  enzymes called **catalytically perfect**: catalase, fumarase,
  triose phosphate isomerase, acetylcholinesterase.  They've
  evolved as far as physics allows.

Plot v vs [S] on a Michaelis-Menten saturation curve; on a
Lineweaver-Burk double-reciprocal plot (1/v vs 1/[S]) inhibitors
diagnose as competitive (intercept on 1/v unchanged), uncompetitive
(parallel lines), or non-competitive (intercept on 1/[S]
unchanged).

## The 7 EC enzyme classes

The **Enzyme Commission** classification gives every enzyme a
4-number EC code by reaction class:

1. **Oxidoreductases** (EC 1) — redox.  Includes dehydrogenases,
   oxidases, reductases.  Workhorses of central metabolism (LDH,
   ADH, GAPDH).
2. **Transferases** (EC 2) — group transfer.  Kinases (P
   transfer), aminotransferases, methyltransferases.  PKA + Src
   here.
3. **Hydrolases** (EC 3) — hydrolytic cleavage.  Proteases
   (chymotrypsin, HIV protease), lipases, glycosidases,
   phosphatases.
4. **Lyases** (EC 4) — non-hydrolytic, non-redox bond cleavage.
   Aldolases, dehydratases, decarboxylases.
5. **Isomerases** (EC 5) — intramolecular rearrangement.
   Triose-phosphate isomerase, mutases, racemases.
6. **Ligases** (EC 6) — bond formation coupled to ATP hydrolysis.
   Aminoacyl-tRNA synthetases, DNA ligase, carbamoyl-phosphate
   synthetase.
7. **Translocases** (EC 7, added 2018) — energy-driven movement
   of ions / molecules across a membrane.  ATP synthase, Na⁺/K⁺
   ATPase, P-type pumps.

## How enzymes achieve transition-state binding

Five recurring catalytic strategies (Jencks 1969):

- **Covalent catalysis** — temporary covalent bond between
  enzyme + substrate.  The serine-protease catalytic triad
  (Ser → His → Asp) forms an acyl-enzyme intermediate; the
  Schiff-base aldolase forms a covalent imine with DHAP.
  See the seeded **Chymotrypsin** + **Class-I aldolase**
  mechanisms in the *Reactions* tab for step-by-step
  walk-throughs.
- **Acid-base catalysis** — His residues (pKa ~ 6) +
  carboxylate side chains shuttle protons.  HIV protease
  uses two Asp residues to activate water as a nucleophile
  for amide hydrolysis (see the seeded **HIV protease**
  mechanism).
- **Metal-ion catalysis** — Mg²⁺, Zn²⁺, Mn²⁺ stabilise
  charges + activate water.  Carbonic anhydrase's Zn²⁺
  drops the pKa of bound water from ~ 16 to ~ 7.  Many
  ATP-dependent enzymes need Mg²⁺ to coordinate the
  triphosphate.
- **Electrostatic catalysis** — preformed charge complementarity
  to the transition state.  RNase A uses two His residues +
  one Lys to stabilise the pentacoordinate phosphate
  transition state of phosphodiester hydrolysis (see the
  seeded **RNase A** mechanism).
- **Proximity + orientation** — enzymes bring two substrates
  together at high effective concentration in a productive
  geometry.  Estimated to contribute up to ~ 10⁵ of the
  rate enhancement on its own.

## Induced fit vs lock-and-key

**Emil Fischer (1894)** proposed substrates fit enzymes like a
**lock-and-key** — rigid complementary shapes.  This works for
many small molecules (e.g. lysozyme + N-acetylmuramic acid).

**Daniel Koshland (1958)** observed that many enzymes change
shape on substrate binding — **induced fit**.  Hexokinase
clamps shut around glucose to exclude water (preventing
hydrolysis of the high-energy phosphate it's about to transfer).
Glucokinase + DNA polymerases + protein kinases all use induced
fit for substrate selectivity.

The modern view: induced fit + conformational selection coexist —
enzymes pre-exist in multiple conformations + substrate binding
selects + further sculpts the catalytically-active one.

## Allosteric regulation

Many enzymes have **allosteric sites** distinct from the active
site where regulators bind + change activity by altering
conformation.  Two classical models:

- **MWC** (Monod-Wyman-Changeux 1965) — the enzyme exists in
  two states (T = tense, low-activity; R = relaxed, high-
  activity); regulators shift the equilibrium between them.
  Predicts cooperative ("sigmoidal") substrate-saturation curves.
- **KNF** (Koshland-Némethy-Filmer 1966) — sequential induced-fit
  changes propagate around a multi-subunit enzyme.

Aspartate transcarbamoylase (ATCase) is the classical MWC
example; haemoglobin (technically a transport protein, not an
enzyme) is the most-studied cooperative system.

## Drug design via transition-state mimics

Pauling's principle gives medicinal chemistry a powerful
strategy: **molecules that resemble the enzyme's transition
state are tightly-binding inhibitors**.  Famous examples:

- **HIV protease inhibitors** (saquinavir, ritonavir,
  indinavir, lopinavir, …) all contain a **non-cleavable
  amide-bond mimic** — typically a hydroxyethylene or
  hydroxymethylene group — that fills the protease active
  site like a tetrahedral transition state but doesn't break.
- **ACE inhibitors** for hypertension (captopril, enalapril)
  mimic the tetrahedral phosphonate transition state of
  angiotensin-converting enzyme.
- **Statins** (atorvastatin, simvastatin) bind HMG-CoA
  reductase ~ 10⁴ × tighter than the natural substrate by
  presenting a stable mimic of the mevaldyl-CoA intermediate.

The Phase-31k SAR series in the *Tools → Medicinal chemistry*
dialog has all three drug classes.

## How enzyme catalysis connects to the rest of organic chemistry

Enzymes use the same arrows + the same nucleophiles +
electrophiles you've seen across the curriculum — Ser-OH is just
a nucleophile, His is just an acid/base, Mg²⁺ is just a Lewis
acid.  What enzymes add is **active-site preorganisation**:
holding all the catalytic residues in exactly the right
positions to lower the transition-state energy by ~ 30 kJ/mol
relative to solution chemistry.  The same active-site ideas
drive the design of **artificial enzymes** + **organocatalysts**
(MacMillan + List + Jacobsen) where small chiral molecules try
to mimic enzyme active-site features in a single ~ 500 Da
catalyst.

## Try it in the app

- **Reactions tab** → search for *chymotrypsin*, *aldolase*,
  *HIV protease*, *RNase A* — all four seeded enzyme
  mechanisms have step-by-step curly-arrow renderings.
- **Glossary tab** → search for *enzyme*, *catalysis*,
  *catalytic triad*, *Schiff base*, *kinetic isotope effect*
  to see how the concepts cross-link.
- **Tools → Medicinal chemistry** → Bioisosteres tab + SAR
  tab to explore how transition-state mimicry drives
  medicinal-chemistry design.
- **Tools → pH explorer** → use the buffer designer to
  explore why most enzymes work best near pH 7 — their His
  pKa sits there.

## Further reading

- Fersht, A. *Structure and Mechanism in Protein Science*
  (3rd ed., 1999) — the comprehensive enzyme-mechanism
  textbook.
- Wolfenden, R.; Snider, M. J. (2001) "The depth of chemical
  time and the power of enzymes as catalysts" *Acc. Chem.
  Res.* **34**, 938.  The OMP decarboxylase / 10¹⁷ × paper.
- Schramm, V. L. (2011) "Enzymatic transition states,
  transition-state analogs, drug design + mechanism" *Annu.
  Rev. Biochem.* **80**, 703.  The transition-state-mimic
  drug-design retrospective.

Next: the **Biosynthesis & natural products** lesson (graduate/
06) extends enzyme catalysis into pathway-scale logic; the
**Macromolecules window** lets you inspect the structures of the
enzymes whose mechanisms you've been reading.
