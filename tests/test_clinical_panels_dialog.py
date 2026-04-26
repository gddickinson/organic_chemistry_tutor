"""Phase 37b (round 137) — pytest-qt cases for the
*Tools → Clinical lab panels…* dialog.
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
    from orgchem.gui.dialogs import clinical_panels as mod
    mod.ClinicalPanelsDialog._instance = None
    yield
    mod.ClinicalPanelsDialog._instance = None


# ---- construction ---------------------------------------------

def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    # Panel combo populated.
    assert d._panel_combo.count() >= 5
    assert not d.isModal()


def test_singleton_returns_same_instance(app):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    a = ClinicalPanelsDialog.singleton(parent=app.window)
    b = ClinicalPanelsDialog.singleton(parent=app.window)
    assert a is b


# ---- panel switching ------------------------------------------

def test_default_loads_first_panel_table(app, qtbot):
    """First panel (BMP) auto-loads on construction."""
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d._table.rowCount() == 8  # BMP


def test_switching_panel_repopulates_table(app, qtbot):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    # Switch to Lipid panel.
    idx = next(i for i in range(d._panel_combo.count())
               if d._panel_combo.itemData(i) == "lipid")
    d._panel_combo.setCurrentIndex(idx)
    assert d._table.rowCount() == 4


def test_panel_meta_text_includes_purpose(app, qtbot):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    text = d._panel_meta.text().lower()
    # Includes a "Purpose" header AND fasting line.
    assert "purpose" in text
    assert "fasting" in text


# ---- analyte row → detail pane --------------------------------

def test_first_analyte_auto_selected(app, qtbot):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    # Title should not be the placeholder; detail HTML
    # should include "Clinical significance".
    assert "Select" not in d._analyte_title.text()
    html = d._analyte_detail.toHtml()
    assert "Clinical significance" in html


def test_select_analyte_focuses_row(app, qtbot):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    ok = d.select_analyte("creatinine")
    assert ok is True
    assert "Creatinine" in d._analyte_title.text()


def test_select_analyte_not_in_panel_returns_false(app, qtbot):
    """LDL is in the Lipid panel, not the BMP — selecting it
    while BMP is loaded should fail cleanly."""
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_analyte("ldl_chol") is False


def test_select_panel_then_analyte(app, qtbot):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_panel("lipid") is True
    assert d.select_analyte("ldl_chol") is True
    assert "LDL" in d._analyte_title.text()


def test_select_panel_unknown_returns_false(app, qtbot):
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    d = ClinicalPanelsDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_panel("bogus") is False


# ---- agent action wiring --------------------------------------

def test_open_clinical_panels_action(app, qtbot):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.clinical_panels import (
        ClinicalPanelsDialog,
    )
    res = invoke("open_clinical_panels")
    assert res.get("opened") is True
    assert ClinicalPanelsDialog._instance is not None


def test_open_with_panel_and_analyte(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_clinical_panels",
                 panel_id="cmp", analyte_id="alt")
    assert res.get("opened") is True
    assert res.get("panel_selected") is True
    assert res.get("analyte_selected") is True


def test_open_with_unknown_analyte_returns_false_flag(app, qtbot):
    from orgchem.agent.actions import invoke
    res = invoke("open_clinical_panels",
                 panel_id="bmp", analyte_id="bogus")
    assert res.get("opened") is True
    assert res.get("panel_selected") is True
    assert res.get("analyte_selected") is False
