"""Regression: Molecule.generate_3d must not give up on large flexible molecules.

RDKit's default ETKDG embedding (random seed 0xF00D) fails for long-chain lipids such as tripalmitin; RDKit's
documented remedy is to retry from random starting coordinates. Before the fix, the 3D viewer had no conformer for
the seeded Tripalmitin / Triolein / POPC / Sphingomyelin rows.
"""
from orgchem.core.molecule import Molecule

TRIPALMITIN = "CCCCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC"


def test_generate_3d_large_flexible_lipid():
    m = Molecule.from_smiles(TRIPALMITIN, generate_3d=True)
    assert m.molblock_3d, "no 3D conformer for tripalmitin"


def test_generate_3d_small_molecule_unchanged():
    m = Molecule.from_smiles("CCO", generate_3d=True)
    assert m.molblock_3d and m.molblock_3d.count("\n") > 9
