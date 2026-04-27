"""Phase BT-2.0 (round 222) — agent actions for the Botany
plant-hormones catalogue + a focused tab-opener that brings up
the new Plant-hormones tab on BotanyMainWindow.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="botany-hormones")
def list_plant_hormones(
    hormone_class: str = "",
) -> List[Dict[str, object]]:
    """Return plant-hormone catalogue entries, optionally
    filtered by class (one of: ``"auxin"`` / ``"cytokinin"`` /
    ``"gibberellin"`` / ``"abscisic-acid"`` / ``"ethylene"`` /
    ``"brassinosteroid"`` / ``"jasmonate"`` /
    ``"salicylic-acid"`` / ``"strigolactone"`` /
    ``"peptide-hormone"``)."""
    from botany.core.plant_hormones import (
        HORMONE_CLASSES, plant_hormone_to_dict,
        list_plant_hormones as _list,
    )
    hc = (hormone_class or "").strip()
    if hc and hc not in HORMONE_CLASSES:
        return [{
            "error": f"Unknown hormone_class {hc!r}; valid: "
                     f"{', '.join(HORMONE_CLASSES)}.",
        }]
    return [plant_hormone_to_dict(h)
            for h in _list(hc or None)]


@action(category="botany-hormones")
def get_plant_hormone(hormone_id: str) -> Dict[str, object]:
    """Return the full record for a single plant hormone by id
    (e.g. ``"iaa"`` / ``"aba"`` / ``"ethylene"`` / ``"sa"`` /
    ``"jasmonic-acid"`` / ``"trans-zeatin"`` / ``"ga3"``)."""
    from botany.core.plant_hormones import (
        get_plant_hormone, plant_hormone_to_dict,
    )
    h = get_plant_hormone(hormone_id)
    if h is None:
        return {"error":
                f"Unknown plant-hormone id: {hormone_id!r}."}
    return plant_hormone_to_dict(h)


@action(category="botany-hormones")
def find_plant_hormones(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    structural class + biosynthesis precursor + perception +
    physiological effect + antagonisms + model plants + notes."""
    from botany.core.plant_hormones import (
        find_plant_hormones, plant_hormone_to_dict,
    )
    return [plant_hormone_to_dict(h)
            for h in find_plant_hormones(needle)]


@action(category="botany-hormones")
def plant_hormones_for_class(
    hormone_class: str,
) -> List[Dict[str, object]]:
    """Return all plant hormones in a single class."""
    from botany.core.plant_hormones import (
        HORMONE_CLASSES, plant_hormone_to_dict,
        plant_hormones_for_class,
    )
    if hormone_class not in HORMONE_CLASSES:
        return [{
            "error": f"Unknown hormone_class "
                     f"{hormone_class!r}; valid: "
                     f"{', '.join(HORMONE_CLASSES)}.",
        }]
    return [plant_hormone_to_dict(h)
            for h in plant_hormones_for_class(hormone_class)]


@action(category="botany-hormones")
def open_botany_plant_hormones_tab() -> Dict[str, Any]:
    """Open the Botany Studio main window + focus its
    *Plant hormones* tab (added in Phase BT-2.0).  Same lazy-
    construction + main-thread-marshalling pattern as
    ``open_botany_studio``.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from botany.gui.windows.botany_main_window import (
            BotanyMainWindow,
        )
        botany_win = getattr(win, "_botany_window", None)
        if botany_win is None:
            botany_win = BotanyMainWindow(parent=win)
            win._botany_window = botany_win
        botany_win.show()
        botany_win.raise_()
        botany_win.activateWindow()
        ok = botany_win.switch_to(
            BotanyMainWindow.TAB_PLANT_HORMONES)
        return {"opened": True,
                "tab": (BotanyMainWindow.TAB_PLANT_HORMONES
                        if ok else None)}

    return run_on_main_thread_sync(_open)
