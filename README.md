# OrgChem Studio

An interactive PySide6 desktop application for **learning and teaching
organic chemistry**. Built on RDKit + 3Dmol.js + SQLAlchemy/SQLite, with
over **500 seeded molecules**, **30 named reactions**, **13 multi-step
mechanisms** (including enzyme active sites), **12 classical synthesis
pathways**, and an integrated **protein / small-molecule interaction
stack** that fetches from RCSB and AlphaFold DB.

The full catalogue of features is reachable from the GUI — the current
audit gate pins **100 % GUI coverage** (every registered agent action
has a corresponding menu / panel / dialog entry) and **642 tests** run
green.

![Main window — molecule workspace](screenshots/tour/01_caffeine.png)

## Feature tour

### Molecule workspace
High-quality RDKit 2D rendering + an interactive 3Dmol.js WebGL
viewer, linked to the database via the left-dock Molecule browser
and the right-dock Properties pane (MW, logP, TPSA, HBD/HBA,
Lipinski violations, QED, rotatable bonds).

![2D viewer](screenshots/tour/05_viewer_2d.png)
![3D viewer](screenshots/tour/06_viewer_3d_3dmol.png)

### Reactions + mechanisms
Reactions tab lists every seeded reaction with the full scheme and
description. Mechanism player steps through curly- and fishhook-arrow
overlays atom-by-atom, now with lone-pair dots and bond-midpoint
arrows (Phase 13c) — used by the seeded HIV-protease and RNase-A
enzyme mechanisms.

![Reactions tab](screenshots/tour/10_reactions.png)

Energy-profile diagrams per reaction with Ea / ΔH annotations:

![Energy profile — Diels-Alder](screenshots/tour/energy_diels-alder.png)

### Synthesis pathways
Multi-step teaching routes (Aspirin, Paracetamol, BHC Ibuprofen,
Vanillin, Met-enkephalin Fmoc SPPS, and more) rendered as vertical
step schemes with reagents above arrows and conditions / yield below.

![Synthesis tab](screenshots/tour/12_synthesis.png)
![Aspirin pathway (Kolbe-Schmitt)](screenshots/pathway_aspirin_kolbe.png)
![Paracetamol 3-step](screenshots/pathway_paracetamol_3step.png)

### Protein / ligand stack (Phase 24)
Proteins tab fetches from RCSB (cached locally) or AlphaFold DB
(pLDDT colour overlay auto-enabled), then provides:

- Grid-based binding-pocket detector.
- Geometric H-bond / salt-bridge / π-stacking / hydrophobic contact
  analyser.
- Protein-protein interface analysis across chain pairs.
- DNA / RNA-ligand contact analyser with intercalation / groove /
  phosphate classification.
- Interactive 3Dmol.js viewer with click-to-inspect (picked residue
  bounces back to Qt via QWebChannel), cartoon / trace / surface
  styles, auto-rotation export, and a 2D PoseView-style interaction
  map exporter.

### Compare
Drop any molecules into slots, get a side-by-side descriptor +
structure comparison.

![Compare tab](screenshots/tour/11_compare.png)

### Glossary
~50 searchable terms across bonding, stereochem, mechanism,
reactions, synthesis, spectroscopy, lab-technique, and enzyme-
mechanism categories. 15 anchor terms ship with example SMILES
rendered on click via the *View figure* button.

![Glossary tab](screenshots/tour/13_glossary.png)

### Tools menu
A single-click path to every core capability, each as its own
dialog:

