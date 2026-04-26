"""Phase 36b / 36c / 36d — `QGraphicsScene` drawing canvas.

Backs the molecular drawing tool the user flagged in Phase 36.
Keeps a live :class:`orgchem.core.drawing.Structure` mirror of
the on-screen atoms + bonds so SMILES round-trip is a single
call away.

Tool modes:

- ``"select"`` — pointer: click an atom to move it (drag), click
  empty canvas to clear the selection.
- ``"atom-<element>"`` — atom-placement tool (C / N / O / P / S /
  F / Cl / Br / I by default); click empty canvas to place,
  click an existing atom to change its element.
- ``"bond"`` — click one atom then another to connect them with a
  single bond (or cycle through single → double → triple by
  clicking an existing bond).
- ``"erase"`` — click an atom to delete it (and its bonds).
- ``"template-<name>"`` *(round 129, Phase 36c)* — ring or FG
  template; click empty canvas to place free-standing, click an
  existing atom to fuse the template anchor with it.  Catalogue
  lives in :mod:`orgchem.core.drawing_templates`.

Round 128 adds **snapshot-based undo / redo** (Phase 36d) — every
logical mutation (atom place / element swap / bond draw / bond
order cycle / erase / drag-move / clear / SMILES-rebuild / template
placement) pushes a `(Structure, positions)` snapshot onto an undo
stack; Ctrl+Z (Undo) / Ctrl+Shift+Z (Redo) buttons walk it.  Stack
depth is capped at 100.

Phase 36e will add stereochemistry (wedge / dash); 36f will add
reaction arrows.
"""
from __future__ import annotations
import copy
import logging
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Qt, Signal, QPointF, QRectF
from PySide6.QtGui import (
    QBrush, QColor, QFont, QKeySequence, QPainter, QPen, QMouseEvent,
    QPolygonF, QShortcut,
)
from PySide6.QtWidgets import (
    QGraphicsEllipseItem, QGraphicsItem, QGraphicsItemGroup,
    QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsScene,
    QGraphicsSimpleTextItem, QGraphicsView,
    QHBoxLayout, QInputDialog, QLabel, QLineEdit, QMenu,
    QPushButton, QSizePolicy, QToolButton, QVBoxLayout, QWidget,
)
from PySide6.QtGui import QAction

from orgchem.core.drawing import (
    Atom, Bond, Structure,
    structure_from_smiles, structure_to_smiles,
)
from orgchem.core.drawing_scheme import Scheme
from orgchem.core.drawing_templates import (
    apply_template, get_template, list_templates,
)

log = logging.getLogger(__name__)


#: Screen distance between two bonded atoms (pixels).  Also the
#: snap distance used by `_hit_atom` + `_hit_bond`.
_BOND_PX = 42.0
_ATOM_RADIUS_PX = 12.0
_HIT_RADIUS_PX = 16.0
_BOND_HIT_TOL_PX = 6.0

#: Max snapshots kept on either undo or redo stack.  100 is
#: more than any teaching molecule will ever need and keeps
#: memory trivial (each snapshot is a few hundred bytes).
_UNDO_STACK_MAX = 100


#: Simple CPK-ish colour scheme for heteroatom labels.
_ATOM_COLOUR = {
    "C":  QColor("#222222"),
    "N":  QColor("#2060B0"),
    "O":  QColor("#C02020"),
    "S":  QColor("#C8A000"),
    "P":  QColor("#C08030"),
    "F":  QColor("#40A040"),
    "Cl": QColor("#40A040"),
    "Br": QColor("#8E3030"),
    "I":  QColor("#6030A0"),
    "H":  QColor("#505050"),
}


