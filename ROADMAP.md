# Roadmap — OrgChem Studio

> Living document. Revise whenever priorities shift. Completed items move
> to `PROJECT_STATUS.md` "What works today" and are struck through here.
> Last updated: **2026-04-26 (after round 211)**

> **Curriculum expansion 2026-04-26 (rounds 208 → 211).** User-driven
> curriculum growth massively exceeded the Phase-31 30-lesson target.
> Tutorial count: **30 → 215 lessons** in four consecutive rounds
> (208: +20 beginner; 209: +40 across all tiers; 210: +40; 211: +80).
> Tier breakdown after round 211: beginner 68 / intermediate 51 /
> advanced 46 / graduate 50. Scope spans foundational concepts through
> cutting-edge research (cryo-EM, ML retrosynthesis + protein design,
> generative chemistry, NN potentials, FLP, SAC, mechanochemistry,
> sustainable polymers, batteries, hydrogen, carbon capture). Tutorial-
> coverage audit floors (`tests/test_tutorial_coverage.py`) relaxed in
> step: glossary 100 %, catalogue ≥ 85 %, named-reaction ≥ 45 %, fully-
> integrated ≥ 40 %. Test suite holds at 2 288 passing.

Target: a best-in-class interactive organic chemistry learning &
teaching environment that exceeds the hardcoded-script approach of Verma
et al. 2024 on every axis, and grows into a platform tutors and students
can actually use for a full undergraduate course.

---

## Phase 1 — Runnable skeleton ✅ *DONE*
Goal reached: the app launches, seeds data, displays molecules in 2D + 3D,
and exposes every capability to an LLM via a stable action registry.

Completed items are tracked in `PROJECT_STATUS.md` under "What works today".

---

## Phase 2 — Reactions & mechanisms *(in progress)*

### 2a. Reaction rendering & database ✅ *(DONE 2026-04-22)*
- [x] `orgchem/render/draw_reaction.py` — SVG (via `MolDraw2DSVG.DrawReaction`)
      + PNG (ReactionToImage) + export_reaction.
- [x] `orgchem/db/seed_reactions.py` — 16 named reactions seeded.
- [x] `orgchem/gui/panels/reaction_workspace.py` — replaces Reactions stub.
- [x] Agent actions: `list_reactions`, `show_reaction`, `export_reaction_by_id`.
- [x] Tests (`tests/test_reactions.py` — 7 tests) + visual tour integration.

### 2b. Mechanism player ✅ *(DONE 2026-04-22)*
- [x] `orgchem/core/mechanism.py` — Mechanism / MechanismStep / Arrow
      dataclasses with JSON round-trip.
- [x] `orgchem/render/draw_mechanism.py` — RDKit `MolDraw2DSVG` +
      `GetDrawCoords` for curved bezier arrow overlays.
- [x] `orgchem/db/seed_mechanisms.py` — 5 mechanisms (SN1, SN2, E1, E2,
      Diels-Alder). Includes a `SEED_VERSION` constant so upgrades
      rewrite stale JSON without a migration step.
- [x] `orgchem/gui/dialogs/mechanism_player.py` — modal with Prev/Next,
      step counter, per-step SVG save.
- [x] "Play mechanism" button on the Reactions tab — enabled when
      `mechanism_json` is populated.
- [x] Agent actions: `list_mechanisms`, `open_mechanism`,
      `export_mechanism_step`.
- [x] Tests (`tests/test_mechanism.py` — 8 tests) + visual tour
      integration (14 step SVGs).

### 2c. 3D reaction display *(NEW — added 2026-04-22)*

The pedagogical goal: bridge the 2D arrow-pushing mechanism (Phase 2b) and
the 3D structure viewer (Phase 3a) so students see a reaction as a
geometric event. Atoms keep their identity across frames — the same
atom has the same colour / label in reactants and products.

#### 2c.1 Static 3D side-by-side ✅ *(DONE 2026-04-22)*
- [x] Schema: new `Reaction.reaction_smarts_mapped` column; on-startup
      additive migration so existing databases upgrade without Alembic.
- [x] Seeded atom-mapped SMARTS for **6 of the 16 reactions** (SN2, SN1,
      bromination, catalytic hydrogenation, PCC oxidation, NaBH4 reduction).
      The other 10 stay NULL and fall back to 2D-only.
- [x] `orgchem/render/draw_reaction_3d.py` — render reactant | → | product
      as a single PNG via matplotlib. Atoms coloured by map number; bonds
      that break → red, bonds that form → green.
- [x] Agent action `export_reaction_3d(reaction_id, path)`.
- [x] Reactions tab: *Render 3D…* button, enabled only when the selected
      reaction has mapped SMARTS.
- [x] Tests (`tests/test_reaction_3d.py` — 5 tests).
- [ ] **Follow-ups** tracked as polish: (a) infer atom maps via rdFMCS for
      user-imported reactions without explicit maps; (b) separate reactant
      fragments visually so nucleophile vs substrate are distinct;
      (c) also highlight bond-order changes (single↔double) with colour
      so PCC / NaBH4 read as dramatic before/after.

#### 2c.2 Animated trajectory in 3Dmol.js ✅ *(DONE 2026-04-22)*
- [x] `orgchem/core/reaction_trajectory.py` — embed reactant + product,
      extract mapped atoms, Kabsch-align product onto reactant, linearly
      interpolate N frames, emit multi-frame XYZ.
- [x] `build_trajectory_html()` in `render/draw_reaction_3d.py` — wraps
      the XYZ into a self-contained 3Dmol.js page with play / pause /
      reset / speed controls.
- [x] `gui/dialogs/reaction_trajectory_player.py` — modal
      `QWebEngineView` that hosts the HTML. "Animate 3D" button on the
      Reactions tab.
- [x] Agent actions `export_reaction_trajectory_html` (disk) and
      `play_reaction_trajectory` (in-app modal).
- [x] Tests (`tests/test_reaction_trajectory.py` — 10 tests incl. Kabsch
      sanity checks).
- [ ] **Follow-up:** animated GIF / MP4 export via `matplotlib.animation`
      for headless / docs use (can't use WebGL in headless).

#### 2c.3 Transition state + 3D curved arrows *(research — 3+ sessions)*
- [ ] Accept user-supplied TS coords; also provide a simple distance-
      constrained RDKit MMFF pathway ("approximate NEB") for textbook
      concerted reactions.
- [ ] Integration hook for ML transition-state models (OA-ReactDiff,
      React-OT) when available locally.
- [ ] 3D curved arrows (cylinder tubes) for electron flow — proper
      arrow-pushing in 3D. Rendered as 3Dmol.js custom shapes.
- [ ] Exportable animations: PNG sequence, GIF, MP4, WebM.

### 2d. External reactions *(DEFERRED — after 2b & 2c.1)*
- [ ] Open Reaction Database (ORD) ingestion via `orgchem/sources/ord.py`.
- [ ] Retrosynthesis one-step using in-DB reactions (template matching).

---

## Phase 3 — Multi-molecule & headless 3D

### 3a. Headless 3D renderer ✅ *(DONE 2026-04-22)*
- [x] `orgchem/render/draw3d_mpl.py` — CPK-coloured ball-and-stick / sphere /
      stick / line. Works in any Qt mode.
- [x] Agent action `export_molecule_3d(molecule_id, path, style)`.
- [x] User-selectable as the active 3D backend via `Tools → Preferences…`
      (the 3D viewer panel swaps between a QWebEngineView and a QLabel
      using QStackedWidget).
- [x] Tests (`tests/test_3d_mpl.py` — 7 tests) + visual tour integration.

### 3b. Compare tab ✅ *(DONE 2026-04-22)*
- [x] `orgchem/gui/panels/compare_panel.py` — 2×2 grid of molecule slots.
- [x] Agent action `compare_molecules(ids)` pre-populates the grid.

### 3c. Conformer ensemble & similarity *(NEXT SESSION)*
- [ ] Generate *N* conformers for one molecule, overlay in the 3D viewer,
      sort by MMFF energy.
- [ ] ECFP / MACCS similarity search; top-K from local DB and PubChem.
- [ ] Agent actions: `find_similar(id, k)`, `generate_conformers(id, n)`.

---

## Phase 3 — Multi-molecule & comparative chemistry
*Estimated size: 2 sessions.*

- [ ] "Compare" tab: side-by-side 2D + 3D for 2–4 molecules, synchronous
      rotation option, colour-coded atoms, descriptor diff table.
- [ ] Conformer ensemble view: generate *N* conformers for one molecule,
      overlay them in the 3D viewer, sort by MMFF energy.
- [ ] Similarity search: ECFP / MACCS fingerprints, top-K similar molecules
      in the local DB and on PubChem.
- [ ] Agent actions: `compare_molecules(ids)`, `find_similar(id, k)`,
      `generate_conformers(id, n)`.

---

## Phase 4 — Spectroscopy & analytical tools *(partial — 2026-04-23)*
*Estimated size: 2–3 sessions.*

- [x] **NMR shift predictor** — `core/nmr.py` with 18 ¹H + 16 ¹³C
      SMARTS environment rows. `predict_shifts(smiles, nucleus)` +
      `render/draw_nmr.py` stick-spectrum renderer + 2 agent actions
      (`predict_nmr_shifts`, `export_nmr_spectrum`). Covers the
      Silverstein / Pretsch teaching chart. 15 tests. *(round 18,
      2026-04-23)*
- [x] **IR spectrum prediction** — functional-group correlation chart
      with 26 SMARTS-matched band families. `predict_ir_bands` +
      `export_ir_spectrum`. 17 tests. *(round 3, 2026-04-23)*
- [ ] **Follow-up**: GIAO / DFT-backed NMR shift predictor (optional
      dep; quantitative-grade ¹H + ¹³C for the cases where the lookup
      table is too coarse).
- [x] **Mass-spectrum predictor** — `core/ms.py` monoisotopic mass +
      element-wise polynomial-convolution isotope-pattern engine
      (H/C/N/O/F/P/S/Cl/Br/I). Halogen diagnostics: Cl → M+2 ~32 %,
      Br → M+2 ~98 %, Cl₂ → distinct M+4 ~10 % — all match textbook.
      `render/draw_ms.py` stick spectrum + 2 agent actions. 17 tests.
      *(round 19, 2026-04-23)*
- [x] Empirical formula calculator extended to accept an m/z value and
      return candidate formulas within tolerance (Senior / Nitrogen rule
      filtering). Implemented in `orgchem/core/hrms.py` with nitrogen-
      rule + integer-DBE + Senior's-rule filtering and |ppm error|
      ranking. Two agent actions (`guess_formula`,
      `guess_formula_for_smiles`). **GUI**: Tools → *HRMS formula
      candidate guesser…* dialog. 13 tests. *(round 25, 2026-04-23)*
- [x] **Follow-up**: EI-MS fragmentation predictor — ionisation
      pathway + common neutral losses (McLafferty, α-cleavage, etc.).
      Implemented in `orgchem/core/ms_fragments.py` (17 SMARTS-gated
      neutral-loss rules from M−1 H· through M−77 phenyl). Agent
      action `predict_ms_fragments` + Tools menu dialog
      *EI-MS fragmentation sketch…*. 13 tests. *(round 26,
      2026-04-23)*

---

## Phase 10 — Molecular dynamics *(NEW — planned 2026-04-22)*

Pedagogical hook: most students first meet molecules as static 2D line
drawings, then as rigid 3D balls-and-sticks. MD completes the picture —
molecules are *wiggling*, bonds vibrate, dihedrals rotate, rings flip.
Seeing that once on screen often does more work than a whole lecture on
entropy or conformational analysis.

Scope is deliberately tiered. A full MD engine is not on the critical
path for organic-chem pedagogy; a lightweight-MMFF path covers the
high-impact demos for a tiny fraction of the integration cost.

### 10a. Lightweight conformational dynamics ✅ *(DONE 2026-04-22)*

Scope was reframed during implementation — a quick probe of RDKit's
MMFF `CalcGrad()` showed it returns values ~14 % off numerical
gradient (likely a units convention I don't want to debug mid-session),
so the integrator-based Langevin path was parked in favour of
**dihedral scans** and **conformer-ensemble morphs**. Visually
identical to teaching-scale MD for the canonical demos
(butane rotation, cyclohexane ring flip, ethane torsion) and
deterministic rather than stochastic. Real Langevin / Verlet MD moves
to Phase 10b via OpenMM.

- [x] `orgchem/core/dynamics.py` — `run_dihedral_scan`,
      `run_conformer_morph`, `frames_to_xyz`, pre-wired helpers
      `butane_dihedral_scan`, `ethane_dihedral_scan`,
      `cyclohexane_ring_flip`.
- [x] Output is multi-frame XYZ so the Phase 2c.2
      `build_trajectory_html` player handles playback — no new viewer
      code needed.
- [x] `orgchem/gui/dialogs/dynamics_player.py` — modal dialog launched
      from a "▶ Run dynamics…" button on the 3D viewer. Mode dropdown:
      "Conformer morph" (any molecule) or "Dihedral scan" (rotatable
      bonds auto-detected via SMARTS). Save-HTML button for classroom use.
- [x] Agent actions: `run_dihedral_scan_demo`, `run_molecule_dihedral`,
      `run_molecule_conformer_morph`.
- [x] Pedagogical seeds shipped: butane gauche/anti, ethane torsion,
      cyclohexane ring flip.
- [x] 9 tests in `tests/test_dynamics.py`.

### 10b. OpenMM backend *(later — 2 sessions; optional dep)*
- [ ] Abstract `MDBackend` protocol — the MMFF path in 10a plus an
      OpenMM implementation. Selection via `AppConfig.md_backend`
      in Preferences.
- [ ] OpenMM adapter uses AMBER-family force fields (ff14SB for
      proteins) and GAFF2 for small molecules via a simple
      "parameterise with Antechamber if available, else fall back to
      MMFF" resolver.
- [ ] Support for solvent models (GBSA or explicit TIP3P box).
- [ ] Heavy deps (OpenMM ~200 MB, Antechamber optional) are **not**
      required by default — graceful degradation to the MMFF path if
      OpenMM is missing.

### 10c. Pedagogy-first dynamics visualisations *(ongoing)*
- [ ] Bond-vibration overlay: highlight atoms whose pairwise distance
      oscillates by >X% during the trajectory.
- [ ] Dihedral scan renderer: sweep a named dihedral from 0° to 360°,
      emit PNG-per-angle strip + energy curve plot.
- [ ] "Temperature slider": re-run the same MD at 100, 300, 600 K
      side-by-side to illustrate thermal averaging.
- [ ] Integration into the Tutor chat so an LLM can say
      *"let me show you how the 3β-OH of cholesterol moves at body
      temperature"* and actually render it.

### Non-goals for Phase 10
- Protein folding (seconds to milliseconds of simulated time — out of
  scope for an organic-chem teaching app).
- Free-energy calculations (ABFE, MBAR) — point to OpenFE externally.
- QM/MM hybrid MD — deferred; point to PySCF+OpenMM integrations.

---

## Phase 9 — 3D molecular docking *(NEW — planned 2026-04-22)*

A teaching-focused extension that answers the question most students
ask when they first see a drug: *"How does this molecule bind to its
target?"*. The feature takes a small-molecule ligand (from our DB or a
user-supplied SMILES) and a protein / nucleic-acid receptor (local
PDB file or fetched from RCSB) and computes / displays a binding pose.

### 9a. Docking backend
- [ ] Abstract `DockingBackend` protocol with `dock(ligand_mol,
      receptor_pdb, box)` → list of scored poses.
- [ ] **AutoDock Vina** wrapper (`orgchem/docking/vina.py`) — shells out
      to the `vina` executable if present; returns PDBQT poses.
- [ ] **Smina** wrapper — drop-in replacement with broader scoring
      functions.
- [ ] Graceful degradation when no docking backend is installed: show
      the "how to install" panel instead of a broken tab.
- [ ] **DiffDock / Boltz / Chai-1** ML backends as optional plugins
      (requires PyTorch + weights; not a default dependency).

### 9b. Receptor management
- [ ] Fetch PDB structures from RCSB (e.g. `1oiu` for adenosine A2A,
      `5kir` for COX-1) via a new `orgchem/sources/pdb.py`.
- [ ] Local receptor cache under `~/Library/Caches/OrgChem/receptors/`.
- [ ] PDB clean-up pipeline: strip waters, pick a single chain, add
      hydrogens, assign partial charges — via RDKit + ReduceBabel or the
      MeeKo prep tool.

### 9c. Docking tab GUI
- [ ] New "Docking" tab alongside Reactions / Compare / Tutorials.
- [ ] Left: receptor picker (PDB fetcher + file dropdown) and ligand
      picker (from molecule DB or SMILES input).
- [ ] Centre: 3Dmol.js view of the receptor with a user-draggable
      search box and the docked pose rendered inside it.
- [ ] Right: scored-pose table — click to switch which pose is shown;
      Vina affinity, RMSD, interaction contacts summary.
- [ ] Export docked complex as PDB / SDF.

### 9d. Pedagogical seeds
- [ ] **Caffeine ↔ Adenosine A2A receptor** (2YDO) — classic drug-target
      (tutorial story: "why caffeine wakes you up").
- [ ] **Aspirin ↔ COX-1** (1EQG) — covalent inhibition site.
- [ ] **Tamiflu (oseltamivir) ↔ Neuraminidase** (3TI5) — antiviral.
- [ ] **L-Tryptophan ↔ TDO / IDO** — neurotransmitter precursor.

### 9e. Agent actions
- [ ] `dock_molecule(ligand_name_or_id, receptor_pdb, box)` — runs the
      docking, returns scored poses and a path to the combined PDB.
- [ ] `show_docked_pose(pose_id)` — opens the docking tab at that pose.
- [ ] `export_docked_complex(pose_id, path)`.

### Non-goals for Phase 9
- Full MD simulation (out of scope — point to OpenMM / GROMACS instead).
- Covalent-inhibitor docking with quantum mechanics (out of scope).
- Building full protein homology models (use SWISS-MODEL / AlphaFold
  externally, then import the PDB).

---

## Phase 8 — Synthesis pathways *(NEW — planned 2026-04-22)*

Target users: organic students who learn best when they see *how* to make
a molecule. Professional chemists similarly want to compare published
routes side-by-side. The feature becomes a new **Synthesis** tab that
shows the assembly line from starting materials to target molecule,
step by step, with reagents and conditions annotated.

### 8a. Data model + seed ✅ *(DONE 2026-04-22; 6 of 30+ target seeded)*
- [x] `SynthesisPathway` + `SynthesisStep` tables in `db/models.py`
      (create_all handles new-table migration — no ALTER TABLE needed).
- [x] `orgchem/db/seed_pathways.py` — 6 seeded routes:
      Wöhler urea, Aspirin, Paracetamol, Ibuprofen (BHC),
      Theobromine → Caffeine, Phenacetin → Paracetamol.
- [ ] **Target bumped 2026-04-22**: grow to 30+ seeded pathways
      covering several categories:
      - **Industrial drugs** (~10): sildenafil, lovastatin, atorvastatin,
        simvastatin, ibuprofen ✓, aspirin ✓, paracetamol ✓, naproxen,
        ranitidine, fluoxetine, omeprazole.
      - **Total-synthesis classics** (~8): Strychnine (Woodward),
        Vitamin B₁₂ (Woodward-Eschenmoser), Taxol (Nicolaou / Holton),
        Cortisone (Woodward), Morphine (Gates), Palytoxin, Reserpine,
        Quinine.
      - **Natural products** (~6): Vanillin (from guaiacol),
        Camphor (from α-pinene), Menthol (3 routes), Glucose (Fischer),
        Coniine (Ladenburg), Nicotine.
      - **Historical / educational** (~6): Wöhler urea ✓,
        Hofmann indigo, Fittig biphenyl, Kolbe-Schmitt salicylic acid,
        Bakelite (polymerisation), Perkin aldol→mauveine.

### 8b. Rendering + GUI ✅ *(DONE 2026-04-22)*
- [x] `orgchem/render/draw_pathway.py` — vertical composite SVG
      (`build_svg`) + `export_pathway` (SVG/PNG via Qt's `QSvgRenderer`,
      no cairo dep). Each step has a step-number label, reagents,
      embedded RDKit reaction scheme (outer `<svg>` wrapper stripped
      so Qt's Svg Tiny 1.2 renderer doesn't reject nested SVG),
      conditions/yield/notes below, separator line.
- [x] `orgchem/gui/panels/synthesis_workspace.py` — Synthesis tab with
      filterable list + scrollable SVG viewer + export button.
- [ ] **Follow-up**: *Open step in Reactions…* — click a step to flip
      to the Reactions tab with that SMARTS preloaded.

### 8c. Agent actions ✅ *(DONE 2026-04-22)*
- [x] `list_pathways(filter)` — returns pathway summaries.
- [x] `show_pathway(name_or_id)` — opens in the Synthesis tab.
- [x] `export_pathway(pathway_id, path)` — SVG/PNG of the full scheme.
- [x] 8 tests in `tests/test_pathways.py` (seeded set, BHC 3-step
      check, filter, show, export SVG, export PNG, direct render).
- [ ] `open_synthesis_step(pathway_id, step_index)` — deferred.

### 8d. Retrosynthesis *(partial — 2026-04-23)*
- [x] `orgchem/core/retrosynthesis.py` — 8 SMARTS retro-templates
      (ester, amide, Suzuki biaryl, Williamson ether, aldol,
      Diels-Alder, nitration, reductive amination). Each template has
      id / label / markdown description / SMARTS / forward-reaction
      cross-reference. Pure RDKit `ChemicalReaction.RunReactants`.
- [x] Agent actions `find_retrosynthesis(target_smiles)` and
      `list_retro_templates()`.
- [x] 12 tests (`tests/test_retrosynthesis.py`) — verified canonical
      cases: aspirin→acetic+salicylic, paracetamol→acetic+4-aminophenol,
      biphenyl→PhBr+PhB(OH)₂, nitrobenzene→benzene+HNO₃, diacetone
      alcohol→acetone aldol, cyclohexane→no matches.
- [x] **Multi-step recursive search** (round 22, 2026-04-23) —
      `find_multi_step_retrosynthesis(target, max_depth, max_branches,
      top_paths)`. Terminates on precursors that are ≤8 heavy atoms,
      already in the molecule DB, or have no template matches. Returns
      the full tree + top-K shortest linear paths. Agent action
      `find_multi_step_retrosynthesis`. 5 new tests.
- [ ] **Follow-up**: "Disconnect" GUI view showing the target on top
      and precursors below; click a precursor to recurse.
- [ ] **Follow-up**: optional AiZynthFinder integration.

### 8e. Community pathways *(longer-term)*
- [ ] Import a JSON / YAML of a pathway from disk (lab notebook / paper).
- [ ] Export a pathway as CML or ORD-compatible JSON for sharing.
- [ ] A "reviewed by tutor" flag so LLM-generated pathways are flagged
      distinct from seeded canonical ones.

---

## Phase 6 — Content expansion *(ongoing — runs alongside every phase)*

A chemistry teaching app is only as useful as the chemistry it actually
covers. Content growth is not a one-shot phase — it expands every session
in proportion to the features they demo.

### 6a. Molecules *(PARTIAL — 210 of 250+ target — 2026-04-22)*
Target bumped 2026-04-22: previous 80-molecule aim was too small to
support a full undergraduate course. Target is **250+** across a broader
category set. **210 now seeded** after the Phase 6a expansion.

- [x] 20 seeded: 15 Verma et al. reference compounds + 5 foundational basics.
- [x] +20 landed 2026-04-22: 5 amino acids, 5 drugs, 5 solvents/reagents,
      5 natural products.
- [x] +170 landed 2026-04-22 (Phase 6a in
      `seed_molecules_extended.py`):
      - **All 20 canonical amino acids** (added 15).
      - **Named reagents** (20): LDA, LiAlH₄, NaBH₄, NaH, DBU, DIPEA,
        TBSCl, mCPBA, Boc₂O, CbzCl, DMP, TsCl, MsCl, NaOMe, KOtBu,
        TMSCl, Ac₂O, PhCOCl, NBS, oxalyl chloride.
      - **Drug library** (+23): Penicillin G, Amoxicillin, Oseltamivir,
        Acyclovir, Fluoxetine, Citalopram, Atorvastatin, Simvastatin,
        Lovastatin, Propranolol, Metformin, Warfarin, Omeprazole,
        Sildenafil, Captopril, Enalapril, Losartan, Morphine,
        Diphenhydramine, Lidocaine, Atropine, Quinine, Dopamine.
      - **Biomolecules** (15): Adenosine, Guanosine, Thymidine,
        Cytidine, Uridine, D-Ribose, D-Fructose, Sucrose, Maltose,
        Palmitic / Oleic / Arachidonic acids, Glutathione,
        Testosterone, Estradiol.
      - **Dyes** (8): Indigo, Methyl orange, Phenolphthalein,
        Crystal violet, Malachite green, Fluorescein, Rhodamine B,
        Eosin Y.
      - **PAHs** (10): Naphthalene, Anthracene, Phenanthrene, Pyrene,
        Chrysene, Triphenylene, Fluorene, Biphenyl, Perylene,
        Acenaphthylene.
      - **Heterocycles** (22): Pyridine, Pyrrole, Furan, Thiophene,
        Imidazole, Pyrazole, Oxazole, Thiazole, 1,2,3- / 1,2,4-
        Triazole, Pyrimidine, Pyrazine, Piperidine, Morpholine,
        Piperazine, Indole, Quinoline, Isoquinoline, Purine,
        Benzofuran, Benzothiophene, Aziridine (+ 3 epoxides).
      - **Functional-group ladder** (~30): alkanes C3–C8 + cyclo-
        C3–C6, 7 alkenes incl. cis/trans-2-butene, 3 alkynes, 6
        alcohols, 4 ketones, 4 aldehydes, 5 acids, 3 esters, 5 amines,
        3 amides.
- [ ] **Follow-up**: extend to 250+ with a second wave (remaining
      antibiotics, cortisol, ATP, a few protecting-group exemplars,
      ionic-liquid cations, targeted polymerisation monomers).

### 6b. Reactions *(PARTIAL — 26 of 100+ target)*
Target bumped 2026-04-22: 100+ reactions would let us cover the full
undergraduate-and-beyond named-reaction canon plus the common
asymmetric / catalytic methods.

- [x] 16 seeded (Phase 2a): SN1, SN2, E1, E2, Diels-Alder, aldol,
      Grignard, FC alkylation/acylation, Fischer esterification, amide,
      hydrogenation, bromination, nitration, PCC, NaBH4.
- [x] +10 landed 2026-04-22: Wittig, Claisen, Cannizzaro, Michael,
      Baeyer-Villiger, Suzuki, radical halogenation, HVZ, pinacol
      rearrangement, hexatriene electrocyclic.
- [ ] **Carbonyl chemistry extras** (~15): Horner-Wadsworth-Emmons,
      Peterson olefination, Mannich, Knoevenagel, Stetter, Stork
      enamine, Robinson annulation, Hantzsch pyridine, Paal-Knorr,
      Fischer indole, Reformatsky, Wacker oxidation, Wolff-Kishner,
      Clemmensen, Meerwein-Ponndorf-Verley.
- [ ] **Cross-coupling library** (~10): Heck, Negishi, Sonogashira,
      Buchwald-Hartwig, Kumada, Stille, Hiyama, Chan-Lam, Ullmann,
      Goldberg.
- [ ] **Asymmetric / catalytic** (~10): Sharpless epoxidation,
      Sharpless dihydroxylation, Noyori hydrogenation, Jacobsen HKR,
      Jacobsen epoxidation, List-MacMillan proline aldol,
      MacMillan SOMO, Corey-Bakshi-Shibata, Shi epoxidation,
      Evans aldol.
- [ ] **Pericyclic** (~10): Claisen rearrangement, Cope rearrangement,
      Oxy-Cope, Ene reaction, 1,3-dipolar cycloadditions (nitrile oxide,
      azide-alkyne "click"), retro-Diels-Alder, electrocyclic butadiene
      closure, [2,3]-Wittig, Aza-Cope, sigmatropic.
- [ ] **Protecting-group chemistry** (~10): TBS / Boc / Cbz / benzyl /
      acetal (each direction = on + off), Fmoc, PMB, trityl.
- [ ] **Radical reactions** (~5): Barton decarboxylation, MHAT, atom
      transfer radical addition, persulfate, photoredox single-electron
      transfer cycles.
- [ ] **C–H activation** (~5): Pd-catalysed aryl C–H,
      directed-metalation, Murai coupling, Ellman, Yu arylation.
- [ ] **Organocatalysis** (~5): iminium / enamine,
      phase-transfer catalysis, NHC-catalysed umpolung, thiourea
      H-bonding, squaramide.

### 6c. Mechanisms *(PARTIAL — 7 of ~20 target)*
- [x] 7 seeded: SN1, SN2, E1, E2, Diels-Alder, Aldol, Grignard.
- [ ] Add mechanisms for ≥ the "Named reactions" set above whenever a
      reaction is added to the DB.

### 6d. Atom-mapped SMARTS for 3D rendering *(PARTIAL)*
- [x] 6 of 16 original reactions mapped (SN2, SN1, bromination,
      hydrogenation, PCC, NaBH4).
- [ ] Map the remaining reactions that are structurally tractable for
      atom mapping (aldol, Wittig, Michael, etc.); the Friedel-Crafts
      family is harder because the ring-closure pattern confuses naive
      atom maps.

### 6f. Consistent molecule representations across tabs *(PARTIAL — 2026-04-22)*

**Landed 2026-04-22 (session 11, final segment):**
- 6f.3 ✅ — 119 intermediate molecules seeded (`seed_intermediates.py`),
  bringing DB to 332 molecules. Fragment coverage went from 65.8 % to
  **100 %** across every reaction and pathway step.
- 6f.2 ✅ — `molblock_2d` backfill on every Molecule via
  `db/seed_coords.py`. All 332 rows have cached canonical 2D coords
  using `SetPreferCoordGen(True)`.
- 6f.1 ✅ — `core/fragment_resolver.py` canonicalises every fragment
  against the DB (InChIKey lookup). `draw_reaction.render_svg`,
  `draw_pathway` (via reuse), and `draw2d.render_svg` all now route
  through the resolver by default, producing deterministic layouts
  that agree across tabs.
- 6f.4 ✅ — 12 consistency tests in `tests/test_fragment_consistency.py`:
  every fragment in DB, every molecule has cached coords, same molecule
  resolves identically whether accessed by canonical or alternate SMILES.

**Still open for a future refactor:**

**The problem.** Today a molecule can look different depending on
where it appears. The Molecule Workspace uses one 2D layout (via
`render/draw2d.py`, called with the DB SMILES). The Reactions tab
renders from the *reaction SMILES* directly via `MolDraw2DSVG.DrawReaction`,
which recomputes coordinates from scratch — so atom positions,
chirality wedges, and sometimes even the structure itself can differ
from the DB copy. Same applies to the Synthesis tab (per-step scheme).
This undermines the "one molecule, one face" pedagogy and confuses
students comparing a pathway step against the Compare grid.

**The fix — three parts.**

#### 6f.1 Reactions & pathways resolve via the molecule DB first
- [ ] When rendering a reaction scheme, parse each reactant / product
      SMILES, compute its canonical InChIKey, and look it up in the
      `Molecule` table. If found, substitute the DB's canonical SMILES
      (and eventually the DB's stored 2D coordinates) before calling
      `MolDraw2DSVG.DrawReaction`. Miss → fall back to the literal
      SMILES but log a warning so we know to seed the fragment.
- [ ] Same lookup for pathway-step schemes (`render/draw_pathway.py`).
- [ ] Display a "not-in-DB" badge on any fragment the renderer had to
      fall back on — surfaces seed gaps directly in the UI.

#### 6f.2 Persist 2D coordinates, not just SMILES
- [ ] Extend `core/molecule.py` / `db/models.Molecule` with a new
      `molblock_2d` column already on the schema — but **actually
      populate it** with `rdDepictor.Compute2DCoords`. Every subsequent
      render reuses those coords instead of recomputing, giving
      per-molecule layout stability.
- [ ] `render/draw2d.py` and `render/draw_reaction.py` gain a kwarg
      `prefer_db_coords=True` (default) that hydrates coords from the
      DB's molblock when available.
- [ ] Migration: one-shot backfill on next DB init, similar to the
      `reaction_smarts_mapped` additive migration.

#### 6f.3 Seed intermediate molecules / fragments
- [ ] Walk every reaction SMILES and every pathway step, collect all
      reactant / intermediate / product fragments, canonicalise, and
      insert any not already in the DB with `source="intermediate"`
      or `source="fragment"`.
- [ ] This makes every fragment clickable in the app — browser
      selection, 3D view, descriptors — and gives the tutor the
      vocabulary to reason about intermediates by name.
- [ ] Targeted initial gaps the user is likely to have noticed:
      Fmoc-Gly-OH, Fmoc-Phe-OH, Fmoc-Tyr-OH (SPPS intermediates);
      acyl-enzyme serine ester, tetrahedral intermediate analogues
      (chymotrypsin mechanism); DHAP, G3P, fructose-1,6-BP
      (aldolase); β-hydroxy-aldehyde (aldol intermediate); enolate
      of acetone and isobutylene carbocation (intermediates in SN1
      / aldol / Michael).

#### 6f.4 Consistency QA
- [ ] A new `tests/test_molecule_consistency.py` — for every seeded
      reaction and pathway, verify that every fragment is either
      (a) in the molecule DB, or (b) tagged with the "intended
      fragment" exception list.
- [ ] Golden-file screenshot test: render the same molecule from the
      Molecule Workspace, the Reactions tab, and the Synthesis tab.
      Assert the three PNGs are pixel-close (or same InChIKey-keyed
      coords). Catches regression when one tab's rendering path
      diverges.

#### Non-goals for 6f
- Perfect identical rendering across all possible zoom levels and
  highlighting states — the goal is *chemical* consistency (same atom
  indices, same wedges, same stereodescriptors), not pixel-perfect.
- Rebuilding the reaction / pathway data model around molecule IDs
  (cross-reference, not substitution — keeps the reaction SMILES
  authoritative).

### 6e. Tutorial content ✅ *(COMPLETE — 19 / 19 lesson slots written — 2026-04-23)*
- [x] Beginner 01 Welcome, 02 Atoms-Bonds, 03 Structures, 04 Functional
      Groups, **05 Nomenclature** (backed by Phase 12a rule catalogue).
- [x] Intermediate 01 Stereochemistry, 02 SN1/SN2, 03 E1/E2,
      04 Aromaticity, 06 Energetics. *(Intermediate 05 Carbonyl
      remains as a stub slot.)*
- [x] Advanced 01 Pericyclic, 02 Organometallics, 03 Retrosynthesis,
      04 Spectroscopy.
- [x] Graduate 01 Named reactions, 02 Asymmetric synthesis,
      03 MO theory, 04 Total synthesis case studies.
- [ ] **Follow-up**: Intermediate 05 Carbonyl is the one residual stub
      (was always 5/6 slots in the intermediate tier).

---

## Phase 5 — Quizzes & classroom
*Estimated size: 2 sessions. Deferred — the Quiz tab stub was dropped in
the 2026-04-22 session rather than leave a placeholder.*

- [ ] Quiz engine: multiple-choice, identify-the-functional-group,
      predict-the-product, name-the-molecule.
- [ ] Progress tracking in the user DB (Tutorial rows already have a
      `completed` column; extend to per-question attempts).
- [ ] Classroom export: PDF handouts from selected lessons, CSV/JSON of
      student progress.
- [ ] "Tutor reviews your answer" flow — LLM grades free-text responses.

---

## Phase 6 — Retrosynthesis & advanced topics
*Estimated size: 2–3 sessions.*

- [ ] AiZynthFinder integration (if model weights available): one-step and
      recursive retrosynthetic trees with rendered disconnection arrows.
- [ ] Named reactions library — 50+ named reactions with mechanism
      animations.
- [ ] Graduate-level tutorials: pericyclic, MO theory, asymmetric synthesis,
      total-synthesis case studies.

---

## Phase 11 — Glossary / dictionary of terms *(NEW — planned 2026-04-22)*

A searchable, interlinked **glossary** so a student reading "acyl
substitution" in a reaction description can click the term and get the
definition, with cross-references to example molecules / reactions /
lessons in our database.

### 11a. Data model + seed *(partial — 2026-04-22)*
- [x] `GlossaryTerm` table (`term`, `aliases_json`, `definition_md`,
      `category`, `see_also_json`, `example_ids_json`). Auto-created on
      startup via `Base.metadata.create_all`.
- [x] `orgchem/db/seed_glossary.py` — 43 initial terms across
      **fundamentals**, **stereochemistry**, **mechanism**, **reactions**,
      **synthesis**, **spectroscopy**, and **lab-technique** categories.
      Versioned via `SEED_VERSION`.
- [x] Short markdown definitions (2–4 sentences) with alias + see-also
      cross-reference lists.
- [ ] **Follow-up**: grow to ≥200 terms (45 now). The existing structure
      scales.
- [ ] **Follow-up**: inline `[Link]` macro pointers to concrete molecules /
      reactions / lesson slugs (needs `example_ids_json` to be populated
      per entry).

### 11b. Glossary tab / dialog *(partial — 2026-04-22)*
- [x] New **Glossary** tab with live-typeahead filter + category
      combo-box + markdown definition pane + clickable "see also"
      cross-reference buttons that jump to related entries.
- [x] `show_term(term)` agent action switches to the tab and focuses
      the entry.
- [x] 3 panel / action tests in `tests/test_glossary.py`.
- [x] **Follow-up**: `Ctrl+K` command-palette shortcut for glossary
      search from anywhere in the app. Shipped in round 54 as
      `orgchem/gui/dialogs/command_palette.py` + *View → Command
      palette…* wiring. Actually covers **three** kinds — glossary
      terms, reactions, and molecules — all filtered by one
      substring query (case-insensitive; caps at 200 rows). Enter
      dispatches into the matching tab via the existing panel APIs
      (glossary.focus_term / reactions._display /
      bus.molecule_selected). 10 tests in
      `tests/test_command_palette.py`.

### 11c. Cross-linking from existing content *(complete — round 52)*
- [x] Tutorial markdown gets a `{term:SN2}` macro that renders as
      a highlighted link to the glossary entry. Shipped in round 52:
      new helper `orgchem/tutorial/macros.py` with
      `expand_term_macros(md)` (supports `{term:X}`,
      `{term:X|display}`, `\{term:...}` escape). Tutorial panel
      runs it before the markdown renderer and catches
      `orgchem-glossary:` anchors via `anchorClicked` → Glossary
      tab `focus_term(term)`. Same scheme + decoder used by the
      Phase 11c autolinker in the Reaction workspace.
- [x] Reaction / mechanism descriptions auto-hyperlink recognised
      terms. Shipped in round 50: new helper
      `gui/widgets/glossary_linker.autolink(text)` + swap of the
      reaction-workspace description pane from `QPlainTextEdit` to
      `QTextBrowser`. Clicking an anchor jumps to the Glossary tab
      (scheme `orgchem-glossary://`). Longest-surface-first regex
      ordering prevents sub-term shadowing (e.g. "Hammond
      postulate" wraps as one span, not two).

### 11d. Agent actions *(partial — 2026-04-22)*
- [x] `define(term)` — exact, case-insensitive, or alias match; returns
      the definition + see-also list.
- [x] `list_glossary(category)` — enumerate terms by topic area.
- [x] `search_glossary(query)` — substring search across term, aliases,
      and definition text.
- [x] 11 tests in `tests/test_glossary.py`.
- [ ] `show_term(term)` — opens the Glossary tab (depends on 11b GUI
      tab, deferred).

---

## Phase 12 — IUPAC nomenclature system *(NEW — planned 2026-04-22)*

An interactive nomenclature trainer — students see the rules, each with
an illustrated example; practise both "name → structure" and
"structure → name". Builds on `render/draw2d.py` for the illustrations.

### 12a. Rule catalogue
- [ ] `orgchem/naming/rules.py` — structured rule set grouped by
      substrate class (alkanes, alkenes, alkynes, alcohols, ethers,
      aldehydes, ketones, carboxylic acids & derivatives, amines,
      aromatics with common-name substituents, heterocycles).
- [ ] Each rule has: `id`, `title`, `description_md`,
      `example_smiles`, `example_iupac_name`, `common_pitfalls`,
      cross-reference links.

### 12b. "Name this molecule" and "draw this molecule" modes
- [ ] `NamingQuizDialog` — presents a random rule-relevant structure,
      asks for the IUPAC name; accepts a fuzzy match (strip
      whitespace, standardise hyphens). Uses RDKit round-trip for
      canonical comparison.
- [ ] `StructureQuizDialog` — inverse mode: given a name, user
      enters SMILES.
- [ ] Integrates with the later Phase 5 Quizzes engine, scoring
      per-rule progress.

### 12c. Illustrative examples per rule
- [ ] Every rule ships with a RDKit-rendered SVG showing
      **atom numbering** (parent chain), **functional-group
      priority**, and the **named substituents**. SVG is generated
      deterministically so the same rule always produces the same
      image.
- [ ] Markdown "Nomenclature cheat-sheet" tutorial lessons generated
      from the rule catalogue.

### 12d. Automated naming (later)
- [ ] Integrate **STOUT** (neural IUPAC namer) behind an optional
      dependency, or **cached PubChem lookup** for a subset of
      seeded molecules. Graceful fallback to "name unknown" when
      offline.
- [ ] Agent action `name_molecule(smiles_or_id)`.

---

## Phase 13 — Reaction-coordinate diagrams & kinetics *(in progress — 2026-04-22)*

Pedagogical gap: students see a reaction as a mechanism (arrows) and as
a 3D geometry (Phases 2b / 2c) but not as an **energy profile**. Phase 13
adds the "energy landscape" view — reactants → TS‡ → intermediates →
products, with activation energies and ΔH annotated.

### 13a. Reaction-coordinate (energy-profile) renderer ✅ *(DONE 2026-04-22)*
- [x] `orgchem/render/draw_energy_profile.py` — matplotlib figure of
      energy vs reaction coordinate. Bezier-smoothed segments, sharp TS‡
      peaks, flat minima. Multi-step profiles (E1 / SN1 with intermediate
      wells) fully supported.
- [x] Per-point annotations: automatic Ea arrow for each TS, ΔH bracket
      across the full profile. Source / unit labelled in the footer so
      pedagogical estimates are flagged distinct from published DFT.
- [ ] **Follow-up**: side panel with 2D structures at each stationary point.
- [ ] **Follow-up**: ΔG / ΔS annotations (only ΔH surfaced so far).

### 13b. Data model ✅ *(DONE 2026-04-22)*
- [x] `core/energy_profile.py`: `ReactionEnergyProfile` +
      `StationaryPoint` dataclasses with JSON round-trip,
      `activation_energies` and `delta_h` helpers, `energy_unit` +
      `source` fields.
- [x] `Reaction.energy_profile_json` column + additive migration in
      `db/session.py`.
- [x] `db/seed_energy_profiles.py` — 4 seeded profiles (SN2, SN1, E1,
      Diels-Alder) with textbook values. Versioned via `SEED_VERSION`.
- [ ] **Follow-up**: seed the remaining 5 mechanism-carrying reactions
      (E2, aldol, Grignard, Wittig, Michael).

### 13c. Detailed step-by-step kinetics diagrams *(partial — 2026-04-23)*
- [x] `orgchem/render/draw_mechanism_composite.py` —
      `build_svg(mechanism) / export_composite(mechanism, path)`
      layout: top-level title block + per-step band (numbered header +
      title + RDKit arrow-pushing SVG body + wrapped description +
      separator). Reuses `render_step_svg` from `draw_mechanism.py`;
      Qt-Svg-Tiny-1.2-safe (no nested <svg>).
- [x] Agent action `export_mechanism_composite(reaction_id, path)`.
- [x] 5 tests (`tests/test_mechanism.py::test_composite_*`).
- [x] **Follow-up**: lone-pair dots on the mechanism atoms.
      `MechanismStep.lone_pairs: List[int]` field + two filled circles
      in `render_step_svg`, positioned opposite the mean-neighbour
      direction so the dots land in empty space. *(round 28,
      2026-04-23)*
- [x] **Follow-up**: `Arrow` dataclass extension for bond-midpoint
      endpoints — `Arrow.from_bond` / `to_bond` tuples resolve to the
      pixel midpoint of the bond between two atom indices, so σ/π-bond
      breaking arrows land canonically. *(round 28, 2026-04-23)*
- [ ] **Follow-up**: formal-charge badges on the mechanism atoms
      (small +/− circles near the atom, colour-coded). Needs another
      `MechanismStep.formal_charges: Dict[int, int]` field + overlay.
- [ ] **Follow-up**: extend the mechanism player (Phase 2b) with a
      *"Full-kinetics view"* toggle — renders all mechanism steps in
      one composite SVG (Schmidt-style) with every curved arrow,
      lone pair, formal charge, and numbered step visible at once.

### 13d. GUI integration *(partial — 2026-04-22)*
- [x] "Energy profile…" button on the Reactions tab, auto-enabled when
      `energy_profile_json` is populated. Opens
      `gui/dialogs/energy_profile_viewer.py` — matplotlib-rendered PNG
      preview, Ea / ΔH summary, save PNG/SVG.
- [ ] "Full kinetics" button on the mechanism player for the composite
      view (depends on 13c).
- [ ] Tutorial lesson `intermediate/06_energetics.md`.

### 13e. Agent actions ✅ *(DONE 2026-04-22)*
- [x] `export_energy_profile(reaction_id, path)` — PNG / SVG by extension.
- [x] `list_energy_profiles()` — enumerate reactions with profiles.
- [x] `get_energy_profile(reaction_id)` — returns the JSON for
      LLM reasoning.
- [ ] `export_kinetics_diagram(reaction_id, path)` — composite-view
      export (depends on 13c).
- [x] 13 tests in `tests/test_energy_profile.py`.

---

## Phase 14 — Orbital symmetry & MO theory *(NEW — planned 2026-04-22)*

The missing "why" layer under pericyclic chemistry and everything FMO-
driven. Goal: an interactive viewer for HOMO / LUMO, curved-arrow
visualisation tied to orbital overlap, and the
**Woodward-Hoffmann selection rules** as a lookup / quiz.

### 14a. Orbital visualisation *(partial — 2026-04-22)*
- [x] Hückel-MO helper in `orgchem/core/huckel.py` — eigendecomposition
      of the π-adjacency matrix with α=0, β=−1. Handles linear polyenes
      (ethene, butadiene, hexatriene), allyl cation/radical/anion,
      aromatics (benzene, Cp⁻, pyrrole, pyridine, furan). Exact textbook
      eigenvalues verified against 16 tests.
- [x] `orgchem/render/draw_mo.py` — matplotlib MO level diagram:
      horizontal bars per MO, occupied electrons as up/down arrows,
      HOMO / LUMO highlighted, degenerate levels side-by-side, α
      reference line.
- [x] Agent actions `huckel_mos(smiles)` and `export_mo_diagram(smiles,
      path)` — LLM can compute + render MO diagrams for any conjugated
      SMILES.
- [ ] **Follow-up**: 3D isosurface overlay on the molecule (positive /
      negative lobes blue / red) for the Clayden-style MO pictograms.
- [ ] **Follow-up**: PySCF integration for full ab initio MOs behind an
      optional dependency.
- [ ] **Follow-up**: a GUI tab / dialog listing all MOs with click-to-
      visualise.

### 14b. Woodward-Hoffmann rules *(partial — 2026-04-23)*
- [x] `orgchem/core/wh_rules.py` — 17 structured rules covering
      cycloadditions (6), electrocyclic (5), sigmatropic (4), and
      general rules (2). Thermal / photochemical regimes, allowed /
      forbidden / disrotatory / conrotatory outcomes, example
      reactions with SMILES.
- [x] `check_allowed(kind, electron_count, regime)` predicate
      reproducing textbook decisions for DA, [2+2], 6π electrocyclic,
      [3,3] sigmatropic, [1,3]-H shift, etc.
- [x] Agent actions `list_wh_rules`, `get_wh_rule`, `check_wh_allowed`
      + 20 tests.
- [ ] **Follow-up**: "WH rule of the day" quiz generator (Phase 5).
- [x] **Follow-up**: cross-link each pericyclic reaction to its WH entry
      — delivered as the `_REACTION_WH_MAP` lookup in
      `core/wh_rules.py`, with `find_wh_rule_for_reaction(name)` as
      the public API. Feeds the `explain_wh` action (round 49).

### 14c. FMO-based arrow pushing
- [ ] Extend the mechanism renderer so curved arrows can be annotated
      with "HOMO(diene) → LUMO(dienophile)" labels.
- [ ] Animation: morph between reactant FMOs and product FMOs over the
      existing Phase 2c.2 trajectory player.

### 14d. Agent actions *(shipped — 2026-04-23 round 49)*
- [x] `show_molecular_orbital(smiles, index)` — picks one MO from
      the Hückel calculation by index (or default = HOMO). Returns
      role (HOMO / LUMO / HOMO-n / LUMO+n), energy in β, occupation.
      Wired on the Orbitals dialog as a row-click detail label on
      the Hückel MOs tab.
- [x] `explain_wh(reaction_name_or_id)` — accepts a DB reaction id
      or a name substring, maps it onto `_REACTION_WH_MAP`, returns
      the matching W-H rule entry (or `matched=False` + note for
      non-pericyclic reactions). Wired as a "For a reaction:"
      Explain button on the Woodward-Hoffmann tab.

---

## Phase 15 — Practical laboratory techniques *(NEW — planned 2026-04-22)*

Bridges "what's on the page" and "what you do at the bench". Four sub-
modules, each a tutorial + interactive demo where possible.

### 15a. Purification *(partial — 2026-04-22)*
- [x] **Recrystallisation**: `core/lab_techniques.py` —
      `solubility_curve` fits Arrhenius-ish curve from 2 anchor points;
      `recrystallisation_yield` predicts crystals / yield % from hot +
      cold solubility values + volume. Agent action
      `recrystallisation_yield`.
- [x] **Distillation**: bp table for 30+ common lab solvents + seeded
      molecules; `distillation_plan(a, b)` recommends simple /
      fractional / non-distillable based on ΔTb. Agent action
      `distillation_plan`.
- [ ] **Follow-up**: interactive solubility curve as a widget (currently
      just the numeric helper).
- [ ] **Follow-up**: vacuum / steam distillation modes.
- [ ] **Follow-up**: sublimation (p-T phase diagram).

### 15b. Chromatography
- [ ] TLC / column / HPLC / GC — animated separation with Rf values
      driven by logP descriptors of our DB molecules.
- [ ] "Pick the mobile-phase polarity" quiz using real-world silica-
      column heuristics.
- [x] `orgchem/render/draw_tlc.py` — deterministic TLC-plate image
      given a mixture of molecule ids + a solvent polarity.

### 15c. Extraction *(partial — 2026-04-22)*
- [x] Henderson-Hasselbalch partition calculator: `fraction_ionised`
      + `extraction_plan` in `core/lab_techniques.py`. Correctly
      predicts which layer an acid / base sits in at a given pH,
      including aspirin-at-pH-1 vs aspirin-at-pH-7.
- [x] Agent action `extraction_plan(pka, ph, is_acid, smiles?)`.
- [ ] **Follow-up**: GUI panel with solvent / pH sliders and animated
      separatory-funnel schematic.
- [ ] **Follow-up**: "Drying the organic layer" mini-lesson (Na₂SO₄ /
      MgSO₄ / sieves choice, water-content implications).

### 15d. Characterisation
- [ ] Coordinates with Phase 4 Spectroscopy — an integrated
      "full workup" view: 1H NMR + 13C + IR + MS predicted for a
      selected molecule, laid out like a lab report.
- [ ] Melting-point / refractive-index / optical-rotation fields on
      the `Molecule` model (nullable, seeded for reference compounds).

### 15e. Agent actions
- [ ] `predict_tlc(molecule_ids, solvent)` — returns Rf per molecule.
- [ ] `simulate_extraction(molecule_id, aqueous_ph, organic_solvent)`.

---

## Phase 16 — Bio-organic chemistry & macromolecules *(NEW — planned 2026-04-22)*

Extends the core organic-chem engine into biology — the same bond-
making / breaking mechanisms, but applied to the molecules of life.

### 16a. Amino acids & peptides
- [ ] All 20 canonical amino acids seeded (5 already present — complete
      the set). 2D + 3D views, pKa side-chain ladder.
- [ ] Peptide-bond formation (amide synthesis) already in the DB as a
      reaction — add a **peptide-coupling workflow** (EDC/HATU,
      activated esters) as its own pathway.
- [ ] **Solid-phase peptide synthesis (SPPS)** walk-through: Merrifield
      resin, Fmoc-chemistry deprotection/coupling cycle, side-chain
      protecting-group strategy (Boc, Trt, OtBu), final cleavage. One
      seeded multi-step pathway (e.g. Met-enkephalin YGGFM).
- [ ] Protein primary structure viewer: given a FASTA / sequence,
      render the backbone in 3D (coarse alpha-carbon trace via 3Dmol.js
      cartoon mode).
- [ ] Zwitterion / isoelectric-point teaching module.

### 16b. Carbohydrates
- [ ] Monosaccharides seeded: glucose ✓, fructose, galactose, mannose,
      ribose, deoxyribose. Fischer / Haworth / chair renderers.
- [ ] Anomers (α / β) teaching demo — the mutarotation trajectory
      (reuses Phase 10a dihedral scan machinery).
- [ ] Disaccharide assembly reactions (glycosidic bond formation):
      maltose, lactose ✓, sucrose, cellobiose.
- [ ] Polysaccharide overview (starch, cellulose, glycogen) — schematic.

### 16c. Lipids & nucleic acids
- [ ] Fatty-acid set (palmitate, oleate, arachidonate, DHA).
      Saturated vs unsaturated teaching demo.
- [ ] Triglyceride assembly reaction (esterification × 3).
- [ ] Phospholipid schematic (head-group + two tails).
- [ ] Nucleotides (ATP, ADP, cAMP) + the four DNA / four RNA bases.
- [ ] Base-pairing H-bond diagram (A-T, G-C, A-U).

### 16d. Enzyme mechanisms *(partial — 2026-04-23)*
- [x] Chymotrypsin serine-protease catalytic-triad mechanism seeded
      (4 steps). *(round 12)*
- [x] Class-I fructose-bisphosphate aldolase Schiff-base mechanism
      seeded (3 steps). *(round 12)*
- [x] **HIV protease** aspartic-protease peptide-hydrolysis
      mechanism seeded (3 steps, reaction row added to
      `seed_reactions.py`, `SEED_VERSION` bumped to 6). First
      mechanism to exercise Phase 13c lone-pair dots (on the water
      attacker) and bond-midpoint arrows (for the C-N σ-bond
      cleavage step). `tests/test_seed_hiv_protease.py` covers
      step structure + JSON round-trip + tuple coercion. *(round 29,
      2026-04-23)*
- [x] **RNase A** 2-step in-line phosphoryl-transfer mechanism
      seeded. Step 1 transphosphorylation (2'-O attacks P, 5'-O
      leaves → 2',3'-cyclic phosphate) and step 2 hydrolysis
      (water attacks P, 2'-O leaves → 3'-phosphate). Both steps
      exercise Phase 13c lone-pair dots (attacker oxygen) **and**
      bond-midpoint arrows (P-O σ-bond cleavage). Reaction row +
      intermediate added; `SEED_VERSION` bumped to 7. *(round 30,
      2026-04-23)*
- [ ] Seed remaining classical enzyme mechanisms in
      `seed_mechanisms.py`: lysozyme (GH family glycoside hydrolase),
      triose-phosphate isomerase, alcohol dehydrogenase (NAD+),
      lactate dehydrogenase, HMG-CoA reductase.
- [ ] New mechanism class `EnzymeMechanism` extending `Mechanism` with
      protein-residue labels on the arrows (e.g. "His57 base").
- [ ] Tie-in to Phase 9 docking — "mechanism in the active site" view.

### 16e. Metabolism (optional stretch)
- [ ] Glycolysis as a 10-step `SynthesisPathway` entry.
- [ ] TCA cycle as a closed-loop pathway renderer.
- [ ] Pedagogical only — full flux-balance analysis is out of scope.

---

## Phase 17 — Physical organic chemistry *(NEW — planned 2026-04-22)*

The quantitative layer: rates, equilibria, substituent effects,
isotopes. Builds on Phase 13 energy profiles.

### 17a. Kinetics vs thermodynamics
- [ ] Interactive "kinetic vs thermodynamic product" demo: pick
      temperature → see which of two products wins (diene-ene
      Diels-Alder endo/exo is the canonical teaching case).
- [ ] Rate-law derivation helper — given a mechanism JSON, derive the
      rate law by the steady-state approximation.
- [ ] Arrhenius plot for any seeded reaction with an activation energy.

### 17b. LFER / Hammett / Taft
- [ ] `orgchem/core/hammett.py` — σ / σ+ / σ- constants for the common
      substituents; compute ρ from a user-supplied (k_X / k_H) series.
- [ ] Interactive Hammett-plot widget: user picks a substituent set,
      app plots log(k/k₀) vs σ and returns ρ + fit quality.
- [ ] Taft steric parameters (Es) supported similarly.

### 17c. Isotope effects
- [ ] Kinetic isotope effect (H/D) teaching module — pick an atom in a
      molecule, app computes the zero-point-energy shift and the
      predicted kH/kD at 298 K (harmonic approximation).
- [ ] Mass-spectrum isotope-pattern helper (already queued in Phase 4).

### 17d. Solvent effects & polarity scales
- [ ] Solvent-polarity scales (ET(30), π*, ε) as a DB table.
- [ ] "Pick the best solvent" quiz for any seeded reaction given its
      mechanism class (SN1 benefits from polar protic, SN2 from polar
      aprotic, …).

### 17e. Agent actions
- [ ] `compute_rate_law(reaction_id)` → string.
- [x] `hammett_fit(data, sigma_type)` → ρ, r², fit line + teaching
      interpretation. Shipped round 55 as
      `core/physical_organic.hammett_fit` + agent action. Ships
      with a curated σₘ / σₚ / σₚ⁻ / σₚ⁺ catalogue for 15 common
      substituents via `list_hammett_substituents`.
- [x] `predict_kie(isotope_pair, partner_element, nu_H_cm1,
      temperature_K)` → primary KIE via Bigeleisen simplification.
      Shipped round 55 in the same module. Signature diverged from
      the original roadmap (`molecule_id, atom_index` was never
      ergonomic — the isotope-pair / ν_H / T form matches how
      textbook problems are phrased).

---

## Phase 18 — Green chemistry & sustainability *(NEW — planned 2026-04-22)*

Tightly integrated with existing Pathways (Phase 8) — we already seed
the BHC ibuprofen route as a green-chemistry exemplar. Phase 18 makes
this a first-class dimension across all pathways.

### 18a. Atom-economy calculator *(partial — 2026-04-22)*
- [x] `orgchem/core/green_metrics.py` — `atom_economy(reaction_smiles)`
      with auto-heaviest-product convention, `e_factor(mass_inputs,
      mass_product)`, `pathway_atom_economy(steps)` overall-AE folder.
- [x] Agent actions `reaction_atom_economy(reaction_id)` and
      `pathway_green_metrics(pathway_id)` — LLM can now reason about
      atom economy without the seeded-only restriction.
- [x] 15 tests in `tests/test_green_metrics.py` (BHC > 70 % AE, Fischer
      ester ~83 %, DA 100 %, bromination ~66 %).
- [ ] **Follow-up**: renderer overlay on the Synthesis tab — each step
      shows its AE % alongside yield; cached in the DB as a nullable
      column for seeded rows.

### 18b. Alternative solvents & reagents
- [ ] Solvent-hazard classifier (preferred / usable / hazardous per the
      CHEM21 solvent guide) as a DB table.
- [ ] Pathway re-writer tool: pick a seeded pathway, app suggests
      greener solvent swaps where applicable.
- [ ] First-class support for **water**, **ionic liquids**
      ([BMIM][PF₆] etc.), and **supercritical CO₂** as reaction media;
      seed at least one pathway per medium to show the contrast with
      traditional VOC-heavy routes.

### 18c. Catalysis focus
- [ ] Catalytic vs stoichiometric flag on `SynthesisStep` — seed
      accurately across all current pathways.
- [ ] Turnover-number / turnover-frequency widgets for catalysed steps
      (when user supplies a mol% loading).

### 18d. Classic comparisons
- [ ] Seed the two **Paracetamol routes** (already have Hoechst 3-step;
      add the 1-step version) and the two **Aspirin routes**
      (already have phenol + acetic anhydride; add Kolbe-Schmitt
      2-step ✓). Classroom asks "which is greener — and why?".
- [ ] Worked-example tutorial `graduate/03_green_chemistry.md`.

### 18e. Agent actions *(partial — 2026-04-23 round 50)*
- [x] `atom_economy(reaction_id)` → %. Shipped earlier as
      `reaction_atom_economy(reaction_id)`; the per-pathway variant
      is `pathway_green_metrics(pathway_id)`.
- [x] `compare_pathways_green(pathway_ids)` → ranked side-by-side
      table of overall atom-economy per route + worst-step AE.
      GUI: new "Compare pathways" tab on the Green metrics dialog.
      (Round 50.) Future work: add E-factor + solvent-class
      columns once `seed_pathways.py` grows reagent/solvent mass
      annotations.

---

## Phase 19 — Medicinal chemistry & drug design *(NEW — planned 2026-04-22)*

Bridges chemistry and pharmacology. Leverages the Phase 9 docking
engine and the existing drug seeds (aspirin, paracetamol, ibuprofen,
naproxen, caffeine, diazepam, fluoxetine, atorvastatin, …).

### 19a. Structure-activity relationships (SAR) *(partial — 2026-04-23)*
- [x] `orgchem/core/sar.py` — `SARSeries` / `SARVariant` dataclasses
      + 2 seeded series: NSAIDs (aspirin / ibuprofen / naproxen /
      acetaminophen vs COX-1 / COX-2) and statins (lovastatin /
      simvastatin / atorvastatin vs HMG-CoA reductase).
      `compute_descriptors` folds Phase 19b's drug-likeness per row.
- [x] `orgchem/render/draw_sar.py` — colour-coded heat-map matrix:
      rows = variants, columns = MW / logP / TPSA / QED / Lipinski
      violations + series-specific activity metrics. Per-column
      min-max rescaling with lower-is-better flip for IC50 /
      violations.
- [x] Agent actions `list_sar_series`, `get_sar_series`,
      `export_sar_matrix` under the **medchem** category.
- [x] 12 tests in `tests/test_sar.py`.
- [ ] **Follow-up**: seed additional SAR series (penicillin β-lactams,
      fluoroquinolones, ACE inhibitors) for teaching depth.
- [ ] **Follow-up**: GUI panel that embeds the matrix inline in the
      Molecule Workspace.

### 19b. Pharmacokinetic descriptors (ADME)
- [ ] Extend `core/descriptors.py` with: Lipinski's 5 violations ✓
      (already there), Veber rules, Ghose filter, PAINS pattern match
      (via RDKit FilterCatalog), QED drug-likeness score.
- [ ] Properties panel gets a "Drug-likeness" group.
- [ ] Optional: cLogP, cLogD at pH 7.4, CNS MPO score.

### 19c. Bioisosteres & scaffold hopping *(partial — 2026-04-23)*
- [x] `orgchem/core/bioisosteres.py` — 14 SMARTS-reaction templates
      covering COOH ↔ tetrazole, Me ↔ CF₃, amide ↔ sulfonamide,
      phenyl → thiophene, O ↔ CH₂, Cl ↔ F, ArOH ↔ ArNH₂, ester →
      amide. Each template has id / label / description /
      bidirectional SMARTS.
- [x] `suggest_bioisosteres(smiles, template_ids=None)` applies all
      matching templates and returns the unique variant set. Self-
      matches excluded; "product has no mapped atoms" warnings
      silenced for templates where byproducts are unmapped by design.
- [x] Agent actions `list_bioisosteres`, `suggest_bioisosteres`
      under **medchem**.
- [x] 11 tests verifying catalogue integrity, canonical ibuprofen →
      tetrazole swap, halogen ladder, CF₃ swap, filter narrowing,
      bad-input handling.
- [ ] **Follow-up**: overlay bioisostere variants against the Phase
      19a SAR matrix to predict how property columns shift.
- [ ] **Follow-up**: GUI "Apply bioisostere" menu on the Molecule
      Workspace.

### 19d. Target-based design (ties to Phase 9 docking)
- [ ] Docking tab gains a **"design a ligand"** mode: user sketches a
      SMILES, docker returns predicted pose + score + ADME flags.
- [ ] Warhead library: seeded covalent-warhead fragments (acrylamide,
      chloromethyl ketone, epoxide, sulfonyl fluoride, Michael
      acceptors from Phase 6).

### 19e. Agent actions
- [ ] `drug_likeness(molecule_id)` → dict of rule-based scores.
- [ ] `suggest_bioisosteres(molecule_id, fg_atom_indices)` → list of
      variant SMILES.
- [ ] `build_sar_table(parent_id, r_variant_ids)` → rendered image
      + underlying data.

---

## Cross-cutting: stereochemistry *(woven through every phase — 2026-04-22)*

Per the user's explicit note: **stereochemistry is not a standalone
topic** — it touches every reaction, every mechanism, every synthesis
route. Rather than silo it into one phase, every other phase has a
"stereo-aware" sub-task. Tracked here so nothing gets missed.

### Where stereochemistry shows up
- **Phase 2b / 2c mechanisms** — SN2 inversion ✅ shown via 3D trajectory;
  E2 anti-periplanar needs highlighting; Diels-Alder endo / exo. **Queue:**
  label each mechanism with the stereochemical outcome.
- **Phase 3a 2D renderer** — wedge / dash bonds + R/S labels + cis/trans
  markers. **Queue:** add CIP priority computation on 2D viewer.
- **Phase 3c conformer ensemble** — for chiral molecules, both
  enantiomers in the ensemble. **Queue:** enantiomer flip button.
- **Phase 6a molecules** — seed molecules as explicit enantiomers where
  it matters (D-glucose vs L-glucose; R-ibuprofen vs S-ibuprofen).
  **Queue:** fill out enantiomer pairs.
- **Phase 8 synthesis pathways** — asymmetric-synthesis pathways
  deserve a chirality-timeline annotation: "stereocentre installed
  at step 3, preserved through steps 4-7". **Queue:** add
  `SynthesisStep.stereochem_note` column.
- **Phase 12 IUPAC naming** — R/S / E/Z descriptors. **Queue:** add
  a "stereodescriptor" sub-module under `naming/`.
- **Phase 13 energy profiles** — ∆∆G‡ for enantiomeric TSs gives ee
  predictions. **Queue:** two-curve energy-profile plotter.
- **Phase 14 orbital symmetry** — supra / antarafacial is pure
  stereochemistry. **Queue:** WH rule demos always animate both faces.
- **Phase 16 bio-organic** — natural chirality preference (L-amino
  acids, D-sugars) is a major teaching topic. **Queue:** sidebar
  lesson.
- **Phase 17 physical organic** — Curtin-Hammett principle; kinetic
  vs thermodynamic control of stereochemistry. **Queue:** add to
  the intermediate energetics tutorial.
- **Phase 19 medicinal chemistry** — stereochemistry in drug action
  (thalidomide R vs S; ibuprofen R vs S). **Queue:** SAR table must
  distinguish enantiomers where relevant.

### Dedicated cross-cutting items
- [x] `orgchem/render/draw2d.py` — wedge/dash output option + R/S
      labelling + E/Z labelling for alkenes (via RDKit's
      `addStereoAnnotation`). (2026-04-22)
- [x] `orgchem/core/stereo.py` — canonical stereodescriptor API:
      `assign_rs`, `assign_ez`, `stereocentre_atoms`, `enantiomer_of`,
      `flip_stereocentre`, `summarise`. Wraps RDKit's `AssignStereochemistry`.
      (2026-04-22)
- [x] Agent actions: `assign_stereodescriptors(smiles|molecule_id)`,
      `enantiomer_of(smiles|molecule_id)`, `flip_stereocentre(smiles,
      atom_index)`, `export_molecule_2d_stereo(smiles, path)`. (2026-04-22)
- [x] 18 tests in `tests/test_stereo.py` covering R/S + E/Z + meso
      diagnosis + enantiomer round-trip + wedge-bond SVG sanity +
      all 4 agent actions. (2026-04-22)
- [ ] Tutorial `intermediate/01_stereochemistry.md` (already in the
      curriculum-gap queue; promote to highest priority).
- [ ] `diastereomers_of(mol)` helper — enumerate diastereomers of
      multi-centre molecules (harder; deferred).

---

## Curriculum coverage matrix *(living gap analysis — 2026-04-22)*

The four-section syllabus the app is built against (per user request).
Each topic is tracked with: **Tutorial** (markdown lesson written?),
**Molecules** (DB entries that exemplify the topic), **Reactions**
(seeded examples), **Mechanisms** (step-by-step arrow pushing),
**Illustration** (3D / 2D visuals available).

### 1. Fundamental concepts

| Topic | Tutorial | Molecules | Reactions | Mechanisms | Illustration |
|-------|----------|-----------|-----------|------------|--------------|
| Lewis structures | ✅ `beginner/03` | full DB | — | — | all 2D/3D views |
| Hybridisation (sp³, sp², sp) | ✅ `beginner/02` | methane, ethene, ethyne | — | — | 3D shows geometry |
| Molecular geometry (VSEPR) | ⚠ partial (in 02) | full DB | — | — | 3D viewer covers it |
| Bond polarity | ❌ | full DB | — | — | needs dipole arrows |
| Intermolecular forces | ❌ | need H-bonded exemplars | — | — | pending |
| Resonance | ❌ | benzene, carbonyl, enolate | — | ⚠ enolate in aldol | needs resonance drawer |
| Formal charge | ❌ | ammonium, nitro, carboxylate | — | — | — |
| pKa / acid-base | ❌ | need pKa ladder molecules | — | — | — |
| Curved-arrow notation | ⚠ implicit in mechs | — | — | ✅ 9 mechanisms | ✅ mechanism player |
| IUPAC nomenclature | ❌ | — | — | — | **Phase 12 planned** |
| Chair conformations | ❌ | cyclohexane | — | — | ⚠ Phase 10a ring-flip demo |
| Newman projections | ❌ | ethane, butane | — | — | needs Newman renderer |
| Steric strain | ❌ | overlaps with above | — | — | — |
| Chirality, R/S | ❌ | many chiral seeded | — | — | needs CIP renderer |
| Fischer projections | ❌ | D-glucose | — | — | needs Fischer renderer |
| Diastereomers / enantiomers | ❌ | threose, glucose anomers | — | — | — |

### 2. Core reaction types & mechanisms

| Topic | Tutorial | Molecules | Reactions | Mechanisms | Illustration |
|-------|----------|-----------|-----------|------------|--------------|
| SN1 / SN2 | ✅ `intermediate/02` | t-BuBr, MeBr | ✅ both | ✅ both | ✅ 3D reaction render |
| E1 / E2 | ✅ `intermediate/03` | 2-BrBu, t-BuBr | ✅ both | ✅ both | ✅ |
| Electrophilic addition (alkenes) | ❌ | ethene | ✅ bromination, hydrogenation | ❌ | ⚠ 3D render for hydrog. |
| Oxidation (e.g. epoxidation) | ❌ | — | ✅ PCC, Baeyer-Villiger | ❌ | ✅ PCC 3D bond-order |
| Radical reactions | ❌ | — | ✅ radical halogenation | ❌ | — |
| Benzene structure / aromaticity | ❌ | benzene, naphthalene… | — | — | — |
| Electrophilic aromatic substitution | ❌ | — | ✅ FC alkylation/acylation, nitration | ❌ | 2D only |
| Aromaticity rules (Hückel) | ❌ | PAH set | — | — | — |
| Aldehydes & ketones (addition) | ❌ | acetone, acetaldehyde | ✅ Grignard, NaBH4 | ✅ Grignard | ✅ |
| Carboxylic acids & derivatives | ❌ | acetic acid, aspirin | ✅ Fischer ester., amide | ❌ | — |
| Alpha-C chemistry (enolate) | ❌ | — | ✅ aldol | ✅ aldol | — |
| Aldol condensation | ❌ | — | ✅ | ✅ | — |
| Claisen condensation | ❌ | — | ✅ | ❌ | — |

### 3. Spectroscopy & structure determination

| Topic | Tutorial | Molecules | Reactions | Mechanisms | Illustration |
|-------|----------|-----------|-----------|------------|--------------|
| IR spectroscopy (functional groups) | ❌ | full DB | — | — | **needs IR renderer — Phase 4** |
| ¹H NMR interpretation | ❌ | full DB | — | — | **needs NMR prediction — Phase 4** |
| ¹³C NMR interpretation | ❌ | full DB | — | — | Phase 4 |
| Mass spectrometry | ❌ | full DB | — | — | **needs MS m/z + isotope — Phase 4** |

### 4. Synthesis & analytical skills

| Topic | Tutorial | Molecules | Reactions | Mechanisms | Illustration |
|-------|----------|-----------|-----------|------------|--------------|
| Retrosynthetic analysis | ❌ | — | — | — | **Phase 2c.3 / 8d planned** |
| Functional group interconversion | ❌ | — | ✅ 26 seeded rxns | ✅ 9 mechs | partial |
| Reagents & conditions | ⚠ in pathways | — | ✅ | ✅ | ✅ pathway schemes |
| Green chemistry | ⚠ in BHC pathway | — | — | — | ✅ BHC pathway |
| Multi-step synthesis | ⚠ 9 pathways | — | — | — | ✅ pathway renders |

### Coverage-work queue (prioritised)

**Highest pedagogical ROI** (implement next):
1. **Stereochemistry tutorial** + a `render/draw2d.py` option to draw
   wedge/dash bonds with R/S labels. (Covers 4 checklist rows at once.)
2. **Aromaticity tutorial** with Hückel-rule explainer + example
   aromatic / antiaromatic / non-aromatic trio (benzene, cyclobutadiene,
   cyclooctatetraene).
3. **Phase 11 Glossary** — unlocks cross-linking from every existing
   tutorial, reaction description, and mechanism note.
4. **Phase 12 Nomenclature** — biggest checklist gap.

**Medium ROI** (next-quarter):
5. **Phase 4 Spectroscopy** — IR chart + ¹H NMR shift predictor (even
   a rule-based one covers the teaching case).
6. Newman-projection renderer (uses existing 3D coords + a 2D view
   down the C-C axis).
7. Fischer-projection renderer for sugars.

**Long-tail**:
8. Resonance-structure drawer (multi-form molecule viewer).
9. Dipole-arrow overlay on 2D / 3D views.
10. pKa ladder / acid-base-titration teaching widget.

### Method
Every time a piece of content (molecule, reaction, mechanism, pathway,
tutorial) lands, update the matching row of this matrix. The goal is
not "all green" — it's "we know where the gaps are, and we attack them
by highest ROI first."

---

## Reaction coverage by educational level *(living — 2026-04-22)*

Complements the subject-area matrix above. Same content, organised by
the level a student first meets it. Updated each session.

### Undergraduate (Foundation)

The bread and butter of organic chemistry — stereochemistry,
regioselectivity, and the logic of electron flow.

| Topic | Reaction seeded | Mechanism | 3D render | Pathway |
|-------|-----------------|-----------|-----------|---------|
| **SN1 / SN2** — inversion, carbocation stability | ✅ both | ✅ both | ✅ both (bond colour) | — |
| **E1 / E2** — Zaitsev vs Hofmann products | ✅ both | ✅ both | — | — |
| **Electrophilic addition** — Markovnikov hydrohalogenation, hydration | ⚠ bromination ✅, hydrogenation ✅; **HX Markovnikov, hydration missing** | ❌ | ✅ H₂ | — |
| **Diels-Alder [4+2]** | ✅ | ✅ | — | — |
| **EAS** — nitration, halogenation, Friedel-Crafts | ✅ nitration, FC-alk, FC-acyl; **Br₂/Fe arene missing** | ❌ | — | — |
| **Carbonyl additions** — Grignard, acetals, imines | ⚠ Grignard ✅; **acetals / imines missing** | ✅ Grignard | — | ✅ Grignard pathway |

### Upper-level undergraduate (Intermediate)

Making C–C bonds and controlling specific functional groups.

| Topic | Reaction seeded | Mechanism | 3D render | Pathway |
|-------|-----------------|-----------|-----------|---------|
| **Enolate: Aldol, Claisen, Michael, Robinson annulation** | ✅ aldol, Claisen, Michael; **Robinson missing** | ✅ aldol, Michael; Claisen ❌ | — | — |
| **Oxidations** — Swern, PCC, Jones, DMP | ⚠ PCC ✅; **Swern, Jones, DMP missing** | ❌ | ✅ PCC (bond-order) | — |
| **Reductions** — LiAlH₄ vs NaBH₄ selectivity | ⚠ NaBH₄ ✅; **LiAlH₄ missing** | ❌ | ✅ NaBH₄ | — |
| **Wittig olefination** | ✅ | ✅ (3-step) | — | — |
| **Nucleophilic acyl substitution** — esters, amides, acid chlorides | ✅ Fischer ester., amide formation | ❌ | — | ✅ Aspirin, Paracetamol |
| **Radical halogenation** — selective alkane functionalisation | ✅ methane + Cl₂ | ❌ | — | — |

### Graduate (Advanced)

Modern synthetic methodology, organometallics, highly specific
transformations.

| Topic | Reaction seeded | Mechanism | 3D render | Pathway |
|-------|-----------------|-----------|-----------|---------|
| **Cross-coupling** — Suzuki, Heck, Sonogashira, Buchwald-Hartwig | ⚠ Suzuki ✅; others **missing** | ❌ | — | — |
| **Olefin metathesis** (Grubbs) | ❌ | ❌ | — | — |
| **Asymmetric synthesis** — Sharpless, Evans, MacMillan organocatalysis | ❌ | ❌ | — | — |
| **Rearrangements** — Beckmann, Curtius, Baeyer-Villiger | ⚠ Baeyer-Villiger ✅, pinacol ✅; **Beckmann, Curtius missing** | ❌ | — | — |
| **Protecting-group chemistry** — BOC, TBS, PMB, benzyl, acetal | ❌ all | ❌ | — | — |
| **Pericyclic** — Diels-Alder, [2+3] dipolar cycloaddition, sigmatropic (Cope, Claisen) | ⚠ Diels-Alder ✅, 6π electrocyclic ✅; **1,3-dipolar, Cope, Claisen rearrangement missing** | ❌ | — | — |

### Summary of gaps by level

**Undergraduate, still missing**: HX / H₂O Markovnikov addition,
bromination of benzene, acetal formation, imine formation, Robinson
annulation. Small and high-impact — **queue first** alongside the
stereochemistry + aromaticity tutorials.

**Intermediate, still missing**: Swern / Jones / DMP oxidations,
LiAlH₄ reduction, Claisen mechanism, Robinson annulation, a more
explicit acyl-substitution family view.

**Graduate, still missing**: nearly all cross-coupling partners beyond
Suzuki, olefin metathesis, the asymmetric-catalysis triad (Sharpless,
Evans, MacMillan), classic rearrangements (Beckmann, Curtius),
protecting-group chemistry, and most pericyclic variants beyond
Diels-Alder.

This is the content-expansion target list for the next several
sessions. Each row maps to a "+ one reaction / one mechanism / one
pathway" commit, so the work is incremental and testable.

---

## Phase 20 — Quality-of-life & polish *(NEW — planned 2026-04-22)*

A running list of smaller usability / infrastructure improvements that
don't fit cleanly under a single feature phase. These are picked up
between larger work items.

### 20a. Offline robustness *(partial — 2026-04-23)*
- [x] Bundle **3Dmol.js** locally so the 3D viewer and trajectory
      player work without internet access. `scripts/fetch_3dmol_js.py`
      is a one-shot urllib downloader that drops the minified bundle
      under `orgchem/gui/assets/3Dmol-min.js`. `build_3dmol_html` now
      splits into a CDN template and an inline template; when the
      local asset exists and `prefer_local=True` (default) it inlines
      the bundle contents so the generated HTML is fully
      self-contained. 5 tests in `tests/test_offline_3dmol.py`.
- [ ] Cache all PubChem fetches under `~/Library/Caches/OrgChem/pubchem/`
      so re-opening a previously seen molecule doesn't hit the network.
- [ ] Offline-mode banner in the Search panel so students know they're
      working from cache.

### 20b. Regression & golden-file testing *(partial — 2026-04-23)*
- [x] `tests/golden/` with 12 baseline PNGs covering: 2D molecule
      renders (benzene / aspirin / caffeine / R-ibuprofen), reaction
      schemes (Diels-Alder / SN2), energy profiles (SN1 / Diels-Alder),
      MO diagrams (benzene / butadiene), IR spectra (acetic acid /
      acetone). `scripts/regen_goldens.py` rewrites them on demand.
- [x] `tests/test_golden_renders.py` — 12 perceptual-hash
      (imagehash.phash) regression tests with `TOLERANCE=8`
      (Hamming-distance threshold). Tests `importorskip` gracefully
      when imagehash isn't installed; runtime env stays lean, CI +
      dev installs light them up.
- [x] Dev deps declared in `requirements-dev.txt` (imagehash + pillow
      already pinned from round 12).
- [ ] **Follow-up**: pytest-qt UI tests for live `MainWindow` drives
      (click buttons, assert state).
- [ ] **Follow-up**: agent-registry contract test — round-trip every
      action's type hints through Anthropic / OpenAI schema emitters.

### 20c. Theming & look-and-feel
- [ ] Dark theme (already an empty `theme` field in `AppConfig`).
      Swap to Qt's Fusion dark palette when selected.
- [ ] Colour-blind-safe rendering option: swap the PCC/NaBH4 red/green
      bond-change highlights for a deuteranopia-safe palette
      (ColorBrewer `Set1` works).
- [ ] Configurable font size / zoom for the whole app — important for
      classroom projection.

### 20d. Session save / restore *(partial — 2026-04-23)*
- [x] `orgchem/core/session_state.py` — YAML-serialised
      `SessionState` dataclass: active tab, current molecule (id +
      SMILES), loaded PDB + ligand, NA-ligand, compare-slot SMILES,
      HRMS measurement, free-form notes. Forwards-compatible loader
      drops unknown keys. Files live under the per-user config dir
      (`sessions_dir()` helper in `utils/paths.py`).
- [x] GUI wiring: File menu entries *Save session…* (Ctrl+S),
      *Load session…* (Ctrl+Shift+O), *Recent sessions ▸* submenu
      populated from `list_sessions()`.
      `MainWindow.capture_session_state` / `apply_session_state`
      snapshot + restore the Proteins panel's PDB id, ligand name,
      NA-ligand name, and the active tab index.
- [x] Three agent actions on a new **session** category:
      `list_sessions`, `save_session_state`, `load_session_state`.
- [x] 10 tests in `tests/test_session_state.py` (YAML round-trip,
      forwards-compat, `save_session`/`load_session`, sanitiser,
      list, agent round-trip).
- [ ] **Follow-up**: "Session templates" — ship a starter set of
      saved sessions (e.g. "caffeine case study", "aspirin case
      study") seeded on first launch.
- [ ] **Follow-up**: persist compare-grid SMILES + the HRMS guesser
      last-measurement automatically. Dataclass fields exist; we
      just need the GUI widgets to report back into
      `capture_session_state`.

### 20e. Batch / scripting conveniences *(partial — 2026-04-23)*
- [x] `orgchem/core/batch.py` + `scripts/batch_render.py` — given a
      CSV / TXT of SMILES, render each to 2D PNG, schematic IR PNG,
      a `descriptors.csv` row (MW / logP / TPSA / HBD / HBA / QED /
      Lipinski pass), and a `report.md` summary with embedded
      thumbnails. Handles bad SMILES gracefully (logged in the
      failures list, good molecules still processed).
- [x] 8 tests covering parser (CSV + TXT formats + missing-column
      error), render smoke, failure isolation, opt-outs,
      file-shortcut, `_safe_name` filename sanitiser.
- [ ] **Follow-up**: "bulk SMILES → DB import" GUI dialog (wraps
      `batch_render_from_file` + the DB insert path).
- [ ] **Follow-up**: "Snapshot → LaTeX" export (TikZ / chemfig
      conversion of SVG).

### 20f. Observability
- [ ] Session-log panel gets a **filter by level** + a **save to file**
      button.
- [ ] Per-action telemetry: how many times each agent action is
      invoked, average runtime. Helps prioritise optimisation work
      over time.

### 20g. Documentation polish
- [ ] `docs/` directory with mkdocs-material. User guide, lesson
      walkthrough, agent API reference (generated from docstrings).
- [ ] Architecture diagram showing the agent-registry / bus / panel
      relationships for onboarding new contributors.
- [ ] `CONTRIBUTING.md` with the file-size cap rule, the additive-
      seed pattern, and the "every feature needs an agent action"
      principle.

---

## Phase 21 — Advanced content & new panels *(NEW — planned 2026-04-22)*

Accelerating content-generation work beyond Phase 6's incremental
additions.

### 21a. Advanced-tier tutorials *(partial — 2026-04-23)*
- [x] `advanced/01_pericyclic.md` — concerted sigmatropic + [n+m] +
      electrocyclic family; ties into the 6π electrocyclic + Diels-Alder
      seeds and the Hückel MO engine. (round landed 2026-04-22)
- [x] `advanced/02_organometallics.md` — cross-coupling catalytic
      cycle (OA / TM / RE); Suzuki / Negishi / Stille / Heck /
      Sonogashira / Buchwald-Hartwig; ligand choice; 18-electron rule.
      Leverages the Suzuki seeded reaction + Phase 6f DB-canonical
      fragment rendering. (round 2, 2026-04-23)
- [x] `advanced/03_retrosynthesis.md` — Corey notation + four core
      disconnection strategies + FGI cheat-sheet + linear vs convergent;
      worked examples against the seeded BHC Ibuprofen, Aspirin (two
      routes), Paracetamol (two routes), and SPPS Met-enkephalin
      pathways. (round 4, 2026-04-23)
- [x] `advanced/04_spectroscopy.md` — IR/¹H NMR/¹³C NMR/MS workflow;
      structure-determination strategy; worked problem integrating all
      four techniques; leans on Phase 4 IR predictor. Advanced tier
      4/4 complete. (round 5, 2026-04-23)

### 21b. Graduate-tier tutorials *(partial — 2026-04-23)*
- [x] `graduate/01_named_reactions.md` — curated tour across 6
      families (C–C, oxidation, reduction, rearrangement,
      substitution, asymmetric). Each entry flagged ✅ / 🟡 / ⬜
      against the seeded DB; also ends with the top-5 Phase 6b
      seeding priorities. (round 6, 2026-04-23)
- [x] `graduate/02_asymmetric.md` — Knowles / Noyori / Sharpless AE+AD
      / Jacobsen epox + HKR / Grubbs / List proline aldol / MacMillan
      imidazolidinone / Jacobsen thiourea / MacMillan SOMO / Evans
      oxazolidinone / CBS reduction. Includes ee/er metrics,
      chiral-drug histories (thalidomide / propranolol / ibuprofen /
      esomeprazole), and a Phase 6b seeding-priority list of 5
      reactions to add next. Ties to `enantiomer_of` /
      `assign_stereodescriptors` actions. (round 7, 2026-04-23)
- [x] `graduate/03_mo_theory.md` — LCAO recipe, simple Hückel, FMO
      theory with worked Diels-Alder / SN2 / EAS examples using the
      live `huckel_mos` and `check_wh_allowed` actions. Notes on
      beyond-Hückel (semi-empirical / HF / DFT / CCSD(T)); 5 key
      MO concepts; Koopmans' theorem tie to photoelectron spectroscopy.
      (round 8, 2026-04-23)
- [x] `graduate/04_total_synthesis.md` — five case studies:
      Strychnine (Woodward 1954), Vitamin B₁₂ (Woodward-Eschenmoser
      1973), Taxol (Nicolaou 1994), Palytoxin (Kishi 1989-94),
      Erythromycin (Woodward 1981). Shared strategic themes
      (convergence, disconnection selection, method-birth-from-
      project, protecting-group choreography, substrate vs catalyst
      stereocontrol). Full curriculum now **18 / 18 lessons complete**.
      (round 9, 2026-04-23)

### 21c. Reaction prediction panel
- [ ] Given a list of starting materials + conditions, predict the
      product via template matching against the seeded reaction set.
      Simple: ranks templates by functional-group overlap; returns
      top-K candidates with confidence scores.
- [ ] Agent action `predict_products(smiles_list, conditions_hint)`.
- [ ] GUI: right-dock widget in the Molecule Workspace with a
      "Predict!" button once reactants are selected.

### 21d. Retrosynthesis panel (builds on Phase 8d)
- [ ] Given a target SMILES, walk the seeded reaction templates in
      reverse. Surface up to 3 single-step disconnections per node;
      recurse to depth 3.
- [ ] GUI: tree-view layout of disconnection graph; click a node to
      jump to that intermediate; solid-outline for in-DB molecules,
      dashed-outline for hypothetical.
- [ ] Agent action `find_pathways_to(target_smiles, max_depth)`.

### 21e. Multi-molecule alignment in the 3D viewer
- [ ] Given N molecules, overlay them in 3D after MCS-based
      alignment (useful for SAR series).
- [ ] GUI: Compare tab gets a "Superpose in 3D" button.

---

## Phase 22 — Developer-experience tooling *(NEW — planned 2026-04-22)*

### 22a. CI / reproducibility *(partial — 2026-04-23)*
- [x] `.github/workflows/test.yml` — GitHub Actions pipeline:
      pytest with xvfb + Qt offscreen + coverage upload; advisory
      ruff lint + format + mypy (non-blocking while the codebase
      stabilises); Python 3.11 + 3.12 matrix.
- [x] `requirements-dev.txt` — pytest, pytest-qt, pytest-cov, ruff,
      mypy, imagehash, matplotlib pinned. Runtime
      `requirements.txt` stays lean.
- [x] `pyproject.toml` — ruff (line-length 100, py311 target, per-file
      ignores for long-SMILES seed files), mypy (lax start,
      ignore_missing_imports for RDKit / PySide / matplotlib /
      numpy), pytest ini (markers, strict, short tb).
- [x] `tests/test_docs_coverage.py` — enforces the CLAUDE.md rule
      "every module must be mentioned in INTERFACE.md" and that
      INTERFACE.md doesn't point at stale files. 6 tests; already
      caught 3 missing entries (`fragment_resolver`, `seed_coords`,
      `seed_intermediates`) which were added in this round.
- [x] **Follow-up**: pre-commit hooks (trailing-whitespace / ruff /
      ruff-format / mypy on `orgchem/core/` / check-yaml /
      check-added-large-files) so the contract runs on every commit.
      Config at `.pre-commit-config.yaml`; activate with
      `pip install pre-commit && pre-commit install`. *(round 28,
      2026-04-23)*
- [x] **Follow-up (partial)**: ruff blocking on a clean subset of
      recently-added modules (`core/hrms.py`, `ms_fragments.py`,
      `na_interactions.py`, `plip_bridge.py`, `ppi.py`, `pockets.py`,
      `protein.py`, `session_state.py`, `render/draw_interaction_map.py`,
      `render/draw_protein_3d.py`). The advisory full-tree ruff run
      still runs with `continue-on-error` until the older modules are
      cleaned up. *(round 28, 2026-04-23)*
- [ ] **Follow-up**: expand the blocking ruff subset to cover all of
      `orgchem/core/` + `orgchem/render/` once the older modules are
      tidied.
- [ ] **Follow-up**: make mypy blocking on `orgchem/core/` once the
      RDKit stubs stabilise.

### 22b. Release packaging
- [ ] PyInstaller recipe → standalone `.app` / `.exe` / AppImage.
      Main hurdle: RDKit wheels + QWebEngineView bundling.
- [ ] Versioning: `orgchem/__init__.__version__` + `version` file read
      from `pyproject.toml`.
- [ ] Changelog automation — `towncrier` or equivalent.

### 22c. Extensibility
- [ ] Plugin architecture: `orgchem.plugins` entry-point group so
      third parties can register new renderers / data sources / LLM
      backends without forking.
- [ ] Example: a `orgchem-docking` plugin that slots in AutoDock
      Vina for Phase 9 without needing the upstream repo to add it.

---

## Phase 24 — Protein structure, folding, and ligand binding *(NEW — planned 2026-04-23; user-flagged)*

The natural extension of Phase 9 (small-molecule docking) — once the
student can see how a drug binds, they should also be able to see
**what it's binding to**: the protein target, its fold, its active
site, and the molecular grammar of the binding interaction. This
phase operationalises the structural-biology side of medicinal chem.

### 24a. Protein structure ingestion *(partial — 2026-04-23)*
- [x] `orgchem/sources/pdb.py` — `fetch_pdb(pdb_id)` + `fetch_pdb_text`
      with RCSB download + local cache at
      `~/Library/Caches/OrgChem/pdb/`. Graceful 404, bad-id rejection,
      `parse_from_cache_or_string` for network-free testing.
- [x] `orgchem/core/protein.py` — `Protein` / `Chain` / `Residue` /
      `Atom` dataclasses + column-fixed PDB parser (no Biopython dep).
      ATOM / HETATM split, element inference, water + ion filtering,
      1-letter sequence helper.
- [x] `SEEDED_PROTEINS` — 6 teaching targets: 2YDO (adenosine-A2A /
      caffeine), 1EQG (COX-1 / ibuprofen), 1HWK (HMG-CoA / atorvastatin),
      1HPV (HIV protease / ritonavir), 4INS (insulin hexamer — PPI
      anchor), 1D12 (doxorubicin-DNA — NA-ligand anchor).
- [x] 4 agent actions under new **protein** category:
      `list_seeded_proteins`, `fetch_pdb`, `get_protein_info`,
      `get_protein_chain_sequence`.
- [x] 16 tests via fixture PDB (no network). *(round 20, 2026-04-23)*
- [ ] **Follow-up**: seed 4 more targets (acetylcholinesterase,
      thrombin, dihydrofolate reductase, carbonic anhydrase).
- [ ] **Follow-up**: DSSP secondary-structure annotation (Biopython
      optional dep).

### 24b. AlphaFold / ESMFold ingestion *(partial — 2026-04-23)*
- [x] `orgchem/sources/alphafold.py` — EBI AlphaFold DB fetch
      (`https://alphafold.ebi.ac.uk/files/AF-{uniprot}-F1-model_v4.pdb`)
      with local cache at `~/Library/Caches/OrgChem/alphafold/`.
      `AlphaFoldResult` dataclass exposes per-residue pLDDT
      (from the B-factor column) + mean pLDDT + confidence bucket
      ("very high" / "confident" / "low" / "very low") matching the
      AFDB colouring convention.
- [x] Agent actions `fetch_alphafold(uniprot_id)` and
      `get_alphafold_info(uniprot_id)` (cache-only).
- [x] 8 tests (`tests/test_alphafold.py`), no network required.
- [ ] **Follow-up**: pLDDT-colour overlay on the 3D viewer panel
      (pedagogical framing of prediction quality).
- [ ] **Follow-up**: ESMFold backend for truly novel sequences
      (optional — requires PyTorch + model weights).

### 24c. Protein-ligand complex display *(partial — 2026-04-23)*
- [ ] Extend `render/draw3d.py` (3Dmol.js backend) with a "protein +
      ligand" mode: cartoon for protein, ball-and-stick for ligand,
      semi-transparent surface around the ligand's 5 Å shell.
- [x] Matplotlib-backed fallback (for headless CI) renders a flat
      2D "interaction map" — ligand centre + each contact residue
      spoke with bond type (H-bond, π-π, salt bridge, hydrophobic).
      Implemented in `orgchem/render/draw_interaction_map.py`: a
      PoseView-style radial diagram with `_KIND_COLOURS` (H-bond blue,
      salt-bridge red, π-stacking purple, hydrophobic green) and
      matching `_KIND_LINESTYLES`. Agent action `export_interaction_map
      (pdb_id, ligand_name, path)` pipes `analyse_binding` ⇒ PNG/SVG
      by extension. 6 tests in `tests/test_interaction_map.py`.
- [ ] New `ProteinComplex` data model: `(protein_pdb, ligand_smiles,
      binding_site_residues, notes)`; seeded with the 8 teaching
      targets above paired with their canonical ligand.

### 24d. Ligand-binding-site detection *(partial — 2026-04-23)*
- [x] `orgchem/core/pockets.py` — grid-based pocket finder (probe
      grid over the bounding box, buriedness check across 8 octants,
      flood-fill clustering of qualifying voxels, ranking by voxel
      count). Annotates top-K pockets with the residues that line
      them. Zero-dep alternative to fpocket.
- [x] Agent action `find_binding_sites(pdb_id, top_k)`.
- [x] 6 tests (`tests/test_pockets.py`) via a synthetic spherical-shell
      fixture where the cavity is known by construction.
- [ ] **Follow-up**: fpocket / SiteMap / PocketMiner shell-out path
      when the local binary is present; graceful fallback to the
      built-in finder when not.
- [ ] **Follow-up**: druggability score per pocket (atom-polarity /
      volume / enclosure-based heuristic).

### 24e. Binding-mechanism analysis *(partial — 2026-04-23)*
- [x] `orgchem/core/binding_contacts.py` — `analyse_binding(protein,
      ligand_name)` returns a `ContactReport` enumerating H-bonds
      (≤ 3.5 Å heavy-atom), salt bridges (≤ 4.5 Å charged N/O), π-π
      (≤ 5.5 Å ring-centroid to Phe/Tyr/Trp/His), hydrophobic
      (≤ 4.5 Å C-C on Ala/Val/Leu/Ile/Met/Pro/Phe/Trp/Tyr).
- [x] Agent action `analyse_binding(pdb_id, ligand_name)`.
- [x] 7 tests with a constructed fixture where H-bond /
      salt-bridge / π-stacking / hydrophobic contacts are all known
      by geometry.
- [ ] **Follow-up**: pharmacophore-role tagging (donor vs acceptor,
      stack vs ionic) on each contact.
- [x] **Follow-up**: feed ContactReport into the 24c 2D interaction
      map renderer (colour-coded dashed lines per contact type).
      *(2026-04-23 — `export_interaction_map` action + renderer.)*

### 24f. Folding-pathway storytelling *(longer-term)*
- [ ] Animated "fold the polypeptide" demo: start from an extended
      chain, apply rotamer sampling + simple Rosetta-lite energy
      minimisation, end at the native fold. Driven by the existing
      Phase 2c.2 3Dmol.js trajectory player.
- [ ] Tutorial `graduate/05_protein_folding.md` — Anfinsen experiment,
      molten globule, chaperones, intrinsic disorder. Links to the
      seeded AlphaFold examples.

### 24g. Pedagogical seeds
- [ ] **"How caffeine wakes you up"** — caffeine + adenosine A2A
      receptor (PDB 2YDO); walk the H-bond contacts + hydrophobic
      stack with Phe168.
- [ ] **"Why aspirin is irreversible"** — aspirin + COX-1 (PDB 1EQG);
      the covalent acetyl-Ser530 contact.
- [ ] **"Why statins work"** — atorvastatin + HMG-CoA reductase (PDB
      1HWK); the mevalonate-mimic pocket.
- [ ] **"Why HIV protease inhibitors failed first-generation"** —
      ritonavir + protease mutant; shows the drug-resistance axis.
- [ ] Each seed is a `ProteinComplex` row + a tutor prompt that
      traces the binding story in natural language.

### 24h. Agent actions
- [ ] `list_proteins()` / `get_protein(pdb_id)` — the seeded set.
- [ ] `fetch_alphafold(uniprot_id)` — AlphaFold DB import.
- [ ] `find_binding_sites(pdb_id)` — pocket enumeration.
- [ ] `analyse_binding(pdb_id, ligand)` — contact breakdown.
- [ ] `export_binding_site(pdb_id, ligand, path)` — 3D scene or 2D
      interaction map PNG.

### 24i. PLIP protein-ligand interaction profiling *(partial — 2026-04-23)*

**PLIP** (Protein-Ligand Interaction Profiler;
https://plip-tool.biotec.tu-dresden.de) is the canonical open-source
tool for detecting non-covalent interactions from a PDB structure.
It classifies:

- Hydrogen bonds (donor / acceptor geometry + distance criteria)
- Halogen bonds
- π-stacking (parallel vs perpendicular)
- π-cation interactions
- Salt bridges
- Hydrophobic contacts
- Water bridges (via ordered waters)
- Metal coordination

Integration plan:

- [x] `orgchem/core/plip_bridge.py` — adapter module with three code
      paths: (1) **Python API** — `from plip.structure.preparation
      import PDBComplex` when importable; (2) **CLI** — invoke
      `plip`/`plipcmd` with `-x` flag on a cached PDB and parse the
      emitted `report.xml`; (3) **Built-in fallback** — delegate to
      `binding_contacts.analyse_binding` with `engine="builtin"`.
      `require_plip=True` short-circuits the fallback for callers who
      need the upgrade or nothing. *(2026-04-23)*
- [x] `PLIPResult` wraps our `ContactReport` + `engine` tag so the
      downstream renderer (Phase 24c) works interchangeably across
      engines. No new data model required.
- [x] Agent actions `plip_capabilities()` (diagnostic) and
      `analyse_binding_plip(pdb_id, ligand_name, require_plip)`.
      8 tests in `tests/test_plip_bridge.py` (blocked-`plip`-import
      fixture exercises the fallback path with no network / no deps).
- [ ] **Follow-up**: REST fallback to `plip-tool.biotec.tu-dresden.de`
      for users who can't pip-install PLIP (needs an Anthropic-friendly
      caching story).
- [ ] **Follow-up**: render integration — overlay PLIP-detected
      contacts on the 3D viewer; the 2D interaction map already flows
      through `ContactReport` and thus works today for the Python API
      and CLI paths.
- [ ] **Follow-up**: disk cache for PLIP runs (analysis is slow; keyed
      on PDB hash + ligand name).

### 24j. Protein-protein interaction (PPI) analysis *(partial — 2026-04-23)*

Many biologically important structures are heteromeric assemblies
(antibody-antigen, hormone-receptor, enzyme-inhibitor peptide).
A teaching tool here lets students see *how* two chains interact.

- [x] Chain-chain interface detection in `orgchem/core/ppi.py`.
      Exposes `analyse_ppi(protein)` (all pairs) and
      `analyse_ppi_pair(protein, chain_a, chain_b)` (single pair).
      Uses the same geometric H-bond / salt-bridge / π-stacking /
      hydrophobic criteria as 24e, applied cross-chain. Returns
      `PPIInterface` records with per-contact records, per-kind
      counts, and sorted interface-residue lists on both sides.
      9 tests in `tests/test_ppi.py` with a constructed two-chain
      fixture where every contact kind is tripped by known geometry.
- [x] Agent actions `analyse_ppi(pdb_id)` and
      `analyse_ppi_pair(pdb_id, chain_a, chain_b)`.
- [ ] **Follow-up**: hotspot analysis — tag interface residues by
      contribution to buried SASA; flag the classic hotspot residues
      (Trp, Tyr, Arg) for teaching.
- [ ] **Follow-up**: shell out to **PISA** (CCP4 / PDB) for the
      gold-standard interface report.
- [ ] **Follow-up**: 2D interface-map renderer that re-uses the
      radial layout from 24c but shows chain-A vs chain-B.
- [ ] **Follow-up seeds**: insulin dimer (4ins), antibody-antigen
      (1i4y), Ras-Raf RBD (4g0n), HIV protease homodimer (1hpv).

### 24k. Nucleic-acid-ligand interactions (DNA / RNA) *(partial — 2026-04-23)*

Same framework as protein-ligand but for nucleic acids. Small-molecule
DNA / RNA binders are a growing drug class (riboswitch modulators,
G-quadruplex stabilisers, DNA intercalators like doxorubicin).

- [x] PDB parser already recognises A/T/G/C/U / DA/DT/DG/DC/DU as
      nucleic-acid residues (Phase 24a `NUCLEOTIDES` set). Sugar +
      phosphate geometry is preserved in the parsed :class:`Residue`
      since we keep every ATOM record.
- [x] Contact analyser specialised for NA in
      `orgchem/core/na_interactions.py`: distinguishes
      **intercalation** (ligand planar between two consecutive base
      centroids with centroid-centroid angle ≥ 120°), **major- /
      minor-groove H-bonds** (name-indexed atom tables per base), and
      **phosphate-backbone contacts** (N/O atoms within 4.5 Å of a
      phosphate oxygen). 8 tests in `tests/test_na_interactions.py`
      with constructed stacked / groove / phosphate fixtures.
- [x] Agent action `analyse_na_binding(pdb_id, ligand_name)` on the
      **protein** category.
- [x] **GUI integration**: new Proteins tab (24-series one-stop) with
      an NA-ligand sub-tab listing the classified contacts.
- [ ] **Follow-up**: covalent-adduct detection (e.g. cisplatin
      crosslinks between adjacent guanines). Needs a covalent-bond
      predicate on top of the current non-covalent model.
- [ ] PLIP runs on nucleic-acid complexes by default, so 24i largely
      reuses. The specialised analysis sits **on top** of PLIP's
      output.
- [ ] Seeded teaching examples:
      - Doxorubicin-DNA intercalation (PDB 1d12)
      - Cisplatin crosslink (PDB 1aio)
      - HIV TAR RNA + argininamide (PDB 1arj) — small-molecule RNA
        binding
      - Flavin mononucleotide riboswitch (PDB 3f2q)
- [ ] Agent actions `analyse_na_ligand(pdb_id, ligand_name)`,
      `classify_binding_mode(pdb_id, ligand_name)` returning one of
      `intercalator` / `groove-binder` / `covalent` / `other`.

### 24l. 3D protein-structure viewer inside the Proteins tab *(partial — 2026-04-23)*

Interactive WebGL view of a loaded PDB, embedded directly in the
Proteins tab so students can rotate / zoom / pick without leaving
the app. Complements the 24c 2D interaction map (great for reports)
by giving an interactive 3D counterpart (great for exploration).

- [x] `orgchem/render/draw_protein_3d.py` — builds a self-contained
      3Dmol.js HTML string from PDB text. Cartoon / trace / surface
      protein styles, ball-and-stick / stick / sphere ligand styles,
      optional `highlight_residues` (yellow-carbon stick overlay +
      `addResLabels`), optional ligand surface for pocket-view,
      optional water / ion visibility. Reuses the Phase 20a offline
      3Dmol.js bundle so the viewer works without network.
- [x] Agent action `export_protein_3d_html(pdb_id, path, ...)` on the
      **protein** category — writes the viewer to disk for sharing.
- [x] GUI integration: **new "3D structure" sub-tab** in the
      Proteins panel (`gui/panels/protein_panel.py`) hosting a
      `QWebEngineView`. Auto-populates residue highlights from the
      most-recent Contacts-tab analysis so the 3D view doubles as a
      binding-site inspector. Controls: protein style / ligand style
      drop-downs, *Waters* toggle, *Ligand surface* toggle, *Render*
      button, *Save HTML…* button. Auto-renders on PDB fetch.
- [x] 13 tests in `tests/test_draw_protein_3d.py` covering style
      combos, residue-highlight JS, water / surface toggles, file
      round-trip, missing-file error, offline inlining, and the
      agent action.
- [x] **Follow-up**: colour-by-pLDDT overlay for AlphaFold models.
      `colour_mode="plddt"` on `build_protein_html` emits a 3Dmol.js
      `colorfunc` that maps atom.b (the B-factor column, where
      AlphaFold stores pLDDT) to the AlphaFold DB gradient
      (`#0053d6`/`#65cbf3`/`#ffdb13`/`#ff7d45`). Proteins tab has a
      *"Colour by pLDDT"* checkbox auto-enabled on AlphaFold fetch.
      5 new tests in `tests/test_draw_protein_3d.py`. *(round 29,
      2026-04-23)*
- [x] **Follow-up**: click-to-inspect residue overlay — wire the
      viewer's picked-atom event back to the Proteins panel.
      `build_protein_html(..., enable_picking=True)` injects a CSS
      overlay + `#pick-label` div + qwebchannel.js loader, and
      attaches a 3Dmol `setClickable` handler. In the Qt host, a
      `_PickBridge(QObject)` with `@Slot(str, str, int) onAtomPicked`
      bounces the picked `(chain, resn, resi)` into a Qt `picked`
      signal that updates a label below the viewer. 4 new HTML-only
      tests in `tests/test_draw_protein_3d.py`. *(round 30,
      2026-04-23)*
- [x] **Follow-up**: export a rotation animation — `spin=True` on
      `build_protein_html` calls 3Dmol's `v.spin("y", 1.0)` so the
      saved HTML auto-rotates on load (no capture-to-GIF step; the
      HTML itself is the animation). Proteins tab has an
      *"Auto-rotate"* checkbox; agent action exposes `spin`,
      `spin_axis`, `spin_speed`. Axis is sanitised to {x, y, z} so
      the parameter can't inject arbitrary JS. 5 tests. *(round 31,
      2026-04-23)*
- [ ] **Follow-up (still open)**: GIF / MP4 capture of the spin for
      embedding in lecture slides; needs a headless browser +
      screen-recording pipeline.

### Dependencies & non-goals
- **Optional deps**: Bio.PDB (Biopython) for parsing, PyTorch +
  ESMFold / openfold weights for folding, **plip** (pip-installable)
  for the local-path interaction profiling, PISA (CCP4) for PPI
  interface analysis. All gated behind graceful fallback so the base
  install stays slim.
- **Out of scope**: full MD simulation of the complex (→ Phase 10b
  OpenMM), binding-free-energy calculations (MMPBSA / alchemical;
  point to OpenFE externally), cryo-EM map fitting (huge separate
  project), de-novo docking (→ Phase 9 Vina / Smina / DiffDock).
- This phase **complements** Phase 9 (docking) rather than replacing
  it — Phase 9 generates the complex; Phase 24 displays + analyses it.
- PLIP is BSD-licensed; their REST endpoint is for academic /
  non-commercial use. The local-install path should be the default
  for production / teaching at scale.

---

## Phase 31 — Seeded content expansion *(NEW — 2026-04-23; user-flagged)*

User directive (2026-04-23): *"please add a roadmap item to further
expand molecules, synthesis examples, tutorials, reactions, synthesis
and all seeded items to grow the scope of the project."* Phase 31 is
a long-running content phase that runs in parallel with every code
phase. Each sub-item is a bundle of additive seeds that graduate
through `SEED_VERSION` bumps, so existing DBs pick them up on next
launch.

**Target end-state (by end of the phase):** 400 molecules, 50 named
reactions, 20 mechanisms, 25 synthesis pathways, 20 energy profiles,
80 glossary terms, 30 tutorial lessons, 40 carbohydrates / 40 lipids
/ 40 nucleic-acid entries, 15 SAR series, 15 seeded proteins.

- [~] **31a. Molecules → 400.** First 25 shipped (α/β-pinene,
      limonene, myrcene, camphor, menthol, geraniol, farnesol;
      18-crown-6, 15-crown-5, free-base porphine; styrene, vinyl
      chloride, ethylene glycol, bisphenol-A, caprolactam;
      glyphosate, atrazine, DDT; glycerol, HMPA, diglyme; indigo,
      methylene blue). ~170 more to come. Keep growing
      `seed_molecules_extended.py`:
      another 190 molecules across families that are currently
      thin — metal complexes (ferrocene, vitamin B12 core,
      cisplatin), macrocycles (18-crown-6, porphyrins, cryptands),
      terpene skeletons (α-pinene, limonene, camphor, menthol),
      alkaloids beyond the current set (morphine, codeine,
      strychnine core, reserpine), polymers / monomers (styrene,
      vinyl chloride, ethylene glycol, bisphenol-A), agrochemicals
      (glyphosate, atrazine, DDT), synthetic dyes (methylene blue,
      malachite green, indigo), common solvents not yet seeded
      (diglyme, HMPA, glycerol, pentane). Each entry tagged via
      `auto_tag` and `seed_source_tags` so the Phase 28 filter
      bar immediately surfaces them.
- [x] **31b. Reactions → 50. COMPLETE (round 157, 2026-04-25); extension to 60 COMPLETE (60/60 after round 182).**  Shipped across rounds 41-175 —
      Buchwald-Hartwig, Sonogashira, Mitsunobu, Swern, HWE,
      Heck (round 121), Negishi (round 123),
      **CuAAC click chemistry (round 134 — Sharpless / Meldal
      / Bertozzi 2022 Nobel)** — Cu(I)-catalysed
      azide-alkyne cycloaddition giving the 1,4-disubstituted
      1,2,3-triazole.  Two-stage Cu-acetylide /
      σ,π-bound-azide ladder cycle (Fokin / Worrell 2013) that
      accelerates the thermal Huisgen reaction ~10⁷-fold AND
      drives complete 1,4-regioselectivity.  Bioorthogonal +
      water-tolerant — the conditions that put click at the
      centre of chemical biology + drug discovery.
      Pedagogically distinct from the 5 existing Pd-coupling
      entries (different transition metal, different mechanism,
      different teaching point about regioselectivity vs.
      thermal).  Two new fragments (`Benzyl azide`,
      `1-Benzyl-4-phenyl-1,2,3-triazole`) seeded alongside —
      fragment-consistency audit clean.  **Round 152 added two
      more entries — Birch reduction (the first SET-mechanism
      reduction in the catalogue; teaches the 4-step ladder
      Na→radical-anion → EtOH-protonation → Na→pentadienyl-
      anion → EtOH-protonation giving the non-conjugated
      1,4-cyclohexadiene; substituent-rule for EDG/EWG
      regiochemistry called out) AND Dess-Martin periodinane
      oxidation (modern, mild I(V) hyper-valent-iodine
      oxidation that complements the existing Swern + PCC +
      Jones; bench-stable + room-temperature + no
      over-oxidation are the killer selectivity arguments).
      Three new intermediate fragments seeded (`Sodium metal
      [Na]`, `Sodium cation [Na+]`, `1,4-Cyclohexadiene`).**
      **Round 153 added two more entries — Sharpless asymmetric
      epoxidation (the first asymmetric-catalysis entry in the
      catalogue; teaches the chiral Ti-tartrate complex,
      allylic-OH substrate restriction, and the Sharpless
      face-selectivity mnemonic; product carries explicit
      tetrahedral chirality markers) AND CBS reduction (the
      second asymmetric-catalysis entry; teaches the
      oxazaborolidine catalyst + BH₃ hydride source + cis-fused
      6-membered TS; pedagogically distinct from the seeded
      NaBH₄ entry — same C=O → C-OH transformation but with
      absolute-configuration control).  Five new intermediate
      fragments seeded (`trans-Crotyl alcohol`, `tert-Butyl
      hydroperoxide`, `(2R,3R)-2,3-Epoxybutan-1-ol`, `Borane
      (BH3)`, `(R)-1-Phenylethanol`).**
      **Round 154 added two more entries — Sharpless asymmetric
      dihydroxylation (the second Nobel-2001 Sharpless entry —
      catalytic K₂OsO₄ + bis-cinchona PHAL chiral ligand
      pre-mixed as AD-mix-α / AD-mix-β + K₃Fe(CN)₆ stoichiometric
      oxidant; [3+2] of OsO₄ + alkene → osmate ester → hydrolysis
      to syn-diol; pedagogically distinct from Sharpless
      epoxidation by working on ANY alkene without an allylic-OH
      restriction) AND Jacobsen-Katsuki epoxidation (Mn(III)(salen)
      catalyst + NaOCl bleach oxidant; Mn(V)=O oxo-intermediate
      delivers oxygen to cis-disubstituted aryl alkenes that
      Sharpless asymmetric epoxidation cannot touch — completes
      the asymmetric-oxygen-installation toolkit).  Six new
      intermediate fragments + a one-shot SMILES backfill that
      fixed a buggy historical `trans-Stilbene` row (had been
      stored under the trans-Stilbene name but with cis SMILES;
      `seed_intermediates._SMILES_FIXES` now corrects it
      idempotently on next launch to `C(=C\\c1ccccc1)/c1ccccc1`).**
      Catalogue now **44/50**; 6 more to come.  Asymmetric-
      catalysis category now carries 4 entries (Sharpless
      epoxidation + CBS + Sharpless AD + Jacobsen).
      **Round 155 added two more entries — Mukaiyama aldol
      (Mukaiyama 1973; Lewis-acid-catalysed crossed aldol
      between a silyl enol ether + aldehyde via an open TS;
      the first asymmetric C-C bond-formation entry in the
      catalogue) AND Evans aldol (Evans 1981; chiral-
      oxazolidinone-auxiliary-controlled diastereoselective
      aldol via a Bu₂BOTf-formed (Z)-boron enolate adding
      through a Zimmerman-Traxler chair TS to give the
      Evans-syn product — pedagogically distinct from
      Mukaiyama by stoichiometric chiral auxiliary + closed
      TS vs sub-stoichiometric chiral catalyst + open TS).
      Five new intermediate fragments seeded (`TMS enol ether
      of acetone`, `(R)-4-Hydroxy-4-phenylbutan-2-one`,
      `Trimethylsilanol TMS-OH`, `N-Propionyl-(S)-4-benzyl-2-
      oxazolidinone`, `Evans syn-aldol product`).  Asymmetric-
      catalysis category now carries 6 entries; the
      asymmetric C-C bond-formation teaching surface is now
      open alongside the C-O / C=O entries shipped in
      rounds 153-154.**
      **Round 156 added two more entries — Stille coupling
      (Migita-Kosugi-Stille 1978; Pd(0)-catalysed C-C coupling
      between aryl/vinyl halide + organostannane via oxidative
      addition → transmetalation → reductive elimination;
      uniquely tolerates water + acid + base + most polar
      functional groups thanks to the air-/moisture-stable Sn
      reagent — but tributyltin's toxicity / persistence is
      the trade-off that pushed Suzuki ahead for commercial
      use; **closes the Pd-coupling family at 5/5 textbook
      canon entries** alongside Suzuki + Negishi + Heck +
      Sonogashira) AND Corey-Chaykovsky epoxidation
      (Corey + Chaykovsky 1965; sulfur-ylide methylene
      transfer to a carbonyl giving an epoxide — pedagogically
      paired with the existing Wittig entry as 'same carbonyl
      substrate, different product class' (alkene vs epoxide)
      via the classic R₃P=CR₂ vs R₂S=CR₂ ylide divide; the
      only catalogue entry that builds a brand-new oxirane
      CH₂ ring atom from a non-alkene C=O substrate, in
      contrast to the C=C-oxidising Sharpless / Jacobsen
      entries).  Four new intermediate fragments seeded
      (`Tributyl(vinyl)stannane`, `Tributyltin bromide`,
      `Dimethylsulfonium methylide`, `Dimethyl sulfide`).**
      Catalogue now **48/50**; just 2 more to come.
      **Round 157 closed Phase 31b at the 50/50 milestone with
      Appel reaction (Appel 1975; PPh₃ + CCl₄ alcohol →
      alkyl chloride via SN2 displacement of the
      alkoxytriphenylphosphonium leaving group with inversion
      of configuration; pedagogically paired with Mitsunobu —
      both PPh₃-mediated alcohol-OH activation paths,
      delivering R-X (Appel) vs R-O-CO-R'/R-N-CO-R'/etc.
      (Mitsunobu)) AND Jones oxidation (Jones 1946; Cr(VI) /
      CrO₃ + H₂SO₄ in acetone over-oxidises 1° alcohol all
      the way to carboxylic acid via gem-diol intermediate;
      pedagogically the **counterpoint** to the seeded
      PCC + Swern + Dess-Martin entries — those were
      specifically designed to STOP at the aldehyde, Jones
      shows what happens when you don't; modern green-
      chemistry replacements (TEMPO/NaOCl, NaIO₄/RuCl₃)
      called out).  Six new intermediate fragments seeded
      (`Carbon tetrachloride CCl4`, `1-Chlorooctane`,
      `Chloroform CHCl3`, `Chromium trioxide CrO3`,
      `Octanoic acid (caprylic acid)`, `Chromium dioxide
      CrO2`).  **Phase 31b 50/50 vision realised after rounds
      152-157 — 12 new entries in 6 rounds.**
      **Round 164 opened the Phase 31b extension to 60-target
      with two alkene-functionalisation entries: Wacker
      oxidation (Smidt et al. 1959; Pd(II)/Cu(II)/O₂
      catalytic cycle that converts a terminal alkene to a
      methyl ketone with **Markovnikov regioselectivity**;
      industrial process for ethylene → acetaldehyde at
      ~ 2 Mt/yr globally; opens the redox-relay teaching
      template for modern aerobic oxidations) AND Brown
      hydroboration-oxidation (H. C. Brown 1956-1959, Nobel
      1979 shared with Wittig; two-step alkene → alcohol via
      concerted 4-centre BH₃ syn-addition + alkaline H₂O₂
      [1,2]-alkyl-shift oxidation; **anti-Markovnikov +
      syn-addition** stereochemistry; the canonical contrast
      pair to Wacker on regio-selectivity AND to Br₂ addition
      on stereochemistry).  Three new intermediate fragments
      seeded (`1-Methylcyclohexene`, `Hydrogen peroxide H2O2`,
      `trans-2-Methylcyclohexanol`).  **Together opens the
      alkene-functionalisation regio-/stereo-selectivity
      teaching surface** that the original 50-entry catalogue
      underserved — Wacker (Markovnikov ketone) +
      Brown (anti-Markovnikov + syn alcohol) sit alongside
      the existing bromination of ethene (Markovnikov syn-
      Br₂-anti) + catalytic hydrogenation (syn H₂ addition).
      Catalogue now **52/60**.
      **Round 165 added two more entries — Robinson
      annulation (Sir Robert Robinson 1935 / Nobel 1947;
      **3-step cascade in one pot**: Michael addition of
      enolate onto MVK + intramolecular aldol on the
      1,5-diketone + dehydration to the cyclohexenone;
      the canonical ring-construction reaction in textbook
      total synthesis — the Wieland-Miescher steroid-
      precursor route uses exactly this cascade; the
      asymmetric Hajos-Parrish proline-catalysed variant
      1971 is the intellectual ancestor of modern
      enamine-catalysis — Nobel 2021 List/Barbas/MacMillan)
      AND Knoevenagel condensation (Emil Knoevenagel 1894;
      variant of aldol where the nucleophile is an
      **active-methylene compound** between two electron-
      withdrawing groups — pKa ~ 11-13 vs simple ketone
      α-CH ~ 20 — so a mild secondary-amine base
      (piperidine / pyridine) is sufficient; Doebner
      modification adds spontaneous decarboxylation of
      one COOH/COOR group; workhorse for cinnamic-acid +
      α,β-unsaturated-ester / nitrile syntheses).  Three
      new intermediate fragments seeded (`Δ1,9-octalin-2-
      one Robinson product`, `Diethyl malonate`, `Diethyl
      benzylidene malonate`).  **Together opens the
      ring-construction + active-methylene C-C bond-
      formation teaching surfaces** alongside the existing
      Diels-Alder + 6π electrocyclic + aldolase entries.
      Catalogue now **54/60**.
      **Round 175 added two more entries — Henry reaction
      (Louis Henry 1895; nitromethane + benzaldehyde →
      2-nitro-1-phenylethanol; base-catalysed nitroaldol;
      pKa contrast with classic aldol — nitroalkane α-H ~ 10
      vs ketone α-H ~ 20 — enables mild secondary-amine /
      KF / fluoride catalysts; aci-nitro carbanion
      intermediate; β-nitro alcohol product is a workhorse
      precursor to chiral 1,2-amino alcohols via
      hydrogenation — chloramphenicol + β-blocker scaffolds;
      Shibasaki Ln-BINOL + Trost Zn-ProPhenol asymmetric
      variants > 90 % ee) AND Hantzsch dihydropyridine
      synthesis (Hantzsch 1881; **the textbook multi-
      component reaction** — aldehyde + 2 β-ketoester + NH₃
      → 1,4-dihydropyridine + 3 H₂O; Knoevenagel +
      enaminone + Michael + dehydration cascade in one pot;
      DHP scaffold is the core of the calcium-channel-
      blocker antihypertensive class — nifedipine 1975,
      amlodipine 1990, felodipine, nicardipine; opens the
      MCR teaching surface alongside the existing Robinson
      annulation + Knoevenagel cascades).  Three new
      intermediate fragments seeded (`Nitromethane`,
      `2-Nitro-1-phenylethanol`, `Hantzsch 1,4-DHP product`).
      Catalogue now **56/60**.  **Round 182 closed the 60/60
      milestone** with **Grubbs olefin metathesis** (Ru-catalysed
      C=C exchange, Nobel 2005 — fills the metathesis gap
      complementing the Pd-cross-coupling cluster), **Wolff-Kishner
      reduction** (carbonyl → CH₂ via hydrazone + base; complements
      Clemmensen for acid-sensitive substrates), **Hofmann
      elimination** (anti-Zaitsev β-elimination from quaternary
      ammonium hydroxide; pedagogical contrast with E2 / Saytzeff),
      and **Ozonolysis with reductive workup** (alkene → 2
      carbonyls via Criegee ozonide; classic structure-determination
      tool).  Five new intermediate fragments seeded (1-Hexene /
      1-Phenyl-1-hexene / 2-Pentyltrimethylammonium / 1-Pentene /
      Ozone).  **Phase 31b → 60/60 SHIPPED.**  Originally**
      Priority
      list: Buchwald-Hartwig amination, Negishi coupling, Heck
      reaction, Stille coupling, Sonogashira coupling, Mitsunobu
      reaction, Swern oxidation, Dess-Martin oxidation, Jones
      oxidation, Oppenauer oxidation, Birch reduction, Corey-Chaykovsky
      epoxidation, Horner-Wadsworth-Emmons, Julia olefination,
      Peterson olefination, Appel reaction, Mukaiyama aldol,
      Evans aldol, Sharpless asymmetric epoxidation, Sharpless
      dihydroxylation, Jacobsen epoxidation, CBS reduction, Shapiro
      reaction, Ramberg-Bäcklund. Atom-mapped SMARTS where
      possible to feed the 3D side-by-side viewer.
- [x] **31c. Mechanisms → 20.** **Complete as of round 62 —
      catalogue now 20 / 20.** Shipped across rounds 59-62:
      Fischer esterification 5-step (round 59), NaBH₄ reduction
      2-step (round 60), nitration of benzene 3-step EAS (round 60),
      Claisen condensation 4-step (round 61), pinacol rearrangement
      4-step with 1,2-methyl shift (round 61), **bromination of
      ethene 3-step bromonium anti-addition (round 62)**,
      **Friedel-Crafts alkylation 3-step EAS via methyl cation
      (round 62)**. The seed file was split into three themed
      sub-modules (classic / enzyme / extra) to keep every file
      under the 500-line cap. SEED_VERSION bumped to 11 so existing
      DBs pick up the two new JSON blobs on next launch. Follow-up
      orphan for a future phase (31f?): Swern, HWE, Mitsunobu,
      Buchwald-Hartwig catalytic cycle, Sonogashira, Sharpless
      epoxidation, CBS, Jacobsen, Stille, Birch, Mukaiyama aldol
      once the 20-target is well past.
- [x] **31d. Synthesis pathways → 25. COMPLETE (round 80).**
      Full catalogue across rounds 41-80:
      Benzocaine 3-step, Lidocaine 2-step, Procaine 2-step,
      Sulfanilamide 3-step chlorosulfonation,
      Phenolphthalein 1-step FC condensation,
      Saccharin 3-step Remsen-Fahlberg,
      Acetanilide 1-step acetylation,
      L-DOPA 3-step Knowles Rh-DIPAMP asymmetric H₂,
      Dopamine 1-step AADC decarboxylation,
      Adipic acid 2-step DuPont KA-oil,
      Nylon-6,6 2-step Carothers polycondensation,
      **Nylon-6 3-step Beckmann / caprolactam** (round 80),
      **Aspartame 2-step Z-peptide coupling** (round 80),
      plus the earlier rounds Wöhler urea, Aspirin (×2),
      Paracetamol (×2), BHC Ibuprofen, Caffeine, Phenacetin,
      Vanillin, Aniline 2-step, 2-methyl-2-butanol Grignard,
      Met-enkephalin Fmoc SPPS.  Catalogue now **25 / 25**.
      Two nylon commodity chains (6 + 6,6) share cyclohexanone
      as pedagogical branch point.  Follow-up priorities for
      a future phase (32+): taxol (abbreviated —
      Baran-style endgame), morphine (Rice or Trost endgame),
      lysergic acid, reserpine (Woodward), cortisone fragment,
      longifolene core, oseltamivir (Shibasaki), sildenafil,
      atorvastatin (final assembly), cephalosporin fragment,
      penicillin V, progesterone (Djerassi endgame), glyphosate
      (industrial). Each with per-step SMILES, conditions, yields,
      notes + reagent annotations.
- [x] **31e. Energy profiles → 20. COMPLETE (round 106).**
      Shipped across rounds 41-106:
      Sonogashira catalytic cycle (OA as RDS), HWE via oxaphosphetane
      collapse, Mitsunobu via oxyphosphonium SN2,
      Claisen condensation (round 98) — "final deprotonation drives
      the equilibrium",
      **Fischer esterification (round 99)** — shallow 5-point
      curve encoding the textbook **thermoneutral equilibrium**
      (|ΔH| < 15 kJ/mol; K ≈ 3) that needs Le Chatelier drive
      (excess ROH or Dean-Stark water removal) to push forward.
      Pairs pedagogically with Claisen: one is driven by the
      final step, the other only by Le Chatelier.
      **Nitration of benzene (round 101)** — canonical 3-point
      EAS saddle-dip-saddle: rate-limiting NO₂⁺ attack TS at
      +90 kJ/mol, Wheland (arenium) intermediate in a shallow
      +45 valley, low-barrier deprotonation, re-aromatised
      product at −25. The σ-complex shape every EAS profile
      inherits.
      **NaBH₄ reduction of acetone (round 102)** — simplest
      irreversible addition shape in the catalogue.  Single
      rate-limiting 4-centre hydride-transfer TS at +55,
      stabilised borate-alkoxide well at −80, trivial aqueous
      workup, strongly exergonic product (ΔH ≈ −115 kJ/mol).
      Teaching complement to Grignard addition (same shape
      family, different nucleophile polarity).
      **Bromination of ethene (round 103)** — canonical
      bromonium-valley anti-addition shape.  RDS is step 1
      (π-electrons attack Br-Br; Br⁻ kicked out) at +80 kJ/mol.
      The 3-membered bromonium intermediate sits in a
      resonance-stabilised valley above reactants but below
      both TSs; that shape is *why* Br⁻ backside-SN2-opens the
      bromonium instead of recombining — anti-addition
      stereochemistry falls out.  Pairs with round-62 mechanism
      JSON.
      **Pinacol rearrangement (round 104)** — 1,2-methyl-shift
      teaching shape.  7 points: ionisation TS (RDS +100) →
      tertiary carbocation well (+40) → migration TS (+50;
      below ionisation TS because migration is fast once
      the cation exists) → oxocarbenium well (−20; below the
      pre-shift carbocation because the O lone pair
      stabilises) → deprotonation → ketone (−70).  The
      "oxocarbenium lower than tert-C⁺" inequality is why
      1,2-shifts run forward, not reverse.
      **Chymotrypsin catalytic triad (round 105)** — first
      **enzyme-catalysed** profile in the catalogue. 9 points,
      4 TSs bracketing two tetrahedral intermediates and the
      covalent acyl-enzyme well. Distinctive "double-hump"
      shape: the acyl-enzyme sits BELOW the Michaelis complex
      (acylation half favourable; deacylation half does the
      remaining work). Both tetrahedral intermediates sit
      above the Michaelis complex but below the highest TS —
      the oxyanion-hole stabilisation point. Covalent
      catalysis splitting one ~80-kJ/mol solution barrier into
      two ~50-kJ/mol enzyme barriers gives the textbook
      kcat/Km enhancement of ~10¹⁰.
      **Friedel-Crafts alkylation (round 106 — CLOSES Phase 31e)**
      — second EAS profile. Pairs with the round-101 nitration
      curve. Distinctive shape: an extra pre-equilibrium TS
      for CH₃⁺ generation via AlCl₃·Cl⁻ abstraction, landing
      in a genuine endergonic free-cation minimum (+25 kJ/mol)
      BEFORE the standard Wheland cycle. That "cation is real
      and unstable" shape is *why* FC alkylation rearranges
      (1° → 2°/3° via H-shift) and over-alkylates (toluene is
      more nucleophilic than benzene) — a textbook failure
      mode that nitration does not share.
      **Catalogue 20/20 — phase CLOSED.** Priority list: 11 more reaction-coordinate
      diagrams. Priority: Diels-Alder endo/exo comparison, Wittig,
      Aldol (enolate vs enol), Claisen, Michael, Heck (β-hydride
      elimination as RDS), Buchwald-Hartwig (oxidative-addition
      RDS), SN2 on 1° / 2° / 3° halides (3-way comparison),
      retro-Diels-Alder. Each with proper Ea / ΔH / ΔG values from
      textbook references.
- [x] **31f. Glossary → 80. COMPLETE (round 77).** Round-63
      batch added hyperconjugation, inductive effect, leaving
      group, enantiomeric excess (ee), keto-enol tautomerism,
      homolysis vs heterolysis, Walden inversion, anomer.
      Round-77 batch closed the target: **Activating &
      deactivating groups** (with ortho/para vs meta EAS
      directing), **Regioselectivity** (vs chemo/stereo),
      **Constitutional isomer** (with 4 sub-type taxonomy).
      Catalogue now **80 / 80**.  Glossary `SEED_VERSION` bumped
      to 8 so existing DBs pick up the new rows on next launch.
      Follow-up: continue-batching earlier round's backlog:
      kinetic vs thermodynamic
      Markovnikov, Saytzeff / Hofmann elimination, anti-periplanar
      geometry, Diels-Alder endo rule, Woodward-Fieser rules,
      tautomerism vs resonance, conformational analysis terminology
      (gauche / anti / eclipsed / staggered), etc. Each gets an
      example_smiles → figure via the Phase 26a pipeline.
- [x] **31g. Tutorials → 30. COMPLETE (round 93).**
      Final distribution: 8 beginner / 10 intermediate /
      6 advanced / 6 graduate.  Rounds 82-93 shipped:
      intermediate/08 Radicals, graduate/05 Catalysis,
      intermediate/09 Polymers, beginner/07 Stereochem 101,
      advanced/05 Green chemistry, intermediate/10
      Protecting groups, beginner/08 Reading SMILES,
      graduate/06 Biosynthesis, **advanced/06 Flow &
      process chemistry** (round 93).  Pre-round-82 seeded
      lessons (acid-base, sugars, nomenclature, structures,
      atoms, welcome, pericyclic, organometallics,
      retrosynthesis, spectroscopy, named reactions,
      asymmetric, MO theory, total synthesis,
      stereochemistry R/S, SN, E, aromaticity, carbonyl,
      energetics) round out the 30.  Pre-empted priorities
      (metal-catalysed C-H activation, flow-specific
      Merck-Codexis deep dive) left for a future phase if
      depth is ever needed.
      beginner (stereochemistry 101, acid-base practice,
      retrosynthesis primer), intermediate (pericyclic warm-up,
      organometallic coupling survey, total-synthesis walkthrough:
      ibuprofen), advanced (asymmetric catalysis, bioorganic:
      sugars + proteins, green chemistry case studies),
      graduate (metal-catalysed C-H activation, flow chemistry,
      photoredox catalysis). Each lesson carries embedded agent
      action calls so learners can interact with the app from
      inside the lesson.
- [~] **31h. Carbohydrates → 40.** First 10 shipped (glucosamine,
      GlcNAc, glucuronic acid, fucose, rhamnose, sorbitol,
      mannitol, xylitol, tagatose, trehalose) — 25 total; 15 more
      to come. Target list: rare sugars
      (tagatose, psicose, allose), aminosugars (glucosamine,
      N-acetylglucosamine, chitosan), uronic acids (glucuronic,
      galacturonic), deoxy sugars beyond dR (fucose, rhamnose),
      sugar alcohols (sorbitol, mannitol, xylitol, erythritol),
      storage / structural polysaccharides (glycogen fragment,
      chitin, hyaluronic acid disaccharide, heparin disaccharide),
      glycoproteins sample (N-glycan core), sweeteners (aspartame
      — bridges to AA category, saccharin, stevioside, sucralose),
      blood-group glycans (H, A, B epitopes).
- [~] **31i. Lipids → 40.** First 10 shipped (caprylic acid C8:0,
      capric acid C10:0, PGE2, TXA2, cholic acid, taurocholic
      acid, progesterone, cortisol, retinol, α-tocopherol) —
      catalogue now **31**; 9 more to come. Priority list:
      medium-chain fatty
      acids (caproic / caprylic / capric), branched-chain
      (phytanic), hydroxy fatty acids (ricinoleic), eicosanoids
      (PGE2, TXA2, LTB4), plasmalogens, cardiolipin, gangliosides
      (GM1), bile acids (cholic, taurocholic), steroid hormones
      beyond testosterone / estradiol (progesterone, cortisol,
      aldosterone, DHT), lipid-soluble vitamins (A / E / K).
- [~] **31j. Nucleic acids → 40.** First 10 shipped (hypoxanthine,
      xanthine, inosine, pseudouridine Ψ, NADH, NADPH, FAD,
      coenzyme A, SAM, GCGCUUUUGCGC RNA hairpin) — catalogue now
      **33**; 7 more to come. Target list: modified /
      non-canonical bases (inosine, pseudouridine, xanthine,
      hypoxanthine, wobble positions), more nucleotide cofactors
      (NADH, NADPH, FAD, FADH2, coenzyme A, SAM), aptamers sample,
      locked NA (LNA) monomer, phosphorothioate linkage example,
      Z-DNA motif, cruciform / hairpin small examples, pre-miRNA
      example sequence.
- [x] **31k. SAR series → 15. COMPLETE (round 163, 2026-04-25).**  Shipped across rounds 40-163:
      β-blockers (5), ACE inhibitors (5), SSRIs (round 96),
      β-lactam penicillins (round 100), PDE5 inhibitors (round 108),
      Benzodiazepines (round 122),
      **Fluoroquinolones (round 133)** — 5 variants: nalidixic
      acid / norfloxacin / ciprofloxacin / levofloxacin /
      moxifloxacin with E. coli + S. aureus + Pseudomonas MIC.
      Three pedagogical SAR inequalities locked in: (a)
      nalidixic acid (no C-6 F, no C-7 piperazine) is ≥50× weaker
      on E. coli than every fluoroquinolone — the C-6 F + C-7
      piperazine SAR move was worth ~100×; (b) ciprofloxacin
      most potent on E. coli (canonical Gram-negative +
      anti-Pseudomonas workhorse); (c) moxifloxacin best on
      S. aureus BUT worst on Pseudomonas (the C-7 bicyclic-amine
      + C-8 methoxy moves widen Gram-positive at the cost of
      anti-Pseudomonas activity).  Generation-by-generation SAR
      walk that pairs cleanly with the round-100 β-lactam story
      — "what does each substituent buy you?".
      **H1-antihistamines (round 158)** — 6 variants spanning
      all three generations: 1st-gen sedating (diphenhydramine
      / chlorpheniramine / hydroxyzine — all BBB-penetrant),
      2nd-gen non-sedating (loratadine carbamate cap + P-gp
      substrate; cetirizine zwitterion from hydroxyzine COOH
      metabolite), 3rd-gen non-sedating + non-cardiotoxic
      (fexofenadine — the terfenadine COOH metabolite that
      eliminated the hERG / torsades-de-pointes liability
      that pulled terfenadine off the market in 1998).
      **Five pedagogical SAR invariants locked in by tests**:
      (a) all 6 textbook landmark drugs present; (b) 1st-gen
      sedating (sedation_score ≥ 3); (c) 2nd / 3rd-gen
      non-sedating (sedation_score ≤ 1); (d) fexofenadine
      sedation_score = 0 (the truly non-sedating anchor);
      (e) cetirizine sedation_score < hydroxyzine
      (zwitterion vs free-OH BBB-penetration story); (f)
      MW band 250-510 Da, fexofenadine the largest.  Pairs
      pedagogically with the round-96 SSRI series as a
      "physico-chemical-properties drive CNS-penetration"
      teaching theme — both stories about how rational
      tweaks (zwitterion / BBB / hERG) turned 1st-gen
      drugs with off-target liabilities into 2nd / 3rd-gen
      best-in-class agents.
      **PPI inhibitors (round 159)** — 5 variants:
      omeprazole (prototype racemate, Astra 1988) /
      esomeprazole (the (S)-enantiomer chiral switch,
      AstraZeneca 2001 — pairs with the SSRI series's
      citalopram → escitalopram chiral switch as the two
      textbook examples of single-enantiomer-from-racemic
      patent-extension paradigm) / lansoprazole
      (Takeda 1991, fluoroethoxy variant) / pantoprazole
      (Byk Gulden 1985/1995, 5-OCHF₂ + 4-OMe — **least
      drug-drug interactions** of any PPI thanks to Phase-II
      sulfotransferase metabolism dominating over CYPs) /
      rabeprazole (Eisai 1999, 3-methoxypropoxy — **fastest
      onset** in the class thanks to higher benzimidazole N
      pKa enabling activation at higher intracellular pH).
      Five pedagogical SAR invariants locked in: (a) all 5
      landmarks present; (b) chiral-switch story (eso ==
      ome MW + logP, but eso has lower CYP dependence and
      ≥ duration); (c) pantoprazole has the lowest CYP
      dependence in the class; (d) rabeprazole has the
      fastest onset; (e) MW band 340-385 Da typical for the
      2-(pyridinylmethylsulfinyl)-1H-benzimidazole template.
      Catalogue now **11/15**.
      **Opioid analgesics (round 160)** — 5 variants
      spanning natural / semi-synthetic / synthetic
      chemotypes: morphine (Sertürner 1804, the natural-
      product prototype + reference for opioid potency) /
      codeine (Robiquet 1832, the **CYP2D6-pro-drug** with
      μ-Ki ~ 200 nM but ~ 10% in-vivo conversion to
      morphine — explains FDA boxed warning for
      paediatric use after deaths in fast metabolisers) /
      hydromorphone (Knoll 1924, semi-synthetic with the
      lowest direct μ-Ki ~ 0.4 nM + cleaner PK in renal
      failure) / oxycodone (Freund + Speyer 1916, semi-
      synthetic from thebaine; oral bioavailability ~ 60-87%
      via 14-OH + 6-keto + 3-OMe combination; OxyContin =
      drug at the centre of US opioid crisis) / fentanyl
      (Janssen 1960, total chemotype switch to 4-anilido-
      piperidine; ~ 100× morphine on weight basis driven
      by logP 4.1 vs morphine's 1.2 → 10-100× faster BBB
      penetration — **THE textbook lipophilicity → potency
      teaching example**, drives illicit-fentanyl-analogue
      epidemic).  Six pedagogical SAR invariants locked in:
      (a) all 5 landmarks present; (b) fentanyl is the
      high-potency anchor; (c) codeine is the pro-drug
      anchor (direct Ki ≥ 50× morphine's); (d) hydromorphone
      has the lowest direct μ-Ki; (e) lipophilicity → potency
      invariant — fentanyl logP ≥ 2 units higher than
      morphine and ≥ 50× potency advantage; (f) codeine
      MW exceeds morphine MW by exactly one methyl group
      (~ 14 Da, the 3-OMe ether).  Catalogue now **12/15**.
      **Anticonvulsants (round 161)** — 5 variants spanning
      4 distinct chemotypes for the same broad indication
      (epilepsy): phenytoin (5,5-diphenylhydantoin; Merritt
      + Putnam 1938) / carbamazepine (dibenzazepine
      tricyclic; Geigy 1962) / valproate (branched fatty
      acid; Meunier 1962 serendipitous discovery; broad-
      spectrum + **CYP INHIBITOR** opposite of phenytoin /
      carbamazepine inducers) / lamotrigine (phenyltriazine;
      GSK 1990; SJS / TEN risk on rapid titration mandates
      6-week slow titration) / levetiracetam (pyrrolidone;
      UCB 1999; **first-in-class** SV2A vesicular-protein
      binder — totally distinct mechanism from Na+-channel
      blockers).  **Six pedagogical SAR invariants locked
      in by tests**: (a) all 5 landmarks present; (b)
      different-scaffolds-for-the-same-biology theme — MW
      range 144-256 Da, span > 100 Da proves chemotype
      diversity vs the family-walk pattern of H1 / PPI /
      opioids; (c) phenytoin + carbamazepine are strong CYP
      inducers; (d) valproate has CYP-induction-score < 0
      (INHIBITOR, opposite direction); (e) levetiracetam is
      the only entry that does NOT block Na+ channels (SV2A
      mechanism); (f) valproate + levetiracetam are the two
      broad-spectrum entries.  **Opens the "different
      scaffolds for the same biology" teaching theme** — the
      complement to the family-walk patterns of the
      preceding rounds.  Catalogue now **13/15**.
      **Direct-oral-anticoagulants (DOACs, round 162)** —
      5 variants spanning the modern Xa- vs IIa-inhibitor
      landscape that displaced warfarin: apixaban (Eliquis,
      BMS/Pfizer 2012; **most-potent Xa Ki 0.08 nM**;
      safest in CKD with only 25% renal clearance) /
      rivaroxaban (Xarelto, Bayer 2008; first DOAC to
      market; food-dependent bioavailability that mandates
      dosing with meals) / edoxaban (Lixiana, Daiichi
      Sankyo 2011; paradoxical "bioavailability decreases
      at high renal clearance" — boxed-warned NOT for
      atrial fibrillation when CrCl > 95 mL/min) /
      dabigatran (Pradaxa, Boehringer Ingelheim 2010;
      **only seeded factor-IIa thrombin inhibitor**;
      amidine + carboxylate zwitterion at physiological
      pH gives potent IIa binding but destroys oral
      bioavailability — only 6.5% as free dabigatran) /
      dabigatran etexilate (the **double-prodrug** that
      caps both polar groups with hexyloxy-carbamate +
      ethyl-ester — raises logP 3.0 → 5.6 and MW 471 →
      628 Da; esterases in the gut wall + blood hydrolyse
      both caps to release active dabigatran).  **Six
      pedagogical SAR invariants locked in by tests**:
      (a) all 5 landmark entries present; (b) Xa-vs-IIa
      target diversity (3 Xa + 2 IIa entries); (c) apixaban
      has the lowest factor-Xa Ki; (d) **prodrug logP
      story** — dabigatran etexilate logP ≥ 2 units
      higher than active dabigatran; (e) **prodrug MW
      story** — dabigatran etexilate ≥ 100 Da heavier
      from both lipophilic caps combined; (f) all 3 Xa
      inhibitors have higher oral bioavailability than
      free dabigatran (the whole reason the etexilate
      prodrug exists).  Catalogue now **14/15**; just 1
      more series to close at the 15/15 milestone.
      **DPP-4 inhibitors (round 163)** — 5 variants of the
      modern incretin-pathway antidiabetic class: sitagliptin
      (Januvia, Merck 2006; first to market + still
      best-selling gliptin worldwide; non-covalent
      competitive inhibitor) / saxagliptin (Onglyza, BMS/AZ
      2009; **covalent reversible** via cyanopyrrolidine
      warhead reacting with Ser-630; lowest nM-band IC50;
      SAVOR-TIMI 53 heart-failure-hospitalisation signal) /
      linagliptin (Tradjenta, BI/Lilly 2011; **xanthine
      scaffold** — total chemotype switch; **only gliptin
      with primarily fecal clearance — no dose adjustment
      in CKD or ESRD**, the only one safe in haemodialysis
      patients) / alogliptin (Nesina, Takeda 2013; uracil-
      based scaffold; lowest logP in the series at 0.4) /
      vildagliptin (Galvus, Novartis 2007; **EU-approved but
      NOT FDA-approved** due to heart-failure + transient
      liver-enzyme concerns; same covalent-cyanopyrrolidine
      mechanism as saxagliptin via a glycyl spacer instead
      of α-amino-acyl).  **Seven pedagogical SAR invariants
      locked in by tests**: all 5 landmarks present;
      covalent-vs-non-covalent split (2 covalent + 3 non-
      covalent); linagliptin is the only gliptin with low
      renal clearance ≤ 10%; the other 4 all require ≥ 20%
      renal clearance dose adjustment in CKD; covalent
      inhibitors have short half-lives ≤ 3 h (compensated
      by sustained tissue inhibition); linagliptin +
      saxagliptin are the two most-potent gliptins (≤ 2 nM
      IC50) by very different routes (xanthine deep-pocket
      fit vs covalent warhead); the other 3 sit in the
      2-30 nM band.  **🎉 Phase 31k CLOSED at the 15/15
      milestone — original Phase 31 vision for SAR series
      fully realised.**  Six new series shipped in rounds
      158-163: H1-antihistamines, PPI inhibitors, opioid
      analgesics, anticonvulsants, DOACs, DPP-4 inhibitors.
      Five major medicinal-chem teaching themes opened
      across these rounds: chiral switch (SSRI + PPI),
      zwitterion / BBB blockade (H1), lipophilicity →
      potency (opioids), different scaffolds for the same
      biology (anticonvulsants), prodrug for bioavailability
      (DOAC dabigatran etexilate).
      Three teaching points
      encoded: (a) vardenafil most potent (regioisomeric
      scaffold + N-Et piperazine); (b) tadalafil is the
      long-half-life outlier (β-carboline chemotype switch,
      17.5 h vs 4 h) — the classic "weekend pill" story;
      (c) tadalafil also has the best PDE6 selectivity (~700×)
      so the chemotype switch resolves both half-life AND
      visual-disturbance liabilities simultaneously.
      Catalogue now **7**; 8 more medicinal-chem families
      to come:
      β-lactam antibiotics, β-blockers, ACE inhibitors,
      benzodiazepines, phenothiazines, PDE5 inhibitors (sildenafil
      analogs), kinase inhibitors (imatinib / dasatinib analogs),
      SSRIs, opioids, antihistamines (H1 / H2), cannabinoid
      analogs, aromatase inhibitors, retinoids.
- [x] **31l. Proteins → 15. COMPLETE (round 116).**
      Shipped across rounds 44-116:
      lysozyme 1LYZ, myoglobin 1MBN, GFP 1EMA,
      haemoglobin 1HHO R-state (round 107),
      KcsA potassium channel 1BL8 (round 114),
      nucleosome 1AOI + IgG 1IGT (round 115),
      **bovine α-chymotrypsin 5CHA + SARS-CoV-2 main protease 6LU7
      (round 116 — CLOSES the phase at 15/15).**  5CHA completes
      the round-62 chymotrypsin-mechanism + round-105 energy-
      profile + now-structure teaching triad for the most-taught
      serine protease in biochemistry.  6LU7 (Jin/Yang/Rao 2020
      *Nature*) is the first SARS-CoV-2 Mpro structure — pairs
      pedagogically with the 1HPV HIV protease entry to contrast
      cysteine-protease covalent catalysis (Cys145-His41, covalent
      warhead → nirmatrelvir/Paxlovid) against aspartic-protease
      non-covalent peptidomimetic inhibition (HIV Mpro + ritonavir).
      **Catalogue 15/15 — phase CLOSED.**  Earlier round-115
      content:  1AOI (Luger /
      Richmond 1997 *Nature* 389:251) captures 147 bp of DNA
      wrapped 1.65× around the H2A/H2B/H3/H4 histone octamer —
      foundation for every nucleosome-positioning + histone-tail
      modification story.  1IGT (Harris / Edmundson 1997
      *Biochemistry* 36:1581) is the first complete IgG at 2.8 Å
      — Y-shaped heavy+light tetramer held together by conserved
      disulfides + Fc interactions, with the Asn297 glycan that
      gates Fc-receptor engagement on display (the entire
      biological-drug glycoengineering arc starts here).
      Catalogue now **13**; 2 more to close the phase: chymotrypsin
      alt form + kinesin motor (or another pedagogically-rich pick).

Shipping cadence: ~1 sub-item per round, interleaved with code
phases. Each sub-item ships its own tests and ROADMAP check-box,
updates `INTERFACE.md` / `PROJECT_STATUS.md` counts, and graduates
the seed version so users on older DBs get the additive upgrade
on next launch.

---

## Phase 32 — Scripting workbench & dynamic scene composer *(NEW — planned 2026-04-23; user-flagged)*

User directive (2026-04-23): *"Add a Python script editor and
console that can serve as a macro for running any element of the
app. It will also be able to run a dynamic viewer window that can
be populated with any molecule, protein, ligand, lipid, nucleic
acid etc — and then manipulated to zoom, rotate, display
molecular dynamics, interactions between multiple molecules, and
can be used to demonstrate any of the reactions and interactions
described elsewhere in the app. The scripts will be able to be
generated by the user or by the LLMs. Several sample scripts will
be created … demonstrating dynamic examples from all of the
different modules and sections."*

### Why this lands naturally on the current architecture
Every GUI click and every LLM tool-call already routes through
the `@action` registry in `orgchem/agent/library.py` (and
sibling `actions_*.py` modules). A user-facing Python REPL
therefore does *not* invent a new API surface — it exposes the
existing registry as `app.call(action_name, **kwargs)` plus
direct `from orgchem.* import …` imports. The LLM tutor already
drives this surface; humans just get the same keys. The
**new** piece is a **scene composer** — a Workbench viewer
that is a scene graph of composable tracks (small-molecule /
protein / ligand / polymer / trajectory / arrow-overlay) with
its own command API. Existing renderers
(`render/draw3d.py`, `render/draw_protein_3d.py`) handle
single-target cases; the composer layers on top via a single
QWebEngineView + 3Dmol.js page driven by a JSON command channel
that extends the Phase-24l QWebChannel bridge (picked atoms
flow Qt-ward; scene mutations flow JS-ward).

### Key design decisions that need locking in before 32a code lands
- **Execution model** — inline REPL (live eval) **and**
  saved-file "run script" (same pattern as PyMOL's command
  line + `.pml` files). Both share one `ScriptContext` globals
  dict so state persists between runs (`v = viewer.add_protein(...)`
  stays resolvable in the next line).
- **Scene composition** — the Workbench viewer is a **scene
  graph** keyed by track name: add / remove / restyle / highlight /
  animate. Each GUI control on the right-side panel mirrors one
  scene-API call, so every interaction can be copied into the
  editor as a script line. (Same "every click is a script"
  principle that made PyMOL's interaction-log so useful for
  teaching.)
- **Thread safety** — scripts execute on a worker thread
  (`utils/threading.py`). GUI touches route through the
  `run_on_main_thread` / `run_on_main_thread_sync` helpers from
  rounds 55-57 so the NSWindow / QTimer constraints are already
  solved.
- **LLM integration** — the tutor gets a "Reply with a script"
  toggle. When on, the system prompt instructs the model to emit
  a fenced ```python block against `ScriptContext` globals; the
  block drops into the editor for the user to run / edit.
  Orthogonal to tool-use: the LLM can still answer one-shot
  questions directly, and can mix both in the same reply.
- **Safety posture** — full-trust local execution, same as
  PyMOL `.pml` or Jupyter notebooks. We do NOT sandbox at the OS
  level. The script library is read-only; user scripts live in
  `platformdirs.user_data_dir / "scripts"`.

### Sub-phases (incremental, each shippable alone)

- [x] **32a. Script editor + REPL dialog.** *(round 64 — shipped 2026-04-23.)*
      `agent/script_context.py` owns the headless half: `ScriptContext`
      + `ExecResult` + `AppProxy` + `WorkbenchNotReadyError` stub for
      the not-yet-wired `viewer` global. `gui/dialogs/script_editor.py`
      — `ScriptEditorDialog` subclass of `QMainWindow` (floating,
      detachable, multi-instance optional).
      - Editor pane: Python syntax highlighting via `QSyntaxHighlighter`
        (tabs for mono-file keep RDKit a real tool, not a
        pretty-printer). Keyboard: Ctrl+Enter runs current
        line / selection; Ctrl+Shift+Enter runs whole buffer.
      - Output pane: stdout / stderr / repr of last expression
        + tracebacks with file-path hyperlinks.
      - Pre-imported globals: `app` (agent-registry proxy with
        `.call(name, **kw)` + every registered action as a direct
        attribute), `chem` (RDKit), `orgchem` (the full package),
        `viewer` (current Workbench scene; creates one lazily on
        first use).
      - File menu: Open / Save / Save-as `.py`; recent-files list;
        Open example… sub-menu populated from the 32d library.
      - Wired into *Tools → Script editor… (Ctrl+Shift+E)* and via
        an `open_script_editor()` agent action (so the LLM can
        launch it for the user).
- [x] **32b. Dynamic scene viewer (Workbench) — HYBRID placement
      (user directive 2026-04-23 round 65).** *(MVP shipped round 66.)*
      `orgchem/scene/` holds the headless Scene class + HTML
      builder; `gui/panels/workbench.py` is the reparentable
      widget; `gui/windows/workbench_window.py` hosts it when
      detached.  Main tabbar gets a "Workbench" tab immediately
      after Molecule Workspace; Detach-as-window / Reattach-as-tab
      reparent the same widget instance (no Scene loss).
      ScriptContext graduates `viewer` from its 32a stub to the
      process-wide Scene.  Follow-ups (defer to 32c): Arrow
      overlays, trajectory tracks, programmatic rotate/zoom/spin,
      highlight(), set_style chrome in the tracks-list UI.
      Default: the
      Workbench renders as a **main-tabbar tab** ("Workbench",
      positioned immediately after *Molecule Workspace*).
      A toolbar **"Detach as window"** button reparents the
      Workbench widget into a `QMainWindow` (`WorkbenchWindow`)
      when the user wants it on a second monitor / side-by-side
      with the Script Editor; a **"Reattach"** button in the
      detached window moves it back into the main tabbar. The
      Workbench widget is therefore defined as a standalone
      `QWidget` subclass (`WorkbenchWidget`) that can parent into
      either host — this is the same pattern Qt uses for
      detachable dock widgets but extended to tab / window.
      Placement preference persists via QSettings
      (`window/workbench/detached` bool + geometry).
      - **Layout** (same in both placements): 3Dmol.js
        QWebEngineView (centre) + tracks dock (right) + timeline
        dock (bottom, hidden until a trajectory-type track is
        added).
      - **Scene API** (`orgchem/scene/scene.py`, new module):
        ```python
        scene.add_molecule(mol_or_smiles, *, track="t1",
                           style="stick", colour="cpk", opacity=1.0)
        scene.add_protein(pdb_id_or_text, *, track,
                          style="cartoon", colour_mode="chain",
                          show_waters=False)
        scene.add_ligand_from_pdb(pdb_id, residue_name,
                                  *, track, style)
        scene.add_trajectory(xyz_frames, *, track, fps, loop)
        scene.add_arrows(arrow_list, *, track)   # mechanism overlays
        scene.rotate(x, y, z)    # degrees, absolute or delta
        scene.zoom(factor)
        scene.spin(axis="y", speed=1.0)
        scene.highlight(track, atoms=[…], colour="yellow")
        scene.set_style(track, style="sphere")
        scene.remove(track)   / scene.clear()
        scene.snapshot(path)  / scene.export_gif(path, n_frames)
        ```
      - Commands serialise to a single-page 3Dmol.js scene via
        a JSON command channel (extension of the Phase-24l
        QWebChannel bridge).
      - Agent action `open_workbench(tab)` opens / focuses the
        window.
- [x] **32c. Track-aware controls GUI.** *(shipped round 69;
      round-85 polish closed the deferred chrome.)*
      `gui/panels/workbench_track_row.py::TrackRow` per row:
      visibility checkbox, bold name label (auto-subtitled with
      SMILES / PDB ID), kind-specific style combo, **colour
      combo + swatch preview with "custom…" → QColorDialog**
      (round 85), **opacity slider 10-100 %** (round 85), ✕
      remove button.  `WorkbenchWidget` toolbar: Fit-to-view,
      Toggle bg (dark ↔ light), Clear, Snapshot PNG…, Export
      HTML….  Round 85 also refactored `scene/html.py::_style_js`
      to build the 3Dmol.js style dict programmatically and
      inject `opacity` consistently across all style modes.
      Deferred to a future round: drag-reorder for the tracks
      list.
      each track with its own row: visibility checkbox, style
      combo, colour swatch, opacity slider, delete button, drag
      handle to reorder. Scene-wide controls: camera reset,
      fit-to-view, spin toggle, background colour. Timeline
      scrubber binds to whichever trajectory track is
      foregrounded. Every control emits its equivalent
      scene-API call to the editor's history log so the user
      can copy-paste "what just happened" back into a script.
- [x] **32d. Script library — 15/15 COMPLETE (rounds 67, 70, 72, 73).**
      `data/script_library/` + `tests/test_script_library.py`
      (headless `ScriptContext` path) + `tests/test_script_library_gui.py`
      (real `ScriptEditorDialog` + `_RunWorker` QThread path via
      pytest-qt, per user directive 2026-04-23).  Shipped so far:
      **01_caffeine_tour**, **02_scene_composer_basics**,
      **03_nsaids_overlay**, **04_mechanism_walkthrough**,
      **05_lipid_mw_report**, **06_retrosynthesis_demo**,
      **07_aspirin_pathway**, **08_stereochem_tour**,
      **09_energy_profile_diels_alder**, **10_huckel_benzene**,
      **11_nsaid_sar**, **12_macromolecule_catalogue**,
      **13_butane_dihedral**, **14_retrosynthesis_tree**,
      **15_glossary_tour**.  Phase 32d target hit exactly.
      Round 71 added ``_CONTENT_MARKERS`` per-demo so silent-zero
      bugs fail loudly (proved with a negative-case test).
      All under
      `data/script_library/`, listed alphabetically:
      1.  `01_caffeine_tour.py` — load caffeine, print full
          descriptor row, save 2D PNG + IR + ¹H NMR stick plots.
      2.  `02_sn2_trajectory.py` — build CH₃Br + OH⁻, render the
          Phase-2c.2 trajectory in the Workbench as an animated
          track, auto-rotate while playing.
      3.  `03_caffeine_a2a_docking.py` — `fetch_pdb("2YDO")` + show
          the bound CAF ligand, run `analyse_binding`, overlay the
          PoseView-style interaction map in a second panel.
      4.  `04_diels_alder_energy.py` — load the seeded energy
          profile, render the reaction-coordinate diagram, jump the
          Workbench camera to each stationary point's 3D structure.
      5.  `05_steroid_family_compare.py` — testosterone / estradiol /
          progesterone / cortisol / cholesterol in one Workbench
          scene, aligned on the shared steroid scaffold; print a
          descriptor table.
      6.  `06_hiv_protease_ppi.py` — load 1HXW, colour chains A/B
          distinctly, compute the PPI interface (Phase 24j), stick-
          render interface residues.
      7.  `07_dna_intercalation.py` — doxorubicin-DNA complex:
          run `analyse_na_binding`, render with the ligand in a
          groove view, slow auto-rotate.
      8.  `08_butane_dihedral_morph.py` — conformational dynamics
          dihedral scan, Workbench-animated, with a matplotlib
          energy-vs-dihedral side panel.
      9.  `09_wheland_mechanism.py` — step through the nitration-
          of-benzene mechanism (round-60 seed), animating each
          curly-arrow overlay for 2 s.
      10. `10_ester_green_metrics.py` — Fischer esterification:
          pretty-print the atom-economy table, E-factor for two
          solvent choices (neat vs toluene).
      11. `11_hammett_fit.py` — fit ρ for a bundled
          p-substituted benzoic-acid dataset; plot log(K/K₀)
          vs σₚ with the fit line.
      12. `12_glucose_anomers.py` — α- vs β-D-glucose overlaid in
          the Workbench; highlight the anomeric carbon; animate
          a chair-flip morph.
      13. `13_nsaid_sar.py` — pull the seeded NSAIDs SAR series,
          export the matrix figure, print a COX-1 / COX-2
          selectivity correlation.
      14. `14_lipid_mw_chainlength.py` — iterate the Lipid
          catalogue, plot MW vs chain length coloured by
          unsaturation count.
      15. `15_aspirin_retro.py` — multi-step retro tree for
          aspirin, render each disconnection's scheme, save a
          composite report PDF.
      Surfaces via *Editor → File → Open example…* and via a
      headless-replay CLI so the whole library becomes part of
      the CI smoke-test.
- [x] **32e. LLM script generation.** *(shipped round 74.)*
      `agent/conversation.py::_SCRIPT_MODE_ADDENDUM` +
      `build_script_mode_system_prompt()` append a Phase-32e
      briefing to the base prompt: ScriptContext globals
      (`app` / `chem` / `orgchem` / `viewer`), Scene API
      (`add_molecule` / `add_protein` / `remove` / `clear`),
      and the fenced ```python block contract.  Tutor panel
      gains a **"Reply with a script"** checkbox that swaps
      the live `Conversation.system_prompt` on toggle (or at
      Connect time if pre-ticked).  When a reply contains
      fenced ```python blocks, each gets a dark monospace
      preview div + a **▶ Run in Script Editor** anchor
      (`orgchem-script:<idx>` URL scheme).  Clicking the
      anchor loads the block into the singleton
      ScriptEditorDialog.  Blocks never auto-run.  12 new
      tests (6 extractor unit tests + 3 system-prompt builder
      tests + 3 pytest-qt integration tests).

**Phase 32 — CLOSED.**  Scripting workbench + scene composer
shipped across 32a (editor) · 32b (Workbench + Scene API) ·
32c (track chrome) · 32d (15-demo library) · 32e (tutor
script mode).  All five sub-phases ✅.

### Out of scope (deferred unless a later phase adds them)
- Script package management / PyPI install — single-file
  artefacts only, using `orgchem.*` and the standard library.
- Multi-user gallery / cloud sync — local only.
- OS-level sandboxing — full-trust, same posture as PyMOL.
- Interactive debugger / breakpoints — tracebacks only; add if
  users ask.

### Tests + docs contract
- Unit tests for `ScriptContext` (eval, save / restore globals,
  traceback capture).
- Unit tests for `Scene` API with a fake 3Dmol.js channel.
- Headless smoke test that runs each of the 15 library scripts
  under `HeadlessApp` and asserts they complete without raising.
- `INTERFACE.md` grows a `scene/` subpackage row and a
  `gui/dialogs/script_editor.py` row.
- GUI-audit pin (Phase 25a) adds `open_script_editor` +
  `open_workbench` actions; coverage must stay at 100 %.

---

## Phase 33 — Cross-surface full-text search *(NEW — 2026-04-23; started round 88)*

Natural extension of the Phase-11b Ctrl+K command palette.
Palette does **name-matching only** (jump to a known molecule /
reaction / glossary term by typing its name); this phase adds
**full-text search** over every text-bearing column in the
seeded DB — descriptions, step notes, glossary definitions,
mechanism-step prose.  A user asking *"where do we discuss
Beckmann?"* should land on the Nylon-6 pathway step 2 +
the adjacent prose without having to know the exact entry
title.

### Sub-phases

- [x] **33a. Headless search core + agent action (round 88).**
      - `orgchem/core/fulltext_search.py` — pure-Python linear
        scan over Molecule / Reaction / SynthesisPathway +
        SynthesisStep / GlossaryTerm tables + mechanism_json
        step list.  `SearchResult` dataclass, `search(query,
        kinds, limit)`.  Title-boost scoring + word-boundary
        bonus + snippet excerpt.
      - `orgchem/agent/actions_search.py` — `fulltext_search`
        agent action with comma-separated kinds filter and
        clean error-return for unknown kinds.
      - 19 unit tests + integration test; GUI audit entry
        provisionally maps to *View → Find… (Ctrl+F)* ahead of
        33b.

- [x] **33b. Ctrl+F Find dialog (shipped round 89).**  New
      `gui/dialogs/fulltext_search.py::FulltextSearchDialog`
      (singleton).  Live-updating query box with 100 ms debounce,
      5-kind checkbox-filter row, results list rendering kind
      badge + bold title + snippet as HTML per row.  Module-level
      `dispatch_search_result(result, main_win)` routes all 5
      kinds — molecule (bus.molecule_selected), reaction
      (`reactions._display`), mechanism-step (same + fires
      `open_mechanism` via the agent registry to pop the player
      dialog), pathway (`synthesis._display`), glossary
      (`glossary.focus_term`).  Wired into *View → Find…*
      (Ctrl+F) in `MainWindow`.  10 new pytest-qt tests (empty
      state, live-search, kind-filter restricts results,
      zero-kinds helpful message, + 6 dispatch-routing unit
      tests via a fake main-window).

- [x] **33c. Surface-integrated search (shipped round 95).**
      Added a `"Full text"` `QCheckBox` next to the existing
      filter box on the **Reactions** tab
      (`reaction_workspace.py`) and **Synthesis** tab
      (`synthesis_workspace.py`).  When unchecked — legacy SQL
      name / category substring filter (unchanged).  When
      checked — `_on_filter` routes through
      `core/fulltext_search.search()`:
      - Reactions: `kinds=["reaction", "mechanism-step"]`,
        collapsing step-note hits onto their parent reaction id
        so a query like *"oxime"* or *"Wheland"* lands on the
        mechanism-bearing reaction rather than repeated rows.
      - Synthesis: `kinds=["pathway"]`, so pathway descriptions
        + step reagents / conditions / notes are searched.
      Both panel models gained a sibling `reload_ids(ids)`
      method that preserves ranked order via a single
      `WHERE id IN (…)` query.  Glossary tab was scoped out —
      its `_TermListModel.reload()` already ILIKEs
      `definition_md`, making a toggle redundant.
      8 new pytest-qt tests
      (`tests/test_fulltext_filter_toggle.py`): default
      name-filter baseline, toggle-on finds step-note-only hits
      ("Raney" → BHC Ibuprofen pathway), empty-query fallback,
      ranked-order preservation in `reload_ids`.  Full-suite
      regression: 958 passing.

---

## Phase 37 — Qualitative inorganic + clinical lab tests *(NEW — 2026-04-25; user-flagged)*

User directive (2026-04-25): two new pedagogical tools —
(a) basic qualitative inorganic tests (flame, hydroxide,
halide, sulfate, carbonate, ammonium, common gas tests)
and (b) basic clinical-chemistry lab panels (Basic
Metabolic Panel, Comprehensive Metabolic Panel, Lipid
Panel).

Pedagogical scope.  Both tools are explicitly "what does
a wet-lab observation tell you?" reference panels — they
don't *simulate* the chemistry, they *describe* it.  The
target audience is undergraduate organic / biochem
students learning to associate ions / analytes with the
diagnostic procedure that detects them.  Each entry
carries enough context (procedure, positive observation,
common interferences for inorganic; normal range,
clinical significance for clinical) that a student can
reproduce a teaching demo or interpret a lab result
sheet without leaving the app.

### 37a — Qualitative inorganic tests
- [x] **Headless catalogue + dialog + agent action — shipped (round 136).**
      `orgchem/core/qualitative_tests.py` with
      `InorganicTest` dataclass + 32-entry catalogue across
      7 categories (flame / hydroxide / halide / sulfate /
      carbonate / ammonium / gas).  Dialog at
      `orgchem/gui/dialogs/qualitative_tests.py` with category
      filter + colour-swatch for visible results.  Agent
      actions `list_inorganic_tests(category)`,
      `get_inorganic_test(test_id)`,
      `find_inorganic_tests_for(target)` in
      `orgchem/agent/actions_qualitative.py`.  Wired into
      *Tools → Qualitative inorganic tests…* (Ctrl+Shift+Q).
      Tests in `tests/test_qualitative_tests.py` (catalogue
      contents + filter + lookup) +
      `tests/test_qualitative_dialog.py` (UI + signal flow).

### 37b — Clinical lab tests (BMP / CMP / Lipid)
- [x] **Headless catalogue + dialog + agent actions —
      shipped (round 137).**  `orgchem/core/clinical_panels.py`
      with `LabAnalyte` + `LabPanel` frozen dataclasses;
      21 unique analytes across 7 categories
      (electrolyte / kidney / liver / lipid / metabolic /
      hormone / vitamin) reused by 6 seeded panels:
      **BMP** (8 analytes: glucose / Ca / Na / K / Cl /
      HCO₃ / BUN / creatinine), **CMP** (BMP + 6: ALT /
      AST / ALP / bilirubin / albumin / total protein),
      **Lipid Panel** (TC / LDL / HDL / TG), **Diabetes
      follow-up** (HbA1c + glucose), **Thyroid** (TSH +
      free T4), **Vitamin D screening** (25(OH)D + Ca).
      CMP literally shares the BMP analyte instances
      (frozen dataclass, identity-equal).  Each analyte
      carries name / abbreviation / units / normal range /
      clinical significance / notes.  Lookup helpers
      `list_panels` / `get_panel(id)` /
      `list_analytes(category)` / `get_analyte(id)` /
      `find_analyte(needle)` (case-insensitive across
      name + abbreviation + id) / `categories()` /
      `analyte_to_dict()` / `panel_to_dict()`.  Dialog at
      `orgchem/gui/dialogs/clinical_panels.py` (singleton,
      modeless): panel-picker combo + meta block +
      per-analyte table + analyte detail pane;
      `select_panel(id)` / `select_analyte(id)`
      programmatic API.  5 agent actions in
      `orgchem/agent/actions_clinical.py` —
      `list_lab_panels`, `get_lab_panel`,
      `list_lab_analytes`, `find_lab_analyte`,
      `open_clinical_panels(panel_id, analyte_id)`.
      Wired into *Tools → Clinical lab panels…*
      (Ctrl+Shift+L).  Tests in
      `tests/test_clinical_panels.py` (29 cases) +
      `tests/test_clinical_panels_dialog.py` (13 cases).

### 37c — Chromatography techniques *(shipped — round 138)*
- [x] **Headless catalogue + dialog + agent actions —
      shipped (round 138).**  `orgchem/core/chromatography_methods.py`
      with `ChromatographyMethod` frozen dataclass + 15-entry
      catalogue across 7 categories: planar (TLC, paper),
      preparative-column (gravity column, flash), gas
      (GC, GC-MS), liquid (HPLC, LC-MS, HILIC), protein
      (FPLC, IEX, SEC, affinity), ion (IC), supercritical
      (SFC).  Each entry surfaces principle / stationary
      phase / mobile phase / detectors / typical analytes /
      strengths / limitations / procedure / notes — the
      strengths-vs-limitations pair is what makes the entry
      pedagogically useful.  Dialog at
      `orgchem/gui/dialogs/chromatography_methods.py`
      (singleton, modeless): category combo + free-text
      filter + list + HTML detail card.  4 agent actions
      in `orgchem/agent/actions_chromatography.py`.  Wired
      into *Tools → Chromatography techniques…*
      (Ctrl+Shift+G).  23 catalogue tests in
      `tests/test_chromatography_methods.py` + 10 dialog
      tests in `tests/test_chromatography_dialog.py`.
      Schematic-diagram SVG / van-Deemter / Rf calculator
      deferred to a 37c.1 polish round if needed.

### 37d — Spectrophotometry techniques *(shipped — round 139)*
- [x] **Headless catalogue + dialog + Beer-Lambert
      calculator + agent actions — shipped (round 139).**
      `orgchem/core/spectrophotometry_methods.py` with
      `SpectrophotometryMethod` frozen dataclass + 12-entry
      catalogue across 5 categories: molecular-uv-vis
      (UV-Vis, fluorescence), molecular-ir (IR/FTIR,
      ATR-FTIR, NIR, Raman, SERS), molecular-chirality
      (CD), atomic (AAS, ICP-OES, ICP-MS), magnetic-
      resonance (NMR).  Each entry surfaces principle,
      light source, sample handling, detector, wavelength
      range, typical analytes, strengths, limitations,
      procedure, notes.  IR + NMR cross-reference the
      existing `core/spectroscopy.py` + `core/nmr.py`
      *predictors* so users see the descriptive vs
      predictive layers integrated in their mental model.
      `beer_lambert_solve(A, ε, l, c)` headless quantitative
      helper — pass any 3 of 4 quantities, get the 4th,
      with positive-input + exactly-one-missing validation.
      Dialog at `orgchem/gui/dialogs/spectrophotometry_methods.py`
      mirrors the Phase-37c chromatography dialog AND adds
      a Beer-Lambert calculator panel (4 spin boxes +
      Solve + Clear + status line).  5 agent actions
      (`list_spectrophotometry_methods`,
      `get_spectrophotometry_method`,
      `find_spectrophotometry_methods`, `beer_lambert`,
      `open_spectrophotometry`).  Wired into *Tools →
      Spectrophotometry techniques…* (Ctrl+Shift+W).
      33 catalogue + Beer-Lambert + agent-action tests in
      `tests/test_spectrophotometry_methods.py` + 14
      pytest-qt dialog tests in
      `tests/test_spectrophotometry_dialog.py`.  Phase 37
      now 4/4 sub-phases complete.

---

## Phase 45 — Lab reagents reference *(SHIPPED 2026-04-25, round 149; user-flagged)*

**Status (round 149): SHIPPED end-to-end.**  Delivered:
- `core/lab_reagents.py` — 75-reagent catalogue across 10
  categories (buffer / acid-base / detergent / reducing-agent /
  salt / protein-prep / stain / solvent / cell-culture /
  molecular-biology), each entry carrying a long-form bench
  card + CAS number.
- `gui/dialogs/lab_reagents.py` — singleton modeless dialog
  with category combo + free-text filter + list + HTML detail
  card (same shape as the Phase-40a Lab Analysers dialog).
  Wired through *Tools → Lab reagents…* (Ctrl+Shift+R).
- `agent/actions_lab_reagents.py` — 4 actions in a new
  `reagent` category (`list_lab_reagents`, `get_lab_reagent`,
  `find_lab_reagents`, `open_lab_reagents`).  CAS searches
  like `find_lab_reagents("67-68-5")` → DMSO work directly.
- 45 new tests in `tests/test_lab_reagents.py`; full suite
  1 798 passing.
- All 4 actions registered in `gui/audit.py`.

### Original scope (kept for reference)

User directive (2026-04-25): *"lab reagents tool"*.

### Pedagogical scope
A reference catalogue of the chemicals + biologicals routinely
ordered as off-the-shelf lab reagents — distinct from the
Phase 6 *molecule database* (which is structure-first) by
keying entries to **how the reagent is used in the lab**:
typical concentration, storage requirements, hazards,
preparation tips, vendor catalogue numbers (representative,
not exhaustive).

### Categories + entries
- **Buffers**: Tris-HCl, HEPES, MOPS, MES, PBS, TBS, citrate,
  carbonate, glycine-HCl, phosphate-citrate (McIlvaine),
  bicarbonate-HCl, BIS-TRIS.
- **Common acids + bases**: HCl 1 M / 6 N, H₂SO₄ conc., HNO₃
  conc., AcOH glacial, NaOH 1 M / 10 N, KOH, NH₄OH conc.
- **Detergents**: SDS, Triton X-100, Tween 20 / 80, NP-40 /
  Igepal CA-630, CHAPS, n-octyl glucoside.
- **Reducing agents**: DTT, β-mercaptoethanol (BME), TCEP,
  glutathione (GSH).
- **Salts**: NaCl, KCl, MgCl₂, CaCl₂, MgSO₄, ammonium sulfate,
  EDTA, EGTA.
- **Protein-prep**: BSA (bovine serum albumin), gelatin,
  protease inhibitor cocktails (PIC, PMSF, leupeptin,
  pepstatin, aprotinin, AEBSF), phosphatase inhibitors
  (sodium fluoride, sodium orthovanadate, β-glycerophosphate).
- **Stains + dyes**: Coomassie (R-250 / G-250), silver nitrate
  (Ag staining), ethidium bromide, SYBR Safe / Green / Gold,
  GelRed / GelGreen, methylene blue, crystal violet.
- **Solvents**: DMSO, DMF, ethanol abs., methanol, acetone,
  chloroform, hexane, THF, dichloromethane (DCM), acetonitrile.
- **Cell-culture media**: DMEM, RPMI-1640, MEM, F-12, IMDM,
  Opti-MEM, FBS / FCS, trypsin-EDTA, antibiotics
  (penicillin-streptomycin), L-glutamine, sodium pyruvate.
- **Molecular-biology reagents**: dNTPs, NTPs, agarose, Taq /
  Pfu / Phusion polymerases, restriction enzymes (EcoRI /
  BamHI / HindIII), T4 DNA ligase, RNase A, DNase I,
  proteinase K.

### Sub-phases
- [ ] **45a — Headless catalogue.**  `core/lab_reagents.py`
      with `LabReagent` frozen dataclass (id / name /
      category / typical_concentration / storage / hazards /
      preparation_notes / cas_number / typical_usage / notes)
      + ~50 entries.
- [ ] **45b — Dialog.**  Singleton modeless dialog at *Tools
      → Lab reagents…* (Ctrl+Shift+R) with category combo +
      filter + list + detail card.
- [ ] **45c — Agent actions.**  `list_lab_reagents` /
      `get_lab_reagent` / `find_lab_reagents` /
      `open_lab_reagents`.

### Risk + scope reality check
Catalogue size is the only knob — 50 entries fit comfortably
in 1 round.  Pure reference data; no quantitative widgets
needed (the existing Phase-39 lab-calculator covers
M₁V₁ = M₂V₂ etc.).

---

## Phase 46 — pH + buffer explorer *(SHIPPED 2026-04-25, round 148; user-flagged)*

**Status (round 148): SHIPPED end-to-end.**  Delivered:
- `core/ph_explorer.py` — 46-acid pKa catalogue across 7 categories
  (mineral / carboxylic / amine / amino-acid / phenol /
  biological-buffer / other), 6 reference cards, 3 solvers
  (`design_buffer`, `buffer_capacity`, `titration_curve`).
- `gui/dialogs/ph_explorer.py` — singleton modeless 4-tab dialog
  (Reference / Buffer designer / Titration curve / pKa lookup)
  wired through *Tools → pH explorer…* (Ctrl+Alt+H).
- `agent/actions_ph_explorer.py` — 7 actions in a new `ph` category
  (`list_pka_acids`, `get_pka_acid`, `find_pka_acids`, `design_buffer`,
  `buffer_capacity`, `simulate_titration`, `open_ph_explorer`).
- 54 new tests in `tests/test_ph_explorer.py`; full suite 1 753
  passing.
- All 7 actions registered in `gui/audit.py`.

### Original scope (kept for reference)

User directive (2026-04-25): *"pH tool (exploring pH concepts
and buffers)"*.

### Pedagogical scope
A focused tool for the most-confused topic in undergraduate
chemistry: pH equilibria + buffer design.  Combines reference
explainers (pH scale, conjugate acid-base pairs, buffer
capacity, polyprotic titrations) with quantitative interactive
widgets that build on the Phase-39a `calc_acid_base.py`
solvers.

### Components

- **Reference cards** — short-form explainers covering:
    - pH definition + autoionisation of water (Kw = 1e-14
      at 25 °C; T-dependence chart).
    - Strong vs weak acid + base behaviour (Henderson-
      Hasselbalch derivation).
    - Buffer capacity β = 2.3 · C_total · α · (1 − α);
      maximum at half-titration (pH = pKa).
    - Polyprotic acids — H₃PO₄ / H₂CO₃ / citric acid
      titration curves, isoelectric point of an amino acid.
    - Common biological buffers + their pH ranges
      (cross-reference Phase 45a buffer entries).
- **Buffer designer widget** — pick conjugate-acid + base + pH
  → calculate the [HA] / [A⁻] mixing ratio (Henderson-
  Hasselbalch) AND the actual mass + volume of stock to mix.
  Surfaces buffer-capacity warnings if the target pH is
  > 1 unit from the chosen pKa.
- **Titration-curve plotter** — dropwise NaOH addition to
  a weak acid; live matplotlib curve update + equivalence-
  point detection.  Shows half-equivalence pH = pKa.
- **pKa lookup table** — 30-50 common acids (acetic,
  formic, citric, phosphoric, carbonic, ammonium, amino-
  acid pKa1/pKa2/pKaR) with pKa values + pH ranges +
  notes.

### Sub-phases
- [ ] **46a — Headless reference + lookup table + buffer
      designer solver.**  `core/ph_explorer.py` carrying
      reference text per topic + a `pKa_TABLE` dict + a
      `design_buffer(target_pH, pKa, total_concentration)
      → {ratio, [HA], [A⁻], mass_HA_g, mass_A_g}` solver.
      Cross-references the Phase-39a Henderson-Hasselbalch
      action.
- [ ] **46b — Dialog.**  Singleton modeless dialog at
      *Tools → pH explorer…* (Ctrl+Alt+H — H for hydrogen).
      Tabbed: reference / buffer designer / titration curve
      / pKa lookup table.
- [ ] **46c — Agent actions.**  `design_buffer` /
      `simulate_titration` / `lookup_pka` /
      `open_ph_explorer`.

### Risk + scope reality check
Likely 2 rounds — 46a (catalogue + buffer-designer solver +
tests) in 1, 46b/c (dialog + agent actions) in 1.

---

## Phase 47 — Biochemistry-by-Kingdom explorer (Macromolecules-style) *(🎉 SHIPPED end-to-end across rounds 166-169, 2026-04-25; user-flagged)*

**Status (round 169): 47a + 47b + 47c + 47d ALL SHIPPED.**

**47a — headless catalogue (round 166)**:
- `core/biochemistry_by_kingdom.py` — `KingdomTopic` frozen
  dataclass + 60 entries spanning all 4 kingdoms × 3
  sub-tabs (15 per kingdom, 5 per (kingdom, subtab) cell).
- Cross-references to Phase-43 cell-components + Phase-42
  metabolic-pathways resolve correctly (test-guarded).
- 33 new tests in `tests/test_biochemistry_by_kingdom.py`.

**47b — GUI window + per-kingdom widget (round 167)**:
- `gui/windows/biochemistry_by_kingdom_window.py` —
  top-level `QMainWindow` opened from *Window → Biochemistry
  by Kingdom…* (Ctrl+Shift+K).  Single persistent instance
  with `QSettings`-persisted geometry + last-active tab.
- `gui/panels/kingdom_subtab_panel.py` — reusable
  `KingdomSubtabPanel` widget hosting the 3 sub-tabs per
  kingdom, plus internal `_SubtabPane` with the filterable-
  list + HTML-detail-card layout.  Detail card auto-shows
  cross-reference sections for Phase-43 cell components +
  Phase-42 metabolic pathways + molecule-DB names where the
  topic carries them.
- `MainWindow.open_biochemistry_by_kingdom_window(kingdom,
  subtab, topic_id)` lazy-constructs the window + supports
  full programmatic navigation.
- 15 new tests in
  `tests/test_biochemistry_by_kingdom_window.py`; full
  suite 2 007 passing.

**47c — agent actions + audit map (round 168)**:
- `agent/actions_biochemistry_by_kingdom.py` — 4 actions in
  a new `kingdom` category (`list_kingdom_topics`,
  `get_kingdom_topic`, `find_kingdom_topics`,
  `open_biochemistry_by_kingdom`).  All filter / lookup /
  cross-reference paths exposed via the agent surface.
- All 4 actions registered in `gui/audit.py`.
- 17 new tests in
  `tests/test_biochemistry_by_kingdom_actions.py`; full
  suite 2 024 passing.

**47d — sub-domain filter on Eukarya tab + plant / animal /
fungus topic expansion (round 169, addressing user
feedback)**:
- New `sub_domain` field on `KingdomTopic` (round-169
  Phase-47d addition; backward-compatible default `""`
  means pan-domain).
- `SUB_DOMAINS` canonical tuple covering animal / plant /
  fungus / protist for Eukarya, gram-positive / gram-
  negative for Bacteria, euryarchaeota / crenarchaeota /
  asgard for Archaea, dna-virus / rna-virus / retrovirus
  for Viruses.  `sub_domains_for_kingdom(k)` helper picks
  the kingdom-specific subset for the GUI.
- `list_topics(kingdom, subtab, sub_domain)` extended with
  the new kwarg.  Pan-domain topics (sub_domain="") match
  any sub-domain query within their kingdom — same
  semantics as Phase-43 cell-component sub-domain queries.
- 8 new explicitly-tagged topics added to the Eukarya tab:
  animal cell-cell junctions (tight + adherens + desmosomes
  + gap), animal nervous system + neurotransmission,
  animal immune system, plant hormones + photoperiodism,
  plant vascular tissue (xylem + phloem), plant polyploidy,
  fungal hyphal growth + secondary metabolism, fungal
  mating types + sexual reproduction.  3 existing topics
  also tagged: photosynthesis (plant), multicellular
  development (animal), Wieland-Miescher steroid context
  topics.
- `KingdomSubtabPanel` GUI extended with a sub-domain combo
  above the inner sub-tabs (kingdom-appropriate label —
  "Kingdom (within Eukarya):" for Eukarya, "Gram-stain
  class:" for Bacteria, "Phylum:" for Archaea, "Genome
  class:" for Viruses).  Combo selection filters all 3
  sub-pane lists simultaneously.
- `list_kingdom_topics` agent action gains the
  `sub_domain` kwarg; clean-error path for unknown
  sub-domain values.
- 13 new tests across `tests/test_biochemistry_by_kingdom.py`
  + `tests/test_biochemistry_by_kingdom_window.py` +
  `tests/test_biochemistry_by_kingdom_actions.py` covering
  the new field + filter semantics + per-kingdom combo
  presence + filter-narrows-pane-lists + canonical-set
  validation + topic_to_dict round-trip.

**🎉 Phase 47 vision realised in 4 rounds (166-169) — 68-
topic biochemistry-by-kingdom explorer with full GUI + agent-
surface integration + kingdom-within-domain sub-domain filter
addressing user feedback; complementary view to the Phase-30
Macromolecules window (chemistry-class organisation).**

### Original scope (kept for reference)

User directive (2026-04-25, round 165): *"Add a new GUI in
the style of the Macromolecules.  This one is for
biochemistry, with tabs for the different kingdoms, and
sub-tabs covering structure, physiology and development,
genetics and evolution — highlighting the molecules and
reactions involved."*

### Pedagogical scope
A second top-level Macromolecules-window-style explorer
that organises biochemistry **by kingdom of life** rather
than **by molecular class** (the existing Macromolecules
window organises Proteins / Carbohydrates / Lipids /
Nucleic Acids by chemical type).  Users get a side-by-side
comparison of how the same biochemical themes (membranes,
ribosomes, energy metabolism, genetic code, signalling)
play out differently across **Eukarya / Bacteria / Archaea**
plus the optional **Viruses** tab — with each kingdom tab
having sub-tabs for **Structure**, **Physiology +
Development**, **Genetics + Evolution**.  Each sub-tab
cross-references the existing Phase-43 cell-component
catalogue, the Phase-42 metabolic-pathways catalogue, and
the Phase-29 lipid / carbohydrate / nucleic-acid
catalogues, surfacing the molecules + reactions involved
inline rather than asking the user to chase them across
existing tools.

### Components
- **`gui/windows/biochemistry_by_kingdom_window.py`** —
  top-level `QMainWindow` opened from *Window →
  Biochemistry by Kingdom…* (Ctrl+Shift+K).  Outer
  `QTabWidget` with one tab per kingdom (Eukarya, Bacteria,
  Archaea, Viruses).  Single persistent instance.
  Geometry + last-active tab persist via
  `QSettings["window/biochemistry_by_kingdom"]`.
- **Per-kingdom inner-tab widget** — `QTabWidget` with
  three sub-tabs:
    - **Structure** — cell-component table for the kingdom
      (re-uses Phase-43 `CellComponent` rows filtered by
      domain), with an HTML detail card per row.
    - **Physiology + Development** — energy metabolism,
      growth + division mechanism, key signalling pathways
      for the kingdom; cross-references Phase-42 metabolic
      pathways AND Phase-43 cellular components.
    - **Genetics + Evolution** — genome organisation
      (chromatin in eukaryotes, nucleoid in bacteria,
      archaeal histone-like proteins); core-genome
      content; horizontal-gene-transfer mechanisms; major
      evolutionary milestones.
  Each sub-tab is a vertical splitter: left pane is a
  filterable list of topics / components / pathways; right
  pane is an HTML detail card with embedded molecule /
  reaction cross-references.
- **Headless-data-core**:
  `core/biochemistry_by_kingdom.py` — `KingdomTopic`
  frozen dataclass + ~60 entries (4 kingdoms × ~5 topics
  per sub-tab × 3 sub-tabs).  Each topic carries
  `kingdom`, `subtab` (`structure` / `physiology` /
  `genetics`), `title`, `body` markdown,
  `cross_reference_cell_component_ids` tuple,
  `cross_reference_pathway_ids` tuple,
  `cross_reference_molecule_names` tuple.
- **Agent actions**: `list_kingdom_topics(kingdom,
  subtab)` / `get_kingdom_topic(id)` / `find_kingdom_topics(
  needle)` / `open_biochemistry_by_kingdom(kingdom, subtab,
  topic_id)`.

### Sub-phases
- [ ] **47a — Headless catalogue.**
      `core/biochemistry_by_kingdom.py` with the
      `KingdomTopic` dataclass + ~60 entries spanning all
      4 kingdoms × 3 sub-tabs.  Lookup helpers + headless
      tests.
- [ ] **47b — Window + per-kingdom widget.**
      `gui/windows/biochemistry_by_kingdom_window.py` +
      `gui/panels/kingdom_subtab_panel.py` for the
      reusable per-kingdom 3-sub-tab widget.  Wired
      through *Window → Biochemistry by Kingdom…*
      (Ctrl+Shift+K).
- [ ] **47c — Agent actions + audit map.**

### Risk + scope reality check
Catalogue size + cross-reference resolution against the
existing Phase-29 / 42 / 43 catalogues are the main scope
drivers.  Likely 2-3 rounds.  Pairs pedagogically with
the existing Macromolecules window (chemistry-class view
vs kingdom view); a *jump-to-Macromolecules-tab* link from
each topic's molecule-cross-reference list is the natural
inter-window glue.

---

## Phase 49 — Cross-module integration audit + glue ✅ *(COMPLETE — all 6 sub-phases SHIPPED across rounds 176-181, 2026-04-25; user-flagged)*

**Status (round 176): 49a SHIPPED.**  Delivered:
- `core/glossary_audit.py` — test-time helper that walks
  every catalogue body / description / notes text + every
  tutorial markdown lesson + every named-reaction `_STARTER`
  description, returning a single ~ 330 kchar text body
  + the lowercase set of all glossary terms + aliases
  (~ 247 entries).  `PHASE_49A_REQUIRED_TERMS` 12-tuple of
  high-priority gates (pH / pKa / buffer / hydrogen
  bonding / LDA / active-methylene / MCR / endosymbiotic
  theory / HGT / CRISPR / chirality / chiral switch).
- 15 new glossary entries appended to
  `db/seed_glossary_extra.py` filling the high-priority
  gaps.  `SEED_VERSION` bumped 9 → 10.
- 9 new tests in `tests/test_glossary_coverage.py` covering
  glossary-set size + catalogue-text size + every required
  term in glossary + every required term used somewhere
  in catalogue/tutorial text + per-domain vocabulary
  (pH-chemistry / synthesis / biology) + audit-module
  public API.

**Status (round 177): 49b SHIPPED.**  Delivered:
- `core/glossary_audit.py` extended with
  `gather_catalogue_molecule_references()` — walks the
  Phase-29 carbohydrate / lipid / nucleic-acid catalogues
  + Phase-31k SAR-series variants + Phase-43 cell-component
  cross-refs + Phase-47 biochemistry-by-kingdom cross-refs,
  returning ~ 250 `(source, name, smiles)` triples (151 with
  parseable SMILES, ~ 100 name-only).
- `db/seed_catalogue_molecules.py` (NEW) —
  `seed_catalogue_molecules_if_needed()` backfills any
  catalogue molecule whose InChIKey isn't already in the
  Molecule DB.  120 molecules seeded on first run; tagged
  with source `carbohydrate-catalogue` / `lipid-catalogue` /
  `nucleic-acid-catalogue` / `sar-<series-id>`.  Idempotent —
  second run adds 0.  Wired into `seed_if_empty()`.
- `tests/test_molecule_db_canonicalisation.py` (NEW) — 6
  tests covering the gather walker (≥ 100 refs, all 4
  SMILES sources), every-SMILES-resolves-by-InChIKey audit
  (with stereo-variant fallback for cases where the
  catalogue ships a stereo isomer of an already-named
  seed compound), every-name-ref-resolves audit, idempotency,
  and a ≥ 50 catalogue-sourced molecules floor.
- Real bug caught: `Citalopram` SMILES in
  `db/seed_molecules_extended.py` had F and CN swapped vs
  the SAR-catalogue version — fixed to the DrugBank
  structure (`CN(C)CCCC1(c2ccc(F)cc2)OCc2cc(C#N)ccc21`).
- `db/queries.py::list_molecules` default `limit` bumped
  500 → 5000 because the DB grew past 500 rows after the
  catalogue backfill, truncating α/β/γ-prefixed sugars +
  alphabetically-late solvents (THF, Testosterone, …)
  from the agent action `list_all_molecules`.

**Status (round 178): 49c SHIPPED.**  Delivered:
- `core/cross_reference_audit.py` (NEW, ~ 250 lines) — walks
  every catalogue's cross-reference fields + validates each
  edge against the destination catalogue / Molecule DB.
  Five relationships audited: cell-component → molecule,
  kingdom-topic → cell-component / metabolic-pathway /
  molecule, microscopy-method → lab-analyser.  Renders a
  human-readable matrix as the living doc + as the failure
  message when an edge breaks.
- `tests/test_cross_reference_graph.py` (NEW) — 7 tests:
  ≥ 50 cross-refs gathered, every declared kind present
  with non-zero count, matrix renders, no broken edges,
  per-kind floors, dataclass hashability + explicit-refs
  validation path.
- 59 cross-reference edges currently in the graph (1 +
  46 + 5 + 1 + 6 across the 5 kinds).  The audit surfaces
  a real coverage gap: only 1 cell-component → molecule +
  1 kingdom-topic → molecule edges exist, despite ~ 100
  catalogue entries that could meaningfully link.  Phase
  49d-f will use the matrix output to drive cross-
  reference expansion.
- Real bug caught on first run: the audit module was using
  the wrong public API name (`list_lab_analysers` vs
  `list_analysers`); fixed before the test suite went
  green.

**Status (round 179): 49d SHIPPED.**  Delivered:
- `core/agent_surface_audit.py` (NEW, ~ 220 lines) — walks
  the agent action registry and verifies every catalogue
  with a Tools-menu dialog has a symmetric agent-action
  surface (opener + canonical lookup trio).  24 catalogue
  surfaces audited.  `EXPECTED_SURFACES` 24-tuple +
  `KNOWN_GAPS` 9-tuple (each entry tags the action name +
  rationale for deferred openers).  `gather_action_names()` /
  `audit_surface()` / `audit_all_surfaces()` /
  `stale_known_gaps()` (catches allow-list drift) /
  `render_audit_text()` (24-row coverage table).
- 2 new agent actions to close the highest-value gaps:
  `open_periodic_table` (`actions_periodic.py`) +
  `open_naming_rules` (`actions_naming.py`).  Both follow
  the established `_gui_dispatch.run_on_main_thread_sync`
  marshalling pattern.
- `gui/audit.py` updated with the 2 new entries so the
  GUI-coverage check stays at 100 %.
- `tests/test_agent_surface_symmetry.py` (NEW) — 7 tests:
  spec sanity (≥ 20 surfaces, no duplicates), KNOWN_GAPS
  well-formed (action_name + non-empty rationale), every
  expected surface complete, KNOWN_GAPS allow-list is
  honest (no stale entries), audit text renders, round-179
  openers registered, round-179 openers in correct
  categories.

**Round-179 baseline.**  24/24 catalogues complete.  9
dialogs deliberately ship without an opener (Spectroscopy /
Stereo / Medchem / Orbitals / Retrosynthesis / Lab
techniques / Green metrics / HRMS / MS fragments — all have
their content surfaced via direct lookup actions).

**Status (round 180): 49e SHIPPED.**  Delivered:
- `core/feature_discovery_audit.py` (NEW, ~ 165 lines) —
  walks the agent registry + `tool_schemas()` + the
  `list_capabilities()` meta action and verifies the AI tutor
  can discover every feature.  Three failure modes audited:
  schema-coverage gap, description gap, category-summary
  gap.  `FeatureDiscoveryReport` dataclass + audit runner +
  smoke checker + text renderer.
- 19 missing category summaries backfilled into
  `agent/actions_meta._CATEGORY_SUMMARIES` (authoring,
  biochem, calc, cell, centrifugation, chromatography,
  clinical, drawing, instrumentation, isomer, kingdom,
  microscopy, ph, phys-org, qualitative, reagent,
  scripting, search, spectrophotometry).  Without these
  the tutor's `list_capabilities()` returned empty
  descriptions for those areas — silently hiding the
  feature surface from the LLM's discovery loop.
- 2 empty-docstring agent actions filled in
  (`get_centrifuge_action` / `get_rotor_action` in
  `actions_centrifugation.py`).
- `tests/test_feature_discovery.py` (NEW) — 9 tests:
  audit clean, registry size floor, every action has a
  schema, every schema has required keys, every category
  has a summary, no stale summaries, list_capabilities
  smoke, round-180 backfilled descriptions are
  substantive, round-180 docstrings non-empty.

**Round-180 baseline.**  243 actions × 43 categories
all clean.

**Status (round 181): 49f SHIPPED — Phase 49 COMPLETE.**

Round-181 deliverables:
- `core/tutorial_coverage_audit.py` (NEW, ~ 200 lines) —
  walks every tutorial markdown lesson + reports
  per-lesson coverage flags across 3 knowledge-graph
  layers (glossary / catalogue molecule / named
  reaction).  `LessonCoverage` per-lesson dataclass +
  `TutorialCoverageReport` aggregate with percentage
  helpers + `lessons_missing(report, layer)` drill-down +
  `render_report_text(report)` plain-text summary.
  Skips authoring-test stub lessons by title prefix.
- Welcome lesson (`beginner/01_welcome.md`) updated with a
  one-sentence chemistry intro mentioning hybridisation +
  pKa so it references at least one glossary term.
- `tests/test_tutorial_coverage.py` (NEW) — 7 tests:
  100 % glossary coverage, ≥ 50 % catalogue molecule
  coverage, ≥ 40 % named-reaction coverage, ≥ 30 lessons
  across 4 levels, report renders, layer-name validation,
  ≥ 15 % "fully-integrated" hit-count-3 lessons.

Round-181 baseline: 31 lessons, 100 % glossary, 54.8 %
catalogue, 45.2 % named-reaction, 16.1 % all-three.

### Phase 49 close-out summary

User directive (round 175): *"ensure modules are well
integrated — words linked to glossary, molecules in the
same format and findable in the database, reactions and
techniques linked between modules, the AI tutor able to
access and use all features"*.

Six sub-phases shipped over rounds 176-181:

| Sub-phase | Round | Module | What it audits |
|-----------|-------|--------|----------------|
| 49a | 176 | `core/glossary_audit.py` | Every catalogue's body text + every tutorial markdown references glossary-defined terms; 15 missing terms backfilled. |
| 49b | 177 | `db/seed_catalogue_molecules.py` + `tests/test_molecule_db_canonicalisation.py` | Every catalogue molecule with a parseable SMILES is a Molecule DB row by InChIKey; 120 catalogue molecules backfilled.  Caught the Citalopram SMILES bug. |
| 49c | 178 | `core/cross_reference_audit.py` | Every catalogue cross-reference resolves to a real target.  5 relationships, 59 edges audited. |
| 49d | 179 | `core/agent_surface_audit.py` | Every Tools-menu dialog has a matching `open_*` agent action + lookup trio.  24/24 surfaces complete after 2 new openers shipped. |
| 49e | 180 | `core/feature_discovery_audit.py` | Every action has a docstring + every category has a summary; 19 missing summaries + 2 empty docstrings backfilled. |
| 49f | 181 | `core/tutorial_coverage_audit.py` | Every tutorial lesson references at least one glossary term; aggregate floors on catalogue + named-reaction coverage. |

Combined: 6 audit modules, 6 test suites (45 total tests),
8 real bugs caught + fixed in the same round, ~ 1500 lines
of audit infrastructure.  The integration sweep produced a
**living dashboard** of cross-module linkage that future
rounds can reference to drive expansion.

### Original spec (kept for reference)

User directive (2026-04-25, round 175): *"Do a code review
and ensure that all modules are well integrated with each
other, for example, words used in modules are included and
linked to the glossary, molecules in all modules are
compatible and in the same format as each other and can be
found in the database, reactions and techniques are linked
between modules, the AI tutor is able to access and use all
features in all modules etc."*

### Pedagogical scope
The catalogue work over the last ~ 30 rounds added many new
content surfaces (Phases 37 / 40 / 41 / 42 / 43 / 44 / 45 /
46 / 47 / 48).  Each shipped its own headless catalogue +
dialog + agent actions, but **cross-module integration** is
uneven — some modules cross-reference Phase-43 cell-
components or the molecule DB, others don't; some glossary
terms are wired into the autolinker, others reference terms
that don't yet exist as glossary entries; the agent surface
covers most actions but a few corners are agent-only or
GUI-only without symmetric exposure.  Phase 49 is an
explicit **integration sweep** to close those gaps.

### Components
- **49a — Glossary autolink coverage audit.**  Walk every
  module's `body` / `description` / `notes` text fields and
  every tutorial markdown lesson; collect every chemistry-
  term mention; verify each term is either (a) already a
  glossary entry, (b) already an alias of a glossary entry,
  or (c) flagged as a missing glossary entry.  Add the
  missing entries to `db/seed_glossary_extra.py`.  Auto-
  generate a `tests/test_glossary_coverage.py` test that
  asserts every catalogued chemistry term has a glossary
  home.
- **49b — Molecule-DB canonicalisation audit.**  Walk every
  catalogue's molecule-name / SMILES references; verify
  each one canonicalises to a real seeded `Molecule` row
  (by InChIKey via the existing `core/fragment_resolver.py`
  helper).  Flag mismatches; either fix the catalogue
  reference OR add the missing molecule to the appropriate
  seed file (`db/seed.py` / `db/seed_molecules_extended.py`
  / `db/seed_intermediates.py`).  This guards against the
  Phase-43 → Molecule-DB rot caught in round 151 + the
  Phase-47 → Phase-42 id-format rot caught in round 166.
- **49c — Cross-module reference graph.**  Generate a
  living document at `docs/CROSS_MODULE_REFERENCES.md` that
  tabulates every cross-reference in the codebase: Phase-47
  → Phase-43 cell components; Phase-47 → Phase-42 metabolic
  pathways; Phase-44 microscopy → Phase-40 lab analysers;
  Phase-29 lipids → Phase-43 membrane components;
  Phase-31k SAR series → Phase-6 molecule database; etc.
  Test-guarded so future renames in any catalogue surface
  immediately as a documentation-coverage fail.
- **49d — Agent-surface symmetry audit.**  Walk every
  GUI-driven feature (every dialog's `Tools` / `Window`
  menu entry, every workspace button) and confirm there's
  a corresponding agent action that opens / drives it.
  The Phase-25a `gui/audit.py` is the existing scaffold —
  Phase 49d closes any remaining gaps + bumps the audit
  test's coverage floor (currently ≥ 60 % from Phase 25a).
  Aim for 100 % open-from-agent coverage of every Tools-
  menu dialog + Window-menu window.
- **49e — Tutor-panel feature-discovery audit.**  Verify
  the Tutor panel's `list_capabilities` action (or
  equivalent introspection path) returns every shipped
  feature name + a one-line description, so an LLM
  driving the app can discover the full surface area
  without reading the source.  Add any missing entries to
  the capabilities surface.
- **49f — Doc-coverage extension.**  The existing
  `tests/test_docs_coverage.py` checks that every
  `orgchem/` module is mentioned in INTERFACE.md.  Phase
  49f extends it to also check that every module
  documented in INTERFACE.md has an entry pointing at it
  from `CLAUDE.md`'s "Where each concern lives" section
  AND that every documented Tools-menu / Window-menu
  shortcut is unique (no Ctrl-shift collisions).

### Sub-phase ordering + risk
49a (glossary coverage) is the lowest-risk first step —
purely additive content work, sets up the autolinker for
every following sub-phase.  49b (molecule-DB
canonicalisation) is next — same additive pattern, guards
against the rot the round-151 + round-166 tests already
caught for narrow slices.  49c-49f are progressively wider
and each ships in its own round.  Likely 6 rounds total.

### Why this matters
Earlier rounds proved that **test-guarded cross-module
references catch real bugs** — the Phase-47 / Phase-43
xref test in round 166 caught a Phase-42 id-format
mismatch (`tca-cycle` vs `tca_cycle`); the Phase-43
cell-component → Molecule-DB xref test in round 151
caught 4 broken cross-references on first run.  Phase 49
generalises those one-off audits into a comprehensive
integration sweep so future content additions land with
their cross-references already wired.

---

## Phase 48 — Isomers exploration tool *(🎉 SHIPPED end-to-end across rounds 170-174, 2026-04-25; user-flagged)*

**Status (round 174): 48a + 48b + 48c + 48d + 48e ALL SHIPPED.**  Delivered:
- `core/isomers.py` — RDKit-backed isomer-relationship core
  with `RELATIONSHIPS` 7-tuple + `IsomerEnumerationResult`
  dataclass + `enumerate_stereoisomers` + `enumerate_tautomers`
  + `classify_isomer_relationship` + `molecular_formula`
  helper.  Classifier walks the 8-step decision tree
  (identical → enantiomer-via-stereo-inversion → meso →
  diastereomer → tautomer-via-enumeration → constitutional-
  via-formula-match → different-molecule fallback).
- 7 new isomer-vocabulary glossary terms appended to
  `db/seed_glossary_extra.py` (Isomerism, Stereoisomer,
  Conformer, Tautomer, Atropisomer, Cis-trans isomerism,
  Optical activity); `SEED_VERSION` bumped 8 → 9 so
  existing DBs pick up the new terms on next launch.
- 20 new tests in `tests/test_isomers.py` covering every
  classifier branch + enumeration + edge cases.
- 1 new test in `tests/test_glossary.py` locking in the
  7 new isomer-vocabulary terms.
- Full suite 2 062 passing.

**48b — Tools → Isomer relationships… dialog (round 171)**:
- `gui/dialogs/isomer_explorer.py` — singleton modeless
  3-tab dialog (Stereoisomers / Tautomers / Classify pair).
- Stereoisomer tab + tautomer tab carry SMILES input +
  max-results spin + meta line showing formula + result
  count + red truncation notice when cap hit.
- Classify-pair tab takes two SMILES + renders a colour-
  coded HTML result with the relationship label + canonical
  RELATIONSHIPS string + 2-row comparison table + per-
  relationship explainer paragraph.
- Wired through *Tools → Isomer relationships…*
  (Ctrl+Shift+B) on the main window.
- 17 new tests in `tests/test_isomer_explorer_dialog.py`;
  full suite 2 080 passing.

**48c — agent actions + audit map (round 172)**:
- `agent/actions_isomers.py` — 4 actions in a new `isomer`
  category: `find_stereoisomers(smiles, max_results)`,
  `find_tautomers(smiles, max_results)`,
  `classify_isomer_pair(smiles_a, smiles_b)` (returns the
  relationship + both molecular formulas so the agent can
  immediately reason about the pair),
  `open_isomer_explorer(tab)`.
- All 4 actions registered in `gui/audit.py`.
- 20 new tests in `tests/test_isomer_actions.py` covering
  every classifier branch + enumeration paths + error
  handling + audit-map registration.
- Full suite 2 100 passing.

**48d — inline 'View isomers' button on the molecule
2D viewer (round 173)**:
- `gui/panels/viewer_2d.py` extended with a "View
  isomers…" button next to the Style combo.
- Disabled until a molecule is selected; enables when a
  `molecule_selected` bus signal carries a SMILES.
- Click pre-fills the Stereoisomers + Tautomers + Classify
  tab inputs, focuses the Stereoisomers tab, AND
  auto-runs the enumeration so the user sees results
  immediately.
- Singleton dialog reused — repeat clicks update the SMILES
  in the same dialog instance.
- 8 new tests in `tests/test_viewer_2d_isomer_button.py`
  covering button presence + initial-disabled / post-
  selection-enabled state + click pre-fills all 3 SMILES
  inputs + lands on Stereoisomers tab + auto-runs
  enumeration + no-op when no SMILES + singleton reuse
  across repeat clicks.
- Full suite 2 108 passing.

**48e — tutorial cross-link (round 174)**:
- New intermediate-level lesson `tutorial/content/
  intermediate/11_isomerism.md` — "Isomerism: a unified
  hierarchy".  Walks the 5-tier hierarchy (constitutional /
  conformer / enantiomer / diastereomer / tautomer +
  identical / different-molecule edge cases) with a
  comparison table + worked SMILES examples that the
  reader can paste into the Phase-48b dialog or use the
  Phase-48d inline button on.  Cross-references all 7
  Phase-48a glossary terms (Isomerism, Stereoisomer,
  Conformer, Tautomer, Atropisomer, Cis-trans isomerism,
  Optical activity).
- Wired into `tutorial/curriculum.py` as the 11th
  intermediate lesson.
- 9 new tests in `tests/test_isomerism_lesson.py` covering
  file existence + level registration + path convention +
  every relationship class mentioned + cross-link to the
  dialog (Ctrl+Shift+B) + cross-link to the inline 'View
  isomers…' button + cross-link to all 7 round-170
  glossary terms + ≥ 5 worked-example SMILES present +
  intermediate-curriculum count grew 10 → 11.
- Full suite 2 117 passing.

**🎉 Phase 48 vision realised in 5 rounds (170-174) —
isomers exploration tool with full headless engine + GUI
dialog + agent surface + inline workspace integration +
tutorial lesson + 7-term glossary expansion.  All four
of the user-flagged round-165 design recommendations
shipped.**

### Original spec (kept for reference)

User directive (2026-04-25, round 165): *"Isomers (so far
there is little mention of them).  What is the best way to
work this into the app?"*

### Best integration recommendation (response to the
### user's design question)
Isomerism touches every part of the app — recommend a
**three-pronged integration** rather than a single new
top-level tool, because isomers are fundamentally a
*relationship between molecules* not a standalone catalogue:

1. **Isomer-relationship explorer dialog** (Tools →
   *Isomer relationships…*, Ctrl+Shift+B) — input a SMILES
   (or pick a molecule from the DB), get back ALL
   **structural isomers** (same molecular formula, different
   connectivity), **stereoisomers** (same connectivity,
   different 3D — enantiomers + diastereomers), **conformers**
   (same connectivity + 3D, different rotamers — links to
   the Phase-10a Dynamics player), and **tautomers** (proton-
   transfer isomers, e.g. keto / enol, amide / iminol —
   surfaced via RDKit's `MolStandardize.tautomer.TautomerEnumerator`).
   Each result row shows the variant 2D + a description of
   the relationship class + a comparison table (MW / logP /
   TPSA — usually identical for stereoisomers, divergent
   for tautomers).  Headless data core +
   `find_isomers(smiles, kinds, max_results)` agent action.
2. **Inline 'View isomers' button on the molecule
   workspace** — a one-click jump from any seeded molecule
   to its isomer-relationship view.
3. **Glossary expansion** — add 8-10 isomer-related glossary
   terms (constitutional / structural isomer, stereoisomer,
   enantiomer, diastereomer, meso compound, conformational
   isomer, tautomer, atropisomer, geometric / cis-trans
   isomer, optical activity / specific rotation) that the
   Reaction-workspace + Tutorial autolinker pick up.
4. **Tutorial-content cross-link** — write 1-2 lessons
   under `tutorial/content/intermediate/` covering
   isomerism with worked examples that link out to the
   isomer-relationship explorer.

### Components (Phase 48a — first round)
- **`core/isomers.py`** — RDKit-backed isomer-finding
  helpers: `enumerate_constitutional_isomers(formula,
  max_results)` (uses RDKit's
  `EnumerateStereoisomers` for stereo + a custom
  `BRICSDecompose`-based routine for connectivity),
  `enumerate_stereoisomers(smiles)`, `enumerate_tautomers(
  smiles)`, `classify_isomer_relationship(smi_a, smi_b)`
  → `"identical"` / `"constitutional"` / `"enantiomer"` /
  `"diastereomer"` / `"meso"` / `"tautomer"` /
  `"conformer"` / `"different molecule"`.
- **`gui/dialogs/isomer_explorer.py`** — Tools → *Isomer
  relationships…* singleton modeless dialog.  SMILES
  input → tabbed results (Constitutional / Stereoisomers
  / Tautomers / Conformers).
- **`agent/actions_isomers.py`** — agent actions in a new
  `isomer` category: `find_isomers`, `classify_isomer_pair`,
  `enumerate_constitutional`, `enumerate_stereoisomers`,
  `enumerate_tautomers`, `open_isomer_explorer`.
- **`db/seed_glossary_isomers.py`** — 8-10 isomer-related
  glossary terms.
- **`gui/panels/molecule_browser.py`** — inline "View
  isomers" button per row.

### Sub-phases
- [ ] **48a — Headless data core + glossary.**
      `core/isomers.py` + glossary expansion.
- [ ] **48b — Dialog.**  Tools → *Isomer relationships…*
      (Ctrl+Shift+B) with the 4-tab results view.
- [ ] **48c — Agent actions.**
- [ ] **48d — Inline 'View isomers' button** on the
      molecule workspace + tutorial content cross-link.

### Risk + scope reality check
Constitutional isomer enumeration is hard (graph-
generation problem) — limit to small molecules (≤ 10 heavy
atoms) for the first round and use a curated lookup table
for larger named molecules.  Stereoisomer + tautomer
enumeration is straightforward via RDKit.  Likely 3-4
rounds total.  The glossary + classify-pair pieces ship
in 1 round; the full enumeration dialog needs careful
RDKit-API selection.

---

## Phase 42 — Metabolic pathways explorer *(NEW — 2026-04-25; user-flagged)*

User directive (2026-04-25): *"Tool for exploring all the
major metabolic pathways of life"*.

### Pedagogical scope
Reference catalogue of the major biochemical pathways with
substrate / enzyme / product chains, regulation, and
cellular compartmentalisation.  Same shape as Phase 37c
(catalogue + dialog) but with richer per-step structure
(each pathway = ordered list of `Step` records pointing at
substrates, enzymes, products, ΔG values, regulatory
allosteric effectors).

### Categories + entries
- **Central carbon metabolism**: glycolysis (10 steps),
  gluconeogenesis (reverse + 4 substitutions), pentose
  phosphate pathway (oxidative + non-oxidative branches),
  TCA cycle (8 steps), oxidative phosphorylation /
  electron transport chain (Complexes I-V).
- **Lipid metabolism**: β-oxidation, fatty-acid
  biosynthesis (FAS), cholesterol biosynthesis (HMG-CoA →
  mevalonate → squalene → cholesterol), triglyceride
  synthesis + breakdown, ketogenesis.
- **Amino-acid metabolism**: urea cycle (5 steps), one-
  carbon metabolism (folate / methionine / SAM cycle),
  nitrogen fixation + assimilation, transamination /
  deamination.
- **Nucleotide metabolism**: purine de novo biosynthesis
  (IMP from PRPP), purine salvage (HGPRT, APRT),
  pyrimidine de novo (UMP from carbamoyl-P), nucleotide
  catabolism + uric-acid pathway.
- **Photosynthesis**: light reactions (PSII / PSI /
  cytochrome b6f / ATP synthase), Calvin cycle (carbon
  fixation), C4 + CAM variants.
- **Specialised metabolism**: heme biosynthesis (8 steps,
  porphyrin ring assembly), bile-acid synthesis,
  steroid-hormone biosynthesis (cholesterol → pregnenolone
  → cortisol / testosterone / estradiol), vitamin
  biosynthesis.
- **Signalling-relevant**: glycogen synthesis +
  breakdown (glycogenesis / glycogenolysis), GPCR
  second-messenger cascades (cAMP / IP3-DAG), MAPK / PI3K
  / Wnt overview.

### Sub-phases
- [x] **42a — Headless catalogue + dialog + agent actions
      — shipped in one round (round 147).**  All three
      sub-phases bundled because the catalogue stayed
      tight.  `core/metabolic_pathways.py` with `Pathway`
      + `PathwayStep` + `RegulatoryEffector` frozen
      dataclasses + 11 seeded pathways across 4 categories
      (central-carbon: glycolysis 10 steps, TCA 8 steps,
      ox-phos 5 complexes, PPP 5 steps; lipid:
      β-oxidation 4 steps, FAS 3 stages, cholesterol 6
      stages; amino-acid: urea cycle 5 steps;
      specialised: heme biosynth 8 steps, Calvin cycle 5
      stages, glycogen metabolism 5 steps).  ΔG values
      from Nelson & Cox 8e; EC numbers from IUBMB /
      BRENDA.  Rich regulatory-effector data (e.g. PFK-1
      lists 4 regulators, HMG-CoA reductase lists statin +
      cholesterol feedback + AMPK).  Dialog at *Tools →
      Metabolic pathways…* (Ctrl+Alt+P) — three-pane
      splitter with pathway list / step table / step
      detail.  5 agent actions in
      `agent/actions_metabolic_pathways.py` under a new
      `biochem` category.  41 tests covering catalogue
      contents + per-pathway teaching invariants
      (glycolysis 10 steps + step-3 PFK regulation,
      hexokinase G6P feedback, TCA 8 steps + SDH membrane-
      bound, Complex IV terminal acceptor, cholesterol
      step 2 statin target, G6PD deficiency note,
      glycogen phosphorylase hormonal regulation) +
      lookup helpers + serialisation + 8 agent actions +
      dialog tests.  All 41 pass on first run.
- [ ] **42a.1 — `nucleotide` category fill-out.**  Purine
      + pyrimidine de-novo synthesis pathways for the
      currently-empty fifth category.  Polish round.

### Risk + scope reality check
Catalogue depth is the trade-off — full pathway with all
isozymes + regulation can run hundreds of lines per
pathway.  Aim for the textbook-essential view first; per-
pathway detail can grow in 42a.1+ polish rounds.

---

## Phase 43 — Cell-component explorer (Eukarya / Bacteria / Archaea) *(SHIPPED 2026-04-25, round 151; user-flagged)*

**Status (round 151): SHIPPED end-to-end.**  Delivered:
- `core/cell_components.py` — 41-component catalogue across the
  3 domains (24 eukaryotic / 11 bacterial / 6 archaeal) and 9
  categories (membrane / organelle / nuclear / cytoskeleton /
  envelope / appendage / extracellular / ribosome / genome).
  Each component carries a tuple of `MolecularConstituent`
  rows; constituents can carry cross-references back to
  Phase-6 molecule-DB rows.
- `gui/dialogs/cell_components.py` — singleton modeless dialog
  with a triple-combo layout (domain + sub-domain + category)
  + free-text filter + list + HTML detail card with the
  molecular-constituents table.  Wired through *Tools → Cell
  components…* (Ctrl+Shift+J).
- `agent/actions_cell_components.py` — 5 actions in a new
  `cell` category (`list_cell_components`,
  `get_cell_component`, `find_cell_components`,
  `cell_components_for_category`, `open_cell_components`).
- 68 new tests in `tests/test_cell_components.py`; full suite
  1 918 passing.
- All 5 actions registered in `gui/audit.py`.

### Original scope (kept for reference)

User directive (2026-04-25): *"Tool for investigating all
the major components of a cell for the different kingdoms,
with explanations of the molecules involved"*.

### Pedagogical scope
A reference catalogue of cellular components keyed to the
three domains of life (Eukarya, Bacteria, Archaea) plus
optional sub-keys (animal / plant / fungus for Eukarya;
gram-positive / gram-negative for Bacteria).  Each
component entry carries its molecular composition with
links / cross-references back to the molecule database
(Phase 6) where applicable.

### Categories + entries
- **Membranes + envelopes**: plasma membrane (Eukarya
  phospholipid bilayer + cholesterol + sphingolipids;
  Bacteria peptidoglycan-bilayer; Archaea ether-linked
  isoprenoid lipids), nuclear envelope, ER (rough +
  smooth), Golgi cisternae, vesicles, peptidoglycan cell
  wall (gram-positive thick vs gram-negative thin +
  outer membrane), plant cell wall (cellulose +
  hemicellulose + pectin), fungal cell wall (chitin),
  archaeal S-layer.
- **Cytoplasmic organelles**: mitochondria (matrix +
  cristae + DNA + ribosomes), chloroplasts (thylakoid +
  stroma), peroxisomes, lysosomes (animal) / vacuoles
  (plant + yeast), ribosomes (80S vs 70S), proteasomes,
  ribosome composition (rRNA + ribosomal proteins).
- **Nuclear components**: nuclear envelope + pores,
  nucleolus (rRNA transcription), nucleoplasm,
  chromatin (histone octamer + DNA), centromere /
  kinetochore, telomere.
- **Cytoskeleton**: actin microfilaments (G-actin /
  F-actin / actin-binding proteins), intermediate
  filaments (keratin / vimentin / lamin / neurofilament),
  microtubules (α/β-tubulin + γ-tubulin nucleation),
  centrosomes / MTOCs, cilia + flagella (axoneme 9+2 in
  Eukarya vs flagellin-based bacterial flagellum).
- **Bacterial extras**: nucleoid (no envelope), pilus /
  fimbriae, capsule, plasmids, mesosomes.
- **Archaeal extras**: pseudopeptidoglycan, ether-linked
  isoprenoid lipids, 80S-like ribosome composition.
- **Extracellular**: ECM (collagen + fibronectin +
  laminin + glycosaminoglycans + proteoglycans for
  animal), cellulose / pectin / lignin for plant cell
  walls, biofilm extracellular polymeric substances
  (EPS) for bacterial biofilms.

### Sub-phases
- [ ] **43a — Headless catalogue.**  `core/cell_components.py`
      with `CellComponent` + `MolecularConstituent` frozen
      dataclasses + ~40 components keyed by domain (Eukarya
      / Bacteria / Archaea) + sub-domain (animal / plant /
      fungus / gram+ / gram-).  Each component:
      compartment, function, key molecules (cross-ref to
      `Molecule` rows where SMILES exists, e.g.
      cholesterol / cellulose / DNA), notable diseases /
      experimental hooks.
- [ ] **43b — Dialog.**  Domain picker + sub-domain combo
      + component list + detail pane with molecular-
      constituent table.  Wired to *Tools → Cell components…*
      (Ctrl+Shift+J).
- [ ] **43c — Agent actions.**  `list_cell_components(domain)`
      / `get_cell_component(id)` /
      `find_cell_components(needle)` /
      `open_cell_components(...)`.

---

## Phase 44 — Microscopy across resolution scales *(SHIPPED 2026-04-25, round 150; user-flagged)*

**Status (round 150): SHIPPED end-to-end.**  Delivered:
- `core/microscopy.py` — 30-method catalogue across 6
  resolution scales (whole-organism / tissue / cellular /
  sub-cellular / single-molecule / clinical-histology), each
  entry tagged with sample-types tuple + cross-references to
  Phase-40a `lab_analysers.py` rows where the same instrument
  appears.
- `gui/dialogs/microscopy.py` — singleton modeless dialog with
  resolution-scale combo + sample-type combo + free-text
  filter + list + HTML detail card.  Wired through *Tools →
  Microscopy techniques…* (Ctrl+Alt+M).
- `agent/actions_microscopy.py` — 5 actions in a new
  `microscopy` category (`list_microscopy_methods`,
  `get_microscopy_method`, `find_microscopy_methods`,
  `microscopy_methods_for_sample`, `open_microscopy`).
- 52 new tests in `tests/test_microscopy.py`; full suite
  1 850 passing.
- All 5 actions registered in `gui/audit.py`.

### Original scope (kept for reference)

User directive (2026-04-25): *"Microscopy tool exploring
uses of microscopes from clinical to research.  Studying
different levels of resolution: whole organism, tissue,
cells, organelles, single molecules"*.

### Pedagogical scope
Cross-cuts the Phase-37d spectrophotometry catalogue + Phase-
40a lab-analysers catalogue but organised by **resolution
scale + sample type** rather than instrument family.
Pedagogically the answer to *"which microscope do I use?"*
depends on what you want to see + at what resolution — a
catalogue keyed to resolution makes that decision tree
explicit.

### Resolution scales + entries
- **Whole-organism (mm-cm)**: stereo dissecting microscope,
  intra-vital microscopy, optical-coherence tomography
  (OCT), small-animal MRI / CT for whole-mouse imaging.
- **Tissue (μm-mm)**: histology brightfield (H&E,
  Trichrome, IHC), polarised light, fluorescence (IHC-IF
  + multiplex IHC like Akoya CODEX / Vectra Polaris), tissue-
  clearing + light-sheet (CLARITY / iDISCO), MALDI imaging
  mass spec.
- **Cellular (μm)**: brightfield + DIC + phase-contrast
  for live cell observation, widefield epifluorescence,
  confocal (Phase 40a Zeiss LSM), spinning-disk confocal
  for high-speed live imaging, 2-photon / multiphoton for
  thick-tissue imaging.
- **Sub-cellular (organelle) (100-500 nm)**: super-
  resolution: SIM (Zeiss Elyra), STORM / PALM (Bruker
  Vutara, Nikon N-STORM), STED (Leica SP8 STED), Airyscan
  (Zeiss).  TIRF for membrane-proximal imaging.
- **Single-molecule (nm-Å)**: single-molecule FRET (smFRET),
  cryo-EM (Phase 40a Krios), cryo-electron tomography (cryo-
  ET), atomic-force microscopy (AFM) for single-molecule
  mechanics, scanning-tunnelling microscopy (STM).
- **Clinical histology workflow**: traditional light
  microscope + paraffin-section H&E (the routine pathology
  workhorse), IHC for cancer-marker staining, frozen-
  section cryostat for intra-operative consultation, digital
  pathology slide scanners (Hamamatsu NanoZoomer, Leica
  Aperio AT2).

### Sub-phases
- [ ] **44a — Headless catalogue.**  `core/microscopy.py`
      with `MicroscopyMethod` + `ResolutionScale` frozen
      dataclasses + ~30 entries keyed by resolution scale.
      Cross-references to Phase 40a `lab_analysers.py`
      where the same instrument appears (e.g. confocal
      `LabAnalyser` ↔ `MicroscopyMethod` for the cellular
      scale).
- [ ] **44b — Dialog.**  Singleton modeless dialog at
      *Tools → Microscopy…* (Ctrl+Shift+Y) — actually
      this conflicts with the Phase-37d Spectrophotometry
      shortcut.  Alt: Ctrl+Alt+M (no clash).  Resolution-
      scale selector + sample-type combo + method list +
      detail pane.
- [ ] **44c — Agent actions.**  `list_microscopy_methods` /
      `get_microscopy_method` / `find_microscopy_methods` /
      `methods_for_resolution(scale)` /
      `methods_for_sample_type(...)` / `open_microscopy(...)`.

### Risk + scope reality check
Most scope-related, modest risk.  Cross-references to the
existing Phase 40a microscopy entries (Zeiss LSM 980,
Lattice Lightsheet, Krios) need pointer fields to avoid
catalogue duplication — keep the `LabAnalyser` rows as
the *instrument* descriptions and the `MicroscopyMethod`
rows as the *resolution-scale-anchored teaching view* on
those instruments.

---

## Phase 40 — Major lab analysers + automation reference *(NEW — 2026-04-25; user-flagged)*

User directive (2026-04-25): *"a tool for exploring major
lab analysers and larger pieces of equipment — including
automation and more specialised items (FLIPR, biochemistry
analyzers, hematology analyzers, molecular analyzers,
immunoassay analyzers).  Specialized items that are found
in hospitals, clinical labs and research environments."*

### Pedagogical scope
A reference catalogue of the *whole-instrument* tier above
Phase 38a's bench-glassware (RBF / condenser / hot-plate
items).  Each entry is a major capital-equipment item the
student will encounter in clinical or research labs but
won't typically build setups around themselves.  Same
catalogue + dialog + agent-action shape as Phase 37c
(chromatography techniques) — long-form reference cards
keyed to a category combo + filter + detail pane.

### Categories + entries

- **Clinical chemistry analysers**: Roche cobas (8000 / pro
  / c701), Siemens Atellica, Beckman AU series, Abbott
  Architect / Alinity c — the workhorse instruments running
  BMP / CMP panels (Phase 37b) at hundreds of samples per
  hour.
- **Hematology analysers**: Sysmex XN-series, Beckman DxH
  900, Siemens ADVIA, Abbott CELL-DYN — automated CBC
  (complete blood count) including 5-part differential,
  reticulocyte count, NRBC, body-fluid analysis.
- **Coagulation analysers**: Stago STA Compact, Sysmex CS
  series, Werfen ACL TOP — PT / aPTT / fibrinogen /
  d-dimer automation.
- **Immunoassay analysers**: Roche cobas e801, Abbott
  Architect i / Alinity i, Siemens Atellica IM, Beckman
  Access — TSH / cardiac troponin / cancer markers /
  hormone panels via chemiluminescent or fluorescent
  immunoassay.
- **Molecular analysers**: Roche cobas 8800 (PCR), Hologic
  Panther, BD MAX, Cepheid GeneXpert (POC PCR), Illumina
  NextSeq / NovaSeq (NGS), Oxford Nanopore MinION /
  PromethION — DNA / RNA quantification + variant calling.
- **Mass-spec systems** (clinical + research): triple-quad
  LC-MS/MS for vitamin D + steroid panels, MALDI-TOF for
  microbial ID (Bruker Biotyper, bioMérieux VITEK MS),
  ICP-MS clinical for trace metals, Orbitrap for
  proteomics.
- **Cell-based / functional assays**: FLIPR (Molecular
  Devices) for Ca²⁺ / membrane-potential GPCR screens,
  high-content imagers (PerkinElmer Operetta, Molecular
  Devices ImageXpress, GE IN Cell), patch-clamp robots
  (Nanion SyncroPatch, Molecular Devices IonWorks).
- **Microscopy + imaging** (research): confocal (Zeiss LSM,
  Leica SP, Nikon A1), spinning-disk (Yokogawa CSU /
  Andor), super-resolution (Zeiss Elyra, Bruker Vutara,
  Nikon N-STORM), light-sheet (Zeiss Lightsheet, Bruker
  Luxendo), cryo-EM (Thermo Krios / Glacios).
- **Sample-prep / liquid-handling automation**: Hamilton
  STAR / NIMBUS, Tecan Fluent / Freedom EVO, Beckman
  Biomek, Opentrons OT-2 (open-source) — automated
  pipetting platforms backing modern high-throughput
  pipelines.
- **Storage / sample management**: Hamilton BiOS L /
  BIONanoArchive (-80 °C automated freezers),
  Thermo Galileo (LN₂ vapor storage), Brooks BioStudies
  (sample tracking software).

### Sub-phases

- [x] **40a — Headless catalogue + dialog + agent actions
      — shipped in one round (round 146).**  All three
      original sub-phases bundled because the catalogue
      stayed tight.  `core/lab_analysers.py` with
      `LabAnalyser` frozen dataclass + 28 entries across
      10 categories: clinical-chemistry (cobas c702,
      Atellica CH 930, Beckman AU5800, Alinity c),
      hematology (Sysmex XN-1000, Beckman DxH 900),
      coagulation (Stago STA R Max 3, Sysmex CS-5100),
      immunoassay (cobas e801, Alinity i, Atellica IM),
      molecular (cobas 8800, Hologic Panther, GeneXpert,
      NovaSeq X, Oxford Nanopore PromethION), mass-spec
      (SCIEX QTRAP 7500, Bruker Biotyper), functional
      (FLIPR Penta, Operetta CLS), microscopy (Zeiss LSM
      980, Lattice Lightsheet 7, Thermo Krios G4),
      automation (Hamilton STAR, Tecan Fluent, Opentrons
      OT-2), storage (Hamilton BiOS, Thermo Galileo).  4
      agent actions in `agent/actions_lab_analysers.py`
      (`list_lab_analysers`, `get_lab_analyser`,
      `find_lab_analysers`, `open_lab_analysers`) under a
      new `instrumentation` category.  Dialog at *Tools →
      Lab analysers…* (Ctrl+Shift+A).  35 tests in
      `tests/test_lab_analysers.py` (catalogue size +
      10-category coverage + every-id-unique +
      user-requested-systems-present + 8 per-row teaching
      invariants for cobas / Sysmex / GeneXpert / NovaSeq
      / Nanopore / FLIPR / Krios / Opentrons + filter +
      lookup + dialog construction + agent-action open
      path).

### Risk + scope reality check
Same shape as Phase 37c — ~3-4 catalogue rounds of writing,
plus dialog + agent actions + tests.  Likely 2 rounds total
(40a + 40b/c bundled).  Pure reference data, no quantitative
widgets needed.

---

## Phase 41 — Centrifugation reference + calculator *(NEW — 2026-04-25; user-flagged)*

User directive (2026-04-25): *"a tool for exploring
centrifugation"*.

### Pedagogical scope
Reference catalogue of centrifuge classes + rotor types +
applications PLUS a quantitative `g_to_rpm` / `rpm_to_g`
calculator widget (the single most-confused conversion in
every centrifugation protocol).

### Categories + entries

- **Centrifuge classes**:
    - **Microcentrifuge** (Eppendorf 5424 / 5425, Beckman
      Microfuge): 1.5-2 mL tubes, ≤ 21 000 × g.
    - **Benchtop centrifuge** (Eppendorf 5810 / 5910,
      Beckman Allegra): 50 mL conical tubes, swinging-bucket
      + fixed-angle rotors, ≤ 30 000 × g.
    - **High-speed centrifuge** (Beckman Avanti J-26 series,
      Sorvall RC-6+): 250-500 mL bottles, ≤ 100 000 × g.
    - **Ultracentrifuge** (Beckman Optima L-90 / Sorvall
      WX 100): vacuum-jacketed, ≤ 600 000 × g (1 000 000 ×
      g with the smallest rotors), refrigerated.
    - **Refrigerated centrifuges** vs ambient — when
      enzymatic activity / RNA stability is at stake.
- **Rotor types**:
    - **Fixed-angle**: high speed + capacity, radial
      pellet.
    - **Swinging-bucket**: gentle on cells / pellet at the
      tube bottom; needed for density-gradient centrifugation.
    - **Vertical** (analytical ultracentrifuges): density-
      gradient analytics.
    - **Continuous-flow** (industrial): protein purification
      at scale.
- **Applications**:
    - **Differential centrifugation** (10 000 × g pellet
      mitochondria, 100 000 × g pellet microsomes, …).
    - **Density-gradient centrifugation** — sucrose
      step-gradients for organelle separation, CsCl
      isopycnic for plasmid prep / virus particles, Percoll
      / Nycodenz for live-cell separation.
    - **Pelleting cells / bacteria** (typical 5000 × g for
      5 min for *E. coli*, 200 × g for 5 min for mammalian
      cells without pelleting hard).
    - **Protein concentration** with Amicon / Vivaspin
      centrifugal filters.
    - **Subcellular fractionation** — homogenate → nuclear
      → mitochondrial → microsomal → cytosolic protocol.
- **Calculator widget**:
    - **g ↔ rpm conversion**: `g = 1.118e-5 · RPM² · r` (r
      in cm, the rotor's max radius).  Pass any 2 of 3.
      The widget needs the rotor selected from a dropdown
      (each rotor carries its own radius) so the conversion
      is right for that rotor — wrong-rotor calculations
      produce real failures (lysed cells, broken tubes).

### Sub-phases — ALL SHIPPED in round 144

- [x] **41a — Headless catalogue + g↔rpm solver.**
      `core/centrifugation.py` with `Centrifuge` /
      `Rotor` / `Application` frozen dataclasses + 9
      centrifuges (microfuge / benchtop / high-speed /
      ultracentrifuge classes) + 10 rotors (fixed-angle /
      swinging-bucket / vertical) + 8 applications
      (cell pelleting, differential, sucrose / CsCl
      density gradient, Amicon concentration, exosome
      isolation, serum separation).  `rpm_to_g` /
      `g_to_rpm` solvers using
      `g = G_FORCE_CONSTANT · RPM² · r` with
      `G_FORCE_CONSTANT = 1.118e-5` — verified against the
      Eppendorf 5424 data sheet (15 000 RPM @ 8.4 cm =
      21 130 × g exactly).
- [x] **41b — Dialog + calculator widget.**  Singleton
      modeless dialog at *Tools → Centrifugation…*
      (Ctrl+Shift+F).  4 tabs: 3 catalogue tabs sharing
      a reusable `_CatalogueTab` helper class, plus a
      g↔RPM `_CalculatorTab` with a rotor-`QComboBox` that
      auto-fills the radius spin AND shows the rotor's
      max RPM so overspeed is visible — entering a speed
      above the rotor's max limit appends an OVERSPEED
      warning to the status line in red.
- [x] **41c — Agent actions.**  8 actions in the
      `centrifugation` category: `list_centrifuges_action`
      / `get_centrifuge_action` /
      `list_rotors_action` / `get_rotor_action` /
      `list_centrifugation_applications` /
      `rpm_to_g_action` / `g_to_rpm_action` /
      `open_centrifugation`.  37 catalogue + solver tests
      in `tests/test_centrifugation.py` + 17 dialog tests
      in `tests/test_centrifugation_dialog.py`.

---

## Phase 39 — Lab calculator (common lab calculations) *(NEW — 2026-04-25; user-flagged)*

User directive (2026-04-25): *"a lab calculator for
performing all common lab calculations"*.

### Pedagogical scope
A single dialog (or scrollable tabbed dialog) that bundles
every routine bench-side calculation an undergraduate /
medicinal-chem student does dozens of times per week.
Headless solvers for each calculation so the same logic is
exposed via agent actions for the tutor / scripts.  Builds
on Phase-37d's pattern (`beer_lambert_solve` headless solver
+ widget) but at much larger scope — a unified calculator
suite, not a single equation.

### Categories + calculations

- **Solution prep / concentration** —
    - Molarity ↔ mass / volume (`m = M·V·MW`).
    - Molality (mol solute per kg solvent).
    - Dilution (`M₁V₁ = M₂V₂` and the `n × dilution-factor`
      version for serial dilutions).
    - % w/w / % w/v / % v/v ↔ molarity conversions.
    - ppm / ppb ↔ mg/L / µg/L conversions.
    - Mole fraction ↔ molarity (with density input).
    - Molarity from mass-percent + density (e.g. concentrated
      HCl 37 % w/w, ρ 1.18 g/mL → 12 M).

- **Stoichiometry** —
    - Limiting reagent (mass / mole inputs for 2-3 reagents
      + balanced-equation stoichiometric coefficients →
      limiting reagent + theoretical mass of product).
    - Percent yield (actual / theoretical × 100).
    - Percent purity (mass actual / mass theoretical for a
      sample of known mass).
    - Atom economy is already in Phase 17a — link cross-refs.

- **Acid-base** —
    - pH ↔ [H⁺] / pOH ↔ [OH⁻].
    - pKa ↔ Ka.
    - Henderson-Hasselbalch (buffer pH given pKa + [HA] +
      [A⁻]; or required ratio for target pH).
    - Buffer capacity (β = 2.3 · C_total · α · (1 − α) at
      half-titration).

- **Gas laws** —
    - PV = nRT (solve for any of P / V / n / T).
    - Combined gas law (P₁V₁/T₁ = P₂V₂/T₂).
    - Density of an ideal gas (ρ = PM / RT).

- **Colligative properties** —
    - Boiling-point elevation (ΔT_b = K_b · b · i).
    - Freezing-point depression (ΔT_f = K_f · b · i).
    - Osmotic pressure (Π = MRT · i).

- **Thermochemistry** —
    - Heat capacity (q = m · c · ΔT).
    - Hess's law accumulator (sum ΔH from a list of
      step ΔH values).
    - Bond-dissociation-energy estimate (sum BDE_breaking −
      sum BDE_forming → ΔH_rxn).

- **Kinetics** —
    - First-order half-life (t½ = ln 2 / k).
    - First-order rate equation (`[A]_t = [A]_0 · e^{-kt}`,
      solve for any).
    - Arrhenius (`k = A · e^{-Ea / RT}`, solve for k / A /
      Ea / T given the others).
    - Eyring (`k = (k_B T / h) · e^{-ΔG‡/RT}`).

- **Equilibrium** —
    - K_eq from concentrations (or partial pressures).
    - Solubility-product K_sp ↔ molar solubility.
    - ICE-table solver for a single equilibrium step.

- **Spectroscopy** —
    - Beer-Lambert (already in `core/spectrophotometry_methods`
      Phase 37d — link cross-ref + add a tab).

- **Practical bench** —
    - Mass ↔ moles ↔ molecules (using NA).
    - SMILES → molecular weight (uses the existing RDKit
      molecular-formula machinery).
    - Reaction-scale calculator (given target moles of
      product, work backward through stoichiometry to mass
      of each reagent).
    - Solution-density lookup (water + common organic
      solvents at 25 °C).

### Sub-phases

- [x] **39a — Headless solvers + tests — shipped (round
      142).**  Seven sibling modules in `orgchem/core/`:
      `calc_solution.py`, `calc_stoichiometry.py`,
      `calc_acid_base.py`, `calc_gas_law.py`,
      `calc_colligative.py`, `calc_thermo_kinetics.py`,
      `calc_equilibrium.py`.  Every solver follows the
      Phase-37d `beer_lambert_solve` pattern: pass any
      N-1 of N quantities (use `None` for the unknown),
      get the full set back with the Nth filled in,
      raise `ValueError` on missing-count != 1 or
      non-positive input.  ~30 solver functions + 4
      module-level constants (R_L_atm, R_J, k_B, h) +
      a `SOLVENT_CONSTANTS` table for the cryoscopic /
      ebullioscopic helpers.  Highlights:
      `molarity_solve` (m = M·V·MW), `dilution_solve`
      (M₁V₁ = M₂V₂), `serial_dilution`,
      `molarity_from_mass_percent` (e.g. concentrated
      HCl 37 % → 12 M), ppm ↔ molarity, `limiting_reagent`,
      `theoretical_yield_g`, `percent_yield`,
      `percent_purity`, `ph_from_h` / `h_from_ph`,
      `pka_to_ka` / `ka_to_pka`, `henderson_hasselbalch`,
      `ideal_gas_solve` (PV = nRT), `combined_gas_law`
      (P₁V₁/T₁ = P₂V₂/T₂), `gas_density` (ρ = PM/RT),
      `boiling_point_elevation` / `freezing_point_depression`
      (with solvent-name auto-fill of K_b / K_f),
      `osmotic_pressure`, `heat_capacity_solve` (q =
      mcΔT), `hess_law_sum`, `first_order_half_life`,
      `first_order_integrated`, `arrhenius_solve`,
      `eyring_rate_constant`,
      `equilibrium_constant_from_concentrations`,
      `ksp_from_solubility` / `solubility_from_ksp`
      (closed form for AnBm salts),
      `ice_solve_a_plus_b` (closed-form quadratic ICE
      with chemically-sensible-root picker).  59 tests
      in `tests/test_calc_solvers.py` covering textbook
      values (29.22 g NaCl in 1 L = 0.5 M, 1 mol gas at
      STP = 22.4 L, 100 g water 20→30 °C = 4184 J,
      0.05 /s rate constant = 13.86 s half-life, AgCl
      K_sp = 1.69e-10, NaCl 1 m in water → ΔTf = 3.72 °C,
      isotonic saline at 37 °C ≈ 7.6 atm osmotic
      pressure) + every error path (missing-count,
      non-positive, unknown solvent, unknown side, etc.).
- [x] **39b — Unified calculator dialog — shipped (round
      143).**  Tabbed `QDialog` with 7 tabs (Solution /
      Stoichiometry / Acid-base / Gas law / Colligative /
      Thermo + kinetics / Equilibrium) backed by the
      Phase-39a solvers.  Reusable `_SolverPanel`
      helper builds the title + N spin boxes + Solve +
      Clear + status-line pattern; spin value 0 = "unknown"
      (passed as None to the solver), which the solver
      fills in.  Custom panels where the symmetric-solve
      pattern doesn't fit cleanly (pH↔[H⁺], pKa↔Ka, K_sp↔s,
      ICE solver).  Colligative tab includes solvent
      `QComboBox` that auto-fills K_b / K_f from the
      `SOLVENT_CONSTANTS` lookup table.
      `_SolverPanel.add_widget` helper handles the
      extra-widget plumbing.  Wired into *Tools → Lab
      calculator…* (Ctrl+Shift+C).  Single `open_lab_calculator(tab="")`
      agent action shipped alongside (per-solver actions
      defer to 39c).  15 pytest-qt tests
      (`test_lab_calculator_dialog.py`) cover construction,
      tab navigation, every panel kind including the
      solvent-dropdown auto-fill + the custom pH↔[H⁺] +
      K_sp↔s direction buttons + agent-action open path.
- [x] **39c — Per-solver agent actions — shipped (round
      145).**  31 thin `@action` wrappers in
      `agent/actions_calc.py`, one per Phase-39a solver
      across all 7 modules.  Common `_wrap(solver,
      **kwargs)` helper converts `ValueError` → `{"error":
      str}` so the agent never sees a Python traceback.
      32 calc actions total (31 solvers + the round-143
      `open_lab_calculator` dialog opener); each
      registered in `gui/audit.py` with a path back to
      its UI panel (or "agent-only" when the solver's
      list-shaped input doesn't fit the spin-box dialog
      pattern, e.g. `limiting_reagent` /
      `equilibrium_constant` / `hess_law_sum`).  33
      pytest cases in `tests/test_calc_actions.py` —
      registry membership invariant (all 31 expected
      action names present) + happy-path verification
      against the same textbook values used in Phase
      39a tests (NaCl 29.22 g, STP 22.414 L, NaCl 1m
      ΔTf = 3.72 °C, AgCl K_sp = 1.69e-10, etc.) +
      every error path (missing-count, percent-purity
      > 100, unknown solvent, ICE both-zero).  All 33
      pass on first run.
- [ ] **39d — Cross-references** to existing helpers
      (Beer-Lambert in Phase 37d, atom-economy in Phase
      17a, formula calculator in `core/formula.py`,
      molecular weight via RDKit).  Documentation only;
      no code duplication.

### Risk + scope reality check
The total surface is large (~25-30 calculations) but each
calculation is small + independent.  Likely 3-4 rounds:
39a in 1-2 (split solvers across modules to keep each
file < 500 lines), 39b in 1 (tabbed dialog), 39c in 1
(thin agent-action wrappers), 39d in 0.5 (just docs).
The pattern is fully nailed down by Phase 37d's Beer-
Lambert widget + helper, so this is largely
"replicate-and-extend" rather than design-from-scratch.

---

## Phase 38 — Lab setup + process simulator *(NEW — 2026-04-25; user-flagged)*

User directive (2026-04-25): *"add a tool for lab setup
and simulation of different processes"* with comprehensive
equipment list, configuration of equipment into setups
(simple distillation, reflux, …), an interactive diagram
where users place equipment + watch simulated reactions,
and seeded demos.

### Pedagogical scope
A live "build the apparatus" canvas paired with a library
of canonical setups.  Two halves:
- **Equipment library** — every piece of glassware /
  hardware undergrads see: round-bottom flasks (RBFs),
  Claisen / distillation adapters, condensers (Liebig /
  Allihn / Graham / Friedrichs), separatory funnels,
  Büchner / Hirsch funnels, fractionating columns, ring
  stands + clamps, heating mantles + Variacs, stirrer-hot-
  plates, thermometers + adapters, vacuum traps, cold
  fingers, dropping funnels, three-neck flasks, septa,
  cannulas, gas inlet adapters, melting-point apparatus,
  IR / GC-MS / HPLC stations.
- **Setups + simulator** — a `QGraphicsScene` canvas that
  takes equipment from a palette and lets the user wire it
  together (e.g. RBF → distillation head → condenser →
  receiver).  Each canonical setup (simple distillation,
  fractional distillation, reflux, soxhlet extraction,
  liquid-liquid extraction, vacuum filtration, recrystallisation
  cooling) has a seeded layout + a step-by-step "what
  happens when you turn on the heat" simulation that
  animates fluid flow / vapour rising / condensate forming.

### Design outline
- **38a — `Equipment` dataclass + headless catalogue —
  shipped (round 140).**  `orgchem/core/lab_equipment.py`
  with `Equipment` + `ConnectionPort` frozen dataclasses;
  42 entries across 12 categories (glassware / adapter /
  condenser / heating / cooling / separation / filtration /
  vacuum / stirring / support / safety / analytical) —
  every piece needed by the canonical Phase-38b setups
  (simple distillation, reflux, Soxhlet, vacuum filtration,
  liquid-liquid extraction).  Each entry: id / name /
  category / description / typical_uses / variants /
  safety_notes / icon_id (placeholder for the future
  Phase-38c canvas SVG) / connection_ports (named
  joints / hoses / sockets the canvas will use to snap
  items).  Joint-type vocabulary: ANSI ground glass
  (`14/20`, `19/22`, `24/29`, `29/32`), `hose`, `socket`,
  `open`, plus equipment-specific tags
  (`thermometer-bulb`, `filter-paper`, …).  Dialog at
  `orgchem/gui/dialogs/lab_equipment.py` (singleton,
  modeless) wired to *Tools → Lab equipment…*
  (Ctrl+Shift+I) — same shape as the Phase-37 catalogue
  dialogs plus a Connection-ports section in the detail
  body.  4 agent actions in
  `orgchem/agent/actions_lab_equipment.py`.  37 tests
  (26 catalogue + 11 dialog).
- **38b — `Setup` dataclass + 6-8 canonical setups —
  shipped (round 141).**  `orgchem/core/lab_setups.py`
  with `Setup` + `SetupConnection` frozen dataclasses
  + 8 seeded setups: simple distillation, fractional
  distillation (= simple + Vigreux), standard reflux,
  reflux with controlled addition, Soxhlet extraction,
  vacuum filtration, liquid-liquid extraction,
  recrystallisation.  Equipment refs are INDICES into
  the setup's equipment list (not ids) so the same
  piece can appear twice (pot + receiver RBF).  New
  `validate_setup(setup)` walks every connection,
  resolves the named ports via the Phase-38a catalogue,
  and returns error strings for: equipment-id typos,
  out-of-range indices, self-loops, unknown port names,
  joint-type mismatches (with `open` as wildcard for
  non-glass-joint contact), male-male or female-female
  port-sex mismatches.  All 8 seeded setups validate
  clean — fixing 4 port-direction bugs in the Phase-38a
  catalogue along the way (distillation-head side arm
  was female, vacuum-adapter top was male, thermometer
  joint type didn't match adapter sleeve, sep funnel
  needed an `outlet` male port for addition-funnel use).
  Dialog at `orgchem/gui/dialogs/lab_setups.py`
  (singleton, modeless) wired to *Tools → Lab setups…*
  (Ctrl+Shift+U): filter + setup list on the left,
  detail card with resolved equipment + connection
  table on the right.  When validation fails the dialog
  renders the errors in red at the bottom of the detail
  card.  5 agent actions in
  `orgchem/agent/actions_lab_setups.py` (`list_lab_setups`,
  `get_lab_setup`, `find_lab_setups`, `validate_lab_setup`,
  `open_lab_setups`).  41 tests (30 catalogue +
  validator + 11 dialog).
- **38c — Equipment palette + `QGraphicsScene` canvas**
  (drag from palette → drop on canvas → snap connection
  ports between adjacent items).  Sub-phases:
  - [x] **38c.1 (round 186, 2026-04-26) SHIPPED** —
    headless palette data layer (`core/lab_palette.py`).
    `PaletteCategory` + `Palette` dataclasses,
    `default_palette()` (every Phase-38a equipment item,
    grouped + ordered across 12 categories),
    `palette_for_setup(setup_id)` (filtered to one Phase-38b
    setup's equipment for the future *Build on canvas*
    button), category-display-order constants, JSON
    serialiser.  11 new tests; 2176 total passing.  No
    Qt imports.
  - [x] **38c.2 (round 187, 2026-04-26) SHIPPED** —
    `QGraphicsScene` canvas widget + palette dock layout
    in a singleton modeless `LabSetupCanvasDialog`.
    `PaletteDock` (`QTreeWidget`-backed) renders
    `default_palette()` with category-grouped collapsible
    sections, click-to-select with `item_selected(eid)`
    Qt signal entry point for 38c.3.  `CanvasView`
    (`QGraphicsView` + 1200×800 `QGraphicsScene`) — empty
    in 38c.2.  Toolbar (Clear canvas / Show all equipment)
    + status bar.  `load_setup(setup_id)` swaps the
    palette to a per-setup view via
    `palette_for_setup(setup_id)`.  12 tests covering
    singleton, modeless flag, palette population +
    grouping + signal emission, category-header
    click-suppression, load-setup happy + unknown-id
    paths, *Show all equipment* reset, empty canvas,
    *Clear canvas* button.
  - [x] **38c.3 (round 188, 2026-04-26) SHIPPED** — drag-
    source on palette (`_PaletteTree.startDrag` packages
    equipment id as `EQUIPMENT_MIME =
    "application/x-orgchem-equipment-id"` MIME payload)
    + drop target on canvas (`CanvasView.dragEnterEvent`
    + `dragMoveEvent` + `dropEvent`).  Drops place an
    `EquipmentGlyph` (`QGraphicsItemGroup` with bordered
    ellipse + name text, movable + selectable so the user
    can rearrange after placing) at the drop position.
    `place_equipment(eid, x, y)` public method on
    `CanvasView` is the same code path used by drops + by
    tests / future agent actions; emits
    `equipment_placed(eid, x, y)` Qt signal.
    `equipment_glyphs()` accessor for inspection.  10 new
    tests covering: canvas accepts drops, palette tree
    drag-enabled, place_equipment returns glyph at right
    pos, unknown-id returns None, multiple glyphs
    coexist, clear-canvas removes glyphs, glyphs are
    movable + selectable, MIME constant exported, full
    drop-event round trip, unrecognised-MIME drops are
    ignored.  Status bar updates on every placement.
  - [x] **38c.4 (round 189, 2026-04-26) SHIPPED** —
    snap-validation against Phase-38a `connection_ports`.
    Extracted `core/lab_setups.validate_port_pair(eq_a,
    port_a, eq_b, port_b)` from the existing per-setup
    validator — single-pair compatibility check (joint
    type + open-wildcard + male/female sex check for
    ground-glass joints, with hose/socket/open marked
    sex-neutral).  `ConnectionLine(QGraphicsLineItem)`
    visual: solid green for valid pairs, dashed red for
    invalid; sits beneath glyphs (zValue=-1).
    `CanvasView.connect_glyphs(g_a, port_a, g_b, port_b)`
    instantiates the line + emits
    `equipment_connected(eid_a, port_a, eid_b, port_b,
    error_or_empty)` Qt signal.  Glyph-level self-loop
    check sits in the canvas (the equipment-level check
    in `validate_port_pair` was wrong — two RBFs share
    the same `Equipment` instance from the frozen
    catalogue, so `is` would always trip; the canvas
    knows about distinct glyph instances).  Dialog
    status bar shows ✓ Connected / ⚠ Port mismatch.  9
    new tests covering: valid pair, two-female-joints
    rejected, unknown-port rejected, open wildcard
    accepts anything, connect_glyphs creates line +
    emits signal, invalid pair dashes red, z-value below
    glyphs, unknown-equipment returns None, clear-canvas
    drops lines.  31 canvas tests total.
  - [x] **38c.5 (round 190, 2026-04-26) SHIPPED** —
    agent actions + *Build on canvas* integration; closes
    Phase 38c.  New `agent/actions_lab_canvas.py` module
    with 5 actions in the `lab-canvas` category:
    `open_lab_setup_canvas(setup_id="")`,
    `place_equipment_on_canvas(equipment_id, x, y)`,
    `connect_canvas_equipment(eid_a, port_a, eid_b,
    port_b)`, `clear_lab_setup_canvas()`,
    `lab_setup_canvas_state()` (JSON snapshot of glyphs +
    connections for tutor introspection).
    `LabSetupCanvasDialog.populate_from_setup(setup_id)`
    method places equipment in a horizontal row + draws
    every connection from the seeded Phase-38b setup.
    *Build on canvas* button added to the Phase-38b
    `LabSetupsDialog` footer (enabled when a setup is in
    focus); clicking it opens the canvas + calls
    `populate_from_setup`.  17 new tests covering all 5
    actions + populate_from_setup + the new button.

**Phase 38c COMPLETE** (rounds 186-190).  Five sub-phases
shipped over 5 rounds: headless palette → Qt scaffolding
→ drag/drop → snap-validation → agent actions.  46 tests
across the canvas suite.  Phase 38d (process simulator)
is the next big multi-round chunk; Phase 38e (Reactions-
tab integration) + Phase 38f (extended agent actions) are
queued.
- **38d — Process simulator**: per-setup state machine that
  animates the sequence ("turn on heat → vapour rises →
  condenser cools → receiver fills"), with adjustable
  parameters (heating rate, condenser temperature) and a
  pedagogical commentary track.  Sub-phases:
  - [x] **38d.1 (round 192, 2026-04-26) SHIPPED** —
    headless state-machine layer (`core/process_simulator.py`).
    `Stage` frozen dataclass + `ProcessSimulator` linear-
    state driver + `simulator_for_setup(setup_id)` builder.
    5 of 8 Phase-38b setups have scripts (simple +
    fractional distillation share `_distillation_stages`
    via a `with_column` flag; reflux, vacuum filtration,
    recrystallisation each have their own).  15 new tests.
  - [x] **38d.2 (round 193, 2026-04-26) SHIPPED** —
    canvas-animation playback dock.
    `SimulationDock(QWidget)` with Play / Pause / Step /
    Reset buttons + speed slider (0.5× to 4×) + stage
    label + description text + progress bar.  `QTimer`
    (10 Hz tick) drives auto-advance based on per-stage
    `duration_seconds` × speed.  Signals
    `stage_changed(stage_id, stage_index)` + `finished()`.
    Wired into `LabSetupCanvasDialog` via a *Run
    simulation* toolbar button + a bottom dock.
    `simulation_dock()` accessor for tests.
    **Refactor**: extracted `EquipmentGlyph` +
    `ConnectionLine` to `gui/dialogs/lab_canvas_items.py`
    so `lab_setup_canvas.py` stays under the 500-line cap
    after the simulator wiring lands.  14 new tests.
  - [ ] 38d.3 — pedagogical commentary track + parameter
    tweaks (heating rate, condenser temperature)
  - [x] **38d.4 (round 194, 2026-04-26) SHIPPED** — 7
    agent actions in the new `simulator` category +
    the 3 remaining setup scripts.  Actions:
    `start_process_simulation(setup_id)` (opens dialog +
    populates from setup + binds simulator + auto-plays),
    `simulator_state` (JSON snapshot for tutor
    introspection), `simulator_step` / `simulator_reset` /
    `simulator_play` / `simulator_pause`,
    `set_simulator_speed(speed)` (clamped 0.5 - 4.0).
    Setup scripts: Soxhlet extraction (6 stages including
    siphon trip), liquid-liquid extraction (6 stages
    including invert+vent + settle), reflux-with-addition
    (6 stages including dropwise).  All 8 Phase-38b setups
    now have simulator scripts.  15 new tests + 1 round-193
    test updated for the new "all setups scripted" reality.

**Phase 38d skipped sub-phase 38d.3 (per-stage canvas
choreography polish)** — left as a low-priority future
follow-up since the dock's text commentary already gives
the pedagogical content; visual flashing of glyphs is
icing, not core function.
- **38e — Connection between the simulator and the
  Reactions tab**: pick a seeded reaction, select the
  matching setup, watch the apparatus + reaction co-animate.
- **38f — Agent actions**: `list_equipment` /
  `list_setups` / `open_lab_setup(setup_id)`.

### Risk + scope reality check
This is the largest user-flagged feature since Phase 36.
Probably 6-10 rounds.  38a + 38b are pure-headless
catalogues and ship in 1 round each.  38c (canvas +
palette) is the Phase-36-equivalent UI work and would
take 2-3 rounds.  38d (simulator + animation) is the
hardest piece — likely 2 rounds for the state-machine
core + 1 for the animation polish.  Scope-wise, the
non-trivial design call is *what level of physical
fidelity does the simulation aim for?*  The honest
answer for an undergraduate teaching tool is "schematic
animation", not real CFD — fluid flow shown as moving
particles + colour gradients, not Navier-Stokes.

---

## Phase 36 — Molecular drawing tool (ChemDraw-equivalent) *(NEW — 2026-04-24; user-flagged)*

User directive (2026-04-24): *"add molecular drawing tool — same
abilities as chemdraw"*.

Motivation.  Every workflow in the app currently starts from a
SMILES string or a seeded database row — a real limitation when
a student asks *"what about this structure I just thought of?"*.
Giving users a live canvas where they can place atoms + bonds,
pull templates off a palette, annotate stereochemistry, and
round-trip their drawing to a SMILES / mol block instantly
unlocks every downstream feature of the app (3D viewer,
descriptors, retrosynthesis, spectroscopy prediction,
fragment search, …) for structures that aren't in the DB.

Scope reality check.  PerkinElmer's commercial ChemDraw has 40+
years of polish.  Reproducing every bell and whistle isn't the
goal; the goal is **a competent educational structure editor** —
what undergrads + medicinal-chem students use 95 % of the time.
Specifically: place atoms + bonds + rings + common FGs, annotate
stereochemistry + charges + isotopes, select + move + delete,
undo/redo, round-trip to RDKit SMILES, export PNG/SVG/MOL.
Not in scope: reaction query editor, advanced 2D clean-up that
matches ChemDraw's "clean structure" button exactly, polymer /
macrocycle notation, proprietary CDX binary I/O.

### Design outline

- **Canvas.**  New `orgchem/gui/panels/drawing_panel.py` built on
  `QGraphicsView` + `QGraphicsScene`.  Atoms are
  `QGraphicsEllipseItem` subclasses carrying `element`, `charge`,
  `radical`, `isotope`, `h_count` fields; bonds are
  `QGraphicsLineItem` subclasses carrying `order` (1/2/3/
  aromatic), `stereo` (none/wedge/dash/either), `begin` / `end`
  atom references.  Scene grid optional (snap-to-0.25-Å).
- **Tool palette.**  Left dock with one button per tool: select,
  erase, atom types (C/N/O/P/S/halogens + custom), single /
  double / triple bond, wedge / dash bond, ring templates
  (benzene, cyclohexane, cyclopentane, cyclobutane, cyclopropane),
  FG templates (COOH, CHO, C=O, NH₂, NO₂, CN, OH, OMe).  Active
  tool drives the canvas-click behaviour.
- **RDKit bridge.**  `orgchem/core/drawing.py` — pure-Python
  module with `Structure` dataclass (atoms + bonds) ↔ RDKit
  `Mol` round-trip via `MolFromMolBlock` / `MolToSmiles`.
  Keeps the GUI module Qt-free at its core so SMILES round-
  trips are fully headless-testable.
- **Undo/redo.**  `QUndoStack` + `QUndoCommand` subclasses
  (`AddAtomCommand`, `AddBondCommand`, `DeleteCommand`, `MoveCommand`,
  `ChangeAtomTypeCommand`, …).  Ctrl-Z / Ctrl-Shift-Z bindings.
- **SMILES paste.**  A ribbon input: paste / type a SMILES, hit
  Enter, canvas rebuilds from RDKit's 2D layout.  Instant mode
  switch between "I drew this" and "I have SMILES".
- **Export.**  *File → Export drawing…* writes PNG / SVG / MOL
  via the existing Phase 20 export helpers.  *File → Paste
  into workspace* ships the SMILES back to the Molecule
  Workspace as a new row.

### Sub-phases

- [x] **36a. `Structure` core + SMILES round-trip — shipped (round 124).**
      New `orgchem/core/drawing.py` with `Atom` (element, charge,
      isotope, radical, aromatic, h_count, chirality ∈
      {none/CW/CCW}), `Bond` (begin_idx, end_idx, order 1/2/3/
      aromatic, stereo ∈ {none/wedge/dash/either}), and
      `Structure` (atoms + bonds + `add_atom` / `add_bond` /
      `neighbours`) dataclasses.  Round-trip helpers: `structure_from_smiles`,
      `structure_to_smiles`, `structure_from_molblock`,
      `structure_to_molblock` — all RDKit-backed, all return
      ``None`` on malformed input rather than raising.  Round-trip
      preserves formal charges, isotopes, radicals,
      atom-centric tetrahedral chirality, and bond-directional
      stereo.  No Qt imports; fully headless-testable.  21 new
      pytest cases in `tests/test_drawing_core.py`: dataclass
      ergonomics (self-loop + out-of-range bond rejection,
      neighbour lookup, bad-stereo-tag fallback, element
      default), 7-SMILES parametric round-trip (methane,
      ethanol, benzene, glycine, L-alanine with stereo, NH₄⁺,
      aspirin), charge / isotope / stereo preservation checks,
      mol-block round-trip via phenylacetic acid, 3 bogus-
      input null-returns (empty / None / unclosed ring),
      and 2 manually-constructed structures simulating the
      Phase 36b canvas path (ethene via explicit double bond,
      NH₄⁺ via charged N with `h_count=4`).  INTERFACE.md
      entry added.

- [x] **36b. Canvas + atom-bond placement — shipped (round 125).**
      New `orgchem/gui/panels/drawing_panel.py` with
      `DrawingPanel(QWidget)` + internal `_DrawingView(QGraphicsView)`
      subclass that forwards mouse events into the panel's
      `handle_canvas_press/move/release` dispatchers.  Toolbar
      buttons: select, atom-C/N/O/P/S/F/Cl/Br/I/H, bond, erase,
      Clear-canvas.  SMILES I/O ribbon above the canvas — typing a
      SMILES + Enter rebuilds via RDKit's `Compute2DCoords`;
      garbage input is silently rejected (canvas stays as-is).
      Live `structure_changed(smiles)` signal fires after every
      mutation so downstream panels (Molecule Workspace, etc.)
      can react.  Bond-tool ergonomics: repeat clicks on the same
      atom pair cycle single → double → triple; empty-canvas
      clicks auto-place a carbon at each end (ChemDraw
      convention).  Erase reindexes every bond that pointed past
      a deleted atom so RDKit conversion doesn't crash later.
      13 new pytest-qt cases in `tests/test_drawing_panel.py`
      (atom placement, element swap, bond draw, bond-order cycle,
      auto-place-endpoints, erase + reindex, SMILES ribbon happy
      path + garbage-reject, clear, `structure_changed` signal).
      `"custom…"` atom dialog is the 36b follow-up polish; rings
      / FG templates are 36c; undo-redo is 36d.  INTERFACE.md
      entry added.

- [x] **36c. Template palette — shipped (round 129).**  New
      `orgchem/core/drawing_templates.py` carries a 20-row
      catalogue: 10 rings (cyclopropane / cyclobutane /
      cyclopentane / cyclohexane / benzene / pyridine /
      pyrimidine / furan / thiophene / pyrrole) + 10 FGs (OH /
      NH₂ / Me / COOH / CHO / C=O / NO₂ / CN / OMe / CF₃).
      `Template` / `TemplateAtom` / `TemplateBond` dataclasses;
      single `apply_template(structure, positions, template,
      anchor_pos, host_atom_idx, scale)` helper.  Two fuse
      modes: `"merge"` (rings — anchor atom fuses with host,
      n-1 atoms appended) and `"attach"` (FGs — anchor is
      added + bonded to host with `attach_order` bonds, with
      optional `auto_attach_element` for empty-canvas
      placement so empty-canvas COOH = acetic acid).  Headless
      core, no Qt imports — fully testable offline.  GUI side:
      `DrawingPanel._build_ui` adds a second toolbar row with
      `template-<name>` tool buttons; `handle_canvas_press`
      routes those tools through `_apply_template_at` which
      pushes one undo snapshot per placement (no-op guard
      preserves clean undo history) and renders only the newly
      appended atoms / bonds.  Indole + NHAc deferred (each
      adds bicycle-fusion or 4-atom chain complexity that's
      better handled in a 36c follow-up; the 20 included cover
      ≥95 % of teaching demand).  18 headless tests in
      `tests/test_drawing_templates_core.py` (catalogue
      contents, free-standing + fused ring placement,
      every FG → SMILES round-trip including the NO₂
      zwitterion + C=O double-bond attach), 13 pytest-qt
      cases in `tests/test_drawing_panel_templates.py`
      (toolbar wiring, single-click placement, fusion onto
      existing atom, undo / redo round-trip, multi-step
      undo chain after template + element swap, signal
      emission, scene-item bookkeeping).  INTERFACE.md +
      ROADMAP.md updated.

- [x] **36d. Undo / redo.**  *(round 128, 2026-04-24)* —
      snapshot-based stack in `DrawingPanel` (not `QUndoStack`).
      Every logical mutation (atom place, element swap, bond
      draw / order cycle, erase atom+bonds, drag-move
      atom, clear canvas, SMILES-rebuild) pushes a deep-copied
      `(Structure, positions)` tuple onto `_undo_stack` before
      mutating.  `undo()` / `redo()` pop the snapshot onto the
      opposite stack and rebuild the scene via
      `_restore_snapshot`.  Toolbar buttons *↶ Undo* / *↷ Redo*
      plus Ctrl+Z / Ctrl+Shift+Z shortcuts scoped to the
      widget.  Depth capped at 100 (`_UNDO_STACK_MAX`).  No-op
      guards on: re-clicking an atom with the same element,
      clicking the same atom twice with the bond tool (cancel),
      clearing an already-empty canvas.  18 pytest-qt tests
      cover every mutation type, stack bounds, redo
      invalidation on new mutation, button enable state, +
      full build-undo-redo round-trip.  Lasso select + drag
      selection + cut/copy/paste deferred to a later polish
      round (36d+).

- [x] **36e. Stereochemistry + charges + isotopes — shipped
      (round 130).**  Two new bond tools: `bond-wedge` (green
      thick pen) and `bond-dash` (blue dashed pen) wired
      through `_handle_stereo_bond_click`.  Same flow as the
      plain bond tool — empty-canvas clicks auto-place
      carbons, repeat clicks on the same pair toggle the
      stereo back to "none", different stereo replaces the
      existing tag.  Right-click on any atom opens a
      `QMenu` with Formal-charge (-2/-1/0/+1/+2), Radical
      electrons (0/1/2), Isotope label (`QInputDialog`),
      and Explicit H count (-1 / 0–4) submenus.  Each entry
      pushes one undo snapshot via the round-128 stack;
      same-value selections are no-ops.  Atom glyph
      rendering decorates non-default atoms: charge
      superscript ("+", "−", "2+", "2−") in red, isotope
      mass number as a left superscript, radical electrons
      as 1-2 bullet dots above the symbol; pure-C atoms
      promote from a dot to a labelled glyph when
      decorated.  Lone-pair decoration deferred as polish
      (the mechanism player has it; the drawing tool doesn't
      need it for SMILES round-trip).  17 pytest-qt cases in
      `tests/test_drawing_panel_stereo.py` covering tool
      registration, wedge / dash placement, toggle off, dash
      → wedge replace, empty-canvas auto-place, undo
      reverses wedge, charge / isotope / radical / H-count
      setters + their undo participation, NH₄⁺ live SMILES
      round-trip, ¹³C isotope SMILES round-trip,
      right-click-on-empty-canvas guard, V2000 mol-block
      writer emits the wedge stereo flag.  Note: RDKit's
      mol-block reader drops the bond direction on
      non-stereocenter bonds — limitation of the SMILES /
      mol-block stereo model, not a writer bug.

- [~] **36f. Reaction arrows + multi-structure schemes.**
      Split into 36f.1 (headless core) and 36f.2 (canvas
      arrow placement + Reactions-tab handoff).
    - [x] **36f.1 — headless scheme core (round 131).**  New
          `orgchem/core/drawing_scheme.py` carries the
          `Scheme` dataclass (`lhs`: `List[Structure]`,
          `rhs`: `List[Structure]`, `arrow` ∈
          `{"forward", "reversible"}`, `reagents` free-text)
          plus `from_smiles_pair`, `from_reaction_smiles`,
          `to_reaction_smiles`, `lhs_smiles` / `rhs_smiles`,
          JSON-friendly `to_dict` / `from_dict`, and
          `is_balanced_atom_counts` (heavy-atom-count sanity
          hint for the future "did you forget the leaving
          group?" prompt).  `"."`-separated SMILES on either
          side are exploded into per-component
          `Structure`s.  Empty halves serialise as the empty
          string to match RDKit reaction-SMILES convention.
          Lazy RDKit import; no Qt deps.  Agent action
          `make_reaction_scheme(lhs_smiles, rhs_smiles,
          arrow="forward", reagents="")` in
          `agent/actions_drawing.py` exposes the bundle
          operation to the tutor / scripts / stdio bridge —
          returns `{reaction_smiles, lhs_canonical,
          rhs_canonical, arrow, reagents, balanced}` on
          success, `{error}` on garbage.  22 headless tests
          in `tests/test_drawing_scheme_core.py` (defaults,
          smiles-pair construction, malformed input
          rejection, reaction-SMILES round-trip with /
          without reagents, per-side SMILES extraction,
          to_dict / from_dict round-trip incl. type-guard,
          balance hint, multi-component edge cases) + 6 new
          agent-action tests in `tests/test_drawing_actions.py`
          (registry membership, basic round-trip, reagents,
          unbalanced flag, garbage rejection, invalid-arrow
          rejection, reversible-arrow preservation).  GUI
          audit registers `make_reaction_scheme` so coverage
          stays at 100 %.
    - [x] **36f.2 — canvas arrow + Reactions-tab handoff —
          shipped (round 132).**  Two new tool keys
          (`arrow-forward` / `arrow-reversible`) on the
          DrawingPanel toolbar; clicking empty canvas places
          a single arrow polygon (`QGraphicsLineItem` shaft +
          `QGraphicsPolygonItem` head, with a stacked
          ⇌-style pair of half-arrows for reversible).  Only
          one arrow per canvas — second placement replaces the
          first, same-position no-op skipped from undo.
          `current_scheme()` partitions atoms by x-coord vs
          arrow x; `_slice_structure` builds per-side
          `Structure`s with re-indexed bonds (drops bonds
          straddling the arrow — the user's drawing said
          "these atoms became those atoms", not "this exact
          bond survived").  Snapshot tuple grew to a 3-tuple
          `(Structure, positions, arrow)` so undo/redo round-
          trips arrow placement; legacy 2-tuple snapshots
          still load defensively.  `clear()` drops the arrow.
          `DrawingToolDialog` gains a *"Send to Reactions
          tab"* footer button: prompts for a reaction name
          via `QInputDialog`, calls the round-55
          `add_reaction` authoring action with the bundled
          reaction SMILES (category `"Drawn"`), opens the
          Reactions tab, calls its `_display(rid)` with the
          new row id.  Duplicate-name path routes to the
          existing row.  16 pytest-qt cases in
          `tests/test_drawing_panel_scheme.py` (toolbar
          wiring, single-arrow constraint, repeat no-op,
          remove arrow, undo / redo / undo-after-replace,
          clear, scheme-is-None without arrow,
          atom-partition by x, bonds-crossing-arrow dropped,
          intra-side bonds preserved with canonical SMILES
          round-trip, arrow-kind propagation, one-empty-side
          edge case, charge survives partitioning) + 5 new
          dialog tests in `tests/test_drawing_tool_dialog.py`
          (button visible, no-arrow info, add_reaction
          invocation, duplicate handling, user-cancel,
          empty-side info).

- [x] **36g. File + workspace integration.**  *(round 126,
      2026-04-24)* — `DrawingToolDialog` in
      `orgchem/gui/dialogs/drawing_tool.py` wraps the Phase-36b
      `DrawingPanel` and is reachable from *Tools → Drawing
      tool…* (Ctrl+Shift+D).  Singleton preserves the canvas
      across re-opens; optional `seed_smiles=` preload for
      future *Open in drawing tool…* handoffs.  Footer:
      *Export drawing…* writes PNG / SVG via
      `render.export.export_molecule_2d`, MOL-V2000 via
      `core.drawing.structure_to_molblock`.  *Send to Molecule
      Workspace* invokes the `add_molecule` authoring action
      with a pollution-safe `Drawn-XXXXXXXX` UUID name +
      `source_tags=["drawn"]`, handles duplicate InChIKey via
      the `existing_id` code path, and fires
      `bus.molecule_selected` so every other panel picks up
      the new row.  11 pytest-qt tests cover singleton,
      export-empty, MOL / PNG export, duplicate handling, and
      error-surfacing.

- [x] **36h. SMILES import ribbon + agent actions.**  *(round
      127, 2026-04-24)* — SMILES import ribbon already shipped
      in 36b (round 125) via `DrawingPanel._smiles_edit`.  The
      new-in-127 piece is the agent-action surface in
      `orgchem/agent/actions_drawing.py`:
      `open_drawing_tool(smiles="")` lazily creates the
      dialog singleton + optional SMILES preload;
      `drawing_to_smiles()` returns canonical SMILES +
      `{n_atoms, n_bonds}`; `drawing_export(path)` writes
      PNG / SVG / MOL by suffix (rejects anything else);
      `drawing_clear()` wipes the canvas.  All four marshal
      onto the Qt main thread via
      `_gui_dispatch.run_on_main_thread_sync` and return
      `{"error": ...}` rather than raising when the GUI isn't
      reachable.  GUI_ENTRY_POINTS entries added — audit
      coverage stays at 100 %.  15 pytest-qt cases cover
      registration, open w/ + w/o seed, missing-main-window
      error, SMILES read (full + empty), export (missing
      dialog, empty canvas, bad extension, MOL + PNG happy
      paths), clear (missing + empty + populated), and an
      end-to-end *open → seed → clear → set-to-pyridine →
      export → round-trip* test.

### Phase 36 status — 8 / 8 sub-phases COMPLETE 🎉
- 36a ✅ headless core (round 124)
- 36b ✅ canvas widget (round 125)
- 36g ✅ dialog + workspace integration (round 126)
- 36h ✅ agent actions (round 127)
- 36d ✅ undo / redo (round 128)
- 36c ✅ ring / FG templates (round 129)
- 36e ✅ stereo wedges + charges + isotopes (round 130)
- 36f.1 ✅ scheme dataclass + reaction-SMILES helpers + agent action (round 131)
- 36f.2 ✅ canvas arrow + Reactions-tab handoff (round 132)

### Phase 36 polish (post-close)
- [x] **Tapered-polygon wedges + hashed-ladder dashes (round 135).**
      Replaced the round-130 pen-only wedge / dash rendering with
      proper geometry.  Wedge = `QGraphicsPolygonItem` triangle —
      apex at the begin atom, base at the end atom (ChemDraw's
      "projects out of the page" convention).  Dash =
      `QGraphicsItemGroup` of perpendicular hash lines that widen
      from the begin atom toward the end atom (ChemDraw's
      "projects behind the page" convention).  New
      `_build_bond_visual(idx)` factory dispatches by stereo;
      `_refresh_bond` swaps scene items wholesale rather than
      mutating in-place across visual types.  Hash spacing /
      half-width / wedge half-width tunables surfaced as class
      attributes so future sizing tweaks land in one place.  15
      new pytest-qt cases in `tests/test_drawing_panel_wedge_geometry.py`
      lock the geometry: wedge is a 3-vertex polygon, apex at
      begin atom, base centre at end atom, base perpendicular to
      bond axis, base width = 2 × `_WEDGE_HALF_WIDTH_PX`, wedge
      brush is the wedge-green colour, dash is a multi-line
      group with hashes that widen toward the end atom, atom
      drag updates the geometry live, stereo flips swap the
      visual type cleanly without leaking scene items.
- [ ] Lasso select + drag-move (multi-atom selection).
- [ ] Indole + NHAc ring / FG templates.
- [ ] Reagents-above-arrow text editor.

### Open questions / risks

- **Layout quality.**  RDKit's `Compute2DCoords` is fine for
  most teaching molecules but lags ChemDraw's 2D-clean for
  fused-ring natural products.  Phase 36 ships RDKit coords
  as-is; optional integration with ChemAxon's layout
  algorithm is out of scope.  If a drawing comes out ugly,
  the user can always manually reposition atoms.
- **CDX / CDXML compatibility.**  Out of scope.  Mentioning
  explicitly so nobody thinks it's a miss — this is the
  single ChemDraw feature we aren't reproducing.
- **Touch / stylus.**  Not targeted (desktop-first app).
  Qt's `QGraphicsView` gives us touch events for free; a
  later polish round could add gesture shortcuts, but
  mouse-first is fine.
- **Canvas size + perf.**  Teaching targets rarely exceed
  50 heavy atoms; `QGraphicsScene` handles thousands without
  effort.  No special perf work needed.

---

## Phase 35 — Universal synonyms + synonym-aware search *(NEW — 2026-04-24; user-flagged)*

User directive (2026-04-24): *"add synonyms to all molecules and
have this be a field that is populated when molecules are loaded.
The synonyms need to be incorporated in all searches etc so users
can find molecules of interest."*

Current state (round 58 baseline):
- `Molecule.synonyms_json` column exists and holds a JSON list
  (e.g. `["Acetaminophen", "Paracetamol", "APAP"]`).
- `orgchem/db/seed_synonyms.py` has a **curated** map (~dozens of
  entries) plus InChIKey-based cross-catalogue reconciliation
  (any molecule whose key matches a Lipid / Carbohydrate /
  Nucleic-acid catalogue entry inherits that entry's canonical
  name as a synonym).
- `db/queries.py::list_molecules` + `find_molecule_by_name` already
  hit `synonyms_json` via `ILIKE '%q%'`.
- `core/fulltext_search.py` reads `synonyms_json` when building
  the molecule blob.
- `sources/pubchem.py::PubChemSource.fetch` pulls synonym lists
  from PubChem and puts them in `Molecule.properties["synonyms"]`
  *— but does NOT persist them to the DB column on import.*

**Gap.** Most seeded molecules + every PubChem-downloaded molecule
ends up with an empty `synonyms_json`.  Users typing *"vitamin C"*,
*"aspirin"*, *"APAP"*, *"ASA"*, *"8-oxoguanine"*, *"Tylenol"*, …
hit only the surfaces that already consult `synonyms_json`
(browser filter, full-text search, find_molecule_by_name) and
miss the ones that don't (**command palette**, **Compare tab
lookup**, **tutor `show_molecule`**).

### Sub-phases

- [ ] **35a. Auto-persist synonyms on PubChem import.** When
      `sources/pubchem.py::PubChemSource.fetch` succeeds, the
      `Molecule.properties["synonyms"]` list is already populated.
      Wire the `download_from_pubchem` agent action (+ the search
      panel's *Import selected* button) to write this list into
      `Molecule.synonyms_json` before the DB insert.  Deduplicate
      against the canonical name + existing synonyms (case-
      insensitive) via the same `_add_syn` helper already in
      `seed_synonyms.py`.

- [x] **35b. Optional PubChem lookup in `add_molecule` (round 113).**
      Shipped the `fetch_synonyms=False` kwarg.  Pipeline: after
      RDKit validation + dedup checks pass, if the caller opted
      in, call the new
      `sources/pubchem.py::fetch_synonyms_by_inchikey(inchikey)`
      helper — which returns `[]` on any failure (missing
      `pubchempy`, HTTP / parse errors, no hit).  Raw synonyms
      pass through the same round-109
      `_looks_like_registry_id` filter to drop CAS / ChEMBL /
      UNII / InChI / InChIKey noise + dedup against the
      canonical name (case-insensitive) + cap at 10.  Cleaned
      list writes to `Molecule.synonyms_json` as JSON in the
      same transaction that inserts the row.  Accepted
      response now carries `synonyms_fetched: int` reporting
      how many natural-language aliases were persisted (0
      when offline / no match / empty — never errors the
      insert).  5 new pytest cases in
      `tests/test_add_molecule_fetch_synonyms.py` with
      monkeypatched `fetch_synonyms_by_inchikey`: default-off
      path, happy-path populates + filters CAS, empty-hit
      insert-still-succeeds, raising-lookup never bubbles up
      (helper catch-all verified via direct `_boom` call),
      and import-error-equivalent simulation via
      `sys.modules.pop` + `builtins.__import__` block.  All
      tests pollution-safe — inserted rows use the
      `Tutor-test-…` prefix that the round-94/97 purge wipes at
      session end.

- [x] **35c. Bulk backfill for existing DB rows — shipped (round 120).**
      New `orgchem/db/backfill_synonyms.py::backfill_synonyms(
      limit, rate_delay_s, min_existing, fetch_fn,
      skip_test_prefix) → BackfillCounts`.  Walks every
      `Molecule` row, skips `Tutor-test…` prefix + empty-
      InChIKey rows, queries PubChem by InChIKey via the
      round-113 `fetch_synonyms_by_inchikey` helper, filters
      registry-IDs through the round-109 palette-shared
      `_looks_like_registry_id`, dedups against the canonical
      name + existing synonyms, caps at 10 per row, writes the
      cleaned list to `synonyms_json`.  Rate-limited default
      200 ms/request stays under PubChem's 5-req/sec free-tier
      ceiling (~85 s for a full ~415-row walk).  Idempotent —
      re-runs only hit rows whose existing-synonym count is
      below `min_existing` (default 1).  Per-row failures
      swallowed so one hiccup doesn't abort the run.
      `fetch_fn` kwarg is test-injectable so pytest runs
      offline.  Companion CLI
      `scripts/backfill_molecule_synonyms.py` with
      `--limit / --rate-delay / --min-existing` flags.
      7 pytest cases (populates empty rows, respects
      min-existing, `min_existing=0` force-refresh, skips
      Tutor-test prefix, skips rows without InChIKey,
      tolerates fetch exception, `--limit` caps network
      calls).  **Phase 35 now 6/6 — CLOSED.**

- [x] **35d. Wire synonyms into the command palette (round 109).**
      `gui/dialogs/command_palette.py::_molecule_entries()` now
      emits one `PaletteEntry` per canonical row **plus** one
      extra aliased entry per synonym — same `target=mid` but
      distinct `label=synonym`, sublabel `"alias of <canonical>"`.
      `_looks_like_registry_id()` helper filters noise (CAS
      `nnn-nn-n`, pure digits, `CHEMBL\d+`, `UNII-…`, `DTXSID`,
      `InChI=…`, 27-char InChIKey pattern) so the palette stays
      readable.  Typing *"Paracetamol"* now reaches Acetaminophen
      via its synonym row; the curated round-58 `Retinol ↔
      Vitamin A` pair is likewise reachable.  2 new pytest-qt
      tests: `test_palette_emits_synonym_aliases` walks every
      row with a non-empty `synonyms_json` and proves ≥1
      reachable via its aliases; `test_palette_filter_registry_ids`
      locks the CAS/ChEMBL/UNII/InChIKey rejection rules.

- [x] **35e. Compare tab lookup + tutor name resolution (round 111).**
      Audit confirmed both surfaces already routed through
      `find_molecule_by_name`, which the round-58 patch wired to
      also ILIKE-match `synonyms_json`.  So no new code — this
      sub-phase is regression-lock-only.  9 new pytest tests in
      `tests/test_synonym_lookup_paths.py` cover the full grid:
      (a) `find_molecule_by_name` direct — resolves
      *"Paracetamol"*→Acetaminophen + *"ASA"*→Aspirin, is
      case-insensitive (`PARACETAMOL / paracetamol / paraCetaMol`
      all dispatch to the same id), returns None for unknown;
      (b) `show_molecule` agent action — resolves both synonym
      pairs + errors on unknown; (c) Compare panel slot
      `_on_load` — typing a synonym into the text field and
      loading the slot yields a title that contains the canonical
      name (proving the resolver fired), not the alias.  Future
      regressions to the round-58 ILIKE behaviour will fail
      these tests immediately.

- [x] **35f. Synonym hint in the molecule browser row (round 110).**
      `_MolListModel.data(DisplayRole)` now appends ` · <first
      synonym>` when a row carries a natural-language alias in
      `synonyms_json` (e.g. *"Acetaminophen   [C8H9NO2]  ·
      Paracetamol"*).  `ToolTipRole` extended to list every
      synonym as a "Also known as: …" line below the SMILES.
      Registry IDs (CAS / ChEMBL / UNII / DTXSID / InChI /
      InChIKey) filtered out via the shared
      `command_palette._looks_like_registry_id()` helper from
      round 109; canonical-name self-references are also
      filtered so the hint is never redundant.  5 new pytest-qt
      tests (`tests/test_molecule_browser_synonym_hint.py`):
      3 unit tests for `_first_natural_synonym` /
      `_all_synonyms` helpers (registry-noise stripping,
      empty-input handling, canonical-self-reference dedup),
      2 integration tests that walk the real seeded DB + prove
      ≥1 row shows a synonym hint + ≥1 tooltip contains
      "Also known as:".

### Design notes / risks

- **Network budget.** The bulk backfill (35c) against ~415
  molecules at 200 ms/req = ~85 s one-shot.  Fine for a
  maintainer; should not run on every app launch.  Gate behind
  an explicit `scripts/backfill_molecule_synonyms.py` CLI, not
  `seed_if_empty`.
- **Pollution risk.** PubChem synonym lists include registry
  IDs (CAS numbers, ChEMBL IDs, UNII, FDA UNII).  Filter these
  out in 35a/35c via a regex that rejects pure-numeric / hex /
  `CHEMBL\d+` / `UNII:` patterns — keep only natural-language
  names.
- **Search UX.**  With 415 molecules × ~10 synonyms each =
  ~4 k palette entries (35d).  Still well under the palette's
  fuzzy-match budget (tested fine at 10 k glossary terms + 35
  reactions in the round-54 launch).  No perf action required
  unless it proves sluggish.
- **Synergy with Phase 33 full-text search.**  Since
  `core/fulltext_search.py` already indexes `synonyms_json`,
  35a + 35c automatically improve Ctrl+F results for
  PubChem-imported molecules without further wiring — a
  nice free win.

### Cross-references to existing tasks

- Round 58 (`seed_synonyms_if_needed`) — the curated map this
  phase extends.
- Round 94 / 97 (`Tutor-test` prefix purge) — backfill must
  not touch test-pollution rows (prefix-gate before querying
  PubChem to avoid wasted requests).
- Phase 33 (cross-surface full-text search) — automatic
  beneficiary of 35a/35c.
- Phase 34 (sequence viewer) — unrelated, but both Phase-34
  and Phase-35 sequence-viewer / synonym metadata are the
  sort of "invisible polish" that makes the app feel
  professional.

---

## Phase 34 — Sequence viewer + cross-linked 3D selection *(NEW — 2026-04-24; user-flagged)*

User directive (2026-04-24): *"Add an Amino-acid sequence viewer to
the 3D protein display panel. The sequence would be displayed in a
rolling text bar, with the user able to select individual amino-acids,
or sequences of [residues] and the selection is indicated on the 3D
rendered image — and vice-versa. The DNA sequence could also be
displayed above the amino-acid sequence. And the ability to identify
and highlight genes and structures (binding pockets, ligand binding
sites) of interest."*

Motivation: the Phase 24l 3D viewer already has click-to-inspect
(picked residue bounces back to Qt via `_PickBridge` / QWebChannel
and posts to the session log), but there's no inverse path — users
can't say *"show me Ser195"* and have the atom highlight on the
ribbon.  A proper linked sequence bar closes that loop and is the
primary way every other structural-biology tool (PyMOL, ChimeraX,
UCSF Chimera, NGL Viewer, Mol*) shows protein data.  Once the
sequence strip exists, overlays for DNA coding strand, pocket
residues, and ligand-contact residues follow naturally.

### Sub-phases

- [x] **34a. Core `SequenceView` dataclass + agent action
      (round 112).**  Shipped `orgchem/core/sequence_view.py`:
      `SequenceView` (pdb_id + `protein_chains` + `dna_chains` +
      `highlights`), `ChainSequence` (chain_id, one_letter,
      three_letter, residue_numbers, kind ∈ {protein, dna, rna}),
      `HighlightSpan` (chain_id, start, end, kind, label, colour)
      — each with JSON-serialisable `to_dict()` for the Qt widget
      + agent action.  `build_sequence_view(protein)` separates
      chains by majority residue-kind; ion-only pseudo-chains
      skipped.  Helpers `attach_contact_highlights(view, report)`
      (Phase 24e contacts → per-kind coloured spans) and
      `attach_pocket_highlights(view, pockets)` (Phase 24d
      pockets → one min-max span per chain) populate the
      `highlights` list.  Shared palette `HIGHLIGHT_COLOURS`
      (pocket=#9FD5A0, ligand-contact=#F5DF50, active-site=#E88B28,
      h-bond=#4B8BD5, salt-bridge=#D04040, π-stacking=#A050C0,
      hydrophobic=#E0984B, user=#F18FB1, gene=#8080C0,
      ss-helix=#C04848, ss-strand=#4878C0).  Residue-id parser
      `_parse_residue_seq_id` coerces "HIS57", "A:HIS57", ints,
      and numeric strings to seq_id.  Agent action
      `get_sequence_view(pdb_id, include_contacts, ligand_name)`
      wrapped in `agent/actions_protein.py` — returns the full
      JSON dict, lazily stamping contact highlights if requested.
      GUI coverage dict updated.  9 pytest cases in
      `tests/test_sequence_view.py` (schema + build + both
      highlight helpers + agent-action happy path + missing-pdb
      error + residue-id coercion fuzz).  No Qt imports in core;
      fully headless-testable.

- [x] **34b. `SequenceBar` Qt widget (round 116).**  Shipped
      `orgchem/gui/widgets/sequence_bar.py` with `SequenceBar`
      (custom `QWidget`) + `SequenceBarPanel` (scroll-area +
      status-label wrapper).  Features: monospace rolling strip
      reading `SequenceView.to_dict()`, residue-number tick marks
      every 10, per-`HighlightSpan` colour-underlay bands keyed by
      `HIGHLIGHT_COLOURS` palette, click for single-residue
      selection, click-drag for span selection (clamped to the
      anchor row for cross-row drags), `selection_changed(chain_id,
      start, end)` Qt signal, multi-chain stacking (DNA/RNA above
      proteins per teaching-reading order).  8 new pytest-qt
      cases in `tests/test_sequence_bar_widget.py` covering empty
      / populated view, programmatic set/clear selection, real
      mouse-driven single + span selection, click-outside
      clearing, and the Panel-wrapper status-line round-trip.
      Mini-map for very long sequences deferred until a 500+
      residue entry shows real pain.

- [x] **34c. Two-way binding to the 3D viewer (round 116/117).**
      **Reverse path (3D → sequence) — shipped round 116.**
      `_on_atom_picked(chain, resn, resi)` now calls
      `self.sequence_panel.set_selection(chain, resi, resi)` so a
      3D click moves the sequence-bar caret onto the corresponding
      letter.
      **Forward path (sequence → 3D) — shipped round 117** via a
      new JS helper injected into every `build_protein_html`
      page: `window.orgchemHighlight(chainId, start, end)` clears
      any previous span + applies yellow-carbon sticks + residue
      labels to the new span, re-rendering in place; companion
      `window.orgchemClearHighlight()` resets to the baseline
      cartoon style.  `_on_sequence_selection` in
      `protein_panel.py` pushes the selection through
      `web_3d.page().runJavaScript(...)` — live, no HTML rebuild,
      no perceptible latency.  The (selection span, JS helper
      call) round-trip is now **fully closed**: user drags a span
      on the sequence bar → 3D ribbon shows it as sticks; user
      clicks a residue on the 3D ribbon → sequence-bar caret moves.
      New regression `test_build_protein_html_exposes_live_highlight_helper`
      checks the generated HTML exposes both helpers with the
      correct `(chainId, start, end)` signature + yellowCarbon
      stick style matching the static pipeline.

- [x] **34d. DNA strand strip — free from 34b (round 116).**
      The `SequenceBar` widget already stacks `dna_chains` rows
      above `protein_chains` rows with identical click + span
      semantics; the `build_sequence_view` builder (Phase 34a)
      classifies chains by majority residue-kind.  PDB entries
      with DNA chains (1BNA, 143D, 1HMH, 1AOI) therefore get
      the DNA strip *for free* on first render.  Dedicated
      nucleic-acid colour palette + phosphate-backbone 3D
      highlight on DNA-span selection is a polish follow-up
      (same 34c live-channel plumbing).

- [~] **34e. Feature-track overlays — pockets + contacts shipped (round 118).**
      `ProteinPanel` now caches the most-recent
      :class:`Pocket` list (`_last_pockets`) and `ContactReport`
      (`_last_contacts`) at analysis time; `_refresh_sequence_bar`
      layers both onto the `SequenceView` via the Phase-34a
      helpers `attach_pocket_highlights` (one green span per
      chain per pocket, collapsed to min-max residue range) +
      `attach_contact_highlights` (one span per contact, kind-
      coloured — H-bond blue, salt-bridge red, π-stacking purple,
      hydrophobic tan).  Caches reset on new PDB / AlphaFold
      fetch so stale features don't bleed into the next structure.
      The existing `SequenceBar._paint_row` renders the underlay
      bars with the per-kind colour from `HIGHLIGHT_COLOURS`.
      3 new pytest cases: end-to-end feature-track full-stack
      test in `test_sequence_view.py`, widget-storage regression,
      and a real `ProteinPanel._refresh_sequence_bar` integration
      test that primes fake caches then asserts the resulting
      widget state.
      **Still open (34e polish):** secondary-structure track
      (requires parsing HELIX / SHEET records in `core/protein.py`
      — the parser currently only reads ATOM / HETATM), user-
      editable tag track with session-state persistence, and
      UniProt gene-annotation track for DBREF-carrying PDBs.

- [x] **34f. Selection-aware agent actions — shipped round 119.**
      Three new `@action(category="protein")` entry points in
      `agent/actions_protein.py` give the tutor / scripts /
      stdio-bridge callers full programmatic control of the
      sequence-bar selection:
      - `select_residues(pdb_id, chain_id, start, end)` —
        dispatches to the main Qt thread via
        `_gui_dispatch.run_on_main_thread`, sets
        `SequenceBarPanel.set_selection(...)`, and calls the
        panel's `_on_sequence_selection` forward-path so the
        round-117 `orgchemHighlight` JS helper runs on the 3D
        viewer.  Auto-swaps reversed bounds.
      - `get_selection(pdb_id)` — returns `{chain_id, start,
        end}` or `{error}` when no selection exists.  Read-only,
        no Qt-thread hop.
      - `clear_selection(pdb_id)` — clears the bar; the
        `_on_sequence_cleared` handler chains into
        `orgchemClearHighlight()` for the live 3D reset.
      Shared `_get_sequence_panel()` helper resolves the
      Proteins-tab panel or returns None; all three actions
      gracefully error-return when the GUI isn't reachable
      (headless / Proteins tab not open / WebEngine missing).
      GUI_ENTRY_POINTS wiring added for all three (audit
      coverage holds at 100 %).  9 new pytest cases:
      bar-selection set, reversed-bounds swap, single-residue,
      get round-trip, empty-selection error, clear clears the
      bar, + 3 monkey-patched "no GUI" error paths.
      **Named-feature highlighting** (`highlight_feature(pdb_id,
      name)` — e.g. *"active site"* / *"signal peptide"*) is
      queued as 34f polish; needs a named-span catalogue that
      34e hasn't shipped yet.

### Design notes

- Fetch → parse → display pipeline is already in place (Phase 24a).
  This phase is **purely GUI + cross-wiring**; no new chemistry
  code.  34a is the only new `core/` module and it's thin
  (pure data extraction from the existing `Protein` dataclass).
- Long protein sequences (>500 residues, e.g. 1KCN myosin
  heavy chain) will need a mini-map + scrollbar.  Budget
  one extra widget for that.
- Multi-chain structures (haemoglobin 1HHO = 4 chains, HIV
  protease 1HPV = 2 chains) should stack chain rows vertically
  — not concatenate — so residue-numbering stays per-chain.
  The existing teaching stories already use chain-prefixed
  residue IDs (`A:SER195`, `B:HIS57`), so this is a cosmetic
  commitment.
- The DNA strand viewer is a lighter version of the same
  widget; consider refactoring 34b so 34d is a single-track
  special case.
- Testing: headless widget tests via pytest-qt with QSignalSpy
  on `selection_changed`; 3D round-trip tests can grab the
  viewer HTML and grep the `highlight_residues` arg without
  needing a real browser.

---

## Phase 30 — Unified Macromolecules window *(NEW — 2026-04-23; user-flagged; COMPLETE 2026-04-23)*

User directive (2026-04-23): *"I think all macromolecules should be in
a separate GUI that is accessed [via] a new menu item."* The Phase 29
sibling tabs (Proteins / Carbohydrates / Lipids / Nucleic-acids)
currently crowd the main-window tabbar and force every user — even
those focused on small-molecule work — to scroll past them. Phase 30
extracts them into a dedicated top-level window so the main window
stays focused on small-molecule workflows, and so the four
macromolecule panels can share a richer common toolbar (sequence-view
toggle, PDB fetch, 3D cartoon, export) without clashing with the main
menu.

- [x] **30a. `MacromoleculesWindow` class.** A new top-level
      `QMainWindow` hosting the Proteins / Carbohydrates / Lipids /
      Nucleic-acids panels as inner tabs. Lives in
      `orgchem/gui/windows/macromolecules_window.py`. Remembers its
      size + last-active tab across sessions (via `QSettings`).
- [x] **30b. Menu entry.** A new *Window → Macromolecules…* action
      on the main window constructs-or-raises the window (single
      persistent instance, not modal). Ctrl+Shift+M accelerator.
      Agent action `open_macromolecules_window(tab)` shipped in
      `agent/actions_windows.py`.
- [x] **30c. Migrate existing panels.** Proteins / Carbohydrates /
      Lipids / Nucleic-acids removed from the main-window tabbar.
      Panels are still constructed once in `MainWindow._build_central`
      and reparented into the secondary window — `win.proteins` etc.
      remain valid attributes so existing agent actions / tests
      keep working.
- [x] **30d. GUI-wiring audit updates.** Every macromolecule agent
      action's `GUI_ENTRY_POINTS` entry now reads
      `"Window → Macromolecules… → {sub-tab} → …"`. New entry for
      `open_macromolecules_window` itself. Coverage gate still 100 %.
- [x] **30e. Cross-panel messaging.** The NA panel's *Fetch PDB*
      button now calls
      `main_window().open_macromolecules_window(tab_label="Proteins")`
      then populates the protein panel's ID field and triggers
      fetch — all inside the secondary window.
- [x] **30f. Tests.** `tests/test_macromolecules_window.py` (9 tests)
      exercises: panels absent from main tabbar, window opens and
      returns same instance on re-open, four inner tabs present,
      `switch_to` focuses and rejects unknown labels, inner panels
      are identity-equal to `win.proteins` etc., agent action works,
      audit entry exists, coverage still 100 %. Full suite: **676
      passed, 1 skipped** (+9).

---

## Phase 29 — Macromolecule tabs (carbohydrates, lipids, nucleic acids) *(NEW — 2026-04-23; user-flagged)*

Sibling tabs for the Proteins tab. Each has its own 2D / 3D
conventions, its own seeded teaching examples, and its own
descriptor panels — trying to squeeze them into the general
molecule viewer loses clarity. Reuses the Phase 24a-k protein
stack where possible (PDB parsing / 3Dmol.js viewer / pLDDT
overlay).

- [x] **29a. Carbohydrates tab.** 2D Haworth + chair / boat
      renderers; 3D via the existing 3Dmol.js path. Seed
      glucose (α/β pyranose + open-chain), fructose (both
      furanose + pyranose), sucrose, lactose, maltose, starch
      fragment (amylose), cellulose fragment. Descriptors:
      glycosidic bond count, D/L designation, anomeric configuration.
- [x] **29b. Lipids tab.** Seed the canonical families: saturated
      fatty acid (stearic), unsaturated (oleic / linoleic / DHA),
      triglyceride, phospholipid (phosphatidylcholine), cholesterol,
      sphingomyelin, vitamin D₃. Rendering: skeletal with chain
      abbreviations for C ≥ 8 so a 24-C lipid fits on screen.
      Descriptors: chain length, degree of unsaturation, ω-3/ω-6
      position, melting-point estimate.
- [x] **29c. Nucleic-acids tab.** Sits on top of Phase 24a
      `protein.py` parser (already handles A/T/G/C/U residues).
      Seed: canonical B-form DNA dodecamer, G-quadruplex, tRNA^Phe,
      a hammerhead ribozyme. Displays: sequence view (strings with
      base-pair bracket annotation), secondary-structure dot-paren,
      3D duplex via 3Dmol.js cartoon. Reuses the Phase 24k NA-ligand
      contact analyser for loaded ligands.
- [ ] **29d. Cross-tab integration.** The Proteins tab's PDB
      viewer recognises nucleic-acid-containing PDBs and defers
      the NA portion to the Nucleic-acids tab for richer display.
      Carbohydrate / lipid links in the Glossary tab jump to the
      matching macromolecule tab.
- [x] **29e. Agent actions.** `list_carbohydrates`,
      `get_carbohydrate`, `carbohydrate_families`, `list_lipids`,
      `get_lipid`, `lipid_families`, `list_nucleic_acids`,
      `get_nucleic_acid`, `nucleic_acid_families` — shipped in
      `agent/actions_carbohydrates.py` and
      `agent/actions_lipids_na.py`.

---

## Phase 28 — Molecule browser: multi-category filters *(NEW — 2026-04-23; user-flagged)*

The left-dock molecule browser filters by a single text substring
today. Phase 28 lets users drill into the DB by *kind* — functional
groups, biological origin, drug class, elemental composition,
charge arrangement, atom-count bands. Expected UI: a filter bar
above the list with **two rolling combo boxes** (category axis →
value) plus the existing free-text field; multiple filter axes
AND together.

- [x] **28a. DB schema extension.** `Molecule` gains two new
      optional columns: `source_tags_json` (a JSON list of
      taxonomy tags like `"plant"`, `"pigment"`, `"hormone"`,
      `"metabolite"`, `"NSAID"`, `"statin"`, etc.) and
      `functional_group_tags_json` (a JSON list of groups auto-
      derived from SMARTS matches: `"carboxylic_acid"`,
      `"alcohol"`, `"aromatic"`, `"amine"`, `"ester"`,
      `"heterocycle"`, `"ketone"`, `"aldehyde"`, `"halide"`,
      `"nitrile"`, …). Plus cached numeric fields for fast
      filtering: `heavy_atom_count INT`, `formal_charge INT`,
      `n_rings INT`, `has_stereo BOOL`. Additive migration in
      `db/session.py` like Phase 26a.
- [x] **28b. Category taxonomies.** Curated lists of categories the
      UI exposes:
      - **Source / origin** — plant natural product, animal
        hormone, bacterial metabolite, fungal metabolite, synthetic
        drug, endogenous metabolite, dye / pigment, terpene,
        alkaloid, amino-acid, carbohydrate, lipid.
      - **Drug class** — NSAID, statin, beta-blocker, SSRI, PPI,
        antibiotic (β-lactam / macrolide / fluoroquinolone),
        antiviral, antihistamine, opioid, corticosteroid,
        chemotherapy agent.
      - **Functional group** — carboxylic acid, alcohol / phenol,
        amine (1°/2°/3°), amide, ester, ether, aldehyde, ketone,
        nitrile, halide, aromatic, heterocycle (N/O/S), sulfonate,
        phosphate, nitro.
      - **Composition** — contains halogen / P / S, organic only
        (C/H/N/O/S/halogens), has metal.
      - **Charge** — neutral, cation, anion, zwitterion.
      - **Atom-count bands** — small (≤ 12 heavy atoms) / medium
        (13–30) / large (31+); ring count 0 / 1-2 / 3+.
- [x] **28c. Auto-tagger.** `orgchem/core/molecule_tags.py` —
      `auto_tag(mol)` returns `{"functional_groups": [...],
      "composition_flags": [...], "charge_category": ...,
      "size_band": ...}`. Driven by a SMARTS catalogue similar to
      the Phase 19c bioisosteres / Phase 8d retro templates. Source
      and drug-class tags come from the seed data (`seed_molecules_extended.py`
      already groups by section — wire those into the JSON column).
- [x] **28d. Molecule browser UI.** Filter bar above the list with:
      *Axis 1* combo (category type) + *Value 1* combo (populated
      from the axis), *Axis 2* + *Value 2*, free-text SMILES /
      name field. AND semantics across axes; "clear filters" button;
      result count shown beside the filter bar. Backed by a
      `Molecule.query_by_tags(...)` helper in `db/queries.py`.
- [x] **28e. Agent actions.** `list_molecule_categories()`,
      `filter_molecules(axis_a, value_a, axis_b, value_b,
      text_query)` on the existing **molecule** category.
      *(round 40, 2026-04-23)*
- [ ] **28f. Tests.** Auto-tagger round-trip for seeded molecules
      (e.g. aspirin gets `carboxylic_acid` + `ester` + `aromatic`),
      DB query by tag, combined AND filter, GUI filter bar drives
      the underlying `list_molecules()` query.

---

## Phase 27 — Interactive periodic table *(NEW — 2026-04-23; user-flagged)*

A clickable periodic table of elements, reachable as a **Tools →
Periodic Table…** menu item (plus an agent action for programmatic
access). Useful as a quick reference while students work through
problems and as a building block for later features (reaction
compatibility, element-filtering in search, electronegativity-based
pKa hints, etc.).

- [x] **27a. Data module.** `orgchem/core/periodic_table.py` —
      minimal dataclass `Element(symbol, name, z, group, period,
      block, atomic_mass, electronegativity, common_oxidation_states,
      electron_configuration, category)` seeded with all 118 elements
      (main-group + transition + lanthanide + actinide). Use
      RDKit's `PeriodicTable` where possible to avoid duplicating
      masses; hand-seed the pedagogical columns (category, common
      oxidation states, etc.) from a trusted source (NIST or IUPAC).
- [ ] **27b. Renderer.** `orgchem/render/draw_periodic_table.py`
      builds a Qt-friendly SVG of the classic 18-column layout.
      Cells colour-coded by category (alkali metal, halogen, noble
      gas, transition metal, lanthanide, actinide, metalloid,
      nonmetal, post-transition metal). Lanthanide / actinide rows
      shown below the main block with a leader arrow.
- [x] **27c. Dialog.** `orgchem/gui/dialogs/periodic_table.py` —
      clickable grid (each cell = a `QPushButton` / `QToolButton`);
      hovering shows a tooltip with the element's full name + mass.
      Clicking opens a side-pane with the full `Element` record and
      a link to the matching glossary term if one exists.
- [x] **27d. Menu entry.** *Tools → Periodic Table…* (Ctrl+Shift+T).
      Registered in the GUI audit so coverage ticks up.
      *(round 36, 2026-04-23)*
- [x] **27e. Agent actions.** `list_elements()`, `get_element(symbol_or_z)`,
      `elements_by_category(cat)` on a new **periodic** category.
      *(round 35, 2026-04-23)*
- [ ] **27f. Tests.** Element count = 118, every row has
      symbol/name/z/mass, category palette covers every element,
      dialog opens headlessly, agent round-trip.
- [ ] **Follow-up**: highlight-on-selection mode — selecting a
      molecule in the browser highlights its constituent elements in
      the periodic-table dialog (teach *"where on the table does
      this molecule live?"*).
- [ ] **Follow-up**: pair with Phase 26 glossary figures so clicking
      an element opens its canonical glossary figure (if seeded).

---

## Phase 26 — Example figures on glossary entries *(NEW — 2026-04-23; user-flagged)*

The glossary already carries markdown definitions with aliases + see-
also cross-refs, but many terms would land much faster with a
figure. Each entry should optionally ship an illustrative image
(2D structure / mechanism snippet / MO diagram / stick spectrum /
3D side-by-side) that the Glossary tab renders inline beneath the
definition.

- [x] **26a. Schema extension.** `GlossaryTerm` model gained
      `example_smiles` and `example_figure_path` columns; the
      additive migration in `db/session.py` ALTERs existing
      `glossary_terms` tables on startup. `seed_glossary` threads
      both fields through insert + update paths, bumped
      `SEED_VERSION` to 3, and seeded 4 anchor terms (Aromaticity,
      Carbocation, Diels-Alder reaction, Aldol reaction) with
      `example_smiles`. 6 tests cover the schema, seed write, and
      the legacy-DB upgrade path. *(round 32, 2026-04-23)*
- [x] **26b. Auto-generator.** `orgchem/core/glossary_figures.py`
      + `scripts/regen_glossary_figures.py` walks every term with
      `example_smiles` and renders PNG / SVG via `draw2d` (single
      molecule) or `draw_reaction` (reaction SMILES). Incremental
      by default; `--force` overwrites. Agent action
      `get_glossary_figure(term, path, fmt)`. 11 tests.
      *(round 33, 2026-04-23)*
- [ ] **26b follow-up.** Per-term overrides: mechanism terms render
      a `MechanismStep` via `draw_mechanism`, MO terms render via
      `draw_mo`, orbital-symmetry terms pull from the W-H catalogue.
- [ ] **26c. Seeded figures.** Hand-curated SMILES / SMARTS /
      reference images for ~15 anchor terms:
      *aromatic*, *carbocation*, *carbanion*, *curly arrow*,
      *tetrahedral intermediate*, *oxyanion hole*, *Schiff base*,
      *Diels-Alder*, *EAS*, *aldol reaction*, *SN2*, *catalytic
      triad*, *in-line phosphoryl transfer*, *retrosynthesis*,
      *atom economy*. Each entry in `seed_glossary.py` gets an
      `example_smiles=...` field.
- [ ] **26d. GUI integration.** The Glossary tab's definition pane
      switches from plain-markdown to an SVG-aware renderer that
      loads the figure below the definition (cached from
      `data/glossary/`). Agent action `get_glossary_figure(term,
      path)` exports a stored figure to disk.
- [ ] **26e. Tests.** Seed-schema round-trip, figure cache hit vs
      miss, Glossary panel renders a figure when present and falls
      back cleanly when absent.

---

## Phase 25 — GUI wiring audit & status check *(COMPLETE — 2026-04-23; user-flagged)*

**As of round 38: 97 / 97 agent actions have GUI entry points = 100 %
coverage.** The `tests/test_gui_audit.py` guard-rail is now pinned at
100 %, so any future agent action must land with a GUI wiring or the
tests fail.


A full-tree review to make sure every feature the back-end provides
is reachable from the GUI (not only from the agent action registry),
and that nothing is a placeholder / stub. Output: a checklist in
`PROJECT_STATUS.md` listing every back-end module with its GUI entry
point, flagging any gaps to close.

- [x] **25a. Inventory** — `orgchem/gui/audit.py` holds a hand-
      maintained `GUI_ENTRY_POINTS` dict keyed by agent-action name;
      `audit()` / `audit_summary()` walk the full registry and
      surface every action alongside its user-facing path or
      *"— missing"*. `scripts/audit_gui_wiring.py` prints the full
      table. `tests/test_gui_audit.py` gates coverage at ≥ 60 % and
      sanity-checks entry strings. Baseline: **65.6 %** (61 of 93
      actions wired). *(round 32, 2026-04-23)*
- [ ] **25b. Surface every core feature in a menu, panel, or
      dialog.** Known candidates to verify:
      - ~~Retrosynthesis (single + multi-step) — agent only → add a
        *Retrosynthesis* dialog or Tools menu entry.~~ *(round 33,
        2026-04-23 — landed as Tools → Retrosynthesis… dialog)*
      - SAR series (Phase 19a) — agent only → add a *SAR matrix*
        viewer.
      - Bioisostere suggester (Phase 19c) — agent only → add a
        *Bioisosteres…* dialog.
      - Drug-likeness report (Phase 19b) — exposed via properties
        panel? verify.
      - Green metrics (Phase 17a/18a) — agent only → either a
        *Green metrics* column on the Reactions tab or a dialog.
      - Lab techniques (Phase 15a-lite) — agent only → *Lab
        techniques…* dialog.
      - Naming rules (Phase 12) — agent only → *IUPAC rule
        browser* (maybe a dock or Glossary-style panel).
      - NMR / MS predictors (Phase 4) — agent only → Tools menu
        dialogs mirroring the HRMS / EI-MS dialogs.
      - Energy profile viewer (Phase 13) — reachable from the
        Reactions tab; verify coverage of all 9 seeded profiles.
      - TLC / Rf predictor (Phase 15b) — agent only → *TLC
        simulator…* dialog.
      - Mechanism player — verify it exposes lone pairs + bond-
        midpoint arrows the Phase 13c round-28 work introduced.
      - Fragmentation dialog — exists (round 26); verify output
        width / column sizing.
- [ ] **25c. Stub hunt** — grep `orgchem/gui/` for `QLabel("…stub
      …")`, `_stub(`, `TODO`, `pass  # …`, `NotImplementedError` and
      resolve each hit (implement, or remove if dead).
- [ ] **25d. Smoke test** — extend `tests/test_smoke_headless.py`
      with a "walk every tab, click every top-level action" test
      that asserts no dialog raises and no panel crashes on empty
      state.
- [ ] **25e. Publish the audit** — drop a checklist into
      `PROJECT_STATUS.md` under *"GUI coverage"* and tick items as
      they land. When the checklist is empty, the status-check is
      done.

---

## Phase 23 — Accessibility & internationalisation *(NEW — planned 2026-04-22)*

- [ ] Screen-reader labels on every interactive widget; tab-order
      audit.
- [ ] Keyboard-only navigation: every menu + panel action reachable
      without the mouse.
- [ ] Extract all user-visible strings into `orgchem/i18n/`;
      first translation target — Spanish (largest undergraduate
      chemistry population after English).
- [ ] RTL-language support audit for the tutor / log panels.

---

## Cross-cutting, any phase
- [x] ~~Image export (2D molecule → PNG / JPG / SVG) + widget screenshots~~ (2026-04-22)
- [x] ~~Agent actions for export + screenshots so LLMs can drive visual tests~~ (2026-04-22)
- [x] ~~`scripts/visual_tour.py` canonical-state gallery~~ (2026-04-22)
- [x] ~~Matplotlib-based headless 3D renderer (for CI / agent mode)~~ (2026-04-22)
- [x] ~~Shaded-sphere upgrade for matplotlib 3D~~ (2026-04-22)
- [x] ~~Compact default window size (1280×780, min 960×640)~~ (2026-04-22)
- [x] ~~Matplotlib 3D framing fix (bbox_inches=tight + ax.set_position)~~ (2026-04-22)
- [x] ~~UTF-8 SVG encoding so non-ASCII arrow labels render correctly~~ (2026-04-22)
- [x] ~~Window-geometry persistence (QSettings round-trip)~~ (2026-04-22)
- [ ] Offline mode: bundle 3Dmol.js as a local file, cache PubChem hits.
- [ ] Screenshot regression: golden-file diff under `tests/golden/` so CI
      can detect unintended rendering changes.
- [ ] pytest-qt UI tests (launch `MainWindow`, drive it through signals,
      click buttons, verify resulting screenshots).
- [ ] IUPAC naming — integrate STOUT or cached PubChem lookups for
      user-imported molecules.
- [ ] Configurable theming (dark mode; already an empty `theme` field in
      `AppConfig`).
- [ ] Bond-midpoint arrow origins + H-atom arrow targets for the
      mechanism player (Phase 2b polish).
- [ ] i18n — extract strings for translation (low priority until demand).
- [ ] Package as a distributable app: PyInstaller bundle, Homebrew
      formula, maybe a .dmg / .msi.

## Non-goals (for now)
- Quantum chemistry calculations (DFT / ab initio). Wrap PySCF as an
  optional plugin if a specific lesson needs it — don't build it into core.
- Full crystallography or protein structure display. PDB ingestion via
  RDKit + 3Dmol.js only as a read-only viewer.
- Authoring chemistry content inside the app. Markdown files edited
  externally are fine; a full WYSIWYG editor is out of scope.

## Decision log
- **2026-04-22** — Scoped **Phase 10 Molecular dynamics** as two
  sub-phases: a lightweight MMFF-based path that reuses the existing
  Phase 2c.2 trajectory player (near-term, no new heavy deps), and an
  optional OpenMM backend for students who want real kinetics (later,
  hidden behind a Preferences switch). Covers the organic-chem
  pedagogical ground (conformational motion, ring flips, dihedral
  rotation) without the fight over force-field parameterisation that
  full MD requires.
- **2026-04-22** — Gallery visual QA pass: confirmed reaction SVGs,
  mechanism SVGs, GUI panels all render legibly. Three fixes landed from
  the pass: (a) default window size 1500×950 → 1280×780 with a 960×640
  minimum so the app fits a 13" MBP; (b) matplotlib 3D framing — switched
  from `tight_layout` to `bbox_inches="tight"` now that atoms are real
  3D spheres (proper bounding box) + `set_position([0,0,1,1])`; (c) SVG
  encoding declaration swapped from `iso-8859-1` to `UTF-8` so arrow
  labels with non-ASCII characters render correctly, plus one stray β
  replaced with ASCII in the seed.
- **2026-04-22** — Planned a 3-level **3D reaction display** roadmap
  (static side-by-side → 3Dmol.js trajectory animation → transition-state
  + 3D curved arrows). Added as new Phase 2c. Prerequisite: atom-mapped
  reaction SMARTS on the seeded reactions.
- **2026-04-22** — Mechanism player ships with **atom-to-atom arrows
  only** for now. Canonical arrow-pushing uses bond-midpoint origins
  (for σ/π breaks) and H-atom targets (for deprotonations); those are
  non-trivial in pure SMILES without explicit Hs. The pedagogical value
  is still clear — arrow direction conveys electron flow. Improvements
  tracked in the cross-cutting backlog.
- **2026-04-22** — Mechanism seed data is versioned (`SEED_VERSION`) so
  data changes roll out on next app launch without a migration step.
- **2026-04-22** — Split `agent/library.py` into
  `library.py` + `actions_reactions.py` when it crossed the 500-line cap.
  Both modules register with the action registry on import of
  `orgchem.agent`.
- **2026-04-22** — Added a **Preferences dialog** (`Tools → Preferences…`)
  as the home for configuration settings that were briefly added inline as
  panel toolbars (e.g. 3D backend). Per-panel dropdowns are kept for
  rendering *styles* (per-molecule choices); backend / theme / log level /
  autogen-3D / online-sources live in Preferences. `bus.config_changed`
  signal re-renders open panels on save.
- **2026-04-22** — Dropped the "Quiz — Phase 2" stub tab rather than leave
  a placeholder; quiz engine now sits in Phase 5 with the rest of the
  classroom tooling.
- **2026-04-22** — Dropped the paper's ratio-normalise formula algorithm
  in favour of a direct molar-mass-based computation; IUPAC 2019 masses are
  now the default. Integer masses remain available as `ATOMIC_MASSES_INTEGER`
  for exact reproduction of Verma et al. Table 1.
- **2026-04-22** — Chose 3Dmol.js over VTK/PyVista for the 3D backend
  (zero-friction styling + native mouse controls); kept `render/draw3d.py`
  minimal so VTK can be swapped in later without touching panels.
- **2026-04-22** — Made the tutor a `QDockWidget` (detachable chat console)
  rather than a separate top-level window, so it integrates with Qt's
  layout / save-state machinery and the user can still tear it off.
- **2026-04-22** — Disabled Chromium GPU compositing in headless mode
  (`--disable-gpu`) to keep QWebEngineView stable across molecule swaps.
  Side-effect: no WebGL → 3Dmol.js blank in headless screenshots. Trade-off
  accepted because (a) 2D + GUI-chrome screenshots cover most use cases and
  (b) real GPU is available in the GUI-launched path. Headless-friendly 3D
  is now a tracked roadmap item.
- **2026-04-22** — Introduced `orgchem/agent/controller.py` so GUI-touching
  actions can find the running `MainWindow` without a circular import with
  `gui/main_window.py`.

## How to use this roadmap
1. Pick the next phase's first un-ticked item.
2. Create a task via `TaskCreate` with that item as the subject.
3. Implement, run `pytest`, tick the item, update `PROJECT_STATUS.md`.
4. If a phase's items are all done, strike through the phase title and
   note the completion date.
