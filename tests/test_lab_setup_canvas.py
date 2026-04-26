"""Phase 38c.2 (round 187) — lab-setup canvas dialog skeleton.

Tests the Qt UI scaffolding shipped in 38c.2: palette dock
populates from the headless palette, canvas view exists, dialog
is a singleton, *Load setup* swaps the palette to a per-setup
filter.

Drag-and-drop wiring (38c.3) ships next round; these tests stay
focused on the structural skeleton so the next round can extend
without breaking them.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")
pytest.importorskip("PySide6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


# ==================================================================
# Shared Qt fixture
# ==================================================================

@pytest.fixture(scope="module")
def qt_app():
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def dialog(qt_app):
    """Fresh dialog per test (avoid singleton bleed across
    tests)."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    # Reset the singleton so each test gets a clean slate.
    LabSetupCanvasDialog._instance = None
    dlg = LabSetupCanvasDialog()
    yield dlg
    LabSetupCanvasDialog._instance = None
    dlg.deleteLater()


# ==================================================================
# Singleton + structural skeleton
# ==================================================================

def test_singleton_returns_same_instance(qt_app):
    from orgchem.gui.dialogs.lab_setup_canvas import (
        LabSetupCanvasDialog,
    )
    LabSetupCanvasDialog._instance = None
    a = LabSetupCanvasDialog.singleton()
    b = LabSetupCanvasDialog.singleton()
    assert a is b
    LabSetupCanvasDialog._instance = None


def test_dialog_is_modeless(dialog):
    """Round 187: dialog should NOT be modal so the user can
    keep working in the molecule workspace alongside it."""
    assert dialog.isModal() is False


def test_dialog_has_palette_dock_and_canvas(dialog):
    from orgchem.gui.dialogs.lab_setup_canvas import (
        CanvasView, PaletteDock,
    )
    assert isinstance(dialog.palette_dock(), PaletteDock)
    assert isinstance(dialog.canvas(), CanvasView)


# ==================================================================
# Palette dock content
# ==================================================================

def test_palette_dock_lists_every_equipment_item(dialog):
    """The dock loads `default_palette()` on construction."""
    from orgchem.core.lab_palette import default_palette
    full = default_palette()
    assert dialog.palette_dock().total_items() == len(full)


def test_palette_dock_groups_by_category(dialog):
    """The tree shows one top-level row per category, with the
    equipment items as children."""
    tree = dialog.palette_dock()._tree
    n_top = tree.topLevelItemCount()
    from orgchem.core.lab_palette import default_palette
    assert n_top == len(default_palette().categories)
    # First top-level row should be "Glassware (4)" given the
    # canonical display order.
    first = tree.topLevelItem(0).text(0)
    assert first.startswith("Glassware")


def test_palette_dock_emits_signal_on_item_click(dialog, qt_app):
    """Clicking an equipment row emits `item_selected(equipment_id)`
    — the entry point Phase 38c.3 will use to start a drag."""
    captured: list[str] = []
    dialog.palette_dock().item_selected.connect(captured.append)
    # Find the first child of the first category and trigger
    # the click handler directly (saves a real mouse event).
    tree = dialog.palette_dock()._tree
    cat = tree.topLevelItem(0)
    assert cat.childCount() > 0
    child = cat.child(0)
    dialog.palette_dock()._on_item_clicked(child, 0)
    assert captured, "no signal emitted"
    assert captured[0]   # non-empty equipment id


def test_palette_dock_ignores_category_header_clicks(dialog):
    """Clicking a category header (top-level row) must NOT emit
    `item_selected` — only equipment leaf rows do."""
    captured: list[str] = []
    dialog.palette_dock().item_selected.connect(captured.append)
    tree = dialog.palette_dock()._tree
    cat = tree.topLevelItem(0)
    dialog.palette_dock()._on_item_clicked(cat, 0)
    assert captured == [], \
        "category-header click should not emit a signal"


# ==================================================================
# Load setup
# ==================================================================

