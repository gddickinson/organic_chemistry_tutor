"""Phase GM-1.0 (round 230) — tests for the OrgChem-side
glue wiring the Genetics + Molecular Biology Studio sibling
into the platform.

Verifies the 6-file glue pattern that ships with every
sibling: headless import + conftest import + Window-menu
entry + main-window slot + GUI audit + agent-surface audit
+ category summary.
"""
from __future__ import annotations
import os
import pytest


# ----------------------------------------------------------------
# Pure-Python (no Qt) glue
# ----------------------------------------------------------------

def test_genetics_imports_via_orgchem_headless():
    """``orgchem.agent.headless.HeadlessApp`` must import the
    genetics sibling so its actions register before any test
    inspects the registry."""
    import inspect
    from orgchem.agent import headless
    src = inspect.getsource(headless)
    assert "import genetics" in src


def test_genetics_imports_via_conftest():
    from pathlib import Path
    src = Path("tests/conftest.py").read_text()
    assert "import genetics" in src


def test_actions_meta_has_genetics_techniques_summary():
    from orgchem.agent.actions_meta import _CATEGORY_SUMMARIES
    assert "genetics-techniques" in _CATEGORY_SUMMARIES
    summary = _CATEGORY_SUMMARIES["genetics-techniques"]
    assert len(summary) > 50, \
        "Category summary should be a substantive description"


def test_gui_audit_has_all_five_genetics_actions():
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    expected = (
        "open_genetics_studio",
        "list_genetics_techniques",
        "get_genetics_technique",
        "find_genetics_techniques",
        "genetics_techniques_for_application",
    )
    for name in expected:
        assert name in GUI_ENTRY_POINTS, \
            f"GUI_ENTRY_POINTS missing {name!r}"
        entry = GUI_ENTRY_POINTS[name]
        assert "Genetics" in entry or "genetics" in entry, \
            f"GUI entry for {name!r} doesn't mention Genetics"


def test_agent_surface_audit_has_genetics_surface():
    from orgchem.core.agent_surface_audit import (
        EXPECTED_SURFACES,
    )
    matches = [s for s in EXPECTED_SURFACES
               if "Genetics" in s.catalogue]
    assert len(matches) >= 1, \
        "EXPECTED_SURFACES is missing the Genetics entry"
    spec = matches[0]
    assert spec.opener == "open_genetics_studio"
    assert spec.list_action == "list_genetics_techniques"
    assert spec.get_action == "get_genetics_technique"
    assert spec.find_action == "find_genetics_techniques"


# ----------------------------------------------------------------
# Qt-touching glue
# ----------------------------------------------------------------

pytest.importorskip("PySide6")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_main_window_has_genetics_attribute(app):
    """The OrgChem main window must declare a
    ``_genetics_window`` attribute (initially ``None``,
    populated lazily on first open)."""
    main = app.window
    assert hasattr(main, "_genetics_window")


def test_main_window_open_genetics_method_exists(app):
    main = app.window
    assert hasattr(main, "open_genetics_studio_window")
    assert callable(main.open_genetics_studio_window)


def test_window_menu_has_genetics_action(app):
    """The Window menu must expose the Genetics studio
    opener."""
    main = app.window
    found = False
    for action in main.menuBar().actions():
        if action.text() != "&Window":
            continue
        for sub in action.menu().actions():
            if "Genetics" in sub.text():
                found = True
                # Verify shortcut.
                shortcut = sub.shortcut().toString()
                assert "Ctrl+Alt+G" in shortcut, \
                    (f"Genetics shortcut is {shortcut!r}, "
                     f"expected 'Ctrl+Alt+G'")
                break
    assert found, "Window menu missing Genetics studio entry"


def test_open_genetics_studio_window_creates_singleton(app):
    main = app.window
    # Reset so we can observe the lazy-construction.
    main._genetics_window = None
    win1 = main.open_genetics_studio_window()
    assert win1 is not None
    assert main._genetics_window is win1
    win2 = main.open_genetics_studio_window()
    assert win2 is win1


def test_open_genetics_studio_window_with_tab_focus(app):
    main = app.window
    win = main.open_genetics_studio_window(
        tab_label="Tutorials")
    assert win.tabs.currentIndex() == 2
