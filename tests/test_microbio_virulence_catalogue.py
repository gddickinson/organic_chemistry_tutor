"""Phase MB-2.0 (round 221) — tests for the Microbio Studio
virulence-factor catalogue + agent actions + cross-studio
integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from microbio.core import virulence_factors
    assert hasattr(virulence_factors, "VirulenceFactor")
    assert hasattr(virulence_factors, "list_virulence_factors")


def test_catalogue_has_at_least_25_entries():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    assert len(list_virulence_factors()) >= 25


def test_every_entry_has_required_fields():
    from microbio.core.virulence_factors import (
        MECHANISM_CLASSES, list_virulence_factors,
    )
    for f in list_virulence_factors():
        assert f.id and isinstance(f.id, str)
        assert f.name
        assert f.mechanism_class in MECHANISM_CLASSES, \
            f"{f.id}: invalid class {f.mechanism_class!r}"
        assert isinstance(f.structural_notes, tuple)
        assert isinstance(f.target_tissue_or_cell, tuple)
        assert isinstance(f.mode_of_action, tuple)
        assert isinstance(f.clinical_syndrome, tuple)
        assert isinstance(f.vaccine_or_antitoxin, tuple)
        assert isinstance(f.cross_reference_microbe_ids, tuple)
        assert isinstance(f.cross_reference_enzyme_ids, tuple)
        assert isinstance(
            f.cross_reference_signaling_pathway_ids, tuple)


def test_post_init_validator_rejects_string_in_tuple_field():
    """Trailing-comma bug class: refused at construction
    time, not silently coerced."""
    from microbio.core.virulence_factors import VirulenceFactor
    with pytest.raises(TypeError):
        VirulenceFactor(
            id="bad-factor", name="Bad",
            mechanism_class="ab-toxin",
            structural_notes="not a tuple",  # ← the bug
            target_tissue_or_cell=(),
            mode_of_action=(),
            clinical_syndrome=(),
            vaccine_or_antitoxin=(),
            cross_reference_microbe_ids=(),
            cross_reference_enzyme_ids=(),
            cross_reference_signaling_pathway_ids=(),
        )


def test_entry_ids_are_unique():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    ids = [f.id for f in list_virulence_factors()]
    assert len(ids) == len(set(ids))


def test_at_least_6_mechanism_classes_represented():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    seen = {f.mechanism_class
            for f in list_virulence_factors()}
    assert len(seen) >= 6


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity
# ------------------------------------------------------------------

def test_cross_reference_microbe_ids_resolve_to_microbio():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    from microbio.core.microbes import list_microbes
    valid_ids = {m.id for m in list_microbes()}
    for f in list_virulence_factors():
        for ref in f.cross_reference_microbe_ids:
            assert ref in valid_ids, \
                (f"{f.id}: dangling microbe xref {ref!r}")


def test_cross_reference_enzyme_ids_resolve_to_biochem():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    from biochem.core.enzymes import list_enzymes
    valid_ids = {e.id for e in list_enzymes()}
    for f in list_virulence_factors():
        for ref in f.cross_reference_enzyme_ids:
            assert ref in valid_ids, \
                (f"{f.id}: dangling enzyme xref {ref!r}")


def test_cross_reference_signaling_pathway_ids_resolve():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    from cellbio.core.cell_signaling import list_pathways
    valid_ids = {p.id for p in list_pathways()}
    for f in list_virulence_factors():
        for ref in f.cross_reference_signaling_pathway_ids:
            assert ref in valid_ids, \
                (f"{f.id}: dangling pathway xref {ref!r}")


def test_at_least_some_entries_have_cross_references():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    has_refs = sum(
        1 for f in list_virulence_factors()
        if (f.cross_reference_microbe_ids
            or f.cross_reference_enzyme_ids
            or f.cross_reference_signaling_pathway_ids))
    assert has_refs >= 15


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_virulence_factor():
    from microbio.core.virulence_factors import (
        get_virulence_factor,
    )
    f = get_virulence_factor("cholera-toxin")
    assert f is not None
    assert f.mechanism_class == "ab-toxin"


def test_get_virulence_factor_unknown_returns_none():
    from microbio.core.virulence_factors import (
        get_virulence_factor,
    )
    assert get_virulence_factor("not-a-real-id") is None


def test_filter_by_class():
    from microbio.core.virulence_factors import (
        list_virulence_factors,
        virulence_factors_for_class,
    )
    poreforming = virulence_factors_for_class("pore-forming")
    assert all(f.mechanism_class == "pore-forming"
               for f in poreforming)
    ids = {f.id for f in poreforming}
    assert "alpha-toxin-staph" in ids
    assert "listeriolysin-o" in ids
    assert {f.id for f in list_virulence_factors(
        mechanism_class="pore-forming")} == ids


def test_find_virulence_factors_by_disease():
    from microbio.core.virulence_factors import (
        find_virulence_factors,
    )
    hits = find_virulence_factors("HUS")
    ids = {f.id for f in hits}
    assert "shiga-toxin" in ids


def test_find_virulence_factors_by_microbe():
    from microbio.core.virulence_factors import (
        find_virulence_factors,
    )
    hits = find_virulence_factors("MRSA")
    ids = {f.id for f in hits}
    assert "pvl" in ids


def test_factor_to_dict_is_serialisable():
    import json
    from microbio.core.virulence_factors import (
        get_virulence_factor, virulence_factor_to_dict,
    )
    f = get_virulence_factor("lps-endotoxin")
    assert f is not None
    out = virulence_factor_to_dict(f)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration + behaviour
# ------------------------------------------------------------------

def test_agent_actions_register_on_microbio_import():
    import microbio  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_virulence_factors",
        "get_virulence_factor",
        "find_virulence_factors",
        "virulence_factors_for_class",
        "open_microbio_virulence_tab",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_virulence_category():
    import microbio  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_virulence_factors",
        "get_virulence_factor",
        "find_virulence_factors",
        "virulence_factors_for_class",
        "open_microbio_virulence_tab",
    ):
        assert reg[name].category == "microbio-virulence"


def test_list_action_returns_dicts():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_virulence_factors")
    assert isinstance(out, list)
    assert len(out) >= 25
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_virulence_factor",
                 factor_id="tetanus-toxin")
    assert isinstance(out, dict)
    assert out["id"] == "tetanus-toxin"


def test_get_action_unknown_id_returns_clean_error():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_virulence_factor", factor_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_class_returns_error():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_virulence_factors",
                 mechanism_class="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_virulence_factors_for_class_action():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("virulence_factors_for_class",
                 mechanism_class="superantigen")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "tsst-1" in ids


def test_find_action_substring():
    import microbio  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_virulence_factors", needle="LPS")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "lps-endotoxin" in ids


# ------------------------------------------------------------------
# GUI-audit + agent-surface-audit + category-summary integration
# ------------------------------------------------------------------

def test_gui_audit_includes_virulence_actions():
    import microbio  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_microbio_virulence_tab",
        "list_virulence_factors",
        "get_virulence_factor",
        "find_virulence_factors",
        "virulence_factors_for_class",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_virulence_surface():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_microbio_virulence_tab"]
    assert len(found) >= 1


def test_microbio_virulence_category_summary_present():
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    assert "microbio-virulence" in _CATEGORY_SUMMARIES
    assert _CATEGORY_SUMMARIES["microbio-virulence"].strip()
