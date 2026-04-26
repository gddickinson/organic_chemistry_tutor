"""Phase 43 (round 151) — *Tools → Cell components…* dialog.

Singleton modeless reference dialog backed by
:mod:`orgchem.core.cell_components`.  Domain combo (eukarya /
bacteria / archaea) + sub-domain combo + category combo +
free-text filter on the left, list of components, HTML detail
card with a per-constituent table on the right.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSplitter,
    QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.cell_components import (
    CellComponent, categories, components_for_category,
    domains, get_component, list_components, sub_domains,
)

log = logging.getLogger(__name__)


_ALL_DOMAINS_LABEL = "(all domains)"
_ALL_SUBS_LABEL = "(all sub-domains)"
_ALL_CATS_LABEL = "(all categories)"


class CellComponentsDialog(QDialog):
    """Reference panel of cellular components keyed to the
    three domains of life."""

    _instance: Optional["CellComponentsDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "CellComponentsDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Cell components")
        self.setModal(False)
        self.resize(1080, 660)
        self._build_ui()
        self._reload_list()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)

        dom_row = QHBoxLayout()
        dom_row.addWidget(QLabel("Domain:"))
        self._dom_combo = QComboBox()
        self._dom_combo.addItem(_ALL_DOMAINS_LABEL)
        for d in domains():
            self._dom_combo.addItem(d)
        self._dom_combo.currentIndexChanged.connect(
            self._reload_list)
        dom_row.addWidget(self._dom_combo, 1)
        left_lay.addLayout(dom_row)

        sub_row = QHBoxLayout()
        sub_row.addWidget(QLabel("Sub-domain:"))
        self._sub_combo = QComboBox()
        self._sub_combo.addItem(_ALL_SUBS_LABEL)
        for s in sub_domains():
            self._sub_combo.addItem(s)
        self._sub_combo.currentIndexChanged.connect(
            self._reload_list)
        sub_row.addWidget(self._sub_combo, 1)
        left_lay.addLayout(sub_row)

        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        self._cat_combo = QComboBox()
        self._cat_combo.addItem(_ALL_CATS_LABEL)
        for c in categories():
            self._cat_combo.addItem(c)
        self._cat_combo.currentIndexChanged.connect(
            self._reload_list)
        cat_row.addWidget(self._cat_combo, 1)
        left_lay.addLayout(cat_row)

        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter by name / molecule (e.g. 'mitochondrion', "
            "'collagen', 'histone', 'flagellum')")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)
        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(300)
        left_lay.addWidget(self._list, 1)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select a component on the left.")
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

    def _reload_list(self) -> None:
        dom = self._dom_combo.currentText()
        sub = self._sub_combo.currentText()
        cat = self._cat_combo.currentText()
        dom_arg = None if dom == _ALL_DOMAINS_LABEL else dom
        sub_arg = None if sub == _ALL_SUBS_LABEL else sub
        entries = list_components(domain=dom_arg,
                                  sub_domain=sub_arg)
        if cat != _ALL_CATS_LABEL:
            cat_set = {c.id for c in components_for_category(cat)}
            entries = [c for c in entries if c.id in cat_set]
        needle = self._filter_edit.text().strip().lower()
        if needle:
            entries = [
                c for c in entries
                if needle in c.id.lower()
                or needle in c.name.lower()
                or any(needle in m.name.lower()
                       for m in c.constituents)
            ]
        self._list.clear()
        for c in entries:
            it = QListWidgetItem(f"{c.name}  —  {c.domain}")
            it.setData(Qt.UserRole, c.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank(
                "No components match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a component on the left.")
            return
        cid = current.data(Qt.UserRole)
        c = get_component(cid)
        if c is None:
            self._show_blank(f"Unknown component id: {cid}")
            return
        self._show_component(c)

    def _show_component(self, c: CellComponent) -> None:
        self._title.setText(c.name)
        sub_str = (", ".join(c.sub_domains)
                   if c.sub_domains else "(all)")
        self._meta.setText(
            f"<b>Domain:</b> {_esc(c.domain)} "
            f"&nbsp;·&nbsp; <b>Sub-domain(s):</b> "
            f"{_esc(sub_str)} "
            f"&nbsp;·&nbsp; <b>Category:</b> "
            f"{_esc(c.category)}"
        )
        rows = []
        for m in c.constituents:
            xref = ""
            if m.cross_reference_molecule_name:
                xref = (f" <i>(→ Molecule DB: "
                        f"{_esc(m.cross_reference_molecule_name)})</i>")
            extra = ""
            if m.notes:
                extra = f"<br/><small>{_esc(m.notes)}</small>"
            rows.append(
                f"<tr><td><b>{_esc(m.name)}</b>{xref}</td>"
                f"<td>{_esc(m.role)}{extra}</td></tr>"
            )
        constituents_table = (
            "<table border='0' cellspacing='4' "
            "cellpadding='3'>" + "".join(rows) + "</table>"
        )
        body = (
            f"<h4>Location</h4><p>{_esc(c.location)}</p>"
            f"<h4>Function</h4><p>{_esc(c.function)}</p>"
            f"<h4>Molecular constituents "
            f"({len(c.constituents)})</h4>"
            f"{constituents_table}"
        )
        if c.notable_diseases:
            body += (f"<h4>Notable diseases</h4>"
                     f"<p>{_esc(c.notable_diseases)}</p>")
        if c.notes:
            body += f"<h4>Notes</h4><p>{_esc(c.notes)}</p>"
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    def select_component(self, component_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == component_id:
                self._list.setCurrentRow(i)
                return True
        return False


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
