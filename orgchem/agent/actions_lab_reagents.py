"""Phase 45 (round 149) — agent actions for the lab-reagents
reference catalogue.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="reagent")
def list_lab_reagents(category: str = "") -> List[Dict[str, str]]:
    """Return every catalogued lab reagent, optionally filtered
    by category (one of: ``"buffer"`` / ``"acid-base"`` /
    ``"detergent"`` / ``"reducing-agent"`` / ``"salt"`` /
    ``"protein-prep"`` / ``"stain"`` / ``"solvent"`` /
    ``"cell-culture"`` / ``"molecular-biology"``)."""
    from orgchem.core.lab_reagents import (
        VALID_CATEGORIES, list_reagents, reagent_to_dict,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    return [reagent_to_dict(r) for r in list_reagents(cat or None)]


@action(category="reagent")
def get_lab_reagent(reagent_id: str) -> Dict[str, str]:
    """Return the full record for a single lab reagent by id
    (e.g. ``"tris-hcl"`` / ``"hepes"`` / ``"sds"`` /
    ``"dmso"``)."""
    from orgchem.core.lab_reagents import (
        get_reagent, reagent_to_dict,
    )
    r = get_reagent(reagent_id)
    if r is None:
        return {"error": f"Unknown lab-reagent id: "
                         f"{reagent_id!r}."}
    return reagent_to_dict(r)


@action(category="reagent")
def find_lab_reagents(needle: str) -> List[Dict[str, str]]:
    """Case-insensitive substring search across id + name +
    category + typical_usage + cas_number."""
    from orgchem.core.lab_reagents import (
        find_reagents, reagent_to_dict,
    )
    return [reagent_to_dict(r) for r in find_reagents(needle)]


@action(category="reagent")
def open_lab_reagents(reagent_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Lab reagents…* dialog and optionally
    focus a specific reagent by id."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.lab_reagents import (
            LabReagentsDialog,
        )
        dlg = LabReagentsDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if reagent_id:
            selected = dlg.select_reagent(reagent_id)
        return {
            "opened": True,
            "selected": selected,
            "reagent_id": reagent_id or None,
        }

    return run_on_main_thread_sync(_open)
