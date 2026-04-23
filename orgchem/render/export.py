"""Higher-level molecule / reaction image export.

File extension determines the format:
- ``.png``, ``.jpg`` → raster via Pillow (RDKit ``MolToImage``)
- ``.svg``           → RDKit vector drawing
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Union

from rdkit import Chem

from orgchem.render.draw2d import render_svg, render_png_bytes
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


def export_molecule_2d(mol: Chem.Mol, path: Union[str, Path],
                       width: int = 600, height: int = 600) -> Path:
    """Export a 2D molecule drawing. Format chosen by *path*'s extension."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    ext = p.suffix.lower()
    if ext == ".svg":
        p.write_text(render_svg(mol, width=width, height=height))
    elif ext in (".png", ".jpg", ".jpeg"):
        p.write_bytes(render_png_bytes(mol, width=width, height=height))
    else:
        raise RenderError(
            f"Unsupported image extension: {ext!r}. Use .png, .jpg, or .svg."
        )
    log.info("Exported 2D molecule → %s (%d bytes)", p, p.stat().st_size)
    return p
