"""Synthesis tab — browse multi-step syntheses of target molecules.

Left: filterable pathway list (by name / target / category).
Right: rendered composite SVG scheme inside a scroll area, plus header
and export button. Selecting a pathway emits nothing on the bus for
now — future extension is to cross-link the current target into the
Molecule Workspace.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QListView, QLineEdit, QLabel,
    QPushButton, QScrollArea, QFileDialog, QMessageBox,
)

from orgchem.db.session import session_scope
from orgchem.db.models import SynthesisPathway
from orgchem.render.draw_pathway import build_svg, export_pathway

log = logging.getLogger(__name__)


class _PathwayListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._rows: list = []

    def reload(self, query: str = "") -> None:
        self.beginResetModel()
        with session_scope() as s:
            stmt = s.query(SynthesisPathway)
            if query:
                q = f"%{query}%"
                stmt = stmt.filter(
                    SynthesisPathway.name.ilike(q)
                    | SynthesisPathway.target_name.ilike(q)
                    | SynthesisPathway.category.ilike(q)
                )
            rows = stmt.order_by(SynthesisPathway.name).all()
            # Detach data we need so session can close.
            self._rows = [
                {"id": r.id, "name": r.name, "target": r.target_name,
                 "category": r.category or ""}
                for r in rows
            ]
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._rows)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        if role == Qt.DisplayRole:
            return f"{row['name']}\n   → {row['target']}"
        if role == Qt.UserRole:
            return row["id"]
        if role == Qt.ToolTipRole:
            return row["category"]
        return None


class SynthesisWorkspacePanel(QWidget):
    def __init__(self):
        super().__init__()
        self._current_id: int | None = None
        self._build_ui()
        self._reload()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # ---- left: list ----
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(2, 2, 2, 2)
        top = QHBoxLayout()
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter by name / target / category…")
        self.filter.textChanged.connect(self._on_filter)
        top.addWidget(QLabel("Filter:"))
        top.addWidget(self.filter)
        lv.addLayout(top)
        self.model = _PathwayListModel()
        self.view = QListView()
        self.view.setModel(self.model)
        self.view.setWordWrap(True)
        self.view.clicked.connect(self._on_clicked)
        lv.addWidget(self.view)
        left.setMaximumWidth(360)
        splitter.addWidget(left)

        # ---- right: scrollable scheme ----
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(4, 4, 4, 4)

        header = QHBoxLayout()
        self.title = QLabel("Select a pathway from the list")
        self.title.setStyleSheet(
            "font-size: 14pt; font-weight: bold; padding: 4px;")
        header.addWidget(self.title, 1)
        self.export_btn = QPushButton("Export pathway…")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self._on_export)
        header.addWidget(self.export_btn)
        rv.addLayout(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: #fafafa;")
        self.svg = QSvgWidget()
        self.svg.setMinimumWidth(1100)
        self.scroll.setWidget(self.svg)
        rv.addWidget(self.scroll, 1)

        splitter.addWidget(right)
        splitter.setStretchFactor(1, 1)
        lay.addWidget(splitter)

    # --------------------------------------------------------------

    def _reload(self) -> None:
        self.model.reload(self.filter.text())

    def _on_filter(self, text: str) -> None:
        self.model.reload(text)

    def _on_clicked(self, idx) -> None:
        pid = self.model.data(idx, Qt.UserRole)
        if pid is None:
            return
        self._display(int(pid))

    def _display(self, pid: int) -> None:
        with session_scope() as s:
            p = s.get(SynthesisPathway, pid)
            if p is None:
                return
            try:
                svg = build_svg(p)
            except Exception as e:  # noqa: BLE001
                log.exception("Pathway render failed")
                QMessageBox.warning(self, "Render failed", str(e))
                return
            self.title.setText(f"{p.name}")
        self._current_id = pid
        self.svg.load(bytes(svg, "utf-8"))
        # Resize the inner widget so the scroll area knows its content size.
        size = self.svg.renderer().defaultSize()
        if not size.isEmpty():
            self.svg.setMinimumSize(size)
            self.svg.resize(size)
        self.export_btn.setEnabled(True)

    def _on_export(self) -> None:
        if self._current_id is None:
            return
        with session_scope() as s:
            p = s.get(SynthesisPathway, self._current_id)
            if p is None:
                return
            name = p.name
            safe = (name.replace("/", "_").replace(":", "")
                    .replace("(", "").replace(")", ""))
        path, _ = QFileDialog.getSaveFileName(
            self, "Export synthesis pathway",
            f"{safe}.svg", "SVG vector (*.svg);;PNG image (*.png)")
        if not path:
            return
        try:
            with session_scope() as s:
                export_pathway(s.get(SynthesisPathway, self._current_id), path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Export failed", str(e))
