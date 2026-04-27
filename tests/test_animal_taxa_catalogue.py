"""Phase AB-1.0 (round 217) — tests for the Animal Biology
Studio animal-taxa catalogue + agent actions + multi-hop
cross-studio integrity + the platform-retrospective lesson.
"""
from __future__ import annotations
import pytest


# ------------------------------------------------------------------
# Catalogue contents
# ------------------------------------------------------------------

def test_catalogue_imports():
    from animal.core import taxa
    assert hasattr(taxa, "AnimalTaxon")
    assert hasattr(taxa, "list_animal_taxa")


def test_catalogue_has_at_least_30_entries():
    from animal.core.taxa import list_animal_taxa
    assert len(list_animal_taxa()) >= 30


def test_every_taxon_has_required_fields():
    from animal.core.taxa import (
        BODY_PLANS, COELOM_TYPES, GERM_LAYERS, PHYLA,
        list_animal_taxa,
    )
    for t in list_animal_taxa():
        assert t.id and isinstance(t.id, str)
        assert t.name
        assert t.full_taxonomic_name
        assert t.phylum in PHYLA, \
            f"{t.id}: invalid phylum {t.phylum!r}"
        assert t.animal_class
        assert t.body_plan in BODY_PLANS, \
            f"{t.id}: invalid body_plan {t.body_plan!r}"
        assert t.germ_layers in GERM_LAYERS, \
            f"{t.id}: invalid germ_layers {t.germ_layers!r}"
        assert t.coelom_type in COELOM_TYPES, \
            f"{t.id}: invalid coelom_type {t.coelom_type!r}"
        assert t.reproductive_strategy
        assert t.ecological_role
        assert isinstance(t.model_organism, bool)
        assert t.genome_size_or_mb
        assert isinstance(
            t.cross_reference_molecule_names, tuple)
        assert isinstance(
            t.cross_reference_signaling_pathway_ids, tuple)
        assert isinstance(
            t.cross_reference_enzyme_ids, tuple)


def test_taxon_ids_are_unique():
    from animal.core.taxa import list_animal_taxa
    ids = [t.id for t in list_animal_taxa()]
    assert len(ids) == len(set(ids))


def test_phyla_diverse():
    """At least 8 of 9 phyla should appear."""
    from animal.core.taxa import list_animal_taxa
    seen = {t.phylum for t in list_animal_taxa()}
    assert len(seen) >= 8


def test_all_body_plans_represented():
    """All 3 body plans must appear: asymmetric (sponge),
    radial (cnidarians + adult echinoderms), bilateral
    (most animals)."""
    from animal.core.taxa import (
        BODY_PLANS, list_animal_taxa,
    )
    seen = {t.body_plan for t in list_animal_taxa()}
    assert seen == set(BODY_PLANS), \
        f"missing body plans: {set(BODY_PLANS) - seen}"


def test_germ_layer_diversity():
    """diploblast (cnidarians), triploblast (most), and
    not-applicable (sponges) must all appear."""
    from animal.core.taxa import (
        GERM_LAYERS, list_animal_taxa,
    )
    seen = {t.germ_layers for t in list_animal_taxa()}
    assert seen == set(GERM_LAYERS), \
        f"missing germ-layer values: " \
        f"{set(GERM_LAYERS) - seen}"


def test_coelom_diversity():
    """All 4 coelom-organisation types should appear:
    acoelomate (planarian), pseudocoelomate (nematodes),
    coelomate (most), not-applicable (sponges + cnidarians)."""
    from animal.core.taxa import (
        COELOM_TYPES, list_animal_taxa,
    )
    seen = {t.coelom_type for t in list_animal_taxa()}
    assert seen == set(COELOM_TYPES), \
        f"missing coelom types: " \
        f"{set(COELOM_TYPES) - seen}"


def test_at_least_some_model_organisms():
    """The catalogue should include several model-organism
    animals (C. elegans, Drosophila, zebrafish, mouse, …)."""
    from animal.core.taxa import list_animal_taxa
    n = sum(1 for t in list_animal_taxa() if t.model_organism)
    assert n >= 10


# ------------------------------------------------------------------
# Cross-studio cross-reference integrity (3-hop)
# ------------------------------------------------------------------

def test_cross_reference_molecule_names_resolve_to_orgchem():
    """Every `cross_reference_molecule_names` entry must
    resolve to a real `Molecule` row in the seeded DB."""
    from animal.core.taxa import list_animal_taxa
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.models import Molecule
    init_db(AppConfig.load())
    with session_scope() as s:
        valid_names = {m.name for m in s.query(Molecule).all()}
    for t in list_animal_taxa():
        for ref in t.cross_reference_molecule_names:
            assert ref in valid_names, \
                (f"{t.id}: dangling orgchem-molecule xref "
                 f"{ref!r}")


