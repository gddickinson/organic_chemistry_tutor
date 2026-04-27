# Drug-drug interactions

A drug-drug interaction (DDI) is a clinically
significant change in one drug's PK or PD caused by
another drug.  DDIs are one of the most common
preventable causes of adverse drug events.

## Classification

Two broad classes:

- **Pharmacokinetic (PK) DDIs** — one drug alters the
  ABSORPTION / DISTRIBUTION / METABOLISM / EXCRETION
  of another → changed concentration.
- **Pharmacodynamic (PD) DDIs** — drugs act on the
  same physiological system → additive, synergistic,
  or antagonistic effect even with normal concentrations.

A single drug pair can have BOTH PK + PD interactions
(e.g. clarithromycin + simvastatin: CYP3A4 inhibition
+ both raise rhabdomyolysis risk).

## PK DDIs — by mechanism

### Absorption-stage interactions

- **pH change** — antacids / PPIs raise gastric pH +
  reduce dissolution of weak-acid drugs (atazanavir,
  ketoconazole, dasatinib).
- **Chelation** — divalent / trivalent cations (Ca²⁺,
  Mg²⁺, Al³⁺, Fe²⁺/³⁺) bind tetracyclines + fluoro-
  quinolones + bisphosphonates → reduced absorption.
  Separate dosing by 2-4 h.
- **Gut motility** — metoclopramide accelerates gastric
  emptying + raises Cmax of paracetamol; opioids slow
  gastric emptying.
- **Adsorbents / binding resins** — cholestyramine
  binds warfarin, digoxin, thyroxine, statins.
- **P-gp inhibition / induction** at the intestinal
  apex — verapamil + clarithromycin INCREASE digoxin
  absorption; rifampicin DECREASES it.

### Distribution-stage interactions

- **Plasma protein displacement** — historically
  invoked for warfarin + sulfonamides; clinically
  almost always overstated.  Free drug increases
  transiently then normalises as clearance rises.  Real
  problem only for narrow-TI drugs with limited
  capacity to clear the rise (phenytoin + valproate is
  one bona fide example).
- **P-gp at the BBB** — verapamil + cyclosporine
  inhibit P-gp → loperamide gains CNS access → opioid
  CNS effects; rifampicin INDUCES P-gp → reduced
  CNS exposure.

### Metabolism-stage interactions — the dominant class

CYP-mediated DDIs cause the majority of clinically-
significant interactions.

**CYP3A4 strong inhibitors** (raise substrate
concentration > 5×):
- Ketoconazole, itraconazole, voriconazole, posaconazole.
- Clarithromycin, telithromycin (mechanism-based).
- Ritonavir, cobicistat (PK boosters in HIV / Hep C).
- Nefazodone.
- Grapefruit juice (mechanism-based; furanocoumarins).

**CYP3A4 strong inducers** (reduce substrate
concentration > 5-fold):
- Rifampicin (the prototype).
- Phenytoin, carbamazepine, phenobarbital.
- St John's Wort (PXR activator).
- Efavirenz, etravirine.

**CYP2D6 inhibitors**:
- Fluoxetine, paroxetine (potent + irreversible-like).
- Bupropion, duloxetine.
- Quinidine.
- Cinacalcet, terbinafine.

Clinically dramatic CYP DDIs:
- **Clarithromycin + simvastatin** → rhabdomyolysis
  (FDA contraindication).
- **Voriconazole + warfarin** → bleeding (CYP2C9 +
  3A4 inhibition).
- **Rifampicin + oral contraceptive** → contraceptive
  failure (CYP3A4 + UGT induction).
- **Paroxetine + tamoxifen** → tamoxifen ineffective
  (CYP2D6 inhibition blocks endoxifen production).
- **Fluconazole + sulfonylureas** → hypoglycaemia
  (CYP2C9).
- **Codeine + paroxetine** → no analgesic effect
  (CYP2D6 blocked → no morphine activation).

### Excretion-stage interactions

- **Probenecid + penicillins** → penicillin
  accumulates (OAT inhibition); historically
  exploited to spare penicillin doses.
- **Lithium + thiazides / NSAIDs / ACEi** → increased
  lithium levels (multiple mechanisms involving renal
  Na+ handling + GFR).
- **Digoxin + quinidine / amiodarone / verapamil /
  dronedarone** → P-gp-mediated reduced renal +
  biliary clearance → digoxin toxicity.
- **Methotrexate + NSAIDs** → reduced renal MTX
  clearance + competition at OAT3.
- **Trimethoprim + RAAS blockers** → hyperkalaemia
  (TMP blocks renal K+ excretion; RAAS blockade
  raises K+).

## PD DDIs

