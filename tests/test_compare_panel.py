"""Tests for the Compare tab bug fixes (drag-drop MIME type + name lookup)."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("PySide6")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- Name-lookup fallback ------------------------------------------------

def test_compare_slot_accepts_molecule_name(app):
    """Typing 'Caffeine' in a slot should resolve it via the DB, not
    throw 'could not parse SMILES'."""
    slot = app.window.compare.slots[0]
    slot.smiles.setText("Caffeine")
    slot._on_load()
    # After a successful load, the title should include the molecule name.
    assert "Caffeine" in slot.title.text(), (
        f"expected title to mention Caffeine, got: {slot.title.text()!r}"
    )


def test_compare_slot_still_accepts_raw_smiles(app):
    slot = app.window.compare.slots[1]
    slot.smiles.setText("CCO")
    slot._on_load()
    # Either the canonical name or the SMILES is fine; just not an error.
    title = slot.title.text()
    assert "error" not in title.lower(), title


def test_compare_slot_substring_match(app):
    """If the exact-name lookup fails, fall back to a substring search."""
    slot = app.window.compare.slots[2]
    slot.smiles.setText("tryptoph")   # lowercase, substring of L-Tryptophan
    slot._on_load()
    assert "Tryptophan" in slot.title.text()


# ---- Drag-and-drop MIME shape -------------------------------------------

def test_browser_provides_drag_mime_data(app):
    """Dragging a row from the molecule browser emits our custom MIME type."""
    from orgchem.gui.panels.molecule_browser import _MIME_MOLECULE_ID
    model = app.window.browser.model
    # Pick the first row (model was already populated on startup).
    from PySide6.QtCore import QModelIndex
    idx = model.index(0, 0, QModelIndex())
    assert idx.isValid()
    md = model.mimeData([idx])
    assert md.hasFormat(_MIME_MOLECULE_ID)
    payload = bytes(md.data(_MIME_MOLECULE_ID)).decode()
    assert payload.isdigit(), f"mime payload not a row id: {payload!r}"
    # MIME type matches the Compare panel's constant.
    from orgchem.gui.panels.compare_panel import _MIME_MOLECULE_ID as other
    assert _MIME_MOLECULE_ID == other


def test_compare_slot_accepts_drops(app):
    """Slots must have acceptDrops set, otherwise Qt never calls dropEvent."""
    for slot in app.window.compare.slots:
        assert slot.acceptDrops(), f"slot {slot.index} isn't a drop target"
