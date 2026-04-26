"""Phase 45 (round 149) — *Tools → Lab reagents…* dialog.

Singleton modeless reference dialog backed by
:mod:`orgchem.core.lab_reagents`.  Same shape as the Phase-40a
*Lab analysers* dialog: category combo + free-text filter on
the left, list of `name — category` rows, HTML detail card on
the right with the 8 standard sections (Typical concentration
/ Storage / Hazards / Preparation / CAS / Usage / Notes).
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

from orgchem.core.lab_reagents import (
    LabReagent, categories, get_reagent, list_reagents,
)

log = logging.getLogger(__name__)


_ALL_CATEGORIES_LABEL = "(all categories)"


class LabReagentsDialog(QDialog):
    """Reference panel of off-the-shelf lab reagents."""

    _instance: Optional["LabReagentsDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "LabReagentsDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Lab reagents")
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
        self._cat_combo.currentIndexChanged.connect(
            self._reload_list)
        cat_row.addWidget(self._cat_combo, 1)
        left_lay.addLayout(cat_row)
        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter by name / id / CAS / usage "
            "(e.g. 'Tris', 'DMSO', 'detergent')")
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
        self._title = QLabel("Select a reagent on the left.")
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
            entries = list_reagents()
        else:
            entries = list_reagents(category=cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            entries = [
                r for r in entries
                if needle in r.id.lower()
                or needle in r.name.lower()
                or needle in r.category.lower()
                or needle in r.typical_usage.lower()
                or needle in r.cas_number.lower()
            ]
        self._list.clear()
        for r in entries:
            it = QListWidgetItem(f"{r.name}  —  {r.category}")
            it.setData(Qt.UserRole, r.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank(
                "No reagents match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a reagent on the left.")
            return
        rid = current.data(Qt.UserRole)
        r = get_reagent(rid)
        if r is None:
            self._show_blank(f"Unknown reagent id: {rid}")
            return
        self._show_reagent(r)

    def _show_reagent(self, r: LabReagent) -> None:
        self._title.setText(r.name)
        self._meta.setText(
            f"<b>Category:</b> {_esc(r.category)} "
            f"&nbsp;·&nbsp; <b>CAS:</b> "
            f"{_esc(r.cas_number)}")
        body = (
            f"<h4>Typical concentration</h4>"
            f"<p>{_esc(r.typical_concentration)}</p>"
            f"<h4>Storage</h4>"
            f"<p>{_esc(r.storage)}</p>"
            f"<h4>Hazards</h4>"
            f"<p>{_esc(r.hazards)}</p>"
            f"<h4>Preparation notes</h4>"
            f"<p>{_esc(r.preparation_notes)}</p>"
            f"<h4>Typical usage</h4>"
            f"<p>{_esc(r.typical_usage)}</p>"
        )
        if r.notes:
            body += f"<h4>Notes</h4><p>{_esc(r.notes)}</p>"
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    def select_reagent(self, reagent_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == reagent_id:
                self._list.setCurrentRow(i)
                return True
        return False


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
