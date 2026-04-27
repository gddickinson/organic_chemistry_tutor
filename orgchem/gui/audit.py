"""GUI wiring audit — Phase 25a (user-flagged).

Every action registered via ``@action`` in
:mod:`orgchem.agent.actions` is an LLM-callable capability. Phase 25
asks that each one is *also* reachable from a menu / panel / dialog
in the GUI, so human users get the same surface. This module stores
the hand-maintained mapping and provides a small walk-the-registry
helper that lists what is and isn't wired up.

The mapping is deliberately string-only (no Qt imports here) so the
audit can run in the headless / tests context without pulling
PySide6 in. Each value describes **how** a user reaches the feature
(menu path, tab name, panel button, etc.). ``""`` means "no GUI
entry yet — add one" and the audit will flag it.

Adding a GUI feature: when you wire a new action into a menu or
panel, update the ``GUI_ENTRY_POINTS`` dict here. ``tests/test_gui_audit.py``
prints the current coverage % on every test run.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


# Hand-maintained mapping. Key = action name as registered via
# @action(category=…) in orgchem/agent/. Value = user-facing path
# for humans, e.g. "Tab → sub-tab" / "Menu → item" / "Panel → button".
#
# An empty string means the action is currently **agent-only** — the
# audit flags it so round-N can wire a GUI entry.
GUI_ENTRY_POINTS: Dict[str, str] = {
    # ---- Molecule -------------------------------------------------
    "list_all_molecules": "Molecule browser dock (left)",
    "list_molecule_categories":
        "Molecule browser dock → filter-bar A / B combos",
    "filter_molecules":
        "Molecule browser dock → filter-bar A / B / free-text row",
    "get_molecule_details": "Molecule browser → Properties dock",
    "show_molecule": "Molecule browser (double-click)",
    "import_smiles": "File → Import SMILES… (Ctrl+I)",
    "compare_molecules": "Compare tab (drop molecules into slots)",

    # ---- Tools ---------------------------------------------------
    "calculate_empirical_formula":
        "Tools → Empirical / Molecular Formula Calculator…",

    # ---- Online --------------------------------------------------
    "search_pubchem": "Search / Download dock (left)",
    "download_from_pubchem": "Search / Download dock → Download",

    # ---- Tutorials ----------------------------------------------
    "list_tutorials": "Tutorials tab (tree view)",
    "open_tutorial": "Tutorials tab (double-click lesson)",

    # ---- Reactions ----------------------------------------------
    "list_reactions": "Reactions tab (filterable list)",
    "show_reaction": "Reactions tab (selection)",
    "export_reaction_by_id": "Reactions tab → Export…",
    "export_reaction_3d": "Reactions tab → 3D…",
    "export_reaction_trajectory_html":
        "Reactions tab → Trajectory HTML",
    "play_reaction_trajectory": "Reactions tab → Play trajectory…",
    "list_energy_profiles": "Reactions tab (has-profile rows marked)",
    "get_energy_profile": "Reactions tab → Energy profile…",
    "export_energy_profile": "Reactions tab → Energy profile… → Save",

    # ---- Mechanism ----------------------------------------------
    "list_mechanisms": "Reactions tab (has-mechanism rows marked)",
    "open_mechanism": "Reactions tab → Open mechanism…",
    "get_mechanism_details":
        "Reactions tab → Open mechanism… (same entry; this action "
        "returns the full arrow JSON for script / tutor use, "
        "no separate UI)",
    "export_mechanism_step": "Mechanism player → Save step…",
    "export_mechanism_composite": "Mechanism player → Save composite…",

    # ---- Synthesis pathways -------------------------------------
    "list_pathways": "Synthesis tab (filterable list)",
    "show_pathway": "Synthesis tab (selection)",
    "export_pathway": "Synthesis tab → Export…",
    "pathway_green_metrics":
        "Tools → Green metrics… → Pathway AE tab",
    "reaction_atom_economy":
        "Tools → Green metrics… → Reaction AE tab",
    "compare_pathways_green":
        "Tools → Green metrics… → Compare pathways tab",

    # ---- Dynamics ------------------------------------------------
    "run_dihedral_scan_demo": "Dynamics dialog (Run dynamics… button)",
    "run_molecule_dihedral": "Dynamics dialog → Dihedral scan",
    "run_molecule_conformer_morph": "Dynamics dialog → Conformer morph",

    # ---- Orbitals -----------------------------------------------
    "huckel_mos":
        "Tools → Orbitals (Hückel / W-H)… → Hückel MOs tab",
    "export_mo_diagram":
        "Tools → Orbitals (Hückel / W-H)… → Hückel MOs tab → Save MO diagram…",
    "list_wh_rules":
        "Tools → Orbitals (Hückel / W-H)… → Woodward-Hoffmann tab",
    "get_wh_rule":
        "Tools → Orbitals (Hückel / W-H)… → Woodward-Hoffmann tab (selection)",
    "check_wh_allowed":
        "Tools → Orbitals (Hückel / W-H)… → Is it allowed? tab",
    "show_molecular_orbital":
        "Tools → Orbitals (Hückel / W-H)… → Hückel MOs tab → row selection",
    "explain_wh":
        "Tools → Orbitals (Hückel / W-H)… → Woodward-Hoffmann tab → "
        "'For a reaction:' Explain",

    # ---- Stereo --------------------------------------------------
    "assign_stereodescriptors": "Molecule 2D viewer (show-stereo toggle)",
    "flip_stereocentre":
        "Tools → Stereochemistry… (per-centre Flip button)",
    "enantiomer_of":
        "Tools → Stereochemistry… → Mirror (enantiomer)",
    "export_molecule_2d_stereo": "File → Export current molecule (2D)…",

    # ---- Glossary -----------------------------------------------
    "define": "Glossary tab (selection)",
    "list_glossary": "Glossary tab",
    "search_glossary": "Glossary tab (filter field)",
    "show_term": "Glossary tab (selection)",
    "get_glossary_figure":
        "Glossary tab → View figure button (per term)",

    # ---- Med-chem -----------------------------------------------
    "drug_likeness": "Properties dock (sub-section)",
    "list_sar_series":
        "Tools → Medicinal chemistry… → SAR series tab",
    "get_sar_series":
        "Tools → Medicinal chemistry… → SAR series tab (selection)",
    "export_sar_matrix":
        "Tools → Medicinal chemistry… → SAR series tab → Export SAR matrix…",
    "list_bioisosteres":
        "Tools → Medicinal chemistry… → Bioisosteres tab",
    "suggest_bioisosteres":
        "Tools → Medicinal chemistry… → Bioisosteres tab → Suggest",

    # ---- Lab ----------------------------------------------------
    "export_tlc_plate":
        "Tools → Lab techniques → TLC / Rf tab → Save plate…",
    "predict_tlc":
        "Tools → Lab techniques… → TLC / Rf tab",
    "predict_rf":
        "Tools → Lab techniques… → TLC / Rf tab (single row)",
    "recrystallisation_yield":
        "Tools → Lab techniques… → Recrystallisation tab",
    "distillation_plan":
        "Tools → Lab techniques… → Distillation tab",
    "extraction_plan":
        "Tools → Lab techniques… → Acid-base extraction tab",

    # ---- Naming -------------------------------------------------
    "list_naming_rules":
        "Tools → IUPAC naming rules…",
    "get_naming_rule":
        "Tools → IUPAC naming rules… (rule list selection)",
    "naming_rule_categories":
        "Tools → IUPAC naming rules… (Category combo)",

    # ---- Spectroscopy -------------------------------------------
    "predict_ir_bands":
        "Tools → Spectroscopy… → IR tab",
    "export_ir_spectrum":
        "Tools → Spectroscopy… → IR tab → Save spectrum…",
    "predict_nmr_shifts":
        "Tools → Spectroscopy… → NMR tab",
    "export_nmr_spectrum":
        "Tools → Spectroscopy… → NMR tab → Save spectrum…",
    "predict_ms":
        "Tools → Spectroscopy… → MS tab",
    "export_ms_spectrum":
        "Tools → Spectroscopy… → MS tab → Save spectrum…",
    "guess_formula": "Tools → HRMS formula candidate guesser…",
    "guess_formula_for_smiles":
        "Tools → HRMS formula candidate guesser… (from SMILES)",
    "predict_ms_fragments": "Tools → EI-MS fragmentation sketch…",

    # ---- Retrosynthesis -----------------------------------------
    "find_retrosynthesis":
        "Tools → Retrosynthesis… → Find single-step",
    "list_retro_templates":
        "Tools → Retrosynthesis… (template list)",
    "find_multi_step_retrosynthesis":
        "Tools → Retrosynthesis… → Find multi-step",

    # ---- Protein ------------------------------------------------
    "list_seeded_proteins": "Window → Macromolecules… → Proteins → seeded-target combo",
    "fetch_pdb": "Window → Macromolecules… → Proteins → Fetch PDB",
    "show_ligand_binding":
        "Window → Macromolecules… → Proteins → (tutor workflow — "
        "single-call fetch + contacts + interaction map + show)",
    # ---- Content authoring (round 55) --------------------------
    "add_molecule":
        "Tutor chat console dock — tutor-driven content authoring; "
        "new molecule shows up in the Molecule browser on refresh",
    "add_reaction":
        "Tutor chat console dock — tutor-driven content authoring; "
        "new reaction shows up in the Reactions tab on refresh",
    "add_glossary_term":
        "Tutor chat console dock — tutor-driven content authoring; "
        "new term shows up in the Glossary tab on refresh",
    "add_tutorial_lesson":
        "Tutor chat console dock — tutor-driven content authoring; "
        "writes a new .md file and appends to the Tutorials tree",
    "add_molecule_synonym":
        "Tutor chat console dock — attach a common-name alias to an "
        "existing molecule row so search / show_molecule resolve both",

    # ---- Physical organic (Phase 17e) --------------------------
    "hammett_fit":
        "Tutor chat console dock — physical-organic action (callable "
        "via the tutor panel; no dedicated dialog yet)",
    "predict_kie":
        "Tutor chat console dock — physical-organic action (callable "
        "via the tutor panel; no dedicated dialog yet)",
    "list_hammett_substituents":
        "Tutor chat console dock — physical-organic helper listing "
        "the σ catalogue from the tutor panel",

    "list_capabilities":
        "Tutor chat console dock — self-introspection action "
        "callable from the tutor panel when asked 'what can you do?'",
    "get_protein_info": "Window → Macromolecules… → Proteins → Summary sub-tab",
    "get_protein_chain_sequence":
        "Window → Macromolecules… → Proteins → Summary sub-tab → Copy sequence",
    "get_sequence_view":
        "Window → Macromolecules… → Proteins → Summary sub-tab "
        "(Phase 34a — headless SequenceView core; the Phase 34b "
        "SequenceBar widget will surface this data in the 3D "
        "sub-tab once shipped)",
    "select_residues":
        "Window → Macromolecules… → Proteins → 3D structure sub-tab "
        "→ sequence-bar click/drag (Phase 34f — programmatic "
        "counterpart that pushes selection from tutor / scripts)",
    "get_selection":
        "Window → Macromolecules… → Proteins → 3D structure sub-tab "
        "→ sequence-bar selection state (Phase 34f introspection)",
    "clear_selection":
        "Window → Macromolecules… → Proteins → 3D structure sub-tab "
        "→ sequence-bar Clear button (Phase 34f programmatic "
        "counterpart)",
    "fetch_alphafold": "Window → Macromolecules… → Proteins → Fetch AlphaFold",
    "get_alphafold_info": "Window → Macromolecules… → Proteins → Summary sub-tab",
    "find_binding_sites": "Window → Macromolecules… → Proteins → Pockets sub-tab",
    "analyse_binding": "Window → Macromolecules… → Proteins → Contacts sub-tab → Analyse binding",
    "export_interaction_map":
        "Window → Macromolecules… → Proteins → Contacts sub-tab → Export interaction map…",
    "analyse_ppi": "Window → Macromolecules… → Proteins → PPI sub-tab → Analyse all chain pairs",
    "analyse_ppi_pair":
        "Window → Macromolecules… → Proteins → PPI sub-tab → per-pair combo + Analyse pair",
    "plip_capabilities": "Window → Macromolecules… → Proteins → PLIP badge",
    "analyse_binding_plip":
        "Window → Macromolecules… → Proteins → Contacts sub-tab → Analyse (PLIP if available)",
    "analyse_na_binding": "Window → Macromolecules… → Proteins → NA-ligand sub-tab",
    "export_protein_3d_html":
        "Window → Macromolecules… → Proteins → 3D structure sub-tab → Save HTML…",

    # ---- Carbohydrates (Phase 29b) ------------------------------
    "list_carbohydrates":
        "Window → Macromolecules… → Carbohydrates → entry list",
    "get_carbohydrate":
        "Window → Macromolecules… → Carbohydrates → entry-list selection → details pane",
    "carbohydrate_families":
        "Window → Macromolecules… → Carbohydrates → Family combo (top filter row)",

    # ---- Lipids (Phase 29b) -------------------------------------
    "list_lipids":
        "Window → Macromolecules… → Lipids → entry list",
    "get_lipid":
        "Window → Macromolecules… → Lipids → entry-list selection → details pane",
    "lipid_families":
        "Window → Macromolecules… → Lipids → Family combo (top filter row)",

    # ---- Nucleic acids (Phase 29c) ------------------------------
    "list_nucleic_acids":
        "Window → Macromolecules… → Nucleic acids → entry list",
    "get_nucleic_acid":
        "Window → Macromolecules… → Nucleic acids → entry-list selection → details pane",
    "nucleic_acid_families":
        "Window → Macromolecules… → Nucleic acids → Family combo (top filter row)",

    # ---- Windows (Phase 30) -------------------------------------
    "open_macromolecules_window":
        "Window → Macromolecules… (Ctrl+Shift+M)",

    # ---- Scripting (Phase 32a / 32b) ----------------------------
    "open_script_editor":
        "Tools → Script editor (Python)… (Ctrl+Shift+E)",
    "open_workbench":
        "Main tabbar → Workbench (or Window → Workbench… / "
        "Ctrl+Shift+B when detached)",

    # ---- Full-text search (Phase 33a) ---------------------------
    "fulltext_search":
        "View → Find… (Ctrl+F) — Phase 33b dialog surfaces this "
        "action as a live search box (round 89).",

    # ---- Drawing tool (Phase 36) --------------------------------
    "open_drawing_tool":
        "Tools → Drawing tool… (Ctrl+Shift+D) — Phase 36g dialog "
        "wraps the Phase-36b drawing canvas.",
    "drawing_to_smiles":
        "Tools → Drawing tool… → SMILES ribbon below the canvas.",
    "drawing_export":
        "Tools → Drawing tool… → Export drawing… footer button.",
    "drawing_clear":
        "Tools → Drawing tool… → Clear canvas toolbar button.",
    "make_reaction_scheme":
        "Tools → Drawing tool… — Phase 36f.1 headless helper, "
        "exposed to the tutor / scripts via the agent registry "
        "(canvas-side reaction-arrow tool ships in 36f.2).",

    # ---- Qualitative inorganic tests (Phase 37a) ----------------
    "list_inorganic_tests":
        "Tools → Qualitative inorganic tests… (Ctrl+Shift+Q) — "
        "category combo + filter + list rows.",
    "get_inorganic_test":
        "Tools → Qualitative inorganic tests… → click a list "
        "row → detail pane.",
    "find_inorganic_tests_for":
        "Tools → Qualitative inorganic tests… → free-text "
        "filter (target ion).",
    "open_qualitative_tests":
        "Tools → Qualitative inorganic tests… (Ctrl+Shift+Q).",

    # ---- Clinical lab panels (Phase 37b) ------------------------
    "list_lab_panels":
        "Tools → Clinical lab panels… (Ctrl+Shift+L) — "
        "panel-picker combo.",
    "get_lab_panel":
        "Tools → Clinical lab panels… → switch combo + read "
        "the panel meta + analyte table.",
    "list_lab_analytes":
        "Tools → Clinical lab panels… → analyte rows are the "
        "union of every panel.",
    "find_lab_analyte":
        "Tools → Clinical lab panels… (text-lookup is "
        "implicit — pick from the panel's table).",
    "open_clinical_panels":
        "Tools → Clinical lab panels… (Ctrl+Shift+L).",

    # ---- Chromatography (Phase 37c) -----------------------------
    "list_chromatography_methods":
        "Tools → Chromatography techniques… "
        "(Ctrl+Shift+G) — category combo + list rows.",
    "get_chromatography_method":
        "Tools → Chromatography techniques… → click a list "
        "row → detail card.",
    "find_chromatography_methods":
        "Tools → Chromatography techniques… → free-text "
        "filter (name / abbreviation).",
    "open_chromatography_methods":
        "Tools → Chromatography techniques… (Ctrl+Shift+G).",

    # ---- Spectrophotometry (Phase 37d) --------------------------
    "list_spectrophotometry_methods":
        "Tools → Spectrophotometry techniques… "
        "(Ctrl+Shift+W) — category combo + list rows.",
    "get_spectrophotometry_method":
        "Tools → Spectrophotometry techniques… → click a "
        "list row → detail card.",
    "find_spectrophotometry_methods":
        "Tools → Spectrophotometry techniques… → free-text "
        "filter (name / abbreviation).",
    "beer_lambert":
        "Tools → Spectrophotometry techniques… → "
        "Beer-Lambert calculator panel at the bottom of "
        "the right pane.",
    "open_spectrophotometry":
        "Tools → Spectrophotometry techniques… (Ctrl+Shift+W).",

    # ---- Lab equipment (Phase 38a) ------------------------------
    "list_lab_equipment":
        "Tools → Lab equipment… (Ctrl+Shift+I) — category "
        "combo + list rows.",
    "get_lab_equipment":
        "Tools → Lab equipment… → click a list row → "
        "detail card.",
    "find_lab_equipment":
        "Tools → Lab equipment… → free-text filter "
        "(name / category).",
    "open_lab_equipment":
        "Tools → Lab equipment… (Ctrl+Shift+I).",

    # ---- Lab setups (Phase 38b) ---------------------------------
    "list_lab_setups":
        "Tools → Lab setups… (Ctrl+Shift+U) — list rows.",
    "get_lab_setup":
        "Tools → Lab setups… → click a list row → detail card.",
    "find_lab_setups":
        "Tools → Lab setups… → free-text filter.",
    "validate_lab_setup":
        "Tools → Lab setups… → detail card surfaces "
        "validation errors at the bottom; agent action "
        "drives this directly.",
    "open_lab_setups":
        "Tools → Lab setups… (Ctrl+Shift+U).",

    # ---- Lab calculator (Phase 39b) -----------------------------
    "open_lab_calculator":
        "Tools → Lab calculator… (Ctrl+Shift+C) — tabbed "
        "dialog with 7 categories of bench calculators.",

    # ---- Lab calculator per-solver actions (Phase 39c) ----------
    # Every solver from Phase 39a is exposed via the agent
    # registry; the dialog itself is the human-facing path,
    # these actions are the script / tutor entry point.  All
    # 31 wrappers point at the same Tools → Lab calculator…
    # dialog tab where the equivalent UI lives.
    "molarity":
        "Tools → Lab calculator… → Solution tab → Molarity panel.",
    "dilution":
        "Tools → Lab calculator… → Solution tab → Dilution panel.",
    "serial_dilution":
        "Tools → Lab calculator… (no UI panel; agent-only "
        "convenience for a step-by-step dilution table).",
    "molarity_from_mass_percent":
        "Tools → Lab calculator… → Solution tab → "
        "Molarity from %w/w panel.",
    "ppm_to_molarity":
        "Tools → Lab calculator… (agent-only convenience; "
        "Solution tab covers M ↔ %w/w but not the dedicated "
        "ppm helper).",
    "molarity_to_ppm":
        "Tools → Lab calculator… (agent-only — same).",
    "limiting_reagent":
        "Tools → Lab calculator… (agent-only; the list-shaped "
        "input doesn't fit the spin-box dialog pattern).",
    "theoretical_yield":
        "Tools → Lab calculator… → Stoichiometry tab → "
        "Theoretical-yield panel.",
    "percent_yield":
        "Tools → Lab calculator… → Stoichiometry tab → "
        "Percent-yield panel.",
    "percent_purity":
        "Tools → Lab calculator… → Stoichiometry tab → "
        "Percent-purity panel.",
    "ph_from_h":
        "Tools → Lab calculator… → Acid-base tab → "
        "[H⁺] → pH button.",
    "h_from_ph":
        "Tools → Lab calculator… → Acid-base tab → "
        "pH → [H⁺] button.",
    "pka_to_ka":
        "Tools → Lab calculator… → Acid-base tab → "
        "pKa → Ka button.",
    "ka_to_pka":
        "Tools → Lab calculator… → Acid-base tab → "
        "Ka → pKa button.",
    "henderson_hasselbalch":
        "Tools → Lab calculator… → Acid-base tab → "
        "Henderson-Hasselbalch panel.",
    "ideal_gas":
        "Tools → Lab calculator… → Gas-law tab → "
        "Ideal-gas panel.",
    "combined_gas_law":
        "Tools → Lab calculator… → Gas-law tab → "
        "Combined-gas-law panel.",
    "gas_density":
        "Tools → Lab calculator… → Gas-law tab → "
        "Gas-density panel.",
    "boiling_point_elevation":
        "Tools → Lab calculator… → Colligative tab → "
        "BP-elevation panel.",
    "freezing_point_depression":
        "Tools → Lab calculator… → Colligative tab → "
        "FP-depression panel.",
    "osmotic_pressure":
        "Tools → Lab calculator… → Colligative tab → "
        "Osmotic-pressure panel.",
    "heat_capacity":
        "Tools → Lab calculator… → Thermo + kinetics tab → "
        "Heat-capacity panel.",
    "hess_law_sum":
        "Tools → Lab calculator… (agent-only convenience; "
        "list-shaped input).",
    "first_order_half_life":
        "Tools → Lab calculator… → Thermo + kinetics tab → "
        "Half-life panel.",
    "first_order_integrated":
        "Tools → Lab calculator… (agent-only — extends the "
        "half-life panel for full [A]_t solves).",
    "arrhenius":
        "Tools → Lab calculator… → Thermo + kinetics tab → "
        "Arrhenius panel.",
    "eyring_rate_constant":
        "Tools → Lab calculator… (agent-only; closed-form "
        "Eyring solve, no widget panel).",
    "equilibrium_constant":
        "Tools → Lab calculator… (agent-only; species-list "
        "shape doesn't fit the spin-box panel).",
    "ksp_from_solubility":
        "Tools → Lab calculator… → Equilibrium tab → "
        "K_sp ↔ s direction button.",
    "solubility_from_ksp":
        "Tools → Lab calculator… → Equilibrium tab → "
        "K_sp ↔ s direction button.",
    "ice_solve_a_plus_b":
        "Tools → Lab calculator… → Equilibrium tab → "
        "ICE-solver panel.",

    # ---- Centrifugation (Phase 41) ------------------------------
    "list_centrifuges_action":
        "Tools → Centrifugation… (Ctrl+Shift+F) → "
        "Centrifuges tab → category combo + list rows.",
    "get_centrifuge_action":
        "Tools → Centrifugation… → Centrifuges tab → click "
        "a list row → detail card.",
    "list_rotors_action":
        "Tools → Centrifugation… → Rotors tab → category "
        "combo + list rows.",
    "get_rotor_action":
        "Tools → Centrifugation… → Rotors tab → click row.",
    "list_centrifugation_applications":
        "Tools → Centrifugation… → Applications tab.",
    "rpm_to_g_action":
        "Tools → Centrifugation… → g↔RPM calculator tab → "
        "RPM → ×g button.",
    "g_to_rpm_action":
        "Tools → Centrifugation… → g↔RPM calculator tab → "
        "×g → RPM button.",
    "open_centrifugation":
        "Tools → Centrifugation… (Ctrl+Shift+F).",

    # ---- Lab analysers (Phase 40a) ------------------------------
    "list_lab_analysers":
        "Tools → Lab analysers… (Ctrl+Shift+A) — category "
        "combo + list rows.",
    "get_lab_analyser":
        "Tools → Lab analysers… → click a list row → "
        "detail card.",
    "find_lab_analysers":
        "Tools → Lab analysers… → free-text filter.",
    "open_lab_analysers":
        "Tools → Lab analysers… (Ctrl+Shift+A).",

    # ---- Metabolic pathways (Phase 42a) ------------------------
    "list_metabolic_pathways":
        "Tools → Metabolic pathways… (Ctrl+Alt+P) → "
        "category combo + pathway list.",
    "get_metabolic_pathway":
        "Tools → Metabolic pathways… → click a pathway "
        "→ meta block + step table.",
    "find_metabolic_pathways":
        "Tools → Metabolic pathways… → free-text "
        "filter (name / overview).",
    "list_pathway_steps":
        "Tools → Metabolic pathways… → pathway "
        "selection populates the step table.",
    "open_metabolic_pathways":
        "Tools → Metabolic pathways… (Ctrl+Alt+P).",

    # ---- pH + buffer explorer (Phase 46) ------------------------
    "list_pka_acids":
        "Tools → pH explorer… (Ctrl+Alt+H) → pKa lookup tab.",
    "get_pka_acid":
        "Tools → pH explorer… → pKa lookup tab → click row.",
    "find_pka_acids":
        "Tools → pH explorer… → pKa lookup tab → free-text "
        "filter.",
    "design_buffer":
        "Tools → pH explorer… → Buffer designer tab → "
        "Design buffer button.",
    "buffer_capacity":
        "Tools → pH explorer… → Buffer designer tab → "
        "Compute β at this pH button.",
    "simulate_titration":
        "Tools → pH explorer… → Titration curve tab → "
        "Simulate titration button.",
    "open_ph_explorer":
        "Tools → pH explorer… (Ctrl+Alt+H).",

    # ---- Lab reagents (Phase 45) --------------------------------
    "list_lab_reagents":
        "Tools → Lab reagents… (Ctrl+Shift+R) → category combo.",
    "get_lab_reagent":
        "Tools → Lab reagents… (Ctrl+Shift+R) → click row.",
    "find_lab_reagents":
        "Tools → Lab reagents… (Ctrl+Shift+R) → filter box.",
    "open_lab_reagents":
        "Tools → Lab reagents… (Ctrl+Shift+R).",

    # ---- Microscopy techniques (Phase 44) -----------------------
    "list_microscopy_methods":
        "Tools → Microscopy techniques… (Ctrl+Alt+M) → "
        "resolution-scale combo.",
    "get_microscopy_method":
        "Tools → Microscopy techniques… → click row.",
    "find_microscopy_methods":
        "Tools → Microscopy techniques… → filter box.",
    "microscopy_methods_for_sample":
        "Tools → Microscopy techniques… → sample-type combo.",
    "open_microscopy":
        "Tools → Microscopy techniques… (Ctrl+Alt+M).",

    # ---- Cell components (Phase 43) -----------------------------
    "list_cell_components":
        "Tools → Cell components… (Ctrl+Shift+J) → "
        "domain + sub-domain combos.",
    "get_cell_component":
        "Tools → Cell components… → click row.",
    "find_cell_components":
        "Tools → Cell components… → filter box.",
    "cell_components_for_category":
        "Tools → Cell components… → category combo.",
    "open_cell_components":
        "Tools → Cell components… (Ctrl+Shift+J).",

    # ---- Biochemistry by Kingdom (Phase 47) ---------------------
    "list_kingdom_topics":
        "Window → Biochemistry by Kingdom… (Ctrl+Shift+K) → "
        "kingdom outer tabs + subtab inner tabs.",
    "get_kingdom_topic":
        "Window → Biochemistry by Kingdom… → click a topic row.",
    "find_kingdom_topics":
        "Window → Biochemistry by Kingdom… → per-pane filter "
        "box.",
    "open_biochemistry_by_kingdom":
        "Window → Biochemistry by Kingdom… (Ctrl+Shift+K).",

    # ---- Isomers (Phase 48) -------------------------------------
    "find_stereoisomers":
        "Tools → Isomer relationships… (Ctrl+Shift+B) → "
        "Stereoisomers tab.",
    "find_tautomers":
        "Tools → Isomer relationships… (Ctrl+Shift+B) → "
        "Tautomers tab.",
    "classify_isomer_pair":
        "Tools → Isomer relationships… (Ctrl+Shift+B) → "
        "Classify pair tab.",
    "open_isomer_explorer":
        "Tools → Isomer relationships… (Ctrl+Shift+B).",

    # ---- Periodic table (Phase 27) ------------------------------
    "list_elements": "Tools → Periodic table… (grid)",
    "get_element":
        "Tools → Periodic table… (click a cell → side-pane)",
    "elements_by_category":
        "Tools → Periodic table… (legend row)",
    "open_periodic_table":
        "Tools → Periodic table… (Ctrl+Shift+T)",
    "open_naming_rules":
        "Tools → IUPAC naming rules…",

    # ---- Phase 38c.5 (round 190) — Lab setup canvas ------------
    "open_lab_setup_canvas":
        "Tools → Lab setup canvas… "
        "(also reachable via Lab setups → Build on canvas)",
    "place_equipment_on_canvas":
        "Lab setup canvas → drag equipment from palette / "
        "agent-driven placement",
    "connect_canvas_equipment":
        "Lab setup canvas → click two glyphs + their ports / "
        "agent-driven connection",
    "clear_lab_setup_canvas":
        "Lab setup canvas → Clear canvas button",
    "lab_setup_canvas_state":
        "Lab setup canvas → introspection (no GUI control)",

    # ---- Phase 38d.4 (round 194) — Process simulator -----------
    "start_process_simulation":
        "Lab setup canvas → Run simulation toolbar button "
        "(also reachable as an agent action)",
    "simulator_state":
        "Lab setup canvas → simulation dock introspection",
    "simulator_step":
        "Lab setup canvas → simulation dock → ⏭ Step button",
    "simulator_reset":
        "Lab setup canvas → simulation dock → ⟲ Reset button",
    "simulator_play":
        "Lab setup canvas → simulation dock → ▶ Play button",
    "simulator_pause":
        "Lab setup canvas → simulation dock → ⏸ Pause button",
    "set_simulator_speed":
        "Lab setup canvas → simulation dock → speed slider",

    # ---- Session (Phase 20d) ------------------------------------
    "list_sessions": "File → Recent sessions ▸",
    "save_session_state": "File → Save session… (Ctrl+S)",
    "load_session_state": "File → Load session… (Ctrl+Shift+O)",

    # ---- Export / screenshots -----------------------------------
    "export_molecule_2d_by_id":
        "File → Export current molecule (2D)… (Ctrl+E)",
    "export_current_molecule_2d":
        "File → Export current molecule (2D)… (Ctrl+E)",
    "export_molecule_3d": "3D viewer → Save PNG…",
    "screenshot_window": "File → Screenshot window… (Ctrl+Shift+P)",
    "screenshot_panel": "File → Screenshot window… (per-panel menu)",

    # ====================================================================
    # === Cell Biology Studio (Phase CB-1.0, round 212) ==================
    # ====================================================================
    # Sibling life-sciences studio.  Opens via Window menu; the
    # signalling catalogue is reachable through the Cell Bio main
    # window's *Signalling* tab.
    "open_cellbio_studio":
        "Window → Cell Biology Studio… (Ctrl+Shift+B)",
    "list_signaling_pathways":
        "Cell Biology Studio → Signalling tab",
    "get_signaling_pathway":
        "Cell Biology Studio → Signalling tab (selection)",
    "find_signaling_pathways":
        "Cell Biology Studio → Signalling tab → filter box",

    # ----- Phase CB-2.0 (round 218) — Cell-cycle catalogue.
    "open_cellbio_cell_cycle_tab":
        "Window → Cell Biology Studio → Cell cycle tab",
    "list_cell_cycle_entries":
        "Cell Biology Studio → Cell cycle tab",
    "get_cell_cycle_entry":
        "Cell Biology Studio → Cell cycle tab (selection)",
    "find_cell_cycle_entries":
        "Cell Biology Studio → Cell cycle tab → filter box",
    "cell_cycle_entries_for_category":
        "Cell Biology Studio → Cell cycle tab → category combo",

    # ====================================================================
    # === Biochemistry Studio (Phase BC-1.0, round 213) ==================
    # ====================================================================
    # Second sibling life-sciences studio.  Opens via Window menu;
    # the enzyme catalogue lives on the Biochem main window's
    # *Enzymes* tab.  *Metabolic pathways* tab bridges to
    # orgchem.core.metabolic_pathways read-only.
    "open_biochem_studio":
        "Window → Biochem Studio… (Ctrl+Shift+Y)",
    "list_enzymes":
        "Biochem Studio → Enzymes tab",
    "get_enzyme":
        "Biochem Studio → Enzymes tab (selection)",
    "find_enzymes":
        "Biochem Studio → Enzymes tab → filter box",
    "enzymes_for_ec_class":
        "Biochem Studio → Enzymes tab → EC-class combo",

    # ----- Phase BC-2.0 (round 219) — Cofactors catalogue.
    "open_biochem_cofactors_tab":
        "Window → Biochem Studio → Cofactors tab",
    "list_cofactors":
        "Biochem Studio → Cofactors tab",
    "get_cofactor":
        "Biochem Studio → Cofactors tab (selection)",
    "find_cofactors":
        "Biochem Studio → Cofactors tab → filter box",
    "cofactors_for_class":
        "Biochem Studio → Cofactors tab → class combo",

    # ====================================================================
    # === Pharmacology Studio (Phase PH-1.0, round 214) ==================
    # ====================================================================
    # Third sibling life-sciences studio.  Opens via Window menu;
    # the drug-class catalogue lives on the Pharm main window's
    # *Drug classes* tab.  *Bridges* tab contains read-only views
    # of biochem.core.enzymes + cellbio.core.cell_signaling.
    "open_pharm_studio":
        "Window → Pharmacology Studio… (Ctrl+Shift+H)",
    "list_drug_classes":
        "Pharmacology Studio → Drug classes tab",
    "get_drug_class":
        "Pharmacology Studio → Drug classes tab (selection)",
    "find_drug_classes":
        "Pharmacology Studio → Drug classes tab → filter box",
    "drug_classes_for_target":
        "Pharmacology Studio → Drug classes tab → target combo",

    # ----- Phase PH-2.0 (round 220) — Receptor catalogue.
    "open_pharm_receptors_tab":
        "Window → Pharmacology Studio → Receptors tab",
    "list_receptors":
        "Pharmacology Studio → Receptors tab",
    "get_receptor":
        "Pharmacology Studio → Receptors tab (selection)",
    "find_receptors":
        "Pharmacology Studio → Receptors tab → filter box",
    "receptors_for_family":
        "Pharmacology Studio → Receptors tab → family combo",

    # ====================================================================
    # === Microbiology Studio (Phase MB-1.0, round 215) ==================
    # ====================================================================
    # Fourth sibling life-sciences studio.  Opens via Window menu;
    # the microbe catalogue lives on the Microbio main window's
    # *Microbes* tab.  *Antibiotic spectrum* tab bridges to
    # pharm.core.drug_classes filtered to the 6 antimicrobial
    # classes.  Microbe entries carry typed cross-references into
    # orgchem cell components + biochem enzymes.
    "open_microbio_studio":
        "Window → Microbiology Studio… (Ctrl+Shift+N)",
    "list_microbes":
        "Microbiology Studio → Microbes tab",
    "get_microbe":
        "Microbiology Studio → Microbes tab (selection)",
    "find_microbes":
        "Microbiology Studio → Microbes tab → filter box",
    "microbes_for_kingdom":
        "Microbiology Studio → Microbes tab → kingdom combo",

    # ----- Phase MB-2.0 (round 221) — Virulence-factor catalogue.
    "open_microbio_virulence_tab":
        "Window → Microbiology Studio → Virulence factors tab",
    "list_virulence_factors":
        "Microbiology Studio → Virulence factors tab",
    "get_virulence_factor":
        "Microbiology Studio → Virulence factors tab (selection)",
    "find_virulence_factors":
        "Microbiology Studio → Virulence factors tab → filter box",
    "virulence_factors_for_class":
        "Microbiology Studio → Virulence factors tab → class combo",

    # ====================================================================
    # === Botany Studio (Phase BT-1.0, round 216) ========================
    # ====================================================================
    # Fifth sibling life-sciences studio.  Opens via Window menu;
    # the plant-taxa catalogue lives on the Botany main window's
    # *Plant taxa* tab.  *Plant secondary metabolites* tab is a
    # live DB-read bridge into orgchem.db.Molecule filtered by
    # source_tags_json to plant-derived natural products
    # (natural-product / terpene / alkaloid / steroid).  Each
    # plant entry carries typed cross-references into orgchem
    # molecules + metabolic pathways + pharm drug classes.
    "open_botany_studio":
        "Window → Botany Studio… (Ctrl+Shift+V)",
    "list_plant_taxa":
        "Botany Studio → Plant taxa tab",
    "get_plant_taxon":
        "Botany Studio → Plant taxa tab (selection)",
    "find_plant_taxa":
        "Botany Studio → Plant taxa tab → filter box",
    "plant_taxa_for_division":
        "Botany Studio → Plant taxa tab → division combo",

    # ----- Phase BT-2.0 (round 222) — Plant-hormones catalogue.
    "open_botany_plant_hormones_tab":
        "Window → Botany Studio → Plant hormones tab",
    "list_plant_hormones":
        "Botany Studio → Plant hormones tab",
    "get_plant_hormone":
        "Botany Studio → Plant hormones tab (selection)",
    "find_plant_hormones":
        "Botany Studio → Plant hormones tab → filter box",
    "plant_hormones_for_class":
        "Botany Studio → Plant hormones tab → class combo",

    # ====================================================================
    # === Animal Biology Studio (Phase AB-1.0, round 217) ================
    # ====================================================================
    # Sixth + FINAL sibling life-sciences studio — completes
    # the 6-studio platform.  Opens via Window menu; the
    # animal-taxa catalogue lives on the Animal main window's
    # *Animal taxa* tab.  *Cell signalling bridge* is the
    # second sibling-side bridge into cellbio.core.cell_signaling
    # (first was Pharm) — filtered to animal-developmental +
    # apoptosis + immune pathways.  Each animal entry carries
    # typed cross-references into orgchem molecules + cellbio
    # signalling pathways + biochem enzymes.
    "open_animal_studio":
        "Window → Animal Biology Studio… (Ctrl+Shift+X)",
    "list_animal_taxa":
        "Animal Biology Studio → Animal taxa tab",
    "get_animal_taxon":
        "Animal Biology Studio → Animal taxa tab (selection)",
    "find_animal_taxa":
        "Animal Biology Studio → Animal taxa tab → filter box",
    "animal_taxa_for_phylum":
        "Animal Biology Studio → Animal taxa tab → phylum combo",

    # ----- Phase AB-2.0 (round 223) — Organ-systems catalogue
    # — FINAL deep-phase round, closes the -2 chain.
    "open_animal_organ_systems_tab":
        "Window → Animal Biology Studio → Organ systems tab",
    "list_organ_systems":
        "Animal Biology Studio → Organ systems tab",
    "get_organ_system":
        "Animal Biology Studio → Organ systems tab (selection)",
    "find_organ_systems":
        "Animal Biology Studio → Organ systems tab → filter box",
    "organ_systems_for_category":
        "Animal Biology Studio → Organ systems tab → category combo",

    # ----- Phase GM-1.0 (round 230) — Genetics + Molecular
    # Biology Studio.  Seventh sibling, post -3 chain.  40-
    # entry molecular-biology-techniques catalogue across 14
    # categories (PCR / sequencing / cloning / CRISPR / blots
    # / in-situ / chromatin / transcriptomics / spatial /
    # proteomics / interactions / structural / epigenetics /
    # delivery) with 5-way typed cross-references into biochem
    # enzymes + cellbio cell-cycle + signalling + animal taxa
    # + orgchem molecules.
    "open_genetics_studio":
        "Window → Genetics + Molecular Biology Studio… "
        "(Ctrl+Alt+G)",
    "list_genetics_techniques":
        "Genetics + Molecular Biology Studio → Techniques tab",
    "get_genetics_technique":
        "Genetics + Molecular Biology Studio → Techniques "
        "tab (selection)",
    "find_genetics_techniques":
        "Genetics + Molecular Biology Studio → Techniques "
        "tab → filter box",
    "genetics_techniques_for_application":
        "Genetics + Molecular Biology Studio → Techniques "
        "tab → category combo",
}


@dataclass
class AuditRow:
    name: str
    category: str
    gui_entry: str            # "" when missing

    @property
    def is_wired(self) -> bool:
        return bool(self.gui_entry.strip())


def audit() -> List[AuditRow]:
    """Return an :class:`AuditRow` per registered agent action."""
    from orgchem.agent.actions import registry
    rows: List[AuditRow] = []
    for name, spec in registry().items():
        rows.append(AuditRow(
            name=name,
            category=spec.category,
            gui_entry=GUI_ENTRY_POINTS.get(name, ""),
        ))
    rows.sort(key=lambda r: (r.category, r.name))
    return rows


def audit_summary() -> Dict[str, object]:
    """Agent-friendly summary: total / wired / missing counts + rows."""
    rows = audit()
    wired = [r for r in rows if r.is_wired]
    missing = [r for r in rows if not r.is_wired]
    return {
        "total_actions": len(rows),
        "wired": len(wired),
        "missing": len(missing),
        "coverage_pct": round(
            100.0 * len(wired) / len(rows) if rows else 0.0, 1),
        "missing_actions": [
            {"name": r.name, "category": r.category} for r in missing
        ],
    }
