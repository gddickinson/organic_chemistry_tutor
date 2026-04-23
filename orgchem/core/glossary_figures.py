"""Glossary example-figure generator — Phase 26b (round 33).

Walks the ``_GLOSSARY`` seed list looking for terms that carry an
``example_smiles`` but no stored figure, and renders each one to
``data/glossary/<slug>.png`` via the Phase-4 / Phase-0 2D drawing
stack (or ``draw_reaction`` when the SMILES contains a ``>>``).

Kept headless and Qt-free so it runs in CI and under the autonomous
test suite.
"""
from __future__ import annotations
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

log = logging.getLogger(__name__)


#: Output directory for auto-generated figures. Relative to the
#: project root — lives alongside ``orgchem/`` rather than inside
#: the package so bundled data is easy to replace.
def default_figure_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "glossary"


_TERM_SLUG_RE = re.compile(r"[^A-Za-z0-9]+")


def term_slug(term: str) -> str:
    """Normalise a glossary term name into a safe filename stem."""
    slug = _TERM_SLUG_RE.sub("_", term.strip().lower()).strip("_")
    return slug or "term"


# ---------------------------------------------------------------------

@dataclass
class FigureResult:
    term: str
    path: Path
    rendered: bool
    skipped_reason: Optional[str] = None   # populated when rendered=False


def render_term(term: str, smiles: str,
                out_dir: Optional[Union[str, Path]] = None,
                force: bool = False,
                fmt: str = "png") -> FigureResult:
    """Render one term's example SMILES to ``out_dir/<slug>.<fmt>``.

    Returns a :class:`FigureResult`. ``force=False`` skips when the
    target file already exists (unchanged stem) so repeated regen
    runs are incremental. ``fmt`` is either ``"png"`` or ``"svg"``.
    """
    from orgchem.render import draw2d, draw_reaction
    d = Path(out_dir) if out_dir else default_figure_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{term_slug(term)}.{fmt}"

    if path.exists() and not force:
        return FigureResult(term=term, path=path, rendered=False,
                            skipped_reason="already exists")

    if not smiles or not smiles.strip():
        return FigureResult(term=term, path=path, rendered=False,
                            skipped_reason="no example_smiles")

    try:
        if ">>" in smiles:
            # Reaction scheme.
            if fmt == "svg":
                path.write_text(draw_reaction.render_svg(smiles),
                                encoding="utf-8")
            else:
                path.write_bytes(draw_reaction.render_png_bytes(smiles))
        else:
            # Single molecule.
            from rdkit import Chem
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return FigureResult(
                    term=term, path=path, rendered=False,
                    skipped_reason=f"invalid SMILES: {smiles!r}")
            if fmt == "svg":
                path.write_text(draw2d.render_svg(mol), encoding="utf-8")
            else:
                path.write_bytes(draw2d.render_png_bytes(mol))
    except Exception as e:  # noqa: BLE001
        return FigureResult(term=term, path=path, rendered=False,
                            skipped_reason=f"render failed: {e}")

    return FigureResult(term=term, path=path, rendered=True)


def regenerate_all(out_dir: Optional[Union[str, Path]] = None,
                   force: bool = False,
                   fmt: str = "png") -> List[FigureResult]:
    """Walk ``_GLOSSARY`` and render every term that has an
    ``example_smiles`` field. Returns one :class:`FigureResult` per
    candidate (including skips)."""
    from orgchem.db.seed_glossary import _GLOSSARY
    results: List[FigureResult] = []
    for entry in _GLOSSARY:
        smi = entry.get("example_smiles")
        if not smi:
            continue
        results.append(
            render_term(entry["term"], smi,
                        out_dir=out_dir, force=force, fmt=fmt)
        )
    log.info("Regen glossary figures: %d rendered, %d skipped",
             sum(1 for r in results if r.rendered),
             sum(1 for r in results if not r.rendered))
    return results


def figure_path_for(term: str,
                    out_dir: Optional[Union[str, Path]] = None,
                    fmt: str = "png") -> Path:
    """Return the conventional cache path for a term (may not exist)."""
    d = Path(out_dir) if out_dir else default_figure_dir()
    return d / f"{term_slug(term)}.{fmt}"
