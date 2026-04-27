"""Phase GM-1.0 (round 230) — Molecular-biology-techniques
panel for Genetics + Molecular Biology Studio.

Category combo + free-text filter + list + HTML detail
card with cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout,
    QWidget,
)

from genetics.core.techniques import (
    CATEGORIES, MolecularBiologyTechnique,
    find_techniques, get_technique, list_techniques,
)

log = logging.getLogger(__name__)


class TechniquesPanel(QWidget):
    """List + detail view for the GM-1.0 molecular-biology-
    techniques catalogue."""

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
            "Filter (name / abbreviation / principle / "
            "platform)…")
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

        items = list_techniques(c)
        if text:
            text_hits = {t.id for t in find_techniques(text)}
            items = [t for t in items if t.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for t in items:
            display = f"{t.abbreviation} — {t.name}"
            li = QListWidgetItem(display)
            li.setData(Qt.UserRole, t.id)
            li.setToolTip(t.category)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching techniques.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        tid = current.data(Qt.UserRole)
        t = get_technique(tid)
        if t is not None:
            self.detail.setHtml(self._render(t))

    def _render(self, t: MolecularBiologyTechnique) -> str:
        def _xref(items, label):
            if not items:
                return ""
            return (f"<h4>Cross-reference: {label}</h4>"
                    f"<p>{', '.join(items)}</p>")

        notes_html = (f"<h4>Notes</h4><p>{t.notes}</p>"
                      if t.notes else "")
        return (
            f"<h2>{t.name}</h2>"
            f"<p><b>Abbreviation:</b> {t.abbreviation} "
            f"&middot; <b>Category:</b> {t.category}</p>"
            f"<h4>Principle</h4><p>{t.principle}</p>"
            f"<h4>Sample types</h4><p>{t.sample_types}</p>"
            f"<h4>Throughput</h4><p>{t.throughput}</p>"
            f"<h4>Typical readout</h4>"
            f"<p>{t.typical_readout}</p>"
            f"<h4>Key reagents</h4><p>{t.key_reagents}</p>"
            f"<h4>Representative platforms</h4>"
            f"<p>{t.representative_platforms}</p>"
            f"<h4>Year introduced</h4>"
            f"<p>{t.year_introduced}</p>"
            f"<h4>Key references</h4>"
            f"<p>{t.key_references}</p>"
            f"<h4>Strengths</h4><p>{t.strengths}</p>"
            f"<h4>Limitations</h4><p>{t.limitations}</p>"
            f"{notes_html}"
            f"{_xref(t.cross_reference_enzyme_ids, 'Biochem enzymes')}"
            f"{_xref(t.cross_reference_cell_cycle_ids, 'Cell Bio cell-cycle entries')}"
            f"{_xref(t.cross_reference_signaling_pathway_ids, 'Cell Bio signalling pathways')}"
            f"{_xref(t.cross_reference_animal_taxon_ids, 'Animal taxa (model organisms)')}"
            f"{_xref(t.cross_reference_molecule_names, 'OrgChem molecules')}"
        )

    def select_technique(self, technique_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == technique_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
