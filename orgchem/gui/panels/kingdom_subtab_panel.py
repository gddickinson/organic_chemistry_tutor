"""Phase 47b (round 167) — per-kingdom 3-sub-tab widget.

Reusable widget for the Biochemistry-by-Kingdom window.  One
instance per kingdom (eukarya / bacteria / archaea / viruses);
each instance hosts an inner `QTabWidget` with three sub-tabs
(structure / physiology / genetics).  Each sub-tab has the
canonical 'filterable list on the left + HTML detail card on
the right' layout that ships across the rest of the app.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSplitter, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget,
)

from orgchem.core.biochemistry_by_kingdom import (
    KingdomTopic, get_topic, list_topics,
    sub_domains_for_kingdom, subtabs,
)


_ALL_SUBDOMAINS_LABEL = "(all)"

log = logging.getLogger(__name__)


_SUBTAB_LABELS = {
    "structure": "Structure",
    "physiology": "Physiology + Development",
    "genetics": "Genetics + Evolution",
}


class _SubtabPane(QWidget):
    """One sub-tab pane — filterable list + HTML detail card."""

    def __init__(
        self,
        kingdom: str,
        subtab: str,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._kingdom = kingdom
        self._subtab = subtab
        self._sub_domain: str = ""   # round 169 — Phase 47d
        self._build_ui()
        self._reload_list()

    def set_sub_domain(self, sub_domain: str) -> None:
        """Round 169 — Phase 47d.  Set the sub-domain filter
        applied to this pane.  Empty string means 'show all'."""
        if sub_domain != self._sub_domain:
            self._sub_domain = sub_domain
            self._reload_list()

    def _build_ui(self) -> None:
        outer = QHBoxLayout(self)
        outer.setContentsMargins(4, 4, 4, 4)
        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText(
            f"Filter {self._kingdom} {self._subtab} topics…")
        self._filter_edit.textChanged.connect(self._reload_list)
        left_lay.addWidget(self._filter_edit)
        self._list = QListWidget()
        self._list.currentItemChanged.connect(self._on_selection)
        self._list.setMinimumWidth(280)
        left_lay.addWidget(self._list, 1)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Select a topic on the left.")
        f = self._title.font()
        f.setBold(True)
        f.setPointSizeF(f.pointSizeF() + 2)
        self._title.setFont(f)
        self._title.setWordWrap(True)
        right_lay.addWidget(self._title)
        self._detail = QTextBrowser()
        self._detail.setOpenExternalLinks(False)
        right_lay.addWidget(self._detail, 1)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        outer.addWidget(splitter)

    def _reload_list(self) -> None:
        topics = list_topics(kingdom=self._kingdom,
                             subtab=self._subtab,
                             sub_domain=self._sub_domain or None)
        needle = self._filter_edit.text().strip().lower()
        if needle:
            topics = [
                t for t in topics
                if needle in t.id.lower()
                or needle in t.title.lower()
                or needle in t.body.lower()
            ]
        self._list.clear()
        for t in topics:
            it = QListWidgetItem(t.title)
            it.setData(Qt.UserRole, t.id)
            self._list.addItem(it)
        if self._list.count():
            self._list.setCurrentRow(0)
        else:
            self._show_blank("No topics match the current filter.")

    def _on_selection(self, current, _previous) -> None:
        if current is None:
            self._show_blank("Select a topic on the left.")
            return
        tid = current.data(Qt.UserRole)
        t = get_topic(tid)
        if t is None:
            self._show_blank(f"Unknown topic id: {tid}")
            return
        self._show_topic(t)

    def _show_topic(self, t: KingdomTopic) -> None:
        self._title.setText(t.title)
        body_html = (
            f"<p>{_esc(t.body)}</p>"
        )
        if t.cross_reference_cell_component_ids:
            body_html += (
                f"<h4>Cross-reference (Phase 43 cell "
                f"components)</h4>"
                f"<p>{_esc(', '.join(t.cross_reference_cell_component_ids))}</p>"
            )
        if t.cross_reference_pathway_ids:
            body_html += (
                f"<h4>Cross-reference (Phase 42 metabolic "
                f"pathways)</h4>"
                f"<p>{_esc(', '.join(t.cross_reference_pathway_ids))}</p>"
            )
        if t.cross_reference_molecule_names:
            body_html += (
                f"<h4>Cross-reference (Molecule database)</h4>"
                f"<p>{_esc(', '.join(t.cross_reference_molecule_names))}</p>"
            )
        if t.notes:
            body_html += f"<h4>Notes</h4><p>{_esc(t.notes)}</p>"
        self._detail.setHtml(body_html)

    def _show_blank(self, message: str) -> None:
        self._title.setText(message)
        self._detail.setHtml("")

    def select_topic(self, topic_id: str) -> bool:
        for i in range(self._list.count()):
            it = self._list.item(i)
            if it.data(Qt.UserRole) == topic_id:
                self._list.setCurrentRow(i)
                return True
        return False


class KingdomSubtabPanel(QWidget):
    """Per-kingdom widget hosting the 3 sub-tabs."""

    def __init__(
        self,
        kingdom: str,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._kingdom = kingdom
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Round 169 — Phase 47d.  Sub-domain combo above the
        # inner tabs.  Only shown when the kingdom HAS
        # meaningful sub-domains (all 4 do, but the helper is
        # the source of truth so future kingdoms can opt out).
        sub_doms = sub_domains_for_kingdom(kingdom)
        self._sub_combo: Optional[QComboBox] = None
        if sub_doms:
            row = QHBoxLayout()
            row.setContentsMargins(4, 4, 4, 0)
            label_text = {
                "eukarya": "Kingdom (within Eukarya):",
                "bacteria": "Gram-stain class:",
                "archaea": "Phylum:",
                "viruses": "Genome class:",
            }.get(kingdom, "Sub-domain:")
            row.addWidget(QLabel(label_text))
            self._sub_combo = QComboBox()
            self._sub_combo.addItem(_ALL_SUBDOMAINS_LABEL)
            for s in sub_doms:
                self._sub_combo.addItem(s)
            self._sub_combo.currentTextChanged.connect(
                self._on_sub_domain_changed)
            row.addWidget(self._sub_combo, 1)
            outer.addLayout(row)

        self._tabs = QTabWidget()
        self._panes: dict[str, _SubtabPane] = {}
        for sub_id in subtabs():
            pane = _SubtabPane(kingdom, sub_id)
            self._panes[sub_id] = pane
            self._tabs.addTab(pane,
                              _SUBTAB_LABELS.get(sub_id, sub_id))
        outer.addWidget(self._tabs)

    def _on_sub_domain_changed(self, text: str) -> None:
        sub_domain = "" if text == _ALL_SUBDOMAINS_LABEL else text
        for pane in self._panes.values():
            pane.set_sub_domain(sub_domain)

    def set_sub_domain(self, sub_domain: str) -> bool:
        """Programmatic sub-domain selection.  Returns True if
        the value was valid for this kingdom."""
        if self._sub_combo is None:
            return False
        if not sub_domain:
            self._sub_combo.setCurrentText(_ALL_SUBDOMAINS_LABEL)
            return True
        idx = self._sub_combo.findText(sub_domain)
        if idx < 0:
            return False
        self._sub_combo.setCurrentIndex(idx)
        return True

    def current_sub_domain(self) -> str:
        if self._sub_combo is None:
            return ""
        text = self._sub_combo.currentText()
        return "" if text == _ALL_SUBDOMAINS_LABEL else text

    @property
    def kingdom(self) -> str:
        return self._kingdom

    def switch_to_subtab(self, subtab: str) -> bool:
        for i in range(self._tabs.count()):
            if self._tabs.widget(i) is self._panes.get(subtab):
                self._tabs.setCurrentIndex(i)
                return True
        return False

    def select_topic(self, subtab: str, topic_id: str) -> bool:
        pane = self._panes.get(subtab)
        if pane is None:
            return False
        if not self.switch_to_subtab(subtab):
            return False
        return pane.select_topic(topic_id)

    def subtab_labels(self) -> list[str]:
        return [self._tabs.tabText(i)
                for i in range(self._tabs.count())]


def _esc(s: str) -> str:
    return ((s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
