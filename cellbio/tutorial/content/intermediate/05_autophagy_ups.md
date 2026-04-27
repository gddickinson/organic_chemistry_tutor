# Autophagy + ubiquitin-proteasome system

Cells don't just synthesise proteins + organelles —
they continuously degrade + recycle them too.  Two
major degradation systems handle the bulk of the
job: the ubiquitin-proteasome system (UPS) for
short-lived + soluble proteins, and autophagy for
bulk cytoplasm + organelles + protein aggregates.

## Why protein degradation matters

- **Quality control** — misfolded proteins are
  removed before they aggregate.
- **Regulation** — many regulatory proteins
  (cyclins, p53, NF-κB inhibitors, HIF-1α) are
  controlled by their degradation rates.
- **Signal termination** — receptor + signalling-
  protein turnover ends signal transduction.
- **Adaptation** — turnover lets cells reshape
  proteome in minutes-hours.
- **Immunity** — peptide presentation on MHC
  class I depends on proteasomal degradation.
- **Nutrient recycling** — autophagy feeds amino-
  acid + lipid + nucleotide pools during
  starvation.

## The ubiquitin-proteasome system (UPS)

The 2004 Nobel Prize in Chemistry to **Aaron
Ciechanover, Avram Hershko, + Irwin Rose** for
discovering ubiquitin-mediated proteolysis.

### Ubiquitin

A small (76 aa) highly conserved protein that
covalently tags substrates for degradation +
many other regulatory roles.

The conjugation cascade (E1-E2-E3):

1. **E1** (UBA1, UBA6) — ATP-dependent activation;
   forms thioester ubiquitin~E1.
2. **E2** (~ 35 in humans) — accepts ubiquitin
   from E1; forms thioester ubiquitin~E2.
3. **E3** (~ 600 in humans!) — substrate-specific
   ligase; transfers ubiquitin from E2 onto a
   substrate lysine ε-NH₂.

### E3 ligase families

- **HECT-domain** — accepts Ub on its own active-
  site Cys then transfers; e.g. NEDD4, ITCH,
  Smurf, HUWE1.
- **RING-domain** — scaffolds E2-Ub + substrate;
  e.g. MDM2, BRCA1, CBL, IAPs.
- **U-box** — RING-like; e.g. CHIP.
- **RBR (RING-between-RING)** — RING + HECT
  hybrid; e.g. Parkin, HOIP.

### Cullin-RING ligases (CRLs)

A massive family of multi-subunit RING ligases:
- **Cullin scaffold** (CUL1-5, CUL7, CUL9).
- **RING-box protein** (RBX1/2).
- **Adaptor + substrate-receptor** (variable;
  hundreds of options).
- **SCF (Skp1-Cullin1-F-box)** — CUL1-based;
  F-box protein selects substrate (~ 70 F-box
  proteins; β-TrCP, Skp2, Fbxw7, Fbxl5).
- **VHL** complex (CUL2 + EloB/C + VHL) — degrades
  HIF-α under normoxia.
- **Cullin-3 + BTB** complexes — Keap1-Cul3
  controls Nrf2.
- **APC/C (anaphase-promoting complex /
  cyclosome)** — large RING ligase with Cdc20 or
  Cdh1 activator; controls cyclin + securin
  degradation in mitosis.

### Polyubiquitin chains

The lysine on which ubiquitin chains are extended
determines the signal:
- **K48 chains** — proteasomal degradation
  (canonical).
- **K11 chains** — proteasomal degradation
  (mitotic substrates).
- **K63 chains** — DNA-damage response, NF-κB
  signalling, autophagy, endocytic sorting.
- **K6 chains** — DNA repair (BRCA1).
- **K27, K29, K33** — minor / specialised.
- **M1 / linear chains** — LUBAC ligase; NF-κB
  + immune signalling.
- **Mono-ubiquitin** — endocytosis, histone
  modification (H2A K119, H2B K120), DNA repair.

The "ubiquitin code" — different chain types
recruit different effector proteins.

### The 26S proteasome

A multi-subunit (~ 2.5 MDa) ATP-dependent
protease.

- **20S core particle** — barrel-shaped; α7β7β7α7
  subunit arrangement; β1 (caspase-like), β2
  (trypsin-like), β5 (chymotrypsin-like)
  catalytic threonines.
- **19S regulatory particle** (caps both ends) —
  recognises poly-Ub substrates (Rpn10, Rpn13);
  unfolds them via AAA+ ATPase ring (Rpt1-6);
  removes ubiquitin (Rpn11 deubiquitinase);
  feeds substrate into the 20S core.

