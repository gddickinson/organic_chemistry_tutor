# Modern modalities

A modality is the physical-chemical class of a
therapeutic — the kind of "thing" the drug is.  The
2010s-2020s broke the small-molecule / biologic
duopoly into a much richer landscape.  Each modality
has distinct PK, PD, manufacturing, and delivery
considerations.

## PROTACs + molecular glues — induced protein
degradation

Instead of inhibiting a protein, recruit the
ubiquitin-proteasome system to DEGRADE it.

### PROTACs

PROteolysis-TArgeting Chimeras: bivalent molecules
with a target-binding warhead + an E3 ligase ligand
joined by a linker.  Bring target + E3 into proximity
→ ubiquitination → proteasomal degradation.

Advantages over small-molecule inhibitors:
- **Catalytic** — one PROTAC molecule can degrade
  many target copies (high efficiency).
- **Removes scaffold + non-catalytic functions** —
  not just catalysis.
- **Overcomes mutations** that confer inhibitor
  resistance.
- **Drugs the "undruggable"** — targets without
  catalytic active sites.

Common E3 ligases:
- **CRBN** (cereblon) — used by IMiDs (thalidomide,
  lenalidomide, pomalidomide); PROTAC IMiD-conjugates.
- **VHL** (von Hippel-Lindau) — first PROTAC ligand
  class to deliver clinical activity.
- **MDM2**, **IAPs**, **DCAF15** — emerging.

Clinical PROTACs:
- **Arvinas ARV-471 (vepdegestrant)** — ER PROTAC,
  Phase 3 in metastatic breast cancer.
- **Arvinas ARV-110 (bavdegalutamide)** — AR PROTAC
  for prostate cancer.
- **Kymera KT-474** — IRAK4 PROTAC for hidradenitis
  suppurativa.
- **C4 Therapeutics CFT8634** — BRD9 PROTAC for SMARCB1-
  deleted tumours.

Limitations:
- Very large molecules (~ 800-1 200 Da); poor oral
  bioavailability.
- "Hook effect" — at high concentrations, PROTAC
  saturates each end + binary complexes form,
  REDUCING ternary-complex formation + degradation.
- Linker optimisation is empirical + tedious.
- Tissue-specific E3 expression limits where degraders
  work.

### Molecular glues

Smaller (~ 500-800 Da) bifunctional concept — a
small molecule binds either target or E3 + induces a
neomorphic protein-protein interface.

Iconic molecular glues:
- **Thalidomide / lenalidomide / pomalidomide** — bind
  CRBN + recruit IKZF1 / IKZF3 (ikaros family) for
  degradation; the molecular-glue mechanism explains
  their multiple myeloma activity.
- **Indisulam** — recruits RBM39 to DCAF15.
- **CC-90009** — GSPT1 degrader for AML.

Advantages: drug-like properties; oral; smaller
chemical-matter cost.  Discovery is empirical (or via
chemical genetics screens) + a hot area for AI
generative chemistry.

## mRNA therapeutics

Synthetic mRNAs encoding therapeutic proteins,
delivered in lipid nanoparticles (LNPs).

### Mechanism

1. mRNA is enzymatically transcribed in vitro from a
   DNA template.
2. Modified nucleotides (pseudouridine ψ,
   N1-methylpseudouridine m1ψ) reduce innate immune
   activation + improve translation (Karikó +
   Weissman 2023 Nobel).
3. Capping (ARCA / CleanCap) + polyA tailing for
   stability + translation.
4. Encapsulated in LNPs (ionisable lipid + cholesterol
   + PEG-lipid + helper phospholipid).
5. Injected (IM for vaccines, IV for therapeutics).
6. LNPs taken up via endocytosis → endosomal escape
   → cytoplasmic translation → protein product.

### Approvals + late-clinical

- **Pfizer-BioNTech BNT162b2 (Comirnaty)** —
  spike-encoding COVID-19 vaccine.
- **Moderna mRNA-1273 (Spikevax)** — COVID-19.
- **Moderna mRNA-1345 (mResvia)** — RSV.
- **Moderna mRNA-1083 + GSK** — combination flu +
  COVID.
- **Personalised cancer vaccines** (Moderna
  mRNA-4157 + Merck pembrolizumab in melanoma; Phase
  3 INTerpath series).
- **CRISPR-Cas9 mRNA + sgRNA + LNP** for in-vivo gene
  editing (Verve VERVE-101 PCSK9; Intellia NTLA-2002
  HAE).

