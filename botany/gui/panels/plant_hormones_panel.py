"""Phase BT-2.0 (round 222) — Plant-hormones panel for Botany
Studio.

Hormone-class combo + free-text filter + list + HTML detail
card with structural class / biosynthesis / perception /
physiological effect / antagonisms / model plants / cross-
references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from botany.core.plant_hormones import (
    HORMONE_CLASSES, PlantHormone,
    find_plant_hormones, get_plant_hormone, list_plant_hormones,
)

log = logging.getLogger(__name__)


class PlantHormonesPanel(QWidget):
    """List + detail view for the BT-2.0 plant-hormones
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
        bar.addWidget(QLabel("Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItem("(all)", "")
        for c in HORMONE_CLASSES:
            self.class_combo.addItem(c, c)
        self.class_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.class_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / receptor / effect / model)…")
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
        c = self.class_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_plant_hormones(c)
        if text:
            text_hits = {h.id for h in find_plant_hormones(text)}
            items = [h for h in items if h.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for h in items:
            li = QListWidgetItem(h.name)
            li.setData(Qt.UserRole, h.id)
            li.setToolTip(h.hormone_class)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching plant hormones.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        hid = current.data(Qt.UserRole)
        h = get_plant_hormone(hid)
        if h is not None:
            self.detail.setHtml(self._render(h))

    def _render(self, h: PlantHormone) -> str:
        def _list_html(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        ant_html = _list_html(h.antagonisms,
                              "<i>None catalogued.</i>")
        xref_m = (", ".join(h.cross_reference_molecule_names)
                  if h.cross_reference_molecule_names
                  else "<i>None catalogued.</i>")
        xref_t = (", ".join(h.cross_reference_plant_taxon_ids)
                  if h.cross_reference_plant_taxon_ids
                  else "<i>None catalogued.</i>")
        notes_html = (f"<h4>Notes</h4><p>{h.notes}</p>"
                      if h.notes else "")
        return (
            f"<h2>{h.name}</h2>"
            f"<p><b>Class:</b> {h.hormone_class}</p>"
            f"<p>{h.structural_class}</p>"
            f"<h4>Biosynthesis precursor</h4>"
            f"{_list_html(h.biosynthesis_precursor)}"
            f"<h4>Perception mechanism</h4>"
            f"{_list_html(h.perception_mechanism)}"
            f"<h4>Primary physiological effect</h4>"
            f"{_list_html(h.primary_physiological_effect)}"
            f"<h4>Antagonisms</h4>{ant_html}"
            f"<h4>Key model plants</h4>"
            f"{_list_html(h.key_model_plants)}"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_m}</p>"
            f"<h4>Cross-reference: Botany plant taxa</h4>"
            f"<p>{xref_t}</p>"
            f"{notes_html}"
        )

    def select_hormone(self, hormone_id: str) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == hormone_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
