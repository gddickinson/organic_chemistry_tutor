"""Phase 37d (round 139) — pytest-qt cases for the
*Tools → Spectrophotometry techniques…* dialog.
"""
from __future__ import annotations
import math
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
    from orgchem.gui.dialogs import spectrophotometry_methods as mod
    mod.SpectrophotometryDialog._instance = None
    yield
    mod.SpectrophotometryDialog._instance = None


# ---- construction ---------------------------------------------

def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 12
    assert not d.isModal()


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    a = SpectrophotometryDialog.singleton(parent=app.window)
    b = SpectrophotometryDialog.singleton(parent=app.window)
    assert a is b


# ---- filtering ------------------------------------------------

def test_category_combo_filters_list(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    full = d._list.count()
    idx = d._cat_combo.findText("atomic")
    assert idx >= 0
    d._cat_combo.setCurrentIndex(idx)
    n = d._list.count()
    assert n == 3   # AAS + ICP-OES + ICP-MS
    assert n < full


def test_text_filter_narrows_list(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("nmr")
    assert d._list.count() == 1


def test_filter_with_no_matches_shows_blank(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no methods" in d._title.text().lower()


# ---- selection updates the detail pane ------------------------

def test_first_method_auto_selected(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    title = d._title.text()
    assert title and "Select" not in title
    html = d._detail.toHtml()
    for section in ("Principle", "Light source",
                    "Sample handling", "Detector",
                    "Procedure"):
        assert section in html


def test_select_method_focuses_specific_row(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_method("nmr")
    assert ok is True
    assert "NMR" in d._title.text()


def test_select_unknown_method_returns_false(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_method("does-not-exist") is False


# ---- Beer-Lambert calculator widget ---------------------------

def test_beer_lambert_solver_fills_concentration(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    d._a_spin.setValue(0.42)
    d._eps_spin.setValue(10500.0)
    d._l_spin.setValue(1.0)
    # Concentration left at 0 (blank).
    d._on_beer_lambert_solve()
    assert math.isclose(d._c_spin.value(), 4.0e-5, rel_tol=1e-3)
    assert "c =" in d._bl_status.text()


def test_beer_lambert_solver_fills_absorbance(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    d._eps_spin.setValue(10500.0)
    d._l_spin.setValue(1.0)
    d._c_spin.setValue(4.0e-5)
    d._on_beer_lambert_solve()
    assert math.isclose(d._a_spin.value(), 0.42, rel_tol=1e-3)


def test_beer_lambert_solver_complains_when_two_blank(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    d._a_spin.setValue(0.42)
    d._eps_spin.setValue(10500.0)
    # l + c both blank.
    d._on_beer_lambert_solve()
    assert "error" in d._bl_status.text().lower()


def test_beer_lambert_solver_clear_resets(app, qtbot):
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    d = SpectrophotometryDialog(parent=app.window)
    qtbot.addWidget(d)
    d._a_spin.setValue(1.0)
    d._eps_spin.setValue(2.0)
    d._on_beer_lambert_clear()
    for s in (d._a_spin, d._eps_spin, d._l_spin, d._c_spin):
        assert s.value() == 0.0


# ---- agent action wiring --------------------------------------

def test_open_action_fires_dialog(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.spectrophotometry_methods import (
        SpectrophotometryDialog,
    )
    res = invoke("open_spectrophotometry")
    assert res.get("opened") is True
    assert res.get("selected") is False
    assert SpectrophotometryDialog._instance is not None


def test_open_action_with_id_focuses_row(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_spectrophotometry", method_id="cd")
    assert res.get("opened") is True
    assert res.get("selected") is True
