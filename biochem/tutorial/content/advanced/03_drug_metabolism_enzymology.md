# Drug metabolism enzymology

The body sees almost every drug as a foreign chemical
("xenobiotic") + immediately starts trying to dispose of
it.  The enzyme set that does this is one of the most
clinically-impactful (+ commercially-impactful) corners
of biochemistry.

## Phase I — functionalisation

Phase I metabolism INTRODUCES or EXPOSES a polar
functional group (typically -OH, -NH₂, -SH, or -COOH).
The product is rarely water-soluble enough to excrete on
its own — but it carries the handle that Phase II will
conjugate.

### Cytochrome P450 (CYP) — the dominant Phase I family

Heme-thiolate monooxygenases.  ~ 57 human CYP genes
across 18 families.  ~ 75 % of clinically-prescribed
drugs are metabolised by just **6 CYPs**: CYP3A4,
CYP2D6, CYP2C9, CYP2C19, CYP1A2, CYP2E1.

Reaction:

R-H + O₂ + NADPH + H+ → R-OH + H₂O + NADP+

Mechanism (Compound I):
1. Substrate binds in the apo-pocket.
2. Fe(III)-heme reduced to Fe(II) (electron from NADPH-
   CYP reductase via FAD/FMN).
3. O₂ binds → Fe(III)-OO⁻ (oxy-ferric).
4. Second electron + protonation → Fe(III)-OOH (Compound
   0).
5. Heterolytic O-O cleavage releases H₂O → Fe(IV)=O π-
   cation radical (Compound I, the highly-reactive
   oxidant).
6. Hydrogen-atom abstraction from substrate → C-OH
   rebound.

### The big six CYPs + their drug substrates

- **CYP3A4** — most-promiscuous (≈ 50 % of drugs):
  midazolam (probe), fentanyl, simvastatin / atorvastatin,
  cyclosporine, tacrolimus, CCBs, many TKIs.  Strong
  inhibitors: ketoconazole, ritonavir, clarithromycin,
  grapefruit juice.  Inducers: rifampicin, phenytoin,
  carbamazepine, St John's Wort.
- **CYP2D6** — debrisoquine; codeine activation,
  tamoxifen activation, antidepressants, antipsychotics,
  β-blockers metoprolol/carvedilol.  ~ 7 % of caucasians
  are poor metabolisers (PMs) → inactive at codeine but
  high tox at metoprolol; ~ 1-3 % are ultra-rapid
  metabolisers (UMs) → codeine → morphine overdose risk.
