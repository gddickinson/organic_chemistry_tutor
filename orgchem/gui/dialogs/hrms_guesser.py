"""HRMS formula-candidate guesser dialog — Phase 4 follow-up.

GUI wrapper around :func:`orgchem.core.hrms.guess_formula`. User enters
a measured monoisotopic mass + ppm tolerance + (optionally) elemental
bounds; the dialog lists ranked formula candidates with DBE and ppm
error.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QDialogButtonBox, QMessageBox, QGroupBox, QHeaderView,
)

from orgchem.core.hrms import DEFAULT_BOUNDS, guess_formula

log = logging.getLogger(__name__)


class HRMSGuesserDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("HRMS formula candidate guesser")
        self.resize(720, 520)

        root = QVBoxLayout(self)
        root.addWidget(QLabel(
            "Given a measured monoisotopic mass + ppm tolerance, "
            "enumerate plausible molecular formulas ranked by |ppm "
            "error|. Filtered by the nitrogen rule, integer DBE and "
            "Senior's rules."
        ))

        # ---- input form ----------------------------------------------
        form_box = QGroupBox("Measurement")
        form = QFormLayout(form_box)
        self.mass = QDoubleSpinBox()
        self.mass.setRange(1.0, 5000.0)
        self.mass.setDecimals(5)
        self.mass.setValue(151.06333)  # paracetamol M as a nice default
        form.addRow("Monoisotopic mass (Da):", self.mass)

        self.ppm = QDoubleSpinBox()
        self.ppm.setRange(0.1, 1000.0)
        self.ppm.setValue(5.0)
        self.ppm.setSingleStep(0.5)
        form.addRow("ppm tolerance:", self.ppm)

        self.top_k = QSpinBox()
        self.top_k.setRange(1, 100)
        self.top_k.setValue(15)
        form.addRow("Top-K candidates:", self.top_k)
        root.addWidget(form_box)

        # ---- elemental bounds ---------------------------------------
        bounds_box = QGroupBox("Elemental bounds (max count)")
        bounds = QFormLayout(bounds_box)
        self._bound_spins: dict[str, QSpinBox] = {}
        for elem in ("C", "H", "N", "O", "S", "P", "F", "Cl", "Br", "I"):
            sp = QSpinBox()
            sp.setRange(0, 300)
            sp.setValue(DEFAULT_BOUNDS[elem][1])
            bounds.addRow(f"max {elem}:", sp)
            self._bound_spins[elem] = sp
        root.addWidget(bounds_box)

        # ---- run button ----------------------------------------------
        btns = QHBoxLayout()
        go = QPushButton("Find candidates")
        go.setDefault(True)
        go.clicked.connect(self._on_run)
        btns.addWidget(go)
        btns.addStretch(1)
        root.addLayout(btns)

        # ---- results ------------------------------------------------
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Formula", "Theoretical mass", "ppm error", "DBE"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table, 1)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    # -------------------------- slots ----------------------------------

    def _on_run(self) -> None:
        bounds = {
            elem: (0, sp.value())
            for elem, sp in self._bound_spins.items()
        }
        try:
            hits = guess_formula(
                mass=float(self.mass.value()),
                ppm_tolerance=float(self.ppm.value()),
                top_k=int(self.top_k.value()),
                bounds=bounds,
            )
        except ValueError as e:
            QMessageBox.warning(self, "HRMS", str(e))
            return
        self.table.setRowCount(len(hits))
        for row, c in enumerate(hits):
            items = [
                QTableWidgetItem(c.formula),
                QTableWidgetItem(f"{c.theoretical_mass:.5f}"),
                QTableWidgetItem(f"{c.ppm_error:+.2f}"),
                QTableWidgetItem(f"{c.dbe:g}"),
            ]
            for col, it in enumerate(items):
                it.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, it)
        log.info("HRMS guesser: %d candidates for %.5f Da ± %.1f ppm",
                 len(hits), self.mass.value(), self.ppm.value())
