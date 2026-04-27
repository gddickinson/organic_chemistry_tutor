# Biologics

Biologic drugs — proteins, peptides, antibodies,
nucleic acids, cells — now account for the majority of
top-selling drugs by revenue + the most clinically-
transformative new approvals.  They follow a different
development + manufacturing + regulatory path than
small molecules.

## What counts as a biologic

The FDA's regulatory definition (Public Health Service
Act Section 351):

> "A virus, therapeutic serum, toxin, antitoxin,
> vaccine, blood, blood component or derivative,
> allergenic product, protein (except any chemically
> synthesised polypeptide), or analogous product...
> applicable to the prevention, treatment, or cure of a
> disease or condition of human beings."

Practical categories:
- **Proteins** — recombinant human insulin, growth
  hormone, EPO, factor VIII, GLP-1 analogues.
- **Monoclonal antibodies** (mAbs).
- **Antibody-drug conjugates** (ADCs).
- **Fusion proteins** (etanercept, abatacept,
  romiplostim, aflibercept).
- **Vaccines** — protein subunit, conjugate, viral
  vector, mRNA.
- **Cell + gene therapies** — CAR-T, AAV, lentiviral.
- **Nucleic-acid therapeutics** — ASOs, siRNAs, mRNAs.

## Monoclonal antibodies — the workhorse modality

mAbs were the breakout biologic technology of the
1990s-2010s.  As of 2026, > 100 mAbs are FDA-approved,
spanning:

- **Oncology** — rituximab, trastuzumab, bevacizumab,
  cetuximab, pembrolizumab, nivolumab, ipilimumab,
  daratumumab, polatuzumab vedotin (ADC).
- **Inflammation / autoimmunity** — adalimumab,
  infliximab, golimumab, etanercept (fusion not mAb),
  ustekinumab, secukinumab, dupilumab, omalizumab.
- **Infectious disease** — palivizumab (RSV),
  bezlotoxumab (C. difficile), various COVID-19
  spike-targeting mAbs (waning relevance).
- **Cardiovascular** — evolocumab, alirocumab (PCSK9),
  inclisiran (siRNA, not mAb).
- **Ophthalmology** — ranibizumab, aflibercept,
  faricimab, brolucizumab.
- **Migraine** — erenumab, fremanezumab, galcanezumab
  (CGRP / CGRP-R).
- **Hematology** — eculizumab, ravulizumab, crovalimab.

### mAb structure

Native IgG: two heavy chains + two light chains, ~ 150
kDa, two antigen-binding sites (Fab) + one Fc region.

Engineering generations (chronological + suffix
naming):
- **Murine** (-omab) — fully mouse.  HAMA response →
  short half-life + immunogenicity.  E.g. muromonab.
  Largely abandoned.
- **Chimeric** (-ximab) — mouse Fv on human Fc.  Less
  immunogenic.  Rituximab, infliximab.
- **Humanised** (-zumab) — mouse CDRs grafted onto
  human framework.  Trastuzumab, omalizumab,
  pembrolizumab.
- **Human / fully human** (-umab) — phage-display
  libraries (Greg Winter Nobel 2018) or transgenic
  mice (HuMAb mouse, XenoMouse).  Adalimumab,
  panitumumab, evolocumab.

### Mechanism of action

mAbs work by:
- **Receptor blockade** — preventing ligand binding
  (cetuximab/EGFR, evolocumab/PCSK9).
- **Receptor activation / agonism** — atezolizumab
  (PD-L1) blocks the inhibitory checkpoint.
- **Ligand sequestration** — adalimumab + infliximab
  capture TNFα; bevacizumab captures VEGF.
- **Complement-dependent cytotoxicity (CDC)** — Fc
  region recruits C1q → MAC formation (rituximab
  partial mechanism).
- **Antibody-dependent cellular cytotoxicity (ADCC)** —
  Fc engages NK-cell FcγRIIIa → target lysis
  (rituximab, trastuzumab).
- **Antibody-dependent cellular phagocytosis (ADCP)** —
  via macrophage Fc receptors.
- **Direct apoptosis induction** — receptor crosslinking
  triggers death signalling (rituximab to a degree).

Fc engineering (afucosylation, mutations like S239D /
I332E) enhances ADCC for oncology mAbs (obinutuzumab,
mogamulizumab); LALA + N297A mutations ablate Fc
function for safety-critical applications.

## Antibody-drug conjugates (ADCs)

A mAb + a cytotoxic payload + a linker.  The mAb
delivers the payload selectively to antigen-expressing
cells.  ADCs combine the targeting precision of mAbs
with the cell-killing power of small molecules.

Key components:
- **mAb** — targets a tumour-expressed antigen.
- **Linker** — cleavable (vc, peptide-cleavable;
  hydrazone, pH-cleavable; disulfide, GSH-cleavable)
  or non-cleavable (released after lysosomal
  degradation of mAb).
- **Payload** — auristatin (MMAE / MMAF, microtubule),
  maytansinoid (DM1 / DM4, microtubule), calicheamicin
  (DNA), camptothecin (topo I — exatecan / SN-38),
  PBD dimers (DNA crosslink).

Approved ADCs (selected):
- **Brentuximab vedotin** (Adcetris) — CD30 / vc-MMAE
  — Hodgkin lymphoma + ALCL.
- **Trastuzumab emtansine (T-DM1, Kadcyla)** — HER2 /
  thioether-DM1 — HER2+ breast cancer.
