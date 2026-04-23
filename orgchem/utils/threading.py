"""Qt-friendly background worker helpers.

Use ``submit(fn, *args, **kwargs)`` for any potentially slow call (DB query,
network request, conformer generation) so the UI thread never blocks.
Connect to the returned ``Worker.signals.result`` / ``.error`` to receive
results on the UI thread.
"""
from __future__ import annotations
import traceback
from typing import Any, Callable

from PySide6.QtCore import QObject, QRunnable, Signal, Slot, QThreadPool


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)        # (exception, traceback string)
    result = Signal(object)
    progress = Signal(int, int)  # (current, total)


class Worker(QRunnable):
    """Run a plain callable on the global Qt thread pool."""

    def __init__(self, fn: Callable[..., Any], *args: Any, **kwargs: Any):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit((e, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


def submit(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Worker:
    """Schedule *fn* on the global thread pool. Returns the Worker for signal wiring."""
    w = Worker(fn, *args, **kwargs)
    QThreadPool.globalInstance().start(w)
    return w
