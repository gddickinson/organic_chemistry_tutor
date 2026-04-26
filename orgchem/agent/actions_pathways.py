"""Agent actions for synthesis pathways (Phase 8).

Kept in its own module so each feature area's actions stay compartmental
and none of the per-area files cross the 500-line cap.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="synthesis")
def list_pathways(filter: str = "") -> List[Dict[str, Any]]:
    """List seeded synthesis pathways. Optional substring filter matches
    name / target / category."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import SynthesisPathway
    with session_scope() as s:
        q = s.query(SynthesisPathway)
        if filter:
            p = f"%{filter}%"
            q = q.filter(
                SynthesisPathway.name.ilike(p)
                | SynthesisPathway.target_name.ilike(p)
                | SynthesisPathway.category.ilike(p)
            )
        rows = q.order_by(SynthesisPathway.name).all()
        return [{"id": r.id, "name": r.name, "target": r.target_name,
                 "category": r.category or "", "source": r.source or "",
                 "steps": len(r.steps)} for r in rows]


@action(category="synthesis")
def show_pathway(name_or_id: str) -> Dict[str, Any]:
    """Open a synthesis pathway in the Synthesis tab (by id or name substring)."""
    from orgchem.agent.controller import main_window
    from orgchem.db.session import session_scope
    from orgchem.db.models import SynthesisPathway

    name_or_id = str(name_or_id)   # tolerate int from prior tool result
    with session_scope() as s:
        if name_or_id.isdigit():
            row = s.get(SynthesisPathway, int(name_or_id))
        else:
            p = f"%{name_or_id}%"
            row = (s.query(SynthesisPathway)
                    .filter(SynthesisPathway.name.ilike(p)
                            | SynthesisPathway.target_name.ilike(p))
                    .first())
        if row is None:
            return {"error": f"No pathway matching {name_or_id!r}"}
        payload = {"id": row.id, "name": row.name,
                   "target": row.target_name,
                   "steps": len(row.steps),
                   "category": row.category or ""}

    win = main_window()
    if win is not None and hasattr(win, "synthesis"):
        from orgchem.agent._gui_dispatch import run_on_main_thread
        pid = int(payload["id"])

        def _show():
            win.synthesis._display(pid)
            for i in range(win.tabs.count()):
                if win.tabs.tabText(i) == "Synthesis":
                    win.tabs.setCurrentIndex(i)
                    break
        run_on_main_thread(_show)
    return payload


@action(category="synthesis")
def pathway_green_metrics(pathway_id: int) -> Dict[str, Any]:
    """Compute atom-economy metrics for a seeded pathway (Phase 18a).

    Returns per-step atom economy and the overall atom economy (the product
    of the per-step fractions — the fraction of the initial reactant atoms
    that survive all the way to the final product). No experimental yield
    or solvent mass is required; the calculation is purely balanced-equation
    based.
    """
    from orgchem.core.green_metrics import pathway_atom_economy, atom_economy
    from orgchem.db.session import session_scope
    from orgchem.db.models import SynthesisPathway

    with session_scope() as s:
        p = s.get(SynthesisPathway, pathway_id)
        if p is None:
            return {"error": f"No pathway id {pathway_id}"}
        name = p.name
        steps = [(st.step_index, st.reaction_smiles) for st in p.steps]

    if not steps:
        return {"error": f"Pathway {name!r} has no steps"}

    per_step: List[Dict[str, Any]] = []
    for idx, rxn in steps:
        ae = atom_economy(rxn)
        per_step.append({"step": idx + 1, "reaction": rxn, **ae})

    overall = pathway_atom_economy([r for _, r in steps])
    return {"id": pathway_id, "name": name,
            "per_step": per_step, "overall": overall}


@action(category="synthesis")
def compare_pathways_green(pathway_ids: List[int]) -> Dict[str, Any]:
    """Compare multiple seeded pathways on green-chemistry metrics
    (Phase 18a orphan — round 50).

    Accepts a list of pathway DB ids. For each, computes per-step
    atom economy + the overall pathway atom economy via
    :func:`pathway_green_metrics`. Returns a side-by-side comparison
    table plus a ranked summary (best overall AE first). Useful for
    classroom exercises that pit two published routes to the same
    target against each other (e.g. Aspirin direct acetylation vs
    Aspirin via Kolbe-Schmitt; Paracetamol industrial 1-step vs
    Hoechst 3-step).
    """
    if not pathway_ids:
        return {"error": "No pathway_ids supplied"}
    rows: List[Dict[str, Any]] = []
    for pid in pathway_ids:
        m = pathway_green_metrics(int(pid))
        if m.get("error"):
            rows.append({"id": pid, "error": m["error"]})
            continue
        rows.append({
            "id": m["id"], "name": m["name"],
            "n_steps": len(m["per_step"]),
            "overall_atom_economy": m["overall"]["overall_atom_economy"],
            "min_step_atom_economy": min(
                (s.get("atom_economy", 100.0) for s in m["per_step"]),
                default=100.0,
            ),
        })
    valid = [r for r in rows if "error" not in r]
    valid.sort(key=lambda r: r["overall_atom_economy"], reverse=True)
    ranked = [{"rank": i + 1, **r} for i, r in enumerate(valid)]
    return {
        "pathway_count": len(rows),
        "rows": rows,
        "ranking": ranked,
        "best_overall_ae": ranked[0]["overall_atom_economy"] if ranked else None,
    }


@action(category="synthesis")
def reaction_atom_economy(reaction_id: int) -> Dict[str, Any]:
    """Atom economy of a single seeded reaction (Phase 18a)."""
    from orgchem.core.green_metrics import atom_economy
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    with session_scope() as s:
        row = s.get(DBRxn, reaction_id)
        if row is None:
            return {"error": f"No reaction id {reaction_id}"}
        name = row.name
        rxn = row.reaction_smarts
    result = atom_economy(rxn)
    result.update({"id": reaction_id, "name": name})
    return result


@action(category="synthesis")
def export_pathway(pathway_id: int, path: str) -> Dict[str, Any]:
    """Export a synthesis pathway to SVG or PNG (by file extension)."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import SynthesisPathway
    from orgchem.render.draw_pathway import export_pathway as _export
    from pathlib import Path as _P

    with session_scope() as s:
        p = s.get(SynthesisPathway, pathway_id)
        if p is None:
            return {"error": f"No pathway id {pathway_id}"}
        name = p.name
        out = _export(p, path)
    return {"path": str(out), "name": name,
            "format": _P(out).suffix.lstrip(".").lower(),
            "size_bytes": out.stat().st_size}
