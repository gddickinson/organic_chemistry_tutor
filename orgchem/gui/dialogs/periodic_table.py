"""Interactive periodic table — Phase 27c (round 36).

Classic 18-column layout: s-block on the left, p-block on the right,
d-block in the middle, and the f-block (lanthanides + actinides)
rendered on separate rows at the bottom with a leader line. Each
cell is a clickable push-button coloured by category; clicking
shows the element's full record in a side-pane.

Reads from the Phase 27a data module — no network, no extra deps.
"""
from __future__ import annotations
import logging
from typing import Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QDialogButtonBox, QScrollArea, QWidget,
    QTextBrowser, QFrame,
)

from orgchem.core.periodic_table import (
    ELEMENTS, CATEGORY_COLOURS, Element, get_element,
)

log = logging.getLogger(__name__)


class PeriodicTableDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Periodic table of elements")
        self.resize(1040, 560)

        root = QVBoxLayout(self)
        top_row = QHBoxLayout()

        # Main table grid + f-block strip (scrollable so the layout
        # stays usable on small screens).
        grid_widget = QWidget()
        self._grid = QGridLayout(grid_widget)
        self._grid.setSpacing(2)
        self._grid.setContentsMargins(4, 4, 4, 4)
        self._build_grid()
        scroll = QScrollArea()
        scroll.setWidget(grid_widget)
        scroll.setWidgetResizable(True)
        top_row.addWidget(scroll, 3)

        # Side-pane for element details.
        self.info = QTextBrowser()
        self.info.setOpenExternalLinks(False)
        self.info.setFixedWidth(280)
        self.info.setHtml(
            "<p style='color:#666'>Click any element to see its details.</p>")
        top_row.addWidget(self.info, 1)
        root.addLayout(top_row, 1)

        # Category legend at the bottom.
        root.addWidget(self._make_legend())

        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        root.addWidget(bb)

        # Select hydrogen by default so the side-pane has content.
        self._show_element(get_element("H"))

    # -----------------------------------------------------------------
    # Grid construction

    def _build_grid(self) -> None:
        """Place each element cell at (period, group - 1). Lanthanides
        and actinides fill rows 8 and 9 respectively, left-aligned
        from group-3."""
        # Main 18-column grid: periods 1..7.
        for e in ELEMENTS:
            if e.group is None:
                continue                 # handled in the f-block loop below
            # Map (period, group) → grid row/col.
            row = e.period - 1
            col = e.group - 1
            self._grid.addWidget(self._make_cell(e), row, col)

        # Lanthanide / actinide rows: rows 7 and 8 (0-indexed), starting
        # from column 2 (i.e. group 3). Elements: La (57)..Lu (71),
        # Ac (89)..Lr (103).
        ln_row = 7
        ac_row = 8
        for e in ELEMENTS:
            if e.group is not None:
                continue
            if e.category == "lanthanide":
                idx = e.z - 57          # 0..14
                self._grid.addWidget(self._make_cell(e), ln_row, 2 + idx)
            elif e.category == "actinide":
                idx = e.z - 89
                self._grid.addWidget(self._make_cell(e), ac_row, 2 + idx)

    def _make_cell(self, e: Element) -> QPushButton:
        btn = QPushButton(f"{e.z}\n{e.symbol}")
        btn.setFixedSize(50, 50)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            f"QPushButton {{"
            f" background-color: {e.colour()};"
            f" border: 1px solid #444;"
            f" border-radius: 4px;"
            f" font-weight: bold; font-size: 10pt;"
            f" text-align: center;"
            f"}}"
            f"QPushButton:hover {{ border: 2px solid #000; }}"
        )
        btn.setToolTip(f"{e.name} ({e.symbol})  ·  Z = {e.z}  ·  "
                       f"{e.atomic_mass:.3f} u")
        btn.clicked.connect(lambda _=False, el=e: self._show_element(el))
        return btn

    def _make_legend(self) -> QWidget:
        w = QFrame()
        w.setFrameShape(QFrame.StyledPanel)
        lay = QHBoxLayout(w)
        lay.setContentsMargins(6, 2, 6, 2)
        lay.addWidget(QLabel("<b>Category:</b>"))
        for cat, colour in CATEGORY_COLOURS.items():
            chip = QLabel(cat.replace("-", " "))
            chip.setStyleSheet(
                f"background:{colour}; padding:2px 6px; "
                f"border:1px solid #666; border-radius:3px; "
                f"margin-right:4px;"
            )
            lay.addWidget(chip)
        lay.addStretch(1)
        return w

    # -----------------------------------------------------------------

    def _show_element(self, el: Optional[Element]) -> None:
        if el is None:
            return
        oxs = ", ".join(f"{s:+d}" for s in el.common_oxidation_states) \
            or "—"
        en = f"{el.electronegativity:.2f}" if el.electronegativity is not None \
            else "—"
        parts = [
            f"<h2 style='margin:0'>"
            f"<span style='color:#555'>{el.z}</span> {el.symbol}</h2>",
            f"<p style='font-size:13px; margin:2px 0'>"
            f"<b>{el.name}</b></p>",
            f"<p style='margin:4px 0'><b>Category:</b> "
            f"{el.category}<br>"
            f"<b>Period:</b> {el.period} · "
            f"<b>Group:</b> {el.group if el.group else '—'} · "
            f"<b>Block:</b> {el.block}</p>",
            f"<p style='margin:4px 0'>"
            f"<b>Atomic mass:</b> {el.atomic_mass:.4f} u<br>"
            f"<b>Pauling χ:</b> {en}<br>"
            f"<b>Common ox. states:</b> {oxs}</p>",
            f"<p style='margin:4px 0'><b>Electron config:</b><br>"
            f"<code style='font-size:11px'>"
            f"{el.electron_configuration or '—'}</code></p>",
        ]
        self.info.setHtml("".join(parts))
