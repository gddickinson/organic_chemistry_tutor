"""Phase MB-1.0 (round 215) — Microbes panel for Microbiology
Studio.

Kingdom combo + gram-type combo + free-text filter + list +
HTML detail card with morphology / replication / pathogenesis
/ antibiotic susceptibility / genome / cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from microbio.core.microbes import (
    GRAM_TYPES, KINGDOMS, Microbe,
    find_microbes, get_microbe, list_microbes,
)

log = logging.getLogger(__name__)


class MicrobesPanel(QWidget):
    """List + detail view for the MB-1.0 microbe catalogue."""

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
        bar.addWidget(QLabel("Kingdom:"))
        self.kingdom_combo = QComboBox()
        self.kingdom_combo.addItem("(all)", "")
        for k in KINGDOMS:
            self.kingdom_combo.addItem(k, k)
        self.kingdom_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.kingdom_combo)

        bar.addWidget(QLabel("Gram:"))
        self.gram_combo = QComboBox()
        self.gram_combo.addItem("(all)", "")
        for g in GRAM_TYPES:
            self.gram_combo.addItem(g, g)
        self.gram_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.gram_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / morphology / pathogenesis)…")
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
        k = self.kingdom_combo.currentData() or None
        g = self.gram_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_microbes(k, g)
        if text:
            text_hits = {m.id for m in find_microbes(text)}
            items = [m for m in items if m.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for m in items:
            li = QListWidgetItem(m.name)
            li.setData(Qt.UserRole, m.id)
            li.setToolTip(m.full_taxonomic_name)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching microbes.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        mid = current.data(Qt.UserRole)
        m = get_microbe(mid)
        if m is not None:
            self.detail.setHtml(self._render(m))

    def _render(self, m: Microbe) -> str:
        baltimore = (f" &middot; <b>Baltimore class:</b> "
                     f"{m.baltimore_class}"
                     if m.baltimore_class else "")
        xref_cc = (", ".join(m.cross_reference_cell_component_ids)
                   if m.cross_reference_cell_component_ids
                   else "<i>None.</i>")
        xref_pc = (", ".join(m.cross_reference_pharm_drug_class_ids)
                   if m.cross_reference_pharm_drug_class_ids
                   else "<i>None.</i>")
        xref_en = (", ".join(m.cross_reference_enzyme_ids)
                   if m.cross_reference_enzyme_ids
                   else "<i>None.</i>")
        notes_html = (f"<h4>Notes</h4><p>{m.notes}</p>"
                      if m.notes else "")
        return (
            f"<h2>{m.name}</h2>"
            f"<p><i>{m.full_taxonomic_name}</i></p>"
            f"<p><b>Kingdom:</b> {m.kingdom} &middot; "
            f"<b>Gram type:</b> {m.gram_type}{baltimore}</p>"
            f"<h4>Morphology</h4><p>{m.morphology}</p>"
            f"<h4>Key metabolism / replication</h4>"
            f"<p>{m.key_metabolism_or_replication}</p>"
            f"<h4>Pathogenesis</h4>"
            f"<p>{m.pathogenesis_summary}</p>"
            f"<h4>Antibiotic / antimicrobial susceptibility</h4>"
            f"<p>{m.antibiotic_susceptibility}</p>"
            f"<h4>Genome size</h4><p>{m.genome_size_or_kb}</p>"
            f"<h4>Reference</h4>"
            f"<p>{m.ictv_or_bergey_reference}</p>"
            f"<h4>Cross-reference: OrgChem cell components</h4>"
            f"<p>{xref_cc}</p>"
            f"<h4>Cross-reference: Pharm drug classes</h4>"
            f"<p>{xref_pc}</p>"
            f"<h4>Cross-reference: Biochem enzymes</h4>"
            f"<p>{xref_en}</p>"
            f"{notes_html}"
        )

    def select_microbe(self, microbe_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == microbe_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
