"""Screenshot utilities — grab Qt widgets (or the main window) to PNG files.

Works in both normal and offscreen Qt platforms, so the same code serves the
``File → Screenshot`` menu action and the headless visual-tour / regression
tests driven by the agent layer.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional, Union

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget

log = logging.getLogger(__name__)


def grab_widget(widget: QWidget, path: Union[str, Path],
                size: Optional[QSize] = None) -> Path:
    """Grab *widget* to a PNG at *path*. Returns the written path.

    If *size* is given the pixmap is smoothly scaled to that bounding box
    (aspect ratio preserved). Parent directories are created as needed.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    pixmap = widget.grab()
    if size is not None:
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    if not pixmap.save(str(p), "PNG"):
        raise IOError(f"Failed to save screenshot to {p}")
    log.info("Screenshot saved: %s (%dx%d)", p, pixmap.width(), pixmap.height())
    return p
