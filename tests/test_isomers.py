"""Phase 48a (round 170) — headless tests for the isomers
exploration core.
"""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# ==================================================================
# RELATIONSHIPS vocabulary + helpers
# ==================================================================

def test_relationships_vocabulary_complete():
    from orgchem.core.isomers import RELATIONSHIPS
    expected = {
        "identical", "constitutional", "enantiomer",
        "diastereomer", "meso", "tautomer",
        "different-molecule",
    }
    assert set(RELATIONSHIPS) == expected


def test_molecular_formula_helper():
    from orgchem.core.isomers import molecular_formula
    assert molecular_formula("CCO") == "C2H6O"
    assert molecular_formula("c1ccccc1") == "C6H6"
    # Unparseable input → None.
    assert molecular_formula("not-a-smiles") is None
    assert molecular_formula("") is None


# ==================================================================
# classify_isomer_relationship — every classification branch
# ==================================================================

def test_identical():
    """Same canonical SMILES (with stereo) → identical."""
    from orgchem.core.isomers import classify_isomer_relationship
    assert classify_isomer_relationship(
        "CCO", "CCO") == "identical"
    # Different SMILES strings, same canonical form.
    assert classify_isomer_relationship(
        "CCO", "OCC") == "identical"
    # Same with stereo.
    assert classify_isomer_relationship(
        "C[C@H](O)C(=O)O",
        "C[C@H](O)C(=O)O") == "identical"


def test_enantiomer_lactic_acid():
    """R-lactic + S-lactic acid are enantiomers."""
    from orgchem.core.isomers import classify_isomer_relationship
    assert classify_isomer_relationship(
        "C[C@H](O)C(=O)O",
        "C[C@@H](O)C(=O)O") == "enantiomer"


def test_diastereomer_threose():
    """(2R,3R)- vs (2R,3S)-2,3-dihydroxybutanoic acid are
    diastereomers — same connectivity, two stereocentres,
    not mirror images."""
    from orgchem.core.isomers import classify_isomer_relationship
    rr = "C[C@H](O)[C@H](O)C(=O)O"
    rs = "C[C@H](O)[C@@H](O)C(=O)O"
    assert classify_isomer_relationship(rr, rs) == "diastereomer"


def test_constitutional_isomers_same_formula():
    """Propanal + acetone share C3H6O but differ in
    connectivity — constitutional isomers."""
    from orgchem.core.isomers import classify_isomer_relationship
    assert classify_isomer_relationship(
        "CCC=O", "CC(C)=O") == "constitutional"


def test_constitutional_isomers_butanols():
    """1-butanol + 2-butanol + isobutanol + tert-butanol
    are all C4H10O constitutional isomers."""
    from orgchem.core.isomers import classify_isomer_relationship
    n_butanol = "CCCCO"
    sec_butanol = "CCC(O)C"
    iso_butanol = "CC(C)CO"
    tert_butanol = "CC(C)(C)O"
    for pair in ((n_butanol, sec_butanol),
                 (n_butanol, iso_butanol),
                 (n_butanol, tert_butanol),
                 (sec_butanol, iso_butanol)):
        assert classify_isomer_relationship(*pair) == \
            "constitutional"


def test_tautomer_acetone_keto_enol():
    """Acetone keto + enol forms are tautomers."""
    from orgchem.core.isomers import classify_isomer_relationship
    assert classify_isomer_relationship(
        "CC(=O)C", "CC(O)=C") == "tautomer"


def test_different_molecule_different_formula():
    """Benzene + toluene have different formulas — not
    isomers at all."""
    from orgchem.core.isomers import classify_isomer_relationship
    assert classify_isomer_relationship(
        "c1ccccc1", "Cc1ccccc1") == "different-molecule"


def test_different_molecule_unparseable():
    """Unparseable input → conservative
    different-molecule answer."""
    from orgchem.core.isomers import classify_isomer_relationship
    assert classify_isomer_relationship(
        "not-a-smiles", "CCO") == "different-molecule"
    assert classify_isomer_relationship(
        "CCO", "") == "different-molecule"


