"""Phase 32a — script execution context for the user-facing REPL.

Hosts a persistent globals dict + an exec loop that routes stdout /
stderr into a capturable buffer and turns exceptions into clean
tracebacks. Zero Qt imports so the class is fully headless-testable.

The dialog in :mod:`orgchem.gui.dialogs.script_editor` wraps this with
an editor pane + output pane; agent scripts (Phase 32e) and the stdio
bridge can reuse ``ScriptContext`` directly.

Pre-imported globals (first eval):

    app      — :class:`AppProxy` with ``.call(action, **kw)`` + every
               registered action as a direct attribute
    chem     — ``rdkit.Chem`` (aliased for brevity)
    orgchem  — the full package
    viewer   — placeholder; lazily replaced with the Workbench scene
               when 32b lands.  Until then, calls raise
               ``WorkbenchNotReadyError``.

State persists between runs: defining a variable on one run, then
referring to it on the next, works.  Use :meth:`reset` to flush.
"""
from __future__ import annotations

import io
import logging
import re
import traceback
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


#: Phase 32e — regex for fenced ```python code blocks in markdown /
#: LLM output.  Also catches the plain ``` variant so the tutor's
#: "run this script" button works even if the LLM omitted the
#: language tag.  The pattern is deliberately permissive; the
#: Script Editor will surface any syntax errors when the user runs.
_CODE_FENCE_RX = re.compile(
    r"```(?:python|py)?\s*\n(.*?)\n?```",
    flags=re.DOTALL | re.IGNORECASE,
)


def extract_python_blocks(text: str) -> List[str]:
    """Return every fenced ```python (or bare ```) code block in
    *text*, in document order.  Empty list when no block matches.

    Used by the tutor panel (Phase 32e) to surface a *Run in
    Script Editor* button per code block the LLM emits.
    """
    if not text:
        return []
    return [m.strip() for m in _CODE_FENCE_RX.findall(text)]

log = logging.getLogger(__name__)


class WorkbenchNotReadyError(RuntimeError):
    """Raised when a script calls the ``viewer`` API before Phase 32b
    (the Workbench window) has been wired in."""


class _WorkbenchStub:
    """Placeholder ``viewer`` object for 32a.  Every attribute access
    raises a helpful error pointing at Phase 32b."""

    def __getattr__(self, name: str) -> Any:  # pragma: no cover - trivial
        raise WorkbenchNotReadyError(
            f"viewer.{name}(…) needs the Workbench window (Phase 32b). "
            "For now, use app.call('show_molecule', …) or one of the "
            "export_*_png actions."
        )


class AppProxy:
    """Thin wrapper around the agent action registry so scripts can say
    ``app.show_molecule('caffeine')`` or ``app.call('show_molecule',
    name_or_id='caffeine')`` interchangeably.

    Attribute access returns a bound callable that invokes the action
    by name.  Unknown attributes raise ``AttributeError`` at lookup
    time so scripts fail fast.
    """

    def __init__(self) -> None:
        # Lazy import so the module remains usable even if the agent
        # library hasn't finished registering everything (tests import
        # actions at different times).
        from orgchem.agent.actions import invoke, registry

        self._invoke: Callable[..., Any] = invoke
        self._registry = registry

    def call(self, action: str, **kwargs: Any) -> Any:
        """Canonical entry: ``app.call('show_molecule', name_or_id='caffeine')``."""
        return self._invoke(action, **kwargs)

    def list_actions(self) -> list[str]:
        """Convenience: every registered action name."""
        return sorted(self._registry().keys())

    def __getattr__(self, name: str) -> Callable[..., Any]:
        if name.startswith("_"):
            raise AttributeError(name)
        actions = self._registry()
        if name not in actions:
            raise AttributeError(
                f"no action named {name!r}; try "
                f"app.list_actions() for the full catalogue"
            )
        return lambda **kw: self._invoke(name, **kw)


@dataclass
class ExecResult:
    """One run of ``ScriptContext.run`` — everything a dialog needs to
    render the output pane."""

    stdout: str = ""
    stderr: str = ""
    #: Python ``repr`` of the last expression, if the snippet is a
    #: single expression statement.  Empty for multi-statement snippets.
    repr_value: str = ""
    traceback: str = ""

    @property
    def ok(self) -> bool:
        return not self.traceback


