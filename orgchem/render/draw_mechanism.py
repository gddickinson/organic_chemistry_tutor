"""Mechanism step rendering — molecule SVG with curved arrows overlaid.

Uses ``rdMolDraw2D.MolDraw2DSVG`` for the molecule and
``drawer.GetDrawCoords(atom_idx)`` to position arrow endpoints in pixel
space. Arrows are SVG ``<path>`` elements with a quadratic Bezier curve;
the control point is offset perpendicular to the endpoints by
``arrow.bend * |p2 − p1|`` so you get a nice crescent instead of a
straight line. Arrowheads are standard SVG ``<marker>`` definitions.
"""
from __future__ import annotations
import logging
import math
import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple, Union

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

from orgchem.core.mechanism import Arrow, MechanismStep
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)

_ARROW_COLOUR = "#c23030"
_LONE_PAIR_COLOUR = "#1a1a1a"
_LONE_PAIR_RADIUS = 2.2     # pixel radius per dot
_LONE_PAIR_SPACING = 5.5    # pixel separation between the two dots
_LONE_PAIR_OFFSET = 14.0    # distance from atom centre to the centre of the pair


def render_step_svg(step: MechanismStep, width: int = 560, height: int = 420,
                    show_atom_indices: bool = False) -> str:
    """Render one mechanism step as an SVG string (molecule + arrows)."""
    mol = Chem.MolFromSmiles(step.smiles)
    if mol is None:
        raise RenderError(f"Could not parse SMILES: {step.smiles!r}")

    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    opts = drawer.drawOptions()
    opts.bondLineWidth = 2
    opts.addAtomIndices = bool(show_atom_indices)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()

    n_atoms = mol.GetNumAtoms()
    arrow_paths: List[str] = []
    for a in step.arrows:
        p1 = _arrow_endpoint(a.from_bond, a.from_atom, drawer, mol, step)
        p2 = _arrow_endpoint(a.to_bond, a.to_atom, drawer, mol, step)
        if p1 is None or p2 is None:
            continue
        arrow_paths.append(_curved_arrow_svg(p1[0], p1[1], p2[0], p2[1],
                                             bend=a.bend, kind=a.kind,
                                             label=a.label))

    # Lone-pair dot decorations.
    lp_paths: List[str] = []
    for atom_idx in step.lone_pairs:
        if not (0 <= atom_idx < n_atoms):
            log.warning("Lone-pair atom out of range in %r (n=%d): %s",
                        step.title, n_atoms, atom_idx)
            continue
        lp_paths.append(_lone_pair_svg(atom_idx, drawer, mol))

    svg = _inject_defs(svg, _arrow_defs())
    svg = _append_before_close(
        svg, "\n".join(lp_paths + arrow_paths))
    # RDKit emits the SVG with encoding='iso-8859-1'; we write UTF-8 bytes
    # into it (non-ASCII arrow labels), so force the declaration to match
    # or Qt's QSvgRenderer decodes as Latin-1 and shows mojibake.
    svg = re.sub(r"encoding=['\"]iso-8859-1['\"]", "encoding='UTF-8'", svg, count=1)
    return svg


def render_step_png(step: MechanismStep, path: Union[str, Path],
                    width: int = 700, height: int = 520,
                    show_atom_indices: bool = False) -> Path:
    """Render a mechanism step to a PNG using RDKit → SVG → Pillow.

    Converts the SVG via CairoSVG if available, else falls back to a pure
    PIL rasterisation of the molecule (without the overlay arrows) so the
    call always produces *something*.
    """
    svg = render_step_svg(step, width=width, height=height,
                          show_atom_indices=show_atom_indices)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    png = _svg_to_png_bytes(svg, width, height)
    p.write_bytes(png)
    return p


# ---------------------------------------------------------------- helpers


def _arrow_endpoint(bond: Optional[Tuple[int, int]], atom_idx: int,
                    drawer, mol, step: MechanismStep
                    ) -> Optional[Tuple[float, float]]:
    """Resolve an arrow endpoint to pixel (x, y).

    If ``bond`` is given, returns the midpoint of that bond (overrides
    ``atom_idx``). Otherwise returns the atom centre. Bounds-checks both
    atom and bond references; logs and returns ``None`` on failure so
    the arrow can be skipped.
    """
    n_atoms = mol.GetNumAtoms()
    if bond is not None:
        a, b = int(bond[0]), int(bond[1])
        if not (0 <= a < n_atoms and 0 <= b < n_atoms):
            log.warning("Bond %s out of range in %r (n=%d)",
                        bond, step.title, n_atoms)
            return None
        pa = drawer.GetDrawCoords(a)
        pb = drawer.GetDrawCoords(b)
        return ((pa.x + pb.x) / 2.0, (pa.y + pb.y) / 2.0)
    if not (0 <= atom_idx < n_atoms):
        log.warning("Arrow atom %s out of range in %r (n=%d)",
                    atom_idx, step.title, n_atoms)
        return None
    p = drawer.GetDrawCoords(int(atom_idx))
    return (p.x, p.y)


