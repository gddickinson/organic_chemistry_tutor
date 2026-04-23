"""Static 3D side-by-side reaction rendering (Phase 2c.1) + trajectory
HTML (Phase 2c.2).

Given an atom-mapped reaction SMARTS, this module:

1. Extracts the reactant side and product side as separate molecules.
2. Embeds 3D coordinates for each via ``AllChem.EmbedMolecule``.
3. Renders both with :mod:`orgchem.render.draw3d_mpl` and composites them
   side-by-side with an arrow between.
4. Colours atoms by their map number so "the same atom" stays the same
   hue across reactant and product — the pedagogical payoff.
5. Highlights bonds that broke (red) and bonds that formed (green) by
   comparing reactant and product bond sets keyed on map-number pairs.

The composite output is a single PNG. Reactions without atom mapping
raise :class:`RenderError` — callers should fall back to the 2D scheme.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np               # noqa: E402
from rdkit import Chem           # noqa: E402
from rdkit.Chem import AllChem   # noqa: E402

from orgchem.messaging.errors import RenderError
from orgchem.render import draw3d_mpl

log = logging.getLogger(__name__)


# A small palette of hues to colour atoms by map number.
# (Used only when `colour_by_map=True` — falls back to CPK otherwise.)
_MAP_HUES = [
    "#E06666", "#6FA8DC", "#93C47D", "#F6B26B", "#8E7CC3",
    "#FFD966", "#76A5AF", "#C27BA0", "#B6D7A8", "#B4A7D6",
]


def _split_reaction(smarts: str) -> Tuple[List[Chem.Mol], List[Chem.Mol]]:
    """Parse a reaction SMARTS into (reactant_mols, product_mols)."""
    rxn = AllChem.ReactionFromSmarts(smarts, useSmiles=True)
    if rxn is None:
        raise RenderError(f"Could not parse reaction: {smarts!r}")
    reactants = [Chem.Mol(rxn.GetReactantTemplate(i))
                 for i in range(rxn.GetNumReactantTemplates())]
    products = [Chem.Mol(rxn.GetProductTemplate(i))
                for i in range(rxn.GetNumProductTemplates())]
    return reactants, products


def _combine(mols: List[Chem.Mol]) -> Chem.Mol:
    """Combine disconnected fragments into a single Mol. Preserves atom maps."""
    if not mols:
        raise RenderError("No molecules to combine")
    combined = mols[0]
    for m in mols[1:]:
        combined = Chem.CombineMols(combined, m)
    # Convert read-only template to an editable Mol with explicit Hs
    rw = Chem.RWMol(combined)
    try:
        Chem.SanitizeMol(rw)
    except Exception:
        # Partial sanitisation — reaction templates sometimes violate
        # valence strictly because they represent intermediates.
        Chem.SanitizeMol(rw, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL
                         ^ Chem.SanitizeFlags.SANITIZE_PROPERTIES)
    return rw.GetMol()


def _embed_with_hs(mol: Chem.Mol, seed: int = 0xF00D) -> Chem.Mol:
    m = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(m, randomSeed=seed) != 0:
        # Try a second attempt with a different seed.
        if AllChem.EmbedMolecule(m, randomSeed=seed + 1) != 0:
            raise RenderError("3D embedding failed")
    try:
        AllChem.MMFFOptimizeMolecule(m)
    except Exception:
        pass
    return m


def _bond_set_by_map(mol: Chem.Mol) -> Set[Tuple[int, int]]:
    """Return {(map_a, map_b)} with map numbers sorted; atoms without map skipped."""
    out: Set[Tuple[int, int]] = set()
    for b in mol.GetBonds():
        a, z = b.GetBeginAtom(), b.GetEndAtom()
        ma, mz = a.GetAtomMapNum(), z.GetAtomMapNum()
        if ma and mz:
            out.add(tuple(sorted((ma, mz))))
    return out


def _bond_orders_by_map(mol: Chem.Mol) -> Dict[Tuple[int, int], float]:
    """Return {(map_a, map_b): bond_order}. Singles=1.0, doubles=2.0, aromatic=1.5."""
    out: Dict[Tuple[int, int], float] = {}
    for b in mol.GetBonds():
        a, z = b.GetBeginAtom(), b.GetEndAtom()
        ma, mz = a.GetAtomMapNum(), z.GetAtomMapNum()
        if ma and mz:
            out[tuple(sorted((ma, mz)))] = b.GetBondTypeAsDouble()
    return out


def render_png(reaction_smarts: str, path: Union[str, Path],
               width: int = 1200, height: int = 520,
               colour_by_map: bool = True,
               elev: float = 20.0, azim: float = -60.0) -> Path:
    """Render a reaction in 3D, reactant → product, to *path*."""
    if not _has_map(reaction_smarts):
        raise RenderError(
            "Reaction has no atom mapping — cannot correlate atoms "
            "between reactant and product in 3D."
        )
    reactants, products = _split_reaction(reaction_smarts)
    r_mol = _embed_with_hs(_combine(reactants))
    p_mol = _embed_with_hs(_combine(products))

    r_orders = _bond_orders_by_map(r_mol)
    p_orders = _bond_orders_by_map(p_mol)
    r_keys, p_keys = set(r_orders), set(p_orders)
    # Bonds that outright broke: present in reactant, absent in product.
    broken = r_keys - p_keys
    formed = p_keys - r_keys
    # Bonds whose order *decreased* across the arrow (e.g. C=O → C-O in
    # NaBH4 reduction). Those look like "half-broken" on the reactant
    # side — highlight red too.
    for k in r_keys & p_keys:
        if r_orders[k] > p_orders[k] + 1e-6:
            broken.add(k)
        elif p_orders[k] > r_orders[k] + 1e-6:
            formed.add(k)

    fig = plt.figure(figsize=(width / 100, height / 100), dpi=100,
                     facecolor="white")
    ax_r = fig.add_subplot(1, 2, 1, projection="3d")
    ax_p = fig.add_subplot(1, 2, 2, projection="3d")

    _render_on_axes(ax_r, r_mol, colour_by_map=colour_by_map,
                    highlighted_bonds=broken, highlight_colour="#c03030")
    _render_on_axes(ax_p, p_mol, colour_by_map=colour_by_map,
                    highlighted_bonds=formed, highlight_colour="#2ba02b")

    for ax in (ax_r, ax_p):
        ax.view_init(elev=elev, azim=azim)
    ax_r.set_position([0.0, 0.04, 0.48, 0.90])
    ax_p.set_position([0.52, 0.04, 0.48, 0.90])

    # Arrow + labels in figure-normalised coords.
    fig.text(0.24, 0.98, "Reactants",  ha="center", fontsize=13, fontweight="bold")
    fig.text(0.76, 0.98, "Products",   ha="center", fontsize=13, fontweight="bold")
    fig.text(0.50, 0.50, "→", ha="center", va="center", fontsize=42,
             color="#404040", fontweight="bold")
    fig.text(0.50, 0.10,
             "red = bond broken    green = bond formed",
             ha="center", va="center", fontsize=9, color="#808080")

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, dpi=100, facecolor="white")
    plt.close(fig)
    log.info("Exported 3D reaction → %s (%d bytes)", p, p.stat().st_size)
    return p


def _has_map(smarts: str) -> bool:
    return ":" in smarts  # cheap but good enough — real SMARTS can have : in ring bonds


# ------------------------------------------------------------------
# Trajectory HTML (Phase 2c.2)
#
# 3Dmol.js natively supports multi-frame playback: ``addModelsAsFrames``
# accepts a multi-model XYZ / SDF string and ``animate()`` plays back
# frame-by-frame. Bonds are auto-inferred by proximity each frame, which
# is exactly what we want — students see bonds appear and disappear as
# atoms move through the transition state.

_TRAJECTORY_HTML_TEMPLATE = """<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{title}</title>
<script src="{js_src}"></script>
<style>
  html, body {{ margin: 0; padding: 0; height: 100%; width: 100%; background: {bg}; font-family: sans-serif; }}
  #viewer {{ width: 100%; height: calc(100vh - 44px); position: relative; }}
  #controls {{ height: 40px; padding: 4px 8px; background: #f4f4f4; border-top: 1px solid #ccc;
               display: flex; align-items: center; gap: 8px; font-size: 13px; color: #333; }}
  button {{ padding: 3px 10px; font-size: 13px; cursor: pointer; }}
