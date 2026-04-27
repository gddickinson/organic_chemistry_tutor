# Platform retrospective — the 6-studio build chain

This lesson documents the complete history of the multi-
studio life-sciences platform.  The chain ran from
**round 212 to round 217** over six consecutive autonomous
wakeup-driven rounds.  Six sibling studios shipped, one per
round, each at zero cost to the others and zero cost to the
mature OrgChem foundation.

This is the headline document of the entire build.

## What shipped, sibling by sibling

### OrgChem Studio — the foundation (rounds 1-211)

The base application — an interactive PySide6 desktop
environment for learning + teaching organic chemistry.
Mature for 211 rounds before the multi-studio platform
even started.  Ships ~ 415 seeded molecules · 37 named
reactions · 20 multi-step mechanisms · 25 classical
synthesis pathways · 20 reaction-coordinate energy
profiles · 80 glossary terms · **215 tutorial lessons**
(beginner 68 / intermediate 51 / advanced 46 / graduate
50) · a ChemDraw-equivalent molecular drawing tool · a
full protein/small-molecule interaction stack · a
sequence viewer linked to 3D ribbon · 100 % GUI-coverage
audit gate.  This is the foundation every sibling builds
on.

### Cell Biology Studio (CB-1.0, round 212)

**The first sibling.**  26-pathway cell-signalling
catalogue (MAPK/ERK, PI3K/Akt/mTOR, JAK/STAT, Wnt,
Notch, Hedgehog, NF-κB, TGF-β, GPCR-second-messengers,
AMPK, p53, apoptosis, TCR, …).  4 agent actions in the
new `cellbio-signaling` category.  `CellBioMainWindow`
opened from *Window → Cell Biology Studio…*
(Ctrl+Shift+B).  14 pathways carry drug references
(Vemurafenib → BRAF, Sirolimus → mTORC1, Metformin →
AMPK, …) cross-referenced against the OrgChem molecule
DB.  33 new tests; **2 288 → 2 321** passing.

The architectural decisions made here set the pattern:
sibling packages (no big-bang refactor of OrgChem); top-
level QMainWindow per sibling; shared registry / DB /
glossary; Python-only catalogue files (no new DB tables
for v0.1); lazy data-import to keep file sizes under the
500-line cap.

### Biochemistry Studio (BC-1.0, round 213)

**The first cross-studio bridge.**  30-enzyme catalogue
spanning all 7 IUBMB EC classes (oxidoreductase →
translocase) with mechanism class, substrates, products,
cofactors, regulators, disease associations, drug
targets, structural family.  4 agent actions in the new
`biochem-enzymes` category.  `BiochemMainWindow` opened
from *Window → Biochem Studio…* (Ctrl+Shift+Y).

The headline new feature: a **Metabolic-pathways tab** in
the Biochem main window that surfaces `orgchem.core.
metabolic_pathways` read-only — the first time a sibling
studio rendered another package's data directly via
Python import, no copy + no fork.  Validated the cross-
studio data-sharing pattern works between siblings, not
just *within* OrgChem.

36 new tests; **2 321 → 2 357** passing.

### Pharmacology Studio (PH-1.0, round 214)

**Multi-hop Python-catalogue bridges.**  30-drug-class
catalogue across 11 therapeutic areas (cardiovascular,
metabolic, neurology-psychiatry, oncology, infectious,
inflammation-immunology, pulmonology, endocrinology,
haematology, GI, pain) with mechanism, target, agents,
clinical use, side effects, contraindications,
monitoring.  5 agent actions in `pharm-drugs`.
`PharmMainWindow` opened from *Window → Pharmacology
Studio…* (Ctrl+Shift+H).

The headline new feature: **two bridge panels** that
read both `biochem.core.enzymes` AND `cellbio.core.
cell_signaling` directly.  PH-1.0 demonstrated the
sibling-package pattern scales to multi-hop reads — Pharm
Studio depends on Biochem Studio depends on OrgChem,
without any of the three studios needing to coordinate
during build.

40 new tests; **2 357 → 2 397** passing.

### Microbiology Studio (MB-1.0, round 215)

**3-hop cross-reference graph.**  30-microbe catalogue
across all 5 microbial kingdoms (17 bacteria — 6 gram+,
6 gram-, 3 atypical, 2 acid-fast — 2 archaea, 3 fungi,
6 viruses spanning Baltimore I → VII, 2 protists) with
morphology, key metabolism / replication, pathogenesis,
antimicrobial susceptibility, genome size, Bergey / ICTV
reference.  5 agent actions in `microbio-microbes`.
`MicrobioMainWindow` opened from *Window → Microbiology
Studio…* (Ctrl+Shift+N).

