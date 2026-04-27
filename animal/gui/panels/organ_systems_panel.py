"""Phase AB-2.0 (round 223) — Organ-systems panel for Animal
Biology Studio.

System-category combo + free-text filter + list + HTML detail
card with summary / organs / cell types / functional anatomy
/ evolutionary origin / disorders / cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from animal.core.organ_systems import (
    OrganSystem, SYSTEM_CATEGORIES,
    find_organ_systems, get_organ_system, list_organ_systems,
)

log = logging.getLogger(__name__)


class OrganSystemsPanel(QWidget):
    """List + detail view for the AB-2.0 organ-systems
    catalogue."""

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
        for c in SYSTEM_CATEGORIES:
            self.category_combo.addItem(c, c)
        self.category_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.category_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (organ / cell / disorder / animal)…")
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

        items = list_organ_systems(c)
        if text:
            text_hits = {s.id for s in find_organ_systems(text)}
            items = [s for s in items if s.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for s in items:
            li = QListWidgetItem(s.name)
            li.setData(Qt.UserRole, s.id)
            li.setToolTip(s.system_category)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching organ systems.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        sid = current.data(Qt.UserRole)
        s = get_organ_system(sid)
        if s is not None:
            self.detail.setHtml(self._render(s))

    def _render(self, s: OrganSystem) -> str:
        def _list_html(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        dis_html = _list_html(s.characteristic_disorders,
                              "<i>None catalogued.</i>")
        xref_m = (", ".join(s.cross_reference_molecule_names)
                  if s.cross_reference_molecule_names
                  else "<i>None catalogued.</i>")
        xref_p = (
            ", ".join(s.cross_reference_signaling_pathway_ids)
            if s.cross_reference_signaling_pathway_ids
            else "<i>None catalogued.</i>")
        xref_e = (", ".join(s.cross_reference_enzyme_ids)
                  if s.cross_reference_enzyme_ids
                  else "<i>None catalogued.</i>")
        xref_t = (
            ", ".join(s.cross_reference_animal_taxon_ids)
            if s.cross_reference_animal_taxon_ids
            else "<i>None catalogued.</i>")
        notes_html = (f"<h4>Notes</h4><p>{s.notes}</p>"
                      if s.notes else "")
        return (
            f"<h2>{s.name}</h2>"
            f"<p><b>Category:</b> {s.system_category}</p>"
            f"<p>{s.short_summary}</p>"
            f"<h4>Representative organs</h4>"
            f"{_list_html(s.representative_organs)}"
            f"<h4>Key cell types</h4>"
            f"{_list_html(s.key_cell_types)}"
            f"<h4>Functional anatomy</h4>"
            f"{_list_html(s.functional_anatomy)}"
            f"<h4>Evolutionary origin</h4>"
            f"{_list_html(s.evolutionary_origin)}"
            f"<h4>Characteristic disorders</h4>{dis_html}"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_m}</p>"
            f"<h4>Cross-reference: Cell Bio signalling</h4>"
            f"<p>{xref_p}</p>"
            f"<h4>Cross-reference: Biochem enzymes</h4>"
            f"<p>{xref_e}</p>"
            f"<h4>Cross-reference: Animal Biology taxa</h4>"
            f"<p>{xref_t}</p>"
            f"{notes_html}"
        )

    def select_system(self, system_id: str) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == system_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
