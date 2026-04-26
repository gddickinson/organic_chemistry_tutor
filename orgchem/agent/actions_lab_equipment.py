"""Phase 38a (round 140) — agent actions for the lab-equipment
catalogue.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="lab")
def list_lab_equipment(category: str = "") -> List[Dict[str, Any]]:
    """Return every catalogued lab-equipment entry, optionally
    filtered by category (one of: ``"glassware"`` /
    ``"adapter"`` / ``"condenser"`` / ``"heating"`` /
    ``"cooling"`` / ``"separation"`` / ``"filtration"`` /
    ``"vacuum"`` / ``"stirring"`` / ``"support"`` /
    ``"safety"`` / ``"analytical"``)."""
    from orgchem.core.lab_equipment import (
        VALID_CATEGORIES, list_equipment, to_dict,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    return [to_dict(e) for e in list_equipment(category=cat or None)]


@action(category="lab")
def get_lab_equipment(equipment_id: str) -> Dict[str, Any]:
    """Return the full record for a single piece of lab
    equipment by id (e.g. ``"rbf"``, ``"liebig_condenser"``,
    ``"sep_funnel"``)."""
    from orgchem.core.lab_equipment import get_equipment, to_dict
    e = get_equipment(equipment_id)
    if e is None:
        return {"error":
                f"Unknown lab-equipment id: {equipment_id!r}."}
    return to_dict(e)


@action(category="lab")
def find_lab_equipment(needle: str) -> List[Dict[str, Any]]:
    """Return every piece of equipment matching the
    (case-insensitive) needle across name + category + id."""
    from orgchem.core.lab_equipment import find_equipment, to_dict
    return [to_dict(e) for e in find_equipment(needle)]


@action(category="lab")
def open_lab_equipment(equipment_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Lab equipment…* dialog and optionally
    focus a specific item."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.lab_equipment import (
            LabEquipmentDialog,
        )
        dlg = LabEquipmentDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if equipment_id:
            selected = dlg.select_equipment(equipment_id)
        return {
            "opened": True,
            "selected": selected,
            "equipment_id": equipment_id or None,
        }

    return run_on_main_thread_sync(_open)
