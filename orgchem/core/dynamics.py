"""Conformational dynamics — "MD for teaching" (Phase 10a).

Rather than implementing a full stochastic MD integrator, this module
generates the *pedagogical* trajectories that organic-chem teaching
actually needs:

- **Dihedral rotation scans** — spin a named 4-atom torsion from 0° to
  360° in small steps, relaxing everything else with MMFF at each
  angle. Used for butane gauche/anti, ethane torsion, any rotatable-bond
  demo.
- **Conformer-ensemble morphs** — embed *N* MMFF-diverse conformers
  (via RDKit's ETKDG) and interpolate between them. Used for
  cyclohexane chair ↔ twist-boat ↔ chair ring flips and similar.

Both paths produce a :class:`DynamicsResult` identical in shape to what
a real MD integrator would emit — a list of ``(n_atoms, 3)`` coord
arrays plus per-atom element symbols. The output is compatible with
``build_trajectory_html`` from :mod:`orgchem.render.draw_reaction_3d`,
so the existing 3Dmol.js player handles playback.

The Phase 10b OpenMM path (real Langevin / Verlet MD) is deferred — the
teaching-scale demos covered here reproduce the visual behaviour
students care about without needing a proper integrator.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolTransforms

from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


@dataclass
class DynamicsResult:
    frames: List[np.ndarray]        # each (n_atoms, 3), Å
    symbols: List[str]              # one symbol per atom
    label: str = ""                 # freeform, used as XYZ comment
    frame_labels: Optional[List[str]] = None


# ---- Dihedral scan -------------------------------------------------------

def run_dihedral_scan(mol: Chem.Mol, *,
                      dihedral_atoms: Tuple[int, int, int, int],
                      n_frames: int = 36,
                      minimise_each: bool = True,
                      start_deg: float = 0.0) -> DynamicsResult:
    """Rotate a named 4-atom dihedral from ``start_deg`` to ``start_deg + 360``
    in *n_frames* steps, relaxing the rest of the molecule at each step.

    *mol* must already have a 3D conformer and (preferably) explicit Hs.
    ``dihedral_atoms`` is the tuple of RDKit atom indices that defines the
    torsion — use :func:`rdkit.Chem.rdMolTransforms.SetDihedralDeg`
    semantics.
    """
    if mol.GetNumConformers() == 0:
        raise RenderError("Molecule has no 3D conformer")
    if len(dihedral_atoms) != 4 or len(set(dihedral_atoms)) != 4:
        raise RenderError("dihedral_atoms must be four distinct atom indices")

    mol = Chem.Mol(mol)   # defensive copy; the scan mutates the conformer
    conf = mol.GetConformer()
    a, b, c, d = dihedral_atoms

    mp = AllChem.MMFFGetMoleculeProperties(mol)
    ff = AllChem.MMFFGetMoleculeForceField(mol, mp) if mp else None
    if ff is None and minimise_each:
        log.warning("MMFF unavailable — running scan without relaxation")
        minimise_each = False

    frames: List[np.ndarray] = []
    frame_labels: List[str] = []
    angles = np.linspace(start_deg, start_deg + 360.0, n_frames, endpoint=False)

    for theta in angles:
        rdMolTransforms.SetDihedralDeg(conf, a, b, c, d, float(theta))
        if minimise_each:
            # Re-fetch FF because topology is the same but we want a fresh
            # force field keyed to the new coordinates.
            ff2 = AllChem.MMFFGetMoleculeForceField(mol, mp)
            # Constrain the dihedral so minimisation doesn't snap back.
            ff2.MMFFAddTorsionConstraint(a, b, c, d, False,
                                         float(theta), float(theta), 1.0e5)
            ff2.Minimize(maxIts=200)
        xyz = np.array([
            [conf.GetAtomPosition(i).x,
             conf.GetAtomPosition(i).y,
             conf.GetAtomPosition(i).z]
            for i in range(mol.GetNumAtoms())
        ])
        frames.append(xyz)
        frame_labels.append(f"θ = {theta:.0f}°")

    log.info("Dihedral scan: %d frames, angle %.0f→%.0f°",
             len(frames), start_deg, start_deg + 360.0)
    return DynamicsResult(
        frames=frames,
        symbols=[a.GetSymbol() for a in mol.GetAtoms()],
        label=f"Dihedral {a}-{b}-{c}-{d} scan",
        frame_labels=frame_labels,
    )


# ---- Conformer-ensemble morph --------------------------------------------

def run_conformer_morph(mol: Chem.Mol, *,
                        n_conformers: int = 10,
                        n_interp_frames: int = 6,
                        seed: int = 0xF00D) -> DynamicsResult:
    """Embed *n_conformers* diverse conformers, sort by MMFF energy, and
    produce a trajectory that interpolates between neighbouring
    conformers with *n_interp_frames* linear steps each.

    Used for ring-flip demos where a dihedral-scan isn't enough.
    """
    mol = Chem.Mol(mol)
    if mol.GetNumAtoms() < 3:
        raise RenderError("Need at least 3 atoms for a morph")

    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    ids = AllChem.EmbedMultipleConfs(mol, numConfs=n_conformers, params=params)
    if not ids:
        raise RenderError("EmbedMultipleConfs produced no conformers")

    # Rank by MMFF energy
    energies: List[Tuple[int, float]] = []
    for cid in ids:
        mp = AllChem.MMFFGetMoleculeProperties(mol)
        ff = AllChem.MMFFGetMoleculeForceField(mol, mp, confId=int(cid))
        if ff is None:
            continue
        ff.Minimize(maxIts=200)
        energies.append((int(cid), ff.CalcEnergy()))
    if not energies:
        raise RenderError("No MMFF-optimised conformers available")
    energies.sort(key=lambda t: t[1])

    # Align the sorted conformers onto the first to reduce overall drift.
    ref_id = energies[0][0]
    for cid, _e in energies[1:]:
        AllChem.AlignMol(mol, mol, atomMap=list(zip(
            range(mol.GetNumAtoms()), range(mol.GetNumAtoms()))),
            prbCid=cid, refCid=ref_id)

    # Extract coords for the sorted list.
    conf_coords: List[np.ndarray] = []
    for cid, _e in energies:
        c = mol.GetConformer(int(cid))
        conf_coords.append(np.array([
            [c.GetAtomPosition(i).x, c.GetAtomPosition(i).y,
             c.GetAtomPosition(i).z]
            for i in range(mol.GetNumAtoms())
        ]))

    frames: List[np.ndarray] = []
    for a, b in zip(conf_coords[:-1], conf_coords[1:]):
        for k in range(n_interp_frames):
            t = k / n_interp_frames
            frames.append(a * (1 - t) + b * t)
    frames.append(conf_coords[-1])

    log.info("Conformer morph: %d conformers → %d frames",
             len(energies), len(frames))
    return DynamicsResult(
        frames=frames,
        symbols=[a.GetSymbol() for a in mol.GetAtoms()],
        label=f"Conformer morph ({len(energies)} conformers)",
    )


# ---- XYZ export ----------------------------------------------------------

def frames_to_xyz(result: DynamicsResult) -> str:
    """Render a :class:`DynamicsResult` as a multi-frame XYZ string."""
    n = len(result.symbols)
    out: List[str] = []
    for idx, frame in enumerate(result.frames):
        out.append(str(n))
        lbl = ""
        if result.frame_labels and idx < len(result.frame_labels):
            lbl = "  " + result.frame_labels[idx]
        out.append(f"frame {idx + 1}/{len(result.frames)}{lbl}")
        for sym, pos in zip(result.symbols, frame):
            out.append(f"{sym} {pos[0]:.4f} {pos[1]:.4f} {pos[2]:.4f}")
    return "\n".join(out) + "\n"


# ---- Convenience: from SMILES -------------------------------------------

def embed_from_smiles(smiles: str, seed: int = 0xF00D) -> Chem.Mol:
    """SMILES → 3D-embedded Mol (with Hs)."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise RenderError(f"Invalid SMILES: {smiles!r}")
    mol = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mol, randomSeed=seed) != 0:
        raise RenderError(f"Could not embed {smiles!r} in 3D")
    AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
    return mol