Inhibitors:
- **Bortezomib (Velcade)** — first proteasome
  inhibitor approved (2003); multiple myeloma +
  mantle cell lymphoma.
- **Carfilzomib (Kyprolis)** — second-generation;
  irreversible.
- **Ixazomib (Ninlaro)** — oral.

### Deubiquitinases (DUBs)

~ 100 in humans; reverse ubiquitination + edit
chains.

Major classes:
- **USP (ubiquitin-specific protease)** family —
  ~ 60 members; USP7 (HAUSP, regulates p53 +
  MDM2), USP1 (FA pathway), USP14 (proteasome-
  associated).
- **UCH** family.
- **OTU** family.
- **MJD** family.
- **JAMM / MPN+** — Zn-dependent metallo-DUBs;
  Rpn11 (proteasome lid), CSN5 (COP9 signalosome),
  BRCC36 (BRCA1 complex).

DUB inhibitors are emerging anti-cancer drug class
(USP7 inhibitors in trials).

## Targeted protein degradation — modern therapy

The UPS is now exploited therapeutically by
**PROTACs** + **molecular glues**:

- **PROTACs** — bivalent small molecules (target-
  binder + E3-recruiter + linker) that induce
  ubiquitination of a chosen target.  Arvinas
  ARV-110 (AR), ARV-471 (ER), Kymera KT-474
  (IRAK4) etc. in clinical trials.
- **Molecular glues** — e.g. IMiDs (thalidomide,
  lenalidomide, pomalidomide) that recruit IKZF1/3
  to CRBN E3 for degradation.
- **Targeted protein-stabilisation (de-targeted
  by UCH-class DUB recruiters)** — emerging.

Covered in detail in **PH-3.0 graduate "Modern
modalities"** lesson.

## Autophagy

The other major degradation pathway — covers what
the proteasome can't (organelles, aggregates,
intracellular pathogens, bulk cytoplasm).

The 2016 Nobel Prize in Physiology or Medicine to
**Yoshinori Ohsumi** for discoveries of mechanisms
of autophagy.

### Three flavours

- **Macroautophagy** — bulk; double-membrane
  autophagosome engulfs cytoplasm + fuses with
  lysosome.
- **Chaperone-mediated autophagy (CMA)** —
  selective; HSC70 + LAMP2A receptor on lysosomal
  membrane import KFERQ-motif-bearing soluble
  proteins one at a time.
- **Microautophagy** — direct invagination of
  lysosomal / late-endosomal membrane to
  internalise cargo.

### Macroautophagy mechanism

1. **Initiation** — ULK1 complex (ULK1 + ATG13 +
   FIP200 + ATG101) activated; ULK1 phosphorylates
   downstream factors.  mTORC1 normally
   phosphorylates / inhibits ULK1; nutrient /
   energy stress relieves the inhibition.
2. **Nucleation** — class III PI3K complex (Vps34
   + Beclin-1 + ATG14L) generates PI3P at the
   isolation membrane (phagophore).
3. **Elongation** — two ubiquitin-like
   conjugation systems extend the membrane:
   - ATG12-ATG5-ATG16L1 (analogous to E1-E2-E3)
   - LC3-PE (LC3 lipidated to phosphatidyl-
     ethanolamine on the autophagosome inner +
     outer membrane).
4. **Closure** — phagophore seals into a double-
   membrane autophagosome.
5. **Fusion + degradation** — autophagosome fuses
   with lysosome (SNARE-mediated; STX17, SNAP-29,
   VAMP8); inner membrane + cargo degraded by
   lysosomal hydrolases.

### Selective autophagy

Cargo-specific receptors carry a LIR (LC3-
interacting region) + a cargo-binding domain:

- **Mitophagy** — damaged mitochondria.
  - **PINK1 / Parkin** pathway: PINK1 stabilises
    on depolarised mitochondrial outer membrane
    → recruits Parkin (E3 ligase) → ubiquitinates
    OMM proteins → recruits OPTN, NDP52, p62,
    NBR1 receptors → autophagosome envelopment.
  - **BNIP3 / NIX / FUNDC1** — receptor-mediated
    mitophagy (developmental, hypoxic).
- **Pexophagy** — peroxisome-selective.
- **Reticulophagy** — ER-selective (FAM134B,
  RTN3, ATL3, CCPG1, TEX264, ATG40).
- **Aggrephagy** — protein aggregates (p62 +
  NBR1 + WDR81 + WDR91 + TOLLIP).
- **Xenophagy** — intracellular pathogens
  (Salmonella, M. tuberculosis, Listeria).
- **Lipophagy** — lipid droplets.
- **Nucleophagy** — nuclear material.
- **Lysophagy** — damaged lysosomes (galectin-
  recognition).

