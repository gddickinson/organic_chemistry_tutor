"""Phase BT-2.0 (round 222) — tests for the Botany Studio
plant-hormones catalogue + agent actions + cross-studio
integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from botany.core import plant_hormones
    assert hasattr(plant_hormones, "PlantHormone")
    assert hasattr(plant_hormones, "list_plant_hormones")


def test_catalogue_has_at_least_20_entries():
    from botany.core.plant_hormones import list_plant_hormones
    assert len(list_plant_hormones()) >= 20


def test_every_entry_has_required_fields():
    from botany.core.plant_hormones import (
        HORMONE_CLASSES, list_plant_hormones,
    )
    for h in list_plant_hormones():
        assert h.id and isinstance(h.id, str)
        assert h.name
        assert h.hormone_class in HORMONE_CLASSES, \
            f"{h.id}: invalid class {h.hormone_class!r}"
        assert h.structural_class
        assert isinstance(h.biosynthesis_precursor, tuple)
        assert isinstance(h.perception_mechanism, tuple)
        assert isinstance(
            h.primary_physiological_effect, tuple)
        assert isinstance(h.antagonisms, tuple)
        assert isinstance(h.key_model_plants, tuple)
        assert isinstance(
            h.cross_reference_molecule_names, tuple)
        assert isinstance(
            h.cross_reference_plant_taxon_ids, tuple)


def test_post_init_validator_rejects_string_in_tuple_field():
    """Trailing-comma bug class refused at construction time."""
    from botany.core.plant_hormones import PlantHormone
    with pytest.raises(TypeError):
        PlantHormone(
            id="bad-hormone", name="Bad",
            hormone_class="auxin",
            structural_class="…",
            biosynthesis_precursor="not a tuple",  # ← the bug
            perception_mechanism=(),
            primary_physiological_effect=(),
            antagonisms=(),
            key_model_plants=(),
            cross_reference_molecule_names=(),
            cross_reference_plant_taxon_ids=(),
        )


def test_entry_ids_are_unique():
    from botany.core.plant_hormones import list_plant_hormones
    ids = [h.id for h in list_plant_hormones()]
    assert len(ids) == len(set(ids))


def test_at_least_6_classes_represented():
    from botany.core.plant_hormones import list_plant_hormones
    seen = {h.hormone_class for h in list_plant_hormones()}
    assert len(seen) >= 6


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity
# ------------------------------------------------------------------

def test_cross_reference_molecule_names_resolve_to_orgchem():
    from botany.core.plant_hormones import list_plant_hormones
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.models import Molecule
    init_db(AppConfig.load())
    with session_scope() as s:
        valid_names = {m.name for m in s.query(Molecule).all()}
    for h in list_plant_hormones():
        for ref in h.cross_reference_molecule_names:
            assert ref in valid_names, \
                (f"{h.id}: dangling molecule xref {ref!r}")


def test_cross_reference_plant_taxon_ids_resolve_to_botany():
    from botany.core.plant_hormones import list_plant_hormones
    from botany.core.taxa import list_plant_taxa
    valid_ids = {t.id for t in list_plant_taxa()}
    for h in list_plant_hormones():
        for ref in h.cross_reference_plant_taxon_ids:
            assert ref in valid_ids, \
                (f"{h.id}: dangling plant-taxon xref {ref!r}")


def test_at_least_some_entries_have_cross_references():
    from botany.core.plant_hormones import list_plant_hormones
    has_refs = sum(
        1 for h in list_plant_hormones()
        if (h.cross_reference_molecule_names
            or h.cross_reference_plant_taxon_ids))
    assert has_refs >= 10


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_plant_hormone():
    from botany.core.plant_hormones import get_plant_hormone
    h = get_plant_hormone("iaa")
    assert h is not None
    assert h.hormone_class == "auxin"


def test_get_plant_hormone_unknown_returns_none():
    from botany.core.plant_hormones import get_plant_hormone
    assert get_plant_hormone("not-a-real-id") is None


def test_filter_by_class():
    from botany.core.plant_hormones import (
        list_plant_hormones, plant_hormones_for_class,
    )
    auxins = plant_hormones_for_class("auxin")
    assert all(h.hormone_class == "auxin" for h in auxins)
    ids = {h.id for h in auxins}
    assert "iaa" in ids
    assert {h.id for h in list_plant_hormones(
        hormone_class="auxin")} == ids


def test_find_plant_hormones_by_receptor():
    from botany.core.plant_hormones import find_plant_hormones
    hits = find_plant_hormones("FERONIA")
    ids = {h.id for h in hits}
    assert "ralf-peptides" in ids


def test_find_plant_hormones_by_concept():
    from botany.core.plant_hormones import find_plant_hormones
    hits = find_plant_hormones("Green Revolution")
    ids = {h.id for h in hits}
    assert "ga3" in ids


def test_hormone_to_dict_is_serialisable():
    import json
    from botany.core.plant_hormones import (
        get_plant_hormone, plant_hormone_to_dict,
    )
    h = get_plant_hormone("aba")
    assert h is not None
    out = plant_hormone_to_dict(h)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration + behaviour
# ------------------------------------------------------------------

def test_agent_actions_register_on_botany_import():
    import botany  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_plant_hormones",
        "get_plant_hormone",
        "find_plant_hormones",
        "plant_hormones_for_class",
        "open_botany_plant_hormones_tab",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_hormones_category():
    import botany  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_plant_hormones",
        "get_plant_hormone",
        "find_plant_hormones",
        "plant_hormones_for_class",
        "open_botany_plant_hormones_tab",
    ):
        assert reg[name].category == "botany-hormones"


def test_list_action_returns_dicts():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_plant_hormones")
    assert isinstance(out, list)
    assert len(out) >= 20
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_plant_hormone", hormone_id="ethylene")
    assert isinstance(out, dict)
    assert out["id"] == "ethylene"


def test_get_action_unknown_id_returns_clean_error():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_plant_hormone", hormone_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_class_returns_error():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_plant_hormones", hormone_class="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_plant_hormones_for_class_action():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("plant_hormones_for_class",
                 hormone_class="cytokinin")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "trans-zeatin" in ids


def test_find_action_substring():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_plant_hormones", needle="strigol")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "strigol" in ids


# ------------------------------------------------------------------
# GUI-audit + agent-surface-audit + category-summary integration
# ------------------------------------------------------------------

def test_gui_audit_includes_plant_hormone_actions():
    import botany  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_botany_plant_hormones_tab",
        "list_plant_hormones",
        "get_plant_hormone",
        "find_plant_hormones",
        "plant_hormones_for_class",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_plant_hormones_surface():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_botany_plant_hormones_tab"]
    assert len(found) >= 1


def test_botany_hormones_category_summary_present():
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    assert "botany-hormones" in _CATEGORY_SUMMARIES
    assert _CATEGORY_SUMMARIES["botany-hormones"].strip()
