"""Agent actions for Phase 10a — conformational dynamics.

All three actions produce multi-frame XYZ that feeds the Phase 2c.2
3Dmol.js trajectory player — no new viewer code needed.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="dynamics")
def run_dihedral_scan_demo(demo: str, path: str = "",
                           n_frames: int = 36) -> Dict[str, Any]:
    """Run a pre-wired dihedral-scan demo and (optionally) write HTML.

    demo: 'butane' (C-C-C-C), 'ethane' (H-C-C-H), or 'cyclohexane'
    (full chair ↔ chair morph via conformer ensemble, *n_frames* ignored).
    """
    from orgchem.core.dynamics import (
        butane_dihedral_scan, ethane_dihedral_scan,
        cyclohexane_ring_flip, frames_to_xyz,
    )
    from orgchem.render.draw_reaction_3d import build_trajectory_html

    demo = demo.lower().strip()
    if demo == "butane":
        r = butane_dihedral_scan(n_frames=n_frames)
    elif demo == "ethane":
        r = ethane_dihedral_scan(n_frames=n_frames)
    elif demo == "cyclohexane":
        r = cyclohexane_ring_flip()
    else:
        return {"error": f"Unknown demo {demo!r}. "
                         "Try 'butane', 'ethane', or 'cyclohexane'."}
    xyz = frames_to_xyz(r)
    html = build_trajectory_html(xyz, title=f"{demo.title()} — {r.label}")
    out: Dict[str, Any] = {"demo": demo, "frames": len(r.frames),
                           "label": r.label}
    if path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html)
        out["path"] = str(p)
        out["size_bytes"] = p.stat().st_size
    return out


@action(category="dynamics")
def run_molecule_dihedral(molecule_id: int,
                          atom_a: int, atom_b: int, atom_c: int, atom_d: int,
                          path: str, n_frames: int = 36) -> Dict[str, Any]:
    """Scan a named dihedral of a DB molecule and export an HTML player.

    ``atom_a`` … ``atom_d`` are 0-based RDKit atom indices defining the
    torsion (same semantics as `rdkit.Chem.rdMolTransforms.SetDihedralDeg`).
    """
    from orgchem.core.dynamics import (
        run_dihedral_scan, frames_to_xyz, embed_from_smiles,
    )
    from orgchem.render.draw_reaction_3d import build_trajectory_html
    from orgchem.db.queries import get_molecule

    row = get_molecule(molecule_id)
    if row is None:
        return {"error": f"No molecule id {molecule_id}"}
    mol = embed_from_smiles(row.smiles)
    try:
        r = run_dihedral_scan(mol, dihedral_atoms=(atom_a, atom_b, atom_c, atom_d),
                              n_frames=n_frames)
    except Exception as e:  # noqa: BLE001
        return {"error": f"Dihedral scan failed: {e}"}
    xyz = frames_to_xyz(r)
    html = build_trajectory_html(xyz, title=f"{row.name} — {r.label}")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    return {"name": row.name, "frames": len(r.frames), "path": str(p),
            "size_bytes": p.stat().st_size}


@action(category="dynamics")
def run_molecule_conformer_morph(molecule_id: int, path: str,
                                 n_conformers: int = 8) -> Dict[str, Any]:
    """Produce a conformer-morph trajectory for any DB molecule."""
    from orgchem.core.dynamics import (
        run_conformer_morph, frames_to_xyz, embed_from_smiles,
    )
    from orgchem.render.draw_reaction_3d import build_trajectory_html
    from orgchem.db.queries import get_molecule

    row = get_molecule(molecule_id)
    if row is None:
        return {"error": f"No molecule id {molecule_id}"}
    mol = embed_from_smiles(row.smiles)
    try:
        r = run_conformer_morph(mol, n_conformers=n_conformers)
    except Exception as e:  # noqa: BLE001
        return {"error": f"Conformer morph failed: {e}"}
    xyz = frames_to_xyz(r)
    html = build_trajectory_html(xyz, title=f"{row.name} — {r.label}")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    return {"name": row.name, "frames": len(r.frames), "path": str(p),
            "size_bytes": p.stat().st_size}
