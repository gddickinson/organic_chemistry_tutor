"""Phase 49d (round 179) — agent-surface symmetry audit.

Test-time helper that walks the agent action registry and verifies
that every catalogue with a Tools-menu dialog also has a
**symmetric agent-action surface**: an opener (``open_<dialog>``)
plus the canonical lookup trio (``list_<X>`` / ``get_<X>`` /
``find_<X>``) that lets the AI tutor do everything a human can do
through the dialog.

Pattern emerged across rounds 136-176:
- Catalogue dialog (`Tools → Foo…`) ↔ `open_foo` action
- Catalogue listing widget ↔ `list_foos` action
- Catalogue lookup-by-id ↔ `get_foo` action
- Catalogue free-text search ↔ `find_foos` action

Round 179 unifies the per-catalogue spec into a single
:data:`EXPECTED_SURFACES` table + a single
:func:`audit_agent_surfaces` walker that reports any missing
actions per catalogue.  :data:`KNOWN_GAPS` allow-lists actions
the GUI ships without (e.g. dialogs that pre-date the agent
layer); a guard test catches stale entries (any action listed in
KNOWN_GAPS that also appears in the registry).

Pure-headless: imports the agent registry only.  No Qt imports.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class SurfaceSpec:
    """One catalogue's expected agent-action surface."""
    catalogue: str          # human label, e.g. "Periodic table"
    opener: str             # required `open_<X>` action name
    list_action: str = ""   # `list_<X>` (empty if N/A)
    get_action: str = ""    # `get_<X>` (empty if N/A)
    find_action: str = ""   # `find_<X>` (empty if N/A)