</style>
</head><body>
<div id="viewer"></div>
<div id="controls">
  <button id="play">▶ Play</button>
  <button id="pause">⏸ Pause</button>
  <button id="reset">↻ Reset</button>
  <span style="margin-left:12px;">Speed:</span>
  <input id="speed" type="range" min="40" max="400" value="{interval}">
  <span style="margin-left:auto; color:#666;">{title}</span>
</div>
<script>
  const viewer = $3Dmol.createViewer("viewer", {{ backgroundColor: "{bg}" }});
  viewer.addModelsAsFrames(`{xyz}`, "xyz");
  viewer.setStyle({{}}, {{ stick: {{ radius: 0.15 }}, sphere: {{ scale: 0.28 }} }});
  viewer.zoomTo();
  viewer.render();

  let interval = {interval};
  let anim = null;
  function startAnim() {{
    if (anim) viewer.stopAnimate();
    anim = viewer.animate({{ loop: "forward", reps: 0, interval: interval }});
  }}
  document.getElementById("play").onclick = startAnim;
  document.getElementById("pause").onclick = () => viewer.stopAnimate();
  document.getElementById("reset").onclick = () => {{
    viewer.stopAnimate(); viewer.setFrame(0); viewer.render();
  }};
  document.getElementById("speed").oninput = (e) => {{
    interval = parseInt(e.target.value); if (anim) startAnim();
  }};
  startAnim();
