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
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QCheckBox, QColorDialog, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QSlider, QToolButton, QWidget,
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


#: Colour-scheme choices by kind.  Small molecules only benefit
#: from CPK (atom-identity) colouring plus a few custom hex
#: options; proteins get the cartoon-specific schemes too.
_COLOUR_CHOICES = {
    TrackKind.MOLECULE: ["cpk", "white", "grey", "red", "blue",
                         "green", "orange", "magenta"],
    TrackKind.LIGAND:   ["cpk", "white", "grey", "red", "blue",
                         "green", "orange", "magenta"],
    TrackKind.PROTEIN:  ["chain", "spectrum", "residue", "cpk",
                         "red", "blue", "green", "orange"],
}

#: Approximate hex for each named colour — used to paint the
#: swatch button's background so the user sees the chosen hue at
#: a glance.  Maps every entry in _COLOUR_CHOICES + the schemes
#: from `_STYLE_CHOICES` / 3Dmol.js's own palette.  cpk / chain /
#: spectrum / residue render as a multi-colour gradient, so the
#: swatch gets a neutral grey placeholder.
_SWATCH_HEX = {
    "cpk":      "#888888",
    "chain":    "#888888",
    "spectrum": "#888888",
    "residue":  "#888888",
    "white":    "#eeeeee",
    "grey":     "#888888",
    "red":      "#cc3333",
    "blue":     "#3355cc",
    "green":    "#339944",
    "orange":   "#cc8833",
    "magenta":  "#cc33aa",
    "yellow":   "#dddd33",
    "cyan":     "#33aacc",
    "purple":   "#663399",
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
    colour_changed = Signal(str, str)         # (track_name, new_colour)
    opacity_changed = Signal(str, float)      # (track_name, 0.0-1.0)
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

        # Colour combo — kind-aware + a "custom…" sentinel that
        # pops a QColorDialog for a free-choice hex pick.
        self._colour = QComboBox(self)
        col_choices = _COLOUR_CHOICES.get(track.kind,
                                          _COLOUR_CHOICES[TrackKind.MOLECULE])
        self._colour.addItems(col_choices + ["custom…"])
        if track.colour in col_choices:
            self._colour.setCurrentText(track.colour)
        else:
            # Custom hex / unknown name — show it as a literal entry.
            self._colour.insertItem(0, track.colour)
            self._colour.setCurrentText(track.colour)
        self._colour.setToolTip(
            "Colour scheme.  Named schemes (cpk / chain / spectrum) "
            "or a plain hue; pick 'custom…' for a QColorDialog-"
            "selected hex code.")
        self._colour.activated.connect(self._on_colour_activated)
        lay.addWidget(self._colour)

        # Tiny swatch label to show the current colour at a glance.
        self._swatch = QLabel(" ", self)
        self._swatch.setFixedWidth(14)
        self._swatch.setToolTip("Preview of the current colour.")
        self._apply_swatch(track.colour)
        lay.addWidget(self._swatch)

        # Opacity slider 0-100 % mapped to 0.0-1.0.
        self._opacity = QSlider(Qt.Horizontal, self)
        self._opacity.setRange(10, 100)     # below 10 % is invisible
        self._opacity.setValue(int(round(track.opacity * 100)))
        self._opacity.setFixedWidth(60)
        self._opacity.setToolTip(
            f"Opacity: {int(track.opacity * 100)} %")
        self._opacity.valueChanged.connect(self._on_opacity_changed)
        lay.addWidget(self._opacity)

        self._remove = QToolButton(self)
        self._remove.setText("✕")
        self._remove.setToolTip("Remove this track from the scene.")
        self._remove.clicked.connect(
            lambda: self.remove_clicked.emit(self._track_name))
        lay.addWidget(self._remove)

    # ---- colour + opacity handlers ------------------------------
    def _on_colour_activated(self, idx: int) -> None:
        """Combo selection handler.  'custom…' pops QColorDialog;
        all other entries propagate verbatim."""
        text = self._colour.itemText(idx)
        if text == "custom…":
            col = QColorDialog.getColor(
                QColor("#888888"), self,
                "Pick a colour for this track")
            if not col.isValid():
                return
            hex_code = col.name()    # e.g. "#8833aa"
            # Insert / select the hex entry as a named colour.
            if self._colour.findText(hex_code) < 0:
                self._colour.insertItem(0, hex_code)
            self._colour.setCurrentText(hex_code)
            self._apply_swatch(hex_code)
            self.colour_changed.emit(self._track_name, hex_code)
            return
        self._apply_swatch(text)
        self.colour_changed.emit(self._track_name, text)

    def _on_opacity_changed(self, pct: int) -> None:
        value = max(pct, 10) / 100.0
        self._opacity.setToolTip(f"Opacity: {pct} %")
        self.opacity_changed.emit(self._track_name, value)

    def _apply_swatch(self, colour: str) -> None:
        """Paint the preview label with *colour* (named or hex)."""
        hex_code = (_SWATCH_HEX.get(colour.lower())
                    or (colour if colour.startswith("#") else "#888888"))
        self._swatch.setStyleSheet(
            f"background:{hex_code}; border: 1px solid #333;")

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

        # Mirror external colour / opacity changes too.
        self._colour.blockSignals(True)
        if self._colour.findText(track.colour) < 0:
            self._colour.insertItem(0, track.colour)
        self._colour.setCurrentText(track.colour)
        self._colour.blockSignals(False)
        self._apply_swatch(track.colour)

        self._opacity.blockSignals(True)
        self._opacity.setValue(int(round(track.opacity * 100)))
        self._opacity.blockSignals(False)
        self._opacity.setToolTip(f"Opacity: {int(track.opacity * 100)} %")

        self._label.setText(self._label_text(track))

    @property
    def track_name(self) -> str:
        return self._track_name
