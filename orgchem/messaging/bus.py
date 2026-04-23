"""Application-wide Qt signal bus.

Single source of truth for cross-panel events. Panels never wire into each
other directly — they ``bus().some_signal.connect(...)`` and emit on the bus.
This keeps the GUI graph additive: new panels just subscribe to existing
signals without touching any other file.
"""
from __future__ import annotations
from typing import Optional
from PySide6.QtCore import QObject, Signal


class AppBus(QObject):
    # ---- selection events ------------------------------------------------
    molecule_selected = Signal(int)       # molecule DB id
    reaction_selected = Signal(int)       # reaction DB id

    # ---- data lifecycle --------------------------------------------------
    molecule_added = Signal(int)
    molecule_removed = Signal(int)
    database_changed = Signal()

    # ---- download / background ------------------------------------------
    download_started = Signal(str, str)          # source_name, query
    download_progress = Signal(str, int, int)    # source_name, current, total
    download_finished = Signal(str, int)         # source_name, num_added
    download_failed = Signal(str, str)           # source_name, error_text

    # ---- logging / user messaging ---------------------------------------
    message_posted = Signal(str, str)            # level, text

    # ---- tutorial / curriculum ------------------------------------------
    tutorial_step_changed = Signal(str, int)     # tutorial_id, step_index

    # ---- configuration --------------------------------------------------
    config_changed = Signal()                    # preferences were saved


_bus: Optional[AppBus] = None


def bus() -> AppBus:
    """Return the process-wide AppBus singleton (lazy-constructed)."""
    global _bus
    if _bus is None:
        _bus = AppBus()
    return _bus
