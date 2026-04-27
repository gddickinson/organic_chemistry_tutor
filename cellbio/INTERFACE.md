# Cell Biology Studio — Interface Map

Read this file FIRST before opening any source file in `cellbio/`.

> **Phase CB-1.0 (round 212, 2026-04-26)** — first slice of a
> planned 6-studio life-sciences platform. Sibling package to
> `orgchem/`; shares the same process, agent registry, SQLite DB,
> and global glossary. No refactor of `orgchem/` — `cellbio/`
> imports from it where useful (bus, agent registry, GUI dispatch).

## Top-level

| Path | Purpose |
|------|---------|
| `cellbio/__init__.py` | Importing the package registers all cellbio agent actions into the shared `orgchem.agent.actions._REGISTRY`. |
| `cellbio/INTERFACE.md` | This file. |
| `cellbio/core/` | Pure-data catalogues (no Qt). |
| `cellbio/agent/` | `@action`-decorated functions that land in the shared registry. |
| `cellbio/gui/` | Qt main window + panels + dialogs (cell-bio-specific). |
| `cellbio/tutorial/` | Cell-bio-specific tutorial curriculum + content. |

## Package: `cellbio/`

### `core/` — data catalogues (no GUI imports)

| File | Key symbols |
|------|-------------|
| `cell_signaling.py` | **Phase CB-1.0** — 25-entry catalogue of canonical cell-signalling pathways (MAPK/ERK, PI3K/Akt/mTOR, JAK/STAT, Wnt, Notch, Hedgehog, NF-κB, TGF-β, GPCR-cAMP-PKA, GPCR-IP₃-Ca²⁺, TLR, cGAS-STING, Hippo-YAP, AMPK, HIF-1α, p53, intrinsic + extrinsic apoptosis, necroptosis, pyroptosis, mTORC1 amino-acid sensing, insulin, EGFR-RAS-RAF, TCR, CaMKII, PKC). `SignalingPathway` frozen dataclass + `CATEGORIES` + `RECEPTOR_CLASSES` enums + lookup helpers (`list_pathways(category)`, `get_pathway(id)`, `find_pathways(needle)`, `pathways_by_receptor_class(rc)`, `pathway_to_dict(p)`). Each entry carries cross-references to `orgchem` molecule names (`cross_reference_molecule_names`) + sister cellbio pathways (`cross_reference_pathway_ids`) — sets up the multi-studio link audit. Pure-headless. |
| `cell_cycle.py` + `cell_cycle_data.py` | **Phase CB-2.0 (round 218)** — 30-entry deep-phase catalogue covering all 5 cell-cycle phases (G1/S/G2/M/G0), all 4 checkpoints (G1/S restriction, intra-S, G2/M, spindle assembly), the 4 canonical cyclin-CDK pairs (D-CDK4/6, E-CDK2, A-CDK2/1, B-CDK1), CIP/KIP + INK4 inhibitors (p21, p27, p16), the Rb/E2F axis, mitotic regulators (Wee1/Myt1, Cdc25, APC/C, Separase/Securin, Aurora kinases, Plk1, SAC components Mad2/BubR1/Bub1/Mps1, condensin/cohesin), and the DNA-damage-response kinases (ATM, ATR, Chk1/Chk2, BRCA1/2, p53). `CellCycleEntry` frozen dataclass + `CATEGORIES` (7-tuple) + lookup helpers (`list_cell_cycle_entries(category)`, `get_cell_cycle_entry(id)`, `find_cell_cycle_entries(needle)`, `cell_cycle_entries_for_category(c)`, `cell_cycle_entry_to_dict(e)`). Each entry carries typed cross-references to existing CB-1.0 signalling pathway ids + Pharm drug-class ids (kinase-inhibitors, taxanes, platinum-chemotherapy). Pure-headless; data file split for the 500-line cap. |

### `agent/` — agent actions

| File | Key symbols |
|------|-------------|
| `actions_signaling.py` | **Phase CB-1.0** — 4 agent actions in the new `cellbio-signaling` category: `list_signaling_pathways(category="", receptor_class="")` / `get_signaling_pathway(pathway_id)` / `find_signaling_pathways(needle)` / `open_cellbio_studio(tab="")` (opens the Cell Bio main window + optionally focuses a tab). Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread via `orgchem.agent._gui_dispatch.run_on_main_thread_sync`. |
| `actions_cell_cycle.py` | **Phase CB-2.0 (round 218)** — 5 agent actions in the new `cellbio-cell-cycle` category: `list_cell_cycle_entries(category="")` / `get_cell_cycle_entry(entry_id)` / `find_cell_cycle_entries(needle)` / `cell_cycle_entries_for_category(category)` / `open_cellbio_cell_cycle_tab()` (opens the Cell Bio main window + focuses the Cell-cycle tab). Same dispatcher pattern as the signalling opener. |

