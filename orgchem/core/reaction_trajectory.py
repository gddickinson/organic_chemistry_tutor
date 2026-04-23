"""Reaction trajectory builder (Phase 2c.2).

Given an atom-mapped reaction SMARTS, this module:

1. Embeds 3D coordinates for the reactant and the product separately.
2. Extracts the sub-set of atoms that carry an atom-map number — these are
   "trackable" across the arrow because the map tells us which product
   atom corresponds to which reactant atom.
3. Kabsch-aligns the product coords onto the reactant coords (minimises
   RMSD of the shared atoms), so the trajectory shows atoms *moving*
   rather than teleporting between unrelated orientations.
4. Linearly interpolates atom positions over *N* frames.
5. Emits a multi-frame XYZ string suitable for 3Dmol.js'
   ``addModelsAsFrames`` + ``animate()`` — bonds are inferred by
   proximity at each frame, so bonds appear / disappear *as the atoms
   move*, which is exactly what a student needs to see.

Pure RDKit + NumPy — no GUI dependencies, easy to test headlessly.
"""
from __future__ import annotations
import logging
from typing import Dict, List, Tuple

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


def build_xyz_trajectory(mapped_smarts: str, n_frames: int = 20,
                         seed: int = 0xF00D) -> str:
    """Build a multi-frame XYZ string morphing reactant → product.

    Only atoms that carry an atom-map number in *mapped_smarts* are
    included in the trajectory. Map numbers set the atom correspondence
    across the arrow. Frames are interpolated uniformly from 0 (pure
    reactant) to 1 (pure product-after-Kabsch-alignment).
    """
    if n_frames < 2:
        raise ValueError("n_frames must be >= 2")

    rxn = AllChem.ReactionFromSmarts(mapped_smarts, useSmiles=True)
    if rxn is None:
        raise RenderError(f"Could not parse reaction: {mapped_smarts!r}")

    reactant = _embed_combined(
        [rxn.GetReactantTemplate(i) for i in range(rxn.GetNumReactantTemplates())],
        seed=seed,
    )
    product = _embed_combined(
        [rxn.GetProductTemplate(i) for i in range(rxn.GetNumProductTemplates())],
        seed=seed + 1,
    )

    r_map = _mapped_atoms(reactant)
    p_map = _mapped_atoms(product)

    common = set(r_map) & set(p_map)
    if not common:
        raise RenderError(
            "Reactant and product share no atom-map numbers — "
            "cannot build a trajectory."
        )
    keys = sorted(common)
    r_coords = np.array([r_map[k][1] for k in keys])
    p_coords = np.array([p_map[k][1] for k in keys])
    symbols = [r_map[k][0] for k in keys]

    p_aligned = kabsch_align(p_coords, r_coords)

    # Linear interpolate — easy v1. A later polish could use MMFF-relaxed
    # waypoints or a simple NEB-like interpolator.
    frames: List[np.ndarray] = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        frames.append(r_coords * (1 - t) + p_aligned * t)

    return _format_xyz(symbols, frames)


# ------------------------------------------------------------------ helpers

def _embed_combined(templates: List[Chem.Mol], seed: int) -> Chem.Mol:
    """Combine disconnected fragments, sanitize partially, embed 3D."""
    if not templates:
        raise RenderError("No templates to embed")
    combined = templates[0]
    for m in templates[1:]:
        combined = Chem.CombineMols(combined, m)
    rw = Chem.RWMol(combined)
    try:
        Chem.SanitizeMol(rw)
    except Exception:
        # Reaction templates often violate strict valence rules because
        # they represent mechanism fragments; sanitise what we can.
        Chem.SanitizeMol(rw, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL
                         ^ Chem.SanitizeFlags.SANITIZE_PROPERTIES)
    mol = rw.GetMol()
    if AllChem.EmbedMolecule(mol, randomSeed=seed) != 0:
        if AllChem.EmbedMolecule(mol, randomSeed=seed + 17) != 0:
            raise RenderError("3D embedding failed")
    try:
        AllChem.MMFFOptimizeMolecule(mol)
    except Exception:
        pass
    return mol


def _mapped_atoms(mol: Chem.Mol) -> Dict[int, Tuple[str, Tuple[float, float, float]]]:
    """Return {map_number: (symbol, (x,y,z))}."""
    conf = mol.GetConformer()
    out: Dict[int, Tuple[str, Tuple[float, float, float]]] = {}
    for atom in mol.GetAtoms():
        mn = atom.GetAtomMapNum()
        if mn:
            p = conf.GetAtomPosition(atom.GetIdx())
            out[mn] = (atom.GetSymbol(), (p.x, p.y, p.z))
    return out


def kabsch_align(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Return *source* rotated & translated onto *target* (minimum RMSD)."""
    assert source.shape == target.shape, "Point sets must have same shape"
    src_c = source - source.mean(axis=0)
    tgt_c = target - target.mean(axis=0)
    H = src_c.T @ tgt_c
    U, _S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    return (src_c @ R.T) + target.mean(axis=0)


def _format_xyz(symbols: List[str], frames: List[np.ndarray]) -> str:
    """Render a multi-frame XYZ string."""
    n = len(symbols)
    lines: List[str] = []
    for idx, frame in enumerate(frames):
        lines.append(str(n))
        lines.append(f"frame {idx + 1}/{len(frames)}")
        for sym, pos in zip(symbols, frame):
            lines.append(f"{sym} {pos[0]:.4f} {pos[1]:.4f} {pos[2]:.4f}")
    return "\n".join(lines) + "\n"
