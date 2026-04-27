"""Phase BC-2.0 (round 219) — agent actions for the biochem
cofactors catalogue + a focused tab-opener that brings up the
new Cofactors tab on the existing BiochemMainWindow.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="biochem-cofactors")
def list_cofactors(
    cofactor_class: str = "",
) -> List[Dict[str, object]]:
    """Return cofactor catalogue entries, optionally filtered by
    class (one of: ``"nicotinamide"`` / ``"flavin"`` /
    ``"acyl-carrier"`` / ``"methyl-donor"`` / ``"phosphate-
    energy"`` / ``"biotin-vitamin"`` / ``"tpp-vitamin"`` /
    ``"plp-vitamin"`` / ``"lipoate"`` / ``"cobalamin-vitamin"``
    / ``"folate"`` / ``"metal-cluster"`` / ``"quinone"`` /
    ``"redox-buffer"``)."""
    from biochem.core.cofactors import (
        COFACTOR_CLASSES, cofactor_to_dict,
        list_cofactors as _list,
    )
    cc = (cofactor_class or "").strip()
    if cc and cc not in COFACTOR_CLASSES:
        return [{
            "error": f"Unknown cofactor_class {cc!r}; valid: "
                     f"{', '.join(COFACTOR_CLASSES)}.",
        }]
    return [cofactor_to_dict(c)
            for c in _list(cc or None)]


@action(category="biochem-cofactors")
def get_cofactor(cofactor_id: str) -> Dict[str, object]:
    """Return the full record for a single cofactor by id (e.g.
    ``"nad-plus"`` / ``"atp"`` / ``"acetyl-coa"`` / ``"sam"`` /
    ``"heme"`` / ``"glutathione"``)."""
    from biochem.core.cofactors import (
        cofactor_to_dict, get_cofactor,
    )
    c = get_cofactor(cofactor_id)
    if c is None:
        return {"error":
                f"Unknown cofactor id: {cofactor_id!r}."}
    return cofactor_to_dict(c)


@action(category="biochem-cofactors")
def find_cofactors(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    chemical summary + role / substrate / feature lists +
    vitamin-origin tags + deficiency diseases + notes +
    cross-reference molecule names."""
    from biochem.core.cofactors import (
        cofactor_to_dict, find_cofactors,
    )
    return [cofactor_to_dict(c) for c in find_cofactors(needle)]


@action(category="biochem-cofactors")
def cofactors_for_class(
    cofactor_class: str,
) -> List[Dict[str, object]]:
    """Return all cofactors in a single class."""
    from biochem.core.cofactors import (
        COFACTOR_CLASSES, cofactor_to_dict,
        cofactors_for_class,
    )
    if cofactor_class not in COFACTOR_CLASSES:
        return [{
            "error": f"Unknown cofactor_class {cofactor_class!r}; "
                     f"valid: {', '.join(COFACTOR_CLASSES)}.",
        }]
    return [cofactor_to_dict(c)
            for c in cofactors_for_class(cofactor_class)]


@action(category="biochem-cofactors")
def open_biochem_cofactors_tab() -> Dict[str, Any]:
    """Open the Biochem Studio main window + focus its
    *Cofactors* tab (added in Phase BC-2.0).  Same lazy-
    construction + main-thread-marshalling pattern as
    ``open_biochem_studio``.

    Returns ``{"opened": True, "tab": "Cofactors"}`` on
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
        from biochem.gui.windows.biochem_main_window import (
            BiochemMainWindow,
        )
        biochem_win = getattr(win, "_biochem_window", None)
        if biochem_win is None:
            biochem_win = BiochemMainWindow(parent=win)
            win._biochem_window = biochem_win
        biochem_win.show()
        biochem_win.raise_()
        biochem_win.activateWindow()
        ok = biochem_win.switch_to(
            BiochemMainWindow.TAB_COFACTORS)
        return {"opened": True,
                "tab": (BiochemMainWindow.TAB_COFACTORS
                        if ok else None)}

    return run_on_main_thread_sync(_open)
