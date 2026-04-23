"""Auto-hyperlink glossary terms in free-text content — Phase 11c.

Takes a plain-text blob (a reaction / mechanism description) and
returns HTML where every recognised glossary term is wrapped in an
``orgchem-glossary://{term}`` anchor. The reaction-workspace panel
uses it to turn descriptions into navigable cross-references; the
synthesis-workspace and glossary panels can reuse it later.

Terms are pulled from :mod:`orgchem.db.seed_glossary` so the linker
ships the same vocabulary as the Glossary tab. Aliases are matched
too (e.g. "Zaitsev's rule" resolves to the canonical "Zaitsev's rule"
term even if the text said "Zaitsev").
"""
from __future__ import annotations
import re
from html import escape
from typing import Dict, List, Tuple

_CACHE: Tuple[List[Tuple[str, str]], re.Pattern] | None = None


SCHEME = "orgchem-glossary"


def _load_terms() -> List[Tuple[str, str]]:
    """Return (surface, canonical-term) pairs sorted longest-first.

    Each canonical term contributes one entry, plus one entry per
    alias. Sorting by length descending ensures multi-word terms
    win over shorter sub-matches inside them (e.g. "Zaitsev's rule"
    is tried before "Zaitsev").
    """
    from orgchem.db.seed_glossary import _GLOSSARY
    pairs: List[Tuple[str, str]] = []
    for entry in _GLOSSARY:
        canonical = entry["term"]
        pairs.append((canonical, canonical))
        for alias in entry.get("aliases", []):
            pairs.append((alias, canonical))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def _build_regex(pairs: List[Tuple[str, str]]) -> re.Pattern:
    """Compile a single case-insensitive regex matching any known
    surface form with word boundaries."""
    # Escape and sort longest-first (already sorted).
    alternation = "|".join(re.escape(s) for s, _ in pairs)
    # ``\b`` works for letters and digits but not Greek / apostrophes,
    # so fall back to a lookaround that excludes in-word continuation.
    pattern = rf"(?<![A-Za-z0-9])(?:{alternation})(?![A-Za-z0-9])"
    return re.compile(pattern, re.IGNORECASE)


def _regex() -> Tuple[List[Tuple[str, str]], re.Pattern]:
    global _CACHE
    if _CACHE is None:
        pairs = _load_terms()
        _CACHE = (pairs, _build_regex(pairs))
    return _CACHE


def _surface_to_canonical_lookup(pairs: List[Tuple[str, str]]) -> Dict[str, str]:
    return {s.lower(): canonical for s, canonical in pairs}


def invalidate_cache() -> None:
    """Reset the compiled regex — call if the glossary changes at
    runtime (e.g. inside a unit test that mutates `_GLOSSARY`)."""
    global _CACHE
    _CACHE = None


def autolink(text: str) -> str:
    """Return ``text`` with recognised glossary terms wrapped in
    anchors. Non-matching characters are HTML-escaped so the result
    is safe to feed into :meth:`QTextBrowser.setHtml`.
    """
    if not text:
        return ""
    pairs, rx = _regex()
    lookup = _surface_to_canonical_lookup(pairs)
    out: List[str] = []
    last = 0
    for m in rx.finditer(text):
        start, end = m.span()
        if start > last:
            out.append(escape(text[last:start]))
        surface = text[start:end]
        canonical = lookup.get(surface.lower(), surface)
        # NOTE: use single-colon `scheme:path` (not `scheme://`)
        # so QUrl leaves the term in `url.path()` rather than
        # normalising it into a lower-cased host. Makes the click
        # handler robust for terms with spaces / apostrophes.
        from urllib.parse import quote as _q
        out.append(
            f'<a href="{SCHEME}:{_q(canonical, safe="")}" '
            f'style="color:#1a5fb4; text-decoration:none;">'
            f'{escape(surface)}</a>'
        )
        last = end
    if last < len(text):
        out.append(escape(text[last:]))
    # Preserve newlines when rendering in QTextBrowser.
    return "<br>".join(seg for seg in "".join(out).split("\n"))
