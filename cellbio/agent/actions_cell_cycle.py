"""Phase CB-2.0 (round 218) — agent actions for the cell-cycle
catalogue + a focused tab-opener that brings up the new Cell-
cycle tab on the existing CellBioMainWindow.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="cellbio-cell-cycle")
def list_cell_cycle_entries(
    category: str = "",
) -> List[Dict[str, object]]:
    """Return cell-cycle catalogue entries, optionally filtered by
    category (one of: ``"phase"`` / ``"checkpoint"`` /
    ``"cyclin-cdk"`` / ``"cdk-inhibitor"`` / ``"pocket-protein"``
    / ``"mitotic-regulator"`` / ``"dna-damage-response"``)."""
    from cellbio.core.cell_cycle import (
        CATEGORIES, cell_cycle_entry_to_dict,
        list_cell_cycle_entries as _list,
    )
    c = (category or "").strip()
    if c and c not in CATEGORIES:
        return [{
            "error": f"Unknown category {c!r}; valid: "
                     f"{', '.join(CATEGORIES)}.",
        }]
    return [cell_cycle_entry_to_dict(e)
            for e in _list(c or None)]


@action(category="cellbio-cell-cycle")
def get_cell_cycle_entry(entry_id: str) -> Dict[str, object]:
    """Return the full record for a single cell-cycle entry by
    id (e.g. ``"g1-phase"`` / ``"cyclin-d-cdk4-cdk6"`` /
    ``"rb-e2f-axis"`` / ``"atm-kinase"`` /
    ``"spindle-assembly-checkpoint"``)."""
    from cellbio.core.cell_cycle import (
        cell_cycle_entry_to_dict, get_cell_cycle_entry,
    )
    e = get_cell_cycle_entry(entry_id)
    if e is None:
        return {"error":
                f"Unknown cell-cycle entry id: {entry_id!r}."}
    return cell_cycle_entry_to_dict(e)


@action(category="cellbio-cell-cycle")
def find_cell_cycle_entries(
    needle: str,
) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    summary + function + components + activator / inhibitor
    lists + disease associations + notes."""
    from cellbio.core.cell_cycle import (
        cell_cycle_entry_to_dict, find_cell_cycle_entries,
    )
    return [cell_cycle_entry_to_dict(e)
            for e in find_cell_cycle_entries(needle)]


@action(category="cellbio-cell-cycle")
def cell_cycle_entries_for_category(
    category: str,
) -> List[Dict[str, object]]:
    """Return all cell-cycle entries in a single category."""
    from cellbio.core.cell_cycle import (
        CATEGORIES, cell_cycle_entries_for_category,
        cell_cycle_entry_to_dict,
    )
    if category not in CATEGORIES:
        return [{
            "error": f"Unknown category {category!r}; valid: "
                     f"{', '.join(CATEGORIES)}.",
        }]
    return [cell_cycle_entry_to_dict(e)
            for e in cell_cycle_entries_for_category(category)]


@action(category="cellbio-cell-cycle")
def open_cellbio_cell_cycle_tab() -> Dict[str, Any]:
    """Open the Cell Bio Studio main window + focus its
    *Cell cycle* tab (added in Phase CB-2.0).  Same lazy-
    construction + main-thread-marshalling pattern as
    ``open_cellbio_studio``.

    Returns ``{"opened": True, "tab": "Cell cycle"}`` on
    success.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from cellbio.gui.windows.cellbio_main_window import (
            CellBioMainWindow,
        )
        cellbio_win = getattr(win, "_cellbio_window", None)
        if cellbio_win is None:
            cellbio_win = CellBioMainWindow(parent=win)
            win._cellbio_window = cellbio_win
        cellbio_win.show()
        cellbio_win.raise_()
        cellbio_win.activateWindow()
        ok = cellbio_win.switch_to(
            CellBioMainWindow.TAB_CELL_CYCLE)
        return {"opened": True,
                "tab": (CellBioMainWindow.TAB_CELL_CYCLE
                        if ok else None)}

    return run_on_main_thread_sync(_open)