def test_cross_reference_signaling_pathway_ids_resolve():
    """Every `cross_reference_signaling_pathway_ids` entry
    must resolve to a real cellbio.core.cell_signaling id."""
    from animal.core.taxa import list_animal_taxa
    from cellbio.core.cell_signaling import list_pathways
    valid_ids = {p.id for p in list_pathways()}
    for t in list_animal_taxa():
        for ref in t.cross_reference_signaling_pathway_ids:
            assert ref in valid_ids, \
                (f"{t.id}: dangling cellbio-signaling xref "
                 f"{ref!r}")


def test_cross_reference_enzyme_ids_resolve():
    """Every `cross_reference_enzyme_ids` entry must resolve
    to a real biochem.core.enzymes id."""
    from animal.core.taxa import list_animal_taxa
    from biochem.core.enzymes import list_enzymes
    valid_ids = {e.id for e in list_enzymes()}
    for t in list_animal_taxa():
        for ref in t.cross_reference_enzyme_ids:
            assert ref in valid_ids, \
                (f"{t.id}: dangling biochem-enzyme xref "
                 f"{ref!r}")


def test_at_least_some_taxa_have_cross_references():
    """Sanity check: at least ⅔ of taxa should connect to
    the platform via at least one cross-reference."""
    from animal.core.taxa import list_animal_taxa
    has_refs = 0
    for t in list_animal_taxa():
        if (t.cross_reference_molecule_names
                or t.cross_reference_signaling_pathway_ids
                or t.cross_reference_enzyme_ids):
            has_refs += 1
    assert has_refs >= 20


def test_homo_sapiens_is_largest_cross_reference_hub():
    """*Homo sapiens* is the convergence point of the
    catalogue — should carry the most cross-references."""
    from animal.core.taxa import (
        get_animal_taxon, list_animal_taxa,
    )
    h = get_animal_taxon("homo-sapiens")
    assert h is not None
    h_count = (len(h.cross_reference_molecule_names)
               + len(h.cross_reference_signaling_pathway_ids)
               + len(h.cross_reference_enzyme_ids))
    for t in list_animal_taxa():
        if t.id == "homo-sapiens":
            continue
        other_count = (
            len(t.cross_reference_molecule_names)
            + len(t.cross_reference_signaling_pathway_ids)
            + len(t.cross_reference_enzyme_ids))
        assert other_count <= h_count, \
            f"{t.id} has more refs than homo-sapiens"


# ------------------------------------------------------------------
# Lookup helpers
# ------------------------------------------------------------------

def test_get_animal_taxon():
    from animal.core.taxa import get_animal_taxon
    t = get_animal_taxon("caenorhabditis-elegans")
    assert t is not None
    assert t.phylum == "nematoda"
    assert t.model_organism


def test_get_animal_taxon_unknown_returns_none():
    from animal.core.taxa import get_animal_taxon
    assert get_animal_taxon("not-a-real-id") is None


def test_filter_by_phylum():
    from animal.core.taxa import (
        animal_taxa_for_phylum, list_animal_taxa,
    )
    chordates = animal_taxa_for_phylum("chordata")
    assert all(t.phylum == "chordata" for t in chordates)
    ids = {t.id for t in chordates}
    assert "homo-sapiens" in ids
    assert "danio-rerio" in ids
    assert {t.id for t in list_animal_taxa(
        phylum="chordata")} == ids


def test_filter_by_body_plan():
    from animal.core.taxa import list_animal_taxa
    radial = list_animal_taxa(body_plan="radial")
    ids = {t.id for t in radial}
    assert "hydra-vulgaris" in ids


def test_find_animal_taxa_by_metabolite_name():
    """Find should hit the cross_reference_molecule_names."""
    from animal.core.taxa import find_animal_taxa
    hits = find_animal_taxa("cortisol")
    ids = {t.id for t in hits}
    assert "homo-sapiens" in ids
    assert "mus-musculus" in ids


def test_find_animal_taxa_by_common_name():
    from animal.core.taxa import find_animal_taxa
    hits = find_animal_taxa("zebrafish")
    ids = {t.id for t in hits}
    assert "danio-rerio" in ids


def test_animal_taxon_to_dict_is_serialisable():
    import json
    from animal.core.taxa import (
        animal_taxon_to_dict, get_animal_taxon,
    )
    t = get_animal_taxon("drosophila-melanogaster")
    assert t is not None
    out = animal_taxon_to_dict(t)
    assert json.dumps(out)