@dataclass
class ScriptContext:
    """Persistent Python globals + a safe-ish exec loop.

    Create one instance per script-editor session.  Call :meth:`run`
    with each snippet; state carries over.  Use :meth:`reset` to
    start fresh.
    """

    globals: Dict[str, Any] = field(default_factory=dict)
    _initialised: bool = False

    def _init_globals(self) -> None:
        if self._initialised:
            return
        # Avoid importing rdkit.Chem at module-import time — keep
        # ``ScriptContext`` cheap to construct for tests.
        import rdkit.Chem as _chem
        import orgchem as _orgchem
        from orgchem.scene import current_scene as _current_scene

        #: Phase 32b: the ``viewer`` global is the process-wide Scene
        #: returned by ``orgchem.scene.current_scene()``.  The
        #: Workbench widget (when open) is already listening to this
        #: Scene, so ``viewer.add_molecule('CCO')`` from a script
        #: updates the visible view automatically.  If the Workbench
        #: hasn't been opened yet, the Scene still accepts commands
        #: — they just accumulate until a view attaches.
        self.globals.update({
            "__name__": "__orgchem_script__",
            "__builtins__": __builtins__,
            "app": AppProxy(),
            "chem": _chem,
            "orgchem": _orgchem,
            "viewer": _current_scene(),
        })
        self._initialised = True

    def reset(self) -> None:
        """Flush all script state.  Re-initialised lazily on next run."""
        self.globals.clear()
        self._initialised = False

    def run(self, source: str) -> ExecResult:
        """Execute a snippet and return captured output + last-expr repr.

        Uses ``compile(..., 'exec')`` for multi-statement snippets and
        falls back to ``'single'`` mode when the snippet is one
        expression — that's how we capture the last-expression
        ``repr`` without printing every statement.
        """
        self._init_globals()
        out = io.StringIO()
        err = io.StringIO()
        repr_value = ""
        tb = ""

        try:
            # Try to treat the whole snippet as a single expression
            # first — gives us the Jupyter-style "last line shows".
            try:
                code = compile(source, "<script>", "eval")
                is_expr = True
            except SyntaxError:
                code = compile(source, "<script>", "exec")
                is_expr = False
        except SyntaxError as e:
            return ExecResult(traceback=self._format_syntax_error(e))

        try:
            with redirect_stdout(out), redirect_stderr(err):
                if is_expr:
                    value = eval(code, self.globals)  # noqa: S307
                    if value is not None:
                        repr_value = repr(value)
                else:
                    exec(code, self.globals)  # noqa: S102
        except BaseException:  # capture KeyboardInterrupt too
            tb = traceback.format_exc()

        return ExecResult(
            stdout=out.getvalue(),
            stderr=err.getvalue(),
            repr_value=repr_value,
            traceback=tb,
        )

    @staticmethod
    def _format_syntax_error(exc: SyntaxError) -> str:
        """Short, consistent rendering of syntax errors for the
        output pane (``traceback.format_exception`` dumps too much
        noise for a one-line script)."""
        where = f"line {exc.lineno}"
        if exc.offset:
            where += f", col {exc.offset}"
        msg = f"SyntaxError: {exc.msg} ({where})"
        if exc.text:
            msg += f"\n    {exc.text.rstrip()}"
            if exc.offset:
                msg += "\n    " + (" " * (max(exc.offset - 1, 0))) + "^"
        return msg


from orgchem.agent.actions import action


@action(category="scripting")
def open_workbench() -> Dict[str, Any]:
    """Focus the Workbench tab (Phase 32b).

    Raises the detached Workbench window if the user has popped
    it out of the main tabbar.  The Workbench shares a single
    process-wide Scene with the ``viewer`` global in scripts —
    opening it just makes the scene visible.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync

    win = controller.require_main_window()

    def _open() -> Dict[str, Any]:
        win.open_workbench()
        return {"opened": True,
                "track_count": len(win.workbench.scene().tracks())}

    return run_on_main_thread_sync(_open)


@action(category="scripting")
def open_script_editor() -> Dict[str, Any]:
    """Open the Python script editor + REPL dialog (Phase 32a).

    The dialog exposes a persistent :class:`ScriptContext` whose
    ``app`` / ``chem`` / ``orgchem`` / ``viewer`` globals let the
    user drive any registered action or render any RDKit object
    without leaving the app.  Lazy-imports the Qt layer so headless
    callers don't accidentally pull in PySide6.
    """
    from orgchem.agent import controller
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    from orgchem.gui.dialogs.script_editor import ScriptEditorDialog

    win = controller.require_main_window()

    def _open() -> Dict[str, Any]:
        dlg = ScriptEditorDialog.singleton(parent=win)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        return {"opened": True}

    return run_on_main_thread_sync(_open)
