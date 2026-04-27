# CRISPR + microbial molecular biology

CRISPR-Cas systems are bacterial + archaeal adaptive
immune systems that, repurposed as programmable
nucleases, have transformed biology and now medicine.
The story is also a microbiology story — the
adaptive-immunity origin, the diversity of natural
CRISPR systems, and the anti-CRISPR arms race are
all microbial phenomena.

## The natural function

CRISPR-Cas systems defend prokaryotes against phages
+ plasmids in three stages:

1. **Adaptation** — capture short DNA fragments from
   invading nucleic acid → integrate as new spacers
   into the CRISPR array.
2. **Expression** — transcribe the array → process
   into mature crRNAs containing one spacer.
3. **Interference** — Cas-effector + crRNA
   complementarily targets + cleaves matching
   foreign nucleic acid.

Discovered in *E. coli* (Ishino 1987) as a curious
repeated sequence, characterised over decades, +
demonstrated to be an immune system by the
Mojica + Horvath / Barrangou + Marraffini + Sontheimer
labs in 2005-2008.

## CRISPR system diversity

The CRISPR-Cas literature now classifies > 30 sub-
types across 6 main types (Makarova 2020 update).

**Class 1** (multi-protein effector complexes):
- **Type I** — Cascade / Cas3 — DNA target;
  collateral DNA cleavage; Cas3 is a helicase-
  nuclease.  Used for clinical diagnostics + Locus
  Bio CRISPR-armed phages.
- **Type III** — Csm / Cmr — RNA + DNA target;
  cleavage only when RNA target is transcribed;
  cyclic-oligoadenylate signalling.
- **Type IV** — minimal; understudied.

**Class 2** (single-protein effectors — the
biotechnology workhorses):
- **Type II** — Cas9 — dsDNA target; needs both
  crRNA + tracrRNA (or fused sgRNA); blunt-end
  cleavage 3 bp upstream of PAM.
- **Type V** — Cas12 family — diverse effectors
  (Cas12a / Cpf1, Cas12b / C2c1, Cas12f / Cas14 —
  miniature ~ 400-700 aa).  Cas12a needs only crRNA,
  cleaves with 5-nt overhangs.
- **Type VI** — Cas13 — RNA-targeting; collateral
  RNase activity → SHERLOCK diagnostics.

## Cas9 — the biotechnology workhorse

The Doudna + Charpentier 2012 *Science* paper showed
*S. pyogenes* Cas9 (SpCas9) could be programmed by a
single-guide RNA (sgRNA = crRNA + tracrRNA fusion) to
cut any dsDNA target with a NGG PAM.  Doudna +
Charpentier 2020 Nobel Prize in Chemistry.

Practical features:
- ~ 1 360 aa / ~ 160 kDa.
- Two nuclease domains: HNH (cleaves target strand) +
  RuvC (cleaves non-target strand).
- Blunt-end DSB ~ 3 bp 5' of PAM.
- Off-targets driven by partial PAM-distal mismatches
  + DNA secondary structure.

Engineered variants:
- **eSpCas9 / SpCas9-HF1 / HypaCas9 / evoCas9** —
  reduced off-target.
- **SpCas9-NG / xCas9 / SpRY** — relaxed PAM (NGG →
  NGN → NRN → NNN).
- **SaCas9** (*S. aureus*) — small (~ 1 050 aa) →
  fits in single AAV.
- **CjCas9** + **NmCas9** — even smaller.
- **dCas9** (catalytically dead) — basis for CRISPRi /
  CRISPRa / base editors / prime editors / epigenome
  editors.

## Cas12a + Cas13 + miniature Cas12f

- **Cas12a / Cpf1** — Zhang lab 2015; T-rich PAM (TTN /
  TTTV); 5-nt 5' overhangs; processes its own pre-
  crRNA → multiplex editing with single transcript.
- **Cas12f / Cas14** — ~ 400-700 aa; AAV-deliverable
  for in-vivo therapy (Acuitas + Mammoth + Tomoda et
  al. work).
- **Cas13** — RNA-targeting; basis for SHERLOCK
  diagnostics + RNA degradation therapeutics
  (anti-COVID, etc.).

## Base editors (BEs)

Liu lab 2016+ — Cas9 nickase fused to a
deaminase:

- **CBE (cytidine base editor)** — APOBEC-like
  cytidine deaminase + nickase Cas9 → C → U editing
  → DNA repair fixes as C → T (or G → A on opposite
  strand).
- **ABE (adenine base editor)** — engineered TadA
  adenine deaminase → A → I → DNA repair fixes as
  A → G (or T → C).
- All 4 transition mutations achievable with CBE +
  ABE.
- No DSB → safer profile (less indel + chromosomal
  rearrangement).

Clinical:
- **VERVE-101 / VERVE-102** — Verve, ABE knockout of
  PCSK9 in liver via LNP for hereditary hyper-
  cholesterolaemia.
- **BEAM-101** — Beam, CBE of HBG promoter to
  reactivate fetal hemoglobin in SCD; ex-vivo HSC
  editing.
- **BEAM-201** — quadruple-edited allogeneic CAR-T
  for relapsed leukaemia.

## Prime editors (PEs)

Liu lab 2019 — Cas9 nickase + reverse transcriptase
+ extended **pegRNA** that contains both the guide
+ a template encoding the desired edit.  All 12
substitutions + small insertions / deletions
possible without DSB.

PE iterations:
- **PE1 / PE2 / PE3 / PE3b** — incremental
  efficiency improvements.
