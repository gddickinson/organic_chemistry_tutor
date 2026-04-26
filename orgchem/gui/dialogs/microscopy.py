"""Phase 44 (round 150) — *Tools → Microscopy…* dialog.

Singleton modeless reference dialog backed by
:mod:`orgchem.core.microscopy`.  Same shape as the Phase-37c
chromatography / Phase-40a lab-analysers dialogs: resolution-
scale combo + sample-type combo + free-text filter on the
left, list of `abbreviation — name` rows, HTML detail card
on the right.
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

from orgchem.core.microscopy import (
    MicroscopyMethod, get_method, list_methods,
    methods_for_sample_type, resolution_scales,
    sample_types,
)

log = logging.getLogger(__name__)


_ALL_SCALES_LABEL = "(all scales)"
_ALL_SAMPLES_LABEL = "(all samples)"


class MicroscopyDialog(QDialog):
    """Reference panel of microscopy techniques organised by
    resolution scale."""

    _instance: Optional["MicroscopyDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "MicroscopyDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Microscopy techniques")
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

        scale_row = QHBoxLayout()
        scale_row.addWidget(QLabel("Resolution scale:"))
        self._scale_combo = QComboBox()
        self._scale_combo.addItem(_ALL_SCALES_LABEL)
        for s in resolution_scales():
            self._scale_combo.addItem(s)
        self._scale_combo.currentIndexChanged.connect(
            self._reload_list)
        scale_row.addWidget(self._scale_combo, 1)
        left_lay.addLayout(scale_row)

        sample_row = QHBoxLayout()
        sample_row.addWidget(QLabel("Sample type:"))
        self._sample_combo = QComboBox()
        self._sample_combo.addItem(_ALL_SAMPLES_LABEL)
        for s in sample_types():
            self._sample_combo.addItem(s)
        self._sample_combo.currentIndexChanged.connect(
            self._reload_list)
        sample_row.addWidget(self._sample_combo, 1)
        left_lay.addLayout(sample_row)

        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            "Filter by name / abbreviation / instrument "
            "(e.g. 'confocal', 'STED', 'Krios')")
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
        scale = self._scale_combo.currentText()
        sample = self._sample_combo.currentText()
        if scale == _ALL_SCALES_LABEL:
            entries = list_methods()
        else:
            entries = list_methods(resolution_scale=scale)
        if sample != _ALL_SAMPLES_LABEL:
            sample_set = set(
                m.id for m in methods_for_sample_type(sample))
            entries = [m for m in entries if m.id in sample_set]
        needle = self._filter_edit.text().strip().lower()
        if needle:
            entries = [
                m for m in entries
                if needle in m.id.lower()
                or needle in m.name.lower()
                or needle in m.abbreviation.lower()
                or needle in m.representative_instruments.lower()
            ]
        self._list.clear()
        for m in entries:
            it = QListWidgetItem(
                f"{m.abbreviation}  —  {m.name}")
            it.setData(Qt.UserRole, m.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank(
                "No methods match the current filter.")

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

    def _show_method(self, m: MicroscopyMethod) -> None:
        self._title.setText(f"{m.name}")
        self._meta.setText(
            f"<b>Abbreviation:</b> {_esc(m.abbreviation)} "
            f"&nbsp;·&nbsp; <b>Resolution scale:</b> "
            f"{_esc(m.resolution_scale)}"
        )
        body = (
            f"<h4>Typical resolution</h4>"
            f"<p>{_esc(m.typical_resolution)}</p>"
            f"<h4>Light source</h4>"
            f"<p>{_esc(m.light_source)}</p>"
            f"<h4>Contrast mechanism</h4>"
            f"<p>{_esc(m.contrast_mechanism)}</p>"
            f"<h4>Sample types</h4>"
            f"<p>{_esc(', '.join(m.sample_types))}</p>"
            f"<h4>Typical uses</h4>"
            f"<p>{_esc(m.typical_uses)}</p>"
            f"<h4>Strengths</h4>"
            f"<p>{_esc(m.strengths)}</p>"
            f"<h4>Limitations</h4>"
            f"<p>{_esc(m.limitations)}</p>"
            f"<h4>Representative instruments</h4>"
            f"<p>{_esc(m.representative_instruments)}</p>"
        )
        if m.cross_reference_lab_analyser_ids:
            body += (
                f"<h4>Cross-reference (Phase 40a Lab analysers)</h4>"
                f"<p>{_esc(', '.join(m.cross_reference_lab_analyser_ids))}</p>"
            )
        if m.notes:
            body += f"<h4>Notes</h4><p>{_esc(m.notes)}</p>"
        self._detail.setHtml(body)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._meta.setText("")
        self._detail.setHtml("")

    def select_method(self, method_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == method_id:
                self._list.setCurrentRow(i)
                return True
        return False


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
