# Drug-receptor basics

A receptor is a molecule (usually a protein) that
recognises a specific ligand + transduces that binding
into a cellular response.  Most drugs work by occupying
a receptor in some way.

## The drug-receptor complex

Drugs bind receptors via a combination of non-covalent
interactions:
- Hydrogen bonds.
- Hydrophobic contacts.
- van der Waals + π-stacking.
- Ionic / salt bridges.
- Occasional covalent bonds (irreversible inhibitors,
  e.g. aspirin acetylating COX, omeprazole sulfenamide
  with H+/K+-ATPase).

Affinity is measured as the dissociation constant
**K_d** — concentration at which 50 % of receptors are
occupied at equilibrium.  K_d ranges:

- Drug-target K_d typically 10 nM to 10 µM.
- Hormone-receptor K_d 0.1 to 10 nM.
- Antibody-antigen K_d 0.01 to 100 nM.
- Substrate-enzyme K_m 1 µM to 10 mM.

## The four kinds of drug-receptor relationship

### Agonist

Binds the receptor + activates it — produces the same
downstream effect as the endogenous ligand (or
mimics it).

- **Full agonist** — produces the maximal possible
  receptor response.  Morphine at μ-opioid; salbutamol
  at β2-adrenergic; isoproterenol at all β-adrenergic.
- **Partial agonist** — produces a sub-maximal response
  even at saturating concentration.  Buprenorphine at
  μ-opioid (~ 40 % of full opioid effect); aripiprazole
  at D2 (low-end partial agonism).  Acts as an agonist
  in low-tone systems but as a functional ANTAGONIST
  in high-tone systems (it competes for the receptor +
  produces less than the endogenous full agonist).

### Antagonist

Binds without activating; blocks the receptor.

- **Competitive antagonist** — binds the same site as
  the agonist, surmountable by raising agonist
  concentration.  Naloxone at μ-opioid; propranolol at
  β-adrenergic; losartan at AT1.  Right-shifts the
  agonist dose-response curve in parallel (Schild plot
  gives K_B).
- **Non-competitive / insurmountable antagonist** —
  binds an allosteric site OR covalently — agonist
  cannot displace.  Phenoxybenzamine at α-adrenergic
  (covalent, persistent days).
- **Uncompetitive antagonist** — binds only when the
  agonist is bound (NMDA channel blockers like memantine
  + ketamine; the ion channel must be open).

### Inverse agonist

Stabilises the receptor's INACTIVE state — so reduces
constitutive (basal, agonist-free) signalling.  Looks
like an antagonist in unstimulated systems but
distinguishable in systems with constitutive activity.

Examples:
- Many "antagonists" reclassified: most H1 antihistamines
  (cetirizine, loratadine) are inverse agonists at H1.
- Naloxone is an inverse agonist at μ-opioid.
- Pindolol is a partial inverse agonist at β-adrenergic.
- Ranitidine + cimetidine at H2.

The clinical implications are usually subtle —
relevant in receptor over-expression states (heart
failure with up-regulated β1, asthma with
constitutively active β2).

### Allosteric modulator

Binds a site distinct from the orthosteric (endogenous-
ligand) site + alters receptor function.

- **PAM (positive allosteric modulator)** — boosts
  agonist activity (BZDs at GABA_A; cinacalcet at CaSR;
  ivacaftor at CFTR; aripiprazole at D2 — actually a
  partial agonist + PAM).
- **NAM (negative allosteric modulator)** — reduces
  agonist activity.  Maraviroc at CCR5 (antagonist
  via NAM).
- **Silent allosteric modulator (SAM)** — binds the
  allosteric site but doesn't change activity at the
  orthosteric ligand; useful as PET tracers.

Allosteric drugs offer subtype selectivity that's hard
to achieve with orthosteric drugs (the orthosteric
site is conserved across receptor subtypes; allosteric
sites diverge).

## Affinity vs efficacy vs potency

These three are related but distinct.

- **Affinity (K_d)** — how tightly the drug binds.
  Determined by the equilibrium of binding.
- **Efficacy** — how big a response a bound drug
  produces.  Full agonist = full efficacy; partial
  agonist = partial; antagonist = zero; inverse agonist
  = negative.
- **Potency (EC50)** — concentration producing 50 %
  maximal response.  Combines affinity + efficacy +
  receptor reserve.

A drug can be high-affinity + low-efficacy (good
antagonist) or low-affinity + high-efficacy (need
high concentration but full response when achieved).

## Receptor reserve / spare receptors

Many tissues have more receptors than needed for the
maximal physiological response.  An agonist can elicit
maximal response while occupying only a small fraction
(say 10-20 %) — the rest are "spare receptors".

Effects:
- EC50 is much LOWER than K_d (high-efficacy agonists
  saturate the response well before saturating
  occupancy).
- Partial agonists show their partial-agonist character
  more dramatically in tissues with low reserve.
- Receptor down-regulation (chronic agonist exposure)
  shifts the spare-receptor pool down, reducing efficacy
  + tolerance.

## Selectivity vs specificity

- **Selectivity** — preference for one target over
  others.  No drug is perfectly selective; the practical
  question is "how big is the gap?"  Atenolol is
  β1-selective vs β2 by ~ 30-fold; metoprolol ~ 75×;
  nebivolol ~ 300×.
- **Specificity** — historical term often used to mean
  "no off-target activity" — strictly aspirational.

Off-target effects drive most adverse drug reactions
(hERG → QT prolongation; muscarinic cross-reactivity →
dry mouth, urinary retention; H1 cross-reactivity →
sedation).

## Receptor regulation — desensitisation, tachyphylaxis,
tolerance

Chronic agonist exposure modifies the receptor system:

- **Receptor phosphorylation** by GRKs → β-arrestin
  recruitment → receptor internalisation +
  desensitisation (within minutes).
- **Down-regulation** — receptor degradation; new
  steady-state receptor number lower (hours-days).
- **Up-regulation** of antagonist-blocked receptors
  (β-blocker withdrawal can precipitate angina /
  arrhythmias from up-regulated β-adrenergic systems).
- **Functional tolerance** — downstream adaptation
  even with intact receptor numbers (opioids, alcohol,
  benzodiazepines).

## How this maps to clinic

Knowing the agonist / antagonist / partial agonist /
inverse agonist + allosteric architecture of a drug
class predicts:

- **Time course of effect** — fast on / off (β-blockers
  short-acting like esmolol) vs persistent (covalent like
  aspirin).
- **Withdrawal phenomena** — antagonists with chronic
  use risk receptor up-regulation, withdrawal storm
  on stoppage.
- **Switch dynamics** — switching a partial agonist
  (buprenorphine) for a full agonist (methadone)
  requires careful timing to avoid precipitated
  withdrawal.
- **Combination strategies** — full agonist for
  emergency rescue, partial agonist for chronic
  maintenance.

## Try it in the app

- **Window → Pharmacology Studio → Receptors** — every
  receptor superfamily with representative agonists +
  antagonists + allosteric modulators.
- **Window → Pharmacology Studio → Drug classes** —
  drug-class entries note agonist / antagonist /
  partial / allosteric.
- **Window → Cell Biology Studio → Signalling** — see
  how receptor occupancy translates to downstream
  pathway activation.

Next: **Pharmacokinetics**.
