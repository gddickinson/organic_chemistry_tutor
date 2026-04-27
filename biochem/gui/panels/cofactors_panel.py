"""Phase BC-2.0 (round 219) — Cofactors panel for Biochem
Studio.

Cofactor-class combo + free-text filter + list + HTML detail
card with chemistry / role / vitamin origin / deficiency
disease / cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from biochem.core.cofactors import (
    COFACTOR_CLASSES, Cofactor,
    find_cofactors, get_cofactor, list_cofactors,
)

log = logging.getLogger(__name__)


class CofactorsPanel(QWidget):
    """List + detail view for the BC-2.0 cofactors catalogue."""

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
        for c in COFACTOR_CLASSES:
            self.class_combo.addItem(c, c)
        self.class_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.class_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / chemistry / vitamin / disease)…")
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
        cc = self.class_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_cofactors(cc)
        if text:
            text_hits = {c.id for c in find_cofactors(text)}
            items = [c for c in items if c.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for c in items:
            li = QListWidgetItem(c.name)
            li.setData(Qt.UserRole, c.id)
            li.setToolTip(c.cofactor_class)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching cofactors.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        cid = current.data(Qt.UserRole)
        c = get_cofactor(cid)
        if c is not None:
            self.detail.setHtml(self._render(c))

    def _render(self, c: Cofactor) -> str:
        def _list_html(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        vit_html = (", ".join(c.vitamin_origin)
                    if c.vitamin_origin
                    else "<i>None (not a vitamin).</i>")
        def_html = _list_html(c.deficiency_disease,
                              "<i>None catalogued.</i>")
        xref_enz = (", ".join(c.cross_reference_enzyme_ids)
                    if c.cross_reference_enzyme_ids
                    else "<i>None catalogued.</i>")
        xref_path = (
            ", ".join(c.cross_reference_metabolic_pathway_ids)
            if c.cross_reference_metabolic_pathway_ids
            else "<i>None catalogued.</i>")
        xref_mol = (
            ", ".join(c.cross_reference_molecule_names)
            if c.cross_reference_molecule_names
            else "<i>None catalogued.</i>")
        notes_html = (f"<h4>Notes</h4><p>{c.notes}</p>"
                      if c.notes else "")
        return (
            f"<h2>{c.name}</h2>"
            f"<p><b>Class:</b> {c.cofactor_class} &middot; "
            f"<b>Vitamin origin:</b> {vit_html}</p>"
            f"<p>{c.chemical_summary}</p>"
            f"<h4>Primary role</h4>{_list_html(c.primary_role)}"
            f"<h4>Carriers / substrates</h4>"
            f"{_list_html(c.carriers_or_substrates)}"
            f"<h4>Key features</h4>{_list_html(c.key_features)}"
            f"<h4>Deficiency disease</h4>{def_html}"
            f"<h4>Cross-reference: Biochem enzymes</h4>"
            f"<p>{xref_enz}</p>"
            f"<h4>Cross-reference: Metabolic pathways</h4>"
            f"<p>{xref_path}</p>"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"{notes_html}"
        )

    def select_cofactor(self, cofactor_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == cofactor_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
