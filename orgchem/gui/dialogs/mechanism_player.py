"""Mechanism step-through player — modal dialog with Prev / Next.

Pedagogically: each step shows the molecule as it stands at that instant,
with red curved arrows overlaid to show electron flow into the *next*
step. Titles and descriptions come from the mechanism JSON. Students
step back and forth to build intuition about concerted vs stepwise.
"""
from __future__ import annotations
import logging

from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit,
    QDialogButtonBox, QFileDialog, QMessageBox,
)

from orgchem.core.mechanism import Mechanism
from orgchem.render.draw_mechanism import render_step_svg

log = logging.getLogger(__name__)


class MechanismPlayerDialog(QDialog):
    def __init__(self, mechanism: Mechanism, reaction_name: str, parent=None):
        super().__init__(parent)
        self.mechanism = mechanism
        self.reaction_name = reaction_name
        self._idx = 0

        self.setWindowTitle(f"Mechanism: {reaction_name}")
        self.resize(820, 720)

        lay = QVBoxLayout(self)

        header = QLabel(f"<b>{reaction_name}</b>")
        header.setStyleSheet("font-size: 15pt; padding: 4px;")
        lay.addWidget(header)

        self.step_title = QLabel()
        self.step_title.setStyleSheet("font-weight: bold; color:#204060; padding: 2px;")
        lay.addWidget(self.step_title)

        self.svg = QSvgWidget()
        self.svg.setMinimumSize(560, 420)
        self.svg.setStyleSheet("background: white; border: 1px solid #ccc;")
        lay.addWidget(self.svg, 1)

        self.desc = QPlainTextEdit()
        self.desc.setReadOnly(True)
        self.desc.setMaximumHeight(140)
        lay.addWidget(self.desc)

        nav = QHBoxLayout()
        self.prev_btn = QPushButton("◀  Prev")
        self.next_btn = QPushButton("Next  ▶")
        self.prev_btn.clicked.connect(self._prev)
        self.next_btn.clicked.connect(self._next)
        self.counter = QLabel()
        self.counter.setAlignment(Qt.AlignCenter)
        nav.addWidget(self.prev_btn)
        nav.addWidget(self.counter, 1)
        nav.addWidget(self.next_btn)

        save_btn = QPushButton("Save step PNG…")
        save_btn.clicked.connect(self._save_png)
        nav.addWidget(save_btn)

        lay.addLayout(nav)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        lay.addWidget(bb)

        self._render()

    # ------------------------------------------------------------------

    def _render(self) -> None:
        total = len(self.mechanism)
        if total == 0:
            self.step_title.setText("(empty mechanism)")
            self.counter.setText("0 / 0")
            return
        step = self.mechanism[self._idx]
        self.step_title.setText(f"{self._idx + 1}. {step.title}")
        self.desc.setPlainText(step.description)
        try:
            svg = render_step_svg(step)
            self.svg.load(bytes(svg, "utf-8"))
        except Exception as e:  # noqa: BLE001
            log.warning("Mechanism render failed: %s", e)
            self.svg.load(b"<svg xmlns='http://www.w3.org/2000/svg'/>")
        self.counter.setText(f"{self._idx + 1} / {total}")
        self.prev_btn.setEnabled(self._idx > 0)
        self.next_btn.setEnabled(self._idx < total - 1)

    def _prev(self) -> None:
        if self._idx > 0:
            self._idx -= 1
            self._render()

    def _next(self) -> None:
        if self._idx < len(self.mechanism) - 1:
            self._idx += 1
            self._render()

    def _save_png(self) -> None:
        step = self.mechanism[self._idx]
        base = f"{self.reaction_name}_step{self._idx + 1}".replace("/", "_")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save mechanism step", f"{base}.svg",
            "SVG vector (*.svg)")
        if not path:
            return
        try:
            svg = render_step_svg(step)
            with open(path, "w") as f:
                f.write(svg)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Save failed", str(e))
