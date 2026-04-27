"""Phase BC-1.0 → BC-2.0 (rounds 213, 219) — Biochem Studio
main window.

Top-level QMainWindow opened from OrgChem main window's
*Window → Biochem Studio…* menu (Ctrl+Shift+Y).  Single
persistent instance — lazily constructed, raise/focus on
subsequent menu clicks.  Geometry persists via
``QSettings["window/biochem"]``.

Tabs: **Enzymes** (BC-1.0, 30-entry EC catalogue) +
**Cofactors** (BC-2.0, 27-entry catalogue covering NAD/FAD/CoA/
SAM/ATP/B-vitamin prosthetic groups/metals/quinones/redox
buffers) + **Metabolic pathways** (BC-1.0, read-only bridge to
OrgChem Phase 42) + **Tutorials**.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QTabWidget, QWidget,
)

from biochem.gui.panels.enzymes_panel import EnzymesPanel
from biochem.gui.panels.cofactors_panel import CofactorsPanel
from biochem.gui.panels.metabolic_bridge_panel import (
    MetabolicBridgePanel,
)
from biochem.gui.panels.biochem_tutorial_panel import (
    BiochemTutorialPanel,
)

log = logging.getLogger(__name__)

_SETTINGS_GROUP = "window/biochem"


class BiochemMainWindow(QMainWindow):
    """Biochem Studio main window."""

    TAB_ENZYMES = "Enzymes"
    TAB_COFACTORS = "Cofactors"
    TAB_PATHWAYS = "Metabolic pathways"
    TAB_TUTORIALS = "Tutorials"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Biochemistry Studio")
        self.resize(1200, 780)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.enzymes = EnzymesPanel()
        self.cofactors = CofactorsPanel()
        self.pathways = MetabolicBridgePanel()
        self.tutorial = BiochemTutorialPanel()
        self.tabs.addTab(self.enzymes, self.TAB_ENZYMES)
        self.tabs.addTab(self.cofactors, self.TAB_COFACTORS)
        self.tabs.addTab(self.pathways, self.TAB_PATHWAYS)
        self.tabs.addTab(self.tutorial, self.TAB_TUTORIALS)
        self.setCentralWidget(self.tabs)

        sb = QStatusBar()
        sb.showMessage(
            "Biochem Studio (Phase BC-1.0 + BC-2.0) — sibling "
            "to OrgChem + Cell Bio.  Cofactors tab added in "
            "BC-2.0; Metabolic-pathways tab bridges to "
            "orgchem.core.metabolic_pathways."
        )
        self.setStatusBar(sb)

        self._restore_state()

    def switch_to(self, label: str) -> bool:
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == label:
                self.tabs.setCurrentIndex(i)
                return True
        return False

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event) -> None:  # noqa: N802
        self._save_state()
        super().closeEvent(event)

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
