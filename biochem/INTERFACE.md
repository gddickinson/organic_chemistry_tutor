# Biochemistry Studio — Interface Map

Read this file FIRST before opening any source file in `biochem/`.

> **Phase BC-1.0 (round 213, 2026-04-26)** — second sibling in
> the multi-studio life-sciences platform (after Cell Bio
> Studio in round 212). Sibling package to `orgchem/` and
> `cellbio/`; shares the same process, agent registry, SQLite
> DB, and global glossary.  Validates the cross-studio data-
> sharing pattern: the *Metabolic pathways* tab in Biochem
> surfaces `orgchem.core.metabolic_pathways` read-only without
> any orgchem refactor.

## Top-level

| Path | Purpose |
|------|---------|
| `biochem/__init__.py` | Importing the package registers all biochem agent actions into the shared `orgchem.agent.actions._REGISTRY`. |
| `biochem/INTERFACE.md` | This file. |
| `biochem/core/` | Pure-data catalogues (no Qt). |
| `biochem/agent/` | `@action`-decorated functions that land in the shared registry. |
| `biochem/gui/` | Qt main window + panels. |
| `biochem/tutorial/` | Biochem-specific tutorial curriculum + content. |

## Package: `biochem/`

### `core/` — data catalogues (no GUI imports)

| File | Key symbols |
|------|-------------|
| `enzymes.py` | **Phase BC-1.0** — `Enzyme` frozen dataclass + `EC_CLASSES` (1-7) + `EC_CLASS_NAMES` map + lookup helpers (`list_enzymes(ec_class, ec_class_name)` / `get_enzyme(id)` / `find_enzymes(needle)` / `enzymes_for_ec_class(ec_class)` / `ec_class_of(enzyme)` / `enzyme_to_dict(e)`). |
| `enzymes_data.py` | The 30-entry catalogue spanning all 7 EC classes — 5 oxidoreductases (alcohol DH, lactate DH, GAPDH, complex IV, CYP3A4-rep), 5 transferases (hexokinase, PKA, EGFR-TK, COMT, UGT), 6 hydrolases (chymotrypsin, trypsin, HIV protease, caspase-3, ACE, lysozyme), 4 lyases (aldolase, carbonic anhydrase, adenylate cyclase, pyruvate decarboxylase), 3 isomerases (TIM, phosphoglycerate mutase, cyclophilin A), 4 ligases (DNA ligase, glutamine synthetase, pyruvate carboxylase, ACC), 3 translocases (Na+/K+-ATPase, F1F0-ATP synthase, P-glycoprotein). Each entry carries: EC number, mechanism class, substrates, products, cofactors, regulators, disease associations, drug targets, cross-references to OrgChem `Molecule` rows + OrgChem metabolic-pathway ids + Cell Bio signalling-pathway ids — sets up the cross-studio link audit. |
| `cofactors.py` + `cofactors_data.py` | **Phase BC-2.0 (round 219)** — 27-entry deep-phase catalogue covering all canonical biochem cofactor classes: nicotinamide (NAD+/H, NADP+/H), flavin (FAD/H₂, FMN), acyl-carrier (CoA, acetyl-CoA), methyl-donor (SAM), phosphate-energy (ATP, ADP, cAMP, GTP), vitamin-derived prosthetic groups (biotin / TPP / PLP / lipoate / cobalamin / tetrahydrofolate), metal cofactors (heme / Mg²⁺ / Zn²⁺), quinone electron carriers (CoQ10 / plastoquinone), and redox-buffer small molecules (glutathione / ascorbate). `Cofactor` frozen dataclass + `COFACTOR_CLASSES` (14-tuple) + lookup helpers (`list_cofactors(cofactor_class)`, `get_cofactor(id)`, `find_cofactors(needle)`, `cofactors_for_class(cc)`, `cofactor_to_dict(c)`). **`__post_init__` validator raises `TypeError` if any tuple-typed field comes in as a plain `str`** — kills the trailing-comma single-element-tuple bug class that bit on CB-2.0 round 218 (caught at construction time, not test time). Each entry carries typed cross-references to existing BC-1.0 enzyme ids + OrgChem metabolic-pathway ids + OrgChem `Molecule` rows by exact name. Pure-headless. |

### `agent/` — agent actions

| File | Key symbols |
|------|-------------|
| `actions_enzymes.py` | **Phase BC-1.0** — 5 agent actions in the new `biochem-enzymes` category: `list_enzymes(ec_class="")` / `get_enzyme(enzyme_id)` / `find_enzymes(needle)` / `enzymes_for_ec_class(ec_class)` / `open_biochem_studio(tab="")` (opens the Biochem main window + optionally focuses a tab). Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread via `orgchem.agent._gui_dispatch.run_on_main_thread_sync`. |
| `actions_cofactors.py` | **Phase BC-2.0 (round 219)** — 5 agent actions in the new `biochem-cofactors` category: `list_cofactors(cofactor_class="")` / `get_cofactor(cofactor_id)` / `find_cofactors(needle)` / `cofactors_for_class(cofactor_class)` / `open_biochem_cofactors_tab()` (opens the Biochem main window + focuses the Cofactors tab). Same dispatcher pattern as the BC-1.0 opener. |

