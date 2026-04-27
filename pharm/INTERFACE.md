# Pharmacology Studio — Interface Map

Read this file FIRST before opening any source file in `pharm/`.

> **Phase PH-1.0 (round 214, 2026-04-26)** — third sibling in
> the multi-studio life-sciences platform (after Cell Bio
> Studio in round 212 + Biochem Studio in round 213). Sibling
> package to `orgchem/`, `cellbio/`, and `biochem/`; shares
> the same process, agent registry, SQLite DB, and global
> glossary.
>
> **Architectural validation (multi-hop):** Pharm Studio ships
> **two** bridge panels — one onto `biochem.core.enzymes`
> (drug-target enzymes) + one onto `cellbio.core.cell_signaling`
> (drug-target receptor pathways).  Demonstrates that the
> cross-studio data-sharing pattern works for any sibling pair,
> not just sibling-to-OrgChem.

## Top-level

| Path | Purpose |
|------|---------|
| `pharm/__init__.py` | Importing the package registers all pharm agent actions into the shared `orgchem.agent.actions._REGISTRY`. |
| `pharm/INTERFACE.md` | This file. |
| `pharm/core/` | Pure-data catalogues (no Qt). |
| `pharm/agent/` | `@action`-decorated functions. |
| `pharm/gui/` | Qt main window + panels. |
| `pharm/tutorial/` | Pharm-specific tutorial curriculum + content. |

## Package: `pharm/`

### `core/` — data catalogues (no GUI imports)

| File | Key symbols |
|------|-------------|
| `drug_classes.py` | **Phase PH-1.0** — `DrugClass` frozen dataclass + `TARGET_CLASSES` (GPCR / RTK / ion-channel / NHR / enzyme / transporter / antibody / nucleic-acid / cytoskeletal / other) + `THERAPEUTIC_AREAS` (cardiovascular / metabolic / neurology-psychiatry / oncology / infectious / inflammation-immunology / pulmonology / endocrinology / haematology / GI / pain) + lookup helpers (`list_drug_classes(target_class, therapeutic_area)` / `get_drug_class(id)` / `find_drug_classes(needle)` / `drug_classes_for_target(target_class)` / `drug_class_to_dict(d)`). |
| `drug_classes_data.py` | The 30-entry catalogue: cardiovascular (β-blockers, ACE inhibitors, ARBs, calcium-channel blockers, loop diuretics, thiazide diuretics, statins, anticoagulants — warfarin / DOACs / heparin), respiratory (β2-agonists), pain + inflammation (NSAIDs, opioids), psychiatry (SSRIs, benzodiazepines, atypical antipsychotics), neurology (antiepileptics), endocrinology (insulin, GLP-1 agonists, SGLT2 inhibitors), GI (PPIs), infectious (β-lactams, macrolides, fluoroquinolones, aminoglycosides, NRTIs, HIV protease inhibitors), oncology (platinum compounds, taxanes, kinase inhibitors, monoclonal antibodies — anti-PD-1 / anti-CD20). Each entry carries: mechanism, molecular target, typical agents, clinical use, common side effects, contraindications, monitoring, and **typed cross-references to OrgChem molecules + Biochem enzyme ids + Cell Bio signalling-pathway ids**. |
| `receptors.py` + `receptors_data.py` | **Phase PH-2.0 (round 220)** — 32-entry deep-phase receptor pharmacology catalogue covering all major drug-target receptor superfamilies: GPCRs (aminergic — β1/β2/α1 adrenergic, M3 muscarinic, D2 dopamine; peptide — μ-opioid, AT1 angiotensin, GLP-1, H1 histamine; cannabinoid CB1), nuclear hormone receptors (steroid — GR/ER/AR/PR; non-steroid — TR/VDR/PPARγ), receptor tyrosine kinases (EGFR, HER2, VEGFR2, insulin receptor), voltage-gated ion channels (Nav1.7, hERG, Cav1.2), ligand-gated (nAChR, GABA-A, NMDA), monoamine transporters (SERT, NET, DAT), other transporters (SGLT2, P-glycoprotein). `Receptor` frozen dataclass + `RECEPTOR_FAMILIES` (10-tuple) + lookup helpers. **`__post_init__` validator** raises `TypeError` on plain-string-in-tuple-field input — same pattern adopted across the -2 chain. Each entry carries 4-way cross-references: PH-1.0 drug-class ids + CB-1.0 signalling-pathway ids + BC-1.0 enzyme ids + OrgChem `Molecule` rows by exact name (Dopamine, Cortisol, Estradiol, etc.). Pure-headless. |

