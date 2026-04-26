"""Phase 37a (round 136) — pytest-qt cases for the
*Tools → Qualitative inorganic tests…* dialog.

Drives the dialog headlessly to verify (a) construction, (b)
category-combo + free-text filtering of the row list, (c) the
detail pane updates on selection, (d) the colour swatch picks
up the entry's `colour_hex`, (e) the `select_test(test_id)`
programmatic path used by the `open_qualitative_tests` agent
action.
"""
from __future__ import annotations
import os

import pytest

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import qualitative_tests as mod
    mod.QualitativeTestsDialog._instance = None
    yield
    mod.QualitativeTestsDialog._instance = None


# ---- construction ---------------------------------------------

def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 30
    assert not d.isModal()


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    a = QualitativeTestsDialog.singleton(parent=app.window)
    b = QualitativeTestsDialog.singleton(parent=app.window)
    assert a is b


# ---- filtering ------------------------------------------------

def test_category_combo_filters_list(app, qtbot):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    full = d._list.count()
    # Switch to halide-only.
    idx = d._cat_combo.findText("halide")
    assert idx >= 0
    d._cat_combo.setCurrentIndex(idx)
    halide_count = d._list.count()
    assert halide_count == 3   # Cl⁻, Br⁻, I⁻
    assert halide_count < full


def test_text_filter_narrows_list(app, qtbot):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("copper")
    # Should match the flame + hydroxide copper entries (≥ 2).
    assert d._list.count() >= 2


def test_filter_with_no_matches_shows_blank(app, qtbot):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no tests" in d._title.text().lower()


# ---- selection updates the detail pane ------------------------

def test_selection_updates_title_and_detail(app, qtbot):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    # First row should have auto-selected on construction.
    title = d._title.text()
    detail_html = d._detail.toHtml()
    assert title  # not empty
    assert "Procedure" in detail_html
    assert "Reagents" in detail_html


def test_select_test_focuses_specific_row(app, qtbot):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_test("flame-na")
    assert ok is True
    assert "Sodium" in d._title.text()


def test_select_unknown_test_returns_false(app, qtbot):
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_test("does-not-exist") is False


# ---- colour swatch --------------------------------------------

def test_swatch_updates_with_selection(app, qtbot):
    """The swatch's stylesheet should contain the entry's
    colour hex after selection."""
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    d = QualitativeTestsDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_test("flame-na")     # sodium yellow #FFD700
    style = d._swatch.styleSheet().lower()
    assert "#ffd700" in style
    d.select_test("hydroxide-cu2")  # blue #1E90FF
    style = d._swatch.styleSheet().lower()
    assert "#1e90ff" in style


# ---- agent action wiring --------------------------------------

def test_open_action_fires_dialog(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.qualitative_tests import (
        QualitativeTestsDialog,
    )
    res = invoke("open_qualitative_tests")
    assert res.get("opened") is True
    assert res.get("selected") is False  # no test_id given
    assert QualitativeTestsDialog._instance is not None


def test_open_action_with_test_id_focuses_row(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_qualitative_tests", test_id="flame-ca")
    assert res.get("opened") is True
    assert res.get("selected") is True
