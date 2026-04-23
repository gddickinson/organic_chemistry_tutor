"""Nucleic-acids tab — Phase 29 (NA sibling).

Same layout as the Carbohydrates / Lipids panels. Entries with a
SMILES render via `draw2d`; entries that are PDB motifs (B-form
DNA, tRNA, G-quadruplex) show a *Fetch in Proteins tab* shortcut
instead of a 2D structure.
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

from orgchem.core.nucleic_acids import (
    NUCLEIC_ACIDS, NucleicAcidEntry, nucleic_acid_families,
)
from orgchem.messaging.bus import bus
from orgchem.render.draw2d import render_svg

log = logging.getLogger(__name__)


class NucleicAcidsPanel(QWidget):
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
            f"Seeded catalogue: {len(NUCLEIC_ACIDS)} entries across "
            f"{len(nucleic_acid_families())} families — bases, "
            f"nucleosides, nucleotides, and canonical PDB motifs."
        ))

        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Family:"))
        self.family_combo = QComboBox()
        self.family_combo.addItem("(all)", "")
        for fam in nucleic_acid_families():
            self.family_combo.addItem(fam, fam)
        self.family_combo.currentIndexChanged.connect(self._populate_list)
        filter_row.addWidget(self.family_combo)
        filter_row.addSpacing(10)
        filter_row.addWidget(QLabel("Filter:"))
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("adenine, tRNA, quadruplex…")
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
        self.meta.setMaximumHeight(200)
        right_lay.addWidget(self.meta, 1)

        row = QHBoxLayout()
        self.copy_btn = QPushButton("Copy SMILES")
        self.copy_btn.clicked.connect(self._on_copy_smiles)
        row.addWidget(self.copy_btn)
        self.fetch_btn = QPushButton("Fetch PDB in Proteins tab")
        self.fetch_btn.clicked.connect(self._on_fetch_pdb)
        self.fetch_btn.setEnabled(False)
        row.addWidget(self.fetch_btn)
        row.addStretch(1)
        right_lay.addLayout(row)
        splitter.addWidget(right)
        splitter.setStretchFactor(1, 2)
        root.addWidget(splitter, 1)

    def _filtered_entries(self) -> List[NucleicAcidEntry]:
        fam = self.family_combo.currentData() or ""
        needle = self.filter.text().strip().lower()
        out: List[NucleicAcidEntry] = []
        for n in NUCLEIC_ACIDS:
            if fam and n.family != fam:
                continue
            if needle:
                hay = " ".join((n.name, n.family, n.strand,
                                n.role, n.pdb_id, n.notes)).lower()
                if needle not in hay:
                    continue
            out.append(n)
        return out

    def _populate_list(self, *_) -> None:
        self.entry_list.clear()
        for n in self._filtered_entries():
            label = f"{n.name}   —   {n.family}"
            if n.pdb_id:
                label += f"   [{n.pdb_id}]"
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, n.name)
            self.entry_list.addItem(item)

    def _current_entry(self) -> Optional[NucleicAcidEntry]:
        item = self.entry_list.currentItem()
        if item is None:
            return None
        name = item.data(Qt.UserRole)
        return next((n for n in NUCLEIC_ACIDS if n.name == name), None)

    def _on_selection(self, cur, _prev) -> None:
        n = self._current_entry()
        if n is None:
            self.meta.clear()
            return
        if n.smiles:
            mol = Chem.MolFromSmiles(n.smiles)
            if mol is not None:
                self.svg.load(QByteArray(render_svg(mol).encode("utf-8")))
        else:
            self.svg.load(QByteArray(b""))
        self.copy_btn.setEnabled(bool(n.smiles))
        self.fetch_btn.setEnabled(bool(n.pdb_id))
        parts = [
            f"<h2 style='margin:0'>{n.name}</h2>",
            f"<p><b>Family:</b> {n.family}",
        ]
        if n.strand:
            parts.append(f" · <b>Strand:</b> {n.strand}")
        if n.role:
            parts.append(f" · <b>Role:</b> {n.role}")
        if n.pdb_id:
            parts.append(f" · <b>PDB:</b> <code>{n.pdb_id}</code>")
        parts.append("</p>")
        if n.notes:
            parts.append(f"<p>{n.notes}</p>")
        if n.smiles:
            parts.append(f"<p style='font-family:monospace; color:#444'>"
                         f"{n.smiles}</p>")
        self.meta.setHtml("".join(parts))

    def _on_copy_smiles(self) -> None:
        n = self._current_entry()
        if n is None or not n.smiles:
            return
        QGuiApplication.clipboard().setText(n.smiles)
        bus().message_posted.emit(
            "INFO", f"Copied SMILES for {n.name} to clipboard")

    def _on_fetch_pdb(self) -> None:
        n = self._current_entry()
        if n is None or not n.pdb_id:
            return
        # Phase 30 — Proteins and Nucleic-acids now share the
        # Macromolecules secondary window. Ask the main window to
        # open/focus the Proteins inner tab, then populate + fetch.
        from orgchem.agent.controller import main_window
        win = main_window()
        if win is None or not hasattr(win, "proteins"):
            bus().message_posted.emit(
                "INFO", f"Proteins workspace unavailable — fetch "
                        f"{n.pdb_id} via the agent API instead.")
            return
        if hasattr(win, "open_macromolecules_window"):
            win.open_macromolecules_window(tab_label="Proteins")
        win.proteins.id_input.setText(n.pdb_id)
        win.proteins._on_fetch_pdb()
