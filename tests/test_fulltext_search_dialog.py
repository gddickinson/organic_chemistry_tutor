"""Phase 33b — Ctrl+F FulltextSearchDialog + dispatch routing tests."""
from __future__ import annotations

import pytest

from orgchem.agent.headless import HeadlessApp

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    with HeadlessApp() as app:
        yield app


def test_dialog_opens_with_empty_state(_app, qtbot):
    from orgchem.gui.dialogs.fulltext_search import FulltextSearchDialog

    dlg = FulltextSearchDialog(parent=None)
    qtbot.addWidget(dlg)

    # Empty query → placeholder row in list, all 5 kinds checked.
    assert dlg._query.text() == ""
    assert dlg._list.count() == 1
    for cb in dlg._kind_checks.values():
        assert cb.isChecked()


def test_dialog_live_search_after_typing(_app, qtbot):
    from orgchem.gui.dialogs.fulltext_search import FulltextSearchDialog

    dlg = FulltextSearchDialog(parent=None)
    qtbot.addWidget(dlg)
    dlg._query.setText("caffeine")
    # Debounce timer needs to fire — waitUntil until results land.
    qtbot.waitUntil(lambda: dlg._list.count() > 1, timeout=3_000)
    assert "result" in dlg._status.text().lower()


def test_dialog_kind_filter_restricts_results(_app, qtbot):
    from orgchem.gui.dialogs.fulltext_search import FulltextSearchDialog

    dlg = FulltextSearchDialog(parent=None)
    qtbot.addWidget(dlg)
    # Only glossary.
    for kind, cb in dlg._kind_checks.items():
        cb.setChecked(kind == "glossary")
    dlg._query.setText("regioselectivity")
    qtbot.waitUntil(lambda: len(dlg._results) > 0, timeout=3_000)
    kinds = {r.kind for r in dlg._results}
    assert kinds == {"glossary"}


def test_dialog_no_kinds_shows_helpful_message(_app, qtbot):
    from orgchem.gui.dialogs.fulltext_search import FulltextSearchDialog

    dlg = FulltextSearchDialog(parent=None)
    qtbot.addWidget(dlg)
    for cb in dlg._kind_checks.values():
        cb.setChecked(False)
    dlg._query.setText("anything")
    qtbot.waitUntil(
        lambda: "at least one" in dlg._status.text().lower(),
        timeout=3_000,
    )


# ---------- dispatch_search_result routing ----------

def _fake_main_win():
    """Minimal stand-in with the attributes dispatch_search_result
    consults.  Collects calls for assertions."""
    class _Tabs:
        def __init__(self):
            self._labels = ["Molecule Workspace", "Reactions",
                            "Compare", "Workbench", "Synthesis",
                            "Glossary", "Tutorials"]
            self._current = 0
        def count(self): return len(self._labels)
        def tabText(self, i): return self._labels[i]
        def setCurrentIndex(self, i): self._current = i

    class _Glossary:
        def __init__(self): self.focused = None
        def focus_term(self, t):
            self.focused = t
            return True

    class _Reactions:
        def __init__(self): self.displayed = None
        def _display(self, rid):
            self.displayed = rid

    class _Synthesis:
        def __init__(self): self.displayed = None
        def _display(self, pid):
            self.displayed = pid

    class _MW:
        def __init__(self):
            self.tabs = _Tabs()
            self.glossary = _Glossary()
            self.reactions = _Reactions()
            self.synthesis = _Synthesis()

    return _MW()


def test_dispatch_routes_glossary_to_focus_term():
    from orgchem.core.fulltext_search import SearchResult
    from orgchem.gui.dialogs.fulltext_search import dispatch_search_result

    mw = _fake_main_win()
    r = SearchResult(kind="glossary", title="SN2", snippet="",
                     score=1.0, key={"term": "SN2"})
    assert dispatch_search_result(r, mw) is True
    assert mw.glossary.focused == "SN2"
    assert mw.tabs._current == mw.tabs._labels.index("Glossary")


def test_dispatch_routes_pathway_to_synthesis():
    from orgchem.core.fulltext_search import SearchResult
    from orgchem.gui.dialogs.fulltext_search import dispatch_search_result

    mw = _fake_main_win()
    r = SearchResult(kind="pathway", title="Aspirin", snippet="",
                     score=1.0, key={"pathway_id": 7})
    assert dispatch_search_result(r, mw) is True
    assert mw.synthesis.displayed == 7
    assert mw.tabs._current == mw.tabs._labels.index("Synthesis")


def test_dispatch_routes_reaction_to_reactions():
    from orgchem.core.fulltext_search import SearchResult
    from orgchem.gui.dialogs.fulltext_search import dispatch_search_result

    mw = _fake_main_win()
    r = SearchResult(kind="reaction", title="Diels-Alder", snippet="",
                     score=1.0, key={"reaction_id": 42})
    assert dispatch_search_result(r, mw) is True
    assert mw.reactions.displayed == 42


def test_dispatch_routes_molecule_via_bus():
    from unittest.mock import MagicMock, patch
    from orgchem.core.fulltext_search import SearchResult
    from orgchem.gui.dialogs.fulltext_search import dispatch_search_result

    mw = _fake_main_win()
    r = SearchResult(kind="molecule", title="Caffeine", snippet="",
                     score=1.0, key={"molecule_id": 1})
    fake_bus = MagicMock()
    with patch("orgchem.messaging.bus.bus", return_value=fake_bus):
        assert dispatch_search_result(r, mw) is True
    fake_bus.molecule_selected.emit.assert_called_once_with(1)


def test_dispatch_returns_false_on_missing_key():
    from orgchem.core.fulltext_search import SearchResult
    from orgchem.gui.dialogs.fulltext_search import dispatch_search_result

    mw = _fake_main_win()
    r = SearchResult(kind="pathway", title="x", snippet="",
                     score=1.0, key={})   # no pathway_id
    assert dispatch_search_result(r, mw) is False


def test_dispatch_returns_false_on_none_main_win():
    from orgchem.core.fulltext_search import SearchResult
    from orgchem.gui.dialogs.fulltext_search import dispatch_search_result

    r = SearchResult(kind="glossary", title="x", snippet="",
                     score=1.0, key={"term": "x"})
    assert dispatch_search_result(r, None) is False
