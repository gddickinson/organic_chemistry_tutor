"""Dynamics player dialog (Phase 10a).

Launched from the 3D viewer's "Run dynamics…" button. Offers two modes:

- **Conformer morph** — works on any molecule, no per-atom input needed.
  Uses :func:`orgchem.core.dynamics.run_conformer_morph` to embed a
  diverse set of conformers and interpolate smoothly through them.

- **Dihedral scan** — user picks a rotatable bond from a dropdown
  populated via RDKit's :mod:`Chem.Lipinski` rotatable-bond finder. The
  scan rotates that torsion from 0° → 360° and relaxes everything else
  with MMFF at each step.

Playback happens in an embedded ``QWebEngineView`` rendering the
Phase 2c.2 multi-frame XYZ → 3Dmol.js HTML, so all the play / pause /
reset / speed controls already exist.
"""
from __future__ import annotations
import logging
from typing import List, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QDialogButtonBox, QMessageBox, QFileDialog,
)

from rdkit import Chem

from orgchem.core.dynamics import (
    run_conformer_morph, run_dihedral_scan, frames_to_xyz,
)
from orgchem.render.draw_reaction_3d import build_trajectory_html

log = logging.getLogger(__name__)


class DynamicsPlayerDialog(QDialog):
    def __init__(self, mol: Chem.Mol, molecule_name: str, parent=None):
        super().__init__(parent)
        self.mol = mol
        self.molecule_name = molecule_name or "molecule"
        self.setWindowTitle(f"Dynamics: {self.molecule_name}")
        self.resize(860, 680)

        self._rot_bonds = _find_rotatable_dihedrals(mol)
        self._html: str = ""
        self._build_ui()
        # Auto-run with a sensible default so the dialog isn't empty.
        self._run()

    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(
            f"<b>{self.molecule_name}</b>  —  conformational dynamics "
            f"(Phase 10a). Pick a mode and press <i>Run</i>."
        ))

        cfg_row = QHBoxLayout()
        cfg_row.addWidget(QLabel("Mode:"))
        self.mode = QComboBox()
        self.mode.addItem("Conformer morph (any molecule)")
        if self._rot_bonds:
            self.mode.addItem("Dihedral scan (rotatable bond)")
        self.mode.currentIndexChanged.connect(self._on_mode_change)
        cfg_row.addWidget(self.mode)

        cfg_row.addWidget(QLabel("  Rotatable bond:"))
        self.bond_cb = QComboBox()
        for (a, b, c, d, descr) in self._rot_bonds:
            self.bond_cb.addItem(descr, (a, b, c, d))
        self.bond_cb.setEnabled(False)
        cfg_row.addWidget(self.bond_cb)

        cfg_row.addStretch(1)
        run_btn = QPushButton("Run")
        run_btn.clicked.connect(self._run)
        cfg_row.addWidget(run_btn)
        lay.addLayout(cfg_row)

        self.view = QWebEngineView()
        lay.addWidget(self.view, 1)

        actions = QHBoxLayout()
        save_btn = QPushButton("Save HTML…")
        save_btn.clicked.connect(self._save_html)
        actions.addWidget(save_btn)
        actions.addStretch(1)
        bb = QDialogButtonBox(QDialogButtonBox.Close)
        bb.rejected.connect(self.reject)
        actions.addWidget(bb)
        lay.addLayout(actions)

    def _on_mode_change(self, _idx: int) -> None:
        self.bond_cb.setEnabled(
            self.mode.currentText().startswith("Dihedral"))

    def _run(self) -> None:
        try:
            if self.mode.currentText().startswith("Dihedral"):
                a, b, c, d = self.bond_cb.currentData()
                result = run_dihedral_scan(
                    self.mol, dihedral_atoms=(a, b, c, d), n_frames=36)
                title = (f"{self.molecule_name} — dihedral "
                         f"{a}-{b}-{c}-{d} scan")
            else:
                result = run_conformer_morph(
                    self.mol, n_conformers=8, n_interp_frames=6)
                title = f"{self.molecule_name} — conformer morph"
        except Exception as e:  # noqa: BLE001
            log.exception("Dynamics run failed")
            QMessageBox.warning(self, "Dynamics failed", str(e))
            return
        xyz = frames_to_xyz(result)
        self._html = build_trajectory_html(xyz, title=title)
        self.view.setHtml(self._html)

    def _save_html(self) -> None:
        if not self._html:
            return
        safe = self.molecule_name.replace("/", "_").replace(" ", "_")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save dynamics HTML", f"{safe}_dynamics.html",
            "HTML (*.html *.htm)")
        if not path:
            return
        with open(path, "w") as f:
            f.write(self._html)


def _find_rotatable_dihedrals(mol: Chem.Mol) -> List[Tuple[int, int, int, int, str]]:
    """Find (a, b, c, d, label) tuples for each non-terminal rotatable bond."""
    pattern = Chem.MolFromSmarts("[!$(*#*)&!D1]-&!@[!$(*#*)&!D1]")
    out: List[Tuple[int, int, int, int, str]] = []
    for b, c in mol.GetSubstructMatches(pattern):
        atom_b = mol.GetAtomWithIdx(b)
        atom_c = mol.GetAtomWithIdx(c)
        a_neighbours = [n for n in atom_b.GetNeighbors() if n.GetIdx() != c]
        d_neighbours = [n for n in atom_c.GetNeighbors() if n.GetIdx() != b]
        if not a_neighbours or not d_neighbours:
            continue
        a = a_neighbours[0].GetIdx()
        d = d_neighbours[0].GetIdx()
        descr = (f"{mol.GetAtomWithIdx(a).GetSymbol()}{a}-"
                 f"{atom_b.GetSymbol()}{b}-"
                 f"{atom_c.GetSymbol()}{c}-"
                 f"{mol.GetAtomWithIdx(d).GetSymbol()}{d}")
        out.append((a, b, c, d, descr))
    return out
