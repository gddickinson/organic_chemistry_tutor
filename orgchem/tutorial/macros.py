"""Tutorial-markdown preprocessor — Phase 11c follow-up.

Supports a single macro that the curriculum markdown files can use
to cross-reference the Glossary tab:

- ``{term:SN2}`` → clickable link to the SN2 glossary entry.
  Body text is the term itself.
- ``{term:SN2|nucleophilic substitution}`` → same link but the
  anchor text is the arbitrary phrase after the pipe. Useful when
  the inline prose needs a natural-reading form that differs from
  the canonical glossary term.

Output is valid markdown (an inline link using the
``orgchem-glossary://`` scheme), so the existing markdown renderer
produces a normal anchor element. The tutorial panel catches
``orgchem-glossary://`` clicks and routes them to the Glossary tab
(same protocol as the reaction-workspace description pane's
Phase 11c autolinker).

The macro is escape-able with a leading backslash:
``\\{term:SN2}`` renders literally as ``{term:SN2}``.
"""
from __future__ import annotations
import re
from urllib.parse import quote


SCHEME = "orgchem-glossary"

# ``{term:SN2}`` or ``{term:SN2|display text}``. ``[^{}|]`` keeps
# both the term id and the display from eating ``{``, ``}``, or
# ``|``, which bounds the macro cleanly. The leading negative
# look-behind preserves the ``\{term:...}`` escape.
_MACRO_RX = re.compile(
    r"(?<!\\)\{term:(?P<term>[^{}|]+?)(?:\|(?P<display>[^{}]+?))?\}"
)
_ESCAPED_RX = re.compile(r"\\\{term:")


def expand_term_macros(markdown_text: str) -> str:
    """Rewrite ``{term:X}`` macros into Markdown links.

    Returns the transformed markdown. Non-macro text is left
    untouched so tables, fenced code, headings etc. render
    normally. Escaped forms (``\\{term:...}``) emit the literal
    curly-brace form with the leading backslash stripped.
    """
    if not markdown_text or "{term:" not in markdown_text:
        return markdown_text

    def _replace(m: re.Match) -> str:
        term = m.group("term").strip()
        display = (m.group("display") or term).strip()
        # Markdown link: [display](orgchem-glossary:Term%20Name)
        # Single-colon form keeps the term in `QUrl.path()` rather
        # than being normalised into a lower-cased host. `quote`
        # handles spaces / punctuation cleanly.
        return f"[{display}]({SCHEME}:{quote(term, safe='')})"

    out = _MACRO_RX.sub(_replace, markdown_text)
    # Post-pass: un-escape any ``\{term:...}`` literal forms.
    out = _ESCAPED_RX.sub("{term:", out)
    return out
