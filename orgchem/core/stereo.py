"""Stereochemistry helpers — cross-cutting per the 2026-04-22 roadmap note.

Stereochemistry is not a standalone topic in this app — it shows up in
every reaction, every mechanism, every synthesis route. This module is the
canonical API other modules call when they need to:

- Assign R/S to tetrahedral stereocentres.
- Assign E/Z to double bonds.
- Flip a single stereocentre.
- Compute the enantiomer of a whole molecule.

All functions take either an RDKit ``Mol`` or a SMILES string. Returns are
Python-native (strings, ints, dicts) so callers outside ``core/`` don't
need to know about RDKit types.
"""
from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Any, Dict, List, Optional, Union

from rdkit import Chem

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------

@dataclass
class StereoDescriptor:
    """One stereocentre or double-bond descriptor."""
    kind: str                 # "R/S" or "E/Z"
    value: str                # "R", "S", "E", "Z", or ""
    atom_indices: List[int]   # single atom for R/S, two atoms for E/Z


def _parse(mol_or_smiles: Union[Chem.Mol, str]) -> Chem.Mol:
    if isinstance(mol_or_smiles, str):
        m = Chem.MolFromSmiles(mol_or_smiles)
        if m is None:
            raise ValueError(f"Unparseable SMILES: {mol_or_smiles!r}")
        return m
    return mol_or_smiles


def assign_descriptors(mol_or_smiles: Union[Chem.Mol, str]) -> List[StereoDescriptor]:
    """Run CIP + E/Z analysis and return all stereodescriptors.

    The input is not mutated — stereodescriptors are computed on a copy.
    """
    src = _parse(mol_or_smiles)
    m = Chem.Mol(src)
    Chem.AssignStereochemistry(m, cleanIt=True, force=True)
    out: List[StereoDescriptor] = []
    for atom in m.GetAtoms():
        cip = atom.GetPropsAsDict().get("_CIPCode")
        if cip:
            out.append(StereoDescriptor(kind="R/S", value=str(cip),
                                        atom_indices=[atom.GetIdx()]))
    for bond in m.GetBonds():
        stereo = bond.GetStereo()
        label = ""
        if stereo == Chem.BondStereo.STEREOE:
            label = "E"
        elif stereo == Chem.BondStereo.STEREOZ:
            label = "Z"
        elif stereo == Chem.BondStereo.STEREOCIS:
            label = "Z"
        elif stereo == Chem.BondStereo.STEREOTRANS:
            label = "E"
        if label:
            out.append(StereoDescriptor(
                kind="E/Z", value=label,
                atom_indices=[bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()],
            ))
    return out


def assign_rs(mol_or_smiles: Union[Chem.Mol, str]) -> Dict[int, str]:
    """Map of atom index → CIP descriptor ('R' or 'S') for every stereocentre."""
    return {d.atom_indices[0]: d.value for d in assign_descriptors(mol_or_smiles)
            if d.kind == "R/S"}


def assign_ez(mol_or_smiles: Union[Chem.Mol, str]) -> Dict[tuple, str]:
    """Map of (atomA, atomB) → 'E' or 'Z' for every stereodefined double bond."""
    out: Dict[tuple, str] = {}
    for d in assign_descriptors(mol_or_smiles):
        if d.kind == "E/Z":
            a, b = sorted(d.atom_indices)
            out[(a, b)] = d.value
    return out


def stereocentre_atoms(mol_or_smiles: Union[Chem.Mol, str]) -> List[int]:
    """Atom indices of every tetrahedral stereocentre (assigned or unassigned)."""
    m = _parse(mol_or_smiles)
    centres = Chem.FindMolChiralCenters(m, includeUnassigned=True,
                                        useLegacyImplementation=False)
    return [idx for idx, _ in centres]


def flip_stereocentre(mol_or_smiles: Union[Chem.Mol, str],
                      atom_index: int) -> str:
    """Invert the chirality tag at one atom; return the new canonical SMILES.

    Raises ``ValueError`` if the atom is not a stereocentre.
    """
    src = _parse(mol_or_smiles)
    m = Chem.Mol(src)
    atom = m.GetAtomWithIdx(atom_index)
    tag = atom.GetChiralTag()
    if tag == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
        atom.SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CCW)
    elif tag == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
        atom.SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CW)
    else:
        raise ValueError(f"Atom {atom_index} is not a tetrahedral stereocentre")
    Chem.AssignStereochemistry(m, cleanIt=True, force=True)
    return Chem.MolToSmiles(m)


def enantiomer_of(mol_or_smiles: Union[Chem.Mol, str]) -> str:
    """Flip *all* stereocentres at once — returns canonical SMILES of the enantiomer.

    A molecule with no stereocentres round-trips to itself.
    """
    src = _parse(mol_or_smiles)
    m = Chem.Mol(src)
    for atom in m.GetAtoms():
        tag = atom.GetChiralTag()
        if tag == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
            atom.SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CCW)
        elif tag == Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
            atom.SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CW)
    Chem.AssignStereochemistry(m, cleanIt=True, force=True)
    return Chem.MolToSmiles(m)


def summarise(mol_or_smiles: Union[Chem.Mol, str]) -> Dict[str, Any]:
    """Human-readable roll-up of all stereo info for one molecule.

    Used by the agent-action layer and by the 2D renderer to draw CIP
    labels on the picture.
    """
    descriptors = assign_descriptors(mol_or_smiles)
    all_centres = stereocentre_atoms(mol_or_smiles)
    assigned = {d.atom_indices[0] for d in descriptors if d.kind == "R/S"}
    unassigned = [i for i in all_centres if i not in assigned]
    return {
        "rs": {d.atom_indices[0]: d.value for d in descriptors if d.kind == "R/S"},
        "ez": [{"atoms": d.atom_indices, "value": d.value}
               for d in descriptors if d.kind == "E/Z"],
        "unassigned_stereocentres": unassigned,
        "n_stereocentres": len(all_centres),
        "is_chiral": len(all_centres) > 0,
    }
