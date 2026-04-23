"""2D structure rendering via RDKit → SVG / PNG bytes.

Kept backend-agnostic so the viewer panel can embed the output in a
``QSvgWidget`` (SVG) or a ``QLabel`` pixmap (PNG).
"""
from __future__ import annotations
import io
from typing import Iterable, Optional

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D, MolToImage


def render_svg(mol: Chem.Mol, width: int = 400, height: int = 400,
               highlight_atoms: Optional[Iterable[int]] = None,
               show_atom_indices: bool = False,
               show_stereo_labels: bool = False,
               use_db_coords: bool = True) -> str:
    """Render *mol* as a self-contained SVG string.

    ``show_stereo_labels=True`` overlays CIP R/S descriptors on each
    stereocentre and E/Z descriptors on each stereodefined double bond,
    using RDKit's ``atomNote`` / ``bondNote`` draw hooks. Wedge / dash
    bonds are always drawn when the SMILES has stereochemistry encoded.

    With ``use_db_coords=True`` (default, Phase 6f) the molecule is first
    routed through :func:`core.fragment_resolver.resolve` so a DB match
    reuses the cached 2D coords — the Molecule Workspace, Compare tab,
    and reaction / pathway schemes all converge on the same layout.
    """
    m = mol
    if use_db_coords:
        try:
            from orgchem.core.fragment_resolver import resolve
            smi = Chem.MolToSmiles(mol)
            r = resolve(smi)
            if r is not None and r.mol is not None and \
                    r.mol.GetNumConformers() > 0:
                m = r.mol
        except Exception:
            pass
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    opts = drawer.drawOptions()
    opts.addAtomIndices = show_atom_indices
    opts.bondLineWidth = 2
    if show_stereo_labels:
        # Use RDKit's built-in CIP + E/Z annotation — requires the mol to have
        # stereo assigned beforehand so we force it on a copy.
        m = Chem.Mol(m)
        Chem.AssignStereochemistry(m, cleanIt=True, force=True)
        opts.addStereoAnnotation = True
    drawer.DrawMolecule(m, highlightAtoms=list(highlight_atoms or []))
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def render_png_bytes(mol: Chem.Mol, width: int = 400, height: int = 400) -> bytes:
    """Render *mol* as PNG bytes (via Pillow)."""
    img = MolToImage(mol, size=(width, height))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