Pros: fast design (mRNA is software); scalable
manufacturing; non-integrating (no genome insertion);
flexible.  Cons: cold-chain (-20 to -80 °C),
LNP-related reactivity (post-vaccination myocarditis,
allergic reactions), mostly liver-tropic IV (LNP
biodistribution challenge).

### Self-amplifying mRNA + circular RNA

- **saRNA** — encode an alphavirus replicase →
  amplify the message in vivo → smaller dose, longer
  expression.  Arcturus, Replicate Bioscience.
- **circRNA** — circular RNA via internal ribosome
  entry sites → no PolyA, no cap, more stable.
  Orna, Laronde.

## AAV gene therapy

Adeno-associated virus delivers a transgene to non-
dividing cells for long-lasting expression.

### Architecture

- **Capsid serotype** — natural (AAV1-13) + engineered
  (AAVrh10, AAV-DJ, AAV-PHP.B for CNS, AAV-Anc80) —
  determines tropism.
- **Vector genome** — promoter + transgene + polyA,
  packaged in single-stranded DNA up to ~ 4.7 kb
  (or self-complementary up to ~ 2.4 kb).
- **Manufacturing** — HEK293 transient triple-
  transfection or insect-Sf9 baculovirus, ultracentrif-
  ugation purification.

### Approved AAV gene therapies

- **Luxturna (voretigene neparvovec)** — RPE65 retinal
  dystrophy; subretinal injection.
- **Zolgensma (onasemnogene abeparvovec)** — SMN1 for
  spinal muscular atrophy; single IV infusion.
- **Hemgenix (etranacogene dezaparvovec)** — F9 for
  haemophilia B.
- **Roctavian (valoctocogene roxaparvovec)** — F8 for
  haemophilia A.
- **Elevidys (delandistrogene moxeparvovec)** — micro-
  dystrophin for DMD.
- **Upstaza (eladocagene exuparvovec)** — AADC
  deficiency; intracerebral injection.

Costs $1-3.5 M per single-dose treatment.

### Limitations

- **Pre-existing neutralising antibodies** to common
  serotypes (~ 30-70 % of population) preclude
  treatment.
- **Re-dosing infeasible** because of induced
  immunogenicity to the capsid.
- **Hepatotoxicity** + complement activation +
  thrombotic microangiopathy at high doses.
- **Expression durability** — transgene expression
  declines over years in dividing tissues.
- **Manufacturing** is constrained + expensive.

## CAR-T + engineered cell therapies

Autologous T cells transduced ex vivo with a
chimeric antigen receptor (CAR) → infused back to
target tumour antigens.

### CAR architecture

- Single-chain Fv (scFv) targeting domain +
  transmembrane + co-stimulatory (CD28 / 4-1BB) +
  CD3ζ activation domain.
- Lentiviral or retroviral or transposon-based
  transduction.
- 2nd / 3rd / 4th-generation CARs add cytokine /
  safety-switch / armoured features.

### Approved CAR-Ts

- **Kymriah (tisagenlecleucel)** — CD19 / 4-1BB —
  paediatric ALL, DLBCL.
- **Yescarta (axicabtagene ciloleucel)** — CD19 / CD28
  — DLBCL, FL, MCL.
- **Tecartus (brexucabtagene autoleucel)** — CD19 /
  CD28 — MCL, ALL.
- **Breyanzi (lisocabtagene maraleucel)** — CD19 /
  4-1BB — DLBCL.
- **Abecma (idecabtagene vicleucel)** — BCMA — multiple
  myeloma.
- **Carvykti (ciltacabtagene autoleucel)** — BCMA —
  multiple myeloma.

Toxicities:
- **Cytokine-release syndrome (CRS)** — fever,
  hypotension, capillary leak.  Tocilizumab + steroids.
- **Immune effector cell-associated neurotoxicity
  syndrome (ICANS)** — encephalopathy, aphasia,
  seizures.

Costs $400 K - $500 K per treatment.

### Allogeneic + off-the-shelf cell therapies

- **Allogeneic CAR-T** — donor-derived, gene-edited
  (TCR knock-out, B2M knock-out, CD52 knock-out for
  lymphodepletion resistance).  Allogene, Caribou,
  Beam.
- **CAR-NK** — natural-killer-cell-based.
  Affimed, Nkarta, Fate.
- **TIL therapy** — tumour-infiltrating lymphocyte
  expansion.  Iovance Lifileucel approved 2024 for
  melanoma.
- **TCR-T** — engineered TCR (instead of CAR).
  Adaptimmune Tecelra (afami-cel) approved 2024
  for synovial sarcoma.

## Base editors + prime editors

