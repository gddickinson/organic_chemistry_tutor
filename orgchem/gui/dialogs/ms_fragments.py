"""EI-MS fragmentation sketch dialog — Phase 4 follow-up.

GUI wrapper around :func:`orgchem.core.ms_fragments.predict_fragments`.
User pastes a SMILES; the dialog lists the molecular ion plus every
candidate neutral loss whose SMARTS precondition matches.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QDialogButtonBox, QMessageBox,
    QHeaderView,
)

from orgchem.core.ms_fragments import predict_fragments

log = logging.getLogger(__name__)


class MSFragmentsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("EI-MS fragmentation sketch")
        self.resize(640, 460)

        root = QVBoxLayout(self)
        root.addWidget(QLabel(
            "Teaching-grade EI-MS fragment predictor. Lists the "
            "molecular ion plus common neutral losses whose SMARTS "
            "precondition matches (M−15 CH₃, M−18 H₂O, M−28 CO, "
            "M−43 acetyl, etc.)."
        ))

        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self.smiles = QLineEdit()
        self.smiles.setPlaceholderText("CC(=O)Oc1ccccc1C(=O)O")
        self.smiles.returnPressed.connect(self._on_run)
        row.addWidget(self.smiles, 1)
        go = QPushButton("Predict fragments")
        go.setDefault(True)
        go.clicked.connect(self._on_run)
        row.addWidget(go)
        root.addLayout(row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["m/z", "Δ", "Label", "Mechanism"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table, 1)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    def _on_run(self) -> None:
        smi = self.smiles.text().strip()
        if not smi:
            return
        try:
            report = predict_fragments(smi)
        except ValueError as e:
            QMessageBox.warning(self, "EI-MS", str(e))
            return
        self.table.setRowCount(len(report.fragments))
        for row, f in enumerate(report.fragments):
            items = [
                QTableWidgetItem(f"{f.mz:.4f}"),
                QTableWidgetItem(f"{f.delta:.4f}"),
                QTableWidgetItem(f.label),
                QTableWidgetItem(f.mechanism),
            ]
            for col, it in enumerate(items):
                if col in (0, 1):
                    it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, col, it)
        log.info("EI-MS: %d fragments for %s", len(report.fragments), smi)
