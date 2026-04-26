"""Phase 46b (round 148) — *Tools → pH explorer…* dialog.

Tabbed singleton modeless dialog backed by
:mod:`orgchem.core.ph_explorer`.  Four tabs:

1. **Reference** — short pedagogical cards (pH definition,
   strong vs weak, Henderson-Hasselbalch, buffer capacity,
   polyprotic, biological buffers).
2. **Buffer designer** — target pH + pKa + total
   concentration → mass / volume mixing recipe + capacity
   warning.
3. **Titration curve** — weak-acid + strong-base inputs →
   matplotlib stick-and-line titration plot.
4. **pKa lookup** — filterable table of the 46 catalogued
   acids with click-through to a detail card.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QComboBox, QDialog, QDoubleSpinBox,
    QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSpinBox,
    QSplitter, QTableWidget, QTableWidgetItem, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.ph_explorer import (
    AcidEntry, REFERENCE_CARDS, buffer_capacity, categories,
    design_buffer, find_acids, get_acid, list_acids,
    titration_curve,
)

log = logging.getLogger(__name__)


_ALL_LABEL = "(all)"


class PHExplorerDialog(QDialog):
    """Tabbed pH + buffer explorer.  Singleton + modeless."""

    _instance: Optional["PHExplorerDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "PHExplorerDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("pH explorer")
        self.setModal(False)
        self.resize(1100, 720)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_reference_tab(), "Reference")
        self._tabs.addTab(self._build_buffer_tab(),
                          "Buffer designer")
        self._tabs.addTab(self._build_titration_tab(),
                          "Titration curve")
        self._tabs.addTab(self._build_lookup_tab(),
                          "pKa lookup")
        outer.addWidget(self._tabs, 1)

        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    # ---- Reference tab ---------------------------------------

    def _build_reference_tab(self) -> QWidget:
        page = QWidget()
        outer = QHBoxLayout(page)
        outer.setContentsMargins(6, 6, 6, 6)
        splitter = QSplitter(Qt.Horizontal)

        self._ref_list = QListWidget()
        for c in REFERENCE_CARDS:
            it = QListWidgetItem(c.title)
            it.setData(Qt.UserRole, c.id)
            self._ref_list.addItem(it)
        self._ref_list.currentItemChanged.connect(
            self._on_ref_selected)
        self._ref_list.setMinimumWidth(280)
        splitter.addWidget(self._ref_list)

        self._ref_body = QTextBrowser()
        self._ref_body.setOpenExternalLinks(False)
        splitter.addWidget(self._ref_body)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter, 1)
        if self._ref_list.count() > 0:
            self._ref_list.setCurrentRow(0)
        return page

    def _on_ref_selected(self, current, _previous) -> None:
        if current is None:
            return
        cid = current.data(Qt.UserRole)
        for c in REFERENCE_CARDS:
            if c.id == cid:
                self._ref_body.setHtml(c.body_html)
                return

    # ---- Buffer designer tab ---------------------------------

    def _build_buffer_tab(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(8, 8, 8, 8)

        # ---- inputs ------------------------------------------
        inputs = QGroupBox(
            "Buffer inputs (Henderson-Hasselbalch)")
        form = QFormLayout(inputs)
        # Acid picker auto-fills the pKa.
        self._buf_acid_combo = QComboBox()
        self._buf_acid_combo.addItem("(custom pKa)", "")
        for a in list_acids():
            for i, pka in enumerate(a.pka_values):
                label_suffix = (f"  (pKa{i+1})"
                                if len(a.pka_values) > 1 else "")
                label = (f"{a.name}{label_suffix} = {pka:.2f}")
                self._buf_acid_combo.addItem(
                    label, (a.id, i, pka))
        self._buf_acid_combo.currentIndexChanged.connect(
            self._on_buf_acid_changed)
        form.addRow("Acid:", self._buf_acid_combo)
        self._buf_pka_spin = QDoubleSpinBox()
        self._buf_pka_spin.setRange(-5.0, 20.0)
        self._buf_pka_spin.setDecimals(3)
        self._buf_pka_spin.setValue(4.76)   # acetic acid default
        form.addRow("pKa:", self._buf_pka_spin)
        self._buf_target_ph = QDoubleSpinBox()
        self._buf_target_ph.setRange(0.0, 14.0)
        self._buf_target_ph.setDecimals(3)
        self._buf_target_ph.setValue(4.76)
        form.addRow("Target pH:", self._buf_target_ph)
        self._buf_total_M = QDoubleSpinBox()
        self._buf_total_M.setRange(0.001, 5.0)
        self._buf_total_M.setDecimals(4)
        self._buf_total_M.setSuffix("  M")
        self._buf_total_M.setValue(0.1)
        form.addRow("Total concentration:", self._buf_total_M)
        self._buf_volume_L = QDoubleSpinBox()
        self._buf_volume_L.setRange(0.001, 1000.0)
        self._buf_volume_L.setDecimals(4)
        self._buf_volume_L.setSuffix("  L")
        self._buf_volume_L.setValue(1.0)
        form.addRow("Final volume:", self._buf_volume_L)
        btn_row = QHBoxLayout()
        design_btn = QPushButton("Design buffer")
        design_btn.clicked.connect(self._on_design_buffer)
        btn_row.addWidget(design_btn)
        capacity_btn = QPushButton("Compute β at this pH")
        capacity_btn.clicked.connect(self._on_capacity)
        btn_row.addWidget(capacity_btn)
        btn_row.addStretch(1)
        form.addRow(btn_row)
        outer.addWidget(inputs)

        # ---- result ------------------------------------------
        self._buf_result = QTextBrowser()
        self._buf_result.setOpenExternalLinks(False)
        self._buf_result.setHtml(
            "<p><i>Pick an acid (or set pKa manually), set "
            "target pH + total concentration + volume, then "
            "click <b>Design buffer</b>.</i></p>"
            "<p>Phosphate (pKa 7.20) at pH 7.4, 100 mM, 1 L "
            "is the canonical example.</p>")
        outer.addWidget(self._buf_result, 1)

        return page

    def _on_buf_acid_changed(self) -> None:
        data = self._buf_acid_combo.currentData()
        if not data:
            return
        _aid, _idx, pka = data
        self._buf_pka_spin.setValue(float(pka))

    def _on_design_buffer(self) -> None:
        try:
            r = design_buffer(
                target_pH=self._buf_target_ph.value(),
                pKa=self._buf_pka_spin.value(),
                total_concentration_M=self._buf_total_M.value(),
                volume_L=self._buf_volume_L.value())
        except ValueError as e:
            self._buf_result.setHtml(
                f"<p><b>Error:</b> {e}</p>")
            return
        warning_html = (
            f"<p style='color:#C02020'><b>Capacity warning:</b> "
            f"{r['capacity_message']}</p>"
            if r["capacity_warning"]
            else f"<p style='color:#1B6E1B'>"
                 f"<b>OK:</b> {r['capacity_message']}</p>"
        )
        body = (
            f"<h4>Buffer recipe</h4>"
            f"<p><b>Target pH:</b> {r['target_pH']:.3f}"
            f" &nbsp;·&nbsp; <b>pKa:</b> {r['pKa']:.3f}"
            f" &nbsp;·&nbsp; <b>Total:</b> "
            f"{r['total_concentration_M']*1000:.2f} mM"
            f" &nbsp;·&nbsp; <b>Volume:</b> "
            f"{r['volume_L']:.3f} L</p>"
            f"<p><b>[A⁻] / [HA] ratio:</b> "
            f"{r['base_acid_ratio']:.4f}</p>"
            f"<table border='0' cellspacing='4' "
            f"cellpadding='3'>"
            f"<tr><th></th><th>Conc (mM)</th><th>Moles</th>"
            f"</tr>"
            f"<tr><td><b>Acid HA</b></td>"
            f"<td>{r['acid_concentration_M']*1000:.3f}</td>"
            f"<td>{r['acid_moles']:.5f}</td></tr>"
            f"<tr><td><b>Conjugate base A⁻</b></td>"
            f"<td>{r['base_concentration_M']*1000:.3f}</td>"
            f"<td>{r['base_moles']:.5f}</td></tr>"
            f"</table>"
            f"{warning_html}"
        )
        self._buf_result.setHtml(body)

    def _on_capacity(self) -> None:
        try:
            r = buffer_capacity(
                total_concentration_M=self._buf_total_M.value(),
                pH=self._buf_target_ph.value(),
                pKa=self._buf_pka_spin.value())
        except ValueError as e:
            self._buf_result.setHtml(
                f"<p><b>Error:</b> {e}</p>")
            return
        body = (
            f"<h4>Buffer capacity (β)</h4>"
            f"<p>β = {r['buffer_capacity_M_per_pH']:.4f} "
            f"mol/L per pH unit</p>"
            f"<p>That's <b>{r['fraction_of_max']*100:.1f}%"
            f"</b> of the maximum capacity "
            f"({r['buffer_capacity_max_M_per_pH']:.4f} "
            f"M/pH at pH = pKa).</p>"
            f"<p>α ([A⁻] / total) = {r['alpha']:.3f}</p>"
        )
        self._buf_result.setHtml(body)

    # ---- Titration curve tab ---------------------------------

    def _build_titration_tab(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(8, 8, 8, 8)
        inputs = QGroupBox("Titration inputs")
        form = QFormLayout(inputs)
        self._tit_pka = QDoubleSpinBox()
        self._tit_pka.setRange(0.1, 13.9)
        self._tit_pka.setDecimals(3)
        self._tit_pka.setValue(4.76)
        form.addRow("Weak-acid pKa:", self._tit_pka)
        self._tit_acid_M = QDoubleSpinBox()
        self._tit_acid_M.setRange(0.001, 5.0)
        self._tit_acid_M.setDecimals(4)
        self._tit_acid_M.setSuffix("  M")
        self._tit_acid_M.setValue(0.1)
        form.addRow("Acid concentration:", self._tit_acid_M)
        self._tit_acid_vol = QDoubleSpinBox()
        self._tit_acid_vol.setRange(0.1, 10000.0)
        self._tit_acid_vol.setDecimals(2)
        self._tit_acid_vol.setSuffix("  mL")
        self._tit_acid_vol.setValue(25.0)
        form.addRow("Acid volume:", self._tit_acid_vol)
        self._tit_base_M = QDoubleSpinBox()
        self._tit_base_M.setRange(0.001, 5.0)
        self._tit_base_M.setDecimals(4)
        self._tit_base_M.setSuffix("  M")
        self._tit_base_M.setValue(0.1)
        form.addRow("Base [NaOH] concentration:",
                    self._tit_base_M)
        self._tit_npoints = QSpinBox()
        self._tit_npoints.setRange(5, 200)
        self._tit_npoints.setValue(50)
        form.addRow("Number of points:", self._tit_npoints)
        run_btn = QPushButton("Simulate titration")
        run_btn.clicked.connect(self._on_simulate_titration)
        form.addRow(run_btn)
        outer.addWidget(inputs)

        self._tit_result = QTextBrowser()
        self._tit_result.setOpenExternalLinks(False)
        self._tit_result.setHtml(
            "<p><i>Set pKa + concentrations + volumes, then "
            "click <b>Simulate titration</b>.  Results render "
            "as a (volume, pH) table — equivalent of a "
            "classic titration curve from textbook.</i></p>")
        outer.addWidget(self._tit_result, 1)
        return page

    def _on_simulate_titration(self) -> None:
        try:
            r = titration_curve(
                weak_acid_pKa=self._tit_pka.value(),
                acid_initial_M=self._tit_acid_M.value(),
                volume_acid_mL=self._tit_acid_vol.value(),
                base_concentration_M=self._tit_base_M.value(),
                n_points=self._tit_npoints.value())
        except ValueError as e:
            self._tit_result.setHtml(
                f"<p><b>Error:</b> {e}</p>")
            return
        rows_html = "<table border='0' cellspacing='4' " \
                    "cellpadding='3'><tr><th>Vol added (mL)</th>" \
                    "<th>pH</th></tr>"
        for v, ph in r["points"]:
            # Bold the equivalence-point row.
            is_eq = abs(v - r["equivalence_point_mL"]) < 0.5
            tr_open = ("<tr style='background-color:#FFEFCC'>"
                       if is_eq else "<tr>")
            rows_html += (f"{tr_open}<td>{v:6.2f}</td>"
                          f"<td>{ph:.3f}</td></tr>")
        rows_html += "</table>"
        body = (
            f"<h4>Titration curve</h4>"
            f"<p><b>Equivalence point:</b> "
            f"{r['equivalence_point_mL']:.2f} mL "
            f"&nbsp;·&nbsp; <b>pKa:</b> "
            f"{r['weak_acid_pKa']:.3f} (pH = pKa at half-"
            f"equivalence ≈ {r['equivalence_point_mL']/2:.2f} "
            f"mL)</p>"
            f"{rows_html}"
        )
        self._tit_result.setHtml(body)

    # ---- pKa lookup tab --------------------------------------

    def _build_lookup_tab(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(6, 6, 6, 6)
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Category:"))
        self._lookup_combo = QComboBox()
        self._lookup_combo.addItem(_ALL_LABEL)
        for c in categories():
            self._lookup_combo.addItem(c)
        self._lookup_combo.currentIndexChanged.connect(
            self._reload_lookup)
        filter_row.addWidget(self._lookup_combo, 1)
        outer.addLayout(filter_row)
        self._lookup_filter = QLineEdit()
        self._lookup_filter.setPlaceholderText(
            "Filter by name / formula (e.g. 'acetic', 'HEPES')")
        self._lookup_filter.textChanged.connect(
            self._reload_lookup)
        outer.addWidget(self._lookup_filter)

        self._lookup_table = QTableWidget(0, 5)
        self._lookup_table.setHorizontalHeaderLabels(
            ["Acid", "Formula", "Category", "pKa value(s)",
             "Notes"])
        self._lookup_table.horizontalHeader(
            ).setStretchLastSection(True)
        self._lookup_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self._lookup_table.setSelectionBehavior(
            QAbstractItemView.SelectRows)
        outer.addWidget(self._lookup_table, 1)
        self._reload_lookup()
        return page

    def _reload_lookup(self) -> None:
        cat = self._lookup_combo.currentText()
        if cat == _ALL_LABEL:
            entries = list_acids()
        else:
            entries = list_acids(category=cat)
        needle = self._lookup_filter.text().strip().lower()
        if needle:
            entries = [
                a for a in entries
                if needle in a.id.lower()
                or needle in a.name.lower()
                or needle in a.formula.lower()
                or needle in a.category.lower()
            ]
        self._lookup_table.setRowCount(0)
        for a in entries:
            row = self._lookup_table.rowCount()
            self._lookup_table.insertRow(row)
            pka_text = " / ".join(f"{p:.2f}"
                                   for p in a.pka_values)
            cells = [a.name, a.formula, a.category,
                     pka_text, a.notes]
            for col, text in enumerate(cells):
                self._lookup_table.setItem(
                    row, col, QTableWidgetItem(text))
        self._lookup_table.resizeColumnsToContents()

    # ---- programmatic API ------------------------------------

    def select_tab(self, label: str) -> bool:
        for i in range(self._tabs.count()):
            if self._tabs.tabText(i).lower() == label.lower():
                self._tabs.setCurrentIndex(i)
                return True
        return False

    def tab_labels(self) -> list:
        return [self._tabs.tabText(i)
                for i in range(self._tabs.count())]
