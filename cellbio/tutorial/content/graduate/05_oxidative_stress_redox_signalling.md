# Oxidative stress + redox signalling

For decades reactive oxygen species (ROS) were
treated as purely destructive — by-products to be
neutralised.  The modern view is more nuanced:
controlled ROS production is a bona fide
signalling mechanism that regulates proliferation,
differentiation, immune responses, and metabolism.
Dysregulation of redox balance underlies ageing
+ cancer + neurodegeneration + cardiovascular
disease.

## The major ROS

| Species | Source | Lifetime | Reactivity |
|---------|--------|----------|------------|
| O₂⁻ (superoxide) | ETC complex I + III leak; NADPH oxidase | µs | Moderate; SOD substrate |
| H₂O₂ | SOD + monoamine oxidase + DAO + NOX2-derived O₂⁻ | s-min | Low (selective; signalling-grade) |
| ·OH (hydroxyl radical) | Fenton reaction (H₂O₂ + Fe²⁺) | ns | Extreme; non-specific damage |
| ¹O₂ (singlet oxygen) | Photosensitisers; some enzymes | µs | High |
| ONOO⁻ (peroxynitrite) | NO + O₂⁻ | s | Very high; protein nitration |
| HOCl (hypochlorous acid) | MPO in neutrophil phagosomes | ms | Bactericidal |
| RNS (reactive nitrogen) | iNOS + nNOS + eNOS + ONOO⁻ | s | Mixed |

H₂O₂ is the redox-signalling currency of cells —
relatively stable, membrane-permeable (especially
through aquaporin-3 + AQP8), reactive primarily
with low-pKa cysteine thiols (Cys-SH → Cys-SOH
→ Cys-SO₂H → Cys-SO₃H sequence).

## ROS sources

### Mitochondria

- ETC complexes I + III leak ~ 0.1-2 % of electron
  flow as O₂⁻ (matrix-side from CI; either side
  from CIII).
- Highest at States 4 (resting, no ADP) +
  reverse electron flow conditions.
- Increases with damaged ETC, hypoxia /
  reperfusion, mtDNA mutations.

### NADPH oxidases (NOX family)

- 7 isoforms in humans (NOX1-5, DUOX1, DUOX2).
- NOX2 (gp91phox) — phagocyte respiratory
  burst; CGD if defective.
- NOX1, NOX4 — vascular smooth muscle, kidney,
  lung; cardiovascular ROS.
- DUOX1 + DUOX2 — thyroid (H₂O₂ for thyroid-
  hormone synthesis); intestinal mucosa (innate
  defence).

### Other sources

- Peroxisomes — fatty-acid β-oxidation.
- ER (CYPs, P450 family).
- Xanthine oxidase (purine catabolism).
- Monoamine oxidases (MAO-A + MAO-B in brain).
- Cyclooxygenase + lipoxygenase.

## Antioxidant defences

### Enzymatic

- **Superoxide dismutases (SODs)** —
  - SOD1 (Cu/Zn; cytosolic + nuclear; mutated
    in familial ALS).
  - SOD2 (Mn; mitochondrial matrix; deletion
    embryonic lethal).
  - SOD3 (Cu/Zn; extracellular).
- **Catalase** — peroxisomal H₂O₂ → H₂O + O₂;
  high-capacity, low-affinity.
- **Glutathione peroxidases (GPx1-8)** —
  selenoproteins; H₂O₂ + GSH → H₂O + GSSG;
  high-affinity.
- **Peroxiredoxins (Prx1-6)** — Cys-thiol-based
  H₂O₂ reduction; high-abundance + selectively
  high-affinity for H₂O₂; central in redox
  signalling.
- **Thioredoxin (Trx) + thioredoxin reductase
  (TrxR)** — recycles oxidised Prx + protein
  disulfides; selenoenzyme TrxR.
- **Glutaredoxin (Grx)** — protein deglutathiony-
  lation; thiol-disulfide remodelling.
- **Sulfiredoxin (Srx)** — reduces Cys-SO₂H
  (sulfinic acid) of Prx back to Cys-SH;
  Cys-SO₃H (sulfonic acid) is irreversible.

### Non-enzymatic

- **Glutathione (GSH)** — mM in cytosol; γ-Glu-
  Cys-Gly tripeptide; central thiol redox buffer.
  GSSG / GSH ratio is the major intracellular
  redox indicator.
- **Vitamin C (ascorbate)** — water-soluble
  electron donor.
- **Vitamin E (α-tocopherol)** — lipid-soluble;
  membrane antioxidant; chain-breaks lipid
  peroxidation.
- **Coenzyme Q (ubiquinone / CoQ10)** — mitochondrial
  + cytoplasmic.
- **Carotenoids** — singlet-oxygen quenchers.
- **Uric acid** — major plasma antioxidant.
- **Flavonoids + polyphenols** — dietary; varied
  potencies.

## H₂O₂ signalling

