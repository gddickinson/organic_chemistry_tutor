"""Phase 47a (round 166) — headless tests for the
biochemistry-by-kingdom catalogue.
"""
from __future__ import annotations
import pytest


# ==================================================================
# Catalogue contents
# ==================================================================

def test_catalogue_size_at_least_sixty():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    assert len(list_topics()) >= 60


def test_all_four_kingdoms_represented():
    from orgchem.core.biochemistry_by_kingdom import (
        KINGDOMS, list_topics,
    )
    seen = {t.kingdom for t in list_topics()}
    assert seen == set(KINGDOMS), \
        f"missing: {set(KINGDOMS) - seen}"


def test_all_three_subtabs_represented():
    from orgchem.core.biochemistry_by_kingdom import (
        SUBTABS, list_topics,
    )
    seen = {t.subtab for t in list_topics()}
    assert seen == set(SUBTABS), \
        f"missing: {set(SUBTABS) - seen}"


def test_each_kingdom_has_balanced_subtab_coverage():
    """Each (kingdom, subtab) cell should have at least 4
    topics — a balanced grid for the dialog's 4-kingdom × 3-
    subtab layout."""
    from orgchem.core.biochemistry_by_kingdom import (
        KINGDOMS, SUBTABS, list_topics,
    )
    for k in KINGDOMS:
        for s in SUBTABS:
            cell = list_topics(kingdom=k, subtab=s)
            assert len(cell) >= 4, \
                f"({k}, {s}) cell has only {len(cell)} " \
                f"topics, expected ≥ 4"


def test_every_entry_has_required_fields():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    for t in list_topics():
        for fname in ("id", "kingdom", "subtab", "title",
                      "body"):
            assert getattr(t, fname), \
                f"missing {fname} on {t.id}"


def test_every_id_unique():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    ids = [t.id for t in list_topics()]
    assert len(ids) == len(set(ids)), \
        f"duplicate ids: " \
        f"{[i for i in ids if ids.count(i) > 1]}"


def test_every_id_lowercase_kebab():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    import re
    pat = re.compile(r"^[a-z0-9][a-z0-9-]*$")
    for t in list_topics():
        assert pat.match(t.id), f"bad id {t.id!r}"


def test_every_id_starts_with_kingdom_subtab():
    """Convention: topic ids start with `<kingdom>-<subtab>-`
    so the dialog can group them visually + the agent action's
    free-text search returns useful results when filtering by
    id substring."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    for t in list_topics():
        prefix = f"{t.kingdom}-{t.subtab}-"
        assert t.id.startswith(prefix), \
            f"id {t.id!r} should start with {prefix!r}"


def test_every_kingdom_in_canonical_set():
    from orgchem.core.biochemistry_by_kingdom import (
        KINGDOMS, list_topics,
    )
    kset = set(KINGDOMS)
    for t in list_topics():
        assert t.kingdom in kset


def test_every_subtab_in_canonical_set():
    from orgchem.core.biochemistry_by_kingdom import (
        SUBTABS, list_topics,
    )
    sset = set(SUBTABS)
    for t in list_topics():
        assert t.subtab in sset


def test_every_body_substantial():
    """Each topic body should be at least 200 characters —
    proves the entries are actual teaching content, not
    placeholder stubs."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    for t in list_topics():
        assert len(t.body) >= 200, \
            f"{t.id} body only {len(t.body)} chars (need ≥ 200)"


# ---- Per-row teaching invariants ------------------------------

def test_eukarya_genetics_includes_endosymbiotic_origin():
    """The endosymbiotic-origin topic is the headline
    eukarya-genetics teaching anchor — it MUST be present
    + cross-reference both mitochondria + chloroplasts."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic("eukarya-genetics-endosymbiotic-origin")
    assert t is not None
    body = t.body.lower()
    assert "endosymbiotic" in body
    assert "margulis" in body or "1967" in body
    assert "mitochondrion" in t.cross_reference_cell_component_ids
    assert "chloroplast" in t.cross_reference_cell_component_ids


def test_bacteria_genetics_includes_horizontal_gene_transfer():
    """HGT is the bacterial-genetics canonical teaching
    point — transformation + transduction + conjugation."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic("bacteria-genetics-horizontal-gene-transfer")
    assert t is not None
    body = t.body.lower()
    assert "transformation" in body
    assert "transduction" in body
    assert "conjugation" in body


