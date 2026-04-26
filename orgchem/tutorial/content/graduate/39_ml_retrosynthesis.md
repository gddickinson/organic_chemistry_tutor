# ML for retrosynthesis — AiZynthFinder, ASKCOS, Synthia

Retrosynthesis is what chemists do every day. It can be
formalised + automated by machine learning. By 2025, ML
retrosynthesis platforms suggest credible routes for 60-80
% of organic targets in seconds.

## What "retrosynthesis" means computationally

Decompose a target molecule **T** into precursor pairs
{P₁, P₂} via **transforms** (reverse-direction templates of
known reactions):

```
T  ←(transform 1)←  P₁ + P₂
                  ←(transform 2)←  P₁' + P₂'
                  ...
```

Continue recursively until precursors are commercially
available (typical "stop": top 10⁵-10⁷ Aldrich /
Enamine REAL compounds).

## Three approaches

### 1. Template-based (Synthia / ASKCOS)

Pre-extract templates from a reaction database (USPTO,
Reaxys, Pistachio) → store as SMARTS rules → apply to
target → enumerate precursors.

- **Pros**: chemically interpretable; gives literature
  precedent.
- **Cons**: scope limited to known transforms; misses
  novel chemistry.

### 2. Template-free (Molecular Transformer)

Train a transformer (like GPT) on a corpus of
(product → reactants) sequences. The model directly
predicts reactant SMILES from product SMILES.

- **Pros**: handles novel transforms.
- **Cons**: less interpretable; hallucinates sometimes.

IBM RXN Molecular Transformer (Schwaller et al. 2019).

### 3. Graph-based ML

Operate on molecular graphs (not SMILES strings) — propose
disconnections directly via graph operations.

- **Pros**: respect molecular structure; better few-shot
  generalisation.
- **Cons**: harder to train + interpret.

## Major platforms

| Platform | Type | Owner |
|----------|------|-------|
| **AiZynthFinder** | template-based, MCTS-driven | open source (AstraZeneca) |
| **ASKCOS** | template-based + neural | open source (MIT Coley) |
| **Synthia** | template-based + heuristics | Sigma-Aldrich (Grzybowski) |
| **Molecular Transformer / IBM RXN** | template-free | IBM |
| **Manifold** (Postera) | hybrid | proprietary |
| **Chemix.ai / Iktos / Insilico** | mixed AI / RL | proprietary |

## Search strategy: MCTS + scoring

Most platforms use **Monte Carlo Tree Search (MCTS)**:

1. Root node = target.
2. Expand node = enumerate disconnections (top K from
   policy network).
3. Score each disconnection (probability of success).
4. Recurse on each child.
5. Stop when reaching commercial SM or step-budget.

Scoring heuristics combine:

- Disconnection probability (template frequency in
  training data).
- Cost of starting materials.
- Number of steps.
- Reaction conditions (avoid forbidden ones).

## Strengths in 2025

- **Coverage**: 60-80 % of drug-like targets get a
  3-7-step route within seconds.
- **Speed**: < 30 sec per target on a desktop.
- **Cost-aware**: prefer cheap SMs.
- **Patent-aware**: avoid patented routes (Synthia).

## Weaknesses

- **Stereochemistry** — most platforms still struggle to
  predict ee correctly.
- **Selectivity** — predicting which Pd cat / which solvent
  / which T is hard.
- **Novel scaffolds** — outside training distribution; many
  fail.
- **Multi-step reagent compatibility** — order matters;
  models sometimes propose protected intermediates that
  conflict with downstream chemistry.

## Validating ML-suggested routes

Always check:

1. **Known reactions?** — every step should map to a
   published reaction or a reasonable extension.
2. **Reagent availability** — Aldrich + Sigma + Combi-Blocks
   + Enamine + AK Sci.
3. **Functional-group tolerance** — does the proposed
   reaction tolerate other groups?
4. **Stereochemistry** — does the route control the
   absolute config you need?

## Combining ML + human

The current workflow:

1. Run AiZynth / ASKCOS to get top 10 routes.
2. Filter manually for plausibility.
3. Try the top 1-2; if fail, iterate.
4. Add human heuristics ("this protecting group won't
   work; that catalyst is too expensive").

ML doesn't replace the chemist; it accelerates the
ideation step.

## Industrial uses

- **Pharma SAR**: generate proposed routes for medicinal-
  chemistry analogues in seconds.
- **Process chemistry**: identify alternative routes when
  patent-blocked.
- **Compound supply**: feed ASKCOS into custom-synthesis
  CRO platforms (WuXi, Pharmaron, AKSciences) for
  on-demand chemistry.
- **Burke iterative cross-coupling** at MIT — hooked into
  AI platforms for automatic code-generation of synthesis
  recipes.

## Try it in the app

- **Tools → Retrosynthesis…** → input target SMILES → see
  template-based disconnection suggestions (a simplified
  version of these platforms).
- **Glossary** → search *Retrosynthesis*, *Synthon*, *AI
  for chemistry*, *Molecular transformer*, *MCTS*.

Next: **ML for protein design (RFdiffusion, ProteinMPNN)**.
