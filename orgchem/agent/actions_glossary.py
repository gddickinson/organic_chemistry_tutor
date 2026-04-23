"""Agent actions for the glossary (Phase 11d).

Provides :func:`define`, :func:`list_glossary`, and :func:`search_glossary`
so an LLM can resolve a term it encounters in a tutorial or reaction
description without needing the GUI tab (Phase 11b, which is deferred).
"""
from __future__ import annotations
import json
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


def _row_to_payload(row) -> Dict[str, Any]:
    return {
        "id": row.id,
        "term": row.term,
        "aliases": json.loads(row.aliases_json) if row.aliases_json else [],
        "definition_md": row.definition_md,
        "category": row.category or "",
        "see_also": json.loads(row.see_also_json) if row.see_also_json else [],
    }


@action(category="glossary")
def define(term: str) -> Dict[str, Any]:
    """Look up a glossary term by exact match (case-insensitive) or alias."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import GlossaryTerm
    from sqlalchemy import select, func

    needle = term.strip()
    with session_scope() as s:
        row = s.scalars(select(GlossaryTerm).where(
            func.lower(GlossaryTerm.term) == needle.lower())).first()
        if row is not None:
            return _row_to_payload(row)
        # try aliases
        for r in s.scalars(select(GlossaryTerm)).all():
            aliases = json.loads(r.aliases_json) if r.aliases_json else []
            if any(a.lower() == needle.lower() for a in aliases):
                return _row_to_payload(r)
    return {"error": f"No glossary term matching {term!r}"}


@action(category="glossary")
def list_glossary(category: str = "") -> List[Dict[str, Any]]:
    """Enumerate glossary terms, optionally filtered by category."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import GlossaryTerm
    from sqlalchemy import select
    out: List[Dict[str, Any]] = []
    with session_scope() as s:
        stmt = select(GlossaryTerm).order_by(GlossaryTerm.term)
        if category:
            stmt = stmt.where(GlossaryTerm.category == category)
        for row in s.scalars(stmt):
            out.append({"id": row.id, "term": row.term,
                        "category": row.category or ""})
    return out


@action(category="glossary")
def show_term(term: str) -> Dict[str, Any]:
    """Open the Glossary tab focused on ``term`` (by exact or alias match)."""
    from orgchem.agent.controller import main_window
    r = define(term)
    if "error" in r:
        return r
    win = main_window()
    if win is not None and hasattr(win, "glossary"):
        from orgchem.agent._gui_dispatch import run_on_main_thread
        term_to_focus = r["term"]

        def _show():
            win.glossary.focus_term(term_to_focus)
            for i in range(win.tabs.count()):
                if win.tabs.tabText(i) == "Glossary":
                    win.tabs.setCurrentIndex(i)
                    break
        run_on_main_thread(_show)
    return {"id": r["id"], "term": r["term"]}


@action(category="glossary")
def get_glossary_figure(term: str, path: str,
                        fmt: str = "png") -> Dict[str, Any]:
    """Render the example figure for a glossary term (Phase 26b).

    Looks up the term in the seed list, pulls its ``example_smiles``,
    and writes a fresh PNG / SVG to ``path``. Returns an error dict
    if the term isn't in the glossary, has no example SMILES, or
    rendering fails.
    """
    from orgchem.core.glossary_figures import render_term
    from orgchem.db.seed_glossary import _GLOSSARY
    row = next((e for e in _GLOSSARY if e["term"].lower() == term.lower()),
               None)
    if row is None:
        return {"error": f"Unknown glossary term: {term!r}"}
    smi = row.get("example_smiles")
    if not smi:
        return {"error": f"{term!r} has no example_smiles"}

    from pathlib import Path as _P
    out = _P(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    result = render_term(term, smi, out_dir=out.parent,
                         force=True, fmt=fmt)
    # Move the file to the exact caller-requested path if the
    # auto-generated stem differs.
    if result.rendered and result.path != out:
        out.write_bytes(result.path.read_bytes())
        try:
            result.path.unlink()
        except OSError:
            pass
    if not result.rendered:
        return {"error": result.skipped_reason or "render failed"}
    return {"term": term, "smiles": smi,
            "path": str(out.resolve()),
            "size_bytes": out.stat().st_size, "format": fmt}


@action(category="glossary")
def search_glossary(query: str) -> List[Dict[str, Any]]:
    """Substring search across term, aliases, and definition text."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import GlossaryTerm
    from sqlalchemy import select, or_
    q = query.strip().lower()
    if not q:
        return []
    pat = f"%{q}%"
    out: List[Dict[str, Any]] = []
    with session_scope() as s:
        for row in s.scalars(select(GlossaryTerm).where(
            or_(GlossaryTerm.term.ilike(pat),
                GlossaryTerm.definition_md.ilike(pat),
                GlossaryTerm.aliases_json.ilike(pat)))):
            out.append({"id": row.id, "term": row.term,
                        "category": row.category or ""})
    return out
