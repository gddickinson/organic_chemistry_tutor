"""Lab techniques dialog — Phase 25b gap-closer (round 35).

Closes five agent-only actions:
``predict_tlc``, ``predict_rf``, ``recrystallisation_yield``,
``distillation_plan``, ``extraction_plan``.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QDoubleSpinBox, QComboBox, QCheckBox,
    QTableWidget, QTableWidgetItem, QDialogButtonBox, QMessageBox,
    QHeaderView, QTabWidget, QWidget, QPlainTextEdit,
)

from orgchem.core.chromatography import simulate_tlc, predict_rf
from orgchem.core.lab_techniques import (
    recrystallisation_yield, distillation_plan, extraction_plan,
)

log = logging.getLogger(__name__)


class LabTechniquesDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Lab techniques")
        self.resize(760, 560)

        root = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._make_tlc_tab(), "TLC / Rf")
        self.tabs.addTab(self._make_recryst_tab(), "Recrystallisation")
        self.tabs.addTab(self._make_distill_tab(), "Distillation")
        self.tabs.addTab(self._make_extract_tab(), "Acid-base extraction")
        root.addWidget(self.tabs, 1)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    # -----------------------------------------------------------------
    # TLC tab

    def _make_tlc_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel(
            "Paste one SMILES per line. Rf values are predicted from "
            "a solvent-polarity model — good enough for teaching."
        ))
        self.tlc_smiles = QPlainTextEdit()
        self.tlc_smiles.setPlaceholderText(
            "c1ccccc1\nCC(=O)O\nOc1ccccc1C(=O)O")
        self.tlc_smiles.setFixedHeight(110)
        lay.addWidget(self.tlc_smiles)

        row = QHBoxLayout()
        row.addWidget(QLabel("Solvent system:"))
        self.tlc_solvent = QLineEdit("hexane:ethyl_acetate:1:1")
        row.addWidget(self.tlc_solvent, 1)
        go = QPushButton("Simulate TLC")
        go.setDefault(True)
        go.clicked.connect(self._on_tlc_run)
        row.addWidget(go)
        lay.addLayout(row)

        self.tlc_table = QTableWidget(0, 3)
        self.tlc_table.setHorizontalHeaderLabels(
            ["SMILES", "Rf", "Migration"])
        self.tlc_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.tlc_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.tlc_table, 1)
        self.tlc_status = QLabel("")
        self.tlc_status.setStyleSheet("color:#555; font-size:12px;")
        lay.addWidget(self.tlc_status)
        return w

    def _on_tlc_run(self) -> None:
        smi = [s.strip() for s in
               self.tlc_smiles.toPlainText().splitlines() if s.strip()]
        if not smi:
            return
        solvent = self.tlc_solvent.text().strip() or "hexane:ethyl_acetate:1:1"
        r = simulate_tlc(smi, solvent=solvent)
        if "error" in r:
            QMessageBox.warning(self, "TLC", r["error"])
            return
        rows = r.get("compounds", [])
        self.tlc_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            rf = float(row.get("rf", 0))
            if rf < 0.15:
                interp = "too polar — stays at baseline"
            elif rf > 0.85:
                interp = "too non-polar — runs with solvent front"
            else:
                interp = f"logP {row.get('logp', 0):+.2f}"
            items = [
                QTableWidgetItem(row.get("smiles", "")),
                QTableWidgetItem(f"{rf:.2f}"),
                QTableWidgetItem(interp),
            ]
            for col, it in enumerate(items):
                self.tlc_table.setItem(i, col, it)
        polarity = r.get("solvent_polarity")
        if polarity is not None:
            self.tlc_status.setText(
                f"Solvent polarity index: {polarity:.2f} · "
                f"{len(rows)} compound(s)"
            )
        else:
            self.tlc_status.setText(f"{len(rows)} compound(s) analysed")

    # -----------------------------------------------------------------
    # Recrystallisation tab

    def _make_recryst_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        form = QFormLayout()
        self.rec_s_hot = _spin(40.0, 0.1, 500.0, 0.5)
        self.rec_s_cold = _spin(2.0, 0.01, 500.0, 0.5)
        self.rec_mass = _spin(5.0, 0.01, 500.0, 0.1)
        self.rec_vol = _spin(50.0, 1.0, 5000.0, 1.0)
        self.rec_purity = _spin(0.95, 0.0, 1.0, 0.01)
        form.addRow("Hot solubility (g/100 mL):", self.rec_s_hot)
        form.addRow("Cold solubility (g/100 mL):", self.rec_s_cold)
        form.addRow("Crude mass (g):", self.rec_mass)
        form.addRow("Solvent volume (mL):", self.rec_vol)
        form.addRow("Crude purity (0–1):", self.rec_purity)
        lay.addLayout(form)

        go = QPushButton("Compute")
        go.clicked.connect(self._on_recryst_run)
        lay.addWidget(go)
        self.rec_out = QLabel("")
        self.rec_out.setStyleSheet(
            "padding:10px; background:#f4f6fb; border-radius:4px; "
            "font-size:13px;")
        self.rec_out.setWordWrap(True)
        lay.addWidget(self.rec_out)
        lay.addStretch(1)
        return w

    def _on_recryst_run(self) -> None:
        r = recrystallisation_yield(
            s_hot=self.rec_s_hot.value(),
            s_cold=self.rec_s_cold.value(),
            m_crude_g=self.rec_mass.value(),
            solvent_volume_ml=self.rec_vol.value(),
            purity_hot=self.rec_purity.value(),
        )
        if "error" in r:
            self.rec_out.setText(f"<span style='color:#b32d2d'><b>Error:</b> "
                                 f"{r['error']}</span>")
            return
        self.rec_out.setText(
            f"<b>Crystals recovered:</b> {r['crystals_g']:.2f} g "
            f"({r['yield_pct']:.1f} % of crude)<br>"
            f"<b>Retained in mother liquor:</b> "
            f"{r['retained_g']:.2f} g<br>"
            f"<b>Dissolved hot:</b> "
            f"{r.get('dissolved_hot_g', 0):.2f} g"
        )

    # -----------------------------------------------------------------
    # Distillation tab

    def _make_distill_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel(
            "Pick two liquids from the built-in b.p. table; the dialog "
            "picks simple / fractional / azeotrope based on ΔTb."
        ))
        row = QHBoxLayout()
        self.dist_a = QLineEdit("ethanol")
        self.dist_b = QLineEdit("water")
        row.addWidget(QLabel("Component A:"))
        row.addWidget(self.dist_a)
        row.addWidget(QLabel("Component B:"))
        row.addWidget(self.dist_b)
        go = QPushButton("Plan")
        go.clicked.connect(self._on_distill_run)
        row.addWidget(go)
        lay.addLayout(row)
        self.dist_out = QLabel("")
        self.dist_out.setStyleSheet(
            "padding:10px; background:#f4f6fb; border-radius:4px; "
            "font-size:13px;")
        self.dist_out.setWordWrap(True)
        lay.addWidget(self.dist_out)
        lay.addStretch(1)
        return w

    def _on_distill_run(self) -> None:
        r = distillation_plan((self.dist_a.text().strip(),
                               self.dist_b.text().strip()))
        if "error" in r:
            self.dist_out.setText(
                f"<span style='color:#b32d2d'><b>Error:</b> "
                f"{r['error']}</span>")
            return
        self.dist_out.setText(
            f"<b>Lower-bp component:</b> {r['lower_bp_component']} "
            f"({r['lower_bp_c']:.1f} °C)<br>"
            f"<b>Higher-bp component:</b> {r['higher_bp_component']} "
            f"({r['higher_bp_c']:.1f} °C)<br>"
            f"<b>ΔTb:</b> {r['delta_c']:.1f} °C<br>"
            f"<b>Technique:</b> {r['technique']}<br>"
            f"<b>Rationale:</b> {r['rationale']}"
        )

    # -----------------------------------------------------------------
    # Extraction tab

    def _make_extract_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel(
            "Henderson-Hasselbalch: predict where a solute partitions "
            "in a two-phase aqueous / organic extraction."
        ))
        form = QFormLayout()
        self.ext_pka = _spin(4.8, -5.0, 20.0, 0.1)
        form.addRow("pKa:", self.ext_pka)
        self.ext_ph = _spin(7.0, 0.0, 14.0, 0.1)
        form.addRow("pH of aqueous phase:", self.ext_ph)
        self.ext_is_acid = QCheckBox("Solute is an acid "
                                     "(unchecked → base)")
        self.ext_is_acid.setChecked(True)
        form.addRow("", self.ext_is_acid)
        self.ext_logp = QDoubleSpinBox()
        self.ext_logp.setRange(-5.0, 10.0)
        self.ext_logp.setValue(2.0)
        self.ext_logp.setSingleStep(0.1)
        form.addRow("logP (neutral form):", self.ext_logp)
        lay.addLayout(form)

        go = QPushButton("Predict partition")
        go.clicked.connect(self._on_extract_run)
        lay.addWidget(go)
        self.ext_out = QLabel("")
        self.ext_out.setStyleSheet(
            "padding:10px; background:#f4f6fb; border-radius:4px; "
            "font-size:13px;")
        self.ext_out.setWordWrap(True)
        lay.addWidget(self.ext_out)
        lay.addStretch(1)
        return w

    def _on_extract_run(self) -> None:
        r = extraction_plan(
            pka=self.ext_pka.value(),
            ph=self.ext_ph.value(),
            is_acid=self.ext_is_acid.isChecked(),
            logp_neutral=self.ext_logp.value(),
        )
        if "error" in r:
            self.ext_out.setText(
                f"<span style='color:#b32d2d'><b>Error:</b> "
                f"{r['error']}</span>")
            return
        dest = r.get("destination", "?")
        colour = "#2d8a3e" if dest == "organic" else "#1b5aa3"
        self.ext_out.setText(
            f"<b>Fraction ionised:</b> "
            f"{r.get('fraction_ionised', 0):.3f}<br>"
            f"<b>Fraction neutral:</b> "
            f"{r.get('fraction_neutral', 0):.3f}<br>"
            f"<b>Predicted layer:</b> "
            f"<span style='color:{colour}; font-weight:bold'>"
            f"{dest}</span><br>"
            f"<b>Tip:</b> {r.get('tip', '')}"
        )


def _spin(default: float, lo: float, hi: float, step: float) -> QDoubleSpinBox:
    sp = QDoubleSpinBox()
    sp.setRange(lo, hi)
    sp.setSingleStep(step)
    sp.setValue(default)
    sp.setDecimals(3 if step < 0.1 else 2)
    return sp
