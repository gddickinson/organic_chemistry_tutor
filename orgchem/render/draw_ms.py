"""Mass-spectrum stick-plot renderer — Phase 4 extension.

Given a SMILES, plot m/z on the x-axis and the computed relative
isotope-pattern intensity (0-100 %) on the y-axis. Labels show
``M / M+1 / M+2 / ...`` with numeric m/z above each peak.

Matches typical EI-MS teaching figures — focuses on the M⁺ envelope
rather than fragmentation (which needs the ionisation-pathway
framework to compute). For a student, this is the "molecular-ion
region" zoom. Exports PNG / SVG by extension.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from orgchem.core.ms import isotope_pattern
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


def render_figure(smiles: str,
                  width: int = 900, height: int = 380,
                  title: str = "",
                  min_intensity: float = 0.01) -> "matplotlib.figure.Figure":
    r = isotope_pattern(smiles)
    if "error" in r:
        raise RenderError(r["error"])
    peaks = [p for p in r["peaks"] if p["intensity"] >= min_intensity]
    if not peaks:
        raise RenderError("no peaks above minimum intensity threshold")

    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    mzs = [p["mz"] for p in peaks]
    ys = [p["intensity"] * 100.0 for p in peaks]

    ax.vlines(mzs, 0, ys, color="#1f3a70", linewidth=2.2)

    for p in peaks:
        y = p["intensity"] * 100
        ax.text(p["mz"], y + 2,
                f"{p['label']}\n{p['mz']:.2f}",
                ha="center", va="bottom", fontsize=8,
                color="#222222")

    # x range: span ~4 Da on each side of the envelope.
    lo = min(mzs) - 2.0
    hi = max(mzs) + 2.0
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 120)
    ax.set_xlabel("m/z", fontsize=11)
    ax.set_ylabel("Relative intensity (%)", fontsize=11)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.4)

    ax.set_title(title or f"Predicted MS — {r['smiles']} "
                          f"({r['formula']}, {r['monoisotopic_mass']:.4f})",
                 fontsize=12)
    fig.text(0.99, 0.01,
             "Molecular-ion region only — fragmentation not predicted.",
             ha="right", va="bottom", fontsize=7, color="#888888")
    fig.tight_layout()
    return fig


def export_ms_spectrum(smiles: str, path: Union[str, Path],
                       width: int = 900, height: int = 380,
                       title: str = "",
                       min_intensity: float = 0.01) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "png"
    if suffix not in ("png", "svg"):
        raise RenderError(
            f"Unsupported MS output format {suffix!r}; use png or svg.")
    fig = render_figure(smiles, width=width, height=height,
                        title=title, min_intensity=min_intensity)
    try:
        fig.savefig(p, format=suffix, bbox_inches="tight",
                    dpi=150 if suffix == "png" else None)
    finally:
        plt.close(fig)
    return p
