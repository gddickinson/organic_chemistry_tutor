"""Phase 34b round 116 — tests for the `SequenceBar` Qt widget.

Drives the widget headlessly via pytest-qt, exercising the JSON
data shape produced by `build_sequence_view().to_dict()`.
"""
from __future__ import annotations
import os

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent

pytest.importorskip("rdkit")
pytest.importorskip("pytestqt", reason="pytest-qt not installed")


# Minimal in-memory PDB fixture: 3 AA chain + 3 nt DNA chain.
_FIXTURE = """\
HEADER    TEST                                     01-JAN-26   1TST
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 20.00           C
ATOM      2  CA  GLY A   2       3.800   0.000   0.000  1.00 20.00           C
ATOM      3  CA  HIS A   3       7.600   0.000   0.000  1.00 20.00           C
ATOM      4  P   DA  B   1      10.000  10.000  10.000  1.00 25.00           P
ATOM      5  P   DT  B   2      13.000  10.000  10.000  1.00 25.00           P
ATOM      6  P   DG  B   3      16.000  10.000  10.000  1.00 25.00           P
END
"""


@pytest.fixture(scope="module")
def _app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as app:
        yield app


@pytest.fixture
def _view_dict():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.sequence_view import build_sequence_view
    protein = parse_pdb_text(_FIXTURE, pdb_id="1TST")
    view = build_sequence_view(protein)
    return view.to_dict()


# ---- basic rendering --------------------------------------------

def test_sequence_bar_set_view_accepts_empty_view(_app, qtbot):
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view({"pdb_id": "", "protein_chains": [],
                  "dna_chains": [], "highlights": []})
    # No crash, no rows, reasonable size-hint.
    assert bar.sizeHint().width() >= 200


def test_sequence_bar_set_view_accepts_real_view(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)
    # 1 DNA row + 1 protein row = 2 total.
    assert len(bar._rows) == 2
    # DNA row is first (stacked above proteins for teaching-reading
    # order).
    assert bar._rows[0].kind == "dna"
    assert bar._rows[0].one_letter == "ATG"
    assert bar._rows[1].kind == "protein"
    assert bar._rows[1].one_letter == "AGH"


# ---- programmatic selection ------------------------------------

def test_programmatic_selection_emits_and_stores(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)

    events = []
    bar.selection_changed.connect(
        lambda cid, s, e: events.append((cid, s, e)))
    bar.set_selection("A", 1, 3)

    assert bar.selection() == ("A", 1, 3)
    assert events == [("A", 1, 3)]


def test_clear_selection_resets_state(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)
    bar.set_selection("A", 1, 2)
    assert bar.selection() is not None
    bar.clear_selection()
    assert bar.selection() is None


# ---- mouse-driven selection ------------------------------------

def _fire_mouse(bar, kind, pos):
    """Helper: synthesise a mouse event + dispatch through the
    widget's handler."""
    from PySide6.QtCore import QPointF
    ev = QMouseEvent(
        kind, QPointF(pos), QPointF(pos),
        Qt.LeftButton, Qt.LeftButton, Qt.NoModifier,
    )
    if kind == QMouseEvent.MouseButtonPress:
        bar.mousePressEvent(ev)
    elif kind == QMouseEvent.MouseMove:
        bar.mouseMoveEvent(ev)
    elif kind == QMouseEvent.MouseButtonRelease:
        bar.mouseReleaseEvent(ev)


def test_click_selects_single_residue(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)
    # Second row is protein A; y offset = tick_h + 1*(char_h+row_pad)/2.
    y = bar._tick_h + bar._char_h + bar._row_pad + bar._char_h // 2
    x = bar._left_pad + bar._char_w + bar._char_w // 2   # col 1 = GLY
    _fire_mouse(bar, QMouseEvent.MouseButtonPress, QPoint(x, y))
    _fire_mouse(bar, QMouseEvent.MouseButtonRelease, QPoint(x, y))
    sel = bar.selection()
    assert sel is not None
    chain_id, start, end = sel
    assert chain_id == "A"
    assert start == 2 and end == 2   # residue number 2 = GLY


