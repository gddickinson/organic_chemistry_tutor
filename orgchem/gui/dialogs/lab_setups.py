"""Phase 38b (round 141) — *Tools → Lab setups…* dialog.

Modeless reference dialog backed by
:mod:`orgchem.core.lab_setups`.  Layout: setup list on the
left, detail card on the right with the setup's purpose,
ordered equipment list (each row resolved to its full
Phase-38a name), connection table, procedure, safety + ped
notes.

When the future Phase-38c canvas ships, this dialog will gain
a *Build on canvas* button that pre-populates the canvas with
the seeded setup's equipment + connections.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSplitter, QTextBrowser,
    QVBoxLayout, QWidget,
)

from orgchem.core.lab_equipment import get_equipment
from orgchem.core.lab_setups import (
    Setup, get_setup, list_setups, validate_setup,
)

log = logging.getLogger(__name__)


class LabSetupsDialog(QDialog):
    """Reference panel of canonical lab setups + per-setup
    equipment + connection detail."""

    _instance: Optional["LabSetupsDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "LabSetupsDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Lab setups")
        self.setModal(False)
        self.resize(1080, 660)
        self._build_ui()
        self._reload_list()

    # ---- UI construction -------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter (e.g. 'distill', 'reflux', 'extract')")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)
        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(260)
        left_lay.addWidget(self._list, 1)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select a setup on the left.")
        f = self._title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 2)
        self._title.setFont(f)
        self._title.setWordWrap(True)
        right_lay.addWidget(self._title)
        self._meta = QLabel("")
        self._meta.setWordWrap(True)
        right_lay.addWidget(self._meta)
        self._detail = QTextBrowser()
        self._detail.setOpenExternalLinks(False)
        right_lay.addWidget(self._detail, 1)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter, 1)

        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    # ---- list management -------------------------------------

    def _reload_list(self) -> None:
        setups = list_setups()
        needle = self._filter_edit.text().strip().lower()
        if needle:
            setups = [
                s for s in setups
                if needle in s.id.lower()
                or needle in s.name.lower()
                or needle in s.purpose.lower()
            ]
        self._list.clear()
        for s in setups:
            it = QListWidgetItem(s.name)
            it.setData(Qt.UserRole, s.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank("No setups match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a setup on the left.")
            return
        sid = current.data(Qt.UserRole)
        s = get_setup(sid)
        if s is None:
            self._show_blank(f"Unknown setup id: {sid}")
            return
        self._show_setup(s)

    # ---- detail rendering ------------------------------------

    def _show_setup(self, s: Setup) -> None:
        self._title.setText(s.name)
        n_eq = len(s.equipment)
        n_conn = len(s.connections)
        self._meta.setText(
            f"<b>Equipment:</b> {n_eq} pieces &nbsp;·&nbsp; "
            f"<b>Connections:</b> {n_conn}")
        # Build the equipment list with resolved names.
        eq_html = "<ol>"
        for eid in s.equipment:
            e = get_equipment(eid)
            label = e.name if e else f"<i>{eid} (unknown)</i>"
            eq_html += (
                f"<li><b>{_html_escape(label)}</b> "
                f"<span style='color: #666'>"
                f"({_html_escape(eid)})</span></li>"
            )
        eq_html += "</ol>"
        # Build the connection table.
        conn_html = "<ul>"
        for c in s.connections:
            from_e = get_equipment(s.equipment[c.from_equipment_idx])
            to_e = get_equipment(s.equipment[c.to_equipment_idx])
            from_name = from_e.name if from_e \
                else s.equipment[c.from_equipment_idx]
            to_name = to_e.name if to_e \
                else s.equipment[c.to_equipment_idx]
            note = (f" — <i>{_html_escape(c.note)}</i>"
                    if c.note else "")
            conn_html += (
                f"<li>{_html_escape(from_name)} "
                f"[<b>{_html_escape(c.from_port)}</b>] → "
                f"{_html_escape(to_name)} "
                f"[<b>{_html_escape(c.to_port)}</b>]"
                f"{note}</li>"
            )
        conn_html += "</ul>"

        body = (
            f"<h4>Purpose</h4><p>{_html_escape(s.purpose)}</p>"
            f"<h4>Equipment ({n_eq})</h4>{eq_html}"
            f"<h4>Connections ({n_conn})</h4>{conn_html}"
        )
        if s.procedure:
            body += (f"<h4>Procedure</h4>"
                     f"<p>{_html_escape(s.procedure)}</p>")
        if s.safety_notes:
            body += (f"<h4>Safety notes</h4>"
                     f"<p>{_html_escape(s.safety_notes)}</p>")
        if s.pedagogical_notes:
            body += (f"<h4>Pedagogical notes</h4>"
                     f"<p>{_html_escape(s.pedagogical_notes)}</p>")
        if s.typical_reactions:
            body += (f"<h4>Typical reactions</h4>"
                     f"<p>{_html_escape(s.typical_reactions)}</p>")
        # Validation status — surfaces stale data after equipment
        # ports are renamed.
        errs = validate_setup(s)
        if errs:
            err_html = "<ul>"
            for e in errs:
                err_html += f"<li>{_html_escape(e)}</li>"
            err_html += "</ul>"
            body += (f"<h4 style='color: #C02020'>"
                     f"Validation errors</h4>{err_html}")
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    # ---- programmatic API ------------------------------------

    def select_setup(self, setup_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == setup_id:
                self._list.setCurrentRow(i)
                return True
        return False


def _html_escape(s: str) -> str:
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
