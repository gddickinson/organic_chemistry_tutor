"""Tests for the Phase 11c `{term:X}` tutorial macro (round 52)."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---------- pure-text macro expansion ------------------------------

def test_expand_term_macros_basic():
    from orgchem.tutorial.macros import expand_term_macros
    src = "An SN2 starts from {term:SN2} geometry."
    out = expand_term_macros(src)
    assert "[SN2](orgchem-glossary:SN2)" in out
    # Leading prose untouched
    assert "An SN2 starts from" in out


def test_expand_term_macros_with_display_override():
    from orgchem.tutorial.macros import expand_term_macros
    src = ("Avoid eclipsing — prefer {term:Anti-periplanar"
           "|anti-periplanar} alignment.")
    out = expand_term_macros(src)
    # Display text uses the piped alt form, link target is the term.
    assert "[anti-periplanar](orgchem-glossary:" in out
    assert "Anti-periplanar" in out   # in the URL portion


def test_expand_term_macros_escaped_literal():
    from orgchem.tutorial.macros import expand_term_macros
    src = r"Type \{term:SN2} to insert a glossary link."
    out = expand_term_macros(src)
    # Escape consumed; literal curly form shown.
    assert out == "Type {term:SN2} to insert a glossary link."


def test_expand_term_macros_preserves_code_blocks():
    """Macros inside fenced code are still expanded (markdown
    rendering will show them literally because the link syntax
    survives code-fence escaping — but the macro itself shouldn't
    be silently dropped)."""
    from orgchem.tutorial.macros import expand_term_macros
    src = "text\n```\n{term:SN2}\n```\n"
    out = expand_term_macros(src)
    # We don't try to parse markdown — the regex just expands in
    # place. It's OK because downstream the markdown renderer sees
    # a valid link target in either context.
    assert "orgchem-glossary:SN2" in out


def test_expand_term_macros_percent_encodes_spaces():
    from orgchem.tutorial.macros import expand_term_macros
    src = "Invoke {term:Hammond postulate} early."
    out = expand_term_macros(src)
    # Spaces in term id get percent-encoded in the URL.
    assert "orgchem-glossary:Hammond%20postulate" in out
    # Display remains the raw phrase.
    assert "[Hammond postulate]" in out


def test_expand_term_macros_idempotent_on_empty():
    from orgchem.tutorial.macros import expand_term_macros
    assert expand_term_macros("") == ""
    assert expand_term_macros("no macros here") == "no macros here"


# ---------- end-to-end through the tutorial panel ------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_tutorial_panel_renders_macro_as_anchor(app, tmp_path):
    """Point the panel at a temp lesson that uses the macro and
    confirm the rendered HTML contains a live anchor."""
    panel = app.window.tutorial_panel
    lesson_path = tmp_path / "macro_demo.md"
    lesson_path.write_text(
        "# Macro demo\n\nSee {term:SN2|SN2 reaction} for context.\n"
    )
    from PySide6.QtWidgets import QTreeWidgetItem
    from PySide6.QtCore import Qt
    item = QTreeWidgetItem(["macro_demo"])
    item.setData(0, Qt.UserRole, {"title": "macro_demo",
                                  "path": str(lesson_path)})
    panel._on_click(item, 0)
    html = panel.browser.toHtml()
    assert "orgchem-glossary:SN2" in html
    # Display label shows up as-is.
    assert "SN2 reaction" in html


def test_tutorial_panel_anchor_routes_to_glossary(app, tmp_path):
    """Clicking an `orgchem-glossary:SN2` anchor should switch
    the main-window tab to Glossary and focus the term."""
    from PySide6.QtCore import QUrl
    panel = app.window.tutorial_panel
    # Force the glossary panel to a different state first.
    win = app.window
    # Pick a non-Glossary starting tab.
    for i in range(win.tabs.count()):
        if win.tabs.tabText(i) != "Glossary":
            win.tabs.setCurrentIndex(i)
            break
    panel._on_anchor(QUrl("orgchem-glossary:SN2"))
    active = win.tabs.tabText(win.tabs.currentIndex())
    assert active == "Glossary", active
