# Project Status — OrgChem Studio

> Living document. Update at the end of every meaningful session.
> Last updated: **2026-04-24** (round 118 — **Phase 34e feature-track overlays — pockets + ligand contacts shipped on the sequence bar**. `ProteinPanel` now caches `_last_pockets` (Phase 24d `find_pockets` output) + `_last_contacts` (Phase 24e `analyse_binding` or PLIP `ContactReport`) at the moment each analysis runs.  `_refresh_sequence_bar` layers both onto the `SequenceView` via the round-112 `attach_pocket_highlights` + `attach_contact_highlights` helpers; the sequence bar paints the bands in the shared `HIGHLIGHT_COLOURS` palette — pocket=green, H-bond=blue, salt-bridge=red, π-stacking=purple, hydrophobic=tan.  Caches reset on new PDB / AlphaFold fetch so stale features from a prior structure don't bleed through.  3 new pytest cases: end-to-end feature-track full-stack (`test_feature_track_overlay_full_stack`), widget-storage regression (`test_sequence_bar_stores_highlights_from_view`), and a `ProteinPanel._refresh_sequence_bar` integration that primes fake pockets + contacts then asserts the widget's `_highlights` contains the expected kinds.  Remaining 34e polish: secondary-structure track (needs HELIX/SHEET records in the PDB parser), user-tag track with session persistence, UniProt gene-annotation track for DBREF-carrying PDBs.  **1 019 tests pass** (+3). Previous round 117 polish — **sequence-bar scroll arrows + Clear button + toggle-deselect**. `SequenceBarPanel` gains ◀ / ▶ scroll arrows (step = 10 residues = 1 tick-mark; `QToolButton.setAutoRepeat(True)` for held-button continuous scroll), a "Clear selection" `QPushButton` (enabled only while a selection exists), and a `selection_cleared` signal. `SequenceBar.mousePressEvent` now defers committing the selection so a press + release without drag on an already-selected residue toggles it off; drag still commits normally. Arrow enable-state mirrors scrollbar position (greyed at ends; both disabled when there's no overflow). `ProteinPanel._on_sequence_cleared` handler runs `window.orgchemClearHighlight()` through `runJavaScript` so the 3D ribbon returns to baseline the instant the user clears or toggles. 7 new pytest-qt tests covering: click-inside-selection toggles off; drag-inside-selection does NOT toggle; `clear_selection()` emits `selection_cleared` idempotently; Clear button disabled-until-selection + click clears + re-disables; panel re-emits cleared signal; scroll arrows step by exactly 10 × char_w px and enable/disable per scrollbar state. Forward-path `test_build_protein_html_exposes_live_highlight_helper` still passes — live sequence→3D highlight still works. **1 016 tests pass** (+7). Previous round 117 — **Phase 34c forward-path shipped — live sequence→3D highlight**. New `window.orgchemHighlight(chainId, start, end)` + `window.orgchemClearHighlight()` JS helpers injected into every `build_protein_html` page: clear any previous span, apply yellow-carbon sticks + residue labels to the new span, re-render — no HTML rebuild, no latency. `ProteinPanel._on_sequence_selection` pushes selections through `web_3d.page().runJavaScript(...)`. Sequence bar drag → 3D ribbon now updates live; combined with the round-116 reverse path (3D click → sequence caret), the full round-trip is closed end-to-end. New regression `test_build_protein_html_exposes_live_highlight_helper` checks the generated HTML exposes both helpers with the correct `(chainId, start, end)` signature + yellowCarbon style consistent with the static pipeline. **1 009 tests pass** (+1). Previous round 116 — **Phase 31l CLOSE at 15/15 + Phase 34b/c/d shipped — sequence viewer integrated into Proteins 3D sub-tab**. 31l close: chymotrypsin 5CHA (structural anchor for the round-62 mechanism + round-105 energy profile; teaching triad complete) + SARS-CoV-2 Mpro 6LU7 (Jin/Yang/Rao 2020 *Nature* — first COVID Mpro structure, cysteine-protease covalent-warhead story; pairs with 1HPV HIV aspartic protease for the proteases-two-chemistries contrast). 34b: new `orgchem/gui/widgets/sequence_bar.py` with `SequenceBar` + `SequenceBarPanel` — monospace rolling strip, residue-number ticks every 10, per-`HighlightSpan` colour underlay bands, click + click-drag selection, multi-chain stacking (DNA/RNA above proteins per teaching-reading order), `selection_changed` Qt signal. 34d: DNA strand is a free by-product of 34b — `build_sequence_view` classifies chains by residue kind so 1BNA/143D/1HMH/1AOI automatically render the nucleotide strip. 34c partial: reverse-path (3D pick → sequence caret) is live via `_on_atom_picked` → `sequence_panel.set_selection`; forward-path (sequence drag → 3D ribbon highlight) posts to the session log + picked-label for now, full `QWebChannel.qtBridge` live-update deferred to a polish round. 8 new pytest-qt tests for the widget; INTERFACE.md entry added. Phase 31 snapshot: 8 of 12 sub-phases at target (31a molecules / 31c mechanisms / 31d pathways / 31e energy profiles / 31f glossary / 31g tutorials / 31k expanding / 31l CLOSED). **1 008 tests pass** (+8). Previous round 115 — **Phase 31l +2 seeded proteins: nucleosome 1AOI + IgG 1IGT**. 1AOI (Luger/Richmond 1997 *Nature*) — the 2.8 Å nucleosome core particle showing 147 bp DNA wrapped 1.65× around the H2A/H2B/H3/H4 histone octamer; anchors every chromatin / histone-tail-modification teaching story. 1IGT (Harris/Edmundson 1997 *Biochemistry*) — first complete IgG structure, Y-shaped tetramer with CDR tips + Fc-region + Asn297 glycan; anchors every antibody-engineering / biological-drug story. Both entries are simple `SeededProtein` rows — PDB fetch / render / contact analysis all flow through the existing Phase 24a-l pipeline automatically. Regression test `test_seeded_proteins_has_core_targets` tightened with content-marker assertions: 1AOI story contains "histone", 1IGT story contains CDR / antigen / Fab. Catalogue now **13/15** proteins — 2 more closes Phase 31l. **1 000 tests pass**. Previous round 114 — **Phase 31l +1 seeded protein (KcsA 1BL8)**. Doyle/MacKinnon 1998 potassium channel — first atomic-resolution ion-channel structure (Nobel 2003). Teaching story captured: TVGYG selectivity filter carbonyl oxygens exactly mimic a K⁺ hydration shell, so K⁺ transit through the filter is near-isoergic while Na⁺ (too small to fill the cage) pays a large dehydration penalty — ~10 000-fold K⁺/Na⁺ selectivity drops out of pure geometry. Pairs pedagogically with 1HHO (cooperativity) as a second "architecture → specificity" anchor. Catalogue now **11/15** proteins. Regression `test_seeded_proteins_has_core_targets` tightened to require 1BL8 + content-assert "selectivity" keyword in the teaching story. **1 000 tests pass** (content-marker added to an existing test, no new test count). Previous round 113 — **🎯 1 000-test milestone + Phase 35b shipped — tutor `add_molecule` fetch_synonyms kwarg**. New `sources/pubchem.py::fetch_synonyms_by_inchikey(inchikey)` helper: best-effort PubChem InChIKey lookup, returns [] on any failure (import/network/parse), never raises. `add_molecule` authoring action accepts `fetch_synonyms=False`; when True, it runs the helper after validation, filters through round-109 `_looks_like_registry_id` + dedup against canonical name, caps at 10, persists the cleaned list to `synonyms_json`, and reports `synonyms_fetched: int` in the accepted response. Offline / missing-pubchempy / empty-hit / raising-lookup paths all leave the insert successful with 0 synonyms — the kwarg is truly optional, never gates acceptance. 5 new pytest cases in `tests/test_add_molecule_fetch_synonyms.py` (default-off, mocked happy path, mocked empty, raising-lookup silence, import-error simulation via `sys.modules.pop`). Phase 35 now **5/6 sub-phases done** (only 35c bulk backfill CLI remains — network-heavy, queued later). **1 000 tests pass** — first four-digit count. Previous round 112 — **Phase 34a shipped — headless sequence-viewer data core**. New `orgchem/core/sequence_view.py` with `SequenceView` / `ChainSequence` / `HighlightSpan` dataclasses + JSON `to_dict()`. `build_sequence_view(protein)` splits Phase-24a `Protein` by residue kind (protein / DNA / RNA); ion-only pseudo-chains skipped. `attach_contact_highlights` + `attach_pocket_highlights` stamp per-kind colour-coded spans via a shared `HIGHLIGHT_COLOURS` palette. Residue-id parser accepts "HIS57"/"A:HIS57"/ints/numeric strings. Agent action `get_sequence_view(pdb_id, include_contacts, ligand_name)` in `agent/actions_protein.py`. INTERFACE.md updated; audit wiring re-pins GUI coverage at **100 %** (128/128). 9 new pytest cases (build + both highlight helpers + agent happy path + missing-pdb error + residue-id fuzz). No Qt imports in core; fully headless-testable. Phase 34 now **1/6** sub-phases done. **995 tests pass** (+9). Previous round 111 — **Phase 35e regression-locked — synonym paths through Compare tab + `show_molecule` agent action**. Audit confirmed both surfaces route through `find_molecule_by_name`, which the round-58 patch wired to consult `synonyms_json` via ILIKE — so this sub-phase is test-only. 9 new pytest cases in `tests/test_synonym_lookup_paths.py`: 4 direct unit tests on `find_molecule_by_name` (Paracetamol→Acetaminophen, ASA→Aspirin, case-insensitive triple-variant, None-on-miss), 3 agent-action tests on `show_molecule` (both pairs + unknown-error path), 2 pytest-qt integration tests driving the Compare panel's slot `_on_load` (typed synonym → canonical name in the slot title). Locks the full user-facing synonym-lookup surface against future refactors. Phase 35 now **4/6 sub-phases done** (35a+35d+35e+35f). **986 tests pass** (+9). Previous round 110 — **Phase 35f shipped — molecule browser shows synonym hint**. List row now reads *"Acetaminophen   [C8H9NO2]  · Paracetamol"* when a natural-language synonym is available. Tooltip extended: *"<SMILES>\n\nAlso known as: <list>"* when synonyms are present, bare SMILES otherwise. Filtering reuses round-109 `_looks_like_registry_id` so CAS / ChEMBL / UNII / DTXSID / InChI / InChIKey noise never appears in the hint; canonical self-references also removed. 5 new pytest-qt tests in `tests/test_molecule_browser_synonym_hint.py` (3 unit tests on the helpers, 2 integration tests walking the seeded DB). Phase 35 now **3/6 sub-phases done** (35a+35d+35f). **977 tests pass** (+5). Previous round 109 — **Phase 35d shipped — command palette learns synonyms**. `_molecule_entries()` now emits one `PaletteEntry` per synonym (same target id, distinct label, sublabel *"alias of <canonical>"*) so typing "Paracetamol" reaches Acetaminophen directly instead of failing. New `_looks_like_registry_id()` helper filters CAS numbers (`nnn-nn-n`), pure digits, `CHEMBL\d+`, `UNII-…`, `DTXSID`, `InChI=…`, and 27-char InChIKey strings — so only natural-language aliases make it into the palette. 2 new pytest-qt tests: (a) every row with ≥1 `synonyms_json` entry is reachable via ≥1 alias; (b) registry-ID rejection rules fuzz-tested against 8 known-bad + 5 known-good strings. Phase 35a was already shipped in round 58 (download_from_pubchem persists synonyms on new-row insert). **972 tests pass** (+2). Previous round 108 — **Phase 31k +1 SAR series (PDE5 inhibitors)**. 5 variants (sildenafil / vardenafil / tadalafil / avanafil / udenafil) with PDE5 IC50 + half-life + PDE6 selectivity columns. Three pedagogically loaded inequalities encoded as hard test assertions: (a) vardenafil is most PDE5-potent of the class, (b) tadalafil has the longest half-life (17.5 h vs ~4 h for the pyrazolopyrimidinone family) — the "weekend pill", (c) tadalafil simultaneously has the highest PDE6 selectivity (~700× vs <15× for the rest) — a single chemotype switch (pyrazolopyrimidinone → β-carboline diketopiperazine) resolves both half-life AND visual-disturbance liabilities. Catalogue now **7/15**. Also: Phase 34 added to ROADMAP — amino-acid sequence viewer + cross-linked 3D selection + DNA strand + feature tracks (user-flagged 2026-04-24). **970 tests pass** (+1). Previous round 107 — **Phase 31l +1 seeded protein (haemoglobin 1HHO R-state)**. Canonical Monod-Wyman-Changeux cooperativity teaching target. Pairs pedagogically with myoglobin (1MBN, round 47) — same globin fold + same heme-b prosthetic group, but four interlocked subunits that rotate ~15° between T (deoxy, cf. 2HHB) and R (oxy, this entry) quaternary states. The teaching story captured in the `SeededProtein.teaching_story` field references both 1MBN for the fold comparison and 2HHB for the T-state rotation delta. Catalogue now **10/15**. Regression test `test_seeded_proteins_has_core_targets` tightened to include 1HHO + content assertion on "cooperativity" keyword. **969 tests pass**. Previous round 106 — **Phase 31e CLOSE — Friedel-Crafts alkylation profile caps the catalogue at 20/20**. 7 points / 3 TSs. Distinguishes itself from the round-101 nitration curve by including the extra pre-equilibrium TS for CH₃⁺ generation (AlCl₃ abstracts Cl⁻). The endergonic free-cation minimum at +25 kJ/mol is the shape fingerprint that explains why FC alkylation rearranges and over-alkylates while nitration does neither (nitronium is a pre-formed stable cation). SEED_VERSION 10 → 11. New `test_friedel_crafts_profile_has_free_cation` locks 3 invariants (3 TSs, free-cation minimum above baseline, Wheland intermediate above baseline). Phase 31e is now **COMPLETE at 20/20**. **969 tests pass** (+1). Previous round 105 — **Phase 31e +1 energy profile (chymotrypsin catalytic triad)**. First enzyme-catalysed profile in the catalogue. 9 points / 4 TSs / 5 minima capturing the canonical "covalent-catalysis double hump": two tetrahedral intermediates bracket a covalent acyl-enzyme well that sits BELOW the Michaelis complex — the structural fact that makes serine proteases ~10¹⁰× faster than solution amide hydrolysis. Both tetrahedral intermediates are real minima lowered by oxyanion-hole H-bonds (Gly-193, Ser-195 backbone NH). SEED_VERSION 9 → 10. New `test_chymotrypsin_profile_acyl_enzyme_well` locks in: exactly 4 TSs, acyl-enzyme < Michaelis complex, both tetrahedral intermediates strictly between Michaelis and the highest TS. Catalogue now **19/20** — one more profile closes Phase 31e. **968 tests pass** (+1). Previous round 104 — **Phase 31e +1 energy profile (pinacol rearrangement)**. Textbook 1,2-methyl-shift shape: 7 points, 3 TSs, 3 minima. Ionisation TS (+100) is RDS; the migration TS (+50) is strictly lower — migration is fast once the tertiary carbocation exists; critically, the post-shift oxocarbenium (−20) sits below the pre-shift carbocation (+40) because O lone-pair donation stabilises C=O⁺-H better than hyperconjugation stabilises tert-C⁺. That inequality IS why 1,2-shifts run forward. SEED_VERSION 8 → 9. New `test_pinacol_profile_methyl_shift_downhill` locks in: 3 TSs present, ionisation TS highest, oxocarbenium < tert-carbocation. Catalogue now **18/20**. **967 tests pass** (+1). Previous round 103 — **Phase 31e +1 energy profile (bromination of ethene)**. Canonical bromonium-valley anti-addition shape: RDS at +80 kJ/mol (step 1 π-attack + Br-Br heterolysis), 3-membered bromonium intermediate at +40 sits above reactants but below both TSs, step-2 backside SN2 opening at +50, strongly exergonic anti-dibromide product at −100. The shape IS the teaching point — it's *why* anti-addition stereochemistry happens (Br⁻ attacks from the opposite face of the bromonium, not the same face). SEED_VERSION 7 → 8. New `test_bromination_profile_bromonium_valley` locks in 4 shape invariants (2TS+3min, RDS is first TS, bromonium above reactants but below both TSs, ΔH < −50). Catalogue now **17/20**. **966 tests pass** (+1). Previous round 102 — **Phase 31e +1 energy profile (NaBH₄ reduction)**. Simplest irreversible-addition shape in the catalogue: single rate-limiting 4-centre hydride-transfer TS at +55 kJ/mol, stabilised borate-alkoxide well at −80, trivial workup TS below the reactant baseline, 2-propanol product at −115 kJ/mol (ΔH < −50 enforced in test). Teaching complement to Grignard addition (same shape class, different nucleophile polarity — Grignard's alkoxide is much deeper due to Mg-O coordination). SEED_VERSION 6 → 7. New `test_nabh4_profile_strongly_exergonic` locks in ΔH < −50 + single-TS-above-baseline invariants. Catalogue now **16/20**. **965 tests pass** (+1). Previous round 101 — **Phase 31e +1 energy profile (nitration of benzene)**. Canonical 3-point EAS saddle-dip-saddle shape: rate-limiting NO₂⁺ attack TS at +90 kJ/mol, Wheland (arenium) intermediate in a shallow resonance-stabilised valley at +45 (sits above reactants but below both TSs), low-barrier deprotonation at +55, re-aromatised nitrobenzene product at −25 kJ/mol. The σ-complex shape every seeded EAS profile will inherit. SEED_VERSION 5 → 6. New `test_nitration_profile_has_wheland_valley` locks in the three shape invariants (first TS > second TS; Wheland above reactants; Wheland below both TSs). Catalogue now **15/20**. **964 tests pass** (+1). Previous round 100 — **milestone: Phase 31k +1 SAR series (β-lactam penicillins)**. 5 variants: Penicillin G / Ampicillin / Amoxicillin / Methicillin / Cloxacillin with MIC (S. aureus) + β-lactamase-stability + oral-bioavailability activity columns. Three textbook teaching points encoded numerically: α-amino tuning oral absorption (20 → 40 → 90 %), steric shielding buys β-lactamase stability, and shielding costs MIC potency (methicillin ~150× weaker than Pen-G). Source: Fleming 1929 / Rolinson 1998. Catalogue now **6/15** series. New `test_beta_lactam_series_landmarks` locks in all three inequalities. **963 tests pass** (+1). Previous round 99 — **Phase 31e +1 energy profile**: shipped Fischer esterification — a shallow 5-point curve encoding the textbook *thermoneutral equilibrium* (|ΔH| < 15 kJ/mol, K ≈ 3). Pairs pedagogically with the round-98 Claisen profile: Claisen is driven by the final deprotonation step, Fischer only by Le Chatelier (excess alcohol or Dean-Stark water removal). SEED_VERSION 4 → 5 so existing DBs pick up the new payload. New `test_fischer_profile_is_thermoneutral` locks in the |ΔH| < 15 invariant. Catalogue now **14/20**. **962 tests pass** (+1). Previous round 98 — **Phase 31e +1 energy profile**: shipped Claisen condensation (4-step ester enolate). Encodes the textbook "final deprotonation drives the equilibrium" teaching point numerically: 4 TSs, 5 minima; the penultimate neutral β-ketoester sits near thermoneutral (|ΔG| < 20 kJ/mol) while the final stabilised enolate drops 35 kJ/mol downhill — precisely the step that makes Claisen work. SEED_VERSION bumped to 4 so existing DBs pick up both the new Claisen payload and any version-3 refreshes. New regression `test_claisen_profile_driven_by_final_deprotonation` locks in the teaching-point geometry. Catalogue now **13/20**. **961 tests pass** (+1). Previous round 97 — **housekeeping round 2**: round-94 pollution purge missed 58 `Tutor-test ester hydrolysis {uuid}` reactions in the user's DB because the prefix was `Tutor-test-` (hyphen-terminated) but one historical authoring-action test used a space. Fixed by (a) normalising that one test to the dash convention, (b) broadening the `TEST_NAME_PREFIX` to `Tutor-test` (no trailing separator), (c) adding the missing `sys.path` prepend in `scripts/cleanup_tutor_test_pollution.py` so the CLI runs without PYTHONPATH, (d) regression test `test_purge_catches_space_suffix_reaction` that inserts a space-suffixed reaction and confirms the default prefix catches it. 58 polluted reactions purged from the live DB. **960 tests pass** (+1). Previous round 96 — **Phase 31k +1 SAR series**: shipped SSRIs (serotonin-reuptake inhibitors). 5 variants: fluoxetine / sertraline / paroxetine / citalopram / escitalopram, each with SERT Ki + NET Ki + SERT-selectivity + R-group / MoA notes. Chiral-switch case study encoded in the data: citalopram racemate 3700× SERT-selective → escitalopram (S-enantiomer) 11200× selective. Catalogue now **5/15** series (was 4). Source: Owens 1997 JPET + Sanchez 2004 BCPT. 2 new regression tests (landmark ordering + MW-band sanity) in `test_sar.py`. **959 tests pass**. Previous round 95 — **Phase 33c close**: surface-integrated full-text filter landed on the Reactions and Synthesis tabs. A new `"Full text"` `QCheckBox` sits beside each tab's filter box; when checked, `_on_filter` routes through `core/fulltext_search.search()` (kinds `reaction`+`mechanism-step` for Reactions — step-note hits collapse onto parent reaction IDs; kind `pathway` for Synthesis — descriptions + step reagents / conditions / notes). Both panel models gained `reload_ids(ids)` helpers that preserve ranked order via one `WHERE id IN (…)` query. Glossary scoped out (its `_TermListModel.reload()` already ILIKEs `definition_md`). 8 new pytest-qt tests (`tests/test_fulltext_filter_toggle.py`) include a "Raney → BHC Ibuprofen" landmark proving step-note-only hits appear only after the toggle. **958 tests pass**. Previous round 94 — housekeeping: **glossary-pollution cleanup**. Purged 165 `Tutor-test-*` glossary rows + 1 molecule row from the user's DB. New `orgchem/db/cleanup.py::purge_tutor_test_pollution()` + `scripts/cleanup_tutor_test_pollution.py` + `tests/conftest.py::pytest_sessionfinish` auto-teardown + 5 regression tests. Phase 31 status unchanged: 31c/d/f/g ✅.

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
19a/c-e are scoped. **694 tests pass + 1 skipped** (round 50).
**Phase 30 shipped end-to-end**: Proteins / Carbohydrates / Lipids /
Nucleic-acids were removed from the main-window tabbar and moved
into a dedicated `MacromoleculesWindow` opened via *Window →
Macromolecules…* (Ctrl+Shift+M). Single persistent instance;
geometry + last-active-tab persist via QSettings. Agent action
`open_macromolecules_window(tab)` added. NA panel's *Fetch PDB*
button now opens/focuses the window's Proteins inner tab rather
than switching the main tabbar. GUI coverage still **100.0 %**
(109 / 109 actions wired). **Phase 31 (content-expansion) — cumulative totals across rounds
44-48**: **+5 reactions** → 35 total (Buchwald-Hartwig, Sonogashira,
Mitsunobu, Swern, HWE); **+18 glossary terms** → 61 (with
`seed_glossary_extra.py` carrying the continued-expansion set);
**+25 carbohydrates** → 25; **+10 lipids** → 31; **+10 nucleic-acid
entries** → 33; **+25 general molecules** → 193 extended
(~380 total in DB with base + intermediates); **+3 energy profiles**
→ 12; **+3 seeded proteins** → 9; **+2 SAR series** → 4 (β-blockers,
ACE inhibitors, each 5 variants); **+2 tutorial lessons** → 21
(beginner acid-base, intermediate sugars); **+2 synthesis
pathways** → 14 (Benzocaine 3-step, Lidocaine 2-step). Plus 19
intermediate-fragment backfills total to keep the fragment-
consistency audit green. Target end-state: 400 molecules, 50 reactions, 20
mechanisms, 25 pathways, 20 energy profiles, 80 glossary terms, 30
tutorials, 40 carbs / 40 lipids / 40 nucleic acids, 15 SAR series,
15 proteins — runs in parallel with future code phases.

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
| Mechanisms seeded                              | **20** (9 classic: SN1/SN2/E1/E2/DA/aldol/Grignard/Wittig/Michael + 4 enzyme: chymotrypsin, aldolase, HIV protease, RNase A + 7 expansion: Fischer ester., NaBH₄, nitration, Claisen, pinacol, **bromination of ethene**, **Friedel-Crafts alkylation**) |
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