def test_classification_is_symmetric():
    """classify_isomer_relationship(a, b) should be symmetric
    for every relationship except possibly tautomer (where
    the enumeration direction may differ for asymmetric
    rule sets)."""
    from orgchem.core.isomers import classify_isomer_relationship
    pairs = [
        ("CCO", "CCO"),                                     # identical
        ("C[C@H](O)C(=O)O", "C[C@@H](O)C(=O)O"),           # enantiomer
        ("CCC=O", "CC(C)=O"),                               # constitutional
        ("c1ccccc1", "Cc1ccccc1"),                          # different
    ]
    for a, b in pairs:
        assert classify_isomer_relationship(a, b) == \
            classify_isomer_relationship(b, a), \
            f"asymmetric classification for {a} / {b}"


# ==================================================================
# enumerate_stereoisomers
# ==================================================================

def test_stereoisomers_two_centres():
    """A molecule with 2 unassigned stereocentres should
    expand to 4 isomers."""
    from orgchem.core.isomers import enumerate_stereoisomers
    res = enumerate_stereoisomers("CC(O)C(O)CO")
    assert len(res.canonical_smiles_list) == 4
    # Every result should carry stereo markers.
    for s in res.canonical_smiles_list:
        assert "@" in s


def test_stereoisomers_no_stereocentres():
    """A flat molecule with no stereocentres returns the
    input unchanged (1 result)."""
    from orgchem.core.isomers import enumerate_stereoisomers
    res = enumerate_stereoisomers("CCO")
    assert len(res.canonical_smiles_list) == 1
    assert res.truncated is False


def test_stereoisomers_fully_specified_input():
    """A fully-specified stereoisomer SMILES returns just
    itself."""
    from orgchem.core.isomers import enumerate_stereoisomers
    res = enumerate_stereoisomers("C[C@H](O)C(=O)O")
    assert len(res.canonical_smiles_list) == 1
    assert res.canonical_smiles_list[0] == "C[C@H](O)C(=O)O"


def test_stereoisomers_max_results_caps():
    """max_results caps the result set + sets truncated=True."""
    from orgchem.core.isomers import enumerate_stereoisomers
    # 4-stereocentre molecule → 16 isomers.  Cap at 4.
    res = enumerate_stereoisomers(
        "CC(O)C(O)C(O)C(O)CO", max_results=4)
    assert len(res.canonical_smiles_list) <= 4
    assert res.truncated is True


def test_stereoisomers_unparseable():
    from orgchem.core.isomers import enumerate_stereoisomers
    res = enumerate_stereoisomers("not-a-smiles")
    assert res.canonical_smiles_list == []
    assert res.truncated is False


# ==================================================================
# enumerate_tautomers
# ==================================================================

def test_tautomers_acetone():
    """Acetone has at least 2 tautomers (keto + enol)."""
    from orgchem.core.isomers import enumerate_tautomers
    res = enumerate_tautomers("CC(=O)C")
    assert len(res.canonical_smiles_list) >= 2


def test_tautomers_pentanedione():
    """2,4-pentanedione is a classic keto/enol equilibrium —
    RDKit's enumerator finds at least 5 tautomers."""
    from orgchem.core.isomers import enumerate_tautomers
    res = enumerate_tautomers("CC(=O)CC(=O)C")
    assert len(res.canonical_smiles_list) >= 5


def test_tautomers_no_tautomerism():
    """Methane has no tautomers — returns just itself."""
    from orgchem.core.isomers import enumerate_tautomers
    res = enumerate_tautomers("C")
    assert len(res.canonical_smiles_list) >= 1


def test_tautomers_unparseable():
    from orgchem.core.isomers import enumerate_tautomers
    res = enumerate_tautomers("not-a-smiles")
    assert res.canonical_smiles_list == []