| Menu item                                 | Closes                                   |
|-------------------------------------------|------------------------------------------|
| Empirical / Molecular Formula Calculator… | Verma 2024 Section A                     |
| HRMS formula candidate guesser…           | Phase 4 MS candidate enumerator          |
| EI-MS fragmentation sketch…               | Common-neutral-loss predictor            |
| Retrosynthesis…                           | 8 SMARTS templates + multi-step tree     |
| Orbitals (Hückel / W-H)…                  | Hückel MOs + Woodward-Hoffmann rules     |
| Lab techniques…                           | TLC / recrystallisation / distillation / extraction |
| Medicinal chemistry (SAR / Bioisosteres)… | Seeded SAR series + bioisostere suggester |
| IUPAC naming rules…                       | 22-rule catalogue browser                |
| Periodic table…                           | Clickable 118-element table              |
| Spectroscopy (IR / NMR / MS)…             | Stick-spectrum predictor + save          |
| Stereochemistry…                          | R/S + E/Z table with Flip + Mirror       |
| Green metrics (atom economy)…             | Reaction AE + pathway overall AE         |

### Conformational dynamics
Rotatable-bond dihedral scans and conformer morphs render as
interactive HTML trajectories through the Phase 2c.2 3Dmol.js
player.

![Butane dihedral scan (interactive HTML)](screenshots/dynamics_butane.html)

### Molecule browser: multi-category filters (Phase 28)
Two rolling combo boxes over the tag taxonomy (functional group /
source / composition / charge / size / ring count / has-stereo) AND
together with the free-text field. Each seeded molecule is auto-
tagged with SMARTS-based functional groups and hand-curated
source / drug-class labels (NSAID, statin, alkaloid, hormone,
steroid, fatty acid, …).

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

For developer tooling (tests / ruff / mypy / pre-commit):

```bash
pip install -r requirements-dev.txt
pre-commit install   # optional: ruff + mypy on every commit
pytest tests/
```

## Headless / LLM-driven operation

Every GUI action is also an agent action via the `@action` registry.
Drive the app from Python:

```python
from orgchem.agent.headless import HeadlessApp
with HeadlessApp() as app:
    app.call("fetch_pdb", pdb_id="2YDO")
    app.call("analyse_binding", pdb_id="2YDO", ligand_name="CAF")
    app.call("export_interaction_map",
             pdb_id="2YDO", ligand_name="CAF",
             path="caffeine_a2a.png")
```

Or from any external process (including a Claude Code session) via
the JSON-over-stdio bridge:

```bash
python main.py --agent-stdio
# then write one JSON request per line, read one JSON response per line
```

## Project orientation

- [`INTERFACE.md`](INTERFACE.md) — navigation map for the codebase. **Read this first.**
- [`CLAUDE.md`](CLAUDE.md) — coding rules enforced by the project.
- [`PROJECT_STATUS.md`](PROJECT_STATUS.md) — what works *today*, with
  metrics and known issues.
- [`ROADMAP.md`](ROADMAP.md) — phased plan through v1.0 and beyond.
- [`SESSION_LOG.md`](SESSION_LOG.md) — rolling development log across
  40+ autonomous-loop rounds.

## Requires
Python 3.11+, RDKit, PySide6 (with QtWebEngine + QtWebChannel),
SQLAlchemy, PubChemPy, platformdirs, PyYAML. See `requirements.txt`
for the full list; `requirements-dev.txt` adds pytest / ruff / mypy
/ pytest-qt / imagehash.

## Reference
Empirical → molecular-formula calculation reimplements and extends
Verma, Singh & Passey, *Rasayan J. Chem.* 17(4): 1460–1472 (2024),
exposed as both a library call (`orgchem/core/formula.py`) and a
Tools menu dialog.

## Status
- **642 tests + 1 skipped** across the full suite (2026-04-23).
- **100 % GUI coverage** of the agent-action registry (102/102
  actions reachable from a menu, panel, or dialog — guard-rail
  pinned in `tests/test_gui_audit.py`).
- All autonomous-loop rounds documented in
  [`SESSION_LOG.md`](SESSION_LOG.md).
- User-flagged roadmap items complete through Phase 29a; Phase 29b
  (Carbohydrates / Lipids / Nucleic-acid tabs) in flight.