def test_load_setup_swaps_palette(dialog):
    """Loading a Phase-38b setup id swaps the palette to that
    setup's equipment list."""
    from orgchem.core.lab_palette import (
        default_palette, palette_for_setup,
    )
    full = len(default_palette())
    target = palette_for_setup("simple_distillation")
    assert dialog.load_setup("simple_distillation") is True
    assert dialog.palette_dock().total_items() == len(target)
    assert dialog.palette_dock().total_items() < full


def test_load_setup_returns_false_for_unknown_id(dialog):
    assert dialog.load_setup("not-a-real-setup-id") is False


def test_show_all_button_resets_palette(dialog):
    """*Show all equipment* button restores the full palette
    after a setup load."""
    from orgchem.core.lab_palette import default_palette
    dialog.load_setup("simple_distillation")
    dialog._on_show_all()
    assert (dialog.palette_dock().total_items()
            == len(default_palette()))


# ==================================================================
# Canvas
# ==================================================================

def test_canvas_starts_empty(dialog):
    """Round-187 (38c.2) canvas has no items — drop wiring is
    deferred to 38c.3."""
    assert dialog.canvas().item_count() == 0


def test_clear_canvas_button_works(dialog):
    """Clicking *Clear canvas* empties the scene (no-op when
    empty, but must not error)."""
    dialog._on_clear()
    assert dialog.canvas().item_count() == 0


# ==================================================================
# Phase 38c.3 — drag/drop wiring + EquipmentGlyph
# ==================================================================

def test_canvas_accepts_drops(dialog):
    """Round-188 (38c.3): the canvas view must accept drops so
    Qt's drag/drop machinery can fire dragEnterEvent."""
    assert dialog.canvas().acceptDrops() is True


def test_palette_tree_is_drag_enabled(dialog):
    """The palette tree's `dragEnabled` flag is on so a click-
    and-hold from a leaf item starts a Qt drag."""
    assert dialog.palette_dock()._tree.dragEnabled() is True


def test_place_equipment_adds_glyph_to_canvas(dialog):
    """`place_equipment(eid, x, y)` adds an `EquipmentGlyph`
    at the requested scene coords + emits `equipment_placed`."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        EquipmentGlyph,
    )
    captured: list = []
    dialog.canvas().equipment_placed.connect(
        lambda *args: captured.append(args))
    glyph = dialog.canvas().place_equipment("rbf", 100.0, 200.0)
    assert isinstance(glyph, EquipmentGlyph)
    assert glyph.equipment_id() == "rbf"
    assert glyph.label() == "Round-bottom flask"
    assert glyph.pos().x() == 100.0
    assert glyph.pos().y() == 200.0
    # Signal emitted with the same payload.
    assert captured == [("rbf", 100.0, 200.0)]


def test_place_equipment_returns_none_for_unknown_id(dialog):
    """Unknown equipment id yields no glyph + no signal."""
    captured: list = []
    dialog.canvas().equipment_placed.connect(
        lambda *args: captured.append(args))
    result = dialog.canvas().place_equipment(
        "not-a-real-equipment", 0, 0)
    assert result is None
    assert captured == []
    assert dialog.canvas().item_count() == 0


def test_multiple_glyphs_coexist(dialog):
    """Placing multiple distinct equipment items leaves them all
    on the canvas — `equipment_glyphs()` enumerates them."""
    dialog.canvas().place_equipment("rbf", 100, 100)
    dialog.canvas().place_equipment("liebig_condenser", 200, 100)
    dialog.canvas().place_equipment("heating_mantle", 100, 200)
    glyphs = dialog.canvas().equipment_glyphs()
    assert len(glyphs) == 3
    eids = {g.equipment_id() for g in glyphs}
    assert eids == {"rbf", "liebig_condenser", "heating_mantle"}


def test_clear_canvas_removes_glyphs(dialog):
    """*Clear canvas* drops every placed glyph."""
    dialog.canvas().place_equipment("rbf", 50, 50)
    dialog.canvas().place_equipment("beaker", 150, 50)
    assert len(dialog.canvas().equipment_glyphs()) == 2
    dialog._on_clear()
    assert len(dialog.canvas().equipment_glyphs()) == 0


def test_glyph_is_movable_and_selectable(dialog):
    """Placed glyphs can be moved + selected so the user can
    rearrange the apparatus after dropping."""
    from PySide6.QtWidgets import QGraphicsItem
    glyph = dialog.canvas().place_equipment("rbf", 0, 0)
    assert glyph.flags() & QGraphicsItem.ItemIsMovable
    assert glyph.flags() & QGraphicsItem.ItemIsSelectable


def test_equipment_mime_constant_exported(dialog):
    """`EQUIPMENT_MIME` is a stable string constant used by
    both the drag source + drop target — exported so future
    sub-phases can reuse it."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        EQUIPMENT_MIME,
    )
    assert EQUIPMENT_MIME.startswith("application/")
    assert "orgchem" in EQUIPMENT_MIME


