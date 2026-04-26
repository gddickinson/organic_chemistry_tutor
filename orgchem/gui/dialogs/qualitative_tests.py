"""Phase 37a (round 136) — *Tools → Qualitative inorganic tests…* dialog.

Modeless reference dialog backed by
:mod:`orgchem.core.qualitative_tests`.  Layout:

- Left: category combo + free-text filter + scrollable test list.
- Right: detail pane with name + target + procedure +
  positive-observation block + a colour swatch matching the
  observed flame / precipitate / gas colour.

The dialog is purely educational — no chemistry runs here, the
data is the content.  Singleton so re-opening preserves the
user's filter / selection.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QComboBox, QDialog, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.qualitative_tests import (
    InorganicTest, categories, get_test, list_tests,
)

log = logging.getLogger(__name__)


_ALL_CATEGORIES_LABEL = "(all categories)"


class QualitativeTestsDialog(QDialog):
    """Reference panel of inorganic-test entries with category
    + free-text filtering and a colour swatch per result."""

    _instance: Optional["QualitativeTestsDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "QualitativeTestsDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Qualitative inorganic tests")
        self.setModal(False)
        self.resize(900, 580)
        self._build_ui()
        self._reload_list()

    # ---- UI construction -------------------------------------

    def _build_ui(self) -> None:
        outer = QHBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        # ---- left pane: filters + list -----------------------
        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        self._cat_combo = QComboBox()
        self._cat_combo.addItem(_ALL_CATEGORIES_LABEL)
        for c in categories():
            self._cat_combo.addItem(c)
        self._cat_combo.currentIndexChanged.connect(self._reload_list)
        cat_row.addWidget(self._cat_combo, 1)
        left.addLayout(cat_row)

        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter by name / target ion (e.g. 'Cu', 'Cl⁻', "
            "'flame', 'NH4')")
        self._filter_edit.textChanged.connect(self._reload_list)
        left.addWidget(self._filter_edit)

        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(280)
        left.addWidget(self._list, 1)

        outer.addLayout(left, 0)

        # ---- right pane: detail + swatch ---------------------
        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select a test on the left.")
        f = self._title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 2)
        self._title.setFont(f)
        self._title.setWordWrap(True)
        right.addWidget(self._title)

        self._meta = QLabel("")
        self._meta.setWordWrap(True)
        right.addWidget(self._meta)

        # Colour swatch: a small framed widget tinted with the
        # entry's `colour_hex`.
        swatch_row = QHBoxLayout()
        swatch_row.addWidget(QLabel("Observation colour:"))
        self._swatch = QLabel()
        self._swatch.setMinimumSize(120, 28)
        self._swatch.setMaximumHeight(28)
        self._swatch.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Fixed)
        self._swatch.setAutoFillBackground(True)
        self._swatch.setStyleSheet(
            "border: 1px solid #888; border-radius: 3px;")
        self._set_swatch_colour("#FFFFFF")
        swatch_row.addWidget(self._swatch, 1)
        right.addLayout(swatch_row)

        self._detail = QTextBrowser()
        self._detail.setOpenExternalLinks(False)
        right.addWidget(self._detail, 1)

        # Footer.
        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        right.addLayout(footer)

        outer.addLayout(right, 1)

    # ---- list management -------------------------------------

    def _reload_list(self) -> None:
        cat = self._cat_combo.currentText()
        if cat == _ALL_CATEGORIES_LABEL:
            tests = list_tests()
        else:
            tests = list_tests(category=cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            tests = [
                t for t in tests
                if needle in t.name.lower()
                or needle in t.target.lower()
                or needle in t.category.lower()
            ]
        self._list.clear()
        for t in tests:
            it = QListWidgetItem(f"{t.target}  —  {t.name}")
            it.setData(Qt.UserRole, t.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank("No tests match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a test on the left.")
            return
        tid = current.data(Qt.UserRole)
        test = get_test(tid)
        if test is None:
            self._show_blank(f"Unknown test id: {tid}")
            return
        self._show_test(test)

    # ---- detail rendering ------------------------------------

    def _show_test(self, t: InorganicTest) -> None:
        self._title.setText(t.name)
        meta_bits = [
            f"<b>Target:</b> {t.target} ({t.target_class})",
            f"<b>Category:</b> {t.category}",
        ]
        self._meta.setText(" &nbsp; · &nbsp; ".join(meta_bits))
        self._set_swatch_colour(t.colour_hex)
        body = (
            f"<h4>Reagents</h4><p>{_html_escape(t.reagents)}</p>"
            f"<h4>Procedure</h4><p>{_html_escape(t.procedure)}</p>"
            f"<h4>Positive observation</h4>"
            f"<p>{_html_escape(t.positive_observation)}</p>"
            f"<h4>Notes</h4><p>{_html_escape(t.notes)}</p>"
        )
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._set_swatch_colour("#FFFFFF")
        self._detail.setHtml("")

    def _set_swatch_colour(self, hex_str: str) -> None:
        col = QColor(hex_str)
        if not col.isValid():
            col = QColor("#FFFFFF")
        pal = QPalette()
        pal.setColor(QPalette.Window, col)
        self._swatch.setPalette(pal)
        # Keep the dynamic colour AND the static border via
        # an inline style — palette alone won't paint over the
        # widget's stylesheet on every Qt platform.
        self._swatch.setStyleSheet(
            f"background-color: {col.name()}; "
            "border: 1px solid #888; border-radius: 3px;")

    # ---- programmatic API ------------------------------------

    def select_test(self, test_id: str) -> bool:
        """Select the row matching *test_id* (used by the agent
        action's *open and focus* path).  Returns True if a row
        was found."""
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == test_id:
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
