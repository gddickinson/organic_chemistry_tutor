# Cancer signalling networks — putting it together

Cancer is a disease of dysregulated signalling. Hanahan +
Weinberg's Hallmarks of Cancer (2000, updated 2011, 2022)
gave us a checklist of acquired capabilities every tumour
shares. Each hallmark maps to specific signalling
pathways — the same ones we've covered in earlier lessons.

## The hallmarks + their signalling drivers

| Hallmark | Major pathway(s) | Frequent driver mutations |
|----------|------------------|---------------------------|
| Sustained proliferative signalling | RTK-RAS-RAF-ERK; PI3K-Akt-mTOR | EGFR, KRAS, BRAF, PIK3CA |
| Evading growth suppressors | Rb, p53 | RB1, TP53, CDKN2A |
| Resisting cell death | Apoptosis pathways | BCL-2 (lymphoma), TP53 (most) |
| Replicative immortality | Telomerase | TERT promoter mutations |
| Inducing angiogenesis | VEGF / VEGFR | HIF-1α stabilisation, VEGF overexpression |
| Activating invasion + metastasis | EMT, Wnt, TGF-β | E-cadherin loss, SNAIL/SLUG |
| Reprogramming energy metabolism | Warburg, mTOR | LDH, glucose transporters |
| Avoiding immune destruction | PD-1/PD-L1, IDO | PD-L1 overexpression |
| Tumour-promoting inflammation | NF-κB, STAT3 | constitutive STAT3 in many |
| Genome instability + mutation | DDR | BRCA1/2, MMR, MGMT |

The "next-generation" hallmarks (2011 + 2022) added
deregulating cellular energetics, avoiding immune
destruction, unlocking phenotypic plasticity, non-
mutational epigenetic reprogramming, polymorphic
microbiomes, senescent cells.

## Why integration matters

Single-pathway thinking misleads. Real tumour signalling
is a network with massive cross-talk:

- RAS activates BOTH MAPK + PI3K (parallel, not serial).
- Cyclin D is a target of MAPK + Akt + Wnt simultaneously.
- p53 is regulated by MDM2 + ATM + ATR + ARF + p14ARF.
- mTORC1 integrates PI3K + amino acids + ATP + growth
  factors.

This redundancy explains why monotherapy fails:

- BRAF inhibitor monotherapy in melanoma → resistance via
  MEK-bypass + Ras-feedback re-activation → BRAF + MEK
  inhibitor combinations now standard.
- EGFR inhibitor monotherapy in NSCLC → resistance via
  T790M + MET amplification + small-cell transformation.
- Endocrine therapy in ER+ breast → resistance via PI3K
  activation → CDK4/6 + endocrine combinations.

Understanding the network gives you predictive resistance
mechanisms + rational combination strategies.

## RAS — the most-mutated oncogene

Three RAS isoforms (KRAS, NRAS, HRAS); ~ 30 % of all
human cancers carry an activating mutation:

- KRAS — most-frequently mutated (pancreatic 90 %, lung
  30 %, colorectal 40 %).
- NRAS — melanoma 20 %, AML.
- HRAS — bladder, head + neck.

Mutations cluster at G12, G13, Q61 — residues critical for
GTP hydrolysis. Mutation locks Ras in the GTP-bound active
state.

For decades RAS was considered "undruggable" — a smooth
GTPase pocket without a small-molecule binding site.
Then **sotorasib** (2021, FDA) + **adagrasib** (2022)
proved KRAS-G12C can be drugged via a covalent allosteric
pocket exposed only in the GDP-bound state. Only G12C is
currently druggable; pan-KRAS + KRAS-G12D inhibitors are
in trials.

## p53 — the guardian of the genome

p53 is the most-mutated tumour suppressor (~ 50 % of all
tumours). It sits at the intersection of:

- DNA damage response (ATM/ATR → p53 stabilisation).
- Cell-cycle arrest (p21 induction).
- Apoptosis (PUMA, NOXA, BAX, FAS).
- Senescence (p16, p21).
- Metabolism (TIGAR, GLS2, SCO2).

