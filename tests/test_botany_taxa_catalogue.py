"""Phase BT-1.0 (round 216) — tests for the Botany Studio
plant-taxa catalogue + agent actions + multi-hop cross-studio
integrity.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from botany.core import taxa
    assert hasattr(taxa, "PlantTaxon")
    assert hasattr(taxa, "list_plant_taxa")


def test_catalogue_has_at_least_30_entries():
    from botany.core.taxa import list_plant_taxa
    assert len(list_plant_taxa()) >= 30


def test_every_taxon_has_required_fields():
    from botany.core.taxa import (
        DIVISIONS, LIFE_CYCLES, PHOTOSYNTHETIC_STRATEGIES,
        list_plant_taxa,
    )
    for t in list_plant_taxa():
        assert t.id and isinstance(t.id, str)
        assert t.name
        assert t.full_taxonomic_name
        assert t.division in DIVISIONS, \
            f"{t.id}: invalid division {t.division!r}"
        assert t.plant_class
        assert t.life_cycle in LIFE_CYCLES, \
            f"{t.id}: invalid life_cycle {t.life_cycle!r}"
        assert t.photosynthetic_strategy in \
            PHOTOSYNTHETIC_STRATEGIES, \
            (f"{t.id}: invalid photosynthetic_strategy "
             f"{t.photosynthetic_strategy!r}")
        assert t.reproductive_strategy
        assert t.ecological_role
        assert t.economic_importance
        assert isinstance(t.model_organism, bool)
        assert t.genome_size_or_mb
        assert isinstance(
            t.cross_reference_molecule_names, tuple)
        assert isinstance(
            t.cross_reference_metabolic_pathway_ids, tuple)
        assert isinstance(
            t.cross_reference_pharm_drug_class_ids, tuple)


def test_taxon_ids_are_unique():
    from botany.core.taxa import list_plant_taxa
    ids = [t.id for t in list_plant_taxa()]
    assert len(ids) == len(set(ids))


def test_divisions_diverse():
    """At least 5 of the 6 divisions should appear."""
    from botany.core.taxa import list_plant_taxa
    seen = {t.division for t in list_plant_taxa()}
    assert len(seen) >= 5


def test_all_photosynthetic_strategies_represented():
    """All 4 photosynthetic strategies must appear in the
    catalogue — including ``not-applicable`` for the
    holoparasite Rafflesia."""
    from botany.core.taxa import (
        PHOTOSYNTHETIC_STRATEGIES, list_plant_taxa,
    )
    seen = {t.photosynthetic_strategy
            for t in list_plant_taxa()}
    assert seen == set(PHOTOSYNTHETIC_STRATEGIES), \
        f"missing strategies: " \
        f"{set(PHOTOSYNTHETIC_STRATEGIES) - seen}"


def test_at_least_some_model_organisms():
    """The catalogue should include several model-organism
    plants (Arabidopsis, rice, maize, Physcomitrium, etc.)."""
    from botany.core.taxa import list_plant_taxa
    n = sum(1 for t in list_plant_taxa() if t.model_organism)
    assert n >= 5


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity (multi-hop)
# ------------------------------------------------------------------

def test_cross_reference_molecule_names_resolve_to_orgchem(
    tmp_path,
):
    """Every `cross_reference_molecule_names` entry must
    resolve to a real `Molecule` row in the seeded DB."""
    from botany.core.taxa import list_plant_taxa
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.models import Molecule
    init_db(AppConfig.load())
    with session_scope() as s:
        valid_names = {m.name for m in s.query(Molecule).all()}
    for t in list_plant_taxa():
        for ref in t.cross_reference_molecule_names:
            assert ref in valid_names, \
                (f"{t.id}: dangling orgchem-molecule xref "
                 f"{ref!r}")


def test_cross_reference_metabolic_pathway_ids_resolve():
    """Every `cross_reference_metabolic_pathway_ids` entry
    must resolve to a real Phase-42 metabolic-pathway id."""
    from botany.core.taxa import list_plant_taxa
    from orgchem.core.metabolic_pathways import (
        list_pathways,
    )
    valid_ids = {p.id for p in list_pathways()}
    for t in list_plant_taxa():
        for ref in t.cross_reference_metabolic_pathway_ids:
            assert ref in valid_ids, \
                (f"{t.id}: dangling metabolic-pathway xref "
                 f"{ref!r}")


def test_cross_reference_pharm_drug_class_ids_resolve():
    """Every `cross_reference_pharm_drug_class_ids` entry must
    resolve to a real `pharm.core.drug_classes` id."""
    from botany.core.taxa import list_plant_taxa
    from pharm.core.drug_classes import list_drug_classes
    valid_ids = {d.id for d in list_drug_classes()}
    for t in list_plant_taxa():
        for ref in t.cross_reference_pharm_drug_class_ids:
            assert ref in valid_ids, \
                (f"{t.id}: dangling pharm-drug-class xref "
                 f"{ref!r}")


def test_at_least_some_taxa_have_cross_references():
    """Sanity check: at least ⅔ of taxa should connect to the
    platform via at least one cross-reference."""
    from botany.core.taxa import list_plant_taxa
    has_refs = 0
    for t in list_plant_taxa():
        if (t.cross_reference_molecule_names
                or t.cross_reference_metabolic_pathway_ids
                or t.cross_reference_pharm_drug_class_ids):
            has_refs += 1
    assert has_refs >= 20


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_plant_taxon():
    from botany.core.taxa import get_plant_taxon
    t = get_plant_taxon("arabidopsis-thaliana")
    assert t is not None
    assert t.division == "angiosperm-eudicot"
    assert t.model_organism


def test_get_plant_taxon_unknown_returns_none():
    from botany.core.taxa import get_plant_taxon
    assert get_plant_taxon("not-a-real-id") is None


def test_filter_by_division():
    from botany.core.taxa import (
        list_plant_taxa, plant_taxa_for_division,
    )
    eudicots = plant_taxa_for_division("angiosperm-eudicot")
    assert all(t.division == "angiosperm-eudicot"
               for t in eudicots)
    ids = {t.id for t in eudicots}
    assert "papaver-somniferum" in ids
    assert {t.id for t in list_plant_taxa(
        division="angiosperm-eudicot")} == ids


def test_filter_by_photosynthetic_strategy():
    from botany.core.taxa import list_plant_taxa
    c4 = list_plant_taxa(photosynthetic_strategy="C4")
    ids = {t.id for t in c4}
    assert "zea-mays" in ids
    cam = list_plant_taxa(photosynthetic_strategy="CAM")
    ids = {t.id for t in cam}
    assert "aloe-vera" in ids


def test_find_plant_taxa_by_metabolite_name():
    """Find should hit the cross_reference_molecule_names."""
    from botany.core.taxa import find_plant_taxa
    hits = find_plant_taxa("morphine")
    ids = {t.id for t in hits}
    assert "papaver-somniferum" in ids


def test_find_plant_taxa_by_common_name():
    from botany.core.taxa import find_plant_taxa
    hits = find_plant_taxa("rubber")
    ids = {t.id for t in hits}
    assert "hevea-brasiliensis" in ids


def test_plant_taxon_to_dict_is_serialisable():
    import json
    from botany.core.taxa import (
        get_plant_taxon, plant_taxon_to_dict,
    )
    t = get_plant_taxon("salix-alba")
    assert t is not None
    out = plant_taxon_to_dict(t)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration
# ------------------------------------------------------------------

def test_agent_actions_register_on_botany_import():
    import botany  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_plant_taxa",
        "get_plant_taxon",
        "find_plant_taxa",
        "plant_taxa_for_division",
        "open_botany_studio",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_botany_category():
    import botany  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_plant_taxa",
        "get_plant_taxon",
        "find_plant_taxa",
        "plant_taxa_for_division",
        "open_botany_studio",
    ):
        assert reg[name].category == "botany-taxa"


def test_list_action_returns_dicts():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_plant_taxa")
    assert isinstance(out, list)
    assert len(out) >= 30
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_plant_taxon",
                 taxon_id="papaver-somniferum")
    assert isinstance(out, dict)
    assert out["id"] == "papaver-somniferum"
    assert "Morphine" in out["cross_reference_molecule_names"]


def test_get_action_unknown_id_returns_clean_error():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_plant_taxon", taxon_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_division_returns_error():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_plant_taxa", division="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_plant_taxa_for_division_action():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("plant_taxa_for_division",
                 division="gymnosperm")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "ginkgo-biloba" in ids
    assert "taxus-brevifolia" in ids


def test_plant_taxa_for_division_unknown_returns_error():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("plant_taxa_for_division", division="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_find_action_substring():
    import botany  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_plant_taxa", needle="quinine")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "cinchona-officinalis" in ids


# ------------------------------------------------------------------
# GUI-audit integration
# ------------------------------------------------------------------

def test_gui_audit_includes_botany_actions():
    import botany  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_botany_studio",
        "list_plant_taxa",
        "get_plant_taxon",
        "find_plant_taxa",
        "plant_taxa_for_division",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_botany_taxa():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_botany_studio"]
    assert len(found) >= 1


# ------------------------------------------------------------------
# Tutorial scaffold
# ------------------------------------------------------------------

def test_botany_curriculum_loads():
    from botany.tutorial.curriculum import CURRICULUM
    assert "beginner" in CURRICULUM
    assert len(CURRICULUM["beginner"]) >= 1


def test_botany_welcome_lesson_exists():
    from botany.tutorial.curriculum import CURRICULUM
    welcome = CURRICULUM["beginner"][0]
    assert welcome["path"].exists()
    body = welcome["path"].read_text()
    assert "Botany Studio" in body
    assert "Pharm" in body
