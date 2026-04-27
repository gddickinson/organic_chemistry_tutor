# Receptor tyrosine kinases + JAK-STAT

GPCRs are the largest receptor superfamily but **receptor
tyrosine kinases** (RTKs) carry the bulk of growth-factor
signalling — and JAK-STAT is the single-pass-receptor
machinery for cytokines. Both are major oncology + immunology
targets.

## RTK architecture

Single-pass type-I transmembrane receptors with three
domains:

- **Extracellular ligand-binding domain** — Ig-like
  domains (EGFR family) or cysteine-rich domains
  (insulin receptor, IGF-1R).
- **Single transmembrane helix**.
- **Intracellular tyrosine kinase domain** + C-terminal
  tail studded with autophosphorylation sites.

## Activation by dimerisation

Most RTKs activate by ligand-induced dimerisation:

1. **Ligand binding** brings two receptor monomers
   together (or stabilises a pre-formed inactive dimer in
   the active conformation).
2. **Dimer trans-autophosphorylation** — each kinase
   domain phosphorylates the other on activation-loop +
   C-terminal tyrosines.
3. **C-terminal phosphotyrosines** become docking sites
   for SH2- and PTB-domain-containing adaptor proteins
   (GRB2, SHC, p85 PI3K, PLCγ).
4. **Adaptor recruitment** activates Ras-MAPK + PI3K-Akt
   + PLCγ-PKC + STAT cascades downstream.

Insulin + IGF-1 receptors are an exception — they're
**constitutive (α2β2) heterotetramers** held by disulfide
bonds. Insulin binding causes a conformational change that
trans-activates the kinase domains without bringing new
monomers together.

## RTK families

About 60 human RTKs in 20 families. Some major ones:

- **ErbB family**: EGFR (HER1), HER2, HER3, HER4 — drive
  epithelial proliferation; EGFR mutations + HER2
  amplification are major lung + breast cancer drivers.
- **VEGFR family**: VEGFR1/2/3 — endothelial; VEGFR2 is
  the angiogenesis driver, target of bevacizumab + the
  "-anib" TKIs.
- **FGFR family**: FGFR1-4 — broad developmental + cancer
  roles.
- **PDGFR family**: PDGFRα/β + KIT + FLT3 + CSF1R — KIT
  drives GIST + mastocytosis (imatinib); FLT3 drives AML.
- **Insulin / IGF-1 receptor family** — metabolism + growth.
- **MET / RON** — wound healing + invasion; MET
  amplification drives gastric cancer + EGFR-TKI
  resistance in NSCLC.
- **TRKs (NTRK1/2/3)** — neurotrophic; NTRK fusions are
  pan-cancer targets (larotrectinib, entrectinib).
- **RET** — thyroid + lung (selpercatinib, pralsetinib for
  RET-altered cancers).

## RTK inhibitors

Two strategies:

- **Antibody therapeutics** — bind the extracellular
  domain + block ligand engagement (cetuximab anti-EGFR,
  trastuzumab anti-HER2, bevacizumab anti-VEGF).
- **Small-molecule TKIs** — bind the intracellular ATP
  pocket of the kinase domain. Variants:
  - Type-I (ATP-competitive, active-DFG-in conformation
    — gefitinib, erlotinib).
  - Type-II (DFG-out conformation — imatinib, sorafenib).
  - Type-III (allosteric — trametinib for MEK).
  - Covalent (osimertinib, afatinib — react with a
    cysteine in the ATP pocket).

## JAK-STAT — the cytokine receptor pathway

Cytokine receptors look superficially like RTKs but
**don't have intrinsic kinase activity**. Instead they
bind constitutively to a JAK kinase (JAK1, JAK2, JAK3, or
TYK2) on their cytoplasmic tail.

Pathway:

1. Cytokine binds — receptor dimerises (or trimerises for
   IL-2-family receptors).
2. Receptor-associated JAKs come into proximity, trans-
   phosphorylate each other.
3. Activated JAKs phosphorylate the receptor's
   cytoplasmic tail.
4. Phosphorylated tail recruits + JAK phosphorylates
   STAT proteins (signal transducers + activators of
   transcription).
5. Phosphorylated STAT dimerises (via SH2-pY interactions),
   translocates to nucleus, drives gene expression.

Key cytokine families:

- **Type-I cytokines** (interleukins, GH, EPO, TPO,
  G-CSF, leptin) — JAK1/2/3 + STAT5 dominant.
- **Type-II cytokines** (interferons IFN-α/β/γ, IL-10
  family) — JAK1 + TYK2 + STAT1/3.

## JAK inhibitors

JAK1/2 inhibitors (ruxolitinib for myelofibrosis +
polycythemia vera; baricitinib + tofacitinib + upadacitinib
for rheumatoid arthritis + IBD; abrocitinib for atopic
dermatitis) are a major modern drug class.

Class-wide warnings: VTE + cardiovascular events + serious
infections + malignancy → black-box labelling.

## Why this matters

- Most growth-factor signalling = RTK-MAPK + RTK-PI3K-Akt.
- Most cytokine signalling = JAK-STAT.
- Most modern oncology = TKI inhibition (imatinib was the
  first, 2001).
- Most modern auto-immunity therapy = JAKi or anti-cytokine
  biologic.

## Try it in the app

- **Cell Bio → Signalling** — `mapk-erk`, `pi3k-akt-mtor`,
  `jak-stat`, `egfr-ras-raf`, `insulin` entries.
- **Pharm → Receptors** — `egfr`, `her2`, `vegfr2`,
  `insulin-receptor` entries.
- **Pharm → Drug classes** — `kinase-inhibitors` covers
  the TKI + JAKi families.
- **Biochem → Enzymes** — `egfr-tk` entry.

Next: **Apoptosis + cell death pathways**.
