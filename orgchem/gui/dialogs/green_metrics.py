"""Green-metrics dialog — Phase 25b final gap-closer (round 38).

Two tabs:

- **Reaction atom economy** — picks a reaction from the DB (by id /
  name search) and shows atom-economy numbers from
  :func:`orgchem.agent.actions_pathways.reaction_atom_economy`.
- **Pathway green metrics** — picks a synthesis pathway and shows
  per-step AE + overall AE.

Closes agent actions ``reaction_atom_economy`` and
``pathway_green_metrics``.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QDialogButtonBox,
    QMessageBox, QHeaderView, QTabWidget, QWidget, QListWidget,
    QListWidgetItem, QAbstractItemView,
)

log = logging.getLogger(__name__)


class GreenMetricsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Green metrics — atom economy")
        self.resize(760, 540)

        root = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._make_reaction_tab(), "Reaction AE")
        self.tabs.addTab(self._make_pathway_tab(), "Pathway AE")
        self.tabs.addTab(self._make_compare_tab(), "Compare pathways")
        root.addWidget(self.tabs, 1)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    # -----------------------------------------------------------------
    # Reaction AE tab

    def _make_reaction_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("Reaction:"))
        self.rxn_combo = QComboBox()
        self._populate_reactions()
        row.addWidget(self.rxn_combo, 1)
        go = QPushButton("Compute")
        go.setDefault(True)
        go.clicked.connect(self._on_reaction_run)
        row.addWidget(go)
        lay.addLayout(row)

        self.rxn_summary = QLabel("")
        self.rxn_summary.setStyleSheet(
            "padding:8px; background:#f4f6fb; border-radius:4px; "
            "font-size:13px;")
        self.rxn_summary.setWordWrap(True)
        lay.addWidget(self.rxn_summary)

        self.rxn_table = QTableWidget(0, 2)
        self.rxn_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.rxn_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.rxn_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.rxn_table, 1)

        if self.rxn_combo.count() > 0:
            self._on_reaction_run()
        return w

    def _populate_reactions(self) -> None:
        try:
            from orgchem.db.session import session_scope
            from orgchem.db.models import Reaction as DBRxn
            with session_scope() as s:
                for row in s.query(DBRxn).order_by(DBRxn.id).all():
                    self.rxn_combo.addItem(f"{row.id}: {row.name}", row.id)
        except Exception as e:  # noqa: BLE001
            log.warning("Could not populate reaction list: %s", e)

    def _on_reaction_run(self) -> None:
        rid = self.rxn_combo.currentData()
        if rid is None:
            return
        from orgchem.agent.actions_pathways import reaction_atom_economy
        r = reaction_atom_economy(reaction_id=int(rid))
        if "error" in r:
            QMessageBox.warning(self, "Green metrics", r["error"])
            return
        self.rxn_summary.setText(
            f"<b>{r.get('name', '?')}</b><br>"
            f"Reaction: <code>{r.get('reaction', '')}</code>"
        )
        self._populate_metrics_table(self.rxn_table, r)

    # -----------------------------------------------------------------
    # Pathway AE tab

    def _make_pathway_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("Pathway:"))
        self.path_combo = QComboBox()
        self._populate_pathways()
        row.addWidget(self.path_combo, 1)
        go = QPushButton("Compute")
        go.setDefault(True)
        go.clicked.connect(self._on_pathway_run)
        row.addWidget(go)
        lay.addLayout(row)

        self.path_summary = QLabel("")
        self.path_summary.setStyleSheet(
            "padding:8px; background:#f4f6fb; border-radius:4px; "
            "font-size:13px;")
        self.path_summary.setWordWrap(True)
        lay.addWidget(self.path_summary)

        self.path_table = QTableWidget(0, 4)
        self.path_table.setHorizontalHeaderLabels(
            ["Step", "Reaction", "AE (%)", "Notes"])
        self.path_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.path_table.setEditTriggers(QTableWidget.NoEditTriggers)
        lay.addWidget(self.path_table, 1)

        if self.path_combo.count() > 0:
            self._on_pathway_run()
        return w

    def _populate_pathways(self) -> None:
        try:
            from orgchem.db.session import session_scope
            from orgchem.db.models import SynthesisPathway
            with session_scope() as s:
                for p in s.query(SynthesisPathway).order_by(
                        SynthesisPathway.id).all():
                    self.path_combo.addItem(f"{p.id}: {p.name}", p.id)
        except Exception as e:  # noqa: BLE001
            log.warning("Could not populate pathway list: %s", e)

    def _on_pathway_run(self) -> None:
        pid = self.path_combo.currentData()
        if pid is None:
            return
        from orgchem.agent.actions_pathways import pathway_green_metrics
        r = pathway_green_metrics(pathway_id=int(pid))
        if "error" in r:
            QMessageBox.warning(self, "Green metrics", r["error"])
            return
        overall = r.get("overall", {})
        pct = overall.get("atom_economy_pct") or \
            overall.get("atom_economy", 0) * 100 if overall else 0
        self.path_summary.setText(
            f"<b>{r.get('name', '?')}</b><br>"
            f"Overall atom economy: <b>{pct:.1f} %</b> across "
            f"{len(r.get('per_step', []))} step(s)."
        )
        steps = r.get("per_step", [])
        self.path_table.setRowCount(len(steps))
        for i, st in enumerate(steps):
            ae_pct = st.get("atom_economy_pct") or \
                (st.get("atom_economy", 0) * 100)
            items = [
                QTableWidgetItem(str(st.get("step", i + 1))),
                QTableWidgetItem(st.get("reaction", "")),
                QTableWidgetItem(f"{ae_pct:.1f}"),
                QTableWidgetItem(st.get("notes", "") or ""),
            ]
            for c, it in enumerate(items):
                self.path_table.setItem(i, c, it)

    # -----------------------------------------------------------------

    def _populate_metrics_table(self, table: QTableWidget,
                                payload: dict) -> None:
        table.setRowCount(0)
        rows = []
        for k, v in payload.items():
            if k in ("name", "reaction", "id", "error", "per_step",
                     "overall"):
                continue
            if isinstance(v, float):
                rows.append((k, f"{v:.4f}"))
            else:
                rows.append((k, str(v)))
        table.setRowCount(len(rows))
        for i, (k, v) in enumerate(rows):
            table.setItem(i, 0, QTableWidgetItem(k))
            table.setItem(i, 1, QTableWidgetItem(v))

    # -----------------------------------------------------------------
    # Compare pathways tab (Phase 18a orphan — round 50)

    def _make_compare_tab(self) -> QWidget:
        w = QWidget()
        lay = QHBoxLayout(w)

        left = QVBoxLayout()
        left.addWidget(QLabel("Select 2+ pathways (Ctrl-click):"))
        self.cmp_list = QListWidget()
        self.cmp_list.setSelectionMode(
            QAbstractItemView.ExtendedSelection)
        try:
            from orgchem.db.session import session_scope
            from orgchem.db.models import SynthesisPathway
            with session_scope() as s:
                for p in s.query(SynthesisPathway).order_by(
                        SynthesisPathway.id).all():
                    it = QListWidgetItem(f"{p.id}: {p.name}")
                    it.setData(Qt.UserRole, p.id)
                    self.cmp_list.addItem(it)
        except Exception as e:  # noqa: BLE001
            log.warning("Could not list pathways for compare tab: %s", e)
        left.addWidget(self.cmp_list, 1)
        go = QPushButton("Compare")
        go.clicked.connect(self._on_compare_run)
        left.addWidget(go)
        lay.addLayout(left, 2)

        right = QVBoxLayout()
        self.cmp_summary = QLabel(
            "Pick two or more pathways, then press Compare.")
        self.cmp_summary.setStyleSheet(
            "padding:8px; background:#f4f6fb; border-radius:4px;")
        self.cmp_summary.setWordWrap(True)
        right.addWidget(self.cmp_summary)
        self.cmp_table = QTableWidget(0, 5)
        self.cmp_table.setHorizontalHeaderLabels(
            ["Rank", "Pathway", "Steps", "Overall AE (%)",
             "Worst step AE (%)"])
        self.cmp_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.cmp_table.setEditTriggers(QTableWidget.NoEditTriggers)
        right.addWidget(self.cmp_table, 1)
        lay.addLayout(right, 3)

        return w

    def _on_compare_run(self) -> None:
        selected = self.cmp_list.selectedItems()
        ids = [it.data(Qt.UserRole) for it in selected]
        if len(ids) < 2:
            QMessageBox.information(
                self, "Compare pathways",
                "Select at least two pathways before comparing.")
            return
        from orgchem.agent.actions_pathways import compare_pathways_green
        res = compare_pathways_green(pathway_ids=[int(i) for i in ids])
        if res.get("error"):
            QMessageBox.warning(self, "Compare pathways", res["error"])
            return
        ranked = res.get("ranking", [])
        best = res.get("best_overall_ae")
        self.cmp_summary.setText(
            f"<b>Compared {res.get('pathway_count', 0)} pathways.</b><br>"
            f"Best overall atom economy: "
            f"<b>{'—' if best is None else f'{best:.1f} %'}</b>"
        )
        self.cmp_table.setRowCount(len(ranked))
        for i, row in enumerate(ranked):
            items = [
                QTableWidgetItem(str(row["rank"])),
                QTableWidgetItem(row.get("name", "?")),
                QTableWidgetItem(str(row.get("n_steps", ""))),
                QTableWidgetItem(f"{row['overall_atom_economy']:.1f}"),
                QTableWidgetItem(
                    f"{row.get('min_step_atom_economy', 0):.1f}"),
            ]
            for c, it in enumerate(items):
                self.cmp_table.setItem(i, c, it)
