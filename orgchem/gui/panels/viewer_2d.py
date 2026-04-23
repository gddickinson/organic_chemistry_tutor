"""2D structure viewer — RDKit SVG rendered in a QSvgWidget."""
from __future__ import annotations
import logging

from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QHBoxLayout, QLabel

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
        self._redraw()

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
