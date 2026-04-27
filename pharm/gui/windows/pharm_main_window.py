"""Phase PH-1.0 (round 214) — Pharmacology Studio main window.

Top-level QMainWindow opened from OrgChem main window's
*Window → Pharmacology Studio…* menu (Ctrl+Shift+H).  Single
persistent instance — lazily constructed, raise/focus on
subsequent menu clicks.  Geometry persists via
``QSettings["window/pharm"]``.

Phase PH-1.0 tabs: **Drug classes** (30 entries × 11
therapeutic areas) + **Bridges** (sub-tabbed view: Biochem
enzymes + Cell Bio signalling) + **Tutorials**.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QTabWidget, QVBoxLayout, QWidget,
)

from pharm.gui.panels.drug_classes_panel import DrugClassesPanel
from pharm.gui.panels.receptors_panel import ReceptorsPanel
from pharm.gui.panels.biochem_bridge_panel import (
    BiochemBridgePanel,
)
from pharm.gui.panels.cellbio_bridge_panel import (
    CellBioBridgePanel,
)
from pharm.gui.panels.pharm_tutorial_panel import (
    PharmTutorialPanel,
)

log = logging.getLogger(__name__)

_SETTINGS_GROUP = "window/pharm"


class _BridgesContainer(QWidget):
    """Sub-tabbed container for the two bridge panels.  Splits
    them so the user can flip between them without navigating
    away from the Bridges tab in the parent QTabWidget."""

    def __init__(
        self,
        biochem: BiochemBridgePanel,
        cellbio: CellBioBridgePanel,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.inner = QTabWidget()
        self.inner.addTab(biochem, "Biochem enzymes")
        self.inner.addTab(cellbio, "Cell Bio signalling")
        layout.addWidget(self.inner)

    def switch_inner(self, label: str) -> bool:
        for i in range(self.inner.count()):
            if self.inner.tabText(i) == label:
                self.inner.setCurrentIndex(i)
                return True
        return False


class PharmMainWindow(QMainWindow):
    """Pharmacology Studio main window."""

    TAB_DRUG_CLASSES = "Drug classes"
    TAB_RECEPTORS = "Receptors"
    TAB_BRIDGES = "Bridges"
    TAB_TUTORIALS = "Tutorials"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Pharmacology Studio")
        self.resize(1200, 780)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.drug_classes = DrugClassesPanel()
        self.receptors = ReceptorsPanel()
        self.biochem_bridge = BiochemBridgePanel()
        self.cellbio_bridge = CellBioBridgePanel()
        self.bridges = _BridgesContainer(
            self.biochem_bridge, self.cellbio_bridge)
        self.tutorial = PharmTutorialPanel()
        self.tabs.addTab(self.drug_classes,
                         self.TAB_DRUG_CLASSES)
        self.tabs.addTab(self.receptors, self.TAB_RECEPTORS)
        self.tabs.addTab(self.bridges, self.TAB_BRIDGES)
        self.tabs.addTab(self.tutorial, self.TAB_TUTORIALS)
        self.setCentralWidget(self.tabs)

        sb = QStatusBar()
        sb.showMessage(
            "Pharmacology Studio (Phase PH-1.0 + PH-2.0) — "
            "sibling #3 of 6.  Receptors tab added in PH-2.0; "
            "Bridges tab reads biochem.core.enzymes + "
            "cellbio.core.cell_signaling read-only."
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
