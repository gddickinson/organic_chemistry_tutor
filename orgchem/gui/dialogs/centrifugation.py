"""Phase 41 (round 144) — *Tools → Centrifugation…* dialog.

Singleton modeless dialog backed by
:mod:`orgchem.core.centrifugation`.  Three tabs (Centrifuges /
Rotors / Applications) each with a category filter + list +
HTML detail card, plus a fourth tab carrying the g↔rpm
calculator with a rotor-dropdown that pre-fills the radius.

The g↔rpm calculator is the headline feature — it's the
single-most-confused conversion every wet-lab worker has to
do, and getting the *rotor radius* right is what makes the
conversion correct.  By driving the radius from the catalogued
rotor (rather than asking the user to type it) we eliminate
the "wrong rotor → wrong RPM → broken tubes" failure mode.
"""
from __future__ import annotations
import logging
from typing import Callable, List, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSplitter,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.centrifugation import (
    Application, Centrifuge, Rotor, VALID_CENTRIFUGE_CLASSES,
    VALID_PROTOCOL_CLASSES, VALID_ROTOR_TYPES,
    g_to_rpm, get_application, get_centrifuge, get_rotor,
    list_applications, list_centrifuges, list_rotors,
    rpm_to_g,
)

log = logging.getLogger(__name__)


_ALL_LABEL = "(all)"


# ------------------------------------------------------------------
# Catalogue tab helper
# ------------------------------------------------------------------

