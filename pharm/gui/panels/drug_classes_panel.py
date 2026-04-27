"""Phase PH-1.0 (round 214) — Drug-classes panel for
Pharmacology Studio.

Target-class combo + therapeutic-area combo + free-text filter
+ list + HTML detail card with mechanism / target / agents /
clinical use / side effects / contraindications / monitoring /
cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from pharm.core.drug_classes import (
    DrugClass, TARGET_CLASSES, THERAPEUTIC_AREAS,
    find_drug_classes, get_drug_class, list_drug_classes,
)

log = logging.getLogger(__name__)


class DrugClassesPanel(QWidget):
    """List + detail view for the PH-1.0 drug-class catalogue."""

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
        bar.addWidget(QLabel("Target:"))
        self.target_combo = QComboBox()
        self.target_combo.addItem("(all)", "")
        for tc in TARGET_CLASSES:
            self.target_combo.addItem(tc, tc)
        self.target_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.target_combo)

        bar.addWidget(QLabel("Therapeutic area:"))
        self.area_combo = QComboBox()
        self.area_combo.addItem("(all)", "")
        for ta in THERAPEUTIC_AREAS:
            self.area_combo.addItem(ta, ta)
        self.area_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.area_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / agent / use / side effect)…")
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
        tc = self.target_combo.currentData() or None
        ta = self.area_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_drug_classes(tc, ta)
        if text:
            text_hits = {d.id for d in find_drug_classes(text)}
            items = [d for d in items if d.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for d in items:
            li = QListWidgetItem(d.name)
            li.setData(Qt.UserRole, d.id)
            li.setToolTip(d.molecular_target)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching drug classes.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        cid = current.data(Qt.UserRole)
        d = get_drug_class(cid)
        if d is not None:
            self.detail.setHtml(self._render(d))

    def _render(self, d: DrugClass) -> str:
        def _list_html(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        agents = ", ".join(d.typical_agents)
        areas = ", ".join(d.therapeutic_areas)
        xref_mol = (", ".join(d.cross_reference_molecule_names)
                    if d.cross_reference_molecule_names
                    else "<i>None.</i>")
        xref_enz = (", ".join(d.cross_reference_enzyme_ids)
                    if d.cross_reference_enzyme_ids
                    else "<i>None.</i>")
        xref_signal = (
            ", ".join(d.cross_reference_signaling_pathway_ids)
            if d.cross_reference_signaling_pathway_ids
            else "<i>None.</i>")
        notes_html = (f"<h4>Notes</h4><p>{d.notes}</p>"
                      if d.notes else "")
        return (
            f"<h2>{d.name}</h2>"
            f"<p><b>Target class:</b> {d.target_class} &middot; "
            f"<b>Therapeutic area(s):</b> {areas}</p>"
            f"<h4>Mechanism</h4><p>{d.mechanism}</p>"
            f"<h4>Molecular target</h4><p>{d.molecular_target}</p>"
            f"<h4>Typical agents</h4><p>{agents}</p>"
            f"<h4>Clinical use</h4>{_list_html(d.clinical_use)}"
            f"<h4>Side effects</h4>{_list_html(d.side_effects)}"
            f"<h4>Contraindications</h4>"
            f"{_list_html(d.contraindications)}"
            f"<h4>Monitoring</h4>{_list_html(d.monitoring)}"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"<h4>Cross-reference: Biochem enzymes</h4>"
            f"<p>{xref_enz}</p>"
            f"<h4>Cross-reference: Cell Bio signalling pathways</h4>"
            f"<p>{xref_signal}</p>"
            f"{notes_html}"
        )

    def select_drug_class(self, class_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == class_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
