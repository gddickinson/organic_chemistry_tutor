"""Agent actions for reactions, mechanisms, and multi-molecule comparison.

Separated from :mod:`orgchem.agent.library` to keep each file under the
500-line project cap. Importing :mod:`orgchem.agent.library` re-exports
this module, so registration still happens on any ``from orgchem.agent
import library`` or ``orgchem.agent.actions.invoke(...)``.
"""
from __future__ import annotations
import json
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action
from orgchem.messaging.bus import bus

log = logging.getLogger(__name__)


# ---- Reactions ------------------------------------------------------

@action(category="reaction")
def list_reactions(filter: str = "") -> List[Dict[str, Any]]:
    """List reactions in the database, optionally filtered by name/category substring."""
    from orgchem.db.queries import list_reactions as _lr
    rows = _lr(query=filter or None)
    return [{"id": r.id, "name": r.name, "category": r.category or "",
             "smiles": r.reaction_smarts} for r in rows]


@action(category="reaction")
def show_reaction(name_or_id: str) -> Dict[str, Any]:
    """Display a reaction in the Reactions tab by name, id, or substring match."""
    from orgchem.agent.controller import main_window
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from sqlalchemy import select, or_

    with session_scope() as s:
        if name_or_id.isdigit():
            row = s.get(DBRxn, int(name_or_id))
        else:
            q = f"%{name_or_id}%"
            stmt = select(DBRxn).where(
                or_(DBRxn.name.ilike(q), DBRxn.category.ilike(q))
            ).limit(1)
            row = s.scalars(stmt).first()
        if row is None:
            return {"error": f"No reaction matching {name_or_id!r}"}
        payload = {"id": row.id, "name": row.name,
                   "category": row.category or "",
                   "smiles": row.reaction_smarts,
                   "description": row.description or ""}

    win = main_window()
    if win is not None and hasattr(win, "reactions"):
        from orgchem.agent._gui_dispatch import run_on_main_thread
        rid = int(payload["id"])

        def _show():
            win.reactions._display(rid)
            for i in range(win.tabs.count()):
                if win.tabs.tabText(i) == "Reactions":
                    win.tabs.setCurrentIndex(i)
                    break
        run_on_main_thread(_show)
    bus().reaction_selected.emit(int(payload["id"]))
    return payload


@action(category="reaction")
def export_reaction_by_id(reaction_id: int, path: str,
                          width: int = 1200, height: int = 360) -> Dict[str, Any]:
    """Export a reaction scheme to SVG/PNG by database id."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.render.draw_reaction import export_reaction

    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        smi, name = row.reaction_smarts, row.name
    out = export_reaction(smi, path, width=width, height=height)
    return {"path": str(out), "name": name,
            "format": out.suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}


@action(category="reaction")
def export_reaction_trajectory_html(reaction_id: int, path: str,
                                    n_frames: int = 24) -> Dict[str, Any]:
    """Build a standalone 3Dmol.js animation HTML for a mapped reaction.

    Writes an HTML file you can open in any browser. Inside, atoms morph
    from reactant to product positions over `n_frames` linearly-interpolated
    frames; bonds are inferred by proximity each frame, so you see bonds
    appear and disappear as the atoms move.
    """
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.core.reaction_trajectory import build_xyz_trajectory
    from orgchem.render.draw_reaction_3d import build_trajectory_html
    from pathlib import Path as _P

    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        mapped = row.reaction_smarts_mapped
        name = row.name
    if not mapped:
        return {"error": f"Reaction {name!r} has no atom-mapped SMARTS."}

    xyz = build_xyz_trajectory(mapped, n_frames=n_frames)
    html = build_trajectory_html(xyz, title=name)
    p = _P(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    return {"path": str(p), "name": name, "frames": n_frames,
            "size_bytes": p.stat().st_size}


@action(category="reaction")
def play_reaction_trajectory(name_or_id: str) -> Dict[str, Any]:
    """Open the 3D trajectory player dialog for a reaction (by id, name, or substring)."""
    from orgchem.agent.controller import require_main_window
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from sqlalchemy import select

    with session_scope() as s:
        if name_or_id.isdigit():
            row = s.get(DBRxn, int(name_or_id))
        else:
            q = f"%{name_or_id}%"
            row = s.scalars(
                select(DBRxn).where(DBRxn.name.ilike(q)).limit(1)
            ).first()
        if row is None:
            return {"error": f"No reaction matching {name_or_id!r}"}
        if not row.reaction_smarts_mapped:
            return {"error": f"Reaction {row.name!r} has no mapped SMARTS."}
        mapped = row.reaction_smarts_mapped
        name = row.name
        rid = row.id

    win = require_main_window()
    from orgchem.agent._gui_dispatch import run_on_main_thread
    from orgchem.gui.dialogs.reaction_trajectory_player import (
        ReactionTrajectoryPlayerDialog,
    )

    def _open():
        dlg = ReactionTrajectoryPlayerDialog(mapped, name, parent=win)
        dlg.show()
        win._trajectory_dialog = dlg  # pin ref
    run_on_main_thread(_open)
    return {"id": rid, "name": name}


@action(category="reaction")
def export_reaction_3d(reaction_id: int, path: str,
                       width: int = 1200, height: int = 520) -> Dict[str, Any]:
    """Render a reaction in 3D side-by-side (reactants | → | products) to PNG.

    Requires an atom-mapped SMARTS in the reaction's
    ``reaction_smarts_mapped`` column. Atoms are coloured by map number so
    "the same atom" has the same hue in reactants and products. Bonds that
    break are drawn in red on the reactant panel; bonds that form are
    drawn in green on the product panel.
    """
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.render.draw_reaction_3d import render_png

    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        mapped = row.reaction_smarts_mapped
        name = row.name
    if not mapped:
        return {"error": f"Reaction {name!r} has no atom-mapped SMARTS; "
                         f"the 3D renderer can't correlate atoms across the arrow."}
    out = render_png(mapped, path, width=width, height=height)
    return {"path": str(out), "name": name,
            "size_bytes": out.stat().st_size}


# ---- Mechanisms -----------------------------------------------------

@action(category="mechanism")
def list_mechanisms() -> List[Dict[str, Any]]:
    """List reactions that have a recorded arrow-pushing mechanism."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from sqlalchemy import select
    out: List[Dict[str, Any]] = []
    with session_scope() as s:
        for row in s.scalars(select(DBRxn).where(DBRxn.mechanism_json.isnot(None))):
            try:
                n_steps = len(json.loads(row.mechanism_json).get("steps", []))
            except Exception:
                n_steps = 0
            out.append({
                "id": row.id, "name": row.name,
                "category": row.category or "", "steps": n_steps,
            })
    return out


