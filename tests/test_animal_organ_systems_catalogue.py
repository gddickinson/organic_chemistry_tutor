"""Phase AB-2.0 (round 223) — tests for the Animal Biology
Studio organ-systems catalogue + agent actions + 4-hop cross-
studio integrity.  FINAL deep-phase round.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from animal.core import organ_systems
    assert hasattr(organ_systems, "OrganSystem")
    assert hasattr(organ_systems, "list_organ_systems")


def test_catalogue_has_at_least_25_entries():
    from animal.core.organ_systems import list_organ_systems
    assert len(list_organ_systems()) >= 25


def test_every_entry_has_required_fields():
    from animal.core.organ_systems import (
        SYSTEM_CATEGORIES, list_organ_systems,
    )
    for s in list_organ_systems():
        assert s.id and isinstance(s.id, str)
        assert s.name
        assert s.system_category in SYSTEM_CATEGORIES, \
            f"{s.id}: invalid category {s.system_category!r}"
        assert s.short_summary
        assert isinstance(s.representative_organs, tuple)
        assert isinstance(s.key_cell_types, tuple)
        assert isinstance(s.functional_anatomy, tuple)
        assert isinstance(s.evolutionary_origin, tuple)
        assert isinstance(s.characteristic_disorders, tuple)
        assert isinstance(
            s.cross_reference_molecule_names, tuple)
        assert isinstance(
            s.cross_reference_signaling_pathway_ids, tuple)
        assert isinstance(s.cross_reference_enzyme_ids, tuple)
        assert isinstance(
            s.cross_reference_animal_taxon_ids, tuple)


def test_post_init_validator_rejects_string_in_tuple_field():
    """Trailing-comma bug class — refused at construction.
    Last validator test of the -2 chain."""
    from animal.core.organ_systems import OrganSystem
    with pytest.raises(TypeError):
        OrganSystem(
            id="bad-system", name="Bad",
            system_category="cardiovascular",
            short_summary="…",
            representative_organs="not a tuple",  # ← the bug
            key_cell_types=(),
            functional_anatomy=(),
            evolutionary_origin=(),
            characteristic_disorders=(),
            cross_reference_molecule_names=(),
            cross_reference_signaling_pathway_ids=(),
            cross_reference_enzyme_ids=(),
            cross_reference_animal_taxon_ids=(),
        )


def test_entry_ids_are_unique():
    from animal.core.organ_systems import list_organ_systems
    ids = [s.id for s in list_organ_systems()]
    assert len(ids) == len(set(ids))


def test_at_least_8_categories_represented():
    from animal.core.organ_systems import list_organ_systems
    seen = {s.system_category for s in list_organ_systems()}
    assert len(seen) >= 8


def test_all_11_canonical_mammalian_systems_present():
    """Every canonical mammalian system should have at least
    one entry."""
    from animal.core.organ_systems import list_organ_systems
    seen = {s.system_category for s in list_organ_systems()}
    canonical = {
        "cardiovascular", "respiratory", "digestive",
        "urinary", "nervous", "endocrine", "immune",
        "musculoskeletal", "integumentary",
        "reproductive-female", "reproductive-male",
        "lymphatic",
    }
    missing = canonical - seen
    assert not missing, f"missing systems: {missing}"


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity (4-hop)
# ------------------------------------------------------------------

def test_cross_reference_molecule_names_resolve_to_orgchem():
    from animal.core.organ_systems import list_organ_systems
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.models import Molecule
    init_db(AppConfig.load())
    with session_scope() as s:
        valid_names = {m.name for m in s.query(Molecule).all()}
    for x in list_organ_systems():
        for ref in x.cross_reference_molecule_names:
            assert ref in valid_names, \
                (f"{x.id}: dangling molecule xref {ref!r}")


def test_cross_reference_signaling_pathway_ids_resolve():
    from animal.core.organ_systems import list_organ_systems
    from cellbio.core.cell_signaling import list_pathways
    valid_ids = {p.id for p in list_pathways()}
    for x in list_organ_systems():
        for ref in x.cross_reference_signaling_pathway_ids:
            assert ref in valid_ids, \
                (f"{x.id}: dangling pathway xref {ref!r}")


def test_cross_reference_enzyme_ids_resolve_to_biochem():
    from animal.core.organ_systems import list_organ_systems
    from biochem.core.enzymes import list_enzymes
    valid_ids = {e.id for e in list_enzymes()}
    for x in list_organ_systems():
        for ref in x.cross_reference_enzyme_ids:
            assert ref in valid_ids, \
                (f"{x.id}: dangling enzyme xref {ref!r}")


def test_cross_reference_animal_taxon_ids_resolve():
    from animal.core.organ_systems import list_organ_systems
    from animal.core.taxa import list_animal_taxa
    valid_ids = {t.id for t in list_animal_taxa()}
    for x in list_organ_systems():
        for ref in x.cross_reference_animal_taxon_ids:
            assert ref in valid_ids, \
                (f"{x.id}: dangling animal-taxon xref {ref!r}")


def test_at_least_some_entries_have_cross_references():
    from animal.core.organ_systems import list_organ_systems
    has_refs = sum(
        1 for x in list_organ_systems()
        if (x.cross_reference_molecule_names
            or x.cross_reference_signaling_pathway_ids
            or x.cross_reference_enzyme_ids
            or x.cross_reference_animal_taxon_ids))
    assert has_refs >= 15


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_organ_system():
    from animal.core.organ_systems import get_organ_system
    s = get_organ_system("nervous-mammalian")
    assert s is not None
    assert s.system_category == "nervous"


def test_get_organ_system_unknown_returns_none():
    from animal.core.organ_systems import get_organ_system
    assert get_organ_system("not-a-real-id") is None


def test_filter_by_category():
    from animal.core.organ_systems import (
        list_organ_systems, organ_systems_for_category,
    )
    comp = organ_systems_for_category("comparative-anatomy")
    assert all(s.system_category == "comparative-anatomy"
               for s in comp)
    ids = {s.id for s in comp}
    assert "regeneration-comparative" in ids
    assert {s.id for s in list_organ_systems(
        system_category="comparative-anatomy")} == ids


def test_find_organ_systems_by_disorder():
    from animal.core.organ_systems import find_organ_systems
    hits = find_organ_systems("Parkinson")
    ids = {s.id for s in hits}
    assert "nervous-mammalian" in ids


def test_find_organ_systems_by_animal():
    from animal.core.organ_systems import find_organ_systems
    hits = find_organ_systems("octopus")
    ids = {s.id for s in hits}
    assert "nervous-comparative" in ids


def test_organ_system_to_dict_is_serialisable():
    import json
    from animal.core.organ_systems import (
        get_organ_system, organ_system_to_dict,
    )
    s = get_organ_system("immune-mammalian")
    assert s is not None
    out = organ_system_to_dict(s)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration + behaviour
# ------------------------------------------------------------------

def test_agent_actions_register_on_animal_import():
    import animal  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_organ_systems",
        "get_organ_system",
        "find_organ_systems",
        "organ_systems_for_category",
        "open_animal_organ_systems_tab",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_organ_systems_category():
    import animal  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_organ_systems",
        "get_organ_system",
        "find_organ_systems",
        "organ_systems_for_category",
        "open_animal_organ_systems_tab",
    ):
        assert reg[name].category == "animal-organ-systems"


def test_list_action_returns_dicts():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_organ_systems")
    assert isinstance(out, list)
    assert len(out) >= 25
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_organ_system",
                 system_id="cardiovascular-mammalian")
    assert isinstance(out, dict)
    assert out["id"] == "cardiovascular-mammalian"


def test_get_action_unknown_id_returns_clean_error():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_organ_system", system_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_category_returns_error():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_organ_systems", system_category="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_organ_systems_for_category_action():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("organ_systems_for_category",
                 system_category="comparative-anatomy")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "regeneration-comparative" in ids


def test_find_action_substring():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_organ_systems", needle="hydra")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "regeneration-comparative" in ids \
        or "muscular-comparative" in ids


# ------------------------------------------------------------------
# GUI-audit + agent-surface-audit + category-summary integration
# ------------------------------------------------------------------

def test_gui_audit_includes_organ_system_actions():
    import animal  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_animal_organ_systems_tab",
        "list_organ_systems",
        "get_organ_system",
        "find_organ_systems",
        "organ_systems_for_category",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_organ_systems_surface():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_animal_organ_systems_tab"]
    assert len(found) >= 1


def test_animal_organ_systems_category_summary_present():
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    assert "animal-organ-systems" in _CATEGORY_SUMMARIES
    assert _CATEGORY_SUMMARIES["animal-organ-systems"].strip()
