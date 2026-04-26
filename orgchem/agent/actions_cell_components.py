"""Phase 43 (round 151) — agent actions for the cell-component
explorer.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="cell")
def list_cell_components(
    domain: str = "",
    sub_domain: str = "",
) -> List[Dict[str, object]]:
    """Return cellular components, optionally filtered by domain
    (one of: ``"eukarya"`` / ``"bacteria"`` / ``"archaea"``)
    and / or sub-domain (one of: ``"animal"`` / ``"plant"`` /
    ``"fungus"`` / ``"protist"`` / ``"gram-positive"`` /
    ``"gram-negative"``)."""
    from orgchem.core.cell_components import (
        DOMAINS, SUB_DOMAINS, component_to_dict,
        list_components,
    )
    d = (domain or "").strip()
    s = (sub_domain or "").strip()
    if d and d not in DOMAINS:
        return [{
            "error": f"Unknown domain {d!r}; valid: "
                     f"{', '.join(DOMAINS)}.",
        }]
    if s and s not in SUB_DOMAINS:
        return [{
            "error": f"Unknown sub-domain {s!r}; valid: "
                     f"{', '.join(SUB_DOMAINS)}.",
        }]
    return [component_to_dict(c)
            for c in list_components(d or None, s or None)]


@action(category="cell")
def get_cell_component(component_id: str) -> Dict[str, object]:
    """Return the full record for a single cellular component
    by id (e.g. ``"mitochondrion"`` / ``"chromatin"`` /
    ``"bacterial-flagellum"``)."""
    from orgchem.core.cell_components import (
        component_to_dict, get_component,
    )
    c = get_component(component_id)
    if c is None:
        return {"error": f"Unknown cell-component id: "
                         f"{component_id!r}."}
    return component_to_dict(c)


@action(category="cell")
def find_cell_components(
    needle: str,
) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    function + constituent names + notes."""
    from orgchem.core.cell_components import (
        component_to_dict, find_components,
    )
    return [component_to_dict(c) for c in find_components(needle)]


@action(category="cell")
def cell_components_for_category(
    category: str,
) -> List[Dict[str, object]]:
    """Return components of a given category (one of:
    ``"membrane"`` / ``"organelle"`` / ``"nuclear"`` /
    ``"cytoskeleton"`` / ``"envelope"`` / ``"appendage"`` /
    ``"extracellular"`` / ``"ribosome"`` / ``"genome"``)."""
    from orgchem.core.cell_components import (
        CATEGORIES, component_to_dict, components_for_category,
    )
    c = (category or "").strip()
    if not c:
        return []
    if c not in CATEGORIES:
        return [{
            "error": f"Unknown category {c!r}; valid: "
                     f"{', '.join(CATEGORIES)}.",
        }]
    return [component_to_dict(x)
            for x in components_for_category(c)]


@action(category="cell")
def open_cell_components(
    component_id: str = "",
) -> Dict[str, Any]:
    """Open the *Tools → Cell components…* dialog and
    optionally focus a specific component by id."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.cell_components import (
            CellComponentsDialog,
        )
        dlg = CellComponentsDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if component_id:
            selected = dlg.select_component(component_id)
        return {
            "opened": True,
            "selected": selected,
            "component_id": component_id or None,
        }

    return run_on_main_thread_sync(_open)