def test_click_drag_selects_span(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)
    y = bar._tick_h + bar._char_h + bar._row_pad + bar._char_h // 2
    x_start = bar._left_pad + bar._char_w // 2              # col 0 → ALA
    x_end = bar._left_pad + 2 * bar._char_w + bar._char_w // 2  # col 2 → HIS
    _fire_mouse(bar, QMouseEvent.MouseButtonPress, QPoint(x_start, y))
    _fire_mouse(bar, QMouseEvent.MouseMove, QPoint(x_end, y))
    _fire_mouse(bar, QMouseEvent.MouseButtonRelease, QPoint(x_end, y))
    sel = bar.selection()
    assert sel is not None
    chain_id, start, end = sel
    assert chain_id == "A"
    assert start == 1 and end == 3


def test_click_outside_clears_selection(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)
    bar.set_selection("A", 1, 2)
    # Click in the left-margin chain-id area (before _left_pad).
    _fire_mouse(bar, QMouseEvent.MouseButtonPress, QPoint(5, 40))
    assert bar.selection() is None


# ---- Round-117 toggle-deselect + Clear + scroll -----------------

def test_click_inside_selection_toggles_it_off(_app, qtbot, _view_dict):
    """Round-117 polish — clicking a residue that's already part of
    the current selection (without dragging) must clear the
    selection entirely and fire `selection_cleared`."""
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)

    # Pre-select protein chain A residues 1-3.
    bar.set_selection("A", 1, 3)
    cleared_events = []
    bar.selection_cleared.connect(lambda: cleared_events.append(True))

    # Now click on residue 2 (inside the selection) — press + release
    # at the same point, no drag.
    y = bar._tick_h + bar._char_h + bar._row_pad + bar._char_h // 2
    x = bar._left_pad + bar._char_w + bar._char_w // 2   # col 1 = res 2
    _fire_mouse(bar, QMouseEvent.MouseButtonPress, QPoint(x, y))
    _fire_mouse(bar, QMouseEvent.MouseButtonRelease, QPoint(x, y))

    assert bar.selection() is None
    assert cleared_events == [True]


def test_click_drag_within_selection_does_not_toggle(_app, qtbot, _view_dict):
    """A drag that starts inside the selection should NOT be
    misinterpreted as a toggle-off — the user is replacing the
    selection, not clearing it."""
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)
    bar.set_selection("A", 1, 3)

    y = bar._tick_h + bar._char_h + bar._row_pad + bar._char_h // 2
    x0 = bar._left_pad + bar._char_w + bar._char_w // 2              # col 1
    x1 = bar._left_pad + 2 * bar._char_w + bar._char_w // 2          # col 2
    _fire_mouse(bar, QMouseEvent.MouseButtonPress, QPoint(x0, y))
    _fire_mouse(bar, QMouseEvent.MouseMove, QPoint(x1, y))
    _fire_mouse(bar, QMouseEvent.MouseButtonRelease, QPoint(x1, y))

    # Drag happened → selection should be the new span, not None.
    sel = bar.selection()
    assert sel is not None
    chain, s, e = sel
    assert chain == "A"
    # Residues 2 → 3 (cols 1 → 2).
    assert s == 2 and e == 3


def test_clear_selection_emits_signal(_app, qtbot, _view_dict):
    """Programmatic `clear_selection()` must also fire the
    `selection_cleared` signal — used by the panel wrapper."""
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view(_view_dict)
    bar.set_selection("A", 1, 3)

    events = []
    bar.selection_cleared.connect(lambda: events.append(True))
    bar.clear_selection()
    assert bar.selection() is None
    assert events == [True]
    # Calling clear twice shouldn't re-fire (idempotent no-op).
    events.clear()
    bar.clear_selection()
    assert events == []