### `gui/` — Qt UI

- `windows/cellbio_main_window.py` — `CellBioMainWindow(QMainWindow)`. Single persistent instance opened from OrgChem main window's *Window → Cell Biology Studio…* menu. Same lifecycle pattern as the Phase-30 Macromolecules window (lazily constructed, raise/focus on subsequent calls, geometry persisted via `QSettings["window/cellbio"]`). Tabs (CB-1.0 + CB-2.0): `Signalling`, `Cell cycle`, `Tutorials`. Programmatic: `switch_to(tab_label)`. `TAB_*` constants exposed for consumers.
- `panels/signaling_panel.py` — `SignalingPanel(QWidget)`. Category combo + receptor-class combo + free-text filter + list + HTML detail card showing key components / function / disease associations / drug targets / cross-references / notes. `select_pathway(pathway_id)` programmatic API.
- `panels/cell_cycle_panel.py` — **Phase CB-2.0** `CellCyclePanel(QWidget)`. Category combo (7 options) + free-text filter + list + HTML detail card showing summary / function / activator-inhibitor lists / disease associations / cross-references. `select_entry(entry_id)` programmatic API.
- `panels/cellbio_tutorial_panel.py` — `CellBioTutorialPanel(QWidget)`. Reads `cellbio.tutorial.curriculum.CURRICULUM`; displays a tree of lessons + a markdown reader. Same pattern as OrgChem's tutorial panel but bound to cellbio's curriculum.

### `tutorial/`

| File | Key symbols |
|------|-------------|
| `curriculum.py` | `CURRICULUM` dict (level → list of lessons). Phase CB-1.0 ships with 1 starter beginner lesson. |
| `content/beginner/01_welcome_cellbio.md` | Welcome lesson — what cell biology is, the five pillars, how to navigate the studio, how it cross-references OrgChem + the planned Biochem / Pharmacology / Microbiology / Botany / Animal Biology studios. |

## Cross-studio integration

How Cell Bio integrates with OrgChem:

| Hook | OrgChem side | Cell Bio side |
|------|--------------|---------------|
| Window menu entry | `orgchem.gui.main_window.MainWindow._build_menu()` adds "Cell Biology Studio…" (Ctrl+Shift+B) | `cellbio.gui.windows.cellbio_main_window.CellBioMainWindow` |
| Headless registration | `orgchem.agent.headless.HeadlessApp.__init__` imports `cellbio` so the registry sees signalling actions | `cellbio/__init__.py` triggers `cellbio.agent.actions_signaling` import |
| Bus | `orgchem.messaging.bus.bus()` | Cell Bio panels use the same singleton |
| Agent registry | `orgchem.agent.actions._REGISTRY` | Cell Bio actions register here |
| GUI audit | `orgchem.gui.audit.GUI_ENTRY_POINTS` extended | Cell Bio actions added under "# === Cell Biology Studio ===" |
| Agent surface audit | `orgchem.core.agent_surface_audit.EXPECTED_SURFACES` extended | Cell Bio adds the Signalling-pathway surface |

## Inter-studio rules (forward-looking)

- Each studio has exactly one **canonical owner** for each topic (see ROADMAP.md). Cell Bio owns: cell components, cell cycle, signalling, cytoskeleton, motors, transporters, receptors, cell types, junctions, adhesion, apoptosis, autophagy, condensates, mechanobio.
- OrgChem owns: small-molecule chemistry, named reactions, retrosynthesis. Cell Bio cross-references these by name.
- Future Biochem owns: enzymes (with mechanism), metabolic pathways. Cell Bio currently overlaps (Phase 42 metabolic pathways still live in orgchem); will migrate to Biochem when that studio stands up.

## Adding to Cell Bio (checklist)

1. New catalogue → `cellbio/core/<name>.py` with frozen dataclass + `_<NAME>` list + lookup helpers + `to_dict`.
2. New agent actions → `cellbio/agent/actions_<name>.py` with `@action(category="cellbio-<name>")`.
3. Add the import to `cellbio/__init__.py` so registration fires on package import.
4. New panel → `cellbio/gui/panels/<name>_panel.py`. Add a tab in `CellBioMainWindow.__init__`.
5. Add an entry to `orgchem/gui/audit.py::GUI_ENTRY_POINTS` for each new action.
6. Add the catalogue to `orgchem/core/agent_surface_audit.py::EXPECTED_SURFACES`.
7. Tests in `tests/test_cellbio_<name>.py`.
8. Update this file.
