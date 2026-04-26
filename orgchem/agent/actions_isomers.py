"""Phase 48c (round 172) — agent actions for the isomer-
relationship core + dialog.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="isomer")
def find_stereoisomers(
    smiles: str,
    max_results: int = 16,
) -> Dict[str, object]:
    """Enumerate the stereoisomers of a SMILES.

    Wraps :func:`orgchem.core.isomers.enumerate_stereoisomers`
    with ``onlyUnassigned=True`` semantics — a fully-specified
    input returns just itself, an under-specified input
    expands to every consistent stereoisomer (2 unassigned
    centres → 4 isomers, 3 → 8, etc.).  Capped at
    ``max_results``; returns ``{"input_smiles": str,
    "canonical_smiles_list": [str, ...], "truncated": bool}``.
    Unparseable input returns an empty list (not an error)."""
    from orgchem.core.isomers import enumerate_stereoisomers
    res = enumerate_stereoisomers(smiles, max_results=max_results)
    return {
        "input_smiles": res.input_smiles,
        "canonical_smiles_list": list(res.canonical_smiles_list),
        "truncated": res.truncated,
    }


@action(category="isomer")
def find_tautomers(
    smiles: str,
    max_results: int = 16,
) -> Dict[str, object]:
    """Enumerate the tautomers of a SMILES.

    Wraps :func:`orgchem.core.isomers.enumerate_tautomers`,
    which uses RDKit's ``MolStandardize.TautomerEnumerator``
    (covers keto/enol, amide/iminol, hydroxypyridine /
    pyridone, nitroso/oxime, ~ 20 documented rules).  Capped
    at ``max_results``; returns the same dict shape as
    :func:`find_stereoisomers`."""
    from orgchem.core.isomers import enumerate_tautomers
    res = enumerate_tautomers(smiles, max_results=max_results)
    return {
        "input_smiles": res.input_smiles,
        "canonical_smiles_list": list(res.canonical_smiles_list),
        "truncated": res.truncated,
    }


@action(category="isomer")
def classify_isomer_pair(
    smiles_a: str,
    smiles_b: str,
) -> Dict[str, str]:
    """Classify the relationship between two molecules as one
    of the canonical RELATIONSHIPS strings: ``"identical"`` /
    ``"constitutional"`` / ``"enantiomer"`` / ``"diastereomer"``
    / ``"meso"`` / ``"tautomer"`` / ``"different-molecule"``.

    Wraps :func:`orgchem.core.isomers.classify_isomer_relationship`.
    Returns ``{"smiles_a": str, "smiles_b": str,
    "relationship": str, "formula_a": str|None, "formula_b":
    str|None}``."""
    from orgchem.core.isomers import (
        classify_isomer_relationship, molecular_formula,
    )
    rel = classify_isomer_relationship(smiles_a, smiles_b)
    return {
        "smiles_a": smiles_a,
        "smiles_b": smiles_b,
        "relationship": rel,
        "formula_a": molecular_formula(smiles_a),
        "formula_b": molecular_formula(smiles_b),
    }


@action(category="isomer")
def open_isomer_explorer(
    tab: str = "",
) -> Dict[str, Any]:
    """Open the *Tools → Isomer relationships…* dialog
    (Ctrl+Shift+B) and optionally focus a specific tab
    (one of: ``"Stereoisomers"`` / ``"Tautomers"`` /
    ``"Classify pair"``)."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the "
                         "app interactively or via HeadlessApp "
                         "first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.isomer_explorer import (
            IsomerExplorerDialog,
        )
        dlg = IsomerExplorerDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        selected = False
        if tab:
            selected = dlg.select_tab(tab)
        return {
            "opened": True,
            "selected": selected,
            "tab": tab or None,
            "available_tabs": dlg.tab_labels(),
        }

    return run_on_main_thread_sync(_open)
