"""Phase 37c (round 138) — *Tools → Chromatography techniques…* dialog.

Modeless reference dialog backed by
:mod:`orgchem.core.chromatography_methods`.  Layout mirrors the
Phase-37a qualitative-tests dialog: left = category combo + filter
+ method list; right = full detail pane covering principle,
phases, detectors, strengths, limitations, procedure, and notes.

Each method is a substantial reference card (200-400 words each),
so the right pane uses a `QTextBrowser` with rendered HTML
sections rather than a colour swatch.
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

from orgchem.core.chromatography_methods import (
    ChromatographyMethod, categories, get_method, list_methods,
)

log = logging.getLogger(__name__)


_ALL_CATEGORIES_LABEL = "(all categories)"


class ChromatographyMethodsDialog(QDialog):
    """Reference panel of chromatography-method entries with
    category + free-text filtering and an HTML detail card."""

    _instance: Optional["ChromatographyMethodsDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "ChromatographyMethodsDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Chromatography techniques")
        self.setModal(False)
        self.resize(1080, 660)
        self._build_ui()
        self._reload_list()

    # ---- UI construction -------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        splitter = QSplitter(Qt.Horizontal)

        # ---- left pane: filters + list -----------------------
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
            "Filter by name / abbreviation (e.g. 'HPLC', 'gas', "
            "'protein')")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)

        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(260)
        left_lay.addWidget(self._list, 1)

        splitter.addWidget(left)

        # ---- right pane: detail card -------------------------
        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select a method on the left.")
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

        # Footer
        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    # ---- list management -------------------------------------

    def _reload_list(self) -> None:
        cat = self._cat_combo.currentText()
        if cat == _ALL_CATEGORIES_LABEL:
            methods = list_methods()
        else:
            methods = list_methods(category=cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            methods = [
                m for m in methods
                if needle in m.name.lower()
                or needle in m.abbreviation.lower()
                or needle in m.category.lower()
                or needle in m.id.lower()
            ]
        self._list.clear()
        for m in methods:
            it = QListWidgetItem(
                f"{m.abbreviation}  —  {m.name}")
            it.setData(Qt.UserRole, m.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank("No methods match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a method on the left.")
            return
        mid = current.data(Qt.UserRole)
        m = get_method(mid)
        if m is None:
            self._show_blank(f"Unknown method id: {mid}")
            return
        self._show_method(m)

    # ---- detail rendering ------------------------------------

    def _show_method(self, m: ChromatographyMethod) -> None:
        self._title.setText(f"{m.name} ({m.abbreviation})")
        self._meta.setText(
            f"<b>Category:</b> {m.category}")
        body = (
            f"<h4>Principle</h4><p>{_html_escape(m.principle)}</p>"
            f"<h4>Stationary phase</h4>"
            f"<p>{_html_escape(m.stationary_phase)}</p>"
            f"<h4>Mobile phase</h4>"
            f"<p>{_html_escape(m.mobile_phase)}</p>"
            f"<h4>Detector(s)</h4>"
            f"<p>{_html_escape(m.detectors)}</p>"
            f"<h4>Typical analytes</h4>"
            f"<p>{_html_escape(m.typical_analytes)}</p>"
            f"<h4>Strengths</h4>"
            f"<p>{_html_escape(m.strengths)}</p>"
            f"<h4>Limitations</h4>"
            f"<p>{_html_escape(m.limitations)}</p>"
            f"<h4>Procedure</h4>"
            f"<p>{_html_escape(m.procedure)}</p>"
        )
        if m.notes:
            body += (
                f"<h4>Notes</h4>"
                f"<p>{_html_escape(m.notes)}</p>"
            )
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    # ---- programmatic API ------------------------------------

    def select_method(self, method_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == method_id:
                self._list.setCurrentRow(i)
                return True
        return False


def _html_escape(s: str) -> str:
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