- **CYP2C9** — warfarin (S-warfarin), phenytoin,
  losartan, NSAIDs.  *2/*3 alleles → reduced warfarin
  dose requirement.
- **CYP2C19** — clopidogrel activation, omeprazole, S-
  citalopram, voriconazole.  *2/*3 PM → ineffective
  clopidogrel (FDA black-box warning).
- **CYP1A2** — caffeine, theophylline, clozapine,
  duloxetine, olanzapine.  Induced by smoking → smokers
  metabolise caffeine + clozapine 50 % faster.
- **CYP2E1** — ethanol, paracetamol (NAPQI route),
  benzene, halothane.  Induced by chronic ethanol →
  amplifies paracetamol hepatotoxicity.

### Other Phase I enzymes

- **Flavin-containing monooxygenases (FMOs)** —
  N-, S-, P-oxidations; less drug-relevant than CYPs but
  metabolise nicotine, tamoxifen, voriconazole.
- **Aldehyde / alcohol dehydrogenases (ADH / ALDH)** —
  ethanol → acetaldehyde → acetate.  ALDH2*2 (East-Asian
  flush) cripples acetaldehyde clearance → flushing,
  cancer risk.  Disulfiram blocks ALDH → aversive
  acetaldehyde build-up.
- **Esterases / amidases** — hydrolyse cocaine,
  procaine, oseltamivir, capecitabine pro-drugs.
- **Monoamine oxidase (MAO-A / MAO-B)** — NT
  catabolism + drug metabolism.  MAOIs (selegiline,
  rasagiline, moclobemide) are old-but-active drug
  classes.
- **Xanthine oxidase** — purine catabolism; allopurinol /
  febuxostat inhibit (gout).

## Phase II — conjugation

Phase II ADDS a hydrophilic conjugate to the Phase-I
product (or directly to the drug if a suitable handle
exists).

### Major Phase II enzymes

- **UDP-glucuronosyl transferases (UGTs)** — most
  abundant.  UGT1A1 conjugates bilirubin (Gilbert's
  syndrome = UGT1A1*28 deficiency → mild
  unconjugated hyperbilirubinaemia).  UGT1A1 also
  glucuronidates **irinotecan's active metabolite SN-38**
  → poor metabolisers have severe diarrhoea + neutropenia
  toxicity (FDA-recommended UGT1A1*28 testing).
- **Sulfotransferases (SULTs)** — small drugs +
  endogenous (steroids, catecholamines, paracetamol low-
  dose).
- **Glutathione S-transferases (GSTs)** — conjugate
  electrophiles to GSH.  Critical NAPQI defence in
  paracetamol overdose; GST polymorphisms modulate cancer
  risk.
- **N-acetyl transferases (NAT1 / NAT2)** —
  isoniazid, sulfonamides, hydralazine.  NAT2 *slow
  acetylator* phenotype (~ 50 % of caucasians) →
  isoniazid neurotoxicity + drug-induced lupus from
  hydralazine / procainamide.
- **Methyltransferases (TPMT, COMT, etc.)** —
  thiopurine S-methyltransferase deficiency causes severe
  azathioprine / 6-MP myelotoxicity; FDA-recommended
  TPMT genotyping.

## Phase III — efflux + transport

Drug-efflux transporters move drugs (+ Phase I/II
metabolites) out of cells:
- **P-gp / MDR1 (ABCB1)** — intestinal absorption +
  blood-brain barrier + tumour MDR.  Inhibited by
  verapamil, ketoconazole, ritonavir, quinidine.
  Substrates: digoxin, dabigatran, many TKIs.
- **BCRP / ABCG2** — second major efflux; methotrexate,
  rosuvastatin, statins.
- **OATP1B1 / OATP1B3** — hepatic uptake; statins
  (especially rosuvastatin), rifampicin, methotrexate.
  SLCO1B1*5 → statin-induced myopathy risk (FDA
  warning).
- **OAT / OCT** — renal-tubular transport; methotrexate,
  metformin (OCT2), penicillins.

## Drug-drug interactions (DDIs)

Most clinically significant DDIs trace to inhibition or
induction of one of the big-six CYPs (Phase I) + UGT1A1
+ MDR1 / OATP1B1 (Phase III).

### Mechanisms

- **Reversible inhibition** — competitive, non-
  competitive, mixed.  E.g. fluconazole inhibits CYP2C9
  → warfarin INR rise.
- **Mechanism-based inhibition (MBI)** — drug or
  metabolite covalently inactivates CYP.  E.g.
  clarithromycin / erythromycin / mibefradil / grapefruit
  furanocoumarins MBI CYP3A4.  Recovery requires
  resynthesis of new CYP protein → slow + persistent
  effect.
- **Induction** — increased CYP transcription via PXR
  (rifampicin, St John's), CAR (phenobarbital,
  phenytoin), AhR (omeprazole, smoking).  Onset days,
  reversal weeks.

### Classic DDIs

- **Warfarin + amiodarone** — amiodarone inhibits CYP2C9
  → bleeding.
- **Statin + clarithromycin / itraconazole** —
  CYP3A4-pathway statins → rhabdomyolysis.
- **Tacrolimus + grapefruit** — CYP3A4 MBI →
  immunosuppressant overexposure.
- **Codeine + paroxetine** — paroxetine inhibits CYP2D6
  → codeine ineffective (no morphine activation).
- **Oral contraceptive + rifampicin** — induces CYP3A4 +
  UGT → contraceptive failure.

## Pharmacogenomics

Genetic variation in drug-metabolising enzymes drives
much inter-patient variability:

- **CYP2D6** — > 130 alleles; *4 / *5 (gene del) /
  *10 / *17 cluster patient as PM/IM/EM/UM.
- **CYP2C9*2 / *3 + VKORC1** — warfarin dose algorithms
  (CPIC guidelines).
- **CYP2C19*2 / *3** — clopidogrel (FDA black-box).
- **TPMT *2 / *3A / *3C** — thiopurine dosing.
- **DPYD *2A** — fluorouracil severe toxicity.
- **UGT1A1*28** — irinotecan dose reduction.
- **HLA-B*57:01** — abacavir hypersensitivity (genotype
  before prescribing).
- **HLA-B*15:02** — carbamazepine SJS / TEN in Han
  Chinese.
- **SLCO1B1*5** — simvastatin myopathy risk.
- **G6PD deficiency** — primaquine / dapsone /
  rasburicase haemolysis.

CPIC (Clinical Pharmacogenetics Implementation
Consortium) maintains the canonical genotype-to-
prescribing guidelines.

## Bioactivation + drug-induced toxicity

Some drugs (or Phase-I metabolites) form REACTIVE
electrophiles that damage proteins / DNA / lipids unless
trapped by GSH.

- **Paracetamol** → NAPQI (CYP2E1 + CYP3A4) → covalent
  adducts in centrilobular hepatocytes.  GSH depletion
  triggers necrosis.  N-acetylcysteine replenishes GSH
  if given < 8-10 h post-ingestion.
- **Halothane** → trifluoroacetyl chloride → halothane
  hepatitis (rare immune-mediated).
- **Diclofenac / nefazodone / troglitazone /
  trovafloxacin** — withdrawn / restricted for
  idiosyncratic hepatotoxicity often involving reactive
  metabolites.
- **Aristolochic acid** (herbal) — A:T → T:A signature
  mutations in urothelial cancers.

The med-chem field actively SCREENS OUT structural
alerts (Mike Williams + Antonia Stepan reviews) — anilines,
nitroaromatics, hydrazines, thiophenes, furans, furanones —
during lead optimisation.

## Try it in the app

- **Window → Biochem Studio → Enzymes** — `cyp3a4` +
  `cyp2d6` + `ugt1a1` + `gst-pi` entries.
- **Window → Biochem Studio → Cofactors** — `nadph` +
  `glutathione` + `udpga` (Phase II co-substrate).
- **Window → Pharmacology Studio → Drug-drug-
  interactions** — paired DDI scenarios with mechanism
  notes.
- **OrgChem → Tools → SAR series** — paracetamol +
  NAPQI structures, statin scaffold series.

Next: **Computational enzymology**.
