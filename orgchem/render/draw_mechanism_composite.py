"""Phase 13c — full-kinetics composite mechanism renderer.

Where `draw_mechanism.render_step_svg` renders a *single* step, this
module stacks **every step** of a mechanism into one long SVG with
numbered step headers, titles, and descriptions. That's the format
students see in teaching figures like the canonical Schmidt-reaction
arrow-pushing diagram — a complete mechanism read top-to-bottom in
one glance.

Separate file from `draw_mechanism.py` so each stays under the 500-line
project cap; the two modules share no state.
"""
from __future__ import annotations
import logging
import re
from pathlib import Path
from typing import List, Union

from orgchem.core.mechanism import Mechanism
from orgchem.messaging.errors import RenderError
from orgchem.render.draw_mechanism import render_step_svg

log = logging.getLogger(__name__)


# Layout constants
_COMPOSITE_WIDTH = 820
_STEP_HEIGHT = 420
_HEADER_HEIGHT = 70      # per-step header band (numbered + title)
_FOOTER_HEIGHT = 90      # per-step description
_TITLE_BLOCK_HEIGHT = 90  # whole-mechanism title block at the top


def build_svg(mechanism: Mechanism, reaction_name: str = "") -> str:
    """Stack every mechanism step into a single composite SVG.

    Each step gets a numbered header ("Step 1:", "Step 2:" ...), a
    title line, the RDKit SVG body (curly/fishhook arrows included),
    and a wrapped description underneath. Read top to bottom.
    """
    steps = list(mechanism.steps)
    if not steps:
        raise RenderError("Mechanism has no steps to render.")

    block_height = _HEADER_HEIGHT + _STEP_HEIGHT + _FOOTER_HEIGHT
    total_height = _TITLE_BLOCK_HEIGHT + block_height * len(steps)

    parts: List[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{_COMPOSITE_WIDTH}" height="{total_height}" '
        f'viewBox="0 0 {_COMPOSITE_WIDTH} {total_height}">'
    )
    parts.append(_svg_style())
    parts.append(
        f'<rect width="{_COMPOSITE_WIDTH}" height="{total_height}" fill="white"/>'
    )

    # Top title block
    parts.append(
        f'<text x="30" y="40" class="mech-title">'
        f'{_esc(reaction_name or "Mechanism — full kinetics view")}</text>'
    )
    parts.append(
        f'<text x="30" y="68" class="mech-sub">'
        f'{len(steps)} step{"s" if len(steps) != 1 else ""} · '
        f'read top to bottom</text>'
    )

    # One block per step
    y_cursor = _TITLE_BLOCK_HEIGHT
    for i, step in enumerate(steps):
        parts.extend(_render_step_block(i, step, y_cursor))
        y_cursor += block_height

    parts.append('</svg>')
    return "\n".join(parts)


