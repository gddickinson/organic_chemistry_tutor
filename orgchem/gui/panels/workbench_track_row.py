"""Phase 32c — per-track row widget for the Workbench tracks list.

Each row in :class:`~orgchem.gui.panels.workbench.WorkbenchWidget`'s
tracks list carries a :class:`TrackRow` with inline controls:

* **Visibility checkbox** — toggles ``Track.visible`` on the Scene.
* **Name label** — the track's user-facing name.
* **Style combo** — switches rendering style (stick / sphere /
  cartoon / surface / …) by calling ``scene.set_style``.
* **Remove button** — drops the track from the Scene.

Kept out of ``workbench.py`` so that file stays comfortably under
the 500-line project cap and the row widget can be reused by any
future Scene-aware panel (e.g. a mini-viewer inside the Compare
tab).
"""
from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QToolButton, QWidget,
)

from orgchem.scene import Track
from orgchem.scene.scene import TrackKind

log = logging.getLogger(__name__)


#: Style choices surfaced by the combo-box.  Keyed per TrackKind so
#: small molecules don't get "cartoon" offered and proteins don't
#: get "line".  The default per kind matches what ``Scene.add_*``
#: already uses.
_STYLE_CHOICES = {
    TrackKind.MOLECULE: ["stick", "ball-and-stick", "sphere", "line"],
    TrackKind.LIGAND:   ["stick", "ball-and-stick", "sphere"],
    TrackKind.PROTEIN:  ["cartoon", "trace", "surface", "stick"],
}


class TrackRow(QWidget):
    """Row-widget that represents one :class:`Track` in the tracks
    list.  Emits a signal per user action so the parent panel can
    forward to the Scene.

    All signals carry the track's name (the stable identifier
    across scene mutations).
    """

    visibility_toggled = Signal(str, bool)    # (track_name, visible)
    style_changed = Signal(str, str)          # (track_name, new_style)
    remove_clicked = Signal(str)              # (track_name,)

    def __init__(self, track: Track,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._track_name = track.name
        self._build_ui(track)

    # ---- UI -----------------------------------------------------
    def _build_ui(self, track: Track) -> None:
        lay = QHBoxLayout(self)
        lay.setContentsMargins(4, 2, 4, 2)
        lay.setSpacing(6)

        self._check = QCheckBox(self)
        self._check.setChecked(track.visible)
        self._check.setToolTip(
            "Show / hide this track in the 3Dmol.js view.")
        self._check.toggled.connect(
            lambda v: self.visibility_toggled.emit(self._track_name, v))
        lay.addWidget(self._check)

        self._label = QLabel(self._label_text(track), self)
        self._label.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        self._label.setStyleSheet("color: #ddd;")
        lay.addWidget(self._label, 1)

        self._style = QComboBox(self)
        choices = _STYLE_CHOICES.get(track.kind,
                                     _STYLE_CHOICES[TrackKind.MOLECULE])
        self._style.addItems(choices)
        if track.style in choices:
            self._style.setCurrentText(track.style)
        else:
            self._style.addItem(track.style)
            self._style.setCurrentText(track.style)
        self._style.setToolTip("Rendering style for this track.")
        self._style.currentTextChanged.connect(
            lambda s: self.style_changed.emit(self._track_name, s))
        lay.addWidget(self._style)

        self._remove = QToolButton(self)
        self._remove.setText("✕")
        self._remove.setToolTip("Remove this track from the scene.")
        self._remove.clicked.connect(
            lambda: self.remove_clicked.emit(self._track_name))
        lay.addWidget(self._remove)

    @staticmethod
    def _label_text(track: Track) -> str:
        subtitle = ""
        if track.meta.get("smiles"):
            subtitle = f"  {track.meta['smiles']}"
        elif track.meta.get("pdb_id"):
            subtitle = f"  {track.meta['pdb_id'].upper()}"
        return f"<b>{track.name}</b>  <i>({track.kind.value})</i>{subtitle}"

    # ---- Mutators (called by parent after a Scene event) --------
    def reflect(self, track: Track) -> None:
        """Re-sync controls after the Scene has changed this track
        (so external mutations stay visible in the UI)."""
        was_checked = self._check.isChecked()
        self._check.blockSignals(True)
        self._check.setChecked(track.visible)
        self._check.blockSignals(False)
        if was_checked != track.visible:
            pass  # state changed externally — no signal needed

        self._style.blockSignals(True)
        if self._style.findText(track.style) < 0:
            self._style.addItem(track.style)
        self._style.setCurrentText(track.style)
        self._style.blockSignals(False)

        self._label.setText(self._label_text(track))

    @property
    def track_name(self) -> str:
        return self._track_name
