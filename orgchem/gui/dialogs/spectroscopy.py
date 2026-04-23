"""Spectroscopy dialog — Phase 25b gap-closer (round 37).

Three tabs: IR bands, NMR shifts, MS isotope pattern. Each shows a
predicted peak table and a *Save spectrum…* button that exports a
schematic PNG/SVG via `render/draw_ir.py` / `draw_nmr.py` / `draw_ms.py`.

Closes five agent-only actions:
``predict_nmr_shifts``, ``predict_ms``,
``export_ir_spectrum``, ``export_nmr_spectrum``, ``export_ms_spectrum``.
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

from orgchem.core.spectroscopy import predict_bands
from orgchem.core.nmr import predict_shifts
from orgchem.core.ms import isotope_pattern, monoisotopic_mass
from orgchem.render.draw_ir import export_ir_spectrum
from orgchem.render.draw_nmr import export_nmr_spectrum
from orgchem.render.draw_ms import export_ms_spectrum

log = logging.getLogger(__name__)


class SpectroscopyDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Spectroscopy — IR / NMR / MS")
        self.resize(780, 560)
        root = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._make_ir_tab(), "IR")
        self.tabs.addTab(self._make_nmr_tab(), "NMR")
        self.tabs.addTab(self._make_ms_tab(), "MS")
        root.addWidget(self.tabs, 1)
        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    # -----------------------------------------------------------------
    # IR

    def _make_ir_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self.ir_smiles = QLineEdit("CC(=O)O")
        self.ir_smiles.returnPressed.connect(self._on_ir_run)
        row.addWidget(self.ir_smiles, 1)
        go = QPushButton("Predict bands")
        go.setDefault(True)
        go.clicked.connect(self._on_ir_run)
        row.addWidget(go)
        save = QPushButton("Save spectrum…")
        save.clicked.connect(self._on_ir_save)
        row.addWidget(save)
        lay.addLayout(row)

        self.ir_table = QTableWidget(0, 4)
        self.ir_table.setHorizontalHeaderLabels(
            ["Group", "ν (cm⁻¹)", "Intensity", "Notes"])
        self.ir_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.ir_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.ir_table, 1)
        return w

    def _on_ir_run(self) -> None:
        smi = self.ir_smiles.text().strip()
        if not smi:
            return
        r = predict_bands(smi)
        if "error" in r:
            QMessageBox.warning(self, "IR", r["error"])
            return
        bands = r.get("bands", [])
        self.ir_table.setRowCount(len(bands))
        for i, b in enumerate(bands):
            items = [
                QTableWidgetItem(b.get("group", "")),
                QTableWidgetItem(str(b.get("wavenumber", ""))),
                QTableWidgetItem(b.get("intensity", "")),
                QTableWidgetItem(b.get("notes", "")),
            ]
            for c, it in enumerate(items):
                self.ir_table.setItem(i, c, it)

    def _on_ir_save(self) -> None:
        smi = self.ir_smiles.text().strip()
        if not smi:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save IR spectrum", "ir_spectrum.png",
            "PNG image (*.png);;SVG image (*.svg)")
        if not path:
            return
        try:
            export_ir_spectrum(smi, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "IR", f"Save failed: {e}")
            return
        QMessageBox.information(self, "IR", f"Saved → {path}")

    # -----------------------------------------------------------------
    # NMR

    def _make_nmr_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self.nmr_smiles = QLineEdit("CC(=O)OCC")
        self.nmr_smiles.returnPressed.connect(self._on_nmr_run)
        row.addWidget(self.nmr_smiles, 1)
        row.addWidget(QLabel("Nucleus:"))
        self.nmr_nucleus = QComboBox()
        self.nmr_nucleus.addItems(["H", "C"])
        row.addWidget(self.nmr_nucleus)
        go = QPushButton("Predict shifts")
        go.setDefault(True)
        go.clicked.connect(self._on_nmr_run)
        row.addWidget(go)
        save = QPushButton("Save spectrum…")
        save.clicked.connect(self._on_nmr_save)
        row.addWidget(save)
        lay.addLayout(row)

        self.nmr_table = QTableWidget(0, 4)
        self.nmr_table.setHorizontalHeaderLabels(
            ["δ (ppm)", "Environment", "Multiplicity", "Count"])
        self.nmr_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.nmr_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.nmr_table, 1)
        return w

    def _on_nmr_run(self) -> None:
        smi = self.nmr_smiles.text().strip()
        if not smi:
            return
        r = predict_shifts(smi, nucleus=self.nmr_nucleus.currentText())
        if "error" in r:
            QMessageBox.warning(self, "NMR", r["error"])
            return
        peaks = r.get("peaks", [])
        self.nmr_table.setRowCount(len(peaks))
        for i, p in enumerate(peaks):
            items = [
                QTableWidgetItem(f"{p.get('shift', 0):.2f}"),
                QTableWidgetItem(p.get("environment", "")),
                QTableWidgetItem(p.get("multiplicity", "")),
                QTableWidgetItem(str(p.get("count", ""))),
            ]
            for c, it in enumerate(items):
                self.nmr_table.setItem(i, c, it)

    def _on_nmr_save(self) -> None:
        smi = self.nmr_smiles.text().strip()
        if not smi:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save NMR spectrum", "nmr_spectrum.png",
            "PNG image (*.png);;SVG image (*.svg)")
        if not path:
            return
        try:
            export_nmr_spectrum(smi, path,
                                nucleus=self.nmr_nucleus.currentText())
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "NMR", f"Save failed: {e}")
            return
        QMessageBox.information(self, "NMR", f"Saved → {path}")

    # -----------------------------------------------------------------
    # MS

    def _make_ms_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self.ms_smiles = QLineEdit("Clc1ccccc1")
        self.ms_smiles.returnPressed.connect(self._on_ms_run)
        row.addWidget(self.ms_smiles, 1)
        go = QPushButton("Predict isotope pattern")
        go.setDefault(True)
        go.clicked.connect(self._on_ms_run)
        row.addWidget(go)
        save = QPushButton("Save spectrum…")
        save.clicked.connect(self._on_ms_save)
        row.addWidget(save)
        lay.addLayout(row)

        self.ms_summary = QLabel("")
        self.ms_summary.setStyleSheet(
            "padding:4px; background:#f4f6fb; border-radius:4px;")
        lay.addWidget(self.ms_summary)

        self.ms_table = QTableWidget(0, 3)
        self.ms_table.setHorizontalHeaderLabels(
            ["m/z", "Rel. intensity", "Label"])
        self.ms_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.ms_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.ms_table, 1)
        return w

    def _on_ms_run(self) -> None:
        smi = self.ms_smiles.text().strip()
        if not smi:
            return
        try:
            result = isotope_pattern(smi)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "MS", f"{type(e).__name__}: {e}")
            return
        peaks = result.get("peaks", []) if isinstance(result, dict) else []
        if not peaks:
            QMessageBox.warning(self, "MS",
                                f"Could not compute isotope pattern "
                                f"for {smi!r}")
            return
        m_mono = result.get("monoisotopic_mass", 0.0)
        self.ms_summary.setText(
            f"Formula: <b>{result.get('formula', '?')}</b> · "
            f"monoisotopic mass: <b>{m_mono:.4f}</b> · "
            f"{len(peaks)} isotopologues shown.")
        self.ms_table.setRowCount(len(peaks))
        for i, p in enumerate(peaks):
            items = [
                QTableWidgetItem(f"{p.get('mz', 0):.4f}"),
                QTableWidgetItem(f"{100 * p.get('intensity', 0):.1f} %"),
                QTableWidgetItem(p.get("label", "")),
            ]
            for c, it in enumerate(items):
                self.ms_table.setItem(i, c, it)

    def _on_ms_save(self) -> None:
        smi = self.ms_smiles.text().strip()
        if not smi:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save MS spectrum", "ms_spectrum.png",
            "PNG image (*.png);;SVG image (*.svg)")
        if not path:
            return
        try:
            export_ms_spectrum(smi, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "MS", f"Save failed: {e}")
            return
        QMessageBox.information(self, "MS", f"Saved → {path}")
