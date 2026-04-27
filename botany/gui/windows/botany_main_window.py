"""Phase BT-1.0 (round 216) — Botany Studio main window.

Top-level QMainWindow opened from OrgChem main window's
*Window → Botany Studio…* menu (Ctrl+Shift+V).  Single
persistent instance — lazily constructed, raise/focus on
subsequent menu clicks.  Geometry persists via
``QSettings["window/botany"]``.

Phase BT-1.0 tabs: **Plant taxa** (30 entries × 6 divisions) +
**Plant secondary metabolites** (live DB-read bridge filtered
to plant-derived natural products) + **Tutorials**.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QTabWidget, QWidget,
)

from botany.gui.panels.plant_taxa_panel import PlantTaxaPanel
from botany.gui.panels.plant_hormones_panel import (
    PlantHormonesPanel,
)
from botany.gui.panels.plant_metabolites_panel import (
    PlantMetabolitesPanel,
)
from botany.gui.panels.botany_tutorial_panel import (
    BotanyTutorialPanel,
)

log = logging.getLogger(__name__)

_SETTINGS_GROUP = "window/botany"


class BotanyMainWindow(QMainWindow):
    """Botany Studio main window."""

    TAB_PLANT_TAXA = "Plant taxa"
    TAB_PLANT_HORMONES = "Plant hormones"
    TAB_METABOLITES = "Plant secondary metabolites"
    TAB_TUTORIALS = "Tutorials"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Botany Studio")
        self.resize(1200, 780)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.plant_taxa = PlantTaxaPanel()
        self.plant_hormones = PlantHormonesPanel()
        self.metabolites = PlantMetabolitesPanel()
        self.tutorial = BotanyTutorialPanel()
        self.tabs.addTab(self.plant_taxa, self.TAB_PLANT_TAXA)
        self.tabs.addTab(self.plant_hormones,
                         self.TAB_PLANT_HORMONES)
        self.tabs.addTab(self.metabolites, self.TAB_METABOLITES)
        self.tabs.addTab(self.tutorial, self.TAB_TUTORIALS)
        self.setCentralWidget(self.tabs)

        sb = QStatusBar()
        sb.showMessage(
            "Botany Studio (Phase BT-1.0 + BT-2.0) — sibling "
            "#5 of 6.  Plant-hormones tab added in BT-2.0; "
            "Plant-secondary-metabolites tab reads "
            "orgchem.db.Molecule rows live; plant-taxa entries "
            "carry typed cross-references into orgchem "
            "molecules + metabolic pathways + pharm drug "
            "classes."
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
