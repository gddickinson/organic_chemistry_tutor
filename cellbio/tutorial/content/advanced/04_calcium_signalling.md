# Calcium signalling

Calcium is the most-versatile intracellular second
messenger.  Cells maintain an enormous Ca²⁺
gradient (cytosol ~ 100 nM vs extracellular ~ 1-2
mM) + exploit it for fast, spatially-precise
signalling that controls fertilisation, contraction,
secretion, gene expression, neurotransmission,
proliferation, and cell death.

## The fundamental gradient

Resting cytosolic [Ca²⁺] ~ 100 nM is maintained
against:
- ECF [Ca²⁺] ~ 1-2 mM (10 000-fold gradient).
- ER [Ca²⁺] ~ 100-500 µM (~ 1 000-fold internal
  gradient).
- Mitochondrial [Ca²⁺] ~ 100 nM at rest but
  briefly micromolar during signalling.

The energy cost of this maintenance is enormous —
ATP-driven SERCA, PMCA, NCX, and MCU consume a
substantial fraction of cellular ATP at rest.

## Channels + transporters

### PM Ca²⁺ entry

- **L-type voltage-gated Ca²⁺ channels (Cav1.x)**
  — depolarisation-triggered; cardiac + smooth
  muscle + endocrine secretion + skeletal-muscle
  ECC; targeted by DHP CCBs (amlodipine,
  nifedipine).
- **N-type, P/Q-type, R-type (Cav2.1-3)** —
  neuronal; neurotransmitter release.
- **T-type (Cav3.1-3.3)** — pacemaker.
- **Ligand-gated** — NMDA receptors, nAChR,
  P2X, 5-HT3 (Ca²⁺-permeable).
- **TRP channels** — TRPC, TRPV, TRPM, TRPP,
  TRPML; varied gating (mechanical, thermal,
  ligand).
- **STIM-Orai (CRAC channels)** — store-operated
  Ca²⁺ entry (SOCE; below).
- **Piezo1 / Piezo2** — mechanically gated
  cation; some Ca²⁺ permeability.

### PM Ca²⁺ efflux

- **PMCA (plasma-membrane Ca²⁺-ATPase)** — high-
  affinity, low-capacity; pumps 1 Ca²⁺ per ATP;
  4 isoforms (PMCA1-4).
- **NCX (Na⁺/Ca²⁺ exchanger)** — low-affinity,
  high-capacity; exchanges 3 Na⁺ for 1 Ca²⁺;
  primarily pumps Ca²⁺ OUT (reverses under
  high cytosolic Na⁺); cardiac repolarisation.
- **NCKX** — Na⁺ + K⁺ + Ca²⁺ exchanger; retinal
  + neuronal.

### ER Ca²⁺ release

- **IP3R (inositol-1,4,5-trisphosphate receptor)**
  — IP3R1, IP3R2, IP3R3.  Tetrameric.  Activated
  by IP3 (PLC product).  Modulated by Ca²⁺ itself
  (biphasic — low Ca²⁺ activates, high Ca²⁺
  inhibits → bell-shaped curve).  Drives Ca²⁺
  oscillations.
- **RyR (ryanodine receptor)** — RyR1 (skeletal
  muscle), RyR2 (cardiac), RyR3 (brain + smooth
  muscle).  Tetrameric.  Activated by Ca²⁺
  (CICR — Ca²⁺-induced Ca²⁺ release).  RyR1
  mutations → malignant hyperthermia + central-
  core disease; RyR2 → CPVT.
- **TPC (two-pore channels)** — endolysosomal
  Ca²⁺; NAADP-activated.

### ER Ca²⁺ uptake

- **SERCA (sarco/endoplasmic-reticulum Ca²⁺-
  ATPase)** — refills ER Ca²⁺ stores after
  release.  3 isoforms (SERCA1 muscle, SERCA2
  cardiac + ubiquitous, SERCA3 specialised).
  Inhibited by **thapsigargin** (research tool;
  triggers ER stress).
- Active research: **istaroxime** (SERCA2a
  activator + Na/K-ATPase inhibitor; heart-failure
  trials).

### Mitochondrial Ca²⁺ handling

- **MCU (mitochondrial Ca²⁺ uniporter)** + **MICU1
  / MICU2 / MICU3 / EMRE / MCUb** complex.  Low-
  affinity; activates only when mitochondria-ER
  contact sites generate local high-[Ca²⁺]
  microdomains.
- **NCLX (mitochondrial Na⁺/Ca²⁺ exchanger)** —
  mitochondrial Ca²⁺ extrusion.