def test_panel_clear_button_disabled_until_selection(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBarPanel
    panel = SequenceBarPanel()
    qtbot.addWidget(panel)
    panel.set_view(_view_dict)
    assert not panel.clear_btn.isEnabled()
    panel.set_selection("A", 2, 3)
    assert panel.clear_btn.isEnabled()
    panel.clear_btn.click()
    assert not panel.clear_btn.isEnabled()
    assert panel.bar.selection() is None


def test_panel_cleared_signal_propagates(_app, qtbot, _view_dict):
    """Panel must re-emit `selection_cleared` whenever the bar
    fires it — so `ProteinPanel._on_sequence_cleared` can trigger
    the 3D orgchemClearHighlight call."""
    from orgchem.gui.widgets.sequence_bar import SequenceBarPanel
    panel = SequenceBarPanel()
    qtbot.addWidget(panel)
    panel.set_view(_view_dict)
    panel.set_selection("A", 1, 2)

    events = []
    panel.selection_cleared.connect(lambda: events.append(True))
    panel.clear_btn.click()
    assert events == [True]


def test_panel_scroll_arrows_wired(_app, qtbot, _view_dict):
    """Structural check — the scroll arrows exist, are enabled /
    disabled in response to overflow state, and the step size is
    the advertised 10 residues worth of pixels.  We drive the
    scrollbar directly (rather than depending on Qt's offscreen
    layout pass to produce overflow) since the exact pixel
    geometry of a hidden widget is unreliable."""
    from orgchem.gui.widgets.sequence_bar import SequenceBarPanel
    panel = SequenceBarPanel()
    qtbot.addWidget(panel)
    panel.set_view(_view_dict)

    # Buttons exist + wired to slots.
    assert panel.scroll_left_btn is not None
    assert panel.scroll_right_btn is not None
    assert panel.SCROLL_STEP_RESIDUES == 10

    # Simulate overflow by directly setting the scrollbar range.
    hbar = panel.scroll.horizontalScrollBar()
    hbar.setMinimum(0)
    hbar.setMaximum(1000)
    hbar.setValue(500)
    panel._update_scroll_button_state()
    assert panel.scroll_left_btn.isEnabled()
    assert panel.scroll_right_btn.isEnabled()

    # Right-click advances by 10 × char_w.
    step_px = panel.SCROLL_STEP_RESIDUES * panel.bar._char_w
    before = hbar.value()
    panel._scroll_right()
    assert hbar.value() == before + step_px
    before = hbar.value()
    panel._scroll_left()
    assert hbar.value() == before - step_px

    # At the maximum value, ▶ should be disabled; at 0, ◀ should be.
    hbar.setValue(hbar.maximum())
    panel._update_scroll_button_state()
    assert not panel.scroll_right_btn.isEnabled()
    assert panel.scroll_left_btn.isEnabled()
    hbar.setValue(0)
    panel._update_scroll_button_state()
    assert panel.scroll_left_btn.isEnabled() is False
    assert panel.scroll_right_btn.isEnabled()


def test_panel_scroll_arrows_disabled_without_overflow(_app, qtbot, _view_dict):
    """No overflow → both scroll arrows disabled."""
    from orgchem.gui.widgets.sequence_bar import SequenceBarPanel
    panel = SequenceBarPanel()
    qtbot.addWidget(panel)
    panel.set_view(_view_dict)
    hbar = panel.scroll.horizontalScrollBar()
    hbar.setMinimum(0)
    hbar.setMaximum(0)
    panel._update_scroll_button_state()
    assert not panel.scroll_left_btn.isEnabled()
    assert not panel.scroll_right_btn.isEnabled()


# ---- Phase 34e feature tracks ----------------------------------

def test_sequence_bar_stores_highlights_from_view(_app, qtbot):
    """Phase 34e round 118 — when the view carries pocket +
    ligand-contact highlights, the widget must store them on
    `_highlights` so `paintEvent` can render the underlay bars."""
    from orgchem.gui.widgets.sequence_bar import SequenceBar
    bar = SequenceBar()
    qtbot.addWidget(bar)
    bar.set_view({
        "pdb_id": "1TST",
        "protein_chains": [{
            "chain_id": "A",
            "one_letter": "AGHDSV",
            "three_letter": ["ALA", "GLY", "HIS", "ASP", "SER", "VAL"],
            "residue_numbers": [1, 2, 3, 4, 5, 6],
            "kind": "protein",
            "length": 6,
        }],
        "dna_chains": [],
        "highlights": [
            {"chain_id": "A", "start": 2, "end": 4,
             "kind": "pocket", "label": "Pocket #1",
             "colour": "#9FD5A0"},
            {"chain_id": "A", "start": 4, "end": 4,
             "kind": "h-bond", "label": "A:4 · h-bond",
             "colour": "#4B8BD5"},
        ],
    })
    assert len(bar._highlights) == 2
    kinds = {h["kind"] for h in bar._highlights}
    assert kinds == {"pocket", "h-bond"}


def test_protein_panel_refresh_applies_feature_tracks(_app, qtbot,
                                                      tmp_path, monkeypatch):
    """Phase 34e round 118 — `ProteinPanel._refresh_sequence_bar`
    must layer pocket + contact highlights onto the sequence view
    when those caches are populated."""
    import orgchem.sources.pdb as pdb_mod
    # Prime the cache with a minimal-but-valid fixture.
    fixture = """\
HEADER    TEST                                     01-JAN-26   1TST
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 20.00           C
ATOM      2  CA  GLY A   2       3.800   0.000   0.000  1.00 20.00           C
ATOM      3  CA  HIS A   3       7.600   0.000   0.000  1.00 20.00           C
ATOM      4  CA  ASP A   4      11.400   0.000   0.000  1.00 20.00           C
END
"""
    cache = tmp_path / "pdb_cache"
    cache.mkdir()
    (cache / "1TST.pdb").write_text(fixture)
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: cache)

    from orgchem.gui.panels.protein_panel import ProteinPanel
    panel = ProteinPanel()
    qtbot.addWidget(panel)
    panel._current_pdb = "1TST"

    # Prime fake pockets + contacts caches without running the
    # full geometric analysers.
    class _Pocket:
        lining_residues = [("A", 2), ("A", 3)]

    class _Contact:
        def __init__(self, chain, residue, kind):
            self.chain = chain
            self.residue = residue
            self.kind = kind

    class _Report:
        contacts = [_Contact("A", 3, "h-bond"),
                    _Contact("A", 4, "salt-bridge")]

    panel._last_pockets = [_Pocket()]
    panel._last_contacts = _Report()
    panel._refresh_sequence_bar()

    if not hasattr(panel, "sequence_panel"):
        pytest.skip("WebEngine not available; sequence panel absent.")

    hl = panel.sequence_panel.bar._highlights
    kinds = {h["kind"] for h in hl}
    assert "pocket" in kinds
    assert "h-bond" in kinds
    assert "salt-bridge" in kinds


# ---- panel wrapper ----------------------------------------------

def test_sequence_bar_panel_updates_status(_app, qtbot, _view_dict):
    from orgchem.gui.widgets.sequence_bar import SequenceBarPanel
    panel = SequenceBarPanel()
    qtbot.addWidget(panel)
    panel.set_view(_view_dict)
    # Status should mention both chain counts.
    text = panel.status.text()
    assert "1 protein" in text
    assert "1 nucleic-acid" in text

    # Programmatic selection propagates to the panel status label
    # AND re-emits the top-level signal.
    events = []
    panel.selection_changed.connect(
        lambda cid, s, e: events.append((cid, s, e)))
    panel.bar.set_selection("A", 2, 3)
    # The panel's own `_on_selection` will trigger on the SequenceBar
    # signal — check both the status and the re-emit.
    assert events == [("A", 2, 3)]
    assert "A:2-3" in panel.status.text()