@action(category="mechanism")
def get_mechanism_details(name_or_id: str) -> Dict[str, Any]:
    """Return the **full mechanism JSON** for a reaction — every step's
    title, description, SMILES, arrow list, lone-pair decorations.

    Use this for programmatic / LLM-driven arrow-pushing workflows
    where :func:`open_mechanism` (which just launches the GUI
    player dialog and returns metadata) isn't enough.  Accepts a
    database id (as string), a full reaction name, or a name
    substring — same lookup rules as :func:`open_mechanism`.

    Returns ``{error: "..."}`` if no matching reaction or if the
    match has no stored ``mechanism_json``.
    """
    import json as _json
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.db.session import session_scope
    from sqlalchemy import select

    with session_scope() as s:
        if name_or_id.isdigit():
            row = s.get(DBRxn, int(name_or_id))
        else:
            q = f"%{name_or_id}%"
            stmt = select(DBRxn).where(DBRxn.name.ilike(q)).limit(1)
            row = s.scalars(stmt).first()
        if row is None:
            return {"error": f"No reaction matching {name_or_id!r}"}
        if not row.mechanism_json:
            return {"error": f"{row.name!r} has no recorded mechanism"}
        try:
            mech = _json.loads(row.mechanism_json)
        except Exception as e:
            return {"error": f"Mechanism JSON invalid: {e}"}
        return {
            "id": row.id,
            "name": row.name,
            "category": row.category,
            "description": row.description,
            "mechanism": mech,
        }


@action(category="mechanism")
def open_mechanism(name_or_id: str) -> Dict[str, Any]:
    """Open the mechanism player for a reaction (by name, id, or substring)."""
    from orgchem.agent.controller import main_window
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.core.mechanism import Mechanism
    from sqlalchemy import select

    with session_scope() as s:
        if name_or_id.isdigit():
            row = s.get(DBRxn, int(name_or_id))
        else:
            q = f"%{name_or_id}%"
            stmt = select(DBRxn).where(DBRxn.name.ilike(q)).limit(1)
            row = s.scalars(stmt).first()
        if row is None:
            return {"error": f"No reaction matching {name_or_id!r}"}
        if not row.mechanism_json:
            return {"error": f"{row.name!r} has no recorded mechanism"}
        name = row.name
        rid = row.id
        mech_json = row.mechanism_json

    try:
        mech = Mechanism.from_json(mech_json)
    except Exception as e:
        return {"error": f"Mechanism JSON invalid: {e}"}

    win = main_window()
    if win is not None:
        from orgchem.agent._gui_dispatch import run_on_main_thread
        from orgchem.gui.dialogs.mechanism_player import MechanismPlayerDialog

        def _open():
            dlg = MechanismPlayerDialog(mech, name, win)
            dlg.show()
            win._mechanism_dialog = dlg  # pin ref so GC doesn't eat it
        run_on_main_thread(_open)

    return {"id": rid, "name": name, "steps": len(mech)}


