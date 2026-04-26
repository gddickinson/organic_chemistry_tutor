"""Phase 38a (round 140) — *Tools → Lab equipment…* dialog.

Modeless reference dialog backed by
:mod:`orgchem.core.lab_equipment`.  Same shape as the Phase
37c/d reference dialogs (category combo + filter + list +
HTML detail card), with one extra section in the detail
view: a list of the item's `connection_ports` so users can
preview the joints / hose connections the future Phase-38c
canvas will use to snap items together.

Singleton so re-opening preserves the user's filter +
selection.
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

from orgchem.core.lab_equipment import (
    Equipment, categories, get_equipment, list_equipment,
)

log = logging.getLogger(__name__)


_ALL_CATEGORIES_LABEL = "(all categories)"


class LabEquipmentDialog(QDialog):
    """Reference panel of lab equipment with category +
    free-text filtering and an HTML detail card."""

    _instance: Optional["LabEquipmentDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "LabEquipmentDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Lab equipment")
        self.setModal(False)
        self.resize(1080, 660)
        self._build_ui()
        self._reload_list()

    # ---- UI construction -------------------------------------

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
            "Filter by name / category (e.g. 'condenser', "
            "'flask', 'vacuum')")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)

        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(260)
        left_lay.addWidget(self._list, 1)

        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select an item on the left.")
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

        # Footer.
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
            items = list_equipment()
        else:
            items = list_equipment(category=cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            items = [
                e for e in items
                if needle in e.name.lower()
                or needle in e.category.lower()
                or needle in e.id.lower()
            ]
        self._list.clear()
        for e in items:
            it = QListWidgetItem(f"{e.name}  —  {e.category}")
            it.setData(Qt.UserRole, e.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank("No equipment matches the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select an item on the left.")
            return
        eid = current.data(Qt.UserRole)
        e = get_equipment(eid)
        if e is None:
            self._show_blank(f"Unknown equipment id: {eid}")
            return
        self._show_equipment(e)

    # ---- detail rendering ------------------------------------

    def _show_equipment(self, e: Equipment) -> None:
        self._title.setText(e.name)
        self._meta.setText(f"<b>Category:</b> {e.category}")
        body = (
            f"<h4>Description</h4>"
            f"<p>{_html_escape(e.description)}</p>"
            f"<h4>Typical uses</h4>"
            f"<p>{_html_escape(e.typical_uses)}</p>"
        )
        if e.variants:
            body += (
                f"<h4>Variants</h4>"
                f"<p>{_html_escape(e.variants)}</p>"
            )
        if e.safety_notes:
            body += (
                f"<h4>Safety notes</h4>"
                f"<p>{_html_escape(e.safety_notes)}</p>"
            )
        if e.connection_ports:
            ports_html = "<ul>"
            for p in e.connection_ports:
                role = "male" if p.is_male else "female"
                ports_html += (
                    f"<li><b>{_html_escape(p.name)}</b> "
                    f"({_html_escape(p.location)}) — "
                    f"{_html_escape(p.joint_type)} ({role})</li>"
                )
            ports_html += "</ul>"
            body += (
                f"<h4>Connection ports</h4>"
                f"<p><i>The future Phase-38c canvas will use "
                f"these named joints to snap items together.</i></p>"
                f"{ports_html}"
            )
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    # ---- programmatic API ------------------------------------

    def select_equipment(self, equipment_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == equipment_id:
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
