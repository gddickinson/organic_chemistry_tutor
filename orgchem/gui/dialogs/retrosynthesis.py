"""Retrosynthesis dialog — Phase 25b gap-closer (round 33).

GUI wrapper around :func:`orgchem.core.retrosynthesis.find_retrosynthesis`
and :func:`orgchem.core.retrosynthesis.find_multi_step_retrosynthesis`.
User pastes a target SMILES, picks single-step vs multi-step, and
sees the proposed disconnections as a table (single-step) or a tree
of precursor paths (multi-step).

Closes the "retrosynthesis is agent-only" gap flagged by the Phase 25a
audit.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
    QDialogButtonBox, QMessageBox, QGroupBox, QHeaderView,
    QTabWidget, QTreeWidget, QTreeWidgetItem,
)

from orgchem.core.retrosynthesis import (
    find_retrosynthesis, find_multi_step_retrosynthesis,
)

log = logging.getLogger(__name__)


class RetrosynthesisDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Retrosynthesis — disconnections")
        self.resize(820, 560)

        root = QVBoxLayout(self)
        root.addWidget(QLabel(
            "Propose retrosynthetic disconnections for a target. "
            "Single-step runs each SMARTS retro template once; "
            "multi-step recurses on every precursor until each leaf is "
            "simple (≤ 8 heavy atoms, already in DB, or no template "
            "matches)."
        ))

        # ---- input form ---------------------------------------------
        form_box = QGroupBox("Target")
        form = QFormLayout(form_box)
        self.smiles = QLineEdit()
        self.smiles.setPlaceholderText("CC(=O)Oc1ccccc1C(=O)O")
        self.smiles.returnPressed.connect(self._on_single)
        form.addRow("Target SMILES:", self.smiles)

        self.max_depth = QSpinBox()
        self.max_depth.setRange(1, 5)
        self.max_depth.setValue(2)
        form.addRow("Max depth (multi-step):", self.max_depth)

        self.max_branches = QSpinBox()
        self.max_branches.setRange(1, 10)
        self.max_branches.setValue(3)
        form.addRow("Max branches per node:", self.max_branches)

        self.top_paths = QSpinBox()
        self.top_paths.setRange(1, 50)
        self.top_paths.setValue(10)
        form.addRow("Top-K linear paths:", self.top_paths)
        root.addWidget(form_box)

        # ---- run buttons --------------------------------------------
        btns = QHBoxLayout()
        go_single = QPushButton("Find single-step")
        go_single.clicked.connect(self._on_single)
        btns.addWidget(go_single)
        go_multi = QPushButton("Find multi-step")
        go_multi.clicked.connect(self._on_multi)
        go_multi.setDefault(True)
        btns.addWidget(go_multi)
        btns.addStretch(1)
        root.addLayout(btns)

        # ---- results ------------------------------------------------
        self.tabs = QTabWidget()
        self.single_table = QTableWidget(0, 3)
        self.single_table.setHorizontalHeaderLabels(
            ["Template", "Forward reaction", "Precursors"])
        self.single_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.single_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabs.addTab(self.single_table, "Single-step")

        self.multi_tree = QTreeWidget()
        self.multi_tree.setHeaderLabels(["Path / node", "Template"])
        self.tabs.addTab(self.multi_tree, "Multi-step")
        root.addWidget(self.tabs, 1)

        self.status = QLabel("")
        self.status.setStyleSheet("color:#555; font-size:12px;")
        root.addWidget(self.status)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

    # ------------------------------------------------------------------

    def _on_single(self) -> None:
        smi = self.smiles.text().strip()
        if not smi:
            return
        r = find_retrosynthesis(smi)
        if "error" in r:
            QMessageBox.warning(self, "Retrosynthesis", r["error"])
            return
        proposals = r.get("proposals", [])
        self.single_table.setRowCount(len(proposals))
        for row, p in enumerate(proposals):
            items = [
                QTableWidgetItem(p["template_id"]),
                QTableWidgetItem(p.get("forward_reaction", "")),
                QTableWidgetItem(" + ".join(p["precursors"])),
            ]
            for col, it in enumerate(items):
                self.single_table.setItem(row, col, it)
        self.status.setText(
            f"Single-step: {len(proposals)} disconnection(s) for "
            f"{r.get('canonical_target', smi)}"
        )
        self.tabs.setCurrentWidget(self.single_table)

    def _on_multi(self) -> None:
        smi = self.smiles.text().strip()
        if not smi:
            return
        r = find_multi_step_retrosynthesis(
            smi,
            max_depth=int(self.max_depth.value()),
            max_branches=int(self.max_branches.value()),
            top_paths=int(self.top_paths.value()),
        )
        if "error" in r:
            QMessageBox.warning(self, "Retrosynthesis", r["error"])
            return
        self._populate_tree(r)
        self.tabs.setCurrentWidget(self.multi_tree)
        n_paths = len(r.get("paths", []))
        self.status.setText(
            f"Multi-step (depth {r.get('max_depth')}): {n_paths} "
            f"linear path(s) flattened from the disconnection tree."
        )

    def _populate_tree(self, result) -> None:
        self.multi_tree.clear()
        tree = result.get("tree")
        if not isinstance(tree, dict):
            return
        root_item = self._add_node(None, tree)
        self.multi_tree.expandItem(root_item)

    def _add_node(self, parent, node) -> QTreeWidgetItem:
        label = node.get("smiles", "?")
        if node.get("terminal"):
            label += "  (terminal)"
        item = QTreeWidgetItem([label, ""])
        if parent is None:
            self.multi_tree.addTopLevelItem(item)
        else:
            parent.addChild(item)
        for branch in node.get("branches", []) or []:
            # Each branch: {"template_id", "precursors": [dict, ...]}
            template_id = branch.get("template_id", "")
            branch_item = QTreeWidgetItem(["via disconnection", template_id])
            item.addChild(branch_item)
            for pre in branch.get("precursors", []):
                if isinstance(pre, dict):
                    self._add_node(branch_item, pre)
                else:
                    branch_item.addChild(QTreeWidgetItem([str(pre), ""]))
        return item
