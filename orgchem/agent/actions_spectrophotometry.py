"""Phase 37d (round 139) — agent actions for the
spectrophotometry-method catalogue + Beer-Lambert calculator.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="spectrophotometry")
def list_spectrophotometry_methods(
        category: str = "") -> List[Dict[str, str]]:
    """Return every catalogued spectrophotometry method,
    optionally filtered by category (one of
    ``"molecular-uv-vis"`` / ``"molecular-ir"`` /
    ``"molecular-chirality"`` / ``"atomic"`` /
    ``"magnetic-resonance"``)."""
    from orgchem.core.spectrophotometry_methods import (
        VALID_CATEGORIES, list_methods, to_dict,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    return [to_dict(m) for m in list_methods(category=cat or None)]


@action(category="spectrophotometry")
def get_spectrophotometry_method(method_id: str) -> Dict[str, str]:
    """Return the full record for a single method by its id
    (e.g. ``"uv_vis"`` / ``"ir_ftir"`` / ``"icp_ms"`` / ``"nmr"``)."""
    from orgchem.core.spectrophotometry_methods import (
        get_method, to_dict,
    )
    m = get_method(method_id)
    if m is None:
        return {"error":
                f"Unknown spectrophotometry method id: {method_id!r}."}
    return to_dict(m)


@action(category="spectrophotometry")
def find_spectrophotometry_methods(
        needle: str) -> List[Dict[str, str]]:
    """Return every method matching the (case-insensitive)
    needle across name + abbreviation + id."""
    from orgchem.core.spectrophotometry_methods import (
        find_methods, to_dict,
    )
    return [to_dict(m) for m in find_methods(needle)]


@action(category="spectrophotometry")
def beer_lambert(
        absorbance: Optional[float] = None,
        molar_absorptivity: Optional[float] = None,
        path_length_cm: Optional[float] = None,
        concentration_M: Optional[float] = None,
        ) -> Dict[str, Any]:
    """Solve the Beer-Lambert law A = ε·l·c.

    Pass any 3 of the 4 quantities; the 4th is computed.
    Units: ε in M⁻¹·cm⁻¹, l in cm, c in M.  Returns
    ``{"absorbance", "molar_absorptivity", "path_length_cm",
    "concentration_M"}`` on success, ``{"error": ...}`` if the
    inputs don't make sense (more than one missing, non-positive
    value, etc.).
    """
    from orgchem.core.spectrophotometry_methods import (
        beer_lambert_solve,
    )
    try:
        return beer_lambert_solve(
            absorbance=absorbance,
            molar_absorptivity=molar_absorptivity,
            path_length_cm=path_length_cm,
            concentration_M=concentration_M,
        )
    except ValueError as e:
        return {"error": str(e)}


@action(category="spectrophotometry")
def open_spectrophotometry(method_id: str = "") -> Dict[str, Any]:
    """Open the *Tools → Spectrophotometry…* dialog and
    optionally focus a specific method."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.spectrophotometry_methods import (
            SpectrophotometryDialog,
        )
        dlg = SpectrophotometryDialog.singleton(parent=win)
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
