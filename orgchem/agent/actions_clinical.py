"""Phase 37b (round 137) — agent actions for the clinical-
chemistry lab-panel catalogue.

Five actions:

- ``list_lab_panels()`` — every panel summary.
- ``get_lab_panel(panel_id)`` — full panel record incl.
  every analyte's normal range + significance.
- ``list_lab_analytes(category="")`` — every analyte across
  every panel, deduplicated, optionally filtered by category.
- ``find_lab_analyte(needle)`` — case-insensitive name /
  abbreviation / id lookup.
- ``open_clinical_panels(panel_id="", analyte_id="")`` — open
  the *Tools → Clinical lab panels…* dialog and optionally
  focus a specific panel + analyte.

Lookup actions are pure-headless; the dialog opener marshals
onto the Qt main thread.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="clinical")
def list_lab_panels() -> List[Dict[str, str]]:
    """Return a one-row-per-panel summary list — id, name,
    short_name, purpose, and analyte count.  Use
    :func:`get_lab_panel` for the full per-analyte detail."""
    from orgchem.core.clinical_panels import list_panels
    return [
        {
            "id": p.id,
            "name": p.name,
            "short_name": p.short_name,
            "purpose": p.purpose,
            "n_analytes": str(len(p.analytes)),
        }
        for p in list_panels()
    ]


@action(category="clinical")
def get_lab_panel(panel_id: str) -> Dict[str, Any]:
    """Return the full record for one panel: meta + every
    analyte's name + units + normal range + clinical
    significance + notes."""
    from orgchem.core.clinical_panels import get_panel, panel_to_dict
    p = get_panel(panel_id)
    if p is None:
        return {"error": f"Unknown lab panel id: {panel_id!r}."}
    return panel_to_dict(p)


@action(category="clinical")
def list_lab_analytes(category: str = "") -> List[Dict[str, str]]:
    """Return every analyte (deduplicated across panels),
    optionally filtered by ``category`` (one of
    ``"electrolyte"`` / ``"kidney"`` / ``"liver"`` /
    ``"lipid"`` / ``"metabolic"`` / ``"hormone"`` /
    ``"vitamin"``)."""
    from orgchem.core.clinical_panels import (
        VALID_CATEGORIES, analyte_to_dict, list_analytes,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    rows = list_analytes(category=cat or None)
    return [analyte_to_dict(a) for a in rows]


@action(category="clinical")
def find_lab_analyte(needle: str) -> List[Dict[str, str]]:
    """Return every analyte whose id, name, or abbreviation
    matches the (case-insensitive) needle.  Useful for
    *"what's BUN?"* / *"tell me about sodium"* prompts."""
    from orgchem.core.clinical_panels import (
        analyte_to_dict, find_analyte,
    )
    return [analyte_to_dict(a) for a in find_analyte(needle)]


@action(category="clinical")
def open_clinical_panels(panel_id: str = "",
                         analyte_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Clinical lab panels…* dialog.

    Optional ``panel_id`` switches the panel combo; optional
    ``analyte_id`` then focuses a specific row in that panel's
    analyte table.  Returns ``{"opened": True,
    "panel_selected": bool, "analyte_selected": bool}`` on
    success or ``{"error": ...}`` when the GUI isn't reachable.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.clinical_panels import (
            ClinicalPanelsDialog,
        )
        dlg = ClinicalPanelsDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        panel_ok = False
        analyte_ok = False
        if panel_id:
            panel_ok = dlg.select_panel(panel_id)
        if analyte_id:
            analyte_ok = dlg.select_analyte(analyte_id)
        return {
            "opened": True,
            "panel_selected": panel_ok,
            "analyte_selected": analyte_ok,
            "panel_id": panel_id or None,
            "analyte_id": analyte_id or None,
        }

    return run_on_main_thread_sync(_open)
