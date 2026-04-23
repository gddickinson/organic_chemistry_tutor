"""Unified Macromolecules window — Phase 30.

Per user directive (2026-04-23): proteins, carbohydrates, lipids,
and nucleic-acids live in a dedicated secondary window rather than
crowding the main-window tabbar. The window is a *single persistent
instance* (not modal) — constructed lazily on first access, then
raised/focused on subsequent menu clicks.

The four inner tabs host the same panels wired under Phase 24 /
Phase 29b / Phase 29c. The panels themselves are unchanged — the
main window still exposes them as attributes (``win.proteins`` etc.)
so existing agent actions and cross-panel messaging keep working.

Geometry + last-active-tab are persisted via ``QSettings`` under
the key family ``window/macromolecules``.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget

log = logging.getLogger(__name__)


_SETTINGS_GROUP = "window/macromolecules"


class MacromoleculesWindow(QMainWindow):
    """Secondary window grouping the four macromolecule workspaces.

    Parameters
    ----------
    panels:
        Mapping of tab-label → already-constructed panel widget.
        The main window creates the panels once and hands them over;
        this window just arranges them in a QTabWidget.
    parent:
        Optional parent (usually the main window). Setting a parent
        keeps the window centred on top of the main app and ensures
        it is destroyed with the app.
    """

    TAB_PROTEINS = "Proteins"
    TAB_CARBOHYDRATES = "Carbohydrates"
    TAB_LIPIDS = "Lipids"
    TAB_NUCLEIC_ACIDS = "Nucleic acids"

    def __init__(
        self,
        panels: dict[str, QWidget],
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        # On macOS, `Qt.Window` keeps the window in the app's window
        # list (separate from a modal dialog) and respects Cmd+W.
        self.setWindowFlag(Qt.Window, True)
        self.setWindowTitle("Macromolecules — OrgChem Studio")
        self.resize(1120, 760)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        # Preserve the canonical ordering — Proteins first since it is
        # the richest tab (PDB / pockets / contacts / 3D / PPI).
        for label in (
            self.TAB_PROTEINS,
            self.TAB_CARBOHYDRATES,
            self.TAB_LIPIDS,
            self.TAB_NUCLEIC_ACIDS,
        ):
            widget = panels.get(label)
            if widget is not None:
                self.tabs.addTab(widget, label)
        self.setCentralWidget(self.tabs)

        self._restore_state()

    # ---------------- navigation ----------------------------------

    def switch_to(self, label: str) -> bool:
        """Focus the inner tab with the given label.

        Returns True if the tab was found, False otherwise. Used by
        the Nucleic-acids panel's *Fetch PDB in Proteins tab* button
        so clicks keep the user inside this window.
        """
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == label:
                self.tabs.setCurrentIndex(i)
                return True
        return False

    # ---------------- lifecycle -----------------------------------

    def showEvent(self, event) -> None:  # noqa: N802 — Qt convention
        super().showEvent(event)
        # Bring the window to front on every open so a second click
        # of the menu raises it even when already shown but buried.
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