def butane_dihedral_scan(n_frames: int = 36) -> DynamicsResult:
    """Pre-wired demo: CH₃-CH₂-CH₂-CH₃ central dihedral rotation."""
    mol = embed_from_smiles("CCCC")
    # For 'CCCC', the four C's are atoms 0, 1, 2, 3 in SMILES order.
    return run_dihedral_scan(mol, dihedral_atoms=(0, 1, 2, 3), n_frames=n_frames)


def ethane_dihedral_scan(n_frames: int = 24) -> DynamicsResult:
    """Pre-wired demo: H-C-C-H torsion for ethane."""
    mol = embed_from_smiles("CC")
    # Find the first H on each C.
    c1 = 0
    c2 = 1
    h1 = next(a.GetIdx() for a in mol.GetAtomWithIdx(c1).GetNeighbors()
              if a.GetSymbol() == "H")
    h2 = next(a.GetIdx() for a in mol.GetAtomWithIdx(c2).GetNeighbors()
              if a.GetSymbol() == "H")
    return run_dihedral_scan(mol, dihedral_atoms=(h1, c1, c2, h2),
                             n_frames=n_frames)


def cyclohexane_ring_flip(n_interp: int = 10) -> DynamicsResult:
    """Pre-wired demo: cyclohexane chair ↔ chair morph via conformer ensemble."""
    mol = embed_from_smiles("C1CCCCC1")
    return run_conformer_morph(mol, n_conformers=8, n_interp_frames=n_interp)
