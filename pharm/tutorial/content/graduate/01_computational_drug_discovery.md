# Computational drug discovery

Computer-aided drug design (CADD) is now central to
every major pharma R&D programme.  The toolkit spans
docking, virtual screening, free-energy calculations,
QSAR / ML, generative chemistry, and structure
prediction.  The 2020s have seen ML transform several
sub-fields without fully replacing physics-based
methods.

## Layers of the CADD stack

From most-physical to most-empirical:

- **Quantum chemistry** — DFT / coupled-cluster on
  active-site clusters.  Mechanistic + reactive
  intermediate work.
- **Molecular dynamics + free-energy** (FEP+, TI,
  ABFE) — physics-based ranking of binding affinities
  with rigorous statistical mechanics.
- **Molecular docking** — geometric / scoring-function
  approach to predict ligand pose + relative
  affinity.
- **QSAR / ML scoring** — empirical models trained on
  experimental data.
- **Pharmacophore / similarity searches** — ligand-
  centric pattern matching.
- **Generative models** — propose novel molecules
  conditioned on properties.
- **Structure prediction** — AlphaFold / ESM /
  Boltz-1 fold proteins from sequence.

A modern CADD programme uses several layers in
combination, escalating from cheap-fast to
expensive-accurate as a small set of compounds is
selected from a large library.

## Structure-based drug design (SBDD)

Requires a 3D structure of the target — historically
from X-ray, NMR, cryo-EM; now also from AlphaFold +
ESM.

**Workflow**:
1. Solve / predict + validate the target structure.
2. Identify the binding site (orthosteric or
   allosteric) — pocket detection (FPocket,
   SiteMap, DoGSiteScorer).
3. Generate / acquire compound library.
4. Dock compounds into the site.
5. Score + rank.
6. Re-score top hits with more rigorous methods.
7. Synthesise + assay top candidates.
8. Iterate with co-crystal structures / cryo-EM of
   improving leads.

**Iconic SBDD success stories**:
- **HIV protease inhibitors** (saquinavir, indinavir,
  ritonavir, lopinavir, nelfinavir, atazanavir,
  darunavir) — driven by 1989 + later HIV protease
  crystal structures.
- **Imatinib** — ATP-pocket targeting based on Bcr-Abl
  + Src crystal structures.
- **Captopril** — first ACE inhibitor, designed from
  the carboxypeptidase A active-site model.
- **Zanamivir + oseltamivir** — neuraminidase
  inhibitors designed from sialic-acid-bound
  structures.
- **Dorzolamide** — carbonic-anhydrase inhibitor for
  glaucoma; rational design programme by Merck.
- **Venetoclax** — fragment-based BCL-2 inhibitor;
  driven by NMR + X-ray of BCL-2 / BCL-XL.
- **Sotorasib + adagrasib** — KRAS-G12C covalent
  inhibitors, driven by the cryptic switch-II pocket
  visible only in mutant structures.
- **Paxlovid (nirmatrelvir)** — covalent SARS-CoV-2
  Mpro inhibitor designed in months.

## Molecular docking

Geometric search for ligand poses in a binding site
+ scoring function for ranking.

**Major programs**:
- **AutoDock** + **AutoDock Vina** — academic
  open-source workhorses.  Lamarckian GA + empirical
  scoring.
- **Glide** (Schrödinger) — commercial; SP / XP /
  IFD modes.
- **GOLD** (CCDC) — genetic algorithm; long-standing
  validation.
- **DOCK** — UCSF; the original.
- **rDock** — open-source; pharmacophore-aware.
- **DiffDock** + **AutoDock Vina v1.2 + AutoDock
  Suite** — recent ML-augmented variants.

**Scoring functions**:
- **Empirical** (ChemPLP, ChemScore, X-Score) —
  polynomial sum of physical-interaction terms
  fitted to experimental K_d data.
- **Force-field-based** (DOCK Grid score, MM-PBSA /
  MM-GBSA) — explicit physics + implicit solvent.
- **Knowledge-based** (DrugScore, SMINA-scoring) —
  potentials derived from PDB co-crystal statistics.
