"""Phase 33a — agent action surfacing the cross-surface full-text
search engine from :mod:`orgchem.core.fulltext_search`.

Headless / scripting layer.  The GUI-facing Ctrl+F dialog (Phase 33b)
layers on top of this action rather than calling the core directly,
so LLM-generated scripts and human-GUI navigation share one surface.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from orgchem.agent.actions import action
from orgchem.core.fulltext_search import SEARCHABLE_KINDS, search


@action(category="search")
def fulltext_search(query: str,
                    limit: int = 50,
                    kinds: str = "") -> Dict[str, Any]:
    """Search every text-bearing column in the seeded database for
    *query* and return ranked matches.

    Args:
        query: the search string.  Case-insensitive, substring
            match.  Empty string returns 0 results.
        limit: cap on number of results returned (default 50).
        kinds: optional comma-separated list restricting which
            kinds of content to search.  Valid kinds:
            ``molecule`` / ``reaction`` / ``pathway`` /
            ``glossary`` / ``mechanism-step``.  Empty = all.

    Returns ``{query, n_results, results: [...]}`` where each
    result carries ``{kind, title, snippet, score, key}``.  The
    ``key`` sub-dict tells the caller how to route a double-click
    back to the originating surface (molecule_id, term, pathway_id,
    reaction_id + step_index, …).
    """
    kinds_list: Optional[List[str]] = None
    if kinds:
        kinds_list = [k.strip() for k in kinds.split(",") if k.strip()]
        # Raise early with a helpful message if a bad kind is passed.
        unknown = [k for k in kinds_list if k not in SEARCHABLE_KINDS]
        if unknown:
            return {
                "error": f"Unknown kind(s): {unknown}. "
                         f"Valid: {list(SEARCHABLE_KINDS)}",
                "query": query, "n_results": 0, "results": [],
            }

    results = search(query, kinds=kinds_list, limit=limit)
    return {
        "query": query,
        "n_results": len(results),
        "results": [r.to_dict() for r in results],
    }
