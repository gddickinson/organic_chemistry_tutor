"""Phase 46c (round 148) — agent actions for the pH +
buffer explorer.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="ph")
def list_pka_acids(category: str = "") -> List[Dict[str, object]]:
    """Return every catalogued acid with pKa values, optionally
    filtered by category (one of: ``"mineral"`` /
    ``"carboxylic"`` / ``"amine"`` / ``"amino-acid"`` /
    ``"phenol"`` / ``"biological-buffer"`` / ``"other"``)."""
    from orgchem.core.ph_explorer import (
        VALID_CATEGORIES, acid_to_dict, list_acids,
    )
    cat = (category or "").strip()
    if cat and cat not in VALID_CATEGORIES:
        return [{
            "error": f"Unknown category {cat!r}; "
                     f"valid: {', '.join(VALID_CATEGORIES)}.",
        }]
    return [acid_to_dict(a) for a in list_acids(cat or None)]


@action(category="ph")
def get_pka_acid(acid_id: str) -> Dict[str, Any]:
    """Return the full record for a single acid by id."""
    from orgchem.core.ph_explorer import acid_to_dict, get_acid
    a = get_acid(acid_id)
    if a is None:
        return {"error": f"Unknown acid id: {acid_id!r}."}
    return acid_to_dict(a)


@action(category="ph")
def find_pka_acids(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    formula + category."""
    from orgchem.core.ph_explorer import (
        acid_to_dict, find_acids,
    )
    return [acid_to_dict(a) for a in find_acids(needle)]


@action(category="ph")
def design_buffer(
    target_pH: float,
    pKa: float,
    total_concentration_M: float,
    volume_L: float = 1.0,
) -> Dict[str, Any]:
    """Buffer-design entry point (Henderson-Hasselbalch +
    capacity warning).  Returns the full mixing recipe — see
    :func:`orgchem.core.ph_explorer.design_buffer` for fields."""
    from orgchem.core.ph_explorer import (
        design_buffer as _design,
    )
    try:
        return _design(
            target_pH=target_pH, pKa=pKa,
            total_concentration_M=total_concentration_M,
            volume_L=volume_L)
    except ValueError as e:
        return {"error": str(e)}


@action(category="ph")
def buffer_capacity(
    total_concentration_M: float,
    pH: float,
    pKa: float,
) -> Dict[str, Any]:
    """β = 2.303 · C_total · α · (1 − α) where α = [A⁻] /
    C_total at the given pH.  Returns the capacity in mol/L
    per pH unit + α + fraction-of-max."""
    from orgchem.core.ph_explorer import (
        buffer_capacity as _bc,
    )
    try:
        return _bc(total_concentration_M=total_concentration_M,
                   pH=pH, pKa=pKa)
    except ValueError as e:
        return {"error": str(e)}


@action(category="ph")
def simulate_titration(
    weak_acid_pKa: float,
    acid_initial_M: float,
    volume_acid_mL: float,
    base_concentration_M: float,
    n_points: int = 50,
) -> Dict[str, Any]:
    """Simulate the titration of a weak acid with a strong
    base (NaOH).  Returns ``points`` as a list of
    ``[volume_mL, pH]`` pairs + the equivalence-point volume."""
    from orgchem.core.ph_explorer import (
        titration_curve as _tc,
    )
    try:
        return _tc(
            weak_acid_pKa=weak_acid_pKa,
            acid_initial_M=acid_initial_M,
            volume_acid_mL=volume_acid_mL,
            base_concentration_M=base_concentration_M,
            n_points=n_points)
    except ValueError as e:
        return {"error": str(e)}


@action(category="ph")
def open_ph_explorer(tab: str = "") -> Dict[str, Any]:
    """Open the *Tools → pH explorer…* dialog and optionally
    focus a specific tab (one of ``Reference`` / ``Buffer
    designer`` / ``Titration curve`` / ``pKa lookup``)."""
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.ph_explorer import (
            PHExplorerDialog,
        )
        dlg = PHExplorerDialog.singleton(parent=win)
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
