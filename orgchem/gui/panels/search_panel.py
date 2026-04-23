"""Left dock (tabbed): online search & download (PubChem today)."""
from __future__ import annotations
import json
import logging

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QComboBox, QMessageBox,
)

from orgchem.messaging.bus import bus
from orgchem.sources.pubchem import PubChemSource
from orgchem.db.session import session_scope
from orgchem.db.models import Molecule as DBMol
from orgchem.utils.threading import submit

log = logging.getLogger(__name__)

_SOURCES = {"PubChem": PubChemSource}


class SearchPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)

        top = QHBoxLayout()
        self.source_cb = QComboBox()
        self.source_cb.addItems(list(_SOURCES.keys()))
        self.query = QLineEdit()
        self.query.setPlaceholderText("e.g. aspirin")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._on_search)
        top.addWidget(QLabel("Source:"))
        top.addWidget(self.source_cb)
        top.addWidget(self.query, 1)
        top.addWidget(search_btn)
        lay.addLayout(top)

        self.results = QTableWidget(0, 3)
        self.results.setHorizontalHeaderLabels(["ID", "Name", "Formula"])
        self.results.horizontalHeader().setStretchLastSection(True)
        self.results.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.results, 1)

        add_btn = QPushButton("Download selected → database")
        add_btn.clicked.connect(self._on_download)
        lay.addWidget(add_btn)

    def _source(self):
        return _SOURCES[self.source_cb.currentText()]()

    def _on_search(self) -> None:
        q = self.query.text().strip()
        if not q:
            return
        src = self._source()
        log.info("Searching %s for %r", src.name, q)
        w = submit(src.search, q, 20)
        w.signals.result.connect(self._fill_results)
        w.signals.error.connect(lambda e: log.error("Search failed: %s", e[0]))

    def _fill_results(self, rows: list) -> None:
        self.results.setRowCount(len(rows))
        for i, r in enumerate(rows):
            self.results.setItem(i, 0, QTableWidgetItem(str(r.get("id", ""))))
            self.results.setItem(i, 1, QTableWidgetItem(str(r.get("name", ""))))
            self.results.setItem(i, 2, QTableWidgetItem(str(r.get("formula", ""))))
        log.info("Got %d results", len(rows))

    def _on_download(self) -> None:
        r = self.results.currentRow()
        if r < 0:
            return
        identifier = self.results.item(r, 0).text()
        src = self._source()
        log.info("Fetching %s id=%s", src.name, identifier)
        w = submit(src.fetch, identifier)
        w.signals.result.connect(self._on_fetched)
        w.signals.error.connect(lambda e: QMessageBox.warning(self, "Download failed", str(e[0])))

    def _on_fetched(self, m) -> None:
        with session_scope() as s:
            row = DBMol(
                name=m.name, smiles=m.smiles, inchi=m.inchi,
                inchikey=m.inchikey, formula=m.formula,
                molblock_3d=m.molblock_3d,
                properties_json=json.dumps(m.properties, default=str),
                source=m.source,
            )
            s.add(row)
            s.flush()
            new_id = row.id
        log.info("Added %s to database as id=%s", m.name, new_id)
        bus().database_changed.emit()
        bus().molecule_added.emit(int(new_id))
