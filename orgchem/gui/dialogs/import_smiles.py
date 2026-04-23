"""Dialog: import a molecule from a SMILES string."""
from __future__ import annotations
import json
import logging

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QLabel, QDialogButtonBox, QMessageBox,
)

from orgchem.core.molecule import Molecule
from orgchem.db.session import session_scope
from orgchem.db.models import Molecule as DBMol
from orgchem.gui.widgets.smiles_input import SmilesInput
from orgchem.messaging.bus import bus

log = logging.getLogger(__name__)


class ImportSmilesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import SMILES")
        self.resize(480, 200)
        lay = QVBoxLayout(self)

        lay.addWidget(QLabel("Molecule name:"))
        self.name = QLineEdit()
        lay.addWidget(self.name)

        lay.addWidget(QLabel("SMILES:"))
        self.smiles = SmilesInput()
        lay.addWidget(self.smiles)

        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self._accept)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)

        self._canonical: str = ""
        self.smiles.smiles_validated.connect(self._on_validated)

    def _on_validated(self, canonical: str) -> None:
        self._canonical = canonical

    def _accept(self) -> None:
        if not self._canonical:
            QMessageBox.warning(self, "Invalid SMILES", "Enter a valid SMILES before importing.")
            return
        name = self.name.text().strip() or self._canonical
        try:
            m = Molecule.from_smiles(self._canonical, name=name)
            m.ensure_properties()
        except Exception as e:  # noqa: BLE001
            log.exception("Molecule build failed")
            QMessageBox.critical(self, "Import failed", str(e))
            return
        with session_scope() as s:
            row = DBMol(
                name=m.name, smiles=m.smiles, inchi=m.inchi, inchikey=m.inchikey,
                formula=m.formula, molblock_3d=m.molblock_3d,
                properties_json=json.dumps(m.properties, default=str),
                source="user-import",
            )
            s.add(row)
            s.flush()
            new_id = row.id
        log.info("Imported %s as id=%d", m.name, new_id)
        bus().database_changed.emit()
        bus().molecule_selected.emit(int(new_id))
        self.accept()
