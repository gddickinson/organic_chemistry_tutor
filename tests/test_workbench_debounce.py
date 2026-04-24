"""Regression tests for the Workbench rebuild-debouncer.

User report (2026-04-23 round 67): running demo 02
(``02_scene_composer_basics.py``) from the Script Editor crashed
the app with ``Compositor returned null texture`` + SIGTRAP —
caused by six rapid ``setHtml`` calls thrashing the macOS Metal
compositor.

Fix: ``WorkbenchWidget._schedule_rebuild`` coalesces scene events
in a single-shot QTimer, so a burst of adds collapses into one
HTML load after the quiet window.  These tests pin that behaviour.
"""
from __future__ import annotations

import pytest

from orgchem.agent.headless import HeadlessApp
from orgchem.scene import reset_current_scene

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    with HeadlessApp() as app:
        yield app


def test_rapid_adds_collapse_into_one_rebuild(_app, qtbot):
    """Adding six molecules in a tight loop must trigger at most
    ONE HTML setHtml call on the embedded QWebEngineView, not six.

    Reproduces the pattern of demo 02 that caused the SIGTRAP on
    macOS.  With the queued-connection + debounce fix, the whole
    burst coalesces.
    """
    from orgchem.gui.panels.workbench import WorkbenchWidget
    from orgchem.scene import current_scene

    reset_current_scene()
    widget = WorkbenchWidget()
    qtbot.addWidget(widget)
    baseline = WorkbenchWidget.rebuild_count

    scene = current_scene()
    # Six adds in a row — the exact pattern demo 02 uses.
    for i, smi in enumerate(["C", "CC", "CCC", "CCCC", "CCCCC",
                             "C1CCCCC1"]):
        scene.add_molecule(smi, track=f"h{i}")

    # Wait for the queued-connection slots + the debounce window
    # to drain before we count rebuilds.
    qtbot.waitUntil(
        lambda: (not widget._rebuild_pending
                 and widget._tracks_list.count() == 6),
        timeout=3_000,
    )

    # At most ONE additional rebuild should have run for the whole
    # burst — not six.  (Exactly one under the normal queued path;
    # leave slack for ≤ 2 to tolerate timing jitter where the first
    # event already drained before later ones arrived.)
    delta = WorkbenchWidget.rebuild_count - baseline
    assert delta <= 2, (
        f"expected at most 2 rebuilds for 6 adds, got {delta}")
    # And all six tracks must be present in the widget's scene.
    assert len(widget._scene.tracks()) == 6


def test_tracks_list_catches_up_after_queued_events(_app, qtbot):
    """Even with the queued-connection bridge, the right-side tracks
    list must end up reflecting every scene event once the event
    loop drains — no lost adds."""
    from orgchem.gui.panels.workbench import WorkbenchWidget
    from orgchem.scene import current_scene

    reset_current_scene()
    widget = WorkbenchWidget()
    qtbot.addWidget(widget)
    scene = current_scene()

    for i in range(4):
        scene.add_molecule("CCO", track=f"mol{i}")

    qtbot.waitUntil(
        lambda: widget._tracks_list.count() == 4,
        timeout=2_000,
    )


def test_subsequent_burst_after_quiet_window_still_debounced(_app, qtbot):
    """A second burst after the first settled must also coalesce —
    not fall through to one-rebuild-per-event."""
    from orgchem.gui.panels.workbench import WorkbenchWidget
    from orgchem.scene import current_scene

    reset_current_scene()
    widget = WorkbenchWidget()
    qtbot.addWidget(widget)
    scene = current_scene()

    # First burst.
    for i in range(3):
        scene.add_molecule("CCO", track=f"a{i}")
    qtbot.waitUntil(
        lambda: (not widget._rebuild_pending
                 and widget._tracks_list.count() == 3),
        timeout=2_000,
    )
    after_first = WorkbenchWidget.rebuild_count

    # Second burst.
    for i in range(3):
        scene.add_molecule("CC", track=f"b{i}")
    qtbot.waitUntil(
        lambda: (not widget._rebuild_pending
                 and widget._tracks_list.count() == 6),
        timeout=2_000,
    )

    delta = WorkbenchWidget.rebuild_count - after_first
    assert delta <= 2, (
        f"second burst coalesce failed, got {delta} rebuilds")
