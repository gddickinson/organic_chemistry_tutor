"""Protein workspace panel — surfaces Phase 24 features in the GUI.

One tab to drive the whole Phase-24 stack:

- **Seeded targets** — drop-down of the teaching-set PDB IDs + any
  fetched-and-cached entries.
- **Fetch from RCSB / AlphaFold** — one-shot download with a cache hit
  shown inline.
- **Summary** — chain / residue / ligand / title read-out.
- **Binding-site pockets** (Phase 24d) and **ligand contacts**
  (Phase 24e) in tabs. The contacts tab has an "Export interaction
  map…" button (Phase 24c).
- **PPI interfaces** (Phase 24j): per-chain-pair contact counts.
- **NA-ligand** (Phase 24k): intercalation / groove / phosphate.
- **PLIP capabilities** badge so students know if the upgraded
  analysis path is available.

All chemistry runs on the main thread here — every analyser is fast
(<1 s on teaching-scale targets). Long-running fetches go through
:mod:`orgchem.utils.threading` via the existing :func:`submit` helper.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QObject, Qt, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QFileDialog, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMessageBox,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QTabWidget, QTextBrowser, QVBoxLayout, QWidget,
)

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    _HAVE_WEBENGINE = True
except ImportError:  # pragma: no cover - web engine is a hard dep in this app
    _HAVE_WEBENGINE = False

try:
    from PySide6.QtWebChannel import QWebChannel
    _HAVE_WEBCHANNEL = True
except ImportError:  # pragma: no cover
    _HAVE_WEBCHANNEL = False


class _PickBridge(QObject):
    """Qt-side object exposed to the 3Dmol.js page via QWebChannel.

    The in-page pick handler calls ``onAtomPicked(chain, resn, resi)``;
    we re-emit as a Qt signal so the Protein panel can update the
    *Picked residue* label.
    """
    picked = Signal(str, str, int)

    @Slot(str, str, int)
    def onAtomPicked(self, chain: str, resn: str, resi: int) -> None:
        self.picked.emit(chain or "", resn or "", int(resi or 0))

from orgchem.messaging.bus import bus

log = logging.getLogger(__name__)


class ProteinPanel(QWidget):
    """One-stop tab covering PDB ingestion, pockets, contacts, PPI, NA."""

    pdb_loaded = Signal(str)   # PDB id once a structure is in memory

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._current_pdb: Optional[str] = None

        root = QVBoxLayout(self)

        # ---- top bar -------------------------------------------------
        top = QHBoxLayout()
        top.addWidget(QLabel("PDB / AlphaFold ID:"))
        self.id_input = QLineEdit()
        self.id_input.setMaximumWidth(120)
        self.id_input.setPlaceholderText("e.g. 2YDO, 1EQG, P04637…")
        top.addWidget(self.id_input)

        self.fetch_btn = QPushButton("Fetch PDB")
        self.fetch_btn.clicked.connect(self._on_fetch_pdb)
        top.addWidget(self.fetch_btn)

        self.fetch_af_btn = QPushButton("Fetch AlphaFold")
        self.fetch_af_btn.clicked.connect(self._on_fetch_alphafold)
        top.addWidget(self.fetch_af_btn)

        top.addSpacing(10)
        self.seeded_combo = QComboBox()
        self.seeded_combo.setMinimumWidth(200)
        self.seeded_combo.addItem("— seeded targets —", "")
        self._populate_seeded()
        self.seeded_combo.currentIndexChanged.connect(self._on_seeded_pick)
        top.addWidget(self.seeded_combo)
        top.addStretch(1)
        root.addLayout(top)

        # ---- summary line -------------------------------------------
        self.summary = QLabel("No structure loaded.")
        self.summary.setStyleSheet(
            "padding:4px; background:#f6f6f8; border-radius:4px;")
        self.summary.setWordWrap(True)
        root.addWidget(self.summary)

        # ---- tabs ----------------------------------------------------
        self.tabs = QTabWidget()
        self.tabs.addTab(self._make_summary_tab(),  "Summary")
        self.tabs.addTab(self._make_3d_tab(),       "3D structure (24l)")
        self.tabs.addTab(self._make_pockets_tab(),  "Pockets (24d)")
        self.tabs.addTab(self._make_contacts_tab(), "Contacts (24e/i)")
        self.tabs.addTab(self._make_ppi_tab(),      "PPI (24j)")
        self.tabs.addTab(self._make_na_tab(),       "NA-ligand (24k)")
        root.addWidget(self.tabs, 1)

        # PLIP badge
        badge_box = QHBoxLayout()
        badge_box.addStretch(1)
        self.plip_badge = QLabel()
        self.plip_badge.setStyleSheet(
            "padding:2px 8px; border-radius:10px; "
            "background:#eef; color:#335;")
        badge_box.addWidget(self.plip_badge)
        root.addLayout(badge_box)
        self._refresh_plip_badge()

    # -----------------------------------------------------------------
    # Summary tab

    def _make_summary_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        self.summary_browser = QTextBrowser()
        self.summary_browser.setOpenExternalLinks(False)
        lay.addWidget(self.summary_browser, 1)

        # Chain sequence row (closes Phase 25b
        # `get_protein_chain_sequence` audit gap).
        seq_row = QHBoxLayout()
        seq_row.addWidget(QLabel("Chain:"))
        self.summary_chain_combo = QComboBox()
        self.summary_chain_combo.setMinimumWidth(80)
        seq_row.addWidget(self.summary_chain_combo)
        self.summary_copy_btn = QPushButton("Copy sequence")
        self.summary_copy_btn.clicked.connect(self._on_copy_chain_sequence)
        seq_row.addWidget(self.summary_copy_btn)
        seq_row.addStretch(1)
        lay.addLayout(seq_row)
        self.summary_seq_label = QLabel("")
        self.summary_seq_label.setStyleSheet(
            "font-family: monospace; background:#f4f6fb; "
            "padding:4px; border-radius:4px;")
        self.summary_seq_label.setWordWrap(True)
        lay.addWidget(self.summary_seq_label)
        return w

    # 3D structure (24l) — interactive 3Dmol.js view

    def _make_3d_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Protein:"))
        self.viewer3d_protein_style = QComboBox()
        self.viewer3d_protein_style.addItems(
            ["cartoon", "trace", "surface"])
        controls.addWidget(self.viewer3d_protein_style)
        controls.addSpacing(8)
        controls.addWidget(QLabel("Ligand:"))
        self.viewer3d_ligand_style = QComboBox()
        self.viewer3d_ligand_style.addItems(
            ["ball-and-stick", "stick", "sphere"])
        controls.addWidget(self.viewer3d_ligand_style)
        controls.addSpacing(8)
        self.viewer3d_show_waters = QCheckBox("Waters")
        controls.addWidget(self.viewer3d_show_waters)
        self.viewer3d_show_surface = QCheckBox("Ligand surface")
        controls.addWidget(self.viewer3d_show_surface)
        self.viewer3d_plddt = QCheckBox("Colour by pLDDT (AlphaFold)")
        self.viewer3d_plddt.setToolTip(
            "Colour the protein by the B-factor column using the "
            "AlphaFold DB gradient. Only meaningful for AlphaFold-"
            "predicted structures, where pLDDT is stored there."
        )
        controls.addWidget(self.viewer3d_plddt)
        self.viewer3d_spin = QCheckBox("Auto-rotate")
        self.viewer3d_spin.setToolTip(
            "Spin the scene around the Y axis — handy for "
            "presentations and for exporting an animated HTML."
        )
        controls.addWidget(self.viewer3d_spin)

        self.viewer3d_render_btn = QPushButton("Render")
        self.viewer3d_render_btn.setDefault(True)
        self.viewer3d_render_btn.clicked.connect(self._on_render_3d)
        controls.addWidget(self.viewer3d_render_btn)
        self.viewer3d_save_btn = QPushButton("Save HTML…")
        self.viewer3d_save_btn.clicked.connect(self._on_save_3d_html)
        controls.addWidget(self.viewer3d_save_btn)
        controls.addStretch(1)
        lay.addLayout(controls)

        if _HAVE_WEBENGINE:
            self.web_3d = QWebEngineView()
            lay.addWidget(self.web_3d, 1)
            # Picked-residue feedback label (Phase 24l click-to-inspect).
            self.picked_label = QLabel("Click a residue in the 3D view "
                                       "to inspect it here.")
            self.picked_label.setStyleSheet(
                "padding:3px 8px; background:#f0f4ff; "
                "border-radius:4px; color:#224;")
            lay.addWidget(self.picked_label)
            self._pick_bridge = _PickBridge(self)
            self._pick_bridge.picked.connect(self._on_atom_picked)
            if _HAVE_WEBCHANNEL:
                self._channel = QWebChannel(self.web_3d)
                self._channel.registerObject("qtBridge", self._pick_bridge)
                self.web_3d.page().setWebChannel(self._channel)
        else:
            self.web_3d = None
            self.picked_label = None
            self._pick_bridge = None
            fallback = QLabel(
                "QtWebEngine not available — install PySide6 with "
                "QtWebEngine support to enable the 3D structure view."
            )
            fallback.setAlignment(Qt.AlignCenter)
            lay.addWidget(fallback, 1)
        return w

    # Pockets (24d)

    def _make_pockets_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        self.pockets_btn = QPushButton("Find binding sites")
        self.pockets_btn.clicked.connect(self._on_find_pockets)
        row.addWidget(self.pockets_btn)
        row.addStretch(1)
        lay.addLayout(row)
        self.pockets_table = self._make_table(
            ["Rank", "Volume (voxels)", "Centre (x, y, z)",
             "# lining residues"])
        lay.addWidget(self.pockets_table, 1)
        return w

    # Contacts (24e / 24i)

    def _make_contacts_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)

        row = QHBoxLayout()
        row.addWidget(QLabel("Ligand (HETATM) name:"))
        self.ligand_input = QLineEdit()
        self.ligand_input.setMaximumWidth(100)
        self.ligand_input.setPlaceholderText("IBP")
        row.addWidget(self.ligand_input)
        self.contacts_btn = QPushButton("Analyse binding")
        self.contacts_btn.clicked.connect(self._on_analyse_binding)
        row.addWidget(self.contacts_btn)
        self.plip_btn = QPushButton("Analyse (PLIP if available)")
        self.plip_btn.clicked.connect(self._on_analyse_binding_plip)
        row.addWidget(self.plip_btn)
        self.export_map_btn = QPushButton("Export interaction map…")
        self.export_map_btn.clicked.connect(self._on_export_map)
        row.addWidget(self.export_map_btn)
        row.addStretch(1)
        lay.addLayout(row)

        self.contacts_table = self._make_table(
            ["Kind", "Ligand atom", "Chain", "Residue", "Distance (Å)"])
        lay.addWidget(self.contacts_table, 1)
        return w

    # PPI (24j)

    def _make_ppi_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        self.ppi_btn = QPushButton("Analyse all chain pairs")
        self.ppi_btn.clicked.connect(self._on_analyse_ppi)
        row.addWidget(self.ppi_btn)
        row.addSpacing(14)
        row.addWidget(QLabel("Or pair:"))
        self.ppi_chain_a = QComboBox()
        self.ppi_chain_b = QComboBox()
        self.ppi_chain_a.setMinimumWidth(60)
        self.ppi_chain_b.setMinimumWidth(60)
        row.addWidget(self.ppi_chain_a)
        row.addWidget(QLabel("×"))
        row.addWidget(self.ppi_chain_b)
        self.ppi_pair_btn = QPushButton("Analyse pair")
        self.ppi_pair_btn.clicked.connect(self._on_analyse_ppi_pair)
        row.addWidget(self.ppi_pair_btn)
        row.addStretch(1)
        lay.addLayout(row)
        self.ppi_table = self._make_table(
            ["Chain A", "Chain B", "# contacts", "By kind"])
        lay.addWidget(self.ppi_table, 1)
        return w

    # NA-ligand (24k)

    def _make_na_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        row = QHBoxLayout()
        row.addWidget(QLabel("Ligand (HETATM) name:"))
        self.na_ligand_input = QLineEdit()
        self.na_ligand_input.setMaximumWidth(100)
        self.na_ligand_input.setPlaceholderText("DM1")
        row.addWidget(self.na_ligand_input)
        self.na_btn = QPushButton("Analyse NA binding")
        self.na_btn.clicked.connect(self._on_analyse_na)
        row.addWidget(self.na_btn)
        row.addStretch(1)
        lay.addLayout(row)
        self.na_table = self._make_table(
            ["Kind", "Ligand atom", "Chain", "Residue",
             "NA atom", "Distance (Å)"])
        lay.addWidget(self.na_table, 1)
        return w

    def _make_table(self, headers: List[str]) -> QTableWidget:
        t = QTableWidget(0, len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setSelectionBehavior(QTableWidget.SelectRows)
        return t

    # -----------------------------------------------------------------
    # Data helpers

    def _populate_seeded(self) -> None:
        try:
            from orgchem.core.protein import list_seeded_proteins
            for row in list_seeded_proteins():
                self.seeded_combo.addItem(
                    f"{row['pdb_id']} — {row['name']}", row["pdb_id"])
        except Exception as e:  # noqa: BLE001
            log.warning("Could not load seeded proteins: %s", e)

    def _refresh_plip_badge(self) -> None:
        try:
            from orgchem.core.plip_bridge import capabilities
            caps = capabilities()
        except Exception:  # noqa: BLE001
            caps = {"available": False}
        if caps.get("available"):
            bits = []
            if caps.get("python_api"):
                bits.append("Python API")
            if caps.get("cli"):
                bits.append("CLI")
            label = "PLIP: " + " + ".join(bits) if bits else "PLIP: yes"
            self.plip_badge.setText(label)
            self.plip_badge.setStyleSheet(
                "padding:2px 8px; border-radius:10px; "
                "background:#dfd; color:#353;")
        else:
            self.plip_badge.setText(
                "PLIP: not installed — using built-in geometry")
            self.plip_badge.setStyleSheet(
                "padding:2px 8px; border-radius:10px; "
                "background:#eef; color:#335;")

    # -----------------------------------------------------------------
    # Slots — fetch

    def _on_seeded_pick(self, idx: int) -> None:
        pid = self.seeded_combo.itemData(idx) or ""
        if pid:
            self.id_input.setText(pid)

    def _on_fetch_pdb(self) -> None:
        pid = self.id_input.text().strip()
        if not pid:
            return
        try:
            from orgchem.sources.pdb import fetch_pdb
            protein = fetch_pdb(pid)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "PDB fetch failed",
                                f"{type(e).__name__}: {e}")
            return
        self._current_pdb = pid.upper()
        self._show_summary(protein.summary())
        self.pdb_loaded.emit(self._current_pdb)
        bus().message_posted.emit("INFO", f"Loaded PDB {pid.upper()}")
        # Auto-render the 3D view so the structure appears immediately.
        try:
            self._on_render_3d()
        except Exception as e:  # noqa: BLE001
            log.warning("3D auto-render failed: %s", e)

    def _on_fetch_alphafold(self) -> None:
        uid = self.id_input.text().strip()
        if not uid:
            return
        try:
            from orgchem.sources.alphafold import fetch_alphafold
            r = fetch_alphafold(uid)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "AlphaFold fetch failed",
                                f"{type(e).__name__}: {e}")
            return
        summary = r.summary()
        self._current_pdb = summary.get("uniprot_id", uid).upper()
        self._show_summary(summary, alphafold=True)
        self.pdb_loaded.emit(self._current_pdb)
        # AlphaFold models ship their pLDDT in the B-factor column —
        # turn on the overlay automatically so students see it.
        self.viewer3d_plddt.setChecked(True)
        try:
            self._on_render_3d()
        except Exception as e:  # noqa: BLE001
            log.warning("3D auto-render failed: %s", e)

    # Slots — analyses

    def _require_loaded(self) -> bool:
        if not self._current_pdb:
            QMessageBox.information(self, "No structure",
                                    "Fetch a PDB (or AlphaFold) first.")
            return False
        return True

    def _on_atom_picked(self, chain: str, resn: str, resi: int) -> None:
        """Update the picked-residue label and nudge the Properties panel."""
        if resn:
            label = f"Picked: {chain}:{resn}{resi}"
        else:
            label = f"Picked: {chain}:{resi}"
        if self.picked_label is not None:
            self.picked_label.setText(label)
        bus().message_posted.emit("INFO", label)

    def _on_render_3d(self) -> None:
        if not self._require_loaded():
            return
        if self.web_3d is None:
            return
        from orgchem.sources.pdb import cached_pdb_path
        from orgchem.render.draw_protein_3d import (
            build_protein_html_from_file,
        )
        p = cached_pdb_path(self._current_pdb)
        if not p.exists():
            QMessageBox.warning(self, "3D structure",
                                f"No cached PDB at {p}")
            return
        # Highlight residues from a prior binding analysis if we have any.
        highlight: List[str] = []
        for row in range(self.contacts_table.rowCount()):
            chain = self.contacts_table.item(row, 2)
            res = self.contacts_table.item(row, 3)
            if chain and res:
                label = f"{chain.text()}:{res.text()}"
                if label not in highlight:
                    highlight.append(label)
        colour_mode = "plddt" if self.viewer3d_plddt.isChecked() else "chain"
        try:
            html = build_protein_html_from_file(
                p,
                protein_style=self.viewer3d_protein_style.currentText(),
                ligand_style=self.viewer3d_ligand_style.currentText(),
                show_waters=self.viewer3d_show_waters.isChecked(),
                show_ligand_surface=self.viewer3d_show_surface.isChecked(),
                highlight_residues=highlight,
                colour_mode=colour_mode,
                enable_picking=True,
                spin=self.viewer3d_spin.isChecked(),
            )
        except FileNotFoundError as e:
            QMessageBox.warning(self, "3D structure", str(e))
            return
        # baseUrl blank so relative paths resolve to nowhere (we inline JS).
        self.web_3d.setHtml(html)
        bus().message_posted.emit(
            "INFO",
            f"3D structure rendered for {self._current_pdb} "
            f"({len(highlight)} residues highlighted)")

    def _on_save_3d_html(self) -> None:
        if not self._require_loaded():
            return
        from orgchem.sources.pdb import cached_pdb_path
        from orgchem.render.draw_protein_3d import (
            build_protein_html_from_file,
        )
        path, _ = QFileDialog.getSaveFileName(
            self, "Save 3D structure HTML",
            f"{self._current_pdb}_3d.html",
            "HTML (*.html)",
        )
        if not path:
            return
        pdb_path = cached_pdb_path(self._current_pdb)
        html = build_protein_html_from_file(
            pdb_path,
            protein_style=self.viewer3d_protein_style.currentText(),
            ligand_style=self.viewer3d_ligand_style.currentText(),
            show_waters=self.viewer3d_show_waters.isChecked(),
            show_ligand_surface=self.viewer3d_show_surface.isChecked(),
            colour_mode="plddt" if self.viewer3d_plddt.isChecked()
                        else "chain",
            spin=self.viewer3d_spin.isChecked(),
        )
        from pathlib import Path as _P
        _P(path).write_text(html, encoding="utf-8")
        bus().message_posted.emit("INFO", f"Saved 3D HTML → {path}")

    def _on_find_pockets(self) -> None:
        if not self._require_loaded():
            return
        from orgchem.sources.pdb import parse_from_cache_or_string
        from orgchem.core.pockets import find_pockets, pockets_summary
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        pockets = find_pockets(protein, top_k=5)
        summary = pockets_summary(pockets)
        self.pockets_table.setRowCount(len(summary["pockets"]))
        for row, p in enumerate(summary["pockets"]):
            cx, cy, cz = p["centre"]
            items = [
                QTableWidgetItem(str(row + 1)),
                QTableWidgetItem(str(p["volume_voxels"])),
                QTableWidgetItem(f"({cx:.1f}, {cy:.1f}, {cz:.1f})"),
                QTableWidgetItem(str(len(p["lining_residues"]))),
            ]
            for col, it in enumerate(items):
                self.pockets_table.setItem(row, col, it)

    def _on_analyse_binding(self) -> None:
        if not self._require_loaded():
            return
        ligand = self.ligand_input.text().strip()
        if not ligand:
            QMessageBox.information(self, "Ligand name",
                                    "Enter a HETATM name first.")
            return
        from orgchem.sources.pdb import parse_from_cache_or_string
        from orgchem.core.binding_contacts import analyse_binding
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        report = analyse_binding(protein, ligand)
        self._populate_contacts_table(report.summary()["contacts"])

    def _on_analyse_binding_plip(self) -> None:
        if not self._require_loaded():
            return
        ligand = self.ligand_input.text().strip()
        if not ligand:
            return
        from orgchem.sources.pdb import (parse_from_cache_or_string,
                                         cached_pdb_path)
        from orgchem.core.plip_bridge import analyse_binding_plip
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        pdb_path = cached_pdb_path(self._current_pdb)
        result = analyse_binding_plip(
            protein, ligand,
            pdb_path=pdb_path if pdb_path.exists() else None,
        )
        self._populate_contacts_table(result.summary()["contacts"])
        bus().message_posted.emit(
            "INFO", f"Analysed {ligand}@{self._current_pdb} via "
                    f"engine={result.engine}")

    def _populate_contacts_table(
            self, contacts: List[Dict[str, Any]]) -> None:
        self.contacts_table.setRowCount(len(contacts))
        for row, c in enumerate(contacts):
            items = [
                QTableWidgetItem(c.get("kind", "")),
                QTableWidgetItem(c.get("ligand_atom", "")),
                QTableWidgetItem(c.get("chain", "")),
                QTableWidgetItem(c.get("residue", "")),
                QTableWidgetItem(f"{c.get('distance', 0):.2f}"),
            ]
            for col, it in enumerate(items):
                self.contacts_table.setItem(row, col, it)

    def _on_export_map(self) -> None:
        if not self._require_loaded():
            return
        ligand = self.ligand_input.text().strip()
        if not ligand:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save interaction map",
            f"{self._current_pdb}_{ligand}.png",
            "PNG image (*.png);;SVG image (*.svg)",
        )
        if not path:
            return
        from orgchem.sources.pdb import parse_from_cache_or_string
        from orgchem.core.binding_contacts import analyse_binding
        from orgchem.render.draw_interaction_map import export_interaction_map
        from orgchem.messaging.errors import RenderError
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        report = analyse_binding(protein, ligand)
        try:
            export_interaction_map(report, path)
        except RenderError as e:
            QMessageBox.warning(self, "Export failed", str(e))
            return
        bus().message_posted.emit("INFO", f"Saved interaction map → {path}")

    def _on_analyse_ppi(self) -> None:
        if not self._require_loaded():
            return
        from orgchem.sources.pdb import parse_from_cache_or_string
        from orgchem.core.ppi import analyse_ppi
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        interfaces = analyse_ppi(protein)
        self.ppi_table.setRowCount(len(interfaces))
        for row, iface in enumerate(interfaces):
            counts: Dict[str, int] = {}
            for c in iface.contacts:
                counts[c.kind] = counts.get(c.kind, 0) + 1
            kind_s = ", ".join(f"{k}:{v}" for k, v in counts.items())
            items = [
                QTableWidgetItem(iface.chain_a),
                QTableWidgetItem(iface.chain_b),
                QTableWidgetItem(str(iface.n_contacts)),
                QTableWidgetItem(kind_s),
            ]
            for col, it in enumerate(items):
                self.ppi_table.setItem(row, col, it)
        if not interfaces:
            QMessageBox.information(
                self, "PPI",
                "No cross-chain contacts detected. "
                "Is this a single-chain protein?")

    def _on_analyse_ppi_pair(self) -> None:
        if not self._require_loaded():
            return
        chain_a = self.ppi_chain_a.currentText().strip()
        chain_b = self.ppi_chain_b.currentText().strip()
        if not chain_a or not chain_b:
            QMessageBox.information(self, "PPI",
                                    "Pick a chain A and chain B first.")
            return
        from orgchem.sources.pdb import parse_from_cache_or_string
        from orgchem.core.ppi import analyse_ppi_pair
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        iface = analyse_ppi_pair(protein, chain_a, chain_b)
        counts: Dict[str, int] = {}
        for c in iface.contacts:
            counts[c.kind] = counts.get(c.kind, 0) + 1
        kind_s = ", ".join(f"{k}:{v}" for k, v in counts.items()) or "—"
        self.ppi_table.setRowCount(1)
        items = [
            QTableWidgetItem(iface.chain_a),
            QTableWidgetItem(iface.chain_b),
            QTableWidgetItem(str(iface.n_contacts)),
            QTableWidgetItem(kind_s),
        ]
        for col, it in enumerate(items):
            self.ppi_table.setItem(0, col, it)
        bus().message_posted.emit(
            "INFO",
            f"PPI {chain_a}↔{chain_b}: {iface.n_contacts} contact(s)")

    def _on_copy_chain_sequence(self) -> None:
        if not self._require_loaded():
            return
        chain_id = self.summary_chain_combo.currentText().strip()
        if not chain_id:
            return
        from orgchem.sources.pdb import parse_from_cache_or_string
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        chain = protein.get_chain(chain_id)
        if chain is None:
            QMessageBox.information(
                self, "Chain sequence",
                f"Chain {chain_id!r} not in {self._current_pdb}. "
                f"Available: {protein.chain_ids}")
            return
        seq = chain.sequence
        from PySide6.QtGui import QGuiApplication
        QGuiApplication.clipboard().setText(seq)
        self.summary_seq_label.setText(seq or "(empty)")
        bus().message_posted.emit(
            "INFO",
            f"Copied {len(seq)}-residue sequence of chain "
            f"{chain_id} from {self._current_pdb} to clipboard")

    def _on_analyse_na(self) -> None:
        if not self._require_loaded():
            return
        ligand = self.na_ligand_input.text().strip()
        if not ligand:
            return
        from orgchem.sources.pdb import parse_from_cache_or_string
        from orgchem.core.na_interactions import analyse_na_binding
        protein = parse_from_cache_or_string(self._current_pdb)
        if protein is None:
            return
        report = analyse_na_binding(protein, ligand)
        contacts = report.summary()["contacts"]
        self.na_table.setRowCount(len(contacts))
        for row, c in enumerate(contacts):
            items = [
                QTableWidgetItem(c.get("kind", "")),
                QTableWidgetItem(c.get("ligand_atom", "")),
                QTableWidgetItem(c.get("chain", "")),
                QTableWidgetItem(c.get("residue", "")),
                QTableWidgetItem(c.get("residue_atom", "")),
                QTableWidgetItem(f"{c.get('distance', 0):.2f}"),
            ]
            for col, it in enumerate(items):
                self.na_table.setItem(row, col, it)
        if not contacts:
            QMessageBox.information(
                self, "NA-ligand",
                "No NA-ligand contacts detected. "
                "Does the structure contain nucleotides?")

    # -----------------------------------------------------------------

    def _show_summary(self, summary: Dict[str, Any],
                      alphafold: bool = False) -> None:
        if alphafold:
            self.summary.setText(
                f"AlphaFold: {summary.get('uniprot_id', '?')} — "
                f"mean pLDDT {summary.get('mean_plddt', 0):.1f} "
                f"({summary.get('confidence', '?')})")
        else:
            self.summary.setText(
                f"{summary.get('pdb_id', '?')} — "
                f"{summary.get('title', '(untitled)')[:80]}"
            )
        self.summary_browser.setPlainText(_format_summary(summary))
        # Populate chain combo boxes for the Summary / PPI tabs.
        chain_ids = summary.get("chain_ids", []) or []
        for combo in (getattr(self, "summary_chain_combo", None),
                      getattr(self, "ppi_chain_a", None),
                      getattr(self, "ppi_chain_b", None)):
            if combo is None:
                continue
            combo.clear()
            for cid in chain_ids:
                combo.addItem(cid, cid)
        # Default the PPI pair to the first two chains if possible.
        if (getattr(self, "ppi_chain_b", None) is not None
                and len(chain_ids) >= 2):
            self.ppi_chain_b.setCurrentIndex(1)
        # Reset sequence label.
        if hasattr(self, "summary_seq_label"):
            self.summary_seq_label.setText("")


def _format_summary(summary: Dict[str, Any]) -> str:
    lines = []
    for key in ("pdb_id", "uniprot_id", "title", "n_chains",
                "chain_ids", "n_residues", "n_atoms", "ligands",
                "mean_plddt", "confidence"):
        if key in summary:
            lines.append(f"{key}: {summary[key]}")
    return "\n".join(lines)
