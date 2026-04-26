"""Phase 41 (round 144) — pytest-qt cases for the
*Tools → Centrifugation…* dialog.
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
    from orgchem.gui.dialogs import centrifugation as mod
    mod.CentrifugationDialog._instance = None
    yield
    mod.CentrifugationDialog._instance = None


# ---- construction ---------------------------------------------

def test_dialog_constructs_with_four_tabs(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    labels = d.tab_labels()
    assert len(labels) == 4
    for must in ("Centrifuges", "Rotors", "Applications",
                 "g ↔ RPM calculator"):
        assert must in labels


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    a = CentrifugationDialog.singleton(parent=app.window)
    b = CentrifugationDialog.singleton(parent=app.window)
    assert a is b


# ---- catalogue tabs --------------------------------------------

def test_centrifuges_tab_lists_entries(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._cent_tab._list.count() >= 8


def test_centrifuges_tab_category_filter(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    # Switch to "ultracentrifuge" only.
    idx = d._cent_tab._cat_combo.findText("ultracentrifuge")
    assert idx >= 0
    d._cent_tab._cat_combo.setCurrentIndex(idx)
    assert d._cent_tab._list.count() >= 2  # Optima + WX 100


def test_select_centrifuge_focuses_row(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    # Move to all-categories first to make the row visible.
    d._cent_tab._cat_combo.setCurrentIndex(0)
    ok = d.select_centrifuge("ultra_optima_xpn")
    assert ok is True


def test_rotors_tab_lists_entries(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._rotor_tab._list.count() >= 8


def test_select_rotor_focuses_row(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_rotor("rotor_sw_41_ti")
    assert ok is True


def test_applications_tab_lists_entries(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._app_tab._list.count() >= 6


# ---- g ↔ rpm calculator tab -----------------------------------

def test_calculator_rotor_dropdown_auto_fills_radius(app, qtbot):
    """Picking a rotor from the dropdown should set the radius
    spin to that rotor's max_radius_cm."""
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    calc = d._calc_tab
    # Find the FA-45-24-11 entry (radius 8.4 cm) in the combo.
    idx = -1
    for i in range(calc._rotor_combo.count()):
        if calc._rotor_combo.itemData(i) == "rotor_fa_45_24_11":
            idx = i
            break
    assert idx >= 0
    calc._rotor_combo.setCurrentIndex(idx)
    assert math.isclose(calc._radius_spin.value(), 8.4,
                        rel_tol=1e-9)


def test_calculator_rpm_to_g_button(app, qtbot):
    """15 000 RPM @ 8.4 cm → 21 130 × g."""
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    calc = d._calc_tab
    calc._radius_spin.setValue(8.4)
    calc._rpm_spin.setValue(15000)
    calc._on_rpm_to_g()
    assert math.isclose(calc._g_spin.value(), 21130,
                        rel_tol=1e-3)


def test_calculator_g_to_rpm_button(app, qtbot):
    """13 000 × g @ 8.4 cm → ~11 766 RPM."""
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    calc = d._calc_tab
    calc._radius_spin.setValue(8.4)
    calc._g_spin.setValue(13000)
    calc._on_g_to_rpm()
    assert math.isclose(calc._rpm_spin.value(), 11765.5,
                        rel_tol=1e-3)


def test_calculator_overspeed_warning(app, qtbot):
    """Setting RPM above the selected rotor's max should
    surface an OVERSPEED warning in the status text."""
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    calc = d._calc_tab
    # Pick FA-45-24-11 (max 21 300 RPM) and exceed it.
    for i in range(calc._rotor_combo.count()):
        if calc._rotor_combo.itemData(i) == "rotor_fa_45_24_11":
            calc._rotor_combo.setCurrentIndex(i)
            break
    calc._rpm_spin.setValue(50000)   # WAY over max
    calc._on_rpm_to_g()
    assert "overspeed" in calc._status.text().lower()


def test_calculator_clear_resets(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    calc = d._calc_tab
    calc._rpm_spin.setValue(15000)
    calc._g_spin.setValue(21130)
    calc._on_clear()
    assert calc._rpm_spin.value() == 0
    assert calc._g_spin.value() == 0


def test_calculator_zero_rpm_error_path(app, qtbot):
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    d = CentrifugationDialog(parent=app.window)
    qtbot.addWidget(d)
    calc = d._calc_tab
    calc._radius_spin.setValue(8.4)
    calc._rpm_spin.setValue(0)
    calc._on_rpm_to_g()
    assert "error" in calc._status.text().lower()


# ---- agent action wiring --------------------------------------

def test_open_action_fires(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.centrifugation import (
        CentrifugationDialog,
    )
    res = invoke("open_centrifugation")
    assert res.get("opened") is True
    assert "Centrifuges" in res["available_tabs"]
    assert CentrifugationDialog._instance is not None


def test_open_action_with_tab(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_centrifugation",
                 tab="g ↔ RPM calculator")
    assert res.get("opened") is True
    assert res.get("selected_tab") is True


def test_open_action_with_rotor_id(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_centrifugation",
                 rotor_id="rotor_sw_41_ti")
    assert res.get("opened") is True
    assert res.get("selected_rotor") is True
