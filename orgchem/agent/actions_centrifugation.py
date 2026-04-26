"""Phase 41 (round 144) — agent actions for the centrifugation
catalogue + g↔rpm calculator.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="centrifugation")
def list_centrifuges_action(
        centrifuge_class: str = "") -> List[Dict[str, object]]:
    """Return every catalogued centrifuge, optionally filtered
    by class (``microfuge`` / ``benchtop`` / ``high-speed`` /
    ``ultracentrifuge``)."""
    from orgchem.core.centrifugation import (
        VALID_CENTRIFUGE_CLASSES, centrifuge_to_dict,
        list_centrifuges,
    )
    cat = (centrifuge_class or "").strip()
    if cat and cat not in VALID_CENTRIFUGE_CLASSES:
        return [{
            "error": f"Unknown centrifuge_class {cat!r}; "
                     f"valid: {', '.join(VALID_CENTRIFUGE_CLASSES)}.",
        }]
    return [centrifuge_to_dict(c)
            for c in list_centrifuges(cat or None)]


@action(category="centrifugation")
def get_centrifuge_action(centrifuge_id: str) -> Dict[str, object]:
    """Look up one centrifuge by id from the catalogue (e.g.
    ``"eppendorf_5424"`` / ``"beckman_optima_xpn"``).  Returns
    the full record as a dict, or ``{"error": ...}`` if the id
    is unknown."""
    from orgchem.core.centrifugation import (
        centrifuge_to_dict, get_centrifuge,
    )
    c = get_centrifuge(centrifuge_id)
    if c is None:
        return {"error":
                f"Unknown centrifuge id: {centrifuge_id!r}."}
    return centrifuge_to_dict(c)


@action(category="centrifugation")
def list_rotors_action(
        rotor_type: str = "") -> List[Dict[str, object]]:
    """Return every catalogued rotor, optionally filtered by
    type (``fixed-angle`` / ``swinging-bucket`` / ``vertical``
    / ``continuous-flow``)."""
    from orgchem.core.centrifugation import (
        VALID_ROTOR_TYPES, list_rotors, rotor_to_dict,
    )
    cat = (rotor_type or "").strip()
    if cat and cat not in VALID_ROTOR_TYPES:
        return [{
            "error": f"Unknown rotor_type {cat!r}; "
                     f"valid: {', '.join(VALID_ROTOR_TYPES)}.",
        }]
    return [rotor_to_dict(r) for r in list_rotors(cat or None)]


@action(category="centrifugation")
def get_rotor_action(rotor_id: str) -> Dict[str, object]:
    """Look up one rotor by id from the catalogue (e.g.
    ``"beckman_ja_25_50"`` / ``"sw41_ti"``).  Returns the full
    record as a dict, or ``{"error": ...}`` if the id is
    unknown."""
    from orgchem.core.centrifugation import (
        get_rotor, rotor_to_dict,
    )
    r = get_rotor(rotor_id)
    if r is None:
        return {"error": f"Unknown rotor id: {rotor_id!r}."}
    return rotor_to_dict(r)


@action(category="centrifugation")
def list_centrifugation_applications(
        protocol_class: str = "") -> List[Dict[str, object]]:
    """Return every catalogued application protocol, optionally
    filtered by class (``differential`` / ``density-gradient`` /
    ``cell-pellet`` / ``protein-concentration``)."""
    from orgchem.core.centrifugation import (
        VALID_PROTOCOL_CLASSES, application_to_dict,
        list_applications,
    )
    cat = (protocol_class or "").strip()
    if cat and cat not in VALID_PROTOCOL_CLASSES:
        return [{
            "error": f"Unknown protocol_class {cat!r}; "
                     f"valid: {', '.join(VALID_PROTOCOL_CLASSES)}.",
        }]
    return [application_to_dict(a)
            for a in list_applications(cat or None)]


@action(category="centrifugation")
def rpm_to_g_action(rpm: float, radius_cm: float
                    ) -> Dict[str, float]:
    """Convert RPM + rotor radius (cm) to relative centrifugal
    force (× g).  ``g = 1.118e-5 · RPM² · r``."""
    from orgchem.core.centrifugation import rpm_to_g
    try:
        return rpm_to_g(rpm, radius_cm)
    except ValueError as e:
        return {"error": str(e)}


@action(category="centrifugation")
def g_to_rpm_action(g_force: float, radius_cm: float
                    ) -> Dict[str, float]:
    """Inverse of :func:`rpm_to_g_action` — given target × g +
    rotor radius (cm), return required RPM."""
    from orgchem.core.centrifugation import g_to_rpm
    try:
        return g_to_rpm(g_force, radius_cm)
    except ValueError as e:
        return {"error": str(e)}


@action(category="centrifugation")
def open_centrifugation(tab: str = "",
                        rotor_id: str = "",
                        centrifuge_id: str = "",
                        application_id: str = ""
                        ) -> Dict[str, Any]:
    """Open the *Tools → Centrifugation…* dialog and optionally
    focus a specific tab + entry.  Returns
    ``{"opened", "selected_tab", "selected_rotor", ...}``.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.centrifugation import (
            CentrifugationDialog,
        )
        dlg = CentrifugationDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        result = {
            "opened": True,
            "selected_tab": False,
            "selected_centrifuge": False,
            "selected_rotor": False,
            "selected_application": False,
            "available_tabs": dlg.tab_labels(),
        }
        if tab:
            result["selected_tab"] = dlg.select_tab(tab)
        if centrifuge_id:
            result["selected_centrifuge"] = (
                dlg.select_centrifuge(centrifuge_id))
        if rotor_id:
            result["selected_rotor"] = dlg.select_rotor(rotor_id)
        if application_id:
            result["selected_application"] = (
                dlg.select_application(application_id))
        return result

    return run_on_main_thread_sync(_open)
