"""Phase 44 (round 150) — agent actions for the microscopy
techniques catalogue.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="microscopy")
def list_microscopy_methods(
    resolution_scale: str = "",
) -> List[Dict[str, object]]:
    """Return every microscopy method, optionally filtered by
    resolution scale (one of: ``"whole-organism"`` /
    ``"tissue"`` / ``"cellular"`` / ``"sub-cellular"`` /
    ``"single-molecule"`` / ``"clinical-histology"``)."""
    from orgchem.core.microscopy import (
        RESOLUTION_SCALES, list_methods, method_to_dict,
    )
    s = (resolution_scale or "").strip()
    if s and s not in RESOLUTION_SCALES:
        return [{
            "error": f"Unknown resolution scale {s!r}; "
                     f"valid: {', '.join(RESOLUTION_SCALES)}.",
        }]
    return [method_to_dict(m) for m in list_methods(s or None)]


@action(category="microscopy")
def get_microscopy_method(method_id: str) -> Dict[str, object]:
    """Return the full record for a single microscopy method
    by id (e.g. ``"confocal"`` / ``"sted"`` / ``"cryo-em"`` /
    ``"afm"``)."""
    from orgchem.core.microscopy import (
        get_method, method_to_dict,
    )
    m = get_method(method_id)
    if m is None:
        return {"error": f"Unknown microscopy method id: "
                         f"{method_id!r}."}
    return method_to_dict(m)


@action(category="microscopy")
def find_microscopy_methods(
    needle: str,
) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    abbreviation + typical_uses + representative_instruments."""
    from orgchem.core.microscopy import (
        find_methods, method_to_dict,
    )
    return [method_to_dict(m) for m in find_methods(needle)]


@action(category="microscopy")
def microscopy_methods_for_sample(
    sample_type: str,
) -> List[Dict[str, object]]:
    """Return microscopy methods that list the given sample
    type as typical (one of: ``"live-organism"`` /
    ``"fixed-tissue"`` / ``"live-cells"`` / ``"fixed-cells"``
    / ``"isolated-organelles"`` / ``"single-molecules"`` /
    ``"biopsy"`` / ``"non-biological"``)."""
    from orgchem.core.microscopy import (
        SAMPLE_TYPES, method_to_dict,
        methods_for_sample_type,
    )
    s = (sample_type or "").strip()
    if not s:
        return []
    if s not in SAMPLE_TYPES:
        return [{
            "error": f"Unknown sample type {s!r}; valid: "
                     f"{', '.join(SAMPLE_TYPES)}.",
        }]
    return [method_to_dict(m) for m in methods_for_sample_type(s)]


@action(category="microscopy")
def open_microscopy(
    method_id: str = "",
) -> Dict[str, Any]:
    """Open the *Tools → Microscopy techniques…* dialog and
    optionally focus a specific method by id."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.microscopy import (
            MicroscopyDialog,
        )
        dlg = MicroscopyDialog.singleton(parent=win)
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