### Targets

H₂O₂ selectively oxidises low-pKa cysteine thiols
(pKa < 7 vs typical ~ 8.5) → Cys-SO⁻ → Cys-SOH →
intramolecular or intermolecular disulfide → Cys-
S-S-protein.  These oxidations are reversible,
specific, and regulatory.

Key targets:
- **Tyrosine phosphatases (PTP1B, PTEN, SHP1/2,
  CDC25)** — Cys at active site; oxidation
  inactivates → enhances RTK + PI3K signalling.
  H₂O₂ pulse extends growth-factor signalling.
- **Kinases** — ASK1 (Trx1 dissociation),
  Src-family, JNK, EGFR.
- **Transcription factors** — KEAP1-NRF2 (key
  ROS response — below); NF-κB; Foxo;
  HSF1; AP-1.
- **Channels + pumps** — RyR2, IP3R, NCX,
  SERCA, Cav, KATP.
- **Metabolic enzymes** — GAPDH (Cys-SH at
  active site sensitive to oxidation;
  metabolic redirection under stress).

### Spatial + temporal organisation

H₂O₂ signalling is highly compartmentalised:
- Local generation by NOX at signalling
  microdomains (PM, endosomes, focal adhesions).
- Local antioxidants tune the response.
- Aquaporin-3 / 8-mediated H₂O₂ permeation
  through PM.

Genetically encoded H₂O₂ sensors:
- **HyPer family** (HyPer3, HyPer7) — circularly
  permuted YFP fused to OxyR thiol switch.
- **roGFP / roGFP2-Orp1** — reduction-oxidation
  GFP variants.
- Subcellular targeting (mito-roGFP, cyto-HyPer,
  ER-HyPer) for compartment-specific imaging.

## The KEAP1-NRF2 pathway

The master cellular response to oxidative +
electrophilic stress.

### At rest

- **NRF2** (NFE2L2) is constitutively translated
  but rapidly degraded.
- **KEAP1** is a Cul3-dependent E3 ligase
  substrate-adapter that ubiquitinates NRF2
  → proteasomal degradation.
- KEAP1 dimer holds NRF2 via two ETGE + DLG
  motifs.

### Under stress

- Reactive cysteines on KEAP1 (Cys151 + Cys273
  + Cys288) get oxidised or alkylated.
- Conformational change releases NRF2
  ubiquitination (NRF2 still binds KEAP1, but
  isn't ubiquitinated — "hinge + latch" model).
- Newly synthesised NRF2 escapes degradation
  + accumulates.
- Translocates to nucleus + binds Maf cofactors
  + binds **antioxidant response elements
  (AREs)** on target gene promoters.
- Upregulates ~ 200 cytoprotective genes:
  - GCL (γ-glutamyl-cysteine ligase) — GSH
    biosynthesis.
  - GST (glutathione S-transferase isoforms).
  - NQO1 (NAD(P)H quinone oxidoreductase).
  - HMOX1 (heme oxygenase 1).
  - Trx + TrxR + Prx + Srx.
  - Phase-II conjugation enzymes (UGTs, SULTs).
  - Phase-III efflux (MRP / MDR) transporters.

### Drugs

- **Dimethyl fumarate (Tecfidera)** — Michael
  acceptor; alkylates KEAP1 Cys → activates
  NRF2; relapsing-remitting MS, psoriasis.
- **Bardoxolone methyl + omaveloxolone (Skyclarys,
  2023)** — synthetic triterpenoids; activate
  NRF2; CKD trials + Friedreich's ataxia
  (omaveloxolone approved).
- **Sulforaphane** (broccoli isothiocyanate) —
  natural NRF2 activator; clinical trials in
  autism + chemoprevention.
- **Curcumin + EGCG** — weak but accessible
  natural NRF2 activators.

In oncology, KEAP1 loss-of-function + NRF2 gain-
of-function mutations are common in lung +
oesophageal cancer + drive resistance to
chemotherapy + radiotherapy.

## Ferroptosis — iron-dependent cell death

Discovered in 2012 (Stockwell + Conrad labs);
distinct from apoptosis + necroptosis +
pyroptosis.

### Mechanism

1. **Iron** (ferrous Fe²⁺) catalyses lipid
   peroxidation via Fenton chemistry on
   polyunsaturated phospholipids (especially
   PE-PUFA).
2. **Lipoxygenases (ALOX15)** + **POR cytochrome
   reductase** also drive PUFA peroxidation.
3. **GPX4 (glutathione peroxidase 4)** is the
   main defence — reduces lipid hydroperoxides
   to lipid alcohols using GSH.
4. **System Xc⁻ (SLC7A11 / SLC3A2)** imports
   cystine for GSH biosynthesis.
5. When GPX4 / system Xc⁻ are inhibited or
   depleted, lipid peroxides accumulate +
   propagate → membrane rupture + cell death.

### FSP1 / CoQ10 axis

- Independent ferroptosis defence: FSP1
  (AIFM2) + CoQ10 (vitamin E-like) trap lipid
  radicals at PM.

### Drugs

- **Erastin + RSL3 + ML162** — ferroptosis
  inducers (research tools); RSL3 covalently
  binds GPX4; erastin inhibits system Xc⁻.
- **Ferrostatin-1 + liproxstatin-1** —
  ferroptosis inhibitors (radical-trapping
  antioxidants).
- **Imidazole ketone erastin (IKE)** + **ML210**
  — improved tool compounds.

### Disease context

- **Tumours** — many cancers depend on system
  Xc⁻ + GPX4 to escape ferroptosis; tumour-
  selective ferroptosis induction is an emerging
  therapeutic strategy.
- **Ischaemia-reperfusion injury** (heart, kidney,
  brain).
- **Neurodegeneration** — dopaminergic neurons
  particularly vulnerable.
- **Doxorubicin cardiotoxicity** — partial
  ferroptotic component.

## Other redox-driven death pathways

- **Pyroptosis** — gasdermin-mediated lytic
  death; inflammasome-driven; release of IL-1β
  + IL-18.
- **Cuproptosis** — copper-dependent death;
  attaches to lipoylated TCA-cycle proteins;
  recently characterised.
- **Necroptosis** — RIPK1 / RIPK3 / MLKL pathway;
  oxidative stress sensitises.

## Mitochondrial ROS + ageing

- Free-radical theory of ageing (Harman 1956)
  posited cumulative oxidative damage as a
  cause of ageing.
- Mostly displaced by more nuanced "mitohormesis"
  + redox-signalling ageing models.
- Antioxidant supplementation has FAILED to
  extend lifespan in most rigorous studies +
  may interfere with adaptive responses
  (exercise, mitochondrial biogenesis).
- mtDNA-mutator mouse + Surf1-knockout +
  Polg-mutator + Sirt3-knockout + Nrf2 KO mice
  all show accelerated ageing, consistent with
  mitochondrial-redox-axis importance.

## Oxidative stress in disease

- **Neurodegeneration** — Parkinson's (substantia
  nigra), Alzheimer's, ALS (SOD1), Huntington's,
  ataxias.
