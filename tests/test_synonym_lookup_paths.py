"""Phase 35e round 111 regression tests — synonym lookup through
every search surface that uses `find_molecule_by_name`.

Both `show_molecule(name)` (agent action / tutor entry point) and
`compare_panel._resolve_one_text()` (Compare tab input field) hit
the same `find_molecule_by_name` helper which already consults
`synonyms_json` via ILIKE.  This file locks the behaviour end-to-end
so future refactors can't silently regress the user-facing path.
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


# ---- find_molecule_by_name direct ---------------------------------

def test_find_molecule_by_name_resolves_paracetamol_to_acetaminophen(app):
    from orgchem.db.queries import find_molecule_by_name
    row = find_molecule_by_name("Paracetamol")
    assert row is not None
    assert row.name == "Acetaminophen", (
        "Seeded synonym 'Paracetamol' must resolve to the "
        "canonical 'Acetaminophen' row (round-58 curated map)")


def test_find_molecule_by_name_resolves_asa(app):
    from orgchem.db.queries import find_molecule_by_name
    row = find_molecule_by_name("ASA")
    assert row is not None
    assert row.name == "Aspirin"


def test_find_molecule_by_name_is_case_insensitive(app):
    from orgchem.db.queries import find_molecule_by_name
    upper = find_molecule_by_name("PARACETAMOL")
    lower = find_molecule_by_name("paracetamol")
    mixed = find_molecule_by_name("paraCetaMol")
    assert upper is not None and lower is not None and mixed is not None
    assert upper.id == lower.id == mixed.id


def test_find_molecule_by_name_unknown_returns_none(app):
    from orgchem.db.queries import find_molecule_by_name
    assert find_molecule_by_name(
        "definitely-not-a-real-molecule-synonym-xyz") is None


# ---- show_molecule agent action -----------------------------------

def test_show_molecule_action_resolves_synonym(app):
    """The tutor / stdio-bridge entry point for 'show me compound X'
    must reach the canonical row via a synonym."""
    res = app.call("show_molecule", name_or_id="Paracetamol")
    # Agent action schema: returns {id, name, formula, ...} on
    # success; {error: ...} on miss.
    assert "error" not in res, res
    assert res.get("name") == "Acetaminophen"


def test_show_molecule_action_resolves_asa(app):
    res = app.call("show_molecule", name_or_id="Acetylsalicylic acid")
    assert "error" not in res, res
    assert res.get("name") == "Aspirin"


def test_show_molecule_action_unknown_synonym_errors(app):
    res = app.call(
        "show_molecule",
        name_or_id="completely-fabricated-drug-name-1234")
    # Either an explicit {error} or a missing name field; both
    # count as "not resolved".  The current implementation
    # returns {error: "..."} on miss.
    assert "error" in res or res.get("id") is None


# ---- Compare tab resolution --------------------------------------

def test_compare_panel_slot_resolves_synonym_text(app, qtbot):
    """Compare-tab per-slot `_on_load` path.  Typing a synonym
    into the slot's SMILES/name input and clicking load should
    reach the canonical molecule via `find_molecule_by_name`."""
    pytest.importorskip("pytestqt")
    from orgchem.gui.panels.compare_panel import ComparePanel
    panel = ComparePanel()
    qtbot.addWidget(panel)
    assert panel.slots, "ComparePanel should have at least 1 slot"
    slot = panel.slots[0]
    slot.smiles.setText("Paracetamol")
    slot._on_load()
    # After load, the slot's title should include the canonical
    # name "Acetaminophen" (not the typed alias), proving the
    # synonym resolution fired and the display text used the DB
    # canonical name.
    assert "Acetaminophen" in slot.title.text(), slot.title.text()


def test_compare_panel_slot_resolves_asa_synonym(app, qtbot):
    """Secondary pair — ensure round-58 curated synonyms aren't
    specific to a single row."""
    pytest.importorskip("pytestqt")
    from orgchem.gui.panels.compare_panel import ComparePanel
    panel = ComparePanel()
    qtbot.addWidget(panel)
    slot = panel.slots[0]
    slot.smiles.setText("ASA")
    slot._on_load()
    assert "Aspirin" in slot.title.text(), slot.title.text()
