"""Phase 36h round 127 — agent actions for the molecular drawing tool.

Gives the tutor / stdio bridge / Python drivers the same access to
the Phase-36g :class:`DrawingToolDialog` that a human gets via
*Tools → Drawing tool…*.  All four actions marshal onto the Qt
main thread via ``run_on_main_thread_sync`` so macOS doesn't abort
on an off-main NSWindow.

Actions
-------
``open_drawing_tool(smiles="")``
    Pop up the drawing dialog.  Optional ``smiles`` preloads the
    canvas so *"open in drawing tool and edit ethene"* is one call.
``drawing_to_smiles()``
    Return the current canvas as a canonical SMILES string.
``drawing_export(path)``
    Write the current canvas to ``path``; format selected by suffix
    (``.png`` / ``.svg`` / ``.mol``).
``drawing_clear()``
    Wipe the canvas so a script can start from a clean slate.
"""
from __future__ import annotations
import logging
from typing import Any, Dict

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


def _dialog():
    """Resolve the live :class:`DrawingToolDialog` singleton.

    Returns ``None`` if the GUI layer isn't reachable (headless
    without a main window, Qt bindings missing, etc.).
    """
    try:
        from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    except Exception:  # noqa: BLE001
        return None
    return DrawingToolDialog._instance


# ---- open ---------------------------------------------------------

@action(category="drawing")
def open_drawing_tool(smiles: str = "") -> Dict[str, Any]:
    """Show the molecular drawing dialog (Phase 36g singleton).

    Pass a SMILES to preload the canvas — useful for *"edit this
    molecule graphically"* flows where the tutor hands an existing
    structure to the drawing tool.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.main_window()
    if win is None:
        return {"error": "Main window not available — run the app "
                         "interactively or via HeadlessApp first."}

    def _open() -> Dict[str, Any]:
        from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
        dlg = DrawingToolDialog.singleton(
            parent=win, seed_smiles=smiles or "")
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        return {
            "opened": True,
            "seeded_smiles": bool(smiles),
            "current_smiles": dlg.panel.current_smiles(),
        }

    return run_on_main_thread_sync(_open)


# ---- read canvas --------------------------------------------------

@action(category="drawing")
def drawing_to_smiles() -> Dict[str, Any]:
    """Return the canonical SMILES for whatever's on the canvas.

    Empty canvas returns ``{"smiles": "", "n_atoms": 0, "n_bonds": 0}``.
    """
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    dlg = _dialog()
    if dlg is None:
        return {"error": "Drawing tool has not been opened yet — "
                         "call `open_drawing_tool` first."}

    def _read() -> Dict[str, Any]:
        s = dlg.panel.get_structure()
        return {
            "smiles": dlg.panel.current_smiles(),
            "n_atoms": s.n_atoms,
            "n_bonds": s.n_bonds,
        }

    return run_on_main_thread_sync(_read)


# ---- export -------------------------------------------------------

@action(category="drawing")
def drawing_export(path: str) -> Dict[str, Any]:
    """Save the current drawing to *path*.

    Format is chosen by suffix — ``.png`` / ``.svg`` go through
    ``render.export.export_molecule_2d``, ``.mol`` goes through
    ``core.drawing.structure_to_molblock`` so 2D coords are preserved.
    """
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    dlg = _dialog()
    if dlg is None:
        return {"error": "Drawing tool has not been opened yet — "
                         "call `open_drawing_tool` first."}

    lower = path.lower()
    if not any(lower.endswith(ext)
               for ext in (".png", ".svg", ".mol")):
        return {"error": "Unsupported file extension — "
                         "use .png, .svg, or .mol."}

    def _write() -> Dict[str, Any]:
        smi = dlg.panel.current_smiles()
        if not smi:
            return {"error": "Canvas is empty — draw at least one "
                             "atom before exporting."}
        try:
            if lower.endswith(".mol"):
                from orgchem.core.drawing import structure_to_molblock
                block = structure_to_molblock(dlg.panel.get_structure())
                if block is None:
                    return {"error": "mol-block conversion failed."}
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(block)
            else:
                from orgchem.core.formats import mol_from_smiles
                from orgchem.render.export import export_molecule_2d
                mol = mol_from_smiles(smi)
                export_molecule_2d(mol, path)
        except Exception as e:  # noqa: BLE001
            log.exception("drawing_export failed")
            return {"error": str(e)}
        return {"saved": True, "path": path, "format": lower[-3:]}

    return run_on_main_thread_sync(_write)


# ---- reaction scheme (Phase 36f.1, round 131) -------------------

@action(category="drawing")
def make_reaction_scheme(
    lhs_smiles: str,
    rhs_smiles: str,
    arrow: str = "forward",
    reagents: str = "",
) -> Dict[str, Any]:
    """Bundle two SMILES strings into a reaction-SMILES record.

    The natural Phase-36f workflow before the canvas-arrow GUI
    lands: the user (or tutor) drew two structures separately,
    knows which is the reactant and which is the product, and
    wants to ship them off to the Reactions tab as a single
    rendered scheme.  No GUI required — pure headless call.

    Returns ``{"reaction_smiles": str, "lhs_canonical": str,
    "rhs_canonical": str, "arrow": str, "reagents": str,
    "balanced": bool}`` on success, ``{"error": str}`` on parse
    failure.  ``balanced`` is the heavy-atom-count sanity hint
    from :func:`is_balanced_atom_counts` — useful as a "did the
    student forget the leaving group?" prompt.
    """
    from orgchem.core.drawing_scheme import (
        Scheme, is_balanced_atom_counts,
    )

    if arrow not in ("forward", "reversible"):
        return {"error": f"Unknown arrow type {arrow!r}; "
                         "use 'forward' or 'reversible'."}
    scheme = Scheme.from_smiles_pair(
        lhs_smiles or "", rhs_smiles or "",
        arrow=arrow, reagents=reagents or "",
    )
    if scheme is None:
        return {"error": "Could not parse one or both SMILES "
                         "strings — check syntax and try again."}
    rxn = scheme.to_reaction_smiles()
    if rxn is None:
        return {"error": "Could not assemble reaction SMILES "
                         "(structure → SMILES conversion failed)."}
    return {
        "reaction_smiles": rxn,
        "lhs_canonical": scheme.lhs_smiles(),
        "rhs_canonical": scheme.rhs_smiles(),
        "arrow": scheme.arrow,
        "reagents": scheme.reagents,
        "balanced": is_balanced_atom_counts(scheme),
    }


# ---- clear --------------------------------------------------------

@action(category="drawing")
def drawing_clear() -> Dict[str, Any]:
    """Wipe the canvas — like clicking the toolbar's *Clear* button.

    Safe to call even on an already-empty canvas.
    """
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    dlg = _dialog()
    if dlg is None:
        return {"error": "Drawing tool has not been opened yet — "
                         "call `open_drawing_tool` first."}

    def _clear() -> Dict[str, Any]:
        dlg.panel.clear()
        return {"cleared": True}

    return run_on_main_thread_sync(_clear)
