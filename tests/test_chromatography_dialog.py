"""Phase 37c (round 138) — pytest-qt cases for the
*Tools → Chromatography techniques…* dialog.
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
    from orgchem.gui.dialogs import chromatography_methods as mod
    mod.ChromatographyMethodsDialog._instance = None
    yield
    mod.ChromatographyMethodsDialog._instance = None


# ---- construction ---------------------------------------------

def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    d = ChromatographyMethodsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 15
    assert not d.isModal()


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    a = ChromatographyMethodsDialog.singleton(parent=app.window)
    b = ChromatographyMethodsDialog.singleton(parent=app.window)
    assert a is b


# ---- filtering ------------------------------------------------

def test_category_combo_filters_list(app, qtbot):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    d = ChromatographyMethodsDialog(parent=app.window)
    qtbot.addWidget(d)
    full = d._list.count()
    idx = d._cat_combo.findText("protein")
    assert idx >= 0
    d._cat_combo.setCurrentIndex(idx)
    n = d._list.count()
    assert n == 4   # FPLC, IEX, SEC, affinity
    assert n < full


def test_text_filter_narrows_list(app, qtbot):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    d = ChromatographyMethodsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("HPLC")
    # HPLC + LC-MS + HILIC contain "hplc" / "lc" tokens.
    assert d._list.count() >= 1


def test_filter_with_no_matches_shows_blank(app, qtbot):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    d = ChromatographyMethodsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no methods" in d._title.text().lower()


# ---- selection updates the detail pane ------------------------

def test_first_method_auto_selected(app, qtbot):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    d = ChromatographyMethodsDialog(parent=app.window)
    qtbot.addWidget(d)
    title = d._title.text()
    assert title and "Select" not in title
    html = d._detail.toHtml()
    # Detail card should include all the standard sections.
    for section in ("Principle", "Stationary phase",
                    "Mobile phase", "Detector", "Procedure"):
        assert section in html


def test_select_method_focuses_specific_row(app, qtbot):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    d = ChromatographyMethodsDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_method("hplc")
    assert ok is True
    assert "HPLC" in d._title.text()


def test_select_unknown_method_returns_false(app, qtbot):
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    d = ChromatographyMethodsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_method("does-not-exist") is False


# ---- agent action wiring --------------------------------------

def test_open_action_fires_dialog(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.chromatography_methods import (
        ChromatographyMethodsDialog,
    )
    res = invoke("open_chromatography_methods")
    assert res.get("opened") is True
    assert res.get("selected") is False
    assert ChromatographyMethodsDialog._instance is not None


def test_open_action_with_id_focuses_row(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_chromatography_methods", method_id="sfc")
    assert res.get("opened") is True
    assert res.get("selected") is True
