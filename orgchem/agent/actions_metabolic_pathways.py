"""Phase 42a (round 147) — agent actions for the
metabolic-pathways catalogue.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="biochem")
def list_metabolic_pathways(category: str = ""
                            ) -> List[Dict[str, object]]:
    """Return every catalogued metabolic pathway, optionally
    filtered by category (one of: ``"central-carbon"`` /
    ``"lipid"`` / ``"amino-acid"`` / ``"nucleotide"`` /
    ``"specialised"``).

    Each entry is the full pathway record incl. ordered list of
    `PathwayStep` records with substrates / enzymes / products /
    ΔG / regulators."""
    from orgchem.core.metabolic_pathways import (
        VALID_CATEGORIES, list_pathways, pathway_to_dict,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    return [pathway_to_dict(p)
            for p in list_pathways(cat or None)]


@action(category="biochem")
def get_metabolic_pathway(pathway_id: str) -> Dict[str, Any]:
    """Return the full pathway record by id."""
    from orgchem.core.metabolic_pathways import (
        get_pathway, pathway_to_dict,
    )
    p = get_pathway(pathway_id)
    if p is None:
        return {"error": f"Unknown pathway id: {pathway_id!r}."}
    return pathway_to_dict(p)


@action(category="biochem")
def find_metabolic_pathways(needle: str
                            ) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    overview."""
    from orgchem.core.metabolic_pathways import (
        find_pathways, pathway_to_dict,
    )
    return [pathway_to_dict(p) for p in find_pathways(needle)]


@action(category="biochem")
def list_pathway_steps(pathway_id: str
                       ) -> List[Dict[str, Any]]:
    """Return only the per-step list for a pathway (lighter
    than the full pathway record)."""
    from orgchem.core.metabolic_pathways import (
        get_pathway, step_to_dict,
    )
    p = get_pathway(pathway_id)
    if p is None:
        return [{"error": f"Unknown pathway id: {pathway_id!r}."}]
    return [step_to_dict(s) for s in p.steps]


@action(category="biochem")
def open_metabolic_pathways(pathway_id: str = "",
                            step_number: int = 0
                            ) -> Dict[str, Any]:
    """Open the *Tools → Metabolic pathways…* dialog and
    optionally focus a pathway + step."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.metabolic_pathways import (
            MetabolicPathwaysDialog,
        )
        dlg = MetabolicPathwaysDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        result = {
            "opened": True,
            "selected_pathway": False,
            "selected_step": False,
            "pathway_id": pathway_id or None,
            "step_number": step_number or None,
        }
        if pathway_id:
            result["selected_pathway"] = (
                dlg.select_pathway(pathway_id))
        if step_number:
            result["selected_step"] = dlg.select_step(step_number)
        return result

    return run_on_main_thread_sync(_open)