- **Cardiovascular** — atherosclerosis (oxidised
  LDL), hypertension, ischaemia-reperfusion,
  heart failure.
- **Diabetes** — β-cell death + insulin-resistance.
- **Cancer** — both promotes (carcinogenesis,
  proliferation signalling) + suppresses (DNA
  damage, ferroptosis, apoptosis).
- **CGD** (chronic granulomatous disease) —
  NOX2 deficiency → can't generate phagocyte
  ROS → recurrent infections.
- **Inflammatory disease** — RA, IBD, COPD —
  ROS-driven tissue damage.

## Therapeutic strategies

- **Antioxidant supplementation** — mostly
  disappointing in clinical trials (vitamin E,
  vitamin C, β-carotene); occasional benefits
  in specific settings (NAC for paracetamol
  overdose; tafamidis for ATTR amyloidosis;
  edaravone for ALS — though edaravone's
  mechanism is debated).
- **Mitochondrial-targeted antioxidants** —
  MitoQ + MitoVitE + SkQ1; Phase 2-3 in PD,
  septic AKI, cardiac surgery.
- **Nrf2 activators** — DMF (MS), omaveloxolone
  (Friedreich), bardoxolone (CKD trials).
- **Ferroptosis modulators** — emerging
  oncology programmes (GPX4 + SLC7A11 +
  ALOX15 inhibitors).
- **NLRP3-inflammasome inhibitors** — emerging
  (MCC950 / dapansutrile).
- **Reduce mitochondrial ROS leakage** —
  exercise + caloric restriction + intermittent
  fasting + metformin all promote mitohormesis +
  improve antioxidant capacity over the long run.

## Cross-link

For mitochondrial ETC + ATP synthase context, see
**BC-3.0 advanced "Oxidative phosphorylation +
chemiosmosis"**.  For autophagy / mitophagy
defence vs damaged mitochondria, see **CB-4.0
intermediate "Autophagy + UPS"**.  For ferroptosis
in oncology, see **CB-3.0 advanced "Cancer
signalling networks"** + **PH-3.0 graduate
"Modern modalities"**.

## Try it in the app

- **Window → Biochem Studio → Enzymes** — SOD +
  catalase + GPx + Trx + Prx entries.
- **Window → Biochem Studio → Cofactors** —
  glutathione + CoQ10 + Vit C + Vit E + NADPH.
- **Window → Pharmacology Studio → Drug
  classes** — antioxidants + DMF + omaveloxolone
  + N-acetylcysteine + idebenone.
- **Window → Cell Biology Studio → Signalling** —
  Nrf2 / inflammasome / apoptosis pathways.

Next: **Intracellular pH + organelle pH**.
