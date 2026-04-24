"""Tests for the Phase 11b Ctrl+K command palette (round 54)."""
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


# ---- pure-data entry builders ------------------------------------

def test_build_palette_entries_includes_three_kinds(app):
    from orgchem.gui.dialogs.command_palette import (
        build_palette_entries, KIND_GLOSSARY, KIND_REACTION, KIND_MOLECULE,
    )
    entries = build_palette_entries()
    kinds = {e.kind for e in entries}
    assert KIND_GLOSSARY in kinds
    assert KIND_REACTION in kinds
    assert KIND_MOLECULE in kinds
    assert len(entries) > 100  # plenty of seeded content


# ---- Phase 35d: synonym aliases -----------------------------------

def test_palette_emits_synonym_aliases(app):
    """Phase 35d round 109 — molecule rows with non-empty
    `synonyms_json` should appear in the palette under each
    synonym, each pointing at the same canonical target."""
    from orgchem.gui.dialogs.command_palette import (
        build_palette_entries, KIND_MOLECULE,
    )
    entries = build_palette_entries()
    by_label = {}
    for e in entries:
        if e.kind == KIND_MOLECULE:
            by_label.setdefault(e.label.lower(), []).append(e)

    # Find any canonical row whose DB record has a synonym.  We
    # don't hard-code which — the curated list already includes
    # Acetaminophen / Paracetamol, Retinol / Vitamin A, etc.
    from orgchem.db.session import session_scope
    from orgchem.db.models import Molecule as DBMol
    import json as _json
    hits = 0
    with session_scope() as s:
        rows = s.query(DBMol).filter(
            DBMol.synonyms_json.isnot(None)).all()
        for r in rows:
            syns = _json.loads(r.synonyms_json or "[]") or []
            for syn in syns:
                if not isinstance(syn, str):
                    continue
                matched = by_label.get(syn.lower(), [])
                if any(e.target == r.id for e in matched):
                    hits += 1
                    break
    assert hits >= 1, (
        "Expected ≥1 molecule to be reachable via at least one "
        "synonym in the palette")


def test_palette_filter_registry_ids():
    """CAS numbers / ChEMBL / UNII / InChIKey / pure digits should
    all be rejected from palette synonym output."""
    from orgchem.gui.dialogs.command_palette import (
        _looks_like_registry_id,
    )
    for junk in ("50-78-2", "123456", "CHEMBL112",
                 "UNII-R16CO5Y76E", "DTXSID9020112",
                 "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
                 "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
                 "NSC 27223", "SCHEMBL6484"):
        assert _looks_like_registry_id(junk), junk
    for real in ("Aspirin", "Acetaminophen", "Vitamin A",
                 "N-acetyl-4-aminophenol", "acetylsalicylic acid"):
        assert not _looks_like_registry_id(real), real


# ---- dialog instantiation + filtering ----------------------------

def test_palette_dialog_instantiates(app):
    from orgchem.gui.dialogs.command_palette import CommandPaletteDialog
    dlg = CommandPaletteDialog(app.window)
    assert dlg.list.count() > 0
    assert dlg.filter_edit.text() == ""


def test_palette_filter_narrows_list(app):
    from orgchem.gui.dialogs.command_palette import CommandPaletteDialog
    dlg = CommandPaletteDialog(app.window)
    baseline = dlg.list.count()
    dlg.filter_edit.setText("SN2")
    narrowed = dlg.list.count()
    assert narrowed < baseline
    # Every shown item should match the query.
    for i in range(narrowed):
        it = dlg.list.item(i)
        text = it.text().lower()
        assert "sn2" in text, text


def test_palette_filter_is_case_insensitive(app):
    from orgchem.gui.dialogs.command_palette import CommandPaletteDialog
    dlg = CommandPaletteDialog(app.window)
    dlg.filter_edit.setText("BENZENE")
    upper = dlg.list.count()
    dlg.filter_edit.setText("benzene")
    lower = dlg.list.count()
    assert upper == lower and upper > 0


def test_palette_filter_caps_at_200(app):
    """Empty query yields up to 200 rows — the ceiling keeps the UI
    responsive with ~400 total entries."""
    from orgchem.gui.dialogs.command_palette import CommandPaletteDialog
    dlg = CommandPaletteDialog(app.window)
    assert dlg.list.count() <= 200


# ---- dispatch routing --------------------------------------------

def test_palette_dispatch_glossary_routes_to_glossary_tab(app):
    from orgchem.gui.dialogs.command_palette import (
        PaletteEntry, KIND_GLOSSARY, dispatch_palette_entry,
    )
    win = app.window
    # Start on the Molecule Workspace so we can prove the switch.
    for i in range(win.tabs.count()):
        if win.tabs.tabText(i) == "Molecule Workspace":
            win.tabs.setCurrentIndex(i)
            break
    entry = PaletteEntry(
        kind=KIND_GLOSSARY, label="SN2", target="SN2",
        sublabel="glossary",
    )
    ok = dispatch_palette_entry(entry, win)
    assert ok is True
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Glossary"


def test_palette_dispatch_reaction_switches_to_reactions(app):
    from orgchem.gui.dialogs.command_palette import (
        PaletteEntry, KIND_REACTION, dispatch_palette_entry,
    )
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    win = app.window
    with session_scope() as s:
        rid = s.query(DBRxn.id).first()[0]
    entry = PaletteEntry(
        kind=KIND_REACTION, label="Example", target=int(rid),
        sublabel="reaction",
    )
    ok = dispatch_palette_entry(entry, win)
    assert ok is True
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Reactions"


def test_palette_activate_closes_dialog(app):
    from orgchem.gui.dialogs.command_palette import CommandPaletteDialog
    dlg = CommandPaletteDialog(app.window)
    dlg.filter_edit.setText("SN2")
    assert dlg.list.count() > 0
    dlg._activate(dlg.list.item(0))
    # `accept()` sets the result to Accepted.
    from PySide6.QtWidgets import QDialog
    assert dlg.result() == QDialog.Accepted


# ---- main-window integration --------------------------------------

def test_main_window_open_command_palette(app, monkeypatch):
    """The Ctrl+K action returns an instantiated dialog — and
    monkeypatching `exec` keeps the test non-modal."""
    from orgchem.gui.dialogs.command_palette import CommandPaletteDialog
    monkeypatch.setattr(CommandPaletteDialog, "exec", lambda self: 0)
    dlg = app.window.open_command_palette()
    assert isinstance(dlg, CommandPaletteDialog)
    assert dlg.list.count() > 0


def test_view_menu_has_command_palette_action(app):
    win = app.window
    # Scan the menubar for the entry + its shortcut.
    found = False
    for menu in win.menuBar().findChildren(type(win.menuBar().actions()[0].menu())):
        for act in menu.actions():
            if act.text() and "Command palette" in act.text():
                assert act.shortcut().toString() == "Ctrl+K"
                found = True
                break
        if found:
            break
    assert found, "Command palette action missing from View menu"
