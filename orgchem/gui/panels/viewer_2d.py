"""2D structure viewer — RDKit SVG rendered in a QSvgWidget."""
from __future__ import annotations
import logging

from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QPushButton,
    QVBoxLayout, QWidget,
)

from rdkit import Chem

from orgchem.messaging.bus import bus
from orgchem.db.queries import get_molecule
from orgchem.core.formats import mol_from_smiles
from orgchem.render.draw2d import render_svg

log = logging.getLogger(__name__)


class Viewer2DPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)

        top = QHBoxLayout()
        top.addWidget(QLabel("Style:"))
        self.style = QComboBox()
        self.style.addItems(["Skeletal", "Atom indices", "Explicit hydrogens", "Kekulé"])
        self.style.currentIndexChanged.connect(self._redraw)
        top.addWidget(self.style)
        top.addStretch(1)
        # Phase 48d (round 173) — inline 'View isomers'
        # button.  One-click jump from the current 2D
        # molecule to the Phase-48 isomer-relationships
        # dialog with the SMILES pre-filled.
        self._isomers_btn = QPushButton("View isomers…")
        self._isomers_btn.setToolTip(
            "Open Tools → Isomer relationships… "
            "(Ctrl+Shift+B) with this molecule's SMILES "
            "pre-filled in the Stereoisomers tab "
            "(Phase 48d).")
        self._isomers_btn.clicked.connect(
            self._on_view_isomers)
        self._isomers_btn.setEnabled(False)
        top.addWidget(self._isomers_btn)
        lay.addLayout(top)

        self.svg = QSvgWidget()
        self.svg.setMinimumSize(280, 280)
        lay.addWidget(self.svg, 1)

        self._current_smiles: str | None = None
        bus().molecule_selected.connect(self._on_mol)

    def _on_mol(self, mol_id: int) -> None:
        row = get_molecule(int(mol_id))
        if row is None:
            return
        self._current_smiles = row.smiles
        self._isomers_btn.setEnabled(bool(row.smiles))
        self._redraw()

    def _on_view_isomers(self) -> None:
        """Phase 48d (round 173) — open the Phase-48 isomer
        explorer dialog with the current molecule's SMILES
        pre-filled in the Stereoisomers + Tautomers tabs."""
        if not self._current_smiles:
            return
        try:
            from orgchem.gui.dialogs.isomer_explorer import (
                IsomerExplorerDialog,
            )
        except Exception as e:
            log.warning(
                "Isomer explorer dialog unavailable: %s", e)
            return
        # Walk up parents to find the main window for the
        # singleton owner.  Fallback to no parent.
        parent_widget = self
        while parent_widget.parent() is not None:
            parent_widget = parent_widget.parent()
        dlg = IsomerExplorerDialog.singleton(
            parent=parent_widget)
        # Pre-fill BOTH enumeration tabs' SMILES inputs +
        # the Classify-pair "A" input so the user lands in a
        # ready-to-run state on whichever tab they switch to.
        dlg._stereo_smiles.setText(self._current_smiles)
        dlg._taut_smiles.setText(self._current_smiles)
        dlg._cls_a.setText(self._current_smiles)
        # Auto-run the stereoisomers enumeration so the user
        # sees results immediately on the default tab —
        # they don't have to click Enumerate themselves.
        dlg.select_tab("Stereoisomers")
        dlg._on_stereo_run()
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def _redraw(self) -> None:
        if not self._current_smiles:
            return
        try:
            mol = mol_from_smiles(self._current_smiles)
        except Exception as e:
            log.warning("2D render: %s", e)
            return
        style = self.style.currentText()
        show_indices = (style == "Atom indices")
        if style == "Explicit hydrogens":
            mol = Chem.AddHs(mol)
        if style == "Kekulé":
            try:
                Chem.Kekulize(mol)
            except Exception:
                pass
        svg = render_svg(mol, show_atom_indices=show_indices)
        self.svg.load(bytes(svg, "utf-8"))
