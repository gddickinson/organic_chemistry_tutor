"""Phase PH-2.0 (round 220) — tests for the Pharm Studio
receptor pharmacology catalogue + agent actions + cross-studio
integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from pharm.core import receptors
    assert hasattr(receptors, "Receptor")
    assert hasattr(receptors, "list_receptors")


def test_catalogue_has_at_least_25_entries():
    from pharm.core.receptors import list_receptors
    assert len(list_receptors()) >= 25


def test_every_entry_has_required_fields():
    from pharm.core.receptors import (
        RECEPTOR_FAMILIES, list_receptors,
    )
    for r in list_receptors():
        assert r.id and isinstance(r.id, str)
        assert r.name
        assert r.receptor_family in RECEPTOR_FAMILIES, \
            f"{r.id}: invalid family {r.receptor_family!r}"
        assert r.receptor_subtype
        assert r.structural_summary
        assert isinstance(r.endogenous_ligands, tuple)
        assert isinstance(r.signalling_output, tuple)
        assert isinstance(r.tissue_distribution, tuple)
        assert isinstance(r.clinical_relevance, tuple)
        assert isinstance(
            r.cross_reference_drug_class_ids, tuple)
        assert isinstance(
            r.cross_reference_signaling_pathway_ids, tuple)
        assert isinstance(r.cross_reference_enzyme_ids, tuple)
        assert isinstance(
            r.cross_reference_molecule_names, tuple)


def test_post_init_validator_rejects_string_in_tuple_field():
    """The trailing-comma bug class — a single string in place
    of a single-element tuple — must raise TypeError loudly at
    construction time.  Same pattern proved out in BC-2.0."""
    from pharm.core.receptors import Receptor
    with pytest.raises(TypeError):
        Receptor(
            id="bad-receptor", name="Bad",
            receptor_family="rtk",
            receptor_subtype="Bad",
            structural_summary="…",
            endogenous_ligands="not a tuple",  # ← the bug
            signalling_output=(),
            tissue_distribution=(),
            clinical_relevance=(),
            cross_reference_drug_class_ids=(),
            cross_reference_signaling_pathway_ids=(),
            cross_reference_enzyme_ids=(),
            cross_reference_molecule_names=(),
        )


def test_entry_ids_are_unique():
    from pharm.core.receptors import list_receptors
    ids = [r.id for r in list_receptors()]
    assert len(ids) == len(set(ids))


def test_at_least_6_families_represented():
    from pharm.core.receptors import list_receptors
    seen = {r.receptor_family for r in list_receptors()}
    assert len(seen) >= 6


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity (4-hop)
# ------------------------------------------------------------------

def test_cross_reference_drug_class_ids_resolve_to_pharm():
    from pharm.core.receptors import list_receptors
    from pharm.core.drug_classes import list_drug_classes
    valid_ids = {d.id for d in list_drug_classes()}
    for r in list_receptors():
        for ref in r.cross_reference_drug_class_ids:
            assert ref in valid_ids, \
                (f"{r.id}: dangling pharm-drug-class xref "
                 f"{ref!r}")


def test_cross_reference_signaling_pathway_ids_resolve():
    from pharm.core.receptors import list_receptors
    from cellbio.core.cell_signaling import list_pathways
    valid_ids = {p.id for p in list_pathways()}
    for r in list_receptors():
        for ref in r.cross_reference_signaling_pathway_ids:
            assert ref in valid_ids, \
                (f"{r.id}: dangling cellbio-signaling xref "
                 f"{ref!r}")


def test_cross_reference_enzyme_ids_resolve_to_biochem():
    from pharm.core.receptors import list_receptors
    from biochem.core.enzymes import list_enzymes
    valid_ids = {e.id for e in list_enzymes()}
    for r in list_receptors():
        for ref in r.cross_reference_enzyme_ids:
            assert ref in valid_ids, \
                (f"{r.id}: dangling biochem-enzyme xref "
                 f"{ref!r}")


def test_cross_reference_molecule_names_resolve_to_orgchem():
    from pharm.core.receptors import list_receptors
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.models import Molecule
    init_db(AppConfig.load())
    with session_scope() as s:
        valid_names = {m.name for m in s.query(Molecule).all()}
    for r in list_receptors():
        for ref in r.cross_reference_molecule_names:
            assert ref in valid_names, \
                (f"{r.id}: dangling orgchem-molecule xref "
                 f"{ref!r}")


def test_at_least_some_entries_have_cross_references():
    from pharm.core.receptors import list_receptors
    has_refs = sum(
        1 for r in list_receptors()
        if (r.cross_reference_drug_class_ids
            or r.cross_reference_signaling_pathway_ids
            or r.cross_reference_enzyme_ids
            or r.cross_reference_molecule_names))
    assert has_refs >= 15


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_receptor():
    from pharm.core.receptors import get_receptor
    r = get_receptor("adrenergic-beta1")
    assert r is not None
    assert r.receptor_family == "gpcr-aminergic"


def test_get_receptor_unknown_returns_none():
    from pharm.core.receptors import get_receptor
    assert get_receptor("not-a-real-id") is None


def test_filter_by_family():
    from pharm.core.receptors import (
        list_receptors, receptors_for_family,
    )
    rtks = receptors_for_family("rtk")
    assert all(r.receptor_family == "rtk" for r in rtks)
    ids = {r.id for r in rtks}
    assert "egfr" in ids
    assert "insulin-receptor" in ids
    assert {r.id for r in list_receptors(
        family="rtk")} == ids


def test_find_receptors_by_drug_class():
    from pharm.core.receptors import find_receptors
    hits = find_receptors("metoprolol")
    ids = {r.id for r in hits}
    assert "adrenergic-beta1" in ids


def test_find_receptors_by_endogenous_ligand():
    from pharm.core.receptors import find_receptors
    hits = find_receptors("dopamine")
    ids = {r.id for r in hits}
    assert "dopamine-d2" in ids or "dat" in ids


def test_receptor_to_dict_is_serialisable():
    import json
    from pharm.core.receptors import (
        get_receptor, receptor_to_dict,
    )
    r = get_receptor("nmda")
    assert r is not None
    out = receptor_to_dict(r)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration + behaviour
# ------------------------------------------------------------------

def test_agent_actions_register_on_pharm_import():
    import pharm  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_receptors",
        "get_receptor",
        "find_receptors",
        "receptors_for_family",
        "open_pharm_receptors_tab",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_receptors_category():
    import pharm  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_receptors",
        "get_receptor",
        "find_receptors",
        "receptors_for_family",
        "open_pharm_receptors_tab",
    ):
        assert reg[name].category == "pharm-receptors"


def test_list_action_returns_dicts():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_receptors")
    assert isinstance(out, list)
    assert len(out) >= 25
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_receptor", receptor_id="egfr")
    assert isinstance(out, dict)
    assert out["id"] == "egfr"


def test_get_action_unknown_id_returns_clean_error():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_receptor", receptor_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_family_returns_error():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_receptors", family="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_receptors_for_family_action():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("receptors_for_family", family="nhr-steroid")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "glucocorticoid-receptor" in ids
    assert "androgen-receptor" in ids


def test_find_action_substring():
    import pharm  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_receptors", needle="hERG")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "herg-kv11-1" in ids


# ------------------------------------------------------------------
# GUI-audit + agent-surface-audit + category-summary integration
# ------------------------------------------------------------------

def test_gui_audit_includes_receptor_actions():
    import pharm  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_pharm_receptors_tab",
        "list_receptors",
        "get_receptor",
        "find_receptors",
        "receptors_for_family",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_receptors_surface():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_pharm_receptors_tab"]
    assert len(found) >= 1


def test_pharm_receptors_category_summary_present():
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    assert "pharm-receptors" in _CATEGORY_SUMMARIES
    assert _CATEGORY_SUMMARIES["pharm-receptors"].strip()
