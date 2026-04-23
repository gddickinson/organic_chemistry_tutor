"""Agent actions for Phase 30 secondary windows.

Exposes `open_macromolecules_window` so tutor chat / stdio bridge /
Python drivers can pop up the unified Macromolecules window and
optionally focus a specific inner tab.
"""
from __future__ import annotations
from typing import Any, Dict

from orgchem.agent.actions import action


@action(category="window")
def open_macromolecules_window(tab: str = "") -> Dict[str, Any]:
    """Show the Macromolecules window (proteins / carbohydrates /
    lipids / nucleic-acids in one place). Pass ``tab`` as one of
    ``"Proteins"``, ``"Carbohydrates"``, ``"Lipids"``, or
    ``"Nucleic acids"`` to focus that inner tab."""
    from orgchem.agent.controller import main_window
    win = main_window()
    if win is None or not hasattr(win, "open_macromolecules_window"):
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}
    mw = win.open_macromolecules_window(tab_label=tab or None)
    active = mw.tabs.tabText(mw.tabs.currentIndex())
    return {
        "shown": True,
        "active_tab": active,
        "tabs": [mw.tabs.tabText(i) for i in range(mw.tabs.count())],
    }
