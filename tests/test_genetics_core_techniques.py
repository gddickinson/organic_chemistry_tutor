"""Phase GM-1.0 (round 230) — tests for the
``genetics.core.techniques`` molecular-biology-techniques
catalogue.

Catalogue size, dataclass-validator behaviour, lookup helpers,
+ cross-reference-resolution gates.
"""
from __future__ import annotations
import pytest


# ----------------------------------------------------------------
# Catalogue size + structure
# ----------------------------------------------------------------

def test_catalogue_has_at_least_30_entries():
    from genetics.core.techniques import list_techniques
    assert len(list_techniques()) >= 30


def test_catalogue_has_40_entries_in_gm10():
    """The shipped GM-1.0 catalogue size is 40 entries."""
    from genetics.core.techniques import list_techniques
    assert len(list_techniques()) == 40


def test_categories_tuple_is_14_long():
    from genetics.core.techniques import CATEGORIES
    assert len(CATEGORIES) == 14
    expected = {
        "pcr", "sequencing", "cloning", "crispr", "blot",
        "in-situ", "chromatin", "transcriptomics", "spatial",
        "proteomics", "interaction", "structural",
        "epigenetics", "delivery",
    }
    assert set(CATEGORIES) == expected


def test_every_category_has_at_least_one_entry():
    from genetics.core.techniques import (
        CATEGORIES, list_techniques,
    )
    cats_in_use = {t.category for t in list_techniques()}
    for c in CATEGORIES:
        assert c in cats_in_use, \
            f"Category {c!r} has no entries in the catalogue"


def test_every_entry_has_unique_id():
    from genetics.core.techniques import list_techniques
    ids = [t.id for t in list_techniques()]
    assert len(ids) == len(set(ids)), \
        "Duplicate technique ids found"


def test_every_entry_has_non_empty_required_fields():
    from genetics.core.techniques import list_techniques
    for t in list_techniques():
        for field in (
            "id", "name", "abbreviation", "category",
            "principle", "sample_types", "throughput",
            "typical_readout", "key_reagents",
            "representative_platforms", "year_introduced",
            "key_references", "strengths", "limitations",
        ):
            value = getattr(t, field)
            assert isinstance(value, str), \
                f"{t.id}.{field} not str"
            assert value.strip(), \
                f"{t.id}.{field} is empty"


# ----------------------------------------------------------------
# Dataclass validator (BC-2.0 pattern, closes trailing-comma bug)
# ----------------------------------------------------------------

def test_validator_refuses_string_for_tuple_field():
    """The __post_init__ validator must reject a plain str
    where a Tuple[str, ...] field is expected."""
    from genetics.core.techniques import (
        MolecularBiologyTechnique,
    )
    with pytest.raises(TypeError):
        MolecularBiologyTechnique(
            id="test", name="Test", abbreviation="T",
            category="pcr",
            principle="x", sample_types="x",
            throughput="x", typical_readout="x",
            key_reagents="x", representative_platforms="x",
            year_introduced="x", key_references="x",
            strengths="x", limitations="x", notes="x",
            cross_reference_enzyme_ids="not-a-tuple",  # noqa
            cross_reference_cell_cycle_ids=(),
            cross_reference_signaling_pathway_ids=(),
            cross_reference_animal_taxon_ids=(),
            cross_reference_molecule_names=(),
        )


def test_validator_refuses_unknown_category():
    from genetics.core.techniques import (
        MolecularBiologyTechnique,
    )
    with pytest.raises(ValueError):
        MolecularBiologyTechnique(
            id="test", name="Test", abbreviation="T",
            category="bogus-category",
            principle="x", sample_types="x",
            throughput="x", typical_readout="x",
            key_reagents="x", representative_platforms="x",
            year_introduced="x", key_references="x",
            strengths="x", limitations="x", notes="x",
            cross_reference_enzyme_ids=(),
            cross_reference_cell_cycle_ids=(),
            cross_reference_signaling_pathway_ids=(),
            cross_reference_animal_taxon_ids=(),
            cross_reference_molecule_names=(),
        )


def test_validator_accepts_valid_tuple_fields():
    from genetics.core.techniques import (
        MolecularBiologyTechnique,
    )
    t = MolecularBiologyTechnique(
        id="test", name="Test", abbreviation="T",
        category="pcr",
        principle="x", sample_types="x",
        throughput="x", typical_readout="x",
        key_reagents="x", representative_platforms="x",
        year_introduced="x", key_references="x",
        strengths="x", limitations="x", notes="x",
        cross_reference_enzyme_ids=("dna-ligase-i",),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    )
    assert t.id == "test"


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def test_get_technique_returns_known_entry():
    from genetics.core.techniques import get_technique
    t = get_technique("crispr-cas9")
    assert t is not None
    assert t.name.startswith("CRISPR-Cas9")
    assert t.category == "crispr"


def test_get_technique_returns_none_for_unknown():
    from genetics.core.techniques import get_technique
    assert get_technique("does-not-exist") is None


def test_list_techniques_filters_by_category():
    from genetics.core.techniques import list_techniques
    crispr_only = list_techniques("crispr")
    assert len(crispr_only) >= 5
    assert all(t.category == "crispr" for t in crispr_only)


