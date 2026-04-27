"""Phase CB-1.0 (round 212) — agent actions for cell-signalling
pathways + the Cell Bio Studio main-window opener.

Three lookup actions (`list_signaling_pathways`,
`get_signaling_pathway`, `find_signaling_pathways`) are pure-
headless; the dialog opener (`open_cellbio_studio`) marshals onto
the Qt main thread via the shared OrgChem dispatcher.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="cellbio-signaling")
def list_signaling_pathways(
    category: str = "",
    receptor_class: str = "",
) -> List[Dict[str, object]]:
    """Return cell-signalling pathways, optionally filtered by
    category (one of: ``"growth-factor"`` / ``"cytokine"`` /
    ``"morphogen"`` / ``"second-messenger"`` / ``"stress-
    response"`` / ``"nutrient-energy"`` / ``"innate-immunity"``
    / ``"adaptive-immunity"`` / ``"cell-death"``) and / or
    receptor_class (e.g. ``"RTK"`` / ``"GPCR"`` /
    ``"cytokine-receptor"`` / ``"TGF-β-receptor"`` /
    ``"Frizzled"`` / ``"Notch"`` / etc.)."""
    from cellbio.core.cell_signaling import (
        CATEGORIES, RECEPTOR_CLASSES, list_pathways,
        pathway_to_dict,
    )
    c = (category or "").strip()
    rc = (receptor_class or "").strip()
    if c and c not in CATEGORIES:
        return [{
            "error": f"Unknown category {c!r}; valid: "
                     f"{', '.join(CATEGORIES)}.",
        }]
    if rc and rc not in RECEPTOR_CLASSES:
        return [{
            "error": f"Unknown receptor class {rc!r}; valid: "
                     f"{', '.join(RECEPTOR_CLASSES)}.",
        }]
    return [pathway_to_dict(p)
            for p in list_pathways(c or None, rc or None)]


@action(category="cellbio-signaling")
def get_signaling_pathway(pathway_id: str) -> Dict[str, object]:
    """Return the full record for a single signalling pathway by
    id (e.g. ``"mapk-erk"`` / ``"pi3k-akt-mtor"`` / ``"jak-stat"`` /
    ``"wnt-beta-catenin"`` / ``"notch"`` / ``"hedgehog"`` /
    ``"nf-kb"`` / ``"tgf-beta-smad"`` / ``"gpcr-camp-pka"`` /
    ``"hippo-yap"`` / ``"ampk"`` / ``"hif1a"`` / ``"p53"`` /
    ``"intrinsic-apoptosis"`` / ``"tcr"`` / etc.)."""
    from cellbio.core.cell_signaling import (
        get_pathway, pathway_to_dict,
    )
    p = get_pathway(pathway_id)
    if p is None:
        return {"error":
                f"Unknown signalling pathway id: {pathway_id!r}."}
    return pathway_to_dict(p)


@action(category="cellbio-signaling")
def find_signaling_pathways(
    needle: str,
) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    canonical function + key components + disease associations +
    drug targets."""
    from cellbio.core.cell_signaling import (
        find_pathways, pathway_to_dict,
    )
    return [pathway_to_dict(p) for p in find_pathways(needle)]


@action(category="cellbio-signaling")
def open_cellbio_studio(tab: str = "") -> Dict[str, Any]:
    """Open the Cell Bio Studio main window (lazily constructed
    on first call).  Optional ``tab`` argument focuses one of the
    inner tabs (``"Signalling"`` / ``"Tutorials"``).  Returns
    ``{"opened": True, "tab": "<label or None>"}``.

    Phase CB-1.0 — first slice of the multi-studio life-sciences
    platform.  Cell Bio Studio is a sibling to OrgChem Studio
    sharing the same process, agent registry, and database.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        # Lazy import to avoid pulling Qt at action-registration
        # time (matters for headless test imports).
        from cellbio.gui.windows.cellbio_main_window import (
            CellBioMainWindow,
        )
        # MainWindow caches the cellbio window instance.
        cellbio_win = getattr(win, "_cellbio_window", None)
        if cellbio_win is None:
            cellbio_win = CellBioMainWindow(parent=win)
            win._cellbio_window = cellbio_win
        cellbio_win.show()
        cellbio_win.raise_()
        cellbio_win.activateWindow()
        focused: Any = None
        if tab:
            ok = cellbio_win.switch_to(tab)
            focused = tab if ok else None
        return {"opened": True, "tab": focused}

    return run_on_main_thread_sync(_open)