def test_archaea_structure_lipid_divide_anchor():
    """The lipid divide is the strongest argument for the
    three-domain phylogeny — must be encoded explicitly."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic("archaea-structure-ether-lipids")
    assert t is not None
    body = t.body.lower()
    assert "ether" in body
    assert "isoprenoid" in body
    assert "three-domain" in body or "lipid divide" in body


def test_archaea_genetics_eukaryote_like_machinery():
    """Archaea look bacterial outside but eukaryote-like
    inside — must be encoded as the headline teaching
    anchor of archaeal information processing."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic("archaea-genetics-eukaryote-like-machinery")
    assert t is not None
    body = t.body.lower()
    assert "eukaryote" in body or "eukaryotic" in body
    assert ("rna polymerase" in body
            or "translation" in body
            or "mcm" in body)


def test_viruses_not_a_domain():
    """Viruses are biological entities but NOT a kingdom —
    the headline pedagogical clarification."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic("viruses-genetics-not-a-domain")
    assert t is not None
    body = t.body.lower()
    assert "ribosome" in body, \
        "must explain the lack of ribosomes (the most-cited " \
        "reason viruses aren't classified as living)"


def test_viruses_baltimore_classification():
    """The Baltimore classification (genome-type → mRNA
    relationship → 7 groups) is the canonical viral-genetics
    teaching anchor."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic("viruses-structure-genome-types")
    assert t is not None
    body = t.body.lower()
    assert "baltimore" in body
    # All 7 Baltimore groups should be mentioned in body or
    # surrounding examples.
    assert "retrovirus" in body or "reverse" in body


def test_viruses_endogenous_retroviruses():
    """ERVs as a major source of host genes — including the
    syncytin → mammalian placenta story — is the headline
    'viruses gave us biology' teaching anchor."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic(
        "viruses-genetics-endogenous-retroviruses")
    assert t is not None
    body = t.body.lower()
    assert "syncytin" in body
    assert "placenta" in body


def test_methanogenesis_archaea_only():
    """Methanogenesis is the only metabolic pathway exclusively
    in archaea — the headline distinctive-physiology anchor."""
    from orgchem.core.biochemistry_by_kingdom import get_topic
    t = get_topic("archaea-physiology-methanogenesis")
    assert t is not None
    body = t.body.lower()
    assert "only" in body or "exclusively" in body or \
        "uniquely" in body


# ---- Cross-reference resolution -------------------------------

def test_cell_component_xrefs_resolve_to_real_ids():
    """Every cross_reference_cell_component_ids entry must
    point to a real Phase-43 cell-component id — guards
    against rot when either catalogue is edited."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    from orgchem.core.cell_components import list_components
    valid = {c.id for c in list_components()}
    failed = []
    for t in list_topics():
        for xref in t.cross_reference_cell_component_ids:
            if xref not in valid:
                failed.append((t.id, xref))
    assert not failed, \
        f"unresolved cell-component xrefs: {failed}"


def test_pathway_xrefs_resolve_to_real_ids():
    """Every cross_reference_pathway_ids entry must point to
    a real Phase-42 metabolic-pathway id."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    from orgchem.core.metabolic_pathways import list_pathways
    valid = {p.id for p in list_pathways()}
    failed = []
    for t in list_topics():
        for xref in t.cross_reference_pathway_ids:
            if xref not in valid:
                failed.append((t.id, xref))
    assert not failed, \
        f"unresolved pathway xrefs: {failed}"


def test_at_least_some_topics_have_cross_references():
    """At least 8 topics should carry cross-references (cell
    components, pathways, or molecules) — proves the
    integration with existing catalogues actually exists."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    n_with_xrefs = sum(
        1 for t in list_topics()
        if (t.cross_reference_cell_component_ids
            or t.cross_reference_pathway_ids
            or t.cross_reference_molecule_names))
    assert n_with_xrefs >= 8, \
        f"only {n_with_xrefs} topics have cross-references; " \
        f"expected ≥ 8 for meaningful integration"