def test_find_techniques_case_insensitive():
    from genetics.core.techniques import find_techniques
    hits_lower = find_techniques("polymerase")
    hits_upper = find_techniques("POLYMERASE")
    assert {t.id for t in hits_lower} \
        == {t.id for t in hits_upper}
    assert len(hits_lower) >= 2


def test_find_techniques_searches_principle():
    """A search for 'thermostable' should find PCR entries
    whose principle mentions thermostable polymerase."""
    from genetics.core.techniques import find_techniques
    hits = find_techniques("thermostable")
    assert any(t.id == "endpoint-pcr" for t in hits)


def test_techniques_for_application_alias():
    from genetics.core.techniques import (
        techniques_for_application,
    )
    hits = techniques_for_application("single-cell")
    assert any(t.id == "scrna-seq" for t in hits)


def test_categories_helper_matches_module_constant():
    from genetics.core.techniques import (
        CATEGORIES, categories,
    )
    assert categories() == CATEGORIES


# ----------------------------------------------------------------
# Cross-reference resolution
# ----------------------------------------------------------------

def test_every_enzyme_xref_resolves_to_a_real_biochem_enzyme():
    from genetics.core.techniques import list_techniques
    from biochem.core.enzymes import get_enzyme
    broken = []
    for t in list_techniques():
        for eid in t.cross_reference_enzyme_ids:
            if get_enzyme(eid) is None:
                broken.append(f"{t.id}: enzyme {eid!r}")
    assert not broken, \
        f"Broken enzyme cross-references: {broken}"


def test_every_cell_cycle_xref_resolves():
    from genetics.core.techniques import list_techniques
    from cellbio.core.cell_cycle import get_cell_cycle_entry
    broken = []
    for t in list_techniques():
        for ccid in t.cross_reference_cell_cycle_ids:
            if get_cell_cycle_entry(ccid) is None:
                broken.append(
                    f"{t.id}: cell-cycle {ccid!r}")
    assert not broken, \
        f"Broken cell-cycle cross-references: {broken}"


def test_every_signaling_xref_resolves():
    from genetics.core.techniques import list_techniques
    from cellbio.core.cell_signaling import get_pathway
    broken = []
    for t in list_techniques():
        for pid in t.cross_reference_signaling_pathway_ids:
            if get_pathway(pid) is None:
                broken.append(f"{t.id}: pathway {pid!r}")
    assert not broken, \
        f"Broken signalling cross-references: {broken}"


def test_every_animal_taxon_xref_resolves():
    from genetics.core.techniques import list_techniques
    from animal.core.taxa import get_animal_taxon
    broken = []
    for t in list_techniques():
        for tid in t.cross_reference_animal_taxon_ids:
            if get_animal_taxon(tid) is None:
                broken.append(f"{t.id}: taxon {tid!r}")
    assert not broken, \
        f"Broken animal-taxon cross-references: {broken}"


def test_every_molecule_name_xref_resolves():
    """Molecule names cross-referenced by technique entries
    must exist as Molecule rows in the seeded DB."""
    from genetics.core.techniques import list_techniques
    from orgchem.config import AppConfig
    from orgchem.db.models import Molecule
    from orgchem.db.session import init_db, session_scope
    init_db(AppConfig.load())
    broken = []
    with session_scope() as s:
        for t in list_techniques():
            for n in t.cross_reference_molecule_names:
                m = (s.query(Molecule)
                     .filter(Molecule.name == n).first())
                if m is None:
                    broken.append(f"{t.id}: molecule {n!r}")
    assert not broken, \
        f"Broken molecule-name cross-references: {broken}"


# ----------------------------------------------------------------
# Catalogue substantive content (sanity check)
# ----------------------------------------------------------------

def test_principle_field_is_substantive():
    """Each technique's principle should be at least 50
    chars — a real explanation, not a stub."""
    from genetics.core.techniques import list_techniques
    for t in list_techniques():
        assert len(t.principle) >= 50, \
            f"{t.id}.principle too short: {t.principle!r}"


def test_at_least_one_entry_per_critical_subclass():
    """The catalogue must include the canonical entries that
    the GM-1.0 brief specifies."""
    from genetics.core.techniques import get_technique
    canonical = (
        "endpoint-pcr", "qpcr", "digital-pcr",
        "sanger-sequencing", "illumina-short-read",
        "pacbio-hifi", "ont-nanopore",
        "gibson-assembly", "golden-gate",
        "crispr-cas9", "crispr-cas12a",
        "base-editor", "prime-editor",
        "crispr-diagnostics",
        "western-blot", "fish", "smfish-merfish",
        "chip-seq", "atac-seq",
        "scrna-seq", "snrna-seq", "ribo-seq",
        "visium-spatial", "slide-seq",
        "bottom-up-proteomics", "proximity-labelling",
        "yeast-two-hybrid", "ap-ms",
        "hi-c", "bisulfite-seq", "methylation-array",
        "lipid-nanoparticle-delivery", "aav-delivery",
    )
    for cid in canonical:
        assert get_technique(cid) is not None, \
            f"Missing canonical technique {cid!r}"