# ----------------------------------------------------------------
# Expected surfaces — one per catalogue dialog under Tools menu.
# ----------------------------------------------------------------
EXPECTED_SURFACES: Tuple[SurfaceSpec, ...] = (
    SurfaceSpec("Cell components", "open_cell_components",
                list_action="list_cell_components",
                get_action="get_cell_component",
                find_action="find_cell_components"),
    SurfaceSpec("Centrifugation", "open_centrifugation"),
    SurfaceSpec("Chromatography methods",
                "open_chromatography_methods",
                list_action="list_chromatography_methods",
                get_action="get_chromatography_method",
                find_action="find_chromatography_methods"),
    SurfaceSpec("Clinical lab panels", "open_clinical_panels",
                list_action="list_lab_panels",
                get_action="get_lab_panel"),
    SurfaceSpec("Drawing tool", "open_drawing_tool"),
    SurfaceSpec("Isomer explorer", "open_isomer_explorer"),
    SurfaceSpec("Lab analysers", "open_lab_analysers",
                list_action="list_lab_analysers",
                get_action="get_lab_analyser",
                find_action="find_lab_analysers"),
    SurfaceSpec("Lab calculator", "open_lab_calculator"),
    SurfaceSpec("Lab equipment", "open_lab_equipment",
                list_action="list_lab_equipment",
                get_action="get_lab_equipment",
                find_action="find_lab_equipment"),
    SurfaceSpec("Lab reagents", "open_lab_reagents",
                list_action="list_lab_reagents",
                get_action="get_lab_reagent",
                find_action="find_lab_reagents"),
    SurfaceSpec("Lab setups", "open_lab_setups",
                list_action="list_lab_setups",
                get_action="get_lab_setup",
                find_action="find_lab_setups"),
    SurfaceSpec("Macromolecules window",
                "open_macromolecules_window"),
    SurfaceSpec("Mechanism player", "open_mechanism"),
    SurfaceSpec("Metabolic pathways",
                "open_metabolic_pathways",
                list_action="list_metabolic_pathways",
                get_action="get_metabolic_pathway",
                find_action="find_metabolic_pathways"),
    SurfaceSpec("Microscopy methods", "open_microscopy",
                list_action="list_microscopy_methods",
                get_action="get_microscopy_method",
                find_action="find_microscopy_methods"),
    SurfaceSpec("Naming rules", "open_naming_rules",
                list_action="list_naming_rules",
                get_action="get_naming_rule"),
    SurfaceSpec("Periodic table", "open_periodic_table",
                list_action="list_elements",
                get_action="get_element"),
    SurfaceSpec("pH explorer", "open_ph_explorer",
                list_action="list_pka_acids",
                get_action="get_pka_acid",
                find_action="find_pka_acids"),
    SurfaceSpec("Qualitative inorganic tests",
                "open_qualitative_tests",
                list_action="list_inorganic_tests",
                get_action="get_inorganic_test"),
    SurfaceSpec("Script editor", "open_script_editor"),
    SurfaceSpec("Spectrophotometry methods",
                "open_spectrophotometry",
                list_action="list_spectrophotometry_methods",
                get_action="get_spectrophotometry_method",
                find_action="find_spectrophotometry_methods"),
    SurfaceSpec("Tutorial browser", "open_tutorial"),
    SurfaceSpec("Workbench", "open_workbench"),
    SurfaceSpec("Biochemistry by kingdom",
                "open_biochemistry_by_kingdom",
                list_action="list_kingdom_topics",
                get_action="get_kingdom_topic",
                find_action="find_kingdom_topics"),
    # Phase CB-1.0 — Cell Bio Studio sibling.  The opener is the
    # Cell Bio main window itself (no per-catalogue dialog); the
    # signalling catalogue lives on the Signalling tab.
    SurfaceSpec("Cell signalling pathways (Cell Bio Studio)",
                "open_cellbio_studio",
                list_action="list_signaling_pathways",
                get_action="get_signaling_pathway",
                find_action="find_signaling_pathways"),
    # Phase CB-2.0 — Cell-cycle catalogue, dedicated tab opener.
    SurfaceSpec("Cell cycle (Cell Bio Studio)",
                "open_cellbio_cell_cycle_tab",
                list_action="list_cell_cycle_entries",
                get_action="get_cell_cycle_entry",
                find_action="find_cell_cycle_entries"),
    # Phase BC-1.0 — Biochem Studio sibling.  The opener is the
    # Biochem main window itself; the enzyme catalogue lives on
    # the Enzymes tab.
    SurfaceSpec("Enzymes (Biochem Studio)",
                "open_biochem_studio",
                list_action="list_enzymes",
                get_action="get_enzyme",
                find_action="find_enzymes"),
    # Phase BC-2.0 — Cofactors catalogue, dedicated tab opener.
    SurfaceSpec("Cofactors (Biochem Studio)",
                "open_biochem_cofactors_tab",
                list_action="list_cofactors",
                get_action="get_cofactor",
                find_action="find_cofactors"),
    # Phase PH-1.0 — Pharmacology Studio sibling.
    SurfaceSpec("Drug classes (Pharm Studio)",
                "open_pharm_studio",
                list_action="list_drug_classes",
                get_action="get_drug_class",
                find_action="find_drug_classes"),
    # Phase PH-2.0 — Receptor pharmacology catalogue, dedicated
    # tab opener.
    SurfaceSpec("Receptors (Pharm Studio)",
                "open_pharm_receptors_tab",
                list_action="list_receptors",
                get_action="get_receptor",
                find_action="find_receptors"),
    # Phase MB-1.0 — Microbiology Studio sibling.
    SurfaceSpec("Microbes (Microbio Studio)",
                "open_microbio_studio",
                list_action="list_microbes",
                get_action="get_microbe",
                find_action="find_microbes"),
    # Phase MB-2.0 — Virulence-factor catalogue, dedicated tab.
    SurfaceSpec("Virulence factors (Microbio Studio)",
                "open_microbio_virulence_tab",
                list_action="list_virulence_factors",
                get_action="get_virulence_factor",
                find_action="find_virulence_factors"),
    # Phase BT-1.0 — Botany Studio sibling.
    SurfaceSpec("Plant taxa (Botany Studio)",
                "open_botany_studio",
                list_action="list_plant_taxa",
                get_action="get_plant_taxon",
                find_action="find_plant_taxa"),
    # Phase BT-2.0 — Plant-hormones catalogue, dedicated tab.
    SurfaceSpec("Plant hormones (Botany Studio)",
                "open_botany_plant_hormones_tab",
                list_action="list_plant_hormones",
                get_action="get_plant_hormone",
                find_action="find_plant_hormones"),
    # Phase AB-1.0 — Animal Biology Studio sibling (sixth +
    # FINAL — completes the 6-studio platform).
    SurfaceSpec("Animal taxa (Animal Biology Studio)",
                "open_animal_studio",
                list_action="list_animal_taxa",
                get_action="get_animal_taxon",
                find_action="find_animal_taxa"),
    # Phase AB-2.0 — Organ-systems catalogue, dedicated tab.
    # FINAL surface added by the -2 deep-phase chain.
    SurfaceSpec("Organ systems (Animal Biology Studio)",
                "open_animal_organ_systems_tab",
                list_action="list_organ_systems",
                get_action="get_organ_system",
                find_action="find_organ_systems"),
)


