"""Phase 34b round 116 — `SequenceBar` widget.

Renders a :class:`SequenceView` (from `orgchem.core.sequence_view`)
as a scrollable monospace strip with:

- One row per protein chain, stacked vertically.
- One row per DNA / RNA chain above the protein rows.
- Residue-number tick marks every 10 positions.
- Click + click-drag selection; the user can pick a single residue
  or a contiguous span.
- Coloured underlay per `HighlightSpan` (pockets / ligand contacts /
  secondary structure / user tags).
- `selection_changed(chain_id, start, end)` Qt signal so the
  surrounding panel can feed the selection into the 3D viewer.

Designed to read the JSON-serialisable
:meth:`SequenceView.to_dict()` shape so the same widget can render
(a) data built in-process from a `Protein` dataclass, or (b) data
returned by the `get_sequence_view(pdb_id)` agent action.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Qt, Signal, QRect, QSize
from PySide6.QtGui import (
    QColor, QFont, QFontMetrics, QPainter, QPen, QMouseEvent,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea, QWidget, QVBoxLayout, QLabel, QSizePolicy,
    QScrollArea, QHBoxLayout, QPushButton, QToolButton,
)


# ---- pure data shape (widget-internal) ----------------------------

@dataclass
class _Row:
    chain_id: str
    one_letter: str
    residue_numbers: List[int]
    kind: str             # protein / dna / rna


def _rows_from_view_dict(view: dict) -> List[_Row]:
    out: List[_Row] = []
    # DNA/RNA row(s) stack above protein row(s) so the
    # molecular-biology reading order (5' → 3' above, N → C
    # below) matches most teaching diagrams.
    for chain in view.get("dna_chains", []) or []:
        out.append(_Row(
            chain_id=chain["chain_id"],
            one_letter=chain["one_letter"],
            residue_numbers=list(chain["residue_numbers"]),
            kind=chain.get("kind", "dna"),
        ))
    for chain in view.get("protein_chains", []) or []:
        out.append(_Row(
            chain_id=chain["chain_id"],
            one_letter=chain["one_letter"],
            residue_numbers=list(chain["residue_numbers"]),
            kind=chain.get("kind", "protein"),
        ))
    return out


# ---- widget --------------------------------------------------------

class SequenceBar(QWidget):
    """Scrollable monospace sequence strip with click-drag selection.

    Usage::

        bar = SequenceBar()
        bar.set_view(view.to_dict())   # or SequenceView.to_dict()
        bar.selection_changed.connect(my_panel.on_sequence_selection)

    Selection semantics:

    - Click one residue → selection is (chain_id, start=resi, end=resi).
    - Click-drag from residue A to residue B on the same row → span.
    - Drag across rows falls back to single-row (clipped at the
      starting row).
    - Clicking outside any row clears the selection.
    """

    #: Emitted whenever the user finishes a selection.  Coordinates
    #: are in PDB-native residue-numbering (not column index).
    selection_changed = Signal(str, int, int)
    #: Emitted when the selection is cleared — either by clicking
    #: an already-selected residue (toggle-off), calling
    #: `clear_selection()`, or via the panel-wrapper Clear button.
    selection_cleared = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._rows: List[_Row] = []
        self._highlights: List[Dict] = []   # raw `HighlightSpan.to_dict`
        self._selection: Optional[Tuple[str, int, int]] = None
        self._drag_anchor: Optional[Tuple[int, int]] = None  # (row_idx, col)
        # Toggle-deselect state: if the mouse-down landed inside the
        # current selection AND the user didn't drag, treat the
        # release as a deselect rather than a re-click.
        self._pressed_inside_selection = False
        self._drag_moved = False
        # Colours ---------------------------------------------------
        self._fg = QColor("#1a1a1a")
        self._bg = QColor("#fafafa")
        self._tick = QColor("#888888")
        self._selection_colour = QColor(80, 140, 210, 96)
        # Layout constants (set via setFont() for DPI-aware sizing)
        self._char_w = 10
        self._char_h = 16
        self._row_pad = 6
        self._left_pad = 40       # space for chain-id label
        self._tick_h = 12
        self._set_monospace_font()
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    # ---- public API -------------------------------------------

    def set_view(self, view: dict) -> None:
        """Replace the displayed rows + highlights in one atomic
        update."""
        self._rows = _rows_from_view_dict(view)
        self._highlights = list(view.get("highlights", []) or [])
        self._selection = None
        self.updateGeometry()
        self.update()

    def clear_selection(self) -> None:
        had_selection = self._selection is not None
        self._selection = None
        self.update()
        if had_selection:
            self.selection_cleared.emit()

    def set_selection(self, chain_id: str, start: int, end: int) -> None:
        """Programmatic selection — used by the 3D click-to-select
        bridge (Phase 34c)."""
        self._selection = (chain_id, start, end)
        self.selection_changed.emit(chain_id, start, end)
        self.update()

    def selection(self) -> Optional[Tuple[str, int, int]]:
        return self._selection

    # ---- sizing -----------------------------------------------

    def sizeHint(self) -> QSize:
        if not self._rows:
            return QSize(self._left_pad + 400, self._tick_h + 20)
        w = self._left_pad + self._char_w * max(
            (len(r.one_letter) for r in self._rows), default=0)
        h = self._tick_h + (self._char_h + self._row_pad) * len(self._rows)
        return QSize(max(w, 400), max(h, 40))

    def minimumSizeHint(self) -> QSize:
        return QSize(200, 40)

    # ---- painting ---------------------------------------------

    def paintEvent(self, event):  # noqa: N802
        p = QPainter(self)
        p.fillRect(self.rect(), self._bg)
        # Tick marks (residue numbers every 10) along top row.
        if self._rows:
            self._paint_ticks(p)
        for i, row in enumerate(self._rows):
            self._paint_row(p, i, row)

    def _paint_ticks(self, p: QPainter) -> None:
        p.setPen(QPen(self._tick))
        y = self._tick_h - 2
        # Pick the widest row to base tick alignment on.
        longest = max(self._rows, key=lambda r: len(r.one_letter))
        for idx, resi in enumerate(longest.residue_numbers):
            if idx % 10 != 0:
                continue
            x = self._left_pad + idx * self._char_w
            p.drawText(x, y, str(resi))

    def _paint_row(self, p: QPainter, row_idx: int, row: _Row) -> None:
        top = self._tick_h + row_idx * (self._char_h + self._row_pad)
        # Chain-id label (left margin).
        p.setPen(QPen(self._fg))
        label_font = QFont(self.font())
        label_font.setBold(True)
        p.setFont(label_font)
        p.drawText(4, top + self._char_h - 2, f"{row.chain_id}:")
        p.setFont(self.font())
        # Highlights for this chain first (painted under the glyphs).
        for h in self._highlights:
            if h.get("chain_id") != row.chain_id:
                continue
            start_col = self._seq_id_to_col(row, int(h.get("start", 0)))
            end_col = self._seq_id_to_col(row, int(h.get("end", 0)))
            if start_col is None or end_col is None:
                continue
            colour = QColor(h.get("colour") or "#C0D0E0")
            colour.setAlpha(100)
            rect = QRect(
                self._left_pad + start_col * self._char_w,
                top, (end_col - start_col + 1) * self._char_w,
                self._char_h,
            )
            p.fillRect(rect, colour)
        # Selection band (painted over highlights, under glyphs).
        if self._selection and self._selection[0] == row.chain_id:
            _, s_start, s_end = self._selection
            sc = self._seq_id_to_col(row, s_start)
            ec = self._seq_id_to_col(row, s_end)
            if sc is not None and ec is not None:
                if sc > ec:
                    sc, ec = ec, sc
                rect = QRect(
                    self._left_pad + sc * self._char_w,
                    top, (ec - sc + 1) * self._char_w,
                    self._char_h,
                )
                p.fillRect(rect, self._selection_colour)
        # Glyph row.
        p.setPen(QPen(self._fg))
        y = top + self._char_h - 3
        for col, ch in enumerate(row.one_letter):
            x = self._left_pad + col * self._char_w
            p.drawText(x + 1, y, ch)

    # ---- mouse interaction -----------------------------------

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        hit = self._hit_row(event.position().toPoint())
        if hit is None:
            self._drag_anchor = None
            self._pressed_inside_selection = False
            self._drag_moved = False
            if self._selection is not None:
                self.clear_selection()   # already emits selection_cleared
            else:
                self.update()
            return
        self._drag_anchor = hit
        self._drag_moved = False
        row_idx, col = hit
        row = self._rows[row_idx]
        resi = self._col_to_seq_id(row, col)
        # Did we click inside the current selection?  If so, a
        # release-without-drag should toggle it off.
        self._pressed_inside_selection = self._is_inside_selection(
            row.chain_id, resi)
        # Don't mutate the selection on press yet — defer until
        # release so a single-click-toggle behaves predictably.
        # (Drag still updates `_selection` incrementally via
        # mouseMoveEvent.)
        if resi is not None and not self._pressed_inside_selection:
            self._selection = (row.chain_id, resi, resi)
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._drag_anchor is None:
            return
        hit = self._hit_row(event.position().toPoint())
        if hit is None:
            return
        anchor_row_idx, anchor_col = self._drag_anchor
        row_idx, col = hit
        # Clamp cross-row drags to the anchor row.
        if row_idx != anchor_row_idx:
            return
        # A real drag happened — suppress any pending toggle.
        if col != anchor_col:
            self._drag_moved = True
            self._pressed_inside_selection = False
        row = self._rows[row_idx]
        start_col, end_col = sorted((anchor_col, col))
        start_resi = self._col_to_seq_id(row, start_col)
        end_resi = self._col_to_seq_id(row, end_col)
        if start_resi is None or end_resi is None:
            return
        self._selection = (row.chain_id, start_resi, end_resi)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        # Toggle-deselect: click landed inside the existing
        # selection, never dragged → clear it on release.
        if self._pressed_inside_selection and not self._drag_moved:
            self._drag_anchor = None
            self._pressed_inside_selection = False
            self.clear_selection()
            return
        if self._drag_anchor is None or self._selection is None:
            self._drag_anchor = None
            self._pressed_inside_selection = False
            self._drag_moved = False
            return
        chain_id, start, end = self._selection
        self.selection_changed.emit(chain_id, start, end)
        self._drag_anchor = None
        self._pressed_inside_selection = False
        self._drag_moved = False

    # Helper for toggle-deselect ------------------------------

    def _is_inside_selection(self, chain_id: str,
                             resi: Optional[int]) -> bool:
        if self._selection is None or resi is None:
            return False
        sel_chain, sel_start, sel_end = self._selection
        if sel_chain != chain_id:
            return False
        lo, hi = sorted((sel_start, sel_end))
        return lo <= resi <= hi

    # ---- geometry helpers ------------------------------------

    def _set_monospace_font(self) -> None:
        font = QFont("Monaco" if self._is_mac() else "Menlo")
        if not font.exactMatch():
            font = QFont("Courier")
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(11)
        self.setFont(font)
        metrics = QFontMetrics(font)
        self._char_w = metrics.horizontalAdvance("M")
        self._char_h = metrics.height()

    def _is_mac(self) -> bool:
        import sys
        return sys.platform == "darwin"

    def _hit_row(self, pt) -> Optional[Tuple[int, int]]:
        """Return (row_idx, column) the click landed on, or None
        if outside any row."""
        if pt.x() < self._left_pad:
            return None
        y = pt.y() - self._tick_h
        if y < 0:
            return None
        row_h = self._char_h + self._row_pad
        row_idx = y // row_h
        if row_idx >= len(self._rows):
            return None
        row_idx = int(row_idx)
        col = (pt.x() - self._left_pad) // self._char_w
        row = self._rows[row_idx]
        if col < 0 or col >= len(row.one_letter):
            return None
        return (row_idx, int(col))

    def _col_to_seq_id(self, row: _Row, col: int) -> Optional[int]:
        if 0 <= col < len(row.residue_numbers):
            return row.residue_numbers[col]
        return None

    def _seq_id_to_col(self, row: _Row, seq_id: int) -> Optional[int]:
        # Linear search is fine — chains rarely exceed ~500 residues.
        for idx, r in enumerate(row.residue_numbers):
            if r == seq_id:
                return idx
        # Fall back to the nearest column if the requested seq_id
        # isn't directly in the list (e.g. insertion codes in weird
        # PDB entries).  Clamp to the range.
        if not row.residue_numbers:
            return None
        if seq_id < row.residue_numbers[0]:
            return 0
        if seq_id > row.residue_numbers[-1]:
            return len(row.residue_numbers) - 1
        return None


# ---- scrollable host ---------------------------------------------

class SequenceBarPanel(QWidget):
    """Scrollable wrapper + selection-summary label for the
    :class:`SequenceBar`.  Drop-in widget for the Proteins 3D
    sub-tab (Phase 34c).

    Round 117 polish — adds a left / right scroll-arrow pair and
    a Clear button.  The scroll arrows step the horizontal
    viewport by ~10 residues per click so long sequences are
    navigable without touching the mouse-scroll wheel; holding
    a modifier isn't required.  The Clear button calls
    :meth:`SequenceBar.clear_selection` and is enabled only
    while a selection exists.
    """

    selection_changed = Signal(str, int, int)
    selection_cleared = Signal()

    #: Viewport step per arrow click, in residues — 10 residues
    #: matches the tick-mark cadence, so one click advances by
    #: exactly one tick.
    SCROLL_STEP_RESIDUES = 10

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(2, 2, 2, 2)
        lay.setSpacing(2)

        # Toolbar row — scroll arrows + Clear button.
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        self.scroll_left_btn = QToolButton()
        self.scroll_left_btn.setText("◀")
        self.scroll_left_btn.setToolTip(
            f"Scroll left {self.SCROLL_STEP_RESIDUES} residues")
        self.scroll_left_btn.setAutoRepeat(True)
        self.scroll_left_btn.setAutoRepeatInterval(90)
        self.scroll_left_btn.clicked.connect(self._scroll_left)
        toolbar.addWidget(self.scroll_left_btn)

        self.scroll_right_btn = QToolButton()
        self.scroll_right_btn.setText("▶")
        self.scroll_right_btn.setToolTip(
            f"Scroll right {self.SCROLL_STEP_RESIDUES} residues")
        self.scroll_right_btn.setAutoRepeat(True)
        self.scroll_right_btn.setAutoRepeatInterval(90)
        self.scroll_right_btn.clicked.connect(self._scroll_right)
        toolbar.addWidget(self.scroll_right_btn)

        toolbar.addSpacing(8)

        self.clear_btn = QPushButton("Clear selection")
        self.clear_btn.setToolTip(
            "Clear the selected residue span (click any selected "
            "residue to toggle it off, or press this button to "
            "clear everything).")
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self._on_clear_clicked)
        toolbar.addWidget(self.clear_btn)

        toolbar.addStretch(1)
        lay.addLayout(toolbar)

        # Sequence display proper.
        self.bar = SequenceBar()
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.bar)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(80)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        lay.addWidget(self.scroll, 1)

        self.status = QLabel("Click + drag to select residues.  "
                             "Click a selected residue again to "
                             "deselect.")
        self.status.setStyleSheet("color:#666; padding:2px;")
        lay.addWidget(self.status)

        self.bar.selection_changed.connect(self._on_selection)
        self.bar.selection_cleared.connect(self._on_cleared)

    def set_view(self, view: dict) -> None:
        self.bar.set_view(view)
        n_prot = len(view.get('protein_chains', []) or [])
        n_dna = len(view.get('dna_chains', []) or [])
        self.status.setText(
            f"{n_prot} protein + {n_dna} nucleic-acid chain(s) loaded")
        # Freshly loaded — no selection yet.
        self.clear_btn.setEnabled(False)
        # Reset horizontal scroll to the start of the sequence.
        self.scroll.horizontalScrollBar().setValue(0)
        # Scroll buttons only matter if the content is wider than
        # the viewport — disable them otherwise.
        self._update_scroll_button_state()

    def set_selection(self, chain_id: str, start: int, end: int) -> None:
        self.bar.set_selection(chain_id, start, end)
        # `set_selection` on the bar doesn't fire `selection_changed`
        # as a user action, but we still want the Clear button
        # enabled — mirror the state directly.
        self.clear_btn.setEnabled(True)

    # ---- internals ---------------------------------------------

    def _on_selection(self, chain_id: str, start: int, end: int) -> None:
        span = (f"{chain_id}:{start}" if start == end
                else f"{chain_id}:{start}-{end}")
        self.status.setText(f"Selected {span}")
        self.clear_btn.setEnabled(True)
        self.selection_changed.emit(chain_id, start, end)

    def _on_cleared(self) -> None:
        self.status.setText("Selection cleared.")
        self.clear_btn.setEnabled(False)
        self.selection_cleared.emit()

    def _on_clear_clicked(self) -> None:
        self.bar.clear_selection()

    def _scroll_left(self) -> None:
        hbar = self.scroll.horizontalScrollBar()
        hbar.setValue(hbar.value() - self.SCROLL_STEP_RESIDUES *
                      self.bar._char_w)
        self._update_scroll_button_state()

    def _scroll_right(self) -> None:
        hbar = self.scroll.horizontalScrollBar()
        hbar.setValue(hbar.value() + self.SCROLL_STEP_RESIDUES *
                      self.bar._char_w)
        self._update_scroll_button_state()

    def _update_scroll_button_state(self) -> None:
        """Enable scroll buttons only when the content overflows +
        grey out the one you can't use right now (already at the
        start / end)."""
        hbar = self.scroll.horizontalScrollBar()
        hbar_maximum = hbar.maximum()
        has_overflow = hbar_maximum > 0
        if not has_overflow:
            self.scroll_left_btn.setEnabled(False)
            self.scroll_right_btn.setEnabled(False)
            return
        self.scroll_left_btn.setEnabled(hbar.value() > 0)
        self.scroll_right_btn.setEnabled(hbar.value() < hbar_maximum)

    def resizeEvent(self, event):  # noqa: N802
        super().resizeEvent(event)
        self._update_scroll_button_state()
