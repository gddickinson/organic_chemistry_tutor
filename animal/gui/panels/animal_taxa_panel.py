"""Phase AB-1.0 (round 217) — Animal-taxa panel for Animal
Biology Studio.

Phylum combo + body-plan combo + free-text filter + list +
HTML detail card with reproductive strategy / ecological role
/ cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from animal.core.taxa import (
    AnimalTaxon, BODY_PLANS, PHYLA,
    find_animal_taxa, get_animal_taxon, list_animal_taxa,
)

log = logging.getLogger(__name__)


class AnimalTaxaPanel(QWidget):
    """List + detail view for the AB-1.0 animal-taxa
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
        bar.addWidget(QLabel("Phylum:"))
        self.phylum_combo = QComboBox()
        self.phylum_combo.addItem("(all)", "")
        for p in PHYLA:
            self.phylum_combo.addItem(p, p)
        self.phylum_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.phylum_combo)

        bar.addWidget(QLabel("Body plan:"))
        self.body_combo = QComboBox()
        self.body_combo.addItem("(all)", "")
        for b in BODY_PLANS:
            self.body_combo.addItem(b, b)
        self.body_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.body_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / class / role / metabolite)…")
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
        p = self.phylum_combo.currentData() or None
        b = self.body_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_animal_taxa(p, b)
        if text:
            text_hits = {t.id for t in find_animal_taxa(text)}
            items = [t for t in items if t.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for t in items:
            li = QListWidgetItem(t.name)
            li.setData(Qt.UserRole, t.id)
            li.setToolTip(t.full_taxonomic_name)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching animal taxa.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        tid = current.data(Qt.UserRole)
        t = get_animal_taxon(tid)
        if t is not None:
            self.detail.setHtml(self._render(t))

    def _render(self, t: AnimalTaxon) -> str:
        model_html = (" &middot; <b>Model organism</b>"
                      if t.model_organism else "")
        xref_mol = (", ".join(t.cross_reference_molecule_names)
                    if t.cross_reference_molecule_names
                    else "<i>None.</i>")
        xref_path = (
            ", ".join(t.cross_reference_signaling_pathway_ids)
            if t.cross_reference_signaling_pathway_ids
            else "<i>None.</i>")
        xref_enz = (
            ", ".join(t.cross_reference_enzyme_ids)
            if t.cross_reference_enzyme_ids
            else "<i>None.</i>")
        notes_html = (f"<h4>Notes</h4><p>{t.notes}</p>"
                      if t.notes else "")
        return (
            f"<h2>{t.name}</h2>"
            f"<p><i>{t.full_taxonomic_name}</i></p>"
            f"<p><b>Phylum:</b> {t.phylum} &middot; "
            f"<b>Class:</b> {t.animal_class}{model_html}</p>"
            f"<p><b>Body plan:</b> {t.body_plan} &middot; "
            f"<b>Germ layers:</b> {t.germ_layers} &middot; "
            f"<b>Coelom:</b> {t.coelom_type} &middot; "
            f"<b>Genome size:</b> {t.genome_size_or_mb}</p>"
            f"<h4>Reproductive strategy</h4>"
            f"<p>{t.reproductive_strategy}</p>"
            f"<h4>Ecological role</h4>"
            f"<p>{t.ecological_role}</p>"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"<h4>Cross-reference: Cell Bio signalling pathways"
            f"</h4><p>{xref_path}</p>"
            f"<h4>Cross-reference: Biochem enzymes</h4>"
            f"<p>{xref_enz}</p>"
            f"{notes_html}"
        )

    def select_taxon(self, taxon_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == taxon_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
