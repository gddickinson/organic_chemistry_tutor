"""Phase CB-1.0 (round 212) — tests for the cell-signalling
pathway catalogue + agent actions + main-window opener.

Pure-headless: no Qt; just verifies the catalogue contents +
that agent actions register + that lookups behave.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from cellbio.core import cell_signaling
    assert hasattr(cell_signaling, "SignalingPathway")
    assert hasattr(cell_signaling, "list_pathways")


def test_catalogue_has_at_least_25_entries():
    """Phase CB-1.0 baseline: ~25 canonical pathways.  Floor only
    so the test doesn't break when we add a pathway."""
    from cellbio.core.cell_signaling import list_pathways
    assert len(list_pathways()) >= 25


def test_every_pathway_has_required_fields():
    from cellbio.core.cell_signaling import list_pathways
    for p in list_pathways():
        assert p.id and isinstance(p.id, str)
        assert p.name
        assert p.category
        assert p.receptor_class
        assert isinstance(p.key_components, tuple)
        assert len(p.key_components) >= 2, \
            f"{p.id}: at least 2 components expected"
        assert p.canonical_function
        assert isinstance(p.disease_associations, tuple)
        assert isinstance(p.drug_targets, tuple)
        for entry in p.drug_targets:
            assert isinstance(entry, tuple) and len(entry) == 2
        assert isinstance(p.cross_reference_molecule_names, tuple)
        assert isinstance(p.cross_reference_pathway_ids, tuple)


def test_categories_are_valid():
    from cellbio.core.cell_signaling import (
        CATEGORIES, list_pathways,
    )
    for p in list_pathways():
        assert p.category in CATEGORIES, \
            f"{p.id}: unknown category {p.category!r}"


def test_receptor_classes_are_valid():
    from cellbio.core.cell_signaling import (
        RECEPTOR_CLASSES, list_pathways,
    )
    for p in list_pathways():
        assert p.receptor_class in RECEPTOR_CLASSES, \
            f"{p.id}: unknown receptor class {p.receptor_class!r}"


def test_pathway_ids_are_unique():
    from cellbio.core.cell_signaling import list_pathways
    ids = [p.id for p in list_pathways()]
    assert len(ids) == len(set(ids))


def test_cross_reference_pathway_ids_resolve():
    """Internal cross-references must point at real pathways."""
    from cellbio.core.cell_signaling import list_pathways
    all_ids = {p.id for p in list_pathways()}
    for p in list_pathways():
        for ref in p.cross_reference_pathway_ids:
            assert ref in all_ids, \
                f"{p.id}: dangling pathway xref {ref!r}"


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_pathway():
    from cellbio.core.cell_signaling import get_pathway
    mapk = get_pathway("mapk-erk")
    assert mapk is not None
    assert "MAPK" in mapk.name


def test_get_pathway_unknown_returns_none():
    from cellbio.core.cell_signaling import get_pathway
    assert get_pathway("not-a-real-id") is None


def test_filter_by_category():
    from cellbio.core.cell_signaling import list_pathways
    cd = list_pathways(category="cell-death")
    cd_ids = {p.id for p in cd}
    assert "intrinsic-apoptosis" in cd_ids
    assert "necroptosis" in cd_ids
    assert "pyroptosis" in cd_ids
    # MAPK is growth-factor, not cell-death:
    assert "mapk-erk" not in cd_ids


def test_filter_by_receptor_class():
    from cellbio.core.cell_signaling import list_pathways
    gpcrs = list_pathways(receptor_class="GPCR")
    ids = {p.id for p in gpcrs}
    # Three GPCR pathways in the catalogue:
    assert "gpcr-camp-pka" in ids
    assert "gpcr-ip3-ca" in ids


def test_find_pathways_by_drug_name():
    """*Find* should hit the drug-targets text."""
    from cellbio.core.cell_signaling import find_pathways
    hits = find_pathways("vemurafenib")
    ids = {p.id for p in hits}
    assert "mapk-erk" in ids


def test_find_pathways_by_disease():
    from cellbio.core.cell_signaling import find_pathways
    hits = find_pathways("colorectal")
    ids = {p.id for p in hits}
    assert "wnt-beta-catenin" in ids


def test_pathway_to_dict_is_serialisable():
    """The to_dict serialiser is what agent actions return."""
    import json
    from cellbio.core.cell_signaling import (
        get_pathway, pathway_to_dict,
    )
    p = get_pathway("p53")
    assert p is not None
    d = pathway_to_dict(p)
    # Must round-trip through json (sets / frozen dataclasses
    # would break agent / LLM consumers).
    assert json.dumps(d)


# ------------------------------------------------------------------
# Agent action registration
# ------------------------------------------------------------------

def test_agent_actions_register_on_cellbio_import():
    """Importing ``cellbio`` registers the four signalling
    actions into the shared OrgChem registry."""
    import cellbio  # noqa: F401 — side-effect import
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_signaling_pathways",
        "get_signaling_pathway",
        "find_signaling_pathways",
        "open_cellbio_studio",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_cellbio_category():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_signaling_pathways",
        "get_signaling_pathway",
        "find_signaling_pathways",
        "open_cellbio_studio",
    ):
        assert reg[name].category == "cellbio-signaling"


def test_list_action_returns_dicts():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_signaling_pathways")
    assert isinstance(out, list)
    assert len(out) >= 25
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_signaling_pathway", pathway_id="ampk")
    assert isinstance(out, dict)
    assert out["id"] == "ampk"
    assert "Metformin" in out["cross_reference_molecule_names"]


def test_get_action_unknown_id_returns_clean_error():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_signaling_pathway",
                 pathway_id="not-a-pathway")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_category_returns_error():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_signaling_pathways", category="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_find_action_substring():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_signaling_pathways", needle="metformin")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "ampk" in ids


# ------------------------------------------------------------------
# GUI-audit integration
# ------------------------------------------------------------------

def test_gui_audit_includes_cellbio_actions():
    """Phase CB-1.0 entries must appear in GUI_ENTRY_POINTS."""
    import cellbio  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_cellbio_studio",
        "list_signaling_pathways",
        "get_signaling_pathway",
        "find_signaling_pathways",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_cellbio_signalling():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_cellbio_studio"]
    assert len(found) >= 1


# ------------------------------------------------------------------
# Tutorial scaffold
# ------------------------------------------------------------------

def test_cellbio_curriculum_loads():
    from cellbio.tutorial.curriculum import CURRICULUM
    assert "beginner" in CURRICULUM
    assert len(CURRICULUM["beginner"]) >= 1


def test_cellbio_welcome_lesson_exists():
    from cellbio.tutorial.curriculum import CURRICULUM
    welcome = CURRICULUM["beginner"][0]
    assert welcome["path"].exists()
    body = welcome["path"].read_text()
    assert "Cell Biology Studio" in body
    assert "OrgChem" in body
