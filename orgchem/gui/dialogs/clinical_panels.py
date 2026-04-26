"""Phase 37b (round 137) — *Tools → Clinical lab panels…* dialog.

Modeless reference dialog backed by
:mod:`orgchem.core.clinical_panels`.  Layout:

- Top: panel picker combo (BMP / CMP / Lipid / DM follow-up /
  Thyroid).
- Middle: panel meta (purpose, sample, procedure, fasting, notes).
- Bottom: per-analyte table with name + units + normal range.
- Right: detail pane for the currently-selected analyte
  (full clinical-significance + interpretation notes).

Singleton so re-opening preserves the user's panel + analyte
selection.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QComboBox, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSplitter, QTableWidget,
    QTableWidgetItem, QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.clinical_panels import (
    LabAnalyte, LabPanel, get_analyte, get_panel, list_panels,
)

log = logging.getLogger(__name__)


class ClinicalPanelsDialog(QDialog):
    """Reference panel of clinical-chemistry lab panels with
    drill-down to per-analyte detail."""

    _instance: Optional["ClinicalPanelsDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "ClinicalPanelsDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Clinical lab panels")
        self.setModal(False)
        self.resize(1020, 640)
        self._build_ui()
        self._reload_panel()

    # ---- UI construction -------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        # ---- top row: panel picker ---------------------------
        top = QHBoxLayout()
        top.addWidget(QLabel("Panel:"))
        self._panel_combo = QComboBox()
        for p in list_panels():
            self._panel_combo.addItem(
                f"{p.short_name} — {p.name}", p.id)
        self._panel_combo.currentIndexChanged.connect(
            self._reload_panel)
        top.addWidget(self._panel_combo, 1)
        outer.addLayout(top)

        # ---- splitter: left = panel + table; right = analyte
        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        self._panel_meta = QLabel("")
        self._panel_meta.setWordWrap(True)
        self._panel_meta.setTextInteractionFlags(
            Qt.TextSelectableByMouse)
        left_lay.addWidget(self._panel_meta)

        self._table = QTableWidget(0, 4)
        self._table.setHorizontalHeaderLabels(
            ["Analyte", "Abbrev.", "Units", "Normal range"])
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.itemSelectionChanged.connect(self._on_row_selected)
        self._table.setMinimumHeight(220)
        left_lay.addWidget(self._table, 1)

        splitter.addWidget(left)

        # right pane: analyte detail
        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._analyte_title = QLabel("Select an analyte on "
                                     "the left.")
        f = self._analyte_title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 2)
        self._analyte_title.setFont(f)
        self._analyte_title.setWordWrap(True)
        right_lay.addWidget(self._analyte_title)

        self._analyte_meta = QLabel("")
        self._analyte_meta.setWordWrap(True)
        right_lay.addWidget(self._analyte_meta)

        self._analyte_detail = QTextBrowser()
        self._analyte_detail.setOpenExternalLinks(False)
        right_lay.addWidget(self._analyte_detail, 1)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        outer.addWidget(splitter, 1)

        # footer
        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    # ---- panel rendering -------------------------------------

    def _reload_panel(self) -> None:
        pid = self._panel_combo.currentData()
        panel = get_panel(pid) if pid else None
        if panel is None:
            self._show_blank_panel()
            return
        meta_html = (
            f"<p><b>Purpose.</b> {_html_escape(panel.purpose)}</p>"
            f"<p><b>Sample.</b> {_html_escape(panel.sample)}"
            f" &nbsp;·&nbsp; <b>Fasting.</b> "
            f"{_html_escape(panel.fasting)}</p>"
            f"<p><b>Procedure.</b> "
            f"{_html_escape(panel.procedure)}</p>"
        )
        if panel.notes:
            meta_html += (
                f"<p><b>Notes.</b> {_html_escape(panel.notes)}</p>"
            )
        self._panel_meta.setText(meta_html)
        self._populate_table(panel)
        # Auto-focus the first analyte row.
        if self._table.rowCount() > 0:
            self._table.selectRow(0)
        else:
            self._show_blank_analyte()

    def _populate_table(self, panel: LabPanel) -> None:
        self._table.setRowCount(0)
        for a in panel.analytes:
            row = self._table.rowCount()
            self._table.insertRow(row)
            for col, text in enumerate([
                a.name, a.abbreviation, a.units, a.normal_range,
            ]):
                it = QTableWidgetItem(text)
                if col == 0:
                    it.setData(Qt.UserRole, a.id)
                self._table.setItem(row, col, it)
        self._table.resizeColumnsToContents()

    def _show_blank_panel(self) -> None:
        self._panel_meta.setText(
            "Select a panel from the picker above.")
        self._table.setRowCount(0)
        self._show_blank_analyte()

    # ---- analyte rendering -----------------------------------

    def _on_row_selected(self) -> None:
        items = self._table.selectedItems()
        if not items:
            self._show_blank_analyte()
            return
        row = items[0].row()
        analyte_id_item = self._table.item(row, 0)
        if analyte_id_item is None:
            self._show_blank_analyte()
            return
        aid = analyte_id_item.data(Qt.UserRole)
        a = get_analyte(aid)
        if a is None:
            self._show_blank_analyte()
            return
        self._show_analyte(a)

    def _show_analyte(self, a: LabAnalyte) -> None:
        self._analyte_title.setText(f"{a.name} ({a.abbreviation})")
        self._analyte_meta.setText(
            f"<b>Category:</b> {a.category} &nbsp;·&nbsp; "
            f"<b>Units:</b> {a.units} &nbsp;·&nbsp; "
            f"<b>Normal:</b> {a.normal_range}"
        )
        body = (
            f"<h4>Clinical significance</h4>"
            f"<p>{_html_escape(a.clinical_significance)}</p>"
            f"<h4>Notes</h4>"
            f"<p>{_html_escape(a.notes)}</p>"
        )
        self._analyte_detail.setHtml(body)

    def _show_blank_analyte(self) -> None:
        self._analyte_title.setText(
            "Select an analyte on the left.")
        self._analyte_meta.setText("")
        self._analyte_detail.setHtml("")

    # ---- programmatic API ------------------------------------

    def select_panel(self, panel_id: str) -> bool:
        """Switch the panel combo to the matching id.  Returns
        True on success."""
        for i in range(self._panel_combo.count()):
            if self._panel_combo.itemData(i) == panel_id:
                self._panel_combo.setCurrentIndex(i)
                return True
        return False

    def select_analyte(self, analyte_id: str) -> bool:
        """Select the table row for the matching analyte id (the
        panel must already contain it).  Returns True on success."""
        for row in range(self._table.rowCount()):
            it = self._table.item(row, 0)
            if it is not None and it.data(Qt.UserRole) == analyte_id:
                self._table.selectRow(row)
                return True
        return False


def _html_escape(s: str) -> str:
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
