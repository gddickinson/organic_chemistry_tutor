"""Agent actions for Phase 12a — IUPAC nomenclature rule catalogue."""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="naming")
def list_naming_rules(category: str = "") -> List[Dict[str, str]]:
    """Enumerate IUPAC naming rules, optionally filtered by category."""
    from orgchem.naming import list_rules
    return list_rules(category=category)


@action(category="naming")
def get_naming_rule(rule_id: str) -> Dict[str, str]:
    """Return full detail (description, examples, pitfalls) for one naming rule."""
    from orgchem.naming import get_rule
    return get_rule(rule_id)


@action(category="naming")
def naming_rule_categories() -> List[str]:
    """Distinct categories present in the catalogue (alkanes, aromatics, …)."""
    from orgchem.naming import rule_categories
    return rule_categories()


@action(category="naming")
def open_naming_rules() -> Dict[str, Any]:
    """Open the *Tools → IUPAC naming rules…* dialog.  Returns
    ``{"opened": True}`` on success or ``{"error": ...}`` if the
    main window isn't reachable (e.g. headless without a GUI)."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.naming_rules import (
            NamingRulesDialog,
        )
        dlg = NamingRulesDialog(win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        return {"opened": True}

    return run_on_main_thread_sync(_open)
