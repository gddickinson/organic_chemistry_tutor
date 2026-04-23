"""Molecular-orbital level-diagram renderer — Phase 14a.

Given a :class:`~orgchem.core.huckel.HuckelResult`, draws the classic
"pile of horizontal lines" MO energy diagram with:

- Energy axis (in β units, α = 0).
- One horizontal bar per MO at its energy.
- Occupied electrons shown as up/down arrows on each line.
- HOMO and LUMO labelled with coloured arrows.
- Degenerate levels (same energy within a tolerance) drawn side by side.

PNG / SVG chosen by file extension. Works headless (Agg backend).
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from orgchem.core.huckel import HuckelResult
from orgchem.messaging.errors import RenderError


_BAR_LEN = 0.28
_DEGENERACY_TOL = 1e-3
_COLOUR_BONDING = "#1f77b4"
_COLOUR_ANTIBONDING = "#d62728"
_COLOUR_NONBONDING = "#666666"
_COLOUR_HOMO = "#1b7a1b"
_COLOUR_LUMO = "#b55a00"


def _group_degenerate(energies: List[float]) -> List[List[int]]:
    """Group MO indices by (approximately) equal energy — preserves input order."""
    groups: List[List[int]] = []
    for i, e in enumerate(energies):
        if groups and abs(e - energies[groups[-1][0]]) < _DEGENERACY_TOL:
            groups[-1].append(i)
        else:
            groups.append([i])
    return groups


def render_figure(result: HuckelResult,
                  width: int = 700, height: int = 600,
                  title: str = "") -> "matplotlib.figure.Figure":
    if not result.energies:
        raise RenderError("Hückel result has no MOs to render.")

    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    homo = result.homo_index
    lumo = result.lumo_index
    occ = result.occupations
    groups = _group_degenerate(result.energies)

    for group in groups:
        count = len(group)
        e = result.energies[group[0]]
        for k, idx in enumerate(group):
            cx = 0.5 + (k - (count - 1) / 2.0) * (_BAR_LEN * 1.15)
            x0, x1 = cx - _BAR_LEN / 2.0, cx + _BAR_LEN / 2.0
            if e > _DEGENERACY_TOL:
                colour = _COLOUR_BONDING
            elif e < -_DEGENERACY_TOL:
                colour = _COLOUR_ANTIBONDING
            else:
                colour = _COLOUR_NONBONDING
            ax.plot([x0, x1], [e, e], color=colour, linewidth=2.5, zorder=3)

            # electrons as up/down arrows
            if occ[idx] >= 1:
                ax.annotate("", xy=(cx - 0.025, e + 0.12),
                            xytext=(cx - 0.025, e - 0.12),
                            arrowprops=dict(arrowstyle="->",
                                            color=colour, lw=1.3))
            if occ[idx] == 2:
                ax.annotate("", xy=(cx + 0.025, e - 0.12),
                            xytext=(cx + 0.025, e + 0.12),
                            arrowprops=dict(arrowstyle="->",
                                            color=colour, lw=1.3))

            # HOMO / LUMO labels
            if idx == homo:
                ax.text(x1 + 0.02, e, "HOMO",
                        color=_COLOUR_HOMO, va="center",
                        fontsize=10, fontweight="bold")
            elif idx == lumo:
                ax.text(x1 + 0.02, e, "LUMO",
                        color=_COLOUR_LUMO, va="center",
                        fontsize=10, fontweight="bold")

            # energy label to the left of the first bar in each group
            if k == 0:
                ax.text(x0 - 0.04, e, f"{e:+.3f} β",
                        ha="right", va="center", fontsize=9, color="#222")

    # α reference line
    ax.axhline(0.0, color="#999999", linestyle=":", linewidth=0.8, zorder=1)
    ax.text(1.25, 0.01, "α", ha="left", va="bottom",
            color="#888", fontsize=9)

    ax.set_xlim(0, 1.3)
    ax.set_ylim(min(result.energies) - 0.6, max(result.energies) + 0.6)
    ax.set_ylabel("Energy (units of β; α = 0)", fontsize=11)
    ax.set_xticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_title(title or f"MO levels — {result.n_pi_atoms} π atoms, "
                          f"{result.n_pi_electrons} π e⁻", fontsize=12)
    fig.tight_layout()
    return fig


def export_mo_diagram(result: HuckelResult, path: Union[str, Path],
                      width: int = 700, height: int = 600,
                      **kwargs) -> Path:
    """Render a Hückel MO level diagram to PNG / SVG (by extension)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "png"
    if suffix not in ("png", "svg"):
        raise RenderError(
            f"Unsupported MO-diagram output format {suffix!r}; use png or svg.")
    fig = render_figure(result, width=width, height=height, **kwargs)
    try:
        fig.savefig(p, format=suffix, bbox_inches="tight",
                    dpi=150 if suffix == "png" else None)
    finally:
        plt.close(fig)
    return p
