"""Molecule geometry for the web front end: RDKit 2D / 3D coordinates as compact JSON.

The browser draws molecules itself (draw2d.js as SVG, viewer3d.js in WebGL), so the API only sends atoms and bonds:

    {"a": [[symbol, x, y, charge, nH, aromatic, isotope, radicals], ...],
     "b": [[i, j, order, stereo], ...]}   order 1/2/3 (Kekule), 4 = aromatic if not kekulizable; stereo 1 wedge, 6 hash

Atom order is RDKit's parse order of the SMILES, which is what the mechanism arrows index into
(see orgchem/core/mechanism.py). 2D layout reuses the stored seed molblock when there is one (the app's canonical
depiction, orgchem/db/seed_coords.py) or CoordGen like Molecule.generate_2d; 3D uses Molecule.generate_3d (ETKDG + MMFF).
"""
from __future__ import annotations

import math
from typing import Optional

from rdkit import Chem, RDLogger
from rdkit.Chem import rdDepictor

RDLogger.DisableLog("rdApp.*")

_ORDER = {Chem.BondType.SINGLE: 1, Chem.BondType.DOUBLE: 2, Chem.BondType.TRIPLE: 3, Chem.BondType.AROMATIC: 4}
_DIR = {Chem.BondDir.BEGINWEDGE: 1, Chem.BondDir.BEGINDASH: 6}


def _r(v: float, nd: int = 3) -> float:
    return round(float(v), nd) + 0.0


def mol_json(mol: Chem.Mol, three_d: bool = False) -> dict:
    """Atoms and bonds of a molecule that already has a conformer."""
    conf = mol.GetConformer()
    atoms = []
    for a in mol.GetAtoms():
        p = conf.GetAtomPosition(a.GetIdx())
        xyz = [_r(p.x), _r(p.y)] + ([_r(p.z)] if three_d else [])
        atoms.append([a.GetSymbol(), *xyz, a.GetFormalCharge(), a.GetTotalNumHs(), int(a.GetIsAromatic()),
                      a.GetIsotope(), a.GetNumRadicalElectrons()])
    kek = Chem.Mol(mol)
    try:  # draw aromatic rings as Kekule structures (alternating single / double), as the desktop 2D viewer does
        Chem.Kekulize(kek, clearAromaticFlags=False)
    except Exception:  # noqa: BLE001 - not kekulizable: keep aromatic bonds (drawn with a dashed inner line)
        kek = mol
    bonds = []
    for b in kek.GetBonds():
        order = _ORDER.get(b.GetBondType(), 1)
        bonds.append([b.GetBeginAtomIdx(), b.GetEndAtomIdx(), order, _DIR.get(b.GetBondDir(), 0)])
    return {"a": atoms, "b": bonds, "dim": 3 if three_d else 2}


def _wedge(mol: Chem.Mol) -> None:
    try:
        Chem.WedgeMolBonds(mol, mol.GetConformer())
    except Exception:  # noqa: BLE001 - wedging is cosmetic
        pass


def depict_smiles(smiles: str) -> Optional[dict]:
    """2D coordinates for a SMILES, keeping the SMILES atom order (for mechanism arrows)."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        rdDepictor.SetPreferCoordGen(True)
        rdDepictor.Compute2DCoords(mol)
    finally:
        rdDepictor.SetPreferCoordGen(False)
    pos = mol.GetConformer().GetPositions()
    if not math.isfinite(float(pos.sum())):  # CoordGen gives NaN for e.g. [H][H]; RDKit's own depictor copes
        rdDepictor.Compute2DCoords(mol)
    _wedge(mol)
    return mol_json(mol)


def depict_molblock(molblock: Optional[str], smiles: str) -> Optional[dict]:
    """2D drawing from the stored seed molblock, falling back to a fresh layout of the SMILES."""
    if molblock:
        mol = Chem.MolFromMolBlock(molblock)
        if mol is not None and mol.GetNumConformers():
            _wedge(mol)
            return mol_json(mol)
    return depict_smiles(smiles)


def coords_3d(smiles: str) -> Optional[dict]:
    """3D conformer from the app's own Molecule.generate_3d (explicit hydrogens), or None if embedding fails."""
    from orgchem.core.molecule import Molecule
    try:
        m = Molecule.from_smiles(smiles, generate_3d=True)
    except Exception:  # noqa: BLE001 - unparsable / unembeddable structures simply have no 3D view
        return None
    if not m.molblock_3d:
        return None
    mol = Chem.MolFromMolBlock(m.molblock_3d, removeHs=False)
    if mol is None:
        return None
    return mol_json(mol, three_d=True)
