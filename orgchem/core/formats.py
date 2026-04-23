"""Format conversion helpers — SMILES, InChI, MOL block, molecular formula."""
from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

from orgchem.messaging.errors import InvalidSMILESError


def mol_from_smiles(smiles: str) -> Chem.Mol:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise InvalidSMILESError(f"Could not parse SMILES: {smiles!r}")
    return mol


def mol_to_smiles(mol: Chem.Mol, canonical: bool = True) -> str:
    return Chem.MolToSmiles(mol, canonical=canonical)


def mol_to_inchi(mol: Chem.Mol) -> str:
    return Chem.MolToInchi(mol)


def mol_to_inchikey(mol: Chem.Mol) -> str:
    return Chem.MolToInchiKey(mol)


def mol_to_molblock(mol: Chem.Mol) -> str:
    return Chem.MolToMolBlock(mol)


def molecular_formula(mol: Chem.Mol) -> str:
    return rdMolDescriptors.CalcMolFormula(mol)
