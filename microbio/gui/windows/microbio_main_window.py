"""Phase MB-1.0 (round 215) — Microbiology Studio main window.

Top-level QMainWindow opened from OrgChem main window's
*Window → Microbiology Studio…* menu (Ctrl+Shift+N).  Single
persistent instance — lazily constructed, raise/focus on
subsequent menu clicks.  Geometry persists via
``QSettings["window/microbio"]``.

Phase MB-1.0 tabs: **Microbes** (30 entries × 5 kingdoms) +
**Antibiotic spectrum** (bridge into pharm.core.drug_classes
filtered to 6 antimicrobial classes) + **Tutorials**.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QTabWidget, QWidget,
)

from microbio.gui.panels.microbes_panel import MicrobesPanel
from microbio.gui.panels.virulence_factors_panel import (
    VirulenceFactorsPanel,
)
from microbio.gui.panels.antibiotic_spectrum_panel import (
    AntibioticSpectrumPanel,
)
from microbio.gui.panels.microbio_tutorial_panel import (
    MicrobioTutorialPanel,
)

log = logging.getLogger(__name__)

_SETTINGS_GROUP = "window/microbio"


class MicrobioMainWindow(QMainWindow):
    """Microbiology Studio main window."""

    TAB_MICROBES = "Microbes"
    TAB_VIRULENCE = "Virulence factors"
    TAB_ANTIBIOTIC_SPECTRUM = "Antibiotic spectrum"
    TAB_TUTORIALS = "Tutorials"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Microbiology Studio")
        self.resize(1200, 780)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.microbes = MicrobesPanel()
        self.virulence_factors = VirulenceFactorsPanel()
        self.antibiotic_spectrum = AntibioticSpectrumPanel()
        self.tutorial = MicrobioTutorialPanel()
        self.tabs.addTab(self.microbes, self.TAB_MICROBES)
        self.tabs.addTab(self.virulence_factors,
                         self.TAB_VIRULENCE)
        self.tabs.addTab(self.antibiotic_spectrum,
                         self.TAB_ANTIBIOTIC_SPECTRUM)
        self.tabs.addTab(self.tutorial, self.TAB_TUTORIALS)
        self.setCentralWidget(self.tabs)

        sb = QStatusBar()
        sb.showMessage(
            "Microbiology Studio (Phase MB-1.0 + MB-2.0) — "
            "sibling #4 of 6.  Virulence-factors tab added "
            "in MB-2.0; Antibiotic-spectrum tab reads "
            "pharm.core.drug_classes; microbe entries carry "
            "typed cross-references into orgchem cell "
            "components + biochem enzymes."
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
