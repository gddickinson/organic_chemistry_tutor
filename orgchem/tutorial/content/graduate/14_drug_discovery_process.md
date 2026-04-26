# Drug discovery process — from target → IND

Bringing a new medicine to first-in-human (IND filing) takes
~ 5-8 years + > $1 billion. The drug-discovery pipeline is
the orchestration of biology + chemistry + DMPK + safety
that turns a hypothesis into a clinical candidate.

## Stages overview

```
Target ID → Hit ID → Hit-to-Lead → Lead Optimisation → Candidate → Preclinical → IND
   1 yr      0.5-1 yr     1-2 yr        2-3 yr           1 yr        1-2 yr
```

## 1. Target identification + validation

- **Disease biology** — what protein / pathway, when
  perturbed, produces a therapeutic effect?
- **Genetic validation** — Mendelian disease + GWAS hits +
  CRISPR knockout phenotypes.
- **Druggability assessment** — does the target have a
  pocket? Can a small molecule modulate it?
- **Target product profile (TPP)** — required potency,
  selectivity, PK, dose, route of administration.

Famous wins: **PCSK9** (familial hypercholesterolemia →
evolocumab + alirocumab), **BCL-2** (CLL → venetoclax),
**KRAS-G12C** (lung cancer → sotorasib + adagrasib).

## 2. Hit identification

Generate starting points:

- **High-throughput screening (HTS)** — typical pharma
  library 1-2 M compounds. Hit rate ~ 0.01-0.1 %.
- **Fragment-based drug design (FBDD)** — screen ~ 1000-
  10 000 fragment-sized (~ 250 Da) compounds at high
  concentration; weak hits (mM K_d) but high efficiency
  per atom. Sources: NMR (SAR by NMR, Fesik), X-ray
  crystallography fragment soaks, SPR, biochemical assay.
  Examples: vemurafenib (PLX-4032 melanoma), venetoclax.
- **DNA-encoded library (DEL)** screening — covered in the
  advanced curriculum.
- **Virtual screening** — dock 10⁶-10⁹ compounds into a
  pocket; pick top-ranked for experimental confirmation.
- **Hit hopping / scaffold hopping** — start from a known
  inhibitor (literature, competitor) + design around it.

## 3. Hit-to-lead

A hit becomes a lead by improving:

- **Potency** — typically 100-1000× to reach single-digit
  µM → nM range.
- **Selectivity** — drop activity vs related off-targets
  (kinase off-target panels, hERG, CYPs).
- **Property profile** — solubility, permeability, plasma
  stability.
- **Synthetic accessibility** — usable as a chemistry
  starting point for SAR.

### Structure-based drug design (SBDD)

X-ray + cryo-EM + AlphaFold structures give a 3D map of the
target pocket. **Co-crystal structures** of hit + protein
let you see what works + design improvements:

- Add H-bond donor / acceptor where there's a polar
  protein partner.
- Fill hydrophobic pockets with cyclopropyl, fluorine,
  CF₃.
- Cap a charged group to break a salt bridge.

### Fragment growing + linking + merging

- **Growing** — add substituents from a fragment toward a
  nearby protein subpocket.
- **Linking** — two fragments in adjacent subpockets can be
  tethered with a linker.
- **Merging** — combine pharmacophore elements from two
  ligands.

## 4. Lead optimisation

Where most chemistry happens. SAR exploration over many
analogues:

- **Free-Wilson + matched-molecular-pair analysis (MMPA)** —
  decompose contributions of substituents.
- **Bioisostere swaps** — replace a metabolically labile
  group (e.g., CH₃ → CF₃, phenyl → thiophene, COOH →
  tetrazole).
- **Conformational restriction** — install a ring or chiral
  centre to bias the bioactive conformation.
- **Property-based design** — design within a Lipinski-
  compliant box; track logP, PSA, HBD, HBA, AromRingCount.

### Metabolic stability + DMPK

- **CYP450 metabolism** — major elimination pathway. CYP3A4,
  2D6, 2C9, 2C19, 1A2 are the big ones. Predict by
  microsomal stability + isoform-specific assays.
- **PK profile** — Cmax, AUC, t½, F (oral bioavailability).
  Ideally daily oral dosing → t½ = 8-24 h.
- **Distribution** — protein-binding (free fraction
  matters), tissue distribution, CNS penetration if needed.
- **Safety in vitro** — hERG IC50 > 30 µM (cardiac safety),
  Ames negative (mutagenicity), no overt CYP3A4 inhibition.

## 5. Candidate selection

The candidate must pass go / no-go criteria:

- Potency + selectivity targets.
- Acceptable PK in 2 species (rat, dog typical).
- Safety pharmacology (hERG, CV, CNS) clean.
- 7-14 day repeat-dose tox in 2 species at 10-30 × predicted
  human dose.
- Manufacturable synthesis (scale-up + cost-of-goods).
- IP position — composition-of-matter patent in place.

## 6. Preclinical → IND

- **GLP toxicology** — 2-13 week studies in rodent + non-
  rodent (dog, monkey).
- **Genotox + carcinogenicity** — for chronic-dose drugs.
- **Reprotox** — for drugs intended for women of
  childbearing age.
- **Manufacturing scale-up** — kg-scale synthesis,
  formulation, stability data, GMP-compliant API.
- **IND-enabling DMPK** — full PK / PD modelling, predicted
  human dose.

The IND package goes to the FDA. After 30-day review with no
clinical-hold, **Phase 1 first-in-human** can start.

## Why most drugs fail

- **Phase 1**: ~ 10 % attrition (PK, immediate tolerability).
- **Phase 2 (efficacy)**: ~ 30 % succeed — the big filter.
  Many drugs are safe but don't work.
- **Phase 3 (confirmation)**: ~ 60 % succeed.
- **Approval**: ~ 90 % of those that finish Phase 3.

Overall: ~ 1 in 10 000 hits make it to market. The cost +
attrition is why pharma R&D budgets are eye-watering.

## Try it in the app

- **Tools → Drug-likeness…** → check Lipinski + Veber +
  Ghose + PAINS for a SMILES.
- **Tools → Medicinal chemistry → SAR series…** → see a
  toy SAR series for COX inhibitors.
- **Glossary** → search *Lead optimisation*, *Fragment-
  based drug design*, *SBDD*, *Bioisostere*, *DMPK*, *IND*.

Next: **X-ray crystallography for chemists**.
