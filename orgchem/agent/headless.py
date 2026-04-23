"""Headless app runner — launches the full app without a visible display.

Used for (a) automated tests and (b) external LLMs (e.g. a Claude Code
session) driving the app programmatically.

Usage
-----
    from orgchem.agent.headless import HeadlessApp

    with HeadlessApp() as app:
        app.call("show_molecule", name_or_id="Caffeine")
        details = app.call("get_molecule_details", molecule_id=7)

``HeadlessApp`` ensures the Qt off-screen platform is active **before** Qt is
imported, which means it also works in CI containers with no display server.
"""
from __future__ import annotations
import os
import sys
import logging
from typing import Any

log = logging.getLogger(__name__)


def _force_offscreen() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    # Chromium's GPU process can't hold a context under ``offscreen`` — force
    # software rendering so QWebEngineView stays alive across multiple page
    # loads (i.e. molecule switches).
    #
    # Caveat: disabling the GPU means 3Dmol.js (which needs WebGL) will not
    # render the molecule in headless mode. The 3D panel will appear blank in
    # screenshot tours. All 2D views, property tables, and GUI panel layouts
    # work normally. For interactive 3D, run ``python main.py`` (no --headless)
    # where Chromium gets a real GPU context and 3Dmol.js renders properly.
    flags = os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "")
    extras = "--disable-gpu --disable-gpu-compositing --no-sandbox"
    if "--disable-gpu" not in flags:
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (flags + " " + extras).strip()


class HeadlessApp:
    def __init__(self, show: bool = False):
        _force_offscreen()
        # Late imports so QT_QPA_PLATFORM is honoured.
        from PySide6.QtWidgets import QApplication
        from orgchem.config import AppConfig
        from orgchem.logging_setup import setup_logging
        from orgchem.db.session import init_db
        from orgchem.db.seed import seed_if_empty
        from orgchem.gui.main_window import MainWindow
        from orgchem.agent import actions  # noqa: F401 — force registry import

        self.cfg = AppConfig.load()
        setup_logging(self.cfg)
        init_db(self.cfg)
        seed_if_empty(self.cfg)

        self._app = QApplication.instance() or QApplication(sys.argv)
        self._app.setApplicationName("OrgChem Studio (headless)")
        self.window = MainWindow(self.cfg)
        if show:
            self.window.show()

    # ------------------------------------------------------------------
    # Public API — invoke any registered action by name.
    def call(self, action_name: str, **kwargs: Any) -> Any:
        from orgchem.agent.actions import invoke
        # Pump the event loop briefly so signal handlers get to run before
        # we compute a result.
        result = invoke(action_name, **kwargs)
        self.pump(times=3)
        return result

    def pump(self, times: int = 1) -> None:
        for _ in range(times):
            self._app.processEvents()

    def shutdown(self) -> None:
        self.window.close()
        self.pump(2)

    # ------------------------------------------------------------------
    # Context-manager sugar.
    def __enter__(self) -> "HeadlessApp":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.shutdown()
