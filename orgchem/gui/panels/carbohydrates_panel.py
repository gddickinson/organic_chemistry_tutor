"""Carbohydrates tab — Phase 29b (round 42).

Sibling to the Proteins tab. Browses the Phase 29a `CARBOHYDRATES`
catalogue with:

- Family combo (all / monosaccharide / disaccharide / polysaccharide).
- Free-text filter on the entry name.
- Entry list (family sub-headings implied by the combo filter).
- Details pane: 2D structure (`draw2d.render_svg`), metadata (form /
  carbonyl type / anomer / glycosidic bond / notes), a
  SMILES copy button, and a "Show in Molecule Workspace" link that
  re-uses the existing viewer if the entry is in the DB.
"""
from __future__ import annotations
import logging
from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import QByteArray
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QListWidget, QListWidgetItem, QPushButton, QSplitter, QFrame,
    QTextBrowser,
)

from rdkit import Chem

from orgchem.core.carbohydrates import (
    CARBOHYDRATES, Carbohydrate, families,
)
from orgchem.messaging.bus import bus
from orgchem.render.draw2d import render_svg

log = logging.getLogger(__name__)


class CarbohydratesPanel(QWidget):
    """Dedicated browser + viewer for the seeded carbohydrate catalogue."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._populate_list()
        if self.entry_list.count() > 0:
            self.entry_list.setCurrentRow(0)

    # -----------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)

        root.addWidget(QLabel(
            f"Seeded catalogue: {len(CARBOHYDRATES)} sugars across "
            f"{len(families())} families. Click any entry to view its "
            f"structure, form, anomer, and glycosidic-bond annotation."
        ))

        # Top filter row.
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Family:"))
        self.family_combo = QComboBox()
        self.family_combo.addItem("(all)", "")
        for fam in families():
            self.family_combo.addItem(fam, fam)
        self.family_combo.currentIndexChanged.connect(self._populate_list)
        filter_row.addWidget(self.family_combo)
        filter_row.addSpacing(10)
        filter_row.addWidget(QLabel("Filter:"))
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("glucose, β, sucrose…")
        self.filter.textChanged.connect(self._populate_list)
        filter_row.addWidget(self.filter, 1)
        root.addLayout(filter_row)

        # Splitter: list on the left, details on the right.
        splitter = QSplitter(Qt.Horizontal)
        self.entry_list = QListWidget()
        self.entry_list.currentItemChanged.connect(self._on_selection)
        splitter.addWidget(self.entry_list)

        right = QFrame()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(6, 6, 6, 6)

        self.svg = QSvgWidget()
        self.svg.setMinimumSize(360, 300)
        right_lay.addWidget(self.svg)

        self.meta = QTextBrowser()
        self.meta.setOpenExternalLinks(False)
        self.meta.setMaximumHeight(160)
        right_lay.addWidget(self.meta, 1)

        row = QHBoxLayout()
        self.copy_btn = QPushButton("Copy SMILES")
        self.copy_btn.clicked.connect(self._on_copy_smiles)
        row.addWidget(self.copy_btn)
        self.show_in_workspace_btn = QPushButton("Show in Molecule Workspace")
        self.show_in_workspace_btn.clicked.connect(
            self._on_show_in_workspace)
        row.addWidget(self.show_in_workspace_btn)
        row.addStretch(1)
        right_lay.addLayout(row)

        splitter.addWidget(right)
        splitter.setStretchFactor(1, 2)
        root.addWidget(splitter, 1)

    # -----------------------------------------------------------------

    def _filtered_entries(self) -> List[Carbohydrate]:
        fam = self.family_combo.currentData() or ""
        needle = self.filter.text().strip().lower()
        out: List[Carbohydrate] = []
        for c in CARBOHYDRATES:
            if fam and c.family != fam:
                continue
            if needle:
                hay = " ".join((c.name, c.family, c.form, c.anomer,
                                c.glycosidic)).lower()
                if needle not in hay:
                    continue
            out.append(c)
        return out

    def _populate_list(self, *_) -> None:
        self.entry_list.clear()
        for c in self._filtered_entries():
            item = QListWidgetItem(
                f"{c.name}   —   {c.family}")
            item.setData(Qt.UserRole, c.name)
            self.entry_list.addItem(item)

    # -----------------------------------------------------------------

    def _current_entry(self) -> Optional[Carbohydrate]:
        item = self.entry_list.currentItem()
        if item is None:
            return None
        name = item.data(Qt.UserRole)
        return next((c for c in CARBOHYDRATES if c.name == name), None)

    def _on_selection(self, cur, _prev) -> None:
        c = self._current_entry()
        if c is None:
            self.meta.clear()
            return
        mol = Chem.MolFromSmiles(c.smiles)
        if mol is not None:
            self.svg.load(QByteArray(render_svg(mol).encode("utf-8")))
        parts = [
            f"<h2 style='margin:0'>{c.name}</h2>",
            f"<p><b>Family:</b> {c.family} · "
            f"<b>Form:</b> {c.form}</p>",
        ]
        if c.carbonyl_type:
            parts.append(f"<p><b>Carbonyl:</b> {c.carbonyl_type}</p>")
        if c.anomer:
            parts.append(f"<p><b>Anomer:</b> {c.anomer}</p>")
        if c.glycosidic:
            parts.append(f"<p><b>Glycosidic bond:</b> {c.glycosidic}</p>")
        if c.notes:
            parts.append(f"<p>{c.notes}</p>")
        parts.append(
            f"<p style='font-family:monospace; color:#444'>"
            f"{c.smiles}</p>"
        )
        self.meta.setHtml("".join(parts))

    def _on_copy_smiles(self) -> None:
        c = self._current_entry()
        if c is None:
            return
        QGuiApplication.clipboard().setText(c.smiles)
        bus().message_posted.emit(
            "INFO", f"Copied SMILES for {c.name} to clipboard")

    def _on_show_in_workspace(self) -> None:
        """Try to find a matching DB molecule by name / InChIKey and
        emit ``molecule_selected`` so the main workspace viewer picks
        it up. Falls back to a bus message if nothing matches."""
        c = self._current_entry()
        if c is None:
            return
        from orgchem.db.queries import find_molecule_by_name, list_molecules
        row = find_molecule_by_name(c.name)
        if row is None:
            # Try substring match.
            hits = list_molecules(query=c.name.split()[0], limit=1)
            row = hits[0] if hits else None
        if row is None:
            bus().message_posted.emit(
                "INFO",
                f"{c.name} isn't in the molecule DB yet — "
                f"use 'Copy SMILES' + File → Import SMILES…")
            return
        bus().molecule_selected.emit(int(row.id))
