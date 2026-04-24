"""Phase 33b — Ctrl+F full-text search dialog.

GUI front-end for :func:`orgchem.core.fulltext_search.search`.
Live-updating text box, per-kind checkbox filters, ranked
results list with kind badges + snippet preview, and
double-click dispatch to the originating surface.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox, QDialog, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QVBoxLayout, QWidget,
)

from orgchem.core.fulltext_search import (
    SEARCHABLE_KINDS,
    SearchResult,
    search,
)

log = logging.getLogger(__name__)


#: Display labels for each kind (the scoring constant is stable
#: but user-facing strings are prettier).
_KIND_LABELS = {
    "molecule":       "Molecule",
    "reaction":       "Reaction",
    "mechanism-step": "Mechanism step",
    "pathway":        "Pathway",
    "glossary":       "Glossary",
}

#: Background colours for the kind-badge tag in each result row.
_KIND_COLOURS = {
    "molecule":       "#3355cc",
    "reaction":       "#cc8833",
    "mechanism-step": "#cc5533",
    "pathway":        "#339944",
    "glossary":       "#8833aa",
}


class FulltextSearchDialog(QDialog):
    """Ctrl+F Find dialog — routes double-clicks to the originating
    surface via :func:`dispatch_search_result`.

    Singleton per app instance (re-opening pulls up the existing
    dialog with its prior query + filter state so the user can
    keep refining)."""

    _instance: Optional["FulltextSearchDialog"] = None

    #: Debounce window between keystrokes before rerunning the
    #: linear scan.  ~1 k rows × a few μs each means ~5 ms in the
    #: worst case, but user-facing typing feels better with a
    #: 100 ms quiet period to avoid flicker.
    _DEBOUNCE_MS = 100

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None) -> "FulltextSearchDialog":
        if cls._instance is None or not cls._instance.isVisible():
            cls._instance = cls(parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Find — full-text search")
        self.setModal(False)
        self.resize(680, 520)

        self._kind_checks: Dict[str, QCheckBox] = {}
        self._search_timer: Optional[QTimer] = None
        self._results: List[SearchResult] = []

        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)

        self._query = QLineEdit(self)
        self._query.setPlaceholderText(
            "Type to search every molecule / reaction / pathway / "
            "glossary term / mechanism step…")
        self._query.textChanged.connect(self._schedule_search)
        self._query.returnPressed.connect(self._run_now)
        root.addWidget(self._query)

        # Filter row — one checkbox per kind.
        filt = QHBoxLayout()
        filt.addWidget(QLabel("Kinds:"))
        for kind in SEARCHABLE_KINDS:
            cb = QCheckBox(_KIND_LABELS.get(kind, kind), self)
            cb.setChecked(True)
            cb.toggled.connect(lambda _=False: self._schedule_search())
            filt.addWidget(cb)
            self._kind_checks[kind] = cb
        filt.addStretch(1)
        root.addLayout(filt)

        # Results list
        self._list = QListWidget(self)
        self._list.itemDoubleClicked.connect(self._on_item_activated)
        self._list.itemActivated.connect(self._on_item_activated)
        # Row height-friendly font settings handled by the
        # inserted HTML per row; keep the widget defaults.
        root.addWidget(self._list, 1)

        # Status strip
        self._status = QLabel("", self)
        self._status.setStyleSheet("color: #888; padding: 2px 4px;")
        root.addWidget(self._status)

        # Kick an empty-state render.
        self._render([])

    # ---- search loop ---------------------------------------------

    def _schedule_search(self) -> None:
        """Debounced rerun — keystroke bursts coalesce."""
        if self._search_timer is None:
            self._search_timer = QTimer(self)
            self._search_timer.setSingleShot(True)
            self._search_timer.timeout.connect(self._run_now)
        self._search_timer.start(self._DEBOUNCE_MS)

    def _run_now(self) -> None:
        q = self._query.text().strip()
        if not q:
            self._render([])
            self._status.setText("")
            return
        kinds = [k for k, cb in self._kind_checks.items()
                 if cb.isChecked()]
        if not kinds:
            self._render([])
            self._status.setText("Select at least one kind.")
            return
        try:
            self._results = search(q, kinds=kinds, limit=100)
        except Exception as e:   # pragma: no cover - defensive
            log.exception("Full-text search failed")
            self._status.setText(f"Error: {e}")
            self._results = []
        self._render(self._results)
        n = len(self._results)
        self._status.setText(
            f"{n} result{'' if n == 1 else 's'} for {q!r}")

    # ---- rendering ----------------------------------------------

    def _render(self, results: List[SearchResult]) -> None:
        self._list.clear()
        if not results:
            item = QListWidgetItem(
                "Start typing to search seeded content…")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable
                                        & ~Qt.ItemIsEnabled)
            self._list.addItem(item)
            return
        for i, r in enumerate(results):
            item = QListWidgetItem(self._list)
            item.setData(Qt.UserRole, i)
            # Two-line label: kind badge + title, then snippet.
            label = QLabel(self._format_row(r), self._list)
            label.setWordWrap(True)
            label.setContentsMargins(6, 4, 6, 4)
            self._list.setItemWidget(item, label)
            item.setSizeHint(label.sizeHint())

    @staticmethod
    def _format_row(r: SearchResult) -> str:
        colour = _KIND_COLOURS.get(r.kind, "#555")
        kind_label = _KIND_LABELS.get(r.kind, r.kind)
        title = (r.title or "").replace("<", "&lt;").replace(">", "&gt;")
        snippet = (r.snippet or "").replace("<", "&lt;").replace(">", "&gt;")
        return (
            f"<div style='margin: 0;'>"
            f"<span style='background:{colour}; color: white; "
            f"padding: 1px 6px; border-radius: 3px; "
            f"font-size: 10pt;'>{kind_label}</span>"
            f" &nbsp; <b>{title}</b>"
            f"<br><span style='color:#888; font-size: 10pt;'>{snippet}</span>"
            f"</div>"
        )

    # ---- dispatch ------------------------------------------------

    def _on_item_activated(self, item: QListWidgetItem) -> None:
        idx = item.data(Qt.UserRole)
        if not isinstance(idx, int):
            return
        if idx < 0 or idx >= len(self._results):
            return
        ok = dispatch_search_result(self._results[idx],
                                    self.parent())
        if ok:
            self.accept()


def dispatch_search_result(result: SearchResult,
                           main_win: Optional[QWidget]) -> bool:
    """Route a :class:`SearchResult` to the originating surface.

    Returns ``True`` on a successful hop.  Module-level so tests
    can exercise routing without instantiating the dialog.

    Handles every :data:`SEARCHABLE_KINDS` kind:

    * ``molecule`` → Molecule Workspace tab via
      ``bus.molecule_selected``.
    * ``reaction`` / ``mechanism-step`` → Reactions tab
      (mechanism step also fires ``open_mechanism`` to pop the
      player dialog open at step 1).
    * ``pathway`` → Synthesis tab via ``synthesis._display``.
    * ``glossary`` → Glossary tab via ``glossary.focus_term``.
    """
    if main_win is None:
        return False
    tabs = getattr(main_win, "tabs", None)
    kind = result.kind
    key = result.key or {}

    if kind == "glossary" and hasattr(main_win, "glossary"):
        if tabs is not None:
            _switch_tab(tabs, "Glossary")
        term = key.get("term") or result.title
        return bool(main_win.glossary.focus_term(term))

    if kind == "reaction" and hasattr(main_win, "reactions"):
        if tabs is not None:
            _switch_tab(tabs, "Reactions")
        rid = key.get("reaction_id")
        if rid is None:
            return False
        try:
            main_win.reactions._display(int(rid))
        except Exception:
            return False
        return True

    if kind == "mechanism-step" and hasattr(main_win, "reactions"):
        # Switch to Reactions + display the parent reaction;
        # opening the mechanism player is delegated to the
        # agent action so thread-safety + dialog-lifetime stay
        # consistent with the existing player path.
        if tabs is not None:
            _switch_tab(tabs, "Reactions")
        rid = key.get("reaction_id")
        if rid is None:
            return False
        try:
            main_win.reactions._display(int(rid))
            from orgchem.agent.actions import invoke
            invoke("open_mechanism", name_or_id=str(rid))
        except Exception:
            log.exception("mechanism-step dispatch failed")
            return False
        return True

    if kind == "pathway" and hasattr(main_win, "synthesis"):
        if tabs is not None:
            _switch_tab(tabs, "Synthesis")
        pid = key.get("pathway_id")
        if pid is None:
            return False
        try:
            main_win.synthesis._display(int(pid))
        except Exception:
            return False
        return True

    if kind == "molecule":
        if tabs is not None:
            _switch_tab(tabs, "Molecule Workspace")
        mid = key.get("molecule_id")
        if mid is None:
            return False
        from orgchem.messaging.bus import bus
        try:
            bus().molecule_selected.emit(int(mid))
        except Exception:
            return False
        return True

    return False


def _switch_tab(tabs, label: str) -> bool:
    for i in range(tabs.count()):
        if tabs.tabText(i) == label:
            tabs.setCurrentIndex(i)
            return True
    return False
