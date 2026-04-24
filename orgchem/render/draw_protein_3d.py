"""3D protein structure viewer — Phase 24l.

Wraps a cached PDB file in a self-contained 3Dmol.js HTML page so the
Proteins tab (and any external caller) can show the full protein +
ligand interactively. Reuses the offline 3Dmol.js bundle from
Phase 20a: when ``orgchem/gui/assets/3Dmol-min.js`` exists the HTML
works without network access.

Default style choices (tuned for teaching):

- Protein chains: **cartoon**, chain-coloured.
- Ligand HETATMs (non-water, non-ion): **ball-and-stick**, coloured
  by element.
- Water / simple ions: hidden by default (too noisy for teaching).
- Optional **binding-site** highlight: residues named via
  ``highlight_residues`` get rendered as sticks + labels so the
  viewer can double as a binding-site inspector.
- Optional **surface** around the ligand for a pocket-view look.

The output is a single HTML string — feed it to
``QWebEngineView.setHtml`` in the GUI or write to disk for sharing.
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Sequence, Union

from orgchem.render.draw3d import (
    _3DMOL_CDN,
    _HTML_TEMPLATE_CDN,
    _HTML_TEMPLATE_INLINE,
    _LOCAL_3DMOL_JS,
    local_3dmol_available,
)


# ---------------------------------------------------------------------
# AlphaFold pLDDT colour gradient — Phase 24l follow-up.
# Values are bucket-midpoints used by the AlphaFold DB viewer.
# Source: https://alphafold.ebi.ac.uk (public colour scheme).
_PLDDT_COLOURS = [
    (90.0, "#0053d6"),   # very high (dark blue)
    (70.0, "#65cbf3"),   # confident (light blue / cyan)
    (50.0, "#ffdb13"),   # low (yellow)
    (0.0,  "#ff7d45"),   # very low (orange)
]


# ---------------------------------------------------------------------
# Picking — Phase 24l click-to-inspect.
#
# When ``enable_picking=True``, 3Dmol attaches a click handler to every
# protein atom. The handler (a) updates an in-page overlay label so the
# viewer is self-contained on its own, and (b) if the page is hosted
# inside a QWebEngineView with a QWebChannel bridge registered as
# ``qtBridge``, forwards the picked (chain, resn, resi) triple via
# ``qtBridge.onAtomPicked`` so the Qt side can update the Properties
# panel.
_PICK_LABEL_CSS = (
    "#pick-label {"
    " position: absolute; top: 8px; left: 8px; "
    " padding: 4px 10px; border-radius: 6px; "
    " background: rgba(0, 0, 0, 0.7); color: #fff; "
    " font-family: sans-serif; font-size: 13px; "
    " pointer-events: none; "
    "}"
)

_PICK_JS = """
var pickLabel = document.getElementById("pick-label");
var qtBridge = null;
if (typeof qt !== "undefined" && qt.webChannelTransport) {
  new QWebChannel(qt.webChannelTransport, function (channel) {
    qtBridge = channel.objects.qtBridge;
  });
}
v.setClickable({hetflag: false}, true, function (atom, viewer) {
  var chain = atom.chain || "";
  var resn = atom.resn || "";
  var resi = atom.resi || 0;
  var txt = chain + ":" + resn + resi + "  (atom " + (atom.atom || "") + ")";
  if (pickLabel) pickLabel.textContent = txt;
  if (qtBridge && qtBridge.onAtomPicked) {
    qtBridge.onAtomPicked(chain, resn, parseInt(resi, 10) || 0);
  }
});
"""


def _plddt_colourfunc_js() -> str:
    """JavaScript callback that maps an atom's B-factor (pLDDT in AF PDBs)
    to the AlphaFold DB colour bucket."""
    # Build: if (p > 90) return "#0053d6"; else if (p > 70) return ...
    clauses = []
    for cutoff, colour in _PLDDT_COLOURS[:-1]:
        clauses.append(f'if (p > {cutoff}) return "{colour}";')
    last = _PLDDT_COLOURS[-1][1]
    clauses.append(f'return "{last}";')
    body = " else ".join(clauses)
    return (
        "function(atom) { "
        "var p = atom.b; "
        f"{body} "
        "}"
    )


# ---------------------------------------------------------------------

def _escape_backticks(text: str) -> str:
    return text.replace("\\", "\\\\").replace("`", "\\`")


def _selection_js(highlight_residues: Sequence[str]) -> str:
    """Build a JS array literal listing the residues to highlight as sticks.

    Each entry is ``"CHAIN:RESNAME+RESNUM"`` (e.g. ``"A:ASP102"``) or
    just ``"RESNAME+RESNUM"`` (treat as any chain). Used to translate
    to 3Dmol.js selection dicts.
    """
    entries: List[str] = []
    for token in highlight_residues:
        token = token.strip()
        if not token:
            continue
        chain = ""
        rest = token
        if ":" in token:
            chain, rest = token.split(":", 1)
        # Split "ASP102" into resn="ASP" + resi=102.
        resn = ""
        resi = ""
        for i, c in enumerate(rest):
            if c.isdigit():
                resn = rest[:i]
                resi = rest[i:]
                break
        entry = "{"
        if resn:
            entry += f'resn: "{resn}"'
        if resi:
            entry += (", " if entry != "{" else "") + f"resi: {resi}"
        if chain:
            entry += (", " if entry != "{" else "") + f'chain: "{chain}"'
        entry += "}"
        entries.append(entry)
    return "[" + ", ".join(entries) + "]"


def _build_model_js(pdb_text: str,
                    protein_style: str,
                    ligand_style: str,
                    highlight_residues: Sequence[str],
                    show_ligand_surface: bool,
                    show_waters: bool,
                    colour_mode: str = "chain",
                    enable_picking: bool = False,
                    spin: bool = False,
                    spin_axis: str = "y",
                    spin_speed: float = 1.0) -> str:
    """Assemble the in-page JS that loads and styles the PDB.

    ``colour_mode`` selects the protein colouring strategy:
    - ``"chain"`` — each chain gets a distinct colour (default).
    - ``"plddt"`` — AlphaFold DB gradient over the B-factor
      (pLDDT) column: dark blue (>90) → cyan (70-90) → yellow
      (50-70) → orange (<50).
    """
    safe_pdb = _escape_backticks(pdb_text)
    hl_js = _selection_js(highlight_residues)

    lines: List[str] = []
    lines.append(f'v.addModel(`{safe_pdb}`, "pdb");')

    # Decide the protein-colour directive.
    if colour_mode == "plddt":
        colour_spec = f'colorfunc: {_plddt_colourfunc_js()}'
    else:
        colour_spec = 'colorscheme: "chain"'

    # Protein backbone
    if protein_style == "cartoon":
        lines.append(
            f'v.setStyle({{hetflag: false}}, '
            f'{{cartoon: {{{colour_spec}}}}});'
        )
    elif protein_style == "surface":
        lines.append(
            f'v.setStyle({{hetflag: false}}, '
            f'{{cartoon: {{{colour_spec}, opacity: 0.6}}}});'
        )
        lines.append('v.addSurface($3Dmol.SurfaceType.VDW, '
                     '{opacity: 0.35, color: "white"}, {hetflag: false});')
    elif protein_style == "trace":
        lines.append(
            f'v.setStyle({{hetflag: false}}, '
            f'{{cartoon: {{style: "trace", {colour_spec}}}}});'
        )
    else:
        lines.append('v.setStyle({hetflag: false}, {cartoon: {}});')

    # Waters / ions
    if not show_waters:
        lines.append('v.setStyle({resn: ["HOH", "WAT", "DOD"]}, {});')

    # Ligands (HETATMs other than water/ions)
    ignore = '["HOH", "WAT", "DOD", "NA", "K", "MG", "CA", "ZN", "FE", "MN", "CL"]'
    if ligand_style == "ball-and-stick":
        lines.append(
            f'v.setStyle({{hetflag: true, not: {{resn: {ignore}}}}}, '
            '{stick: {colorscheme: "Jmol"}, sphere: {scale: 0.25}});'
        )
    elif ligand_style == "stick":
        lines.append(
            f'v.setStyle({{hetflag: true, not: {{resn: {ignore}}}}}, '
            '{stick: {colorscheme: "Jmol", radius: 0.18}});'
        )
    elif ligand_style == "sphere":
        lines.append(
            f'v.setStyle({{hetflag: true, not: {{resn: {ignore}}}}}, '
            '{sphere: {scale: 0.35, colorscheme: "Jmol"}});'
        )

    # Highlighted residues
    if highlight_residues:
        lines.append(f'var hl = {hl_js};')
        lines.append(
            'hl.forEach(function(sel) { v.setStyle(sel, '
            '{stick: {colorscheme: "yellowCarbon", radius: 0.2}}); '
            'v.addResLabels(sel, {fontSize: 11, '
            'backgroundColor: "black", backgroundOpacity: 0.7}); });'
        )

    # Optional ligand surface (pocket viz)
    if show_ligand_surface:
        lines.append(
            f'v.addSurface($3Dmol.SurfaceType.VDW, '
            '{opacity: 0.6, color: "white"}, '
            f'{{hetflag: true, not: {{resn: {ignore}}}}});'
        )

    if enable_picking:
        lines.append(_PICK_JS.strip())

    # Phase 34c — expose a global JS helper `orgchemHighlight` so the
    # Qt side can push a sequence-bar selection into the live 3D
    # viewer via `page.runJavaScript(...)` without re-rendering the
    # whole HTML.  Clears any previous overlay before applying the
    # new one.  Safe no-op when called with invalid args.
    lines.append(_LIVE_HIGHLIGHT_JS.strip())

    if spin:
        # 3Dmol.js: v.spin(axis, speed) — axis ∈ {"x", "y", "z"},
        # speed in degrees per frame. Called last so the rendered
        # scene is already composed.
        axis = spin_axis if spin_axis in ("x", "y", "z") else "y"
        lines.append(f'v.spin("{axis}", {float(spin_speed)});')

    return "\n  ".join(lines)


#: Phase 34c — JS helper for live sequence→3D highlighting.
#: Exposes `window.orgchemHighlight(chainId, start, end)` and
#: `window.orgchemClearHighlight()`.  The helper resets the sticks
#: applied by the previous call (tracked via a module-level pair),
#: then stick-highlights every residue in the [start, end] range
#: on `chainId` in yellow-carbon + labels them, mirroring the
#: static `highlight_residues` pipeline.
_LIVE_HIGHLIGHT_JS = """
window.__orgchemActiveHighlight = null;
window.orgchemClearHighlight = function () {
  var prev = window.__orgchemActiveHighlight;
  if (prev && prev.chain && typeof prev.start === "number") {
    // Reset the previous span's style to cartoon-only
    // (`{}` = inherit default protein style).
    v.setStyle({chain: prev.chain, resi: prev.resi},
               {cartoon: {}});
    v.removeAllLabels();
    v.render();
    window.__orgchemActiveHighlight = null;
  }
};
window.orgchemHighlight = function (chainId, start, end) {
  try {
    if (!chainId) return;
    var s = parseInt(start, 10);
    var e = parseInt(end, 10);
    if (isNaN(s) || isNaN(e)) return;
    if (s > e) { var tmp = s; s = e; e = tmp; }
    window.orgchemClearHighlight();
    var resiRange = [];
    for (var i = s; i <= e; i++) resiRange.push(i);
    var sel = {chain: String(chainId), resi: resiRange};
    v.setStyle(sel, {
      stick: {colorscheme: "yellowCarbon", radius: 0.2},
      cartoon: {},
    });
    v.addResLabels(sel, {fontSize: 11, backgroundColor: "black",
                         backgroundOpacity: 0.7});
    v.render();
    window.__orgchemActiveHighlight = {chain: chainId, resi: resiRange};
  } catch (err) {
    // Swallow — a bad selection shouldn't crash the viewer.
    console && console.warn && console.warn("orgchemHighlight: " + err);
  }
};
"""


# ---------------------------------------------------------------------
# Public API

def build_protein_html(pdb_text: str,
                       protein_style: str = "cartoon",
                       ligand_style: str = "ball-and-stick",
                       highlight_residues: Optional[Sequence[str]] = None,
                       show_ligand_surface: bool = False,
                       show_waters: bool = False,
                       background: str = "white",
                       prefer_local: bool = True,
                       js_src: Optional[str] = None,
                       colour_mode: str = "chain",
                       enable_picking: bool = False,
                       spin: bool = False,
                       spin_axis: str = "y",
                       spin_speed: float = 1.0,
                       ) -> str:
    """Return a self-contained HTML document rendering a PDB structure.

    ``highlight_residues`` accepts entries like ``"A:ASP102"``,
    ``"ARG195"``, or just ``"TYR"``. Matching residues get a
    yellow-carbon stick overlay plus a text label — handy when the
    Protein tab uses this view to visualise a binding site.

    ``colour_mode`` chooses how protein atoms are coloured:
    ``"chain"`` (default) gives each chain a distinct colour;
    ``"plddt"`` reads the B-factor column as AlphaFold pLDDT and
    applies the AlphaFold DB gradient (dark blue ≥ 90, cyan ≥ 70,
    yellow ≥ 50, orange < 50).

    ``enable_picking=True`` (Phase 24l follow-up) attaches a 3Dmol
    click handler to every protein atom. Clicking shows the
    residue identity (chain:resn+resi) in an overlay label; if the
    page is hosted inside a QWebEngineView with a QWebChannel bridge
    registered as ``qtBridge``, the same info is forwarded to the
    Qt side via ``qtBridge.onAtomPicked(chain, resn, resi)``.

    ``spin=True`` (Phase 24l follow-up) auto-rotates the rendered
    scene around ``spin_axis`` (x / y / z, default y) at
    ``spin_speed`` degrees per frame. Great for exporting a
    self-contained rotation animation HTML — no user interaction
    required.
    """
    hl = tuple(highlight_residues or ())
    model_js = _build_model_js(pdb_text, protein_style=protein_style,
                               ligand_style=ligand_style,
                               highlight_residues=hl,
                               show_ligand_surface=show_ligand_surface,
                               show_waters=show_waters,
                               colour_mode=colour_mode,
                               enable_picking=enable_picking,
                               spin=spin, spin_axis=spin_axis,
                               spin_speed=spin_speed)
    if js_src is None and prefer_local and local_3dmol_available():
        html = _HTML_TEMPLATE_INLINE.format(
            js_body=_LOCAL_3DMOL_JS.read_text(),
            bg=background, model_js=model_js,
        )
    else:
        html = _HTML_TEMPLATE_CDN.format(
            js_src=js_src or _3DMOL_CDN,
            bg=background, model_js=model_js,
        )
    if enable_picking:
        html = _inject_picking_scaffolding(html)
    return html


def _inject_picking_scaffolding(html: str) -> str:
    """Splice the CSS overlay, pick-label div, and qwebchannel.js
    script reference into the viewer HTML."""
    # CSS
    html = html.replace(
        "</style>", _PICK_LABEL_CSS + "\n</style>", 1
    )
    # Pick-label div — placed after the viewer div.
    html = html.replace(
        '<div id="viewer"></div>',
        '<div id="viewer"></div>'
        '<div id="pick-label">click a residue…</div>',
        1,
    )
    # QWebChannel loader — Qt ships this at qrc:///qtwebchannel/
    # and it no-ops cleanly when the page isn't inside a
    # QWebEngineView (the `qt` global stays undefined).
    qwc = (
        '<script src="qrc:///qtwebchannel/qwebchannel.js"></script>\n'
    )
    html = html.replace("</head>", qwc + "</head>", 1)
    return html


def build_protein_html_from_file(pdb_path: Union[str, Path],
                                 **kwargs) -> str:
    p = Path(pdb_path)
    if not p.exists():
        raise FileNotFoundError(f"No PDB file at {p}")
    return build_protein_html(p.read_text(encoding="utf-8"), **kwargs)


def export_protein_html(pdb_text: str, out_path: Union[str, Path],
                        **kwargs) -> Path:
    """Write the viewer HTML to ``out_path`` and return the absolute path."""
    html = build_protein_html(pdb_text, **kwargs)
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    return p.resolve()
