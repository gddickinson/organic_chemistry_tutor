"""Agent actions for Phase 27 — periodic table (round 35)."""
from __future__ import annotations
from typing import Any, Dict, List

from orgchem.agent.actions import action


@action(category="periodic")
def list_elements() -> List[Dict[str, Any]]:
    """All 118 elements with symbol, Z, period, group, category,
    atomic mass, electronegativity, common oxidation states."""
    from orgchem.core.periodic_table import list_elements as _list
    return _list()


@action(category="periodic")
def get_element(symbol_or_z: str) -> Dict[str, Any]:
    """Look up an element by symbol (case-insensitive) or Z."""
    from orgchem.core.periodic_table import get_element as _get
    e = _get(symbol_or_z)
    if e is None:
        return {"error": f"Unknown element: {symbol_or_z!r}"}
    return e.to_dict()


@action(category="periodic")
def elements_by_category(category: str) -> List[Dict[str, Any]]:
    """Filter the table by category — e.g. ``halogen``,
    ``noble-gas``, ``transition-metal``, ``lanthanide``."""
    from orgchem.core.periodic_table import elements_by_category as _by
    return [e.to_dict() for e in _by(category)]


@action(category="periodic")
def open_periodic_table() -> Dict[str, Any]:
    """Open the *Tools → Periodic table…* dialog (Ctrl+Shift+T).
    Returns ``{"opened": True}`` on success or ``{"error": ...}``
    if the main window isn't reachable."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.periodic_table import (
            PeriodicTableDialog,
        )
        dlg = PeriodicTableDialog(win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        return {"opened": True}

    return run_on_main_thread_sync(_open)
