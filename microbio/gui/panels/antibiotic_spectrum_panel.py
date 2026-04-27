"""Phase MB-1.0 (round 215) — Antibiotic-spectrum bridge panel.

Read-only view of ``pharm.core.drug_classes`` filtered to the
six antimicrobial classes (β-lactams, macrolides,
fluoroquinolones, aminoglycosides, HIV PIs, NRTIs).  Demonstrates
Microbio Studio reading another sibling's data directly via
Python import — no copy, no fork.

The *Open in Pharmacology Studio* button hands off to the Pharm
main window pre-selected to the chosen drug class for the full
mechanism / contraindication / monitoring view.
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
from pharm.core.drug_classes import (
    DrugClass, get_drug_class, list_drug_classes,
)

log = logging.getLogger(__name__)

# Antimicrobial drug classes from the PH-1.0 catalogue.  Kept
# here (not in pharm) because the *categorisation as
# antimicrobial* is a microbio-driven view of pharm's data.
_ANTIMICROBIAL_CLASS_IDS = (
    "beta-lactams",
    "macrolides",
    "fluoroquinolones",
    "aminoglycosides",
    "hiv-pis",
    "nrtis",
)


class AntibioticSpectrumPanel(QWidget):
    """Bridge view onto pharm.core.drug_classes (antimicrobials)."""

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
            "<b>Antimicrobial drug classes (read-only bridge to "
            "Pharmacology Studio).</b>  These six classes from "
            "<code>pharm.core.drug_classes</code> are filtered "
            "here as the antimicrobial subset.  Use the "
            "Microbes tab to see which classes hit which "
            "organism (via <code>cross_reference_pharm_drug_"
            "class_ids</code>)."
        ))

        bar = QHBoxLayout()
        self.open_pharm_btn = QPushButton(
            "Open in Pharmacology Studio…")
        self.open_pharm_btn.setToolTip(
            "Hand off to the Pharm Studio main window for the "
            "full mechanism / contraindication view.")
        self.open_pharm_btn.clicked.connect(
            self._on_open_in_pharm)
        bar.addWidget(self.open_pharm_btn)
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
        keep = set(_ANTIMICROBIAL_CLASS_IDS)
        for d in list_drug_classes():
            if d.id not in keep:
                continue
            li = QListWidgetItem(d.name)
            li.setData(Qt.UserRole, d.id)
            li.setToolTip(d.molecular_target)
            self.list_widget.addItem(li)

    def _on_select(
        self,
        current: Optional[QListWidgetItem],
        _previous: Optional[QListWidgetItem] = None,
    ) -> None:
        if current is None:
            return
        cid = current.data(Qt.UserRole)
        d = get_drug_class(cid)
        if d is None:
            return
        self.detail.setHtml(self._render(d))

    def _render(self, d: DrugClass) -> str:
        agents = ", ".join(d.typical_agents)
        clin = "<ul>" + "".join(f"<li>{x}</li>"
                                for x in d.clinical_use) + "</ul>"
        side = "<ul>" + "".join(f"<li>{x}</li>"
                                for x in d.side_effects) + "</ul>"
        return (
            f"<h2>{d.name}</h2>"
            f"<p><b>Mechanism:</b> {d.mechanism}</p>"
            f"<p><b>Molecular target:</b> {d.molecular_target}</p>"
            f"<h4>Typical agents</h4><p>{agents}</p>"
            f"<h4>Clinical use</h4>{clin}"
            f"<h4>Side effects</h4>{side}"
            f"<p style='color:#888'><i>Source: "
            f"<code>pharm.core.drug_classes</code> "
            f"(Phase PH-1.0).</i></p>"
        )

    def _on_open_in_pharm(self) -> None:
        """Hand off to Pharm Studio main window."""
        try:
            from orgchem.agent import controller
            from pharm.gui.windows.pharm_main_window import (
                PharmMainWindow,
            )
            main_win = controller.main_window()
            if main_win is None:
                return
            pharm_win = getattr(
                main_win, "_pharm_window", None)
            if pharm_win is None:
                pharm_win = PharmMainWindow(parent=main_win)
                main_win._pharm_window = pharm_win
            pharm_win.show()
            pharm_win.raise_()
            pharm_win.activateWindow()
            current = self.list_widget.currentItem()
            if current is not None:
                cid = current.data(Qt.UserRole)
                pharm_win.switch_to("Drug classes")
                pharm_win.drug_classes.select_drug_class(cid)
        except Exception:  # noqa: BLE001
            log.exception(
                "Failed to open Pharm Studio from microbio "
                "antibiotic-spectrum panel.")

    def select_drug_class(self, class_id: str) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == class_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
