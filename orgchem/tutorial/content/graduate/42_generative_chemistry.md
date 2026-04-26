# Generative chemistry models — ChemBERTa, MolFormer, diffusion

The cheminformatics + retrosynthesis lessons covered
discriminative ML (predicting properties or routes).
**Generative models** instead create new molecules — useful
for de novo drug design, material discovery, exploring
chemical space.

## Three generative paradigms

### 1. Sequence models (SMILES generation)

Treat a SMILES string as a sequence of tokens; train a
language model to predict the next token. Sample new
SMILES.

| Model | Training data | Use |
|-------|---------------|-----|
| ChemBERTa (Chithrananda 2020) | 77 M PubChem | property prediction (BERT-style) |
| MolFormer (IBM 2022) | 1.1 B PubChem + ZINC | property prediction + few-shot |
| MolFormer-XL (IBM 2024) | larger | better generalisation |
| RNN + RL (REINVENT 2.0) | curated targets | de novo design with reward |
| MolGPT (Bagal 2022) | 1 M | conditional SMILES generation |

### 2. Variational autoencoders (VAE)

Encode molecules into a continuous latent space; decode
back to molecules. The latent space allows interpolation
+ optimisation.

- **CharVAE** (Gomez-Bombarelli 2018) — early SMILES VAE.
- **JT-VAE** (junction tree VAE) — operates on graph
  fragments; better validity.
- **HierVAE** (Jin 2020) — hierarchical fragments + scaffolds.

### 3. Diffusion + score-based

Diffuse pure noise → iteratively denoise to a molecule.
Modern (post-2022) state-of-the-art:

- **EDM** (E(3)-equivariant diffusion model) —
  generates 3D molecules.
- **GeoLDM** (geometric LDM) — latent diffusion for 3D
  small-molecule design.
- **DiffSBDD** (Schneuing 2023) — diffusion for structure-
  based drug design (target's pocket → bound ligand).
- **MolDiff** — joint molecule + atom-position diffusion.

### 4. Graph generative models

Operate directly on molecular graphs:

- **GraphAF, GraphDF** — autoregressive graph generation.
- **MoFlow** — normalising flow on molecules.
- **Grids on graphs** — newer architectures.

## Conditional generation

The interesting + useful problem: generate molecules
**satisfying constraints**:

- **Property targets**: logP < 5, MW < 500, QED > 0.7,
  TPSA < 140 → drug-likeness.
- **Activity targets**: predicted activity > 8 against
  target X.
- **Synthetic accessibility**: SA score < 4.
- **Pocket fit**: shape complementary to a specific
  protein pocket.

Conditioning techniques:

- **Reinforcement learning** (REINVENT, MolDQN) — reward
  the desired property.
- **Latent-space optimisation** — gradient descent in the
  VAE's latent space toward target property.
- **Diffusion guidance** — classifier-free guidance toward
  property (DiffSBDD).

## Famous results

- **Insilico Medicine** — generated INS018_055 (renal
  fibrosis drug); first AI-generated drug to reach
  Phase II trials in 2024.
- **Generate Biomedicines** — designed proteins;
  partnership with Amgen + Novartis.
- **Cradle / Latent / Recursion / Genesis Therapeutics**
  — generative models for drug design pipeline.
- **DiffSBDD** + **PocketGen** — design against COVID
  protease + KRAS pocket; experimentally validated
  binders.

## Validity + novelty + uniqueness

When evaluating a generative model:

| Metric | What it measures |
|--------|------------------|
| **Validity** | % of outputs that are valid SMILES (no syntax errors) |
| **Uniqueness** | % of unique molecules among generated set |
| **Novelty** | % NOT in training set |
| **Diversity** | Tanimoto distance distribution |
| **Drug-likeness** | QED, Lipinski violations |
| **Synthetic accessibility** | SA score |
| **Property hit rate** | % of generated molecules meeting property targets |

A good model achieves > 95 % validity, > 95 % unique,
> 90 % novel, with high property hit rate.

## Open challenges

- **Training data bias** — most models trained on PubChem
  / ZINC; novel scaffolds (natural products, macrocycles)
  underrepresented.
- **Stereochemistry** — handling cis/trans + R/S in
  SMILES generation.
- **Synthesisability** — many "clever" generated molecules
  can't actually be made.
- **In vivo validity** — predicted-active molecules often
  fail in animal models.

## Hybrid + conformal generation

Modern frontier:

- **Generate + retrosynthesis check** — only keep
  generated molecules whose route AiZynthFinder can find.
- **Generate + ADME prediction filter** — pre-rank for
  PK before synthesis.
- **Generate in protein-pocket context** (DiffSBDD) —
  geometry-aware design.

## Try it in the app

- **Tools → Drawing tool…** → manually design + check
  drug-likeness.
- **Tools → Drug-likeness…** → run Lipinski + Veber +
  PAINS on a candidate.
- **Tools → Retrosynthesis…** → check if a generated
  molecule has a tractable route.
- **Glossary** → search *Generative model*, *VAE*,
  *Diffusion model*, *DiffSBDD*, *MolFormer*, *REINVENT*.

Next: **Crystal structure prediction**.
