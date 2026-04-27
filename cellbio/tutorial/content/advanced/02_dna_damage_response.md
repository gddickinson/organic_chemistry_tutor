# DNA damage response + cell-cycle checkpoints

A diploid human cell sustains ~ 10 000 - 100 000 DNA
lesions per day from endogenous + exogenous sources.
Surviving requires a fast, accurate, integrated DNA
damage response (DDR) that detects damage, halts the cell
cycle, recruits repair machinery, and — if damage is
overwhelming — triggers apoptosis.

## The damage spectrum

Different lesions need different repair pathways:

- **Single-strand breaks (SSBs)** — base excision repair
  (BER), single-strand annealing.
- **Double-strand breaks (DSBs)** — most-dangerous lesion
  type. Two repair routes:
  - **Homologous recombination (HR)** — high-fidelity,
    uses sister chromatid as template; requires S/G2.
  - **Non-homologous end joining (NHEJ)** — error-prone;
    works in any cycle phase.
- **Bulky adducts** (UV photoproducts, cisplatin) —
  nucleotide excision repair (NER).
- **Mismatches + small indels** — mismatch repair (MMR).
- **Base alkylation** — direct reversal (MGMT, ALKBH).
- **Crosslinks** — Fanconi anaemia pathway.

## The signalling apex: ATM + ATR

Two PIKK-family kinases sense damage + drive the DDR:

- **ATM** — senses DSBs via the MRN complex (Mre11-Rad50-
  Nbs1). Active in all cycle phases.
- **ATR** — senses ssDNA at stalled replication forks via
  RPA-coated ssDNA + ATRIP. Mainly S-phase + G2.

Both phosphorylate hundreds of substrates in the SQ/TQ
motif format.

## Checkpoint kinases + Cdc25 inhibition

ATM + ATR activate the effector checkpoint kinases:

- **ATM → Chk2** (CHEK2)
- **ATR → Chk1** (CHEK1)

Chk1 + Chk2 phosphorylate the **Cdc25** family of
phosphatases. Phosphorylated Cdc25 binds 14-3-3 + gets
sequestered to cytoplasm + ubiquitinated for destruction.

Loss of Cdc25 → CDKs stay phosphorylated on Tyr15 by Wee1
→ CDK activity blocked → cell cycle arrests.

## Three checkpoints

### G1/S checkpoint

DNA damage at G1 → ATM → Chk2 + p53. Phosphorylated p53
escapes MDM2 → transactivates p21^Cip1/Waf1. p21 binds +
inhibits Cyclin E-CDK2 + Cyclin D-CDK4/6 → Rb stays
hypophosphorylated → E2F bound → no S-phase entry.

p53 is the master G1/S checkpoint. ~ 50 % of human
tumours have lost p53.

### Intra-S checkpoint

Replication-fork stress (depleted dNTPs, UV damage,
nucleotide-analogue exposure) → ATR → Chk1 → Cdc25A
destruction → CDK2 inhibition → late-origin firing
suppressed + fork stabilisation. Fork-protection complex
(BRCA2, BRCA1, Rad51, FANCD2) prevents fork collapse.

### G2/M checkpoint

DSBs in G2 → ATM/ATR → Chk1/Chk2 → Cdc25B/C inhibition →
CDK1 stays Tyr15-phosphorylated by Wee1 → no mitotic
entry. p53 → 14-3-3σ → cytoplasmic Cyclin B-CDK1
sequestration adds belt-and-braces.

## Repair pathway choice in S/G2

DSBs in S/G2 face an HR-vs-NHEJ choice:

- **53BP1 + Shieldin** push toward NHEJ (block end
  resection).
- **BRCA1 + CtIP + MRN** push toward HR (initiate
  resection).

The balance is set by cell cycle (HR only with sister
chromatid available) + chromatin context (heterochromatin
NHEJ-prone).

## BRCA + PARP — synthetic lethality

The most beautiful clinical exploitation of DDR:

- **PARP1** detects SSBs + recruits repair machinery via
  PAR (poly-ADP-ribose) chain on substrates.
- **PARP inhibitors** (olaparib, niraparib, rucaparib,
  talazoparib) block PARP → SSBs accumulate → at the
  next replication fork they convert to DSBs → require
  HR repair.
- BRCA1/2-mutant tumours can't do HR → forced into
  error-prone NHEJ → catastrophic genome instability →
  tumour cell death.
- Normal cells with intact BRCA can still do HR → tumour
  selectivity.

Olaparib was the first FDA-approved PARP inhibitor (2014,
ovarian cancer). Now standard for BRCA1/2-mutant ovarian
+ breast + prostate + pancreatic cancer.

## Therapeutic targets in DDR

- **PARP** inhibitors — ↑ ssDNA breaks → DSBs → HR-
  defective tumour death.
- **ATR** inhibitors (berzosertib, ceralasertib) —
  blockade in tumours with high replication stress (MYC-
  driven, CCNE1-amplified).
- **ATM** inhibitors (AZD0156, AZD1390) — sensitise to
  radiotherapy.
- **WEE1** inhibitors (adavosertib) — push p53-mutant
  tumours into mitosis with damage → mitotic catastrophe.
- **CHK1** inhibitors (prexasertib) — chemo-sensitisation.

## Inherited DDR syndromes

- **Ataxia-telangiectasia** — homozygous ATM loss; cerebellar
  ataxia, immunodeficiency, lymphoma predisposition.
- **Nijmegen breakage syndrome** — NBS1 (NBN) mutation; the
  Mre11 complex is broken.
- **Bloom syndrome** — BLM helicase loss; sister-chromatid-
  exchange storms.
- **Fanconi anaemia** — crosslink-repair pathway defects;
  bone-marrow failure + AML.
- **Hereditary breast + ovarian cancer** — germline BRCA1/2
  mutations.
- **Lynch syndrome** — germline MMR defects → microsatellite
  instability → CRC + endometrial cancer.

## Try it in the app

- **Cell Bio → Cell cycle** — `atm-kinase`, `atr-kinase`,
  `chk1-chk2`, `brca1-brca2`, `p53-master-tumour-suppressor`,
  `g1-s-restriction-point`, `intra-s-checkpoint`,
  `g2-m-checkpoint` entries.
- **Cell Bio → Signalling** — `p53` entry.

Next: **Cancer signalling networks — putting it together**.
