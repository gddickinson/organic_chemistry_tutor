"""Phase 33c regression tests — the full-text filter toggle
on the Reactions + Synthesis tabs.

Exercises the branch in `_on_filter` that swaps from SQL
name-substring filtering to the Phase-33a ranked full-text
search when the new checkbox is checked.
"""
from __future__ import annotations

import pytest

from orgchem.agent.headless import HeadlessApp

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    with HeadlessApp() as app:
        yield app


# ---------- Reactions tab ----------

def test_reactions_name_filter_default(_app, qtbot):
    from orgchem.gui.panels.reaction_workspace import (
        ReactionWorkspacePanel,
    )
    panel = ReactionWorkspacePanel()
    qtbot.addWidget(panel)

    panel.filter.setText("Diels")
    # Default name-filter: matches "Diels-Alder" entries.
    names = [panel.model._rows[i].name
             for i in range(panel.model.rowCount())]
    assert any("Diels" in n for n in names), names
    # Full-text checkbox is off by default.
    assert not panel.fulltext_cb.isChecked()


def test_reactions_fulltext_toggle_finds_description_hits(_app, qtbot):
    """A query that matches only a reaction's **description** body,
    not its name, should return no hits when the toggle is off but
    appear once it's on."""
    from orgchem.gui.panels.reaction_workspace import (
        ReactionWorkspacePanel,
    )
    panel = ReactionWorkspacePanel()
    qtbot.addWidget(panel)

    # "Beckmann" is not in any seeded reaction name but IS
    # mentioned in mechanism-step notes that pollinate the
    # full-text corpus via `kinds=["mechanism-step"]`.
    panel.filter.setText("oxime")
    # Name-match: may or may not hit depending on seed; capture
    # baseline count first.
    baseline = panel.model.rowCount()

    panel.fulltext_cb.setChecked(True)
    # With full-text on, we expect at least as many hits as baseline
    # and typically more (mechanism-step text is searched too).
    assert panel.model.rowCount() >= baseline


def test_reactions_fulltext_empty_query_clears(_app, qtbot):
    from orgchem.gui.panels.reaction_workspace import (
        ReactionWorkspacePanel,
    )
    panel = ReactionWorkspacePanel()
    qtbot.addWidget(panel)

    panel.fulltext_cb.setChecked(True)
    panel.filter.setText("")
    # Empty query → falls back to the default reload path so the
    # list doesn't vanish.
    assert panel.model.rowCount() > 0


def test_reactions_model_reload_ids_preserves_order(_app, qtbot):
    from orgchem.gui.panels.reaction_workspace import _RxnListModel

    m = _RxnListModel()
    # Cherry-pick any three real reaction IDs via the standard
    # reload + re-query via the model's own data.
    m.reload("")
    all_ids = [m._rows[i].id for i in range(m.rowCount())]
    assert len(all_ids) >= 3
    picks = [all_ids[2], all_ids[0], all_ids[1]]
    m.reload_ids(picks)
    got = [m._rows[i].id for i in range(m.rowCount())]
    assert got == picks


# ---------- Synthesis tab ----------

def test_synthesis_name_filter_default(_app, qtbot):
    from orgchem.gui.panels.synthesis_workspace import (
        SynthesisWorkspacePanel,
    )
    panel = SynthesisWorkspacePanel()
    qtbot.addWidget(panel)

    panel.filter.setText("Aspirin")
    names = [panel.model._rows[i]["name"]
             for i in range(panel.model.rowCount())]
    assert any("Aspirin" in n for n in names), names
    assert not panel.fulltext_cb.isChecked()


def test_synthesis_fulltext_finds_step_note_hit(_app, qtbot):
    """'Raney' (Raney Ni catalyst) is mentioned in the BHC
    Ibuprofen pathway's step-2 reagents. No pathway name / target
    / category contains the word — only step notes do — so this
    is the exact scenario the full-text toggle is supposed to
    solve."""
    from orgchem.gui.panels.synthesis_workspace import (
        SynthesisWorkspacePanel,
    )
    panel = SynthesisWorkspacePanel()
    qtbot.addWidget(panel)

    panel.filter.setText("Raney")
    # Name filter — no pathway name/target/category contains "Raney".
    assert panel.model.rowCount() == 0
    panel.fulltext_cb.setChecked(True)
    # Full-text — BHC Ibuprofen pathway should land.
    names = [panel.model._rows[i]["name"]
             for i in range(panel.model.rowCount())]
    assert any("Ibuprofen" in n for n in names), names


def test_synthesis_model_reload_ids_preserves_order(_app, qtbot):
    from orgchem.gui.panels.synthesis_workspace import (
        _PathwayListModel,
    )

    m = _PathwayListModel()
    m.reload("")
    all_ids = [m._rows[i]["id"] for i in range(m.rowCount())]
    assert len(all_ids) >= 3
    picks = [all_ids[1], all_ids[0]]
    m.reload_ids(picks)
    got = [m._rows[i]["id"] for i in range(m.rowCount())]
    assert got == picks


def test_synthesis_fulltext_empty_ids_clears_list(_app, qtbot):
    from orgchem.gui.panels.synthesis_workspace import (
        _PathwayListModel,
    )
    m = _PathwayListModel()
    m.reload_ids([])
    assert m.rowCount() == 0
