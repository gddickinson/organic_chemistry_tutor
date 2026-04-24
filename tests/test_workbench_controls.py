"""Phase 32c tests — per-track row controls + scene-wide toolbar.

User directive 2026-04-23 round 69: "Can you add more controls to
the workbench viewer? ... including the ability to toggle different
tracks."  These tests pin the wiring of the inline track controls
and the three new toolbar actions (Fit-to-view / Toggle-bg /
Export-HTML).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from orgchem.agent.headless import HeadlessApp
from orgchem.scene import reset_current_scene

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    with HeadlessApp() as app:
        yield app


def _make_widget(qtbot):
    from orgchem.gui.panels.workbench import WorkbenchWidget
    from orgchem.scene import current_scene

    reset_current_scene()
    widget = WorkbenchWidget()
    qtbot.addWidget(widget)
    return widget, current_scene()


def _find_row(widget, track_name: str):
    """Return the TrackRow widget for a given track name, or None."""
    lst = widget._tracks_list
    for i in range(lst.count()):
        item = lst.item(i)
        row = lst.itemWidget(item)
        if row is not None and row.track_name == track_name:
            return row
    return None


def test_track_row_checkbox_toggles_visibility(_app, qtbot):
    widget, scene = _make_widget(qtbot)
    scene.add_molecule("CCO", track="eth")
    qtbot.waitUntil(
        lambda: widget._tracks_list.count() == 1, timeout=2_000)

    row = _find_row(widget, "eth")
    assert row is not None

    row._check.setChecked(False)        # user clicks the checkbox
    # The signal fires synchronously in Qt, so the Scene sees the
    # new state immediately.
    assert scene.tracks()[0].visible is False

    row._check.setChecked(True)
    assert scene.tracks()[0].visible is True


def test_track_row_style_combo_updates_scene(_app, qtbot):
    widget, scene = _make_widget(qtbot)
    scene.add_molecule("CCO", track="eth")
    qtbot.waitUntil(
        lambda: widget._tracks_list.count() == 1, timeout=2_000)

    row = _find_row(widget, "eth")
    row._style.setCurrentText("sphere")
    assert scene.tracks()[0].style == "sphere"


def test_track_row_remove_button_drops_track(_app, qtbot):
    widget, scene = _make_widget(qtbot)
    scene.add_molecule("CCO", track="eth")
    scene.add_molecule("CC",  track="eta")
    qtbot.waitUntil(
        lambda: widget._tracks_list.count() == 2, timeout=2_000)

    row = _find_row(widget, "eth")
    row._remove.click()
    qtbot.waitUntil(
        lambda: len(scene.tracks()) == 1, timeout=2_000)
    assert [t.name for t in scene.tracks()] == ["eta"]


def test_toggle_background_flips_scene_colour(_app, qtbot):
    widget, _scene = _make_widget(qtbot)
    assert widget._background == "#1e1e1e"
    widget._on_toggle_background()
    assert widget._background == "#ffffff"
    widget._on_toggle_background()
    assert widget._background == "#1e1e1e"


def test_export_html_writes_file(tmp_path, _app, qtbot):
    widget, scene = _make_widget(qtbot)
    scene.add_molecule("CCO")

    out = tmp_path / "scene.html"
    # Short-circuit the file-dialog by monkey-patching
    # ``QFileDialog.getSaveFileName`` so the handler gets the
    # path without user interaction.
    from PySide6.QtWidgets import QFileDialog
    original = QFileDialog.getSaveFileName
    QFileDialog.getSaveFileName = staticmethod(
        lambda *a, **kw: (str(out), "HTML documents (*.html)"))
    try:
        widget._on_export_html_clicked()
    finally:
        QFileDialog.getSaveFileName = original

    assert out.exists()
    body = out.read_text()
    assert "<!DOCTYPE html>" in body
    assert "v.addModel" in body   # at least one model got serialised


def test_fit_to_view_schedules_rebuild(_app, qtbot):
    from orgchem.gui.panels.workbench import WorkbenchWidget

    widget, scene = _make_widget(qtbot)
    scene.add_molecule("CCO")
    qtbot.waitUntil(
        lambda: not widget._rebuild_pending, timeout=2_000)

    baseline = WorkbenchWidget.rebuild_count
    widget._on_fit_clicked()
    qtbot.waitUntil(
        lambda: not widget._rebuild_pending, timeout=2_000)
    assert WorkbenchWidget.rebuild_count > baseline


def test_track_row_signals_have_correct_track_name(_app, qtbot):
    """TrackRow emissions must carry the stable track name so the
    parent can route the mutation back to the Scene even if list
    indices shuffle mid-update."""
    widget, scene = _make_widget(qtbot)
    scene.add_molecule("CCO", track="alpha")
    scene.add_molecule("CC",  track="beta")
    qtbot.waitUntil(
        lambda: widget._tracks_list.count() == 2, timeout=2_000)

    row_beta = _find_row(widget, "beta")
    assert row_beta.track_name == "beta"
    row_beta._style.setCurrentText("sphere")
    # The beta track's style changed — alpha's remains default.
    by_name = {t.name: t for t in scene.tracks()}
    assert by_name["beta"].style == "sphere"
    assert by_name["alpha"].style == "stick"
