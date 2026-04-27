# Botany Studio — Interface Map

> **Phase BT-1.0 (round 216, 2026-04-26)** — fifth sibling
> in the multi-studio life-sciences platform (after Cell Bio
> CB-1.0, Biochem BC-1.0, Pharmacology PH-1.0, Microbiology
> MB-1.0).  Sibling package alongside `orgchem/`, `cellbio/`,
> `biochem/`, `pharm/`, and `microbio/`.  Shares the same
> process, agent registry, SQLite DB, and global glossary.
>
> **Architectural validation:** Botany reads three sibling
> catalogues — `orgchem/db/Molecule` rows (plant natural
> products via name xref), `orgchem.core.metabolic_pathways`
> (Calvin cycle, glycolysis, etc.), and `pharm.core.
> drug_classes` (plant-derived drug classes — opioids from
> poppy, NSAIDs from willow, taxanes from yew).  Confirms the
> cross-studio data-sharing pattern works for any sibling
> triple — and the *Plant secondary metabolites* bridge
> demonstrates a *direct DB read* (not a sibling-package
> import) for the first time.

## Top-level

| Path | Purpose |
|------|---------|
| `botany/__init__.py` | Imports `botany.agent.actions_taxa` to register actions. |
| `botany/INTERFACE.md` | This file. |
| `botany/core/` | Pure-data catalogues (no Qt). |
| `botany/agent/` | `@action`-decorated functions. |
| `botany/gui/` | Qt main window + panels. |
| `botany/tutorial/` | Botany-specific tutorial curriculum + content. |

## Package: `botany/`

### `core/` — data catalogues

| File | Key symbols |
|------|-------------|
| `taxa.py` | **Phase BT-1.0** — `PlantTaxon` frozen dataclass + `DIVISIONS` (bryophyta / lycopodiophyta / pteridophyta / gymnosperm / angiosperm-monocot / angiosperm-eudicot) + `PHOTOSYNTHETIC_STRATEGIES` (C3 / C4 / CAM / not-applicable) + `LIFE_CYCLES` (annual / biennial / perennial / not-applicable) + lookup helpers (`list_plant_taxa` / `get_plant_taxon` / `find_plant_taxa` / `plant_taxa_for_division` / `plant_taxon_to_dict`). |
| `taxa_data.py` | 30-entry catalogue spanning the 6 major plant divisions: 1 bryophyte (*Physcomitrium patens* — model moss), 1 lycophyte (*Selaginella moellendorffii* — model resurrection plant), 2 ferns (*Azolla filiculoides* — N-fixing water fern, *Pteridium aquilinum* — bracken), 4 gymnosperms (*Ginkgo biloba* — living fossil, *Taxus brevifolia* — Pacific yew + paclitaxel, *Pinus taeda* — loblolly pine, *Picea abies* — Norway spruce), 8 monocots (*Oryza sativa* — rice, *Zea mays* — maize C4, *Saccharum officinarum* — sugarcane C4, *Triticum aestivum* — wheat, *Musa acuminata* — banana, *Allium sativum* — garlic, *Vanilla planifolia* — vanilla CAM, *Aloe vera* — CAM), 14 eudicots (*Arabidopsis thaliana* — model dicot, *Solanum lycopersicum* — tomato, *Nicotiana tabacum* — tobacco, *Papaver somniferum* — opium poppy, *Salix alba* — willow, *Coffea arabica* — coffee, *Cinchona officinalis* — quinine, *Mentha piperita* — peppermint, *Theobroma cacao* — cacao, *Atropa belladonna* — deadly nightshade, *Camellia sinensis* — tea, *Capsicum annuum* — chili, *Hevea brasiliensis* — rubber tree, *Rafflesia arnoldii* — non-photosynthetic parasite).  Each entry: full taxonomic name, division, class, life cycle, photosynthetic strategy, reproductive strategy, ecological role, economic importance, model_organism flag, genome size, **typed cross-references to molecule names + metabolic-pathway ids + pharm drug-class ids**. |

### `agent/` — agent actions

