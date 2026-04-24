"""Phase 32d GUI-path smoke tests — run every bundled demo
through the **real** :class:`ScriptEditorDialog` + its
``_RunWorker`` QThread, not just through ``ScriptContext``
directly.  Catches regressions in the editor wiring (output
pane colour-coding, worker threading, error propagation) that
headless ``ScriptContext`` tests miss.

Uses ``pytest-qt`` to drive the dialog; Qt runs in offscreen
platform mode (set globally by :mod:`orgchem.agent.headless`).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from orgchem.agent.headless import HeadlessApp
from orgchem.scene import reset_current_scene

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


_SCRIPT_DIR = Path(__file__).resolve().parents[1] / "data" / "script_library"


def _discover_scripts() -> list[Path]:
    if not _SCRIPT_DIR.exists():
        return []
    return sorted(p for p in _SCRIPT_DIR.glob("*.py"))


@pytest.fixture(scope="module")
def _app():
    with HeadlessApp() as app:
        yield app


@pytest.mark.parametrize(
    "script_path", _discover_scripts(),
    ids=lambda p: p.name,
)
def test_demo_runs_through_script_editor_dialog(
    script_path: Path, _app, qtbot,
):
    """Load a demo into the real ``ScriptEditorDialog``, click Run,
    wait for the worker to finish, and assert the output pane
    shows stdout content without a red traceback block.

    This exercises the full GUI path: the dialog is constructed,
    the worker thread runs the snippet, the finished signal
    delivers the ``ExecResult``, and the HTML-colour-coded output
    is written to the `QPlainTextEdit`.
    """
    from orgchem.gui.dialogs.script_editor import ScriptEditorDialog

    reset_current_scene()
    dlg = ScriptEditorDialog(parent=None)
    qtbot.addWidget(dlg)
    dlg._editor.setPlainText(script_path.read_text())

    # Kick off execution via the same code path the Run button
    # uses, then wait (with a generous timeout) for the worker
    # to emit finished_result.
    dlg._run_all()
    # The worker emits `finished_result(ExecResult)` then
    # `finished()`; we use `waitUntil` on the status label flipping
    # back to "ok" / "error" since that's what the slot sets.
    qtbot.waitUntil(
        lambda: dlg._status.text() in ("ok", "error"),
        timeout=30_000,
    )

    status = dlg._status.text()
    output = dlg._output.toPlainText()
    assert status == "ok", (
        f"{script_path.name} — dialog status is {status!r}\n"
        f"--- output pane ---\n{output}\n"
    )
    # Output pane should carry the ">>> …" echo line + stdout
    # content from the demo.
    assert ">>>" in output, f"no command echo in output: {output!r}"
    assert output.strip().splitlines()[1:], (
        f"{script_path.name} produced only the echo line — "
        f"no real stdout:\n{output}"
    )
