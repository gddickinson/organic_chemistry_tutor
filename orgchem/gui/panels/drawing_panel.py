"""Phase 36b / 36d — `QGraphicsScene` drawing canvas.

Backs the molecular drawing tool the user flagged in Phase 36.
Keeps a live :class:`orgchem.core.drawing.Structure` mirror of
the on-screen atoms + bonds so SMILES round-trip is a single
call away.

Tool modes (round 125):

- ``"select"`` — pointer: click an atom to move it (drag), click
  empty canvas to clear the selection.
- ``"atom-<element>"`` — atom-placement tool (C / N / O / P / S /
  F / Cl / Br / I by default); click empty canvas to place,
  click an existing atom to change its element.
- ``"bond"`` — click one atom then another to connect them with a
  single bond (or cycle through single → double → triple by
  clicking an existing bond).
- ``"erase"`` — click an atom to delete it (and its bonds).

Round 128 adds **snapshot-based undo / redo** (Phase 36d) — every
logical mutation (atom place / element swap / bond draw / bond
order cycle / erase / drag-move / clear / SMILES-rebuild) pushes
a `(Structure, positions)` snapshot onto an undo stack; Ctrl+Z
(Undo) / Ctrl+Shift+Z (Redo) buttons walk it.  Stack depth is
capped at 100.

Phase 36c will layer a ring / FG template palette on top; 36e
will add stereochemistry (wedge / dash); 36f will add reaction
arrows.
"""
from __future__ import annotations
import copy
import logging
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Qt, Signal, QPointF, QRectF
from PySide6.QtGui import (
    QBrush, QColor, QFont, QKeySequence, QPainter, QPen, QMouseEvent,
    QShortcut,
)
from PySide6.QtWidgets import (
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsScene,
    QGraphicsSimpleTextItem, QGraphicsView,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget,
)

from orgchem.core.drawing import (
    Atom, Bond, Structure,
    structure_from_smiles, structure_to_smiles,
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
        # Phase 36d undo/redo: stacks of (Structure, positions) tuples.
        # Invariant: the *current* canvas state is NOT on either stack.
        self._undo_stack: List[Tuple[Structure, List[Tuple[float, float]]]] = []
        self._redo_stack: List[Tuple[Structure, List[Tuple[float, float]]]] = []
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
        """Drop every atom + bond.  Emits `structure_changed("")`.

        ``record_undo=False`` bypasses the Phase-36d snapshot —
        used internally by `_load_structure` + `_restore_snapshot`
        where the outer call already manages the stack."""
        if record_undo and not self._structure.is_empty:
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

    def _snapshot(
            self) -> Tuple[Structure, List[Tuple[float, float]]]:
        """Capture a deep-copied snapshot of the current canvas —
        structure + per-atom screen positions."""
        struct = copy.deepcopy(self._structure)
        positions = [tuple(items.get("pos", (0.0, 0.0)))
                     for items in self._atom_items]
        return struct, positions

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

    def _restore_snapshot(
            self, snap: Tuple[Structure, List[Tuple[float, float]]]
            ) -> None:
        """Wipe + rebuild the scene from a snapshot.  Does NOT
        push anything onto the undo stack — caller handles that."""
        struct, positions = snap
        # Remove existing scene items.
        for items in self._atom_items:
            for it in items.values():
                if it is not None and hasattr(it, "scene") and it.scene():
                    self._scene.removeItem(it)
        for b in self._bond_items:
            if b.scene():
                self._scene.removeItem(b)
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

    def _bond_between(self, a: int, b: int) -> Optional[int]:
        for i, bond in enumerate(self._structure.bonds):
            if {bond.begin_idx, bond.end_idx} == {a, b}:
                return i
        return None

    # ---- drawing primitives --------------------------------

    def _draw_atom(self, idx: int, pos: QPointF) -> None:
        r = _ATOM_RADIUS_PX
        element = self._structure.atoms[idx].element
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
        # Carbon atoms: show only a small dot (ChemDraw
        # convention).  Heteroatoms: show the element label.
        if element != "C":
            label = QGraphicsSimpleTextItem(element)
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
        bond = self._structure.bonds[idx]
        a_pos = self._atom_items[bond.begin_idx]["pos"]
        b_pos = self._atom_items[bond.end_idx]["pos"]
        line = QGraphicsLineItem(a_pos[0], a_pos[1], b_pos[0], b_pos[1])
        pen = QPen(QColor("#222"))
        pen.setWidthF(1.6 if bond.order == 1 else 1.2)
        line.setPen(pen)
        line.setZValue(-1)     # under atoms
        self._scene.addItem(line)
        self._bond_items.append(line)
        self._apply_bond_order_style(idx)

    def _refresh_bond(self, idx: int) -> None:
        """Redraw a bond after its endpoints moved or its order
        changed."""
        bond = self._structure.bonds[idx]
        a_pos = self._atom_items[bond.begin_idx]["pos"]
        b_pos = self._atom_items[bond.end_idx]["pos"]
        line = self._bond_items[idx]
        line.setLine(a_pos[0], a_pos[1], b_pos[0], b_pos[1])
        self._apply_bond_order_style(idx)

    def _apply_bond_order_style(self, idx: int) -> None:
        """Minimal stub that shows bond order via pen width;
        proper offset-parallel double/triple-bond rendering is
        Phase 36c polish."""
        bond = self._structure.bonds[idx]
        line = self._bond_items[idx]
        pen = line.pen()
        widths = {1: 1.6, 2: 4.0, 3: 6.0, 4: 2.4}
        pen.setWidthF(widths.get(bond.order, 1.6))
        if bond.order == 4:
            pen.setStyle(Qt.DashLine)    # aromatic as dashed for now
        else:
            pen.setStyle(Qt.SolidLine)
        line.setPen(pen)

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