# ---- Filter / lookup ------------------------------------------

def test_list_filtered_by_kingdom():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    arch = list_topics(kingdom="archaea")
    assert all(t.kingdom == "archaea" for t in arch)
    assert len(arch) >= 10


def test_list_filtered_by_subtab():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    gen = list_topics(subtab="genetics")
    assert all(t.subtab == "genetics" for t in gen)
    assert len(gen) >= 15


def test_list_filtered_by_kingdom_and_subtab():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    arch_gen = list_topics(kingdom="archaea", subtab="genetics")
    for t in arch_gen:
        assert t.kingdom == "archaea"
        assert t.subtab == "genetics"
    assert len(arch_gen) >= 4


def test_list_unknown_kingdom_returns_empty():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    assert list_topics(kingdom="not-a-kingdom") == []


def test_list_unknown_subtab_returns_empty():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    assert list_topics(subtab="not-a-subtab") == []


def test_get_unknown_id_returns_none():
    from orgchem.core.biochemistry_by_kingdom import get_topic
    assert get_topic("does-not-exist") is None


def test_find_substring_case_insensitive():
    from orgchem.core.biochemistry_by_kingdom import find_topics
    a = {t.id for t in find_topics("CRISPR")}
    b = {t.id for t in find_topics("crispr")}
    assert a == b
    assert any("crispr" in tid for tid in a)


def test_find_empty_returns_empty():
    from orgchem.core.biochemistry_by_kingdom import find_topics
    assert find_topics("") == []


def test_find_searches_cross_reference_fields():
    """A search for a Phase-43 cell-component id like
    'mitochondrion' should land on topics that cross-reference
    it (not just topics that mention the word in the body)."""
    from orgchem.core.biochemistry_by_kingdom import find_topics
    hits = {t.id for t in find_topics("mitochondrion")}
    assert "eukarya-genetics-endosymbiotic-origin" in hits, \
        "find_topics should walk cross_reference fields"


def test_canonical_tuples_round_trip():
    from orgchem.core.biochemistry_by_kingdom import (
        KINGDOMS, SUBTABS, kingdoms, subtabs,
    )
    assert kingdoms() == KINGDOMS
    assert subtabs() == SUBTABS


# ---- topic_to_dict serialisation ------------------------------

# ==================================================================
# Round 169 / Phase 47d — sub-domain filter + plant / animal /
# fungus topic expansion
# ==================================================================

def test_catalogue_grew_to_at_least_sixty_eight():
    """Round 169 added 8 plant / animal / fungus topics to the
    eukarya tab + tagged 3 existing topics with sub_domain
    annotations.  Catalogue now ≥ 68."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    assert len(list_topics()) >= 68


def test_eukarya_kingdom_grew_to_at_least_twenty_three():
    """Eukarya tab grew from 15 → 23 topics with the round-169
    sub-domain expansion."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    assert len(list_topics(kingdom="eukarya")) >= 23


def test_sub_domains_for_kingdom_helper():
    from orgchem.core.biochemistry_by_kingdom import (
        sub_domains_for_kingdom,
    )
    assert sub_domains_for_kingdom("eukarya") == (
        "animal", "plant", "fungus", "protist")
    assert sub_domains_for_kingdom("bacteria") == (
        "gram-positive", "gram-negative")
    assert sub_domains_for_kingdom("archaea") == (
        "euryarchaeota", "crenarchaeota", "asgard")
    assert sub_domains_for_kingdom("viruses") == (
        "dna-virus", "rna-virus", "retrovirus")
    assert sub_domains_for_kingdom("not-a-kingdom") == ()


