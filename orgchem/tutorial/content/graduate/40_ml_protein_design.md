# ML for protein design — RFdiffusion + ProteinMPNN

After AlphaFold solved structure prediction (2020-2021),
the next ML revolution is **de novo protein design**:
asking "design a protein that does X" + getting a sequence
that folds to do exactly that. By 2025, Baker lab + others
have demonstrated dozens of working proteins designed this
way.

## The protein-design problem

For a desired function:

- **Binding**: design a protein that binds a specific
  small molecule, peptide, or another protein.
- **Catalysis**: design an enzyme that catalyses a
  specific reaction.
- **Structure**: design a fold that doesn't exist in
  nature (e.g. mini-protein with novel topology).
- **Switch**: design a protein that changes conformation
  in response to a ligand.

## Two-stage workflow

### Stage 1: backbone design (RFdiffusion)

```
inputs: desired functional motif (binding loop, active site geometry)
outputs: 3D backbone coordinates that include the motif
```

RFdiffusion (Watson + Baker, *Nature* 2023) is a diffusion
model trained on the PDB:

- Start from random noise (random Cα positions).
- Iteratively denoise toward a low-energy backbone with
  the desired motif.
- Output: 3D Cα + Cβ trace; no sequence yet.

Variants:

- **Hallucination** — start from constraints + iteratively
  refine.
- **Inpainting** — fill in missing parts of a partially
  specified structure.
- **Symmetric design** — generate a backbone with C₂, C₃,
  ... point-group symmetry.

### Stage 2: sequence design (ProteinMPNN)

```
inputs: backbone coordinates from RFdiffusion
outputs: amino-acid sequence that folds to that backbone
```

ProteinMPNN (Dauparas + Baker, *Science* 2022) is a graph
neural network trained on PDB:

- For each residue position, predict identity from
  backbone neighbours' geometry.
- Sequence is internally consistent (predicted to fold to
  the input backbone).
- 100-fold faster than physics-based methods (Rosetta).

### Validate

- AlphaFold2 / 3 predict folded structure of the designed
  sequence.
- Compare to target backbone.
- If RMSD < 1 Å, the design is "self-consistent".
- Then synthesise the gene + express in *E. coli* + test
  experimentally.

## Successes

By 2025:

- **Mini-protein binders** to dozens of disease targets:
  PD-L1, IL-23, SARS-CoV-2 spike, GPCRs, kinases.
- **Novel folds** — proteins with topologies absent from
  nature.
- **Dimers + tetramers** with exact geometry.
- **Protein-mimetic enzymes** — designed retro-aldolases,
  Kemp eliminases, Diels-Alderases (limited turnover but
  proof-of-concept).
- **Logic gates + switches** — designed proteins with
  conformational control.

## Major actors

- **Baker lab (Univ. Washington)** — RFdiffusion,
  ProteinMPNN, hallucination methods.
- **Generate Biomedicines** — design biologics for therapy.
- **Cradle / Latent / Profluent / Demis Cyclica** —
  startups in this space.
- **DeepMind Isomorphic Labs** — drug discovery via AI
  protein structure + design.
- **Insilico Medicine + Recursion** — drug + protein
  design.

## Application areas

### Therapeutics

- **De novo binders** — small (50-100 AA) proteins that
  bind specific targets; cheaper to manufacture than
  antibodies; oral availability potential.
- **Enzymes for chemistry** — designed retroaldolases for
  asymmetric synthesis.
- **Vaccines** — designed antigens (Baker lab COVID-19
  multivalent particle).

### Diagnostics

- Designed binders for biomarker detection.
- Protein-based logic circuits in synthetic biology.

### Materials

- Designed protein cages for drug delivery.
- Protein-based hydrogels with programmable mechanics.

## Limits

- **Functional design** is harder than binding —
  enzymes have low turnover (10-1000 vs 10⁶ for natural).
- **Stability** in vivo — many designed proteins have low
  thermal / proteolytic stability.
- **Solubility** — folding ≠ solubility; ~ 30 % of
  designs aggregate.
- **In vivo function** — clinical translation slow;
  immunogenicity + PK uncertainties.

## Compared to natural protein engineering

Pre-2020 protein engineering: mutate a natural protein +
screen for improved properties (Arnold's directed
evolution).

Post-2020: design a protein from scratch.

Both work; the natural-engineering approach now uses ML
+ AlphaFold to guide which mutations to test.

## Try it in the app

- **Proteins tab** → fetch any PDB → see the sequence +
  fold; AlphaFold-predicted models also accessible.
- **Tools → Macromolecules window…** → explore proteins
  + sequence viewer.
- **Glossary** → search *AlphaFold*, *RFdiffusion*,
  *ProteinMPNN*, *Protein design*, *De novo*,
  *Catalytic triad*, *Density functional theory*.

Next: **Neural network potentials deeper**.
