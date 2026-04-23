"""Regression tests for the cross-thread GUI dispatch helper
introduced after the round-55 crash:

    QObject::setParent: Cannot set parent, new parent is in a
        different thread
    NSWindow should only be instantiated on the main thread!

The bug was that `show_ligand_binding` (and `open_macromolecules_
window`) lazily instantiated a QMainWindow / NSWindow directly
from the tutor panel's _ChatWorker (a QThread). macOS aborts.

Fix: every GUI-touching agent action goes through
`run_on_main_thread`, which posts onto the Qt main event loop
via `QTimer.singleShot(0, ...)`.
"""
from __future__ import annotations
import os
import threading

import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_run_on_main_thread_direct_call(app):
    """Calling from the main thread runs inline."""
    from orgchem.agent._gui_dispatch import run_on_main_thread
    seen = []

    def bump():
        seen.append(1)

    ok = run_on_main_thread(bump)
    assert ok is True
    assert seen == [1]


def test_run_on_main_thread_from_worker(app):
    """From a background thread, dispatch is queued. The callable
    runs once the main thread processes events (pumped below)."""
    from orgchem.agent._gui_dispatch import run_on_main_thread
    ran = threading.Event()
    seen = []

    def cb():
        seen.append("main-thread-ran")
        ran.set()

    def bg():
        ok = run_on_main_thread(cb)
        assert ok is True

    t = threading.Thread(target=bg)
    t.start()
    t.join(timeout=2.0)
    # Pump the main-thread event loop so the queued QTimer fires.
    # The worker queues QTimer onto the main thread; we have to
    # drive the main loop to let it execute.
    import time
    deadline = time.time() + 3.0
    while time.time() < deadline and not ran.is_set():
        app.pump(20)
    assert ran.is_set(), "Queued callable never ran"
    assert seen == ["main-thread-ran"]


def test_open_macromolecules_window_from_background_thread(app):
    """The exact crash the user hit — opening the window from a
    worker-thread agent-action call. With the thread guard in
    place this must not abort the process."""
    from orgchem.agent.actions import invoke
    result = {}

    def bg():
        result["r"] = invoke("open_macromolecules_window",
                             tab="Proteins")

    t = threading.Thread(target=bg)
    t.start()
    t.join(timeout=5.0)
    # Give the main loop time to process the queued show.
    app.pump(50)
    assert result.get("r") is not None, "action never returned"
    r = result["r"]
    assert "error" not in r, r
    assert r["shown"] is True
    assert "Proteins" in r["tabs"]


def test_show_reaction_from_background_thread(app):
    """Round-56 hardening: `show_reaction` touches the Reactions
    tab directly and would crash off-main without a dispatch wrap."""
    from orgchem.agent.actions import invoke
    result = {}

    def bg():
        result["r"] = invoke("show_reaction", name_or_id="Fischer")

    t = threading.Thread(target=bg)
    t.start()
    t.join(timeout=5.0)
    app.pump(100)
    assert "r" in result
    assert "error" not in result["r"], result["r"]


def test_show_pathway_from_background_thread(app):
    from orgchem.agent.actions import invoke
    result = {}

    def bg():
        # Pick the first seeded pathway.
        rows = invoke("list_pathways")
        if rows:
            result["r"] = invoke("show_pathway",
                                 name_or_id=str(rows[0]["id"]))

    t = threading.Thread(target=bg)
    t.start()
    t.join(timeout=5.0)
    app.pump(100)
    assert "r" in result


def test_show_term_from_background_thread(app):
    from orgchem.agent.actions import invoke
    result = {}

    def bg():
        result["r"] = invoke("show_term", term="SN2")

    t = threading.Thread(target=bg)
    t.start()
    t.join(timeout=5.0)
    app.pump(100)
    assert "r" in result
    assert "error" not in result["r"]


def test_run_on_main_thread_sync_returns_result_inline(app):
    """When called on the main thread the sync variant runs inline."""
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    assert run_on_main_thread_sync(lambda: 42) == 42


def test_run_on_main_thread_sync_from_worker_returns_result(app):
    """From a worker thread, runs on main and returns the value."""
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    import time
    box = {}

    def bg():
        box["r"] = run_on_main_thread_sync(lambda: "from-main",
                                           timeout=5.0)

    t = threading.Thread(target=bg)
    t.start()
    # Drive the main loop so the queued callable executes.
    deadline = time.time() + 5.0
    while time.time() < deadline and "r" not in box:
        app.pump(20)
    t.join(timeout=1.0)
    assert box.get("r") == "from-main"


def test_run_on_main_thread_sync_propagates_exceptions(app):
    """Exceptions raised on the main thread re-raise on the worker."""
    from orgchem.agent._gui_dispatch import run_on_main_thread_sync
    import time
    errors = []

    def raises():
        raise ValueError("boom from main")

    def bg():
        try:
            run_on_main_thread_sync(raises, timeout=3.0)
        except ValueError as e:
            errors.append(str(e))

    t = threading.Thread(target=bg)
    t.start()
    deadline = time.time() + 3.0
    while time.time() < deadline and not errors:
        app.pump(20)
    t.join(timeout=1.0)
    assert errors and "boom from main" in errors[0]


def test_screenshot_window_from_worker(app, tmp_path):
    """Round-57 regression: taking a screenshot from a worker
    thread must round-trip through the main thread and return the
    saved path — not crash or lose the file."""
    from orgchem.agent.actions import invoke
    box = {}
    out_path = tmp_path / "shot.png"

    def bg():
        try:
            box["r"] = invoke("screenshot_window",
                              path=str(out_path), settle_ms=50)
        except Exception as e:  # noqa: BLE001
            box["exc"] = e

    import time
    t = threading.Thread(target=bg)
    t.start()
    deadline = time.time() + 15.0
    while time.time() < deadline and "r" not in box and "exc" not in box:
        app.pump(50)
    t.join(timeout=2.0)
    assert "exc" not in box, box.get("exc")
    assert "r" in box
    r = box["r"]
    assert "error" not in r, r
    assert out_path.exists()
    assert out_path.stat().st_size > 1000


def test_show_ligand_binding_from_background_thread_does_not_crash(app):
    """The end-to-end flow the crashed user saw — calling
    show_ligand_binding from a worker thread. We don't require the
    actual PDB fetch to succeed (it may be network-gated); the
    point is the GUI dispatch doesn't take down the process."""
    from orgchem.agent.actions import invoke
    result = {}

    def bg():
        try:
            result["r"] = invoke(
                "show_ligand_binding",
                pdb_id="2YDO", ligand_name="ADN",
            )
        except Exception as e:  # noqa: BLE001
            result["exc"] = e

    t = threading.Thread(target=bg)
    t.start()
    t.join(timeout=30.0)
    app.pump(100)
    # Either a clean response or a structured error — but never
    # an unhandled exception that would have aborted the process.
    assert "exc" not in result, result.get("exc")
    assert "r" in result
