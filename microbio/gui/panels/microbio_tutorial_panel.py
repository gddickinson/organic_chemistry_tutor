"""Phase MB-1.0 (round 215) — Microbio Studio tutorial panel."""
from __future__ import annotations
import logging
from typing import Any, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel, QSplitter, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget,
)

from microbio.tutorial.curriculum import CURRICULUM
from microbio.tutorial.loader import load_lesson

log = logging.getLogger(__name__)


class MicrobioTutorialPanel(QWidget):
    """Tree of microbio lessons + markdown reader."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._populate()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        outer.addWidget(QLabel(
            "<b>Microbiology Studio — tutorials.</b>  "
            "Phase MB-1.0 ships one starter lesson; the full "
            "Microbio curriculum is planned for Phase MB-4."))

        split = QSplitter(Qt.Horizontal)
        outer.addWidget(split, stretch=1)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Lesson"])
        self.tree.itemSelectionChanged.connect(self._on_select)
        split.addWidget(self.tree)

        self.viewer = QTextBrowser()
        self.viewer.setOpenExternalLinks(True)
        split.addWidget(self.viewer)
        split.setStretchFactor(0, 1)
        split.setStretchFactor(1, 3)

    def _populate(self) -> None:
        self.tree.clear()
        first_item: Optional[QTreeWidgetItem] = None
        for level, lessons in CURRICULUM.items():
            top = QTreeWidgetItem(self.tree, [level.title()])
            top.setExpanded(True)
            for lesson in lessons:
                child = QTreeWidgetItem(top, [lesson["title"]])
                child.setData(0, Qt.UserRole, lesson)
                if first_item is None:
                    first_item = child
        if first_item is not None:
            self.tree.setCurrentItem(first_item)

    def _on_select(self) -> None:
        items = self.tree.selectedItems()
        if not items:
            return
        data: Optional[Dict[str, Any]] = items[0].data(
            0, Qt.UserRole)
        if not data:
            self.viewer.clear()
            return
        try:
            md = load_lesson(data["path"])
        except Exception as e:  # noqa: BLE001
            self.viewer.setHtml(f"<pre>Error loading: {e}</pre>")
            return
        self.viewer.setMarkdown(md)
