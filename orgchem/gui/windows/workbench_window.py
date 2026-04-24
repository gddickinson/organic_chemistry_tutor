"""Phase 32b — Detached Workbench window.

Standalone ``QMainWindow`` host for :class:`~orgchem.gui.panels.workbench.WorkbenchWidget`
when the user clicks *Detach as window*.  Re-emits the widget's
``reattach_requested`` signal so ``MainWindow`` knows to pull the
widget back into its tabbar.

Geometry persists via ``QSettings("window/workbench/…")`` so the
window opens in the same spot on next launch.
"""
from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import QSettings, Signal
from PySide6.QtWidgets import QMainWindow, QWidget

log = logging.getLogger(__name__)


class WorkbenchWindow(QMainWindow):
    """Top-level window that hosts a :class:`WorkbenchWidget`.

    The widget is passed in (not created here), so ``MainWindow``
    can move the exact same widget instance between its tabbar
    and this window without losing the Scene or the 3Dmol.js
    camera state.

    Signals:
        reattach_requested()       — user clicked "Reattach as tab".
        closed_by_user()           — user closed the window directly
                                     via the window-frame X; should
                                     be treated identically to a
                                     reattach request so the widget
                                     survives.
    """

    reattach_requested = Signal()
    closed_by_user = Signal()

    _SETTINGS_KEY_GEOM = "window/workbench/geometry"

    def __init__(self, widget: QWidget,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Workbench — detached")
        self.resize(980, 640)
        self.setCentralWidget(widget)

        # Hook the widget's Reattach button straight through.
        if hasattr(widget, "reattach_requested"):
            widget.reattach_requested.connect(
                self.reattach_requested.emit)

        self._restore_geometry()

    def _restore_geometry(self) -> None:
        s = QSettings()
        geom = s.value(self._SETTINGS_KEY_GEOM)
        if geom is not None:
            self.restoreGeometry(geom)

    def _save_geometry(self) -> None:
        s = QSettings()
        s.setValue(self._SETTINGS_KEY_GEOM, self.saveGeometry())

    def closeEvent(self, event) -> None:   # noqa: N802 — Qt API
        self._save_geometry()
        self.closed_by_user.emit()
        # Do NOT let Qt actually delete the central widget — the
        # main window still needs it to reattach.
        self.takeCentralWidget()
        super().closeEvent(event)
