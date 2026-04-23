"""Tutorials tab — curriculum tree + markdown lesson viewer."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QTextBrowser,
)

from orgchem.tutorial.curriculum import CURRICULUM
from orgchem.tutorial.loader import load_tutorial_markdown


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
        self.browser.setOpenExternalLinks(True)
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
        try:
            import markdown as md_mod
            html = md_mod.markdown(md, extensions=["fenced_code", "tables"])
        except ImportError:
            html = "<pre>" + md + "</pre>"
        self.browser.setHtml(html)