- **mPTP (mitochondrial permeability transition
  pore)** — opens at very high mitochondrial
  Ca²⁺ + oxidative stress; necrotic + apoptotic
  cell death pathway.

Mitochondrial Ca²⁺ uptake serves two roles:
- **Buffering** — sequesters cytosolic Ca²⁺
  spikes.
- **Signalling** — activates 3 mitochondrial
  matrix dehydrogenases (PDH, IDH, αKGDH) →
  metabolic upregulation matched to Ca²⁺-driven
  energy demand.

## IP3-mediated Ca²⁺ release

Canonical second-messenger pathway:

1. GPCR (Gαq) or RTK → PLCβ or PLCγ activation.
2. PLC hydrolyses PI(4,5)P₂ → IP3 + DAG.
3. IP3 diffuses + binds IP3R on ER membrane.
4. IP3R opens → Ca²⁺ release into cytosol.
5. Ca²⁺ rise activates downstream effectors
   (calmodulin, CaMKII, calcineurin, PKC, etc.).
6. SERCA pumps Ca²⁺ back into ER; PMCA + NCX
   extrudes across PM.

Repeated stimulation generates Ca²⁺ OSCILLATIONS
(period seconds-minutes), encoding signal
intensity in oscillation FREQUENCY (frequency-
modulated coding).

## Store-operated Ca²⁺ entry (SOCE)

When ER Ca²⁺ is depleted, the cell signals to PM:

1. **STIM1 / STIM2** — ER-membrane proteins with
   luminal Ca²⁺-binding EF-hand domains.
2. ER Ca²⁺ depletion → STIM dissociates from
   Ca²⁺ → conformational change.
3. STIM oligomerises + translocates to ER-PM
   contact sites.
4. STIM binds **Orai1 / Orai2 / Orai3** PM
   channels.
5. CRAC (Ca²⁺-release-activated Ca²⁺) channels
   open → highly Ca²⁺-selective influx.

CRAC current is essential for:
- T-cell activation (NFAT signalling).
- Mast-cell degranulation.
- Many secretory + proliferation responses.

Orai1 + STIM1 mutations cause severe combined
immunodeficiency (SCID) + immunodeficiency-related
syndromes.

CRAC inhibitors (CM-128, RP-3128) in trials for
autoimmune disease.

## Ca²⁺-binding effectors

### Calmodulin (CaM)

- 16 kDa; 4 EF-hand Ca²⁺-binding sites.
- Ubiquitous Ca²⁺ sensor.
- Conformational change on Ca²⁺ binding allows
  binding to ~ 300+ target proteins via "IQ
  motifs" or other sequences.
- Targets include CaMKII, calcineurin, MLCK,
  NOS, adenylate cyclase, CaMKK, IP3R + RyR
  themselves.

### CaMKII

- Dodecameric kinase activated by Ca²⁺-CaM.
- Auto-phosphorylates → Ca²⁺-CaM-independent
  activity → "memory" of Ca²⁺ pulses.
- LTP induction in hippocampal CA1.
- Cardiac CaMKIIδ — heart-failure pathology
  + arrhythmia.

### Calcineurin (PP2B)

- Ca²⁺-CaM-activated serine/threonine phosphatase.
- Dephosphorylates NFAT → nuclear translocation
  → T-cell-receptor-driven gene expression.
- Inhibited by **cyclosporine** (binds cyclophilin)
  + **tacrolimus** (binds FKBP12); drugs target
  the cyclophilin-cyclosporine + FKBP-tacrolimus
  complex against calcineurin → T-cell
  immunosuppression.

### Other Ca²⁺ sensors

- **Synaptotagmin** — fast Ca²⁺ sensor for
  synaptic-vesicle exocytosis.
- **Calbindin / parvalbumin / calretinin** — Ca²⁺
  buffers in specific neurons (interneuron
  markers).
- **Calsequestrin** — high-capacity Ca²⁺-binding
  protein in SR lumen.
- **Calreticulin / calnexin** — ER Ca²⁺ buffers
  + glycoprotein QC chaperones.
- **S100 family** — small Ca²⁺-binding proteins
  with diverse roles + cancer-marker (S100B
  melanoma).
- **Recoverin / GCAPs** — phototransduction.

## Ca²⁺ in specific contexts

### Excitation-contraction coupling (ECC)

- **Skeletal muscle** — DHP receptor (Cav1.1)
  in T-tubule mechanically coupled to RyR1 in
  SR; voltage-driven RyR1 opening (no Ca²⁺
  trigger needed).
- **Cardiac muscle** — Cav1.2 Ca²⁺ entry triggers
  RyR2 via CICR (Ca²⁺-induced Ca²⁺ release).
