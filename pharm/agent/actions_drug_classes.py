"""Phase PH-1.0 (round 214) — agent actions for the
Pharmacology Studio drug-class catalogue + Pharm main-window
opener.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="pharm-drugs")
def list_drug_classes(
    target_class: str = "",
    therapeutic_area: str = "",
) -> List[Dict[str, object]]:
    """Return drug classes, optionally filtered by molecular
    target class (``"GPCR"`` / ``"RTK"`` / ``"ion-channel"`` /
    ``"NHR"`` / ``"enzyme"`` / ``"transporter"`` /
    ``"antibody-target"`` / ``"nucleic-acid"`` / ``"other"``)
    and / or therapeutic area (``"cardiovascular"`` /
    ``"metabolic"`` / ``"neurology-psychiatry"`` /
    ``"oncology"`` / ``"infectious"`` /
    ``"inflammation-immunology"`` / ``"pulmonology"`` /
    ``"endocrinology"`` / ``"haematology"`` /
    ``"gastrointestinal"`` / ``"pain"``)."""
    from pharm.core.drug_classes import (
        TARGET_CLASSES, THERAPEUTIC_AREAS,
        drug_class_to_dict, list_drug_classes as _list,
    )
    tc = (target_class or "").strip()
    ta = (therapeutic_area or "").strip()
    if tc and tc not in TARGET_CLASSES:
        return [{
            "error": f"Unknown target_class {tc!r}; valid: "
                     f"{', '.join(TARGET_CLASSES)}.",
        }]
    if ta and ta not in THERAPEUTIC_AREAS:
        return [{
            "error": f"Unknown therapeutic_area {ta!r}; valid: "
                     f"{', '.join(THERAPEUTIC_AREAS)}.",
        }]
    return [drug_class_to_dict(d)
            for d in _list(tc or None, ta or None)]


@action(category="pharm-drugs")
def get_drug_class(class_id: str) -> Dict[str, object]:
    """Return the full record for a single drug class by id
    (e.g. ``"beta-blockers"`` / ``"ace-inhibitors"`` /
    ``"statins"`` / ``"ssris"`` / ``"opioids"`` /
    ``"checkpoint-inhibitors"`` / ``"glp1-agonists"``)."""
    from pharm.core.drug_classes import (
        drug_class_to_dict, get_drug_class,
    )
    d = get_drug_class(class_id)
    if d is None:
        return {"error":
                f"Unknown drug class id: {class_id!r}."}
    return drug_class_to_dict(d)


@action(category="pharm-drugs")
def find_drug_classes(needle: str) -> List[Dict[str, object]]:
    """Case-insensitive substring search across id + name +
    mechanism + molecular target + typical agents + clinical
    use + side effects."""
    from pharm.core.drug_classes import (
        drug_class_to_dict, find_drug_classes,
    )
    return [drug_class_to_dict(d) for d in find_drug_classes(needle)]


@action(category="pharm-drugs")
def drug_classes_for_target(
    target_class: str,
) -> List[Dict[str, object]]:
    """Return all drug classes hitting a specific target type."""
    from pharm.core.drug_classes import (
        TARGET_CLASSES, drug_class_to_dict,
        drug_classes_for_target,
    )
    if target_class not in TARGET_CLASSES:
        return [{
            "error": f"Unknown target_class {target_class!r}; "
                     f"valid: {', '.join(TARGET_CLASSES)}.",
        }]
    return [drug_class_to_dict(d)
            for d in drug_classes_for_target(target_class)]


@action(category="pharm-drugs")
def open_pharm_studio(tab: str = "") -> Dict[str, Any]:
    """Open the Pharmacology Studio main window (lazily
    constructed on first call).  Optional ``tab`` argument
    focuses one of the inner tabs (``"Drug classes"`` /
    ``"Bridges"`` / ``"Tutorials"``).

    Phase PH-1.0 — third sibling in the multi-studio life-
    sciences platform.  The Bridges tab surfaces both
    ``biochem.core.enzymes`` (drug-targetable) AND
    ``cellbio.core.cell_signaling`` (drug-target receptor
    pathways) read-only — multi-hop cross-studio data
    sharing.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error":
                "Main window not available — run the app "
                "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from pharm.gui.windows.pharm_main_window import (
            PharmMainWindow,
        )
        pharm_win = getattr(win, "_pharm_window", None)
        if pharm_win is None:
            pharm_win = PharmMainWindow(parent=win)
            win._pharm_window = pharm_win
        pharm_win.show()
        pharm_win.raise_()
        pharm_win.activateWindow()
        focused: Any = None
        if tab:
            ok = pharm_win.switch_to(tab)
            focused = tab if ok else None
        return {"opened": True, "tab": focused}

    return run_on_main_thread_sync(_open)
