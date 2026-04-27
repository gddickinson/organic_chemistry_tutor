"""Phase BT-1.0 (round 216) — Plant-secondary-metabolites
bridge panel.

Read-only view of the OrgChem ``Molecule`` DB filtered to plant-
derived natural products.  Demonstrates Botany Studio reading
another sibling's data DIRECTLY FROM SQLITE (not from a Python
catalogue) — the first sibling whose bridge does so.  Confirms
the cross-studio pattern works for live DB rows + per-row
``source_tags_json`` filtering.

The *Open in Molecule Workspace* button fires
``bus().molecule_selected.emit(mol_id)`` so the user lands in
the OrgChem main-window molecule tab.
"""
from __future__ import annotations
import json
import logging
from typing import List, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSplitter, QTextBrowser,
    QVBoxLayout, QWidget,
)

from orgchem.db.queries import list_molecules
from orgchem.messaging.bus import bus

log = logging.getLogger(__name__)

# Plant-relevant source tags from the OrgChem DB.  Hand-curated
# botany-driven view of the molecule store.  Order matters —
# `(all plant-derived)` aggregates every tag below it.
PLANT_RELEVANT_TAGS: Tuple[Tuple[str, str], ...] = (
    ("(all plant-derived)", "*plant"),
    ("Natural products", "natural-product"),
    ("Terpenes / monoterpenes", "terpene"),
    ("Alkaloids", "alkaloid"),
    ("Steroids", "steroid"),
)


def _has_tag(row, tag: str) -> bool:
    """Substring-test a row's source_tags_json safely."""
    if not row.source_tags_json:
        return False
    try:
        tags = json.loads(row.source_tags_json)
    except Exception:  # noqa: BLE001
        return False
    return tag in tags


def _matches_filter(row, tag_value: str) -> bool:
    """Tag-value matcher.  Special ``*plant`` aggregates."""
    if tag_value == "*plant":
        return any(_has_tag(row, t)
                   for _, t in PLANT_RELEVANT_TAGS
                   if t != "*plant")
    return _has_tag(row, tag_value)


class PlantMetabolitesPanel(QWidget):
    """Bridge view onto OrgChem Molecule rows tagged as plant-
    derived natural products."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._populate()
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        outer.addWidget(QLabel(
            "<b>Plant-derived secondary metabolites (read-only "
            "bridge to the OrgChem molecule DB).</b>  Filtered "
            "live from <code>orgchem.db.Molecule</code> by "
            "<code>source_tags_json</code> entries.  Click "
            "<i>Open in Molecule Workspace</i> to focus the "
            "selected compound in the OrgChem main window."
        ))

        bar = QHBoxLayout()
        bar.addWidget(QLabel("Category:"))
        self.tag_combo = QComboBox()
        for label, tag in PLANT_RELEVANT_TAGS:
            self.tag_combo.addItem(label, tag)
        self.tag_combo.currentIndexChanged.connect(
            self._populate)
        bar.addWidget(self.tag_combo)

        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Filter by name…")
        self.filter_edit.textChanged.connect(self._populate)
        bar.addWidget(self.filter_edit, stretch=1)

        self.open_btn = QPushButton(
            "Open in Molecule Workspace…")
        self.open_btn.setToolTip(
            "Switch the OrgChem main window to the molecule "
            "tab + load the selected compound.")
        self.open_btn.clicked.connect(self._on_open_in_workspace)
        bar.addWidget(self.open_btn)
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

    def _filtered_rows(self) -> List:
        tag_value = self.tag_combo.currentData() or "*plant"
        text = (self.filter_edit.text() or "").strip().lower()
        rows = []
        for row in list_molecules(limit=10000):
            if not _matches_filter(row, tag_value):
                continue
            if text and text not in (row.name or "").lower():
                continue
            rows.append(row)
        return rows

    def _populate(self) -> None:
        rows = self._filtered_rows()
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for row in rows:
            li = QListWidgetItem(row.name or f"#{row.id}")
            li.setData(Qt.UserRole, row.id)
            li.setToolTip(row.smiles or "")
            self.list_widget.addItem(li)
        self.list_widget.blockSignals(False)

        if rows:
            self.list_widget.setCurrentRow(0)
        else:
            self.detail.setHtml(
                "<p><i>No matching plant-derived "
                "metabolites.</i></p>")

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        mol_id = current.data(Qt.UserRole)
        from orgchem.db.queries import get_molecule
        m = get_molecule(mol_id)
        if m is None:
            return
        try:
            tags = json.loads(m.source_tags_json or "[]")
        except Exception:  # noqa: BLE001
            tags = []
        plant_tags = [t for _, t in PLANT_RELEVANT_TAGS
                      if t != "*plant" and t in tags]
        tag_html = (", ".join(plant_tags)
                    if plant_tags else "<i>none</i>")
        formula_html = (
            f"<p><b>Formula:</b> {m.formula}</p>"
            if m.formula else "")
        smiles_html = (
            f"<p><b>SMILES:</b> <code>"
            f"{m.smiles}</code></p>"
            if m.smiles else "")
        return self.detail.setHtml(
            f"<h2>{m.name}</h2>"
            f"<p><b>Plant-relevant tags:</b> {tag_html}</p>"
            f"{formula_html}"
            f"{smiles_html}"
            f"<p style='color:#888'><i>Source: "
            f"<code>orgchem.db.Molecule</code> "
            f"(live DB read).</i></p>"
        )

    def _on_open_in_workspace(self) -> None:
        """Hand off to the OrgChem main-window molecule tab."""
        item = self.list_widget.currentItem()
        if item is None:
            return
        mol_id = item.data(Qt.UserRole)
        try:
            bus().molecule_selected.emit(int(mol_id))
        except Exception:  # noqa: BLE001
            log.exception(
                "Failed to emit molecule_selected from botany "
                "metabolites panel.")

    def select_molecule(self, mol_id: int) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and int(item.data(Qt.UserRole)) == int(mol_id):
                self.list_widget.setCurrentRow(i)
                return True
        return False
