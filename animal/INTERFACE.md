# Animal Biology Studio — Interface Map

> **Phase AB-1.0 (round 217, 2026-04-26)** — sixth + FINAL
> sibling in the multi-studio life-sciences platform.
> Sibling package alongside `orgchem/`, `cellbio/`, `biochem/`,
> `pharm/`, `microbio/`, and `botany/`.  Shares the same
> process, agent registry, SQLite DB, and global glossary.
>
> **Architectural validation (final).** Animal reads three
> sibling catalogues directly: `orgchem.db.Molecule` rows
> (animal-derived hormones / neurotransmitters / metabolites
> by name), `cellbio.core.cell_signaling` (developmental +
> apoptosis + immune pathways), and `biochem.core.enzymes`
> (animal-source enzymes — chymotrypsin, ACE, etc.).  AB-1.0
> is the second sibling whose bridge panel reads
> ``cellbio.core.cell_signaling`` (the first was Pharm via
> `cellbio_bridge_panel.py`), confirming the cellbio API is
> stable enough to support multiple consumers.
>
> **The platform is now complete.**  Six sibling studios
> alongside OrgChem.  See `tutorial/content/beginner/02_
> platform_retrospective.md` for the full history.

## Top-level

| Path | Purpose |
|------|---------|
| `animal/__init__.py` | Imports `animal.agent.actions_taxa` to register actions. |
| `animal/INTERFACE.md` | This file. |
| `animal/core/` | Pure-data catalogues (no Qt). |
| `animal/agent/` | `@action`-decorated functions. |
| `animal/gui/` | Qt main window + panels. |
| `animal/tutorial/` | Animal-specific tutorial curriculum + content (incl. the platform retrospective lesson). |

## Package: `animal/`

### `core/` — data catalogues

| File | Key symbols |
|------|-------------|
| `taxa.py` | **Phase AB-1.0** — `AnimalTaxon` frozen dataclass + `PHYLA` (porifera / cnidaria / platyhelminthes / nematoda / mollusca / annelida / arthropoda / echinodermata / chordata) + `BODY_PLANS` (radial / bilateral / asymmetric) + `GERM_LAYERS` (diploblast / triploblast / not-applicable) + `COELOM_TYPES` (acoelomate / pseudocoelomate / coelomate / not-applicable) + lookup helpers. |
| `taxa_data.py` | 30-entry catalogue spanning all 9 major animal phyla.  Bilateral, triploblast, coelomate organisation dominates; sponges are the asymmetric outgroup; cnidarians the radial diploblast outgroup; nematodes pseudocoelomate.  Each entry: full taxonomic name, phylum, class, body plan, germ layers, coelom type, reproductive strategy, ecological role, model_organism flag, genome size, and **typed cross-references to OrgChem `Molecule` rows by name + `cellbio.core.cell_signaling` ids + `biochem.core.enzymes` ids**.  All cross-reference IDs verified against destination catalogues. |

### `agent/` — agent actions

| File | Key symbols |
|------|-------------|
| `actions_taxa.py` | 5 `@action(category="animal-taxa")` actions: `list_animal_taxa(phylum="", body_plan="")`, `get_animal_taxon(taxon_id)`, `find_animal_taxa(needle)`, `animal_taxa_for_phylum(phylum)`, `open_animal_studio(tab="")`. |
| `organ_systems.py` + `organ_systems_data.py` | **Phase AB-2.0 (round 223)** — 25-entry deep-phase catalogue covering the 11 canonical mammalian organ systems (cardiovascular, respiratory, digestive, urinary, nervous, endocrine, immune, musculoskeletal, integumentary, reproductive-female, reproductive-male, lymphatic) PLUS 13 comparative-anatomy entries (open vs closed circulation, gills + tracheae + air sacs, ruminant + avian + hindgut digestion, nerve nets vs centralised + cephalopod brains, protonephridia / metanephridia / Malpighian tubules, regeneration outliers, eye evolution, fish single-circuit hearts, invertebrate innate immunity, insect ecdysone signalling, muscle-type evolution, hermaphroditism + parthenogenesis, ectothermy vs endothermy). `OrganSystem` frozen dataclass + `SYSTEM_CATEGORIES` (13-tuple) + lookup helpers + `__post_init__` tuple validator. Each entry: representative organs, key cell types, functional anatomy, evolutionary origin, characteristic disorders, **4-way typed cross-references** to OrgChem `Molecule` rows + CB-1.0 signalling pathways + BC-1.0 enzymes + AB-1.0 animal-taxon ids. Pure-headless. |
| `actions_organ_systems.py` | **Phase AB-2.0 (round 223)** — 5 agent actions in the new `animal-organ-systems` category: `list_organ_systems(system_category="")` / `get_organ_system(system_id)` / `find_organ_systems(needle)` / `organ_systems_for_category(system_category)` / `open_animal_organ_systems_tab()`.  This is the FINAL agent-action category added by the -2 deep-phase chain (round 223 of 6). |

