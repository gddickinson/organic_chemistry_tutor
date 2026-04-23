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
    "get_protein_info": "Window → Macromolecules… → Proteins → Summary sub-tab",
    "get_protein_chain_sequence":
        "Window → Macromolecules… → Proteins → Summary sub-tab → Copy sequence",
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

    # ---- Periodic table (Phase 27) ------------------------------
    "list_elements": "Tools → Periodic table… (grid)",
    "get_element":
        "Tools → Periodic table… (click a cell → side-pane)",
    "elements_by_category":
        "Tools → Periodic table… (legend row)",

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
