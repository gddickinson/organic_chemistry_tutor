"""Phase PH-2.0 (round 220) — agent actions for the Pharm
receptor pharmacology catalogue + a focused tab-opener that
brings up the new Receptors tab on the existing PharmMainWindow.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="pharm-receptors")
def list_receptors(family: str = "") -> List[Dict[str, object]]:
    """Return receptor catalogue entries, optionally filtered
    by family (one of: ``"gpcr-aminergic"`` / ``"gpcr-peptide"``
    / ``"gpcr-other"`` / ``"nhr-steroid"`` / ``"nhr-other"`` /
    ``"rtk"`` / ``"ion-channel-vg"`` / ``"ion-channel-lg"`` /
    ``"transporter-monoamine"`` / ``"transporter-other"``)."""
    from pharm.core.receptors import (
        RECEPTOR_FAMILIES, receptor_to_dict,
        list_receptors as _list,
    )
    f = (family or "").strip()
    if f and f not in RECEPTOR_FAMILIES:
        return [{
            "error": f"Unknown family {f!r}; valid: "
                     f"{', '.join(RECEPTOR_FAMILIES)}.",
        }]
    return [receptor_to_dict(r)
            for r in _list(f or None)]


@action(category="pharm-receptors")
def get_receptor(receptor_id: str) -> Dict[str, object]:
    """Return the full record for a single receptor by id (e.g.
    ``"adrenergic-beta1"`` / ``"opioid-mu"`` / ``"egfr"`` /
    ``"insulin-receptor"`` / ``"nmda"`` / ``"sglt2"``)."""
    from pharm.core.receptors import (
        get_receptor, receptor_to_dict,
    )
    r = get_receptor(receptor_id)
    if r is None:
        return {"error":
                f"Unknown receptor id: {receptor_id!r}."}
    return receptor_to_dict(r)


@action(category="pharm-receptors")
def find_receptors(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    subtype + structural summary + ligands + signalling +
    tissue distribution + clinical relevance + notes."""
    from pharm.core.receptors import (
        find_receptors, receptor_to_dict,
    )
    return [receptor_to_dict(r) for r in find_receptors(needle)]


@action(category="pharm-receptors")
def receptors_for_family(
    family: str,
) -> List[Dict[str, object]]:
    """Return all receptors in a single family."""
    from pharm.core.receptors import (
        RECEPTOR_FAMILIES, receptor_to_dict,
        receptors_for_family,
    )
    if family not in RECEPTOR_FAMILIES:
        return [{
            "error": f"Unknown family {family!r}; valid: "
                     f"{', '.join(RECEPTOR_FAMILIES)}.",
        }]
    return [receptor_to_dict(r)
            for r in receptors_for_family(family)]


@action(category="pharm-receptors")
def open_pharm_receptors_tab() -> Dict[str, Any]:
    """Open the Pharm Studio main window + focus its
    *Receptors* tab (added in Phase PH-2.0).  Same lazy-
    construction + main-thread-marshalling pattern as
    ``open_pharm_studio``.

    Returns ``{"opened": True, "tab": "Receptors"}`` on
    success.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from pharm.gui.windows.pharm_main_window import (
            PharmMainWindow,
        )
        pharm_win = getattr(win, "_pharm_window", None)
        if pharm_win is None:
            pharm_win = PharmMainWindow(parent=win)
            win._pharm_window = pharm_win
        pharm_win.show()
        pharm_win.raise_()
        pharm_win.activateWindow()
        ok = pharm_win.switch_to(PharmMainWindow.TAB_RECEPTORS)
        return {"opened": True,
                "tab": (PharmMainWindow.TAB_RECEPTORS
                        if ok else None)}

    return run_on_main_thread_sync(_open)
