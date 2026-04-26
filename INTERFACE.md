# OrgChem Studio — Interface Map

Read this file FIRST before opening any source file. It is the navigation map
for the project. Update it whenever the module layout changes.

## Top-level

| File / Dir          | Purpose |
|---------------------|---------|
| `main.py`           | Application entry point. Loads config → inits DB → seeds → opens main window. Also hosts the `--agent-stdio` and `--headless` launch flags. |
| `orgchem/`          | Main application package (see below). |
| `data/`             | Bundled static data (optional seeds, tutorial assets). |
| `tests/`            | pytest suite. |
| `refs/`             | Reference papers (e.g. Verma et al. 2024 whose formula calculator we reimplement). |
| `scripts/`          | Utility scripts: `visual_tour.py` (canonical-state gallery regen), `regen_goldens.py` (Phase 20b golden-baseline writer), `batch_render.py` (Phase 20e CLI), `fetch_3dmol_js.py` (Phase 20a offline bundle), `claude_drive_demo.py` (agent walkthrough). |
| `CLAUDE.md`         | Project-specific Claude Code instructions (references this file). |
| `PROJECT_STATUS.md` | What works *today*, plus metrics and known issues. |
| `ROADMAP.md`        | Phased plan through v1.0 and beyond. |
| `SESSION_LOG.md`    | Rolling development log. |
| `requirements.txt`  | Python deps. |

## Package: `orgchem/`

### `config.py`
- `AppConfig` dataclass: db_path, log/cache dirs, theme, 3D style defaults, online-sources flag.
- `AppConfig.load()` / `.save()` — YAML round-trip via platformdirs.

### `logging_setup.py`
- `setup_logging(cfg)` — installs rotating file handler + console handler + `BusHandler`
  (logging → AppBus → `SessionLogPanel`).