- **ML scoring** (Vinardo, RF-Score, gnina, DiffDock
  scoring) — neural network or random forest trained
  on PDBbind-class datasets.

**Pose-prediction** correlation is decent (top pose
within 2 Å of crystal pose ~ 60-80 % of the time);
**affinity ranking** correlation with experimental
K_d / IC50 is poor (R² typically 0.2-0.4).  Docking
is best for hit-finding + qualitative ranking, NOT
for quantitative SAR.

## Virtual screening

Two flavours:

### Ligand-based (LBVS)

Train ML or pharmacophore models on KNOWN actives +
inactives.  No structure required.

- **Pharmacophore matching** (Catalyst, Phase) — match
  3D arrangements of features.
- **Similarity search** (Tanimoto on Morgan / ECFP4
  fingerprints) — fast + simple.
- **Random forest / gradient boosting** trained on
  ChEMBL data.
- **Graph neural networks** — DeepChem, Chemprop,
  Schnet, MEGNet, MACE.

### Structure-based (SBVS)

Dock a library against the target structure +
rank.  Library sizes:
- Vendor catalogues: ~ 10-100 M (ZINC, Enamine REAL).
- Make-on-demand virtual libraries: 10⁹-10¹⁰
  compounds (Enamine REAL Space, WuXi virtual,
  MolPort).
- Generative outputs: theoretically unbounded.

**Ultra-large-scale virtual screens** (UCSF Shoichet
group): screen 10⁸-10⁹ compounds against a
GPCR or kinase, hit rate ~ 1-5 % at confirmation.
Several discoveries published, > 10 % hit rates for
specific targets.

## Free-energy calculations

The gold standard for relative + absolute
binding-affinity prediction:

- **FEP+ (Schrödinger)** — Gold standard for ranking
  congeneric series (R-group + scaffold variations
  on the same core).  RMSE ~ 1 kcal/mol on validation
  sets; ~ 1.5 kcal/mol in real-world prospective use.
- **TI / λ-dynamics** — equivalent physics, older
  implementation.
- **ABFE (alchemical absolute binding free energy)** —
  unanchored; more demanding but answers "is this
  a binder at all?"
- **Replica-exchange + Hamiltonian REMD** — improved
  sampling.

Used by virtually every large-pharma + most
mid-cap-biotech med-chem teams since 2017-2020.
Schrödinger's FEP+ benchmark studies showed > 80 %
of compounds correctly classified as more / less
potent than reference; sufficient for
prospective design selection.

## QSAR + ML

Quantitative structure-activity relationship modelling
predicts an endpoint (potency, ADME, tox) from
chemical structure.

**Modern approaches**:
- **Random forests** + **XGBoost** on Morgan / RDKit
  / MACCS / Mordred descriptors.
- **Graph neural networks** treating the molecule as
  a graph (Chemprop, MoleculeNet, Schnet, MEGNet).
- **Transformer / language models** treating SMILES
  as text (ChemBERTa, MolFormer, MolT5).
- **Multi-task learning** — jointly predict potency +
  selectivity + ADME for shared embeddings.
- **Active learning** — iteratively choose the next
  experiments to maximise model improvement.

**Benchmarks**: MoleculeNet, Therapeutics Data
Commons (TDC), Polaris.  Published R² typically 0.6-
0.8 for activity prediction within a series; new
chemotype generalisation remains hard.

## Generative chemistry

Generate molecules de novo conditioned on properties:

- **VAE / RL approaches** (REINVENT, JT-VAE, MolGAN).
- **Transformer / language models** (MolGPT, ChemTS).
- **Diffusion models** (DiffDock, EquiBind for binding;
  GeoDiff, MolGen for property-conditioned).
- **Equivariant generative models** with 3D
  coordinates (E-NF, EDM, MolDiff).
- **Active-site-conditioned generation** (Pocket2Mol,
  ResGen, TargetDiff) — generate ligands fitting a
  given binding pocket.

Companies: Insilico Medicine (INS018_055 in clinic),
Recursion (REC-994 in clinic), BenevolentAI,
Atomwise, Cradle, Iktos, Charmed Labs.

## AlphaFold + structure prediction

