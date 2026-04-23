"""Central logging configuration.

Attaches three handlers to the root logger:
  1. a rotating file handler (``orgchem.log`` in the user log dir),
  2. a stream handler to stderr,
  3. a ``BusHandler`` that forwards records to the Qt AppBus so the
     ``SessionLogPanel`` can display them.
"""
from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler

from orgchem.config import AppConfig
from orgchem.messaging.logger import attach_bus_handler


_FMT = "%(asctime)s  %(levelname)-7s  %(name)s — %(message)s"


def setup_logging(cfg: AppConfig) -> None:
    root = logging.getLogger()
    root.setLevel(getattr(logging, cfg.log_level, logging.INFO))

    # Avoid duplicate handlers when called twice (e.g. tests).
    for h in list(root.handlers):
        root.removeHandler(h)

    fmt = logging.Formatter(_FMT)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    root.addHandler(ch)

    log_file = cfg.log_dir / "orgchem.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=3)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    attach_bus_handler()
    logging.getLogger("orgchem").info("Logging initialised → %s", log_file)
