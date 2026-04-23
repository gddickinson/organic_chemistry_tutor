"""Molecular descriptor calculators."""
from __future__ import annotations
from typing import Any, Dict

from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen, rdMolDescriptors


def compute_all(mol: Chem.Mol) -> Dict[str, Any]:
    """Return a dict of common descriptors for *mol*."""
    return {
        "mol_weight": Descriptors.MolWt(mol),
        "exact_mass": Descriptors.ExactMolWt(mol),
        "heavy_atom_count": mol.GetNumHeavyAtoms(),
        "logp": Crippen.MolLogP(mol),
        "tpsa": Descriptors.TPSA(mol),
        "h_bond_donors": Lipinski.NumHDonors(mol),
        "h_bond_acceptors": Lipinski.NumHAcceptors(mol),
        "rotatable_bonds": Descriptors.NumRotatableBonds(mol),
        "aromatic_rings": rdMolDescriptors.CalcNumAromaticRings(mol),
        "aliphatic_rings": rdMolDescriptors.CalcNumAliphaticRings(mol),
        "rings_total": mol.GetRingInfo().NumRings(),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "formal_charge": Chem.GetFormalCharge(mol),
        "lipinski_violations": _lipinski_violations(mol),
    }


def _lipinski_violations(mol: Chem.Mol) -> int:
    v = 0
    if Descriptors.MolWt(mol) > 500:
        v += 1
    if Crippen.MolLogP(mol) > 5:
        v += 1
    if Lipinski.NumHDonors(mol) > 5:
        v += 1
    if Lipinski.NumHAcceptors(mol) > 10:
        v += 1
    return v
