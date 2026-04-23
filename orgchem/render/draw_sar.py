"""SAR matrix renderer — Phase 19a.

Given a :class:`~orgchem.core.sar.SARSeries`, render a **heat-map-style**
matrix: rows are molecule variants, columns are a mix of structural
descriptors (MW, logP, TPSA, QED) and the series' activity metrics.

Each cell gets a background colour proportional to the value's rank in
its column — a per-column min-max rescaling so big-magnitude columns
(IC50 in nM, daily dose in mg) don't visually drown the smaller ones
(QED 0-1).

Output is PNG / SVG per file extension, same as every other renderer
in the project.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import List, Union

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from orgchem.core.sar import SARSeries
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


# Columns always shown first: molecule descriptors.
_DESCRIPTOR_COLS = ["mw", "logp", "tpsa", "qed", "lipinski_violations"]


def _row_values(row: dict, cols: List[str]) -> List[float]:
    out: List[float] = []
    for c in cols:
        v = row.get(c)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            out.append(float(v))
        else:
            out.append(float("nan"))
    return out


def render_figure(series: SARSeries,
                  width: int = 1100, height: int = 460,
                  title: str = "") -> "matplotlib.figure.Figure":
    rows = series.compute_descriptors()
    if not rows:
        raise RenderError(f"SAR series {series.id!r} has no variants.")

    cols = list(_DESCRIPTOR_COLS) + list(series.activity_columns)
    data = np.array([_row_values(r, cols) for r in rows], dtype=float)

    # Per-column normalisation to [0, 1]; NaNs (missing values) stay NaN
    # and render as neutral grey.
    data_norm = np.full_like(data, np.nan)
    for j in range(data.shape[1]):
        col = data[:, j]
        mask = ~np.isnan(col)
        if mask.sum() < 2:
            data_norm[mask, j] = 0.5
            continue
        lo, hi = np.nanmin(col), np.nanmax(col)
        if hi - lo < 1e-9:
            data_norm[mask, j] = 0.5
        else:
            # Small values → dark blue; large → bright red. Invert for
            # "lower-is-better" medchem metrics (IC50 / lipinski_violations)
            # so the green row always wins.
            norm = (col - lo) / (hi - lo)
            if _is_lower_better(cols[j]):
                norm = 1.0 - norm
            data_norm[:, j] = np.where(mask, norm, np.nan)

    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    cmap = plt.get_cmap("RdYlGn")
    # Lay down colour patches individually so NaNs become grey.
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            v = data_norm[i, j]
            colour = "#dddddd" if np.isnan(v) else cmap(v)
            ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1,
                                       facecolor=colour, edgecolor="white"))
            raw = data[i, j]
            label = "—" if np.isnan(raw) else _pretty(raw)
            ax.text(j + 0.5, -i - 0.5, label,
                    ha="center", va="center", fontsize=9,
                    color="#222222")

    ax.set_xlim(0, data.shape[1])
    ax.set_ylim(-data.shape[0], 1)
    ax.set_aspect("equal")
    ax.set_xticks([c + 0.5 for c in range(data.shape[1])])
    ax.set_xticklabels([_col_label(c) for c in cols], rotation=20,
                       ha="right", fontsize=9)
    ax.set_yticks([-i - 0.5 for i in range(data.shape[0])])
    ax.set_yticklabels([r["name"] for r in rows], fontsize=10)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title(title or f"SAR — {series.name}", fontsize=12, pad=12)
    fig.text(0.99, 0.01, f"target: {series.target}  —  source: {series.source}",
             ha="right", va="bottom", fontsize=7, color="#666666")
    fig.tight_layout()
    return fig


def _col_label(c: str) -> str:
    mapping = {
        "mw": "MW",
        "logp": "logP",
        "tpsa": "TPSA",
        "qed": "QED",
        "lipinski_violations": "Lipinski viol.",
    }
    return mapping.get(c, c.replace("_", " "))


def _is_lower_better(col: str) -> bool:
    # Metrics where smaller = better
    lower = {"lipinski_violations", "cox1_ic50_uM", "cox2_ic50_uM",
             "ic50_nM", "daily_dose_mg", "mw", "tpsa"}
    return col in lower


def _pretty(v: float) -> str:
    if abs(v) >= 1000:
        return f"{v:.0f}"
    if abs(v) >= 10:
        return f"{v:.1f}"
    return f"{v:.2f}"


def export_sar_matrix(series: SARSeries, path: Union[str, Path],
                      width: int = 1100, height: int = 460,
                      title: str = "") -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "png"
    if suffix not in ("png", "svg"):
        raise RenderError(
            f"Unsupported SAR output format {suffix!r}; use png or svg.")
    fig = render_figure(series, width=width, height=height, title=title)
    try:
        fig.savefig(p, format=suffix, bbox_inches="tight",
                    dpi=150 if suffix == "png" else None)
    finally:
        plt.close(fig)
    return p