def export_composite(mechanism: Mechanism, path: Union[str, Path],
                     reaction_name: str = "") -> Path:
    """Write the composite to disk. SVG (preferred) or PNG (via Qt)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    svg = build_svg(mechanism, reaction_name=reaction_name)
    suffix = p.suffix.lower()
    if suffix == ".svg":
        p.write_text(svg)
    elif suffix in (".png", ".jpg", ".jpeg"):
        p.write_bytes(_svg_to_png_bytes(svg))
    else:
        raise RenderError(
            f"Unsupported composite extension: {suffix!r}. Use .svg or .png."
        )
    log.info("Exported composite mechanism → %s (%d bytes)",
             p, p.stat().st_size)
    return p


# ------------------------------------------------------------------
# Internals

def _render_step_block(step_index: int, step, y_top: int) -> List[str]:
    parts: List[str] = []
    hdr_y = y_top + 32

    # Step number + title
    parts.append(
        f'<text x="30" y="{hdr_y}" class="step-num">'
        f'Step {step_index + 1}</text>'
    )
    if step.title:
        parts.append(
            f'<text x="120" y="{hdr_y}" class="step-title">'
            f'{_esc(step.title)}</text>'
        )

    # Scheme with arrows — extract RDKit's body so we can embed inside
    # our outer <svg>.
    try:
        svg = render_step_svg(step,
                              width=_COMPOSITE_WIDTH - 60,
                              height=_STEP_HEIGHT)
        body = _extract_svg_body(svg)
        scheme_y = y_top + _HEADER_HEIGHT
        parts.append(
            f'<g transform="translate(30, {scheme_y})">{body}</g>'
        )
    except Exception as e:  # noqa: BLE001
        log.warning("Composite step %d render failed: %s", step_index, e)
        parts.append(
            f'<text x="30" y="{y_top + _HEADER_HEIGHT + 40}" '
            f'class="err">(could not render step: {_esc(str(e))})</text>'
        )

    # Wrapped description underneath
    foot_y = y_top + _HEADER_HEIGHT + _STEP_HEIGHT + 26
    if step.description:
        wrapped = _wrap(step.description, 95)
        for j, line in enumerate(wrapped.split("\n")):
            parts.append(
                f'<text x="30" y="{foot_y + j * 16}" '
                f'class="step-desc">{_esc(line)}</text>'
            )

    # Separator line between blocks
    sep_y = y_top + _HEADER_HEIGHT + _STEP_HEIGHT + _FOOTER_HEIGHT - 2
    parts.append(
        f'<line x1="30" y1="{sep_y}" x2="{_COMPOSITE_WIDTH - 30}" '
        f'y2="{sep_y}" stroke="#d0d0d0" stroke-width="1"/>'
    )
    return parts


def _svg_style() -> str:
    return (
        '<style>'
        '.mech-title { font-family: sans-serif; font-size: 20px; '
        'font-weight: bold; fill: #1a2b4a; }'
        '.mech-sub { font-family: sans-serif; font-size: 12px; '
        'fill: #666666; font-style: italic; }'
        '.step-num { font-family: sans-serif; font-size: 16px; '
        'font-weight: bold; fill: #1f4d9a; }'
        '.step-title { font-family: sans-serif; font-size: 15px; '
        'fill: #204060; }'
        '.step-desc { font-family: sans-serif; font-size: 12px; '
        'fill: #333333; }'
        '.err { font-family: sans-serif; font-size: 12px; fill: #b33; }'
        '</style>'
    )


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def _wrap(text: str, width: int) -> str:
    """Naïve word-wrap; good enough for single-paragraph descriptions."""
    if not text:
        return ""
    import textwrap
    return "\n".join(textwrap.wrap(text, width=width)) or text


def _extract_svg_body(svg: str) -> str:
    """Return the primitives *inside* an outer ``<svg>`` wrapper so the
    content can be dropped into another SVG's ``<g>``. Same as the
    pathway-renderer helper — Qt Svg Tiny 1.2 rejects nested <svg>."""
    body = re.sub(r"<\?xml[^?]*\?>", "", svg, count=1).lstrip()
    m = re.search(r"<svg[^>]*>", body, re.IGNORECASE | re.DOTALL)
    if m:
        body = body[m.end():]
    body = re.sub(r"</svg\s*>\s*$", "", body, flags=re.IGNORECASE)
    return body


def _svg_to_png_bytes(svg: str) -> bytes:
    """SVG → PNG via Qt's QSvgRenderer (no cairosvg dep)."""
    from PySide6.QtCore import QSize, QByteArray
    from PySide6.QtGui import QImage, QPainter, QColor
    from PySide6.QtSvg import QSvgRenderer
    from PySide6.QtWidgets import QApplication

    if QApplication.instance() is None:
        import os
        import sys
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        _ = QApplication(sys.argv)

    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    size = renderer.defaultSize() if not renderer.defaultSize().isEmpty() \
        else QSize(_COMPOSITE_WIDTH, _COMPOSITE_WIDTH)
    img = QImage(size, QImage.Format_ARGB32)
    img.fill(QColor("white"))
    painter = QPainter(img)
    renderer.render(painter)
    painter.end()
    ba = QByteArray()
    from PySide6.QtCore import QBuffer
    buf = QBuffer(ba)
    buf.open(QBuffer.WriteOnly)
    img.save(buf, "PNG")
    return bytes(ba.data())
