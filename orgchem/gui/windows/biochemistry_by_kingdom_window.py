"""Phase 47b (round 167) — Biochemistry-by-Kingdom window.

Per user directive (2026-04-25, round 165): a second top-level
Macromolecules-window-style explorer that organises
biochemistry by **kingdom of life** rather than by molecular
class.  Top-level `QMainWindow` with one outer tab per kingdom
(Eukarya / Bacteria / Archaea / Viruses); each kingdom tab
hosts a `KingdomSubtabPanel` with three sub-tabs (Structure /
Physiology+Development / Genetics+Evolution).

Single persistent instance (not modal) — constructed lazily on
first access, then raised / focused on subsequent opens.
Geometry + last-active outer tab persist via `QSettings` under
the key family ``window/biochemistry_by_kingdom``.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget

from orgchem.core.biochemistry_by_kingdom import kingdoms
from orgchem.gui.panels.kingdom_subtab_panel import (
    KingdomSubtabPanel,
)

log = logging.getLogger(__name__)


_SETTINGS_GROUP = "window/biochemistry_by_kingdom"


_KINGDOM_LABELS = {
    "eukarya": "Eukarya",
    "bacteria": "Bacteria",
    "archaea": "Archaea",
    "viruses": "Viruses",
}


class BiochemistryByKingdomWindow(QMainWindow):
    """Top-level secondary window grouping the four kingdom
    explorers."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle(
            "Biochemistry by Kingdom — OrgChem Studio")
        self.resize(1180, 780)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self._panels: dict[str, KingdomSubtabPanel] = {}
        for kid in kingdoms():
            panel = KingdomSubtabPanel(kid)
            self._panels[kid] = panel
            self.tabs.addTab(panel,
                             _KINGDOM_LABELS.get(kid, kid))
        self.setCentralWidget(self.tabs)

        self._restore_state()

    # ---------------- navigation ------------------------------

    def switch_to_kingdom(self, kingdom: str) -> bool:
        """Focus the outer tab for a given kingdom id."""
        panel = self._panels.get(kingdom)
        if panel is None:
            return False
        for i in range(self.tabs.count()):
            if self.tabs.widget(i) is panel:
                self.tabs.setCurrentIndex(i)
                return True
        return False

    def select_topic(
        self,
        kingdom: str,
        subtab: str,
        topic_id: str,
    ) -> bool:
        """Focus the kingdom + subtab + select the topic."""
        if not self.switch_to_kingdom(kingdom):
            return False
        return self._panels[kingdom].select_topic(
            subtab, topic_id)

    def kingdom_panel(
        self,
        kingdom: str,
    ) -> Optional[KingdomSubtabPanel]:
        """Return the per-kingdom panel widget."""
        return self._panels.get(kingdom)

    def kingdom_labels(self) -> list[str]:
        return [self.tabs.tabText(i)
                for i in range(self.tabs.count())]

    # ---------------- lifecycle -------------------------------

    def showEvent(self, event) -> None:  # noqa: N802 — Qt
        super().showEvent(event)
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event) -> None:  # noqa: N802 — Qt
        self._save_state()
        super().closeEvent(event)

    # ---------------- state persistence -----------------------

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
