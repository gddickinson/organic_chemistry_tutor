"""Phase BT-1.0 (round 216) — Plant-taxa panel for Botany Studio.

Division combo + photosynthetic-strategy combo + free-text
filter + list + HTML detail card with reproductive strategy /
ecological role / economic importance / cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from botany.core.taxa import (
    DIVISIONS, PHOTOSYNTHETIC_STRATEGIES, PlantTaxon,
    find_plant_taxa, get_plant_taxon, list_plant_taxa,
)

log = logging.getLogger(__name__)


class PlantTaxaPanel(QWidget):
    """List + detail view for the BT-1.0 plant-taxa catalogue."""

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
        bar.addWidget(QLabel("Division:"))
        self.division_combo = QComboBox()
        self.division_combo.addItem("(all)", "")
        for d in DIVISIONS:
            self.division_combo.addItem(d, d)
        self.division_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.division_combo)

        bar.addWidget(QLabel("Photosynthesis:"))
        self.photo_combo = QComboBox()
        self.photo_combo.addItem("(all)", "")
        for p in PHOTOSYNTHETIC_STRATEGIES:
            self.photo_combo.addItem(p, p)
        self.photo_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.photo_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / role / metabolite)…")
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
        d = self.division_combo.currentData() or None
        p = self.photo_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_plant_taxa(d, p)
        if text:
            text_hits = {t.id for t in find_plant_taxa(text)}
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
                "<p><i>No matching plant taxa.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        tid = current.data(Qt.UserRole)
        t = get_plant_taxon(tid)
        if t is not None:
            self.detail.setHtml(self._render(t))

    def _render(self, t: PlantTaxon) -> str:
        model_html = (" &middot; <b>Model organism</b>"
                      if t.model_organism else "")
        xref_mol = (", ".join(t.cross_reference_molecule_names)
                    if t.cross_reference_molecule_names
                    else "<i>None.</i>")
        xref_path = (
            ", ".join(t.cross_reference_metabolic_pathway_ids)
            if t.cross_reference_metabolic_pathway_ids
            else "<i>None.</i>")
        xref_drug = (
            ", ".join(t.cross_reference_pharm_drug_class_ids)
            if t.cross_reference_pharm_drug_class_ids
            else "<i>None.</i>")
        notes_html = (f"<h4>Notes</h4><p>{t.notes}</p>"
                      if t.notes else "")
        return (
            f"<h2>{t.name}</h2>"
            f"<p><i>{t.full_taxonomic_name}</i></p>"
            f"<p><b>Division:</b> {t.division} &middot; "
            f"<b>Class:</b> {t.plant_class}{model_html}</p>"
            f"<p><b>Life cycle:</b> {t.life_cycle} &middot; "
            f"<b>Photosynthesis:</b> "
            f"{t.photosynthetic_strategy} &middot; "
            f"<b>Genome size:</b> {t.genome_size_or_mb}</p>"
            f"<h4>Reproductive strategy</h4>"
            f"<p>{t.reproductive_strategy}</p>"
            f"<h4>Ecological role</h4>"
            f"<p>{t.ecological_role}</p>"
            f"<h4>Economic importance</h4>"
            f"<p>{t.economic_importance}</p>"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"<h4>Cross-reference: metabolic pathways</h4>"
            f"<p>{xref_path}</p>"
            f"<h4>Cross-reference: Pharm drug classes</h4>"
            f"<p>{xref_drug}</p>"
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
