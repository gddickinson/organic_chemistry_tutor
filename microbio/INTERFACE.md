# Microbiology Studio — Interface Map

> **Phase MB-1.0 (round 215, 2026-04-26)** — fourth sibling
> in the multi-studio life-sciences platform (after Cell Bio
> CB-1.0, Biochem BC-1.0, Pharmacology PH-1.0).  Sibling
> package alongside `orgchem/`, `cellbio/`, `biochem/`, and
> `pharm/`.  Shares the same process, agent registry, SQLite
> DB, and global glossary.
>
> **Architectural validation:** Microbio reads three sibling
> catalogues directly — `orgchem.core.cell_components` (cell-
> structure cross-refs for bacteria / archaea / fungi),
> `pharm.core.drug_classes` (the antibiotic-spectrum bridge
> panel), and `biochem.core.enzymes` (clinically-relevant
> microbial / host enzymes).  Confirms the cross-studio data-
> sharing pattern works for any sibling triple.

## Top-level

| Path | Purpose |
|------|---------|
| `microbio/__init__.py` | Imports `microbio.agent.actions_microbes` to register actions. |
| `microbio/INTERFACE.md` | This file. |
| `microbio/core/` | Pure-data catalogues (no Qt). |
| `microbio/agent/` | `@action`-decorated functions. |
| `microbio/gui/` | Qt main window + panels. |
| `microbio/tutorial/` | Microbio-specific tutorial curriculum + content. |

## Package: `microbio/`

### `core/` — data catalogues

| File | Key symbols |
|------|-------------|
| `microbes.py` | **Phase MB-1.0** — `Microbe` frozen dataclass + `KINGDOMS` (bacteria / archaea / fungus / virus / protist) + `GRAM_TYPES` (gram-positive / gram-negative / acid-fast / atypical / not-applicable) + `BALTIMORE_CLASSES` (I-VII for viruses) + lookup helpers. |
| `microbes_data.py` | 30-microbe catalogue: 6 gram+ bacteria (S. aureus, S. pyogenes, S. pneumoniae, E. faecalis, C. difficile, L. monocytogenes), 6 gram- (E. coli, K. pneumoniae, P. aeruginosa, N. meningitidis, H. pylori, S. typhi), 3 atypical (Mycoplasma pneumoniae, Chlamydia trachomatis, Treponema pallidum), 2 mycobacteria (M. tuberculosis, M. leprae), 2 archaea (Methanobrevibacter smithii, Sulfolobus acidocaldarius), 3 fungi (Candida albicans, Aspergillus fumigatus, Cryptococcus neoformans), 6 viruses (SARS-CoV-2, HIV-1, Influenza A, HBV, HSV-1, Norovirus), 2 protists (Plasmodium falciparum, Toxoplasma gondii). Each entry: full taxonomic name, kingdom, gram_type, morphology, key_metabolism_or_replication, pathogenesis_summary, antibiotic_susceptibility (phrases), genome_size_or_kb, ICTV_or_Bergey_reference, **typed cross-references to `orgchem.core.cell_components` ids + `pharm.core.drug_classes` ids + `biochem.core.enzymes` ids**. |

### `agent/` — agent actions

