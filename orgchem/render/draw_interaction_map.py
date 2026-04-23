"""Protein-ligand 2D interaction map — Phase 24c.

Given a :class:`ContactReport` (Phase 24e output), draw a flat "spoke"
diagram: ligand as a centre disc, surrounding residues as labelled
circles around it, each connected by a dashed line colour-coded by
interaction type:

- **Green**      — hydrophobic
- **Blue**       — H-bond
- **Red**        — salt bridge
- **Purple**     — π-stacking

Style inspired by PoseView / LigPlot+. Pure matplotlib, no extra deps.
Output: PNG / SVG by file extension.
"""
from __future__ import annotations
import logging
from math import cos, pi, sin
from pathlib import Path
from typing import Dict, List, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from orgchem.core.binding_contacts import Contact, ContactReport
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


_KIND_COLOURS: Dict[str, str] = {
    "h-bond":        "#1f77b4",  # blue
    "salt-bridge":   "#d62728",  # red
    "pi-stacking":   "#9467bd",  # purple
    "hydrophobic":   "#2ca02c",  # green
}
_KIND_LINESTYLES: Dict[str, str] = {
    "h-bond":        "--",
    "salt-bridge":   "-",
    "pi-stacking":   ":",
    "hydrophobic":   "-.",
}


# ---------------------------------------------------------------------

def render_figure(report: ContactReport,
                  width: int = 900, height: int = 700,
                  title: str = "") -> "matplotlib.figure.Figure":
    if report.n_contacts == 0:
        raise RenderError(
            f"No contacts to draw for {report.ligand_name!r}; "
            "nothing to render."
        )

    # Collapse multiple contacts to the same residue so each appears once.
    per_residue: Dict[str, List[Contact]] = {}
    for c in report.contacts:
        key = f"{c.protein_chain}:{c.protein_residue}"
        per_residue.setdefault(key, []).append(c)

    n = len(per_residue)
    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    # Ligand at centre
    ax.add_patch(plt.Circle((0, 0), 0.22, facecolor="#fff2a8",
                            edgecolor="#6a4f00", linewidth=2, zorder=3))
    ax.text(0, 0, report.ligand_name,
            ha="center", va="center", fontsize=11, fontweight="bold",
            color="#3e2e00", zorder=4)

    # Residues around the ligand in a circle
    radius = 1.2
    for i, (res_label, contacts) in enumerate(per_residue.items()):
        theta = 2 * pi * i / n - pi / 2.0
        rx, ry = radius * cos(theta), radius * sin(theta)
        # Each interaction drawn as its own dashed line.
        for c in contacts:
            colour = _KIND_COLOURS.get(c.kind, "#888888")
            linestyle = _KIND_LINESTYLES.get(c.kind, "--")
            ax.plot([0, rx], [0, ry], color=colour,
                    linestyle=linestyle, linewidth=1.6, alpha=0.85,
                    zorder=1)
            # Distance label at midpoint
            mx, my = rx * 0.55, ry * 0.55
            ax.text(mx, my, f"{c.distance:.1f}",
                    fontsize=7, color=colour,
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.1",
                              fc="white", ec="none", alpha=0.6),
                    zorder=2)
        # Residue node
        ax.add_patch(plt.Circle((rx, ry), 0.12,
                                facecolor="white", edgecolor="#444",
                                linewidth=1.2, zorder=3))
        chain, rest = res_label.split(":", 1)
        ax.text(rx, ry, rest,
                ha="center", va="center", fontsize=9, zorder=4)

    # Legend
    legend_items = [
        plt.Line2D([0], [0], color=_KIND_COLOURS[k],
                   linestyle=_KIND_LINESTYLES[k], linewidth=2,
                   label=k)
        for k in ("h-bond", "salt-bridge", "pi-stacking", "hydrophobic")
        if any(c.kind == k for c in report.contacts)
    ]
    if legend_items:
        ax.legend(handles=legend_items, loc="lower left", fontsize=9,
                  frameon=True, facecolor="white")

    pad = radius + 0.35
    ax.set_xlim(-pad, pad)
    ax.set_ylim(-pad, pad)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_title(
        title or f"Interaction map — {report.pdb_id} × {report.ligand_name}",
        fontsize=12,
    )
    fig.text(0.99, 0.01,
             f"{report.n_contacts} contacts · geometric model "
             "(install PLIP for angle-aware detection)",
             ha="right", va="bottom", fontsize=7, color="#888888")
    fig.tight_layout()
    return fig


def export_interaction_map(report: ContactReport,
                           path: Union[str, Path],
                           width: int = 900, height: int = 700,
                           title: str = "") -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "png"
    if suffix not in ("png", "svg"):
        raise RenderError(
            f"Unsupported interaction-map format {suffix!r}; use png or svg."
        )
    fig = render_figure(report, width=width, height=height, title=title)
    try:
        fig.savefig(p, format=suffix, bbox_inches="tight",
                    dpi=150 if suffix == "png" else None)
    finally:
        plt.close(fig)
    return p
