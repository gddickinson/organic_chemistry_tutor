"""Phase BC-2.0 (round 219) — tests for the Biochem Studio
cofactors catalogue + agent actions + cross-studio integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from biochem.core import cofactors
    assert hasattr(cofactors, "Cofactor")
    assert hasattr(cofactors, "list_cofactors")


def test_catalogue_has_at_least_25_entries():
    from biochem.core.cofactors import list_cofactors
    assert len(list_cofactors()) >= 25


def test_every_entry_has_required_fields():
    from biochem.core.cofactors import (
        COFACTOR_CLASSES, list_cofactors,
    )
    for c in list_cofactors():
        assert c.id and isinstance(c.id, str)
        assert c.name
        assert c.cofactor_class in COFACTOR_CLASSES, \
            f"{c.id}: invalid class {c.cofactor_class!r}"
        assert c.chemical_summary
        assert isinstance(c.primary_role, tuple)
        assert isinstance(c.carriers_or_substrates, tuple)
        assert isinstance(c.key_features, tuple)
        assert isinstance(c.vitamin_origin, tuple)
        assert isinstance(c.deficiency_disease, tuple)
        assert isinstance(c.cross_reference_enzyme_ids, tuple)
        assert isinstance(
            c.cross_reference_metabolic_pathway_ids, tuple)
        assert isinstance(
            c.cross_reference_molecule_names, tuple)


def test_post_init_validator_rejects_string_in_tuple_field():
    """The trailing-comma bug class — a single string in place
    of a single-element tuple — must raise TypeError loudly at
    construction time, not silently corrupt the dataclass."""
    from biochem.core.cofactors import Cofactor
    with pytest.raises(TypeError):
        Cofactor(
            id="bad-cofactor", name="Bad", cofactor_class="flavin",
            chemical_summary="…",
            primary_role="not a tuple",  # ← the bug
            carriers_or_substrates=(),
            key_features=(), vitamin_origin=(),
            deficiency_disease=(),
            cross_reference_enzyme_ids=(),
            cross_reference_metabolic_pathway_ids=(),
            cross_reference_molecule_names=(),
        )


def test_entry_ids_are_unique():
    from biochem.core.cofactors import list_cofactors
    ids = [c.id for c in list_cofactors()]
    assert len(ids) == len(set(ids))


def test_at_least_6_classes_represented():
    from biochem.core.cofactors import list_cofactors
    seen = {c.cofactor_class for c in list_cofactors()}
    assert len(seen) >= 6


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity
# ------------------------------------------------------------------

def test_cross_reference_enzyme_ids_resolve_to_biochem():
    """Every enzyme xref must resolve to a real BC-1.0 enzyme
    id."""
    from biochem.core.cofactors import list_cofactors
    from biochem.core.enzymes import list_enzymes
    valid_ids = {e.id for e in list_enzymes()}
    for c in list_cofactors():
        for ref in c.cross_reference_enzyme_ids:
            assert ref in valid_ids, \
                (f"{c.id}: dangling biochem-enzyme xref "
                 f"{ref!r}")


def test_cross_reference_metabolic_pathway_ids_resolve():
    """Every metabolic-pathway xref must resolve to a real
    orgchem.core.metabolic_pathways id."""
    from biochem.core.cofactors import list_cofactors
    from orgchem.core.metabolic_pathways import list_pathways
    valid_ids = {p.id for p in list_pathways()}
    for c in list_cofactors():
        for ref in c.cross_reference_metabolic_pathway_ids:
            assert ref in valid_ids, \
                (f"{c.id}: dangling metabolic-pathway xref "
                 f"{ref!r}")


def test_cross_reference_molecule_names_resolve_to_orgchem():
    """Every molecule-name xref must resolve to a real Molecule
    row in the seeded DB."""
    from biochem.core.cofactors import list_cofactors
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.models import Molecule
    init_db(AppConfig.load())
    with session_scope() as s:
        valid_names = {m.name for m in s.query(Molecule).all()}
    for c in list_cofactors():
        for ref in c.cross_reference_molecule_names:
            assert ref in valid_names, \
                (f"{c.id}: dangling orgchem-molecule xref "
                 f"{ref!r}")


def test_at_least_some_entries_have_cross_references():
    from biochem.core.cofactors import list_cofactors
    has_refs = sum(
        1 for c in list_cofactors()
        if (c.cross_reference_enzyme_ids
            or c.cross_reference_metabolic_pathway_ids
            or c.cross_reference_molecule_names))
    assert has_refs >= 15


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_cofactor():
    from biochem.core.cofactors import get_cofactor
    c = get_cofactor("nad-plus")
    assert c is not None
    assert c.cofactor_class == "nicotinamide"


def test_get_cofactor_unknown_returns_none():
    from biochem.core.cofactors import get_cofactor
    assert get_cofactor("not-a-real-id") is None


def test_filter_by_class():
    from biochem.core.cofactors import (
        cofactors_for_class, list_cofactors,
    )
    flavins = cofactors_for_class("flavin")
    assert all(c.cofactor_class == "flavin" for c in flavins)
    ids = {c.id for c in flavins}
    assert "fad" in ids
    assert "fmn" in ids
    assert {c.id for c in list_cofactors(
        cofactor_class="flavin")} == ids


def test_find_cofactors_by_vitamin():
    from biochem.core.cofactors import find_cofactors
    hits = find_cofactors("riboflavin")
    ids = {c.id for c in hits}
    assert "fad" in ids


def test_find_cofactors_by_disease():
    from biochem.core.cofactors import find_cofactors
    hits = find_cofactors("pellagra")
    ids = {c.id for c in hits}
    assert "nad-plus" in ids or "nadh" in ids


def test_cofactor_to_dict_is_serialisable():
    import json
    from biochem.core.cofactors import (
        cofactor_to_dict, get_cofactor,
    )
    c = get_cofactor("atp")
    assert c is not None
    out = cofactor_to_dict(c)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration + behaviour
# ------------------------------------------------------------------

def test_agent_actions_register_on_biochem_import():
    import biochem  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_cofactors",
        "get_cofactor",
        "find_cofactors",
        "cofactors_for_class",
        "open_biochem_cofactors_tab",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_cofactors_category():
    import biochem  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_cofactors",
        "get_cofactor",
        "find_cofactors",
        "cofactors_for_class",
        "open_biochem_cofactors_tab",
    ):
        assert reg[name].category == "biochem-cofactors"


def test_list_action_returns_dicts():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_cofactors")
    assert isinstance(out, list)
    assert len(out) >= 25
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_cofactor", cofactor_id="acetyl-coa")
    assert isinstance(out, dict)
    assert out["id"] == "acetyl-coa"


def test_get_action_unknown_id_returns_clean_error():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_cofactor", cofactor_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_class_returns_error():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_cofactors", cofactor_class="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_cofactors_for_class_action():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("cofactors_for_class",
                 cofactor_class="phosphate-energy")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "atp" in ids
    assert "gtp" in ids


def test_find_action_substring():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_cofactors", needle="heme")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "heme" in ids


# ------------------------------------------------------------------
# GUI-audit + agent-surface-audit + category-summary integration
# ------------------------------------------------------------------

def test_gui_audit_includes_cofactor_actions():
    import biochem  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_biochem_cofactors_tab",
        "list_cofactors",
        "get_cofactor",
        "find_cofactors",
        "cofactors_for_class",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_cofactors_surface():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_biochem_cofactors_tab"]
    assert len(found) >= 1


def test_biochem_cofactors_category_summary_present():
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    assert "biochem-cofactors" in _CATEGORY_SUMMARIES
    assert _CATEGORY_SUMMARIES["biochem-cofactors"].strip()
