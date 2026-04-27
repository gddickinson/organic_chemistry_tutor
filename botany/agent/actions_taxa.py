"""Phase BT-1.0 (round 216) — agent actions for the Botany Studio
plant-taxa catalogue + Botany main-window opener.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="botany-taxa")
def list_plant_taxa(
    division: str = "",
    photosynthetic_strategy: str = "",
) -> List[Dict[str, object]]:
    """Return plant taxa, optionally filtered by division
    (``"bryophyta"`` / ``"lycopodiophyta"`` / ``"pteridophyta"``
    / ``"gymnosperm"`` / ``"angiosperm-monocot"`` /
    ``"angiosperm-eudicot"``) and / or photosynthetic strategy
    (``"C3"`` / ``"C4"`` / ``"CAM"`` / ``"not-applicable"``)."""
    from botany.core.taxa import (
        DIVISIONS, PHOTOSYNTHETIC_STRATEGIES,
        list_plant_taxa as _list, plant_taxon_to_dict,
    )
    d = (division or "").strip()
    p = (photosynthetic_strategy or "").strip()
    if d and d not in DIVISIONS:
        return [{
            "error": f"Unknown division {d!r}; valid: "
                     f"{', '.join(DIVISIONS)}.",
        }]
    if p and p not in PHOTOSYNTHETIC_STRATEGIES:
        return [{
            "error": f"Unknown photosynthetic_strategy "
                     f"{p!r}; valid: "
                     f"{', '.join(PHOTOSYNTHETIC_STRATEGIES)}.",
        }]
    return [plant_taxon_to_dict(t)
            for t in _list(d or None, p or None)]


@action(category="botany-taxa")
def get_plant_taxon(taxon_id: str) -> Dict[str, object]:
    """Return the full record for a single plant taxon by id
    (e.g. ``"arabidopsis-thaliana"`` / ``"papaver-somniferum"``
    / ``"taxus-brevifolia"`` / ``"zea-mays"``)."""
    from botany.core.taxa import (
        get_plant_taxon, plant_taxon_to_dict,
    )
    t = get_plant_taxon(taxon_id)
    if t is None:
        return {"error":
                f"Unknown plant taxon id: {taxon_id!r}."}
    return plant_taxon_to_dict(t)


@action(category="botany-taxa")
def find_plant_taxa(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + common
    name + full taxonomic name + class + reproductive strategy
    + ecological role + economic importance + cross-reference
    molecule names + notes."""
    from botany.core.taxa import (
        find_plant_taxa, plant_taxon_to_dict,
    )
    return [plant_taxon_to_dict(t)
            for t in find_plant_taxa(needle)]


@action(category="botany-taxa")
def plant_taxa_for_division(
    division: str,
) -> List[Dict[str, object]]:
    """Return all plant taxa in a single division."""
    from botany.core.taxa import (
        DIVISIONS, plant_taxa_for_division,
        plant_taxon_to_dict,
    )
    if division not in DIVISIONS:
        return [{
            "error": f"Unknown division {division!r}; valid: "
                     f"{', '.join(DIVISIONS)}.",
        }]
    return [plant_taxon_to_dict(t)
            for t in plant_taxa_for_division(division)]


@action(category="botany-taxa")
def open_botany_studio(tab: str = "") -> Dict[str, Any]:
    """Open the Botany Studio main window (lazily constructed
    on first call).  Optional ``tab`` argument focuses one of
    the inner tabs (``"Plant taxa"`` / ``"Plant secondary
    metabolites"`` / ``"Tutorials"``).

    Phase BT-1.0 — fifth sibling in the multi-studio life-
    sciences platform.  The Plant secondary metabolites tab
    bridges directly to the OrgChem molecule DB (filtered to
    plant-derived natural products via ``source_tags``) — the
    first sibling whose bridge reads the SQLite store directly
    rather than another Python catalogue.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from botany.gui.windows.botany_main_window import (
            BotanyMainWindow,
        )
        botany_win = getattr(win, "_botany_window", None)
        if botany_win is None:
            botany_win = BotanyMainWindow(parent=win)
            win._botany_window = botany_win
        botany_win.show()
        botany_win.raise_()
        botany_win.activateWindow()
        focused: Any = None
        if tab:
            ok = botany_win.switch_to(tab)
            focused = tab if ok else None
        return {"opened": True, "tab": focused}

    return run_on_main_thread_sync(_open)
