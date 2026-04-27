"""Phase MB-1.0 (round 215) — agent actions for the Microbiology
Studio microbe catalogue + Microbio main-window opener.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="microbio-microbes")
def list_microbes(
    kingdom: str = "",
    gram_type: str = "",
) -> List[Dict[str, object]]:
    """Return microbes, optionally filtered by kingdom
    (``"bacteria"`` / ``"archaea"`` / ``"fungus"`` / ``"virus"``
    / ``"protist"``) and / or Gram type (``"gram-positive"`` /
    ``"gram-negative"`` / ``"acid-fast"`` / ``"atypical"`` /
    ``"not-applicable"``)."""
    from microbio.core.microbes import (
        GRAM_TYPES, KINGDOMS,
        list_microbes as _list, microbe_to_dict,
    )
    k = (kingdom or "").strip()
    g = (gram_type or "").strip()
    if k and k not in KINGDOMS:
        return [{
            "error": f"Unknown kingdom {k!r}; valid: "
                     f"{', '.join(KINGDOMS)}.",
        }]
    if g and g not in GRAM_TYPES:
        return [{
            "error": f"Unknown gram_type {g!r}; valid: "
                     f"{', '.join(GRAM_TYPES)}.",
        }]
    return [microbe_to_dict(m)
            for m in _list(k or None, g or None)]


@action(category="microbio-microbes")
def get_microbe(microbe_id: str) -> Dict[str, object]:
    """Return the full record for a single microbe by id (e.g.
    ``"staphylococcus-aureus"`` / ``"escherichia-coli"`` /
    ``"mycobacterium-tuberculosis"`` / ``"sars-cov-2"`` /
    ``"plasmodium-falciparum"``)."""
    from microbio.core.microbes import (
        get_microbe, microbe_to_dict,
    )
    m = get_microbe(microbe_id)
    if m is None:
        return {"error":
                f"Unknown microbe id: {microbe_id!r}."}
    return microbe_to_dict(m)


@action(category="microbio-microbes")
def find_microbes(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    full taxonomic name + morphology + metabolism + pathogenesis
    + antibiotic susceptibility + reference."""
    from microbio.core.microbes import (
        find_microbes, microbe_to_dict,
    )
    return [microbe_to_dict(m) for m in find_microbes(needle)]


@action(category="microbio-microbes")
def microbes_for_kingdom(kingdom: str) -> List[Dict[str, object]]:
    """Return all microbes in a single kingdom."""
    from microbio.core.microbes import (
        KINGDOMS, microbe_to_dict, microbes_for_kingdom,
    )
    if kingdom not in KINGDOMS:
        return [{
            "error": f"Unknown kingdom {kingdom!r}; valid: "
                     f"{', '.join(KINGDOMS)}.",
        }]
    return [microbe_to_dict(m)
            for m in microbes_for_kingdom(kingdom)]


@action(category="microbio-microbes")
def open_microbio_studio(tab: str = "") -> Dict[str, Any]:
    """Open the Microbiology Studio main window (lazily
    constructed on first call).  Optional ``tab`` argument
    focuses one of the inner tabs (``"Microbes"`` /
    ``"Antibiotic spectrum"`` / ``"Tutorials"``).

    Phase MB-1.0 — fourth sibling in the multi-studio life-
    sciences platform.  The Antibiotic spectrum tab is a
    bridge into ``pharm.core.drug_classes`` filtered to the
    antimicrobial classes (β-lactams, macrolides,
    fluoroquinolones, aminoglycosides, HIV PIs, NRTIs).
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
        focused: Any = None
        if tab:
            ok = microbio_win.switch_to(tab)
            focused = tab if ok else None
        return {"opened": True, "tab": focused}

    return run_on_main_thread_sync(_open)
