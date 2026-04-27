"""Phase CB-1.0 (round 212) — Signalling-pathway panel for the
Cell Bio Studio main window.

Layout: category combo + receptor-class combo + free-text filter
+ pathway list on the left; HTML detail card on the right with
key components / function / disease associations / drug targets /
cross-references / notes.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from cellbio.core.cell_signaling import (
    CATEGORIES, RECEPTOR_CLASSES, SignalingPathway,
    find_pathways, get_pathway, list_pathways,
)

log = logging.getLogger(__name__)


class SignalingPanel(QWidget):
    """List + detail view for cell-signalling pathways."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._refresh_list()
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    # ---------------- UI ------------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        # Filter bar
        filter_bar = QHBoxLayout()
        filter_bar.addWidget(QLabel("Category:"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItem("(all)", "")
        for c in CATEGORIES:
            self.cat_combo.addItem(c, c)
        self.cat_combo.currentIndexChanged.connect(self._refresh_list)
        filter_bar.addWidget(self.cat_combo)

        filter_bar.addWidget(QLabel("Receptor:"))
        self.rc_combo = QComboBox()
        self.rc_combo.addItem("(all)", "")
        for rc in RECEPTOR_CLASSES:
            self.rc_combo.addItem(rc, rc)
        self.rc_combo.currentIndexChanged.connect(self._refresh_list)
        filter_bar.addWidget(self.rc_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (name / drug / disease)…")
        self.filter_edit.textChanged.connect(self._refresh_list)
        filter_bar.addWidget(self.filter_edit, stretch=1)

        outer.addLayout(filter_bar)

        # Splitter: list | detail
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

    # ---------------- model ---------------------------------------

    def _refresh_list(self) -> None:
        cat = self.cat_combo.currentData() or None
        rc = self.rc_combo.currentData() or None
        text = (self.filter_edit.text() or "").strip()

        items = list_pathways(cat, rc)
        if text:
            text_hits = set(p.id for p in find_pathways(text))
            items = [p for p in items if p.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for p in items:
            li = QListWidgetItem(p.name)
            li.setData(Qt.UserRole, p.id)
            li.setToolTip(p.canonical_function)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)
        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching pathways.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        pid = current.data(Qt.UserRole)
        p = get_pathway(pid)
        if p is None:
            return
        self.detail.setHtml(self._render(p))

    def _render(self, p: SignalingPathway) -> str:
        comp_html = "".join(
            f"<li>{c}</li>" for c in p.key_components)
        disease_html = "".join(
            f"<li>{d}</li>" for d in p.disease_associations)
        drug_rows = "".join(
            f"<tr><td>{drug}</td><td>{tgt}</td></tr>"
            for drug, tgt in p.drug_targets)
        drug_html = (
            f"<table border='1' cellpadding='4' "
            f"cellspacing='0'>"
            f"<tr><th>Drug</th><th>Target</th></tr>"
            f"{drug_rows}</table>"
            if drug_rows else "<i>None catalogued.</i>"
        )
        xref_mol = ", ".join(p.cross_reference_molecule_names) \
            if p.cross_reference_molecule_names else "<i>None.</i>"
        xref_path = ", ".join(p.cross_reference_pathway_ids) \
            if p.cross_reference_pathway_ids else "<i>None.</i>"
        notes_html = (f"<h4>Notes</h4><p>{p.notes}</p>"
                      if p.notes else "")
        return (
            f"<h2>{p.name}</h2>"
            f"<p><b>id:</b> <code>{p.id}</code> &middot; "
            f"<b>category:</b> {p.category} &middot; "
            f"<b>receptor class:</b> {p.receptor_class}</p>"
            f"<h4>Canonical function</h4>"
            f"<p>{p.canonical_function}</p>"
            f"<h4>Key components (in pathway order)</h4>"
            f"<ol>{comp_html}</ol>"
            f"<h4>Disease associations</h4>"
            f"<ul>{disease_html}</ul>"
            f"<h4>Drug targets</h4>"
            f"{drug_html}"
            f"<h4>Cross-reference: OrgChem molecules</h4>"
            f"<p>{xref_mol}</p>"
            f"<h4>Cross-reference: sister signalling pathways</h4>"
            f"<p>{xref_path}</p>"
            f"{notes_html}"
        )

    # ---------------- programmatic API ----------------------------

    def select_pathway(self, pathway_id: str) -> bool:
        """Focus the row whose id matches ``pathway_id``.  Returns
        True if found, False otherwise.  Used by the
        ``open_cellbio_studio`` agent action when called with a
        deep-link target."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None and item.data(Qt.UserRole) == pathway_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
