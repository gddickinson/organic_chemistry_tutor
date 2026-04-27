"""Phase MB-1.0 (round 215) — tests for the Microbiology Studio
microbe catalogue + agent actions + multi-hop cross-studio
integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from microbio.core import microbes
    assert hasattr(microbes, "Microbe")
    assert hasattr(microbes, "list_microbes")


def test_catalogue_has_at_least_30_entries():
    from microbio.core.microbes import list_microbes
    assert len(list_microbes()) >= 30


def test_every_microbe_has_required_fields():
    from microbio.core.microbes import (
        BALTIMORE_CLASSES, GRAM_TYPES, KINGDOMS, list_microbes,
    )
    for m in list_microbes():
        assert m.id and isinstance(m.id, str)
        assert m.name
        assert m.full_taxonomic_name
        assert m.kingdom in KINGDOMS, \
            f"{m.id}: invalid kingdom {m.kingdom!r}"
        assert m.gram_type in GRAM_TYPES, \
            f"{m.id}: invalid gram_type {m.gram_type!r}"
        # Baltimore class only set for viruses
        if m.kingdom == "virus":
            assert m.baltimore_class in BALTIMORE_CLASSES, \
                (f"{m.id}: virus must have valid baltimore "
                 f"class, got {m.baltimore_class!r}")
        else:
            assert m.baltimore_class == "", \
                (f"{m.id}: non-virus must have empty baltimore "
                 f"class, got {m.baltimore_class!r}")
        assert m.morphology
        assert m.key_metabolism_or_replication
        assert m.pathogenesis_summary
        assert m.antibiotic_susceptibility
        assert m.genome_size_or_kb
        assert m.ictv_or_bergey_reference
        assert isinstance(
            m.cross_reference_cell_component_ids, tuple)
        assert isinstance(
            m.cross_reference_pharm_drug_class_ids, tuple)
        assert isinstance(
            m.cross_reference_enzyme_ids, tuple)


def test_microbe_ids_are_unique():
    from microbio.core.microbes import list_microbes
    ids = [m.id for m in list_microbes()]
    assert len(ids) == len(set(ids))


def test_kingdoms_diverse():
    """All 5 microbial kingdoms must be represented."""
    from microbio.core.microbes import KINGDOMS, list_microbes
    seen = {m.kingdom for m in list_microbes()}
    assert seen == set(KINGDOMS), \
        f"missing kingdoms: {set(KINGDOMS) - seen}"


def test_gram_types_diverse():
    """At least 4 of the 5 Gram types should appear."""
    from microbio.core.microbes import list_microbes
    seen = {m.gram_type for m in list_microbes()}
    assert len(seen) >= 4


def test_viruses_cover_multiple_baltimore_classes():
    """The 6 seeded viruses should span at least 4 Baltimore
    classes — proves breadth."""
    from microbio.core.microbes import list_microbes
    classes = {m.baltimore_class for m in list_microbes()
               if m.kingdom == "virus"}
    assert len(classes) >= 4


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity (multi-hop)
# ------------------------------------------------------------------

def test_cross_reference_cell_component_ids_resolve_to_orgchem():
    """Every cross_reference_cell_component_ids entry must
    resolve to a real orgchem.core.cell_components id."""
    from microbio.core.microbes import list_microbes
    from orgchem.core.cell_components import (
        list_components as _list,
    )
    valid_ids = {c.id for c in _list()}
    for m in list_microbes():
        for ref in m.cross_reference_cell_component_ids:
            assert ref in valid_ids, \
                (f"{m.id}: dangling orgchem cell-component xref "
                 f"{ref!r}")


def test_cross_reference_pharm_drug_class_ids_resolve_to_pharm():
    """Multi-hop validation: every pharm-drug-class xref must
    resolve to a real pharm.core.drug_classes id."""
    from microbio.core.microbes import list_microbes
    from pharm.core.drug_classes import (
        list_drug_classes as _list,
    )
    valid_ids = {d.id for d in _list()}
    for m in list_microbes():
        for ref in m.cross_reference_pharm_drug_class_ids:
            assert ref in valid_ids, \
                (f"{m.id}: dangling pharm-drug-class xref "
                 f"{ref!r}")


def test_cross_reference_enzyme_ids_resolve_to_biochem():
    """Multi-hop validation: every biochem-enzyme xref must
    resolve to a real biochem.core.enzymes id."""
    from microbio.core.microbes import list_microbes
    from biochem.core.enzymes import (
        list_enzymes as _list,
    )
    valid_ids = {e.id for e in _list()}
    for m in list_microbes():
        for ref in m.cross_reference_enzyme_ids:
            assert ref in valid_ids, \
                (f"{m.id}: dangling biochem-enzyme xref "
                 f"{ref!r}")


def test_at_least_some_microbes_have_cross_references():
    """Sanity check: not every microbe can have empty cross-
    references — that would mean the catalogue is isolated
    from the platform."""
    from microbio.core.microbes import list_microbes
    has_refs = 0
    for m in list_microbes():
        if (m.cross_reference_cell_component_ids
                or m.cross_reference_pharm_drug_class_ids
                or m.cross_reference_enzyme_ids):
            has_refs += 1
    # At least half the catalogue should connect to the platform.
    assert has_refs >= 15


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_microbe():
    from microbio.core.microbes import get_microbe
    m = get_microbe("escherichia-coli")
    assert m is not None
    assert m.kingdom == "bacteria"
    assert m.gram_type == "gram-negative"


def test_get_microbe_unknown_returns_none():
    from microbio.core.microbes import get_microbe
    assert get_microbe("not-a-real-id") is None


def test_filter_by_kingdom():
    from microbio.core.microbes import (
        list_microbes, microbes_for_kingdom,
    )
    bacteria = microbes_for_kingdom("bacteria")
    assert all(m.kingdom == "bacteria" for m in bacteria)
    assert "escherichia-coli" in {m.id for m in bacteria}
    assert {m.id for m in list_microbes(
        kingdom="bacteria")} == {m.id for m in bacteria}


def test_filter_by_gram_type():
    from microbio.core.microbes import list_microbes
    pos = list_microbes(gram_type="gram-positive")
    ids = {m.id for m in pos}
    assert "staphylococcus-aureus" in ids
    assert "escherichia-coli" not in ids


def test_find_microbes_by_morphology():
    from microbio.core.microbes import find_microbes
    hits = find_microbes("coccus")
    ids = {m.id for m in hits}
    # Cocci should match Staph + Strep
    assert "staphylococcus-aureus" in ids


def test_find_microbes_by_disease():
    from microbio.core.microbes import find_microbes
    hits = find_microbes("malaria")
    ids = {m.id for m in hits}
    assert "plasmodium-falciparum" in ids


def test_microbe_to_dict_is_serialisable():
    import json
    from microbio.core.microbes import (
        get_microbe, microbe_to_dict,
    )
    m = get_microbe("mycobacterium-tuberculosis")
    assert m is not None
    out = microbe_to_dict(m)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration
# ------------------------------------------------------------------

def test_agent_actions_register_on_microbio_import():
    import microbio  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_microbes",
        "get_microbe",
        "find_microbes",
        "microbes_for_kingdom",
        "open_microbio_studio",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_microbio_category():
    import microbio  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_microbes",
        "get_microbe",
        "find_microbes",
        "microbes_for_kingdom",
        "open_microbio_studio",
    ):
        assert reg[name].category == "microbio-microbes"


def test_list_action_returns_dicts():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_microbes")
    assert isinstance(out, list)
    assert len(out) >= 30
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_microbe", microbe_id="hiv-1")
    assert isinstance(out, dict)
    assert out["id"] == "hiv-1"
    assert out["kingdom"] == "virus"


def test_get_action_unknown_id_returns_clean_error():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_microbe", microbe_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_kingdom_returns_error():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_microbes", kingdom="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_microbes_for_kingdom_action():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("microbes_for_kingdom", kingdom="virus")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "hiv-1" in ids
    assert "sars-cov-2" in ids


def test_microbes_for_kingdom_unknown_returns_error():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("microbes_for_kingdom", kingdom="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_find_action_substring():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_microbes", needle="tuberculosis")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "mycobacterium-tuberculosis" in ids


# ------------------------------------------------------------------
# GUI-audit integration
# ------------------------------------------------------------------

def test_gui_audit_includes_microbio_actions():
    import microbio  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_microbio_studio",
        "list_microbes",
        "get_microbe",
        "find_microbes",
        "microbes_for_kingdom",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_microbio_microbes():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_microbio_studio"]
    assert len(found) >= 1


# ------------------------------------------------------------------
# Tutorial scaffold
# ------------------------------------------------------------------

def test_microbio_curriculum_loads():
    from microbio.tutorial.curriculum import CURRICULUM
    assert "beginner" in CURRICULUM
    assert len(CURRICULUM["beginner"]) >= 1


def test_microbio_welcome_lesson_exists():
    from microbio.tutorial.curriculum import CURRICULUM
    welcome = CURRICULUM["beginner"][0]
    assert welcome["path"].exists()
    body = welcome["path"].read_text()
    assert "Microbiology Studio" in body
    assert "Pharm" in body
