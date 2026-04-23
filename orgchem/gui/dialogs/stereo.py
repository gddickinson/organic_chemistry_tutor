"""Stereochemistry dialog — Phase 25b gap-closer (round 37).

Paste a SMILES → table of stereocentres with R/S / E/Z labels, click
any row to flip that centre, or click the global *Mirror (enantiomer)*
button. Closes agent actions ``flip_stereocentre`` and
``enantiomer_of``.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QDialogButtonBox,
    QMessageBox, QHeaderView,
)

from orgchem.core.stereo import (
    summarise, flip_stereocentre, enantiomer_of,
)

log = logging.getLogger(__name__)


class StereoDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Stereochemistry — CIP descriptors")
        self.resize(680, 480)

        root = QVBoxLayout(self)
        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self.smiles = QLineEdit("C[C@@H](O)C(=O)O")
        self.smiles.returnPressed.connect(self._on_analyse)
        row.addWidget(self.smiles, 1)
        go = QPushButton("Analyse")
        go.setDefault(True)
        go.clicked.connect(self._on_analyse)
        row.addWidget(go)
        mirror = QPushButton("Mirror (enantiomer)")
        mirror.clicked.connect(self._on_mirror)
        row.addWidget(mirror)
        root.addLayout(row)

        self.summary = QLabel("")
        self.summary.setStyleSheet(
            "padding:4px; background:#f4f6fb; border-radius:4px;")
        self.summary.setWordWrap(True)
        root.addWidget(self.summary)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Kind", "Atom / Bond", "Descriptor", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table, 1)

        self.result_out = QLabel("")
        self.result_out.setStyleSheet(
            "padding:8px; background:#edf6ed; border-radius:4px; "
            "font-family: monospace;")
        self.result_out.setWordWrap(True)
        root.addWidget(self.result_out)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

        self._on_analyse()

    # -----------------------------------------------------------------

    def _on_analyse(self) -> None:
        smi = self.smiles.text().strip()
        if not smi:
            return
        try:
            s = summarise(smi)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Stereo",
                                f"{type(e).__name__}: {e}")
            return
        # summarise() returns {"rs": {atom_idx: "R"|"S"}, "ez": [...],
        # "unassigned_stereocentres": [...], "n_stereocentres": N,
        # "is_chiral": bool}
        rs = s.get("rs", {}) or {}
        ez = s.get("ez", []) or []
        unassigned = s.get("unassigned_stereocentres", []) or []
        self.summary.setText(
            f"<b>{s.get('n_stereocentres', 0)}</b> stereocentre(s) · "
            f"{len(rs)} R/S assigned · "
            f"{len(ez)} E/Z assigned · "
            f"{len(unassigned)} unassigned · "
            f"chiral = {s.get('is_chiral', False)}"
        )

        rows = []
        for atom_idx, label in rs.items():
            rows.append(("R/S", str(atom_idx), label, atom_idx))
        for entry in ez:
            if isinstance(entry, dict):
                bond_idx = entry.get("bond_index") or entry.get("bond", "?")
                rows.append(("E/Z", str(bond_idx),
                             entry.get("label", ""), None))
            else:
                rows.append(("E/Z", "—", str(entry), None))

        self.table.setRowCount(len(rows))
        for i, (kind, idx_txt, label, flip_idx) in enumerate(rows):
            items = [
                QTableWidgetItem(kind),
                QTableWidgetItem(idx_txt),
                QTableWidgetItem(str(label)),
                QTableWidgetItem(""),
            ]
            for c, it in enumerate(items):
                self.table.setItem(i, c, it)
            if kind == "R/S" and flip_idx is not None:
                btn = QPushButton("Flip")
                btn.clicked.connect(
                    lambda _=False, a=int(flip_idx): self._flip(a))
                self.table.setCellWidget(i, 3, btn)
        self.result_out.setText(
            f"Input SMILES: <code>{smi}</code>"
        )

    def _flip(self, atom_idx: int) -> None:
        smi = self.smiles.text().strip()
        if not smi:
            return
        try:
            new = flip_stereocentre(smi, atom_idx)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Stereo", str(e))
            return
        self.result_out.setText(
            f"Flipped atom {atom_idx} → <code>{new}</code>")
        self.smiles.setText(new)
        self._on_analyse()

    def _on_mirror(self) -> None:
        smi = self.smiles.text().strip()
        if not smi:
            return
        try:
            new = enantiomer_of(smi)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Stereo", str(e))
            return
        self.result_out.setText(
            f"Mirrored → <code>{new}</code>")
        self.smiles.setText(new)
        self._on_analyse()