def test_drop_event_places_equipment(dialog, qt_app):
    """Round-trip: synthesise a drop event with the equipment
    MIME payload + verify it lands on the canvas as a glyph."""
    from PySide6.QtCore import QMimeData, QPoint, QPointF, Qt
    from PySide6.QtGui import QDropEvent
    from orgchem.gui.dialogs.lab_setup_canvas import (
        EQUIPMENT_MIME,
    )
    canvas = dialog.canvas()
    mime = QMimeData()
    mime.setData(EQUIPMENT_MIME, b"erlenmeyer")
    pos = QPointF(150, 75)
    # PySide6's QDropEvent ctor: (pos, actions, mime, buttons,
    # modifiers, type=Drop).
    evt = QDropEvent(
        pos, Qt.CopyAction, mime,
        Qt.LeftButton, Qt.NoModifier,
    )
    canvas.dropEvent(evt)
    glyphs = canvas.equipment_glyphs()
    assert len(glyphs) == 1
    assert glyphs[0].equipment_id() == "erlenmeyer"


def test_drop_ignores_unrecognised_mime(dialog):
    """A drop carrying a different MIME type is forwarded to
    the parent class and does NOT place an equipment glyph."""
    from PySide6.QtCore import QMimeData, QPointF, Qt
    from PySide6.QtGui import QDropEvent
    canvas = dialog.canvas()
    mime = QMimeData()
    mime.setText("just plain text")
    evt = QDropEvent(
        QPointF(100, 100), Qt.CopyAction, mime,
        Qt.LeftButton, Qt.NoModifier,
    )
    canvas.dropEvent(evt)
    assert canvas.equipment_glyphs() == []


# ==================================================================
# Phase 38c.4 — snap-validation
# ==================================================================

def test_validate_port_pair_compatible():
    """Two compatible 24/29 ground-glass joints (male ↔ female)
    validate clean."""
    from orgchem.core.lab_equipment import get_equipment
    from orgchem.core.lab_setups import validate_port_pair
    rbf = get_equipment("rbf")             # 24/29 female "neck"
    head = get_equipment("distillation_head")
    # distillation_head's "bottom" port is 24/29 male — fits the
    # 24/29 female RBF neck.
    err = validate_port_pair(
        rbf, "neck", head, "bottom")
    assert err is None, f"unexpected error: {err}"


def test_validate_port_pair_two_female_joints_rejected():
    """Two female 24/29 ground-glass joints can't physically
    connect — the validator catches it as a sex mismatch."""
    from orgchem.core.lab_equipment import get_equipment
    from orgchem.core.lab_setups import validate_port_pair
    rbf = get_equipment("rbf")  # both have 24/29 female necks
    err = validate_port_pair(rbf, "neck", rbf, "neck")
    assert err is not None
    assert "sex" in err.lower() or "mismatch" in err.lower()


def test_validate_port_pair_unknown_port_rejected():
    from orgchem.core.lab_equipment import get_equipment
    from orgchem.core.lab_setups import validate_port_pair
    rbf = get_equipment("rbf")
    head = get_equipment("distillation_head")
    err = validate_port_pair(
        rbf, "not-a-real-port", head, "bottom")
    assert err is not None
    assert "not on" in err


