"""Render a :class:`SynthesisPathway` as a vertical stack of step schemes.

Each step produces a single reaction SVG (via :func:`draw_reaction.render_svg`)
with the reagents text above the arrow and conditions below. The renderer
returns either:

- a composite SVG string that stacks all steps with step-number labels, OR
- a path on disk when :func:`export_pathway_png` is called.

The GUI panel consumes the SVG for display; the agent's
``export_pathway`` action uses the file-producing form.
"""
from __future__ import annotations
import io
import logging
import re
from pathlib import Path
from typing import List, Optional, Union

from orgchem.db.models import SynthesisPathway, SynthesisStep
from orgchem.render.draw_reaction import render_svg as _step_svg
from orgchem.messaging.errors import RenderError

log = logging.getLogger(__name__)


_STEP_WIDTH = 1100
_STEP_HEIGHT = 300
_HEADER_HEIGHT = 110   # title, reagents above the arrow
_FOOTER_HEIGHT = 60    # conditions + yield below


def build_svg(pathway: SynthesisPathway) -> str:
    """Return a single composite SVG representing the whole pathway."""
    steps = list(pathway.steps)
    if not steps:
        raise RenderError(f"Pathway {pathway.name!r} has no steps")

    block_height = _HEADER_HEIGHT + _STEP_HEIGHT + _FOOTER_HEIGHT
    total_height = 140 + block_height * len(steps)  # 140 = pathway header

    out: List[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{_STEP_WIDTH}" height="{total_height}" viewBox="0 0 '
        f'{_STEP_WIDTH} {total_height}">'
    )
    out.append(_svg_style())
    out.append(
        f'<rect width="{_STEP_WIDTH}" height="{total_height}" fill="white"/>'
    )
    # Pathway header
    out.append(
        f'<text x="30" y="44" class="pw-title">{_esc(pathway.name)}</text>'
    )
    subtitle = f"Target: {pathway.target_name}"
    if pathway.category:
        subtitle += f"   ·   {pathway.category}"
    if pathway.source:
        subtitle += f"   ·   {_esc(pathway.source)}"
    out.append(f'<text x="30" y="74" class="pw-sub">{_esc(subtitle)}</text>')
    if pathway.description:
        desc = _wrap(pathway.description, 110)
        out.append(
            f'<text x="30" y="104" class="pw-desc">{_esc(desc)}</text>'
        )

    # Steps
    y_cursor = 140
    for step in steps:
        out.extend(_render_step_block(step, y_cursor))
        y_cursor += block_height

    out.append('</svg>')
    return "\n".join(out)


