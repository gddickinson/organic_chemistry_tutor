# Genetics + Molecular Biology Studio — Interface Map

> **Phase GM-1.0 (round 230, 2026-04-26)** — seventh
> sibling in the multi-studio life-sciences platform.
> Sibling package alongside `orgchem/`, `cellbio/`,
> `biochem/`, `pharm/`, `microbio/`, `botany/`, and
> `animal/`.  Shares the same process, agent registry,
> SQLite DB, and global glossary.
>
> **Architectural validation.**  GM-1.0 reads four
> sibling catalogues directly: `biochem.core.enzymes`
> (the molecular workhorses underlying every technique),
> `cellbio.core.cell_cycle` (chromatin / DDR /
> replication context), `cellbio.core.cell_signaling`
> (apoptosis / DDR / immunity pathways), and
> `animal.core.taxa` (model organisms used to develop +
> validate techniques).  GM-1.0 is the THIRD sibling
> whose bridge panel reads `biochem.core.enzymes`
> (after Pharm + Animal indirectly via cross-refs);
> confirms the biochem API is stable across multiple
> consumers.
>
> **The platform is now complete with 7 siblings.**
> See `tutorial/content/beginner/01_welcome_genetics.md`
> for the full 7-sibling-platform overview.

## Top-level

| Path | Purpose |
|------|---------|
| `genetics/__init__.py` | Imports `genetics.agent.actions_techniques` to register actions. |
| `genetics/INTERFACE.md` | This file. |
| `genetics/core/` | Pure-data catalogues (no Qt). |
| `genetics/agent/` | `@action`-decorated functions. |
| `genetics/gui/` | Qt main window + panels. |
| `genetics/tutorial/` | Genetics-specific tutorial curriculum + content. |

## Package: `genetics/`

### `core/` — data catalogues

| File | Key symbols |
|------|-------------|
| `techniques.py` | **Phase GM-1.0** — `MolecularBiologyTechnique` frozen dataclass + `CATEGORIES` (14-tuple: pcr / sequencing / cloning / crispr / blot / in-situ / chromatin / transcriptomics / spatial / proteomics / interaction / structural / epigenetics / delivery) + lookup helpers + `__post_init__` tuple validator (BC-2.0 pattern that closed the trailing-comma bug class permanently). |
| `techniques_data.py` | 40-entry catalogue spanning every major class of molecular-biology technique.  Each entry is a long-form bench card: principle, sample types, throughput, key reagents (cross-link to BC-1.0 enzymes), typical readouts, limitations, representative platforms, year of introduction, key references.  **5-way typed cross-references** to `biochem.core.enzymes` ids + `cellbio.core.cell_cycle` ids + `cellbio.core.cell_signaling` ids + `animal.core.taxa` ids + OrgChem `Molecule` row names.  All cross-reference IDs verified at write time. |

### `agent/` — agent actions

| File | Key symbols |
|------|-------------|
| `actions_techniques.py` | 5 `@action(category="genetics-techniques")` actions: `list_genetics_techniques(category="")`, `get_genetics_technique(technique_id)`, `find_genetics_techniques(needle)`, `genetics_techniques_for_application(application)`, `open_genetics_studio(tab="")`. |

### `gui/` — Qt UI

- `windows/genetics_main_window.py` — `GeneticsMainWindow(QMainWindow)`.  Singleton opened from *Window → Genetics + Molecular Biology Studio…* (Ctrl+Alt+G).  Three tabs: `Techniques`, `Cross-references`, `Tutorials`.  `QSettings["window/genetics"]`.
- `panels/techniques_panel.py` — `TechniquesPanel`.  Category combo + free-text filter + list + HTML detail card with cross-refs.  `select_technique(technique_id)` programmatic API.
- `panels/molecular_biology_bridge_panel.py` — Read-only bridge into `biochem.core.enzymes` filtered to nucleic-acid-acting enzymes (DNA polymerases / ligases / restriction enzymes / reverse transcriptases / nucleases / topoisomerases / helicases / etc.).  *Open in Biochem Studio…* hand-off button.  Modeled on `animal/gui/panels/cellbio_signaling_bridge_panel.py` and `pharm/gui/panels/cellbio_bridge_panel.py`.
- `panels/genetics_tutorial_panel.py` — `GeneticsTutorialPanel`.  Same minimal pattern as previous siblings.

### `tutorial/`

| File | Key symbols |
|------|-------------|
| `curriculum.py` | 1 starter Welcome lesson at beginner tier. |
| `loader.py` | `load_lesson(path)`. |
| `content/beginner/01_welcome_genetics.md` | Welcome lesson + 7-sibling-platform context. |

## Cross-studio integration

| Hook | Genetics side |
|------|---------------|
| Window menu entry | *Window → Genetics + Molecular Biology Studio…* (Ctrl+Alt+G) |
| Headless registration | `orgchem.agent.headless.HeadlessApp.__init__` imports `genetics` after `animal` |
| Agent registry | Genetics actions register in shared `orgchem.agent.actions._REGISTRY` |
| **Multi-hop data sharing** | Genetics reads `biochem.core.enzymes` + `cellbio.core.cell_cycle` + `cellbio.core.cell_signaling` + `animal.core.taxa` + `orgchem.db.Molecule` via Python import |
| GUI audit | `orgchem.gui.audit.GUI_ENTRY_POINTS` extended |
| Agent surface audit | `orgchem.core.agent_surface_audit.EXPECTED_SURFACES` extended |
| Category summary | `orgchem.agent.actions_meta._CATEGORY_SUMMARIES` extended |

## Cross-studio cross-references (typed edges)

| Edge | Example |
|------|---------|
| genetics-technique → biochem-enzyme-id | `endpoint-pcr` → `dna-ligase-i`; `gibson-assembly` → `dna-ligase-i`; `golden-gate` → `dna-ligase-i`; `hi-c` → `dna-ligase-i`; `bottom-up-proteomics` → `trypsin`, `chymotrypsin`; `ap-ms` → `trypsin` |
| genetics-technique → cellbio-cell-cycle-id | `endpoint-pcr` → `s-phase`; `crispr-cas9` → `g2-m-checkpoint`, `intra-s-checkpoint`; `chip-seq` → `g1-phase`, `s-phase`; `hi-c` → `g1-phase`, `m-phase`; `fish` → `m-phase` |
| genetics-technique → cellbio-signaling-pathway-id | `crispr-cas9` → `p53` |
| genetics-technique → animal-taxon-id | `illumina-short-read` → `homo-sapiens`; `crispr-cas9` → `mus-musculus`, `danio-rerio`, `caenorhabditis-elegans`; `scrna-seq` → `mus-musculus`, `homo-sapiens`, `danio-rerio`, `drosophila-melanogaster`; `lipid-nanoparticle-delivery` → `homo-sapiens`, `mus-musculus`; `aav-delivery` → `homo-sapiens` |
| genetics-technique → orgchem-molecule-name | `endpoint-pcr` → "Adenine", "Guanine", "Cytosine", "Thymine"; `base-editor` → "Adenine", "Cytosine", "Guanine", "Thymine"; `bisulfite-seq` → "Cytosine"; `methylation-array` → "Cytosine" |

Validated at test time so a future rename in any
sibling catalogue surfaces the broken edge immediately.
