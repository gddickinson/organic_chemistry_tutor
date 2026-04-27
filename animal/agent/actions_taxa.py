"""Phase AB-1.0 (round 217) — agent actions for the Animal Biology
Studio animal-taxa catalogue + Animal main-window opener.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="animal-taxa")
def list_animal_taxa(
    phylum: str = "",
    body_plan: str = "",
) -> List[Dict[str, object]]:
    """Return animal taxa, optionally filtered by phylum
    (``"porifera"`` / ``"cnidaria"`` / ``"platyhelminthes"`` /
    ``"nematoda"`` / ``"mollusca"`` / ``"annelida"`` /
    ``"arthropoda"`` / ``"echinodermata"`` / ``"chordata"``)
    and / or body plan (``"asymmetric"`` / ``"radial"`` /
    ``"bilateral"``)."""
    from animal.core.taxa import (
        BODY_PLANS, PHYLA, animal_taxon_to_dict,
        list_animal_taxa as _list,
    )
    p = (phylum or "").strip()
    b = (body_plan or "").strip()
    if p and p not in PHYLA:
        return [{
            "error": f"Unknown phylum {p!r}; valid: "
                     f"{', '.join(PHYLA)}.",
        }]
    if b and b not in BODY_PLANS:
        return [{
            "error": f"Unknown body_plan {b!r}; valid: "
                     f"{', '.join(BODY_PLANS)}.",
        }]
    return [animal_taxon_to_dict(t)
            for t in _list(p or None, b or None)]


@action(category="animal-taxa")
def get_animal_taxon(taxon_id: str) -> Dict[str, object]:
    """Return the full record for a single animal taxon by id
    (e.g. ``"caenorhabditis-elegans"`` / ``"drosophila-
    melanogaster"`` / ``"danio-rerio"`` / ``"mus-musculus"`` /
    ``"homo-sapiens"``)."""
    from animal.core.taxa import (
        animal_taxon_to_dict, get_animal_taxon,
    )
    t = get_animal_taxon(taxon_id)
    if t is None:
        return {"error":
                f"Unknown animal taxon id: {taxon_id!r}."}
    return animal_taxon_to_dict(t)


@action(category="animal-taxa")
def find_animal_taxa(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + common
    name + full taxonomic name + class + reproductive strategy
    + ecological role + cross-reference molecule names + notes."""
    from animal.core.taxa import (
        animal_taxon_to_dict, find_animal_taxa,
    )
    return [animal_taxon_to_dict(t)
            for t in find_animal_taxa(needle)]


@action(category="animal-taxa")
def animal_taxa_for_phylum(
    phylum: str,
) -> List[Dict[str, object]]:
    """Return all animal taxa in a single phylum."""
    from animal.core.taxa import (
        PHYLA, animal_taxa_for_phylum, animal_taxon_to_dict,
    )
    if phylum not in PHYLA:
        return [{
            "error": f"Unknown phylum {phylum!r}; valid: "
                     f"{', '.join(PHYLA)}.",
        }]
    return [animal_taxon_to_dict(t)
            for t in animal_taxa_for_phylum(phylum)]


@action(category="animal-taxa")
def open_animal_studio(tab: str = "") -> Dict[str, Any]:
    """Open the Animal Biology Studio main window (lazily
    constructed on first call).  Optional ``tab`` argument
    focuses one of the inner tabs (``"Animal taxa"`` /
    ``"Cell signalling bridge"`` / ``"Tutorials"``).

    Phase AB-1.0 — sixth + final sibling in the multi-studio
    life-sciences platform.  AB-1.0 completes the platform —
    the Cell-signalling-bridge tab makes it the second
    sibling that reads ``cellbio.core.cell_signaling``
    directly (the first was Pharm), confirming the cellbio
    API is stable enough for multiple consumers.
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
        focused: Any = None
        if tab:
            ok = animal_win.switch_to(tab)
            focused = tab if ok else None
        return {"opened": True, "tab": focused}

    return run_on_main_thread_sync(_open)