- **PE4 / PE5** — engineered MMR-evasion increases
  efficiency.
- **PEmax / TwinPE** — recent improvements.

Clinical: **Prime Medicine PM359** for chronic
granulomatous disease (CYBB editing) — first prime-
editor IND filed 2023.

## CRISPR therapeutics

Approved + late-stage:
- **Casgevy (exa-cel)** — Vertex / CRISPR Therapeutics;
  ex-vivo HSC CRISPR-Cas9 editing of BCL11A enhancer
  → fetal hemoglobin reactivation; SCD + β-thalassaemia.
  FDA-approved December 2023 — **first approved
  CRISPR drug**.
- **Intellia NTLA-2002** — in-vivo CRISPR-Cas9 LNP
  editing of KLKB1 for hereditary angioedema; Phase
  3 successful 2024.
- **Intellia NTLA-2001** — in-vivo TTR knockout for
  hATTR; Phase 3.
- **Verve VERVE-101 / -102** — in-vivo PCSK9 base
  edit for FH; Phase 1b.
- **Editas EDIT-101** — CEP290 retinal in-vivo
  AAV-Cas9 (mixed clinical results).
- **Beam BEAM-201** — multiplex base-edited
  allogeneic CAR-T.

## Anti-CRISPR proteins

A microbial counter-defence — phages encode Acr
proteins that bind + inactivate Cas effectors.

- **AcrIIA1-6** — anti-SpCas9 + others; first
  discovered in listeriaphages + streptococcal phages.
- **AcrIIC1-3** — anti-NmCas9.
- **AcrVA1 / VA4** — anti-Cas12a.
- **AcrVI** — anti-Cas13.
- **Acr structures** — diverse folds; some bind PAM
  pocket, some HNH or RuvC domains, some sgRNA
  loading.

Clinical / biotech use of Acrs:
- Tissue-restricted CRISPR (express Acr in off-target
  tissues).
- Editing-window control.
- Self-limiting CRISPR therapeutics (avoid prolonged
  Cas activity in vivo).

## CRISPR diagnostics

Cas13's collateral RNA cleavage activity (cleaves
nearby ssRNA after specific RNA recognition) +
Cas12's similar collateral DNA cleavage power point-
of-care molecular diagnostics:

- **SHERLOCK (Specific High-sensitivity Enzymatic
  Reporter UnLOCKing)** — Zhang lab; Sherlock Bio
  + Mammoth Bio.  Cas13a + RPA isothermal
  amplification + fluorescent reporter; attomolar
  sensitivity; SARS-CoV-2 + Lassa + Zika + Ebola
  + drug-resistance markers.
- **DETECTR** — Doudna lab; Cas12a + RPA + reporter.
- **SHINE / CARMEN** — multiplex / scalable CRISPR
  diagnostics.

Some platforms reached EUA during COVID-19; broader
clinical adoption pending regulatory + cost
optimisation.

## Microbial CRISPR phylogeny + ecology

CRISPR systems are present in:
- ~ 40 % of sequenced bacterial genomes.
- ~ 90 % of sequenced archaeal genomes.

Distribution biased by:
- Phage burden (more phages → more selection for
  CRISPR).
- Genome size (CRISPR more common in larger
  genomes).
- Lifestyle (intracellular obligate parasites lack
  CRISPR more often).

Spacer arrays as molecular records of past phage
encounters — used to reconstruct phage-host
ecological history.

## Restriction-modification + other defence

CRISPR is one defence among many:
- **Restriction-modification (R-M) systems** —
  Type I, II, III, IV.  Hundreds of variants.
- **Abortive infection (Abi)** systems — programmed
  cell death.
- **Toxin-antitoxin** loci — diverse roles incl. abi.
- **DISARM, BREX, Druantia, Wadjet, Septu, Hachiman**
  — recently-characterised diverse defence systems
  (Sorek + Bondy-Denomy labs).
- **Pyocins / pyocines / colicins / microcins** —
  bacterial-vs-bacterial chemical warfare.

The genomes of bacteria + archaea encode
extraordinary defensive diversity reflecting deep
evolutionary co-existence with phages + parasitic
mobile elements.

## Bacterial genetics + molecular biology essentials

Microbial molecular biology underpins much of
classical molecular genetics:
- *E. coli* + λ phage — the model that taught us
  transcription / translation / regulation
  (Pardee-Jacob-Monod operon model).
- **Plasmids** — circular replicons; pBR322 +
  pUC19 + pET cloning + expression vectors.
- **Conjugation** — F-plasmid; Hfr crosses; the
  founding mechanism of bacterial genetics.
- **Transformation + transduction** — natural
  competence in *S. pneumoniae* + *B. subtilis*;
  P1 / P22 generalised transducers.
- **Restriction enzymes** — discovered in bacteria
  as anti-phage defence; fuelled all of classical
  recombinant DNA.

A future **Genetics + Molecular Biology Studio**
sibling will deepen technique-level coverage of
cloning + expression + sequencing + recombinant DNA.

## Try it in the app

- **Window → Microbiology Studio → Microbes** —
  *S. pyogenes* (SpCas9), *S. aureus* (SaCas9),
  *N. meningitidis* (NmCas9), *F. novicida* (Cpf1)
  source-organism entries.
- **Window → Biochem Studio → Enzymes** — Cas9,
  Cas12, Cas13, restriction enzymes, RNase III.
- **Window → Pharmacology Studio → Drug classes** —
  CRISPR therapeutics + base / prime editors as a
  modality class.

Next: **Antimicrobial resistance epidemiology +
stewardship**.