### Chaperone-mediated autophagy

- HSC70 chaperone recognises KFERQ motifs in
  cytosolic soluble proteins.
- Substrate complex docks onto LAMP2A on
  lysosomal membrane.
- LAMP2A multimerises + translocates substrate
  into lysosomal lumen for degradation.
- Substrates include GAPDH, IκB, α-synuclein,
  MEF2A, MYOCD, transcription factors.
- Decreased CMA activity in Parkinson's, Alzheimer's,
  Huntington's, and ageing.

### Regulation

- **mTORC1** — central inhibitor of autophagy
  under nutrient / amino-acid sufficiency.
- **AMPK** — central activator under energy stress
  (low ATP / high AMP).
- **TFEB** — master transcriptional regulator;
  starvation / lysosomal stress causes mTORC1-
  mediated TFEB dephosphorylation + nuclear
  import → upregulates autophagy + lysosomal
  biogenesis genes ("CLEAR network").
- **ULK1 + Beclin-1** — phosphorylation-controlled
  hubs.

### Drug + disease relevance

- **Hydroxychloroquine + chloroquine** — block
  autophagosome-lysosome fusion via lysosomal
  alkalinisation.  Repurposed in some oncology
  + RA + lupus indications.
- **mTOR inhibitors** — rapamycin / sirolimus +
  everolimus + temsirolimus + ridaforolimus
  ACTIVATE autophagy; clinical use in
  immunosuppression + oncology + tuberous
  sclerosis.
- **AMPK activators** — metformin + AICAR.

Disease links:
- **Neurodegeneration** — PD (PINK1 / Parkin);
  AD (autophagy decline + Aβ / tau aggregate
  clearance); HD (impaired autophagy of mutant
  HTT).
- **Cancer** — context-dependent; promotes
  early tumour suppression but supports
  established tumour survival.
- **Crohn's disease** — ATG16L1 + IRGM + NOD2
  variants impair anti-bacterial autophagy.
- **Vici syndrome + Vici syndrome variants** —
  EPG5, ATG7, ATG2B, ATG16L1 mutations cause
  human autophagy disorders.
- **Lysosomal storage diseases** — block
  autophagy flux at the degradation step.

## ER-associated degradation (ERAD)

A specialised QC system intersecting UPS +
membranes:
- Misfolded ER luminal + transmembrane proteins.
- Recognised by ER chaperones (BiP, calnexin,
  calreticulin) + lectins (OS-9, XTP3-B).
- Retrotranslocated to cytosol via Hrd1 / Sel1L
  + Derlins + Hrd1-associated VCP/p97 AAA+
  ATPase.
- Ubiquitinated en route + degraded by 26S
  proteasome.
- ΔF508-CFTR (most-common CF mutation) is
  cleared by ERAD → loss of function on the cell
  surface.  Trikafta (lumacaftor / elexacaftor /
  ivacaftor) corrects.

## Lysosomal degradation interface

Both autophagy + endocytic-pathway cargo converge
at the lysosome.  Lysosomal hydrolases handle
final degradation; lysosomal storage diseases
block the throughput at specific substrates
(covered in **CB-4.0 advanced "Lysosomal
degradation + lysosomal storage diseases"
lesson**).

## Clinical pharmacology summary

- **Bortezomib + carfilzomib + ixazomib** —
  proteasome inhibitors; multiple myeloma.
- **PROTACs** — emerging clinical degraders.
- **Hydroxychloroquine** — autophagy inhibitor;
  rheumatology + oncology repurposing.
- **Sirolimus / everolimus / temsirolimus** —
  mTOR inhibitors → autophagy activators;
  oncology + transplant.
- **IMiDs (thalidomide / lenalidomide /
  pomalidomide)** — molecular glues; multiple
  myeloma.
- **Trikafta** — CFTR correctors / potentiators
  bypass ERAD; cystic fibrosis.
- **MDM2-p53 inhibitors** (idasanutlin,
  navtemadlin) — block MDM2 E3 activity →
  stabilise p53; cancer.

## Try it in the app

- **OrgChem → Tools → Cell components** —
  proteasome + lysosome + autophagosome entries.
- **Window → Cell Biology Studio → Cell cycle
  tab** — APC/C-mediated cyclin degradation in
  mitosis.
- **Window → Pharmacology Studio → Drug classes**
  — proteasome inhibitors + mTOR inhibitors +
  PROTACs.
- **Window → Biochem Studio → Enzymes** —
  proteasomal protease + lysosomal hydrolase
  entries.

Next: **Cell-cell adhesion + extracellular
matrix**.
