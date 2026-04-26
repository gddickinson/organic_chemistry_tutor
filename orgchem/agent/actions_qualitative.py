"""Phase 37a (round 136) — agent actions for the qualitative
inorganic-test catalogue.

Three actions exposed to the tutor / scripts / stdio bridge:

- ``list_inorganic_tests(category="")`` — every entry, filtered
  by category if given.
- ``get_inorganic_test(test_id)`` — full detail for one entry.
- ``find_inorganic_tests_for(target)`` — every test matching an
  ion or gas (e.g. ``"Cu²⁺"`` / ``"Cu2+"`` / ``"Cl-"`` —
  case + sub/superscript tolerant).
- ``open_qualitative_tests(test_id="")`` — open the *Tools →
  Qualitative inorganic tests…* dialog, optionally focusing
  a specific entry.

The lookup actions are pure-headless; the dialog opener
marshals onto the Qt main thread.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="qualitative")
def list_inorganic_tests(category: str = "") -> List[Dict[str, str]]:
    """Return every catalogued qualitative-inorganic-test entry,
    optionally filtered by ``category`` (one of: ``"flame"``,
    ``"hydroxide"``, ``"halide"``, ``"sulfate"``, ``"carbonate"``,
    ``"ammonium"``, ``"gas"``).  Empty string returns the full
    catalogue.
    """
    from orgchem.core.qualitative_tests import (
        list_tests, to_dict, VALID_CATEGORIES,
    )
    cat: str = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    rows = list_tests(category=cat or None)
    return [to_dict(t) for t in rows]


@action(category="qualitative")
def get_inorganic_test(test_id: str) -> Dict[str, str]:
    """Return the full record for a single qualitative-test
    entry by its id (e.g. ``"flame-na"`` / ``"hydroxide-cu2"``)."""
    from orgchem.core.qualitative_tests import get_test, to_dict
    t = get_test(test_id)
    if t is None:
        return {"error": f"Unknown qualitative-test id: {test_id!r}."}
    return to_dict(t)


@action(category="qualitative")
def find_inorganic_tests_for(target: str) -> List[Dict[str, str]]:
    """Return every test whose target matches *target* (an ion
    or gas, e.g. ``"Cu²⁺"`` / ``"Cu2+"`` / ``"CO2"``).  Lookup
    is case + sub/superscript tolerant — the user can type the
    plain-ASCII form on a keyboard."""
    from orgchem.core.qualitative_tests import find_tests_for, to_dict
    rows = find_tests_for(target)
    return [to_dict(t) for t in rows]


@action(category="qualitative")
def open_qualitative_tests(test_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Qualitative inorganic tests…* dialog
    and, if ``test_id`` is given, focus that entry.  Returns
    ``{"opened": True, "selected": <bool>}`` on success or
    ``{"error": ...}`` when the GUI isn't reachable."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.qualitative_tests import (
            QualitativeTestsDialog,
        )
        dlg = QualitativeTestsDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if test_id:
            selected = dlg.select_test(test_id)
        return {"opened": True, "selected": selected,
                "test_id": test_id or None}

    return run_on_main_thread_sync(_open)