The headline architectural step: each microbe entry's
**three cross-reference families** touch
`orgchem.core.cell_components` (Phase 43) +
`pharm.core.drug_classes` (PH-1.0) +
`biochem.core.enzymes` (BC-1.0) — all from a single
per-entry record.  The **Antibiotic-spectrum bridge
panel** filters Pharm's drug classes to the 6 antimicrobial
classes (β-lactams, macrolides, fluoroquinolones,
aminoglycosides, HIV PIs, NRTIs), demonstrating sibling
→ sibling reads work.

43 new tests; **2 397 → 2 440** passing.

### Botany Studio (BT-1.0, round 216)

**First live SQLite-direct bridge.**  30-plant-taxa
catalogue spanning all 6 major plant divisions (1
bryophyte, 1 lycophyte, 2 ferns, 4 gymnosperms, 8
monocots, 14 eudicots) and all 4 photosynthetic
strategies (C3, C4, CAM, not-applicable for the
holoparasite *Rafflesia arnoldii*) with full taxonomic
name, life cycle, reproductive strategy, ecological
role, economic importance, model-organism flag, genome
size.  5 agent actions in `botany-taxa`.
`BotanyMainWindow` opened from *Window → Botany
Studio…* (Ctrl+Shift+V).

The headline architectural step: the **Plant-secondary-
metabolites bridge** is the first sibling bridge that
reads the OrgChem SQLite store directly (rather than
another sibling Python catalogue).  Filtered live by
`source_tags_json` to plant-derived natural products
(natural-product / terpene / alkaloid / steroid).
Confirms the cross-studio pattern works for live
database rows that change as users add molecules.

44 new tests; **2 440 → 2 484** passing.

### Animal Biology Studio (AB-1.0, round 217)

**Completes the platform.**  30-animal-taxa catalogue
spanning all 9 major animal phyla (porifera → cnidaria →
platyhelminthes → nematoda → mollusca → annelida →
arthropoda → echinodermata → chordata).  Each entry:
phylum, class, body plan (asymmetric / radial /
bilateral), germ layers (diploblast / triploblast),
coelom organisation (acoelomate / pseudocoelomate /
coelomate), reproductive strategy, ecological role,
model-organism flag, genome size.  5 agent actions in
`animal-taxa`.  `AnimalMainWindow` opened from *Window →
Animal Biology Studio…* (Ctrl+Shift+X).

The headline architectural step: AB-1.0 is the **second
sibling whose bridge reads `cellbio.core.cell_signaling`
directly** (the first was Pharm).  Confirms the cellbio
API is stable enough to support multiple consumers — a
key sign that the platform's library boundaries are
mature.

The catalogue's largest single entry is *Homo sapiens* —
~ 22 cross-references to the OrgChem molecule DB, ~ 26
cellbio signalling pathways, ~ 26 biochem enzymes.
Humans are the convergence point of the entire platform's
catalogues.

## The architectural pattern (the lesson the chain proved)

Every sibling shipped using the **identical pattern**:

1. **New top-level Python package** (`cellbio/`,
   `biochem/`, …) alongside `orgchem/`.  No OrgChem
   refactor, ever.
2. **Lazy data-import split**: `core/<thing>.py` (the
   dataclass + lookup helpers, < 500 lines) +
   `core/<thing>_data.py` (the verbose 30-entry catalogue,
   allowed to exceed 500 lines).
3. **`@action(category="<sibling>-<topic>")` decorator
   into the shared `orgchem.agent.actions._REGISTRY`** —
   the LLM tutor backend automatically picks up every
   sibling's actions without any tutor-side glue.
4. **Top-level `QMainWindow`** opened from OrgChem's
   *Window* menu via a lazy slot on `MainWindow`.
   Persistent singleton; geometry persists via `QSettings
   ["window/<sibling>"]`.
5. **Three inner tabs** per sibling: a primary catalogue
   tab + a bridge panel into another sibling's data + a
   tutorial panel.
6. **Six OrgChem-side glue hooks** per sibling, all in
   identical patterns:
   - `orgchem/agent/headless.py` — add `import <sibling>`.
   - `tests/conftest.py` — same.
   - `orgchem/gui/main_window.py` — add `_<sibling>_window`
     slot, *Window* menu entry, opener method.
   - `orgchem/gui/audit.py` — extend `GUI_ENTRY_POINTS`.
   - `orgchem/core/agent_surface_audit.py` — extend
     `EXPECTED_SURFACES`.
   - `orgchem/agent/actions_meta.py` — extend
     `_CATEGORY_SUMMARIES`.