def export_pathway(pathway: SynthesisPathway, path: Union[str, Path]) -> Path:
    """Export the pathway to *path*. Extension .svg or .png."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    svg = build_svg(pathway)
    if p.suffix.lower() == ".svg":
        p.write_text(svg)
    elif p.suffix.lower() in (".png", ".jpg", ".jpeg"):
        p.write_bytes(_svg_to_png_bytes(svg))
    else:
        raise RenderError(
            f"Unsupported extension: {p.suffix!r}. Use .svg or .png."
        )
    log.info("Exported pathway → %s (%d bytes)", p, p.stat().st_size)
    return p


# ----------------------------------------------------------------- internals

def _render_step_block(step: SynthesisStep, y_top: int) -> List[str]:
    parts: List[str] = []
    # Step header band
    hdr_y = y_top + 40
    parts.append(
        f'<text x="30" y="{hdr_y}" class="step-num">Step {step.step_index + 1}</text>'
    )
    if step.reagents:
        parts.append(
            f'<text x="150" y="{hdr_y}" class="step-reagents">'
            f'{_esc(step.reagents)}</text>'
        )

    # Step scheme — embed the reaction SVG's *body*. We can't nest a whole
    # <svg> inside our composite because Qt's SVG renderer is Svg Tiny 1.2
    # (no nested <svg>). Strip RDKit's outer wrapper and keep only the
    # drawing primitives.
    try:
        scheme = _step_svg(step.reaction_smiles,
                           width=_STEP_WIDTH - 60,
                           height=_STEP_HEIGHT)
        scheme = _extract_svg_body(scheme)
        scheme_y = y_top + _HEADER_HEIGHT
        parts.append(
            f'<g transform="translate(30, {scheme_y})">{scheme}</g>'
        )
    except Exception as e:  # noqa: BLE001
        log.warning("Failed to render step %d: %s", step.step_index, e)
        parts.append(
            f'<text x="30" y="{y_top + _HEADER_HEIGHT + 40}" '
            f'class="err">(could not render step: {_esc(str(e))})</text>'
        )

    # Footer: conditions + yield + notes
    footer_y = y_top + _HEADER_HEIGHT + _STEP_HEIGHT + 24
    foot_parts: List[str] = []
    if step.conditions:
        foot_parts.append(step.conditions)
    if step.yield_pct is not None:
        foot_parts.append(f"yield {step.yield_pct:.0f} %")
    if foot_parts:
        parts.append(
            f'<text x="30" y="{footer_y}" class="step-cond">'
            f'{_esc("   ·   ".join(foot_parts))}</text>'
        )
    if step.notes:
        notes = _wrap(step.notes, 110)
        parts.append(
            f'<text x="30" y="{footer_y + 22}" class="step-note">'
            f'{_esc(notes)}</text>'
        )

    # Visual separator between steps
    sep_y = y_top + _HEADER_HEIGHT + _STEP_HEIGHT + _FOOTER_HEIGHT
    parts.append(
        f'<line x1="30" y1="{sep_y}" x2="{_STEP_WIDTH - 30}" y2="{sep_y}" '
        f'stroke="#e0e0e0" stroke-width="1"/>'
    )
    return parts


def _svg_style() -> str:
    return (
        '<style>'
        '.pw-title { font: bold 22pt sans-serif; fill: #1a1a1a; }'
        '.pw-sub   { font: 12pt sans-serif; fill: #666; }'
        '.pw-desc  { font: 11pt sans-serif; fill: #444; }'
        '.step-num { font: bold 14pt sans-serif; fill: #2a5885; }'
        '.step-reagents { font: 12pt monospace; fill: #0b6b2b; }'
        '.step-cond { font: 11pt sans-serif; fill: #666; font-style: italic; }'
        '.step-note { font: 11pt sans-serif; fill: #444; }'
        '.err       { font: 12pt sans-serif; fill: #c03030; }'
        '</style>'
    )


def _wrap(text: str, width: int) -> str:
    """Crude single-line wrap (SVG text is single-line; we just truncate)."""
    text = " ".join(text.split())
    if len(text) <= width:
        return text
    return text[: width - 1] + "…"


def _esc(s: Optional[str]) -> str:
    if s is None:
        return ""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def _strip_xml_decl(svg: str) -> str:
    """Remove any ``<?xml ...?>`` prolog so the SVG can be embedded inside
    another SVG's <g>."""
    return re.sub(r"<\?xml[^?]*\?>", "", svg, count=1).lstrip()


def _extract_svg_body(svg: str) -> str:
    """Return the drawing primitives *inside* the outer ``<svg>`` tag,
    stripping the XML prolog and the wrapper. Needed because Qt's
    Svg Tiny 1.2 renderer rejects nested ``<svg>`` elements.
    """
    body = _strip_xml_decl(svg)
    m = re.search(r"<svg[^>]*>", body, re.IGNORECASE | re.DOTALL)
    if m:
        body = body[m.end():]
    # Strip the trailing </svg>
    body = re.sub(r"</svg\s*>\s*$", "", body, flags=re.IGNORECASE)
    return body


def _svg_to_png_bytes(svg: str) -> bytes:
    """SVG → PNG via Qt's QSvgRenderer (no cairosvg dep)."""
    from PySide6.QtCore import QSize, QByteArray
    from PySide6.QtGui import QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
    from PySide6.QtWidgets import QApplication

    if QApplication.instance() is None:
        import os, sys
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        _ = QApplication(sys.argv)

    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    size = renderer.defaultSize()
    if size.isEmpty():
        size = QSize(_STEP_WIDTH, _STEP_HEIGHT)
    img = QImage(size, QImage.Format_ARGB32)
    img.fill(0xFFFFFFFF)
    painter = QPainter(img)
    renderer.render(painter)
    painter.end()
    buf = QByteArray()
    from PySide6.QtCore import QBuffer
    qbuf = QBuffer(buf)
    qbuf.open(QBuffer.WriteOnly)
    img.save(qbuf, "PNG")
    return bytes(buf)