### `core/` — chemistry back-end (no GUI imports)
| File | Key symbols |
|------|-------------|
| `formats.py` | `mol_from_smiles`, `mol_to_smiles`, `mol_to_inchi`, `mol_to_inchikey`, `mol_to_molblock`, `molecular_formula`. |
| `molecule.py` | `Molecule` dataclass wrapping an `rdkit.Chem.Mol`; `.from_smiles`, `.generate_3d`, `.ensure_properties`. |
| `reaction.py` | `Reaction` (SMARTS + metadata). |
| `mechanism.py` | `Mechanism` / `MechanismStep` / `Arrow` dataclasses with `to_json` / `from_json`. Stored in `Reaction.mechanism_json`. Phase 13c follow-up fields: `Arrow.from_bond` / `to_bond` (bond-midpoint endpoints, e.g. π-bond attack) and `MechanismStep.lone_pairs` (list of atom indices decorated with lone-pair dots). Legacy JSON without these fields still loads. |
| `energy_profile.py` | `ReactionEnergyProfile` / `StationaryPoint` dataclasses with JSON round-trip, `activation_energies` and `delta_h` helpers. Stored in `Reaction.energy_profile_json` (Phase 13). |
| `reaction_trajectory.py` | `build_xyz_trajectory(mapped_smarts, n_frames)` and `kabsch_align(src, target)` — Phase 2c.2 trajectory builder. Pure RDKit + NumPy, no GUI deps. |
| `dynamics.py` | `run_dihedral_scan(mol, dihedral_atoms)`, `run_conformer_morph(mol)`, `frames_to_xyz(result)` — Phase 10a conformational dynamics. Plus pre-wired `butane_dihedral_scan`, `ethane_dihedral_scan`, `cyclohexane_ring_flip` demos. |
| `descriptors.py` | `compute_all(mol)` — MW, logP, TPSA, Lipinski violations, ring counts, formal charge. |
| `conformers.py` | `embed_3d(mol, num_confs, seed, optimise)` — MMFF-optimised conformers. |
| `formula.py` | `compute_formula(percentages, molar_mass)` — Verma et al. 2024 Section A as a library. |
| `green_metrics.py` | `atom_economy(reaction_smiles)`, `e_factor(mass_inputs, mass_product)`, `pathway_atom_economy(steps)` — Trost / Sheldon green-chemistry metrics (Phase 17a / 18a). Pure RDKit, headless. |
| `huckel.py` | `huckel(mol)`, `huckel_for_smiles(smi)` → `HuckelResult` (π-system MOs via adjacency-matrix eigendecomposition, α=0, β=−1). Auto-detects conjugated carbon radicals / cations / anions. Gives exact textbook values for ethene, butadiene, benzene, Cp⁻, etc. (Phase 14a). |
| `wh_rules.py` | 17 Woodward-Hoffmann rules (cycloadditions, electrocyclic, sigmatropic, general) + `check_allowed(kind, e⁻, regime)` predicate (Phase 14b). |
| `spectroscopy.py` | `predict_bands(smiles)`, `describe_prediction(smiles)` — teaching-grade IR correlation chart (26 functional-group → wavenumber entries). SMARTS-based detection, Silverstein-style output (Phase 4). |
| `nmr.py` | `predict_shifts(smiles, nucleus)` — ¹H + ¹³C shift predictor backed by SMARTS environment tables (18 ¹H + 16 ¹³C rows). Peak list sorted high-to-low ppm, multiplicity hints for ¹H (Phase 4 extension). |
| `ms.py` | `monoisotopic_mass(smiles)` + `isotope_pattern(smiles)` — HRMS-grade mass + M / M+1 / M+2 / … envelope via element-wise polynomial convolution. Covers H/C/N/O/F/P/S/Cl/Br/I; halogen diagnostics reproduce the canonical 3:1 / 1:1 textbook intensities (Phase 4). |
| `hrms.py` | `guess_formula(mass, ppm_tolerance, bounds, top_k)` — enumerate candidate molecular formulas whose theoretical monoisotopic mass fits a measured HRMS peak; filtered by the nitrogen rule, integer DBE, and Senior's rule; ranked by |ppm error| with a light heteroatom-combinatorics penalty. `suggest_formula_for_smiles` is a SMILES → mass → guess round-trip helper. (Phase 4 follow-up) |
| `ms_fragments.py` | `predict_fragments(smiles, min_mz)` → `FragmentReport` enumerating the molecular ion plus common EI-MS neutral losses (M−15 CH₃, M−17 OH, M−18 H₂O, M−27 HCN, M−28 CO/C₂H₄, M−29 CHO, M−31 OCH₃, M−43 acetyl/propyl, M−44 CO₂, M−45 COOH/OEt, M−57 tBu, M−77 Ph). Each rule carries a tuple of SMARTS preconditions so a loss fires only when the molecule has the requisite functional group. (Phase 4 follow-up) |
| `session_state.py` | `SessionState` dataclass + YAML I/O (`save_session`, `load_session`), `list_sessions`, `default_session_path`. Captures the minimum set of user state (active tab, current molecule SMILES, loaded PDB id + ligand, HRMS measurement, compare slots, free-form notes) so a later launch can resume. Forwards-compatible parser drops unknown YAML keys. (Phase 20d) |
| `retrosynthesis.py` | `find_retrosynthesis(smiles)`, `apply_template`, `list_templates` — 8 SMARTS retro-templates (ester / amide / Suzuki biaryl / Williamson ether / aldol / Diels-Alder / nitration / reductive amination). Pure RDKit ChemicalReaction engine. Phase 8d. |
| `sar.py` | `SARSeries` / `SARVariant` dataclasses + `SAR_LIBRARY` (NSAIDs COX, statins HMG-CoA). `compute_descriptors` folds Phase 19b drug-likeness into each variant row. (Phase 19a) |
| `batch.py` | `batch_render(entries, out_dir)` + `batch_render_from_file(input_path, out_dir)` — reads a CSV / TXT of SMILES and writes per-molecule 2D / IR PNGs + `descriptors.csv` + `report.md`. Used by `scripts/batch_render.py`. (Phase 20e) |
| `bioisosteres.py` | `BIOISOSTERES` catalogue (14 SMARTS templates covering COOH↔tetrazole, Me↔CF₃, amide↔sulfonamide, phenyl→thiophene, O↔CH₂, Cl↔F, ArOH↔ArNH₂, ester→amide) + `suggest_bioisosteres(smiles)`. (Phase 19c) |
| `protein.py` | `Protein` / `Chain` / `Residue` / `Atom` dataclasses + `parse_pdb_text` / `parse_pdb_file` + `SEEDED_PROTEINS` catalogue of 6 teaching targets (A2A-caffeine, COX-1-ibuprofen, HMG-CoA-atorvastatin, HIV protease dimer + ritonavir, insulin hexamer, doxorubicin-DNA). Column-fixed PDB parser, no Biopython dep. (Phase 24a) |
| `binding_contacts.py` | `analyse_binding(protein, ligand_name)` → `ContactReport` with per-contact `{kind, ligand_atom, chain, residue, distance}`. Geometric H-bond / salt-bridge / π-stacking / hydrophobic detection; no external deps (Phase 24e). |
| `pockets.py` | `find_pockets(protein)` + `pockets_summary` — grid-based cavity detector (probe grid + buriedness + flood-fill clustering). Ranks by voxel volume, annotates lining residues. Dep-free teaching-grade fpocket alternative. (Phase 24d) |
| `ppi.py` | `analyse_ppi(protein)` / `analyse_ppi_pair(protein, a, b)` → `PPIInterface` per chain pair carrying `PPIContact` records. Same H-bond / salt-bridge / π-stacking / hydrophobic criteria as `binding_contacts.py`, applied cross-chain. `ppi_summary` top-level dict for agent return. Dep-free. (Phase 24j) |
| `plip_bridge.py` | Optional PLIP adapter — `plip_available()`, `capabilities()`, `analyse_binding_plip(protein, ligand_name, require_plip=False)` → `PLIPResult(report, engine)`. Prefers the PLIP Python API, falls back to the `plip` / `plipcmd` CLI (XML output), and finally to `binding_contacts.analyse_binding` — with the `engine` tag telling the caller which code path ran. (Phase 24i) |
| `na_interactions.py` | `analyse_na_binding(protein, ligand_name)` → `NAContactReport` with four kinds: intercalation (ligand ring sandwiched between consecutive bases, centroid-centroid angle ≥ 120°), major-groove-hb / minor-groove-hb (name-indexed atom tables per nucleotide), phosphate-contact. Dep-free, reuses the Phase 24a PDB parser which already recognises A/T/G/C/U / DA/DT/DG/DC/DU residues. (Phase 24k) |
| `fragment_resolver.py` | `resolve(smiles)`, `canonical_reaction_smiles(rxn)`, `audit_reaction(rxn)` — InChIKey-based DB lookup so rendering pipelines reuse canonical 2D coords everywhere. Phase 6f.1. |
| `fulltext_search.py` | **Phase 33a** — cross-surface full-text search over every text-bearing column in the seeded DB.  Pure-Python linear scan (~1 k rows × ~300 chars, fast enough without an FTS index).  `search(query, kinds=None, limit=50) → List[SearchResult]` with title-boost scoring + word-boundary bonus + snippet excerpt.  `SEARCHABLE_KINDS = (molecule, reaction, pathway, glossary, mechanism-step)`.  `SearchResult.key` carries dispatch info (molecule_id / term / pathway_id / reaction_id + step_index).  Mechanism steps surface individually so a "Beckmann" query lands on the Nylon-6 step 2 description directly. |
| `drawing.py` | **Phase 36a (round 124)** — headless structure-editor data core for the upcoming ChemDraw-equivalent drawing tool.  `Atom` (element, charge, isotope, radical, aromatic, h_count, chirality ∈ {none, CW, CCW}) / `Bond` (begin_idx, end_idx, order 1/2/3/aromatic, stereo ∈ {none, wedge, dash, either}) / `Structure` (atoms + bonds) dataclasses with `add_atom(element, **kw)` + `add_bond(a, b, order, stereo)` helpers.  RDKit-backed round-trip: `structure_from_smiles(smi)` / `structure_to_smiles(s, canonical=True)` / `structure_from_molblock(block)` / `structure_to_molblock(s)` — all return ``None`` on malformed input rather than raising.  Preserves formal charges, isotope labels, radical electrons, tetrahedral atom-centric chirality, and wedge/dash bond-directional stereo across the round-trip.  No Qt imports; fully headless-testable. |
| `tutorial_coverage_audit.py` | **Phase 49f (round 181)** — sixth and final sub-phase of the user-flagged Phase-49 cross-module integration sweep.  Test-time helper that walks every tutorial markdown lesson and reports which knowledge-graph layers it references: glossary / catalogue molecule / named reaction.  `LessonCoverage(level, title, path, has_glossary_ref, has_catalogue_molecule_ref, has_named_reaction_ref)` per-lesson dataclass with `hit_count()` (0-3) helper + `TutorialCoverageReport` aggregate with `with_glossary_pct()` / `with_catalogue_molecule_pct()` / `with_named_reaction_pct()` percentage methods.  `audit_tutorial_coverage()` walks `tutorial.curriculum.CURRICULUM` filtering out authoring-test stub lessons (any lesson whose title contains "test lesson" — they're injected by the round-94 authoring-action test suite and have no chemistry content).  `lessons_missing(report, layer)` per-layer drill-down (`"glossary"` / `"catalogue"` / `"named-reaction"` — raises `ValueError` on unknown layer).  `render_report_text(report)` plain-text 5-line summary for failure messages + the Phase-49f doc.  Pure-headless: lazy imports of every catalogue module so a stripped-down environment doesn't crash the audit.  Round-181 baseline: 31 lessons, 100 % glossary coverage (achieved by adding a one-sentence chemistry intro to the welcome lesson in the same round), 54.8 % catalogue-molecule coverage, 45.2 % named-reaction coverage, 16.1 % "fully-integrated" (hits all three layers). |
| `feature_discovery_audit.py` | **Phase 49e (round 180)** — fifth sub-phase of the user-flagged Phase-49 cross-module integration sweep.  Test-time helper that walks the agent action registry + the LLM-facing `tool_schemas()` generator + the `list_capabilities()` meta action and verifies the AI tutor backend can discover every feature the app ships.  Three failure modes audited: (1) **Schema-coverage gap** — registered action not surfaced in `tool_schemas()` so the LLM literally can't call it; (2) **Description gap** — action ships with no docstring → empty description in the tool schema; (3) **Category-summary gap** — registered category not in `actions_meta._CATEGORY_SUMMARIES` so the tutor's `list_capabilities()` returns an empty description for that area.  `FeatureDiscoveryReport(total_actions, total_categories, total_schemas, actions_missing_description, actions_missing_from_schemas, schemas_missing_required_keys, categories_missing_summary)` dataclass + `audit_feature_discovery()` runner + `list_capabilities_smoke()` (no-arg `list_capabilities()` invocation as a smoke check) + `render_report_text(report)` for the failure messages + the Phase-49e doc.  `REQUIRED_SCHEMA_KEYS` + `REQUIRED_INPUT_SCHEMA_KEYS` constants document the Anthropic / OpenAI tool-schema shape contract.  Pure-headless: imports the agent registry only.  Round-180 baseline: 243 actions × 43 categories all clean after backfilling 19 missing category summaries (authoring / biochem / calc / cell / centrifugation / chromatography / clinical / drawing / instrumentation / isomer / kingdom / microscopy / ph / phys-org / qualitative / reagent / scripting / search / spectrophotometry) and 2 empty-docstring actions (`get_centrifuge_action` / `get_rotor_action`) found by the first run. |
| `agent_surface_audit.py` | **Phase 49d (round 179)** — fourth sub-phase of the user-flagged Phase-49 cross-module integration sweep.  Test-time helper that walks the agent action registry and verifies every catalogue with a Tools-menu dialog has a symmetric agent-action surface (opener `open_<X>` + canonical lookup trio `list_<X>` / `get_<X>` / `find_<X>`).  `SurfaceSpec(catalogue, opener, list_action, get_action, find_action)` frozen dataclass + `SurfaceAuditReport(spec, missing_actions)` + `EXPECTED_SURFACES` 24-tuple covering every Tools-menu catalogue dialog (Cell components / Centrifugation / Chromatography / Clinical panels / Drawing tool / Isomer explorer / Lab analysers / Lab calculator / Lab equipment / Lab reagents / Lab setups / Macromolecules window / Mechanism player / Metabolic pathways / Microscopy / Naming rules / Periodic table / pH explorer / Qualitative tests / Script editor / Spectrophotometry / Tutorial / Workbench / Biochemistry by kingdom).  `KNOWN_GAPS` allow-lists 9 dialogs that ship without an `open_*` action (each entry is `(action_name, rationale)` so a future reader knows WHY it's deferred — Spectroscopy / Stereo / Medchem / Orbitals / Retrosynthesis / Lab techniques / Green metrics / HRMS / MS fragments).  Public API: `gather_action_names()` (full set from `agent.actions.registry()`), `audit_surface(spec)` / `audit_all_surfaces()`, `gather_known_gaps()` / `stale_known_gaps()` (catches allow-list drift — any action listed in `KNOWN_GAPS` that DOES exist now), `render_audit_text()` (24-row table: catalogue name + ok / MISSING + total complete / total + KNOWN_GAPS count).  Pure-headless: imports only the agent registry, no Qt imports.  Round-179 baseline: **24/24** complete after `open_periodic_table` + `open_naming_rules` were added in the same round to close the two highest-value gaps. |
| `cross_reference_audit.py` | **Phase 49c (round 178)** — third sub-phase of the user-flagged Phase-49 cross-module integration sweep.  Test-time helper that walks every catalogue's cross-reference fields, validates each edge against the destination catalogue / Molecule DB, and reports broken links + a renderable matrix.  Five cross-reference relationships audited: `cell-component → molecule` (Phase-43 `MolecularConstituent.cross_reference_molecule_name` → `Molecule.name`); `kingdom-topic → cell-component` (Phase-47 `KingdomTopic.cross_reference_cell_component_ids` → `CellComponent.id`); `kingdom-topic → metabolic-pathway` (Phase-47 `KingdomTopic.cross_reference_pathway_ids` → `Pathway.id`); `kingdom-topic → molecule` (Phase-47 `KingdomTopic.cross_reference_molecule_names` → `Molecule.name`); `microscopy-method → lab-analyser` (Phase-44 `MicroscopyMethod.cross_reference_lab_analyser_ids` → `LabAnalyser.id`).  `CrossRef(source_kind, source_id, target_kind, target_id)` frozen dataclass + `CrossRefReport(total, broken, by_kind)` dataclass + four public APIs: `gather_all_cross_references()` (flat list of every edge — currently 59 across 5 kinds), `validate_cross_references(refs=None)` (resolves every edge + reports broken; molecule-name lookups go via `find_molecule_by_name`-style normalised names + synonyms), `cross_reference_matrix()` (`{(source_kind, target_kind): edge_count}`), `render_matrix_text()` (left-aligned plain-text matrix for the Phase-49c doc + failure messages).  Pure-headless: no Qt imports.  Lazy DB import so the gather walker runs without a seeded database (broken-name detection then becomes unavailable for that one kind, but structural walks still produce the matrix).  Caught a real bug on first run when the wrong public API name was used for `lab_analysers` (`list_lab_analysers` vs `list_analysers`); Phase 49d-f will use the matrix output to drive cross-reference expansion in low-coverage catalogues. |
| `glossary_audit.py` | **Phase 49a (round 176)** — first sub-phase of the user-flagged Phase-49 cross-module integration sweep.  Test-time helper that walks every catalogue body / description / notes text + every tutorial markdown lesson + every named-reaction `_STARTER` description, then verifies that pedagogically-important chemistry terms are covered by the glossary.  Three public API entry points: `glossary_term_set()` returns the lowercase set of every glossary term + alias across `seed_glossary._GLOSSARY` + `seed_glossary_extra.EXTRA_TERMS` (~ 247 entries after the round-176 backfill); `all_catalogue_text()` returns the concatenated body text (~ 330 kchars after walking 7 catalogues + 35 tutorial lessons + 56 reaction descriptions); `PHASE_49A_REQUIRED_TERMS` is the canonical 12-term tuple of high-priority gates (pH, pKa, buffer, hydrogen bonding, lithium diisopropylamide, active-methylene compound, multi-component reaction, endosymbiotic theory, horizontal gene transfer, CRISPR, chirality, chiral switch).  No Qt imports; pure-Python; no DB dependency (reads glossary entries directly from the seed-file Python data structures).  Used by the round-176 coverage tests for high-priority required-term gates; will be extended in Phase 49b-f for additional cross-module audits. |
| `isomers.py` | **Phase 48a (round 170)** — isomer-relationship core for the upcoming Phase-48 isomers exploration tool.  RDKit-backed.  `RELATIONSHIPS` canonical 7-tuple (`identical` / `constitutional` / `enantiomer` / `diastereomer` / `meso` / `tautomer` / `different-molecule`).  `IsomerEnumerationResult` frozen dataclass (input_smiles / canonical_smiles_list / truncated).  Three public enumerators / classifiers: `enumerate_stereoisomers(smiles, max_results=16)` wraps RDKit's `EnumerateStereoisomers` with `onlyUnassigned=True` so a fully-specified input returns just itself while an under-specified input expands to every consistent stereoisomer; `enumerate_tautomers(smiles, max_results=16)` wraps `MolStandardize.TautomerEnumerator` (covers keto/enol, amide/iminol, hydroxypyridine/pyridone, nitroso/oxime, ~20 documented rules); `classify_isomer_relationship(smiles_a, smiles_b)` is the core comparator that walks an 8-step decision tree to return one of the RELATIONSHIPS strings (identical → enantiomer-via-stereo-inversion → meso → diastereomer → tautomer-via-enumeration → constitutional-via-formula-match → different-molecule fallback).  Plus `molecular_formula(smiles)` + `_canonical(smi)` + `_canonical_no_stereo(smi)` helpers.  No Qt imports; fully headless-testable.  Phase 48b (dialog), 48c (agent actions), 48d (inline 'View isomers' workspace button), 48e (tutorial cross-link) ship in subsequent rounds. |
| `biochemistry_by_kingdom.py` | **Phase 47a (round 166)** — biochemistry-by-kingdom catalogue for the upcoming Macromolecules-style explorer.  `KingdomTopic` frozen dataclass (id / kingdom ∈ {eukarya, bacteria, archaea, viruses} / subtab ∈ {structure, physiology, genetics} / title / body markdown / cross_reference_cell_component_ids tuple → Phase-43 ids / cross_reference_pathway_ids tuple → Phase-42 ids / cross_reference_molecule_names tuple / notes) + 60 entries — exactly **15 per kingdom × 4 kingdoms × 3 sub-tabs = 60** balanced grid: **eukarya/structure** (plasma membrane architecture, organelles + endomembrane, nucleus + NPC, ECM + plant + fungal cell walls, three-filament cytoskeleton); **eukarya/physiology** (aerobic respiration, photosynthesis, cell cycle + mitosis, GPCR signalling, multicellular development + morphogen gradients); **eukarya/genetics** (chromatin + nucleosomes, RNA splicing, meiosis + recombination, telomeres + senescence, endosymbiotic origin); **bacteria/structure** (gram divide, prokaryotic minimalism, flagellar rotary motor, biofilms + EPS, capsule + virulence); **bacteria/physiology** (anaerobic fermentation + diverse e⁻ acceptors, binary fission + FtsZ, quorum sensing, sporulation + endospores, secondary metabolism + natural-product antibiotics); **bacteria/genetics** (circular chromosome + nucleoid, HGT — transformation/transduction/conjugation, CRISPR-Cas adaptive immunity, restriction-modification systems, evolutionary rate); **archaea/structure** (ether-linked isoprenoid lipids — the lipid divide, pseudopeptidoglycan + S-layers, extremophile adaptations, archaellum convergent rotary motor, cellular minimalism); **archaea/physiology** (methanogenesis — exclusively archaeal, no human pathogens, syntrophic partners + anaerobic methane oxidation, bacteriorhodopsin + light-driven proton pumps, psychrophilic + acidophilic archaea); **archaea/genetics** (eukaryote-like transcription + translation, archaeal histones + chromatin precursors, Asgard archaea + eocyte hypothesis, archaeal CRISPR-Cas, deep evolutionary roots + LUCA); **viruses/structure** (capsid architectures, enveloped vs naked, spike glycoproteins + receptor binding, Baltimore classification, bacteriophage architectures); **viruses/physiology** (generic 6-stage life cycle, lytic vs lysogenic phage cycles, mutation rates + quasispecies, cell + tissue tropism, immune evasion); **viruses/genetics** (NOT a kingdom + why, endogenous retroviruses + host-genome contributions like syncytin/placenta, virus-host arms race + Red Queen, viroids + RNA-world relics, pandemic emergence + spillover).  Cross-references resolve to real Phase-43 cell-component ids + Phase-42 metabolic-pathway ids — guarded by tests so future renames + edits surface immediately.  Lookup helpers `list_topics(kingdom, subtab)`, `get_topic(id)`, `find_topics(needle)` (case-insensitive substring across id + title + body + xref fields), `kingdoms()`, `subtabs()`, `topic_to_dict(t)`.  No Qt imports; fully headless-testable. |
| `cell_components.py` | **Phase 43 (round 151)** — cell-component explorer (Eukarya / Bacteria / Archaea).  `CellComponent` frozen dataclass (id / name / domain ∈ {eukarya, bacteria, archaea} / sub_domains tuple ∈ {animal, plant, fungus, protist, gram-positive, gram-negative} / category ∈ {membrane, organelle, nuclear, cytoskeleton, envelope, appendage, extracellular, ribosome, genome} / location / function / constituents tuple of `MolecularConstituent` / notable_diseases / notes) + nested `MolecularConstituent` dataclass (name / role / notes / cross_reference_molecule_name).  41 components: 24 eukaryotic (eukaryotic plasma membrane, RER, SER, Golgi, mitochondrion, chloroplast, lysosome, vacuole, peroxisome, proteasome, 80S ribosome, nuclear envelope, nucleolus, chromatin, telomere, centromere/kinetochore, actin microfilament, microtubule, intermediate filament, centrosome, eukaryotic cilium/flagellum, animal ECM, plant cell wall, fungal cell wall) + 11 bacterial (bacterial plasma membrane, gram+ peptidoglycan, gram- peptidoglycan, gram- outer membrane, bacterial nucleoid, plasmid, bacterial flagellum, pilus/fimbria, capsule, biofilm EPS, 70S ribosome) + 6 archaeal (archaeal plasma membrane with ether-linked isoprenoid lipids, pseudopeptidoglycan, S-layer, archaeal 70S ribosome with eukaryote-like translation machinery, archaeal nucleoid with histone-like proteins, archaellum).  Each constituent can carry a `cross_reference_molecule_name` pointing back to a Phase-6 molecule-DB row (e.g. cholesterol on the eukaryotic plasma membrane resolves to the seeded `Cholesterol` row).  Lookup helpers `list_components(domain, sub_domain)` (sub-domain query: components with empty sub_domains tuple match any sub-domain within their domain — so mitochondrion appears under sub_domain="animal" without being animal-specific), `get_component(id)`, `find_components(needle)` (across id + name + function + constituent names + notes), `components_for_category(category)`, `domains()`, `sub_domains()`, `categories()`, `component_to_dict(c)`.  No Qt imports; fully headless-testable. |
| `microscopy.py` | **Phase 44 (round 150)** — microscopy across resolution scales.  `MicroscopyMethod` frozen dataclass (id / name / abbreviation / resolution_scale ∈ {whole-organism, tissue, cellular, sub-cellular, single-molecule, clinical-histology} / sample_types tuple ∈ {live-organism, fixed-tissue, live-cells, fixed-cells, isolated-organelles, single-molecules, biopsy, non-biological} / typical_resolution / light_source / contrast_mechanism / typical_uses / strengths / limitations / representative_instruments / cross_reference_lab_analyser_ids tuple / notes) + 30 entries across all 6 resolution scales: **whole-organism** (stereo dissecting, intra-vital, OCT, small-animal MRI), **tissue** (brightfield H&E, multiplex IHC CODEX/Vectra, light-sheet, MALDI imaging, polarised-light), **cellular** (phase contrast, DIC Nomarski, widefield epifluorescence, laser-scanning confocal, spinning-disk confocal, two-photon multi-photon), **sub-cellular** (SIM, STORM, PALM, STED, Airyscan, TIRF), **single-molecule** (smFRET, cryo-EM, cryo-ET, AFM, STM), **clinical-histology** (clinical light microscope, frozen-section cryostat, clinical IHC, digital-pathology slide scanner).  Cross-references to Phase-40a `lab_analysers.py` for instruments that appear both as an *instrument* (40a) and a *resolution-anchored teaching view* (44) — e.g. `confocal` xrefs `zeiss_lsm_980`, `cryo-em` + `cryo-et` xref `thermo_krios_g4`, `light-sheet` xrefs `zeiss_lattice_lightsheet`, `maldi-imaging` xrefs `bruker_biotyper`.  Lookup helpers `list_methods(resolution_scale)`, `get_method(id)`, `find_methods(needle)` (across id + name + abbreviation + typical_uses + representative_instruments), `methods_for_sample_type(sample)` (e.g. `methods_for_sample_type("live-cells")` returns phase-contrast / widefield / spinning-disk / 2P / TIRF), `resolution_scales()`, `sample_types()`, `method_to_dict(m)`.  No Qt imports; fully headless-testable. |
| `lab_reagents.py` | **Phase 45 (round 149)** — off-the-shelf lab-reagents reference catalogue.  `LabReagent` frozen dataclass (id / name / category / typical_concentration / storage / hazards / preparation_notes / cas_number / typical_usage / notes) + 75 entries across 10 categories: `buffer` (Tris-HCl, HEPES, MOPS, MES, PBS, TBS, citrate, carbonate, glycine-HCl, McIlvaine, BIS-TRIS), `acid-base` (HCl 1 M / 6 N, conc. H₂SO₄, conc. HNO₃, glacial AcOH, NaOH, KOH, conc. NH₄OH), `detergent` (SDS, Triton X-100, Tween 20, NP-40 / Igepal CA-630, CHAPS, n-octyl-glucoside), `reducing-agent` (DTT, BME, TCEP, GSH), `salt` (NaCl, KCl, MgCl₂, CaCl₂, MgSO₄, AmSO₄, EDTA, EGTA), `protein-prep` (BSA, protease-inhibitor cocktail, phosphatase-inhibitor cocktail), `stain` (Coomassie R-250 / G-250, ethidium bromide, SYBR Safe, AgNO₃, methylene blue, crystal violet), `solvent` (DMSO, DMF, ethanol abs, methanol, acetone, chloroform, hexane, THF, DCM, acetonitrile), `cell-culture` (DMEM, RPMI-1640, MEM, F-12, Opti-MEM, FBS, trypsin-EDTA, Pen-Strep, L-glutamine), `molecular-biology` (dNTPs, agarose, Taq / Phusion polymerases, EcoRI / BamHI restriction enzymes, T4 DNA ligase, RNase A, RNase-free DNase I, proteinase K).  Each entry is a long-form bench card with the practical handling tips (e.g. SDS precipitates < 15 °C — rewarm; Tris pH-drifts ~0.03/°C, always pH at use temperature; DMSO freezes at 18.5 °C; vanadate must be activated; EtBr is mutagenic; Phusion has ~50× lower error rate than Taq).  Lookup helpers `list_reagents(category)`, `get_reagent(id)`, `find_reagents(needle)` (across id + name + category + typical_usage + cas_number — CAS searches like "67-68-5" → DMSO work directly), `categories()`, `reagent_to_dict(r)`.  No Qt imports; fully headless-testable. |
| `ph_explorer.py` | **Phase 46 (round 148)** — pH + buffer explorer headless data core. Three frozen dataclasses + helpers: `AcidEntry` (id / name / formula / category ∈ {mineral, carboxylic, amine, amino-acid, phenol, biological-buffer, other} / pka_values tuple / notes), `ReferenceCard` (id / title / body markdown). 46-acid pKa catalogue across 7 categories — mineral (HCl, H₂SO₄, H₃PO₄, HNO₃, HF, H₂CO₃, H₂S, HClO₄), carboxylic (formic, acetic, propionic, lactic, citric, oxalic, malonic, malic, tartaric, benzoic, ascorbic), amine (ammonium, methyl-/dimethyl-/trimethylammonium, pyridinium, imidazolium), amino-acid (gly / ala / asp / glu / his / lys / arg / cys / tyr — α-COOH + α-NH₃⁺ + sidechain pKas), phenol (phenol, p-nitrophenol, 2,4,6-trinitrophenol), biological-buffer (Tris 8.10, HEPES 7.55, MES 6.10, MOPS 7.20, BIS-TRIS 6.50, PIPES 6.76, CHES 9.30), other (HCN, H₂O₂). 6 reference cards (ph_definition, strong_weak, henderson_hasselbalch, buffer_capacity, polyprotic, biological_buffers). Solvers: `design_buffer(target_pH, pKa, total_concentration_M, volume_L)` → ratio + [HA] / [A⁻] split + moles + capacity_warning + capacity_message; `buffer_capacity(total_concentration_M, pH, pKa)` → β = 2.303 · C · α · (1 − α) + α + fraction_of_max; `titration_curve(weak_acid_pKa, acid_initial_M, volume_acid_mL, base_concentration_M, n_points)` → (vol_mL, pH) points + equivalence_point_mL via charge-balance solve. Lookup helpers `list_acids(category)`, `get_acid(id)`, `find_acids(needle)`, `categories()`, `acid_to_dict(a)`. No Qt imports; fully headless-testable. |
| `metabolic_pathways.py` | **Phase 42a (round 147)** — major metabolic-pathway catalogue with per-step substrates / enzymes / products / ΔG / regulators.  Three frozen dataclasses: `RegulatoryEffector` (name / mode ∈ {activator, inhibitor} / mechanism), `PathwayStep` (step_number / substrates / enzyme_name / ec_number / products / reversibility ∈ {reversible, irreversible} / delta_g_kjmol / regulatory_effectors / notes), `Pathway` (id / name / category / cellular_compartment / overview / overall_delta_g_kjmol / textbook_reference / steps).  11 seeded pathways across 4 of 5 categories: `central-carbon` (glycolysis 10 steps, TCA cycle 8 steps, ox-phos / ETC 5 complexes, pentose phosphate 5 steps), `lipid` (β-oxidation 4 steps, fatty-acid biosynthesis 3 stages, cholesterol biosynthesis 6 stages), `amino-acid` (urea cycle 5 steps), `specialised` (heme biosynthesis 8 steps, Calvin cycle 5 stages, glycogen metabolism 5 steps).  `nucleotide` category reserved for purine + pyrimidine de-novo (42a follow-up).  ΔG values from Nelson & Cox 8e; EC numbers from IUBMB / BRENDA.  Each step's `regulatory_effectors` captures the textbook regulators (e.g. PFK-1 step in glycolysis lists ATP / Citrate / AMP / Fructose-2,6-bisphosphate; HMG-CoA reductase lists Cholesterol / oxysterols / AMPK / Statins).  Lookup helpers + per-pathway and per-step `to_dict`. |
| `lab_analysers.py` | **Phase 40a (round 146)** — major-lab-analyser reference catalogue.  `LabAnalyser` frozen dataclass (id / name / manufacturer / category / function / typical_throughput / sample_volume / detection_method / typical_assays / strengths / limitations / notes) + 28 entries across 10 categories: `clinical-chemistry` (Roche cobas c702, Siemens Atellica CH 930, Beckman AU5800, Abbott Alinity c), `hematology` (Sysmex XN-1000, Beckman DxH 900), `coagulation` (Stago STA R Max 3, Sysmex CS-5100), `immunoassay` (Roche cobas e801, Abbott Alinity i, Siemens Atellica IM), `molecular` (cobas 8800, Hologic Panther, Cepheid GeneXpert, Illumina NovaSeq X, Oxford Nanopore PromethION), `mass-spec` (SCIEX QTRAP 7500, Bruker MALDI Biotyper), `functional` (Molecular Devices FLIPR Penta, PerkinElmer Operetta CLS), `microscopy` (Zeiss LSM 980, Zeiss Lattice Lightsheet 7, Thermo Krios G4 cryo-TEM), `automation` (Hamilton STAR, Tecan Fluent, Opentrons OT-2), `storage` (Hamilton BiOS, Thermo Galileo).  Each entry is a long-form reference card capturing the instrument's clinical / research role + the strengths-vs-limitations trade-off.  Lookup helpers + `to_dict`. |
| `centrifugation.py` | **Phase 41 (round 144)** — centrifugation reference catalogue + g↔rpm calculator.  Three frozen dataclasses: `Centrifuge` (id / name / manufacturer / centrifuge_class ∈ {microfuge, benchtop, high-speed, ultracentrifuge} / max_speed_rpm / max_g_force / typical_capacity / refrigerated / typical_uses / notes), `Rotor` (id / name / rotor_type ∈ {fixed-angle, swinging-bucket, vertical, continuous-flow} / max_radius_cm / min_radius_cm / max_speed_rpm / typical_tubes / notes), `Application` (id / name / protocol_class ∈ {differential, density-gradient, cell-pellet, protein-concentration} / recommended_g_force / recommended_duration / recommended_rotor_type / description / notes).  Catalogue: 9 centrifuges (Eppendorf 5424/5425/5810/5910 + Beckman Allegra/Avanti + Sorvall RC-6/WX 100 + Beckman Optima XPN), 10 rotors (microfuge / benchtop / high-speed JA-25.50 / JA-10 / JLA-8.1000 / ultracentrifuge Ti-70 / SW 41 Ti / TLA-100 / VTi 50), 8 applications (cell pelleting mammalian + E. coli, differential organelle prep, sucrose / CsCl gradient, Amicon concentration, exosome isolation, serum separation).  Headless solvers `rpm_to_g(rpm, radius_cm)` / `g_to_rpm(g_force, radius_cm)` using `g = G_FORCE_CONSTANT · RPM² · r` with `G_FORCE_CONSTANT = 1.118e-5` — verified against the Eppendorf 5424 data sheet (15 000 RPM @ 8.4 cm = 21 130 × g exactly).  Lookup helpers + `to_dict` per dataclass. |
| `calc_solution.py` / `calc_stoichiometry.py` / `calc_acid_base.py` / `calc_gas_law.py` / `calc_colligative.py` / `calc_thermo_kinetics.py` / `calc_equilibrium.py` | **Phase 39a (round 142)** — headless lab-calculator solvers.  Seven sibling modules covering ~30 routine bench calculations.  Every solver follows the Phase-37d `beer_lambert_solve` pattern: pass any N-1 of N quantities (use `None` for the unknown), get the full set back with the Nth filled in, raise `ValueError` on missing-count != 1 or non-positive input.  **`calc_solution.py`**: `molarity_solve(mass_g, molarity_M, volume_L, molecular_weight_gmol)` (m = M·V·MW), `dilution_solve(M1, V1, M2, V2)` (M₁V₁ = M₂V₂), `serial_dilution(initial, factor, n_steps)`, `molarity_from_mass_percent(%w/w, density, MW)` (e.g. concentrated HCl 37 % w/w, ρ 1.18 → 12 M), `ppm_to_molarity` / `molarity_to_ppm`.  **`calc_stoichiometry.py`**: `limiting_reagent([{name, moles, stoich_coeff}, …])` (returns the index + name + per-reagent equivalent units), `theoretical_yield_g`, `percent_yield(actual, theoretical, percent)` (any 2 of 3), `percent_purity`.  **`calc_acid_base.py`**: `ph_from_h` / `h_from_ph` (returns full pH/pOH/[H⁺]/[OH⁻]), `pka_to_ka` / `ka_to_pka`, `henderson_hasselbalch(pH, pKa, base_acid_ratio)` (any 2 of 3 — the buffer-design entry point).  **`calc_gas_law.py`**: `R_L_ATM_PER_MOL_K = 0.0820573661` constant, `ideal_gas_solve(P, V, n, T)` (any 3 of 4), `combined_gas_law(P1/V1/T1/P2/V2/T2)` (any 5 of 6), `gas_density(P, MW, T)` (ρ = PM/RT).  **`calc_colligative.py`**: `SOLVENT_CONSTANTS` table (water / benzene / chloroform / acetic acid / ethanol / CCl₄ / cyclohexane / camphor — K_b + K_f), `boiling_point_elevation` / `freezing_point_depression` (any 3 of 4 quantities OR pass `solvent="water"` to auto-fill K_b/K_f), `osmotic_pressure(M, T, i, P)` (Π = MRT·i).  **`calc_thermo_kinetics.py`**: `R_J_PER_MOL_K`, `K_B`, `H_PLANCK` constants, `heat_capacity_solve(q, m, c, ΔT)` (q = mcΔT — q + ΔT can be negative), `hess_law_sum([step ΔH])` (multi-step ΔH accumulator), `first_order_half_life(k OR t½)` (t½ = ln 2 / k), `first_order_integrated([A]_0, [A]_t, k, t)`, `arrhenius_solve(k, A, Ea, T)` (k = A·exp(-Ea/RT), any 3 of 4), `eyring_rate_constant(ΔG‡, T)` (k = (k_B·T/h)·exp(-ΔG‡/RT)).  **`calc_equilibrium.py`**: `equilibrium_constant_from_concentrations([{name, conc, coeff, side}, …])` (K = Π[product]^coeff / Π[reactant]^coeff), `ksp_from_solubility(s, n, m)` / `solubility_from_ksp(K_sp, n, m)` for AnBm salts, `ice_solve_a_plus_b(K, A₀, B₀, C₀, D₀)` (closed-form quadratic ICE solver for A + B ⇌ C + D with all coeffs = 1; picks the chemically-meaningful root via `_pick_chem_root`).  Phase 39b dialog + 39c agent actions queued for the next two rounds. |
| `lab_setups.py` | **Phase 38b (round 141)** — canonical lab-apparatus configurations + connection validator.  `Setup` frozen dataclass (id / name / purpose / equipment ids in display order / `SetupConnection` records / procedure / safety_notes / pedagogical_notes / typical_reactions / icon_id) + `SetupConnection` (from_equipment_idx / from_port / to_equipment_idx / to_port / note).  Equipment refs are indices into the setup's equipment list (not ids) so the same piece can appear twice in one setup (pot + receiver RBF, two Erlenmeyers in extraction).  8 seeded setups: simple distillation, fractional distillation (= simple + Vigreux column), standard reflux, reflux with controlled addition (3-neck RBF + addition funnel + thermometer), Soxhlet extraction, vacuum filtration (Büchner + filter flask + cold trap + aspirator), liquid-liquid extraction, recrystallisation.  `validate_setup(setup)` walks every connection, looks up the named ports on the referenced equipment via the Phase-38a catalogue, and returns a list of error strings (empty = valid).  Validation rules: equipment indices in range, port names exist, joint types match (with `open` as wildcard for non-glass-joint contact like clamp grip / hot-plate top), male ↔ female complementarity for ground-glass joints (skip for `hose` / `socket` / `open`).  Lookup helpers `list_setups()` / `get_setup(id)` / `find_setups(needle)` (case-insensitive substring across id + name + purpose) / `to_dict(setup)`.  Sets up the future Phase-38c canvas's snap-validation logic — when a user drags equipment from the palette onto the canvas, the same `validate_setup` call surfaces real-time port-mismatch errors. |
| `lab_equipment.py` | **Phase 38a (round 140)** — lab-equipment reference catalogue + first piece of the multi-round Phase-38 lab-setup simulator.  `Equipment` frozen dataclass (id / name / category / description / typical_uses / variants / safety_notes / icon_id / connection_ports) + `ConnectionPort` frozen dataclass (name / location / joint_type / is_male) for the future Phase-38c canvas's snap-validation logic.  42-entry catalogue across 12 categories: `glassware` (4), `adapter` (6), `condenser` (6), `heating` (5), `cooling` (2), `separation` (3), `filtration` (3), `vacuum` (4), `stirring` (2), `support` (4), `safety` (2), `analytical` (1).  Joint-type vocabulary includes ANSI ground-glass (`14/20`, `19/22`, `24/29`, `29/32`), `hose` (rubber tubing), `socket` (electrical), `open` (no-constraint), and a handful of equipment-specific joints (`thermometer-bulb`, `filter-paper`, `MP-capillary`, etc.).  Lookup helpers `list_equipment(category)` / `get_equipment(id)` / `find_equipment(needle)` (case-insensitive substring across id + name + category) / `categories()` / `to_dict(equipment)` (ports serialise as a list of dicts so the agent action returns JSON-friendly data).  Reference data only; canvas + setup simulator land in 38b-38f. |
| `spectrophotometry_methods.py` | **Phase 37d (round 139)** — spectrophotometry-method reference catalogue.  `SpectrophotometryMethod` frozen dataclass (id / name / abbreviation / category / principle / light_source / sample_handling / detector / wavelength_range / typical_analytes / strengths / limitations / procedure / notes) + 12-entry catalogue across 5 categories: `molecular-uv-vis` (UV-Vis, fluorescence), `molecular-ir` (IR/FTIR, ATR-FTIR, NIR, Raman, SERS), `molecular-chirality` (CD), `atomic` (AAS, ICP-OES, ICP-MS), `magnetic-resonance` (NMR).  Each entry is a long-form reference card; IR/FTIR + NMR entries cross-reference the existing `core/spectroscopy.py` and `core/nmr.py` *predictors* so users see the descriptive vs predictive split.  Lookup helpers `list_methods(category)` / `get_method(id)` / `find_methods(needle)` (case-insensitive substring across id + name + abbreviation) / `categories()` / `to_dict(method)`.  Plus `beer_lambert_solve(absorbance, molar_absorptivity, path_length_cm, concentration_M)` quantitative helper — pass any 3 of 4 quantities and get the 4th, with positive-input + exactly-one-missing validation. |
| `chromatography_methods.py` | **Phase 37c (round 138)** — chromatography-method reference catalogue.  `ChromatographyMethod` frozen dataclass (id / name / abbreviation / category / principle / stationary_phase / mobile_phase / detectors / typical_analytes / strengths / limitations / procedure / notes) + 15-entry catalogue across 7 categories: `planar` (TLC, paper), `preparative-column` (gravity column, flash), `gas` (GC, GC-MS), `liquid` (HPLC, LC-MS, HILIC), `protein` (FPLC, IEX, SEC, affinity), `ion` (IC), `supercritical` (SFC).  Each entry is a 200-400-word reference card surfacing the principle + the strengths / limitations trade-off explicitly.  Lookup helpers `list_methods(category)` / `get_method(id)` / `find_methods(needle)` (case-insensitive substring across id + name + abbreviation) / `categories()` / `to_dict(method)`.  Reference data only; no separation simulation runs. |
| `clinical_panels.py` | **Phase 37b (round 137)** — clinical-chemistry lab-panel catalogue.  `LabAnalyte` (frozen dataclass: id / name / abbreviation / category / units / normal_range / clinical_significance / notes) + `LabPanel` (frozen dataclass: id / name / short_name / purpose / sample / procedure / fasting / analytes / notes).  21 unique analytes across 7 categories (electrolyte / kidney / liver / lipid / metabolic / hormone / vitamin) reused by 5 seeded panels: **BMP** (8 analytes — glucose / Ca / Na / K / Cl / HCO₃ / BUN / creatinine), **CMP** (BMP + 6 liver/protein), **Lipid Panel** (TC / LDL / HDL / TG), **Diabetes follow-up** (HbA1c + glucose), **Thyroid** (TSH + free T4), **Vitamin D screening** (25(OH)D + Ca).  CMP literally shares the BMP analyte instances (frozen dataclass, identity-equal).  Lookup helpers `list_panels()` / `get_panel(id)` / `list_analytes(category)` / `get_analyte(id)` / `find_analyte(needle)` (case-insensitive name + abbreviation + id) / `categories()` / `analyte_to_dict()` / `panel_to_dict()`.  Reference data only — not a clinical decision-support tool. |
| `qualitative_tests.py` | **Phase 37a (round 136)** — qualitative inorganic-test catalogue.  `InorganicTest` dataclass + 32-entry catalogue across 7 categories: `flame` (Li / Na / K / Ca / Sr / Ba / Cu / Cs), `hydroxide` (Cu²⁺ / Fe²⁺ / Fe³⁺ / Al³⁺ / Mg²⁺ / Ca²⁺ / Zn²⁺ / Pb²⁺ / Mn²⁺), `halide` (Cl⁻ / Br⁻ / I⁻), `sulfate` (SO₄²⁻), `carbonate` (CO₃²⁻ / HCO₃⁻), `ammonium` (NH₄⁺), `gas` (H₂ / O₂ / CO₂ / Cl₂ / NH₃ / HCl / SO₂ / NO₂).  Each entry: `id` / `name` / `category` / `target` (Unicode ion label, e.g. `"Cu²⁺"`) / `target_class` (`cation` / `anion` / `gas`) / `reagents` / `procedure` / `positive_observation` / `colour_hex` (for the dialog's swatch) / `notes` (interferences + follow-up tests + amphoteric flags).  Lookup helpers `list_tests(category)` / `get_test(test_id)` / `find_tests_for(target)` (case + Unicode-sub/superscript-tolerant — `"Cu2+"` and `"Cu²⁺"` and `"cu  2  +"` all hash the same via `_normalise_ion_label`) / `categories()` / `to_dict(test)`.  No Qt imports; fully headless-testable. |
| `drawing_scheme.py` | **Phase 36f.1 (round 131)** — reaction-scheme data core for the drawing tool. `Scheme` dataclass (`lhs`: `List[Structure]`, `rhs`: `List[Structure]`, `arrow` ∈ {`forward`, `reversible`}, `reagents` free-text) + `from_smiles_pair(lhs, rhs, arrow, reagents)`, `from_reaction_smiles("LHS>reagents>RHS")`, `to_reaction_smiles()`, `lhs_smiles()` / `rhs_smiles()`, JSON-friendly `to_dict()` / `from_dict(payload)`.  `is_balanced_atom_counts(scheme)` heavy-atom-count sanity hint for the future GUI's "did you forget the leaving group?" prompt.  `"."`-separated SMILES on either side are exploded into per-component `Structure`s so a multi-substrate scheme like `"CC(=O)Cl.NC"` lands as two LHS structures.  Empty halves serialise as the empty string (`""` / `"CCO>>"` / `">>"`) to match RDKit reaction-SMILES convention.  No Qt imports; RDKit lazy-imported so the dataclass is usable in environments without RDKit.  Used by the `make_reaction_scheme` agent action.  Sets up Phase 36f.2 (canvas-arrow tool + Reactions-tab handoff) for round 132. |
| `drawing_templates.py` | **Phase 36c (round 129)** — ring + functional-group template catalogue for the drawing canvas.  `Template` / `TemplateAtom` / `TemplateBond` dataclasses + 20-row catalogue: 10 rings (cyclopropane / cyclobutane / cyclopentane / cyclohexane / benzene / pyridine / pyrimidine / furan / thiophene / pyrrole) + 10 FGs (OH / NH₂ / Me / COOH / CHO / C=O / NO₂ / CN / OMe / CF₃).  `apply_template(structure, positions, template, anchor_pos, host_atom_idx, scale)` — pure function that returns a fresh `(Structure, positions)` tuple.  Two fuse modes: `"merge"` (rings — anchor atom fuses with host, n-1 atoms appended), `"attach"` (FGs — anchor atom is added + bonded to host with `attach_order`-many bonds, with optional `auto_attach_element` for empty-canvas placement so e.g. clicking COOH on empty canvas yields acetic acid).  Catalogue helpers `list_template_names()` / `list_templates(kind)` / `get_template(name)`.  Unit-bond-length coords scaled by `DEFAULT_SCALE_PX = 42.0` (matches DrawingPanel's `_BOND_PX`); y is flipped at placement to match Qt's screen convention.  No Qt imports; headless-testable. |
| `sequence_view.py` | **Phase 34a (round 112)** — headless sequence-viewer data core. `SequenceView` (protein_chains + dna_chains + highlights) / `ChainSequence` (chain_id, one_letter, three_letter, residue_numbers, kind=protein/dna/rna) / `HighlightSpan` (chain_id, start, end, kind, label, colour) dataclasses with JSON-serialisable `to_dict()` for the Qt widget + agent action. `build_sequence_view(protein)` splits a Phase-24a `Protein` by majority residue-kind into protein vs DNA/RNA chains. `attach_contact_highlights(view, report)` + `attach_pocket_highlights(view, pockets)` stamp per-kind colour-coded spans via a shared `HIGHLIGHT_COLOURS` palette (pocket=green, ligand-contact=yellow, active-site=orange, h-bond=blue, salt-bridge=red, π-stacking=purple, hydrophobic=tan, …). Agent action `get_sequence_view(pdb_id, include_contacts, ligand_name)` wrapped in `agent/actions_protein.py`. No Qt imports; fully headless-testable. |
| `stereo.py` | `assign_rs(mol)`, `assign_ez(mol)`, `stereocentre_atoms(mol)`, `flip_stereocentre(mol, idx)`, `enantiomer_of(mol)`, `summarise(mol)` — canonical CIP / E-Z API (cross-cutting stereochem helper). Wraps RDKit's `AssignStereochemistry`. |
| `druglike.py` | `lipinski(mol)`, `veber(mol)`, `ghose(mol)`, `pains(mol)`, `qed_score(mol)`, `drug_likeness_report(mol)` — medicinal-chem descriptor panel (Phase 19b). |
| `chromatography.py` | `predict_rf(smiles, solvent)`, `simulate_tlc(smiles_list, solvent)`, `solvent_polarity(name_or_mixture)` — TLC/Rf teaching predictor (Phase 15b). |
| `lab_techniques.py` | `solubility_curve`, `recrystallisation_yield`, `distillation_plan`, `extraction_plan`, `fraction_ionised` — practical-lab teaching helpers (Phase 15a-lite). |
| `physical_organic.py` | **Phase 17e** — `hammett_fit(data, sigma_type)` least-squares regresses log(k/k₀) against a curated Hammett σ table (σₘ, σₚ, σₚ⁻, σₚ⁺ for ~15 common substituents) and returns ρ, r², the fit line, and a teaching-grade interpretation (sign / magnitude of ρ); `predict_kie(isotope_pair, partner_element, nu_H_cm1, temperature_K)` computes the primary KIE from the Bigeleisen simplification (ZPE difference driven by reduced-mass ratio). Numpy-free; agent-action wrappers in `agent/actions_phys_org.py`. |
| `glossary_figures.py` | `render_term(term, smiles, out_dir)` + `regenerate_all(out_dir)` — incremental PNG/SVG generator for the Phase 26a `example_smiles` field. Delegates to `draw2d` (single molecules) or `draw_reaction` (SMILES with `>>`). `term_slug()` normalises term names into filename stems; `default_figure_dir()` points at `data/glossary/`. Companion script `scripts/regen_glossary_figures.py`, agent action `get_glossary_figure(term, path)`. (Phase 26b) |
| `molecule_tags.py` | `auto_tag(mol_or_smiles)` → `TagResult` with functional-group / composition / charge / size-band / ring-band / stereo tags. 27 SMARTS-based functional groups (carboxylic acid → phosphate), 7 composition flags (halogen / P / S / pure-organic / metal / …), 4 charge categories (neutral / cation / anion / zwitterion), 3 size bands (≤ 12 / 13-30 / ≥ 31 heavy atoms), 3 ring-count bands. `FILTER_AXES` + `list_filter_axes()` surface the taxonomy for the filter-bar UI — includes the **source** axis (drug-class / NSAID / statin / alkaloid / hormone / steroid / fatty-acid / …) curated by `seed_source_tags.py`. (Phase 28c + 28b) |
| `carbohydrates.py` | `Carbohydrate` dataclass + 25-row `CARBOHYDRATES` catalogue covering monosaccharides (glucose α/β/open-chain, fructose, ribose / 2-deoxyribose, galactose, mannose, tagatose), aminosugars (glucosamine, GlcNAc), uronic acids (glucuronic), deoxy sugars (fucose, rhamnose), sugar alcohols (sorbitol, mannitol, xylitol), disaccharides (sucrose, lactose, maltose, cellobiose, trehalose), polysaccharide fragments (amylose α-1,4, cellulose β-1,4). `list_carbohydrates(family)`, `get_carbohydrate(name)`, `families()` helpers. (Phase 29a + 31h) |
| `identity.py` | **Round 58** — molecular-identity utilities shared across every catalogue. `canonical_smiles(smi)` via RDKit; `inchikey(smi)` as the gold-standard identity hash; `same_molecule(a, b)` safe wrapper; `normalise_name(name)` for case-/parenthetical-tolerant name matching ("Retinol (vitamin A)" → "retinol"). Used by the DB query helpers, the PubChem importer, and `add_molecule` / `add_molecule_synonym` so the same compound can't be stored twice under different-looking SMILES or names. |
| `lipids.py` | `Lipid` dataclass + 31-row `LIPIDS` catalogue across families `fatty-acid` (C8 caprylic → C22 DHA, ω-3 / ω-6 / ω-9 tags, plus eicosanoids PGE2 / TXA2), `triglyceride` (tripalmitin, triolein), `phospholipid` (POPC, POPE, phosphatidic acid), `sphingolipid` (ceramide, sphingomyelin), `sterol` (cholesterol, ergosterol; bile acids cholic / taurocholic; hormones testosterone / estradiol / progesterone / cortisol), and fat-soluble `vitamin` / hormone (vitamin D₃, retinol A, α-tocopherol E). Chain-length / unsaturation-count / ω-designation / melting-point metadata. `list_lipids(family)`, `get_lipid(name)`, `lipid_families()` helpers. (Phase 29b + 31i) |
| `nucleic_acids.py` | `NucleicAcidEntry` dataclass + 33-row `NUCLEIC_ACIDS` catalogue across families `nucleobase` (A/G/C/T/U + m6A / m5C; hypoxanthine, xanthine), `nucleoside` (adenosine / guanosine / cytidine / uridine / thymidine / 2'-deoxyadenosine; inosine, pseudouridine Ψ), `nucleotide` (ATP, cAMP, GTP, NAD⁺ / NADH / NADPH, FAD, CoA, SAM), `oligonucleotide` (ApG dinucleotide, GCGCUUUUGCGC RNA hairpin), and `pdb-motif` (1BNA B-DNA dodecamer, 1RNA, 143D G-quadruplex, 1EHZ tRNA-Phe, 1HMH hammerhead ribozyme). Strand = DNA / RNA tag. `list_nucleic_acids(family)`, `get_nucleic_acid(name)`, `nucleic_acid_families()` helpers. (Phase 29c + 31j) |
| `periodic_table.py` | `ELEMENTS` (full 1-118 list) + `Element` dataclass (symbol/name/Z/group/period/block/category/mass/electronegativity/oxidation-states/electron-configuration). `CATEGORY_COLOURS` palette keyed by category (alkali-metal / halogen / noble-gas / transition-metal / lanthanide / actinide / …). Masses pulled from RDKit's `GetPeriodicTable`. Lookup helpers `list_elements()`, `get_element(symbol_or_z)`, `elements_by_category(cat)`, `categories()`. Agent actions on a new **periodic** category. (Phase 27a) |

### `db/`
| File | Key symbols |
|------|-------------|
| `models.py` | SQLAlchemy ORM: `Molecule`, `Reaction`, `Tutorial`, `Tag`, `SynthesisPathway`, `SynthesisStep`, `GlossaryTerm` + M2M tables. |
| `session.py` | `init_db(cfg)`, `session_scope()` context manager. |
| `queries.py` | `list_molecules`, `get_molecule`, `find_molecule_by_name`, `add_molecule`, `count_molecules`, `list_reactions`, **`query_by_tags(axis_a, value_a, axis_b, value_b, text_query)`** (Phase 28d — AND-filters molecules by up to two tag axes + a free-text substring), `list_molecule_category_values()`. |
| `seed.py` | `seed_if_empty(cfg)` — chains to `seed_reactions_if_empty()`, `seed_mechanisms_if_empty()`, and `seed_pathways_if_empty()`. Additive backfill so existing DBs pick up new content on upgrade. |
| `seed_reactions.py` | 26 textbook named reactions; 6 of them carry atom-mapped SMARTS (using `[CH3:N]`-style explicit-H notation) for 3D side-by-side rendering. |
| `seed_molecules_extended.py` | Phase 6a extended seed: ~170 additional molecules across amino acids (complete 20), named reagents, drug library, biomolecules, dyes, PAHs, heterocycles, and a functional-group ladder. Additive by name. |
| `seed_mechanisms.py` | **Facade** — owns the name-substring → builder `_MECH_MAP`, the `SEED_VERSION` sentinel (bumped to 11 round 62), and the `seed_mechanisms_if_empty(force)` seeder. The 20 builder functions themselves live in three themed sub-modules so no file exceeds the 500-line cap. |
| `seed_mechanisms_classic.py` | 9 textbook mechanisms: SN1, SN2, E1, E2, Diels-Alder, Aldol condensation, Grignard addition, Wittig, Michael. Pure-arrow pedagogy, no Phase 13c decorations. |
| `seed_mechanisms_enzyme.py` | 4 enzyme-active-site mechanisms: chymotrypsin (serine-protease catalytic triad), class-I aldolase (Schiff-base aldol), HIV protease (aspartic-protease peptide hydrolysis), RNase A (2-step phosphoryl transfer). HIV and RNase entries exercise the Phase 13c lone-pair dot + bond-midpoint arrow features. |
| `seed_mechanisms_extra.py` | 7 Phase-31c expansion mechanisms (rounds 59-62): Fischer esterification (5-step acid catalysis), NaBH₄ reduction (1-step hydride transfer), nitration of benzene (3-step EAS through Wheland), Claisen condensation (4-step ester enolate), pinacol rearrangement (4-step with 1,2-methyl shift), **bromination of ethene** (3-step bromonium + anti addition, round 62), **Friedel-Crafts alkylation** (3-step EAS via methyl cation, round 62). |
| `seed_pathways.py` | 12 seeded synthesis pathways: Wöhler urea, Aspirin (industrial + Kolbe-Schmitt), Paracetamol (industrial + Hoechst 3-step), BHC Ibuprofen 3-step, Caffeine from theobromine, Phenacetin→Paracetamol, Vanillin from eugenol, Aniline from benzene 2-step, 2-Methyl-2-butanol via Grignard, **Met-enkephalin via Fmoc SPPS 5-step (Phase 16a)**. |
| `seed_energy_profiles.py` | 4 seeded reaction-coordinate energy profiles (SN2, SN1, E1, Diels-Alder) with textbook Ea / ΔH values. Versioned via `SEED_VERSION` so upgrades overwrite stale JSON. |
| `seed_glossary.py` | Base glossary catalogue (~51 terms across bonding / stereochemistry / mechanism / reactions / synthesis / spectroscopy / lab-technique categories). Short markdown definitions with alias + see-also lists. Extends itself with `seed_glossary_extra.EXTRA_TERMS` on import. |
| `seed_glossary_extra.py` | Phase 31f continued-expansion glossary terms (Saytzeff/Hofmann, Bürgi-Dunitz, KIE, HOMO/LUMO, endo rule, gauche, A-value, pharmacophore, prodrug, J-coupling — currently 10 entries). Kept separate from `seed_glossary.py` so the main seed file stays near the 500-line soft cap. |
| `seed_intermediates.py` | Phase 6f.3 — 119 intermediate molecules (carbocations, enolates, Fmoc-AAs, enzyme substrates, common ions, halides, etc.). Additive by name so re-runs skip duplicates. |
| `seed_coords.py` | Phase 6f.2 — one-shot backfill of `Molecule.molblock_2d` for every DB row, via `rdDepictor.SetPreferCoordGen(True) + Compute2DCoords`. Called automatically from `seed_if_empty`. |
| `seed_tags.py` | Phase 28a — backfill of functional-group / composition / charge / size / ring columns on every seeded molecule, driven by `core/molecule_tags.auto_tag`. Idempotent; called automatically from `seed_if_empty`. |
| `backfill_synonyms.py` | **Phase 35c (round 120)** — bulk PubChem synonym backfill for every `Molecule` row whose `synonyms_json` is empty (or below a caller-supplied threshold). `backfill_synonyms(limit, rate_delay_s, min_existing, fetch_fn, skip_test_prefix) → BackfillCounts`. Walks rows, skips `Tutor-test` names + empty-InChIKey rows, queries PubChem by InChIKey via `sources/pubchem.fetch_synonyms_by_inchikey`, filters registry-IDs (CAS / ChEMBL / UNII / InChI / InChIKey) through the palette-shared `_looks_like_registry_id`, merges deduplicated. Rate-limited (default 200 ms/req stays under PubChem's 5 req/sec free-tier cap). Per-row failures swallowed so one network hiccup doesn't abort the whole run. `fetch_fn` kwarg is test-injectable so pytest runs offline. Companion CLI `scripts/backfill_molecule_synonyms.py` with `--limit`, `--rate-delay`, `--min-existing` flags. |
| `cleanup.py` | **Round 94** — `purge_tutor_test_pollution(prefix="Tutor-test-")` + `PurgeCounts` dataclass.  Deletes any Molecule / Reaction / GlossaryTerm / SynthesisPathway (+ cascade) / Tutorial row whose name starts with the test-fixture prefix.  Invoked from `tests/conftest.py::pytest_sessionfinish` so future authoring-action test runs clean up their own trail (previously left ~165 glossary rows in a dev's local DB).  Also exposed via the standalone `scripts/cleanup_tutor_test_pollution.py` one-shot utility for users with pre-existing pollution.  Safe: idempotent, prefix-gated, real seeded content can't collide. |
| `seed_source_tags.py` | Phase 28b — hand-curated `{name → [source-tag, …]}` map covering NSAIDs / statins / antibiotics / SSRIs / β-blockers / hormones / steroids / neurotransmitters / alkaloids / nucleosides / sugars / fatty acids / dyes / reagent subclasses. Idempotent backfill into `Molecule.source_tags_json` with a version sentinel. `list_source_tag_values()` enumerates the full taxonomy for the filter bar. |
| `seed_synonyms.py` | **Round 58** — `seed_synonyms_if_needed()` fills `Molecule.synonyms_json` from (a) a curated `{canonical_name → [alias, …]}` map (Retinol ↔ Vitamin A, Aspirin ↔ Acetylsalicylic acid, Acetaminophen ↔ Paracetamol, …) and (b) cross-catalogue reconciliation — any row whose InChIKey matches a Lipid / Carbohydrate / Nucleic-acid catalogue entry inherits that entry's canonical name as a synonym. Idempotent; runs once on every `seed_if_empty()` call. |
| `seed_catalogue_molecules.py` | **Phase 49b (round 177)** — `seed_catalogue_molecules_if_needed()` backfills any Phase-29 lipid / carbohydrate / nucleic-acid catalogue entry + Phase-31k SAR-series variant whose InChIKey isn't already a `Molecule` row.  Generalises the round-58 InChIKey reconciliation by ADDING missing rows (tagged with source `carbohydrate-catalogue` / `lipid-catalogue` / `nucleic-acid-catalogue` / `sar-<series-id>`) rather than only adding aliases.  Catalogue molecules become first-class DB rows discoverable via the molecule browser, addressable by `find_molecule_by_name`, and available as substrates for descriptors / retrosynthesis / conformers.  Idempotent — re-running adds nothing because the InChIKey-uniqueness check skips any molecule already in the DB.  Audited by the round-177 catalogue-canonicalisation test suite under `tests/`. |

### `sources/` — online data plugins
| File | Key symbols |
|------|-------------|
| `base.py` | Abstract `DataSource.search / fetch`. |
| `pubchem.py` | `PubChemSource` via `pubchempy`. |
| `pdb.py` | `fetch_pdb(pdb_id)` → `Protein` with local-cache-first policy (`~/Library/Caches/OrgChem/pdb/`); `fetch_pdb_text`, `cached_pdb_path`, `parse_from_cache_or_string`, `clear_cache`. Phase 24a. |
| `alphafold.py` | `fetch_alphafold(uniprot_id)` → `AlphaFoldResult` with per-residue pLDDT + mean-pLDDT confidence bucket ("very high" / "confident" / "low" / "very low"); EBI AlphaFold DB v4 endpoint, cached under `~/Library/Caches/OrgChem/alphafold/`. Phase 24b. |

New sources (ChEMBL, ORD, ChEBI) just subclass `DataSource` and are registered in
`gui/panels/search_panel.py`.

### `render/` — stateless rendering helpers
| File | Key symbols |
|------|-------------|
| `draw2d.py` | `render_svg(mol, ..., show_stereo_labels=False)`, `render_png_bytes(mol, ...)`. With `show_stereo_labels=True` draws wedge/dash bonds + CIP R/S + E/Z annotations via RDKit's `addStereoAnnotation` option. |
| `draw3d.py` | `build_3dmol_html([molblocks], style, ...)`, `build_from_molecule(m, style)`, `local_3dmol_available`, `local_3dmol_path`. Interactive WebGL path. Phase 20a: inlines a local `orgchem/gui/assets/3Dmol-min.js` when present (fetch with `scripts/fetch_3dmol_js.py`) so the HTML works offline; falls back to the CDN URL otherwise. |
| `draw3d_mpl.py` | `render_png(mol, path, style, ...)` — matplotlib 3D. Works in any Qt mode; the *only* 3D path that works headlessly. Styles: ball-and-stick / sphere (both use real shaded `plot_surface` spheres) + stick / line. CPK-coloured. |
| `draw_reaction.py` | `render_svg(smiles)`, `render_png_bytes(smiles)`, `export_reaction(smiles, path)` — uses `MolDraw2DSVG.DrawReaction` for top-quality schemes. |
| `draw_mechanism.py` | `render_step_svg(step)` — RDKit `MolDraw2DSVG` + `GetDrawCoords` to overlay curved bezier arrows (curly + fishhook) between atoms or at **bond midpoints** (via `Arrow.from_bond` / `to_bond`), plus **lone-pair dot pairs** (from `MechanismStep.lone_pairs`) placed opposite the mean neighbour direction so dots land in empty space. Returns composable SVG. (Phase 13c) |
| `draw_mechanism_composite.py` | `export_composite(mechanism, path)` — Phase 13c "full-kinetics" layout: stacks every mechanism step into one numbered SVG (Schmidt-style). PNG/SVG by extension. |
| `draw_energy_profile.py` | `export_profile(profile, path)` + `render_figure(profile)` — matplotlib reaction-coordinate diagrams with Bezier-smoothed curves through stationary points, TS‡ peaks, auto-annotated Ea and ΔH arrows (Phase 13). |
| `draw_mo.py` | `export_mo_diagram(HuckelResult, path)` — matplotlib MO level diagram: horizontal bars per MO, occupied electrons as arrows, HOMO/LUMO highlighted, degenerate levels side-by-side, α reference (Phase 14a). |
| `draw_ir.py` | `export_ir_spectrum(smiles, path)` — schematic IR sketch (transmittance dips + labels) from the Phase 4 band predictor. PNG/SVG. |
| `draw_tlc.py` | `export_tlc_plate(tlc_result, path)` + `render_figure(tlc_result)` — schematic TLC-plate figure from `core/chromatography.simulate_tlc` output: silica panel, baseline, solvent front, one coloured spot per compound at its predicted Rf, and a legend mapping lane number to SMILES + logP. PNG/SVG. Wired into *Tools → Lab techniques → TLC / Rf tab → Save plate…* and agent action `export_tlc_plate`. (Phase 15b follow-up, round 53) |
| `draw_nmr.py` | `export_nmr_spectrum(smiles, path, nucleus)` — stick NMR spectrum (peaks at predicted ppm with environment labels). PNG/SVG. |
| `draw_ms.py` | `export_ms_spectrum(smiles, path)` — molecular-ion-region stick MS spectrum with M / M+1 / M+2 labels. PNG/SVG. |
| `draw_interaction_map.py` | `export_interaction_map(ContactReport, path)` — PoseView-style 2D ligand-centred radial diagram with colour-coded dashed lines per interaction type (H-bond / salt-bridge / π-stacking / hydrophobic). PNG/SVG. Phase 24c. |
| `draw_protein_3d.py` | `build_protein_html(pdb_text, protein_style, ligand_style, highlight_residues, show_waters, show_ligand_surface, colour_mode, enable_picking, spin, spin_axis, spin_speed)` + file / export helpers — self-contained 3Dmol.js HTML viewer for a PDB. Cartoon / trace / surface protein styles, ball-and-stick / stick / sphere ligand styles, optional residue highlight (adds a yellow-carbon stick overlay + `addResLabels`), optional ligand surface for pocket-view, **`colour_mode="plddt"`** which emits a JS `colorfunc` that maps B-factor to the AlphaFold DB gradient (dark blue ≥ 90, cyan ≥ 70, yellow ≥ 50, orange < 50), **`enable_picking=True`** (round 30) which attaches a 3Dmol click handler, shows the picked `chain:resn+resi` in an in-page overlay label, and forwards the same info to a Qt host via `qtBridge.onAtomPicked` (QWebChannel), and **`spin=True`** (round 31) which auto-rotates via `v.spin(axis, speed)` (axis sanitised to {x, y, z}). Inlines the offline bundle when present. Phase 24l + follow-ups. |
| `draw_sar.py` | `export_sar_matrix(series, path)` — colour-coded descriptor + activity heat-map matrix for a SAR series. Phase 19a. |
| `draw_reaction_3d.py` | `render_png(mapped_smarts, path)` — **static 3D side-by-side** (Phase 2c.1). Embeds reactant & product, renders them with `draw3d_mpl` in one figure with a forward arrow between; atoms coloured by atom-map number so identity persists across the arrow; bonds that break/form highlighted in red/green (includes bond-order change detection). Plus `build_trajectory_html(xyz)` — **animation player** (Phase 2c.2): wraps a multi-frame XYZ in a self-contained 3Dmol.js page with play/pause/reset/speed controls. |
| `draw_pathway.py` | `build_svg(pathway)` and `export_pathway(pathway, path)` — **synthesis pathway renderer** (Phase 8). Vertical stack of step schemes: each step has a number label, reagents above the arrow, the reaction scheme (RDKit MolDraw2DSVG body extracted), conditions / yield / notes below, separator line between steps. |
| `export.py` | `export_molecule_2d(mol, path, ...)` — chooses PNG/SVG/JPG by file extension. |
| `screenshot.py` | `grab_widget(widget, path, size=None)` — any `QWidget` → PNG file. |

### `messaging/` — cross-cutting concerns
| File | Key symbols |
|------|-------------|
| `bus.py` | Singleton `AppBus(QObject)`; signals: `molecule_selected`, `database_changed`, `message_posted`, `download_*`, … Access via `bus()`. |
| `errors.py` | Exception hierarchy: `OrgChemError` → `ChemistryError`/`InvalidSMILESError`/`ConformerGenerationError`/`DatabaseError`/`NetworkError`/`RenderError`. |
| `logger.py` | `BusHandler` — logging records become `message_posted` signals. |

### `utils/`
| File | Key symbols |
|------|-------------|
| `paths.py` | `data_dir()`, `config_path()`, `log_dir()`, `cache_dir()`, `sessions_dir()` (Phase 20d saved sessions) — platformdirs-backed. |
| `threading.py` | `Worker(QRunnable)`, `submit(fn, *args, **kwargs)` — background workers with signals. |

### `gui/` — PySide6 UI

- `main_window.py` — `MainWindow`: menus, tabs, docks, bus hookup.
- `panels/`
  - `molecule_browser.py` — left dock: filterable list of DB molecules.
  - `viewer_2d.py` — RDKit SVG 2D viewer with style selector.
  - `viewer_3d.py` — 3D viewer with two backends swapped in a `QStackedWidget`:
    **3Dmol** (interactive WebGL, default) and **matplotlib** (static PNG,
    works headlessly). Backend chosen in `Tools → Preferences…`. Style
    selector stays per-panel. *Save PNG…* button exports via matplotlib.
  - `properties.py` — right dock: descriptor table.
  - `session_log.py` — bottom dock: bus-driven log with level filter.
  - `search_panel.py` — online search / download panel.
  - `tutorial_panel.py` — curriculum tree + markdown browser.
  - `tutor_panel.py` — **chat console dock**, tears off into a floating window;
    pluggable backend (Anthropic / OpenAI / Ollama) with full tool-use access
    to every action in the agent registry.
  - `reaction_workspace.py` — Reactions tab: filterable list + rendered
    scheme (RDKit `MolDraw2DSVG.DrawReaction`) + description + export.
  - `compare_panel.py` — Compare tab: 2×2 grid of molecule slots (2D +
    mini descriptor table each); per-slot SMILES entry or
    `compare_molecules([ids])` agent action.
  - `synthesis_workspace.py` — Synthesis tab: filterable pathway list +
    scrollable scheme viewer + export button. Renders vertical
    step-by-step synthesis schemes for seeded classical routes (Aspirin,
    Paracetamol, BHC Ibuprofen, Wöhler, etc.).
  - `drawing_panel.py` — **Phase 36b / 36c / 36d / 36e / 36f.2** molecular-drawing
    canvas.  `QGraphicsScene`-based widget with a toolbar (select /
    atom-C/N/O/P/S/F/Cl/Br/I/H / bond / wedge / dash / erase /
    Undo / Redo / Clear) + SMILES round-trip ribbon + live
    `DrawingPanel.structure_changed(smiles)` Qt signal.  Backed by
    the Phase-36a `Structure` core — every atom-placement / bond-draw
    / element-change / erase action keeps a mirrored `Structure` in
    sync so `current_smiles()` is a single-call round-trip.  Repeat
    bond clicks cycle single → double → triple → single; bond-tool
    clicks on empty canvas auto-place a carbon at each end (ChemDraw
    convention).  **Phase 36c (round 129)** adds a second toolbar
    row with the 20-template ring + FG palette from
    `core/drawing_templates.py`: tool key `"template-<name>"` routes
    canvas clicks through `_apply_template_at` which delegates the
    geometric merge to the headless `apply_template` function then
    renders only the newly appended scene items.  Ring templates
    fuse the anchor with the clicked atom; FG templates auto-place
    a carbon host on empty canvas.  **Phase 36d (round 128)** adds
    snapshot-based undo/redo: `_push_undo` captures a `(Structure,
    positions)` deep copy before each logical mutation (atom place,
    element swap, bond draw, bond order cycle, erase atom/bond,
    drag-move, clear, SMILES rebuild, template placement); `undo()`
    / `redo()` pop the most recent snapshot onto the opposite stack
    and rebuild the scene via `_restore_snapshot`.  Stack depth
    capped at `_UNDO_STACK_MAX = 100`.  Toolbar buttons
    enable/disable off `can_undo` / `can_redo`; Ctrl+Z /
    Ctrl+Shift+Z `QShortcut`s scoped to the widget.  No-op guards:
    re-clicking the same atom with the same element, cancelling
    the bond tool by clicking the same atom twice, clearing an
    already-empty canvas, and template placements that don't
    actually mutate the structure all skip the snapshot so the
    undo history stays clean.  **Phase 36e (round 130)** adds
    wedge / dash bond tools (`bond-wedge` / `bond-dash` tool
    keys) wired through `_handle_stereo_bond_click` — same
    flow as the plain bond tool but new bonds get `order=1` +
    the requested `stereo`, and clicking an existing bond
    TOGGLES the stereo (same stereo → none; otherwise switch).
    Wedges render as a tapered-triangle `QGraphicsPolygonItem`
    (apex at the begin atom, ChemDraw-style; round-135 polish),
    dashes as a `QGraphicsItemGroup` of perpendicular hashes
    that widen toward the end atom (also round 135), "either"
    as grey dotted line.  `_build_bond_visual(idx)` factory
    decides the visual type per bond; `_refresh_bond` drops the
    old item from the scene and rebuilds (cheap on
    teaching-scale molecules and avoids dual update paths
    across visual types).  Right-click on
    any atom opens a context menu (`handle_canvas_right_click`
    + `_DrawingView.mousePressEvent` button-button check) with
    Formal-charge (-2/-1/0/+1/+2), Radical electrons (0/1/2),
    Isotope label (QInputDialog), and Explicit H count
    (-1=auto/0/1/2/3/4) submenus — each entry pushes one undo
    snapshot via `_set_atom_charge` / `_set_atom_radical` /
    `_set_atom_isotope` / `_set_atom_h_count`; same-value
    selections are no-ops that don't pollute undo history.
    Atom glyph rendering now decorates non-default atoms:
    charge as a superscript ("+", "−", "2+", "2−") in red,
    isotope mass number as a left superscript, radical
    electrons as 1-2 bullet dots above the symbol; pure-C
    atoms with charge / isotope / radical promote from a dot
    to a labelled glyph so decorations have somewhere to
    anchor.  **Phase 36f.2 (round 132)** adds reaction-arrow
    tools: `arrow-forward` (→) and `arrow-reversible` (⇌)
    tool keys.  Single-arrow-per-canvas constraint — second
    placement replaces the first; same-position no-op skipped
    from undo.  Arrow rendered as a `QGraphicsLineItem` shaft
    + `QGraphicsPolygonItem` arrowhead (stacked half-arrows
    for the reversible kind).  `current_scheme()` partitions
    atoms by x vs the arrow's x-coord and returns a
    `core.drawing_scheme.Scheme` with a fresh `Structure` per
    side (built by `_slice_structure`; bonds straddling the
    arrow are dropped).  Snapshot tuple grew to a 3-tuple
    `(Structure, positions, arrow)` so undo / redo round-trip
    arrow placement; `_restore_snapshot` accepts legacy
    2-tuples defensively.  `clear()` + `remove_arrow()` drop
    the arrow.  All Phase 36 sub-phases now complete.
  - `glossary_panel.py` — Glossary tab (Phase 11b): filterable term
    list + category combo + markdown definition pane + clickable
    "See also" cross-references. Feeds off the `GlossaryTerm` table.
  - `carbohydrates_panel.py` — **Carbohydrates tab** (Phase 29b).
    Sibling of the Proteins tab. Family combo (monosaccharide /
    disaccharide / polysaccharide) + free-text filter + entry
    list on the left. Details pane on the right shows a rendered
    2D structure (QSvgWidget fed by `draw2d.render_svg`), HTML
    meta block (family / form / carbonyl type / anomer / glycosidic
    bond / notes), *Copy SMILES* and *Show in Molecule Workspace*
    buttons. Wires `list_carbohydrates`, `get_carbohydrate`, and
    `carbohydrate_families` to a user-facing surface.
  - `lipids_panel.py` — **Lipids tab** (Phase 29b). Family combo
    (fatty-acid / triglyceride / phospholipid / sphingolipid /
    sterol / vitamin) + free-text filter + entry list on the left.
    Details pane shows the 2D structure + HTML meta block (family
    / chain-length / unsaturation / ω-designation / melting point
    / notes) + *Copy SMILES* and *Show in Molecule Workspace*
    buttons. Wires `list_lipids`, `get_lipid`, `lipid_families`.
  - `nucleic_acids_panel.py` — **Nucleic acids tab** (Phase 29c).
    Family combo (nucleobase / nucleoside / nucleotide /
    oligonucleotide / pdb-motif) + free-text filter + entry list.
    Details pane shows the 2D structure when a SMILES is defined;
    for PDB-motif entries (1BNA B-DNA, 1EHZ tRNA, 143D G-quadruplex,
    1HMH hammerhead) it exposes a *Fetch PDB in Proteins tab*
    button that switches the main-window tab and triggers the
    proteins panel's fetch slot. Wires `list_nucleic_acids`,
    `get_nucleic_acid`, `nucleic_acid_families`.
  - `protein_panel.py` — **Proteins tab** (Phase 24 GUI): PDB /
    AlphaFold ID input, seeded-target drop-down, structure summary,
    plus sub-tabs: **3D structure (24l)** (interactive 3Dmol.js
    view — cartoon / trace / surface + ligand styles + water toggle
    + ligand-surface toggle + "Save HTML…" export; highlights
    residues from the most-recent Contacts analysis automatically),
    Pockets (24d), Contacts (24e + 24i PLIP-aware button), PPI
    (24j), NA-ligand (24k). Includes an "Export interaction map"
    button (24c) and a badge showing whether PLIP is installed.
    All analyses run in-process on the current cached PDB. The 3D
    sub-tab has a *"Colour by pLDDT (AlphaFold)"* checkbox that swaps
    the protein colouring to the AlphaFold DB gradient; it's auto-
    enabled whenever a structure is fetched via *Fetch AlphaFold*.
    Click-to-inspect (round 30): protein atoms are made clickable
    and picks bounce through a QWebChannel-registered `_PickBridge`
    QObject (`picked(chain, resn, resi)` signal) so a *"Picked:
    A:HIS57"*-style label updates beneath the viewer; the same event
    also posts to the session-log bus.
- `audit.py` — **GUI wiring audit** (Phase 25a). Hand-maintained
  `GUI_ENTRY_POINTS` dict (action name → user-facing path) + the
  `audit()` / `audit_summary()` helpers. Companion CLI at
  `scripts/audit_gui_wiring.py` prints coverage %. Paired regression
  test in tests/test\_gui\_audit.py keeps coverage ≥ 60 % and
  grows the baseline as gaps get filled.
- `windows/macromolecules_window.py` — **Macromolecules window**
  (Phase 30). Top-level `QMainWindow` opened from *Window →
  Macromolecules…* (Ctrl+Shift+M) and hosting Proteins /
  Carbohydrates / Lipids / Nucleic-acids as inner tabs. Single
  persistent instance, lazily constructed on first call to
  `MainWindow.open_macromolecules_window(tab_label=None)`. Geometry
  + last-active tab persist via `QSettings["window/macromolecules"]`.
  `switch_to(label)` helper lets cross-panel code (e.g. the NA
  panel's *Fetch PDB in Proteins tab* button) focus a specific
  inner tab. Agent action `open_macromolecules_window(tab)` in
  `agent/actions_windows.py` exposes the same behaviour to the
  tutor panel and stdio bridge.
- `windows/biochemistry_by_kingdom_window.py` — **Biochemistry-
  by-Kingdom window** (Phase 47b, round 167).  Top-level
  `QMainWindow` opened from *Window → Biochemistry by
  Kingdom…* (Ctrl+Shift+K).  Companion to the Macromolecules
  window — same content but organised by **kingdom of life**
  (Eukarya / Bacteria / Archaea / Viruses) rather than
  molecular class.  Single persistent instance, lazily
  constructed on first call to
  `MainWindow.open_biochemistry_by_kingdom_window(kingdom=None,
  subtab=None, topic_id=None)`.  Geometry + last-active outer
  tab persist via `QSettings["window/biochemistry_by_kingdom"]`.
  Each outer tab hosts a `KingdomSubtabPanel` widget with the
  three sub-tabs.  Programmatic API: `switch_to_kingdom(id)`,
  `select_topic(kingdom, subtab, topic_id)`, `kingdom_panel(id)`,
  `kingdom_labels()`.
- `panels/kingdom_subtab_panel.py` — **Per-kingdom subtab
  widget** (Phase 47b, round 167).  Reusable
  `KingdomSubtabPanel` widget — one instance per kingdom,
  hosting a `QTabWidget` with the three sub-tabs (Structure
  / Physiology+Development / Genetics+Evolution).  Each
  sub-tab is an internal `_SubtabPane` with the canonical
  filterable-list-on-the-left + HTML-detail-card-on-the-right
  layout.  Detail card shows the topic body markdown plus
  cross-reference sections for **Phase-43 cell components**,
  **Phase-42 metabolic pathways**, and **molecule-database
  names** — only rendered when the topic carries cross-
  references for that category.  `switch_to_subtab(subtab)`
  + `select_topic(subtab, topic_id)` + `subtab_labels()`
  programmatic API.
- `windows/workbench_window.py` — **Phase 32b** detached Workbench
  host. `WorkbenchWindow` is a `QMainWindow` that centres a
  `WorkbenchWidget` when the user clicks *Detach as window* on
  the Workbench toolbar. Emits `reattach_requested` / `closed_by_user`
  signals that `MainWindow._reattach_workbench` catches to pull
  the widget back into the tabbar. Geometry persists via
  `QSettings["window/workbench/geometry"]`. Calls `takeCentralWidget()`
  on close so Qt doesn't delete the widget Mother Hen still owns.
- `panels/workbench_track_row.py` — **Phase 32c** per-track row
  widget for the Workbench's right-side tracks list. `TrackRow`
  carries a visibility checkbox, a bold name label (auto-adds
  SMILES / PDB-ID subtitle from `Track.meta`), a kind-specific
  style `QComboBox` (small-molecule vs protein choices), and a
  ✕ remove button. Emits `visibility_toggled(name, bool)` /
  `style_changed(name, style)` / `remove_clicked(name)` signals
  the Workbench forwards to the Scene. `reflect(track)` re-syncs
  controls after external scene mutations. Kept separate so
  `workbench.py` stays under the 500-line cap and the row widget
  can be reused by other Scene-aware panels.
- `panels/workbench.py` — **Phase 32b / 32c** `WorkbenchWidget`.
  Toolbar (Detach/Reattach/Fit-to-view/Toggle-bg/Clear/Snapshot-PNG
  /Export-HTML) + `QWebEngineView` (3Dmol.js) + right-side tracks
  list using `TrackRow` per row for inline visibility ☑︎ + style
  combo + ✕ remove. Subscribes to `orgchem.scene.current_scene()`
  via a thread-safe `Signal + Qt.QueuedConnection` bridge so
  scene mutations from a script-worker QThread marshal onto the
  main thread — **fix for round-67 SIGTRAP** reported when demo 02
  mutated the scene off-main-thread.  `_schedule_rebuild` +
  `_REBUILD_DEBOUNCE_MS = 50` coalesces a burst of scene events
  into one HTML reload to stop the macOS Metal compositor from
  thrashing WebGL. `grab_png(path)` uses `QWidget.grab()` so
  snapshots work under offscreen Qt without requiring the widget
  to be visible. Reparents cleanly between the main tabbar and
  `WorkbenchWindow` — the Scene instance is persistent across
  reparenting, so the Script Editor keeps driving the same view.
  `_on_toggle_background` flips scene background dark ↔ light;
  `_on_export_html_clicked` writes a standalone .html of the
  current scene via a file dialog. `rebuild_count` class attr is
  exposed for regression tests.
- `widgets/sequence_bar.py` — **Phase 34b (round 116)** `SequenceBar` + `SequenceBarPanel` widgets. Reads the JSON-serialisable `SequenceView.to_dict()` shape (from `core/sequence_view.py`) and renders one monospace row per chain (DNA/RNA stacked above proteins), residue-number tick marks every 10, per-chain `HighlightSpan` underlay colour bands, and click / click-drag selection with a `selection_changed(chain_id, start, end)` Qt signal. `SequenceBarPanel` wraps the bar in a `QScrollArea` + status-line label. Drop-in for the Proteins 3D sub-tab — Phase 34c round-trip: 3D pick → sequence caret move via `_on_atom_picked` → `sequence_panel.set_selection`; sequence drag → `_on_sequence_selection` handler in `protein_panel.py` (3D highlight re-render on selection is a later 34c follow-up).
- `widgets/smiles_input.py` — validated SMILES `QLineEdit` that emits canonical form.
- `widgets/glossary_linker.py` — **Phase 11c** autolink helper:
  `autolink(text)` returns HTML where every recognised glossary
  term (pulled from `seed_glossary._GLOSSARY`) is wrapped in an
  `orgchem-glossary://{term}` anchor. Used by the Reaction
  workspace description pane (`reaction_workspace.py`) and safe
  to reuse for any free-text pane that wants clickable glossary
  cross-refs. Longest-first ordering prevents sub-term shadowing.
- `dialogs/`
  - `import_smiles.py` — add a molecule by SMILES.
  - `formula_calculator.py` — GUI wrapper for `core/formula.py` (Verma Section A).
  - `hrms_guesser.py` — GUI wrapper for `core/hrms.py` (Phase 4
    follow-up): enter measured monoisotopic mass + ppm tolerance +
    elemental bounds, get a ranked candidate-formula table with DBE
    and ppm error.
  - `ms_fragments.py` — GUI wrapper for `core/ms_fragments.py`: paste
    a SMILES → ranked table of fragment m/z + Δ + label + mechanism.
    Tools menu entry *EI-MS fragmentation sketch…*.
  - `medchem.py` — Tools → *Medicinal chemistry…*. Two-tab:
    **SAR series** (seeded-series picker + descriptor + activity
    table + *Export SAR matrix…*), **Bioisosteres** (SMILES →
    ranked catalogue suggestions). Closes `list_sar_series`,
    `get_sar_series`, `export_sar_matrix`, `list_bioisosteres`,
    `suggest_bioisosteres` audit gaps. (round 36)
  - `spectroscopy.py` — Tools → *Spectroscopy (IR / NMR / MS)…*.
    Three tabs: IR band prediction + save schematic spectrum, NMR
    ¹H / ¹³C shift prediction + save stick spectrum, MS isotope
    pattern + save stick spectrum. Closes `predict_ir_bands`,
    `export_ir_spectrum`, `predict_nmr_shifts`,
    `export_nmr_spectrum`, `predict_ms`, `export_ms_spectrum`
    audit gaps. (round 37)
  - `green_metrics.py` — Tools → *Green metrics (atom economy)…*.
    Two tabs: Reaction AE (DB-reaction picker) and Pathway AE
    (pathway picker → per-step + overall AE table). Closes
    `reaction_atom_economy` + `pathway_green_metrics` audit gaps.
    (round 38)
  - `stereo.py` — Tools → *Stereochemistry…*. SMILES → R/S + E/Z
    descriptor table with per-row *Flip* buttons + global
    *Mirror (enantiomer)* button. Closes `flip_stereocentre` and
    `enantiomer_of` audit gaps. (round 37)
  - `naming_rules.py` — Tools → *IUPAC naming rules…*. Category
    combo + rule list + rich-text body (title / description /
    example SMILES + IUPAC + common name / pitfalls). Closes
    `list_naming_rules`, `get_naming_rule`,
    `naming_rule_categories`. (round 36)
  - `periodic_table.py` — Tools → *Periodic table…* (Ctrl+Shift+T).
    Classic 18-column clickable grid from `orgchem/core/periodic_table.py`
    cells coloured by category, lanthanide/actinide rows at the
    bottom, side-pane shows Z / mass / χ / oxidation states /
    electron config for the clicked element; legend strip lists
    every category palette. Closes `list_elements`, `get_element`,
    `elements_by_category`. (Phase 27c, round 36)
  - `lab_techniques.py` — Tools → *Lab techniques…*. Four-tab:
    TLC / Rf simulator (paste SMILES + solvent → Rf table),
    Recrystallisation (hot/cold solubility + crude mass → yield),
    Distillation (two components → simple/fractional/azeotrope plan),
    Acid-base extraction (pKa + pH + logP → layer prediction).
    Closes five Phase 25b audit gaps:
    `predict_tlc`, `predict_rf`, `recrystallisation_yield`,
    `distillation_plan`, `extraction_plan`.
  - `orbitals.py` — Tools → *Orbitals (Hückel / W-H)…*. Three-tab
    dialog: **Hückel MOs** (SMILES input → MO energies table +
    *Save MO diagram…*), **Woodward-Hoffmann** rule browser (family
    combo → rule list → full HTML description), **Is it allowed?**
    quick-check for pericyclic steps. Closes five Phase 25b audit
    gaps: `huckel_mos`, `export_mo_diagram`, `list_wh_rules`,
    `get_wh_rule`, `check_wh_allowed`.
  - `retrosynthesis.py` — GUI wrapper for `core/retrosynthesis.py`
    (Phase 25b gap-close). Target-SMILES input, depth / branches /
    top-K spinners, two result tabs: *Single-step* (flat
    disconnection table) and *Multi-step* (tree view of the
    recursive precursor search). Tools menu entry *Retrosynthesis…*.
  - `fulltext_search.py` — **Phase 33b** Ctrl+F find dialog.
    Singleton per app instance.  `QLineEdit` live-updating query
    box (debounced 100 ms via `QTimer`), 5-checkbox kind-filter
    row, results list with kind-badge + bold title + snippet
    preview rendered as HTML via `QLabel` per row.  Double-click
    / return-key activation routes through module-level
    `dispatch_search_result(result, main_win)` — handles all 5
    kinds (molecule via bus.molecule_selected, reaction via
    `reactions._display`, mechanism-step via the `open_mechanism`
    agent action, pathway via `synthesis._display`, glossary via
    `glossary.focus_term`).  Wired into *View → Find… (Ctrl+F)*.
  - `cell_components.py` — **Phase 43 (round 151)**
    *Tools → Cell components…* (Ctrl+Shift+J).
    Singleton modeless dialog backed by
    `core/cell_components.py`.  Layout: domain combo
    (eukarya / bacteria / archaea) + sub-domain combo
    (animal / plant / fungus / protist / gram-positive
    / gram-negative) + category combo (membrane /
    organelle / nuclear / cytoskeleton / envelope /
    appendage / extracellular / ribosome / genome) +
    free-text filter + list of components on the left;
    right pane = title + meta line (domain + sub-
    domains + category) + HTML detail card with sections
    **Location** / **Function** / **Molecular constituents**
    (rendered as a 2-column table — name + role, with
    the name italicised + tagged "→ Molecule DB:" when
    the constituent has a cross-reference to a
    Phase-6 molecule row) / **Notable diseases** (only
    when set) / **Notes** (only when set).
    `select_component(id)` programmatic API for the agent
    open path.
  - `microscopy.py` — **Phase 44 (round 150)**
    *Tools → Microscopy techniques…* (Ctrl+Alt+M).
    Singleton modeless dialog backed by
    `core/microscopy.py`.  Layout: resolution-scale combo
    + sample-type combo + free-text filter on the left,
    list of `abbreviation — name` rows; right pane = title
    + meta line (abbreviation + resolution scale) + HTML
    detail card with sections **Typical resolution** /
    **Light source** / **Contrast mechanism** / **Sample
    types** / **Typical uses** / **Strengths** /
    **Limitations** / **Representative instruments** /
    **Cross-reference (Phase 40a Lab analysers)** (only
    when a method has cross-references).  `select_method(id)`
    programmatic API for the agent open path.
  - `isomer_explorer.py` — **Phase 48b (round 171)**
    *Tools → Isomer relationships…* (Ctrl+Shift+B).
    Singleton modeless dialog backed by `core/isomers.py`.
    Three tabs: **Stereoisomers** (SMILES + max-results
    spin → list of canonical SMILES via
    `enumerate_stereoisomers`), **Tautomers** (SMILES +
    max-results spin → list via `enumerate_tautomers`),
    **Classify pair** (two SMILES inputs → HTML result
    showing the colour-coded relationship label + the
    canonical RELATIONSHIPS string + a 2-row comparison
    table + a brief per-relationship explainer paragraph).
    Each enumeration tab shows a meta line with the input
    SMILES + molecular formula + the count of results +
    a red 'truncated at max=N' notice when the cap was
    hit.  `select_tab(label)` + `tab_labels()` programmatic
    API for the agent open path.
  - `lab_reagents.py` — **Phase 45 (round 149)**
    *Tools → Lab reagents…* (Ctrl+Shift+R).  Singleton
    modeless dialog backed by `core/lab_reagents.py`.
    Same shape as the Phase-40a *Lab analysers* dialog
    (category combo + free-text filter + list +
    HTML detail card with sections Typical
    concentration / Storage / Hazards / Preparation /
    Typical usage / Notes; CAS shown in the
    sub-title meta line).  `select_reagent(id)`
    programmatic API for the agent open path.
  - `ph_explorer.py` — **Phase 46 (round 148)**
    *Tools → pH explorer…* (Ctrl+Alt+H).  Singleton
    modeless dialog with 4 tabs: **Reference** (6
    teaching cards rendered as HTML), **Buffer
    designer** (pKa-acid combo auto-fills the pKa
    spinbox; target pH / total concentration / volume
    spinboxes drive `core.ph_explorer.design_buffer`;
    result pane shows ratio + [HA] / [A⁻] split + moles +
    colour-coded capacity verdict — red `Capacity
    warning:` when ΔpH > 1, green `OK:` otherwise),
    **Titration curve** (weak-acid pKa + initial M +
    volume mL + base M spinboxes drive
    `titration_curve`; result pane renders the
    (vol_mL, pH) points as an HTML table with the
    equivalence-point row highlighted), **pKa lookup**
    (category combo + free-text filter +
    `QTableWidget` of name / formula / category /
    pKa values).  `select_tab(label)` + `tab_labels()`
    programmatic API for the agent open path.
  - `metabolic_pathways.py` — **Phase 42a (round 147)**
    *Tools → Metabolic pathways…* (Ctrl+Alt+P).
    Singleton modeless dialog backed by
    `core/metabolic_pathways.py`.  Three-pane horizontal
    splitter: left = category combo + filter + pathway
    list, middle = pathway meta block + per-step
    `QTableWidget` (#, Enzyme, EC, Rev?, ΔG kJ/mol),
    right = step detail pane showing substrates /
    products / regulatory effectors / notes for the
    currently-selected step.  Reversibility column uses
    ↔ for reversible / → for irreversible glyphs.
    `select_pathway(id)` + `select_step(step_number)`
    programmatic API for the agent open path.
  - `lab_analysers.py` — **Phase 40a (round 146)**
    *Tools → Lab analysers…* (Ctrl+Shift+A).  Singleton
    modeless dialog backed by `core/lab_analysers.py`.
    Same shape as the Phase-37c chromatography dialog
    (category combo + free-text filter + list +
    HTML detail card with Function / Throughput / Sample
    / Detection / Assays / Strengths / Limitations /
    Notes sections).  `select_analyser(id)` programmatic
    API for the agent open path.
  - `centrifugation.py` — **Phase 41 (round 144)**
    *Tools → Centrifugation…* (Ctrl+Shift+F).  Singleton
    modeless dialog with 4 tabs: 3 catalogue tabs
    (Centrifuges / Rotors / Applications) using a reusable
    `_CatalogueTab` helper class, and a g↔RPM `_CalculatorTab`
    that's the headline feature.  Catalogue tabs have
    category combo + filter + list + HTML detail card;
    `_CatalogueTab` constructor takes the enumeration +
    detail-renderer + row-label callables, so all 3
    catalogue tabs share one implementation.  Calculator
    tab has a rotor `QComboBox` that auto-fills the radius
    spin from the selected rotor's `max_radius_cm` AND
    surfaces a `Max RPM for this rotor: <N>` label so
    overspeed is visible up front; entering a speed above
    that limit appends an OVERSPEED warning to the status
    line in red.  RPM↔×g and ×g↔RPM dedicated direction
    buttons + Clear.  Programmatic API:
    `select_tab(label)` / `select_centrifuge(id)` /
    `select_rotor(id)` / `select_application(id)` for the
    `open_centrifugation` agent action.
  - `lab_calculator.py` — **Phase 39b (round 143)**
    *Tools → Lab calculator…* (Ctrl+Shift+C).  Tabbed
    `QDialog` with 7 tabs (Solution / Stoichiometry /
    Acid-base / Gas law / Colligative / Thermo + kinetics
    / Equilibrium) backed by the Phase-39a solver
    modules.  Reusable `_SolverPanel` helper class — a
    titled `QGroupBox` with N labelled `QDoubleSpinBox`
    fields + Solve + Clear buttons + a status line that
    shows the rearranged equation in human form.  Spin
    value 0 = "unknown" (passed as `None` to the
    solver); the solver fills it in.  Custom panels
    where the symmetric-solve pattern doesn't fit
    cleanly: pH ↔ [H⁺] uses two dedicated buttons (one
    per direction), pKa ↔ Ka same, K_sp ↔ molar
    solubility uses 4 spins (s, K_sp, n, m) + two
    direction buttons, ICE solver has 5 inputs + 5
    output displays.  Colligative tab's BP elevation +
    FP depression panels include a `solvent` `QComboBox`
    that auto-fills K_b / K_f from
    `core/calc_colligative.SOLVENT_CONSTANTS` — the
    `_SolverPanel.add_widget` helper handles the
    extra-widget plumbing.  `select_tab(label)` +
    `tab_labels()` programmatic API for the agent-action
    open path.  Singleton modeless dialog. |
  - `lab_setups.py` — **Phase 38b (round 141)**
    *Tools → Lab setups…* (Ctrl+Shift+U).  Modeless
    singleton dialog backed by `core/lab_setups.py`.
    Layout: filter + setup list on the left, detail
    card on the right with Purpose / Equipment (resolved
    to full Phase-38a names) / Connections (port-to-port
    table with notes) / Procedure / Safety / Pedagogical
    / Typical-reactions sections.  When a setup fails
    validation against the Phase-38a equipment / port
    catalogue (e.g. after a port rename), the validation
    errors render at the bottom of the detail card in
    red — surfaces stale data without needing to re-run
    tests.  `select_setup(id)` programmatic API for the
    `open_lab_setups` agent action.  Future Phase-38c
    addition: a *Build on canvas* button that
    pre-populates a `QGraphicsScene` from the seeded
    setup's equipment + connections.
  - `lab_equipment.py` — **Phase 38a (round 140)**
    *Tools → Lab equipment…* (Ctrl+Shift+I).  Modeless
    singleton dialog backed by `core/lab_equipment.py`.
    Same shape as the Phase-37c/d catalogue dialogs (category
    combo + free-text filter + list + HTML detail card)
    plus a *Connection ports* section in the detail body
    that lists every named joint / hose / socket on the
    selected item — the data the future Phase-38c canvas
    will use to snap items together.  `select_equipment(id)`
    programmatic API for the agent-action open path.
  - `spectrophotometry_methods.py` — **Phase 37d (round 139)**
    *Tools → Spectrophotometry techniques…* (Ctrl+Shift+W).
    Modeless singleton dialog backed by
    `core/spectrophotometry_methods.py`.  Layout mirrors
    the chromatography dialog (category combo + filter +
    list + HTML detail card with 9 sections — Principle /
    Light source / Sample handling / Detector / Typical
    analytes / Strengths / Limitations / Procedure /
    Notes), PLUS a collapsible Beer-Lambert calculator
    panel at the bottom of the right pane: four
    `QDoubleSpinBox` fields (A / ε / l / c) + *Solve* +
    *Clear* buttons + a status line that shows the
    rearranged equation in human form.  Solver delegates
    to `beer_lambert_solve` and surfaces validation
    errors inline.  `select_method(method_id)`
    programmatic API for the agent-action open path.
  - `chromatography_methods.py` — **Phase 37c (round 138)**
    *Tools → Chromatography techniques…* (Ctrl+Shift+G).
    Modeless singleton dialog backed by
    `core/chromatography_methods.py`.  Layout mirrors the
    Phase-37a qualitative-tests dialog: left = category combo
    + free-text filter + `QListWidget` of `abbreviation —
    name` rows; right = title + meta line + `QTextBrowser`
    detail card with seven HTML sections (Principle,
    Stationary phase, Mobile phase, Detector(s), Typical
    analytes, Strengths, Limitations, Procedure, Notes).
    `select_method(method_id)` programmatic API for the
    `open_chromatography_methods` agent action.
  - `clinical_panels.py` — **Phase 37b (round 137)**
    *Tools → Clinical lab panels…* (Ctrl+Shift+L).  Modeless
    singleton dialog backed by `core/clinical_panels.py`.
    Layout: top row = panel-picker `QComboBox`
    (BMP / CMP / Lipid / DM follow-up / Thyroid /
    Vitamin D); horizontal `QSplitter` below with left =
    panel meta block (purpose / sample / fasting / procedure
    / notes) + per-analyte `QTableWidget` (4 columns: name,
    abbreviation, units, normal range), right = analyte
    detail pane (title + meta line + clinical-significance
    + interpretation notes).  Auto-selects first panel +
    first analyte on construction.  `select_panel(panel_id)`
    + `select_analyte(analyte_id)` programmatic API for the
    `open_clinical_panels` agent action.  Reference panel
    only — no chemistry / interpretation code runs, the
    data IS the content.
  - `qualitative_tests.py` — **Phase 37a (round 136)**
    *Tools → Qualitative inorganic tests…* (Ctrl+Shift+Q).
    Modeless singleton dialog backed by
    `core/qualitative_tests.py`.  Layout: left side =
    category combo (`(all categories)` + 7 categories) +
    free-text filter + `QListWidget` of `target — name`
    rows; right side = title + meta line (target + class +
    category) + colour swatch (auto-tinted from the entry's
    `colour_hex`) + `QTextBrowser` detail pane (Reagents /
    Procedure / Positive observation / Notes sections).
    `select_test(test_id)` programmatic API for the
    `open_qualitative_tests` agent action.  No chemistry
    runs — it's a reference panel, the data IS the content.
  - `drawing_tool.py` — **Phase 36g (round 126) + 36f.2 (round 132)**
    molecular drawing dialog. Modeless `DrawingToolDialog(QDialog)`
    singleton wrapping the Phase-36b `DrawingPanel`. Footer
    buttons: *Export drawing…* (PNG/SVG via
    `render.export.export_molecule_2d`, MOL-V2000 via
    `core.drawing.structure_to_molblock`), *Send to Molecule
    Workspace* (invokes the `add_molecule` authoring action with
    a `Drawn-XXXXXXXX` UUID name + `source_tags=["drawn"]`,
    handles duplicate-InChIKey via `existing_id`, fires
    `bus.molecule_selected` so every panel picks up the new row),
    and *Send to Reactions tab* (round 132 — pulls a
    `core.drawing_scheme.Scheme` from `panel.current_scheme()`,
    rejects empty / one-side-empty schemes with an info popup,
    prompts for a reaction name via `QInputDialog`, invokes the
    `add_reaction` authoring action with category `"Drawn"`,
    routes to the Reactions tab via `_open_reaction(rid)` which
    walks `MainWindow.tabs` for the Reactions panel and calls its
    `_display(rid)`; duplicate-name path opens the existing row).
    `singleton(parent, seed_smiles="")` classmethod preserves the
    canvas across re-opens and lets *Open in drawing tool…* hooks
    preload an existing molecule. Tools menu entry *Drawing tool…
    (Ctrl+Shift+D)*.
  - `script_editor.py` — **Phase 32a** Python REPL + editor dialog.
    Top pane: `QPlainTextEdit` with monospace font and a default
    snippet. Bottom pane: dark output console with colour-coded
    stdout / stderr / repr / traceback. Toolbar: Run (Ctrl+Enter),
    Run-selection (Ctrl+Shift+Enter), Stop, Reset globals, Open…,
    Save…. Singleton per app instance so `ScriptContext` globals
    persist across re-opens. Wrapper runs snippets on a `_RunWorker`
    QThread so long calls don't freeze the UI. Tools menu entry
    *Script editor (Python)… (Ctrl+Shift+E)*.
  - `command_palette.py` — **Ctrl+K command palette** (Phase 11b
    follow-up, round 54). Single-keystroke jump-to-anything dialog:
    type a glossary term, reaction name, or molecule name and Enter
    to route into the matching tab. Entry assembler
    `build_palette_entries()` pulls ~400 rows from the seeded DB +
    `_GLOSSARY`; `dispatch_palette_entry(entry, main_win)` owns
    the routing (Glossary → `focus_term`, Reactions →
    `reactions._display`, Molecule Workspace via
    `bus.molecule_selected`). Wired into *View → Command palette…*.
  - `preferences.py` — global settings: default 3D backend, 3D style, log
    level, theme, autogen-3D-on-import, online sources. Saves to YAML and
    emits `bus.config_changed`.
  - `mechanism_player.py` — modal step-through for a `Mechanism`, with
    Prev / Next / step counter / per-step SVG save.
  - `reaction_trajectory_player.py` — modal 3D animation host
    (QWebEngineView + 3Dmol.js). Play/pause/reset/speed in-HTML.
  - `energy_profile_viewer.py` — modal for Phase 13d: shows the
    reaction-coordinate diagram (matplotlib-rendered PNG preview +
    summary of Ea / ΔH + save button). Launched from the *Energy
    profile…* button on the Reactions tab.
  - `dynamics_player.py` — modal for Phase 10a conformational dynamics:
    mode dropdown (conformer morph / dihedral scan) + rotatable-bond
    picker. Plays via the same trajectory HTML.

### `agent/` — LLM / headless control layer

| File | Key symbols |
|------|-------------|
| `actions.py` | `@action` decorator, `registry()`, `invoke(name, **kw)`, `tool_schemas()` — typed action registry auto-emits Anthropic / OpenAI tool schemas. |
| `controller.py` | `set_main_window(win)` / `main_window()` / `require_main_window()` — process-wide pointer so GUI-touching actions (screenshots, menu triggers) can reach the running window without a circular import. |
| `library.py` | Built-in actions. Categories: **molecule** (`list_all_molecules`, `get_molecule_details`, `show_molecule`, `import_smiles`, `compare_molecules`), **tools** (`calculate_empirical_formula`), **online** (`search_pubchem`, `download_from_pubchem`), **tutorial** (`list_tutorials`, `open_tutorial`), **reaction** (`list_reactions`, `show_reaction`, `export_reaction_by_id`, `export_reaction_3d`, `export_reaction_trajectory_html`, `play_reaction_trajectory`, `list_energy_profiles`, `get_energy_profile`, `export_energy_profile`), **mechanism** (`list_mechanisms`, `open_mechanism`, `export_mechanism_step`), **synthesis** (`list_pathways`, `show_pathway`, `export_pathway`, `pathway_green_metrics`, `reaction_atom_economy`), **dynamics** (`run_dihedral_scan_demo`, `run_molecule_dihedral`, `run_molecule_conformer_morph`), **orbitals** (`huckel_mos`, `export_mo_diagram`, `list_wh_rules`, `get_wh_rule`, `check_wh_allowed`), **stereo** (`assign_stereodescriptors`, `flip_stereocentre`, `enantiomer_of`, `export_molecule_2d_stereo`), **glossary** (`define`, `list_glossary`, `search_glossary`, `show_term`), **medchem** (`drug_likeness`), **lab** (`predict_tlc`, `predict_rf`, `recrystallisation_yield`, `distillation_plan`, `extraction_plan`), **naming** (`list_naming_rules`, `get_naming_rule`, `naming_rule_categories`), **spectroscopy** (`predict_ir_bands`, `export_ir_spectrum`, `guess_formula`, `guess_formula_for_smiles`, `predict_ms_fragments`), **session** (`list_sessions`, `save_session_state`, `load_session_state`), **periodic** (`list_elements`, `get_element`, `elements_by_category`), **synthesis** (... `find_retrosynthesis`, `list_retro_templates`, `find_multi_step_retrosynthesis`), **medchem** (`drug_likeness`, `list_sar_series`, `get_sar_series`, `export_sar_matrix`, `list_bioisosteres`, `suggest_bioisosteres`), **protein** (`list_seeded_proteins`, `fetch_pdb`, `get_protein_info`, `get_protein_chain_sequence`, `fetch_alphafold`, `get_alphafold_info`, `find_binding_sites`, `analyse_binding`, `export_interaction_map`, `analyse_ppi`, `analyse_ppi_pair`, `plip_capabilities`, `analyse_binding_plip`, `analyse_na_binding`, `export_protein_3d_html`), **export** (`export_molecule_2d_by_id`, `export_current_molecule_2d`, `export_molecule_3d`, `screenshot_window`, `screenshot_panel`). |
| `conversation.py` | `Conversation` — orchestrates the tool-use loop (user → model → actions → model → …). |
| `headless.py` | `HeadlessApp` — launches the full app with `QT_QPA_PLATFORM=offscreen`; use from tests or external Python drivers. |
| `bridge.py` | JSON-over-stdio bridge (`python main.py --agent-stdio`) so any external process (incl. a Claude Code session) can drive the app line-by-line. |
| `actions_search.py` | **Phase 33a** — `fulltext_search(query, limit, kinds)` agent action.  Thin wrapper around `core.fulltext_search.search()`; accepts comma-separated `kinds` for filtering + returns JSON-serialisable dicts keyed by `{kind, title, snippet, score, key}`.  Validates unknown kinds with a clear error-return path instead of raising. |
| `actions_isomers.py` | **Phase 48c (round 172)** — isomer-relationship agent actions in the new `isomer` category: `find_stereoisomers(smiles, max_results=16)` (wraps `core.isomers.enumerate_stereoisomers` — under-specified input expands to all consistent stereoisomers; returns `{input_smiles, canonical_smiles_list, truncated}` dict; unparseable input → empty list, NOT an error), `find_tautomers(smiles, max_results=16)` (wraps `enumerate_tautomers`; covers RDKit's ~ 20 tautomer rules — keto/enol, amide/iminol, hydroxypyridine/pyridone, nitroso/oxime), `classify_isomer_pair(smiles_a, smiles_b)` (wraps `classify_isomer_relationship` — returns `{smiles_a, smiles_b, relationship, formula_a, formula_b}` dict where `relationship` is one of the canonical 7 RELATIONSHIPS strings; the formulas surface AS PART OF THE RESPONSE so the agent can immediately reason about whether the pair shares a formula), `open_isomer_explorer(tab="")` (open the *Tools → Isomer relationships…* dialog and optionally focus a specific tab — Stereoisomers / Tautomers / Classify pair).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread.  All 4 registered in `gui/audit.py`. |
| `actions_biochemistry_by_kingdom.py` | **Phase 47c (round 168)** — biochemistry-by-kingdom agent actions in the new `kingdom` category: `list_kingdom_topics(kingdom="", subtab="")` (clean error dict for unknown kingdom or sub-tab), `get_kingdom_topic(topic_id)`, `find_kingdom_topics(needle)` (case-insensitive substring across id + title + body + cross-reference fields), `open_biochemistry_by_kingdom(kingdom="", subtab="", topic_id="")` (open the *Window → Biochemistry by Kingdom…* window — Ctrl+Shift+K — and optionally focus a specific kingdom outer tab + sub-tab + topic).  Lookup actions are pure-headless; the window opener marshals onto the Qt main thread and reports `selected: True/False` so the agent can introspect failure paths (unknown kingdom / id).  All 4 registered in `gui/audit.py`. |
| `actions_cell_components.py` | **Phase 43 (round 151)** — cell-component agent actions in the new `cell` category: `list_cell_components(domain="", sub_domain="")` (clean error dict for unknown domain or sub-domain), `get_cell_component(component_id)`, `find_cell_components(needle)`, `cell_components_for_category(category)` (returns the components of a category — empty for empty category, error dict for unknown category), `open_cell_components(component_id="")` (open the *Tools → Cell components…* dialog and optionally focus an entry).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread. |
| `actions_microscopy.py` | **Phase 44 (round 150)** — microscopy agent actions in the new `microscopy` category: `list_microscopy_methods(resolution_scale="")`, `get_microscopy_method(method_id)`, `find_microscopy_methods(needle)` (case-insensitive substring), `microscopy_methods_for_sample(sample_type)` (returns the methods listing the given sample type as typical — empty for unknown samples; clean error dict when the sample is non-empty but unrecognised), `open_microscopy(method_id="")` (open the *Tools → Microscopy techniques…* dialog and optionally focus an entry).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread. |
| `actions_lab_reagents.py` | **Phase 45 (round 149)** — lab-reagents agent actions in the new `reagent` category: `list_lab_reagents(category="")`, `get_lab_reagent(reagent_id)`, `find_lab_reagents(needle)` (case-insensitive substring across id + name + category + typical_usage + cas_number — CAS searches like "67-68-5" → DMSO work directly), `open_lab_reagents(reagent_id="")` (open the *Tools → Lab reagents…* dialog and optionally focus an entry).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread. |
| `actions_ph_explorer.py` | **Phase 46 (round 148)** — pH + buffer agent actions in the new `ph` category: `list_pka_acids(category="")`, `get_pka_acid(acid_id)`, `find_pka_acids(needle)` (case-insensitive substring across id + name + formula + category), `design_buffer(target_pH, pKa, total_concentration_M, volume_L=1.0)` (Henderson-Hasselbalch + capacity warning), `buffer_capacity(total_concentration_M, pH, pKa)` (β + α + fraction_of_max), `simulate_titration(weak_acid_pKa, acid_initial_M, volume_acid_mL, base_concentration_M, n_points=50)` (full curve + equivalence point), `open_ph_explorer(tab="")` (open the *Tools → pH explorer…* dialog and optionally focus a tab).  Lookup + solver actions are pure-headless; solver actions return `{"error": ...}` on bad input rather than raising; the dialog opener marshals onto the Qt main thread. |
| `actions_metabolic_pathways.py` | **Phase 42a (round 147)** — metabolic-pathway agent actions in the `biochem` category: `list_metabolic_pathways(category="")`, `get_metabolic_pathway(pathway_id)`, `find_metabolic_pathways(needle)` (case-insensitive across id + name + overview), `list_pathway_steps(pathway_id)` (lighter than the full pathway record — just the step list), `open_metabolic_pathways(pathway_id="", step_number=0)` (opens the *Tools → Metabolic pathways…* dialog and optionally focuses pathway + step). |
| `actions_lab_analysers.py` | **Phase 40a (round 146)** — major-lab-analyser agent actions in the `instrumentation` category: `list_lab_analysers(category="")`, `get_lab_analyser(analyser_id)`, `find_lab_analysers(needle)` (case-insensitive substring across id + name + manufacturer + category), `open_lab_analysers(analyser_id="")` (open the *Tools → Lab analysers…* dialog and optionally focus an entry).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread. |
| `actions_centrifugation.py` | **Phase 41 (round 144)** — centrifugation agent actions in the `centrifugation` category: `list_centrifuges_action(centrifuge_class="")`, `get_centrifuge_action(centrifuge_id)`, `list_rotors_action(rotor_type="")`, `get_rotor_action(rotor_id)`, `list_centrifugation_applications(protocol_class="")`, `rpm_to_g_action(rpm, radius_cm)`, `g_to_rpm_action(g_force, radius_cm)`, `open_centrifugation(tab, rotor_id, centrifuge_id, application_id)` (open the *Tools → Centrifugation…* dialog and optionally focus tab + entry).  Lookup + solver actions are pure-headless; the dialog opener marshals onto the Qt main thread.  Solver actions return `{"error": ...}` on bad input rather than raising. |
| `actions_calc.py` | **Phase 39b (round 143) + 39c (round 145)** — lab-calculator agent actions.  39b: `open_lab_calculator(tab="")` opens the *Tools → Lab calculator…* tabbed dialog and optionally focuses one of the 7 tabs.  39c: 31 per-solver wrappers, one per Phase-39a solver, all in the `calc` category — `molarity` / `dilution` / `serial_dilution` / `molarity_from_mass_percent` / `ppm_to_molarity` / `molarity_to_ppm` / `limiting_reagent` / `theoretical_yield` / `percent_yield` / `percent_purity` / `ph_from_h` / `h_from_ph` / `pka_to_ka` / `ka_to_pka` / `henderson_hasselbalch` / `ideal_gas` / `combined_gas_law` / `gas_density` / `boiling_point_elevation` / `freezing_point_depression` / `osmotic_pressure` / `heat_capacity` / `hess_law_sum` / `first_order_half_life` / `first_order_integrated` / `arrhenius` / `eyring_rate_constant` / `equilibrium_constant` / `ksp_from_solubility` / `solubility_from_ksp` / `ice_solve_a_plus_b`.  Each wrapper has the same kwargs as the underlying solver and returns the solver's result dict on success, `{"error": str}` when the solver raises `ValueError`.  Common `_wrap` helper handles the exception-to-error-dict conversion.  32 calc actions total (31 solvers + 1 dialog opener); GUI audit references each. |
| `actions_lab_setups.py` | **Phase 38b (round 141)** — lab-setup agent actions: `list_lab_setups()` (full catalogue with equipment + connection details), `get_lab_setup(setup_id)`, `find_lab_setups(needle)`, `validate_lab_setup(setup_id)` (returns `{"valid": bool, "errors": [str]}` — useful for the future Phase-38c canvas to verify a user-built setup before *Run simulation*), `open_lab_setups(setup_id="")` (open the *Tools → Lab setups…* dialog and optionally focus a specific setup).  Lookup + validation actions are pure-headless; the dialog opener marshals onto the Qt main thread.  All five registered under the `lab` category. |
| `actions_lab_equipment.py` | **Phase 38a (round 140)** — lab-equipment agent actions: `list_lab_equipment(category="")` (full catalogue, optional category filter — unknown categories return `{"error": ...}`), `get_lab_equipment(equipment_id)` (full record by id with serialised connection ports), `find_lab_equipment(needle)` (case-insensitive substring), `open_lab_equipment(equipment_id="")` (open the *Tools → Lab equipment…* dialog and optionally focus an item).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread.  All four registered under the `lab` category. |
| `actions_spectrophotometry.py` | **Phase 37d (round 139)** — spectrophotometry-method agent actions: `list_spectrophotometry_methods(category="")`, `get_spectrophotometry_method(method_id)`, `find_spectrophotometry_methods(needle)`, `beer_lambert(absorbance, molar_absorptivity, path_length_cm, concentration_M)` (pass any 3 of 4 quantities; returns the full 4-tuple or `{"error": ...}`), `open_spectrophotometry(method_id="")` (open the *Tools → Spectrophotometry techniques…* dialog and optionally focus a method).  Lookup + Beer-Lambert actions are pure-headless; the dialog opener marshals onto the Qt main thread.  All five registered under the `spectrophotometry` category. |
| `actions_chromatography.py` | **Phase 37c (round 138)** — chromatography-method agent actions: `list_chromatography_methods(category="")` (full catalogue, optional category filter), `get_chromatography_method(method_id)` (full record by id), `find_chromatography_methods(needle)` (case-insensitive name / abbreviation / id substring match), `open_chromatography_methods(method_id="")` (open the *Tools → Chromatography techniques…* dialog and optionally focus a method).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread.  All four registered under the `chromatography` category. |
| `actions_clinical.py` | **Phase 37b (round 137)** — clinical lab-panel agent actions: `list_lab_panels()` (one-row-per-panel summary), `get_lab_panel(panel_id)` (full record incl. every analyte), `list_lab_analytes(category="")` (every analyte deduplicated across panels, optionally category-filtered), `find_lab_analyte(needle)` (case-insensitive name / abbreviation / id), `open_clinical_panels(panel_id="", analyte_id="")` (open the *Tools → Clinical lab panels…* dialog and optionally focus a panel + row).  Lookup actions are pure-headless; the dialog opener marshals onto the Qt main thread via `_gui_dispatch.run_on_main_thread_sync`.  All five registered under the `clinical` category. |
| `actions_qualitative.py` | **Phase 37a (round 136)** — qualitative inorganic-test agent actions: `list_inorganic_tests(category="")` (full catalogue, optionally filtered — unknown categories get a clean `{"error": ...}`), `get_inorganic_test(test_id)` (full record by id), `find_inorganic_tests_for(target)` (every test matching an ion / gas — case + sub/superscript tolerant via the `_normalise_ion_label` helper, so `"Cu²⁺"` and `"Cu2+"` hit the same rows), `open_qualitative_tests(test_id="")` (open the *Tools → Qualitative inorganic tests…* dialog and optionally focus a specific entry; marshals onto the Qt main thread via `_gui_dispatch.run_on_main_thread_sync`).  All four registered under the `qualitative` category. |
| `actions_drawing.py` | **Phase 36h (round 127) + 36f.1 (round 131)** — drawing-tool agent actions: `open_drawing_tool(smiles="")` (lazy singleton dialog, optional SMILES preload), `drawing_to_smiles()` (canvas → canonical SMILES + `{n_atoms, n_bonds}`), `drawing_export(path)` (PNG/SVG via `render.export.export_molecule_2d`, MOL-V2000 via `core.drawing.structure_to_molblock`; rejects other suffixes), `drawing_clear()` (wipe canvas), `make_reaction_scheme(lhs_smiles, rhs_smiles, arrow="forward", reagents="")` (round 131 — pure-headless wrapper around `core.drawing_scheme.Scheme` that bundles two SMILES into a `LHS>reagents>RHS` reaction-SMILES string + canonical-SMILES echo + balanced-atom-count flag; rejects unknown arrow types or unparseable SMILES with a clean `{"error": ...}` response).  The four GUI-touching actions marshal onto the Qt main thread via `_gui_dispatch.run_on_main_thread_sync`; `make_reaction_scheme` is fully headless.  Every entry point returns `{"error": ...}` when the main window or the drawing dialog isn't reachable rather than raising. |
| `script_context.py` | **Phase 32a** — persistent Python REPL context for the scripting workbench. `ScriptContext` owns a globals dict with pre-imported `app` (an `AppProxy` exposing every registered action as `app.<name>(…)` + `app.call('name', **kw)` + `app.list_actions()`), `chem` (RDKit), `orgchem`, and a `viewer` stub that raises `WorkbenchNotReadyError` pending Phase 32b. `run(source)` returns an `ExecResult` with captured stdout / stderr / last-expression repr / traceback. `reset()` flushes state. Also registers the `open_script_editor` agent action (main-thread-dispatched through `_gui_dispatch`). |
| `llm/base.py` | `LLMBackend` abstract class + `ChatMessage` / `ToolCall` / `ToolResult` dataclasses. |
| `llm/anthropic_backend.py` | Claude via the `anthropic` SDK. |
| `llm/openai_backend.py` | OpenAI-compatible (works with Azure, DeepSeek, Groq, …). |
| `llm/ollama_backend.py` | Local inference via Ollama's HTTP API. |

**Adding a new LLM-callable action**: decorate a function in
`agent/library.py` (or any module you import) with `@action(category="…")`.
The tutor panel and the stdio bridge pick it up automatically.

### `scene/` — Phase 32b scene composer
| File | Key symbols |
|------|-------------|
| `scene.py` | `Scene` class (observable scene graph), `Track` dataclass with `name` / `kind` (`molecule` / `protein` / `ligand`) / `data` / `source_format` (`mol` / `pdb`) / `style` / `colour` / `visible` / `opacity` / `meta`, `SceneEvent` enum (TRACK_ADDED, TRACK_REMOVED, TRACK_STYLE_CHANGED, TRACK_VISIBILITY_CHANGED, CLEARED, CAMERA_CHANGED). Public API: `add_molecule(smi_or_mol, *, track, style, colour)` → embeds 3D coords if absent; `add_protein(pdb_id_or_text, *, track, style, colour)` — 4-char alphanumeric string is treated as a PDB ID and fetched via `sources.pdb.fetch_pdb_text`; `remove(name)`, `clear()`, `set_visible(name, bool)`, `set_style(name, style=, colour=, opacity=)`, `snapshot(path)` (requires a Workbench listener with `grab_png`), `listen(fn)` with unsubscribe thunk. Process-wide singleton via `current_scene()` / `reset_current_scene()`. Zero Qt imports — fully headless-testable. |
| `html.py` | `build_scene_html(scene, background)` — assembles a complete 3Dmol.js HTML page for every visible track. Reuses the bundled local 3Dmol.js asset (`gui/assets/3Dmol-min.js`) from `render/draw3d.py` when present; falls back to CDN. Protein tracks get an automatic HETATM stick overlay so bound ligands stay visible under cartoon styles. Empty scenes emit a placeholder label instead of a broken `zoomTo()`. |

### `tutorial/`
| File | Key symbols |
|------|-------------|
| `curriculum.py` | `CURRICULUM` dict: level → list of lessons with markdown paths. |
| `loader.py` | `load_tutorial_markdown(path)`. |
| `macros.py` | **Phase 11c follow-up** — `expand_term_macros(md)` preprocesses `{term:SN2}` / `{term:SN2\|display}` forms into proper Markdown links to the `orgchem-glossary:` scheme. The tutorial panel runs this before handing markdown to the renderer and catches the anchor clicks to switch the Glossary tab. Supports a `\{term:…}` escape for literal display. |
| `content/` | Markdown lessons organised by level (`beginner/`, `intermediate/`, `advanced/`, `graduate/`). **Intermediate tier is complete** as of 2026-04-22 (stereochemistry, SN1/SN2, E1/E2, aromaticity, carbonyl, energetics). |

### `naming/` (Phase 12)
| File | Key symbols |
|------|-------------|
| `rules.py` | `NamingRule` dataclass; `RULES` list of 22 IUPAC rules across 11 categories; `list_rules(category)`, `get_rule(id)`, `rule_categories()`. Drives the agent actions `list_naming_rules` / `get_naming_rule` / `naming_rule_categories`. |

## Inter-module rules
1. `core/` must not import from `gui/`, `db/`, or `sources/`.
2. `gui/` panels communicate via `messaging/bus.py`, never directly with each other.
3. Long-running work (DB, network, conformer gen) goes through `utils/threading.py`.
4. Every user-visible message uses `logging` — the bus handler routes to the GUI.
5. All files stay under 500 lines; split if growing.

## Adding a new panel (checklist)
1. Create `orgchem/gui/panels/my_panel.py`.
2. Subscribe to the `bus()` signals you need in `__init__`.
3. Register it in `MainWindow._build_docks()` or `_build_central()`.
4. Update this file (`INTERFACE.md`).

## Adding a new data source
1. Create `orgchem/sources/my_source.py` — subclass `DataSource`.
2. Add to `_SOURCES` in `gui/panels/search_panel.py`.
3. Update this file.

## Headless / LLM-driven operation
- Python driver:
  ```python
  from orgchem.agent.headless import HeadlessApp
  with HeadlessApp() as app:
      app.call("show_molecule", name_or_id="Caffeine")
      app.call("screenshot_window", path="caffeine.png", settle_ms=1000)
  ```
- External process (incl. Claude Code):
  ```
  python main.py --agent-stdio
  ```
  then write one JSON request per line, read one JSON response per line.
- Smoke test: `pytest tests/test_smoke_headless.py`.
- Worked example: `scripts/claude_drive_demo.py {direct|stdio}`.
- Visual tour (gallery under `screenshots/tour/`): `python scripts/visual_tour.py`.

## Image export & screenshots
- **2D structures** — works in both GUI and headless modes (pure RDKit path).
  File menu: *Export current molecule (2D)…* (Ctrl+E). Agent actions:
  `export_molecule_2d_by_id(molecule_id, path)` and
  `export_current_molecule_2d(path)`.
- **Screenshots** — any `QWidget` → PNG via `QWidget.grab()`. File menu:
  *Screenshot window…* (Ctrl+Shift+P). Agent actions: `screenshot_window(path)`
  and `screenshot_panel(name, path)` (aliases: `2d`, `3d`, `browser`,
  `props`, `tutor`, `session_log`, `tutorial`, `search`).
- **Offscreen caveat**: in headless mode we disable Chromium's GPU (needed
  for stability across molecule swaps), which also disables WebGL — so the
  3D panel is blank in headless screenshots. Run `python main.py`
  interactively for full 3D.
