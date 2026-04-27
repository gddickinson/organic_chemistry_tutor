"""Phase BC-1.0 (round 213) — agent actions for the Biochem
Studio enzyme catalogue + the Biochem main-window opener.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="biochem-enzymes")
def list_enzymes(
    ec_class: int = 0,
) -> List[Dict[str, object]]:
    """Return enzymes in the BC-1.0 catalogue, optionally
    filtered by EC class (1 = oxidoreductase, 2 = transferase,
    3 = hydrolase, 4 = lyase, 5 = isomerase, 6 = ligase,
    7 = translocase).  ``ec_class=0`` = no filter (default).
    """
    from biochem.core.enzymes import (
        EC_CLASSES, enzyme_to_dict,
        list_enzymes as _list_enzymes,
    )
    cls: object = ec_class if ec_class > 0 else None
    if cls is not None and cls not in EC_CLASSES:
        return [{
            "error": f"Unknown EC class {ec_class!r}; "
                     f"valid: {EC_CLASSES}.",
        }]
    return [enzyme_to_dict(e)
            for e in _list_enzymes(ec_class=cls)]


@action(category="biochem-enzymes")
def get_enzyme(enzyme_id: str) -> Dict[str, object]:
    """Return the full record for a single enzyme by id
    (e.g. ``"chymotrypsin"`` / ``"hexokinase"`` /
    ``"hiv-protease"`` / ``"atp-synthase"`` / ``"acc"``).
    """
    from biochem.core.enzymes import enzyme_to_dict, get_enzyme
    e = get_enzyme(enzyme_id)
    if e is None:
        return {"error":
                f"Unknown enzyme id: {enzyme_id!r}."}
    return enzyme_to_dict(e)


@action(category="biochem-enzymes")
def find_enzymes(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    EC number + mechanism class + substrates / products /
    cofactors + disease associations + drug-target rows.
    """
    from biochem.core.enzymes import (
        enzyme_to_dict, find_enzymes,
    )
    return [enzyme_to_dict(e) for e in find_enzymes(needle)]


@action(category="biochem-enzymes")
def enzymes_for_ec_class(
    ec_class: int,
) -> List[Dict[str, object]]:
    """Return all enzymes of a given EC class (1-7)."""
    from biochem.core.enzymes import (
        EC_CLASSES, enzyme_to_dict, enzymes_for_ec_class,
    )
    if ec_class not in EC_CLASSES:
        return [{
            "error": f"Unknown EC class {ec_class!r}; "
                     f"valid: {EC_CLASSES}.",
        }]
    return [enzyme_to_dict(e)
            for e in enzymes_for_ec_class(ec_class)]


@action(category="biochem-enzymes")
def open_biochem_studio(tab: str = "") -> Dict[str, Any]:
    """Open the Biochem Studio main window (lazily constructed
    on first call).  Optional ``tab`` argument focuses one of
    the inner tabs (``"Enzymes"`` / ``"Metabolic pathways"`` /
    ``"Tutorials"``).  Returns
    ``{"opened": True, "tab": "<label or None>"}``.

    Phase BC-1.0 — second sibling in the multi-studio life-
    sciences platform (after Cell Bio Studio).  The Metabolic
    pathways tab surfaces ``orgchem.core.metabolic_pathways``
    read-only — validates the cross-studio data-sharing
    pattern.
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
        focused: Any = None
        if tab:
            ok = biochem_win.switch_to(tab)
            focused = tab if ok else None
        return {"opened": True, "tab": focused}

    return run_on_main_thread_sync(_open)
