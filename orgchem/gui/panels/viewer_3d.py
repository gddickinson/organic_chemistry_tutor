"""3D molecule viewer panel.

Two interchangeable backends, chosen in ``Tools → Preferences…``:

- **3Dmol**      (default) — QWebEngineView + 3Dmol.js. Interactive rotate /
  zoom / pick. Requires WebGL (so only usable in a normal GUI launch;
  Chromium's GPU is disabled under offscreen Qt for stability).
- **matplotlib** — renders a PNG via :mod:`orgchem.render.draw3d_mpl` and
  shows it in a ``QLabel``. Static, but works in any mode including
  headless / screenshot tours.

The ``Style`` combo stays in the panel — it's a per-molecule rendering
choice, not a preference.
"""
from __future__ import annotations
import logging
import tempfile
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QStackedWidget,
    QPushButton, QFileDialog, QMessageBox,
)

from orgchem.config import AppConfig
from orgchem.messaging.bus import bus
from orgchem.messaging.errors import ConformerGenerationError
from orgchem.db.queries import get_molecule
from orgchem.core.molecule import Molecule
from orgchem.core.conformers import embed_3d  # noqa: F401 (re-exported for tests)
from orgchem.render.draw3d import build_3dmol_html
from orgchem.render import draw3d_mpl

log = logging.getLogger(__name__)


class Viewer3DPanel(QWidget):
    def __init__(self, cfg: AppConfig):
        super().__init__()
        self.cfg = cfg
        self._current_molblock: str | None = None
        self._current_name: str = ""

        lay = QVBoxLayout(self)
        self._build_toolbar(lay)
        self._build_stack(lay)

        bus().molecule_selected.connect(self._on_mol)
        bus().config_changed.connect(self._rerender)
        self._render_empty()

    # ------------------------------------------------------------------
    def _build_toolbar(self, lay: QVBoxLayout) -> None:
        top = QHBoxLayout()
        top.addWidget(QLabel("Style:"))
        self.style = QComboBox()
        self.style.addItems(["stick", "ball-and-stick", "sphere", "line"])
        self.style.setCurrentText(self.cfg.default_3d_style)
        self.style.currentTextChanged.connect(self._rerender)
        top.addWidget(self.style)
        top.addStretch(1)
        save_btn = QPushButton("Save PNG…")
        save_btn.setToolTip(
            "Save the current 3D structure to a PNG file via the matplotlib "
            "renderer (works for both backends)."
        )
        save_btn.clicked.connect(self._on_save_png)
        top.addWidget(save_btn)

        dyn_btn = QPushButton("▶ Run dynamics…")
        dyn_btn.setToolTip(
            "Play a conformational-dynamics animation for this molecule "
            "(Phase 10a: dihedral scan or conformer morph)."
        )
        dyn_btn.clicked.connect(self._on_run_dynamics)
        top.addWidget(dyn_btn)

        lay.addLayout(top)

    def _build_stack(self, lay: QVBoxLayout) -> None:
        self.stack = QStackedWidget()
        self.web = QWebEngineView()
        self.web.setMinimumSize(280, 280)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumSize(280, 280)
        self.image.setStyleSheet("background: white;")
        self.stack.addWidget(self.web)     # index 0 — 3Dmol
        self.stack.addWidget(self.image)   # index 1 — matplotlib
        lay.addWidget(self.stack, 1)

    # ------------------------------------------------------------------
    def _backend(self) -> str:
        """Current backend, resolved fresh from config each call."""
        b = getattr(self.cfg, "default_3d_backend", "3Dmol").lower()
        return "matplotlib" if b.startswith("mat") else "3Dmol"

    def _render_empty(self) -> None:
        if self._backend() == "3Dmol":
            self.stack.setCurrentIndex(0)
            self.web.setHtml(
                "<html><body style='background:white;color:#aaa;"
                "font-family:sans-serif;text-align:center;padding-top:40%;'>"
                "<h3>Select a molecule to view in 3D</h3></body></html>"
            )
        else:
            self.stack.setCurrentIndex(1)
            self.image.setText("Select a molecule to view in 3D")

    def _on_mol(self, mol_id: int) -> None:
        row = get_molecule(int(mol_id))
        if row is None:
            return
        self._current_name = row.name
        mb = row.molblock_3d
        if not mb:
            try:
                m = Molecule.from_smiles(row.smiles, name=row.name, generate_3d=True)
                mb = m.molblock_3d
            except ConformerGenerationError as e:
                log.warning("3D embed failed for %s: %s", row.name, e)
                self._error(f"3D generation failed for {row.name}")
                return
        self._current_molblock = mb
        self._rerender()

    def _rerender(self) -> None:
        if not self._current_molblock:
            return
        if self._backend() == "3Dmol":
            self._render_3dmol()
        else:
            self._render_mpl()

    def _render_3dmol(self) -> None:
        self.stack.setCurrentIndex(0)
        html = build_3dmol_html([self._current_molblock],
                                style=self.style.currentText())
        self.web.setHtml(html)

    def _render_mpl(self) -> None:
        self.stack.setCurrentIndex(1)
        mol = _molblock_to_mol(self._current_molblock)
        if mol is None:
            self._error("Could not parse 3D MOL block")
            return
        tmp = Path(tempfile.gettempdir()) / f"orgchem_viewer3d_{id(self)}.png"
        try:
            draw3d_mpl.render_png(mol, tmp, style=self.style.currentText(),
                                  width=700, height=600)
        except Exception as e:  # noqa: BLE001
            log.exception("matplotlib 3D render failed")
            self._error(f"matplotlib render failed: {e}")
            return
        pix = QPixmap(str(tmp))
        self.image.setPixmap(pix.scaled(
            self.image.width(), self.image.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation,
        ))

    def _error(self, msg: str) -> None:
        self.stack.setCurrentIndex(1)
        self.image.setText(msg)
        self.image.setStyleSheet("color:#c03030; background:white;")

    def _on_run_dynamics(self) -> None:
        if not self._current_molblock:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, "No molecule",
                                    "Select a molecule first.")
            return
        from orgchem.gui.dialogs.dynamics_player import DynamicsPlayerDialog
        mol = _molblock_to_mol(self._current_molblock)
        if mol is None:
            return
        dlg = DynamicsPlayerDialog(mol, self._current_name, parent=self)
        dlg.show()

    def _on_save_png(self) -> None:
        if not self._current_molblock:
            QMessageBox.information(self, "Nothing to save", "Select a molecule first.")
            return
        suggested = (self._current_name or "molecule") + "_3d.png"
        path, _ = QFileDialog.getSaveFileName(
            self, "Save 3D view (PNG)", suggested, "PNG (*.png)")
        if not path:
            return
        mol = _molblock_to_mol(self._current_molblock)
        if mol is None:
            QMessageBox.warning(self, "Save failed", "Could not parse MOL block.")
            return
        try:
            draw3d_mpl.render_png(mol, path, style=self.style.currentText())
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Save failed", str(e))


def _molblock_to_mol(molblock: str):
    from rdkit import Chem
    return Chem.MolFromMolBlock(molblock, removeHs=False)
