"""Phase 36f.1 (round 131) — headless tests for the
reaction-scheme core.

Covers the :class:`Scheme` dataclass, both directions of the
SMILES round-trip (pair / reaction-string), per-side SMILES
extraction, JSON-friendly :meth:`Scheme.to_dict` /
:meth:`Scheme.from_dict`, and the balanced-atom-count sanity
hint.  No Qt imports.
"""
from __future__ import annotations

import pytest

pytest.importorskip("rdkit")

from orgchem.core.drawing import structure_from_smiles
from orgchem.core.drawing_scheme import (
    Scheme,
    is_balanced_atom_counts,
)


# ---- empty-state defaults --------------------------------------

def test_scheme_defaults_to_empty():
    s = Scheme()
    assert s.lhs == []
    assert s.rhs == []
    assert s.arrow == "forward"
    assert s.reagents == ""
    assert s.is_empty
    assert s.n_lhs_atoms == 0
    assert s.n_rhs_atoms == 0


def test_unknown_arrow_falls_back_to_forward():
    s = Scheme(arrow="loop-the-loop")
    assert s.arrow == "forward"


def test_explicit_reversible_arrow_preserved():
    s = Scheme(arrow="reversible")
    assert s.arrow == "reversible"


# ---- from_smiles_pair ------------------------------------------

def test_from_smiles_pair_simple_substitution():
    s = Scheme.from_smiles_pair("CBr.[OH-]", "CO.[Br-]")
    assert s is not None
    assert len(s.lhs) == 2
    assert len(s.rhs) == 2
    assert s.n_lhs_atoms == s.n_rhs_atoms


def test_from_smiles_pair_garbage_returns_none():
    assert Scheme.from_smiles_pair("!!nope", "C") is None
    assert Scheme.from_smiles_pair("C", "!!nope") is None


def test_from_smiles_pair_empty_lhs_is_valid():
    """Empty LHS = "starting from nothing" = synthetic-target
    scheme.  Should parse OK."""
    s = Scheme.from_smiles_pair("", "CCO")
    assert s is not None
    assert s.lhs == []
    assert len(s.rhs) == 1


# ---- reaction-SMILES round-trip --------------------------------

def test_to_reaction_smiles_basic():
    s = Scheme.from_smiles_pair("CCO", "CC=O")
    assert s is not None
    rxn = s.to_reaction_smiles()
    assert rxn == "CCO>>CC=O"


def test_to_reaction_smiles_with_reagents():
    s = Scheme.from_smiles_pair("CCO", "CC=O", reagents="[Cr]")
    assert s.to_reaction_smiles() == "CCO>[Cr]>CC=O"


def test_from_reaction_smiles_round_trip():
    rxn = "CC(=O)Cl.NC>>CC(=O)NC.Cl"
    scheme = Scheme.from_reaction_smiles(rxn)
    assert scheme is not None
    assert len(scheme.lhs) == 2
    assert len(scheme.rhs) == 2
    # Round-trip via canonical SMILES.
    from rdkit import Chem
    rxn2 = scheme.to_reaction_smiles()
    # Compare canonicalised LHS / RHS components.
    lhs_in = sorted(Chem.CanonSmiles(p)
                    for p in rxn.split(">")[0].split("."))
    lhs_out = sorted(Chem.CanonSmiles(p)
                     for p in rxn2.split(">")[0].split("."))
    assert lhs_in == lhs_out


def test_from_reaction_smiles_preserves_reagents():
    scheme = Scheme.from_reaction_smiles("CCO>[Cr]>CC=O")
    assert scheme is not None
    assert scheme.reagents == "[Cr]"


def test_from_reaction_smiles_rejects_malformed():
    # Wrong number of arrow segments.
    assert Scheme.from_reaction_smiles("CCO>CC=O") is None
    assert Scheme.from_reaction_smiles("foo") is None
    assert Scheme.from_reaction_smiles("") is None


def test_from_reaction_smiles_rejects_garbage_components():
    assert Scheme.from_reaction_smiles("!!nope>>C") is None


# ---- per-side SMILES ------------------------------------------

def test_lhs_smiles_joins_components_with_dot():
    s = Scheme.from_smiles_pair("CC.OO", "CCO")
    from rdkit import Chem
    parts = s.lhs_smiles().split(".")
    canon = sorted(Chem.CanonSmiles(p) for p in parts)
    assert canon == sorted(
        [Chem.CanonSmiles("CC"), Chem.CanonSmiles("OO")])


def test_rhs_smiles_empty_on_empty_rhs():
    s = Scheme.from_smiles_pair("CCO", "")
    assert s.rhs_smiles() == ""


# ---- to_dict / from_dict ---------------------------------------

def test_to_dict_round_trip():
    original = Scheme.from_smiles_pair(
        "CC=O", "CCO", reagents="NaBH4", arrow="forward")
    payload = original.to_dict()
    rebuilt = Scheme.from_dict(payload)
    assert rebuilt is not None
    assert rebuilt.arrow == "forward"
    assert rebuilt.reagents == "NaBH4"
    from rdkit import Chem
    assert Chem.CanonSmiles(rebuilt.lhs_smiles()) == \
           Chem.CanonSmiles("CC=O")
    assert Chem.CanonSmiles(rebuilt.rhs_smiles()) == \
           Chem.CanonSmiles("CCO")


def test_from_dict_with_garbage_smiles_returns_none():
    assert Scheme.from_dict({"lhs": "!!nope", "rhs": "C"}) is None


def test_from_dict_rejects_non_dict():
    assert Scheme.from_dict("not a dict") is None
    assert Scheme.from_dict(None) is None


# ---- atom-count balance hint ----------------------------------

def test_empty_scheme_is_trivially_balanced():
    assert is_balanced_atom_counts(Scheme()) is True


def test_balanced_aldehyde_reduction():
    s = Scheme.from_smiles_pair("CC=O", "CCO")
    assert is_balanced_atom_counts(s) is True


def test_unbalanced_when_atom_counts_differ():
    # CC → CCO: oxidation product gained an oxygen, no
    # corresponding LHS source — clearly unbalanced.
    s = Scheme.from_smiles_pair("CC", "CCO")
    assert is_balanced_atom_counts(s) is False


# ---- multi-component edge cases -------------------------------

def test_to_reaction_smiles_skips_empty_substructures():
    """A scheme with an empty Structure mixed in should still
    serialise cleanly — empty halves render as '' separators."""
    from orgchem.core.drawing import Structure
    s = Scheme(lhs=[structure_from_smiles("CC"), Structure()],
               rhs=[structure_from_smiles("CCO")])
    rxn = s.to_reaction_smiles()
    assert rxn == "CC>>CCO"


def test_n_atom_counts_match_structure_state():
    s = Scheme.from_smiles_pair("CCO", "CC=O")
    assert s.n_lhs_atoms == 3
    assert s.n_rhs_atoms == 3