### `agent/` — agent actions

| File | Key symbols |
|------|-------------|
| `actions_drug_classes.py` | **Phase PH-1.0** — 5 agent actions in the new `pharm-drugs` category: `list_drug_classes(target_class="", therapeutic_area="")` / `get_drug_class(class_id)` / `find_drug_classes(needle)` / `drug_classes_for_target(target_class)` / `open_pharm_studio(tab="")`. |
| `actions_receptors.py` | **Phase PH-2.0 (round 220)** — 5 agent actions in the new `pharm-receptors` category: `list_receptors(family="")` / `get_receptor(receptor_id)` / `find_receptors(needle)` / `receptors_for_family(family)` / `open_pharm_receptors_tab()` (focuses the new Receptors tab). Same dispatcher pattern as the PH-1.0 opener. |

### `gui/` — Qt UI

- `windows/pharm_main_window.py` — `PharmMainWindow(QMainWindow)`. Single persistent instance opened from OrgChem main window's *Window → Pharmacology Studio…* menu (Ctrl+Shift+H). Three tabs: `Drug classes`, `Bridges`, `Tutorials`. Geometry persists via `QSettings["window/pharm"]`.
- `panels/drug_classes_panel.py` — `DrugClassesPanel(QWidget)`. Target-class combo + therapeutic-area combo + free-text filter + list + HTML detail card. `select_drug_class(class_id)` programmatic API.
- `panels/biochem_bridge_panel.py` — Read-only view of `biochem.core.enzymes` filtered to drug-targetable enzymes (drug_targets non-empty). *Open in Biochem* button hands off to the Biochem main window.
- `panels/cellbio_bridge_panel.py` — Read-only view of `cellbio.core.cell_signaling` filtered to pathways with drug_targets populated. *Open in Cell Bio* button hands off.
- `panels/pharm_tutorial_panel.py` — Reads `pharm.tutorial.curriculum.CURRICULUM`.

### `tutorial/`

| File | Key symbols |
|------|-------------|
| `curriculum.py` | 1 starter beginner lesson; full curriculum planned for PH-4. |
| `loader.py` | `load_lesson(path)`. |
| `content/beginner/01_welcome_pharm.md` | Welcome lesson. |

## Cross-studio integration

| Hook | Pharm side |
|------|------------|
| Window menu entry | *Window → Pharmacology Studio…* (Ctrl+Shift+H) |
| Headless registration | `orgchem.agent.headless.HeadlessApp.__init__` imports `pharm` after `cellbio` + `biochem` |
| Agent registry | Pharm actions register in shared `orgchem.agent.actions._REGISTRY` |
| **Multi-hop data sharing** | Pharm reads BOTH `biochem.core.enzymes` AND `cellbio.core.cell_signaling` via direct Python import |
| GUI audit | `orgchem.gui.audit.GUI_ENTRY_POINTS` extended |
| Agent surface audit | `orgchem.core.agent_surface_audit.EXPECTED_SURFACES` extended |

## Cross-studio cross-references (typed edges)

Each drug class can carry up to three families of cross-reference:

| Edge | Example |
|------|---------|
| drug-class → orgchem-molecule | β-blockers → Propranolol, Metoprolol, Atenolol |
| drug-class → biochem-enzyme-id | ACE inhibitors → "ace" (biochem.core.enzymes id) |
| drug-class → cellbio-signaling-pathway-id | β-blockers → "gpcr-camp-pka" (cellbio.core.cell_signaling id) |

Validated at test time so a future rename in any sibling surfaces the broken edge immediately.

## Adding to Pharm (checklist)

Same as Biochem — see `biochem/INTERFACE.md`.
