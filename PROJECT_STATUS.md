# Project Status — OrgChem Studio

> Living document. Update at the end of every meaningful session.
> Last updated: **2026-04-23** (round 43 — Phase 29b Lipids + 29c Nucleic-acids tabs shipped)

## Current phase
**Phases 1, 2a, 2b, 2c.1, 2c.2, 3a, 3b, 6a (partial), 8a–c, 10a, 11a/b/d
(partial), 13a/b/d/e, 14a (partial), 15a/b/c (partial), 17a, 18a, 19b
(partial) complete, plus the cross-cutting stereochemistry layer.** The
app now covers seven independent layers of organic chemistry information
for every seeded reaction — 2D scheme → 3D side-by-side → 3D trajectory
animation → arrow-pushing mechanism → reaction-coordinate energy profile
→ atom-economy metrics → stereo descriptors. Plus a searchable
**Glossary tab** (43 terms), a **Hückel MO** engine with level-diagram
renderer, drug-likeness analysis (Lipinski/Veber/Ghose/PAINS/QED), TLC
Rf predictor, recrystallisation/distillation/acid-base-extraction
helpers, and R/S + E/Z wedge/dash 2D rendering. **210 molecules**, 26
reactions, 9 mechanisms, 11 synthesis pathways, 9 energy profiles, 43
glossary terms. Future phases 9 (docking), 10b (OpenMM MD), 13c
(full-kinetics composite), 12 (IUPAC nomenclature), 14b (orbital
isosurfaces), 15d (characterisation), 16 (bio-organic), 17b-e / 18b-e /
19a/c-e are scoped. **667 tests pass + 1 skipped** (round 43, +16
new from Phase 29b Lipids tab (21-entry catalogue — fatty acids,
triglycerides, phospholipids, sphingolipids, sterols, fat-soluble
vitamins / hormones) and Phase 29c Nucleic-acids tab (23-entry
catalogue — bases, nucleosides, nucleotides, short oligos +
canonical PDB motifs 1BNA / 1EHZ / 143D / 1HMH). Both panels mirror
the Carbohydrates tab pattern (family combo + free-text filter +
entry list + 2D SVG viewer + meta pane); NA panel's PDB-motif rows
expose a *Fetch PDB in Proteins tab* button. GUI coverage remains
**100.0 %** (108 / 108 actions wired). User directive logged
mid-round: all macromolecule surfaces should be unified into a
separate window opened from a menu item — captured as Phase 30.

## What works today

### Data & chemistry
- SQLite database auto-created per user (platformdirs-aware path).
- Seeded with 20 molecules on first run: 5 beginner basics + all 15 Verma
  et al. 2024 reference compounds (Nicotine … Cocaine).
- RDKit-backed `Molecule` wrapper: canonical SMILES, InChI, InChIKey,
  Hill-ordered formula, MMFF-optimised 3D conformers, Lipinski descriptors.
- Empirical → molecular formula calculator using **IUPAC 2019 atomic
  masses by default** (robust algorithm; see `core/formula.py`). Integer
  masses available via `ATOMIC_MASSES_INTEGER` for paper reproduction.

### GUI (PySide6)
- Dockable / tabbed main window with full menu bar + status bar.
- 2D viewer — RDKit SVG rendering with style selector (skeletal / atom
  indices / explicit hydrogens / Kekulé).
- 3D viewer — QWebEngineView + 3Dmol.js with style selector (stick /
  ball-and-stick / sphere / line).
- Molecule browser, Properties table, Session log, Online search (PubChem),
  Tutorial tree, Import-SMILES dialog, Formula Calculator dialog.
- Tutor chat console dock — detachable into a floating window.

### LLM / agent layer (the "Claude can drive the GUI" feature)
- Typed action registry with auto-emitted Anthropic / OpenAI tool schemas.
- 9 built-in actions (list_all_molecules, show_molecule, import_smiles,
  get_molecule_details, calculate_empirical_formula, search_pubchem,
  download_from_pubchem, list_tutorials, open_tutorial).
- Three drivers sharing the same registry:
  - **In-app chat console** (Anthropic / OpenAI / Ollama backends)
  - **Headless Python** (`from orgchem.agent.headless import HeadlessApp`)
  - **Stdio subprocess** (`python main.py --agent-stdio`) — the path any
    external LLM (incl. a Claude Code session) uses.
- Pluggable LLM backends: Anthropic Claude, OpenAI-compatible
  (Azure / DeepSeek / Groq / …), Ollama (local models).

### Tutorials
- Curriculum tree: beginner / intermediate / advanced / graduate, 17
  lesson slots.
- Markdown loader with graceful "content pending" fallback.
- One completed sample lesson: `beginner/01_welcome.md`.

### Image export & screenshots
- 2D structures → PNG / JPG / SVG (file-extension dispatch).
  `File → Export current molecule (2D)…` (Ctrl+E) in the GUI.
- Any Qt widget → PNG via `QWidget.grab()`. `File → Screenshot window…`
  (Ctrl+Shift+P) in the GUI.
- Both exposed as agent actions (`export_molecule_2d_by_id`,
  `screenshot_window`, `screenshot_panel` with friendly panel aliases).
- `scripts/visual_tour.py` produces a 22-file gallery of canonical states
  for regression eyeballing.

### Reactions (Phase 2a)
- 16 named reactions seed the DB on first launch (SN1, SN2, E1, E2,
  Diels-Alder, aldol, Grignard, Friedel-Crafts alkylation/acylation,
  Fischer esterification, amide formation, hydrogenation, bromination,
  nitration, PCC oxidation, NaBH4 reduction).
- **Reactions tab** — filterable list + rendered scheme (RDKit
  `MolDraw2DSVG.DrawReaction`) + description + SVG/PNG export.
- Agent actions: `list_reactions`, `show_reaction`, `export_reaction_by_id`.

### Mechanism arrow-pushing player (Phase 2b)
- `core/mechanism.py` — `Mechanism` / `MechanismStep` / `Arrow` dataclasses
  with JSON round-trip. Stored in `Reaction.mechanism_json`.
- `render/draw_mechanism.py` — RDKit SVG + `GetDrawCoords()` overlays
  curved red bezier arrows between atoms (curly or fishhook).
- **7 mechanisms** seeded: SN1 (4 steps), SN2 (2 steps), E1 (3 steps),
  E2 (2 steps), Diels-Alder (2 steps), Aldol (3 steps), Grignard (3 steps).
  Atom-index-keyed arrows encode the canonical textbook electron-flow
  picture for each.
- **Play mechanism button** on the Reactions tab — enabled for reactions
  with `mechanism_json`; opens a Prev / Next player dialog.
- Agent actions: `list_mechanisms`, `open_mechanism`, `export_mechanism_step`.
- `SEED_VERSION` constant so seed-data changes roll out automatically
  without a migration script.

### 3D reaction display — side-by-side (Phase 2c.1)
- `render/draw_reaction_3d.py` — given an atom-mapped reaction SMARTS,
  embed reactant + product in 3D, render them in one figure with a
  forward arrow between, colour atoms by map number so identity is
  preserved across the arrow, highlight broken/formed bonds red/green.
- **6 reactions** have atom-mapped SMARTS seeded (SN2, SN1, bromination,
  catalytic hydrogenation, PCC oxidation, NaBH4 reduction). New schema
  column `Reaction.reaction_smarts_mapped`; on-startup additive migration
  adds the column to existing databases without Alembic.
- **Render 3D… button** on the Reactions tab, enabled when a mapped
  SMARTS is present.
- Agent action `export_reaction_3d(reaction_id, path)`.

### Conformational dynamics (new — Phase 10a)
- `orgchem/core/dynamics.py` — no-deps-added module that produces
  teaching-scale animations via two strategies:
  - **Dihedral scan**: rotate a named torsion 0°→360° with MMFF
    relaxation (and a torsion constraint) at each step. Physically
    meaningful conformational-barrier walk.
  - **Conformer morph**: embed N diverse conformers (ETKDG), sort by
    MMFF energy, align, and linearly interpolate. Handles ring flips
    where a single dihedral-scan wouldn't capture the whole motion.
- Multi-frame XYZ output plugs straight into the Phase 2c.2
  `build_trajectory_html` 3Dmol.js player → play/pause/reset/speed for
  free.
- **▶ Run dynamics…** button on the 3D viewer panel; opens
  `DynamicsPlayerDialog` — user picks mode (and rotatable bond if
  scanning). Save-HTML for classroom handouts.
- Pedagogical seeds: butane gauche/anti, ethane torsion, cyclohexane
  ring flip — all accessible via `run_dihedral_scan_demo`.
- Agent actions: `run_dihedral_scan_demo`, `run_molecule_dihedral`,
  `run_molecule_conformer_morph`.

### Synthesis pathways (new — Phase 8)
- New DB tables `synthesis_pathways` and `synthesis_steps`; created
  automatically by `Base.metadata.create_all` for both new and
  existing databases.
- `orgchem/db/seed_pathways.py` — 6 seeded classics: Wöhler urea
  (1828, historic), Aspirin (Kolbe/Bayer 1897), Paracetamol (industrial
  N-acetylation), **BHC Ibuprofen (3 steps, green-chemistry award-winner)**,
  Caffeine by N-methylation of theobromine, Phenacetin → Paracetamol
  (metabolic / historic). Each step has reactants, reagents, conditions,
  yield (where known), and a teaching note.
- `orgchem/render/draw_pathway.py` — composite SVG (`build_svg`) + PNG/SVG
  export. Vertical stack of step schemes; each step has a number label,
  reagents text above the arrow, the embedded reaction scheme (outer
  `<svg>` wrapper stripped for Qt compatibility), conditions/yield below,
  and a separator line.
- `orgchem/gui/panels/synthesis_workspace.py` — **new Synthesis tab**:
  filterable list of pathways on the left, scrollable SVG viewer on
  the right with target name, description, and per-step rendering.
- Agent actions: `list_pathways`, `show_pathway`, `export_pathway`.
- 8 tests in `tests/test_pathways.py`.

### 3D reaction animation (new — Phase 2c.2)
- `core/reaction_trajectory.py` — given an atom-mapped SMARTS, embeds
  reactant + product, Kabsch-aligns product onto reactant, linearly
  interpolates *N* frames of atom positions, emits multi-frame XYZ.
- `render/draw_reaction_3d.build_trajectory_html` — wraps the XYZ in a
  self-contained 3Dmol.js page with play / pause / reset / speed
  controls. 3Dmol's `addModelsAsFrames` + `animate()` handles playback;
  bonds are inferred by proximity each frame, so bonds appear /
  disappear as atoms move through the transition state.
- `gui/dialogs/reaction_trajectory_player.py` — modal QWebEngineView
  host. **▶ Animate 3D button** on the Reactions tab.
- Agent actions: `export_reaction_trajectory_html` (disk, suitable for
  classroom slideshows) and `play_reaction_trajectory` (in-app modal).

### Window ergonomics + persistence (new)
- Default window: **1280×780** (was 1500×950) with 960×640 minimum —
  fits on a 13"/14" MBP.
- Panel minimums dropped to 280×280 so the user can compact further.
- Bottom log dock starts at 110 px (was auto-sized to ~180).
- `QSettings` round-trips `saveGeometry()` / `saveState()` on
  `closeEvent`, restored in `__init__`. User's resized / re-docked
  layout persists.

### Headless 3D (Phase 3a + polish)
- Matplotlib renderer with CPK colours; styles: ball-and-stick, sphere
  (both render real shaded spheres via per-atom `plot_surface`), plus
  stick and line. Works in any Qt platform mode including offscreen
  Chromium. `export_molecule_3d` agent action + *Save PNG…* button on
  the 3D viewer.
- User-selectable as the active 3D backend in `Tools → Preferences…`
  (default remains the interactive 3Dmol.js viewer).

### Compare tab (new — Phase 3b)
- 2×2 grid of molecule slots. Per-slot SMILES entry with live validation;
  `compare_molecules([id1, id2, ...])` agent action pre-populates. Each
  slot shows the 2D structure + formula / MW / logP / TPSA / ring count /
  HBD-HBA.

### Preferences (new)
- `Tools → Preferences…` (Ctrl+,) opens a settings dialog for default 3D
  backend, default 3D style, theme, log level, autogen-3D-on-import, and
  online-sources toggle. Saves to YAML + emits `bus.config_changed` so
  open panels re-render immediately.

### Tutorial content
- Six lessons now populated: beginner *Welcome*, *Atoms Bonds &
  Hybridisation*, *Lewis and Skeletal Structures*, *Functional Groups*;
  intermediate *SN1 vs SN2*, *E1 vs E2*. Other 11 lesson slots still
  show "content pending".

## Health metrics

| Metric                                         | Value           |
|------------------------------------------------|-----------------|
| Molecules seeded                               | **332** (210 main + 122 intermediate) |
| Reactions seeded                               | 28 (incl. 2 enzyme reactions) |
| Mechanisms seeded                              | 11 (SN1/SN2/E1/E2/DA/Aldol/Grignard/Wittig/Michael + chymotrypsin + aldolase) |
| Reactions with atom-mapped SMARTS              | 6               |
| **Synthesis pathways seeded**                  | **12** (7 multi-step, incl. Fmoc SPPS 5-step for Met-enkephalin) |
| **Energy profiles seeded**                     | **4** (SN2, SN1, E1, Diels-Alder) |
| **Glossary terms seeded**                      | **43** (across 7 categories) |
| File-size cap                                  | 500 lines (all ✓) |
| Formula unit tests passing                     | 10 / 10         |
| Headless end-to-end smoke tests passing        | 4 / 4           |
| Screenshot / export tests passing              | 7 / 7           |
| Reaction tests passing                         | 8 / 8           |
| Headless 3D (matplotlib) tests passing         | 7 / 7           |
| Mechanism tests passing                        | 8 / 8           |
| 3D reaction render tests passing               | 5 / 5           |
| Reaction trajectory tests passing              | 10 / 10         |
| Synthesis pathway tests passing                | 9 / 9           |
| Conformational-dynamics tests passing          | 9 / 9           |
| Compare panel tests passing                    | 5 / 5           |
| Energy-profile tests passing                   | 13 / 13         |
| **Green-metrics tests passing**                | **15 / 15**     |
| **Hückel MO tests passing**                    | **16 / 16**     |
| **Stereochemistry tests passing**              | **18 / 18**     |
| **Glossary tests passing**                     | **11 / 11**     |
| Drug-likeness / TLC tests passing              | 18 / 18         |
| Lab-techniques tests passing                   | 15 / 15         |
| Naming-rule tests passing                      | 13 / 13         |
| **Fragment-consistency tests passing**         | **12 / 12**     |
| **Total tests passing**                        | **238 / 238**   |
| Full `pytest tests/` runtime (warm)            | ~5 s            |
| Dependencies installed & confirmed working     | rdkit 2026.3.1, PySide6 6.10.2, SQLAlchemy 2.0.31, pubchempy 1.0.5, matplotlib 3.9.1 |

## Verified runtime paths
- `python main.py` — GUI launches, DB seeds (40 molecules, 26 reactions,
  7 mechanisms, 6 pathways), 5 tabs render (Molecule Workspace,
  Tutorials, Reactions, Compare, **Synthesis**).
- `python main.py --headless` — offscreen Qt platform.
- `python main.py --agent-stdio` — JSON-per-line bridge handshake works.
- `python scripts/claude_drive_demo.py {direct|stdio}` — agent driving.
- `python scripts/visual_tour.py` — 56-file gallery covering main tabs,
  reactions, compare, matplotlib 3D renderings, 20 mechanism step SVGs,
  4 reaction scheme SVGs, 5 static 3D reaction renders, 3 interactive
  3D animation HTMLs, **6 synthesis-pathway PNGs**, and a Synthesis-tab
  full-window screenshot.
- `pytest tests/` — **67 / 67 pass** in ~4 s.

## Known issues / limitations
- Several Verma-set SMILES (notably the paper's Lycopene chain and
  Coronene/Corannulene) may need cleanup — RDKit canonicalises them on
  load, but visual parity with the paper's drawings should be spot-checked.
- `download_from_pubchem` needs an internet connection; no retries /
  rate-limiting yet.
- 3Dmol.js loads from CDN by default — no offline bundle yet.
- **3Dmol.js panel is blank in headless / offscreen mode** — Chromium's
  GPU is disabled for stability. Workaround: set `Tools → Preferences… →
  Default 3D backend` to `matplotlib` (works in any mode). The GUI-mode
  app with the default 3Dmol backend renders 3D interactively as usual.
- IUPAC naming (for a new user-imported molecule) falls back to PubChem or
  the SMILES; no local IUPAC namer.
- No automated UI pixel-diff tests yet (screenshots saved, not diffed).
- Tutorial content: 6 of 17 lessons written; the rest still show
  "content pending".
- Only 5 of the 16 seeded reactions have mechanisms (SN1, SN2, E1, E2,
  Diels-Alder). Roadmap item: fill in aldol, Grignard, Friedel-Crafts,
  etc.
- Mechanism arrows are atom-to-atom only — no bond-midpoint origins and
  no H-atom targets. Pedagogically close but imperfect (e.g. E2 "base
  takes β-H" arrow lands on the β-carbon, not the H).
- Qt's default SVG renderer doesn't have Greek glyphs — mechanism arrow
  labels use plain ASCII ("new bond", "pi shift") rather than "σ" / "π".

## Reference papers
- Verma, Singh, Passey (2024) — "Python Program for Structure and Molecular
  Formula of Organic Compounds", *Rasayan J. Chem.* 17(4):1460–1472.
  `refs/4325_pdf.pdf`. Section A reimplemented in
  `orgchem/core/formula.py`; the 15 compounds from Tables 2/3 seed the DB.

## How to verify the current state yourself
```bash
python -m compileall -q orgchem main.py tests scripts   # syntax check
pytest tests/ -v                                        # 13 tests, ~29 s
python scripts/claude_drive_demo.py direct              # end-to-end demo
```

## What updates this document
At the end of each session with meaningful progress, bump "Last updated",
move items out of **Known issues** as they're resolved, and sync the
Health metrics table with actual numbers from `pytest` / `wc -l`.