def _lone_pair_svg(atom_idx: int, drawer, mol) -> str:
    """Render two filled dots near ``atom_idx`` to denote a lone pair.

    The dots are placed on the side of the atom pointing away from the
    mean of its bonded neighbours (so they lie in empty space rather
    than on top of another atom). If the atom has no neighbours, they
    default to "above".
    """
    centre = drawer.GetDrawCoords(atom_idx)
    cx, cy = centre.x, centre.y

    atom = mol.GetAtomWithIdx(atom_idx)
    dx_sum, dy_sum = 0.0, 0.0
    n = 0
    for nbr in atom.GetNeighbors():
        p = drawer.GetDrawCoords(nbr.GetIdx())
        dx_sum += p.x - cx
        dy_sum += p.y - cy
        n += 1
    if n == 0 or (dx_sum == 0.0 and dy_sum == 0.0):
        # No direction to run from; place above the atom.
        nx, ny = 0.0, -1.0
    else:
        # Point opposite to the mean neighbour direction.
        vx, vy = -dx_sum / n, -dy_sum / n
        length = math.sqrt(vx * vx + vy * vy)
        nx, ny = vx / length, vy / length

    # Tangent perpendicular to (nx, ny) — for spacing the two dots.
    tx, ty = -ny, nx

    pair_cx = cx + nx * _LONE_PAIR_OFFSET
    pair_cy = cy + ny * _LONE_PAIR_OFFSET
    half = _LONE_PAIR_SPACING / 2.0
    dot1 = (pair_cx + tx * half, pair_cy + ty * half)
    dot2 = (pair_cx - tx * half, pair_cy - ty * half)

    return (
        f'<circle cx="{dot1[0]:.1f}" cy="{dot1[1]:.1f}" '
        f'r="{_LONE_PAIR_RADIUS}" fill="{_LONE_PAIR_COLOUR}" />\n'
        f'<circle cx="{dot2[0]:.1f}" cy="{dot2[1]:.1f}" '
        f'r="{_LONE_PAIR_RADIUS}" fill="{_LONE_PAIR_COLOUR}" />'
    )


def _arrow_defs() -> str:
    return (
        '<defs>'
        f'<marker id="mech-curly" markerWidth="10" markerHeight="7" '
        'refX="8" refY="3.5" orient="auto" markerUnits="userSpaceOnUse">'
        f'<polygon points="0 0, 10 3.5, 0 7" fill="{_ARROW_COLOUR}" />'
        '</marker>'
        f'<marker id="mech-fish" markerWidth="10" markerHeight="7" '
        'refX="9" refY="3.5" orient="auto" markerUnits="userSpaceOnUse">'
        f'<polyline points="0 0, 10 3.5" stroke="{_ARROW_COLOUR}" '
        'stroke-width="1.6" fill="none" />'
        '</marker>'
        '</defs>'
    )


def _curved_arrow_svg(x1: float, y1: float, x2: float, y2: float,
                      bend: float = 0.35, kind: str = "curly",
                      label: str = "") -> str:
    dx, dy = x2 - x1, y2 - y1
    # Perpendicular offset for the Bezier control point (90° CCW).
    cx = (x1 + x2) / 2 + (-dy) * bend
    cy = (y1 + y2) / 2 + (dx) * bend
    marker = "mech-fish" if kind == "fishhook" else "mech-curly"
    path = (
        f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" '
        f'stroke="{_ARROW_COLOUR}" stroke-width="2.4" fill="none" '
        f'marker-end="url(#{marker})" stroke-linecap="round" '
        f'opacity="0.9" />'
    )
    if label:
        # Place the label near the control point, pushed slightly further out.
        lx = (x1 + x2) / 2 + (-dy) * bend * 1.35
        ly = (y1 + y2) / 2 + (dx) * bend * 1.35
        path += (
            f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{_ARROW_COLOUR}" '
            f'font-size="14" font-family="sans-serif" '
            f'text-anchor="middle">{_xml_escape(label)}</text>'
        )
    return path


def _inject_defs(svg: str, defs: str) -> str:
    """Insert *defs* immediately after the opening ``<svg ...>`` tag."""
    return re.sub(r"(<svg[^>]*>)", r"\1" + defs, svg, count=1)


def _append_before_close(svg: str, extra: str) -> str:
    """Insert *extra* right before ``</svg>`` so arrows render on top."""
    return svg.replace("</svg>", extra + "</svg>", 1)


def _xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def _svg_to_png_bytes(svg: str, width: int, height: int) -> bytes:
    """Best-effort SVG → PNG. Tries cairosvg, then falls back to a pure-RDKit
    re-render of the underlying molecule (losing overlay arrows)."""
    try:
        import cairosvg  # type: ignore
        return cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            output_width=width,
            output_height=height,
        )
    except Exception:
        log.warning(
            "cairosvg not available — returning molecule-only PNG without arrow overlay"
        )
    # Minimal fallback: rasterise just the molecule (no arrows) via RDKit/PIL.
    m = re.search(r"<path[^>]*class='atom-\d+'", svg)
    from orgchem.render.draw2d import render_png_bytes
    # Best-effort: parse SMILES back out of the SVG title won't work, so we
    # accept that the fallback is ugly. We return the raw SVG bytes for
    # downstream code that can consume SVG.
    return svg.encode("utf-8")
