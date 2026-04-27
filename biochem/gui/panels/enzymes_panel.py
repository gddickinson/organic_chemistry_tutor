"""Phase BC-1.0 (round 213) — Enzymes panel for Biochem Studio.

EC-class combo + free-text filter + list of enzymes; HTML detail
card with EC number / mechanism / substrates / products /
cofactors / regulators / disease associations / drug targets /
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

from biochem.core.enzymes import (
    EC_CLASS_NAMES, Enzyme,
    find_enzymes, get_enzyme, list_enzymes,
)

log = logging.getLogger(__name__)


class EnzymesPanel(QWidget):
    """List + detail view for the BC-1.0 enzyme catalogue."""

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
        bar.addWidget(QLabel("EC class:"))
        self.ec_combo = QComboBox()
        self.ec_combo.addItem("(all)", 0)
        for ec_num, ec_name in EC_CLASS_NAMES.items():
            self.ec_combo.addItem(
                f"{ec_num} — {ec_name}", ec_num)
        self.ec_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.ec_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / drug / disease / EC #)…")
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
        self.detail.setOpenExternalLinks(False)
        split.addWidget(self.detail)

        split.setStretchFactor(0, 1)
        split.setStretchFactor(1, 2)

    def _refresh_list(self) -> None:
        ec = self.ec_combo.currentData() or 0
        text = (self.filter_edit.text() or "").strip()

        items = list_enzymes(ec_class=ec if ec else None)
        if text:
            text_hits = {e.id for e in find_enzymes(text)}
            items = [e for e in items if e.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for e in items:
            li = QListWidgetItem(
                f"[{e.ec_number}] {e.name}")
            li.setData(Qt.UserRole, e.id)
            li.setToolTip(e.mechanism_class)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching enzymes.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        eid = current.data(Qt.UserRole)
        e = get_enzyme(eid)
        if e is not None:
            self.detail.setHtml(self._render(e))

    def _render(self, e: Enzyme) -> str:
        def _list(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        drug_rows = "".join(
            f"<tr><td>{drug}</td><td>{tgt}</td></tr>"
            for drug, tgt in e.drug_targets)
        drug_html = (
            "<table border='1' cellpadding='4' "
            "cellspacing='0'>"
            "<tr><th>Drug</th><th>Target</th></tr>"
            f"{drug_rows}</table>"
            if drug_rows else "<i>None catalogued.</i>"
        )
        xref_mol = (", ".join(e.cross_reference_molecule_names)
                    if e.cross_reference_molecule_names
                    else "<i>None.</i>")
        xref_path = (", ".join(e.cross_reference_pathway_ids)
                     if e.cross_reference_pathway_ids
                     else "<i>None.</i>")
        xref_signal = (
            ", ".join(e.cross_reference_signaling_pathway_ids)
            if e.cross_reference_signaling_pathway_ids
            else "<i>None.</i>")
        ec_name = EC_CLASS_NAMES.get(e.ec_class, "?")
        notes_html = (f"<h4>Notes</h4><p>{e.notes}</p>"
                      if e.notes else "")
        return (
            f"<h2>{e.name}</h2>"
            f"<p><b>EC:</b> {e.ec_number} &middot; "
            f"<b>Class {e.ec_class}:</b> {ec_name} &middot; "
            f"<b>Mechanism:</b> {e.mechanism_class}</p>"
            f"<p><b>Structural family:</b> "
            f"{e.structural_family}</p>"
            f"<h4>Substrates</h4>{_list(e.substrates)}"
            f"<h4>Products</h4>{_list(e.products)}"
            f"<h4>Cofactors</h4>{_list(e.cofactors)}"
            f"<h4>Regulators</h4>{_list(e.regulators)}"
            f"<h4>Disease associations</h4>"
            f"{_list(e.disease_associations)}"
            f"<h4>Drug targets</h4>{drug_html}"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"<h4>Cross-reference: OrgChem metabolic pathways</h4>"
            f"<p>{xref_path}</p>"
            f"<h4>Cross-reference: Cell Bio signalling pathways</h4>"
            f"<p>{xref_signal}</p>"
            f"{notes_html}"
        )

    def select_enzyme(self, enzyme_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == enzyme_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
