"""Phase AB-2.0 (round 223) — agent actions for the Animal
organ-systems catalogue + a focused tab-opener.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="animal-organ-systems")
def list_organ_systems(
    system_category: str = "",
) -> List[Dict[str, object]]:
    """Return organ-system catalogue entries, optionally
    filtered by system category (one of: ``"cardiovascular"``
    / ``"respiratory"`` / ``"digestive"`` / ``"urinary"`` /
    ``"nervous"`` / ``"endocrine"`` / ``"immune"`` /
    ``"musculoskeletal"`` / ``"integumentary"`` /
    ``"reproductive-female"`` / ``"reproductive-male"`` /
    ``"lymphatic"`` / ``"comparative-anatomy"``)."""
    from animal.core.organ_systems import (
        SYSTEM_CATEGORIES, organ_system_to_dict,
        list_organ_systems as _list,
    )
    sc = (system_category or "").strip()
    if sc and sc not in SYSTEM_CATEGORIES:
        return [{
            "error": f"Unknown system_category {sc!r}; valid: "
                     f"{', '.join(SYSTEM_CATEGORIES)}.",
        }]
    return [organ_system_to_dict(s)
            for s in _list(sc or None)]


@action(category="animal-organ-systems")
def get_organ_system(system_id: str) -> Dict[str, object]:
    """Return the full record for a single organ-system entry
    by id (e.g. ``"cardiovascular-mammalian"`` /
    ``"nervous-mammalian"`` / ``"regeneration-comparative"`` /
    ``"eyes-comparative"``)."""
    from animal.core.organ_systems import (
        get_organ_system, organ_system_to_dict,
    )
    s = get_organ_system(system_id)
    if s is None:
        return {"error":
                f"Unknown organ-system id: {system_id!r}."}
    return organ_system_to_dict(s)


@action(category="animal-organ-systems")
def find_organ_systems(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    summary + organs + cell types + functional anatomy +
    evolutionary origin + disorders + notes."""
    from animal.core.organ_systems import (
        find_organ_systems, organ_system_to_dict,
    )
    return [organ_system_to_dict(s)
            for s in find_organ_systems(needle)]


@action(category="animal-organ-systems")
def organ_systems_for_category(
    system_category: str,
) -> List[Dict[str, object]]:
    """Return all organ-system entries in a single category."""
    from animal.core.organ_systems import (
        SYSTEM_CATEGORIES, organ_system_to_dict,
        organ_systems_for_category,
    )
    if system_category not in SYSTEM_CATEGORIES:
        return [{
            "error": f"Unknown system_category "
                     f"{system_category!r}; valid: "
                     f"{', '.join(SYSTEM_CATEGORIES)}.",
        }]
    return [organ_system_to_dict(s)
            for s in organ_systems_for_category(system_category)]


@action(category="animal-organ-systems")
def open_animal_organ_systems_tab() -> Dict[str, Any]:
    """Open the Animal Biology Studio main window + focus its
    *Organ systems* tab (added in Phase AB-2.0).
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from animal.gui.windows.animal_main_window import (
            AnimalMainWindow,
        )
        animal_win = getattr(win, "_animal_window", None)
        if animal_win is None:
            animal_win = AnimalMainWindow(parent=win)
            win._animal_window = animal_win
        animal_win.show()
        animal_win.raise_()
        animal_win.activateWindow()
        ok = animal_win.switch_to(
            AnimalMainWindow.TAB_ORGAN_SYSTEMS)
        return {"opened": True,
                "tab": (AnimalMainWindow.TAB_ORGAN_SYSTEMS
                        if ok else None)}

    return run_on_main_thread_sync(_open)