| File | Key symbols |
|------|-------------|
| `actions_taxa.py` | 5 `@action(category="botany-taxa")` actions: `list_plant_taxa(division="", photosynthetic_strategy="")`, `get_plant_taxon(taxon_id)`, `find_plant_taxa(needle)`, `plant_taxa_for_division(division)`, `open_botany_studio(tab="")`. |
| `plant_hormones.py` + `plant_hormones_data.py` | **Phase BT-2.0 (round 222)** — 21-entry deep-phase catalogue spanning all 10 canonical phytohormone classes: 4 auxins (IAA, 2,4-D, NAA, IBA), 3 cytokinins (trans-zeatin, kinetin, BAP), 2 gibberellins (GA3, GA4), 1 abscisic acid, 1 ethylene, 2 brassinosteroids (brassinolide, castasterone), 2 jasmonates (JA, MeJA), 1 salicylic acid, 2 strigolactones (strigol, orobanchol), 3 peptide hormones (CLE, systemin, RALF). `PlantHormone` frozen dataclass + `HORMONE_CLASSES` (10-tuple) + lookup helpers + `__post_init__` tuple validator. Each entry: structural class, biosynthesis precursor, perception mechanism (TIR1, AHK, GID1, PYR/PYL/RCAR, ETR1, BRI1, COI1, NPR1, D14, FERONIA…), primary physiological effect, antagonisms, key model plants, and 2-way cross-references to OrgChem `Molecule` rows + BT-1.0 plant-taxon ids. Pure-headless. |
| `actions_plant_hormones.py` | **Phase BT-2.0 (round 222)** — 5 agent actions in the new `botany-hormones` category: `list_plant_hormones(hormone_class="")` / `get_plant_hormone(hormone_id)` / `find_plant_hormones(needle)` / `plant_hormones_for_class(hormone_class)` / `open_botany_plant_hormones_tab()`. |

### `gui/` — Qt UI

- `windows/botany_main_window.py` — `BotanyMainWindow(QMainWindow)`. Singleton opened from *Window → Botany Studio…* (Ctrl+Shift+V).  Three tabs: `Plant taxa`, `Plant secondary metabolites`, `Tutorials`.  `QSettings["window/botany"]`.
- `panels/plant_taxa_panel.py` — `PlantTaxaPanel`. Division combo + photosynthetic-strategy combo + free-text filter + list + HTML detail card with cross-refs.  `select_taxon(taxon_id)` programmatic API.
- `panels/plant_metabolites_panel.py` — Read-only bridge into the OrgChem molecule DB filtered to plant-derived natural products.  Source-tag combo (alkaloid / steroid / fatty-acid / dye / drug-class / all-tagged-plant-products), free-text filter, list, detail card.  *Open in Molecule Workspace* button fires `bus().molecule_selected.emit(mol_id)` so the user lands in the OrgChem main-window molecule tab.
- `panels/botany_tutorial_panel.py` — `BotanyTutorialPanel`.  Same minimal pattern as cellbio / biochem / pharm / microbio tutorial panels.

### `tutorial/`

| File | Key symbols |
|------|-------------|
| `curriculum.py` | 1 starter beginner lesson; full curriculum planned for BT-4. |
| `loader.py` | `load_lesson(path)`. |
| `content/beginner/01_welcome_botany.md` | Welcome lesson. |

## Cross-studio integration

| Hook | Botany side |
|------|-------------|
| Window menu entry | *Window → Botany Studio…* (Ctrl+Shift+V) |
| Headless registration | `orgchem.agent.headless.HeadlessApp.__init__` imports `botany` after `microbio` |
| Agent registry | Botany actions register in shared `orgchem.agent.actions._REGISTRY` |
| **Multi-hop data sharing** | Botany reads `orgchem.db.Molecule` rows directly + `orgchem.core.metabolic_pathways` + `pharm.core.drug_classes` via Python import |
| GUI audit | `orgchem.gui.audit.GUI_ENTRY_POINTS` extended |
| Agent surface audit | `orgchem.core.agent_surface_audit.EXPECTED_SURFACES` extended |

## Cross-studio cross-references (typed edges)

| Edge | Example |
|------|---------|
| plant-taxon → orgchem-molecule-name | Papaver somniferum → "Morphine", "Codeine" |
| plant-taxon → metabolic-pathway-id | Zea mays → "calvin_cycle", "glycolysis" |
| plant-taxon → pharm-drug-class-id | Salix alba → "nsaids" (aspirin); Papaver somniferum → "opioids"; Taxus brevifolia → "taxanes" |

Validated at test time so a future rename in any sibling
catalogue surfaces the broken edge immediately.
