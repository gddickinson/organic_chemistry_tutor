# Roadmap — OrgChem Studio

> Living document. Revise whenever priorities shift. Completed items move
> to `PROJECT_STATUS.md` "What works today" and are struck through here.
> Last updated: **2026-04-22**

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
- [~] **31b. Reactions → 50.** First 5 shipped (Buchwald-Hartwig,
      Sonogashira, Mitsunobu, Swern, HWE). 19 more named reactions
      still to come. Priority
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
- [~] **31k. SAR series → 15.** Shipped across rounds 40-108:
      β-blockers (5), ACE inhibitors (5), SSRIs (round 96),
      β-lactam penicillins (round 100),
      **PDE5 inhibitors (round 108)** — 5 variants: sildenafil /
      vardenafil / tadalafil / avanafil / udenafil with PDE5 IC50
      + half-life + PDE6 selectivity. Three teaching points
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

- [ ] **35c. Bulk backfill for existing DB rows.**
      `orgchem/db/backfill_synonyms.py` + companion
      `scripts/backfill_molecule_synonyms.py` CLI.  Walks every
      `Molecule` row with an empty / short `synonyms_json`,
      queries PubChem by InChIKey (using the existing pubchempy
      adapter), appends returned synonyms.  Rate-limited (1 req
      / 200 ms) to stay under PubChem's 5 req/sec free-tier cap.
      Idempotent — re-running after a few new imports just
      top-ups the unfilled rows.  One-off: also reconcile
      against the ChEMBL / DrugBank names when present in
      `properties`.

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

- [ ] **34f. Selection-aware agent actions.**  Expose the full
      selection round-trip through the `@action` registry so
      tutor / scripts can drive it:
      - `select_residues(pdb_id, chain, start, end)` — updates
        both the 3D overlay and the sequence bar.
      - `get_selection(pdb_id)` — returns the current selection
        as `{chain_id, start, end, resnames}`.
      - `highlight_feature(pdb_id, feature_name)` — selects a
        named span (e.g. *"active site"* or *"signal peptide"*).
      - `clear_selection(pdb_id)`.

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