class _CatalogueTab(QWidget):
    """One reusable category-list-detail tab.  Constructor
    takes the helpers needed to enumerate + render entries —
    which makes Centrifuges / Rotors / Applications tabs share
    one implementation."""

    def __init__(self,
                 categories: Tuple[str, ...],
                 list_fn: Callable[[Optional[str]], list],
                 get_fn: Callable[[str], object],
                 detail_renderer: Callable[[object], str],
                 row_label: Callable[[object], str],
                 row_id: Callable[[object], str],
                 placeholder: str,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._categories = categories
        self._list_fn = list_fn
        self._get_fn = get_fn
        self._detail_renderer = detail_renderer
        self._row_label = row_label
        self._row_id = row_id
        self._placeholder = placeholder
        self._build_ui()
        self._reload_list()

    def _build_ui(self) -> None:
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        self._cat_combo = QComboBox()
        self._cat_combo.addItem(_ALL_LABEL)
        for c in self._categories:
            self._cat_combo.addItem(c)
        self._cat_combo.currentIndexChanged.connect(self._reload_list)
        cat_row.addWidget(self._cat_combo, 1)
        left_lay.addLayout(cat_row)
        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter by name / id…")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)
        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(240)
        left_lay.addWidget(self._list, 1)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel(self._placeholder)
        f = self._title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 2)
        self._title.setFont(f)
        self._title.setWordWrap(True)
        right_lay.addWidget(self._title)
        self._detail = QTextBrowser()
        self._detail.setOpenExternalLinks(False)
        right_lay.addWidget(self._detail, 1)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter, 1)

    def _reload_list(self) -> None:
        cat = self._cat_combo.currentText()
        if cat == _ALL_LABEL:
            entries = self._list_fn(None)
        else:
            entries = self._list_fn(cat)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            entries = [e for e in entries
                       if needle in self._row_id(e).lower()
                       or needle in self._row_label(e).lower()]
        self._list.clear()
        for e in entries:
            it = QListWidgetItem(self._row_label(e))
            it.setData(Qt.UserRole, self._row_id(e))
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._title.setText("No entries match the filter.")
            self._detail.setHtml("")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            return
        eid = current.data(Qt.UserRole)
        e = self._get_fn(eid)
        if e is None:
            return
        self._title.setText(self._row_label(e))
        self._detail.setHtml(self._detail_renderer(e))

    def select_entry(self, entry_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == entry_id:
                self._list.setCurrentRow(i)
                return True
        return False


# ------------------------------------------------------------------
# Detail renderers
# ------------------------------------------------------------------

def _render_centrifuge(c: Centrifuge) -> str:
    refrig = "yes" if c.refrigerated else "no"
    return (
        f"<p><b>Manufacturer:</b> {_esc(c.manufacturer)}"
        f" &nbsp;·&nbsp; <b>Class:</b> "
        f"{_esc(c.centrifuge_class)}</p>"
        f"<p><b>Max speed:</b> {c.max_speed_rpm} RPM "
        f"&nbsp;·&nbsp; <b>Max RCF:</b> {c.max_g_force:,} × g "
        f"&nbsp;·&nbsp; <b>Refrigerated:</b> {refrig}</p>"
        f"<p><b>Capacity:</b> {_esc(c.typical_capacity)}</p>"
        f"<h4>Typical uses</h4><p>{_esc(c.typical_uses)}</p>"
        + (f"<h4>Notes</h4><p>{_esc(c.notes)}</p>" if c.notes else "")
    )


def _render_rotor(r: Rotor) -> str:
    radius_text = (f"{r.max_radius_cm} cm"
                   if r.max_radius_cm == r.min_radius_cm
                   else f"{r.min_radius_cm}–{r.max_radius_cm} cm "
                        "(min–max for swinging-bucket arms)")
    return (
        f"<p><b>Type:</b> {_esc(r.rotor_type)} &nbsp;·&nbsp; "
        f"<b>Max speed:</b> {r.max_speed_rpm:,} RPM "
        f"&nbsp;·&nbsp; <b>Radius:</b> {radius_text}</p>"
        f"<p><b>Tubes:</b> {_esc(r.typical_tubes)}</p>"
        + (f"<h4>Notes</h4><p>{_esc(r.notes)}</p>" if r.notes else "")
    )


def _render_application(a: Application) -> str:
    return (
        f"<p><b>Protocol class:</b> {_esc(a.protocol_class)}</p>"
        f"<p><b>Recommended RCF:</b> "
        f"{_esc(a.recommended_g_force)} &nbsp;·&nbsp; "
        f"<b>Duration:</b> {_esc(a.recommended_duration)} "
        f"&nbsp;·&nbsp; <b>Rotor type:</b> "
        f"{_esc(a.recommended_rotor_type)}</p>"
        f"<h4>Description</h4><p>{_esc(a.description)}</p>"
        + (f"<h4>Notes</h4><p>{_esc(a.notes)}</p>" if a.notes else "")
    )


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


# ------------------------------------------------------------------
# g ↔ rpm calculator tab
# ------------------------------------------------------------------

class _CalculatorTab(QWidget):
    """Headline feature: g↔rpm conversion with rotor-dropdown
    radius pre-fill.  Picking a catalogued rotor sets the
    radius spin box AND clamps the max RPM warning."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)

        # ---- rotor picker ------------------------------------
        rotor_box = QGroupBox(
            "Rotor selection (auto-fills radius)")
        rotor_form = QFormLayout(rotor_box)
        self._rotor_combo = QComboBox()
        self._rotor_combo.addItem("(custom radius)", "")
        for r in list_rotors():
            label = (f"{r.name} — {r.rotor_type} "
                     f"({r.max_radius_cm} cm)")
            self._rotor_combo.addItem(label, r.id)
        self._rotor_combo.currentIndexChanged.connect(
            self._on_rotor_changed)
        rotor_form.addRow("Rotor:", self._rotor_combo)
        self._radius_spin = QDoubleSpinBox()
        self._radius_spin.setDecimals(2)
        self._radius_spin.setRange(0.1, 100.0)
        self._radius_spin.setValue(8.4)
        self._radius_spin.setSuffix("  cm")
        rotor_form.addRow("Radius r:", self._radius_spin)
        self._max_rpm_label = QLabel(
            "Max RPM for this rotor: (custom)")
        self._max_rpm_label.setWordWrap(True)
        rotor_form.addRow(self._max_rpm_label)
        outer.addWidget(rotor_box)

        # ---- conversion --------------------------------------
        calc_box = QGroupBox(
            "g ↔ RPM (g = 1.118 × 10⁻⁵ · RPM² · r)")
        calc_form = QFormLayout(calc_box)
        self._rpm_spin = QDoubleSpinBox()
        self._rpm_spin.setDecimals(0)
        self._rpm_spin.setRange(0, 200000)
        self._rpm_spin.setValue(0)
        self._rpm_spin.setSuffix("  RPM")
        calc_form.addRow("Speed:", self._rpm_spin)
        self._g_spin = QDoubleSpinBox()
        self._g_spin.setDecimals(0)
        self._g_spin.setRange(0, 1_000_000_000)
        self._g_spin.setValue(0)
        self._g_spin.setSuffix("  × g")
        calc_form.addRow("RCF:", self._g_spin)
        btn_row = QHBoxLayout()
        rpm_to_g_btn = QPushButton("RPM → × g")
        g_to_rpm_btn = QPushButton("× g → RPM")
        clear_btn = QPushButton("Clear")
        btn_row.addWidget(rpm_to_g_btn)
        btn_row.addWidget(g_to_rpm_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch(1)
        calc_form.addRow(btn_row)
        self._status = QLabel(
            "Select a rotor or enter a custom radius, then "
            "fill in either RPM or × g and click the "
            "matching button.")
        self._status.setWordWrap(True)
        calc_form.addRow(self._status)
        outer.addWidget(calc_box)

        rpm_to_g_btn.clicked.connect(self._on_rpm_to_g)
        g_to_rpm_btn.clicked.connect(self._on_g_to_rpm)
        clear_btn.clicked.connect(self._on_clear)

        outer.addStretch(1)

        # Initial state: pick the first rotor as a sensible
        # default so the radius spin reads a real value.
        if self._rotor_combo.count() > 1:
            self._rotor_combo.setCurrentIndex(1)

    # ---- slots ------------------------------------------------

    def _on_rotor_changed(self) -> None:
        rid = self._rotor_combo.currentData()
        if not rid:
            self._max_rpm_label.setText(
                "Max RPM for this rotor: (custom)")
            return
        rotor = get_rotor(rid)
        if rotor is None:
            return
        self._radius_spin.setValue(rotor.max_radius_cm)
        self._max_rpm_label.setText(
            f"Max RPM for this rotor: "
            f"<b>{rotor.max_speed_rpm:,} RPM</b> "
            f"({rotor.rotor_type})")

    def _on_rpm_to_g(self) -> None:
        try:
            r = rpm_to_g(self._rpm_spin.value(),
                        self._radius_spin.value())
        except ValueError as e:
            self._status.setText(f"<b>Error:</b> {e}")
            return
        self._g_spin.blockSignals(True)
        self._g_spin.setValue(r["g_force"])
        self._g_spin.blockSignals(False)
        self._status.setText(
            f"g = 1.118e-5 · {self._rpm_spin.value():,.0f}² "
            f"· {self._radius_spin.value():.2f} = "
            f"<b>{r['g_force']:,.0f} × g</b>")
        self._maybe_warn_overspeed()

    def _on_g_to_rpm(self) -> None:
        try:
            r = g_to_rpm(self._g_spin.value(),
                         self._radius_spin.value())
        except ValueError as e:
            self._status.setText(f"<b>Error:</b> {e}")
            return
        self._rpm_spin.blockSignals(True)
        self._rpm_spin.setValue(r["rpm"])
        self._rpm_spin.blockSignals(False)
        self._status.setText(
            f"RPM = √({self._g_spin.value():,.0f} ÷ (1.118e-5 · "
            f"{self._radius_spin.value():.2f})) = "
            f"<b>{r['rpm']:,.0f} RPM</b>")
        self._maybe_warn_overspeed()

    def _on_clear(self) -> None:
        self._rpm_spin.setValue(0)
        self._g_spin.setValue(0)
        self._status.setText(
            "Select a rotor or enter a custom radius, then "
            "fill in either RPM or × g and click the "
            "matching button.")

    def _maybe_warn_overspeed(self) -> None:
        rid = self._rotor_combo.currentData()
        if not rid:
            return
        rotor = get_rotor(rid)
        if rotor is None:
            return
        if self._rpm_spin.value() > rotor.max_speed_rpm:
            current = self._status.text()
            self._status.setText(
                current
                + f" &nbsp;·&nbsp; <span style='color:#C02020'>"
                f"<b>OVERSPEED:</b> exceeds rotor max "
                f"{rotor.max_speed_rpm:,} RPM!</span>")


# ------------------------------------------------------------------
# Dialog
# ------------------------------------------------------------------

class CentrifugationDialog(QDialog):
    """Centrifugation reference dialog: Centrifuges / Rotors /
    Applications catalogue tabs + g↔rpm calculator tab."""

    _instance: Optional["CentrifugationDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "CentrifugationDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Centrifugation reference + calculator")
        self.setModal(False)
        self.resize(1080, 660)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        self._tabs = QTabWidget()

        self._cent_tab = _CatalogueTab(
            categories=VALID_CENTRIFUGE_CLASSES,
            list_fn=list_centrifuges,
            get_fn=get_centrifuge,
            detail_renderer=_render_centrifuge,
            row_label=lambda c: f"{c.name} — {c.centrifuge_class}",
            row_id=lambda c: c.id,
            placeholder="Select a centrifuge on the left.",
        )
        self._tabs.addTab(self._cent_tab, "Centrifuges")

        self._rotor_tab = _CatalogueTab(
            categories=VALID_ROTOR_TYPES,
            list_fn=list_rotors,
            get_fn=get_rotor,
            detail_renderer=_render_rotor,
            row_label=lambda r: f"{r.name} — {r.rotor_type}",
            row_id=lambda r: r.id,
            placeholder="Select a rotor on the left.",
        )
        self._tabs.addTab(self._rotor_tab, "Rotors")

        self._app_tab = _CatalogueTab(
            categories=VALID_PROTOCOL_CLASSES,
            list_fn=list_applications,
            get_fn=get_application,
            detail_renderer=_render_application,
            row_label=lambda a: f"{a.name} — {a.protocol_class}",
            row_id=lambda a: a.id,
            placeholder="Select an application on the left.",
        )
        self._tabs.addTab(self._app_tab, "Applications")

        self._calc_tab = _CalculatorTab()
        self._tabs.addTab(self._calc_tab, "g ↔ RPM calculator")

        outer.addWidget(self._tabs, 1)
        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        outer.addLayout(footer)

    # ---- programmatic API ------------------------------------

    def select_tab(self, label: str) -> bool:
        for i in range(self._tabs.count()):
            if self._tabs.tabText(i).lower() == label.lower():
                self._tabs.setCurrentIndex(i)
                return True
        return False

    def tab_labels(self) -> List[str]:
        return [self._tabs.tabText(i)
                for i in range(self._tabs.count())]

    def select_centrifuge(self, centrifuge_id: str) -> bool:
        return self._cent_tab.select_entry(centrifuge_id)

    def select_rotor(self, rotor_id: str) -> bool:
        return self._rotor_tab.select_entry(rotor_id)

    def select_application(self, app_id: str) -> bool:
        return self._app_tab.select_entry(app_id)
