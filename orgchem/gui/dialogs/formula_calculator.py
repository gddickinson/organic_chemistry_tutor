"""Empirical / molecular formula calculator — GUI wrapper for ``core/formula.py``.

Implements (and extends) the approach from Verma et al. 2024
(*Rasayan J. Chem.* 17:1460–1472, `refs/4325_pdf.pdf`)."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QDialogButtonBox, QMessageBox, QComboBox,
)

from orgchem.core.formula import (
    compute_formula, ATOMIC_MASSES, ATOMIC_MASSES_INTEGER,
)


class FormulaCalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Empirical / Molecular Formula")
        self.resize(520, 450)
        lay = QVBoxLayout(self)

        lay.addWidget(QLabel(
            "Enter each element's mass percentage, then the compound's molar mass."
        ))

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Element", "Percentage (%)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        lay.addWidget(self.table)

        row_btns = QHBoxLayout()
        add = QPushButton("+ row")
        add.clicked.connect(lambda: self._add_row("", ""))
        rm = QPushButton("– row")
        rm.clicked.connect(self._rm_row)
        row_btns.addWidget(add); row_btns.addWidget(rm); row_btns.addStretch(1)
        lay.addLayout(row_btns)

        mass_row = QHBoxLayout()
        mass_row.addWidget(QLabel("Molar mass (g/mol):"))
        self.mass = QLineEdit()
        mass_row.addWidget(self.mass)
        mass_row.addSpacing(12)
        mass_row.addWidget(QLabel("Atomic masses:"))
        self.mass_table = QComboBox()
        self.mass_table.addItems(["IUPAC 2019 (default)", "Integer (Verma 2024)"])
        self.mass_table.setToolTip(
            "Integer masses reproduce Verma et al. 2024 Table 1 exactly; "
            "IUPAC masses are more accurate and work for the same cases."
        )
        mass_row.addWidget(self.mass_table)
        lay.addLayout(mass_row)

        self.result = QLabel()
        self.result.setStyleSheet("font-family: monospace; padding: 8px; background: #f4f4f4;")
        self.result.setWordWrap(True)
        self.result.setMinimumHeight(60)
        lay.addWidget(self.result)

        bb = QDialogButtonBox()
        calc = bb.addButton("Compute", QDialogButtonBox.AcceptRole)
        close = bb.addButton(QDialogButtonBox.Close)
        calc.clicked.connect(self._compute)
        close.clicked.connect(self.reject)
        lay.addWidget(bb)

        # Seed with the paper's nicotine example
        for sym, pct in [("C", "74.00"), ("H", "8.70"), ("N", "17.27")]:
            self._add_row(sym, pct)
        self.mass.setText("162")

    def _add_row(self, sym: str, pct: str) -> None:
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(sym))
        self.table.setItem(r, 1, QTableWidgetItem(pct))

    def _rm_row(self) -> None:
        r = self.table.currentRow()
        if r >= 0:
            self.table.removeRow(r)

    def _compute(self) -> None:
        pcts: dict = {}
        for r in range(self.table.rowCount()):
            sym_item = self.table.item(r, 0)
            pct_item = self.table.item(r, 1)
            if not sym_item or not pct_item:
                continue
            sym = sym_item.text().strip()
            try:
                pct = float(pct_item.text())
            except ValueError:
                continue
            if sym:
                pcts[sym] = pct
        try:
            mm = float(self.mass.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Molar mass must be a number.")
            return
        masses = ATOMIC_MASSES_INTEGER if "Integer" in self.mass_table.currentText() else ATOMIC_MASSES
        try:
            res = compute_formula(pcts, mm, masses=masses)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Cannot compute", str(e))
            return
        self.result.setText(
            f"Empirical:  {res.empirical_formula}   (mass {res.empirical_mass:.2f} g/mol)\n"
            f"Molecular:  {res.molecular_formula}   (GCD scale ×{res.scale_factor})\n"
            f"Max rounding residual: {res.max_residual:.3f} atoms"
            + (f" ({res.worst_element})" if res.worst_element else "")
        )