def test_validate_port_pair_open_wildcard():
    """A port with joint_type ``open`` (clamp grip / hot-plate
    top) accepts any other port — used for non-glass-joint
    contact like a clamp holding an RBF."""
    from orgchem.core.lab_equipment import get_equipment
    from orgchem.core.lab_setups import validate_port_pair
    rbf = get_equipment("rbf")
    clamp = get_equipment("clamp_3prong")
    # clamp's "jaws" port is open; pair with the RBF's neck.
    err = validate_port_pair(
        rbf, "neck", clamp, "jaws")
    assert err is None


def test_canvas_connect_glyphs_creates_line(dialog):
    """`connect_glyphs` adds a `ConnectionLine` to the scene
    and emits `equipment_connected`."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        ConnectionLine,
    )
    captured: list = []
    dialog.canvas().equipment_connected.connect(
        lambda *args: captured.append(args))
    g_a = dialog.canvas().place_equipment("rbf", 100, 100)
    g_b = dialog.canvas().place_equipment(
        "distillation_head", 300, 100)
    line = dialog.canvas().connect_glyphs(
        g_a, "neck", g_b, "bottom")
    assert isinstance(line, ConnectionLine)
    assert line.is_valid() is True
    assert line.error() is None
    # Signal payload: (eid_a, port_a, eid_b, port_b, error="")
    assert captured == [(
        "rbf", "neck", "distillation_head", "bottom", ""
    )]


def test_canvas_connect_glyphs_invalid_pair_dashes_red(dialog):
    """An incompatible port pair still draws a `ConnectionLine`
    but tags it with the error string + dashed-red style."""
    captured: list = []
    dialog.canvas().equipment_connected.connect(
        lambda *args: captured.append(args))
    g_a = dialog.canvas().place_equipment("rbf", 100, 100)
    g_b = dialog.canvas().place_equipment("rbf", 300, 100)
    # Two RBFs both have female 24/29 necks — ground-glass sex
    # mismatch.
    line = dialog.canvas().connect_glyphs(
        g_a, "neck", g_b, "neck")
    assert line is not None
    assert line.is_valid() is False
    assert line.error() is not None
    assert "sex" in line.error().lower() or \
        "mismatch" in line.error().lower()
    # Signal carries the error string in slot 4.
    assert len(captured) == 1
    eid_a, p_a, eid_b, p_b, err = captured[0]
    assert err   # non-empty


def test_connection_line_z_value_below_glyphs(dialog):
    """Connection lines render under glyphs so the equipment
    overlays the line endpoints."""
    g_a = dialog.canvas().place_equipment("rbf", 0, 0)
    g_b = dialog.canvas().place_equipment(
        "distillation_head", 200, 0)
    line = dialog.canvas().connect_glyphs(
        g_a, "neck", g_b, "bottom")
    assert line.zValue() < g_a.zValue()


def test_canvas_connect_glyphs_unknown_equipment_returns_none(
        dialog):
    """If somehow a glyph carries an equipment id that's no
    longer in the catalogue, `connect_glyphs` returns None
    rather than crashing."""
    from orgchem.gui.dialogs.lab_setup_canvas import (
        EquipmentGlyph,
    )
    g_a = dialog.canvas().place_equipment("rbf", 0, 0)
    # Synthesise a glyph with a bogus equipment id.
    g_b = EquipmentGlyph("not-a-real-id", "Phantom")
    g_b.setPos(200, 0)
    dialog.canvas()._scene.addItem(g_b)
    line = dialog.canvas().connect_glyphs(
        g_a, "neck", g_b, "anything")
    assert line is None


def test_clear_canvas_removes_connection_lines(dialog):
    """*Clear canvas* drops every `ConnectionLine` along with
    every glyph."""
    g_a = dialog.canvas().place_equipment("rbf", 0, 0)
    g_b = dialog.canvas().place_equipment(
        "distillation_head", 200, 0)
    dialog.canvas().connect_glyphs(g_a, "neck", g_b, "inlet")
    assert len(dialog.canvas().connection_lines()) == 1
    dialog._on_clear()
    assert dialog.canvas().connection_lines() == []
    assert dialog.canvas().equipment_glyphs() == []
