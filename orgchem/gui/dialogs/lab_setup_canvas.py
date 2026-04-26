"""*Tools → Lab setup canvas…* dialog (Phase 38c + 38d).

Hosts the palette dock + `QGraphicsView` canvas + simulator
playback dock.  Heavy graphics-item classes live in
:mod:`gui.dialogs.lab_canvas_items`; the simulator playback
controls live in :mod:`gui.dialogs.lab_simulation_dock`.
"""
from __future__ import annotations
import logging
from typing import List, Optional

from PySide6.QtCore import QMimeData, Qt, Signal
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import (
    QDialog, QGraphicsScene, QGraphicsView, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSplitter,
    QStatusBar, QToolBar, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget,
)

from orgchem.core.lab_equipment import get_equipment
from orgchem.core.lab_palette import (
    Palette, default_palette, palette_for_setup,
)
from orgchem.gui.dialogs.lab_canvas_items import (
    ConnectionLine, EquipmentGlyph,
)
from orgchem.gui.dialogs.lab_simulation_dock import (
    SimulationDock,
)

log = logging.getLogger(__name__)


#: MIME type carried in the drag payload from palette → canvas.
EQUIPMENT_MIME = "application/x-orgchem-equipment-id"


# ----------------------------------------------------------------
# _PaletteTree — QTreeWidget subclass that emits a drag with the
# equipment id as the MIME payload.
# ----------------------------------------------------------------
class _PaletteTree(QTreeWidget):
    """Drag-source tree for the palette.  Overrides
    :meth:`startDrag` to package the selected equipment id as
    :data:`EQUIPMENT_MIME` so the canvas drop target can
    identify what was dropped."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setIndentation(12)
        self.setDragEnabled(True)

    def startDrag(self, supported_actions: Qt.DropActions
                  ) -> None:   # noqa: N802 (Qt naming)
        item = self.currentItem()
        if item is None:
            return
        eid = item.data(0, Qt.UserRole) or ""
        if not eid:
            return  # category-header click — nothing to drag
        mime = QMimeData()
        mime.setData(EQUIPMENT_MIME, eid.encode("utf-8"))
        # Also set plain text for debugging visibility.
        mime.setText(eid)
        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec(Qt.CopyAction)


# ----------------------------------------------------------------
# PaletteDock — collapsible category-grouped equipment list.
# ----------------------------------------------------------------
class PaletteDock(QWidget):
    """Left-pane palette of draggable equipment grouped by
    category.

    Phase 38c.2 status: shows the full inventory; clicking an
    item highlights it + emits :pyattr:`item_selected` carrying
    the equipment id.  Phase 38c.3 will turn the items into
    drag sources for the canvas.
    """

    item_selected = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._palette: Palette = default_palette()
        self._build_ui()
        self._reload()

    # ---- public API ------------------------------------------
    def set_palette(self, palette: Palette) -> None:
        """Swap the palette (e.g. focusing on one setup's
        equipment via :func:`palette_for_setup`)."""
        self._palette = palette
        self._reload()

    def selected_equipment_id(self) -> Optional[str]:
        item = self._tree.currentItem()
        if item is None:
            return None
        return item.data(0, Qt.UserRole)

    def total_items(self) -> int:
        return len(self._palette)

    # ---- internals -------------------------------------------
    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self._heading = QLabel("Equipment palette")
        self._heading.setStyleSheet("font-weight: bold;")
        layout.addWidget(self._heading)
        # Round 188 — _PaletteTree subclass implements drag start.
        self._tree = _PaletteTree()
        self._tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._tree, 1)

    def _reload(self) -> None:
        self._tree.clear()
        for cat in self._palette.categories:
            cat_item = QTreeWidgetItem([
                f"{cat.label}  ({len(cat)})"
            ])
            # Mark category rows so click-events ignore them.
            cat_item.setData(0, Qt.UserRole, "")
            cat_item.setExpanded(True)
            for eid in cat.equipment_ids:
                eq = get_equipment(eid)
                label = eq.name if eq is not None else eid
                row = QTreeWidgetItem([label])
                row.setData(0, Qt.UserRole, eid)
                cat_item.addChild(row)
            self._tree.addTopLevelItem(cat_item)
        self._heading.setText(
            f"Equipment palette ({len(self._palette)} items)"
        )

    def _on_item_clicked(self, item: QTreeWidgetItem,
                         _column: int) -> None:
        eid = item.data(0, Qt.UserRole)
        if eid:   # ignore category-header clicks
            self.item_selected.emit(eid)


# ----------------------------------------------------------------
# CanvasView — the right-pane QGraphicsView.
# ----------------------------------------------------------------
class CanvasView(QGraphicsView):
    """``QGraphicsView`` backing the lab-setup canvas.

    Round 188 (38c.3) accepts drops from :class:`PaletteDock`
    (MIME type :data:`EQUIPMENT_MIME`) and places an
    :class:`EquipmentGlyph` at the drop position.  Glyphs are
    movable + selectable.  Phase 38c.4 will wire snap-validation
    against Phase-38a connection ports.
    """

    #: Emitted whenever an equipment glyph is placed.
    equipment_placed = Signal(str, float, float)

    #: Emitted whenever two glyphs are connected.  Carries
    #: ``(equipment_a_id, port_a, equipment_b_id, port_b,
    #: error_or_empty)`` — empty error string means valid.
    equipment_connected = Signal(str, str, str, str, str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self._scene.setSceneRect(0, 0, 1200, 800)
        self.setScene(self._scene)
        # White background; future polish round can add grid.
        self.setBackgroundBrush(Qt.white)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setAcceptDrops(True)

    # ---- public helpers --------------------------------------
    def clear_canvas(self) -> None:
        self._scene.clear()

    def item_count(self) -> int:
        return len(self._scene.items())

    def equipment_glyphs(self) -> List[EquipmentGlyph]:
        """Every placed :class:`EquipmentGlyph` in the scene.
        Used by tests + future agent actions to inspect canvas
        state."""
        return [it for it in self._scene.items()
                if isinstance(it, EquipmentGlyph)]

    def connection_lines(self) -> List[ConnectionLine]:
        """Every :class:`ConnectionLine` in the scene."""
        return [it for it in self._scene.items()
                if isinstance(it, ConnectionLine)]

    def connect_glyphs(self, glyph_a: EquipmentGlyph,
                       port_a: str,
                       glyph_b: EquipmentGlyph,
                       port_b: str
                       ) -> Optional[ConnectionLine]:
        """Phase 38c.4 — draw a connection between two placed
        glyphs at the named ports.  Validates the port pair via
        :func:`core.lab_setups.validate_port_pair`; the resulting
        :class:`ConnectionLine` renders in solid green when valid
        + dashed red when invalid (so a port mismatch is
        immediately visible).  Returns the line, or ``None`` if
        either equipment id is unresolvable."""
        from orgchem.core.lab_equipment import get_equipment
        from orgchem.core.lab_setups import validate_port_pair
        eq_a = get_equipment(glyph_a.equipment_id())
        eq_b = get_equipment(glyph_b.equipment_id())
        if eq_a is None or eq_b is None:
            return None
        if glyph_a is glyph_b:
            error: Optional[str] = ("self-loop: cannot connect "
                                    "a glyph to itself")
        else:
            error = validate_port_pair(
                eq_a, port_a, eq_b, port_b)
        line = ConnectionLine(
            glyph_a, port_a, glyph_b, port_b, error)
        self._scene.addItem(line)
        self.equipment_connected.emit(
            glyph_a.equipment_id(), port_a,
            glyph_b.equipment_id(), port_b,
            error or "",
        )
        return line

    def place_equipment(self, equipment_id: str,
                        x: float, y: float
                        ) -> Optional[EquipmentGlyph]:
        """Place an :class:`EquipmentGlyph` at ``(x, y)`` in
        scene coordinates.  Used both by the drop handler and
        directly by tests / agent actions (no real drag needed).
        Returns the placed glyph, or ``None`` if the equipment
        id is unknown."""
        from orgchem.core.lab_equipment import get_equipment
        eq = get_equipment(equipment_id)
        if eq is None:
            return None
        glyph = EquipmentGlyph(equipment_id, eq.name)
        glyph.setPos(x, y)
        self._scene.addItem(glyph)
        self.equipment_placed.emit(equipment_id, x, y)
        return glyph

    # ---- drag/drop event handlers ----------------------------
    def dragEnterEvent(self, event) -> None:   # noqa: N802
        if event.mimeData().hasFormat(EQUIPMENT_MIME):
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event) -> None:   # noqa: N802
        if event.mimeData().hasFormat(EQUIPMENT_MIME):
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event) -> None:   # noqa: N802
        if not event.mimeData().hasFormat(EQUIPMENT_MIME):
            super().dropEvent(event)
            return
        eid = bytes(
            event.mimeData().data(EQUIPMENT_MIME)).decode("utf-8")
        # Map the view-coordinate drop position to scene coords.
        scene_pos = self.mapToScene(event.position().toPoint())
        self.place_equipment(eid, scene_pos.x(), scene_pos.y())
        event.acceptProposedAction()


# ----------------------------------------------------------------
# Dialog
# ----------------------------------------------------------------
class LabSetupCanvasDialog(QDialog):
    """Modeless singleton dialog hosting the Phase-38c canvas
    + equipment palette.

    Round-187 (38c.2) status: UI skeleton only — palette
    populates from :func:`default_palette()`, canvas is empty.
    The *Load setup* button accepts a Phase-38b setup id and
    swaps the palette to that setup's equipment list (no
    canvas rendering yet).
    """

    _instance: Optional["LabSetupCanvasDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None
                  ) -> "LabSetupCanvasDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Lab setup canvas")
        self.setModal(False)
        self.resize(1280, 760)
        self._build_ui()

    # ---- UI ---------------------------------------------------
    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(4, 4, 4, 4)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self._clear_btn = QPushButton("Clear canvas")
        self._clear_btn.clicked.connect(self._on_clear)
        toolbar.addWidget(self._clear_btn)
        toolbar.addSeparator()
        self._all_btn = QPushButton("Show all equipment")
        self._all_btn.clicked.connect(self._on_show_all)
        toolbar.addWidget(self._all_btn)
        toolbar.addSeparator()
        # Phase 38d.2 — Run simulation button.
        self._run_sim_btn = QPushButton("▶ Run simulation")
        self._run_sim_btn.clicked.connect(self._on_run_simulation)
        toolbar.addWidget(self._run_sim_btn)
        outer.addWidget(toolbar)

        splitter = QSplitter(Qt.Horizontal)
        self._palette_dock = PaletteDock()
        self._palette_dock.item_selected.connect(
            self._on_item_selected)
        splitter.addWidget(self._palette_dock)
        self._canvas = CanvasView()
        self._canvas.equipment_placed.connect(
            self._on_equipment_placed)
        self._canvas.equipment_connected.connect(
            self._on_equipment_connected)
        splitter.addWidget(self._canvas)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([260, 1020])
        outer.addWidget(splitter, 1)

        # Phase 38d.2 — simulator dock at the bottom (initially
        # empty / disabled until *Run simulation* is clicked).
        self._sim_dock = SimulationDock()
        self._sim_dock.setMaximumHeight(220)
        outer.addWidget(self._sim_dock)

        self._status = QStatusBar()
        self._status.showMessage(
            "Drag equipment from the palette onto the canvas")
        outer.addWidget(self._status)

        # Phase 38d.2 — track the most-recently-loaded setup so
        # *Run simulation* knows which script to start.
        self._loaded_setup_id: str = ""

    # ---- API used by future sub-phases + tests ---------------
    def palette_dock(self) -> PaletteDock:
        return self._palette_dock

    def canvas(self) -> CanvasView:
        return self._canvas

    def load_setup(self, setup_id: str) -> bool:
        """Swap the palette to the equipment from a Phase-38b
        setup.  Returns ``True`` on success, ``False`` for
        unknown setup id."""
        palette = palette_for_setup(setup_id)
        if palette is None:
            return False
        self._palette_dock.set_palette(palette)
        self._loaded_setup_id = setup_id
        self._status.showMessage(
            f"Loaded setup {setup_id!r} — "
            f"{len(palette)} equipment items")
        return True

    def simulation_dock(self) -> SimulationDock:
        """Phase 38d.2 — the simulation playback dock at the
        bottom of the dialog."""
        return self._sim_dock

    def _on_run_simulation(self) -> None:
        """Phase 38d.2 — *Run simulation* toolbar button.  Loads
        the simulator script for the currently-loaded setup
        into the bottom dock + auto-plays it."""
        from orgchem.core.process_simulator import (
            simulator_for_setup,
        )
        sid = self._loaded_setup_id
        if not sid:
            self._status.showMessage(
                "Load a setup first (Build on canvas, or "
                "open with a setup_id) — no simulator without "
                "a setup")
            return
        sim = simulator_for_setup(sid)
        if sim is None:
            self._status.showMessage(
                f"No simulator script for setup {sid!r} yet "
                f"(38d.4 adds the remaining 3 setups)")
            self._sim_dock.set_simulator(None)
            return
        self._sim_dock.set_simulator(sim)
        self._sim_dock.play()
        self._status.showMessage(
            f"Running {sid!r}: {sim.total_stages} stages")

    def populate_from_setup(self, setup_id: str) -> bool:
        """Phase 38c.5 — pre-populate the canvas with a seeded
        Phase-38b setup's equipment + connections.  Lays
        equipment out in a horizontal row + draws each
        connection.  Returns ``True`` on success.

        Powers the *Build on canvas* button on the *Lab setups…*
        dialog + the `open_lab_setup_canvas(setup_id=...)`
        agent action.
        """
        from orgchem.core.lab_setups import get_setup
        setup = get_setup(setup_id)
        if setup is None:
            return False
        # Also swap the palette to the per-setup view so the
        # user only sees the relevant items.
        self.load_setup(setup_id)
        # Clear any prior canvas state.
        self._canvas.clear_canvas()
        # Place each equipment in a horizontal row.  Coordinates
        # are illustrative; future polish round can auto-layout.
        glyphs: list = []
        spacing_x = 180
        base_x = 120
        base_y = 280
        for i, eid in enumerate(setup.equipment):
            g = self._canvas.place_equipment(
                eid, base_x + i * spacing_x, base_y)
            glyphs.append(g)
        # Draw each connection between the resolved glyphs.
        for conn in setup.connections:
            ai, bi = conn.from_equipment_idx, conn.to_equipment_idx
            if (0 <= ai < len(glyphs) and 0 <= bi < len(glyphs)
                    and glyphs[ai] is not None
                    and glyphs[bi] is not None):
                self._canvas.connect_glyphs(
                    glyphs[ai], conn.from_port,
                    glyphs[bi], conn.to_port,
                )
        self._status.showMessage(
            f"Built setup {setup.name!r}: "
            f"{len(setup.equipment)} items, "
            f"{len(setup.connections)} connections")
        return True

    # ---- slots ------------------------------------------------
    def _on_clear(self) -> None:
        self._canvas.clear_canvas()
        self._status.showMessage("Canvas cleared")

    def _on_show_all(self) -> None:
        self._palette_dock.set_palette(default_palette())
        self._status.showMessage(
            f"Showing full palette "
            f"({self._palette_dock.total_items()} items)")

    def _on_item_selected(self, eid: str) -> None:
        eq = get_equipment(eid)
        if eq is None:
            return
        self._status.showMessage(
            f"Selected: {eq.name} ({eid}) — drag onto canvas")

    def _on_equipment_placed(self, eid: str,
                             x: float, y: float) -> None:
        eq = get_equipment(eid)
        name = eq.name if eq is not None else eid
        self._status.showMessage(
            f"Placed {name} at ({int(x)}, {int(y)}) — "
            f"{self._canvas.item_count()} items on canvas")

    def _on_equipment_connected(self, eid_a: str, port_a: str,
                                eid_b: str, port_b: str,
                                error: str) -> None:
        if error:
            self._status.showMessage(
                f"⚠ Port mismatch ({eid_a}.{port_a} → "
                f"{eid_b}.{port_b}): {error}"
            )
        else:
            self._status.showMessage(
                f"✓ Connected {eid_a}.{port_a} → "
                f"{eid_b}.{port_b}"
            )
