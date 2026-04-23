"""IUPAC naming-rule browser — Phase 25b gap-closer (round 36).

Closes three agent-only actions: ``list_naming_rules``,
``get_naming_rule``, ``naming_rule_categories``.
"""
from __future__ import annotations
import logging
from html import escape

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QDialogButtonBox, QTextBrowser, QListWidget, QListWidgetItem,
    QWidget,
)

from orgchem.naming.rules import RULES, rule_categories

log = logging.getLogger(__name__)


class NamingRulesDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("IUPAC naming rules")
        self.resize(760, 540)

        root = QVBoxLayout(self)
        root.addWidget(QLabel(
            "Browse the IUPAC 2013 recommendations catalogue. "
            f"{len(RULES)} rules across {len(rule_categories())} "
            "categories."
        ))

        body = QHBoxLayout()
        left = QVBoxLayout()
        left.addWidget(QLabel("Category:"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItem("(all)", "")
        for cat in rule_categories():
            self.cat_combo.addItem(cat, cat)
        self.cat_combo.currentIndexChanged.connect(self._rebuild_list)
        left.addWidget(self.cat_combo)

        self.rule_list = QListWidget()
        self.rule_list.currentItemChanged.connect(self._on_selection)
        left.addWidget(self.rule_list, 1)
        body.addLayout(left, 2)

        self.body_browser = QTextBrowser()
        self.body_browser.setOpenExternalLinks(False)
        body.addWidget(self.body_browser, 3)
        root.addLayout(body, 1)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

        self._rebuild_list()

    def _rebuild_list(self) -> None:
        selected_cat = self.cat_combo.currentData() or ""
        self.rule_list.clear()
        for r in RULES:
            if selected_cat and r.category != selected_cat:
                continue
            item = QListWidgetItem(f"{r.id}  —  {r.title}")
            item.setData(Qt.UserRole, r.id)
            self.rule_list.addItem(item)
        if self.rule_list.count() > 0:
            self.rule_list.setCurrentRow(0)

    def _on_selection(self, cur, _prev) -> None:
        if cur is None:
            self.body_browser.clear()
            return
        rule_id = cur.data(Qt.UserRole)
        rule = next((r for r in RULES if r.id == rule_id), None)
        if rule is None:
            return
        parts = [
            f"<h2>{escape(rule.title)}</h2>",
            f"<p><b>Category:</b> {escape(rule.category)} · "
            f"<b>ID:</b> <code>{escape(rule.id)}</code></p>",
            f"<p>{escape(rule.description_md)}</p>",
        ]
        if getattr(rule, "example_smiles", ""):
            parts.append(
                f"<p><b>Example SMILES:</b> "
                f"<code>{escape(rule.example_smiles)}</code></p>"
            )
        if getattr(rule, "example_iupac", ""):
            parts.append(
                f"<p><b>IUPAC name:</b> "
                f"<code>{escape(rule.example_iupac)}</code></p>"
            )
        if getattr(rule, "example_common", ""):
            parts.append(
                f"<p><b>Common name:</b> "
                f"<code>{escape(rule.example_common)}</code></p>"
            )
        if getattr(rule, "pitfalls", ""):
            parts.append(
                f"<p><b>Pitfalls:</b> {escape(rule.pitfalls)}</p>"
            )
        self.body_browser.setHtml("".join(parts))