**AlphaFold2** (2021) + **AlphaFold3** (2024)
revolutionised structural biology — near-experimental
accuracy from sequence alone for ~ 95 % of proteins.

Implications for drug discovery:
- Structures available for almost every druggable
  protein (~ 200 M in AlphaFold DB).
- New target classes opened (especially intrinsically
  disordered + previously-uncrystallisable).
- AlphaFold-driven SBDD: pocket prediction + virtual
  screening on AF models.
- Some open issues — AF models lack the ligand-bound
  conformation; allosteric pockets often missing;
  small movements (e.g. DFG-out vs DFG-in for
  kinases) sometimes wrong.

**ESMFold** (Meta, 2022) — comparable accuracy at
60× speed.

**Boltz-1** + **AlphaFold3** — predict
protein-ligand complexes directly from sequence +
SMILES.

## Cryptic + allosteric pockets

Many high-value targets (KRAS, SHP2, PI3Kα selectivity)
opened up only when CRYPTIC pockets — pockets visible
only in transient or mutant conformations — were
identified.

Methods:
- **Mixed-solvent MD** (MixMD, FTMap) — simulate
  protein with many small organic probes; cluster
  hot spots.
- **Markov state models (MSM)** — sample slow protein
  motions + identify rare open-pocket states.
- **DEEP DOCKING + ULTRA SCREENS** — sometimes
  uncover ligands that occupy cryptic pockets.

## ADME-tox prediction

Cheap, fast, increasingly accurate ML models cover
the typical med-chem screening cascade:
- **Solubility** (logS) — standard since the 1990s
  (ESOL, GSE, ML).
- **Permeability** — Caco-2, MDCK, PAMPA.
- **Lipophilicity** (logP, logD).
- **Metabolic stability** — microsomal half-life by
  species.
- **CYP inhibition** (3A4, 2D6, 2C9, 2C19, 1A2).
- **hERG inhibition** — cardiac safety gate.
- **Mutagenicity** (Ames, micronucleus).
- **PPB, RBP, blood-plasma ratio.**

ADMET Predictor + AdmetSAR + SwissADME + ChemDes +
DeepTox are widely used.

## Limitations + open challenges

- **Activity-cliff blind spots** — ML struggles when
  small structural changes produce large activity
  shifts.
- **Out-of-distribution** generalisation — performance
  degrades on novel chemotypes.
- **Affinity prediction** still only 1-2 kcal/mol
  RMSE at best (~ 5-30× in K_d).
- **Resistance / mutation effects** under-modelled.
- **Polypharmacology + selectivity panels** — multi-
  task ML is helping but far from solved.
- **Validation transparency** — many published
  benchmarks data-leak; rigorous time-split or
  cluster-split evaluation is rarer than it should
  be.

## How to integrate CADD into a programme

A typical workflow:
1. **Library design** — diverse subset for HTS or
   focused design for SBDD.
2. **Initial screen** — wet-lab HTS (10⁵-10⁷) +
   virtual screen (10⁸-10¹⁰) in parallel.
3. **Hit triage** — re-dock + re-score; ML ADMET
   filter.
4. **Hit confirmation** — biochemical + biophysical
   (SPR, MST, ITC).
5. **Structure-based optimisation** with co-crystal
   feedback.
6. **FEP+ ranking** of next-round designs.
7. **Synthesis + assay** of top 5-20 designs per cycle.
8. **Iterate** until clinical-candidate quality.

Modern ML-first companies (Insilico, Recursion) push
generative models earlier, sometimes skipping HTS
entirely.

## Try it in the app

- **OrgChem → Tools → Drug-likeness** — Lipinski +
  Veber + Ghose + PAINS + QED, Phase 19b
  drug-likeness panel.
- **OrgChem → Tools → Retrosynthesis** — mini-Aizynth
  (Phase 8d) for generated-molecule synthetic
  feasibility.
- **OrgChem → Tools → Bioisosteres** — round-30 SAR
  bioisostere catalogue.
- **OrgChem → Macromolecules → Proteins** — fetch
  PDBs + analyse pockets (Phase 24d) + binding
  contacts (Phase 24e).

Next: **Real-world evidence + RCTs**.
