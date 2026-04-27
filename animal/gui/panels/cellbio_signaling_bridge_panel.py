"""Phase AB-1.0 (round 217) — Cell-signalling-bridge panel.

Read-only view of ``cellbio.core.cell_signaling`` filtered to
animal-relevant developmental + apoptosis + immune pathways
(the catalogue subsets most heavily characterised in animal
models).  AB-1.0 is the SECOND sibling whose bridge reads
``cellbio.core.cell_signaling`` directly (the first was Pharm
via `cellbio_bridge_panel.py`), confirming the cellbio API is
stable enough to support multiple consumers.

The *Open in Cell Biology Studio…* button hands off to the
Cell Bio main window pre-selected to the chosen pathway.
"""
from __future__ import annotations
import logging
from typing import Optional, Tuple

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

# Pathways most central to animal biology: developmental
# patterning + apoptosis + immune signalling.  Hand-curated
# from the CB-1.0 catalogue.  Dropping pathways already
# surfaced in the Pharm bridge (it's a different curatorial
# slice — Pharm chose drug-targeted pathways; AB chose
# animal-developmental pathways) is fine — they OVERLAP, by
# design.
_ANIMAL_RELEVANT_PATHWAY_IDS: Tuple[str, ...] = (
    "wnt-beta-catenin",
    "notch",
    "hedgehog",
    "tgf-beta-smad",
    "egfr-ras-raf",
    "mapk-erk",
    "pi3k-akt-mtor",
    "jak-stat",
    "insulin",
    "intrinsic-apoptosis",
    "tnf-extrinsic-apoptosis",
    "necroptosis",
    "pyroptosis",
    "tlr",
    "tcr",
    "nf-kb",
    "cgas-sting",
    "p53",
    "hippo-yap",
    "ampk",
    "mtorc1-aa-sensing",
)


class CellBioSignalingBridgePanel(QWidget):
    """Bridge view onto cellbio.core.cell_signaling (animal-
    relevant subset)."""

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
            "<b>Animal-relevant signalling pathways (read-only "
            "bridge to Cell Biology Studio).</b>  Subset of "
            "<code>cellbio.core.cell_signaling</code> covering "
            "the developmental + apoptosis + immune pathways "
            "most heavily characterised in animal models.  "
            "Use the Animal taxa tab to see which animals "
            "anchored which pathway."
        ))

        bar = QHBoxLayout()
        self.open_cellbio_btn = QPushButton(
            "Open in Cell Biology Studio…")
        self.open_cellbio_btn.setToolTip(
            "Hand off to the Cell Bio Studio main window "
            "for the full pathway view.")
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
        keep = set(_ANIMAL_RELEVANT_PATHWAY_IDS)
        # Preserve the curated order so devel pathways come
        # first, then apoptosis, then immune.
        for pid in _ANIMAL_RELEVANT_PATHWAY_IDS:
            p = get_pathway(pid)
            if p is None or p.id not in keep:
                continue
            li = QListWidgetItem(p.name)
            li.setData(Qt.UserRole, p.id)
            li.setToolTip(p.receptor_class)
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
        components = ", ".join(p.key_components) \
            or "<i>None.</i>"
        diseases = ", ".join(p.disease_associations) \
            or "<i>None.</i>"
        drug_rows = ""
        if p.drug_targets:
            drug_rows = (
                "<table border='1' cellpadding='4' "
                "cellspacing='0'>"
                "<tr><th>Drug</th><th>Target</th></tr>"
                + "".join(
                    f"<tr><td>{drug}</td><td>{tgt}</td></tr>"
                    for drug, tgt in p.drug_targets)
                + "</table>"
            )
        else:
            drug_rows = "<p><i>None catalogued.</i></p>"
        return (
            f"<h2>{p.name}</h2>"
            f"<p><b>Category:</b> {p.category} &middot; "
            f"<b>Receptor class:</b> {p.receptor_class}</p>"
            f"<h4>Key components</h4><p>{components}</p>"
            f"<h4>Canonical function</h4>"
            f"<p>{p.canonical_function}</p>"
            f"<h4>Disease associations</h4><p>{diseases}</p>"
            f"<h4>Drug targets</h4>{drug_rows}"
            f"<p style='color:#888'><i>Source: "
            f"<code>cellbio.core.cell_signaling</code> "
            f"(Phase CB-1.0).</i></p>"
        )

    def _on_open_in_cellbio(self) -> None:
        """Hand off to Cell Biology Studio main window."""
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
                # Some cellbio versions expose .signaling.select_pathway.
                signaling = getattr(
                    cellbio_win, "signaling", None)
                if signaling is not None and hasattr(
                        signaling, "select_pathway"):
                    signaling.select_pathway(pid)
        except Exception:  # noqa: BLE001
            log.exception(
                "Failed to open Cell Bio Studio from animal "
                "signalling-bridge panel.")

    def select_pathway(self, pathway_id: str) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == pathway_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
