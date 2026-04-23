"""Conformer generation and optimisation."""
from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import AllChem

from orgchem.messaging.errors import ConformerGenerationError


def embed_3d(mol: Chem.Mol, num_confs: int = 1, seed: int = 0xF00D,
             optimise: bool = True) -> Chem.Mol:
    """Add hydrogens, embed *num_confs* conformers, and optionally MMFF-optimise."""
    mol = Chem.AddHs(mol)
    if num_confs == 1:
        if AllChem.EmbedMolecule(mol, randomSeed=seed) != 0:
            raise ConformerGenerationError("EmbedMolecule returned non-zero status")
    else:
        ids = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs, randomSeed=seed)
        if not ids:
            raise ConformerGenerationError("EmbedMultipleConfs produced no conformers")
    if optimise:
        try:
            if num_confs == 1:
                AllChem.MMFFOptimizeMolecule(mol)
            else:
                AllChem.MMFFOptimizeMoleculeConfs(mol)
        except Exception:
            pass  # best-effort — report a valid conformer even if optimisation fails
    return mol
