"""Phase CB-1.0 → CB-2.0 (rounds 212, 218) — Cell Bio Studio
main window.

Top-level QMainWindow opened from the OrgChem main window's
*Window → Cell Biology Studio…* menu (Ctrl+Shift+B).  Single
persistent instance — lazily constructed, raise/focus on
subsequent menu clicks.  Geometry + last-active tab persist via
``QSettings["window/cellbio"]``.

Tabs: **Signalling** (CB-1.0, 26-pathway catalogue) +
**Cell cycle** (CB-2.0, 30-entry catalogue — phases /
checkpoints / cyclin-CDKs / DDR) + **Tutorials**.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QTabWidget, QWidget,
)

from cellbio.gui.panels.signaling_panel import SignalingPanel
from cellbio.gui.panels.cell_cycle_panel import CellCyclePanel
from cellbio.gui.panels.cellbio_tutorial_panel import (
    CellBioTutorialPanel,
)

log = logging.getLogger(__name__)


_SETTINGS_GROUP = "window/cellbio"


class CellBioMainWindow(QMainWindow):
    """Cell Biology Studio main window."""

    TAB_SIGNALLING = "Signalling"
    TAB_CELL_CYCLE = "Cell cycle"
    TAB_TUTORIALS = "Tutorials"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Cell Biology Studio")
        self.resize(1100, 760)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.signaling = SignalingPanel()
        self.cell_cycle = CellCyclePanel()
        self.tutorial = CellBioTutorialPanel()
        self.tabs.addTab(self.signaling, self.TAB_SIGNALLING)
        self.tabs.addTab(self.cell_cycle, self.TAB_CELL_CYCLE)
        self.tabs.addTab(self.tutorial, self.TAB_TUTORIALS)
        self.setCentralWidget(self.tabs)

        sb = QStatusBar()
        sb.showMessage(
            "Cell Bio Studio (Phase CB-1.0 + CB-2.0) — "
            "sibling to OrgChem Studio.  Cell cycle tab "
            "added in CB-2.0.")
        self.setStatusBar(sb)

        self._restore_state()

    # ---------------- navigation ----------------------------------

    def switch_to(self, label: str) -> bool:
        """Focus the inner tab with the given label.  Returns True
        if found."""
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == label:
                self.tabs.setCurrentIndex(i)
                return True
        return False

    # ---------------- lifecycle -----------------------------------

    def showEvent(self, event) -> None:  # noqa: N802 — Qt convention
        super().showEvent(event)
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event) -> None:  # noqa: N802 — Qt convention
        self._save_state()
        super().closeEvent(event)

    # ---------------- state persistence ---------------------------

    def _save_state(self) -> None:
        s = QSettings()
        s.beginGroup(_SETTINGS_GROUP)
        s.setValue("geometry", self.saveGeometry())
        s.setValue("tab_index", self.tabs.currentIndex())
        s.endGroup()

    def _restore_state(self) -> None:
        s = QSettings()
        s.beginGroup(_SETTINGS_GROUP)
        geom = s.value("geometry", None)
        if isinstance(geom, (QByteArray, bytes)):
            self.restoreGeometry(QByteArray(geom))
        idx_val = s.value("tab_index", 0)
        try:
            idx = int(idx_val)
        except (TypeError, ValueError):
            idx = 0
        if 0 <= idx < self.tabs.count():
            self.tabs.setCurrentIndex(idx)
        s.endGroup()
