"""Phase 36g round 126 — *Tools → Drawing tool…* dialog.

Thin wrapper around the Phase-36b :class:`DrawingPanel` that adds
the file I/O + workspace-integration bits so the canvas is
actually *useful*:

- *Export drawing…* → PNG / SVG (via the existing Phase-20
  `render.export_molecule_2d` helper) or MOL (V2000 mol-block
  from the Phase-36a `structure_to_molblock`).
- *Send to Molecule Workspace* → insert the current canvas
  structure as a new `Molecule` row through the round-55
  `add_molecule` authoring action (pollution-safe `Drawn-XXXX`
  naming default).
- Opens preloaded with an optional SMILES so *Open in drawing
  tool…* on the Molecule Workspace (future polish) can route
  existing molecules into the canvas.

Singleton per app instance so re-opening preserves the user's
drawing.
"""
from __future__ import annotations
import logging
import uuid
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QFileDialog, QHBoxLayout, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

from orgchem.gui.panels.drawing_panel import DrawingPanel

log = logging.getLogger(__name__)


class DrawingToolDialog(QDialog):
    """Modeless drawing-tool dialog.  One per main-window
    instance; `singleton()` returns / creates it on demand."""

    _instance: Optional["DrawingToolDialog"] = None

    @classmethod
    def singleton(cls, parent: Optional[QWidget] = None,
                  seed_smiles: str = "") -> "DrawingToolDialog":
        if cls._instance is None:
            cls._instance = cls(parent=parent)
        if seed_smiles:
            cls._instance.load_smiles(seed_smiles)
        return cls._instance

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Molecular drawing tool")
        self.setModal(False)
        self.resize(820, 620)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)

        self.panel = DrawingPanel()
        lay.addWidget(self.panel, 1)

        # Footer buttons: Export + Send to workspace + Close.
        footer = QHBoxLayout()
        self.export_btn = QPushButton("Export drawing…")
        self.export_btn.setToolTip(
            "Save the current canvas as PNG / SVG / MOL "
            "(V2000 mol-block).")
        self.export_btn.clicked.connect(self._on_export)
        footer.addWidget(self.export_btn)

        self.send_btn = QPushButton("Send to Molecule Workspace")
        self.send_btn.setToolTip(
            "Insert the current drawing into the database as a "
            "new Molecule row + select it on the Molecule "
            "Workspace so 2D/3D viewers + descriptors + "
            "retrosynthesis + spectroscopy all run on it "
            "immediately.")
        self.send_btn.clicked.connect(self._on_send_to_workspace)
        footer.addWidget(self.send_btn)

        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        footer.addWidget(close_btn)
        lay.addLayout(footer)

    # ---- public API -----------------------------------------

    def load_smiles(self, smi: str) -> bool:
        """Replace the canvas with *smi*.  Returns True on
        success, False if RDKit can't parse the string."""
        return self.panel.set_structure_from_smiles(smi)

    # ---- slots ----------------------------------------------

    def _on_export(self) -> None:
        smi = self.panel.current_smiles()
        if not smi:
            QMessageBox.information(
                self, "Nothing to export",
                "Draw at least one atom before exporting.")
            return
        path, chosen_filter = QFileDialog.getSaveFileName(
            self, "Export drawing",
            "drawing.png",
            "PNG image (*.png);;SVG vector (*.svg);;"
            "MOL V2000 (*.mol)")
        if not path:
            return
        lower = path.lower()
        try:
            if lower.endswith(".mol"):
                from orgchem.core.drawing import structure_to_molblock
                block = structure_to_molblock(self.panel.get_structure())
                if block is None:
                    raise RuntimeError("mol-block conversion failed.")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(block)
            else:
                # PNG + SVG use the existing RDKit SVG/PNG renderer.
                from orgchem.core.formats import mol_from_smiles
                from orgchem.render.export import export_molecule_2d
                mol = mol_from_smiles(smi)
                export_molecule_2d(mol, path)
        except Exception as e:  # noqa: BLE001
            log.exception("Export drawing failed")
            QMessageBox.warning(self, "Export failed", str(e))

    def _on_send_to_workspace(self) -> None:
        smi = self.panel.current_smiles()
        if not smi:
            QMessageBox.information(
                self, "Nothing to send",
                "Draw at least one atom first.")
            return
        # Default name: `Drawn-XXXXXXXX` with an 8-char UUID suffix.
        # User can rename after insertion if they want a better name.
        name = f"Drawn-{uuid.uuid4().hex[:8]}"
        try:
            from orgchem.agent.actions import invoke
            res = invoke(
                "add_molecule", mol_name=name, smiles=smi,
                notes=f"Drawn in the Phase-36 drawing tool.",
                source_tags=["drawn"],
            )
        except Exception as e:  # noqa: BLE001
            log.exception("add_molecule invocation failed")
            QMessageBox.warning(self, "Send failed", str(e))
            return
        if res.get("status") != "accepted":
            reason = res.get("reason", "unknown")
            if res.get("existing_id") is not None:
                # Duplicate InChIKey / name / SMILES — jump to the
                # existing row instead.
                eid = res["existing_id"]
                QMessageBox.information(
                    self, "Already in library",
                    f"That molecule is already in the library "
                    f"(id={eid}).  Selecting it in the Molecule "
                    f"Workspace.")
                self._select_molecule(eid)
                return
            QMessageBox.warning(self, "Send rejected", reason)
            return
        self._select_molecule(res["id"])
        QMessageBox.information(
            self, "Added to library",
            f"Molecule added as '{name}' (id={res['id']}).  It's "
            f"now the active molecule in the Molecule Workspace.")

    def _select_molecule(self, mol_id: int) -> None:
        """Fire `bus.molecule_selected` so every panel picks the
        new row up without the user clicking through."""
        from orgchem.messaging.bus import bus
        bus().database_changed.emit()
        bus().molecule_selected.emit(int(mol_id))
