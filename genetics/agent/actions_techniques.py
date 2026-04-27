"""Phase GM-1.0 (round 230) — agent actions for the Genetics
+ Molecular Biology Studio molecular-biology-techniques
catalogue + Genetics main-window opener.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="genetics-techniques")
def list_genetics_techniques(
    category: str = "",
) -> List[Dict[str, object]]:
    """Return molecular-biology techniques, optionally filtered
    by category (``"pcr"`` / ``"sequencing"`` / ``"cloning"``
    / ``"crispr"`` / ``"blot"`` / ``"in-situ"`` /
    ``"chromatin"`` / ``"transcriptomics"`` / ``"spatial"`` /
    ``"proteomics"`` / ``"interaction"`` / ``"structural"`` /
    ``"epigenetics"`` / ``"delivery"``)."""
    from genetics.core.techniques import (
        CATEGORIES, list_techniques as _list,
        technique_to_dict,
    )
    c = (category or "").strip()
    if c and c not in CATEGORIES:
        return [{
            "error": f"Unknown category {c!r}; valid: "
                     f"{', '.join(CATEGORIES)}.",
        }]
    return [technique_to_dict(t)
            for t in _list(c or None)]


@action(category="genetics-techniques")
def get_genetics_technique(
    technique_id: str,
) -> Dict[str, object]:
    """Return the full record for a single molecular-biology
    technique by id (e.g. ``"qpcr"`` / ``"illumina-short-
    read"`` / ``"crispr-cas9"`` / ``"chip-seq"`` /
    ``"scrna-seq"`` / ``"visium"``)."""
    from genetics.core.techniques import (
        get_technique, technique_to_dict,
    )
    t = get_technique(technique_id)
    if t is None:
        return {"error":
                f"Unknown genetics technique id: "
                f"{technique_id!r}."}
    return technique_to_dict(t)


@action(category="genetics-techniques")
def find_genetics_techniques(
    needle: str,
) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    abbreviation + category + principle + sample types +
    typical readout + key reagents + representative platforms
    + notes."""
    from genetics.core.techniques import (
        find_techniques, technique_to_dict,
    )
    return [technique_to_dict(t)
            for t in find_techniques(needle)]


@action(category="genetics-techniques")
def genetics_techniques_for_application(
    application: str,
) -> List[Dict[str, object]]:
    """Return all techniques whose typical-readout, principle,
    or notes match the given application keyword (e.g.
    ``"diagnostic"`` / ``"single-cell"`` / ``"variant
    calling"`` / ``"chromatin"``)."""
    from genetics.core.techniques import (
        techniques_for_application, technique_to_dict,
    )
    return [technique_to_dict(t)
            for t in techniques_for_application(application)]


@action(category="genetics-techniques")
def open_genetics_studio(tab: str = "") -> Dict[str, Any]:
    """Open the Genetics + Molecular Biology Studio main
    window (lazily constructed on first call).  Optional
    ``tab`` argument focuses one of the inner tabs
    (``"Techniques"`` / ``"Cross-references"`` /
    ``"Tutorials"``).

    Phase GM-1.0 — seventh sibling in the multi-studio
    life-sciences platform; first round of the new
    -1-extension phase.  GM-1.0's Cross-references tab
    bridges into ``biochem.core.enzymes`` filtered to
    nucleic-acid-acting enzymes (DNA / RNA polymerases,
    ligases, restriction enzymes, reverse transcriptases,
    etc.), with hand-off to Biochem Studio.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import (
        run_on_main_thread_sync,
    )

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from genetics.gui.windows.genetics_main_window import (
            GeneticsMainWindow,
        )
        gen_win = getattr(win, "_genetics_window", None)
        if gen_win is None:
            gen_win = GeneticsMainWindow(parent=win)
            win._genetics_window = gen_win
        gen_win.show()
        gen_win.raise_()
        gen_win.activateWindow()
        focused: Any = None
        if tab:
            ok = gen_win.switch_to(tab)
            focused = tab if ok else None
        return {"opened": True, "tab": focused}

    return run_on_main_thread_sync(_open)
