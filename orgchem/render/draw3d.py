"""3D molecule rendering — builds self-contained HTML for embedding in a
``QWebEngineView`` via 3Dmol.js.

The viewer panel calls ``build_3dmol_html([molblock, ...])`` and hands the
resulting HTML to ``QWebEngineView.setHtml``. 3Dmol.js provides native
mouse-driven rotate / zoom / pick with no Qt OpenGL code.

Phase 20a: if a local copy of 3Dmol.js is present at
``orgchem/gui/assets/3Dmol-min.js``, its contents are **inlined** into the
HTML so the whole page is self-contained and the app works offline.
Use ``scripts/fetch_3dmol_js.py`` to download the bundle once. The CDN
URL stays as the default fallback.
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Optional

_3DMOL_CDN = "https://3dmol.org/build/3Dmol-min.js"
_LOCAL_ASSET_DIR = Path(__file__).resolve().parents[1] / "gui" / "assets"
_LOCAL_3DMOL_JS = _LOCAL_ASSET_DIR / "3Dmol-min.js"


def local_3dmol_available() -> bool:
    """True when a bundled 3Dmol.js exists locally."""
    return _LOCAL_3DMOL_JS.exists() and _LOCAL_3DMOL_JS.stat().st_size > 1000


def local_3dmol_path() -> Path:
    """Absolute path to the local 3Dmol.js asset (may not exist)."""
    return _LOCAL_3DMOL_JS

_HTML_TEMPLATE_CDN = """<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<script src="{js_src}"></script>
<style>
  html, body, #viewer {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
  body {{ background: {bg}; }}
</style>
</head><body><div id="viewer"></div>
<script>
  let v = $3Dmol.createViewer("viewer", {{ backgroundColor: "{bg}" }});
  {model_js}
  v.zoomTo();
  v.render();
</script></body></html>
"""

_HTML_TEMPLATE_INLINE = """<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<script>
{js_body}
</script>
<style>
  html, body, #viewer {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
  body {{ background: {bg}; }}
</style>
</head><body><div id="viewer"></div>
<script>
  let v = $3Dmol.createViewer("viewer", {{ backgroundColor: "{bg}" }});
  {model_js}
  v.zoomTo();
  v.render();
</script></body></html>
"""


def _style_spec(style: str) -> str:
    if style == "stick":
        return "{stick: {radius: 0.15}}"
    if style == "ball-and-stick":
        return "{stick: {radius: 0.12}, sphere: {scale: 0.25}}"
    if style == "sphere":
        return "{sphere: {scale: 0.35}}"
    if style == "line":
        return "{line: {}}"
    if style == "cartoon":
        return "{cartoon: {}}"
    return "{stick: {}}"


def _models_js(molblocks: List[str], style: str) -> str:
    parts: List[str] = []
    spec = _style_spec(style)
    for mb in molblocks:
        safe = mb.replace("\\", "\\\\").replace("`", "\\`")
        parts.append(f'v.addModel(`{safe}`, "mol");')
        parts.append(f'v.setStyle({{model: -1}}, {spec});')
    return "\n  ".join(parts)


def build_3dmol_html(molblocks: List[str], style: str = "stick",
                     background: str = "white",
                     js_src: Optional[str] = None,
                     prefer_local: bool = True) -> str:
    """Return a complete HTML document that renders *molblocks* with 3Dmol.js.

    By default (``prefer_local=True``) uses the locally-bundled
    ``orgchem/gui/assets/3Dmol-min.js`` if present — the whole HTML is
    self-contained and works offline. Falls back to the CDN URL (or the
    explicit ``js_src`` when passed).

    Pass ``prefer_local=False`` to force CDN use regardless of what's
    bundled (useful for size-constrained outputs).
    """
    model_js = _models_js(molblocks or [], style)
    if js_src is None and prefer_local and local_3dmol_available():
        return _HTML_TEMPLATE_INLINE.format(
            js_body=_LOCAL_3DMOL_JS.read_text(),
            bg=background,
            model_js=model_js,
        )
    return _HTML_TEMPLATE_CDN.format(
        js_src=js_src or _3DMOL_CDN,
        bg=background,
        model_js=model_js,
    )


def build_from_molecule(mol_obj, style: str = "stick") -> str:
    """Convenience: generate 3D if absent, then return HTML for that molecule."""
    mb = getattr(mol_obj, "molblock_3d", None)
    if not mb:
        mol_obj.generate_3d()
        mb = mol_obj.molblock_3d
    return build_3dmol_html([mb], style=style)
