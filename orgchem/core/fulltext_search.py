"""Phase 33a — cross-surface full-text search.

Linear-scan search over every text-bearing column in the seeded
database: molecule names + descriptions, reaction names +
descriptions + mechanism step titles / descriptions, synthesis
pathway names + descriptions + step notes, glossary terms +
definitions.  Returns ranked :class:`SearchResult` rows with an
excerpt snippet around each match.

Designed as pure Python with no persistent index — the seeded
corpus is ~1000 rows × average ~300 chars of text = ~300 KB, so
a linear pass on every query takes a few ms.  Keeping it simple
avoids the upkeep of an FTS5 index + trigger-driven sync.

**Not imported by the GUI directly** — the Phase-33b dialog
(``gui/dialogs/fulltext_search.py``) and the
``fulltext_search`` agent action both delegate here.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

log = logging.getLogger(__name__)


#: The five kinds of searchable content.  Fixed set; exposed as a
#: tuple so callers can present filter checkboxes without importing
#: the DB layer.
SEARCHABLE_KINDS: Tuple[str, ...] = (
    "molecule", "reaction", "pathway", "glossary", "mechanism-step",
)


@dataclass
class SearchResult:
    """One hit.  Enough information to render a row in the Phase-33b
    dialog AND to route a double-click back to the originating
    surface.

    ``key`` is a kind-specific dict the caller uses to dispatch —
    e.g. ``{"molecule_id": 42}`` for a molecule row,
    ``{"term": "SN2"}`` for a glossary term,
    ``{"reaction_id": 7, "step_index": 2}`` for a mechanism step.
    """

    kind: str
    title: str
    snippet: str
    score: float
    key: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "title": self.title,
            "snippet": self.snippet,
            "score": round(self.score, 4),
            "key": self.key,
        }


# ---------------------------------------------------------------
# Scoring + snippet helpers

_WORD_RE = re.compile(r"\w+", flags=re.UNICODE)


def _score(text: str, query_lower: str) -> float:
    """Cheap relevance score: count occurrences + word-boundary bonus.
    Returns 0.0 when the query is absent."""
    if not text or not query_lower:
        return 0.0
    lo = text.lower()
    n_hits = lo.count(query_lower)
    if n_hits == 0:
        return 0.0
    # Word-boundary bonus: +1 per hit that's flanked by non-word
    # characters (so "SN2" matches "SN2 reaction" with the bonus,
    # but "psndata" doesn't).
    bonus = 0
    escaped = re.escape(query_lower)
    for m in re.finditer(rf"\b{escaped}\b", lo):
        bonus += 1
    return float(n_hits) + 0.5 * bonus


def _snippet(text: str, query_lower: str, window: int = 60) -> str:
    """Extract a context excerpt around the first hit in *text*."""
    if not text:
        return ""
    lo = text.lower()
    idx = lo.find(query_lower)
    if idx < 0:
        # Fallback: return the text head.
        return text[: window * 2].replace("\n", " ")
    start = max(0, idx - window)
    end = min(len(text), idx + len(query_lower) + window)
    excerpt = text[start:end].replace("\n", " ").strip()
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(text) else ""
    return prefix + excerpt + suffix


# ---------------------------------------------------------------
# Corpus builders — one per model.  Each returns an iterable of
# (kind, title, text_blob, key_dict) tuples.  Blob gets searched;
# title gets a big score multiplier.

_TITLE_BOOST = 3.0


def _iter_molecules() -> Iterable[Tuple[str, str, str, Dict[str, Any]]]:
    from orgchem.db.session import session_scope
    from orgchem.db.models import Molecule
    with session_scope() as s:
        for m in s.query(Molecule).all():
            blob_parts = [m.name or "", m.smiles or "", m.formula or ""]
            if m.source:
                blob_parts.append(m.source)
            if m.properties_json:
                # Include any tutor notes.
                try:
                    p = json.loads(m.properties_json)
                    note = p.get("tutor_notes") or ""
                    if note:
                        blob_parts.append(note)
                except Exception:
                    pass
            if m.synonyms_json:
                try:
                    syns = json.loads(m.synonyms_json) or []
                    blob_parts.extend(str(x) for x in syns)
                except Exception:
                    pass
            yield ("molecule",
                   m.name or f"Molecule #{m.id}",
                   " ".join(blob_parts),
                   {"molecule_id": m.id, "smiles": m.smiles})


def _iter_reactions() -> Iterable[Tuple[str, str, str, Dict[str, Any]]]:
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction
    with session_scope() as s:
        for r in s.query(Reaction).all():
            blob = " ".join([r.name or "", r.category or "",
                             r.description or ""])
            yield ("reaction",
                   r.name or f"Reaction #{r.id}",
                   blob,
                   {"reaction_id": r.id})


def _iter_mechanism_steps() -> Iterable[Tuple[str, str, str,
                                              Dict[str, Any]]]:
    """Mechanism steps live inside ``Reaction.mechanism_json``.
    Surface each step as its own searchable row so someone
    searching for 'oxime' lands on the Beckmann step, not just
    on the whole Nylon-6 description."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction
    with session_scope() as s:
        for r in s.query(Reaction).all():
            if not r.mechanism_json:
                continue
            try:
                mech = json.loads(r.mechanism_json)
            except Exception:
                continue
            for i, step in enumerate(mech.get("steps", [])):
                title = step.get("title") or f"Step {i+1}"
                desc = step.get("description") or ""
                blob = " ".join([title, desc, step.get("smiles", "")])
                yield ("mechanism-step",
                       f"{r.name} — {title}",
                       blob,
                       {"reaction_id": r.id, "step_index": i})


