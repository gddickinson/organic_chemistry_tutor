"""Reusable SMILES input widget with live validation."""
from __future__ import annotations
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel

from rdkit import Chem

from orgchem.core.formats import mol_from_smiles
from orgchem.messaging.errors import InvalidSMILESError


class SmilesInput(QWidget):
    smiles_validated = Signal(str)   # emits canonical SMILES

    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Enter SMILES, e.g. c1ccccc1")
        self.edit.textChanged.connect(self._on_changed)
        self.status = QLabel("")
        lay.addWidget(self.edit)
        lay.addWidget(self.status)

    def _on_changed(self, text: str) -> None:
        text = text.strip()
        if not text:
            self.status.setText("")
            self.status.setStyleSheet("")
            return
        try:
            mol = mol_from_smiles(text)
        except InvalidSMILESError:
            self.status.setText("✗ invalid SMILES")
            self.status.setStyleSheet("color: #c03030;")
            return
        canonical = Chem.MolToSmiles(mol)
        self.status.setText(f"✓ {canonical}")
        self.status.setStyleSheet("color: #207020;")
        self.smiles_validated.emit(canonical)
