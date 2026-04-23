"""OrgChem Studio — application entry point.

Modes
-----
- ``python main.py``                — normal desktop GUI.
- ``python main.py --agent-stdio``  — headless; reads JSON-per-line requests on
                                      stdin and writes JSON responses on stdout.
                                      Intended for external LLMs (incl. a
                                      Claude Code session driving it as a
                                      subprocess).
- ``python main.py --headless``     — starts the app with the off-screen Qt
                                      platform. Useful for CI smoke tests.
"""
from __future__ import annotations
import argparse
import logging
import os
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="orgchem")
    parser.add_argument("--agent-stdio", action="store_true",
                        help="Run the JSON-over-stdio agent bridge")
    parser.add_argument("--headless", action="store_true",
                        help="Use the off-screen Qt platform (no visible window)")
    parser.add_argument("--show-window", action="store_true",
                        help="With --agent-stdio, also show the window (debug)")
    args = parser.parse_args(argv)

    if args.headless or args.agent_stdio:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    if args.agent_stdio:
        # Late import so the Qt platform override is honoured.
        from orgchem.agent.bridge import run
        return run(show=args.show_window)

    # ---- Normal GUI launch ------------------------------------------
    from PySide6.QtWidgets import QApplication
    from orgchem.config import AppConfig
    from orgchem.logging_setup import setup_logging
    from orgchem.db.session import init_db
    from orgchem.db.seed import seed_if_empty
    from orgchem.gui.main_window import MainWindow
    from orgchem.agent import library  # noqa: F401 — register actions

    cfg = AppConfig.load()
    setup_logging(cfg)
    log = logging.getLogger("orgchem.main")

    init_db(cfg)
    log.info("Database ready at %s", cfg.db_path)
    seed_if_empty(cfg)

    app = QApplication(sys.argv)
    app.setApplicationName("OrgChem Studio")
    app.setOrganizationName("OrgChem")

    win = MainWindow(cfg)
    win.show()
    log.info("UI shown — entering Qt event loop")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
