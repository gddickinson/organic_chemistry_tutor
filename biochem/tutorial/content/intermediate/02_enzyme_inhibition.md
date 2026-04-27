# Enzyme inhibition

Inhibitors slow down enzymes.  Most drugs are enzyme
inhibitors of one kind or another; understanding inhibition
modes is understanding most of pharmacology.

Inhibition splits along two axes:

1. **Reversibility** — reversible (binds non-covalently)
   vs irreversible (covalent, slow-binding, or mechanism-
   based).
2. **Where the inhibitor binds** — competitive,
   non-competitive, uncompetitive, mixed.

## Competitive inhibition

The inhibitor binds the **active site**, competing with
substrate.  Pure competitive inhibitors look just like the
substrate or the substrate's transition state.

Effect on kinetics:

- **Vmax unchanged** — at high [S], substrate outcompetes
  inhibitor; reaches the original maximum rate.
- **Apparent Km increased** by factor (1 + [I]/Ki).
  More substrate is needed to reach Vmax/2.

Lineweaver-Burk diagnostic: lines with different
inhibitor concentrations all **intersect on the y-axis**
(same 1/Vmax intercept).

Examples:

- **Methotrexate** competes with dihydrofolate at
  dihydrofolate reductase.
- **Captopril** competes with angiotensin I peptide at
  ACE.
- **Statins** (HMG-CoA reductase) — partially competitive
  + transition-state-mimicking.

## Non-competitive inhibition

The inhibitor binds at an **allosteric** site, separate
from the active site.  Substrate + inhibitor can be bound
simultaneously — but the EI complex doesn't catalyse.

Effect on kinetics:

- **Vmax decreased** by factor 1/(1 + [I]/Ki).  Some
  enzyme is permanently disabled.
- **Km unchanged** — substrate still binds with the same
  affinity to the active site.

Lineweaver-Burk diagnostic: lines **intersect on the
x-axis** (same -1/Km).

Examples:

- **Allopurinol → xanthine oxidase** (binds active site
  + gets oxidised in place — actually mixed/suicide).
- **Cyanide → cytochrome c oxidase** (binds heme iron,
  blocks O₂).
- **Some metal-chelating inhibitors** (EDTA on metalloenzymes).

## Uncompetitive inhibition

The inhibitor binds **only the ES complex**, not free E.
The inhibitor has nothing to bind to until substrate has
already engaged the active site.

Effect on kinetics:

- **Vmax decreased** by factor 1/(1 + [I]/Ki).
- **Km decreased** by the same factor — paradoxically,
  the affinity for substrate appears to *increase*.

Lineweaver-Burk diagnostic: **parallel lines** at
different inhibitor concentrations.

Pure uncompetitive inhibitors are rare.  Examples:

- **Lithium** on inositol monophosphatase (IMPase) — a
  proposed mechanism for its mood-stabilising effect.
- **Fosamprenavir** on HIV protease — uncompetitive
  component.

## Mixed (non-competitive) inhibition

The inhibitor binds both E and ES, but with different
affinities.  Most "real" non-competitive inhibitors are
actually mixed.

Effect on kinetics:

- **Vmax decreased**.
- **Km may increase or decrease** depending on whether
  the inhibitor has a higher affinity for E or ES.

Lineweaver-Burk diagnostic: lines intersect off both
axes.

## Irreversible (covalent) inhibition

The inhibitor forms a **covalent bond** with the enzyme,
permanently disabling it.  Examples:

- **Aspirin → COX-1 + COX-2** — acetylates a serine in
  the active site.  The platelet effect lasts ~ 7-10
  days because platelets can't synthesise new COX.
- **Penicillin → bacterial transpeptidases** (PBPs) —
  the β-lactam acylates the active-site serine.
- **Omeprazole → H⁺/K⁺-ATPase** — disulfide-forms with
  active-site cysteine.
- **Osimertinib → EGFR T790M** — covalent acrylamide
  reacts with C797.

Kinetically, irreversible inhibition is usually time-
dependent: enzyme activity decays as more enzyme molecules
are inactivated.  The relevant parameter is **kinact / Ki**
(potency × maximal inactivation rate).

## Slow-binding + tight-binding inhibition

Some reversible inhibitors bind so slowly (or so tightly)
that the standard MM treatment breaks.

- **Slow-binding** — koff is so slow that the inhibitor-
  enzyme complex effectively persists.  Methotrexate fits
  this category at low [I].
- **Tight-binding** — Ki is so low (~ pM-nM) that the
  inhibitor concentration is comparable to enzyme
  concentration.  Need explicit treatment of the
  enzyme-inhibitor stoichiometry.

## Mechanism-based ("suicide") inhibition

The inhibitor is processed through the enzyme's normal
catalytic cycle until a reactive intermediate forms that
covalently modifies the enzyme:

- **Allopurinol → xanthine oxidase** — oxidised to
  alloxanthine in the active site, then traps the Mo
  cofactor.
- **5-Fluorouracil → thymidylate synthase** — forms a
  covalent ternary complex with enzyme + folate cofactor.
- **DFMO (eflornithine) → ornithine decarboxylase** —
  difluoromethylornithine; sleeping-sickness drug.

Mechanism-based inhibitors give exceptional selectivity
because only the target enzyme can activate them.

## Drug examples by mode

| Drug | Target | Mode |
|------|--------|------|
| Captopril | ACE | Competitive |
| Methotrexate | DHFR | Competitive (slow-binding) |
| Statins (atorva-, rosuva-, etc.) | HMG-CoA reductase | Competitive (TS analogue) |
| Allopurinol | Xanthine oxidase | Suicide / mechanism-based |
| Aspirin | COX-1 / COX-2 | Irreversible (acetylation) |
| Omeprazole | H+/K+-ATPase | Irreversible (covalent disulfide) |
| Penicillin | PBPs | Irreversible (covalent acyl) |
| Osimertinib | EGFR T790M | Irreversible (covalent C797) |
| 5-Fluorouracil | Thymidylate synthase | Mechanism-based |

## Why this matters

- **Selectivity** — competitive inhibitors targeting an
  active site are usually less selective than allosteric
  ones (active sites are conserved across enzyme families).
- **Resistance** — competitive inhibitors are easily
  resisted by point mutations in the active-site pocket
  (EGFR T790M defeats first-gen TKIs); allosteric +
  covalent inhibitors are usually more robust.
- **Dosing** — irreversible inhibitors need only achieve
  enzyme target once, then the duration of action is
  set by enzyme resynthesis rate (PPI dosing every
  morning).

## Try it in the app

- **Window → Biochem Studio → Enzymes** — entries note
  the major drug inhibitors per enzyme.
- **Window → Pharmacology Studio → Drug classes** —
  most entries are inhibitors of a specific enzyme
  target.

Next: **Allostery and cooperativity**.
