"""Matplotlib 3D molecule renderer.

Backup / headless path for the 3D viewer: works everywhere matplotlib works,
needs no WebGL, produces real PNG images of molecules in any Qt platform
mode (including offscreen Chromium where 3Dmol.js fails).

Supported styles:
  - ``ball-and-stick``  atoms as spheres, bonds as lines (default)
  - ``sphere``          CPK-style space-filling
  - ``stick``           thick bond lines, small atom markers
  - ``line``            thin wireframe
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Union

import matplotlib
matplotlib.use("Agg")  # force non-interactive backend for headless safety
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from rdkit import Chem  # noqa: E402

from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


# CPK (Corey-Pauling-Koltun) colours for atoms.
_CPK: dict[str, str] = {
    "H":  "#F0F0F0", "C":  "#303030", "N":  "#3050F8", "O":  "#FF0D0D",
    "F":  "#90E050", "P":  "#FF8000", "S":  "#FFD600", "Cl": "#1FF01F",
    "Br": "#A62929", "I":  "#940094", "Na": "#AB5CF2", "Mg": "#8AFF00",
    "Ca": "#3DFF00", "Fe": "#E06633", "Zn": "#7D80B0", "Cu": "#C88033",
}
_DEFAULT_COLOUR = "#B0B0B0"

# Van-der-Waals radii (Å) for sphere style; covalent radii for ball-and-stick.
_VDW: dict[str, float] = {
    "H": 1.20, "C": 1.70, "N": 1.55, "O": 1.52, "F": 1.47, "P": 1.80,
    "S": 1.80, "Cl": 1.75, "Br": 1.85, "I": 1.98,
}
_COV: dict[str, float] = {
    "H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57, "P": 1.07,
    "S": 1.05, "Cl": 1.02, "Br": 1.20, "I": 1.39,
}


def render_png(mol: Chem.Mol, path: Union[str, Path],
               width: int = 800, height: int = 600,
               style: str = "ball-and-stick",
               background: str = "white",
               elev: float = 20.0, azim: float = -60.0) -> Path:
    """Render a 3D molecule to a PNG file.

    The molecule must have at least one 3D conformer. See
    :func:`orgchem.core.conformers.embed_3d`.
    """
    if mol.GetNumConformers() == 0:
        raise RenderError("Molecule has no 3D coordinates; call embed_3d first.")

    conf = mol.GetConformer()
    positions = np.array([
        [conf.GetAtomPosition(i).x,
         conf.GetAtomPosition(i).y,
         conf.GetAtomPosition(i).z]
        for i in range(mol.GetNumAtoms())
    ])

    fig = plt.figure(figsize=(width / 100, height / 100), dpi=100,
                     facecolor=background)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(background)

    _draw_bonds(ax, mol, positions, style)
    _draw_atoms(ax, mol, positions, style)

    _tidy_axes(ax, positions)
    ax.view_init(elev=elev, azim=azim)

    # Force the 3D axes to fill the figure — matplotlib's default leaves
    # ~40 % margin around a 3D Axes3D, which wastes the image.
    ax.set_position([0.0, 0.0, 1.0, 1.0])

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # bbox_inches="tight" crops to actual drawn content — with real spheres
    # (plot_surface) that's the molecule's bounding volume, giving proper
    # framing on any molecule size.
    fig.savefig(p, dpi=100, facecolor=background,
                bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    log.info("Rendered 3D → %s (%d bytes)", p, p.stat().st_size)
    return p


# ---- helpers --------------------------------------------------------------

def _scatter_size(symbol: str, style: str) -> float:
    """Return a scatter marker size in pts²."""
    if style == "sphere":
        return (_VDW.get(symbol, 1.5) * 180) ** 1.0
    if style == "ball-and-stick":
        return (_COV.get(symbol, 0.7) * 220) ** 1.0
    if style == "stick":
        return 40.0
    if style == "line":
        return 5.0
    return 100.0


def _bond_width(style: str, order: float) -> float:
    base = {"line": 0.8, "stick": 3.5, "ball-and-stick": 2.2, "sphere": 0.0}.get(style, 2.0)
    if order >= 2:
        base *= 1.4
    return base


def _draw_atoms(ax, mol: Chem.Mol, positions: np.ndarray, style: str) -> None:
    if style == "line":
        return  # pure wireframe, no markers
    if style in ("ball-and-stick", "sphere"):
        # Real shaded spheres via plot_surface — much closer to ball-and-stick
        # drawings in a textbook than flat scatter markers.
        for i, atom in enumerate(mol.GetAtoms()):
            symbol = atom.GetSymbol()
            colour = _CPK.get(symbol, _DEFAULT_COLOUR)
            if style == "sphere":
                radius = _VDW.get(symbol, 1.5) * 0.65
            else:
                radius = _COV.get(symbol, 0.7) * 0.55
            _plot_sphere(ax, positions[i], radius, colour)
        return
    # stick / fallback: small depth-shaded markers
    colours = [_CPK.get(atom.GetSymbol(), _DEFAULT_COLOUR) for atom in mol.GetAtoms()]
    sizes = [_scatter_size(atom.GetSymbol(), style) for atom in mol.GetAtoms()]
    ax.scatter(
        positions[:, 0], positions[:, 1], positions[:, 2],
        c=colours, s=sizes,
        edgecolors="black", linewidths=0.4,
        depthshade=True,
    )


def _plot_sphere(ax, centre: np.ndarray, radius: float, colour: str,
                 n_theta: int = 16, n_phi: int = 10) -> None:
    """Draw a single shaded sphere on *ax*. Low-poly (~150 quads) for speed."""
    theta = np.linspace(0.0, 2.0 * np.pi, n_theta)
    phi = np.linspace(0.0, np.pi, n_phi)
    x = centre[0] + radius * np.outer(np.cos(theta), np.sin(phi))
    y = centre[1] + radius * np.outer(np.sin(theta), np.sin(phi))
    z = centre[2] + radius * np.outer(np.ones_like(theta), np.cos(phi))
    ax.plot_surface(x, y, z, color=colour, edgecolor="none",
                    linewidth=0, antialiased=False, shade=True,
                    rstride=1, cstride=1, alpha=1.0)


def _draw_bonds(ax, mol: Chem.Mol, positions: np.ndarray, style: str) -> None:
    if style == "sphere":
        return  # space-filling hides bonds
    for bond in mol.GetBonds():
        i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        pi, pj = positions[i], positions[j]
        order = bond.GetBondTypeAsDouble()
        if style == "ball-and-stick":
            # Split bond by midpoint to colour each half by its atom.
            mid = (pi + pj) / 2
            ci = _CPK.get(mol.GetAtomWithIdx(i).GetSymbol(), _DEFAULT_COLOUR)
            cj = _CPK.get(mol.GetAtomWithIdx(j).GetSymbol(), _DEFAULT_COLOUR)
            ax.plot([pi[0], mid[0]], [pi[1], mid[1]], [pi[2], mid[2]],
                    color=ci, linewidth=_bond_width(style, order), solid_capstyle="round")
            ax.plot([mid[0], pj[0]], [mid[1], pj[1]], [mid[2], pj[2]],
                    color=cj, linewidth=_bond_width(style, order), solid_capstyle="round")
        else:
            ax.plot([pi[0], pj[0]], [pi[1], pj[1]], [pi[2], pj[2]],
                    color="#202020", linewidth=_bond_width(style, order),
                    solid_capstyle="round")
        # Double / triple bonds: extra parallel lines offset perpendicular to viewer.
        if order >= 2 and style != "line":
            v = pj - pi
            # Pick an arbitrary perpendicular vector for the offset.
            perp = np.cross(v, [0, 0, 1])
            if np.linalg.norm(perp) < 1e-6:
                perp = np.cross(v, [0, 1, 0])
            perp = perp / (np.linalg.norm(perp) + 1e-9) * 0.15
            offsets = [perp] if order == 2 else [perp, -perp]
            for off in offsets:
                ax.plot([pi[0] + off[0], pj[0] + off[0]],
                        [pi[1] + off[1], pj[1] + off[1]],
                        [pi[2] + off[2], pj[2] + off[2]],
                        color="#202020", linewidth=_bond_width(style, 1.0) * 0.7)


def _tidy_axes(ax, positions: np.ndarray) -> None:
    ax.set_axis_off()
    lo, hi = positions.min(axis=0), positions.max(axis=0)
    centre = (lo + hi) / 2
    # Tight span: enough buffer that the VdW sphere of a terminal atom
    # isn't clipped, but not so much that the molecule becomes a speck in
    # a cube. 0.55× + 1.2 Å works for both small (caffeine) and elongated
    # (cholesterol) molecules.
    span = max(hi - lo) * 0.55 + 1.2
    for setlim, c in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), centre):
        setlim(c - span, c + span)
    ax.set_box_aspect([1, 1, 1])
