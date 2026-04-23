"""Teaching-grade NMR stick-spectrum renderer — Phase 4 extension.

Given a SMILES, draw a schematic NMR trace: ppm on the x-axis
(decreasing left-to-right, NMR convention), stick peaks at the
mid-point of each predicted environment range, labelled with the
functional-group name.

Not a real NMR spectrum — just a **cheat-sheet picture** of which
environments should appear where. Real data needs experiment or
GIAO/DFT. Output: PNG / SVG by extension.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from orgchem.core.nmr import predict_shifts
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


def render_figure(smiles: str, nucleus: str = "H",
                  width: int = 900, height: int = 400,
                  title: str = "") -> "matplotlib.figure.Figure":
    res = predict_shifts(smiles, nucleus)
    if "error" in res:
        raise RenderError(res["error"])

    # Axis range: ¹H standard 0–12 ppm; ¹³C 0–220 ppm.
    if nucleus.upper() == "H":
        x_lo, x_hi = 0.0, 12.0
    else:
        x_lo, x_hi = 0.0, 220.0

    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    for pk in res["peaks"]:
        lo, hi = pk["range_ppm"]
        centre = 0.5 * (lo + hi)
        height_k = 0.4 + 0.1 * min(pk["n_matches"], 5)
        # Stick peak
        ax.vlines(centre, 0, height_k, color="#1f3a70", linewidth=2)
        # Shaded band showing the range
        ax.axvspan(lo, hi, ymin=0, ymax=0.05,
                   alpha=0.3, color="#1f3a70")
        # Label + integration count
        label = pk["environment"].replace(" (", "\n(")
        ax.text(centre, height_k + 0.05,
                f"{label}\n×{pk['n_matches']}",
                ha="center", va="bottom", fontsize=8,
                color="#222222")

    ax.set_xlim(x_hi, x_lo)   # invert — NMR convention (high ppm left)
    ax.set_ylim(-0.05, 1.4)
    ax.set_xlabel(f"Chemical shift δ ({nucleus.upper()}, ppm)",
                  fontsize=11)
    ax.set_yticks([])
    for spine in ("top", "left", "right"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", linestyle=":", alpha=0.4)

    ax.set_title(title or f"Predicted {nucleus.upper()} NMR — {smiles}",
                 fontsize=12)
    fig.text(0.99, 0.01,
             "Teaching sketch — see SDBS / BMRB for measured spectra.",
             ha="right", va="bottom", fontsize=7, color="#888888")
    fig.tight_layout()
    return fig


def export_nmr_spectrum(smiles: str, path: Union[str, Path],
                        nucleus: str = "H",
                        width: int = 900, height: int = 400,
                        title: str = "") -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "png"
    if suffix not in ("png", "svg"):
        raise RenderError(
            f"Unsupported NMR output format {suffix!r}; use png or svg.")
    fig = render_figure(smiles, nucleus=nucleus,
                        width=width, height=height, title=title)
    try:
        fig.savefig(p, format=suffix, bbox_inches="tight",
                    dpi=150 if suffix == "png" else None)
    finally:
        plt.close(fig)
    return p
