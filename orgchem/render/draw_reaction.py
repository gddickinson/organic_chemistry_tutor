"""High-quality 2D reaction rendering via RDKit.

Uses ``rdMolDraw2D.MolDraw2DSVG.DrawReaction`` — the latest RDKit rendering
path, which lays out reactant → arrow → product(s) horizontally with
coloured atom highlights and supports conditions / catalysts above the arrow.

Accepts reaction SMILES (``A.B>>C.D``) or reaction SMARTS with atom mapping
(``[C:1]=[O:2]>>[C:1]([H])[O:2][H]``).
"""
from __future__ import annotations
import io
import logging
from pathlib import Path
from typing import Optional, Union

from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D

from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


def parse_reaction(reaction_smiles: str):
    """Parse a reaction SMILES / SMARTS, raising :class:`RenderError` on failure."""
    try:
        rxn = AllChem.ReactionFromSmarts(reaction_smiles, useSmiles=True)
    except Exception as e:  # RDKit raises ValueError for malformed input
        raise RenderError(f"Could not parse reaction {reaction_smiles!r}: {e}") from e
    if rxn is None:
        # Fallback to SMARTS interpretation for mapped SMARTS strings.
        try:
            rxn = AllChem.ReactionFromSmarts(reaction_smiles)
        except Exception as e:
            raise RenderError(f"Could not parse reaction {reaction_smiles!r}: {e}") from e
    if rxn is None:
        raise RenderError(f"Could not parse reaction: {reaction_smiles!r}")
    return rxn


def _normalize_reaction_smiles(reaction_smiles: str) -> str:
    """Phase 6f.1: route every fragment through the DB so reactions use
    the same canonical SMILES / 2D layout students saw in the Molecule
    Workspace. Silently falls back to the input when the DB is not
    available (e.g. in pure-core unit tests).
    """
    try:
        from orgchem.core.fragment_resolver import canonical_reaction_smiles
        normalized = canonical_reaction_smiles(reaction_smiles)
        return normalized or reaction_smiles
    except Exception as e:
        log.debug("Reaction normalisation skipped (%s)", e)
        return reaction_smiles


def render_svg(reaction_smiles: str, width: int = 1200, height: int = 360,
               highlight_by_reactant: bool = True,
               use_db_coords: bool = True) -> str:
    """Render a reaction to an SVG string.

    With ``use_db_coords=True`` (default) every fragment is passed
    through the Phase 6f resolver: fragments present in the molecule DB
    use the DB's canonical SMILES, producing deterministic layouts that
    match what the Molecule Workspace would show.
    """
    src = _normalize_reaction_smiles(reaction_smiles) if use_db_coords \
        else reaction_smiles
    rxn = parse_reaction(src)
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    opts = drawer.drawOptions()
    opts.bondLineWidth = 2
    opts.padding = 0.08
    drawer.DrawReaction(rxn, highlightByReactant=highlight_by_reactant)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def render_png_bytes(reaction_smiles: str, width: int = 1200, height: int = 360) -> bytes:
    """Render a reaction to PNG bytes using RDKit's PIL-based ReactionToImage."""
    from rdkit.Chem.Draw import ReactionToImage
    rxn = parse_reaction(reaction_smiles)
    # Derive subimage size from the total requested height (reactions render
    # as a row of boxes roughly ``height × height`` each).
    sub = (max(200, height), max(200, height))
    img = ReactionToImage(rxn, subImgSize=sub)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def export_reaction(reaction_smiles: str, path: Union[str, Path],
                    width: int = 1200, height: int = 360,
                    highlight_by_reactant: bool = True) -> Path:
    """Write a reaction drawing to *path* — extension picks SVG or PNG."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    ext = p.suffix.lower()
    if ext == ".svg":
        p.write_text(render_svg(reaction_smiles, width, height,
                                highlight_by_reactant=highlight_by_reactant))
    elif ext in (".png", ".jpg", ".jpeg"):
        p.write_bytes(render_png_bytes(reaction_smiles, width, height))
    else:
        raise RenderError(f"Unsupported image extension: {ext!r}")
    log.info("Exported reaction → %s (%d bytes)", p, p.stat().st_size)
    return p
