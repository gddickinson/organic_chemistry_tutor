# Cheminformatics + ML for chemistry

**Cheminformatics** is the application of computer methods
to chemical problems: encoding molecules, searching
databases, predicting properties. Machine learning has
swallowed a growing share of the field since AlphaFold's
2020 protein-structure breakthrough showed what neural nets
could do.

## Molecular representations

How do you give a molecule to a computer?

### SMILES + InChI strings

- **SMILES** — Daylight's 1988 line notation. Compact,
  human-readable, but multiple SMILES per molecule
  (canonicalisation needed).
- **Canonical SMILES** — RDKit / OpenBabel deterministic
  ordering algorithm.
- **InChI** — IUPAC's canonical 1990s string; layered (atoms,
  bonds, charges, isotopes, stereo). Designed for structure
  search, not human reading.
- **InChIKey** — 27-char hash of InChI. Identity hash
  used for DB cross-referencing.

### Fingerprints

Bit vectors (typically 1024-2048 bits) encoding substructure
presence / absence:

- **MACCS keys** — 166 hand-curated SMARTS substructures.
  Cheap + interpretable; weak for novel scaffolds.
- **ECFP / Morgan fingerprints** — circular topological
  fingerprints with adjustable radius (ECFP4, ECFP6).
  Modern workhorse for similarity search.
- **RDKit FP** — combination of Morgan + path-based.
- **Atom-pair, topological-torsion** — for diverse coverage.

**Tanimoto coefficient** measures similarity:
T = |A ∩ B| / |A ∪ B|. Classic threshold: 0.7 = "similar".

### Graph representations

A molecule IS a graph (atoms = nodes, bonds = edges). Modern
deep-learning approaches operate directly on molecular
graphs:

- **Graph Convolutional Networks (GCN)** — Kipf, Duvenaud.
- **Message Passing Neural Networks (MPNN)** — Gilmer et al.
- **Graph Attention Networks (GAT)** — Veličković.
- **Graph Transformers** — global self-attention over atoms.

### 3D representations

For physics-aware tasks (binding affinity, conformer
energies, IR spectra):

- **Cartesian coordinates** — straightforward but not
  invariant to rotation.
- **Internal coordinates** — bond lengths, angles, dihedrals.
- **Equivariant neural networks** — SchNet, PaiNN,
  TorchANI, MACE, AlphaFold's IPA — built-in rotational +
  translational equivariance.

## Property prediction

### Quantitative SAR (QSAR)

Linear regression / random forests / gradient boosting on
molecular descriptors → property:

- **Solubility** (Esol, Delaney 2004) — old + still useful
  as a baseline.
- **logP** (Crippen) — atom-contribution model;
  RDKit's `Descriptors.MolLogP`.
- **PAMPA / Caco-2 permeability** — ML on whole-molecule
  features; vendor offerings (Optibrium StarDrop, BIOVIA
  Pipeline Pilot).

### Deep-learning models

- **ChemBERTa, MoLFormer, MolFormer-XL** — transformer
  pre-trained on hundreds of millions of SMILES; fine-tune
  for property prediction.
- **DimeNet, GemNet, MACE** — 3D-aware architectures for
  energies + forces. Used as **ML potentials** in MD
  simulations.
- **AlphaFold-multimer / AlphaFold2 / 3** — fold prediction
  reframed as sequence → structure — the most influential
  ML-for-chemistry result so far.

## Generative models

Designing new molecules:

- **VAE-based** (Gomez-Bombarelli) — latent space → decode
  novel SMILES.
- **RNN-based** (REINVENT, MolDQN) — RL agents trained to
  output desirable molecules.
- **Diffusion models** (DiffSBDD, EDM, GeoLDM) — diffuse
  noise → denoised molecule, conditioned on protein
  pocket.
- **GFlowNets** (Bengio) — sample diverse high-reward
  molecules with proper Boltzmann weighting.

## Reaction prediction + retrosynthesis

- **Forward prediction** — given reactants → predict
  products. **Molecular Transformer** (IBM, Schwaller) +
  **RXNFP** (reaction fingerprints).
- **Retrosynthesis** — given target → predict precursors.
  **3N-MCTS** (Segler, Waller), **Aizynthfinder** (Genheden),
  **ASKCOS** (Coley) all integrate with route-planning.
- **Yield prediction** — Doyle's HTE datasets + transformer
  models predict reaction yield from conditions.

## Datasets you should know

- **PubChem** (~ 110 M compounds), **ChEMBL** (~ 2.4 M
  compounds with bioactivity), **DrugBank** (~ 14 K drugs).
- **ZINC22 / Enamine REAL** (~ 10⁹ make-on-demand
  compounds).
- **Reaxys / SciFinder** (commercial) — ~ 100 M reactions +
  yields.
- **USPTO** (open) — ~ 3 M reactions extracted from US
  patents 1976-2016. Workhorse for ML-reaction-prediction
  benchmarks.
- **CSD** — Cambridge Structural Database (~ 1.2 M small-
  molecule X-ray structures). Source of conformer
  templates.
- **PDB** (~ 220 K experimental + AlphaFold DB ~ 200 M
  predicted protein structures).

## Limits + critiques

- **Distribution shift** — ML models trained on commercial
  drugs fail on natural products + bRo5 macrocycles.
- **Single-task vs multi-task** — pre-training on broad
  property data (Tox21, ChEMBL) helps on few-shot tasks.
- **Reproducibility** — many cheminformatics ML papers
  don't release code or use unrealistic train/test splits
  (random vs scaffold split makes huge difference).
- **No mechanistic insight** — predicting yield ≠
  understanding why a reaction works.

## Try it in the app

- **Tools → Drug-likeness…** → see Lipinski / Veber / Ghose
  applied to any SMILES.
- **Tools → Retrosynthesis…** → template-based
  retrosynthetic search returns top-K disconnections.
- **Glossary** → search *SMILES*, *InChI*, *Tanimoto
  similarity*, *Morgan fingerprint*, *QSAR*, *AlphaFold*.

Next: **Drug discovery process — from target → IND**.
