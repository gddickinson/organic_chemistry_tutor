"""Phase 37c (round 138) — agent actions for the chromatography
methods catalogue.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="chromatography")
def list_chromatography_methods(
        category: str = "") -> List[Dict[str, str]]:
    """Return every catalogued chromatography method,
    optionally filtered by category (one of ``"planar"`` /
    ``"preparative-column"`` / ``"gas"`` / ``"liquid"`` /
    ``"protein"`` / ``"ion"`` / ``"supercritical"``)."""
    from orgchem.core.chromatography_methods import (
        VALID_CATEGORIES, list_methods, to_dict,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    return [to_dict(m) for m in list_methods(category=cat or None)]


@action(category="chromatography")
def get_chromatography_method(method_id: str) -> Dict[str, str]:
    """Return the full record for a single method by its id
    (e.g. ``"hplc"`` / ``"sec"`` / ``"sfc"``)."""
    from orgchem.core.chromatography_methods import (
        get_method, to_dict,
    )
    m = get_method(method_id)
    if m is None:
        return {"error":
                f"Unknown chromatography method id: {method_id!r}."}
    return to_dict(m)


@action(category="chromatography")
def find_chromatography_methods(
        needle: str) -> List[Dict[str, str]]:
    """Return every method matching the (case-insensitive)
    needle across name + abbreviation + id (e.g. ``"hplc"``,
    ``"protein"``, ``"gas"``)."""
    from orgchem.core.chromatography_methods import (
        find_methods, to_dict,
    )
    return [to_dict(m) for m in find_methods(needle)]


@action(category="chromatography")
def open_chromatography_methods(
        method_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Chromatography techniques…* dialog and
    optionally focus a specific method."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.chromatography_methods import (
            ChromatographyMethodsDialog,
        )
        dlg = ChromatographyMethodsDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if method_id:
            selected = dlg.select_method(method_id)
        return {
            "opened": True,
            "selected": selected,
            "method_id": method_id or None,
        }

    return run_on_main_thread_sync(_open)
