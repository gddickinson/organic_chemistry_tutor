"""Phase AB-1.0 (round 217) — Animal Biology Studio main window.

Top-level QMainWindow opened from OrgChem main window's
*Window → Animal Biology Studio…* menu (Ctrl+Shift+X).  Single
persistent instance — lazily constructed, raise/focus on
subsequent menu clicks.  Geometry persists via
``QSettings["window/animal"]``.

Phase AB-1.0 tabs: **Animal taxa** (30 entries × 9 phyla) +
**Cell signalling bridge** (read-only view of cellbio.core.
cell_signaling filtered to animal-developmental + apoptosis +
immune pathways) + **Tutorials**.

Animal Biology Studio is the **sixth + final sibling** in the
multi-studio life-sciences platform.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QTabWidget, QWidget,
)

from animal.gui.panels.animal_taxa_panel import AnimalTaxaPanel
from animal.gui.panels.organ_systems_panel import (
    OrganSystemsPanel,
)
from animal.gui.panels.cellbio_signaling_bridge_panel import (
    CellBioSignalingBridgePanel,
)
from animal.gui.panels.animal_tutorial_panel import (
    AnimalTutorialPanel,
)

log = logging.getLogger(__name__)

_SETTINGS_GROUP = "window/animal"


class AnimalMainWindow(QMainWindow):
    """Animal Biology Studio main window."""

    TAB_ANIMAL_TAXA = "Animal taxa"
    TAB_ORGAN_SYSTEMS = "Organ systems"
    TAB_SIGNALLING_BRIDGE = "Cell signalling bridge"
    TAB_TUTORIALS = "Tutorials"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Animal Biology Studio")
        self.resize(1200, 780)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.animal_taxa = AnimalTaxaPanel()
        self.organ_systems = OrganSystemsPanel()
        self.signalling_bridge = CellBioSignalingBridgePanel()
        self.tutorial = AnimalTutorialPanel()
        self.tabs.addTab(self.animal_taxa,
                         self.TAB_ANIMAL_TAXA)
        self.tabs.addTab(self.organ_systems,
                         self.TAB_ORGAN_SYSTEMS)
        self.tabs.addTab(self.signalling_bridge,
                         self.TAB_SIGNALLING_BRIDGE)
        self.tabs.addTab(self.tutorial, self.TAB_TUTORIALS)
        self.setCentralWidget(self.tabs)

        sb = QStatusBar()
        sb.showMessage(
            "Animal Biology Studio (Phase AB-1.0 + AB-2.0) — "
            "sibling #6 of 6, COMPLETES THE PLATFORM.  "
            "Organ-systems tab added in AB-2.0; Cell-"
            "signalling-bridge tab reads cellbio.core."
            "cell_signaling; animal-taxa entries carry typed "
            "cross-references into orgchem molecules + "
            "cellbio signalling pathways + biochem enzymes."
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
