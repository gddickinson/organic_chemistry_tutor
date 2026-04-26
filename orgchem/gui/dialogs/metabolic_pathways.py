"""Phase 42a (round 147) — *Tools → Metabolic pathways…*
dialog.

Singleton modeless dialog backed by
:mod:`orgchem.core.metabolic_pathways`.  Layout:

- Top: category combo + free-text filter + pathway list.
- Middle: pathway meta block (compartment / overview /
  textbook reference / overall ΔG).
- Bottom: per-step `QTableWidget` (step / enzyme / EC /
  reversibility / ΔG) + step detail panel showing
  substrates / products / regulatory effectors / notes
  for the currently-selected step.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QComboBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSplitter, QTableWidget, QTableWidgetItem,
    QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.metabolic_pathways import (
    Pathway, PathwayStep, categories, get_pathway,
    list_pathways,
)

log = logging.getLogger(__name__)


_ALL_CATEGORIES_LABEL = "(all categories)"


class MetabolicPathwaysDialog(QDialog):
    """Reference panel of major metabolic pathways with
    drill-down to per-step detail."""

    _instance: Optional["MetabolicPathwaysDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "MetabolicPathwaysDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Metabolic pathways")
        self.setModal(False)
        self.resize(1200, 760)
        self._build_ui()
        self._reload_list()

    # ---- UI construction -------------------------------------

    def _build_ui(self) -> None:
        outer = QHBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        splitter = QSplitter(Qt.Horizontal)

        # ---- left pane: filter + pathway list ----------------
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
            "Filter pathways (e.g. 'glycolysis', 'urea')")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)
        self._pathway_list = QListWidget()
        self._pathway_list.currentItemChanged.connect(
            self._on_pathway_selection)
        self._pathway_list.setMinimumWidth(260)
        left_lay.addWidget(self._pathway_list, 1)
        splitter.addWidget(left)

        # ---- middle pane: meta + step table ------------------
        middle = QWidget()
        mid_lay = QVBoxLayout(middle)
        mid_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select a pathway on the left.")
        f = self._title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 2)
        self._title.setFont(f)
        self._title.setWordWrap(True)
        mid_lay.addWidget(self._title)
        self._meta = QLabel("")
        self._meta.setWordWrap(True)
        self._meta.setTextInteractionFlags(
            Qt.TextSelectableByMouse)
        mid_lay.addWidget(self._meta)
        self._step_table = QTableWidget(0, 5)
        self._step_table.setHorizontalHeaderLabels(
            ["#", "Enzyme", "EC", "Rev?", "ΔG (kJ/mol)"])
        self._step_table.horizontalHeader().setStretchLastSection(False)
        self._step_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self._step_table.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        self._step_table.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self._step_table.itemSelectionChanged.connect(
            self._on_step_selected)
        self._step_table.setMinimumHeight(220)
        mid_lay.addWidget(self._step_table, 1)
        splitter.addWidget(middle)

        # ---- right pane: step detail -------------------------
        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._step_title = QLabel("Select a step on the left.")
        f = self._step_title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 1)
        self._step_title.setFont(f)
        self._step_title.setWordWrap(True)
        right_lay.addWidget(self._step_title)
        self._step_detail = QTextBrowser()
        self._step_detail.setOpenExternalLinks(False)
        right_lay.addWidget(self._step_detail, 1)
        splitter.addWidget(right)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)
        outer.addWidget(splitter, 1)

    # ---- list management -------------------------------------

    def _reload_list(self) -> None:
        cat = self._cat_combo.currentText()
        if cat == _ALL_CATEGORIES_LABEL:
            pathways = list_pathways()
        else:
            pathways = list_pathways(category=cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            pathways = [
                p for p in pathways
                if needle in p.id.lower()
                or needle in p.name.lower()
                or needle in p.overview.lower()
            ]
        self._pathway_list.clear()
        for p in pathways:
            it = QListWidgetItem(p.name)
            it.setData(Qt.UserRole, p.id)
            self._pathway_list.addItem(it)
        if self._pathway_list.count():
            self._pathway_list.setCurrentRow(0)
        else:
            self._show_blank("No pathways match the filter.")

    def _on_pathway_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a pathway on the left.")
            return
        pid = current.data(Qt.UserRole)
        p = get_pathway(pid)
        if p is None:
            self._show_blank(f"Unknown pathway: {pid}")
            return
        self._show_pathway(p)

    # ---- pathway rendering -----------------------------------

    def _show_pathway(self, p: Pathway) -> None:
        self._title.setText(p.name)
        meta_html = (
            f"<p><b>Category:</b> {_esc(p.category)} "
            f"&nbsp;·&nbsp; <b>Compartment:</b> "
            f"{_esc(p.cellular_compartment)} "
            f"&nbsp;·&nbsp; <b>Steps:</b> {len(p.steps)}</p>"
            f"<p>{_esc(p.overview)}</p>"
        )
        if p.overall_delta_g_kjmol is not None:
            meta_html += (
                f"<p><b>Overall ΔG:</b> "
                f"{p.overall_delta_g_kjmol:+.1f} kJ/mol "
                f"&nbsp;·&nbsp; <b>Reference:</b> "
                f"{_esc(p.textbook_reference)}</p>")
        else:
            meta_html += (
                f"<p><b>Reference:</b> "
                f"{_esc(p.textbook_reference)}</p>")
        self._meta.setText(meta_html)
        self._populate_steps(p)
        if self._step_table.rowCount() > 0:
            self._step_table.selectRow(0)
        else:
            self._show_blank_step()

    def _populate_steps(self, p: Pathway) -> None:
        self._step_table.setRowCount(0)
        for s in p.steps:
            row = self._step_table.rowCount()
            self._step_table.insertRow(row)
            cells = [
                str(s.step_number),
                s.enzyme_name,
                s.ec_number,
                "↔" if s.reversibility == "reversible" else "→",
                (f"{s.delta_g_kjmol:+.1f}"
                 if s.delta_g_kjmol is not None else "—"),
            ]
            for col, text in enumerate(cells):
                it = QTableWidgetItem(text)
                if col == 0:
                    it.setData(Qt.UserRole, s.step_number)
                self._step_table.setItem(row, col, it)
        self._step_table.resizeColumnsToContents()

    def _on_step_selected(self) -> None:
        items = self._step_table.selectedItems()
        if not items:
            self._show_blank_step()
            return
        row = items[0].row()
        step_no_item = self._step_table.item(row, 0)
        if step_no_item is None:
            self._show_blank_step()
            return
        step_number = step_no_item.data(Qt.UserRole)
        # Resolve the current pathway + step.
        pid = self._pathway_list.currentItem().data(Qt.UserRole)
        p = get_pathway(pid)
        if p is None:
            return
        for s in p.steps:
            if s.step_number == step_number:
                self._show_step(s)
                return

    def _show_step(self, s: PathwayStep) -> None:
        rev = ("reversible (↔)" if s.reversibility == "reversible"
               else "irreversible (→)")
        self._step_title.setText(
            f"Step {s.step_number}: {s.enzyme_name}")
        body = (
            f"<p><b>EC number:</b> {_esc(s.ec_number)} "
            f"&nbsp;·&nbsp; <b>Reversibility:</b> "
            f"{rev}</p>"
        )
        if s.delta_g_kjmol is not None:
            body += (
                f"<p><b>ΔG:</b> {s.delta_g_kjmol:+.1f} kJ/mol</p>")
        body += (
            f"<h4>Substrates</h4><p>"
            + ", ".join(_esc(x) for x in s.substrates)
            + "</p>"
            f"<h4>Products</h4><p>"
            + ", ".join(_esc(x) for x in s.products)
            + "</p>"
        )
        if s.regulatory_effectors:
            eff_html = "<ul>"
            for r in s.regulatory_effectors:
                eff_html += (
                    f"<li><b>{_esc(r.name)}</b> "
                    f"({_esc(r.mode)}) — "
                    f"{_esc(r.mechanism)}</li>")
            eff_html += "</ul>"
            body += (
                f"<h4>Regulatory effectors</h4>{eff_html}")
        if s.notes:
            body += f"<h4>Notes</h4><p>{_esc(s.notes)}</p>"
        self._step_detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._step_table.setRowCount(0)
        self._show_blank_step()

    def _show_blank_step(self) -> None:
        self._step_title.setText("Select a step on the left.")
        self._step_detail.setHtml("")

    # ---- programmatic API ------------------------------------

    def select_pathway(self, pathway_id: str) -> bool:
        for i in range(self._pathway_list.count()):
            it = self._pathway_list.item(i)
            if it.data(Qt.UserRole) == pathway_id:
                self._pathway_list.setCurrentRow(i)
                return True
        return False

    def select_step(self, step_number: int) -> bool:
        for row in range(self._step_table.rowCount()):
            it = self._step_table.item(row, 0)
            if it is not None \
                    and it.data(Qt.UserRole) == step_number:
                self._step_table.selectRow(row)
                return True
        return False


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
