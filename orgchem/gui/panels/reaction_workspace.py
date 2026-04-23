"""Reactions tab — filterable reaction list + rendered scheme & description.

Replaces the ``Reactions — Phase 2`` placeholder tab. Emits
``bus.reaction_selected`` so future panels (mechanism player, tutorial
cross-links) can react without this file knowing about them.
"""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QListView, QLineEdit, QLabel,
    QPushButton, QPlainTextEdit, QFileDialog, QMessageBox,
)

from orgchem.messaging.bus import bus
from orgchem.db.queries import list_reactions
from orgchem.db.session import session_scope
from orgchem.db.models import Reaction as DBRxn
from orgchem.render.draw_reaction import render_svg, export_reaction

log = logging.getLogger(__name__)


class _RxnListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._rows: list = []

    def reload(self, query: str = "") -> None:
        self.beginResetModel()
        self._rows = list_reactions(query=query or None)
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._rows)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        if role == Qt.DisplayRole:
            return f"{row.name}    [{row.category or ''}]"
        if role == Qt.UserRole:
            return row.id
        if role == Qt.ToolTipRole:
            return row.reaction_smarts
        return None


class ReactionWorkspacePanel(QWidget):
    def __init__(self):
        super().__init__()
        self._current_id: Optional[int] = None
        self._current_smiles: str = ""
        self._build_ui()
        bus().database_changed.connect(self._reload)
        self._reload()

    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # ---- left: filterable list ----
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(2, 2, 2, 2)
        top = QHBoxLayout()
        self.filter = QLineEdit()
        self.filter.setPlaceholderText("Filter by name or category…")
        self.filter.textChanged.connect(self._on_filter)
        top.addWidget(QLabel("Filter:"))
        top.addWidget(self.filter)
        lv.addLayout(top)
        self.model = _RxnListModel()
        self.view = QListView()
        self.view.setModel(self.model)
        self.view.clicked.connect(self._on_clicked)
        lv.addWidget(self.view)
        left.setMaximumWidth(380)
        splitter.addWidget(left)

        # ---- right: scheme + description ----
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(4, 4, 4, 4)

        self.title = QLabel("Select a reaction from the list")
        self.title.setStyleSheet("font-size: 14pt; font-weight: bold; padding: 4px;")
        rv.addWidget(self.title)

        self.svg = QSvgWidget()
        self.svg.setMinimumHeight(280)
        self.svg.setStyleSheet("background: white; border: 1px solid #ccc;")
        rv.addWidget(self.svg, 1)

        meta_row = QHBoxLayout()
        self.category = QLabel("")
        self.category.setStyleSheet("color:#666; font-style:italic;")
        meta_row.addWidget(self.category)
        meta_row.addStretch(1)
        self.play_btn = QPushButton("▶ Play mechanism")
        self.play_btn.setEnabled(False)
        self.play_btn.setToolTip(
            "Step through the mechanism arrows one frame at a time. "
            "Enabled when the reaction has a mechanism recorded."
        )
        self.play_btn.clicked.connect(self._on_play_mechanism)
        meta_row.addWidget(self.play_btn)
        self.render_3d_btn = QPushButton("Render 3D…")
        self.render_3d_btn.setEnabled(False)
        self.render_3d_btn.setToolTip(
            "Render the reactant and product in 3D side-by-side. "
            "Enabled when the reaction has an atom-mapped SMARTS."
        )
        self.render_3d_btn.clicked.connect(self._on_render_3d)
        meta_row.addWidget(self.render_3d_btn)
        self.animate_3d_btn = QPushButton("▶ Animate 3D")
        self.animate_3d_btn.setEnabled(False)
        self.animate_3d_btn.setToolTip(
            "Play an interactive 3D animation of the reaction "
            "(atoms morph between reactant and product)."
        )
        self.animate_3d_btn.clicked.connect(self._on_animate_3d)
        meta_row.addWidget(self.animate_3d_btn)
        self.energy_btn = QPushButton("Energy profile…")
        self.energy_btn.setEnabled(False)
        self.energy_btn.setToolTip(
            "Show the reaction-coordinate diagram "
            "(reactants → TS‡ → intermediates → products). "
            "Enabled when the reaction has a seeded energy profile."
        )
        self.energy_btn.clicked.connect(self._on_energy_profile)
        meta_row.addWidget(self.energy_btn)
        export_btn = QPushButton("Export reaction…")
        export_btn.clicked.connect(self._on_export)
        meta_row.addWidget(export_btn)
        rv.addLayout(meta_row)

        self.description = QPlainTextEdit()
        self.description.setReadOnly(True)
        self.description.setMaximumHeight(140)
        rv.addWidget(self.description)

        self.smiles_label = QLabel("")
        self.smiles_label.setStyleSheet("font-family: monospace; color:#888; padding:2px;")
        self.smiles_label.setWordWrap(True)
        rv.addWidget(self.smiles_label)

        splitter.addWidget(right)
        splitter.setStretchFactor(1, 1)
        lay.addWidget(splitter)

    # ------------------------------------------------------------------
    def _reload(self) -> None:
        self.model.reload(self.filter.text())

    def _on_filter(self, text: str) -> None:
        self.model.reload(text)

    def _on_clicked(self, idx) -> None:
        rid = self.model.data(idx, Qt.UserRole)
        if rid is None:
            return
        self._display(int(rid))

    def _display(self, rid: int) -> None:
        with session_scope() as s:
            row = s.get(DBRxn, rid)
            if row is None:
                return
            smiles = row.reaction_smarts or ""
            name = row.name
            category = row.category or ""
            description = row.description or ""
            mechanism_json = row.mechanism_json or ""
            mapped_smarts = row.reaction_smarts_mapped or ""
            energy_json = row.energy_profile_json or ""
        self._current_id = rid
        self._current_smiles = smiles
        self._current_name = name
        self._current_mechanism_json = mechanism_json
        self._current_mapped = mapped_smarts
        self._current_energy_json = energy_json
        self.title.setText(name)
        self.category.setText(category)
        self.description.setPlainText(description)
        self.smiles_label.setText(smiles)
        self.play_btn.setEnabled(bool(mechanism_json))
        self.render_3d_btn.setEnabled(bool(mapped_smarts))
        self.animate_3d_btn.setEnabled(bool(mapped_smarts))
        self.energy_btn.setEnabled(bool(energy_json))
        try:
            svg = render_svg(smiles)
            self.svg.load(bytes(svg, "utf-8"))
        except Exception as e:  # noqa: BLE001
            log.warning("Reaction render failed for id=%d: %s", rid, e)
            self.svg.load(b"<svg xmlns='http://www.w3.org/2000/svg'/>")
        bus().reaction_selected.emit(int(rid))

    def _on_play_mechanism(self) -> None:
        if not getattr(self, "_current_mechanism_json", ""):
            return
        from orgchem.core.mechanism import Mechanism
        from orgchem.gui.dialogs.mechanism_player import MechanismPlayerDialog
        try:
            mech = Mechanism.from_json(self._current_mechanism_json)
        except Exception as e:  # noqa: BLE001
            log.exception("Bad mechanism JSON")
            QMessageBox.warning(self, "Mechanism error", str(e))
            return
        MechanismPlayerDialog(mech, self._current_name, self).exec()

    def _on_render_3d(self) -> None:
        mapped = getattr(self, "_current_mapped", "")
        if not mapped:
            return
        from orgchem.render.draw_reaction_3d import render_png
        safe = (self._current_name or "reaction").replace("/", "_").replace(":", "")
        path, _ = QFileDialog.getSaveFileName(
            self, "Render reaction in 3D",
            f"{safe}_3d.png", "PNG (*.png)")
        if not path:
            return
        try:
            render_png(mapped, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "3D render failed", str(e))

    def _on_animate_3d(self) -> None:
        mapped = getattr(self, "_current_mapped", "")
        if not mapped:
            return
        from orgchem.gui.dialogs.reaction_trajectory_player import (
            ReactionTrajectoryPlayerDialog,
        )
        try:
            dlg = ReactionTrajectoryPlayerDialog(
                mapped, self._current_name, parent=self)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Animate failed", str(e))
            return
        dlg.exec()

    def _on_energy_profile(self) -> None:
        energy_json = getattr(self, "_current_energy_json", "")
        if not energy_json:
            return
        from orgchem.core.energy_profile import ReactionEnergyProfile
        try:
            prof = ReactionEnergyProfile.from_json(energy_json)
        except Exception as e:  # noqa: BLE001
            log.exception("Bad energy profile JSON")
            QMessageBox.warning(self, "Energy profile error", str(e))
            return
        from orgchem.gui.dialogs.energy_profile_viewer import (
            EnergyProfileViewerDialog,
        )
        dlg = EnergyProfileViewerDialog(prof, self._current_name, self)
        dlg.exec()

    def _on_export(self) -> None:
        if not self._current_smiles:
            QMessageBox.information(self, "Nothing to export",
                                    "Select a reaction first.")
            return
        safe = (self.title.text() or "reaction").replace("/", "_").replace(":", "")
        path, _ = QFileDialog.getSaveFileName(
            self, "Export reaction", f"{safe}.svg",
            "SVG vector (*.svg);;PNG image (*.png)")
        if not path:
            return
        try:
            export_reaction(self._current_smiles, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Export failed", str(e))
