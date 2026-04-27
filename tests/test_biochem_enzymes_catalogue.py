"""Phase BC-1.0 (round 213) — tests for the Biochem Studio
enzyme catalogue + agent actions + cross-studio bridge.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from biochem.core import enzymes
    assert hasattr(enzymes, "Enzyme")
    assert hasattr(enzymes, "list_enzymes")


def test_catalogue_has_at_least_30_entries():
    """BC-1.0 baseline: ~ 30 enzymes."""
    from biochem.core.enzymes import list_enzymes
    assert len(list_enzymes()) >= 30


def test_every_enzyme_has_required_fields():
    from biochem.core.enzymes import list_enzymes
    for e in list_enzymes():
        assert e.id and isinstance(e.id, str)
        assert e.name
        assert e.ec_number
        assert e.ec_class in (1, 2, 3, 4, 5, 6, 7), \
            f"{e.id}: invalid ec_class {e.ec_class!r}"
        assert e.mechanism_class
        assert isinstance(e.substrates, tuple)
        assert isinstance(e.products, tuple)
        assert isinstance(e.cofactors, tuple)
        assert isinstance(e.regulators, tuple)
        assert isinstance(e.disease_associations, tuple)
        assert isinstance(e.drug_targets, tuple)
        for entry in e.drug_targets:
            assert isinstance(entry, tuple) and len(entry) == 2
        assert isinstance(e.cross_reference_molecule_names, tuple)
        assert isinstance(e.cross_reference_pathway_ids, tuple)
        assert isinstance(
            e.cross_reference_signaling_pathway_ids, tuple)


def test_ec_numbers_match_ec_class():
    """The first dotted segment of ec_number must equal
    ec_class."""
    from biochem.core.enzymes import list_enzymes
    for e in list_enzymes():
        first = e.ec_number.split(".")[0]
        assert first == str(e.ec_class), \
            (f"{e.id}: EC {e.ec_number} does not start with "
             f"class {e.ec_class}")


def test_all_seven_ec_classes_represented():
    """Catalogue spans every IUBMB EC class (1-7)."""
    from biochem.core.enzymes import list_enzymes
    classes = {e.ec_class for e in list_enzymes()}
    assert classes == {1, 2, 3, 4, 5, 6, 7}


def test_enzyme_ids_are_unique():
    from biochem.core.enzymes import list_enzymes
    ids = [e.id for e in list_enzymes()]
    assert len(ids) == len(set(ids))


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity
# ------------------------------------------------------------------

def test_cross_reference_pathway_ids_resolve_to_orgchem():
    """Every `cross_reference_pathway_ids` entry must resolve
    to a real orgchem.core.metabolic_pathways pathway id —
    catches stale references when orgchem renames a pathway."""
    from biochem.core.enzymes import list_enzymes
    from orgchem.core.metabolic_pathways import (
        list_pathways as orgchem_list_pathways,
    )
    valid_ids = {p.id for p in orgchem_list_pathways()}
    for e in list_enzymes():
        for ref in e.cross_reference_pathway_ids:
            assert ref in valid_ids, \
                (f"{e.id}: dangling orgchem-pathway xref "
                 f"{ref!r}")


def test_cross_reference_signaling_pathway_ids_resolve_to_cellbio():
    """Cross-studio: every `cross_reference_signaling_pathway_ids`
    entry must resolve to a real cellbio.core.cell_signaling
    pathway id."""
    from biochem.core.enzymes import list_enzymes
    from cellbio.core.cell_signaling import (
        list_pathways as cellbio_list_pathways,
    )
    valid_ids = {p.id for p in cellbio_list_pathways()}
    for e in list_enzymes():
        for ref in e.cross_reference_signaling_pathway_ids:
            assert ref in valid_ids, \
                (f"{e.id}: dangling cellbio-signaling xref "
                 f"{ref!r}")


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_enzyme():
    from biochem.core.enzymes import get_enzyme
    e = get_enzyme("chymotrypsin")
    assert e is not None
    assert "Chymotrypsin" in e.name
    assert e.ec_class == 3


def test_get_enzyme_unknown_returns_none():
    from biochem.core.enzymes import get_enzyme
    assert get_enzyme("not-a-real-id") is None


def test_filter_by_ec_class():
    from biochem.core.enzymes import (
        list_enzymes, enzymes_for_ec_class,
    )
    hyd = enzymes_for_ec_class(3)
    assert all(e.ec_class == 3 for e in hyd)
    assert "chymotrypsin" in {e.id for e in hyd}
    # list_enzymes with class arg behaves the same:
    assert {e.id for e in list_enzymes(ec_class=3)} == \
        {e.id for e in hyd}


def test_find_enzymes_by_drug_name():
    from biochem.core.enzymes import find_enzymes
    hits = find_enzymes("captopril")
    ids = {e.id for e in hits}
    assert "ace" in ids


def test_find_enzymes_by_disease():
    from biochem.core.enzymes import find_enzymes
    hits = find_enzymes("hypertension")
    ids = {e.id for e in hits}
    assert "ace" in ids


def test_enzyme_to_dict_is_serialisable():
    import json
    from biochem.core.enzymes import (
        get_enzyme, enzyme_to_dict,
    )
    e = get_enzyme("hexokinase")
    assert e is not None
    d = enzyme_to_dict(e)
    assert json.dumps(d)


# ------------------------------------------------------------------
# Agent action registration
# ------------------------------------------------------------------

def test_agent_actions_register_on_biochem_import():
    import biochem  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_enzymes",
        "get_enzyme",
        "find_enzymes",
        "enzymes_for_ec_class",
        "open_biochem_studio",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_biochem_category():
    import biochem  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_enzymes",
        "get_enzyme",
        "find_enzymes",
        "enzymes_for_ec_class",
        "open_biochem_studio",
    ):
        assert reg[name].category == "biochem-enzymes"


def test_list_action_returns_dicts():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_enzymes")
    assert isinstance(out, list)
    assert len(out) >= 30


def test_get_action_returns_full_record():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_enzyme", enzyme_id="atp-synthase")
    assert isinstance(out, dict)
    assert out["id"] == "atp-synthase"
    assert out["ec_class"] == 7


def test_get_action_unknown_id_returns_clean_error():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_enzyme", enzyme_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_ec_class_returns_error():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_enzymes", ec_class=99)
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_enzymes_for_ec_class_action():
    import biochem  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("enzymes_for_ec_class", ec_class=7)
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "atp-synthase" in ids
    assert "na-k-atpase" in ids


# ------------------------------------------------------------------
# GUI-audit integration
# ------------------------------------------------------------------

def test_gui_audit_includes_biochem_actions():
    import biochem  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_biochem_studio",
        "list_enzymes",
        "get_enzyme",
        "find_enzymes",
        "enzymes_for_ec_class",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_biochem_enzymes():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_biochem_studio"]
    assert len(found) >= 1


# ------------------------------------------------------------------
# Tutorial scaffold
# ------------------------------------------------------------------

def test_biochem_curriculum_loads():
    from biochem.tutorial.curriculum import CURRICULUM
    assert "beginner" in CURRICULUM
    assert len(CURRICULUM["beginner"]) >= 1


def test_biochem_welcome_lesson_exists():
    from biochem.tutorial.curriculum import CURRICULUM
    welcome = CURRICULUM["beginner"][0]
    assert welcome["path"].exists()
    body = welcome["path"].read_text()
    assert "Biochemistry Studio" in body
    assert "OrgChem" in body
    assert "Cell Bio" in body