### `gui/` — Qt UI

- `windows/biochem_main_window.py` — `BiochemMainWindow(QMainWindow)`. Single persistent instance opened from OrgChem main window's *Window → Biochem Studio…* menu (Ctrl+Shift+Y). Same lifecycle pattern as the Phase-30 Macromolecules window + Phase-CB-1.0 Cell Bio window. Three tabs: `Enzymes`, `Metabolic pathways`, `Tutorials`. Programmatic: `switch_to(tab_label)`. Geometry persists via `QSettings["window/biochem"]`.
- `panels/enzymes_panel.py` — `EnzymesPanel(QWidget)`. EC-class combo + free-text filter + list + HTML detail card showing EC number / mechanism class / substrates / products / cofactors / regulators / disease associations / drug targets / cross-references to OrgChem pathways + Cell Bio signalling. `select_enzyme(enzyme_id)` programmatic API.
- `panels/metabolic_bridge_panel.py` — **The architectural validation.** Surfaces `orgchem.core.metabolic_pathways` read-only inside Biochem Studio. Demonstrates that sibling studios can share data without refactor — pathway entries live in OrgChem; Biochem reads them. A *Open in OrgChem Tools menu…* button hands off to the existing OrgChem dialog for full editing.
- `panels/biochem_tutorial_panel.py` — Reads `biochem.tutorial.curriculum.CURRICULUM`; same pattern as cellbio's tutorial panel.

### `tutorial/`

| File | Key symbols |
|------|-------------|
| `curriculum.py` | `CURRICULUM` dict. Phase BC-1.0 ships 1 starter beginner lesson. |
| `loader.py` | `load_lesson(path)` — markdown reader. |
| `content/beginner/01_welcome_biochem.md` | Welcome lesson — what biochemistry covers, what ships in BC-1.0, how the bridge panel + cross-references work, where the studio is heading. |

## Cross-studio integration

| Hook | OrgChem side | Biochem side |
|------|--------------|--------------|
| Window menu entry | `orgchem.gui.main_window.MainWindow._build_menu()` adds "Biochem Studio…" (Ctrl+Shift+Y) | `biochem.gui.windows.biochem_main_window.BiochemMainWindow` |
| Headless registration | `orgchem.agent.headless.HeadlessApp.__init__` imports `biochem` after `cellbio` | `biochem/__init__.py` triggers `biochem.agent.actions_enzymes` import |
| Bus | `orgchem.messaging.bus.bus()` | Biochem panels use the same singleton |
| Agent registry | `orgchem.agent.actions._REGISTRY` | Biochem actions register here |
| **Data sharing** | `orgchem.core.metabolic_pathways` (Phase 42, 11 pathways) | **`metabolic_bridge_panel.py` reads this directly** — no copy, no refactor |
| GUI audit | `orgchem.gui.audit.GUI_ENTRY_POINTS` extended | Biochem actions added under "# === Biochem Studio ===" |
| Agent surface audit | `orgchem.core.agent_surface_audit.EXPECTED_SURFACES` extended | Biochem adds the Enzymes catalogue surface |

## Cross-studio cross-references (typed edges)

Each enzyme can carry up to three families of cross-reference:

| Edge | Example |
|------|---------|
| enzyme → orgchem-molecule | Hexokinase → Glucose, ATP, ADP |
| enzyme → orgchem-pathway-id | Hexokinase → "glycolysis" (orgchem.core.metabolic_pathways id) |
| enzyme → cellbio-signaling-pathway-id | EGFR-TK → "egfr-ras-raf" (cellbio.core.cell_signaling id) |

These are validated at test time so a future rename in any studio surfaces the broken edge immediately.

## Inter-studio rules (forward-looking)

- **OrgChem owns**: small-molecule chemistry, named reactions, retrosynthesis, **metabolic pathways for now** (Biochem reads them but doesn't redefine).
- **Cell Bio owns**: cellular structures, signalling pathways, cytoskeleton, motors, transporters.
- **Biochem owns**: enzymes (EC catalogue), cofactors, biochemical kinetics, biopolymer sequences.
- **Migration of metabolic pathways from OrgChem → Biochem** is deferred to Phase BC-3 or later; the bridge panel pattern lets us defer indefinitely with no functional cost.

## Adding to Biochem (checklist)

1. New catalogue → `biochem/core/<name>.py` with frozen dataclass + `_<NAME>` list + lookup helpers + `to_dict`.
2. New agent actions → `biochem/agent/actions_<name>.py` with `@action(category="biochem-<name>")`.
3. Add the import to `biochem/__init__.py`.
4. New panel → `biochem/gui/panels/<name>_panel.py`. Add a tab in `BiochemMainWindow.__init__`.
5. Add an entry to `orgchem/gui/audit.py::GUI_ENTRY_POINTS` for each new action.
6. Add the catalogue to `orgchem/core/agent_surface_audit.py::EXPECTED_SURFACES`.
7. Add a category summary to `orgchem/agent/actions_meta.py::_CATEGORY_SUMMARIES`.
8. Tests in `tests/test_biochem_<name>.py`.
9. Update this file.
