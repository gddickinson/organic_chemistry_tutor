"""Bottom dock: session log driven by ``bus().message_posted``."""
from __future__ import annotations
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QPushButton, QComboBox, QLabel,
)

from orgchem.messaging.bus import bus

_LEVEL_ORDER = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
_LEVEL_COLOURS = {
    "DEBUG":    "#888888",
    "INFO":     "#202020",
    "WARNING":  "#b07000",
    "ERROR":    "#c03030",
    "CRITICAL": "#8a0a0a",
}


class SessionLogPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)

        top = QHBoxLayout()
        top.addWidget(QLabel("Level:"))
        self.level = QComboBox()
        self.level.addItems(_LEVEL_ORDER[:4])
        self.level.setCurrentText("INFO")
        top.addWidget(self.level)
        top.addStretch(1)
        clear = QPushButton("Clear")
        clear.clicked.connect(self._clear)
        top.addWidget(clear)
        lay.addLayout(top)

        self.edit = QPlainTextEdit()
        self.edit.setReadOnly(True)
        self.edit.setMaximumBlockCount(5000)
        lay.addWidget(self.edit, 1)

        bus().message_posted.connect(self._on_msg)

    def _threshold(self) -> int:
        return _LEVEL_ORDER.index(self.level.currentText())

    def _on_msg(self, level: str, text: str) -> None:
        if level not in _LEVEL_ORDER:
            return
        if _LEVEL_ORDER.index(level) < self._threshold():
            return
        colour = _LEVEL_COLOURS.get(level, "#202020")
        html = f'<span style="color:{colour}"><b>[{level}]</b> {_escape(text)}</span>'
        self.edit.appendHtml(html)
        self.edit.moveCursor(QTextCursor.End)

    def _clear(self) -> None:
        self.edit.clear()


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
