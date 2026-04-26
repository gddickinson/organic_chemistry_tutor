"""Phase 38c.3 + 38c.4 — graphics items for the lab-setup canvas.

Extracted from `lab_setup_canvas.py` in round 193 to keep that
file under the 500-line cap when Phase-38d.2 simulation wiring
lands.

- :class:`EquipmentGlyph` — placeholder visual for one piece of
  placed equipment (`QGraphicsItemGroup` with bordered ellipse +
  name text, movable + selectable).  Phase 38c.3.
- :class:`ConnectionLine` — visual link between two equipment
  glyphs at named ports (solid green for valid pairs, dashed red
  for invalid).  Phase 38c.4.

Both classes are pure-Qt-graphics; no business logic.  The
canvas dialog instantiates them and owns the scene.
"""
from __future__ import annotations
from typing import Optional

from PySide6.QtCore import QLineF, Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import (
    QGraphicsEllipseItem, QGraphicsItem, QGraphicsItemGroup,
    QGraphicsLineItem, QGraphicsTextItem,
)


#: Default glyph footprint on the canvas (px).
GLYPH_W = 96
GLYPH_H = 56


class EquipmentGlyph(QGraphicsItemGroup):
    """Placeholder glyph for one piece of placed equipment.

    Round 188 (38c.3) renders a bordered ellipse + the equipment
    name as text.  Movable + selectable.  Phase 38c.4 added the
    `_active` flag for the simulator-stage highlight overlay
    (Phase 38d.2).
    """

    def __init__(self, equipment_id: str, label: str,
                 parent: Optional[QGraphicsItem] = None):
        super().__init__(parent)
        self._equipment_id = equipment_id
        self._label = label
        self._active: bool = False
        self._ellipse = QGraphicsEllipseItem(
            -GLYPH_W / 2, -GLYPH_H / 2, GLYPH_W, GLYPH_H)
        self._ellipse.setBrush(QBrush(QColor(245, 245, 250)))
        self._ellipse.setPen(QPen(QColor(60, 60, 80), 1.4))
        self.addToGroup(self._ellipse)
        text = QGraphicsTextItem(label)
        text.setDefaultTextColor(QColor(20, 20, 30))
        br = text.boundingRect()
        text.setPos(-br.width() / 2, -br.height() / 2)
        self.addToGroup(text)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def equipment_id(self) -> str:
        return self._equipment_id

    def label(self) -> str:
        return self._label

    def set_active(self, active: bool) -> None:
        """Phase 38d.2 — toggle the simulator-stage highlight.
        Active glyphs render with a thicker amber border so the
        user can see which piece of equipment the current
        process stage is acting on."""
        if active == self._active:
            return
        self._active = active
        if active:
            self._ellipse.setPen(QPen(QColor(220, 140, 30), 3.5))
            self._ellipse.setBrush(
                QBrush(QColor(255, 248, 220)))
        else:
            self._ellipse.setPen(QPen(QColor(60, 60, 80), 1.4))
            self._ellipse.setBrush(
                QBrush(QColor(245, 245, 250)))

    def is_active(self) -> bool:
        return self._active


class ConnectionLine(QGraphicsLineItem):
    """Visual connection between two :class:`EquipmentGlyph`
    instances at the named ports.

    Solid green line for compatible ports, dashed red line for
    incompatible.  The validation result is computed by
    :func:`core.lab_setups.validate_port_pair` at construction
    time + carried as ``error`` (``None`` when valid).
    """

    def __init__(self, glyph_a: "EquipmentGlyph", port_a: str,
                 glyph_b: "EquipmentGlyph", port_b: str,
                 error: Optional[str],
                 parent: Optional[QGraphicsItem] = None):
        super().__init__(parent)
        self._glyph_a = glyph_a
        self._glyph_b = glyph_b
        self._port_a = port_a
        self._port_b = port_b
        self._error = error
        a = glyph_a.scenePos()
        b = glyph_b.scenePos()
        self.setLine(QLineF(a.x(), a.y(), b.x(), b.y()))
        if error is None:
            pen = QPen(QColor(40, 140, 70), 2.4)
            pen.setStyle(Qt.SolidLine)
        else:
            pen = QPen(QColor(190, 40, 40), 2.4)
            pen.setStyle(Qt.DashLine)
        self.setPen(pen)
        # Sit beneath the glyphs so the equipment overlays the
        # endpoint of the line.
        self.setZValue(-1.0)

    def equipment_a_id(self) -> str:
        return self._glyph_a.equipment_id()

    def equipment_b_id(self) -> str:
        return self._glyph_b.equipment_id()

    def port_a(self) -> str:
        return self._port_a

    def port_b(self) -> str:
        return self._port_b

    def error(self) -> Optional[str]:
        return self._error

    def is_valid(self) -> bool:
        return self._error is None