### `gui/` — Qt UI

- `windows/animal_main_window.py` — `AnimalMainWindow(QMainWindow)`.  Singleton opened from *Window → Animal Biology Studio…* (Ctrl+Shift+X).  Three tabs: `Animal taxa`, `Cell signalling bridge`, `Tutorials`.  `QSettings["window/animal"]`.
- `panels/animal_taxa_panel.py` — `AnimalTaxaPanel`.  Phylum combo + body-plan combo + free-text filter + list + HTML detail card with cross-refs.  `select_taxon(taxon_id)` programmatic API.
- `panels/cellbio_signaling_bridge_panel.py` — Read-only bridge into `cellbio.core.cell_signaling` filtered to animal-relevant developmental + apoptosis + immune pathways.  *Open in Cell Biology Studio…* hand-off button.  Modeled on `microbio/gui/panels/antibiotic_spectrum_panel.py` and `pharm/gui/panels/cellbio_bridge_panel.py`.
- `panels/animal_tutorial_panel.py` — `AnimalTutorialPanel`.  Same minimal pattern as previous siblings.

### `tutorial/`

| File | Key symbols |
|------|-------------|
| `curriculum.py` | 2 starter lessons: Welcome + **platform retrospective**. |
| `loader.py` | `load_lesson(path)`. |
| `content/beginner/01_welcome_animal.md` | Welcome lesson. |
| `content/beginner/02_platform_retrospective.md` | The full 6-studio retrospective — what shipped across CB / BC / PH / MB / BT / AB, the architectural pattern, the test-count growth, the cross-reference graph, the queued deeper-phase work for each sibling. |

## Cross-studio integration

| Hook | Animal side |
|------|-------------|
| Window menu entry | *Window → Animal Biology Studio…* (Ctrl+Shift+X) |
| Headless registration | `orgchem.agent.headless.HeadlessApp.__init__` imports `animal` after `botany` |
| Agent registry | Animal actions register in shared `orgchem.agent.actions._REGISTRY` |
| **Multi-hop data sharing** | Animal reads `orgchem.db.Molecule` rows directly + `cellbio.core.cell_signaling` + `biochem.core.enzymes` via Python import |
| GUI audit | `orgchem.gui.audit.GUI_ENTRY_POINTS` extended |
| Agent surface audit | `orgchem.core.agent_surface_audit.EXPECTED_SURFACES` extended |

## Cross-studio cross-references (typed edges)

| Edge | Example |
|------|---------|
| animal-taxon → orgchem-molecule-name | *Homo sapiens* → "Cortisol", "Cholesterol", "ATP (adenosine-5'-triphosphate)", "Dopamine" |
| animal-taxon → cellbio-signaling-pathway-id | *D. melanogaster* → "hedgehog", "notch", "wnt-beta-catenin"; *C. elegans* → "intrinsic-apoptosis" |
| animal-taxon → biochem-enzyme-id | *Bos taurus* → "chymotrypsin"; mammals → "ace", "atp-synthase" |

Validated at test time so a future rename in any sibling
catalogue surfaces the broken edge immediately.
