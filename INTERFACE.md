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
| `stereo.py` | `assign_rs(mol)`, `assign_ez(mol)`, `stereocentre_atoms(mol)`, `flip_stereocentre(mol, idx)`, `enantiomer_of(mol)`, `summarise(mol)` — canonical CIP / E-Z API (cross-cutting stereochem helper). Wraps RDKit's `AssignStereochemistry`. |
| `druglike.py` | `lipinski(mol)`, `veber(mol)`, `ghose(mol)`, `pains(mol)`, `qed_score(mol)`, `drug_likeness_report(mol)` — medicinal-chem descriptor panel (Phase 19b). |
| `chromatography.py` | `predict_rf(smiles, solvent)`, `simulate_tlc(smiles_list, solvent)`, `solvent_polarity(name_or_mixture)` — TLC/Rf teaching predictor (Phase 15b). |
| `lab_techniques.py` | `solubility_curve`, `recrystallisation_yield`, `distillation_plan`, `extraction_plan`, `fraction_ionised` — practical-lab teaching helpers (Phase 15a-lite). |
| `glossary_figures.py` | `render_term(term, smiles, out_dir)` + `regenerate_all(out_dir)` — incremental PNG/SVG generator for the Phase 26a `example_smiles` field. Delegates to `draw2d` (single molecules) or `draw_reaction` (SMILES with `>>`). `term_slug()` normalises term names into filename stems; `default_figure_dir()` points at `data/glossary/`. Companion script `scripts/regen_glossary_figures.py`, agent action `get_glossary_figure(term, path)`. (Phase 26b) |
| `molecule_tags.py` | `auto_tag(mol_or_smiles)` → `TagResult` with functional-group / composition / charge / size-band / ring-band / stereo tags. 27 SMARTS-based functional groups (carboxylic acid → phosphate), 7 composition flags (halogen / P / S / pure-organic / metal / …), 4 charge categories (neutral / cation / anion / zwitterion), 3 size bands (≤ 12 / 13-30 / ≥ 31 heavy atoms), 3 ring-count bands. `FILTER_AXES` + `list_filter_axes()` surface the taxonomy for the filter-bar UI — includes the **source** axis (drug-class / NSAID / statin / alkaloid / hormone / steroid / fatty-acid / …) curated by `seed_source_tags.py`. (Phase 28c + 28b) |
| `carbohydrates.py` | `Carbohydrate` dataclass + 15-row `CARBOHYDRATES` catalogue covering monosaccharides (glucose α/β/open-chain, fructose, ribose / 2-deoxyribose, galactose, mannose), disaccharides (sucrose, lactose, maltose, cellobiose), polysaccharide fragments (amylose α-1,4, cellulose β-1,4). `list_carbohydrates(family)`, `get_carbohydrate(name)`, `families()` helpers for the upcoming Carbohydrates tab (Phase 29b). (Phase 29a) |
| `lipids.py` | `Lipid` dataclass + 21-row `LIPIDS` catalogue across families `fatty-acid` (lauric / palmitic / stearic / oleic / linoleic / α-linolenic / arachidonic / EPA / DHA), `triglyceride` (tripalmitin, triolein), `phospholipid` (POPC, POPE, phosphatidic acid), `sphingolipid` (ceramide, sphingomyelin), `sterol` (cholesterol, ergosterol), and fat-soluble `vitamin` / hormone (vitamin D₃, testosterone, estradiol). Carries chain-length / unsaturation-count / ω-designation / melting-point metadata. `list_lipids(family)`, `get_lipid(name)`, `lipid_families()` helpers. (Phase 29b) |
| `nucleic_acids.py` | `NucleicAcidEntry` dataclass + 23-row `NUCLEIC_ACIDS` catalogue across families `nucleobase` (A/G/C/T/U + m6A, m5C), `nucleoside` (adenosine / guanosine / cytidine / uridine / thymidine / 2'-deoxyadenosine), `nucleotide` (ATP, cAMP, GTP, NAD⁺), `oligonucleotide` (ApG dinucleotide), and `pdb-motif` (1BNA B-DNA dodecamer, 1RNA, 143D G-quadruplex, 1EHZ tRNA-Phe, 1HMH hammerhead ribozyme). Strand = DNA / RNA tag. `list_nucleic_acids(family)`, `get_nucleic_acid(name)`, `nucleic_acid_families()` helpers. (Phase 29c) |
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
| `seed_mechanisms.py` | Multi-step mechanisms for 13 reactions (SN1, SN2, E1, E2, Diels-Alder, Aldol, Grignard, Wittig, Michael + enzyme mechanisms: chymotrypsin catalytic triad, class-I aldolase Schiff-base aldol, HIV protease aspartic-protease peptide hydrolysis, **RNase A 2-step phosphoryl transfer** — both enzyme mechanisms exercise Phase 13c lone-pair dots + bond-midpoint arrows). Versioned via `SEED_VERSION` (bumped to 7 round 30). |
| `seed_pathways.py` | 12 seeded synthesis pathways: Wöhler urea, Aspirin (industrial + Kolbe-Schmitt), Paracetamol (industrial + Hoechst 3-step), BHC Ibuprofen 3-step, Caffeine from theobromine, Phenacetin→Paracetamol, Vanillin from eugenol, Aniline from benzene 2-step, 2-Methyl-2-butanol via Grignard, **Met-enkephalin via Fmoc SPPS 5-step (Phase 16a)**. |
| `seed_energy_profiles.py` | 4 seeded reaction-coordinate energy profiles (SN2, SN1, E1, Diels-Alder) with textbook Ea / ΔH values. Versioned via `SEED_VERSION` so upgrades overwrite stale JSON. |
| `seed_glossary.py` | ~43 seeded glossary terms across bonding / stereochemistry / mechanism / reactions / synthesis / spectroscopy / lab-technique categories. Short markdown definitions with alias + see-also lists. |
| `seed_intermediates.py` | Phase 6f.3 — 119 intermediate molecules (carbocations, enolates, Fmoc-AAs, enzyme substrates, common ions, halides, etc.). Additive by name so re-runs skip duplicates. |
| `seed_coords.py` | Phase 6f.2 — one-shot backfill of `Molecule.molblock_2d` for every DB row, via `rdDepictor.SetPreferCoordGen(True) + Compute2DCoords`. Called automatically from `seed_if_empty`. |
| `seed_tags.py` | Phase 28a — backfill of functional-group / composition / charge / size / ring columns on every seeded molecule, driven by `core/molecule_tags.auto_tag`. Idempotent; called automatically from `seed_if_empty`. |
| `seed_source_tags.py` | Phase 28b — hand-curated `{name → [source-tag, …]}` map covering NSAIDs / statins / antibiotics / SSRIs / β-blockers / hormones / steroids / neurotransmitters / alkaloids / nucleosides / sugars / fatty acids / dyes / reagent subclasses. Idempotent backfill into `Molecule.source_tags_json` with a version sentinel. `list_source_tag_values()` enumerates the full taxonomy for the filter bar. |

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
- `widgets/smiles_input.py` — validated SMILES `QLineEdit` that emits canonical form.
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
| `llm/base.py` | `LLMBackend` abstract class + `ChatMessage` / `ToolCall` / `ToolResult` dataclasses. |
| `llm/anthropic_backend.py` | Claude via the `anthropic` SDK. |
| `llm/openai_backend.py` | OpenAI-compatible (works with Azure, DeepSeek, Groq, …). |
| `llm/ollama_backend.py` | Local inference via Ollama's HTTP API. |

**Adding a new LLM-callable action**: decorate a function in
`agent/library.py` (or any module you import) with `@action(category="…")`.
The tutor panel and the stdio bridge pick it up automatically.

### `tutorial/`
| File | Key symbols |
|------|-------------|
| `curriculum.py` | `CURRICULUM` dict: level → list of lessons with markdown paths. |
| `loader.py` | `load_tutorial_markdown(path)`. |
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
