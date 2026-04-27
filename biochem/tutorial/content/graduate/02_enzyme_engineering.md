# Enzyme engineering + directed evolution

The promise: design or evolve enzymes that catalyse
arbitrary chemistry with industrial-grade activity,
selectivity, and stability.  The reality (2026): three
paths converging — directed evolution, structure-based
design, and ML-driven design — each with mature wins.

## Directed evolution — Frances Arnold's approach

Frances Arnold won the **2018 Nobel Prize in Chemistry**
"for the directed evolution of enzymes" (sharing with
George Smith + Greg Winter for phage display).  The
core insight: don't try to design — evolve.

### The basic cycle

1. **Library construction** — random mutagenesis (error-
   prone PCR, mutator strains, DNA shuffling, site-
   saturation mutagenesis at chosen positions).
2. **Expression** — in *E. coli* / yeast / cell-free.
3. **Screening or selection** — measure activity per
   variant.  Selection is preferred (alive vs dead);
   screening (assay each variant) limits library size.
4. **Pick the best 1-10** — sequence, characterise.
5. **Iterate** — winners become parents for the next
   round.

### Library quality is everything

- **epPCR** (error-prone PCR) gives random mutations
  ~ 0.5-2 % per base — too many missense, mostly
  destabilising.
- **Site-saturation mutagenesis (NNK / NNS codons)** at
  chosen positions explores all 20 AAs at one residue.
- **DNA shuffling** (Stemmer 1994) recombines parental
  genes — bigger phenotypic jumps.
- **Iterative saturation (CASTing, ISM)** — Reetz's
  systematic active-site coverage.
- **Protein engineering by homologous recombination** —
  SCHEMA + RASPP (Pierce + Arnold) preserve fold
  integrity while shuffling.

### Iconic Arnold-lab examples

- **P450 BM3** evolved from fatty-acid hydroxylase to
  an enzyme that catalyses **carbene insertion into
  C-H bonds** + **N-H insertion** + **cyclopropanation
  of olefins** — chemistry that doesn't exist in
  natural enzymes.  The active site held compound I,
  but a few mutations let it stabilise an Fe-carbene
  / Fe-nitrene instead.
- **Subtilisin variants** with ~ 10⁵-fold solvent-
  resistance improvements for industrial detergents.
- **R-selective transaminases** for pharmaceutical chiral
  amine synthesis.

### Industrial directed-evolution successes

- **Codexis sitagliptin transaminase** — replaced a
  rhodium-catalysed asymmetric hydrogenation with a 27-
  mutation evolved enzyme; > 99.95 % ee, 13 % yield
  improvement, ~ 19 % cost reduction at multi-tonne
  scale.  Merck patent (2010) — paradigm-defining.
- **Codexis HMG-CoA reductase** for atorvastatin
  intermediate synthesis.
- **Solugen + Ginkgo Bioworks + Zymergen** —
  fermentation enzymes for diverse chemistries.
- **Novozymes** + **DSM** — detergent / food-processing /
  biofuel enzymes (subtilisins, amylases, cellulases,
  phytases, lipases).

## Rational + structure-based design

When you know the structure + mechanism, you can pick
mutations:

- **Stability engineering** — proline introduction at
  loop turns, disulfide engineering, computational
  ΔΔG predictions (Rosetta ddg_monomer, FoldX).
- **Selectivity flipping** — switch
  enantio/regio/chemoselectivity by reshaping the
  active-site pocket (Reetz's CAST methodology).
- **Substrate-binding-pocket reshaping** — extend
  substrate scope (e.g. ω-transaminases for bulky
  ketones).
- **De-novo enzyme design** —
  - **Inside-out** approach: design a quantum-mechanical
    "theozyme" of the TS + ideal residues, scaffold-
    search the PDB for compatible folds, optimise
    sequence with Rosetta.
  - **Baker lab** has published Kemp eliminase, Diels-
    Alderase, retro-aldolase, esterase, organophosphate
    hydrolase, luciferase — most then evolved further to
    boost kcat by 10²-10⁴.

## Machine-learning enters

ML is rapidly becoming the third pillar:

- **Mutation-effect prediction** (zero-shot) —
  - **ESM-2 / ESM3** language models score variant
    likelihoods (high-likelihood variants more often
    fold + function).
  - **EVE / DeepSequence** — alignment-based
    autoregressive variant scoring.
  - Used to filter directed-evolution libraries before
    wet-lab screening, dramatically improving hit rates.
- **Sequence-to-function regression** — train a small
  network on a directed-evolution screening dataset (~ 10²-
  10⁵ measured variants) → predict activity for unmeasured
  variants → recommend the next round's library.
  Wittmann + Arnold's MLDE (machine-learning-assisted
  directed evolution) showed 10× efficiency gains.
