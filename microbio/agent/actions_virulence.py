"""Phase MB-2.0 (round 221) — agent actions for the Microbio
virulence-factor catalogue + a focused tab-opener that brings
up the new Virulence-factors tab on MicrobioMainWindow.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="microbio-virulence")
def list_virulence_factors(
    mechanism_class: str = "",
) -> List[Dict[str, object]]:
    """Return virulence-factor catalogue entries, optionally
    filtered by mechanism class (one of: ``"ab-toxin"`` /
    ``"pore-forming"`` / ``"superantigen"`` / ``"adhesin"`` /
    ``"capsule"`` / ``"secretion-system"`` /
    ``"immune-evasion"`` / ``"biofilm"`` / ``"endotoxin"``)."""
    from microbio.core.virulence_factors import (
        MECHANISM_CLASSES, virulence_factor_to_dict,
        list_virulence_factors as _list,
    )
    mc = (mechanism_class or "").strip()
    if mc and mc not in MECHANISM_CLASSES:
        return [{
            "error": f"Unknown mechanism_class {mc!r}; valid: "
                     f"{', '.join(MECHANISM_CLASSES)}.",
        }]
    return [virulence_factor_to_dict(f)
            for f in _list(mc or None)]


@action(category="microbio-virulence")
def get_virulence_factor(factor_id: str) -> Dict[str, object]:
    """Return the full record for a single virulence factor by
    id (e.g. ``"diphtheria-toxin"`` / ``"cholera-toxin"`` /
    ``"alpha-toxin-staph"`` / ``"tsst-1"`` / ``"lps-endotoxin"``)."""
    from microbio.core.virulence_factors import (
        get_virulence_factor, virulence_factor_to_dict,
    )
    f = get_virulence_factor(factor_id)
    if f is None:
        return {"error":
                f"Unknown virulence-factor id: {factor_id!r}."}
    return virulence_factor_to_dict(f)


@action(category="microbio-virulence")
def find_virulence_factors(
    needle: str,
) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    mechanism class + structural notes + target tissue + mode
    of action + clinical syndrome + vaccine info + notes."""
    from microbio.core.virulence_factors import (
        find_virulence_factors, virulence_factor_to_dict,
    )
    return [virulence_factor_to_dict(f)
            for f in find_virulence_factors(needle)]


@action(category="microbio-virulence")
def virulence_factors_for_class(
    mechanism_class: str,
) -> List[Dict[str, object]]:
    """Return all virulence factors in a single mechanism
    class."""
    from microbio.core.virulence_factors import (
        MECHANISM_CLASSES, virulence_factor_to_dict,
        virulence_factors_for_class,
    )
    if mechanism_class not in MECHANISM_CLASSES:
        return [{
            "error": f"Unknown mechanism_class "
                     f"{mechanism_class!r}; valid: "
                     f"{', '.join(MECHANISM_CLASSES)}.",
        }]
    return [virulence_factor_to_dict(f)
            for f in virulence_factors_for_class(
                mechanism_class)]


@action(category="microbio-virulence")
def open_microbio_virulence_tab() -> Dict[str, Any]:
    """Open the Microbio Studio main window + focus its
    *Virulence factors* tab (added in Phase MB-2.0).  Same
    lazy-construction + main-thread-marshalling pattern as
    ``open_microbio_studio``.

    Returns ``{"opened": True, "tab": "Virulence factors"}``
    on success.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from microbio.gui.windows.microbio_main_window import (
            MicrobioMainWindow,
        )
        microbio_win = getattr(win, "_microbio_window", None)
        if microbio_win is None:
            microbio_win = MicrobioMainWindow(parent=win)
            win._microbio_window = microbio_win
        microbio_win.show()
        microbio_win.raise_()
        microbio_win.activateWindow()
        ok = microbio_win.switch_to(
            MicrobioMainWindow.TAB_VIRULENCE)
        return {"opened": True,
                "tab": (MicrobioMainWindow.TAB_VIRULENCE
                        if ok else None)}

    return run_on_main_thread_sync(_open)
