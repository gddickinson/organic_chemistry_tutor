"""Phase 38a (round 140) — pytest-qt cases for the
*Tools → Lab equipment…* dialog.
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
    from orgchem.gui.dialogs import lab_equipment as mod
    mod.LabEquipmentDialog._instance = None
    yield
    mod.LabEquipmentDialog._instance = None


# ---- construction ---------------------------------------------

def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 35
    assert not d.isModal()


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    a = LabEquipmentDialog.singleton(parent=app.window)
    b = LabEquipmentDialog.singleton(parent=app.window)
    assert a is b


# ---- filtering ------------------------------------------------

def test_category_combo_filters_list(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    full = d._list.count()
    idx = d._cat_combo.findText("condenser")
    assert idx >= 0
    d._cat_combo.setCurrentIndex(idx)
    n = d._list.count()
    assert n >= 5   # liebig + allihn + graham + friedrichs + dimroth + air
    assert n < full


def test_text_filter_narrows_list(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("flask")
    # rbf + 3neck rbf + erlenmeyer + filter flask should match.
    assert d._list.count() >= 4


def test_filter_with_no_matches_shows_blank(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no equipment" in d._title.text().lower()


# ---- selection updates the detail pane ------------------------

def test_first_item_auto_selected(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    title = d._title.text()
    assert title and "Select" not in title
    html = d._detail.toHtml()
    for section in ("Description", "Typical uses"):
        assert section in html


def test_selecting_3neck_shows_three_ports_in_html(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_equipment("rbf_3neck")
    html = d._detail.toHtml()
    # Three port names should appear in the rendered detail.
    for port in ("center", "left", "right"):
        assert port in html.lower()


def test_select_equipment_focuses_specific_row(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_equipment("liebig_condenser")
    assert ok is True
    assert "Liebig" in d._title.text()


def test_select_unknown_equipment_returns_false(app, qtbot):
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    d = LabEquipmentDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_equipment("does-not-exist") is False


# ---- agent action wiring --------------------------------------

def test_open_action_fires_dialog(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.lab_equipment import (
        LabEquipmentDialog,
    )
    res = invoke("open_lab_equipment")
    assert res.get("opened") is True
    assert res.get("selected") is False
    assert LabEquipmentDialog._instance is not None


def test_open_action_with_id_focuses_row(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_lab_equipment", equipment_id="sep_funnel")
    assert res.get("opened") is True
    assert res.get("selected") is True
