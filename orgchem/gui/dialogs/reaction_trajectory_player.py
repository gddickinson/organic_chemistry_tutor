"""Reaction trajectory player — modal 3Dmol.js animation (Phase 2c.2).

Shows the atoms morphing from reactant to product positions with bonds
auto-appearing / auto-disappearing as atoms move (3Dmol.js proximity
bonding each frame). Play / pause / reset / speed controls live inside
the HTML page — the dialog is just a QWebEngineView host.
"""
from __future__ import annotations
import logging

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox,
)

from orgchem.core.reaction_trajectory import build_xyz_trajectory
from orgchem.render.draw_reaction_3d import build_trajectory_html

log = logging.getLogger(__name__)


class ReactionTrajectoryPlayerDialog(QDialog):
    def __init__(self, mapped_smarts: str, reaction_name: str,
                 n_frames: int = 24, parent=None):
        super().__init__(parent)
        self.mapped_smarts = mapped_smarts
        self.reaction_name = reaction_name
        self.n_frames = n_frames
        self.setWindowTitle(f"3D animation: {reaction_name}")
        self.resize(820, 640)

        lay = QVBoxLayout(self)

        header = QLabel(f"<b>{reaction_name}</b>  —  {n_frames} frames, "
                        "atoms coloured by element, bonds inferred each frame.")
        header.setStyleSheet("color:#444; padding: 4px;")
        lay.addWidget(header)

        self.view = QWebEngineView()
        lay.addWidget(self.view, 1)

        bar = QHBoxLayout()
        self.save_btn = QPushButton("Save HTML…")
        self.save_btn.clicked.connect(self._save_html)
        bar.addWidget(self.save_btn)
        bar.addStretch(1)
        close_btn = QDialogButtonBox(QDialogButtonBox.Close)
        close_btn.rejected.connect(self.reject)
        bar.addWidget(close_btn)
        lay.addLayout(bar)

        self._html = ""
        self._build()

    def _build(self) -> None:
        try:
            xyz = build_xyz_trajectory(self.mapped_smarts,
                                       n_frames=self.n_frames)
            self._html = build_trajectory_html(
                xyz, title=self.reaction_name)
        except Exception as e:  # noqa: BLE001
            log.exception("Trajectory build failed")
            self._html = (
                f"<html><body style='color:#c03030;padding:30px'>"
                f"<h3>Could not build trajectory</h3><pre>{e}</pre>"
                f"</body></html>")
        self.view.setHtml(self._html)

    def _save_html(self) -> None:
        if not self._html:
            return
        safe = (self.reaction_name or "reaction").replace("/", "_").replace(":", "")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save trajectory HTML",
            f"{safe}_trajectory.html", "HTML (*.html *.htm)")
        if not path:
            return
        try:
            with open(path, "w") as f:
                f.write(self._html)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Save failed", str(e))