# ----------------------------------------------------------------
# KNOWN_GAPS — dialogs that ship without an `open_*` action plus
# the rationale.  A guard test fails if any of these now exist in
# the registry (so the allow-list stays honest).  Round-179
# baseline: 9 Tools-menu dialogs lack agent openers.  Each entry
# is a (action_name, rationale) tuple.
# ----------------------------------------------------------------
KNOWN_GAPS: Tuple[Tuple[str, str], ...] = (
    ("open_spectroscopy",
     "Spectroscopy tools (IR/NMR/MS) are surfaced via individual "
     "predict_/export_ actions; no dialog opener yet."),
    ("open_stereo",
     "Stereo dialog has direct agent actions "
     "(assign_stereodescriptors, flip_stereocentre, "
     "enantiomer_of); no dialog opener yet."),
    ("open_medchem",
     "Medchem dialog content surfaced via list_sar_series / "
     "list_bioisosteres / suggest_bioisosteres."),
    ("open_orbitals",
     "Orbitals dialog content surfaced via huckel_mos / "
     "list_wh_rules / check_wh_allowed."),
    ("open_retrosynthesis",
     "Retrosynthesis dialog content surfaced via "
     "find_retrosynthesis / find_multi_step_retrosynthesis."),
    ("open_lab_techniques",
     "Lab-techniques dialog content surfaced via predict_tlc / "
     "recrystallisation_yield / distillation_plan / "
     "extraction_plan."),
    ("open_green_metrics",
     "Green-metrics dialog content surfaced via "
     "reaction_atom_economy / pathway_green_metrics."),
    ("open_hrms_guesser",
     "HRMS guesser surfaced via guess_formula / "
     "guess_formula_for_smiles."),
    ("open_ms_fragments",
     "MS-fragments dialog surfaced via predict_ms_fragments."),
)


# ----------------------------------------------------------------
# Audit
# ----------------------------------------------------------------
@dataclass
class SurfaceAuditReport:
    """Per-catalogue audit result."""
    spec: SurfaceSpec
    missing_actions: List[str] = field(default_factory=list)

    def is_complete(self) -> bool:
        return not self.missing_actions


def gather_action_names() -> Set[str]:
    """Return the full set of registered agent action names."""
    from orgchem.agent.actions import registry
    return set(registry().keys())


def audit_surface(spec: SurfaceSpec,
                  available: Optional[Set[str]] = None
                  ) -> SurfaceAuditReport:
    """Verify one catalogue's surface against the registry.  Pass
    ``available`` to reuse a single registry snapshot across many
    spec audits."""
    if available is None:
        available = gather_action_names()
    missing = []
    for required in (spec.opener, spec.list_action,
                     spec.get_action, spec.find_action):
        if required and required not in available:
            missing.append(required)
    return SurfaceAuditReport(spec=spec, missing_actions=missing)


def audit_all_surfaces() -> List[SurfaceAuditReport]:
    """Audit every entry in :data:`EXPECTED_SURFACES`."""
    available = gather_action_names()
    return [audit_surface(s, available) for s in EXPECTED_SURFACES]


def gather_known_gaps() -> Set[str]:
    """Just the action-name half of :data:`KNOWN_GAPS`."""
    return {name for name, _rationale in KNOWN_GAPS}


def stale_known_gaps() -> List[str]:
    """Return the action names in KNOWN_GAPS that DO exist in the
    registry — i.e. allow-list entries that should be deleted now
    that the action has shipped.  Empty list = allow-list is
    honest."""
    available = gather_action_names()
    return sorted(name for name, _rationale in KNOWN_GAPS
                  if name in available)


def render_audit_text(reports: Optional[List[SurfaceAuditReport]] = None
                      ) -> str:
    """Render the audit as a human-readable report."""
    if reports is None:
        reports = audit_all_surfaces()
    rows = []
    rows.append("Catalogue                             Status")
    rows.append("-" * 60)
    n_complete = 0
    for r in reports:
        if r.is_complete():
            rows.append(f"{r.spec.catalogue:<37} ok")
            n_complete += 1
        else:
            rows.append(
                f"{r.spec.catalogue:<37} MISSING: "
                f"{', '.join(r.missing_actions)}"
            )
    rows.append("-" * 60)
    rows.append(
        f"{n_complete}/{len(reports)} catalogues have complete "
        f"agent-action surfaces"
    )
    rows.append("")
    rows.append(f"KNOWN_GAPS: {len(KNOWN_GAPS)} dialogs deliberately "
                f"ship without an `open_*` action (see source for "
                f"per-entry rationale)")
    return "\n".join(rows)
