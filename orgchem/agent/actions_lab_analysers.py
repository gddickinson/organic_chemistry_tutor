"""Phase 40a (round 146) — agent actions for the major
lab-analysers catalogue.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="instrumentation")
def list_lab_analysers(category: str = "") -> List[Dict[str, str]]:
    """Return every catalogued major lab analyser, optionally
    filtered by category (one of: ``"clinical-chemistry"`` /
    ``"hematology"`` / ``"coagulation"`` / ``"immunoassay"`` /
    ``"molecular"`` / ``"mass-spec"`` / ``"functional"`` /
    ``"microscopy"`` / ``"automation"`` / ``"storage"``)."""
    from orgchem.core.lab_analysers import (
        VALID_CATEGORIES, list_analysers, to_dict,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    return [to_dict(a) for a in list_analysers(cat or None)]


@action(category="instrumentation")
def get_lab_analyser(analyser_id: str) -> Dict[str, str]:
    """Return the full record for a single lab analyser by id
    (e.g. ``"cobas_c702"`` / ``"sysmex_xn1000"`` /
    ``"illumina_novaseq_x"``)."""
    from orgchem.core.lab_analysers import get_analyser, to_dict
    a = get_analyser(analyser_id)
    if a is None:
        return {"error": f"Unknown lab-analyser id: "
                         f"{analyser_id!r}."}
    return to_dict(a)


@action(category="instrumentation")
def find_lab_analysers(needle: str) -> List[Dict[str, str]]:
    """Case-insensitive substring search across id + name +
    manufacturer + category."""
    from orgchem.core.lab_analysers import (
        find_analysers, to_dict,
    )
    return [to_dict(a) for a in find_analysers(needle)]


@action(category="instrumentation")
def open_lab_analysers(analyser_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Lab analysers…* dialog and optionally
    focus a specific analyser by id."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.lab_analysers import (
            LabAnalysersDialog,
        )
        dlg = LabAnalysersDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if analyser_id:
            selected = dlg.select_analyser(analyser_id)
        return {
            "opened": True,
            "selected": selected,
            "analyser_id": analyser_id or None,
        }

    return run_on_main_thread_sync(_open)