def test_filter_eukarya_animal_includes_pan_eukaryotic():
    """Pan-eukaryotic topics (sub_domain="") must surface
    under EVERY sub-domain query within their kingdom — so
    e.g. mitochondria + GPCR signalling appear under
    sub_domain='animal' even though they're eukaryote-wide.
    This mirrors the Phase-43 cell-component sub-domain
    semantics."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    animal_topics = list_topics(kingdom="eukarya",
                                sub_domain="animal")
    ids = {t.id for t in animal_topics}
    # Pan-eukaryotic (no sub_domain tag).
    assert "eukarya-physiology-aerobic-respiration" in ids
    assert "eukarya-physiology-signalling-gpcr" in ids
    # Animal-specific.
    assert "eukarya-structure-animal-tight-junctions" in ids
    assert "eukarya-physiology-animal-nervous-system" in ids


def test_filter_eukarya_plant_excludes_animal_only():
    """Plant filter must NOT surface animal-only topics."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    plant_topics = list_topics(kingdom="eukarya",
                               sub_domain="plant")
    ids = {t.id for t in plant_topics}
    # Plant-specific.
    assert "eukarya-physiology-photosynthesis" in ids
    assert "eukarya-structure-plant-vascular-tissue" in ids
    assert "eukarya-physiology-plant-auxin-photoperiodism" in ids
    assert "eukarya-genetics-plant-polyploidy" in ids
    # Animal-only must NOT appear under plant filter.
    assert "eukarya-structure-animal-tight-junctions" not in ids
    assert "eukarya-physiology-animal-nervous-system" not in ids


def test_filter_eukarya_fungus_includes_chitin_wall():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    fungus_topics = list_topics(kingdom="eukarya",
                                sub_domain="fungus")
    ids = {t.id for t in fungus_topics}
    assert "eukarya-physiology-fungus-hyphal-growth" in ids
    assert "eukarya-genetics-fungus-mating-types" in ids


def test_unknown_sub_domain_returns_empty():
    from orgchem.core.biochemistry_by_kingdom import list_topics
    assert list_topics(sub_domain="not-a-sub-domain") == []


def test_every_sub_domain_in_canonical_set():
    """Every topic's sub_domain field must be empty or in the
    canonical SUB_DOMAINS tuple."""
    from orgchem.core.biochemistry_by_kingdom import (
        SUB_DOMAINS, list_topics,
    )
    sset = set(SUB_DOMAINS) | {""}
    for t in list_topics():
        assert t.sub_domain in sset, \
            f"{t.id} has unknown sub_domain {t.sub_domain!r}"


def test_plant_animal_fungus_topic_count_at_least_eight():
    """Round 169 added at least 8 explicitly plant / animal /
    fungus topics."""
    from orgchem.core.biochemistry_by_kingdom import list_topics
    n = sum(1 for t in list_topics()
            if t.sub_domain in ("animal", "plant", "fungus"))
    assert n >= 8, \
        f"only {n} explicitly tagged topics; expected ≥ 8 " \
        f"after the round-169 expansion"


def test_topic_to_dict_includes_sub_domain():
    from orgchem.core.biochemistry_by_kingdom import (
        get_topic, topic_to_dict,
    )
    d = topic_to_dict(
        get_topic("eukarya-physiology-photosynthesis"))
    assert "sub_domain" in d
    assert d["sub_domain"] == "plant"


def test_topic_to_dict_keys():
    from orgchem.core.biochemistry_by_kingdom import (
        get_topic, topic_to_dict,
    )
    d = topic_to_dict(
        get_topic("eukarya-genetics-endosymbiotic-origin"))
    expected = {
        "id", "kingdom", "subtab", "title", "body",
        "cross_reference_cell_component_ids",
        "cross_reference_pathway_ids",
        "cross_reference_molecule_names",
        "notes",
        "sub_domain",   # round 169 / Phase 47d
    }
    assert set(d.keys()) == expected