class DrawingPanel(QWidget):
    """Canvas + toolbar widget.  Pure QGraphics; no RDKit import
    at the module level — all SMILES round-trips route through
    `orgchem.core.drawing` (Phase 36a)."""

    #: Emitted whenever the canvas mutates (atom added / bond
    #: drawn / item deleted).  Carriers the current SMILES (or
    #: empty string when the canvas is empty / invalid).
    structure_changed = Signal(str)

    ELEMENT_TOOLS = ("C", "N", "O", "P", "S",
                     "F", "Cl", "Br", "I", "H")

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._structure = Structure()
        # Parallel list of scene items mirrored against
        # `_structure.atoms` / `_structure.bonds`.  Index i in
        # `_atom_items` is the QGraphicsItem for structure atom i.
        self._atom_items: List[Dict] = []   # each: {"dot", "label", "pos"}
        self._bond_items: List[QGraphicsLineItem] = []
        self._tool: str = "atom-C"
        self._bond_first_atom: Optional[int] = None   # mid-draw state
        self._drag_atom_idx: Optional[int] = None
        # Phase 36d undo/redo: stacks of (Structure, positions, arrow) tuples.
        # Invariant: the *current* canvas state is NOT on either stack.
        # Phase 36f.2 (round 132): snapshot tuple grew a third slot for the
        # optional reaction arrow ((x, y, kind) or None).
        self._undo_stack: List[Tuple[Structure, List[Tuple[float, float]],
                                     Optional[Tuple[float, float, str]]]] = []
        self._redo_stack: List[Tuple[Structure, List[Tuple[float, float]],
                                     Optional[Tuple[float, float, str]]]] = []
        # Phase 36f.2: at most one arrow on the canvas; (x, y, "forward"
        # | "reversible").  ``None`` means no arrow placed.
        self._arrow: Optional[Tuple[float, float, str]] = None
        self._arrow_items: List = []   # QGraphicsItems backing the arrow
        self._build_ui()

    # ---- UI construction ------------------------------------

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(3)

        # Top toolbar — tool buttons + "Clear" + SMILES I/O ribbon.
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        self._tool_buttons: Dict[str, QToolButton] = {}
        for label, key in [
            ("⟲ Select", "select"),
            ("C", "atom-C"), ("N", "atom-N"), ("O", "atom-O"),
            ("P", "atom-P"), ("S", "atom-S"),
            ("F", "atom-F"), ("Cl", "atom-Cl"),
            ("Br", "atom-Br"), ("I", "atom-I"),
            ("— bond", "bond"),
            ("◣ wedge", "bond-wedge"),
            ("◌ dash", "bond-dash"),
            ("→ arrow", "arrow-forward"),
            ("⇌ rev.arrow", "arrow-reversible"),
            ("✕ erase", "erase"),
        ]:
            btn = QToolButton()
            btn.setText(label)
            btn.setCheckable(True)
            btn.clicked.connect(
                lambda _chk=False, k=key: self.set_tool(k))
            toolbar.addWidget(btn)
            self._tool_buttons[key] = btn
        toolbar.addSpacing(12)
        self._undo_btn = QPushButton("↶ Undo")
        self._undo_btn.setToolTip("Undo last change (Ctrl+Z)")
        self._undo_btn.setEnabled(False)
        self._undo_btn.clicked.connect(self.undo)
        toolbar.addWidget(self._undo_btn)
        self._redo_btn = QPushButton("↷ Redo")
        self._redo_btn.setToolTip("Redo (Ctrl+Shift+Z)")
        self._redo_btn.setEnabled(False)
        self._redo_btn.clicked.connect(self.redo)
        toolbar.addWidget(self._redo_btn)
        toolbar.addSpacing(12)
        self._clear_btn = QPushButton("Clear canvas")
        self._clear_btn.clicked.connect(self.clear)
        toolbar.addWidget(self._clear_btn)
        toolbar.addStretch(1)
        lay.addLayout(toolbar)

        # Template palette — second row.  Phase 36c (round 129).
        tpl_row = QHBoxLayout()
        tpl_row.setContentsMargins(0, 0, 0, 0)
        tpl_row.addWidget(QLabel("Templates:"))
        for tpl in list_templates(kind="ring"):
            btn = QToolButton()
            btn.setText(tpl.label)
            btn.setToolTip(f"Insert {tpl.name} ring "
                           "(click empty canvas to place; click an "
                           "atom to fuse).")
            btn.setCheckable(True)
            tool_key = f"template-{tpl.name}"
            btn.clicked.connect(
                lambda _chk=False, k=tool_key: self.set_tool(k))
            tpl_row.addWidget(btn)
            self._tool_buttons[tool_key] = btn
        tpl_row.addSpacing(8)
        for tpl in list_templates(kind="fg"):
            btn = QToolButton()
            btn.setText(tpl.label)
            btn.setToolTip(f"Insert {tpl.name.upper()} group "
                           "(click an atom to attach; click empty "
                           "canvas to place on a fresh carbon).")
            btn.setCheckable(True)
            tool_key = f"template-{tpl.name}"
            btn.clicked.connect(
                lambda _chk=False, k=tool_key: self.set_tool(k))
            tpl_row.addWidget(btn)
            self._tool_buttons[tool_key] = btn
        tpl_row.addStretch(1)
        lay.addLayout(tpl_row)

        # Keyboard shortcuts — scoped to this widget so they fire
        # even when the Drawing dialog isn't the top-level window.
        undo_sc = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo_sc.activated.connect(self.undo)
        redo_sc = QShortcut(QKeySequence("Ctrl+Shift+Z"), self)
        redo_sc.activated.connect(self.redo)

        # SMILES ribbon — paste / display current SMILES.
        smiles_row = QHBoxLayout()
        smiles_row.setContentsMargins(0, 0, 0, 0)
        smiles_row.addWidget(QLabel("SMILES:"))
        self._smiles_edit = QLineEdit()
        self._smiles_edit.setPlaceholderText(
            "Paste a SMILES + press Enter to rebuild canvas; "
            "or draw here and watch it populate.")
        self._smiles_edit.returnPressed.connect(self._on_smiles_entered)
        smiles_row.addWidget(self._smiles_edit, 1)
        lay.addLayout(smiles_row)

        # Canvas.
        self._scene = QGraphicsScene()
        self._scene.setSceneRect(QRectF(-300, -220, 600, 440))
        self._view = _DrawingView(self)
        self._view.setScene(self._scene)
        self._view.setRenderHint(QPainter.Antialiasing, True)
        self._view.setMinimumSize(360, 300)
        self._view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lay.addWidget(self._view, 1)

        # Default tool = place-carbon.
        self.set_tool("atom-C")

    # ---- public API ----------------------------------------

    def current_smiles(self) -> str:
        """Return the canonical SMILES for the current canvas.
        Empty string if the canvas is empty or invalid."""
        s = self.get_structure()
        if s.is_empty:
            return ""
        smi = structure_to_smiles(s)
        return smi or ""

    def get_structure(self) -> Structure:
        """Return the live :class:`Structure` mirror.  Callers
        shouldn't mutate this directly; use the widget's
        tool-API methods instead."""
        return self._structure

    def set_structure_from_smiles(self, smi: str) -> bool:
        """Replace the canvas with the SMILES-rebuilt structure.
        Returns ``True`` on success, ``False`` if RDKit couldn't
        parse the input."""
        s = structure_from_smiles(smi)
        if s is None:
            return False
        self._load_structure(s)
        return True

    def clear(self, *, record_undo: bool = True) -> None:
        """Drop every atom + bond + the reaction arrow.  Emits
        `structure_changed("")`.

        ``record_undo=False`` bypasses the Phase-36d snapshot —
        used internally by `_load_structure` + `_restore_snapshot`
        where the outer call already manages the stack."""
        if record_undo and (
                not self._structure.is_empty or self._arrow is not None):
            self._push_undo()
        self._structure = Structure()
        for items in self._atom_items:
            for it in items.values():
                if it is not None and hasattr(it, "scene") and it.scene():
                    self._scene.removeItem(it)
        for b in self._bond_items:
            if b.scene():
                self._scene.removeItem(b)
        self._atom_items.clear()
        self._bond_items.clear()
        self._remove_arrow_items()
        self._arrow = None
        self._bond_first_atom = None
        self._drag_atom_idx = None
        self._smiles_edit.setText("")
        self.structure_changed.emit("")
        if record_undo:
            self._update_undo_buttons()

    def set_tool(self, tool: str) -> None:
        """Switch the active tool.  Updates toolbar-button
        highlighting."""
        self._tool = tool
        for k, b in self._tool_buttons.items():
            b.setChecked(k == tool)
        self._bond_first_atom = None

    def tool(self) -> str:
        return self._tool

    # ---- undo / redo (Phase 36d) ----------------------------

    def _snapshot(self) -> Tuple[
            Structure,
            List[Tuple[float, float]],
            Optional[Tuple[float, float, str]]]:
        """Capture a deep-copied snapshot of the current canvas —
        structure + per-atom screen positions + arrow state.
        Phase 36f.2 added the arrow slot."""
        struct = copy.deepcopy(self._structure)
        positions = [tuple(items.get("pos", (0.0, 0.0)))
                     for items in self._atom_items]
        arrow = self._arrow
        return struct, positions, arrow

    def _push_undo(self) -> None:
        """Push the current state onto the undo stack.  Clears
        the redo stack — any outstanding redo history is
        invalidated by a fresh mutation.  Bounded by
        :data:`_UNDO_STACK_MAX`."""
        self._undo_stack.append(self._snapshot())
        if len(self._undo_stack) > _UNDO_STACK_MAX:
            # Drop oldest; caps memory even if the user
            # mashes buttons.
            del self._undo_stack[0]
        self._redo_stack.clear()
        self._update_undo_buttons()

    def _restore_snapshot(self, snap: Tuple) -> None:
        """Wipe + rebuild the scene from a snapshot.  Does NOT
        push anything onto the undo stack — caller handles that.

        Accepts both 2-tuple (legacy, pre-Phase-36f.2) and
        3-tuple snapshots so an in-flight session that started
        before round 132 doesn't crash on its first undo."""
        if len(snap) == 3:
            struct, positions, arrow = snap
        else:
            struct, positions = snap
            arrow = None
        # Remove existing scene items.
        for items in self._atom_items:
            for it in items.values():
                if it is not None and hasattr(it, "scene") and it.scene():
                    self._scene.removeItem(it)
        for b in self._bond_items:
            if b.scene():
                self._scene.removeItem(b)
        self._remove_arrow_items()
        self._atom_items.clear()
        self._bond_items.clear()
        self._bond_first_atom = None
        self._drag_atom_idx = None
        self._structure = copy.deepcopy(struct)
        # Redraw everything.
        for i, atom in enumerate(self._structure.atoms):
            pos = positions[i] if i < len(positions) else (40.0 * i, 0.0)
            self._atom_items.append({"pos": (pos[0], pos[1])})
            self._draw_atom(i, QPointF(pos[0], pos[1]))
        for i in range(len(self._structure.bonds)):
            self._draw_bond(i)
        # Restore arrow.
        self._arrow = arrow
        if self._arrow is not None:
            self._render_arrow()
        # Emit changed without pushing a fresh snapshot.
        smi = self.current_smiles()
        self._smiles_edit.blockSignals(True)
        self._smiles_edit.setText(smi)
        self._smiles_edit.blockSignals(False)
        self.structure_changed.emit(smi)

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def undo(self) -> None:
        """Pop the most recent snapshot off the undo stack,
        push the current state onto the redo stack, and restore
        the popped snapshot."""
        if not self._undo_stack:
            return
        current = self._snapshot()
        snap = self._undo_stack.pop()
        self._redo_stack.append(current)
        if len(self._redo_stack) > _UNDO_STACK_MAX:
            del self._redo_stack[0]
        self._restore_snapshot(snap)
        self._update_undo_buttons()

    def redo(self) -> None:
        """Mirror of :meth:`undo`."""
        if not self._redo_stack:
            return
        current = self._snapshot()
        snap = self._redo_stack.pop()
        self._undo_stack.append(current)
        if len(self._undo_stack) > _UNDO_STACK_MAX:
            del self._undo_stack[0]
        self._restore_snapshot(snap)
        self._update_undo_buttons()

    def _update_undo_buttons(self) -> None:
        self._undo_btn.setEnabled(self.can_undo())
        self._redo_btn.setEnabled(self.can_redo())

    # ---- mouse dispatch (called by the _DrawingView) ----------

    def handle_canvas_press(self, scene_pos: QPointF) -> None:
        atom_idx = self._hit_atom(scene_pos)
        tool = self._tool
        if tool == "erase":
            if atom_idx is not None:
                self._delete_atom(atom_idx)
            else:
                bond_idx = self._hit_bond(scene_pos)
                if bond_idx is not None:
                    self._delete_bond(bond_idx)
            return
        if tool == "select":
            if atom_idx is not None:
                # Snapshot on drag-start so a full drag is one
                # logical undo step, not one per mouseMove.
                self._push_undo()
            self._drag_atom_idx = atom_idx
            return
        if tool == "bond":
            self._handle_bond_click(atom_idx, scene_pos)
            return
        if tool == "bond-wedge":
            self._handle_stereo_bond_click(atom_idx, scene_pos, "wedge")
            return
        if tool == "bond-dash":
            self._handle_stereo_bond_click(atom_idx, scene_pos, "dash")
            return
        if tool == "arrow-forward":
            self._place_arrow(scene_pos, "forward")
            return
        if tool == "arrow-reversible":
            self._place_arrow(scene_pos, "reversible")
            return
        if tool.startswith("template-"):
            name = tool.split("-", 1)[1]
            self._apply_template_at(name, scene_pos, atom_idx)
            return
        # atom-<element> tool.
        if tool.startswith("atom-"):
            element = tool.split("-", 1)[1]
            if atom_idx is None:
                self._add_atom(element, scene_pos)
            else:
                self._change_atom_element(atom_idx, element)
            return

    def handle_canvas_move(self, scene_pos: QPointF) -> None:
        if self._tool != "select" or self._drag_atom_idx is None:
            return
        self._move_atom(self._drag_atom_idx, scene_pos)

    def handle_canvas_release(self, scene_pos: QPointF) -> None:
        self._drag_atom_idx = None

    # ---- tool implementations -------------------------------

    def _add_atom(self, element: str, scene_pos: QPointF,
                  *, record_undo: bool = True) -> int:
        if record_undo:
            self._push_undo()
        idx = self._structure.add_atom(element)
        self._atom_items.append({"pos": (scene_pos.x(), scene_pos.y())})
        self._draw_atom(idx, scene_pos)
        self._emit_changed()
        return idx

    def _change_atom_element(self, idx: int, element: str) -> None:
        if idx < 0 or idx >= len(self._structure.atoms):
            return
        # Skip if the element isn't actually changing — saves a
        # pointless undo snapshot when the user re-clicks with the
        # same tool.
        if self._structure.atoms[idx].element == element:
            return
        self._push_undo()
        self._structure.atoms[idx].element = element
        # Reset valence-dependent flags that the new element may
        # invalidate (aromatic N vs neutral C, etc.).
        self._structure.atoms[idx].aromatic = False
        self._structure.atoms[idx].charge = 0
        self._structure.atoms[idx].h_count = -1
        self._refresh_atom_glyph(idx)
        self._emit_changed()

    def _move_atom(self, idx: int, scene_pos: QPointF) -> None:
        items = self._atom_items[idx]
        items["pos"] = (scene_pos.x(), scene_pos.y())
        if "dot" in items:
            r = _ATOM_RADIUS_PX
            items["dot"].setRect(scene_pos.x() - r, scene_pos.y() - r,
                                 2 * r, 2 * r)
        if "label" in items and items["label"] is not None:
            br = items["label"].boundingRect()
            items["label"].setPos(scene_pos.x() - br.width() / 2,
                                  scene_pos.y() - br.height() / 2)
        # Redraw any bond that touches this atom.
        for b_idx, bond in enumerate(self._structure.bonds):
            if bond.begin_idx == idx or bond.end_idx == idx:
                self._refresh_bond(b_idx)

    def _delete_atom(self, idx: int,
                     *, record_undo: bool = True) -> None:
        if record_undo:
            self._push_undo()
        # Remove every bond that touches the atom first.
        bonds_to_drop = [i for i, b in enumerate(self._structure.bonds)
                         if b.begin_idx == idx or b.end_idx == idx]
        for b_idx in reversed(bonds_to_drop):
            # Nested delete is part of the same logical mutation;
            # don't push a second undo snapshot.
            self._delete_bond(b_idx, record_undo=False)
        # Remove the atom itself.
        items = self._atom_items.pop(idx)
        for it in items.values():
            if it is not None and hasattr(it, "scene") and it.scene():
                self._scene.removeItem(it)
        del self._structure.atoms[idx]
        # Re-index every bond that pointed past the deleted atom.
        for bond in self._structure.bonds:
            if bond.begin_idx > idx:
                bond.begin_idx -= 1
            if bond.end_idx > idx:
                bond.end_idx -= 1
        self._emit_changed()

    def _delete_bond(self, idx: int,
                     *, record_undo: bool = True) -> None:
        if record_undo:
            self._push_undo()
        item = self._bond_items.pop(idx)
        if item.scene():
            self._scene.removeItem(item)
        del self._structure.bonds[idx]
        self._emit_changed()

    def _handle_bond_click(self, atom_idx: Optional[int],
                           scene_pos: QPointF) -> None:
        # First click: remember the source atom (place one if the
        # user clicked empty canvas, as ChemDraw does).  The
        # first-click placement IS a mutation in its own right,
        # so let `_add_atom` push its own snapshot.
        if self._bond_first_atom is None:
            if atom_idx is None:
                atom_idx = self._add_atom("C", scene_pos)
            self._bond_first_atom = atom_idx
            return
        # Second click: complete the bond.  Push one snapshot
        # for the whole logical mutation (possible auto-place +
        # bond create / order cycle).
        self._push_undo()
        if atom_idx is None:
            atom_idx = self._add_atom("C", scene_pos, record_undo=False)
        if atom_idx == self._bond_first_atom:
            # Clicked the same atom twice — treat as cancel.
            # Drop the snapshot we just pushed so cancel doesn't
            # pollute undo history.
            self._undo_stack.pop()
            self._update_undo_buttons()
            self._bond_first_atom = None
            return
        existing = self._bond_between(self._bond_first_atom, atom_idx)
        if existing is not None:
            # Cycle order: 1 → 2 → 3 → 1.
            cur = self._structure.bonds[existing].order
            new_order = 1 if cur >= 3 else cur + 1
            self._structure.bonds[existing].order = new_order
            self._refresh_bond(existing)
        else:
            self._structure.add_bond(self._bond_first_atom, atom_idx, order=1)
            self._draw_bond(len(self._structure.bonds) - 1)
        self._bond_first_atom = None
        self._emit_changed()

    def _apply_template_at(self, name: str, scene_pos: QPointF,
                           host_atom_idx: Optional[int]) -> None:
        """Phase 36c — fold a ring or FG template into the canvas.

        Pushes one undo snapshot, then delegates the geometric
        merge to :func:`orgchem.core.drawing_templates.apply_template`
        so the headless core stays the source of truth for layout
        + bond bookkeeping.  Adds scene items only for the *new*
        atoms / bonds appended to the structure.
        """
        tpl = get_template(name)
        if tpl is None:
            log.warning("Unknown template: %r", name)
            return
        self._push_undo()
        old_n_atoms = self._structure.n_atoms
        old_n_bonds = self._structure.n_bonds
        positions = [items.get("pos", (0.0, 0.0))
                     for items in self._atom_items]
        new_struct, new_positions = apply_template(
            self._structure,
            positions,
            tpl,
            anchor_pos=(scene_pos.x(), scene_pos.y()),
            host_atom_idx=host_atom_idx,
            scale=_BOND_PX,
        )
        # No-op guard: if nothing was added, drop the snapshot we
        # just pushed so cancel doesn't pollute undo history.
        if (new_struct.n_atoms == old_n_atoms
                and new_struct.n_bonds == old_n_bonds):
            self._undo_stack.pop()
            self._update_undo_buttons()
            return
        self._structure = new_struct
        # Render every newly appended atom + bond.  Existing atoms
        # / bonds keep their scene items unchanged so the overlap
        # of fused-ring anchors stays seamless.
        for i in range(old_n_atoms, len(new_struct.atoms)):
            x, y = new_positions[i]
            self._atom_items.append({"pos": (x, y)})
            self._draw_atom(i, QPointF(x, y))
        for i in range(old_n_bonds, len(new_struct.bonds)):
            self._draw_bond(i)
        self._emit_changed()

    def _handle_stereo_bond_click(
            self, atom_idx: Optional[int], scene_pos: QPointF,
            stereo: str) -> None:
        """Phase 36e — wedge / dash bond placement.

        Mirrors :meth:`_handle_bond_click` but every new bond
        gets ``order=1`` + the requested ``stereo`` (``"wedge"``
        or ``"dash"``).  Clicking an existing bond TOGGLES the
        stereo: same stereo → ``"none"``; any other → switch to
        the requested stereo.  Empty-canvas auto-place behaviour
        matches the plain bond tool — clicking empty canvas as
        the first / second click of a wedge bond places a fresh
        carbon.
        """
        if self._bond_first_atom is None:
            if atom_idx is None:
                atom_idx = self._add_atom("C", scene_pos)
            self._bond_first_atom = atom_idx
            return
        self._push_undo()
        if atom_idx is None:
            atom_idx = self._add_atom(
                "C", scene_pos, record_undo=False)
        if atom_idx == self._bond_first_atom:
            self._undo_stack.pop()
            self._update_undo_buttons()
            self._bond_first_atom = None
            return
        existing = self._bond_between(self._bond_first_atom, atom_idx)
        if existing is not None:
            bond = self._structure.bonds[existing]
            if bond.stereo == stereo:
                bond.stereo = "none"
            else:
                bond.stereo = stereo
                bond.order = 1
            self._refresh_bond(existing)
        else:
            self._structure.add_bond(
                self._bond_first_atom, atom_idx,
                order=1, stereo=stereo)
            self._draw_bond(len(self._structure.bonds) - 1)
        self._bond_first_atom = None
        self._emit_changed()

    def _bond_between(self, a: int, b: int) -> Optional[int]:
        for i, bond in enumerate(self._structure.bonds):
            if {bond.begin_idx, bond.end_idx} == {a, b}:
                return i
        return None

    # ---- reaction arrow (Phase 36f.2) -----------------------

    #: Pixel half-width of the rendered arrow shaft.
    _ARROW_HALF_WIDTH_PX = 50.0

    def _place_arrow(self, scene_pos: QPointF, kind: str) -> None:
        """Drop a reaction arrow at the click point, replacing
        any existing arrow (only one arrow per canvas).

        Pushes one undo snapshot per placement so the round-128
        stack picks the change up.  Re-clicking with the same
        kind at exactly the same point is a no-op (would still
        push a snapshot otherwise).
        """
        if kind not in ("forward", "reversible"):
            return
        new_state = (scene_pos.x(), scene_pos.y(), kind)
        if self._arrow == new_state:
            return
        self._push_undo()
        self._set_arrow(new_state)
        self._emit_changed()

    def _set_arrow(self,
                   state: Optional[Tuple[float, float, str]]) -> None:
        """Replace the current arrow without pushing an undo
        snapshot — used by `_restore_snapshot` and the public
        `_place_arrow` (which manages the snapshot itself)."""
        self._remove_arrow_items()
        self._arrow = state
        if state is not None:
            self._render_arrow()

    def _remove_arrow_items(self) -> None:
        for it in self._arrow_items:
            if it is not None and hasattr(it, "scene") and it.scene():
                self._scene.removeItem(it)
        self._arrow_items.clear()

    def _render_arrow(self) -> None:
        """Draw the arrow shaft + head(s) at `self._arrow`.

        Forward arrow = single rightward arrowhead; reversible =
        ``⇌`` style with two stacked half-arrows (one rightward
        on top, one leftward on bottom).  Pen is a muted
        slate-grey so the arrow doesn't fight the molecule
        glyphs for attention.
        """
        if self._arrow is None:
            return
        ax, ay, kind = self._arrow
        w = self._ARROW_HALF_WIDTH_PX
        head_len = 12.0
        head_off = 5.0
        pen = QPen(QColor("#444"))
        pen.setWidthF(2.0)
        pen.setCapStyle(Qt.RoundCap)
        if kind == "forward":
            shaft = QGraphicsLineItem(ax - w, ay, ax + w, ay)
            shaft.setPen(pen)
            shaft.setZValue(-2)
            self._scene.addItem(shaft)
            self._arrow_items.append(shaft)
            head = QPolygonF([
                QPointF(ax + w, ay),
                QPointF(ax + w - head_len, ay - head_off),
                QPointF(ax + w - head_len, ay + head_off),
            ])
            head_item = QGraphicsPolygonItem(head)
            head_item.setBrush(QBrush(QColor("#444")))
            head_item.setPen(pen)
            head_item.setZValue(-2)
            self._scene.addItem(head_item)
            self._arrow_items.append(head_item)
        else:  # reversible
            offset = 4.0
            # Top shaft + right-pointing arrowhead.
            top = QGraphicsLineItem(
                ax - w, ay - offset, ax + w, ay - offset)
            top.setPen(pen)
            top.setZValue(-2)
            self._scene.addItem(top)
            self._arrow_items.append(top)
            top_head = QPolygonF([
                QPointF(ax + w, ay - offset),
                QPointF(ax + w - head_len,
                        ay - offset - head_off),
                QPointF(ax + w - head_len, ay - offset),
            ])
            top_item = QGraphicsPolygonItem(top_head)
            top_item.setBrush(QBrush(QColor("#444")))
            top_item.setPen(pen)
            top_item.setZValue(-2)
            self._scene.addItem(top_item)
            self._arrow_items.append(top_item)
            # Bottom shaft + left-pointing arrowhead.
            bot = QGraphicsLineItem(
                ax - w, ay + offset, ax + w, ay + offset)
            bot.setPen(pen)
            bot.setZValue(-2)
            self._scene.addItem(bot)
            self._arrow_items.append(bot)
            bot_head = QPolygonF([
                QPointF(ax - w, ay + offset),
                QPointF(ax - w + head_len,
                        ay + offset + head_off),
                QPointF(ax - w + head_len, ay + offset),
            ])
            bot_item = QGraphicsPolygonItem(bot_head)
            bot_item.setBrush(QBrush(QColor("#444")))
            bot_item.setPen(pen)
            bot_item.setZValue(-2)
            self._scene.addItem(bot_item)
            self._arrow_items.append(bot_item)

    def remove_arrow(self) -> None:
        """Public clearer — drop the arrow if any.  Pushes one
        undo snapshot when an arrow was actually present."""
        if self._arrow is None:
            return
        self._push_undo()
        self._set_arrow(None)
        self._emit_changed()

    def has_arrow(self) -> bool:
        return self._arrow is not None

    def arrow_state(self) -> Optional[Tuple[float, float, str]]:
        return self._arrow

    def current_scheme(self) -> Optional[Scheme]:
        """Phase 36f.2 — partition the canvas into a reaction
        :class:`Scheme` based on each atom's x position vs the
        arrow's x position.  Atoms left of the arrow → LHS;
        atoms right → RHS.  Bonds whose endpoints straddle the
        arrow are dropped (the user's drawing said *"these
        atoms became those atoms"*, not *"this exact bond
        survived"*).

        Returns ``None`` when no arrow is on the canvas — caller
        should prompt the user to place one first.
        """
        if self._arrow is None:
            return None
        ax, _ay, kind = self._arrow
        lhs_indices: List[int] = []
        rhs_indices: List[int] = []
        for i, items in enumerate(self._atom_items):
            x, _y = items.get("pos", (0.0, 0.0))
            if x < ax:
                lhs_indices.append(i)
            else:
                rhs_indices.append(i)
        lhs_struct = self._slice_structure(lhs_indices)
        rhs_struct = self._slice_structure(rhs_indices)
        lhs_list: List[Structure] = (
            [lhs_struct] if not lhs_struct.is_empty else [])
        rhs_list: List[Structure] = (
            [rhs_struct] if not rhs_struct.is_empty else [])
        return Scheme(lhs=lhs_list, rhs=rhs_list, arrow=kind)

    def _slice_structure(self, atom_indices: List[int]) -> Structure:
        """Build a fresh :class:`Structure` from a subset of the
        live structure's atoms.  Bonds with both endpoints in the
        subset are copied over with re-indexed endpoints."""
        out = Structure()
        idx_map: Dict[int, int] = {}
        for old_i in atom_indices:
            atom = self._structure.atoms[old_i]
            new_i = out.add_atom(atom.element)
            out.atoms[new_i].charge = atom.charge
            out.atoms[new_i].isotope = atom.isotope
            out.atoms[new_i].radical = atom.radical
            out.atoms[new_i].h_count = atom.h_count
            out.atoms[new_i].aromatic = atom.aromatic
            out.atoms[new_i].chirality = atom.chirality
            idx_map[old_i] = new_i
        atom_set = set(atom_indices)
        for b in self._structure.bonds:
            if b.begin_idx in atom_set and b.end_idx in atom_set:
                out.add_bond(idx_map[b.begin_idx],
                             idx_map[b.end_idx],
                             order=b.order, stereo=b.stereo)
        return out

    # ---- right-click atom-property menu (Phase 36e) ---------

    def handle_canvas_right_click(self, scene_pos: QPointF,
                                  global_pos) -> None:
        """Open a context menu over the atom under the cursor.
        Lets the user set formal charge, isotope label, radical
        electrons, or explicit hydrogen count without leaving
        the canvas."""
        atom_idx = self._hit_atom(scene_pos)
        if atom_idx is None:
            return
        menu = QMenu(self)
        atom = self._structure.atoms[atom_idx]
        # ---- charge submenu --------------------------------
        charge_menu = menu.addMenu("Formal charge")
        for value in (-2, -1, 0, +1, +2):
            label = f"{value:+d}" if value != 0 else "0 (neutral)"
            act = QAction(label, charge_menu)
            act.setCheckable(True)
            act.setChecked(atom.charge == value)
            act.triggered.connect(
                lambda _chk=False, i=atom_idx, v=value:
                self._set_atom_charge(i, v))
            charge_menu.addAction(act)
        # ---- radical submenu --------------------------------
        rad_menu = menu.addMenu("Radical electrons")
        for value in (0, 1, 2):
            act = QAction(str(value), rad_menu)
            act.setCheckable(True)
            act.setChecked(atom.radical == value)
            act.triggered.connect(
                lambda _chk=False, i=atom_idx, v=value:
                self._set_atom_radical(i, v))
            rad_menu.addAction(act)
        # ---- isotope ----------------------------------------
        iso_act = QAction(
            f"Isotope label… (current: {atom.isotope or 'natural'})",
            menu)
        iso_act.triggered.connect(
            lambda _chk=False, i=atom_idx: self._prompt_atom_isotope(i))
        menu.addAction(iso_act)
        # ---- explicit H -------------------------------------
        h_menu = menu.addMenu("Explicit H count")
        for value in (-1, 0, 1, 2, 3, 4):
            label = "auto (-1)" if value == -1 else str(value)
            act = QAction(label, h_menu)
            act.setCheckable(True)
            act.setChecked(atom.h_count == value)
            act.triggered.connect(
                lambda _chk=False, i=atom_idx, v=value:
                self._set_atom_h_count(i, v))
            h_menu.addAction(act)
        menu.exec(global_pos)

    def _set_atom_charge(self, atom_idx: int, value: int) -> None:
        atom = self._structure.atoms[atom_idx]
        if atom.charge == value:
            return
        self._push_undo()
        atom.charge = value
        self._refresh_atom_glyph(atom_idx)
        self._emit_changed()

    def _set_atom_radical(self, atom_idx: int, value: int) -> None:
        atom = self._structure.atoms[atom_idx]
        if atom.radical == value:
            return
        self._push_undo()
        atom.radical = value
        self._emit_changed()

    def _set_atom_isotope(self, atom_idx: int, value: int) -> None:
        atom = self._structure.atoms[atom_idx]
        if atom.isotope == value:
            return
        self._push_undo()
        atom.isotope = max(0, int(value))
        self._refresh_atom_glyph(atom_idx)
        self._emit_changed()

    def _set_atom_h_count(self, atom_idx: int, value: int) -> None:
        atom = self._structure.atoms[atom_idx]
        if atom.h_count == value:
            return
        self._push_undo()
        atom.h_count = value
        self._emit_changed()

    def _prompt_atom_isotope(self, atom_idx: int) -> None:
        atom = self._structure.atoms[atom_idx]
        value, ok = QInputDialog.getInt(
            self, "Isotope label",
            f"Mass number for atom {atom_idx} ({atom.element}):\n"
            "Enter 0 for natural abundance.",
            value=int(atom.isotope), minValue=0, maxValue=300, step=1)
        if ok:
            self._set_atom_isotope(atom_idx, int(value))

    # ---- drawing primitives --------------------------------

    def _draw_atom(self, idx: int, pos: QPointF) -> None:
        r = _ATOM_RADIUS_PX
        atom = self._structure.atoms[idx]
        element = atom.element
        items = self._atom_items[idx]
        # Invisible hit-target circle — sits under the label so
        # clicks near the glyph still register.  Also provides the
        # carbon-point marker for pure-C atoms.
        dot = QGraphicsEllipseItem(
            pos.x() - r, pos.y() - r, 2 * r, 2 * r)
        dot.setBrush(QBrush(QColor("#FFFFFF")))
        dot.setPen(QPen(QColor("#FFFFFF")))
        # Stack dot behind the label.
        dot.setZValue(0)
        self._scene.addItem(dot)
        items["dot"] = dot
        # Phase 36e: render the element symbol when the atom is
        # heteroatom OR has a non-default charge / isotope.  Pure
        # C with no decoration stays as a point dot.
        decorated = (element != "C"
                     or atom.charge != 0
                     or atom.isotope > 0
                     or atom.radical > 0)
        if decorated:
            label_text = element
            label = QGraphicsSimpleTextItem(label_text)
            label.setBrush(_ATOM_COLOUR.get(element, QColor("#222")))
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            label.setFont(font)
            br = label.boundingRect()
            label.setPos(pos.x() - br.width() / 2,
                         pos.y() - br.height() / 2)
            label.setZValue(1)
            self._scene.addItem(label)
            items["label"] = label
            # Charge superscript (top-right of element label).
            if atom.charge != 0:
                sign = "+" if atom.charge > 0 else "−"
                mag = abs(atom.charge)
                ctxt = f"{mag if mag > 1 else ''}{sign}"
                charge_label = QGraphicsSimpleTextItem(ctxt)
                charge_label.setBrush(QColor("#A02020"))
                cf = QFont()
                cf.setPointSize(8)
                cf.setBold(True)
                charge_label.setFont(cf)
                charge_label.setPos(
                    pos.x() + br.width() / 2 - 1,
                    pos.y() - br.height() / 2 - 4)
                charge_label.setZValue(2)
                self._scene.addItem(charge_label)
                items["charge_label"] = charge_label
            # Isotope superscript (top-left).
            if atom.isotope > 0:
                iso_label = QGraphicsSimpleTextItem(str(atom.isotope))
                iso_label.setBrush(QColor("#404040"))
                isf = QFont()
                isf.setPointSize(8)
                iso_label.setFont(isf)
                ibr = iso_label.boundingRect()
                iso_label.setPos(
                    pos.x() - br.width() / 2 - ibr.width(),
                    pos.y() - br.height() / 2 - 2)
                iso_label.setZValue(2)
                self._scene.addItem(iso_label)
                items["iso_label"] = iso_label
            # Radical dots (one or two small circles above the atom).
            if atom.radical > 0:
                for k in range(min(atom.radical, 2)):
                    dot_r = 1.6
                    cx = pos.x() + (k - 0.5) * 4 if atom.radical > 1 \
                        else pos.x()
                    cy = pos.y() - br.height() / 2 - 6
                    rdot = QGraphicsEllipseItem(
                        cx - dot_r, cy - dot_r, 2 * dot_r, 2 * dot_r)
                    rdot.setBrush(QBrush(QColor("#000")))
                    rdot.setPen(QPen(QColor("#000")))
                    rdot.setZValue(2)
                    self._scene.addItem(rdot)
                    items[f"radical_{k}"] = rdot
        else:
            items["label"] = None
            # Shrink the dot so pure-C atoms render as a point.
            carbon_r = 2.0
            dot.setRect(pos.x() - carbon_r, pos.y() - carbon_r,
                        2 * carbon_r, 2 * carbon_r)
            dot.setBrush(QBrush(QColor("#222")))
            dot.setPen(QPen(QColor("#222")))

    def _refresh_atom_glyph(self, idx: int) -> None:
        """Re-render the atom after an element change."""
        items = self._atom_items[idx]
        pos_tuple = items.get("pos") or (0, 0)
        for it in items.values():
            if it is not None and hasattr(it, "scene") and it.scene():
                self._scene.removeItem(it)
        self._atom_items[idx] = {"pos": pos_tuple}
        self._draw_atom(idx, QPointF(pos_tuple[0], pos_tuple[1]))

    def _draw_bond(self, idx: int) -> None:
        """Add the visual for bond *idx* to the scene + the
        per-bond list.  Wedge / dash get tapered-polygon and
        hashed-ladder geometry; everything else stays as a
        plain `QGraphicsLineItem`."""
        item = self._build_bond_visual(idx)
        self._scene.addItem(item)
        self._bond_items.append(item)

    def _refresh_bond(self, idx: int) -> None:
        """Drop + rebuild the visual for bond *idx*.

        We can't mutate-in-place across visual types (a
        wedge-→-line stereo flip changes the QGraphicsItem
        subclass), so refresh always swaps the scene item.
        Cheap on a teaching-scale molecule and far simpler
        than maintaining two parallel update paths.
        """
        old = self._bond_items[idx]
        if old is not None and old.scene():
            self._scene.removeItem(old)
        new = self._build_bond_visual(idx)
        self._scene.addItem(new)
        self._bond_items[idx] = new

    # Pen / brush palette for bond visuals.  Centralised here so
    # tweaks land in one place.
    _STEREO_WEDGE_COLOUR = QColor("#1B6E1B")    # solid green
    _STEREO_DASH_COLOUR = QColor("#1B4FA8")     # dashed blue
    _STEREO_EITHER_COLOUR = QColor("#888888")   # squiggle grey
    _BOND_DEFAULT_COLOUR = QColor("#222222")
    #: Half-width of the wide end of a tapered wedge (px).
    _WEDGE_HALF_WIDTH_PX = 5.0
    #: Hash spacing along the dashed bond (px).
    _DASH_HASH_SPACING_PX = 4.0
    #: Half-width range for hashed-dash bond (begin → end).
    _DASH_HALF_WIDTH_BEGIN = 1.0
    _DASH_HALF_WIDTH_END = 5.0

    def _build_bond_visual(self, idx: int) -> QGraphicsItem:
        """Construct (but don't insert) a fresh scene item for
        bond *idx* based on its current order + stereo."""
        bond = self._structure.bonds[idx]
        a_pos = self._atom_items[bond.begin_idx]["pos"]
        b_pos = self._atom_items[bond.end_idx]["pos"]
        ax, ay = a_pos
        bx, by = b_pos
        if bond.stereo == "wedge":
            return self._build_wedge_item(ax, ay, bx, by)
        if bond.stereo == "dash":
            return self._build_dash_item(ax, ay, bx, by)
        # Plain line for orders 1/2/3/aromatic + the default
        # ('none' / 'either') stereo.  Encoding via pen width +
        # dash pattern is enough — proper double-bond offset
        # rendering is a future polish round.
        line = QGraphicsLineItem(ax, ay, bx, by)
        pen = QPen(self._BOND_DEFAULT_COLOUR)
        widths = {1: 1.6, 2: 4.0, 3: 6.0, 4: 2.4}
        pen.setWidthF(widths.get(bond.order, 1.6))
        if bond.stereo == "either":
            pen.setColor(self._STEREO_EITHER_COLOUR)
            pen.setWidthF(2.0)
            pen.setStyle(Qt.DotLine)
        elif bond.order == 4:
            pen.setStyle(Qt.DashLine)
        else:
            pen.setStyle(Qt.SolidLine)
        line.setPen(pen)
        line.setZValue(-1)
        return line

    def _build_wedge_item(self, ax: float, ay: float,
                          bx: float, by: float) -> QGraphicsItem:
        """Tapered solid triangle: apex at the begin atom (a),
        base at the end atom (b).  Reads as *"this bond projects
        out of the page toward the end atom"*, matching ChemDraw."""
        dx, dy = bx - ax, by - ay
        length = (dx * dx + dy * dy) ** 0.5
        if length < 1e-3:
            # Degenerate (begin / end coincide) — fall back to a
            # tiny line so we don't divide by zero.
            return QGraphicsLineItem(ax, ay, bx, by)
        # Perpendicular unit vector (-dy, dx) / length.
        px, py = -dy / length, dx / length
        h = self._WEDGE_HALF_WIDTH_PX
        polygon = QPolygonF([
            QPointF(ax, ay),
            QPointF(bx + h * px, by + h * py),
            QPointF(bx - h * px, by - h * py),
        ])
        item = QGraphicsPolygonItem(polygon)
        item.setBrush(QBrush(self._STEREO_WEDGE_COLOUR))
        pen = QPen(self._STEREO_WEDGE_COLOUR)
        pen.setWidthF(0.0)   # fill-only
        item.setPen(pen)
        item.setZValue(-1)
        return item

    def _build_dash_item(self, ax: float, ay: float,
                         bx: float, by: float) -> QGraphicsItem:
        """Hashed ladder: a stack of short perpendicular lines
        getting wider toward the end atom.  Reads as *"this bond
        projects behind the page toward the end atom"*, matching
        ChemDraw's dashed-wedge convention.

        Returned as a `QGraphicsItemGroup` so the per-hash lines
        move together when the bond gets refreshed."""
        dx, dy = bx - ax, by - ay
        length = (dx * dx + dy * dy) ** 0.5
        if length < 1e-3:
            return QGraphicsLineItem(ax, ay, bx, by)
        ux, uy = dx / length, dy / length
        px, py = -uy, ux                     # perpendicular unit vector
        # Number of hashes scales with bond length — minimum 4 so
        # short bonds still read as a "ladder" rather than two dots.
        n_hashes = max(4, int(length / self._DASH_HASH_SPACING_PX))
        group = QGraphicsItemGroup()
        pen = QPen(self._STEREO_DASH_COLOUR)
        pen.setWidthF(1.4)
        pen.setCapStyle(Qt.RoundCap)
        for i in range(n_hashes):
            # Parameter along bond, [0, 1].  Skip t=0 so the first
            # hash sits a bit away from the begin atom.
            t = (i + 1) / (n_hashes + 1)
            cx = ax + t * dx
            cy = ay + t * dy
            half = (self._DASH_HALF_WIDTH_BEGIN
                    + t * (self._DASH_HALF_WIDTH_END
                           - self._DASH_HALF_WIDTH_BEGIN))
            line = QGraphicsLineItem(
                cx - half * px, cy - half * py,
                cx + half * px, cy + half * py,
            )
            line.setPen(pen)
            group.addToGroup(line)
        group.setZValue(-1)
        return group

    # ---- SMILES ribbon --------------------------------------

    def _on_smiles_entered(self) -> None:
        text = self._smiles_edit.text().strip()
        if not text:
            self.clear()
            return
        ok = self.set_structure_from_smiles(text)
        if not ok:
            # Keep the user's typed text so they can correct it;
            # status label already shows the failure.
            log.warning("Canvas SMILES parse failed: %r", text)

    def _load_structure(self, s: Structure) -> None:
        """Replace the canvas with *s* + lay the atoms out via
        RDKit's `Compute2DCoords`.  Used by the SMILES ribbon and
        by external callers via `set_structure_from_smiles`."""
        # Push a single snapshot so SMILES-rebuild is one undo step.
        self._push_undo()
        self.clear(record_undo=False)
        # Use RDKit for the 2D layout so the SMILES-built canvas
        # doesn't pile every atom on top of each other.
        try:
            from rdkit import Chem
            from rdkit.Chem import AllChem
            from orgchem.core.drawing import _rdkit_from_structure
            mol = _rdkit_from_structure(s)
            if mol is not None:
                AllChem.Compute2DCoords(mol)
                conf = mol.GetConformer()
                coords = [(conf.GetAtomPosition(i).x * 36,
                           -conf.GetAtomPosition(i).y * 36)
                          for i in range(mol.GetNumAtoms())]
            else:
                coords = None
        except Exception:  # noqa: BLE001
            coords = None
        self._structure = Structure(atoms=[a for a in s.atoms],
                                    bonds=[b for b in s.bonds])
        # Draw every atom.
        for i, atom in enumerate(self._structure.atoms):
            if coords is not None:
                x, y = coords[i]
            else:
                x, y = 40.0 * i, 0.0
            self._atom_items.append({"pos": (x, y)})
            self._draw_atom(i, QPointF(x, y))
        for i in range(len(self._structure.bonds)):
            self._draw_bond(i)
        self._emit_changed()

    def _emit_changed(self) -> None:
        smi = self.current_smiles()
        self._smiles_edit.blockSignals(True)
        self._smiles_edit.setText(smi)
        self._smiles_edit.blockSignals(False)
        self.structure_changed.emit(smi)
        self._update_undo_buttons()

    # ---- hit testing ----------------------------------------

    def _hit_atom(self, scene_pos: QPointF) -> Optional[int]:
        best = None
        best_d2 = _HIT_RADIUS_PX ** 2
        for i, items in enumerate(self._atom_items):
            px, py = items["pos"]
            d2 = (px - scene_pos.x()) ** 2 + (py - scene_pos.y()) ** 2
            if d2 <= best_d2:
                best_d2 = d2
                best = i
        return best

    def _hit_bond(self, scene_pos: QPointF) -> Optional[int]:
        for i, bond in enumerate(self._structure.bonds):
            a = self._atom_items[bond.begin_idx]["pos"]
            b = self._atom_items[bond.end_idx]["pos"]
            d = _point_line_distance(
                (scene_pos.x(), scene_pos.y()), a, b)
            if d <= _BOND_HIT_TOL_PX:
                return i
        return None