### Synergistic toxicity

- **Multiple CNS depressants** — opioids + benzo-
  diazepines + alcohol → respiratory depression.
  Black-box warning on opioid + BZD co-prescription.
- **Multiple anticholinergics** — TCAs + first-gen
  antihistamines + bladder antimuscarinics →
  delirium, urinary retention, constipation
  (anticholinergic burden).
- **Multiple QT-prolongers** — fluoroquinolones +
  ondansetron + methadone + macrolides + many
  antipsychotics → torsades de pointes.
- **Serotonin syndrome** — SSRI + MAOI; SSRI +
  tramadol; SSRI + linezolid; SSRI + triptan (less
  common).
- **Hypoglycaemia** — sulfonylurea + insulin + alcohol.
- **Hyperkalaemia** — RAAS blockers + spironolactone +
  K+-sparing diuretics + TMP/SMX + NSAIDs.

### Therapeutic synergy

- **β-lactam + aminoglycoside** for endocarditis.
- **Combination antiretroviral therapy** for HIV.
- **RIPE** for tuberculosis (rifampicin + isoniazid +
  pyrazinamide + ethambutol).
- **Triple-drug heart-failure** — RAAS blocker +
  β-blocker + MRA + SGLT2i.
- **Anti-cancer combinations** designed for non-
  overlapping toxicities + presumed synergy.

### Antagonism

- **Naloxone + opioids** — opioid reversal.
- **Flumazenil + benzodiazepines** — BZD reversal.
- **Idarucizumab + dabigatran** — DOAC reversal.
- **Andexanet alfa + Xa inhibitors** — DOAC reversal.
- **Vitamin K + warfarin** — warfarin reversal.
- **Atropine + organophosphate poisoning** — muscarinic
  blockade.
- **Naltrexone + alcohol craving** (PD opioid
  antagonism in reward pathways).

## Predicting + preventing DDIs

Tools for clinicians:
- **Lexicomp / UpToDate / Micromedex / BNF** — DDI
  databases with severity ratings.
- **EHR DDI alerts** — high false-positive rate causes
  alert fatigue.
- **FDA Drug Interaction tables** — for new approvals.
- **University of Liverpool HEP-iChart + HIV-iChart** —
  authoritative for DAA + ART regimens.
- **Pharmacist medication review** — best-evidence
  reduction in clinically significant DDIs.

## DDI testing in development

FDA + EMA require:
- **In vitro CYP inhibition / induction** screening for
  every NCE.
- **In vitro transporter (P-gp, BCRP, OATP1B1/3, OAT,
  OCT) screening**.
- **Clinical PK DDI studies** for likely real-world
  combinations (typically with strong CYP3A4 inhibitor +
  inducer + substrate).
- **Population PK + PBPK modelling** to predict
  untested clinical scenarios.

The FDA "Drug Development + Drug Interactions: Table
of Substrates, Inhibitors and Inducers" is the
authoritative reference.

## DDI traps to know

### Mechanism-based (irreversible) inhibition

Some inhibitors covalently inactivate CYP — recovery
requires de novo enzyme synthesis (days).  Effects
persist days after the inhibitor stops.

Notorious offenders:
- Clarithromycin, erythromycin (CYP3A4).
- Mibefradil (withdrawn — CYP3A4 MBI).
- Ritonavir (CYP3A4 + CYP2D6 — used as a "PK
  booster").
- Grapefruit juice (CYP3A4 — single glass effect
  ~ 24 h; chronic effect ~ 72 h).

### Time-dependent induction onset

Inducers (rifampicin, phenytoin, carbamazepine,
St John's Wort) take days for effect onset (induction
requires new transcription + translation) + days-weeks
to wash out — affecting drugs PRESCRIBED LATER as
well as concurrent.

### Pharmacogenomic confounding

Same DDI severity varies by CYP genotype (CYP2D6 PMs
already have low metabolism + further inhibition has
less proportional effect; UMs may have apparently
"normal" metabolism even with inhibition that would
massively affect EMs).

## Cross-link

For comprehensive coverage of drug-metabolising enzymes
+ Phase I/II/III mechanisms + pharmacogenomics, see the
**BC-3.0 advanced lesson "Drug metabolism enzymology"**.

## Try it in the app

- **Window → Biochem Studio → Enzymes** — `cyp3a4`,
  `cyp2d6`, etc., for the principal DDI sites.
- **Window → Pharmacology Studio → Drug classes** —
  per-class DDI flags + clinically-significant
  interactions.
- **Window → Pharmacology Studio → Receptors** — PD
  interaction context (multiple CNS depressants,
  serotonin syndrome).

Next: **Drug development pipeline**.
