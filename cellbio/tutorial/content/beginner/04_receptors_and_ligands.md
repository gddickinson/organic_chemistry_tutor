# Receptors and ligands

A receptor is a protein that selectively binds a ligand
and converts that binding event into a downstream signal.
Receptor-ligand interaction is the molecular substrate of
both endogenous physiology and pharmacology.

## What makes a good ligand-receptor pair

Three properties define receptor pharmacology:

- **Affinity** — how tightly the ligand binds. Quantified
  by Kd (the ligand concentration at which 50 % of
  receptors are occupied). Endogenous neurotransmitters
  often have nM-µM Kd; high-affinity engineered antibodies
  reach pM-fM.
- **Selectivity** — preference for one receptor over
  related family members. β1- vs β2-selective adrenergic
  drugs hinge on subtle structural differences in the
  ligand-binding pocket.
- **Efficacy** — what happens after binding. Full agonists
  give the maximum receptor response; partial agonists
  give a sub-maximal response even at full occupancy;
  antagonists bind but produce no response (and block
  agonist binding); inverse agonists actively *decrease*
  basal receptor activity.

## Orthosteric vs allosteric sites

Most drugs + endogenous ligands bind the **orthosteric
site** — the same pocket the natural ligand uses.

**Allosteric ligands** bind a separate site + modulate the
receptor's response to orthosteric ligand. Benzodiazepines
are the classic example — they bind the GABA-A receptor at
a site distinct from GABA itself + potentiate GABA's effect
without being agonists themselves (positive allosteric
modulators, PAMs).

Allosteric ligands have practical advantages: subtype
selectivity (the allosteric site is less conserved than
the orthosteric pocket) + ceiling effects (without
endogenous agonist, allosteric modulators do nothing).

## The dose-response curve

Plotting fraction of receptors occupied (or biological
response) vs ligand concentration on a log axis gives the
classic sigmoidal dose-response curve. Two parameters
characterise it:

- **EC50** (or Kd for binding) — the concentration giving
  50 % response. Lower EC50 = more potent ligand.
- **Emax** — the maximum response achievable. Defines
  intrinsic efficacy.

A full agonist has the same Emax as the endogenous ligand;
a partial agonist has lower Emax even at saturating
concentrations.

## Receptor regulation

Cells don't leave their receptors permanently exposed to
ligand. Several feedback mechanisms desensitise receptors:

- **GRK / arrestin internalisation** — agonist-occupied
  GPCRs get phosphorylated by GRK kinases, recruit β-
  arrestin, and undergo clathrin-mediated endocytosis.
  Removes them from the cell surface temporarily
  (resensitisation) or permanently (downregulation).
- **Receptor downregulation** — chronic agonist exposure
  reduces total receptor number via lysosomal degradation
  + reduced gene expression.
- **Tachyphylaxis** — rapid loss of response on repeated
  dosing; classic with short-acting β2-agonist overuse in
  asthma.

## Endogenous vs synthetic ligands

Most drug discovery starts from an endogenous ligand and
modifies it for:

- **Drug-like properties** — oral availability, BBB
  crossing, half-life.
- **Subtype selectivity** — hit β1 not β2.
- **Functional selectivity** — bias signalling toward one
  downstream branch (e.g. G-protein vs β-arrestin).

Sometimes drugs are completely unrelated to endogenous
ligands — discovered via high-throughput screening or
serendipity (cisplatin, lithium, sulfa drugs).

## Why this matters

Every drug action is a receptor-ligand interaction.
Understanding affinity + selectivity + efficacy gives you
a framework for predicting:

- Why one statin is more potent than another (rosuvastatin
  vs simvastatin Kd for HMG-CoA reductase).
- Why one β-blocker is cardio-selective while another
  isn't (metoprolol vs propranolol).
- Why partial agonists can be safer (buprenorphine for
  opioid use disorder vs full-agonist methadone).

## Try it in the app

- **Window → Pharmacology Studio → Receptors tab** — see
  endogenous ligands per receptor + drug-class targets.
- **Tools → Lab calculator → Acid-base tab** for pKa /
  protonation logic relevant to receptor binding (Ki vs
  pH).

Next: **Second messengers — cAMP, IP3, Ca²⁺**.
