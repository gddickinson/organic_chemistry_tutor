"""Phase GM-1.0 (round 230) — Cross-references / molecular-
biology bridge panel.

Read-only bridge into ``biochem.core.enzymes`` filtered to
nucleic-acid-acting enzymes (DNA polymerases, RNA polymerases,
ligases, restriction enzymes, reverse transcriptases,
exonucleases, helicases, nucleases) — the molecular workhorses
underlying every technique in the GM-1.0 catalogue.

The *Open in Biochem Studio…* button hands off to the Biochem
main window pre-selected to the chosen enzyme.

GM-1.0 is the seventh sibling whose bridge reads from
``biochem.core.enzymes`` (the BC-1.0 catalogue is sparse on
nucleic-acid enzymes — only `dna-ligase-i` currently — but
the bridge panel is forward-compatible as future BC catalogue
expansions add DNA / RNA polymerases + restriction enzymes +
reverse transcriptases).
"""
from __future__ import annotations
import logging
from typing import List, Optional

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


# Keywords identifying nucleic-acid-acting enzymes.  Matches
# against id + name + ec_class + reaction text fields.
_NUCLEIC_ACID_KEYWORDS = (
    "dna polymerase", "rna polymerase", "polymerase",
    "ligase", "restriction", "endonuclease",
    "exonuclease", "nuclease", "topoisomerase",
    "helicase", "reverse transcriptase",
    "transcriptase", "primase", "telomerase",
    "integrase", "recombinase",
)


def _is_nucleic_acid_enzyme(e: Enzyme) -> bool:
    """Filter for enzymes that act on nucleic acids."""
    parts = [e.id, e.name, e.ec_number, str(e.ec_class),
             e.mechanism_class, e.notes]
    parts.extend(e.substrates)
    parts.extend(e.products)
    haystack = " ".join(parts).lower()
    return any(k in haystack for k in _NUCLEIC_ACID_KEYWORDS)


def filtered_nucleic_acid_enzymes() -> List[Enzyme]:
    """Public helper used by tests."""
    return [e for e in list_enzymes()
            if _is_nucleic_acid_enzyme(e)]


class MolecularBiologyBridgePanel(QWidget):
    """Bridge view onto biochem.core.enzymes filtered to
    nucleic-acid enzymes."""

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
            "<b>Nucleic-acid-acting enzymes "
            "(read-only bridge into Biochem Studio).</b>  "
            "Subset of <code>biochem.core.enzymes</code> "
            "covering the DNA polymerases / ligases / "
            "restriction enzymes / reverse transcriptases "
            "/ nucleases that underlie every technique in "
            "the Techniques tab.  The BC-1.0 catalogue is "
            "currently sparse on nucleic-acid enzymes — "
            "this bridge will populate as future BC "
            "catalogue expansions ship."
        ))

        bar = QHBoxLayout()
        self.open_biochem_btn = QPushButton(
            "Open in Biochem Studio…")
        self.open_biochem_btn.setToolTip(
            "Hand off to the Biochem Studio main window "
            "for the full enzyme detail view.")
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
        for e in filtered_nucleic_acid_enzymes():
            li = QListWidgetItem(e.name)
            li.setData(Qt.UserRole, e.id)
            li.setToolTip(e.ec_number)
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
        substrates = ", ".join(e.substrates) \
            or "<i>None.</i>"
        products = ", ".join(e.products) or "<i>None.</i>"
        return (
            f"<h2>{e.name}</h2>"
            f"<p><b>EC number:</b> {e.ec_number} &middot; "
            f"<b>Class:</b> {e.ec_class}</p>"
            f"<h4>Mechanism class</h4>"
            f"<p>{e.mechanism_class}</p>"
            f"<h4>Substrates</h4><p>{substrates}</p>"
            f"<h4>Products</h4><p>{products}</p>"
            f"<h4>Notes</h4><p>{e.notes}</p>"
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
                biochem_win = BiochemMainWindow(
                    parent=main_win)
                main_win._biochem_window = biochem_win
            biochem_win.show()
            biochem_win.raise_()
            biochem_win.activateWindow()
            current = self.list_widget.currentItem()
            if current is not None:
                eid = current.data(Qt.UserRole)
                biochem_win.switch_to("Enzymes")
                enzymes = getattr(
                    biochem_win, "enzymes", None)
                if enzymes is not None and hasattr(
                        enzymes, "select_enzyme"):
                    enzymes.select_enzyme(eid)
        except Exception:  # noqa: BLE001
            log.exception(
                "Failed to open Biochem Studio from "
                "genetics bridge panel.")

    def select_enzyme(self, enzyme_id: str) -> bool:
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item is not None \
                    and item.data(Qt.UserRole) == enzyme_id:
                self.list_widget.setCurrentRow(i)
                return True
        return False
