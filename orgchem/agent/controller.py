"""Process-wide pointer to the running :class:`MainWindow`.

Agent actions that must reach into the GUI (take a screenshot, raise a
panel, export the currently-selected molecule) call :func:`main_window` or
:func:`require_main_window` here. The main window calls
:func:`set_main_window` from its ``__init__``. In pure-headless / no-GUI
contexts, ``main_window()`` returns ``None``.

Keeping this in a tiny separate module avoids a circular import between
``agent.library`` and ``gui.main_window``.
"""
from __future__ import annotations
from typing import Optional

from PySide6.QtWidgets import QMainWindow

_main_window: Optional[QMainWindow] = None


def set_main_window(win: QMainWindow) -> None:
    """Register the running MainWindow instance."""
    global _main_window
    _main_window = win


def main_window() -> Optional[QMainWindow]:
    return _main_window


def require_main_window() -> QMainWindow:
    w = _main_window
    if w is None:
        raise RuntimeError(
            "Main window not registered — an action that needs the GUI "
            "was invoked before MainWindow was constructed."
        )
    return w