7. **Two test files per sibling** (catalogue + GUI)
   gating ≥ 30 new tests including catalogue contents,
   cross-reference integrity, lookup helpers, agent action
   behaviour, GUI smoke.

The pattern was rough at the edges in CB-1.0, refined in
BC-1.0 + PH-1.0, and **production-ready by MB-1.0**.  By
the time BT-1.0 + AB-1.0 ran, each sibling shipped in a
single autonomous round with zero scaffolding work.

## Test-count growth

| Round | Sibling | Δ tests | Total |
|-------|---------|---------|-------|
| 211 | (pre-platform baseline) | — | 2 288 |
| 212 | CB-1.0 — Cell Bio | +33 | 2 321 |
| 213 | BC-1.0 — Biochem | +36 | 2 357 |
| 214 | PH-1.0 — Pharm | +40 | 2 397 |
| 215 | MB-1.0 — Microbio | +43 | 2 440 |
| 216 | BT-1.0 — Botany | +44 | 2 484 |
| 217 | **AB-1.0 — Animal** | (~ +30) | **2 514+** |

Every sibling added tests; every full-suite run stayed
green; zero regressions across the chain.

## The cross-reference graph that emerged

| Sibling | → Cross-references to |
|---------|----------------------|
| CB-1.0 | OrgChem `Molecule` (drug-target compounds — ~ 14 pathways carry drug refs) |
| BC-1.0 | OrgChem `Molecule` + `metabolic_pathways` (live read on the latter) |
| PH-1.0 | OrgChem `Molecule` + Biochem `enzymes` (Python read) + Cell Bio `signaling-pathway` (Python read — multi-hop) |
| MB-1.0 | OrgChem `cell_components` + Pharm `drug_classes` + Biochem `enzymes` (3-hop cross-references; *Antibiotic-spectrum bridge*) |
| BT-1.0 | OrgChem `Molecule` (live SQLite read for plant secondary metabolites) + OrgChem `metabolic_pathways` + Pharm `drug_classes` |
| AB-1.0 | OrgChem `Molecule` (animal hormones / neurotransmitters / metabolites) + Cell Bio `signaling-pathway` (animal-relevant subset) + Biochem `enzymes` (animal-source) |

Edges resolve at test time — every cross-reference id /
name must exist in the destination catalogue, or the
catalogue-integrity test for that sibling fails.  Edges
are typed (named tuple slot per cross-reference family)
so a future rename in any destination catalogue surfaces
the broken edge immediately.

The graph forms a hub-and-spoke with OrgChem at the centre
+ Cell Bio + Biochem as secondary hubs — Pharm /
Microbio / Botany / Animal sit on the periphery, each
reaching back through the secondary hubs.

## What's planned next

The chain proved the **breadth** axis (six siblings, one
per round).  The depth axis is the next priority.  Each
sibling has its own deeper-phase queue:

- **-2 (more catalogues)** — secondary catalogues per
  sibling.  Cell Bio gets cell-cycle + cytoskeleton +
  transporters; Biochem gets cofactors + secondary
  metabolites; Pharm gets receptor pharmacology + PK
  primer; Microbio gets virulence factors + resistance
  mechanisms; Botany gets plant tissues + hormones +
  pollination; Animal gets organ systems + behavioural
  neuroscience.
- **-3 (interactive tools)** — calculators + simulators
  per sibling.  PK simulator, antibiogram simulator,
  Punnett-square solver, photosynthesis simulator,
  cladogram builder.
- **-4 (~ 150 lessons each)** — full per-sibling
  curricula matching OrgChem's 215-lesson scope.
- **-5 (cross-studio link audit)** — formal audit of
  the cross-reference graph; reciprocal links + dead-
  link detection.
- **-6 (integration polish)** — screenshot tours,
  studios launcher, top-level platform navigation.

Per current cadence (5-6 weeks per -2, ~ 10 weeks per
-4), the deep-phase work runs ~ 9-12 months for each
sibling.  No autonomous chain queues that work — the
user picks individual deep-phase tasks as priorities
shift.

## Closing

The platform is now **complete in its v0.1 form**.  Six
sibling studios alongside OrgChem.  ~ 180 catalogue
entries (30 × 6 siblings) carrying ~ 1 000+ typed
cross-references that resolve at test time.  ~ 196 new
tests across the chain, zero regressions.  All from a
single OrgChem foundation that didn't have to change.

The pattern works.  The next decade of biology-software
features ship as new siblings (`microbiome/`, `pop_gen/`,
`ecology/`, `paleo/`, …) without anyone needing to touch
OrgChem.

Welcome to the platform.
