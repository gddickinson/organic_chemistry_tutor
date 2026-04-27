"""Phase GM-1.0 (round 230) — Genetics + Molecular Biology
Studio main window.

Top-level QMainWindow opened from OrgChem main window's
*Window → Genetics + Molecular Biology Studio…* menu
(Ctrl+Alt+G).  Single persistent instance — lazily
constructed, raise/focus on subsequent menu clicks.
Geometry persists via ``QSettings["window/genetics"]``.

Phase GM-1.0 tabs: **Techniques** (40-entry molecular-biology-
techniques catalogue across 14 categories) + **Cross-
references** (read-only bridge to biochem.core.enzymes
filtered to nucleic-acid-acting enzymes) + **Tutorials**.

Genetics + Molecular Biology Studio is the **seventh
sibling** in the multi-studio life-sciences platform.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar, QTabWidget, QWidget,
)

from genetics.gui.panels.techniques_panel import (
    TechniquesPanel,
)
from genetics.gui.panels.molecular_biology_bridge_panel import (
    MolecularBiologyBridgePanel,
)
from genetics.gui.panels.genetics_tutorial_panel import (
    GeneticsTutorialPanel,
)

log = logging.getLogger(__name__)

_SETTINGS_GROUP = "window/genetics"


class GeneticsMainWindow(QMainWindow):
    """Genetics + Molecular Biology Studio main window."""

    TAB_TECHNIQUES = "Techniques"
    TAB_CROSS_REFERENCES = "Cross-references"
    TAB_TUTORIALS = "Tutorials"

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle(
            "Genetics + Molecular Biology Studio")
        self.resize(1200, 780)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.techniques = TechniquesPanel()
        self.bridge = MolecularBiologyBridgePanel()
        self.tutorial = GeneticsTutorialPanel()
        self.tabs.addTab(self.techniques,
                         self.TAB_TECHNIQUES)
        self.tabs.addTab(self.bridge,
                         self.TAB_CROSS_REFERENCES)
        self.tabs.addTab(self.tutorial,
                         self.TAB_TUTORIALS)
        self.setCentralWidget(self.tabs)

        sb = QStatusBar()
        sb.showMessage(
            "Genetics + Molecular Biology Studio (Phase "
            "GM-1.0) — sibling #7 of 7.  40-entry "
            "molecular-biology-techniques catalogue across "
            "14 categories; cross-references into Biochem "
            "enzymes + Cell Bio cell-cycle + signalling + "
            "Animal Biology model organisms + OrgChem "
            "molecules."
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
