"""Application preferences dialog.

Centralises config choices that used to live on per-panel toolbars. Saving
writes ``AppConfig`` to disk and emits ``bus.config_changed`` so open
panels can re-render using the new settings immediately.
"""
from __future__ import annotations
import logging

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QCheckBox,
    QDialogButtonBox, QLabel,
)

from orgchem.config import AppConfig
from orgchem.messaging.bus import bus

log = logging.getLogger(__name__)


class PreferencesDialog(QDialog):
    def __init__(self, cfg: AppConfig, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self.setWindowTitle("Preferences")
        self.resize(500, 360)

        lay = QVBoxLayout(self)
        header = QLabel(
            "Global defaults for viewers, logging, and data sources. "
            "Changes apply immediately to open panels."
        )
        header.setStyleSheet("color:#555;")
        header.setWordWrap(True)
        lay.addWidget(header)

        form = QFormLayout()

        self.backend = QComboBox()
        self.backend.addItems(["3Dmol", "matplotlib"])
        self.backend.setCurrentText(cfg.default_3d_backend)
        self.backend.setToolTip(
            "3Dmol = interactive WebGL (GUI only). "
            "matplotlib = static PNG, works headlessly."
        )
        form.addRow("Default 3D backend:", self.backend)

        self.style3d = QComboBox()
        self.style3d.addItems(["stick", "ball-and-stick", "sphere", "line"])
        self.style3d.setCurrentText(cfg.default_3d_style)
        form.addRow("Default 3D style:", self.style3d)

        self.theme = QComboBox()
        self.theme.addItems(["light", "dark"])
        self.theme.setCurrentText(cfg.theme)
        self.theme.setToolTip("Dark mode is a roadmap item — light is active today.")
        form.addRow("Theme:", self.theme)

        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level.setCurrentText(cfg.log_level)
        form.addRow("Log level:", self.log_level)

        self.autogen_3d = QCheckBox("Generate 3D coordinates on import")
        self.autogen_3d.setChecked(cfg.autogen_3d_on_import)
        form.addRow("", self.autogen_3d)

        self.online = QCheckBox("Enable online data sources (PubChem, …)")
        self.online.setChecked(cfg.online_sources_enabled)
        form.addRow("", self.online)

        lay.addLayout(form)
        lay.addStretch(1)

        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self._accept)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)

    def _accept(self) -> None:
        self.cfg.default_3d_backend = self.backend.currentText()
        self.cfg.default_3d_style = self.style3d.currentText()
        self.cfg.theme = self.theme.currentText()
        self.cfg.log_level = self.log_level.currentText()
        self.cfg.autogen_3d_on_import = self.autogen_3d.isChecked()
        self.cfg.online_sources_enabled = self.online.isChecked()
        try:
            self.cfg.save()
        except Exception:  # noqa: BLE001
            log.exception("Saving preferences failed")
        bus().config_changed.emit()
        log.info("Preferences updated")
        self.accept()
