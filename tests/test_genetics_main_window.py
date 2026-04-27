"""Phase GM-1.0 (round 230) — GUI smoke tests for
GeneticsMainWindow.
"""
from __future__ import annotations
import os
import pytest


pytest.importorskip("PySide6")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_window_constructs_and_has_three_tabs(app):
    from genetics.gui.windows.genetics_main_window import (
        GeneticsMainWindow,
    )
    win = GeneticsMainWindow()
    assert win.tabs.count() == 3
    labels = [win.tabs.tabText(i)
              for i in range(win.tabs.count())]
    assert labels == [
        win.TAB_TECHNIQUES,
        win.TAB_CROSS_REFERENCES,
        win.TAB_TUTORIALS,
    ]


def test_window_title_set(app):
    from genetics.gui.windows.genetics_main_window import (
        GeneticsMainWindow,
    )
    win = GeneticsMainWindow()
    assert "Genetics" in win.windowTitle()


def test_switch_to_focuses_named_tab(app):
    from genetics.gui.windows.genetics_main_window import (
        GeneticsMainWindow,
    )
    win = GeneticsMainWindow()
    assert win.switch_to(win.TAB_CROSS_REFERENCES) is True
    assert win.tabs.currentIndex() == 1
    assert win.switch_to(win.TAB_TUTORIALS) is True
    assert win.tabs.currentIndex() == 2


def test_switch_to_unknown_tab_returns_false(app):
    from genetics.gui.windows.genetics_main_window import (
        GeneticsMainWindow,
    )
    win = GeneticsMainWindow()
    assert win.switch_to("Bogus tab name") is False


def test_open_studio_action_lazily_constructs_window(app):
    """``open_genetics_studio`` must lazily construct the
    window the first time + return the same singleton on
    subsequent calls."""
    from orgchem.agent.actions import invoke
    out1 = invoke("open_genetics_studio")
    assert out1.get("opened") is True
    main_win = app.window
    win1 = main_win._genetics_window
    assert win1 is not None
    out2 = invoke("open_genetics_studio")
    assert out2.get("opened") is True
    win2 = main_win._genetics_window
    assert win1 is win2  # Same singleton.


def test_open_studio_with_tab_arg_focuses_tab(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_genetics_studio",
                 tab="Cross-references")
    assert out.get("tab") == "Cross-references"
    main_win = app.window
    assert (main_win._genetics_window.tabs.currentIndex()
            == 1)
