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

from PySide6.QtCore import Qt, QThread, QUrl, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPlainTextEdit, QPushButton,
    QCheckBox, QComboBox, QLabel, QMessageBox,
)

from orgchem.config import AppConfig
from orgchem.agent.llm.base import ChatMessage, available_backends
from orgchem.agent.conversation import (
    Conversation,
    build_script_mode_system_prompt,
)
from orgchem.agent.script_context import extract_python_blocks
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
    #: Internal scheme used for embedded "Run in Script Editor"
    #: anchors in the transcript.  Format: ``orgchem-script:<idx>``
    #: where ``<idx>`` is a key into ``self._script_blocks``.
    _SCRIPT_URL_SCHEME = "orgchem-script"

    def __init__(self, cfg: AppConfig):
        super().__init__()
        self.cfg = cfg
        self._convo: Conversation | None = None
        self._worker: _ChatWorker | None = None
        #: Phase 32e — maps ``orgchem-script:<idx>`` anchor → extracted
        #: Python block.  Populated as the tutor emits replies; read by
        #: :meth:`_on_anchor_clicked` when the user clicks the link.
        self._script_blocks: dict[int, str] = {}
        self._next_block_idx: int = 0
        self._build_ui()

    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)

        cfg_row = QHBoxLayout()
        cfg_row.addWidget(QLabel("Backend:"))
        self.backend_cb = QComboBox()
        self.backend_cb.addItems(list(available_backends().keys()))
        self.backend_cb.currentTextChanged.connect(self._on_backend_changed)
        cfg_row.addWidget(self.backend_cb)
        cfg_row.addWidget(QLabel("Model:"))
        # Editable combo: free-text for OpenAI / Anthropic custom models,
        # auto-populated dropdown for Ollama (probed from /api/tags).
        self.model_edit = QComboBox()
        self.model_edit.setEditable(True)
        self.model_edit.lineEdit().setPlaceholderText(
            "(use backend default)")
        cfg_row.addWidget(self.model_edit, 1)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._connect)
        cfg_row.addWidget(self.connect_btn)
        lay.addLayout(cfg_row)
        # Initial populate once the widget is built.
        self._on_backend_changed(self.backend_cb.currentText())

        # Phase 32e — script-mode toggle.  When checked, the tutor's
        # system prompt is extended with the ScriptContext-globals
        # briefing (see ``build_script_mode_system_prompt``) and any
        # fenced ```python blocks in a reply gain a clickable
        # "Run in Script Editor" link in the transcript.
        script_row = QHBoxLayout()
        self.script_mode_cb = QCheckBox("Reply with a script")
        self.script_mode_cb.setToolTip(
            "When enabled, the tutor writes fenced ```python blocks "
            "that can be sent to the Script Editor (Tools → Script "
            "editor… / Ctrl+Shift+E) for the user to run.  Blocks "
            "never auto-execute."
        )
        self.script_mode_cb.toggled.connect(self._on_script_mode_toggled)
        script_row.addWidget(self.script_mode_cb)
        script_row.addStretch(1)
        lay.addLayout(script_row)

        self.transcript = QTextBrowser()
        # Our "Run in Script Editor" anchors use a custom scheme —
        # take over URL handling so QTextBrowser doesn't try to
        # open them in the system browser.
        self.transcript.setOpenExternalLinks(False)
        self.transcript.setOpenLinks(False)
        self.transcript.anchorClicked.connect(self._on_anchor_clicked)
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
            "• <b>ollama</b> — probes <code>localhost:11434</code> and "
            "auto-populates the Model dropdown with your installed "
            "tags; pre-selects a tool-use-capable model if one is "
            "installed (llama3.1 / llama3.2 / qwen2.5 / …)."
        )

    # ------------------------------------------------------------------
    def _on_backend_changed(self, name: str) -> None:
        """Repopulate the Model dropdown when the backend selection
        changes. For Ollama we probe ``/api/tags`` on a best-effort
        basis; other backends get a blank editable combo."""
        self.model_edit.blockSignals(True)
        self.model_edit.clear()
        if name == "ollama":
            try:
                from orgchem.agent.llm.ollama_backend import (
                    ollama_list_models,
                )
                models = ollama_list_models()
            except NetworkError:
                models = []
            except Exception:  # noqa: BLE001
                models = []
            if models:
                self.model_edit.addItems(models)
                # Pre-select the best tool-use candidate so the user
                # can just click Connect.
                from orgchem.agent.llm.ollama_backend import (
                    _pick_best_model,
                )
                best = _pick_best_model(models)
                if best:
                    idx = self.model_edit.findText(best)
                    if idx >= 0:
                        self.model_edit.setCurrentIndex(idx)
                self.model_edit.lineEdit().setPlaceholderText(
                    f"(installed: {len(models)})")
            else:
                self.model_edit.lineEdit().setPlaceholderText(
                    "(Ollama not reachable at localhost:11434)")
        else:
            self.model_edit.lineEdit().setPlaceholderText(
                "(use backend default)")
        self.model_edit.blockSignals(False)

    def _connect(self) -> None:
        name = self.backend_cb.currentText()
        cls = available_backends().get(name)
        if cls is None:
            QMessageBox.warning(self, "Unknown backend", name)
            return
        # For Ollama, probe first so we give a clear error at Connect
        # time rather than 30 seconds into the first /api/chat request.
        if name == "ollama":
            try:
                from orgchem.agent.llm.ollama_backend import (
                    ollama_list_models,
                )
                installed = ollama_list_models()
            except NetworkError as e:
                QMessageBox.critical(
                    self, "Ollama not reachable",
                    f"{e}\n\nStart Ollama with `ollama serve` or open "
                    f"the Ollama desktop app, then try Connect again.",
                )
                return
            if not installed:
                QMessageBox.warning(
                    self, "No Ollama models installed",
                    "Ollama is running but no models are pulled yet. "
                    "Run e.g. `ollama pull llama3.1` in a terminal, "
                    "then click Connect.",
                )
                return
            requested = self.model_edit.currentText().strip()
            if requested and requested not in installed:
                QMessageBox.warning(
                    self, "Ollama model not installed",
                    f"Model {requested!r} is not on this Ollama "
                    f"server.\nInstalled: {', '.join(installed)}",
                )
                return
        try:
            backend = cls(model=self.model_edit.currentText().strip() or "")
        except Exception as e:  # noqa: BLE001
            QMessageBox.critical(self, "Backend init failed", str(e))
            return
        self._convo = Conversation(backend=backend)
        # Phase 32e: if the user pre-ticked "Reply with a script"
        # before connecting, apply the addendum now.
        if self.script_mode_cb.isChecked():
            self._convo.system_prompt = build_script_mode_system_prompt()
        extra = ""
        tool_note = ""
        if name == "ollama":
            n_models = len(getattr(backend, 'available_models', []))
            extra = f" · {n_models} local model(s) available"
            from orgchem.agent.llm.ollama_backend import model_supports_tools
            if not model_supports_tools(backend.model):
                tool_note = (
                    "<br><span style='color:#c07a00'>⚠ This model "
                    "doesn't advertise tool-use support — the tutor "
                    "can chat but won't invoke agent actions. For "
                    "full tool use, try <code>ollama pull "
                    "llama3.1</code> or <code>qwen2.5</code>.</span>"
                )
        self._append_system(
            f"Connected to <b>{name}</b> "
            f"(model: <code>{backend.model or '(default)'}</code>){extra}. "
            f"Ask away.{tool_note}"
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
        """Render a tutor reply.  Phase 32e: if the reply contains
        fenced ```python blocks, each gets a trailing *Run in
        Script Editor* anchor (``orgchem-script:<idx>``) that the
        ``_on_anchor_clicked`` handler routes into the Script
        Editor dialog."""
        blocks = extract_python_blocks(text)
        if not blocks:
            self._append(
                f"<p><b style='color:#2d7a2d'>Tutor:</b> {_esc(text)}</p>")
            return

        # Build a transcript entry that keeps the prose context but
        # substitutes each ```python … ``` span with a monospace
        # preview + a Run link.
        from orgchem.agent.script_context import _CODE_FENCE_RX

        parts: list[str] = []
        cursor = 0
        block_iter = iter(blocks)
        for match in _CODE_FENCE_RX.finditer(text):
            prose = text[cursor:match.start()]
            if prose.strip():
                parts.append(_esc(prose))
            block = next(block_iter, "").strip()
            idx = self._next_block_idx
            self._next_block_idx += 1
            self._script_blocks[idx] = block
            preview = block if len(block) <= 500 else (
                block[:500].rstrip() + "\n# … (truncated — full "
                "block loads into the editor)")
            parts.append(
                "<div style='background:#111;color:#e8e8e8;"
                "padding:8px;margin:6px 0;"
                "font-family:Menlo,Consolas,monospace;"
                "white-space:pre-wrap;border-left:3px solid #4a9;'>"
                f"{_esc(preview)}</div>"
                f"<p><a href='{self._SCRIPT_URL_SCHEME}:{idx}'>"
                f"▶ Run in Script Editor</a></p>"
            )
            cursor = match.end()
        tail = text[cursor:]
        if tail.strip():
            parts.append(_esc(tail))

        self._append(
            "<p><b style='color:#2d7a2d'>Tutor:</b> "
            + "".join(parts) + "</p>"
        )

    def _on_script_mode_toggled(self, checked: bool) -> None:
        """Keep the live conversation's system prompt in sync with the
        script-mode checkbox.  Takes effect from the next turn; no
        reconnect needed."""
        if self._convo is None:
            # Will be applied at Connect time via the same logic.
            return
        from orgchem.agent.conversation import _SYSTEM_PROMPT
        if checked:
            self._convo.system_prompt = build_script_mode_system_prompt()
            self._append_system(
                "<i>Script mode on — the tutor will reply with "
                "Python blocks you can run.</i>"
            )
        else:
            self._convo.system_prompt = _SYSTEM_PROMPT
            self._append_system("<i>Script mode off.</i>")

    def _on_anchor_clicked(self, url: QUrl) -> None:
        """Route anchor clicks in the transcript.  The script-URL
        scheme (``orgchem-script:<idx>``) loads the indexed block
        into the Script Editor dialog; any other scheme falls
        through to the default external-browser path."""
        if url.scheme() != self._SCRIPT_URL_SCHEME:
            # Delegate non-script URLs to the system browser.
            from PySide6.QtGui import QDesktopServices
            QDesktopServices.openUrl(url)
            return
        try:
            idx = int(url.path() or url.toString().split(":", 1)[1])
        except (ValueError, IndexError):
            return
        block = self._script_blocks.get(idx)
        if not block:
            return
        # Singleton dialog — the user's prior globals persist.
        from orgchem.gui.dialogs.script_editor import ScriptEditorDialog
        dlg = ScriptEditorDialog.singleton(parent=self.window())
        dlg._editor.setPlainText(block)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

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
