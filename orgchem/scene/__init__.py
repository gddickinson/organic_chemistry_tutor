"""Phase 32b — scene-graph composer for the dynamic Workbench viewer.

The Scene is a lightweight, headless-first **composable scene graph**:
a list of named Tracks plus a command log.  Tracks know what they
render (a small molecule, a protein, a ligand), their style, and
whether they're currently visible.  The Scene rebuilds a 3Dmol.js
HTML page from scratch on every mutation — simple, stateless, and
avoids the bidirectional JS command channel that would otherwise
need a QWebChannel bridge.

Entry points:

    from orgchem.scene import current_scene, Scene

    scene = current_scene()
    scene.add_molecule("CCO")
    scene.add_protein("2YDO")
    scene.snapshot("out.png")
    scene.clear()

The Workbench widget (``gui/panels/workbench.py``) listens for
``SceneEvent`` callbacks and re-renders its embedded 3Dmol.js page
whenever the scene changes.  Scripts that execute before the
Workbench is created still work — commands queue up, tracks
accumulate, and are replayed into the view on first attach.
"""
from orgchem.scene.scene import (
    Scene,
    SceneEvent,
    SceneListener,
    Track,
    current_scene,
    reset_current_scene,
)

__all__ = [
    "Scene",
    "SceneEvent",
    "SceneListener",
    "Track",
    "current_scene",
    "reset_current_scene",
]
