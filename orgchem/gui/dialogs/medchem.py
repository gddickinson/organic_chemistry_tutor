"""Medicinal-chemistry dialog — Phase 25b gap-closer (round 36).

Two tabs:

- **SAR series** — pick a seeded series (NSAIDs vs COX, statins vs
  HMG-CoA, …), view the variant table with descriptors + activity
  columns, and *Export SAR matrix…* to a PNG/SVG heat-map.
- **Bioisosteres** — paste a SMILES → ranked bioisosteric
  replacements from the `BIOISOSTERES` catalogue. Matching template
  rows link back to the catalogue description.

Closes five agent-only actions:
``list_sar_series``, ``get_sar_series``, ``export_sar_matrix``,
``list_bioisosteres``, ``suggest_bioisosteres``.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QDialogButtonBox, QMessageBox, QHeaderView, QTabWidget,
    QWidget, QFileDialog,
)

from orgchem.core.sar import SAR_LIBRARY
from orgchem.core.bioisosteres import (
    BIOISOSTERES, suggest_bioisosteres,
)
from orgchem.render.draw_sar import export_sar_matrix

log = logging.getLogger(__name__)


class MedChemDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Medicinal chemistry — SAR & Bioisosteres")
        self.resize(820, 560)

        root = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._make_sar_tab(), "SAR series")
        self.tabs.addTab(self._make_bioisostere_tab(), "Bioisosteres")
        root.addWidget(self.tabs, 1)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    # -----------------------------------------------------------------
    # SAR tab

    def _make_sar_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("Series:"))
        self.sar_combo = QComboBox()
        for s in SAR_LIBRARY:
            self.sar_combo.addItem(f"{s.id} — {s.name}", s.id)
        self.sar_combo.currentIndexChanged.connect(self._on_sar_pick)
        row.addWidget(self.sar_combo, 1)
        self.sar_export_btn = QPushButton("Export SAR matrix…")
        self.sar_export_btn.clicked.connect(self._on_sar_export)
        row.addWidget(self.sar_export_btn)
        lay.addLayout(row)

        self.sar_meta = QLabel("")
        self.sar_meta.setStyleSheet(
            "padding:4px; background:#f4f6fb; border-radius:4px;")
        self.sar_meta.setWordWrap(True)
        lay.addWidget(self.sar_meta)

        self.sar_table = QTableWidget(0, 0)
        self.sar_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.sar_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.sar_table, 1)

        if SAR_LIBRARY:
            self.sar_combo.setCurrentIndex(0)
            self._on_sar_pick(0)
        return w

    def _current_series(self):
        sid = self.sar_combo.currentData()
        return next((s for s in SAR_LIBRARY if s.id == sid), None)

    def _on_sar_pick(self, _idx) -> None:
        s = self._current_series()
        if s is None:
            return
        self.sar_meta.setText(
            f"<b>{s.name}</b> · target: {s.target} · "
            f"parent: <code>{s.parent_scaffold_smiles}</code> · "
            f"source: {s.source}"
        )
        rows = s.compute_descriptors()
        if not rows:
            self.sar_table.setRowCount(0)
            self.sar_table.setColumnCount(0)
            return
        headers = ["name", "r_group", "smiles", "mw", "logp", "tpsa",
                   "qed", "lipinski_violations"] + list(s.activity_columns)
        self.sar_table.setColumnCount(len(headers))
        self.sar_table.setHorizontalHeaderLabels(headers)
        self.sar_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, key in enumerate(headers):
                val = row.get(key, "")
                if isinstance(val, float):
                    txt = f"{val:.3f}"
                else:
                    txt = str(val) if val is not None else ""
                self.sar_table.setItem(r, c, QTableWidgetItem(txt))

    def _on_sar_export(self) -> None:
        s = self._current_series()
        if s is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save SAR matrix", f"{s.id}_matrix.png",
            "PNG image (*.png);;SVG image (*.svg)")
        if not path:
            return
        try:
            export_sar_matrix(s, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "SAR", f"Export failed: {e}")
            return
        QMessageBox.information(self, "SAR", f"Saved → {path}")

    # -----------------------------------------------------------------
    # Bioisosteres tab

    def _make_bioisostere_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self.bio_smiles = QLineEdit()
        self.bio_smiles.setPlaceholderText("CC(=O)Oc1ccccc1C(=O)O")
        self.bio_smiles.returnPressed.connect(self._on_bio_run)
        row.addWidget(self.bio_smiles, 1)
        go = QPushButton("Suggest")
        go.setDefault(True)
        go.clicked.connect(self._on_bio_run)
        row.addWidget(go)
        lay.addLayout(row)

        lay.addWidget(QLabel("Catalogue (click a row to see which "
                             "template it came from):"))
        self.bio_table = QTableWidget(0, 3)
        self.bio_table.setHorizontalHeaderLabels(
            ["Template", "Label", "Suggested SMILES"])
        self.bio_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.bio_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.bio_table, 1)

        self.bio_status = QLabel(
            f"{len(BIOISOSTERES)} templates in catalogue.")
        self.bio_status.setStyleSheet("color:#555; font-size:12px;")
        lay.addWidget(self.bio_status)
        return w

    def _on_bio_run(self) -> None:
        smi = self.bio_smiles.text().strip()
        if not smi:
            return
        r = suggest_bioisosteres(smi)
        if "error" in r:
            QMessageBox.warning(self, "Bioisosteres", r["error"])
            return
        variants = r.get("variants", [])
        self.bio_table.setRowCount(len(variants))
        for i, v in enumerate(variants):
            items = [
                QTableWidgetItem(v.get("template_id", "")),
                QTableWidgetItem(v.get("label", "")),
                QTableWidgetItem(v.get("smiles", "")),
            ]
            for col, it in enumerate(items):
                self.bio_table.setItem(i, col, it)
        self.bio_status.setText(
            f"{len(variants)} bioisosteric variants for "
            f"{r.get('target', smi)}"
        )