Most p53 mutations are missense in the DNA-binding domain
(R175H, R248W, R273H — the classic "hotspots") that
abolish target-gene transactivation. Some "GOF" mutants
gain new oncogenic functions independent of WT p53 loss.

Therapeutic strategies:

- **Restore WT p53 function in mutant tumours** — APR-246
  (eprenetapopt, PRIMA-1MET) refolds Y220C + R175H to a
  WT-like state. FDA submission 2024 for TP53-mutant
  MDS/AML.
- **MDM2 inhibitors** in WT-p53 tumours — idasanutlin,
  milademetan. Block MDM2-mediated p53 degradation +
  re-activate p53.
- **Synthetic lethality** with p53 loss — Wee1
  inhibition, ATR inhibition exploit checkpoint
  dependencies in p53-mutant cells.

## The PI3K-Akt-mTOR axis

The other major proliferative + survival pathway:

- **PI3K** (class I) — generates PIP3 from PIP2.
  PIK3CA mutations (E542K, E545K, H1047R) are very
  common in ER+ breast cancer.
- **PTEN** — opposes PI3K (PIP3 → PIP2). Loss is the
  major PI3K-pathway-activating event in many cancers.
- **Akt** — recruited to PIP3, phosphorylated by PDK1 +
  mTORC2, drives survival (BAD, BIM, FoxO) + growth +
  glucose uptake.
- **mTORC1** — protein synthesis + ribosome biogenesis.
- **mTORC2** — Akt activation + cytoskeleton.

Drugs:

- **PI3K inhibitors**: alpelisib (PIK3CA-mutant breast),
  copanlisib (FL), idelalisib (CLL).
- **Akt inhibitors**: capivasertib (FDA 2023, AKT1-mutant
  + PIK3CA-mutant breast).
- **mTOR inhibitors**: rapalogs (sirolimus, everolimus,
  temsirolimus); next-gen TORKinibs (sapanisertib).

## The immune-checkpoint axis

The 2018 Nobel-winning revolution: PD-1 + CTLA-4 + LAG-3
+ TIGIT inhibition unleashes existing T-cell anti-tumour
responses.

- **Anti-PD-1**: nivolumab, pembrolizumab, cemiplimab.
- **Anti-PD-L1**: atezolizumab, durvalumab, avelumab.
- **Anti-CTLA-4**: ipilimumab.
- **Anti-LAG-3**: relatlimab (in combo with nivolumab).

Hallmark transformation: 5 % long-term survival in
metastatic melanoma (pre-2011) → 50 % long-term survival
(combo ipi-nivo).

## Future directions

- **ADCs** (antibody-drug conjugates) — targeted
  cytotoxin delivery; trastuzumab-deruxtecan for HER2-
  expressing breast + gastric.
- **PROTACs / molecular glues** — degrade rather than
  inhibit; thalidomide-CRBN-IMiDs are the prototype;
  ARV-110 (BAVDEGALUTAMIDE) targets AR for prostate
  cancer.
- **CAR-T + bispecific T-cell engagers** — re-direct T
  cells to surface antigens.
- **Synthetic-lethality 2.0** — beyond PARP/BRCA;
  exploiting Werner helicase synthetic lethality with
  MSI-high cancers, MAT2A in MTAP-deleted tumours, etc.

## Try it in the app

- **Cell Bio → Signalling** — `mapk-erk`, `pi3k-akt-mtor`,
  `wnt-beta-catenin`, `p53`, `intrinsic-apoptosis`,
  `egfr-ras-raf` entries.
- **Cell Bio → Cell cycle** — full Phase CB-2.0
  catalogue.
- **Pharm → Drug classes** — `kinase-inhibitors`,
  `checkpoint-inhibitors` entries.
- **Pharm → Receptors** — `egfr`, `her2`, `vegfr2`
  entries.

Next: **Quantitative signalling — the field's modern frontier**.
