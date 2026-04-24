"""Command palette — Phase 11b follow-up.

A VS-Code-style "type anywhere → jump anywhere" dialog. Bound to
``Ctrl+K`` from the main window. The initial implementation focuses
on the glossary (since that's the Phase 11b roadmap item) but also
surfaces reactions and molecules from the seeded DB — one dialog,
one keystroke, three kinds of target.

Each result row is tagged with its *kind* so the dispatch logic
knows where to route the user: Glossary tab for terms, Reactions
tab for reactions, Molecule Workspace for molecules. The dialog
calls back into the main window's existing panel API (no new
plumbing).

Usage in tests::

    dlg = CommandPaletteDialog(app.window)
    dlg.filter_edit.setText("SN2")
    assert dlg.list.count() > 0
    dlg._activate(dlg.list.item(0))
"""
from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Any, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QLabel, QWidget,
)

log = logging.getLogger(__name__)


# Kinds the palette knows how to dispatch.
KIND_GLOSSARY = "glossary"
KIND_REACTION = "reaction"
KIND_MOLECULE = "molecule"


@dataclass
class PaletteEntry:
    """One row in the command palette."""
    kind: str
    label: str            # Shown in the list
    target: Any           # Identifier passed to the dispatcher
    sublabel: str = ""    # Secondary descriptor (category / SMILES)


def _glossary_entries() -> List[PaletteEntry]:
    try:
        from orgchem.db.seed_glossary import _GLOSSARY
    except Exception:  # noqa: BLE001
        return []
    out: List[PaletteEntry] = []
    for e in _GLOSSARY:
        out.append(PaletteEntry(
            kind=KIND_GLOSSARY,
            label=e["term"],
            target=e["term"],
            sublabel=f"glossary · {e.get('category', '')}".strip(" ·"),
        ))
    return out


def _reaction_entries() -> List[PaletteEntry]:
    try:
        from orgchem.db.session import session_scope
        from orgchem.db.models import Reaction as DBRxn
        with session_scope() as s:
            rows = s.query(DBRxn).all()
            out = [
                PaletteEntry(
                    kind=KIND_REACTION,
                    label=r.name,
                    target=r.id,
                    sublabel=f"reaction · {r.category or ''}".strip(" ·"),
                )
                for r in rows
            ]
        return out
    except Exception:  # noqa: BLE001
        return []


def _molecule_entries() -> List[PaletteEntry]:
    """Phase 35d — one entry per (canonical name, synonym) so a user
    typing *'Vitamin A'* reaches the Retinol row via the palette
    even though the canonical label is 'Retinol'."""
    try:
        import json
        from orgchem.db.session import session_scope
        from orgchem.db.models import Molecule as DBMol
        with session_scope() as s:
            rows = s.query(DBMol.id, DBMol.name, DBMol.smiles,
                           DBMol.synonyms_json).all()
            out: List[PaletteEntry] = []
            for mid, name, smiles, syn_json in rows:
                if not name:
                    continue
                out.append(PaletteEntry(
                    kind=KIND_MOLECULE,
                    label=name,
                    target=mid,
                    sublabel=f"molecule · {smiles or ''}"[:80],
                ))
                # Synonym aliases — same target id, distinct label so
                # the substring match can find either name.
                if not syn_json:
                    continue
                try:
                    syns = json.loads(syn_json) or []
                except Exception:  # noqa: BLE001
                    continue
                seen_lower = {name.lower()}
                for syn in syns:
                    if not syn or not isinstance(syn, str):
                        continue
                    key = syn.strip()
                    if not key or key.lower() in seen_lower:
                        continue
                    # Drop registry-ID synonyms (CAS / ChEMBL /
                    # UNII / DTXSID etc) — they're noise in a
                    # name-first palette.
                    if _looks_like_registry_id(key):
                        continue
                    seen_lower.add(key.lower())
                    out.append(PaletteEntry(
                        kind=KIND_MOLECULE,
                        label=key,
                        target=mid,
                        sublabel=f"alias of {name}",
                    ))
        return out
    except Exception:  # noqa: BLE001
        return []


def _looks_like_registry_id(s: str) -> bool:
    """Return True if *s* looks like a registry identifier (CAS, UNII,
    ChEMBL, DTXSID, EC-number, …) rather than a natural-language name.
    Phase 35d — used to filter palette-synonym noise."""
    import re
    s = s.strip()
    if not s:
        return True
    # Pure-digit CID / ChEMBL / NSC / EC fragments.
    if re.fullmatch(r"\d+(-\d+)*", s):
        return True
    # CAS numbers: xxxxxxx-xx-x.
    if re.fullmatch(r"\d{1,7}-\d{2}-\d", s):
        return True
    # Registry prefixes.
    for prefix in ("CHEMBL", "UNII", "DTXSID", "DTXCID", "NSC",
                   "BRN", "FDA", "MFCD", "CCDS", "SCHEMBL",
                   "EINECS", "RTECS"):
        if s.upper().startswith(prefix):
            return True
    # InChI / InChIKey string.
    if s.startswith("InChI=") or re.fullmatch(r"[A-Z]{14}-[A-Z]{10}-[A-Z]",
                                              s):
        return True
    return False


