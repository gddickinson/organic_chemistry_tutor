"""Agent actions for Phase 30 secondary windows.

Exposes `open_macromolecules_window` so tutor chat / stdio bridge /
Python drivers can pop up the unified Macromolecules window and
optionally focus a specific inner tab.
"""
from __future__ import annotations
from typing import Any, Dict

from orgchem.agent.actions import action


_TABS = ("Proteins", "Carbohydrates", "Lipids", "Nucleic acids")


@action(category="window")
def open_macromolecules_window(tab: str = "") -> Dict[str, Any]:
    """Show the Macromolecules window (proteins / carbohydrates /
    lipids / nucleic-acids in one place). Pass ``tab`` as one of
    ``"Proteins"``, ``"Carbohydrates"``, ``"Lipids"``, or
    ``"Nucleic acids"`` to focus that inner tab.

    Safe to call from any thread — the actual widget instantiation
    is marshalled onto the Qt main thread via ``run_on_main_thread``
    because macOS crashes if any NSWindow is created off-main.
    """
    from orgchem.agent.controller import main_window
    from orgchem.agent._gui_dispatch import run_on_main_thread
    win = main_window()
    if win is None or not hasattr(win, "open_macromolecules_window"):
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}
    requested_tab = tab or _TABS[0]

    def _show():
        win.open_macromolecules_window(tab_label=tab or None)

    ok = run_on_main_thread(_show)
    return {
        "shown": ok,
        "active_tab": requested_tab,
        "tabs": list(_TABS),
    }
