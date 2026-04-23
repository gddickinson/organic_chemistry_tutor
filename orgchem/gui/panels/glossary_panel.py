"""Glossary tab — searchable dictionary of organic-chemistry terms (Phase 11b).

Three controls: a filter box (substring search across term / aliases /
definition text), a category combo-box, and the result list. Selecting
an entry shows its markdown definition in the right pane, plus any
see-also cross-references as clickable buttons that jump to the related
term.
"""
from __future__ import annotations
import json
import logging
from typing import List, Optional

from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QListView, QLineEdit,
    QLabel, QComboBox, QTextBrowser, QPushButton,
)

from orgchem.db.session import session_scope
from orgchem.db.models import GlossaryTerm
from sqlalchemy import select, or_

log = logging.getLogger(__name__)


class _TermListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._rows: list = []

    def reload(self, query: str = "", category: str = "") -> None:
        self.beginResetModel()
        with session_scope() as s:
            stmt = select(GlossaryTerm).order_by(GlossaryTerm.term)
            if category and category != "All":
                stmt = stmt.where(GlossaryTerm.category == category)
            if query:
                pat = f"%{query.strip()}%"
                stmt = stmt.where(or_(
                    GlossaryTerm.term.ilike(pat),
                    GlossaryTerm.definition_md.ilike(pat),
                    GlossaryTerm.aliases_json.ilike(pat),
                ))
            self._rows = list(s.scalars(stmt).all())
            # detach from session for display use
            for r in self._rows:
                s.expunge(r)
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._rows)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        if role == Qt.DisplayRole:
            return f"{row.term}    [{row.category or ''}]"
        if role == Qt.UserRole:
            return row.id
        if role == Qt.ToolTipRole:
            try:
                aliases = json.loads(row.aliases_json) if row.aliases_json else []
            except Exception:
                aliases = []
            return "aliases: " + ", ".join(aliases) if aliases else ""
        return None


