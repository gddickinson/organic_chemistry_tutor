"""Phase 36 polish (round 135) — geometry tests for the
tapered-polygon wedge + hashed-ladder dash bond renderers.

The earlier `test_drawing_panel_stereo.py` round-130 cases verify
the *data-model* effect of wedge / dash tools (Bond.stereo flips
correctly, undo round-trips, mol-block writer emits the stereo
flag).  These tests verify the *visual primitives* — that wedges
produce a real `QGraphicsPolygonItem` triangle, dashes produce a
`QGraphicsItemGroup` of perpendicular hashes, the geometry
matches the bond-end positions, and refreshes after atom drag
keep the wedge in sync.
"""
from __future__ import annotations
import math
import os

import pytest
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import (
    QGraphicsItemGroup, QGraphicsLineItem, QGraphicsPolygonItem,
)

pytest.importorskip("rdkit")
pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def _app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as app:
        yield app


# ---- helpers --------------------------------------------------

def _build_wedge_panel(qtbot, *, stereo: str = "wedge"):
    """Build a panel with a single C-C bond and the requested
    stereo flag.  Returns the panel."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = DrawingPanel()
    qtbot.addWidget(panel)
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    panel.set_tool(f"bond-{stereo}")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    return panel


# ---- wedge geometry -------------------------------------------

def test_wedge_renders_as_polygon_item(_app, qtbot):
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    item = panel._bond_items[0]
    assert isinstance(item, QGraphicsPolygonItem), \
        f"expected QGraphicsPolygonItem, got {type(item).__name__}"


def test_wedge_polygon_is_a_triangle(_app, qtbot):
    """Apex at the begin atom + two-vertex base at the end atom."""
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    item = panel._bond_items[0]
    poly = item.polygon()
    assert poly.size() == 3, f"expected 3 vertices, got {poly.size()}"


def test_wedge_apex_at_begin_atom(_app, qtbot):
    """Vertex 0 of the polygon should sit on the begin atom
    (within sub-pixel tolerance)."""
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    item = panel._bond_items[0]
    poly = item.polygon()
    apex = poly[0]
    begin_x, begin_y = panel._atom_items[0]["pos"]
    assert abs(apex.x() - begin_x) < 0.5
    assert abs(apex.y() - begin_y) < 0.5


def test_wedge_base_centre_at_end_atom(_app, qtbot):
    """Average of vertices 1 + 2 should sit on the end atom."""
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    item = panel._bond_items[0]
    poly = item.polygon()
    base_cx = (poly[1].x() + poly[2].x()) / 2
    base_cy = (poly[1].y() + poly[2].y()) / 2
    end_x, end_y = panel._atom_items[1]["pos"]
    assert abs(base_cx - end_x) < 0.5
    assert abs(base_cy - end_y) < 0.5


def test_wedge_base_is_perpendicular_to_bond_axis(_app, qtbot):
    """The base of the triangle (vertex 1 → vertex 2) should be
    perpendicular to the begin → end bond axis."""
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    item = panel._bond_items[0]
    poly = item.polygon()
    bond_dx = poly[1].x() - poly[0].x()  # apex → base midpoint dir
    bond_dy = poly[1].y() - poly[0].y()
    base_dx = poly[2].x() - poly[1].x()
    base_dy = poly[2].y() - poly[1].y()
    # Pure perpendicular: (b · base_b) component is the dot product
    # in the bond direction; bond direction = end - begin.
    end_x, end_y = panel._atom_items[1]["pos"]
    begin_x, begin_y = panel._atom_items[0]["pos"]
    bond_dir_x, bond_dir_y = end_x - begin_x, end_y - begin_y
    dot = base_dx * bond_dir_x + base_dy * bond_dir_y
    assert abs(dot) < 1e-3, f"base not perpendicular: dot={dot}"


def test_wedge_base_width_matches_constant(_app, qtbot):
    """Triangle base width = 2 × _WEDGE_HALF_WIDTH_PX."""
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    item = panel._bond_items[0]
    poly = item.polygon()
    base_dx = poly[2].x() - poly[1].x()
    base_dy = poly[2].y() - poly[1].y()
    base_len = math.hypot(base_dx, base_dy)
    expected = 2 * DrawingPanel._WEDGE_HALF_WIDTH_PX
    assert abs(base_len - expected) < 0.5


def test_wedge_brush_is_solid_green(_app, qtbot):
    from orgchem.gui.panels.drawing_panel import DrawingPanel
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    item = panel._bond_items[0]
    assert item.brush().color() == DrawingPanel._STEREO_WEDGE_COLOUR


# ---- dash geometry --------------------------------------------

def test_dash_renders_as_item_group(_app, qtbot):
    panel = _build_wedge_panel(qtbot, stereo="dash")
    item = panel._bond_items[0]
    assert isinstance(item, QGraphicsItemGroup), \
        f"expected QGraphicsItemGroup, got {type(item).__name__}"


def test_dash_group_has_multiple_hash_lines(_app, qtbot):
    """A 60-px C-C dashed bond should pack at least 4 hashes."""
    panel = _build_wedge_panel(qtbot, stereo="dash")
    item = panel._bond_items[0]
    children = item.childItems()
    assert len(children) >= 4
    # All children should be QGraphicsLineItem hashes.
    for child in children:
        assert isinstance(child, QGraphicsLineItem)


def test_dash_hashes_widen_toward_end_atom(_app, qtbot):
    """First hash should be narrower than the last hash."""
    panel = _build_wedge_panel(qtbot, stereo="dash")
    item = panel._bond_items[0]
    children = item.childItems()
    first = children[0].line()
    last = children[-1].line()
    first_len = math.hypot(first.dx(), first.dy())
    last_len = math.hypot(last.dx(), last.dy())
    assert last_len > first_len + 1.0, \
        f"hash widening too small: {first_len}→{last_len}"


# ---- refresh after atom move ----------------------------------

def test_wedge_follows_atom_drag(_app, qtbot):
    """Move the end atom and verify the wedge polygon's base
    centre tracks the new position."""
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    # Drag end atom (idx 1).  Use the panel's select tool path.
    panel.set_tool("select")
    panel.handle_canvas_press(QPointF(30, 0))
    panel.handle_canvas_move(QPointF(80, 40))
    panel.handle_canvas_release(QPointF(80, 40))
    item = panel._bond_items[0]
    assert isinstance(item, QGraphicsPolygonItem)
    poly = item.polygon()
    base_cx = (poly[1].x() + poly[2].x()) / 2
    base_cy = (poly[1].y() + poly[2].y()) / 2
    assert abs(base_cx - 80.0) < 0.5
    assert abs(base_cy - 40.0) < 0.5


def test_dash_follows_atom_drag(_app, qtbot):
    panel = _build_wedge_panel(qtbot, stereo="dash")
    panel.set_tool("select")
    panel.handle_canvas_press(QPointF(30, 0))
    panel.handle_canvas_move(QPointF(60, 20))
    panel.handle_canvas_release(QPointF(60, 20))
    item = panel._bond_items[0]
    assert isinstance(item, QGraphicsItemGroup)
    # Last hash should sit close to the new end-atom position.
    last = item.childItems()[-1].line()
    last_cx = (last.x1() + last.x2()) / 2
    last_cy = (last.y1() + last.y2()) / 2
    end_x, end_y = panel._atom_items[1]["pos"]
    assert abs(last_cx - end_x) < 5.0
    assert abs(last_cy - end_y) < 5.0


# ---- stereo flip swaps visual type ----------------------------

def test_flipping_wedge_to_dash_changes_item_type(_app, qtbot):
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    assert isinstance(panel._bond_items[0], QGraphicsPolygonItem)
    panel.set_tool("bond-dash")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    assert isinstance(panel._bond_items[0], QGraphicsItemGroup)


def test_flipping_dash_back_to_plain_uses_line(_app, qtbot):
    """Toggle dash off → bond reverts to plain QGraphicsLineItem."""
    panel = _build_wedge_panel(qtbot, stereo="dash")
    assert isinstance(panel._bond_items[0], QGraphicsItemGroup)
    panel.set_tool("bond-dash")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    assert panel.get_structure().bonds[0].stereo == "none"
    assert isinstance(panel._bond_items[0], QGraphicsLineItem)


# ---- old item gets removed from scene -------------------------

def test_refresh_removes_old_scene_item(_app, qtbot):
    """A stereo flip must NOT leave orphan items on the scene —
    the old line / polygon should be removed before the new one
    is added."""
    panel = _build_wedge_panel(qtbot, stereo="wedge")
    n_before = len(panel._scene.items())
    # Toggle wedge off.
    panel.set_tool("bond-wedge")
    panel.handle_canvas_press(QPointF(-30, 0))
    panel.handle_canvas_press(QPointF(30, 0))
    n_after = len(panel._scene.items())
    # Item count should be the same (1 bond visual replaced 1 bond
    # visual; atoms unchanged).
    assert n_before == n_after, \
        f"scene leaked items: {n_before} → {n_after}"
