"""Tutor chat console — pluggable LLM (Anthropic / OpenAI / Ollama) with
full tool-use access to the agent action registry.

Lives in a :class:`QDockWidget` so the user can tear it off into a floating
window. Every turn:
  * user text is pushed to :class:`Conversation`
  * the model may invoke one or more actions (which can move the molecule
    viewer, open a lesson, compute a formula, …)
  * assistant prose + tool-use records are shown in the transcript.
"""
from __future__ import annotations
import logging
from typing import Any

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPlainTextEdit, QPushButton,
    QComboBox, QLabel, QLineEdit, QMessageBox,
)

from orgchem.config import AppConfig
from orgchem.agent.llm.base import ChatMessage, available_backends
from orgchem.agent.conversation import Conversation
from orgchem.messaging.errors import NetworkError

log = logging.getLogger(__name__)


class _ChatWorker(QThread):
    assistant_turn = Signal(object)   # ChatMessage
    done = Signal()
    failed = Signal(str)

    def __init__(self, convo: Conversation, text: str):
        super().__init__()
        self.convo = convo
        self.text = text

    def run(self) -> None:
        try:
            for msg in self.convo.send(self.text):
                self.assistant_turn.emit(msg)
        except NetworkError as e:
            self.failed.emit(str(e))
        except Exception as e:  # noqa: BLE001
            log.exception("Tutor turn failed")
            self.failed.emit(f"{type(e).__name__}: {e}")
        finally:
            self.done.emit()


class TutorPanel(QWidget):
    def __init__(self, cfg: AppConfig):
        super().__init__()
        self.cfg = cfg
        self._convo: Conversation | None = None
        self._worker: _ChatWorker | None = None
        self._build_ui()

    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)

        cfg_row = QHBoxLayout()
        cfg_row.addWidget(QLabel("Backend:"))
        self.backend_cb = QComboBox()
        self.backend_cb.addItems(list(available_backends().keys()))
        cfg_row.addWidget(self.backend_cb)
        cfg_row.addWidget(QLabel("Model:"))
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("(use backend default)")
        cfg_row.addWidget(self.model_edit, 1)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._connect)
        cfg_row.addWidget(self.connect_btn)
        lay.addLayout(cfg_row)

        self.transcript = QTextBrowser()
        self.transcript.setOpenExternalLinks(True)
        lay.addWidget(self.transcript, 1)

        input_row = QHBoxLayout()
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText(
            "Ask the tutor… e.g. 'show me caffeine and explain why it's a stimulant'"
        )
        self.input.setFixedHeight(80)
        input_row.addWidget(self.input, 1)
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self._send)
        self.send_btn.setFixedWidth(80)
        input_row.addWidget(self.send_btn)
        lay.addLayout(input_row)

        self._append_system(
            "Choose a backend and click <b>Connect</b> to begin.<br>"
            "• <b>anthropic</b> — needs ANTHROPIC_API_KEY in the environment<br>"
            "• <b>openai</b> — needs OPENAI_API_KEY (or a compatible base URL)<br>"
            "• <b>ollama</b> — connects to http://localhost:11434 by default (local models)"
        )

    # ------------------------------------------------------------------
    def _connect(self) -> None:
        name = self.backend_cb.currentText()
        cls = available_backends().get(name)
        if cls is None:
            QMessageBox.warning(self, "Unknown backend", name)
            return
        try:
            backend = cls(model=self.model_edit.text().strip() or "")
        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Backend init failed", str(e))
            return
        self._convo = Conversation(backend=backend)
        self._append_system(
            f"Connected to <b>{name}</b> "
            f"(model: <code>{backend.model or '(default)'}</code>). Ask away."
        )

    # ------------------------------------------------------------------
    def _send(self) -> None:
        if self._convo is None:
            QMessageBox.information(self, "Not connected", "Click Connect first.")
            return
        if self._worker is not None and self._worker.isRunning():
            return
        text = self.input.toPlainText().strip()
        if not text:
            return
        self.input.clear()
        self._append_user(text)
        self.send_btn.setEnabled(False)

        self._worker = _ChatWorker(self._convo, text)
        self._worker.assistant_turn.connect(self._on_turn)
        self._worker.failed.connect(self._on_failed)
        self._worker.done.connect(self._on_done)
        self._worker.start()

    def _on_turn(self, msg: ChatMessage) -> None:
        if msg.text:
            self._append_assistant(msg.text)
        for tc in msg.tool_calls:
            self._append_tool(tc.name, tc.arguments)

    def _on_failed(self, err: str) -> None:
        self._append_system(f"<span style='color:#c03030'><b>Error:</b> {err}</span>")

    def _on_done(self) -> None:
        self.send_btn.setEnabled(True)

    # ------------------------------------------------------------------
    def _append_user(self, text: str) -> None:
        self._append(f"<p><b style='color:#2a5885'>You:</b> {_esc(text)}</p>")

    def _append_assistant(self, text: str) -> None:
        self._append(f"<p><b style='color:#2d7a2d'>Tutor:</b> {_esc(text)}</p>")

    def _append_tool(self, name: str, args: Any) -> None:
        self._append(
            f"<p style='color:#777;font-family:monospace'>&nbsp;↳ called <b>{name}</b>({_esc(str(args))})</p>"
        )

    def _append_system(self, html: str) -> None:
        self._append(f"<p style='color:#888;font-style:italic'>{html}</p>")

    def _append(self, html: str) -> None:
        self.transcript.moveCursor(QTextCursor.End)
        self.transcript.insertHtml(html)
        self.transcript.moveCursor(QTextCursor.End)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