@action(category="mechanism")
def export_mechanism_composite(reaction_id: int, path: str) -> Dict[str, Any]:
    """Export the **full-kinetics composite** of a mechanism (Phase 13c).

    Stacks every step of the mechanism into one tall SVG / PNG —
    numbered "Step 1", "Step 2", ... with arrows + descriptions.
    Matches the Schmidt-reaction teaching-figure layout.
    """
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.core.mechanism import Mechanism
    from orgchem.render.draw_mechanism_composite import export_composite
    from orgchem.messaging.errors import RenderError
    from pathlib import Path as _P

    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        if not row.mechanism_json:
            return {"error": f"Reaction {row.name!r} has no mechanism"}
        mech = Mechanism.from_json(row.mechanism_json)
        name = row.name

    try:
        out = export_composite(mech, path, reaction_name=name)
    except RenderError as e:
        return {"error": str(e)}
    return {"path": str(out), "name": name,
            "steps": len(mech),
            "format": _P(out).suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}


@action(category="mechanism")
def export_mechanism_step(reaction_id: int, step_index: int,
                          path: str, width: int = 700, height: int = 520) -> Dict[str, Any]:
    """Export a single mechanism step to SVG. step_index is 0-based."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.core.mechanism import Mechanism
    from orgchem.render.draw_mechanism import render_step_svg
    from pathlib import Path as _P

    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        if not row.mechanism_json:
            return {"error": f"Reaction {row.name!r} has no mechanism"}
        mech = Mechanism.from_json(row.mechanism_json)

    if not (0 <= step_index < len(mech)):
        return {"error": f"step_index {step_index} out of range 0..{len(mech) - 1}"}

    step = mech[step_index]
    p = _P(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    svg = render_step_svg(step, width=width, height=height)
    p.write_text(svg)
    return {"path": str(p), "step": step_index, "title": step.title,
            "size_bytes": p.stat().st_size}


# ---- Energy profiles (Phase 13) -------------------------------------

@action(category="reaction")
def list_energy_profiles() -> List[Dict[str, Any]]:
    """List reactions that have a recorded reaction-coordinate energy profile."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.core.energy_profile import ReactionEnergyProfile
    from sqlalchemy import select
    out: List[Dict[str, Any]] = []
    with session_scope() as s:
        for row in s.scalars(select(DBRxn).where(DBRxn.energy_profile_json.isnot(None))):
            try:
                prof = ReactionEnergyProfile.from_json(row.energy_profile_json)
                points = len(prof)
                unit = prof.energy_unit
            except Exception:
                points, unit = 0, ""
            out.append({
                "id": row.id, "name": row.name,
                "category": row.category or "",
                "points": points, "unit": unit,
            })
    return out


@action(category="reaction")
def get_energy_profile(reaction_id: int) -> Dict[str, Any]:
    """Return the stored energy-profile JSON for a reaction (or an error)."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        if not row.energy_profile_json:
            return {"error": f"Reaction {row.name!r} has no energy profile"}
        return {"id": row.id, "name": row.name,
                "profile": json.loads(row.energy_profile_json)}


@action(category="reaction")
def export_energy_profile(reaction_id: int, path: str,
                          width: int = 900, height: int = 540) -> Dict[str, Any]:
    """Render a reaction's energy profile to PNG or SVG (chosen by extension)."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.core.energy_profile import ReactionEnergyProfile
    from orgchem.render.draw_energy_profile import export_profile

    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        if not row.energy_profile_json:
            return {"error": f"Reaction {row.name!r} has no energy profile"}
        prof = ReactionEnergyProfile.from_json(row.energy_profile_json)
        name = row.name
    prof.reaction_id = reaction_id
    out = export_profile(prof, path, width=width, height=height)
    return {"path": str(out), "name": name,
            "format": out.suffix.lstrip(".").lower(),
            "points": len(prof),
            "size_bytes": out.stat().st_size}


# ---- Multi-molecule comparison --------------------------------------

@action(category="molecule")
def compare_molecules(molecule_ids: list) -> Dict[str, Any]:
    """Fill the Compare tab with up to 4 molecules from the given DB ids."""
    from orgchem.agent.controller import require_main_window
    win = require_main_window()
    if not hasattr(win, "compare"):
        return {"error": "Compare tab unavailable"}
    from orgchem.agent._gui_dispatch import run_on_main_thread
    ids = [int(i) for i in molecule_ids]
    # `set_molecule_ids` returns a count synchronously; it touches
    # widgets so it has to run on main. When called off-main we can't
    # easily round-trip the return value without a lock, so we just
    # report the requested count — the tutor sees the tab fill.
    def _fill():
        win.compare.set_molecule_ids(ids)
        for i in range(win.tabs.count()):
            if win.tabs.tabText(i) == "Compare":
                win.tabs.setCurrentIndex(i)
                break
    run_on_main_thread(_fill)
    return {"loaded": len(ids), "requested": len(molecule_ids)}
