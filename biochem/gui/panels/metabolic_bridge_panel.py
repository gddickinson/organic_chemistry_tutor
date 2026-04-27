"""Phase BC-1.0 (round 213) — Metabolic-pathways bridge panel.

**The architectural validation of the multi-studio platform.**
This Biochem-Studio panel surfaces ``orgchem.core.metabolic_pathways``
(Phase 42, 11 pathways) **read-only** without copying the data
or refactoring orgchem.  Demonstrates that sibling studios can
share data through plain Python imports.

A *Open in OrgChem Tools menu…* button hands off to the existing
OrgChem Phase-42a dialog for users who want full editing.

The pattern generalises: when the future Pharmacology / Microbio /
Botany / Animal-bio studios need to surface OrgChem (or each
other's) data, they can do it the same way — read-only bridge
panel + hand-off button.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSplitter, QTextBrowser, QVBoxLayout, QWidget,
)

# Direct import of orgchem catalogue — no fork, no copy.
from orgchem.core.metabolic_pathways import (
    Pathway, get_pathway, list_pathways, pathway_to_dict,
)

log = logging.getLogger(__name__)


class MetabolicBridgePanel(QWidget):
    """Bridge view onto orgchem.core.metabolic_pathways."""

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
            "<b>Metabolic pathways (read-only bridge to "
            "OrgChem).</b>  These pathways are seeded in "
            "<code>orgchem.core.metabolic_pathways</code> "
            "(Phase 42).  Biochem Studio surfaces them here "
            "without duplicating the data — the cross-studio "
            "data-sharing pattern."
        ))

        bar = QHBoxLayout()
        self.open_orgchem_btn = QPushButton(
            "Open in OrgChem Tools menu…")
        self.open_orgchem_btn.setToolTip(
            "Hand off to the OrgChem Phase-42 metabolic-"
            "pathways dialog for full editing + step-level "
            "exploration.")
        self.open_orgchem_btn.clicked.connect(
            self._on_open_in_orgchem)
        bar.addWidget(self.open_orgchem_btn)
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
        for p in list_pathways():
            li = QListWidgetItem(p.name)
            li.setData(Qt.UserRole, p.id)
            li.setToolTip(p.category)
            self.list_widget.addItem(li)

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        pid = current.data(Qt.UserRole)
        p = get_pathway(pid)
        if p is None:
            return
        self.detail.setHtml(self._render(p))

    def _render(self, p: Pathway) -> str:
        steps_html = ""
        for step in p.steps:
            sub = ", ".join(step.substrates) or "—"
            prod = ", ".join(step.products) or "—"
            arrow = ("⇌" if step.reversibility == "reversible"
                     else "→")
            ec = (f" (EC {step.ec_number})"
                  if step.ec_number else "")
            dG = (f" — ΔG = {step.delta_g_kjmol} kJ/mol"
                  if step.delta_g_kjmol is not None else "")
            steps_html += (
                f"<li><b>Step {step.step_number}:</b> "
                f"{step.enzyme_name}{ec}<br/>"
                f"{sub} {arrow} {prod}{dG}</li>")
        compartment = p.cellular_compartment or "—"
        ref = p.textbook_reference or "—"
        return (
            f"<h2>{p.name}</h2>"
            f"<p><b>Category:</b> {p.category} &middot; "
            f"<b>Compartment:</b> {compartment}</p>"
            f"<p><b>Overall ΔG:</b> "
            f"{p.overall_delta_g_kjmol if p.overall_delta_g_kjmol is not None else '—'} kJ/mol</p>"
            f"<p><b>Textbook ref:</b> {ref}</p>"
            f"<h4>Overview</h4>"
            f"<p>{p.overview}</p>"
            f"<h4>Steps</h4>"
            f"<ol>{steps_html}</ol>"
            f"<p style='color:#888'><i>Source: "
            f"<code>orgchem.core.metabolic_pathways</code> "
            f"(Phase 42a).</i></p>"
        )

    # ---------------- bridge actions ------------------------------

    def _on_open_in_orgchem(self) -> None:
        """Hand off to OrgChem's Phase-42 metabolic-pathways
        dialog.  Surfaces the same data with full step-level
        editing + selection."""
        try:
            from orgchem.agent import controller
            from orgchem.gui.dialogs.metabolic_pathways import (
                MetabolicPathwaysDialog,
            )
            main_win = controller.main_window()
            current = self.list_widget.currentItem()
            pid = current.data(Qt.UserRole) if current else None
            dlg = MetabolicPathwaysDialog.singleton(
                parent=main_win)
            dlg.show()
            dlg.raise_()
            dlg.activateWindow()
            if pid:
                dlg.select_pathway(pid)
        except Exception:  # noqa: BLE001
            log.exception(
                "Failed to open OrgChem metabolic-pathways "
                "dialog from biochem bridge panel.")

    def select_pathway(self, pathway_id: str) -> bool:
        """Programmatic selection."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == pathway_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