def _iter_pathways() -> Iterable[Tuple[str, str, str, Dict[str, Any]]]:
    from orgchem.db.session import session_scope
    from orgchem.db.models import SynthesisPathway, SynthesisStep
    with session_scope() as s:
        for p in s.query(SynthesisPathway).all():
            blob_parts = [p.name or "", p.target_name or "",
                          p.description or "", p.category or "",
                          p.source or ""]
            # Fold in each step's notes + reagents + conditions —
            # that's where the teaching payload hides.
            for step in s.query(SynthesisStep).filter_by(
                    pathway_id=p.id).all():
                blob_parts.extend([
                    step.reaction_smiles or "",
                    step.reagents or "",
                    step.conditions or "",
                    step.notes or "",
                ])
            yield ("pathway",
                   p.name or f"Pathway #{p.id}",
                   " ".join(blob_parts),
                   {"pathway_id": p.id})


def _iter_glossary() -> Iterable[Tuple[str, str, str, Dict[str, Any]]]:
    from orgchem.db.session import session_scope
    from orgchem.db.models import GlossaryTerm
    with session_scope() as s:
        for g in s.query(GlossaryTerm).all():
            blob_parts = [g.term or "", g.definition_md or "",
                          g.category or ""]
            if g.aliases_json:
                try:
                    aliases = json.loads(g.aliases_json) or []
                    blob_parts.extend(str(x) for x in aliases)
                except Exception:
                    pass
            yield ("glossary",
                   g.term,
                   " ".join(blob_parts),
                   {"term": g.term})


_BUILDERS = {
    "molecule":       _iter_molecules,
    "reaction":       _iter_reactions,
    "mechanism-step": _iter_mechanism_steps,
    "pathway":        _iter_pathways,
    "glossary":       _iter_glossary,
}


def search(
    query: str,
    kinds: Optional[Iterable[str]] = None,
    limit: int = 50,
) -> List[SearchResult]:
    """Run a full-text search across the seeded corpus.

    Args:
        query: the search string.  Case-insensitive, substring
            match.  Whitespace-stripped; empty query returns
            an empty list.
        kinds: which content kinds to include (see
            :data:`SEARCHABLE_KINDS`).  ``None`` = all.
        limit: cap on results returned.

    Returns a list of :class:`SearchResult` sorted by descending
    score.  Title hits always rank above body-only hits because
    of the ``_TITLE_BOOST`` multiplier.
    """
    q = (query or "").strip()
    if not q:
        return []
    query_lower = q.lower()

    wanted = set(kinds) if kinds is not None else set(SEARCHABLE_KINDS)
    unknown = wanted - set(SEARCHABLE_KINDS)
    if unknown:
        raise ValueError(
            f"unknown search kind(s): {sorted(unknown)}. "
            f"Valid: {list(SEARCHABLE_KINDS)}")

    results: List[SearchResult] = []
    for kind, builder in _BUILDERS.items():
        if kind not in wanted:
            continue
        try:
            for (_, title, blob, key) in builder():
                title_score = _score(title, query_lower) * _TITLE_BOOST
                body_score = _score(blob, query_lower)
                total = title_score + body_score
                if total <= 0:
                    continue
                snippet = _snippet(title, query_lower) \
                    if title_score > 0 else _snippet(blob, query_lower)
                results.append(SearchResult(
                    kind=kind, title=title, snippet=snippet,
                    score=total, key=key,
                ))
        except Exception:
            log.exception("Search builder for %r failed", kind)

    results.sort(key=lambda r: (-r.score, r.kind, r.title))
    return results[:limit]
