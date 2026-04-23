"""Tests for the Phase 30 Macromolecules secondary window.

The unified window hosts proteins + carbohydrates + lipids + NA
panels as inner tabs. Covers: menu construction, lazy build,
focus-tab, re-open raises without reconstructing, agent action,
GUI audit, and the NA → Proteins cross-nav that now lives inside
the window instead of the main tabbar.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_main_tabbar_no_longer_lists_macromolecules(app):
    win = app.window
    labels = [win.tabs.tabText(i) for i in range(win.tabs.count())]
    for label in ("Proteins", "Carbohydrates", "Lipids", "Nucleic acids"):
        assert label not in labels, (
            f"{label} still on main tabbar: {labels}"
        )


def test_open_window_returns_same_instance(app):
    """Calling the opener twice should not construct a fresh
    window — it's a single persistent instance."""
    win = app.window
    w1 = win.open_macromolecules_window()
    w2 = win.open_macromolecules_window()
    assert w1 is w2


def test_window_hosts_four_inner_tabs(app):
    mw = app.window.open_macromolecules_window()
    inner = [mw.tabs.tabText(i) for i in range(mw.tabs.count())]
    for expected in ("Proteins", "Carbohydrates", "Lipids",
                     "Nucleic acids"):
        assert expected in inner, inner


def test_switch_to_focuses_tab(app):
    mw = app.window.open_macromolecules_window()
    assert mw.switch_to("Lipids") is True
    assert mw.tabs.tabText(mw.tabs.currentIndex()) == "Lipids"
    assert mw.switch_to("Carbohydrates") is True
    assert mw.tabs.tabText(mw.tabs.currentIndex()) == "Carbohydrates"


def test_switch_to_unknown_label_returns_false(app):
    mw = app.window.open_macromolecules_window()
    assert mw.switch_to("Does-not-exist") is False


def test_inner_panels_are_the_mainwindow_panel_attributes(app):
    """Cross-panel code still hits the main window's ``self.proteins``
    etc. — those attributes must be *the same widget* as the inner
    tab or the NA fetch-PDB handoff would operate on a stale panel."""
    win = app.window
    mw = win.open_macromolecules_window()
    by_label: dict[str, object] = {
        mw.tabs.tabText(i): mw.tabs.widget(i)
        for i in range(mw.tabs.count())
    }
    assert by_label["Proteins"] is win.proteins
    assert by_label["Carbohydrates"] is win.carbohydrates
    assert by_label["Lipids"] is win.lipids
    assert by_label["Nucleic acids"] is win.nucleic_acids


def test_agent_action_opens_window_and_reports_state(app):
    from orgchem.agent.actions import invoke
    result = invoke("open_macromolecules_window", tab="Lipids")
    assert result.get("shown") is True
    assert result["active_tab"] == "Lipids"
    assert set(result["tabs"]) == {
        "Proteins", "Carbohydrates", "Lipids", "Nucleic acids",
    }


def test_audit_entry_for_window_action(app):
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    entry = GUI_ENTRY_POINTS.get("open_macromolecules_window", "")
    assert "Window → Macromolecules" in entry


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
