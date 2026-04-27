"""Phase PH-1.0 (round 214) — Biochem bridge panel.

Read-only view of ``biochem.core.enzymes`` filtered to drug-
targetable enzymes (those with non-empty ``drug_targets``).
Demonstrates Pharm-Studio reading another sibling's data
directly via Python import — no copy, no fork.

The *Open in Biochem Studio* button hands off to the Biochem
main window for full editing.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

# Direct import — sibling data sharing.
from biochem.core.enzymes import (
    Enzyme, get_enzyme, list_enzymes,
)

log = logging.getLogger(__name__)


class BiochemBridgePanel(QWidget):
    """Bridge view onto biochem.core.enzymes (drug-targetable)."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._populate()
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)

        outer.addWidget(QLabel(
            "<b>Drug-targetable enzymes (read-only bridge to "
            "Biochem Studio).</b>  These enzymes are seeded in "
            "<code>biochem.core.enzymes</code>; Pharm Studio "
            "filters to those with at least one drug target."
        ))

        bar = QHBoxLayout()
        self.open_biochem_btn = QPushButton(
            "Open in Biochem Studio…")
        self.open_biochem_btn.setToolTip(
            "Hand off to the Biochem Studio main window for "
            "full enzyme exploration.")
        self.open_biochem_btn.clicked.connect(
            self._on_open_in_biochem)
        bar.addWidget(self.open_biochem_btn)
        bar.addStretch(1)
        outer.addLayout(bar)

        split = QSplitter(Qt.Horizontal)
        outer.addWidget(split, stretch=1)

        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(
            self._on_select)
        split.addWidget(self.list_widget)

        self.detail = QTextBrowser()
        split.addWidget(self.detail)
        split.setStretchFactor(0, 1)
        split.setStretchFactor(1, 2)

    def _populate(self) -> None:
        self.list_widget.clear()
        for e in list_enzymes():
            if not e.drug_targets:
                continue  # not drug-targetable
            li = QListWidgetItem(
                f"[{e.ec_number}] {e.name}")
            li.setData(Qt.UserRole, e.id)
            li.setToolTip(e.mechanism_class)
            self.list_widget.addItem(li)

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        eid = current.data(Qt.UserRole)
        e = get_enzyme(eid)
        if e is None:
            return
        self.detail.setHtml(self._render(e))

    def _render(self, e: Enzyme) -> str:
        drug_rows = "".join(
            f"<tr><td>{drug}</td><td>{tgt}</td></tr>"
            for drug, tgt in e.drug_targets)
        diseases = ", ".join(e.disease_associations) \
            or "<i>None.</i>"
        return (
            f"<h2>{e.name}</h2>"
            f"<p><b>EC:</b> {e.ec_number} &middot; "
            f"<b>Mechanism:</b> {e.mechanism_class}</p>"
            f"<h4>Drug targets</h4>"
            f"<table border='1' cellpadding='4' cellspacing='0'>"
            f"<tr><th>Drug</th><th>Target</th></tr>"
            f"{drug_rows}</table>"
            f"<h4>Disease associations</h4><p>{diseases}</p>"
            f"<p style='color:#888'><i>Source: "
            f"<code>biochem.core.enzymes</code> "
            f"(Phase BC-1.0).</i></p>"
        )

    def _on_open_in_biochem(self) -> None:
        """Hand off to Biochem Studio main window."""
        try:
            from orgchem.agent import controller
            from biochem.gui.windows.biochem_main_window import (
                BiochemMainWindow,
            )
            main_win = controller.main_window()
            if main_win is None:
                return
            biochem_win = getattr(
                main_win, "_biochem_window", None)
            if biochem_win is None:
                biochem_win = BiochemMainWindow(parent=main_win)
                main_win._biochem_window = biochem_win
            biochem_win.show()
            biochem_win.raise_()
            biochem_win.activateWindow()
            current = self.list_widget.currentItem()
            if current is not None:
                eid = current.data(Qt.UserRole)
                biochem_win.switch_to("Enzymes")
                biochem_win.enzymes.select_enzyme(eid)
        except Exception:  # noqa: BLE001
            log.exception(
                "Failed to open Biochem Studio from pharm "
                "bridge panel.")

    def select_enzyme(self, enzyme_id: str) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == enzyme_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
