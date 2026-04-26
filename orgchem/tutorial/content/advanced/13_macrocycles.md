# Macrocycle synthesis — escaping flatland

A **macrocycle** is a ring of 12+ atoms. Macrocycles bridge
the gap between small-molecule drugs (< 500 Da, rigid +
flat) and biologics (> 5000 Da, large + slow). They access
extracellular targets that small molecules can't (e.g.
protein-protein interactions) without losing oral
bioavailability — **modality #2.5** in modern pharma.

## Why macrocycles?

- **Conformational pre-organisation** — pre-formed bioactive
  shape, smaller entropic cost on binding.
- **Larger surface area** — engages flat protein-protein
  interfaces.
- **Reduced rotatable bonds** — better permeability than
  open-chain analogues of similar MW (Veber rule).
- **Often natural products** — vancomycin, FK506, rapamycin,
  erythromycin, ivermectin, daptomycin, eribulin → all
  macrocyclic.

## The synthesis problem

Forming a 12+ membered ring intramolecularly competes with
**intermolecular dimerisation + oligomerisation** because the
two reactive ends are conformationally far apart. Three
strategies:

### 1. High dilution

Below ~ 1 mM substrate, intramolecular > intermolecular by
mass-action. Slow + low-throughput. Standard for first
attempts.

### 2. Templating

Use a metal cation, a hydrogen-bond donor, or a covalent
template that pre-organises the chain into a near-cyclic
shape. Sauvage's catenane + Stoddart's rotaxane synthesis
(2016 Nobel) work this way.

### 3. Peptide turn / β-turn templates

For peptidic macrocycles, install a D-amino acid + Pro to
nucleate a turn — the linear precursor wants to be cyclic
already.

## Bond-forming methods

Modern macrocyclisations use:

| Method | Bond formed | Example |
|--------|-------------|---------|
| **RCM** (ring-closing metathesis) | C=C | Eribulin (Halaven) |
| **Macrolactonisation** | ester | Erythromycin, FK506 |
| **Macrolactamisation** | amide | Vancomycin, daptomycin |
| **Pd cross-coupling** | C-C / C-N | many drug discovery efforts |
| **CuAAC click** | triazole | peptidomimetic stapled peptides |
| **Disulfide** | S-S | oxytocin, octreotide |
| **Glaser-Hay** | C≡C-C≡C | Sondheimer-Gilbert annulenes |
| **Nucleic-acid-templated synthesis** | various | mRNA-display libraries |

## Stapled peptides

Synthetic helix-locking by C–C macrocyclisation across i, i+4
or i, i+7:

- **Hydrocarbon staple** (Verdine) — two α-methyl, α-alkenyl
  amino acids in a peptide, linked by RCM.
- **Lactam bridge** — Lys + Glu sidechains form an amide.
- **Disulfide bridge** — Cys + Cys.

The α-helix conformation is locked, doubling cellular
penetration + protease stability vs the linear analog.
**ALRN-6924** (MDM2/MDMX inhibitor) reached clinical trials.

## Natural-product macrolides

Polyketide synthases (PKS) build long acyl chains then
cyclise enzymatically — nature's solution to the macro-
lactonisation problem.

- **Erythromycin** — 14-membered, antibiotic, $billion drug.
- **FK506 (tacrolimus)** — 23-membered, immunosuppressant.
- **Rapamycin (sirolimus)** — 31-membered, mTOR inhibitor.
- **Avermectins (ivermectin)** — 16-membered, antiparasitic
  (2015 Nobel: Ōmura + Campbell).

## Beyond Lipinski

Lipinski's rule of 5 (MW < 500, logP < 5, HBD < 5, HBA < 10)
defines "drug-like" small molecules. Macrocycles routinely
violate it:

- **Cyclosporin A** — MW 1203, 11 amide bonds, 7 NH
  potential donors → still orally bioavailable because most
  N-H bonds are intramolecularly H-bonded in the active
  conformation.
- **Beyond rule-of-5 (bRo5) space** — MW 500-1500, modest
  PSA, conformational chameleonicity (folds tightly in
  membranes, opens up in water).

Modern pharma actively explores this space — Pfizer's
PROTAC platform, Celgene's CC-99677, Vertex's lumacaftor
analogues all push above 500 Da.

## Try it in the app

- **Reactions tab** → load Grubbs metathesis — RCM for
  macrocyclisation.
- **Tools → Drug-likeness…** → compare cyclosporin (bRo5)
  vs ibuprofen (rule-of-5) MW + logP + PSA + HBD.
- **Glossary** → search *Macrocycle*, *Macrolactonisation*,
  *RCM*, *Stapled peptide*, *bRo5 space*.

Next: **Solid-phase synthesis — building peptides + nucleic
acids on resin**.
