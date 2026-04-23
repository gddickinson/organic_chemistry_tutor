"""Cross-thread GUI dispatch helper.

Agent actions can be called from either the main Qt thread (e.g.
via the stdio bridge on startup) or a worker thread (the tutor
panel's `_ChatWorker`). On macOS, instantiating any `NSWindow` off
the main thread aborts the whole process with
``NSWindow should only be instantiated on the main thread!`` —
reported by a user on 2026-04-23 when the tutor called
`show_ligand_binding`, which lazily constructs the Macromolecules
window.

:func:`run_on_main_thread` takes a zero-arg callable and runs it
on the thread owning :class:`QApplication` — synchronously when
already on the main thread, or asynchronously via
:meth:`QTimer.singleShot(0, ...)` (documented as thread-safe)
otherwise. Returns whether dispatch succeeded; the caller is
responsible for any return-value plumbing (usually none — the
callable's side effect is what matters).
"""
from __future__ import annotations
import logging
import threading
from typing import Any, Callable

log = logging.getLogger(__name__)


class MainThreadTimeout(TimeoutError):
    """`run_on_main_thread_sync` couldn't complete within its
    timeout (the main event loop is probably blocked)."""


def run_on_main_thread(fn: Callable[[], None]) -> bool:
    """Run ``fn`` on the Qt main thread.

    - If there's no ``QApplication`` (e.g. pure-unit-test / CLI
      usage), runs the callable inline and returns True.
    - If we're already on the main thread, calls ``fn()`` directly
      and returns True.
    - Otherwise posts ``fn`` to the main event loop via
      :meth:`QTimer.singleShot` and returns True (the call is
      queued; it won't run until the main thread processes events).

    Returns False only if dispatch itself errors (logged and
    swallowed so agent actions don't crash on best-effort UI
    surfacing).
    """
    try:
        from PySide6.QtCore import QCoreApplication, QThread, QTimer
    except ImportError:
        try:
            fn()
        except Exception:  # noqa: BLE001
            log.exception("run_on_main_thread inline fallback failed")
        return True

    app = QCoreApplication.instance()
    if app is None:
        try:
            fn()
        except Exception:  # noqa: BLE001
            log.exception("run_on_main_thread no-QApp fallback failed")
        return True

    try:
        if QThread.currentThread() is app.thread():
            fn()
            return True
    except Exception:  # noqa: BLE001
        # Very defensive — thread() can raise if the app is
        # mid-teardown. Fall through to QTimer dispatch.
        pass

    try:
        # ``QTimer.singleShot(msec, context, functor)`` runs the
        # functor on ``context``'s thread. The 2-arg overload
        # ``QTimer.singleShot(0, fn)`` runs ``fn`` on the CALLING
        # thread — no use to us from a worker. Passing the
        # QApplication as context means the slot executes on the
        # thread that owns the app (i.e. the main / GUI thread).
        QTimer.singleShot(0, app, fn)
        return True
    except Exception:  # noqa: BLE001
        log.exception("run_on_main_thread QTimer dispatch failed")
        return False


def run_on_main_thread_sync(fn: Callable[[], Any],
                            timeout: float = 5.0) -> Any:
    """Run ``fn`` on the Qt main thread and return its result.

    Blocking counterpart to :func:`run_on_main_thread`. When
    called from the main thread, runs inline. Otherwise posts
    ``fn`` onto the main event loop via ``QTimer.singleShot`` and
    blocks the caller thread on a :class:`threading.Event` until
    the slot has executed.

    Used for actions that must return a computed value to the
    caller (e.g. screenshot functions returning the saved path,
    :func:`QWidget.grab` results).

    Raises :class:`MainThreadTimeout` if the main loop doesn't
    run the slot within ``timeout`` seconds. That usually means
    the main thread is blocked on I/O or a modal dialog.
    """
    try:
        from PySide6.QtCore import QCoreApplication, QThread, QTimer
    except ImportError:
        return fn()

    app = QCoreApplication.instance()
    if app is None:
        return fn()

    try:
        if QThread.currentThread() is app.thread():
            return fn()
    except Exception:  # noqa: BLE001
        pass

    done = threading.Event()
    box: dict = {}

    def _run():
        try:
            box["result"] = fn()
        except BaseException as exc:  # noqa: BLE001 — capture *any* error
            box["error"] = exc
        finally:
            done.set()

    try:
        QTimer.singleShot(0, app, _run)
    except Exception:  # noqa: BLE001
        log.exception(
            "run_on_main_thread_sync QTimer dispatch failed")
        return fn()

    if not done.wait(timeout=timeout):
        raise MainThreadTimeout(
            f"Main thread didn't execute the queued callable within "
            f"{timeout}s — it's probably blocked (modal dialog, "
            f"long compute, etc.)."
        )
    if "error" in box:
        raise box["error"]
    return box.get("result")