# ------------------------------------------------------------------
# Agent action registration
# ------------------------------------------------------------------

def test_agent_actions_register_on_animal_import():
    import animal  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_animal_taxa",
        "get_animal_taxon",
        "find_animal_taxa",
        "animal_taxa_for_phylum",
        "open_animal_studio",
    ):
        assert name in reg, f"missing action: {name}"


def test_agent_actions_have_animal_category():
    import animal  # noqa: F401
    from orgchem.agent.actions import registry
    reg = registry()
    for name in (
        "list_animal_taxa",
        "get_animal_taxon",
        "find_animal_taxa",
        "animal_taxa_for_phylum",
        "open_animal_studio",
    ):
        assert reg[name].category == "animal-taxa"


def test_list_action_returns_dicts():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_animal_taxa")
    assert isinstance(out, list)
    assert len(out) >= 30
    assert all(isinstance(o, dict) for o in out)


def test_get_action_returns_full_record():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_animal_taxon",
                 taxon_id="homo-sapiens")
    assert isinstance(out, dict)
    assert out["id"] == "homo-sapiens"
    assert "Cortisol" in out["cross_reference_molecule_names"]


def test_get_action_unknown_id_returns_clean_error():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("get_animal_taxon", taxon_id="not-real")
    assert isinstance(out, dict)
    assert "error" in out


def test_list_action_unknown_phylum_returns_error():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("list_animal_taxa", phylum="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_animal_taxa_for_phylum_action():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("animal_taxa_for_phylum",
                 phylum="arthropoda")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "drosophila-melanogaster" in ids
    assert "apis-mellifera" in ids


def test_animal_taxa_for_phylum_unknown_returns_error():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("animal_taxa_for_phylum", phylum="bogus")
    assert isinstance(out, list)
    assert len(out) == 1
    assert "error" in out[0]


def test_find_action_substring():
    import animal  # noqa: F401
    from orgchem.agent.actions import invoke
    out = invoke("find_animal_taxa", needle="axolotl")
    assert isinstance(out, list)
    ids = {o["id"] for o in out}
    assert "ambystoma-mexicanum" in ids


# ------------------------------------------------------------------
# GUI-audit integration
# ------------------------------------------------------------------

def test_gui_audit_includes_animal_actions():
    import animal  # noqa: F401
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in (
        "open_animal_studio",
        "list_animal_taxa",
        "get_animal_taxon",
        "find_animal_taxa",
        "animal_taxa_for_phylum",
    ):
        assert name in GUI_ENTRY_POINTS
        assert GUI_ENTRY_POINTS[name].strip()


def test_agent_surface_audit_has_animal_taxa():
    from orgchem.core.agent_surface_audit import EXPECTED_SURFACES
    found = [s for s in EXPECTED_SURFACES
             if s.opener == "open_animal_studio"]
    assert len(found) >= 1


# ------------------------------------------------------------------
# Tutorial scaffold + platform-retrospective coverage
# ------------------------------------------------------------------

def test_animal_curriculum_loads():
    from animal.tutorial.curriculum import CURRICULUM
    assert "beginner" in CURRICULUM
    # Both the welcome + the platform retrospective.
    assert len(CURRICULUM["beginner"]) >= 2


def test_animal_welcome_lesson_exists():
    from animal.tutorial.curriculum import CURRICULUM
    welcome = CURRICULUM["beginner"][0]
    assert welcome["path"].exists()
    body = welcome["path"].read_text()
    assert "Animal Biology Studio" in body


def test_platform_retrospective_lesson_mentions_every_sibling():
    """The platform retrospective must mention all 5 sibling
    studios + OrgChem by name + every sibling phase code."""
    from animal.tutorial.curriculum import CURRICULUM
    retro = CURRICULUM["beginner"][1]
    assert retro["path"].exists()
    body = retro["path"].read_text()
    # Every studio name.
    assert "OrgChem" in body
    assert "Cell Biology" in body or "Cell Bio" in body
    assert "Biochem" in body
    assert "Pharmacology" in body or "Pharm" in body
    assert "Microbiology" in body or "Microbio" in body
    assert "Botany" in body
    assert "Animal Biology" in body or "AB-1.0" in body
    # Every phase code.
    for code in ("CB-1.0", "BC-1.0", "PH-1.0",
                 "MB-1.0", "BT-1.0", "AB-1.0"):
        assert code in body, f"missing phase code: {code}"
    # The architectural-pattern markers.
    assert "shared" in body.lower()
    assert "registry" in body.lower()
    assert "cross-reference" in body.lower()
