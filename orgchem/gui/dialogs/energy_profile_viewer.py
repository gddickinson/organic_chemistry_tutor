"""Energy-profile viewer — modal dialog wrapping the matplotlib renderer.

Shows the reaction-coordinate diagram for a reaction (Phase 13d).
Read-only — students step through the existing TS / intermediate / product
points, read off barrier heights, and can save the figure.
"""
from __future__ import annotations
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QDialogButtonBox, QFileDialog, QMessageBox,
)

from orgchem.core.energy_profile import ReactionEnergyProfile
from orgchem.render.draw_energy_profile import export_profile

log = logging.getLogger(__name__)


class EnergyProfileViewerDialog(QDialog):
    def __init__(self, profile: ReactionEnergyProfile,
                 reaction_name: str, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.reaction_name = reaction_name

        self.setWindowTitle(f"Energy profile: {reaction_name}")
        self.resize(1000, 680)

        lay = QVBoxLayout(self)

        header = QLabel(f"<b>{profile.title or reaction_name}</b>")
        header.setStyleSheet("font-size: 14pt; padding: 4px;")
        lay.addWidget(header)

        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setStyleSheet("background: white; border: 1px solid #ccc;")
        self.image.setMinimumSize(820, 480)
        scroll = QScrollArea()
        scroll.setWidget(self.image)
        scroll.setWidgetResizable(True)
        lay.addWidget(scroll, 1)

        info = QLabel(self._summary_text())
        info.setStyleSheet("color:#444; padding:4px; font-family: monospace;")
        info.setWordWrap(True)
        lay.addWidget(info)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save PNG / SVG…")
        save_btn.clicked.connect(self._save)
        btn_row.addStretch(1)
        btn_row.addWidget(save_btn)
        lay.addLayout(btn_row)

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        lay.addWidget(bb)

        self._render_preview()

    # ------------------------------------------------------------------

    def _summary_text(self) -> str:
        ea = self.profile.activation_energies
        dh = self.profile.delta_h
        u = self.profile.energy_unit
        lines = [f"Stationary points: {len(self.profile)}"]
        if ea:
            lines.append("Activation energies: " +
                         ", ".join(f"{v:+.0f} {u}" for v in ea))
        if dh is not None:
            lines.append(f"Overall ΔH: {dh:+.0f} {u}")
        if self.profile.source:
            lines.append(f"Source: {self.profile.source}")
        return "\n".join(lines)

    def _render_preview(self) -> None:
        try:
            with TemporaryDirectory() as d:
                out = export_profile(self.profile, Path(d) / "preview.png",
                                     width=960, height=560)
                pix = QPixmap(str(out))
            if pix.isNull():
                raise RuntimeError("pixmap load failed")
            self.image.setPixmap(pix)
        except Exception as e:  # noqa: BLE001
            log.warning("Energy profile preview failed: %s", e)
            self.image.setText(f"Render failed: {e}")

    def _save(self) -> None:
        safe = (self.reaction_name or "reaction").replace("/", "_").replace(":", "")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save energy profile",
            f"{safe}_energy.png",
            "PNG image (*.png);;SVG vector (*.svg)")
        if not path:
            return
        try:
            export_profile(self.profile, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Save failed", str(e))
