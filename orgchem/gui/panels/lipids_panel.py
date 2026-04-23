"""Lipids tab — Phase 29 (lipids sibling).

Mirrors the Phase 29b `CarbohydratesPanel` layout. The right pane
shows the 2D structure + lipid-specific metadata (chain length,
unsaturations, ω-designation, melting point, notes).
"""
from __future__ import annotations
import logging
from typing import List, Optional

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QGuiApplication
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QListWidget, QListWidgetItem, QPushButton, QSplitter, QFrame,
    QTextBrowser,
)

from rdkit import Chem

from orgchem.core.lipids import LIPIDS, Lipid, lipid_families
from orgchem.messaging.bus import bus
from orgchem.render.draw2d import render_svg

log = logging.getLogger(__name__)


class LipidsPanel(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._populate_list()
        if self.entry_list.count() > 0:
            self.entry_list.setCurrentRow(0)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)

        root.addWidget(QLabel(
            f"Seeded catalogue: {len(LIPIDS)} lipids across "
            f"{len(lipid_families())} families. Click any entry "
            f"to see its chain-length, unsaturations, "
            f"ω-designation, and melting point."
        ))

        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Family:"))
        self.family_combo = QComboBox()
        self.family_combo.addItem("(all)", "")
        for fam in lipid_families():
            self.family_combo.addItem(fam, fam)
        self.family_combo.currentIndexChanged.connect(self._populate_list)
        filter_row.addWidget(self.family_combo)
        filter_row.addSpacing(10)
        filter_row.addWidget(QLabel("Filter:"))
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("omega-3, stearic, phospholipid…")
        self.filter.textChanged.connect(self._populate_list)
        filter_row.addWidget(self.filter, 1)
        root.addLayout(filter_row)

        splitter = QSplitter(Qt.Horizontal)
        self.entry_list = QListWidget()
        self.entry_list.currentItemChanged.connect(self._on_selection)
        splitter.addWidget(self.entry_list)

        right = QFrame()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(6, 6, 6, 6)
        self.svg = QSvgWidget()
        self.svg.setMinimumSize(420, 260)
        right_lay.addWidget(self.svg)
        self.meta = QTextBrowser()
        self.meta.setOpenExternalLinks(False)
        self.meta.setMaximumHeight(180)
        right_lay.addWidget(self.meta, 1)

        row = QHBoxLayout()
        self.copy_btn = QPushButton("Copy SMILES")
        self.copy_btn.clicked.connect(self._on_copy_smiles)
        row.addWidget(self.copy_btn)
        self.show_btn = QPushButton("Show in Molecule Workspace")
        self.show_btn.clicked.connect(self._on_show_in_workspace)
        row.addWidget(self.show_btn)
        row.addStretch(1)
        right_lay.addLayout(row)
        splitter.addWidget(right)
        splitter.setStretchFactor(1, 2)
        root.addWidget(splitter, 1)

    def _filtered_entries(self) -> List[Lipid]:
        fam = self.family_combo.currentData() or ""
        needle = self.filter.text().strip().lower()
        out: List[Lipid] = []
        for l in LIPIDS:
            if fam and l.family != fam:
                continue
            if needle:
                hay = " ".join((l.name, l.family, l.omega_designation,
                                l.notes)).lower()
                if needle not in hay:
                    continue
            out.append(l)
        return out

    def _populate_list(self, *_) -> None:
        self.entry_list.clear()
        for l in self._filtered_entries():
            item = QListWidgetItem(f"{l.name}   —   {l.family}")
            item.setData(Qt.UserRole, l.name)
            self.entry_list.addItem(item)

    def _current_entry(self) -> Optional[Lipid]:
        item = self.entry_list.currentItem()
        if item is None:
            return None
        name = item.data(Qt.UserRole)
        return next((l for l in LIPIDS if l.name == name), None)

    def _on_selection(self, cur, _prev) -> None:
        l = self._current_entry()
        if l is None:
            self.meta.clear()
            return
        mol = Chem.MolFromSmiles(l.smiles)
        if mol is not None:
            self.svg.load(QByteArray(render_svg(mol).encode("utf-8")))
        bits = [f"<h2 style='margin:0'>{l.name}</h2>",
                f"<p><b>Family:</b> {l.family}"]
        if l.chain_length is not None:
            bits.append(f" · <b>Chain:</b> C{l.chain_length}")
        if l.unsaturations is not None:
            bits.append(f":{l.unsaturations}")
        if l.omega_designation:
            bits.append(f" ({l.omega_designation})")
        bits.append("</p>")
        if l.melting_point_c is not None:
            bits.append(f"<p><b>m.p.:</b> {l.melting_point_c:.1f} °C</p>")
        if l.notes:
            bits.append(f"<p>{l.notes}</p>")
        bits.append(f"<p style='font-family:monospace; color:#444'>"
                    f"{l.smiles}</p>")
        self.meta.setHtml("".join(bits))

    def _on_copy_smiles(self) -> None:
        l = self._current_entry()
        if l is None:
            return
        QGuiApplication.clipboard().setText(l.smiles)
        bus().message_posted.emit(
            "INFO", f"Copied SMILES for {l.name} to clipboard")

    def _on_show_in_workspace(self) -> None:
        l = self._current_entry()
        if l is None:
            return
        from orgchem.db.queries import find_molecule_by_name, list_molecules
        row = find_molecule_by_name(l.name)
        if row is None:
            # Fall back to the first word (e.g. "Palmitic").
            token = l.name.split()[0]
            hits = list_molecules(query=token, limit=1)
            row = hits[0] if hits else None
        if row is None:
            bus().message_posted.emit(
                "INFO",
                f"{l.name} isn't in the molecule DB yet — use "
                f"'Copy SMILES' + File → Import SMILES…")
            return
        bus().molecule_selected.emit(int(row.id))