- **Trastuzumab deruxtecan (T-DXd, Enhertu)** — HER2 /
  vc-camptothecin (DXd) — HER2-low + HER2+ breast,
  gastric, lung cancers.  Bystander effect from
  membrane-permeable payload.
- **Sacituzumab govitecan (Trodelvy)** — TROP2 /
  vc-SN-38 — TNBC + HR+ breast.
- **Polatuzumab vedotin** (Polivy) — CD79b / vc-MMAE —
  DLBCL.
- **Enfortumab vedotin** — Nectin-4 / vc-MMAE —
  urothelial cancer.

## Fusion proteins

Two protein domains genetically joined:

- **Etanercept** — TNFα receptor extracellular domain
  + IgG1 Fc → soluble decoy for TNFα.  RA, psoriasis.
- **Abatacept** — CTLA-4 + Fc → blocks T-cell
  costimulation.  RA.
- **Aflibercept** — VEGFR1/2 domains + Fc → VEGF /
  PlGF trap.  AMD, mCRC.
- **Romiplostim** — TPO peptide + Fc → TPO mimetic.
  ITP.
- **Dulaglutide** + **albiglutide** — GLP-1 + Fc / HSA
  → long-half-life GLP-1 agonists.

## Bispecific antibodies + multispecifics

Engineered to bind two antigens:

- **Blinatumomab (Blincyto)** — BiTE (CD19 × CD3) →
  redirects T cells to lyse B-cell ALL cells.
- **Emicizumab (Hemlibra)** — bridges activated FIX +
  FX → mimics FVIIIa for haemophilia A.
- **Mosunetuzumab + epcoritamab + glofitamab + odronextamab**
  — CD20 × CD3 BiTEs for B-cell lymphomas.
- **Teclistamab + elranatamab + talquetamab + linvoseltamab**
  — BCMA / GPRC5D × CD3 for multiple myeloma.
- **Faricimab** — VEGF × Ang-2 for AMD / DME.
- **Tezepelumab** — TSLP for severe asthma.

## Biosimilars

Biologics differ from small-molecule generics:
- Manufactured in living cells; minor structural
  differences inevitable batch-to-batch.
- Cannot be exactly chemically reproduced.
- Regulators require CLINICAL comparability
  demonstration.

EMA + FDA biosimilar pathways:
- **Comparability** in analytical, structural, PK / PD,
  + clinical-efficacy / safety data.
- Phase 3-equivalent comparability studies typically
  required.
- **Interchangeability** is a separate higher bar —
  US FDA only.

Approved biosimilars:
- Filgrastim biosimilars (Zarxio, Nivestym, Granix).
- Trastuzumab biosimilars (Ogivri, Herzuma, Trazimera).
- Adalimumab biosimilars (Amjevita, Cyltezo, Hyrimoz,
  Hadlima, Yusimry, Hulio).
- Bevacizumab biosimilars (Mvasi, Zirabev).
- Insulin biosimilars (Semglee for insulin glargine).

Cost typically 15-35 % below originator.  Adoption
slower than small-molecule generics due to clinician
inertia + payer dynamics.

## Manufacturing

mAbs + most biologics are produced in:
- **CHO cells** (Chinese hamster ovary) — workhorse;
  > 70 % of approved mAbs.
- **HEK293** — for many gene therapies.
- **Yeast** (Pichia pastoris) — insulin, some
  recombinant proteins.
- **E. coli** — for non-glycosylated proteins (insulin,
  growth hormone, Fab fragments).
- **Mammalian cell-free systems** — emerging for
  on-demand production.

Process is bioreactor-scale (200-25 000 L), followed
by extensive downstream purification (Protein A
affinity → ion exchange → SEC → viral inactivation →
filtration → formulation).

Manufacturing dominates COGS; ~ $50-200 / g for typical
mAbs at scale.

## Immunogenicity

mAbs + biologics can trigger anti-drug antibodies
(ADAs) → loss of efficacy + hypersensitivity.

Mitigators:
- Humanisation / fully-human design.
- Avoidance of T-cell epitopes (in silico screening).
- Aggregate-free formulation.
- Manageable subcutaneous routes (less immunogenic
  than IV in some cases — counterintuitive, but
  steady-state SC release reduces peak antigen
  presentation).

Some patient populations are inherently immunogenic-
prone (e.g. RA patients on monotherapy adalimumab
develop ADAs more often than those on adalimumab +
methotrexate).

## Cell + gene therapies

Cover briefly here; more in the graduate "Modern
modalities" lesson.

- **CAR-T** — autologous T cells transduced with a
  chimeric antigen receptor (anti-CD19 in approved
  haematologic products).
- **AAV gene therapy** — adeno-associated virus
  delivers a transgene to non-dividing cells (Luxturna
  for RPE65 retinal dystrophy; Zolgensma for SMA;
  Roctavian + Hemgenix for haemophilia).
- **Lentiviral ex-vivo gene therapy** — autologous
  HSCs corrected ex vivo (Skysona for ALD; Zynteglo +
  Casgevy for β-thalassaemia / SCD).

## Try it in the app

- **Window → Pharmacology Studio → Drug classes** —
  monoclonal antibody class entries (TNFα, IL-6, PD-1,
  CD20, HER2, anti-CGRP), ADC entries.
- **OrgChem → Macromolecules → Proteins** — fetch
  rituximab Fab, trastuzumab Fab, pembrolizumab Fab
  via PDB IDs (e.g. 2OSL, 1N8Z, 5DK3).
- **Window → Biochem Studio → Enzymes** — biologic
  drug targets (PCSK9, complement C5, etc.) sit
  here.

Next: **Pharmacogenomics**.
