"""Logging handler that republishes records on the Qt ``AppBus``.

The ``SessionLogPanel`` subscribes to ``bus().message_posted`` — meaning any
application code that calls ``logging.info(...)`` automatically shows up in
the GUI log without importing any GUI symbol.
"""
from __future__ import annotations
import logging

from orgchem.messaging.bus import bus


class BusHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            text = self.format(record)
            bus().message_posted.emit(record.levelname, text)
        except Exception:
            self.handleError(record)


def attach_bus_handler(level: int = logging.INFO) -> BusHandler:
    h = BusHandler()
    h.setLevel(level)
    h.setFormatter(logging.Formatter("%(asctime)s  %(name)s — %(message)s", "%H:%M:%S"))
    logging.getLogger().addHandler(h)
    return h
