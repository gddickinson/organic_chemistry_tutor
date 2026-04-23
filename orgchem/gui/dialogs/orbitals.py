"""Orbitals — Hückel MOs + Woodward-Hoffmann rule browser.

Phase 25b gap-closer (round 34): five actions that previously lived
only on the agent registry now have a dedicated Tools dialog —
``huckel_mos``, ``export_mo_diagram``, ``list_wh_rules``,
``get_wh_rule``, ``check_wh_allowed``.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QSpinBox, QTableWidget,
    QTableWidgetItem, QDialogButtonBox, QMessageBox, QHeaderView,
    QTabWidget, QTextBrowser, QFileDialog, QListWidget,
    QListWidgetItem, QWidget, QGroupBox,
)

from orgchem.core.huckel import huckel_for_smiles
from orgchem.core.wh_rules import RULES, check_allowed
from orgchem.render.draw_mo import export_mo_diagram

log = logging.getLogger(__name__)


class OrbitalsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Orbitals — Hückel MOs & Woodward-Hoffmann rules")
        self.resize(820, 580)

        root = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._make_huckel_tab(), "Hückel MOs")
        self.tabs.addTab(self._make_wh_tab(),     "Woodward-Hoffmann")
        self.tabs.addTab(self._make_predicate_tab(), "Is it allowed?")
        root.addWidget(self.tabs, 1)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    # -----------------------------------------------------------------
    # Hückel tab

    def _make_huckel_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel(
            "Enter a π-system SMILES; the solver returns the MO "
            "eigenvalues (α + k·β), occupancies, and HOMO/LUMO."
        ))
        row = QHBoxLayout()
        row.addWidget(QLabel("SMILES:"))
        self.huckel_smiles = QLineEdit()
        self.huckel_smiles.setPlaceholderText("c1ccccc1")
        self.huckel_smiles.returnPressed.connect(self._on_huckel_run)
        row.addWidget(self.huckel_smiles, 1)
        go = QPushButton("Compute MOs")
        go.setDefault(True)
        go.clicked.connect(self._on_huckel_run)
        row.addWidget(go)
        self.huckel_save = QPushButton("Save MO diagram…")
        self.huckel_save.clicked.connect(self._on_huckel_save)
        self.huckel_save.setEnabled(False)
        row.addWidget(self.huckel_save)
        lay.addLayout(row)

        self.huckel_summary = QLabel("")
        self.huckel_summary.setStyleSheet(
            "padding:4px; background:#f4f6fb; border-radius:4px;")
        lay.addWidget(self.huckel_summary)

        self.huckel_table = QTableWidget(0, 5)
        self.huckel_table.setHorizontalHeaderLabels(
            ["#", "Energy (α+kβ)", "k coefficient", "Occupancy",
             "Frontier"])
        self.huckel_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.huckel_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.huckel_table.currentCellChanged.connect(
            self._on_huckel_row_changed)
        lay.addWidget(self.huckel_table, 1)
        # Phase 14d — row selection reveals the `show_molecular_orbital`
        # detail: role (HOMO / LUMO / HOMO-n / LUMO+n), energy in β,
        # occupancy. Populated from the selected row.
        self.huckel_mo_detail = QLabel(
            "Select a row above for frontier details.")
        self.huckel_mo_detail.setStyleSheet(
            "padding:6px; background:#eef3ff; border-radius:4px; "
            "font-family:monospace;")
        self.huckel_mo_detail.setWordWrap(True)
        lay.addWidget(self.huckel_mo_detail)
        self._last_huckel = None
        self._last_huckel_smiles = ""
        return w

    def _on_huckel_run(self) -> None:
        smi = self.huckel_smiles.text().strip()
        if not smi:
            return
        try:
            result = huckel_for_smiles(smi)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Hückel", f"{type(e).__name__}: {e}")
            return
        if result is None or not getattr(result, "energies", None):
            QMessageBox.information(
                self, "Hückel",
                "No π-system detected. Try a conjugated SMILES "
                "(e.g. `c1ccccc1` or `C=CC=C`).")
            return
        self._last_huckel = result
        self._last_huckel_smiles = smi
        self._populate_huckel_table(result)
        self.huckel_save.setEnabled(True)
        homo = result.homo_index
        lumo = result.lumo_index
        self.huckel_summary.setText(
            f"n π-electrons: {result.n_pi_electrons} · "
            f"n MOs: {len(result.energies)} · "
            f"HOMO: MO {homo+1 if homo is not None else '—'} · "
            f"LUMO: MO {lumo+1 if lumo is not None else '—'}"
        )

    def _populate_huckel_table(self, result) -> None:
        self.huckel_table.setRowCount(len(result.energies))
        homo = result.homo_index
        lumo = result.lumo_index
        occupations = result.occupations
        for i, k in enumerate(result.energies):
            frontier = ""
            if i == homo:
                frontier = "HOMO"
            elif i == lumo:
                frontier = "LUMO"
            items = [
                QTableWidgetItem(str(i + 1)),
                QTableWidgetItem(f"α{k:+.4f}β"),
                QTableWidgetItem(f"{k:+.4f}"),
                QTableWidgetItem(str(occupations[i])),
                QTableWidgetItem(frontier),
            ]
            for col, it in enumerate(items):
                it.setTextAlignment(Qt.AlignCenter)
                self.huckel_table.setItem(i, col, it)

    def _on_huckel_row_changed(self, row: int, _col: int,
                               _prev_row: int, _prev_col: int) -> None:
        """Wire the `show_molecular_orbital` agent action to row
        selection (Phase 14d)."""
        if (row < 0 or self._last_huckel is None
                or not self._last_huckel_smiles):
            return
        try:
            from orgchem.agent.actions import invoke
            res = invoke("show_molecular_orbital",
                         smiles=self._last_huckel_smiles, index=row)
        except Exception:
            return
        if res.get("error"):
            self.huckel_mo_detail.setText(res["error"])
            return
        self.huckel_mo_detail.setText(
            f"MO #{res['index'] + 1}  ·  role = {res['role']}  ·  "
            f"energy = α{res['energy_beta']:+.4f}β  ·  "
            f"occupation = {res['occupation']}   "
            f"(HOMO = #{res['homo_index'] + 1} / "
            f"LUMO = #{res['lumo_index'] + 1}; "
            f"{res['n_pi_electrons']} π e⁻ across "
            f"{res['n_pi_atoms']} atoms)"
        )

    def _on_huckel_save(self) -> None:
        if self._last_huckel is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save MO diagram", "mo_diagram.png",
            "PNG image (*.png);;SVG image (*.svg)")
        if not path:
            return
        try:
            export_mo_diagram(self._last_huckel, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Hückel", f"Save failed: {e}")
            return
        QMessageBox.information(self, "Hückel", f"Saved → {path}")

    # -----------------------------------------------------------------
    # W-H browser tab

    def _make_wh_tab(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)

        left = QVBoxLayout()
        left.addWidget(QLabel("Family:"))
        self.wh_family = QComboBox()
        self.wh_family.addItem("(all)", "")
        for fam in sorted({r.family for r in RULES}):
            self.wh_family.addItem(fam, fam)
        self.wh_family.currentIndexChanged.connect(self._rebuild_wh_list)
        left.addWidget(self.wh_family)

        self.wh_list = QListWidget()
        self.wh_list.currentItemChanged.connect(self._on_wh_selection)
        left.addWidget(self.wh_list, 1)

        # Phase 14d / 14b follow-up — `explain_wh`: type a reaction
        # name and jump to the matching W-H rule.
        explain_row = QHBoxLayout()
        explain_row.addWidget(QLabel("For a reaction:"))
        self.wh_reaction_input = QLineEdit()
        self.wh_reaction_input.setPlaceholderText(
            "e.g. Diels-Alder, Claisen rearrangement, 1,5-H shift")
        explain_row.addWidget(self.wh_reaction_input, 1)
        self.wh_explain_btn = QPushButton("Explain")
        self.wh_explain_btn.clicked.connect(self._on_wh_explain)
        explain_row.addWidget(self.wh_explain_btn)
        left.addLayout(explain_row)

        lay.addLayout(left, 2)

        self.wh_body = QTextBrowser()
        self.wh_body.setOpenExternalLinks(False)
        lay.addWidget(self.wh_body, 3)

        self._rebuild_wh_list()
        return w

    def _rebuild_wh_list(self) -> None:
        selected = self.wh_family.currentData() or ""
        self.wh_list.clear()
        for r in RULES:
            if selected and r.family != selected:
                continue
            item = QListWidgetItem(f"{r.id}  —  {r.title}")
            item.setData(Qt.UserRole, r.id)
            self.wh_list.addItem(item)
        if self.wh_list.count() > 0:
            self.wh_list.setCurrentRow(0)

    def _on_wh_explain(self) -> None:
        """Phase 14d — `explain_wh`. Find the W-H rule that governs
        the user-typed reaction and select it in the list."""
        query = self.wh_reaction_input.text().strip()
        if not query:
            return
        try:
            from orgchem.agent.actions import invoke
            res = invoke("explain_wh", reaction_name_or_id=query)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Explain W-H", f"{e}")
            return
        if res.get("error"):
            QMessageBox.information(self, "Explain W-H", res["error"])
            return
        if not res.get("matched"):
            QMessageBox.information(
                self, "Explain W-H",
                res.get("note") or "No pericyclic rule matched.")
            return
        rule_id = res["rule_id"]
        # Make sure the family filter shows the rule, then select it.
        self.wh_family.setCurrentIndex(0)  # (all)
        self._rebuild_wh_list()
        for i in range(self.wh_list.count()):
            item = self.wh_list.item(i)
            if item.data(Qt.UserRole) == rule_id:
                self.wh_list.setCurrentRow(i)
                break

    def _on_wh_selection(self, cur, _prev) -> None:
        if cur is None:
            self.wh_body.clear()
            return
        rule_id = cur.data(Qt.UserRole)
        rule = next((r for r in RULES if r.id == rule_id), None)
        if rule is None:
            self.wh_body.clear()
            return
        from html import escape as _e
        parts = [
            f"<h2>{_e(rule.title)}</h2>",
            f"<p><b>Family:</b> {_e(rule.family)}<br>"
            f"<b>Regime:</b> {_e(rule.regime)}<br>"
            f"<b>Outcome:</b> {_e(rule.outcome)}</p>",
            f"<p>{_e(rule.description_md)}</p>",
        ]
        if rule.example:
            parts.append(f"<p><b>Example:</b> {_e(rule.example)}</p>")
        if rule.example_smiles:
            parts.append(f"<p><code>{_e(rule.example_smiles)}</code></p>")
        self.wh_body.setHtml("".join(parts))

    # -----------------------------------------------------------------
    # Allowed-predicate quick-check tab

    def _make_predicate_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel(
            "Quick-check a pericyclic step against the textbook "
            "allowed-ness rules."
        ))

        form = QFormLayout()
        self.pred_kind = QComboBox()
        self.pred_kind.addItems(["cycloaddition", "electrocyclic",
                                 "sigmatropic"])
        form.addRow("Kind:", self.pred_kind)
        self.pred_electrons = QSpinBox()
        self.pred_electrons.setRange(2, 20)
        self.pred_electrons.setValue(6)
        form.addRow("Electrons in TS:", self.pred_electrons)
        self.pred_regime = QComboBox()
        self.pred_regime.addItems(["thermal", "photochemical"])
        form.addRow("Regime:", self.pred_regime)
        lay.addLayout(form)

        go = QPushButton("Check")
        go.clicked.connect(self._on_predicate_run)
        lay.addWidget(go)

        self.pred_result = QLabel("")
        self.pred_result.setStyleSheet(
            "padding:10px; background:#f4f6fb; border-radius:4px; "
            "font-size:14px;")
        self.pred_result.setWordWrap(True)
        lay.addWidget(self.pred_result)
        lay.addStretch(1)
        return w

    def _on_predicate_run(self) -> None:
        r = check_allowed(
            kind=self.pred_kind.currentText(),
            electron_count=int(self.pred_electrons.value()),
            regime=self.pred_regime.currentText(),
        )
        if "error" in r:
            QMessageBox.warning(self, "Orbitals", r["error"])
            return
        ok = r.get("allowed", False)
        colour = "#2d8a3e" if ok else "#b32d2d"
        flag = "ALLOWED" if ok else "FORBIDDEN"
        self.pred_result.setText(
            f"<span style='color:{colour}; font-weight:bold'>"
            f"{flag}</span><br>"
            f"Geometry: {r.get('geometry', '?')}<br>"
            f"Reason: {r.get('reason', '')}"
        )
