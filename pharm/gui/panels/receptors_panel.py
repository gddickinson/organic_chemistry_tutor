"""Phase PH-2.0 (round 220) — Receptors panel for Pharm Studio.

Receptor-family combo + free-text filter + list + HTML detail
card with structural summary / endogenous ligands / signalling
output / tissue distribution / clinical relevance / cross-
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

from pharm.core.receptors import (
    RECEPTOR_FAMILIES, Receptor,
    find_receptors, get_receptor, list_receptors,
)

log = logging.getLogger(__name__)


class ReceptorsPanel(QWidget):
    """List + detail view for the PH-2.0 receptor catalogue."""

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
        bar.addWidget(QLabel("Family:"))
        self.family_combo = QComboBox()
        self.family_combo.addItem("(all)", "")
        for f in RECEPTOR_FAMILIES:
            self.family_combo.addItem(f, f)
        self.family_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.family_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / ligand / tissue / drug)…")
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
        f = self.family_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_receptors(f)
        if text:
            text_hits = {r.id for r in find_receptors(text)}
            items = [r for r in items if r.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for r in items:
            li = QListWidgetItem(r.name)
            li.setData(Qt.UserRole, r.id)
            li.setToolTip(r.receptor_subtype)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching receptors.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        rid = current.data(Qt.UserRole)
        r = get_receptor(rid)
        if r is not None:
            self.detail.setHtml(self._render(r))

    def _render(self, r: Receptor) -> str:
        def _list_html(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        xref_dc = (", ".join(r.cross_reference_drug_class_ids)
                   if r.cross_reference_drug_class_ids
                   else "<i>None catalogued.</i>")
        xref_path = (
            ", ".join(r.cross_reference_signaling_pathway_ids)
            if r.cross_reference_signaling_pathway_ids
            else "<i>None catalogued.</i>")
        xref_enz = (", ".join(r.cross_reference_enzyme_ids)
                    if r.cross_reference_enzyme_ids
                    else "<i>None catalogued.</i>")
        xref_mol = (
            ", ".join(r.cross_reference_molecule_names)
            if r.cross_reference_molecule_names
            else "<i>None catalogued.</i>")
        notes_html = (f"<h4>Notes</h4><p>{r.notes}</p>"
                      if r.notes else "")
        return (
            f"<h2>{r.name}</h2>"
            f"<p><b>Family:</b> {r.receptor_family} &middot; "
            f"<b>Subtype:</b> {r.receptor_subtype}</p>"
            f"<p>{r.structural_summary}</p>"
            f"<h4>Endogenous ligands</h4>"
            f"{_list_html(r.endogenous_ligands)}"
            f"<h4>Signalling output</h4>"
            f"{_list_html(r.signalling_output)}"
            f"<h4>Tissue distribution</h4>"
            f"{_list_html(r.tissue_distribution)}"
            f"<h4>Clinical relevance</h4>"
            f"{_list_html(r.clinical_relevance)}"
            f"<h4>Cross-reference: Pharm drug classes</h4>"
            f"<p>{xref_dc}</p>"
            f"<h4>Cross-reference: Cell Bio signalling</h4>"
            f"<p>{xref_path}</p>"
            f"<h4>Cross-reference: Biochem enzymes</h4>"
            f"<p>{xref_enz}</p>"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"{notes_html}"
        )

    def select_receptor(self, receptor_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == receptor_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
