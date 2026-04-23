"""High-level Molecule wrapper around an ``rdkit.Chem.Mol`` with bookkeeping."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

from orgchem.core.formats import (
    mol_from_smiles, mol_to_smiles, mol_to_inchi, mol_to_inchikey,
    molecular_formula,
)
from orgchem.messaging.errors import ConformerGenerationError


@dataclass
class Molecule:
    name: str
    smiles: str
    inchi: Optional[str] = None
    inchikey: Optional[str] = None
    formula: Optional[str] = None
    molblock_2d: Optional[str] = None
    molblock_3d: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    source: Optional[str] = None
    db_id: Optional[int] = None

    _rdkit_mol: Optional[Chem.Mol] = field(default=None, repr=False)

    @classmethod
    def from_smiles(cls, smiles: str, name: str = "", generate_3d: bool = True) -> "Molecule":
        mol = mol_from_smiles(smiles)
        m = cls(
            name=name or smiles,
            smiles=mol_to_smiles(mol),
            inchi=mol_to_inchi(mol),
            inchikey=mol_to_inchikey(mol),
            formula=molecular_formula(mol),
        )
        m._rdkit_mol = mol
        if generate_3d:
            try:
                m.generate_3d()
            except ConformerGenerationError:
                pass  # allow 2D-only molecules to persist
        return m

    def rdkit_mol(self) -> Chem.Mol:
        if self._rdkit_mol is None:
            self._rdkit_mol = mol_from_smiles(self.smiles)
        return self._rdkit_mol

    def generate_2d(self) -> str:
        """Compute and cache a canonical 2D depiction (MolBlock).

        Used by Phase 6f: the same layout is then reused anywhere the
        molecule is drawn, so it looks identical in the Molecule
        Workspace, a reaction scheme, a pathway step, etc.
        """
        from rdkit.Chem import rdDepictor
        mol = Chem.Mol(self.rdkit_mol())
        rdDepictor.Compute2DCoords(mol)
        # Normalize with RDKit's new coord-generation layout for nicer rings
        try:
            rdDepictor.SetPreferCoordGen(True)
            rdDepictor.Compute2DCoords(mol)
        except Exception:
            pass
        self.molblock_2d = Chem.MolToMolBlock(mol)
        return self.molblock_2d

    def generate_3d(self, seed: int = 0xF00D) -> None:
        mol = Chem.AddHs(self.rdkit_mol())
        if AllChem.EmbedMolecule(mol, randomSeed=seed) != 0:
            raise ConformerGenerationError(f"EmbedMolecule failed for {self.smiles}")
        try:
            AllChem.MMFFOptimizeMolecule(mol)
        except Exception:
            pass  # optimisation is best-effort; still have a valid conformer
        self.molblock_3d = Chem.MolToMolBlock(mol)

    def ensure_properties(self) -> None:
        mol = self.rdkit_mol()
        p = self.properties
        p.setdefault("mol_weight", Descriptors.MolWt(mol))
        p.setdefault("exact_mass", Descriptors.ExactMolWt(mol))
        p.setdefault("logp", Descriptors.MolLogP(mol))
        p.setdefault("tpsa", Descriptors.TPSA(mol))
        p.setdefault("num_h_donors", Descriptors.NumHDonors(mol))
        p.setdefault("num_h_acceptors", Descriptors.NumHAcceptors(mol))
        p.setdefault("num_rotatable_bonds", Descriptors.NumRotatableBonds(mol))
        p.setdefault("num_rings", mol.GetRingInfo().NumRings())
        p.setdefault("num_atoms", mol.GetNumAtoms())
        p.setdefault("num_heavy_atoms", mol.GetNumHeavyAtoms())
