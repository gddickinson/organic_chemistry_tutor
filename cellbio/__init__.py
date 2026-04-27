"""Cell Biology Studio — sibling package to ``orgchem``.

**Phase CB-1.0** — first slice of the multi-studio life-sciences
platform.  Cell Bio Studio shares OrgChem's process: same Qt event
loop, same agent registry, same SQLite DB, same global glossary.
The only thing it adds is a new top-level QMainWindow with cell-
biology-specific catalogues, panels, and a tutorial track.

Importing ``cellbio`` triggers registration of cellbio's agent
actions into the shared registry — so headless drivers + the tutor
panel pick them up without any extra wiring.
"""
from __future__ import annotations

# Force agent-action registration on package import.  Same pattern
# that orgchem.agent.headless uses for orgchem's own actions.
from cellbio.agent import actions_signaling  # noqa: F401
# Phase CB-2.0 (round 218) — additive cell-cycle catalogue.
from cellbio.agent import actions_cell_cycle  # noqa: F401
