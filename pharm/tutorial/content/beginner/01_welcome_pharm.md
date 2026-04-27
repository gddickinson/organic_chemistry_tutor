# Welcome to Pharmacology Studio

Pharmacology Studio is the **third sibling** in the multi-
studio life-sciences platform — a dedicated workspace for
drug classes + therapeutic targets + clinical pharmacology.

This is **Phase PH-1.0** (round 214). The full Pharm catalogue
+ tools + tutorials roll out over Phases PH-2 → PH-6.

## What ships in Phase PH-1.0

Three tabs:

### 1. Drug classes — 30-entry catalogue across 11 therapeutic areas

Indexed by **molecular target type** + **therapeutic area**:

- **Cardiovascular** (8): β-blockers, ACE inhibitors, ARBs,
  calcium-channel blockers, loop + thiazide diuretics,
  statins, anticoagulants, antiplatelets.
- **Pulmonology** (1): β2-agonists.
- **Pain + inflammation** (2): NSAIDs, opioids.
- **Neurology / psychiatry** (4): SSRIs, benzodiazepines,
  atypical antipsychotics, antiepileptics.
- **Endocrinology / metabolic** (3): insulin, GLP-1
  agonists, SGLT2 inhibitors.
- **Gastrointestinal** (1): PPIs.
- **Infectious** (5): β-lactams, macrolides, fluoroquinolones,
  aminoglycosides, HIV protease inhibitors, NRTIs.
- **Oncology** (4): platinum chemotherapy, taxanes, kinase
  inhibitors, anti-PD-1 checkpoint inhibitors, anti-CD20.

Each entry carries: mechanism, molecular target, typical
agents, clinical use, side effects, contraindications,
monitoring requirements, and **typed cross-references** to:

- OrgChem `Molecule` rows (e.g. β-blockers → Propranolol,
  Metoprolol; ACE inhibitors → Captopril, Lisinopril,
  Ramipril, Enalapril).
- Biochem enzyme ids (e.g. ACE inhibitors → "ace"; HIV PIs
  → "hiv-protease", "cyp3a4"; insulin → "hexokinase").
- Cell Bio signalling-pathway ids (e.g. β-blockers →
  "gpcr-camp-pka"; kinase inhibitors → "egfr-ras-raf",
  "mapk-erk", "pi3k-akt-mtor"; checkpoint inhibitors →
  "tcr", "jak-stat").

### 2. Bridges — multi-hop cross-studio data sharing

Pharm Studio ships **two** bridge panels under one tab:

- **Biochem enzymes** — read-only view of `biochem.core.
  enzymes` filtered to drug-targetable enzymes (those with
  ≥ 1 entry in their `drug_targets`). Shows which approved
  drugs hit which enzyme.
- **Cell Bio signalling** — read-only view of
  `cellbio.core.cell_signaling` filtered to pathways with
  drug targets populated. Shows the pathway-level context
  for kinase inhibitors, GPCR antagonists, NHR modulators.

This is **multi-hop cross-studio data sharing**: Pharm
imports both Biochem and Cell Bio directly via Python.
Validates the architectural pattern works for any sibling
pair, not just sibling-to-OrgChem.

### 3. Tutorials — Pharm-specific curriculum

This welcome lesson + the planned ~ 150-200 lessons over
Phase PH-4.

## How it sits in the platform

Four studios live together as of round 214:

| Studio | Status | Opener |
|--------|--------|--------|
| OrgChem Studio | Mature (rounds 1-211; 215 lessons) | Default main window |
| Cell Bio Studio | Phase CB-1.0 (round 212) | Window → Cell Biology Studio… (Ctrl+Shift+B) |
| Biochem Studio | Phase BC-1.0 (round 213) | Window → Biochem Studio… (Ctrl+Shift+Y) |
| **Pharmacology Studio** | **Phase PH-1.0 (round 214)** — this | Window → Pharmacology Studio… (Ctrl+Shift+H) |
| Microbiology Studio | Planned (next) | — |
| Botany Studio | Planned | — |
| Animal Biology Studio | Planned | — |

All four share **one process, one Qt event loop, one SQLite
DB, one global glossary, one agent registry**.

## Cross-studio links you can already see

Open the Drug classes tab → select **Statins** → the right
pane shows:

- *Cross-reference: OrgChem molecules*: **Cholesterol**
  (real `Molecule` row).
- *Cross-reference: Biochem enzymes*: (empty for statins —
  but ACE inhibitors → `ace`; checkpoint inhibitors → none;
  HIV PIs → `hiv-protease` + `cyp3a4`).
- *Cross-reference: Cell Bio signalling*: (varies by
  class — kinase inhibitors hit `egfr-ras-raf` /
  `mapk-erk`).

Open the Bridges tab → Biochem enzymes sub-tab → see all
drug-targetable enzymes. Click *Open in Biochem Studio* to
hand off to that studio's Enzymes tab pre-selected to the
chosen enzyme.

## What's next

- **Phase PH-2** — more catalogues: receptor pharmacology
  details, dose-response data, pharmacokinetics primer.
- **Phase PH-3** — interactive tools: PK simulator (Cmax /
  AUC / t½ from administered dose), receptor occupancy
  calculator, drug-interaction checker.
- **Phase PH-4** — ~ 150-200 pharm tutorial lessons.
- **Phase PH-5** — formal cross-studio cross-reference audit
  (currently tested via test_pharm_drug_classes_catalogue.py).
- **Phase PH-6** — integration polish + screenshot tour.
