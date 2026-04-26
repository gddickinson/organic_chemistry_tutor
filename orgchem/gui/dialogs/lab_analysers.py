"""Phase 40a (round 146) — *Tools → Lab analysers…* dialog.

Singleton modeless reference dialog backed by
:mod:`orgchem.core.lab_analysers`.  Same shape as the
Phase-37c chromatography dialog: category combo + free-text
filter on the left, list of `name — manufacturer` rows,
HTML detail card on the right with the standard 9 sections
(Function / Throughput / Sample / Detection / Assays /
Strengths / Limitations / Notes).
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSplitter,
    QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.lab_analysers import (
    LabAnalyser, categories, get_analyser, list_analysers,
)

log = logging.getLogger(__name__)


_ALL_CATEGORIES_LABEL = "(all categories)"


class LabAnalysersDialog(QDialog):
    """Reference panel of major lab analysers + automation
    instruments."""

    _instance: Optional["LabAnalysersDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "LabAnalysersDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Lab analysers")
        self.setModal(False)
        self.resize(1080, 660)
        self._build_ui()
        self._reload_list()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        self._cat_combo = QComboBox()
        self._cat_combo.addItem(_ALL_CATEGORIES_LABEL)
        for c in categories():
            self._cat_combo.addItem(c)
        self._cat_combo.currentIndexChanged.connect(self._reload_list)
        cat_row.addWidget(self._cat_combo, 1)
        left_lay.addLayout(cat_row)
        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter by name / manufacturer (e.g. 'Roche', "
            "'NovaSeq', 'GeneXpert')")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)
        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(280)
        left_lay.addWidget(self._list, 1)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select an analyser on the left.")
        f = self._title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 2)
        self._title.setFont(f)
        self._title.setWordWrap(True)
        right_lay.addWidget(self._title)
        self._meta = QLabel("")
        self._meta.setWordWrap(True)
        right_lay.addWidget(self._meta)
        self._detail = QTextBrowser()
        self._detail.setOpenExternalLinks(False)
        right_lay.addWidget(self._detail, 1)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter, 1)

        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    def _reload_list(self) -> None:
        cat = self._cat_combo.currentText()
        if cat == _ALL_CATEGORIES_LABEL:
            entries = list_analysers()
        else:
            entries = list_analysers(category=cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            entries = [
                a for a in entries
                if needle in a.id.lower()
                or needle in a.name.lower()
                or needle in a.manufacturer.lower()
                or needle in a.category.lower()
            ]
        self._list.clear()
        for a in entries:
            it = QListWidgetItem(
                f"{a.name}  —  {a.manufacturer}")
            it.setData(Qt.UserRole, a.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank("No analysers match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select an analyser on the left.")
            return
        aid = current.data(Qt.UserRole)
        a = get_analyser(aid)
        if a is None:
            self._show_blank(f"Unknown analyser id: {aid}")
            return
        self._show_analyser(a)

    def _show_analyser(self, a: LabAnalyser) -> None:
        self._title.setText(f"{a.name}")
        self._meta.setText(
            f"<b>Manufacturer:</b> {_esc(a.manufacturer)} "
            f"&nbsp;·&nbsp; <b>Category:</b> {_esc(a.category)}")
        body = (
            f"<h4>Function</h4>"
            f"<p>{_esc(a.function)}</p>"
            f"<h4>Typical throughput</h4>"
            f"<p>{_esc(a.typical_throughput)}</p>"
            f"<h4>Sample</h4>"
            f"<p>{_esc(a.sample_volume)}</p>"
            f"<h4>Detection method</h4>"
            f"<p>{_esc(a.detection_method)}</p>"
            f"<h4>Typical assays</h4>"
            f"<p>{_esc(a.typical_assays)}</p>"
            f"<h4>Strengths</h4>"
            f"<p>{_esc(a.strengths)}</p>"
            f"<h4>Limitations</h4>"
            f"<p>{_esc(a.limitations)}</p>"
        )
        if a.notes:
            body += f"<h4>Notes</h4><p>{_esc(a.notes)}</p>"
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    def select_analyser(self, analyser_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == analyser_id:
                self._list.setCurrentRow(i)
                return True
        return False


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
