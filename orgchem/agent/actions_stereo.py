"""Agent actions for stereochemistry — cross-cutting per 2026-04-22.

Wraps :mod:`orgchem.core.stereo` so LLMs / the stdio bridge can assign
descriptors, flip individual stereocentres, or compute the enantiomer of
a seeded molecule.
"""
from __future__ import annotations
import logging
from typing import Any, Dict

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="stereo")
def assign_stereodescriptors(smiles: str = "", molecule_id: int = 0) -> Dict[str, Any]:
    """Assign R/S + E/Z descriptors for a molecule, by SMILES or DB id.

    Returns {"rs": {atom_index: "R"|"S"}, "ez": [...],
             "unassigned_stereocentres": [...], "n_stereocentres": N,
             "is_chiral": bool, "smiles": <input>}.
    """
    from orgchem.core.stereo import summarise
    smi = smiles
    if not smi and molecule_id:
        from orgchem.db.session import session_scope
        from orgchem.db.models import Molecule as DBMol
        with session_scope() as s:
            row = s.get(DBMol, int(molecule_id))
            if row is None:
                return {"error": f"No molecule id {molecule_id}"}
            smi = row.smiles
    if not smi:
        return {"error": "Supply either smiles= or molecule_id="}
    try:
        summary = summarise(smi)
    except ValueError as e:
        return {"error": str(e)}
    return {"smiles": smi, **summary}


@action(category="stereo")
def flip_stereocentre(smiles: str, atom_index: int) -> Dict[str, Any]:
    """Invert the chirality tag at one atom; return new canonical SMILES."""
    from orgchem.core.stereo import flip_stereocentre as _flip, summarise
    try:
        new_smi = _flip(smiles, atom_index)
    except ValueError as e:
        return {"error": str(e)}
    return {"original_smiles": smiles, "new_smiles": new_smi,
            **summarise(new_smi)}


@action(category="stereo")
def enantiomer_of(smiles: str = "", molecule_id: int = 0) -> Dict[str, Any]:
    """Return the enantiomer's canonical SMILES (all stereocentres inverted)."""
    from orgchem.core.stereo import enantiomer_of as _ent, summarise
    smi = smiles
    if not smi and molecule_id:
        from orgchem.db.session import session_scope
        from orgchem.db.models import Molecule as DBMol
        with session_scope() as s:
            row = s.get(DBMol, int(molecule_id))
            if row is None:
                return {"error": f"No molecule id {molecule_id}"}
            smi = row.smiles
    if not smi:
        return {"error": "Supply either smiles= or molecule_id="}
    try:
        new_smi = _ent(smi)
    except ValueError as e:
        return {"error": str(e)}
    return {"original_smiles": smi, "enantiomer_smiles": new_smi,
            **summarise(new_smi)}


@action(category="stereo")
def export_molecule_2d_stereo(smiles: str, path: str,
                              width: int = 500, height: int = 400) -> Dict[str, Any]:
    """Render a molecule to 2D with CIP R/S and E/Z annotations + wedge bonds.

    Output format chosen by file extension: ``.svg`` or ``.png``.
    """
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    from pathlib import Path
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"error": f"Unparseable SMILES: {smiles!r}"}
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "svg"
    if suffix == "svg":
        d = rdMolDraw2D.MolDraw2DSVG(width, height)
        d.drawOptions().addStereoAnnotation = True
        d.drawOptions().bondLineWidth = 2
        d.DrawMolecule(mol)
        d.FinishDrawing()
        p.write_text(d.GetDrawingText())
    elif suffix == "png":
        d = rdMolDraw2D.MolDraw2DCairo(width, height)
        d.drawOptions().addStereoAnnotation = True
        d.drawOptions().bondLineWidth = 2
        d.DrawMolecule(mol)
        d.FinishDrawing()
        p.write_bytes(d.GetDrawingText())
    else:
        return {"error": f"Unsupported format {suffix!r}; use svg or png"}
    return {"path": str(p), "smiles": smiles, "format": suffix,
            "size_bytes": p.stat().st_size}
