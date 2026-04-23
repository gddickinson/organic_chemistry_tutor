"""Right dock: molecular property table for the selected molecule."""
from __future__ import annotations
import json
import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

from orgchem.messaging.bus import bus
from orgchem.db.queries import get_molecule
from orgchem.core.descriptors import compute_all
from orgchem.core.formats import mol_from_smiles

log = logging.getLogger(__name__)


class PropertiesPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Property", "Value"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.table)
        bus().molecule_selected.connect(self._on_mol)

    def _on_mol(self, mol_id: int) -> None:
        row = get_molecule(int(mol_id))
        if row is None:
            return
        props: dict = {}
        if row.properties_json:
            try:
                props.update(json.loads(row.properties_json))
            except Exception:
                pass
        try:
            props.update(compute_all(mol_from_smiles(row.smiles)))
        except Exception as e:
            log.warning("Descriptor calc failed: %s", e)

        meta = [
            ("Name", row.name),
            ("Formula", row.formula or ""),
            ("SMILES", row.smiles),
            ("InChIKey", row.inchikey or ""),
            ("Source", row.source or ""),
        ]
        rows = meta + [(k, _fmt(v)) for k, v in sorted(props.items())]
        self.table.setRowCount(len(rows))
        for i, (k, v) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.table.setItem(i, 1, QTableWidgetItem(str(v)))


def _fmt(v) -> str:
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v)
