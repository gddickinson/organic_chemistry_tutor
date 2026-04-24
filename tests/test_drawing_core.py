"""Phase 36a round 124 — tests for the headless structure-editor
data core (`orgchem/core/drawing.py`)."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# ---- dataclass ergonomics ---------------------------------------

def test_structure_add_atom_returns_index():
    from orgchem.core.drawing import Structure
    s = Structure()
    i0 = s.add_atom("C")
    i1 = s.add_atom("N")
    assert i0 == 0 and i1 == 1
    assert s.n_atoms == 2
    assert s.atoms[1].element == "N"


def test_structure_add_bond_validates_endpoints():
    from orgchem.core.drawing import Structure
    s = Structure()
    a = s.add_atom("C")
    b = s.add_atom("N")
    s.add_bond(a, b, order=3)
    assert s.n_bonds == 1
    # Self-loop is a value error.
    with pytest.raises(ValueError):
        s.add_bond(a, a)
    # Out-of-range endpoint is an index error.
    with pytest.raises(IndexError):
        s.add_bond(a, 99)


def test_structure_neighbours_ignores_direction():
    from orgchem.core.drawing import Structure
    s = Structure()
    a = s.add_atom("C")
    b = s.add_atom("C")
    c = s.add_atom("C")
    s.add_bond(a, b)
    s.add_bond(c, a)   # bond in reverse order — still a neighbour
    assert sorted(s.neighbours(a)) == [1, 2]


def test_bond_stereo_accepts_known_values_only():
    from orgchem.core.drawing import Bond
    b = Bond(0, 1, stereo="bogus")
    # Bad stereo tag falls back to 'none' rather than raising.
    assert b.stereo == "none"
    b = Bond(0, 1, stereo="wedge")
    assert b.stereo == "wedge"


def test_atom_defaults_element_to_carbon():
    from orgchem.core.drawing import Atom
    assert Atom().element == "C"
    assert Atom(element="").element == "C"


# ---- SMILES round-trip -------------------------------------------

@pytest.mark.parametrize("smi,expected_n_atoms", [
    ("C", 1),                  # methane
    ("CCO", 3),                # ethanol
    ("c1ccccc1", 6),           # benzene
    ("NCC(=O)O", 5),           # glycine
    ("C[C@@H](N)C(=O)O", 6),   # L-alanine with stereo
    ("[NH4+]", 1),             # charged ammonium
    ("CC(=O)OC1=CC=CC=C1C(=O)O", 13),  # aspirin
])
def test_structure_from_smiles_round_trip(smi, expected_n_atoms):
    from orgchem.core.drawing import (
        structure_from_smiles, structure_to_smiles,
    )
    from rdkit import Chem
    s = structure_from_smiles(smi)
    assert s is not None
    assert s.n_atoms == expected_n_atoms
    out = structure_to_smiles(s)
    assert out is not None
    # Canonical identity — compare canonicalised forms.
    assert Chem.CanonSmiles(out) == Chem.CanonSmiles(smi)


def test_structure_from_smiles_rejects_bogus_input():
    from orgchem.core.drawing import structure_from_smiles
    assert structure_from_smiles("") is None
    assert structure_from_smiles(None) is None
    assert structure_from_smiles("!!not-a-smiles!!") is None
    # Unclosed ring is a classic RDKit reject.
    assert structure_from_smiles("c1ccccc") is None


def test_structure_to_smiles_empty_returns_none():
    from orgchem.core.drawing import Structure, structure_to_smiles
    s = Structure()
    assert structure_to_smiles(s) is None


# ---- charge / isotope / radical preservation --------------------

def test_round_trip_preserves_charge():
    from orgchem.core.drawing import (
        structure_from_smiles, structure_to_smiles,
    )
    from rdkit import Chem
    s = structure_from_smiles("[NH4+]")
    out = structure_to_smiles(s)
    assert Chem.CanonSmiles(out) == Chem.CanonSmiles("[NH4+]")


def test_round_trip_preserves_isotope():
    from orgchem.core.drawing import (
        structure_from_smiles, structure_to_smiles,
    )
    from rdkit import Chem
    # 13C-labelled methanol.
    s = structure_from_smiles("[13CH3]O")
    out = structure_to_smiles(s)
    assert Chem.CanonSmiles(out) == Chem.CanonSmiles("[13CH3]O")


def test_round_trip_preserves_stereo():
    """Wedge / dash handled via RDKit BondDir — a simple test
    picks a chiral centre and confirms the CanonSmiles survives
    the round-trip."""
    from orgchem.core.drawing import (
        structure_from_smiles, structure_to_smiles,
    )
    from rdkit import Chem
    smi = "C[C@H](N)C(=O)O"     # L-alanine
    s = structure_from_smiles(smi)
    out = structure_to_smiles(s)
    assert Chem.CanonSmiles(out) == Chem.CanonSmiles(smi)


# ---- mol-block round-trip ---------------------------------------

def test_structure_to_molblock_round_trip():
    from orgchem.core.drawing import (
        structure_from_smiles, structure_to_molblock,
        structure_from_molblock, structure_to_smiles,
    )
    from rdkit import Chem
    smi = "c1ccc(cc1)CC(=O)O"    # phenylacetic acid
    s = structure_from_smiles(smi)
    block = structure_to_molblock(s)
    assert block is not None
    assert "V2000" in block or "V3000" in block
    s2 = structure_from_molblock(block)
    assert s2 is not None
    assert (Chem.CanonSmiles(structure_to_smiles(s2))
            == Chem.CanonSmiles(smi))


def test_structure_from_molblock_rejects_bogus_input():
    from orgchem.core.drawing import structure_from_molblock
    assert structure_from_molblock("") is None
    assert structure_from_molblock(None) is None
    assert structure_from_molblock("not a mol block") is None


# ---- hand-built structure → SMILES (canvas-path simulation) -----

def test_manually_built_structure_produces_correct_smiles():
    """Simulate the canvas path (Phase 36b): user clicks + drags
    to build an ethene molecule manually, round-trip via
    structure_to_smiles produces 'C=C'."""
    from orgchem.core.drawing import (
        Structure, structure_to_smiles,
    )
    from rdkit import Chem
    s = Structure()
    a = s.add_atom("C")
    b = s.add_atom("C")
    s.add_bond(a, b, order=2)
    out = structure_to_smiles(s)
    assert Chem.CanonSmiles(out) == Chem.CanonSmiles("C=C")


def test_manually_built_structure_with_heteroatom_and_charge():
    """User draws an ammonium cation (NH₄⁺) atom-by-atom."""
    from orgchem.core.drawing import (
        Structure, structure_to_smiles,
    )
    from rdkit import Chem
    s = Structure()
    s.add_atom("N", charge=1, h_count=4)
    out = structure_to_smiles(s)
    assert Chem.CanonSmiles(out) == Chem.CanonSmiles("[NH4+]")
