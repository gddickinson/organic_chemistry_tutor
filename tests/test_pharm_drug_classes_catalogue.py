"""Phase PH-1.0 (round 214) — tests for the Pharmacology
Studio drug-class catalogue + agent actions + multi-hop
cross-studio integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from pharm.core import drug_classes
    assert hasattr(drug_classes, "DrugClass")
    assert hasattr(drug_classes, "list_drug_classes")


def test_catalogue_has_at_least_30_entries():
    from pharm.core.drug_classes import list_drug_classes
    assert len(list_drug_classes()) >= 30


def test_every_drug_class_has_required_fields():
    from pharm.core.drug_classes import (
        TARGET_CLASSES, THERAPEUTIC_AREAS, list_drug_classes,
    )
    for d in list_drug_classes():
        assert d.id and isinstance(d.id, str)
        assert d.name
        assert d.target_class in TARGET_CLASSES, \
            f"{d.id}: invalid target_class {d.target_class!r}"
        assert isinstance(d.therapeutic_areas, tuple)
        assert len(d.therapeutic_areas) >= 1, \
            f"{d.id}: at least one therapeutic area required"
        for ta in d.therapeutic_areas:
            assert ta in THERAPEUTIC_AREAS, \
                f"{d.id}: invalid therapeutic_area {ta!r}"
        assert d.mechanism
        assert d.molecular_target
        assert isinstance(d.typical_agents, tuple)
        assert len(d.typical_agents) >= 1
        assert isinstance(d.clinical_use, tuple)
        assert isinstance(d.side_effects, tuple)
        assert isinstance(d.contraindications, tuple)
        assert isinstance(d.monitoring, tuple)
        assert isinstance(
            d.cross_reference_molecule_names, tuple)
        assert isinstance(d.cross_reference_enzyme_ids, tuple)
        assert isinstance(
            d.cross_reference_signaling_pathway_ids, tuple)


def test_drug_class_ids_are_unique():
    from pharm.core.drug_classes import list_drug_classes
    ids = [d.id for d in list_drug_classes()]
    assert len(ids) == len(set(ids))


def test_target_classes_diverse():
    """Round-214 catalogue should cover at least 6 of the 9
    target classes — proves breadth."""
    from pharm.core.drug_classes import list_drug_classes
    classes = {d.target_class for d in list_drug_classes()}
    assert len(classes) >= 6


def test_therapeutic_areas_diverse():
    """At least 6 of the 11 therapeutic areas should appear."""
    from pharm.core.drug_classes import list_drug_classes
    seen = set()
    for d in list_drug_classes():
        seen.update(d.therapeutic_areas)
    assert len(seen) >= 6


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity (multi-hop)
# ------------------------------------------------------------------

def test_cross_reference_enzyme_ids_resolve_to_biochem():
    """Every `cross_reference_enzyme_ids` entry must resolve to
    a real biochem.core.enzymes id — catches stale references
    when biochem renames an enzyme."""
    from pharm.core.drug_classes import list_drug_classes
    from biochem.core.enzymes import (
        list_enzymes as biochem_list_enzymes,
    )
    valid_ids = {e.id for e in biochem_list_enzymes()}
    for d in list_drug_classes():
        for ref in d.cross_reference_enzyme_ids:
            assert ref in valid_ids, \
                (f"{d.id}: dangling biochem-enzyme xref "
                 f"{ref!r}")


def test_cross_reference_signaling_pathway_ids_resolve_to_cellbio():
    """Multi-hop validation: every
    `cross_reference_signaling_pathway_ids` entry must resolve
    to a real cellbio.core.cell_signaling pathway id."""
    from pharm.core.drug_classes import list_drug_classes
    from cellbio.core.cell_signaling import (
        list_pathways as cellbio_list_pathways,
    )
    valid_ids = {p.id for p in cellbio_list_pathways()}
    for d in list_drug_classes():
        for ref in d.cross_reference_signaling_pathway_ids:
            assert ref in valid_ids, \
                (f"{d.id}: dangling cellbio-signaling xref "
                 f"{ref!r}")


def test_at_least_some_pharm_classes_have_cross_references():
    """Sanity check: not every drug class can have empty
    cross-references — that would mean the catalogue is
    isolated from the platform."""
    from pharm.core.drug_classes import list_drug_classes
    has_refs = 0
    for d in list_drug_classes():
        if (d.cross_reference_molecule_names
                or d.cross_reference_enzyme_ids
                or d.cross_reference_signaling_pathway_ids):
            has_refs += 1
    # At least half the catalogue should connect to the platform.
    assert has_refs >= 15


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_drug_class():
    from pharm.core.drug_classes import get_drug_class
    d = get_drug_class("ace-inhibitors")
    assert d is not None
    assert d.target_class == "enzyme"
    assert "ace" in d.cross_reference_enzyme_ids


def test_get_drug_class_unknown_returns_none():
    from pharm.core.drug_classes import get_drug_class
    assert get_drug_class("not-a-real-id") is None


def test_filter_by_target_class():
    from pharm.core.drug_classes import (
        list_drug_classes, drug_classes_for_target,
    )
    gpcrs = drug_classes_for_target("GPCR")
    assert all(d.target_class == "GPCR" for d in gpcrs)
    assert "beta-blockers" in {d.id for d in gpcrs}
    assert {d.id for d in list_drug_classes(
        target_class="GPCR")} == {d.id for d in gpcrs}


def test_filter_by_therapeutic_area():
    from pharm.core.drug_classes import list_drug_classes
    onco = list_drug_classes(therapeutic_area="oncology")
    ids = {d.id for d in onco}
    assert "platinum-chemotherapy" in ids
    assert "kinase-inhibitors" in ids
    assert "beta-blockers" not in ids


def test_find_drug_classes_by_agent():
    from pharm.core.drug_classes import find_drug_classes
    hits = find_drug_classes("propranolol")
    ids = {d.id for d in hits}
    assert "beta-blockers" in ids


def test_find_drug_classes_by_disease():
    from pharm.core.drug_classes import find_drug_classes
    hits = find_drug_classes("hypertension")
    ids = {d.id for d in hits}
    assert "ace-inhibitors" in ids


def test_drug_class_to_dict_is_serialisable():
    import json
    from pharm.core.drug_classes import (
        get_drug_class, drug_class_to_dict,
    )
    d = get_drug_class("statins")
    assert d is not None
    out = drug_class_to_dict(d)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration
# ------------------------------------------------------------------

def test_agent_actions_register_on_pharm_import():
    import pharm  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_drug_classes",
        "get_drug_class",
        "find_drug_classes",
        "drug_classes_for_target",
        "open_pharm_studio",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_pharm_category():
    import pharm  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_drug_classes",
        "get_drug_class",
        "find_drug_classes",
        "drug_classes_for_target",
        "open_pharm_studio",
    ):
        assert reg[name].category == "pharm-drugs"


def test_list_action_returns_dicts():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_drug_classes")
    assert isinstance(out, list)
    assert len(out) >= 30


def test_get_action_returns_full_record():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_drug_class", class_id="glp1-agonists")
    assert isinstance(out, dict)
    assert out["id"] == "glp1-agonists"
    assert "endocrinology" in out["therapeutic_areas"]


def test_get_action_unknown_id_returns_clean_error():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_drug_class", class_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_target_returns_error():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_drug_classes", target_class="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_drug_classes_for_target_action():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("drug_classes_for_target",
                 target_class="enzyme")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "ace-inhibitors" in ids
    assert "statins" in ids


# ------------------------------------------------------------------
# GUI-audit integration
# ------------------------------------------------------------------

def test_gui_audit_includes_pharm_actions():
    import pharm  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_pharm_studio",
        "list_drug_classes",
        "get_drug_class",
        "find_drug_classes",
        "drug_classes_for_target",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_pharm_drugs():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_pharm_studio"]
    assert len(found) >= 1


# ------------------------------------------------------------------
# Tutorial scaffold
# ------------------------------------------------------------------

def test_pharm_curriculum_loads():
    from pharm.tutorial.curriculum import CURRICULUM
    assert "beginner" in CURRICULUM
    assert len(CURRICULUM["beginner"]) >= 1


def test_pharm_welcome_lesson_exists():
    from pharm.tutorial.curriculum import CURRICULUM
    welcome = CURRICULUM["beginner"][0]
    assert welcome["path"].exists()
    body = welcome["path"].read_text()
    assert "Pharmacology Studio" in body
    assert "Biochem" in body
    assert "Cell Bio" in body