# ---- geometry helpers ------------------------------------------

def _point_line_distance(p: Tuple[float, float],
                         a: Tuple[float, float],
                         b: Tuple[float, float]) -> float:
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    ll2 = dx * dx + dy * dy
    if ll2 == 0:
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
    t = ((px - ax) * dx + (py - ay) * dy) / ll2
    t = max(0.0, min(1.0, t))
    cx = ax + t * dx
    cy = ay + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5


# ---- internal view subclass ------------------------------------

class _DrawingView(QGraphicsView):
    """Minimal QGraphicsView that forwards mouse events to the
    owning `DrawingPanel`."""

    def __init__(self, panel: DrawingPanel):
        super().__init__()
        self._panel = panel
        self.setDragMode(QGraphicsView.NoDrag)

    def mousePressEvent(self, event: QMouseEvent) -> None:   # noqa: N802
        pos = self.mapToScene(event.pos())
        if event.button() == Qt.RightButton:
            self._panel.handle_canvas_right_click(
                pos, event.globalPosition().toPoint())
            return
        self._panel.handle_canvas_press(pos)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:    # noqa: N802
        pos = self.mapToScene(event.pos())
        self._panel.handle_canvas_move(pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        pos = self.mapToScene(event.pos())
        self._panel.handle_canvas_release(pos)
        super().mouseReleaseEvent(event)
