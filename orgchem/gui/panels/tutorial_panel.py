"""Tutorials tab — curriculum tree + markdown lesson viewer."""
from __future__ import annotations

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QTextBrowser,
)

from orgchem.tutorial.curriculum import CURRICULUM
from orgchem.tutorial.loader import load_tutorial_markdown
from orgchem.tutorial.macros import expand_term_macros, SCHEME as GLOSSARY_SCHEME


def _decode_glossary_term(url: QUrl) -> str:
    """Extract the term string from an ``orgchem-glossary:`` URL,
    tolerating both single-colon (``scheme:Term%20Name``) and
    legacy double-slash (``scheme://Term``) forms."""
    from urllib.parse import unquote
    # Strip the scheme + any separator prefix off the full string.
    raw = url.toString()
    prefix = GLOSSARY_SCHEME + ":"
    if raw.startswith(prefix):
        raw = raw[len(prefix):]
    # Peel a `//` (authority marker) if present.
    raw = raw.lstrip("/")
    return unquote(raw)


class TutorialPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QHBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Curriculum")
        self.tree.setMaximumWidth(320)
        self.tree.itemClicked.connect(self._on_click)
        lay.addWidget(self.tree)

        self.browser = QTextBrowser()
        # External http(s) links still open in the user's browser,
        # but we route the internal `orgchem-glossary://` scheme
        # through `anchorClicked` → Glossary tab.
        self.browser.setOpenExternalLinks(True)
        self.browser.setOpenLinks(False)
        self.browser.anchorClicked.connect(self._on_anchor)
        lay.addWidget(self.browser, 1)

        self._populate()

    def _populate(self) -> None:
        for level, lessons in CURRICULUM.items():
            parent = QTreeWidgetItem([level.title()])
            for lesson in lessons:
                child = QTreeWidgetItem([lesson["title"]])
                child.setData(0, Qt.UserRole, lesson)
                parent.addChild(child)
            self.tree.addTopLevelItem(parent)
        self.tree.expandAll()

    def _on_click(self, item, _col) -> None:
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        md = load_tutorial_markdown(data["path"])
        # Phase 11c follow-up — expand `{term:X}` macros before
        # handing the text to the markdown renderer, so term
        # cross-references become clickable links to the Glossary.
        md = expand_term_macros(md)
        try:
            import markdown as md_mod
            html = md_mod.markdown(md, extensions=["fenced_code", "tables"])
        except ImportError:
            html = "<pre>" + md + "</pre>"
        self.browser.setHtml(html)

    def _on_anchor(self, url: QUrl) -> None:
        """Route `orgchem-glossary:<term>` clicks to the Glossary
        tab. Any other scheme opens externally via Qt's default
        handler (QDesktopServices)."""
        if url.scheme() != GLOSSARY_SCHEME:
            from PySide6.QtGui import QDesktopServices
            QDesktopServices.openUrl(url)
            return
        term = _decode_glossary_term(url)
        from orgchem.agent.controller import main_window
        win = main_window()
        if win is None or not hasattr(win, "glossary"):
            return
        tabs = getattr(win, "tabs", None)
        if tabs is not None:
            for i in range(tabs.count()):
                if tabs.tabText(i) == "Glossary":
                    tabs.setCurrentIndex(i)
                    break
        win.glossary.focus_term(term)
