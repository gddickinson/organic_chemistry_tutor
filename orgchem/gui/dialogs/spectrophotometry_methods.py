"""Phase 37d (round 139) — *Tools → Spectrophotometry…* dialog.

Modeless reference dialog backed by
:mod:`orgchem.core.spectrophotometry_methods`.  Layout mirrors
the Phase-37c chromatography dialog (category combo + filter +
list + HTML detail card) plus a small Beer-Lambert calculator
widget at the bottom — three of A / ε / l / c in, the fourth
out.

Beer-Lambert calculator (the only quantitative widget in the
catalogue tools so far) lives at the bottom of the right pane:
- Four `QDoubleSpinBox` fields for A / ε (M⁻¹·cm⁻¹) / l (cm) /
  c (M).
- A *Solve* button that fills the empty field via
  :func:`orgchem.core.spectrophotometry_methods.beer_lambert_solve`.
- A status label that surfaces the equation in human form
  ("c = A / (ε · l) = 4.0e-5 M").
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSplitter, QTextBrowser,
    QVBoxLayout, QWidget,
)

from orgchem.core.spectrophotometry_methods import (
    SpectrophotometryMethod, beer_lambert_solve, categories,
    get_method, list_methods,
)

log = logging.getLogger(__name__)


_ALL_CATEGORIES_LABEL = "(all categories)"


class SpectrophotometryDialog(QDialog):
    """Reference panel of spectrophotometry-method entries with
    category + free-text filtering, an HTML detail card, and a
    Beer-Lambert calculator."""

    _instance: Optional["SpectrophotometryDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "SpectrophotometryDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Spectrophotometry techniques")
        self.setModal(False)
        self.resize(1100, 720)
        self._build_ui()
        self._reload_list()

    # ---- UI construction -------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        splitter = QSplitter(Qt.Horizontal)

        # ---- left pane: filter + list ------------------------
        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        self._cat_combo = QComboBox()
        self._cat_combo.addItem(_ALL_CATEGORIES_LABEL)
        for c in categories():
            self._cat_combo.addItem(c)
        self._cat_combo.currentIndexChanged.connect(self._reload_list)
        cat_row.addWidget(self._cat_combo, 1)
        left_lay.addLayout(cat_row)

        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter by name / abbreviation / category")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)

        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(260)
        left_lay.addWidget(self._list, 1)

        splitter.addWidget(left)

        # ---- right pane: detail + Beer-Lambert ---------------
        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select a method on the left.")
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

        # ---- Beer-Lambert calculator (collapsible) -----------
        bl_box = QGroupBox("Beer-Lambert calculator (A = ε · l · c)")
        bl_box.setCheckable(True)
        bl_box.setChecked(False)
        bl_form = QFormLayout(bl_box)
        self._a_spin = self._spin(0.0, 10.0, "")
        self._eps_spin = self._spin(0.0, 1e8, "M⁻¹·cm⁻¹")
        self._eps_spin.setDecimals(1)
        self._l_spin = self._spin(0.0, 100.0, "cm")
        self._c_spin = self._spin(0.0, 100.0, "M")
        self._c_spin.setDecimals(8)
        bl_form.addRow("Absorbance A:", self._a_spin)
        bl_form.addRow("Molar absorptivity ε:", self._eps_spin)
        bl_form.addRow("Path length l:", self._l_spin)
        bl_form.addRow("Concentration c:", self._c_spin)
        btn_row = QHBoxLayout()
        self._bl_solve_btn = QPushButton("Solve for empty field")
        self._bl_solve_btn.clicked.connect(self._on_beer_lambert_solve)
        btn_row.addWidget(self._bl_solve_btn)
        self._bl_clear_btn = QPushButton("Clear")
        self._bl_clear_btn.clicked.connect(self._on_beer_lambert_clear)
        btn_row.addWidget(self._bl_clear_btn)
        btn_row.addStretch(1)
        bl_form.addRow(btn_row)
        self._bl_status = QLabel(
            "Leave exactly one field blank (zero); the "
            "calculator fills it.")
        self._bl_status.setWordWrap(True)
        bl_form.addRow(self._bl_status)
        right_lay.addWidget(bl_box)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter, 1)

        # Footer.
        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    @staticmethod
    def _spin(minimum: float, maximum: float,
              suffix: str) -> QDoubleSpinBox:
        s = QDoubleSpinBox()
        s.setRange(minimum, maximum)
        s.setDecimals(4)
        if suffix:
            s.setSuffix(f"  {suffix}")
        s.setValue(0.0)
        return s

    # ---- list management -------------------------------------

    def _reload_list(self) -> None:
        cat = self._cat_combo.currentText()
        if cat == _ALL_CATEGORIES_LABEL:
            methods = list_methods()
        else:
            methods = list_methods(category=cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            methods = [
                m for m in methods
                if needle in m.name.lower()
                or needle in m.abbreviation.lower()
                or needle in m.category.lower()
                or needle in m.id.lower()
            ]
        self._list.clear()
        for m in methods:
            it = QListWidgetItem(
                f"{m.abbreviation}  —  {m.name}")
            it.setData(Qt.UserRole, m.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank("No methods match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a method on the left.")
            return
        mid = current.data(Qt.UserRole)
        m = get_method(mid)
        if m is None:
            self._show_blank(f"Unknown method id: {mid}")
            return
        self._show_method(m)

    # ---- detail rendering ------------------------------------

    def _show_method(self, m: SpectrophotometryMethod) -> None:
        self._title.setText(f"{m.name} ({m.abbreviation})")
        self._meta.setText(
            f"<b>Category:</b> {m.category} &nbsp;·&nbsp; "
            f"<b>Range:</b> {_html_escape(m.wavelength_range)}")
        body = (
            f"<h4>Principle</h4><p>{_html_escape(m.principle)}</p>"
            f"<h4>Light source</h4>"
            f"<p>{_html_escape(m.light_source)}</p>"
            f"<h4>Sample handling</h4>"
            f"<p>{_html_escape(m.sample_handling)}</p>"
            f"<h4>Detector</h4>"
            f"<p>{_html_escape(m.detector)}</p>"
            f"<h4>Typical analytes</h4>"
            f"<p>{_html_escape(m.typical_analytes)}</p>"
            f"<h4>Strengths</h4>"
            f"<p>{_html_escape(m.strengths)}</p>"
            f"<h4>Limitations</h4>"
            f"<p>{_html_escape(m.limitations)}</p>"
            f"<h4>Procedure</h4>"
            f"<p>{_html_escape(m.procedure)}</p>"
        )
        if m.notes:
            body += f"<h4>Notes</h4><p>{_html_escape(m.notes)}</p>"
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    # ---- Beer-Lambert calculator slots -----------------------

    def _on_beer_lambert_solve(self) -> None:
        a = self._a_spin.value()
        eps = self._eps_spin.value()
        l = self._l_spin.value()
        c = self._c_spin.value()
        # Treat 0 as "blank".
        kwargs: dict = {}
        empty: list = []
        for name, val in (
                ("absorbance", a), ("molar_absorptivity", eps),
                ("path_length_cm", l), ("concentration_M", c)):
            if val > 0:
                kwargs[name] = val
            else:
                empty.append(name)
        if len(empty) != 1:
            self._bl_status.setText(
                f"<b>Error:</b> need exactly one blank "
                f"field, got {len(empty)}.")
            return
        try:
            res = beer_lambert_solve(**kwargs)
        except ValueError as e:
            self._bl_status.setText(f"<b>Error:</b> {e}")
            return
        # Update the previously-empty spin box.
        target = empty[0]
        if target == "absorbance":
            self._a_spin.setValue(res["absorbance"])
            txt = (f"A = ε · l · c = {res['molar_absorptivity']:.1f} · "
                   f"{res['path_length_cm']} · "
                   f"{res['concentration_M']:.2e} = "
                   f"{res['absorbance']:.4f}")
        elif target == "molar_absorptivity":
            self._eps_spin.setValue(res["molar_absorptivity"])
            txt = (f"ε = A / (l · c) = "
                   f"{res['molar_absorptivity']:.1f} M⁻¹·cm⁻¹")
        elif target == "path_length_cm":
            self._l_spin.setValue(res["path_length_cm"])
            txt = (f"l = A / (ε · c) = "
                   f"{res['path_length_cm']:.4f} cm")
        else:
            self._c_spin.setValue(res["concentration_M"])
            txt = (f"c = A / (ε · l) = "
                   f"{res['concentration_M']:.4e} M")
        self._bl_status.setText(txt)

    def _on_beer_lambert_clear(self) -> None:
        for s in (self._a_spin, self._eps_spin,
                  self._l_spin, self._c_spin):
            s.setValue(0.0)
        self._bl_status.setText(
            "Leave exactly one field blank (zero); the "
            "calculator fills it.")

    # ---- programmatic API ------------------------------------

    def select_method(self, method_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == method_id:
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
