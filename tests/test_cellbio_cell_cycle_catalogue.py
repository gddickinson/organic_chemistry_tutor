"""Phase CB-2.0 (round 218) — tests for the Cell Bio Studio
cell-cycle catalogue + agent actions + cross-studio integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from cellbio.core import cell_cycle
    assert hasattr(cell_cycle, "CellCycleEntry")
    assert hasattr(cell_cycle, "list_cell_cycle_entries")


def test_catalogue_has_at_least_25_entries():
    from cellbio.core.cell_cycle import list_cell_cycle_entries
    assert len(list_cell_cycle_entries()) >= 25


def test_every_entry_has_required_fields():
    from cellbio.core.cell_cycle import (
        CATEGORIES, list_cell_cycle_entries,
    )
    for e in list_cell_cycle_entries():
        assert e.id and isinstance(e.id, str)
        assert e.name
        assert e.category in CATEGORIES, \
            f"{e.id}: invalid category {e.category!r}"
        assert e.phase_or_role
        assert e.summary
        assert e.function
        assert isinstance(e.key_components, tuple)
        assert len(e.key_components) >= 1
        assert isinstance(e.activated_by, tuple)
        assert isinstance(e.inhibited_by, tuple)
        assert isinstance(e.disease_associations, tuple)
        assert isinstance(
            e.cross_reference_signaling_pathway_ids, tuple)
        assert isinstance(
            e.cross_reference_pharm_drug_class_ids, tuple)
        assert isinstance(
            e.cross_reference_molecule_names, tuple)


def test_entry_ids_are_unique():
    from cellbio.core.cell_cycle import list_cell_cycle_entries
    ids = [e.id for e in list_cell_cycle_entries()]
    assert len(ids) == len(set(ids))


def test_at_least_5_categories_represented():
    from cellbio.core.cell_cycle import list_cell_cycle_entries
    seen = {e.category for e in list_cell_cycle_entries()}
    assert len(seen) >= 5


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity
# ------------------------------------------------------------------

def test_cross_reference_signaling_pathway_ids_resolve():
    """Every signalling-pathway xref must resolve to a real
    cellbio.core.cell_signaling id."""
    from cellbio.core.cell_cycle import list_cell_cycle_entries
    from cellbio.core.cell_signaling import list_pathways
    valid_ids = {p.id for p in list_pathways()}
    for e in list_cell_cycle_entries():
        for ref in e.cross_reference_signaling_pathway_ids:
            assert ref in valid_ids, \
                (f"{e.id}: dangling cellbio-signaling xref "
                 f"{ref!r}")


def test_cross_reference_pharm_drug_class_ids_resolve():
    """Every pharm-drug-class xref must resolve to a real
    pharm.core.drug_classes id."""
    from cellbio.core.cell_cycle import list_cell_cycle_entries
    from pharm.core.drug_classes import list_drug_classes
    valid_ids = {d.id for d in list_drug_classes()}
    for e in list_cell_cycle_entries():
        for ref in e.cross_reference_pharm_drug_class_ids:
            assert ref in valid_ids, \
                (f"{e.id}: dangling pharm-drug-class xref "
                 f"{ref!r}")


def test_at_least_some_entries_have_cross_references():
    from cellbio.core.cell_cycle import list_cell_cycle_entries
    has_refs = sum(
        1 for e in list_cell_cycle_entries()
        if (e.cross_reference_signaling_pathway_ids
            or e.cross_reference_pharm_drug_class_ids))
    assert has_refs >= 15


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_cell_cycle_entry():
    from cellbio.core.cell_cycle import get_cell_cycle_entry
    e = get_cell_cycle_entry("cyclin-d-cdk4-cdk6")
    assert e is not None
    assert e.category == "cyclin-cdk"


def test_get_cell_cycle_entry_unknown_returns_none():
    from cellbio.core.cell_cycle import get_cell_cycle_entry
    assert get_cell_cycle_entry("not-a-real-id") is None


def test_filter_by_category():
    from cellbio.core.cell_cycle import (
        cell_cycle_entries_for_category,
        list_cell_cycle_entries,
    )
    phases = cell_cycle_entries_for_category("phase")
    assert all(e.category == "phase" for e in phases)
    ids = {e.id for e in phases}
    assert "g1-phase" in ids
    assert "m-phase" in ids
    assert {e.id for e in list_cell_cycle_entries(
        category="phase")} == ids


def test_find_cell_cycle_entries_by_disease():
    from cellbio.core.cell_cycle import find_cell_cycle_entries
    hits = find_cell_cycle_entries("retinoblastoma")
    ids = {e.id for e in hits}
    assert "rb-e2f-axis" in ids


def test_find_cell_cycle_entries_by_drug_keyword():
    from cellbio.core.cell_cycle import find_cell_cycle_entries
    hits = find_cell_cycle_entries("palbociclib")
    ids = {e.id for e in hits}
    assert "cyclin-d-cdk4-cdk6" in ids \
        or "g1-s-restriction-point" in ids


def test_entry_to_dict_is_serialisable():
    import json
    from cellbio.core.cell_cycle import (
        cell_cycle_entry_to_dict, get_cell_cycle_entry,
    )
    e = get_cell_cycle_entry("p53-master-tumour-suppressor")
    assert e is not None
    out = cell_cycle_entry_to_dict(e)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration + behaviour
# ------------------------------------------------------------------

def test_agent_actions_register_on_cellbio_import():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_cell_cycle_entries",
        "get_cell_cycle_entry",
        "find_cell_cycle_entries",
        "cell_cycle_entries_for_category",
        "open_cellbio_cell_cycle_tab",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_cell_cycle_category():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_cell_cycle_entries",
        "get_cell_cycle_entry",
        "find_cell_cycle_entries",
        "cell_cycle_entries_for_category",
        "open_cellbio_cell_cycle_tab",
    ):
        assert reg[name].category == "cellbio-cell-cycle"


def test_list_action_returns_dicts():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_cell_cycle_entries")
    assert isinstance(out, list)
    assert len(out) >= 25
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_cell_cycle_entry",
                 entry_id="cyclin-b-cdk1")
    assert isinstance(out, dict)
    assert out["id"] == "cyclin-b-cdk1"


def test_get_action_unknown_id_returns_clean_error():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_cell_cycle_entry", entry_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_category_returns_error():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_cell_cycle_entries", category="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_cell_cycle_entries_for_category_action():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("cell_cycle_entries_for_category",
                 category="cyclin-cdk")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "cyclin-d-cdk4-cdk6" in ids
    assert "cyclin-b-cdk1" in ids


def test_find_action_substring():
    import cellbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_cell_cycle_entries", needle="aurora")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "aurora-kinases" in ids


# ------------------------------------------------------------------
# GUI-audit + agent-surface-audit integration
# ------------------------------------------------------------------

def test_gui_audit_includes_cell_cycle_actions():
    import cellbio  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_cellbio_cell_cycle_tab",
        "list_cell_cycle_entries",
        "get_cell_cycle_entry",
        "find_cell_cycle_entries",
        "cell_cycle_entries_for_category",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_cell_cycle_surface():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_cellbio_cell_cycle_tab"]
    assert len(found) >= 1


def test_cellbio_cell_cycle_category_summary_present():
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    assert "cellbio-cell-cycle" in _CATEGORY_SUMMARIES
    assert _CATEGORY_SUMMARIES["cellbio-cell-cycle"].strip()