class GlossaryPanel(QWidget):
    """Dictionary tab — filter + list + markdown viewer."""

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._populate_categories()
        self._reload()

    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # Left: filter + category + list
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(2, 2, 2, 2)

        top = QHBoxLayout()
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter…")
        self.filter.textChanged.connect(self._on_filter_changed)
        top.addWidget(QLabel("Search:"))
        top.addWidget(self.filter, 1)
        lv.addLayout(top)

        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        self.category = QComboBox()
        self.category.currentTextChanged.connect(self._on_filter_changed)
        cat_row.addWidget(self.category, 1)
        lv.addLayout(cat_row)

        self.model = _TermListModel()
        self.view = QListView()
        self.view.setModel(self.model)
        self.view.clicked.connect(self._on_clicked)
        lv.addWidget(self.view, 1)

        left.setMaximumWidth(420)
        splitter.addWidget(left)

        # Right: markdown definition
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(6, 6, 6, 6)

        self.title = QLabel("Pick a term from the list")
        self.title.setStyleSheet(
            "font-size: 15pt; font-weight: bold; padding: 4px;")
        rv.addWidget(self.title)

        self.aliases = QLabel("")
        self.aliases.setStyleSheet("color:#888; font-style:italic; padding: 2px;")
        self.aliases.setWordWrap(True)
        rv.addWidget(self.aliases)

        self.body = QTextBrowser()
        self.body.setOpenExternalLinks(False)
        self.body.setStyleSheet(
            "QTextBrowser { font-size: 11pt; padding: 8px; }")
        rv.addWidget(self.body, 1)

        self.see_also_row = QHBoxLayout()
        rv.addLayout(self.see_also_row)

        # "View figure" row — closes Phase 25b `get_glossary_figure`
        # audit gap. Only enabled when the current term has an
        # `example_smiles` to render from.
        self.figure_row = QHBoxLayout()
        self.view_figure_btn = QPushButton("View figure")
        self.view_figure_btn.setEnabled(False)
        self.view_figure_btn.clicked.connect(self._on_view_figure)
        self.figure_row.addWidget(self.view_figure_btn)
        self.figure_row.addStretch(1)
        rv.addLayout(self.figure_row)
        self._current_term_smiles = ""
        self._current_term_name = ""

        splitter.addWidget(right)
        splitter.setStretchFactor(1, 1)
        lay.addWidget(splitter)

    # ------------------------------------------------------------------

    def _populate_categories(self) -> None:
        """Scan the DB once to populate the category combo."""
        with session_scope() as s:
            cats = {row[0] for row in s.query(GlossaryTerm.category).distinct().all()
                    if row[0]}
        self.category.blockSignals(True)
        self.category.clear()
        self.category.addItem("All")
        for c in sorted(cats):
            self.category.addItem(c)
        self.category.blockSignals(False)

    def _reload(self) -> None:
        self.model.reload(self.filter.text().strip(),
                          self.category.currentText())

    def _on_filter_changed(self, *_):
        self._reload()

    def _on_clicked(self, idx) -> None:
        term_id = self.model.data(idx, Qt.UserRole)
        if term_id is None:
            return
        self._display(int(term_id))

    def _display(self, term_id: int) -> None:
        with session_scope() as s:
            row = s.get(GlossaryTerm, term_id)
            if row is None:
                return
            term = row.term
            category = row.category or ""
            md = row.definition_md
            try:
                aliases = json.loads(row.aliases_json) if row.aliases_json else []
            except Exception:
                aliases = []
            try:
                see_also = json.loads(row.see_also_json) if row.see_also_json else []
            except Exception:
                see_also = []
            example_smiles = row.example_smiles or ""
        self._current_term_name = term
        self._current_term_smiles = example_smiles
        self.view_figure_btn.setEnabled(bool(example_smiles))
        self.title.setText(f"{term}   —   {category}" if category else term)
        self.aliases.setText("Aliases: " + ", ".join(aliases)
                             if aliases else "")
        self.body.setMarkdown(md)

        # replace the "see also" buttons
        while self.see_also_row.count():
            item = self.see_also_row.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        if see_also:
            self.see_also_row.addWidget(QLabel("See also:"))
            for related in see_also:
                btn = QPushButton(related)
                btn.setFlat(True)
                btn.setStyleSheet("color: #1f4d9a; text-decoration: underline;")
                btn.clicked.connect(lambda _, t=related: self._jump_to(t))
                self.see_also_row.addWidget(btn)
        self.see_also_row.addStretch(1)

    def _on_view_figure(self) -> None:
        """Render the current term's example SMILES into a modal
        dialog with the generated PNG."""
        if not self._current_term_smiles:
            return
        import tempfile
        from pathlib import Path
        from PySide6.QtGui import QPixmap
        from PySide6.QtWidgets import (
            QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QMessageBox,
        )
        from orgchem.core.glossary_figures import render_term
        with tempfile.TemporaryDirectory(prefix="gloss_") as td:
            result = render_term(self._current_term_name,
                                 self._current_term_smiles,
                                 out_dir=td, force=True, fmt="png")
            if not result.rendered:
                QMessageBox.warning(
                    self, "Glossary figure",
                    result.skipped_reason or "Render failed")
                return
            pix = QPixmap(str(result.path))
        if pix.isNull():
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(f"{self._current_term_name} — example figure")
        dlg.resize(pix.width() + 40, pix.height() + 80)
        lay = QVBoxLayout(dlg)
        lbl = QLabel()
        lbl.setPixmap(pix)
        lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl, 1)
        lay.addWidget(QLabel(f"SMILES: {self._current_term_smiles}"))
        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(dlg.reject)
        lay.addWidget(bb)
        dlg.exec()

    def _jump_to(self, term: str) -> None:
        """Look up ``term`` by exact name or alias and display it."""
        with session_scope() as s:
            row = s.scalars(select(GlossaryTerm).where(
                GlossaryTerm.term == term)).first()
            if row is None:
                # try aliases
                for r in s.scalars(select(GlossaryTerm)):
                    try:
                        aliases = json.loads(r.aliases_json) if r.aliases_json else []
                    except Exception:
                        continue
                    if term in aliases:
                        row = r
                        break
            if row is None:
                return
            tid = row.id
        self._display(tid)

    # ------------------------------------------------------------------
    # External API — callable from agent actions ("show_term(term)").

    def focus_term(self, term: str) -> bool:
        """Scroll to and display the term; returns True if found."""
        self.filter.clear()
        self.category.setCurrentText("All")
        self._reload()
        for i, row in enumerate(self.model._rows):
            if row.term.lower() == term.lower():
                idx = self.model.index(i, 0)
                self.view.setCurrentIndex(idx)
                self._display(row.id)
                return True
        return False