Refined CRISPR variants with single-nucleotide
precision + no double-strand-break:

- **Base editors (BE)** (Liu lab) — Cas9 nickase fused
  to a deaminase.  Cytidine BE: C→T (CBE), Adenine
  BE: A→G (ABE).
- **Prime editors (PE)** — Cas9 nickase fused to
  reverse transcriptase + an extended pegRNA encoding
  the desired edit.  Can do all 12 base substitutions
  + small insertions / deletions.

Clinical:
- **Verve VERVE-101 / VERVE-102** — in vivo ABE
  knock-out of PCSK9 for familial hypercholesterolaemia.
  Lipid nanoparticle delivery.
- **Beam BEAM-101** — CBE editing HBG promoter to
  reactivate fetal hemoglobin in SCD.  Ex vivo HSC
  editing.
- **Beam BEAM-201** — quadruple-BE T-cell editing
  for relapsed/refractory leukaemia.
- **Prime Medicine PM359** — chronic granulomatous
  disease ex vivo HSC editing.

## Antisense oligonucleotides + siRNA

Short modified oligonucleotides that bind RNA
sequence-specifically:

### ASOs

- **Mipomersen** — apoB ASO (withdrawn).
- **Inotersen** — TTR ASO for hereditary ATTR.
- **Tegsedi + Wainua (eplontersen)** — TTR ASOs.
- **Spinraza (nusinersen)** — SMN2 splice-modulating
  ASO for SMA; intrathecal.
- **Tofersen (Qalsody)** — SOD1 ASO for SOD1-ALS;
  intrathecal.
- **Casimersen, eteplirsen, golodirsen, viltolarsen**
  — DMD exon-skipping ASOs.

### siRNAs (GalNAc-conjugated for liver delivery)

- **Patisiran (Onpattro)** — TTR siRNA in LNP for
  hATTR.
- **Vutrisiran (Amvuttra)** — TTR siRNA, GalNAc-
  conjugated, SC.
- **Lumasiran (Oxlumo)** — HAO1 siRNA for primary
  hyperoxaluria.
- **Inclisiran (Leqvio)** — PCSK9 siRNA; SC every 6
  months for hypercholesterolaemia.
- **Givosiran (Givlaari)** — ALAS1 siRNA for acute
  hepatic porphyria.

## Other emerging modalities

- **Antibody-oligonucleotide conjugates (AOCs)** —
  Avidity AOC1001 + AOC1020 + AOC1044 for muscle
  delivery.
- **Mirror-image / D-amino acid peptides** — protease-
  resistant.
- **Macrocyclic peptides** — Chugai's mid-size
  modality push.
- **Xeno-nucleic acids (XNAs)** — enzymatically-
  resistant.
- **Engineered live biotherapeutics** (Vedanta,
  Seres) — defined microbial consortia.
- **Bacteriophage therapy** — personalised + cocktail
  for MDR infections.
- **CRISPR therapeutics in vivo** beyond the liver —
  Editas, Intellia, Beam pipelines.

## How modalities change pharmacology

Modality choice cascades through every PK / PD /
manufacturing / regulatory parameter:

| Parameter | Small molecule | mAb | mRNA | AAV | CAR-T |
|-----------|---------------|-----|------|-----|-------|
| Half-life | Hours-days | Days-weeks | Days (protein) | Years | "Lifelong" cells |
| Dosing freq. | Daily | Weeks-months | Weeks-months | Once | Once |
| Route | Oral / IV | IV / SC | IM / IV | IV / local | IV |
| Cost / treatment | $1-100 K | $50-250 K | $100-2 000 | $1-3.5 M | $400-500 K |
| Manufacturing | Bulk chem | Cell culture | IVT + LNP | Cell culture + ultracentrif. | Patient-specific |
| Re-dosable | Yes | Yes | Yes | No | Possible 2nd-dose |

Modern pharmacology requires fluency across all of
these; the discovery + development organisation that
masters multi-modality is the one that can pursue
the right molecule for each biological problem.

## Try it in the app

- **OrgChem → Macromolecules → Proteins** — fetch
  PCSK9, BCMA, CD19 + study domain organisation.
- **Window → Pharmacology Studio → Drug classes** —
  PROTAC, mRNA-vaccine, CAR-T, AAV, ASO classes
  (catalogue continues to grow).
- **Window → Cell Biology Studio → Signalling** —
  pathway context for the targets these modalities
  address.

This concludes the **PH-3.0 tutorial expansion**.

Next sibling: **Microbiology** — your tour through
microbial diversity + antibiotics + vaccines + the
microbiome + emerging infections.