| File | Key symbols |
|------|-------------|
| `actions_microbes.py` | 5 `@action(category="microbio-microbes")` actions: `list_microbes(kingdom="")`, `get_microbe(microbe_id)`, `find_microbes(needle)`, `microbes_for_kingdom(kingdom)`, `open_microbio_studio(tab="")`. |
| `virulence_factors.py` + `virulence_factors_data.py` | **Phase MB-2.0 (round 221)** — 30-entry deep-phase catalogue covering all 9 canonical bacterial virulence-mechanism classes: 8 AB-toxins (diphtheria, cholera, pertussis, Shiga, anthrax LF + EF, tetanus, botulinum), 5 pore-forming cytolysins (α-toxin, streptolysin O, pneumolysin, PVL, listeriolysin O), 3 superantigens (TSST-1, SEA-SEE, SpeA), 3 adhesins (UPEC fimbriae, M protein, Yersinia YadA/Invasin), 3 capsules (GAS hyaluronate, pneumococcal polysaccharide, anthrax poly-γ-D-glutamate), 3 secretion systems (T3SS, T4SS-CagA, T6SS), 3 immune-evasion factors (IgA1 protease, Protein A, Neisseria Opa antigenic variation), 1 biofilm + quorum-sensing entry, 1 LPS / lipid-A endotoxin entry. `VirulenceFactor` frozen dataclass + `MECHANISM_CLASSES` (9-tuple) + lookup helpers + `__post_init__` tuple validator. Each entry carries 3-way typed cross-references to MB-1.0 source-organism ids + BC-1.0 enzyme ids + CB-1.0 signalling-pathway ids. Pure-headless. |
| `actions_virulence.py` | **Phase MB-2.0 (round 221)** — 5 agent actions in the new `microbio-virulence` category: `list_virulence_factors(mechanism_class="")` / `get_virulence_factor(factor_id)` / `find_virulence_factors(needle)` / `virulence_factors_for_class(mechanism_class)` / `open_microbio_virulence_tab()`. |

### `gui/` — Qt UI

- `windows/microbio_main_window.py` — `MicrobioMainWindow(QMainWindow)`. Singleton opened from *Window → Microbiology Studio…* (Ctrl+Shift+N). Three tabs: `Microbes`, `Antibiotic spectrum`, `Tutorials`. `QSettings["window/microbio"]`.
- `panels/microbes_panel.py` — `MicrobesPanel`. Kingdom combo + gram-type combo + free-text filter + list + HTML detail card with cross-refs to cell components / drug classes / enzymes.  `select_microbe(microbe_id)` programmatic API.
- `panels/antibiotic_spectrum_panel.py` — Read-only view of `pharm.core.drug_classes` filtered to the 6 antimicrobial classes (β-lactams, macrolides, fluoroquinolones, aminoglycosides, HIV PIs, NRTIs).  Module-level `_ANTIMICROBIAL_CLASS_IDS` constant captures the categorisation (microbio-driven view of pharm's data, not a pharm-side flag).  *Open in Pharmacology Studio…* button hands off to the Pharm main window pre-selected to the chosen drug class.  `select_drug_class(class_id)` programmatic API.
- `panels/microbio_tutorial_panel.py` — `MicrobioTutorialPanel`. Same minimal pattern as cellbio / biochem / pharm tutorial panels.

### `tutorial/`

| File | Key symbols |
|------|-------------|
| `curriculum.py` | 1 starter beginner lesson; full curriculum planned for MB-4. |
| `loader.py` | `load_lesson(path)`. |
| `content/beginner/01_welcome_microbio.md` | Welcome lesson. |

## Cross-studio integration

| Hook | Microbio side |
|------|---------------|
| Window menu entry | *Window → Microbiology Studio…* (Ctrl+Shift+N) |
| Headless registration | `orgchem.agent.headless.HeadlessApp.__init__` imports `microbio` after `pharm` |
| Agent registry | Microbio actions register in shared `orgchem.agent.actions._REGISTRY` |
| **Multi-hop data sharing** | Microbio reads `orgchem.core.cell_components` + `pharm.core.drug_classes` + `biochem.core.enzymes` via direct Python import |
| GUI audit | `orgchem.gui.audit.GUI_ENTRY_POINTS` extended |
| Agent surface audit | `orgchem.core.agent_surface_audit.EXPECTED_SURFACES` extended |

## Cross-studio cross-references (typed edges)

| Edge | Example |
|------|---------|
| microbe → orgchem-cell-component-id | E. coli → "bacterial-plasma-membrane", "peptidoglycan-gram-negative", "outer-membrane-gram-negative", "bacterial-flagellum" |
| microbe → pharm-drug-class-id | S. aureus → "beta-lactams", "macrolides", "fluoroquinolones" |
| microbe → biochem-enzyme-id | HIV-1 → "hiv-protease" |

Validated at test time so a future rename in any sibling surfaces the broken edge immediately.

## Adding to Microbio (checklist)

Same as Pharm — see `pharm/INTERFACE.md`.
