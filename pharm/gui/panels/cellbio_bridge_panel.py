"""Phase PH-1.0 (round 214) — Cell Bio bridge panel.

Read-only view of ``cellbio.core.cell_signaling`` filtered to
pathways with non-empty drug-targets.  Demonstrates Pharm
reading a SECOND sibling's data — multi-hop cross-studio data
sharing.
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
from cellbio.core.cell_signaling import (
    SignalingPathway, get_pathway, list_pathways,
)

log = logging.getLogger(__name__)


class CellBioBridgePanel(QWidget):
    """Bridge view onto cellbio.core.cell_signaling
    (drug-targeted pathways)."""

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
            "<b>Drug-targeted signalling pathways (read-only "
            "bridge to Cell Bio Studio).</b>  These pathways "
            "are seeded in <code>cellbio.core.cell_signaling</code>; "
            "Pharm Studio filters to those with at least one "
            "catalogued drug target."
        ))

        bar = QHBoxLayout()
        self.open_cellbio_btn = QPushButton(
            "Open in Cell Biology Studio…")
        self.open_cellbio_btn.setToolTip(
            "Hand off to the Cell Bio Studio main window for "
            "full pathway exploration.")
        self.open_cellbio_btn.clicked.connect(
            self._on_open_in_cellbio)
        bar.addWidget(self.open_cellbio_btn)
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
            if not p.drug_targets:
                continue  # not drug-targeted
            li = QListWidgetItem(p.name)
            li.setData(Qt.UserRole, p.id)
            li.setToolTip(p.canonical_function)
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

    def _render(self, p: SignalingPathway) -> str:
        drug_rows = "".join(
            f"<tr><td>{drug}</td><td>{tgt}</td></tr>"
            for drug, tgt in p.drug_targets)
        diseases = ", ".join(p.disease_associations) \
            or "<i>None.</i>"
        components = ", ".join(p.key_components)
        return (
            f"<h2>{p.name}</h2>"
            f"<p><b>Receptor class:</b> {p.receptor_class} "
            f"&middot; <b>Category:</b> {p.category}</p>"
            f"<h4>Function</h4><p>{p.canonical_function}</p>"
            f"<h4>Key components</h4><p>{components}</p>"
            f"<h4>Drug targets</h4>"
            f"<table border='1' cellpadding='4' cellspacing='0'>"
            f"<tr><th>Drug</th><th>Target</th></tr>"
            f"{drug_rows}</table>"
            f"<h4>Disease associations</h4><p>{diseases}</p>"
            f"<p style='color:#888'><i>Source: "
            f"<code>cellbio.core.cell_signaling</code> "
            f"(Phase CB-1.0).</i></p>"
        )

    def _on_open_in_cellbio(self) -> None:
        try:
            from orgchem.agent import controller
            from cellbio.gui.windows.cellbio_main_window import (
                CellBioMainWindow,
            )
            main_win = controller.main_window()
            if main_win is None:
                return
            cellbio_win = getattr(
                main_win, "_cellbio_window", None)
            if cellbio_win is None:
                cellbio_win = CellBioMainWindow(parent=main_win)
                main_win._cellbio_window = cellbio_win
            cellbio_win.show()
            cellbio_win.raise_()
            cellbio_win.activateWindow()
            current = self.list_widget.currentItem()
            if current is not None:
                pid = current.data(Qt.UserRole)
                cellbio_win.switch_to("Signalling")
                cellbio_win.signaling.select_pathway(pid)
        except Exception:  # noqa: BLE001
            log.exception(
                "Failed to open Cell Bio Studio from pharm "
                "bridge panel.")

    def select_pathway(self, pathway_id: str) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == pathway_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
