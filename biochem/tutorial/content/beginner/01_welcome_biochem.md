# Welcome to Biochemistry Studio

Biochemistry Studio is the **second sibling** in the multi-
studio life-sciences platform — a dedicated workspace for
enzymes, metabolic pathways, and the chemistry of life.

This is **Phase BC-1.0** (round 213). The full Biochem
catalogue + tools + tutorials roll out over Phases BC-2 →
BC-6.

## What ships in Phase BC-1.0

Three tabs:

### 1. Enzymes — 30-entry EC-class catalogue

Every enzyme classified by **IUBMB EC number** (1.x → 7.x):

- **EC 1 — Oxidoreductases** (5 entries): alcohol DH, lactate
  DH, GAPDH, cytochrome c oxidase, CYP3A4.
- **EC 2 — Transferases** (5): hexokinase, PKA, EGFR-TK,
  COMT, UGT1A1.
- **EC 3 — Hydrolases** (6): chymotrypsin, trypsin, HIV
  protease, caspase-3, ACE, lysozyme.
- **EC 4 — Lyases** (4): aldolase, carbonic anhydrase,
  adenylate cyclase, pyruvate decarboxylase.
- **EC 5 — Isomerases** (3): TIM, phosphoglycerate mutase,
  cyclophilin A.
- **EC 6 — Ligases** (4): DNA ligase I, glutamine synthetase,
  pyruvate carboxylase, ACC.
- **EC 7 — Translocases** (3, newest IUBMB class): Na⁺/K⁺-
  ATPase, F₁F₀-ATP synthase, P-glycoprotein.

Each entry carries: EC number, mechanism class, substrates,
products, cofactors, regulators, disease associations, drug
targets, structural family, and **typed cross-references** to:

- OrgChem `Molecule` rows (e.g. ACE → captopril, lisinopril,
  ramipril; TIM → DHAP, glyceraldehyde-3-phosphate).
- OrgChem metabolic-pathway ids (e.g. hexokinase → glycolysis;
  pyruvate carboxylase → tca_cycle; ACC → fatty_acid_synthesis).
- Cell Bio Studio signalling-pathway ids (e.g. EGFR-TK →
  egfr-ras-raf, mapk-erk, pi3k-akt-mtor; ACC → ampk + insulin).

### 2. Metabolic pathways — read-only bridge to OrgChem

**The architectural validation of the multi-studio platform.**
This Biochem-Studio tab surfaces `orgchem.core.metabolic_
pathways` (Phase 42, 11 pathways: glycolysis, TCA cycle, ox-
phos, pentose phosphate, β-oxidation, fatty-acid biosynthesis,
cholesterol biosynthesis, urea cycle, heme biosynthesis,
Calvin cycle, glycogen metabolism) **read-only** without
copying or refactoring.

Each pathway lists its full step sequence with substrates,
enzymes (incl. EC numbers + reversibility + ΔG), and
regulators. A *Open in OrgChem Tools menu…* button hands off
to the existing OrgChem dialog for full editing.

The pattern generalises: every future sibling studio
(Pharmacology, Microbiology, Botany, Animal Biology) can
surface OrgChem (or each other's) data the same way.

### 3. Tutorials — biochem-specific curriculum

This welcome lesson + the planned ~ 150-200 lessons over
Phase BC-4.

## How it sits in the platform

Three studios live together as of round 213:

| Studio | Status | Opener |
|--------|--------|--------|
| OrgChem Studio | Mature (rounds 1-211; 215 lessons) | Default main window |
| Cell Bio Studio | Phase CB-1.0 (round 212) | Window → Cell Biology Studio… (Ctrl+Shift+B) |
| **Biochem Studio** | **Phase BC-1.0 (round 213)** — this | Window → Biochem Studio… (Ctrl+Shift+Y) |
| Pharmacology Studio | Planned | — |
| Microbiology Studio | Planned | — |
| Botany Studio | Planned | — |
| Animal Biology Studio | Planned | — |

All three share **one process, one Qt event loop, one SQLite
DB, one global glossary, one agent registry**. The *Sister
studios* row in the README maps the wider plan.

## Cross-studio links you can already see

Open the Enzymes tab → select **Hexokinase** → the right pane
shows:

- *Cross-reference: OrgChem molecules*: Glucose, ATP, ADP,
  Glucose-6-phosphate (real `Molecule` rows in OrgChem's DB).
- *Cross-reference: OrgChem metabolic pathways*: glycolysis,
  pentose_phosphate (real ids in `orgchem.core.metabolic_
  pathways`).
- *Cross-reference: Cell Bio signalling pathways*: insulin
  (the `insulin` id in `cellbio.core.cell_signaling`).

This is the multi-studio platform working: one enzyme, three
studios' worth of context.

Open the Metabolic pathways tab → select **glycolysis** → see
all 10 steps with EC-numbered enzymes — the same data driving
OrgChem's Phase-42a *Tools → Metabolic pathways…* dialog.
Click *Open in OrgChem Tools menu…* to hand off to the full
OrgChem dialog.

## What's next

- **Phase BC-2** — more catalogues: cofactors + coenzymes
  (NAD/NADP, FAD, CoA, SAM, biotin, TPP, PLP, B12), amino
  acid catalogue with biosynthesis routes, nucleotide
  biosynthesis, vitamins, biopolymer sequence tools.
- **Phase BC-3** — interactive tools: Michaelis-Menten kinetics
  fitter (Lineweaver-Burk, Eadie-Hofstee, Hanes-Woolf plots),
  cofactor-cycle simulator (NAD⁺/NADH balance, ATP turnover),
  metabolic-network visualiser.
- **Phase BC-4** — ~ 150-200 biochem tutorial lessons.
- **Phase BC-5** — formal cross-studio cross-reference audit
  (currently the typed edges exist + are exposed; the audit
  test is queued).
- **Phase BC-6** — integration polish + screenshot tour.
