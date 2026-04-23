"""Compare tab — 2×2 grid of molecule slots for side-by-side comparison.

Each slot shows a 2D structure, name, formula, and a mini descriptor table
(MW, logP, TPSA, ring count). The grid accepts molecules from:

- the database (load by id via the agent action `compare_molecules`)
- direct SMILES entry per slot
- drag-drop from the browser (future — needs a QMimeData hook-up)

Replaces the former ``Compare — Phase 2`` tab stub.
"""
from __future__ import annotations
import logging
from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame,
)

from orgchem.core.formats import mol_from_smiles
from orgchem.core.descriptors import compute_all
from orgchem.db.queries import get_molecule
from orgchem.render.draw2d import render_svg
from orgchem.messaging.bus import bus
from orgchem.messaging.errors import InvalidSMILESError

log = logging.getLogger(__name__)


#: Internal MIME type used when dragging a molecule row out of the
#: MoleculeBrowserPanel list view into a Compare slot.
_MIME_MOLECULE_ID = "application/x-orgchem-molecule-id"


class _Slot(QFrame):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background: white;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)

        # Title + SMILES input.
        self.title = QLabel(f"Slot {index + 1} — empty")
        self.title.setStyleSheet("font-weight: bold; padding: 2px;")
        lay.addWidget(self.title)

        entry = QHBoxLayout()
        self.smiles = QLineEdit()
        self.smiles.setPlaceholderText(
            "Enter a molecule name or SMILES (drag from Molecule browser also works)"
        )
        self.smiles.returnPressed.connect(self._on_load)
        load_btn = QPushButton("Load")
        load_btn.setFixedWidth(60)
        load_btn.clicked.connect(self._on_load)
        entry.addWidget(self.smiles, 1)
        entry.addWidget(load_btn)
        lay.addLayout(entry)

        # Drop target: accept the mime payload the molecule browser
        # emits when a user drags a row from the left dock.
        self.setAcceptDrops(True)

        self.svg = QSvgWidget()
        self.svg.setMinimumHeight(220)
        lay.addWidget(self.svg, 1)

        self.props = QLabel("")
        self.props.setStyleSheet("font-family: monospace; color:#555; padding:4px;")
        self.props.setWordWrap(True)
        lay.addWidget(self.props)

    # ----- public API -----

    def load_by_id(self, mol_id: int) -> bool:
        row = get_molecule(int(mol_id))
        if row is None:
            self._error(f"No molecule id {mol_id}")
            return False
        return self._display(row.smiles, row.name)

    def load_by_smiles(self, smiles: str, name: str = "") -> bool:
        return self._display(smiles.strip(), name or smiles.strip())

    def clear(self) -> None:
        self.title.setText(f"Slot {self.index + 1} — empty")
        self.smiles.clear()
        self.svg.load(b"<svg xmlns='http://www.w3.org/2000/svg'/>")
        self.props.clear()

    # ----- internals -----

    def _on_load(self) -> None:
        text = self.smiles.text().strip()
        if not text:
            return
        # Try a DB name lookup first — "Caffeine" should resolve to the
        # seeded row rather than hit the SMILES parser and fail.
        from orgchem.db.queries import find_molecule_by_name, list_molecules
        try:
            row = find_molecule_by_name(text)
            if row is None:
                hits = list_molecules(query=text, limit=1)
                if hits:
                    row = hits[0]
        except Exception:
            row = None
        if row is not None:
            self._display(row.smiles, row.name)
        else:
            # Not a known name — treat as raw SMILES.
            self._display(text, text)

    def _display(self, smiles: str, name: str) -> bool:
        try:
            mol = mol_from_smiles(smiles)
        except InvalidSMILESError as e:
            self._error(str(e))
            return False
        self.smiles.setText(smiles)
        self.title.setText(f"Slot {self.index + 1} — {name}")
        self.svg.load(bytes(render_svg(mol, width=320, height=240), "utf-8"))
        desc = compute_all(mol)
        self.props.setText(
            f"Formula: {desc['formula']}     MW: {desc['mol_weight']:.2f}\n"
            f"logP: {desc['logp']:.2f}        TPSA: {desc['tpsa']:.1f} Å²\n"
            f"Rings: {desc['rings_total']}  (arom {desc['aromatic_rings']})   "
            f"HBD/HBA: {desc['h_bond_donors']}/{desc['h_bond_acceptors']}"
        )
        return True

    def _error(self, msg: str) -> None:
        self.title.setText(f"Slot {self.index + 1} — error")
        self.props.setStyleSheet("color:#c03030; font-family:monospace; padding:4px;")
        self.props.setText(msg)

    # ---- drag-and-drop ---------------------------------------------------

    def dragEnterEvent(self, event) -> None:  # noqa: N802 — Qt override
        mime = event.mimeData()
        if mime.hasFormat(_MIME_MOLECULE_ID):
            event.acceptProposedAction()
            self.setStyleSheet("background: #eef5ff; border: 2px solid #2a5885;")
        else:
            event.ignore()

    def dragLeaveEvent(self, event) -> None:  # noqa: N802
        self.setStyleSheet("background: white;")
        event.accept()

    def dropEvent(self, event) -> None:  # noqa: N802
        mime = event.mimeData()
        if not mime.hasFormat(_MIME_MOLECULE_ID):
            event.ignore()
            return
        try:
            mol_id = int(bytes(mime.data(_MIME_MOLECULE_ID)).decode())
        except Exception:
            event.ignore()
            return
        self.load_by_id(mol_id)
        self.setStyleSheet("background: white;")
        event.acceptProposedAction()


class ComparePanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)

        header = QHBoxLayout()
        header.addWidget(QLabel(
            "<b>Compare</b> — up to four molecules side-by-side. "
            "Type a SMILES and hit Load, or use the "
            "<code>compare_molecules</code> agent action with a list of IDs."
        ))
        header.addStretch(1)
        clear_all = QPushButton("Clear all")
        clear_all.clicked.connect(self.clear_all)
        header.addWidget(clear_all)
        lay.addLayout(header)

        grid = QGridLayout()
        self.slots: List[_Slot] = []
        for i in range(4):
            slot = _Slot(i)
            self.slots.append(slot)
            grid.addWidget(slot, i // 2, i % 2)
        lay.addLayout(grid, 1)

        bus().database_changed.connect(self._refresh_selected)

    # ----- public API used by agent.library.compare_molecules -----

    def set_molecule_ids(self, ids: List[int]) -> int:
        """Fill the first N slots (N ≤ 4) from DB ids. Returns count loaded."""
        count = 0
        for slot, mol_id in zip(self.slots, ids[:4]):
            if slot.load_by_id(int(mol_id)):
                count += 1
        return count

    def clear_all(self) -> None:
        for s in self.slots:
            s.clear()

    def _refresh_selected(self) -> None:
        # No-op for now; if a slot held a DB id we'd re-fetch here.
        pass
