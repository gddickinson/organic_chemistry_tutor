"""Teaching-grade IR-spectrum renderer — Phase 4.

Given a SMILES, plot a **schematic** IR spectrum: wavenumber on the x
axis (4000 → 500 cm⁻¹, traditional absorbance-down convention), a
shaded band for each predicted characteristic absorption, labelled
with the functional-group class.

This is a **pedagogical sketch**, not a measured spectrum. The
intensity axis is symbolic (strong / medium / weak mapped to three
dip depths). Real IR spectra need FTIR data; point students to the
NIST WebBook link in the caption.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from orgchem.core.spectroscopy import predict_bands
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


_INTENSITY_DEPTH = {
    "strong":   0.85,
    "medium":   0.55,
    "weak":     0.30,
    "variable": 0.50,
}


def render_figure(smiles: str,
                  width: int = 900, height: int = 420,
                  title: str = "") -> "matplotlib.figure.Figure":
    res = predict_bands(smiles)
    if "error" in res:
        raise RenderError(res["error"])

    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    # IR spectra are conventionally plotted with wavenumber decreasing
    # left-to-right, absorbance pointing down. We use transmittance-
    # style dips.
    x = np.linspace(500, 4000, 2000)
    y = np.full_like(x, 1.0)  # baseline transmittance

    for band in res["bands"]:
        lo, hi = band["range_cm1"]
        centre = 0.5 * (lo + hi)
        sigma = max(10.0, 0.25 * (hi - lo))
        depth = _INTENSITY_DEPTH.get(band["intensity"], 0.55)
        # Gaussian dip centred at mid-range.
        y -= depth * np.exp(-0.5 * ((x - centre) / sigma) ** 2)

        # Label the band.
        label = band["group"].split("(")[0].strip()
        ax.text(centre, 1.04, label, ha="center", va="bottom",
                fontsize=8, color="#333333",
                rotation=0, clip_on=False)

    ax.plot(x, y, color="#1f3a70", linewidth=1.6)
    ax.fill_between(x, y, 1.0, color="#1f3a70", alpha=0.10)
    ax.set_xlim(4000, 500)      # invert x axis (high ν on the left)
    ax.set_ylim(-0.05, 1.25)
    ax.set_xlabel("Wavenumber (cm⁻¹)", fontsize=11)
    ax.set_ylabel("Transmittance (schematic)", fontsize=11)
    ax.set_title(title or f"Predicted IR spectrum — {smiles}",
                 fontsize=12)
    ax.grid(axis="x", linestyle=":", alpha=0.4)

    fig.text(0.99, 0.01,
             "Teaching sketch — see NIST WebBook for measured spectra.",
             ha="right", va="bottom", fontsize=7, color="#888888")
    fig.tight_layout()
    return fig


def export_ir_spectrum(smiles: str, path: Union[str, Path],
                       width: int = 900, height: int = 420,
                       title: str = "") -> Path:
    """Render a schematic IR spectrum to PNG or SVG."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "png"
    if suffix not in ("png", "svg"):
        raise RenderError(
            f"Unsupported IR output format {suffix!r}; use png or svg."
        )
    fig = render_figure(smiles, width=width, height=height, title=title)
    try:
        fig.savefig(p, format=suffix, bbox_inches="tight",
                    dpi=150 if suffix == "png" else None)
    finally:
        plt.close(fig)
    return p
