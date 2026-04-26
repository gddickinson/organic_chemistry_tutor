"""Phase 38b (round 141) — agent actions for the lab-setup
catalogue.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="lab")
def list_lab_setups() -> List[Dict[str, Any]]:
    """Return every catalogued canonical lab setup (simple
    distillation, fractional distillation, reflux, Soxhlet,
    vacuum filtration, liquid-liquid extraction,
    recrystallisation, …).  Each row carries the full setup
    record incl. ordered equipment list + connections."""
    from orgchem.core.lab_setups import list_setups, to_dict
    return [to_dict(s) for s in list_setups()]


@action(category="lab")
def get_lab_setup(setup_id: str) -> Dict[str, Any]:
    """Return the full record for a single lab setup."""
    from orgchem.core.lab_setups import get_setup, to_dict
    s = get_setup(setup_id)
    if s is None:
        return {"error": f"Unknown lab-setup id: {setup_id!r}."}
    return to_dict(s)


@action(category="lab")
def find_lab_setups(needle: str) -> List[Dict[str, Any]]:
    """Case-insensitive substring search over id + name +
    purpose."""
    from orgchem.core.lab_setups import find_setups, to_dict
    return [to_dict(s) for s in find_setups(needle)]


@action(category="lab")
def validate_lab_setup(setup_id: str) -> Dict[str, Any]:
    """Validate a setup's connections against the Phase-38a
    equipment / port catalogue.  Returns ``{"valid": True}``
    on a clean setup, ``{"valid": False, "errors": [...]}``
    on validation failures.  Useful for the future Phase-38c
    canvas to verify a user-built setup before they hit
    *Run simulation*."""
    from orgchem.core.lab_setups import get_setup, validate_setup
    s = get_setup(setup_id)
    if s is None:
        return {"error": f"Unknown lab-setup id: {setup_id!r}."}
    errs = validate_setup(s)
    return {"valid": not errs, "errors": errs}


@action(category="lab")
def open_lab_setups(setup_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Lab setups…* dialog and optionally
    focus a specific setup."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
        dlg = LabSetupsDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if setup_id:
            selected = dlg.select_setup(setup_id)
        return {
            "opened": True,
            "selected": selected,
            "setup_id": setup_id or None,
        }

    return run_on_main_thread_sync(_open)
