"""Reaction-coordinate (energy-profile) renderer — Phase 13a.

Draws a reaction coordinate diagram with matplotlib:

- x-axis: reaction progress (unitless).
- y-axis: relative energy in ``profile.energy_unit``.
- TS‡ points are rendered as sharp peaks with a ‡ suffix; minima
  (reactants / intermediates / products) as smoothed plateaux.
- Each segment between adjacent points is a Bezier arc shaped by whether
  the endpoints are minima or transition states, giving the familiar
  "mountain-range" energy profile without needing the author to specify
  curvature.
- Activation energies Ea, overall ΔH, and intermediate-well depths are
  annotated automatically.

Output: PNG or SVG, chosen by file extension. Works headless (Agg
backend); no QWidget needed.

The input is a :class:`ReactionEnergyProfile` — no other dependencies
on the app. The output is a :class:`pathlib.Path` to the written file.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import List, Tuple, Union

import matplotlib
matplotlib.use("Agg")  # force non-interactive backend for headless safety
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from orgchem.core.energy_profile import ReactionEnergyProfile, StationaryPoint
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


_MIN_COLOUR = "#1f77b4"   # blue — reactant / intermediate / product
_TS_COLOUR  = "#d62728"   # red  — transition state
_ANNOT_COLOUR = "#444444"
_CURVE_COLOUR = "#333333"
_WELL_COLOUR = "#1f77b4"


def _bezier_between(x0: float, y0: float, x1: float, y1: float,
                    is_left_ts: bool, is_right_ts: bool,
                    n: int = 40) -> Tuple[np.ndarray, np.ndarray]:
    """Cubic-Bezier segment shaped so peaks are sharp and minima plateau.

    Control points are placed horizontally from each endpoint — their
    distance is larger when the endpoint is a minimum (flatter approach)
    and smaller when the endpoint is a TS (steeper approach).
    """
    dx = x1 - x0
    c0_w = 0.45 if not is_left_ts else 0.28
    c1_w = 0.45 if not is_right_ts else 0.28
    cx0, cy0 = x0 + c0_w * dx, y0
    cx1, cy1 = x1 - c1_w * dx, y1
    t = np.linspace(0.0, 1.0, n)
    one_t = 1.0 - t
    bx = (one_t ** 3) * x0 + 3 * (one_t ** 2) * t * cx0 + 3 * one_t * (t ** 2) * cx1 + (t ** 3) * x1
    by = (one_t ** 3) * y0 + 3 * (one_t ** 2) * t * cy0 + 3 * one_t * (t ** 2) * cy1 + (t ** 3) * y1
    return bx, by


def _build_curve(points: List[StationaryPoint]) -> Tuple[np.ndarray, np.ndarray,
                                                          List[float], List[float]]:
    """Return (curve_x, curve_y, point_x, point_y) for rendering."""
    n = len(points)
    xs = list(range(n))
    ys = [p.energy for p in points]
    curve_x: List[float] = []
    curve_y: List[float] = []
    for i in range(n - 1):
        bx, by = _bezier_between(
            xs[i], ys[i], xs[i + 1], ys[i + 1],
            is_left_ts=points[i].is_ts,
            is_right_ts=points[i + 1].is_ts,
        )
        if i > 0:
            bx, by = bx[1:], by[1:]   # avoid double-plotting the shared endpoint
        curve_x.extend(bx.tolist())
        curve_y.extend(by.tolist())
    return np.asarray(curve_x), np.asarray(curve_y), xs, ys


def _annotate_barriers(ax, points: List[StationaryPoint],
                       xs: List[float], ys: List[float]) -> None:
    """Draw dashed Ea lines from the preceding minimum up to each TS."""
    last_min_i = None
    for i, p in enumerate(points):
        if p.is_ts:
            if last_min_i is not None:
                ea = p.energy - points[last_min_i].energy
                xm = (xs[last_min_i] + xs[i]) / 2.0
                ax.plot([xs[last_min_i], xs[i]],
                        [points[last_min_i].energy, points[last_min_i].energy],
                        linestyle=":", color=_ANNOT_COLOUR, linewidth=0.9, alpha=0.7)
                ax.annotate(
                    "", xy=(xs[i], p.energy),
                    xytext=(xs[i], points[last_min_i].energy),
                    arrowprops=dict(arrowstyle="<->", color=_ANNOT_COLOUR, lw=1.2),
                )
                ax.text(xs[i] + 0.05, (p.energy + points[last_min_i].energy) / 2.0,
                        f"Ea = {ea:+.0f}",
                        ha="left", va="center", color=_ANNOT_COLOUR, fontsize=9)
        else:
            last_min_i = i


def _annotate_delta_h(ax, profile: ReactionEnergyProfile,
                      xs: List[float], ys: List[float]) -> None:
    """Draw a ΔH bracket from first to last minimum."""
    points = profile.points
    minima = [(i, p) for i, p in enumerate(points) if not p.is_ts]
    if len(minima) < 2:
        return
    i0, p0 = minima[0]
    i1, p1 = minima[-1]
    if p0.energy == p1.energy:
        return
    dh = p1.energy - p0.energy
    x_right = xs[i1] + 0.5
    ax.annotate(
        "", xy=(x_right, p1.energy), xytext=(x_right, p0.energy),
        arrowprops=dict(arrowstyle="<->", color=_WELL_COLOUR, lw=1.2),
    )
    ax.text(x_right + 0.08, (p0.energy + p1.energy) / 2.0,
            f"ΔH = {dh:+.0f} {profile.energy_unit.split('/')[0]}",
            ha="left", va="center", color=_WELL_COLOUR, fontsize=9)


def render_figure(profile: ReactionEnergyProfile,
                  width: int = 900, height: int = 540,
                  show_barriers: bool = True,
                  show_delta_h: bool = True,
                  title: str = "") -> "matplotlib.figure.Figure":
    """Build and return a matplotlib Figure for the profile.

    The caller is responsible for ``plt.close(fig)`` when done. Prefer
    :func:`export_profile` if you just want a file on disk.
    """
    if len(profile) < 2:
        raise RenderError("Energy profile needs at least 2 stationary points.")

    dpi = 100
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)

    curve_x, curve_y, xs, ys = _build_curve(profile.points)
    ax.plot(curve_x, curve_y, color=_CURVE_COLOUR, linewidth=2.3, zorder=2)

    # stationary-point markers
    for i, p in enumerate(profile.points):
        colour = _TS_COLOUR if p.is_ts else _MIN_COLOUR
        marker = "^" if p.is_ts else "o"
        ax.scatter([xs[i]], [ys[i]], c=colour, s=75, marker=marker,
                   zorder=4, edgecolors="white", linewidths=1.4)

    # labels
    y_range = (max(ys) - min(ys)) or 1.0
    pad = 0.055 * y_range
    for i, p in enumerate(profile.points):
        label = f"{p.label}{'‡' if p.is_ts and '‡' not in p.label else ''}"
        ax.text(xs[i], ys[i] + pad,
                label, ha="center", va="bottom",
                fontsize=10, color=_TS_COLOUR if p.is_ts else _MIN_COLOUR,
                fontweight="bold")
        if p.note:
            ax.text(xs[i], ys[i] - pad, p.note,
                    ha="center", va="top", fontsize=8, color="#666666")

    if show_barriers:
        _annotate_barriers(ax, profile.points, xs, ys)
    if show_delta_h:
        _annotate_delta_h(ax, profile, xs, ys)

    ax.set_xlabel("Reaction progress →", fontsize=11)
    ax.set_ylabel(f"Relative energy ({profile.energy_unit})", fontsize=11)
    ax.set_title(title or profile.title or "Reaction energy profile", fontsize=12)

    # cosmetic axes
    ax.set_xticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.4)

    # breathing room
    ax.set_xlim(-0.5, len(profile) - 0.5 + 1.2)  # right pad for ΔH label
    ax.set_ylim(min(ys) - 3 * pad, max(ys) + 3.5 * pad)

    # footer: source / unit
    if profile.source:
        fig.text(0.99, 0.02, f"Source: {profile.source}",
                 ha="right", va="bottom", fontsize=7, color="#888888")

    fig.tight_layout()
    return fig


def export_profile(profile: ReactionEnergyProfile, path: Union[str, Path],
                   width: int = 900, height: int = 540,
                   **kwargs) -> Path:
    """Render a profile to PNG / SVG. Format chosen by file extension."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suffix = p.suffix.lower().lstrip(".") or "png"
    if suffix not in ("png", "svg"):
        raise RenderError(
            f"Unsupported energy-profile output format {suffix!r}; use png or svg.")
    fig = render_figure(profile, width=width, height=height, **kwargs)
    try:
        fig.savefig(p, format=suffix, bbox_inches="tight", dpi=150 if suffix == "png" else None)
    finally:
        plt.close(fig)
    return p
