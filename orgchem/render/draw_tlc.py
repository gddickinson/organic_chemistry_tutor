"""TLC plate image renderer — Phase 15b follow-up.

Takes the output of :func:`orgchem.core.chromatography.simulate_tlc`
(or any compatible ``{compounds: [{smiles, rf}, …], solvent: str}``
dict) and produces a schematic TLC plate: a rectangle with a baseline
at the bottom, a solvent front at the top, and one coloured spot per
compound at its predicted Rf. Each lane is labelled with the lane
number (1, 2, 3, ...) below the baseline; a legend maps lane numbers
to SMILES strings.

The output is a matplotlib figure saved to PNG or SVG (decided by the
file extension of the ``path`` argument). No Qt / GUI dependency, so
the agent action can run headless.

Typical use:

>>> from orgchem.core.chromatography import simulate_tlc
>>> from orgchem.render.draw_tlc import export_tlc_plate
>>> data = simulate_tlc(["CC(=O)O", "c1ccccc1", "CCO"],
...                     solvent="hexane:ethyl_acetate:1:1")
>>> export_tlc_plate(data, "demo.png")
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

log = logging.getLogger(__name__)


# One distinct colour per lane — cycled if > 10 lanes. Chosen for
# reasonable contrast on a pale silica background.
_LANE_COLOURS = (
    "#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e",
    "#17becf", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22",
)


def render_figure(tlc_result: Mapping[str, Any],
                  width: float = 6.4,
                  height: float = 5.6,
                  title: Optional[str] = None) -> plt.Figure:
    """Return a matplotlib ``Figure`` of the TLC plate.

    The caller owns the figure — use :func:`export_tlc_plate` if you
    just want to save straight to a file.
    """
    compounds = tlc_result.get("compounds") or []
    solvent = tlc_result.get("solvent", "unspecified solvent")
    polarity = tlc_result.get("solvent_polarity")

    # Filter out error rows so the plate doesn't draw a spot at rf=0
    # for a SMILES the predictor couldn't parse.
    valid = [c for c in compounds if "rf" in c]

    fig, ax = plt.subplots(figsize=(width, height))
    # Plate geometry. X goes 0..1 with margin, lane centres evenly
    # spaced. Y goes 0 (baseline) to 1 (solvent front) plus a small
    # margin so the annotations aren't clipped.
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.15, 1.18)
    ax.set_aspect("equal")
    ax.axis("off")

    # Silica-gel panel background.
    plate = FancyBboxPatch(
        (-0.02, -0.04), 1.04, 1.12,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        linewidth=1.0, edgecolor="#6a6a6a",
        facecolor="#f4f1e6",   # pale silica tint
        zorder=1,
    )
    ax.add_patch(plate)

    # Baseline (origin) — pencil line a quarter-inch from the bottom.
    ax.plot([0.02, 0.98], [0.0, 0.0], color="#333", lw=0.9, zorder=2)
    ax.text(0.02, -0.06, "baseline (origin)", fontsize=8,
            color="#444", ha="left", va="top")

    # Solvent front at Rf = 1.
    ax.plot([0.02, 0.98], [1.0, 1.0], color="#6a6a6a",
            lw=0.8, ls="--", zorder=2)
    ax.text(0.98, 1.06, "solvent front (Rf = 1)", fontsize=8,
            color="#444", ha="right", va="bottom")

    # Lane spacing.
    n = max(len(valid), 1)
    margin = 0.10
    usable = 1.0 - 2 * margin
    xs = [margin + (i + 0.5) * usable / n for i in range(n)]

    for i, (x, comp) in enumerate(zip(xs, valid)):
        rf = float(comp["rf"])
        colour = _LANE_COLOURS[i % len(_LANE_COLOURS)]
        # Spot — ellipse-ish blob, diameter ~ 0.045 in plot units.
        spot = Circle(
            (x, rf), 0.032,
            facecolor=colour, edgecolor=colour,
            alpha=0.82, zorder=3,
        )
        ax.add_patch(spot)
        # Rf annotation to the right of the spot.
        ax.text(x + 0.04, rf, f"{rf:.2f}", fontsize=8,
                color="#222", va="center")
        # Lane label below the baseline.
        ax.text(x, -0.08, str(i + 1), fontsize=9,
                color="#222", ha="center", va="top",
                fontweight="bold")

    # Title + solvent strip at the very top.
    if title is None:
        title = f"TLC plate — {solvent}"
    ax.text(0.5, 1.14, title, fontsize=11, ha="center",
            fontweight="bold")
    if polarity is not None:
        ax.text(0.5, 1.09, f"solvent polarity score: {polarity:.2f}",
                fontsize=8.5, ha="center", color="#555")

    # Legend: lane → SMILES. Put it in an axes annotation box below
    # the plate, in-figure so it's saved with the PNG.
    if valid:
        legend_lines = []
        for i, comp in enumerate(valid, start=1):
            smi = comp.get("smiles", "?")
            if len(smi) > 42:
                smi = smi[:39] + "…"
            legend_lines.append(f"{i}. {smi}   (logP {comp.get('logp', 0):+.2f})")
        ax.text(
            0.02, -0.12, "\n".join(legend_lines),
            fontsize=7.5, family="monospace", color="#222",
            va="top", ha="left",
        )

    fig.tight_layout()
    return fig


def export_tlc_plate(tlc_result: Mapping[str, Any],
                     path: Union[str, Path],
                     width: float = 6.4, height: float = 5.6,
                     title: Optional[str] = None,
                     dpi: int = 160) -> Path:
    """Render the TLC plate and save to ``path``. Format is picked
    from the file extension (PNG or SVG). Returns the absolute path
    written, raising if matplotlib couldn't save."""
    out = Path(path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig = render_figure(tlc_result, width=width, height=height, title=title)
    try:
        fig.savefig(out, dpi=dpi, bbox_inches="tight")
    finally:
        plt.close(fig)
    log.info("Exported TLC plate → %s (%d compounds)",
             out, len(tlc_result.get("compounds") or []))
    return out