</script>
</body></html>
"""


def build_trajectory_html(xyz: str, title: str = "Reaction trajectory",
                          background: str = "white",
                          interval_ms: int = 120,
                          js_src: str = "https://3dmol.org/build/3Dmol-min.js") -> str:
    """Wrap a multi-frame XYZ string into a playable 3Dmol.js HTML page.

    The returned HTML is self-contained — load it in a ``QWebEngineView``
    (or any browser) to get a play / pause / reset / speed-slider UI.
    """
    safe = xyz.replace("\\", "\\\\").replace("`", "\\`")
    return _TRAJECTORY_HTML_TEMPLATE.format(
        title=_html_escape(title),
        bg=background,
        interval=int(interval_ms),
        xyz=safe,
        js_src=js_src,
    )


def _html_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def _render_on_axes(ax, mol: Chem.Mol, colour_by_map: bool,
                    highlighted_bonds: Set[Tuple[int, int]],
                    highlight_colour: str) -> None:
    """Render *mol* onto *ax* as ball-and-stick."""
    if mol.GetNumConformers() == 0:
        raise RenderError("Molecule has no 3D coords")
    conf = mol.GetConformer()
    positions = np.array([
        [conf.GetAtomPosition(i).x,
         conf.GetAtomPosition(i).y,
         conf.GetAtomPosition(i).z] for i in range(mol.GetNumAtoms())
    ])

    # Draw bonds
    for bond in mol.GetBonds():
        i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        ma = mol.GetAtomWithIdx(i).GetAtomMapNum()
        mz = mol.GetAtomWithIdx(j).GetAtomMapNum()
        key = tuple(sorted((ma, mz))) if (ma and mz) else None
        colour = highlight_colour if key and key in highlighted_bonds else "#202020"
        width = 3.2 if key and key in highlighted_bonds else 1.6
        pi, pj = positions[i], positions[j]
        ax.plot([pi[0], pj[0]], [pi[1], pj[1]], [pi[2], pj[2]],
                color=colour, linewidth=width, solid_capstyle="round")

    # Draw atoms as shaded spheres.
    for i, atom in enumerate(mol.GetAtoms()):
        symbol = atom.GetSymbol()
        mapn = atom.GetAtomMapNum()
        if colour_by_map and mapn:
            colour = _MAP_HUES[(mapn - 1) % len(_MAP_HUES)]
        else:
            colour = draw3d_mpl._CPK.get(symbol, draw3d_mpl._DEFAULT_COLOUR)
        radius = draw3d_mpl._COV.get(symbol, 0.7) * 0.55
        draw3d_mpl._plot_sphere(ax, positions[i], radius, colour)

    ax.set_axis_off()
    lo, hi = positions.min(axis=0), positions.max(axis=0)
    centre = (lo + hi) / 2
    span = max(hi - lo) * 0.55 + 1.2
    for setlim, c in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), centre):
        setlim(c - span, c + span)
    ax.set_box_aspect([1, 1, 1])
