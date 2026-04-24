"""Phase 32a — Script Editor + REPL dialog.

Editor pane (top) + output pane (bottom) + Run / Run-selection / Reset
buttons.  Wraps a persistent :class:`orgchem.agent.script_context.ScriptContext`
that exposes every registered action via ``app.<name>(…)`` plus
``chem`` / ``orgchem`` / ``viewer`` globals.

Singleton per app instance (re-opening the dialog brings the existing
window forward instead of replacing the user's in-progress script).
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QTextCursor
from PySide6.QtWidgets import (
    QDialog, QFileDialog, QHBoxLayout, QLabel, QMessageBox,
    QPlainTextEdit, QPushButton, QSplitter, QVBoxLayout, QWidget,
)

from orgchem.agent.script_context import ExecResult, ScriptContext

log = logging.getLogger(__name__)


_SNIPPET = """# OrgChem Studio — Python REPL
# Press Ctrl+Enter (or click Run) to execute the editor contents.
# Globals: app, chem, orgchem, viewer (Phase 32b)

print('registered actions:', len(app.list_actions()))
print('  some examples:', app.list_actions()[:8])
"""


class _RunWorker(QThread):
    """Execute a script on a worker thread so the UI stays responsive
    for long calls (e.g. PDB fetch, conformer generation)."""

    finished_result = Signal(object)   # emits ExecResult

    def __init__(self, ctx: ScriptContext, source: str,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._ctx = ctx
        self._source = source

    def run(self) -> None:  # noqa: D401 — QThread override
        try:
            result = self._ctx.run(self._source)
        except BaseException as e:  # pragma: no cover - defensive
            result = ExecResult(traceback=f"worker crashed: {e!r}")
        self.finished_result.emit(result)


class ScriptEditorDialog(QDialog):
    """Python REPL + editor dialog.

    The dialog is a singleton per QApplication so that the user's
    ``ScriptContext`` state (globals, imports, defined variables)
    persists across Tools → *Script editor…* invocations.
    """

    _instance: Optional["ScriptEditorDialog"] = None

    # -------- construction / singleton --------
    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None) -> "ScriptEditorDialog":
        if cls._instance is None or not cls._instance.isVisible():
            cls._instance = cls(parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Script editor — Phase 32a")
        self.setModal(False)
        self.resize(900, 620)

        self._ctx = ScriptContext()
        self._worker: Optional[_RunWorker] = None
        self._current_path: Optional[Path] = None

        self._build_ui()
        self._wire_shortcuts()

        # Prime with a friendly snippet so the user has something
        # obvious to run.
        self._editor.setPlainText(_SNIPPET)

    # -------- layout --------
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)

        # Toolbar row ---------------------------------------------
        toolbar = QHBoxLayout()
        self._btn_run = QPushButton("Run  (Ctrl+Enter)")
        self._btn_run_sel = QPushButton("Run selection")
        self._btn_stop = QPushButton("Stop")
        self._btn_stop.setEnabled(False)
        self._btn_reset = QPushButton("Reset globals")
        self._btn_open = QPushButton("Open…")
        self._btn_save = QPushButton("Save…")
        for b in (self._btn_run, self._btn_run_sel, self._btn_stop,
                  self._btn_reset, self._btn_open, self._btn_save):
            toolbar.addWidget(b)
        toolbar.addStretch(1)
        self._status = QLabel("ready")
        self._status.setStyleSheet("color: #666;")
        toolbar.addWidget(self._status)
        root.addLayout(toolbar)

        # Editor + output panes -----------------------------------
        split = QSplitter(Qt.Vertical, self)
        root.addWidget(split, 1)

        mono = QFont("Menlo, Consolas, monospace")
        mono.setStyleHint(QFont.Monospace)

        self._editor = QPlainTextEdit(self)
        self._editor.setFont(mono)
        self._editor.setTabChangesFocus(False)
        self._editor.setPlaceholderText(
            "# type a Python snippet; Ctrl+Enter to run\n"
            "print(app.list_actions()[:5])"
        )
        split.addWidget(self._editor)

        self._output = QPlainTextEdit(self)
        self._output.setFont(mono)
        self._output.setReadOnly(True)
        self._output.setStyleSheet(
            "background: #111; color: #e8e8e8; border: 1px solid #333;"
        )
        split.addWidget(self._output)
        split.setStretchFactor(0, 3)
        split.setStretchFactor(1, 2)

        # Button wiring -------------------------------------------
        self._btn_run.clicked.connect(self._run_all)
        self._btn_run_sel.clicked.connect(self._run_selection)
        self._btn_stop.clicked.connect(self._stop_worker)
        self._btn_reset.clicked.connect(self._reset_globals)
        self._btn_open.clicked.connect(self._open_file)
        self._btn_save.clicked.connect(self._save_file)

    def _wire_shortcuts(self) -> None:
        # Ctrl+Enter → run whole buffer.
        QShortcut(QKeySequence("Ctrl+Return"), self, self._run_all)
        QShortcut(QKeySequence("Ctrl+Enter"), self, self._run_all)
        # Ctrl+Shift+Enter → run selection (same binding on mac).
        QShortcut(QKeySequence("Ctrl+Shift+Return"), self,
                  self._run_selection)
        # Ctrl+L → clear output pane.
        QShortcut(QKeySequence("Ctrl+L"), self, self._output.clear)

    # -------- execution --------
    def _run_all(self) -> None:
        src = self._editor.toPlainText()
        if not src.strip():
            return
        self._dispatch(src)

    def _run_selection(self) -> None:
        cursor = self._editor.textCursor()
        src = cursor.selectedText().replace(" ", "\n")
        if not src.strip():
            src = self._current_line()
        if not src.strip():
            return
        self._dispatch(src)

    def _current_line(self) -> str:
        cursor = self._editor.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        return cursor.selectedText().replace(" ", "\n")

    def _dispatch(self, source: str) -> None:
        if self._worker is not None and self._worker.isRunning():
            QMessageBox.information(
                self, "Busy", "A script is still running — wait or press Stop.")
            return
        self._append_output(f">>> {self._one_liner(source)}\n",
                            colour="#7ab7ff")
        self._btn_run.setEnabled(False)
        self._btn_run_sel.setEnabled(False)
        self._btn_stop.setEnabled(True)
        self._status.setText("running…")
        self._worker = _RunWorker(self._ctx, source, self)
        self._worker.finished_result.connect(self._on_run_finished)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.start()

    def _on_run_finished(self, result: ExecResult) -> None:
        if result.stdout:
            self._append_output(result.stdout)
        if result.stderr:
            self._append_output(result.stderr, colour="#ffaa66")
        if result.repr_value:
            self._append_output(result.repr_value + "\n", colour="#aaffaa")
        if result.traceback:
            self._append_output(result.traceback, colour="#ff6666")
        self._btn_run.setEnabled(True)
        self._btn_run_sel.setEnabled(True)
        self._btn_stop.setEnabled(False)
        self._status.setText("ok" if result.ok else "error")
        self._worker = None

    def _stop_worker(self) -> None:
        if self._worker is None:
            return
        # QThread doesn't cleanly interrupt arbitrary Python —
        # request termination and warn the user.
        self._worker.requestInterruption()
        self._worker.terminate()
        self._worker.wait(500)
        self._append_output("(script interrupted)\n", colour="#ffaa66")
        self._btn_run.setEnabled(True)
        self._btn_run_sel.setEnabled(True)
        self._btn_stop.setEnabled(False)
        self._status.setText("stopped")
        self._worker = None

    def _reset_globals(self) -> None:
        self._ctx.reset()
        self._append_output("(globals reset)\n", colour="#aaffaa")
        self._status.setText("ready")

    # -------- file i/o --------
    def _open_file(self) -> None:
        start = str(self._current_path or Path.home())
        path, _ = QFileDialog.getOpenFileName(
            self, "Open script", start, "Python scripts (*.py)")
        if not path:
            return
        try:
            text = Path(path).read_text()
        except OSError as e:
            QMessageBox.critical(self, "Open failed", str(e))
            return
        self._editor.setPlainText(text)
        self._current_path = Path(path)
        self.setWindowTitle(f"Script editor — {self._current_path.name}")

    def _save_file(self) -> None:
        start = str(self._current_path or Path.home() / "script.py")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save script", start, "Python scripts (*.py)")
        if not path:
            return
        try:
            Path(path).write_text(self._editor.toPlainText())
        except OSError as e:
            QMessageBox.critical(self, "Save failed", str(e))
            return
        self._current_path = Path(path)
        self.setWindowTitle(f"Script editor — {self._current_path.name}")

    # -------- output helpers --------
    def _append_output(self, text: str, colour: Optional[str] = None) -> None:
        cursor = self._output.textCursor()
        cursor.movePosition(QTextCursor.End)
        if colour:
            cursor.insertHtml(
                f'<span style="color: {colour}; white-space: pre-wrap;">'
                f'{self._html_escape(text)}</span>'
            )
        else:
            cursor.insertText(text)
        self._output.setTextCursor(cursor)
        self._output.ensureCursorVisible()

    @staticmethod
    def _html_escape(text: str) -> str:
        return (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>")
        )

    @staticmethod
    def _one_liner(source: str) -> str:
        first = source.strip().splitlines()[0] if source.strip() else ""
        if len(source.strip().splitlines()) > 1:
            first += "  …"
        return first[:120]
