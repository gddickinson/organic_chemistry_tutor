"""Phase 38b (round 141) — pytest-qt cases for the
*Tools → Lab setups…* dialog.
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
    from orgchem.gui.dialogs import lab_setups as mod
    mod.LabSetupsDialog._instance = None
    yield
    mod.LabSetupsDialog._instance = None


def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._list.count() >= 8
    assert not d.isModal()


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    a = LabSetupsDialog.singleton(parent=app.window)
    b = LabSetupsDialog.singleton(parent=app.window)
    assert a is b


def test_text_filter_narrows_list(app, qtbot):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("reflux")
    # reflux + reflux_with_addition = 2 rows.
    assert d._list.count() == 2


def test_filter_with_no_matches_shows_blank(app, qtbot):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    d._filter_edit.setText("zzzz-no-match")
    assert d._list.count() == 0
    assert "no setups" in d._title.text().lower()


def test_first_setup_auto_selected_with_full_detail(app, qtbot):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert "Select" not in d._title.text()
    html = d._detail.toHtml()
    for section in ("Purpose", "Equipment", "Connections",
                    "Procedure", "Pedagogical notes"):
        assert section in html


def test_select_setup_focuses_specific_row(app, qtbot):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_setup("vacuum_filtration")
    assert ok is True
    assert "Vacuum filtration" in d._title.text()


def test_detail_shows_resolved_equipment_names(app, qtbot):
    """Equipment list should render the human-readable
    NAME (from Phase 38a) for each id."""
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_setup("simple_distillation")
    html = d._detail.toHtml()
    # Names from the Phase-38a catalogue should appear.
    assert "Round-bottom flask" in html
    assert "Liebig condenser" in html
    assert "Distillation head" in html


def test_detail_shows_connection_table(app, qtbot):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    d.select_setup("simple_distillation")
    html = d._detail.toHtml()
    # Port names appear in the connection list.
    assert "neck" in html
    assert "thermometer" in html


def test_select_unknown_setup_returns_false(app, qtbot):
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    d = LabSetupsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_setup("does-not-exist") is False


def test_open_action_fires_dialog(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.lab_setups import LabSetupsDialog
    res = invoke("open_lab_setups")
    assert res.get("opened") is True
    assert res.get("selected") is False
    assert LabSetupsDialog._instance is not None


def test_open_action_with_id_focuses_row(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_lab_setups", setup_id="recrystallisation")
    assert res.get("opened") is True
    assert res.get("selected") is True
