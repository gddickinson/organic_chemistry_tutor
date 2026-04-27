"""Phase MB-2.0 (round 221) — Virulence-factors panel for
Microbiology Studio.

Mechanism-class combo + free-text filter + list + HTML detail
card with structural notes / target tissue / mode of action /
clinical syndrome / vaccine info / cross-references.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

from microbio.core.virulence_factors import (
    MECHANISM_CLASSES, VirulenceFactor,
    find_virulence_factors, get_virulence_factor,
    list_virulence_factors,
)

log = logging.getLogger(__name__)


class VirulenceFactorsPanel(QWidget):
    """List + detail view for the MB-2.0 virulence-factor
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
        bar.addWidget(QLabel("Mechanism:"))
        self.class_combo = QComboBox()
        self.class_combo.addItem("(all)", "")
        for c in MECHANISM_CLASSES:
            self.class_combo.addItem(c, c)
        self.class_combo.currentIndexChanged.connect(
            self._refresh_list)
        bar.addWidget(self.class_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter (toxin / target / syndrome / vaccine)…")
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

        items = list_virulence_factors(c)
        if text:
            text_hits = {f.id
                         for f in find_virulence_factors(text)}
            items = [f for f in items if f.id in text_hits]

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for f in items:
            li = QListWidgetItem(f.name)
            li.setData(Qt.UserRole, f.id)
            li.setToolTip(f.mechanism_class)
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if items:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching virulence factors.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        fid = current.data(Qt.UserRole)
        f = get_virulence_factor(fid)
        if f is not None:
            self.detail.setHtml(self._render(f))

    def _render(self, f: VirulenceFactor) -> str:
        def _list_html(items, fallback="<i>None.</i>"):
            return ("<ul>" + "".join(f"<li>{x}</li>"
                                      for x in items) + "</ul>"
                    if items else fallback)

        vacc_html = _list_html(
            f.vaccine_or_antitoxin,
            "<i>None catalogued.</i>")
        xref_m = (", ".join(f.cross_reference_microbe_ids)
                  if f.cross_reference_microbe_ids
                  else "<i>None catalogued.</i>")
        xref_e = (", ".join(f.cross_reference_enzyme_ids)
                  if f.cross_reference_enzyme_ids
                  else "<i>None catalogued.</i>")
        xref_p = (
            ", ".join(f.cross_reference_signaling_pathway_ids)
            if f.cross_reference_signaling_pathway_ids
            else "<i>None catalogued.</i>")
        notes_html = (f"<h4>Notes</h4><p>{f.notes}</p>"
                      if f.notes else "")
        return (
            f"<h2>{f.name}</h2>"
            f"<p><b>Mechanism class:</b> "
            f"{f.mechanism_class}</p>"
            f"<h4>Structural notes</h4>"
            f"{_list_html(f.structural_notes)}"
            f"<h4>Target tissue / cell</h4>"
            f"{_list_html(f.target_tissue_or_cell)}"
            f"<h4>Mode of action</h4>"
            f"{_list_html(f.mode_of_action)}"
            f"<h4>Clinical syndrome</h4>"
            f"{_list_html(f.clinical_syndrome)}"
            f"<h4>Vaccine / antitoxin</h4>{vacc_html}"
            f"<h4>Cross-reference: Microbio source organisms"
            f"</h4><p>{xref_m}</p>"
            f"<h4>Cross-reference: Biochem enzymes</h4>"
            f"<p>{xref_e}</p>"
            f"<h4>Cross-reference: Cell Bio signalling</h4>"
            f"<p>{xref_p}</p>"
            f"{notes_html}"
        )

    def select_factor(self, factor_id: str) -> bool:
        """Focus the row whose id matches.  Returns True if
        found."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == factor_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
