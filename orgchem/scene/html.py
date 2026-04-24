"""Phase 32b — HTML page builder for the Workbench scene.

Produces a complete, self-contained 3Dmol.js page that renders
every visible track in the :class:`~orgchem.scene.Scene`.  Reuses
the bundled local 3Dmol.js asset from :mod:`orgchem.render.draw3d`
when available; falls back to the CDN.

Kept separate from :mod:`orgchem.render.draw3d` so the scene's
multi-model assembly logic doesn't pollute the single-target path.
"""
from __future__ import annotations

import json
from typing import List

from orgchem.render.draw3d import (
    _3DMOL_CDN,
    _HTML_TEMPLATE_CDN,
    _HTML_TEMPLATE_INLINE,
    _LOCAL_3DMOL_JS,
    local_3dmol_available,
)
from orgchem.scene.scene import Scene, Track, TrackKind


def _style_js(track: Track) -> str:
    """3Dmol.js style selector block for a single track.

    Returned as a JS object literal passed to ``v.setStyle`` /
    ``v.addStyle``.  Built programmatically (dict → ``json.dumps``)
    so we can inject ``opacity`` + colour choices for every
    style consistently — Phase 32c+ round 85.
    """
    style = track.style.lower()
    colour = track.colour.lower()
    opacity = float(track.opacity)

    # Combined two-key style: ball-and-stick draws BOTH sticks and
    # spheres, so we have to set both inner dicts consistently.
    if style == "ball-and-stick":
        stick_inner = {"radius": 0.12}
        sphere_inner = {"scale": 0.25}
        if opacity < 1.0:
            stick_inner["opacity"] = opacity
            sphere_inner["opacity"] = opacity
        return json.dumps({"stick": stick_inner, "sphere": sphere_inner})

    # Map style name → (3Dmol.js key, default params).
    if style in ("cartoon", "trace"):
        key = "cartoon"
        inner = {} if style == "cartoon" else {"style": "trace"}
        # Protein-level colour variants.
        if colour == "chain":
            inner["colorscheme"] = "chainbow"
        elif colour == "spectrum":
            inner["color"] = "spectrum"
        elif colour == "residue":
            inner["colorscheme"] = "amino"
        # "cpk" is the default — leave inner untouched.
    elif style == "surface":
        key = "surface"
        # Surface gets a softer default (0.6) when no override —
        # otherwise follow the track's opacity field exactly.
        inner = {"opacity": opacity if opacity != 1.0 else 0.6}
        return json.dumps({key: inner})
    elif style == "stick":
        key, inner = "stick", {"radius": 0.15}
    elif style == "sphere":
        key, inner = "sphere", {"scale": 0.35}
    elif style == "line":
        key, inner = "line", {}
    else:
        key, inner = "stick", {}

    if opacity < 1.0:
        inner["opacity"] = opacity
    return json.dumps({key: inner})


def _models_js_for_scene(tracks: List[Track]) -> str:
    """Serialise every visible track to a stream of
    ``v.addModel`` + ``v.setStyle`` calls."""
    parts: List[str] = []
    for t in tracks:
        if not t.visible:
            continue
        # JSON-encode the data so it's safe inside a JS template
        # literal regardless of newlines / backticks / unicode.
        payload = json.dumps(t.data)
        fmt = json.dumps(t.source_format)
        parts.append(f'v.addModel({payload}, {fmt});')
        parts.append(f'v.setStyle({{model: -1}}, {_style_js(t)});')
        # For proteins that also have ligands (HETATM), add a stick
        # overlay so ligands aren't invisible in cartoon mode.
        if t.kind == TrackKind.PROTEIN:
            parts.append(
                'v.setStyle({model: -1, hetflag: true}, '
                '{stick: {radius: 0.2}, sphere: {scale: 0.25}});'
            )
    if not parts:
        # Empty scene — avoid the zoomTo/render that 3Dmol.js trips on.
        parts.append('v.addLabel("Scene empty — add a track to begin.", '
                     '{position: {x:0, y:0, z:0}, backgroundColor: "#111", '
                     'fontColor: "#ccc"});')
    return "\n  ".join(parts)


def build_scene_html(scene: Scene, background: str = "#1e1e1e") -> str:
    """Return a complete HTML document for the current scene."""
    model_js = _models_js_for_scene(scene.tracks())
    if local_3dmol_available():
        return _HTML_TEMPLATE_INLINE.format(
            js_body=_LOCAL_3DMOL_JS.read_text(),
            bg=background,
            model_js=model_js,
        )
    return _HTML_TEMPLATE_CDN.format(
        js_src=_3DMOL_CDN,
        bg=background,
        model_js=model_js,
    )
