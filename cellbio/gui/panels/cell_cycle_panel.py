"""Phase CB-2.0 (round 218) — Cell-cycle panel for Cell Bio
Studio.

Category combo + free-text filter + list + HTML detail card
with summary / function / activator-inhibitor lists / disease
associations / cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from cellbio.core.cell_cycle import (
    CATEGORIES, CellCycleEntry,
    find_cell_cycle_entries, get_cell_cycle_entry,
    list_cell_cycle_entries,
)

log = logging.getLogger(__name__)


class CellCyclePanel(QWidget):
    """List + detail view for the CB-2.0 cell-cycle catalogue."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._refresh_list()
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        bar = QHBoxLayout()
        bar.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItem("(all)", "")
        for c in CATEGORIES:
            self.category_combo.addItem(c, c)
        self.category_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.category_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / function / disease / drug)…")
        self.filter_edit.textChanged.connect(self._refresh_list)
        bar.addWidget(self.filter_edit, stretch=1)
        outer.addLayout(bar)

        split = QSplitter(Qt.Horizontal)
        outer.addWidget(split, stretch=1)

        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(
            self._on_select)
        split.addWidget(self.list_widget)

        self.detail = QTextBrowser()
        split.addWidget(self.detail)
        split.setStretchFactor(0, 1)
        split.setStretchFactor(1, 2)

    def _refresh_list(self) -> None:
        c = self.category_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_cell_cycle_entries(c)
        if text:
            text_hits = {e.id
                         for e in find_cell_cycle_entries(text)}
            items = [e for e in items if e.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for e in items:
            li = QListWidgetItem(e.name)
            li.setData(Qt.UserRole, e.id)
            li.setToolTip(f"{e.category} — {e.phase_or_role}")
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching cell-cycle entries.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        eid = current.data(Qt.UserRole)
        e = get_cell_cycle_entry(eid)
        if e is not None:
            self.detail.setHtml(self._render(e))

    def _render(self, e: CellCycleEntry) -> str:
        def _list_html(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        diseases = (", ".join(e.disease_associations)
                    if e.disease_associations
                    else "<i>None catalogued.</i>")
        xref_path = (
            ", ".join(e.cross_reference_signaling_pathway_ids)
            if e.cross_reference_signaling_pathway_ids
            else "<i>None.</i>")
        xref_drug = (
            ", ".join(e.cross_reference_pharm_drug_class_ids)
            if e.cross_reference_pharm_drug_class_ids
            else "<i>None.</i>")
        xref_mol = (
            ", ".join(e.cross_reference_molecule_names)
            if e.cross_reference_molecule_names
            else "<i>None catalogued.</i>")
        notes_html = (f"<h4>Notes</h4><p>{e.notes}</p>"
                      if e.notes else "")
        return (
            f"<h2>{e.name}</h2>"
            f"<p><b>Category:</b> {e.category} &middot; "
            f"<b>Phase / role:</b> {e.phase_or_role}</p>"
            f"<p>{e.summary}</p>"
            f"<h4>Function</h4><p>{e.function}</p>"
            f"<h4>Key components</h4>"
            f"{_list_html(e.key_components)}"
            f"<h4>Activated by</h4>"
            f"{_list_html(e.activated_by)}"
            f"<h4>Inhibited by</h4>"
            f"{_list_html(e.inhibited_by)}"
            f"<h4>Disease associations</h4><p>{diseases}</p>"
            f"<h4>Cross-reference: Cell Bio signalling</h4>"
            f"<p>{xref_path}</p>"
            f"<h4>Cross-reference: Pharm drug classes</h4>"
            f"<p>{xref_drug}</p>"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"{notes_html}"
        )

    def select_entry(self, entry_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == entry_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
