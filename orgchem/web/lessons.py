"""Tutorial lessons for the web interface, from the desktop app's own curriculum.

Same pipeline as the Tutorial panel (orgchem/gui/panels/tutorial_panel.py): load the markdown with
load_tutorial_markdown, expand {term:X} macros with expand_term_macros, render with Python-Markdown (fenced_code +
tables). The only web-specific step: glossary links (orgchem-glossary:Term) become #/glossary/Term routes.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote

LEVELS = ("beginner", "intermediate", "advanced", "graduate")
_GLOSS_HREF = re.compile(r'href="orgchem-glossary:([^"]*)"')


def _slug(path: Path) -> str:
    return f"{path.parent.name}/{path.stem}"


@lru_cache(maxsize=1)
def lesson_index() -> list:
    """Every lesson in curriculum order: slug, level, number within the level, title."""
    from orgchem.tutorial.curriculum import CURRICULUM
    out = []
    for level in LEVELS:
        for i, lesson in enumerate(CURRICULUM.get(level, []), start=1):
            path = Path(lesson["path"])
            if not path.exists():
                continue
            out.append({"slug": _slug(path), "level": level, "n": i, "title": lesson["title"],
                        "words": len(path.read_text(encoding="utf-8").split())})
    return out


def _render(md_text: str) -> str:
    import markdown
    from orgchem.tutorial.macros import expand_term_macros
    html = markdown.markdown(expand_term_macros(md_text), extensions=["fenced_code", "tables"])
    return _GLOSS_HREF.sub(lambda m: 'href="#/glossary/' + _attr(unquote(m.group(1))) + '"', html)


def _attr(s: str) -> str:
    from urllib.parse import quote
    return quote(s, safe="")


def lesson(slug: str):
    """One lesson as HTML with its neighbours in curriculum order, or None."""
    from orgchem.tutorial.curriculum import CURRICULUM
    from orgchem.tutorial.loader import load_tutorial_markdown
    idx = lesson_index()
    pos = next((i for i, e in enumerate(idx) if e["slug"] == slug), None)
    if pos is None:
        return None
    entry = idx[pos]
    path = next(Path(le["path"]) for le in CURRICULUM[entry["level"]] if _slug(Path(le["path"])) == slug)
    html = _render(load_tutorial_markdown(path))
    nb = lambda j: ({"slug": idx[j]["slug"], "title": idx[j]["title"]} if 0 <= j < len(idx) else None)  # noqa: E731
    return dict(entry, html=html, prev=nb(pos - 1), next=nb(pos + 1),
                source=f"orgchem/tutorial/content/{slug}.md")