- **Structure-aware ML** — combine AlphaFold-predicted
  ΔΔG + ML-derived activity → **multi-objective
  optimisation** for activity + stability + solubility
  + selectivity.
- **Generative design** — protein language models +
  diffusion models (RFdiffusion, Chroma) generate novel
  protein backbones; ESM3 + ProteinMPNN design sequences
  to fit them.  The Baker lab has demonstrated
  experimentally validated de-novo binders + enzymes
  designed end-to-end with no homologous starting point.

## Cell-free + high-throughput screening tech

The bottleneck used to be screening; now it's library
quality:

- **Microfluidic droplet sorting (FADS, AADS)** —
  > 10⁵-10⁶ variants/day at single-cell resolution.
- **Continuous-evolution platforms** — PACE (phage-
  assisted continuous evolution, Liu lab) couples
  enzyme activity to phage propagation; runs > 10²-10⁴
  generations / week.
- **Cell-free expression** — accelerates DBT (design-
  build-test) cycles; PURE system for highest control.
- **Deep mutational scanning (DMS)** — measures fitness
  for every single point mutation; gold-standard for
  fitness landscape mapping.

## Engineering targets that have moved the field

- **Cytochromes P450** — non-natural carbene + nitrene
  chemistries (Arnold).
- **Transaminases** — sitagliptin (Codexis); now > 50
  industrial chiral amine processes.
- **Imine reductases (IREDs)** — chiral-amine synthesis
  via reductive amination.
- **Halogenases / fluorinases** — biocatalytic C-X bond
  formation; the natural fluorinase (FlA) catalyses the
  only known biological C-F bond.
- **Carbonic-anhydrase + cellulase variants** for
  industrial CO₂ capture + cellulosic-ethanol.
- **Plastic-degrading enzymes** — PETase / MHETase
  variants from *I. sakaiensis*; LCC-ICCG variant
  (Tournier 2020) achieves 90 % PET-bottle depolymerisation
  in 10 h at 72 °C — Carbios commercialising.
- **CRISPR-Cas variants** — base editors (Liu lab),
  prime editors, miniaturised Cas12f variants for AAV
  delivery — engineered via deep mutational scanning +
  rational design.

## Design + practical tips

- **Start from the closest natural enzyme** — even when
  using ML or design, evolutionary inheritance gives
  you a solubility + folding + expression head-start.
- **Engineer stability FIRST** — destabilising
  activity-improving mutations are common; consensus +
  computational stabilisation buys mutational headroom.
  "Buying stability to spend on activity" is a Rink +
  Arnold mantra.
- **Combinatorial + iterative** — single mutations
  rarely give industrial-grade gains; combinations
  (often 5-30) do.
- **Library quality > library size** — focus mutations
  at active-site / shell-1 residues + couple with
  ML-guided enrichment.
- **Wash + iterate fast** — DBT cycle compression beats
  individual-step optimisation.

## Open challenges

- Enzymes for **non-natural chemistry** still mostly
  hijack natural catalytic machinery (P450 → carbene,
  enoate-reductase → photoredox).  De-novo catalysis of
  arbitrary chemistries remains the holy grail.
- **Activity + multi-objective** trade-offs hard to
  navigate even with ML.
- Predicting **substrate scope** + **selectivity**
  reliably from structure is still elusive.
- Industrial deployment requires **stability under
  process conditions** — solvent, temperature, pH,
  shear — that lab evolution doesn't always capture.

## Try it in the app

- **OrgChem → Macromolecules → Proteins** — fetch
  P450 BM3 (PDB 1JPZ) + sitagliptin transaminase + LCC
  PETase variants for structural intuition.
- **Window → Biochem Studio → Enzymes** —
  `cytochrome-p450-bm3` + `transaminase` entries link
  the engineering literature.
- **Window → Pharmacology Studio → Drug development** —
  Codexis sitagliptin case study.

Next: **Metabolomics + flux analysis**.