- **Smooth muscle** — Cav1.2 + IP3R Ca²⁺ release;
  Ca²⁺-CaM-MLCK phosphorylation of myosin light
  chain → contraction.

### Synaptic transmission

- AP arrives at presynaptic terminal → opens
  Cav2.1/2.2.
- Local microdomain Ca²⁺ rise (10-100 µM
  briefly).
- Synaptotagmin senses Ca²⁺ → synchronises
  SNARE-mediated synaptic-vesicle fusion in
  < 1 ms.
- Botulinum + tetanus toxins cleave SNAREs
  (covered in **CB-3.0 graduate "Membrane
  trafficking"**).

### Fertilisation

- Sperm-egg fusion triggers a Ca²⁺ wave across
  the egg cytosol (PLCζ-IP3-IP3R).
- Cortical-granule exocytosis blocks polyspermy.
- Egg activation + zygotic gene-expression
  programme.

### Apoptosis

- Sustained / excessive Ca²⁺ overload triggers
  mPTP opening + intrinsic apoptosis.
- Calcineurin dephosphorylates BAD → BAD-BCL-XL
  binding shifts pro-apoptotic.

### Gene expression

- NFAT (calcineurin substrate) → T-cell + immune
  + cardiac hypertrophy gene programmes.
- CREB phosphorylation by CaMK / CaMKK / CaMKIV
  → activity-dependent transcription in neurons.
- DREAM / KChIP3 — Ca²⁺-dependent transcriptional
  repressor.

### Cell migration

- Spatially restricted Ca²⁺ pulses at the leading
  edge regulate Rho-GTPase + focal-adhesion
  dynamics.

## Pharmacology

| Drug class | Target | Use |
|------------|--------|-----|
| Dihydropyridine CCB | Cav1.x | Hypertension, angina |
| Non-DHP CCB (verapamil, diltiazem) | Cav1.2 | Hypertension, AVNRT |
| Ziconotide | Cav2.2 (N-type) | Chronic pain (intrathecal) |
| Ethosuximide | Cav3 (T-type) | Absence seizures |
| Ryanodine (research) | RyR | Tool compound; toxic |
| Dantrolene | RyR1 | Malignant hyperthermia |
| Thapsigargin (research) | SERCA | Tool compound |
| Cyclosporine, tacrolimus | Calcineurin | Immunosuppression |
| BAPTA / EGTA / EDTA | Ca²⁺ chelators | Research; clinical Ca²⁺-binding (EDTA in lead poisoning) |
| Bisphosphonates | Bone Ca²⁺ resorption | Osteoporosis |
| Calcimimetics (cinacalcet) | CaSR PAM | Secondary hyperparathyroidism |
| Levosimendan | Troponin C Ca²⁺-sensitiser + KATP | Acute heart failure |

## Imaging Ca²⁺

- **Chemical indicators** — Fura-2, Indo-1,
  Fluo-4, Calcium Green (ratiometric vs single-
  wavelength).
- **GECIs (genetically encoded)** — GCaMP1 →
  GCaMP3 → GCaMP6s/m/f → GCaMP7 → GCaMP8
  (Janelia jGCaMP8s/m/f variants); RCaMP +
  R-GECO red-shifted alternatives; jRGECO1a,
  jGCaMP8.
- **Mitochondrial- + ER-targeted variants** —
  mtGCaMP, ER-G-CEPIA, R-CEPIA.
- **Sub-cellular targeting** via signal peptides
  + membrane-tethering motifs.
- **Two-photon Ca²⁺ imaging** — standard for
  in-vivo neural-circuit recording in mouse.
  See **AB-3.0 graduate "Neuroscience frontiers"**.

## Cross-link

For ECC + cardiac arrhythmias + channelopathies,
see the **CB-4.0 intermediate "Ion channels +
electrical signalling" lesson** (last).  For
Ca²⁺ in fertilisation + early development, see
**AB-3.0 beginner "How animals develop"**.  For
Ca²⁺ in plant signalling, see **BT-3.0
intermediate "Phytohormones in depth"** (Ca²⁺ +
CaM-CDPK + CBL-CIPK pathways).

## Try it in the app

- **Window → Pharmacology Studio → Drug classes** —
  CCBs + ryanodine modulators + immunosuppressants.
- **Window → Cell Biology Studio → Cell cycle
  tab** — Ca²⁺-dependent CaMKII / calcineurin /
  CDK regulators.
- **Window → Animal Biology Studio → Organ
  systems** — cardiac + skeletal muscle ECC
  context.

Next: **Cell migration + cancer invasion**.