def build_palette_entries() -> List[PaletteEntry]:
    """Return every entry the palette can dispatch, in a sensible
    order (glossary first because the keystroke was scoped to that
    in the Phase 11b roadmap item)."""
    return _glossary_entries() + _reaction_entries() + _molecule_entries()


class CommandPaletteDialog(QDialog):
    """Small modeless-feeling dialog that overlays the main window.

    Opens via ``Ctrl+K``. Typing filters the list (case-insensitive
    substring match across label + sublabel). Enter or double-click
    dispatches to the matching tab.
    """

    def __init__(self, parent: Optional[QWidget] = None,
                 entries: Optional[List[PaletteEntry]] = None):
        super().__init__(parent)
        self.setWindowTitle("Command palette")
        # Narrow + tall — VS-Code-like.
        self.resize(580, 440)
        self.setWindowFlag(Qt.Dialog, True)
        self._all_entries: List[PaletteEntry] = (
            list(entries) if entries is not None
            else build_palette_entries()
        )

        root = QVBoxLayout(self)
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(
            "Type a term, reaction, or molecule name…")
        self.filter_edit.textChanged.connect(self._refresh)
        self.filter_edit.returnPressed.connect(self._on_enter)
        root.addWidget(self.filter_edit)

        self.hint = QLabel(
            f"<span style='color:#777'>{len(self._all_entries)} "
            f"entries · ↑↓ to move, Enter to jump, Esc to close</span>"
        )
        root.addWidget(self.hint)

        self.list = QListWidget()
        self.list.itemActivated.connect(self._activate)
        self.list.itemDoubleClicked.connect(self._activate)
        root.addWidget(self.list, 1)

        self._refresh()

    # ------------------------------------------------------------------

    def _refresh(self) -> None:
        query = self.filter_edit.text().strip().lower()
        self.list.clear()
        shown = 0
        for e in self._all_entries:
            hay = (e.label + " " + e.sublabel).lower()
            if query and query not in hay:
                continue
            item = QListWidgetItem(f"{e.label}\n    {e.sublabel}")
            item.setData(Qt.UserRole, e)
            self.list.addItem(item)
            shown += 1
            # Don't flood the list for an empty query — top 200 is
            # more than any human scrolls through.
            if shown >= 200:
                break
        if self.list.count() > 0:
            self.list.setCurrentRow(0)
        self.hint.setText(
            f"<span style='color:#777'>{self.list.count()} of "
            f"{len(self._all_entries)} entries · "
            f"↑↓ to move, Enter to jump, Esc to close</span>"
        )

    def _on_enter(self) -> None:
        item = self.list.currentItem()
        if item is not None:
            self._activate(item)

    def _activate(self, item: QListWidgetItem) -> None:
        entry: PaletteEntry = item.data(Qt.UserRole)
        if entry is None:
            return
        try:
            dispatch_palette_entry(entry, self.parent())
        finally:
            self.accept()


def dispatch_palette_entry(entry: PaletteEntry,
                           main_win: Optional[QWidget]) -> bool:
    """Route a palette entry into the matching tab / panel. Returns
    True if the dispatch succeeded. Kept as a module-level function
    so tests can exercise routing without instantiating the dialog."""
    if main_win is None:
        return False
    tabs = getattr(main_win, "tabs", None)
    if entry.kind == KIND_GLOSSARY and hasattr(main_win, "glossary"):
        if tabs is not None:
            _switch_tab(tabs, "Glossary")
        return main_win.glossary.focus_term(entry.target)
    if entry.kind == KIND_REACTION and hasattr(main_win, "reactions"):
        if tabs is not None:
            _switch_tab(tabs, "Reactions")
        try:
            main_win.reactions._display(int(entry.target))
        except Exception:  # noqa: BLE001
            return False
        return True
    if entry.kind == KIND_MOLECULE:
        if tabs is not None:
            _switch_tab(tabs, "Molecule Workspace")
        from orgchem.messaging.bus import bus
        try:
            bus().molecule_selected.emit(int(entry.target))
        except Exception:  # noqa: BLE001
            return False
        return True
    return False


def _switch_tab(tabs, label: str) -> bool:
    for i in range(tabs.count()):
        if tabs.tabText(i) == label:
            tabs.setCurrentIndex(i)
            return True
    return False
