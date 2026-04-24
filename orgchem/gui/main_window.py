"""Main application window — docks, tabs, menus, status bar."""
from __future__ import annotations
import logging
from typing import Optional

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow, QDockWidget, QTabWidget, QSplitter, QWidget, QVBoxLayout,
    QMessageBox, QLabel, QStatusBar,
)

from orgchem.config import AppConfig
from orgchem.messaging.bus import bus
from orgchem.agent.controller import set_main_window
from orgchem.gui.panels.molecule_browser import MoleculeBrowserPanel
from orgchem.gui.panels.viewer_2d import Viewer2DPanel
from orgchem.gui.panels.viewer_3d import Viewer3DPanel
from orgchem.gui.panels.properties import PropertiesPanel
from orgchem.gui.panels.session_log import SessionLogPanel
from orgchem.gui.panels.tutorial_panel import TutorialPanel
from orgchem.gui.panels.search_panel import SearchPanel
from orgchem.gui.panels.tutor_panel import TutorPanel
from orgchem.gui.dialogs.import_smiles import ImportSmilesDialog
from orgchem.gui.dialogs.formula_calculator import FormulaCalculatorDialog
from orgchem.gui.dialogs.hrms_guesser import HRMSGuesserDialog
from orgchem.gui.dialogs.ms_fragments import MSFragmentsDialog
from orgchem.gui.dialogs.retrosynthesis import RetrosynthesisDialog
from orgchem.gui.dialogs.orbitals import OrbitalsDialog
from orgchem.gui.dialogs.lab_techniques import LabTechniquesDialog
from orgchem.gui.dialogs.medchem import MedChemDialog
from orgchem.gui.dialogs.naming_rules import NamingRulesDialog
from orgchem.gui.dialogs.periodic_table import PeriodicTableDialog
from orgchem.gui.dialogs.spectroscopy import SpectroscopyDialog
from orgchem.gui.dialogs.stereo import StereoDialog
from orgchem.gui.dialogs.green_metrics import GreenMetricsDialog
from orgchem.gui.dialogs.preferences import PreferencesDialog

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, cfg: AppConfig):
        super().__init__()
        self.cfg = cfg
        self.setWindowTitle("OrgChem Studio")
        # Fit 13"/14" MBP (usable height ~820 px after menu bar / dock).
        # Users can resize up on larger displays.
        self.resize(1280, 780)
        self.setMinimumSize(960, 640)
        self._build_central()
        self._build_docks()
        # Snapshot the pristine layout *before* any user customisation
        # is restored — so "Reset layout" has something to fall back to.
        self._default_window_state = self.saveState()
        self._default_geometry = self.saveGeometry()
        self._build_menus()
        self._build_status()
        self._connect_bus()
        set_main_window(self)
        self._restore_geometry()
        log.info("Main window ready")

    # ---------------- layout ------------------------------------------

    def _build_central(self) -> None:
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)

        # Molecule Workspace: 2D | 3D
        mol_tab = QWidget()
        mv = QVBoxLayout(mol_tab)
        mv.setContentsMargins(2, 2, 2, 2)
        split = QSplitter(Qt.Horizontal)
        self.viewer_2d = Viewer2DPanel()
        self.viewer_3d = Viewer3DPanel(self.cfg)
        split.addWidget(self.viewer_2d)
        split.addWidget(self.viewer_3d)
        split.setSizes([500, 500])
        mv.addWidget(split)
        self.tabs.addTab(mol_tab, "Molecule Workspace")

        # Workbench (Phase 32b) — scriptable scene composer.
        from orgchem.gui.panels.workbench import WorkbenchWidget
        self.workbench = WorkbenchWidget(parent=self)
        self.workbench.detach_requested.connect(self._detach_workbench)
        self.workbench.reattach_requested.connect(self._reattach_workbench)
        self.tabs.addTab(self.workbench, "Workbench")
        self._workbench_window = None  # filled when detached

        # Tutorials
        self.tutorial_panel = TutorialPanel()
        self.tabs.addTab(self.tutorial_panel, "Tutorials")

        # Reactions (replaces the former "Reactions — Phase 2" stub)
        from orgchem.gui.panels.reaction_workspace import ReactionWorkspacePanel
        self.reactions = ReactionWorkspacePanel()
        self.tabs.addTab(self.reactions, "Reactions")

        # Compare (replaces the former "Multi-molecule comparison" stub)
        from orgchem.gui.panels.compare_panel import ComparePanel
        self.compare = ComparePanel()
        self.tabs.addTab(self.compare, "Compare")

        # Synthesis (Phase 8) — multi-step routes to target molecules.
        from orgchem.gui.panels.synthesis_workspace import SynthesisWorkspacePanel
        self.synthesis = SynthesisWorkspacePanel()
        self.tabs.addTab(self.synthesis, "Synthesis")

        # Glossary (Phase 11b) — searchable dictionary of terms.
        from orgchem.gui.panels.glossary_panel import GlossaryPanel
        self.glossary = GlossaryPanel()
        self.tabs.addTab(self.glossary, "Glossary")

        # Phase 30 — Macromolecules (Proteins / Carbohydrates /
        # Lipids / Nucleic-acids) live in a dedicated secondary
        # window rather than the main-window tabbar. The panels are
        # still constructed here so that (a) cross-cutting attributes
        # like ``win.proteins`` stay available to agent actions and
        # other panels, and (b) the window opens instantly on first
        # menu click without building panels on the hot path.
        from orgchem.gui.panels.protein_panel import ProteinPanel
        from orgchem.gui.panels.carbohydrates_panel import CarbohydratesPanel
        from orgchem.gui.panels.lipids_panel import LipidsPanel
        from orgchem.gui.panels.nucleic_acids_panel import NucleicAcidsPanel
        self.proteins = ProteinPanel()
        self.carbohydrates = CarbohydratesPanel()
        self.lipids = LipidsPanel()
        self.nucleic_acids = NucleicAcidsPanel()
        self._macromolecules_window: Optional[QMainWindow] = None

        self.setCentralWidget(self.tabs)

    def _build_docks(self) -> None:
        # Left column: molecule browser + online search
        self.browser = MoleculeBrowserPanel()
        self.search = SearchPanel()
        d_browse = QDockWidget("Molecules", self)
        d_browse.setObjectName("dock_molecules")
        d_browse.setWidget(self.browser)
        self.addDockWidget(Qt.LeftDockWidgetArea, d_browse)
        d_search = QDockWidget("Search / Download", self)
        d_search.setObjectName("dock_search")
        d_search.setWidget(self.search)
        self.addDockWidget(Qt.LeftDockWidgetArea, d_search)
        self.tabifyDockWidget(d_browse, d_search)
        d_browse.raise_()

        # Right column: properties
        self.props = PropertiesPanel()
        d_props = QDockWidget("Properties", self)
        d_props.setObjectName("dock_properties")
        d_props.setWidget(self.props)
        self.addDockWidget(Qt.RightDockWidgetArea, d_props)

        # Right column (tabbed under properties): Tutor chat console
        self.tutor = TutorPanel(self.cfg)
        d_tutor = QDockWidget("Tutor (chat)", self)
        d_tutor.setObjectName("dock_tutor")
        d_tutor.setWidget(self.tutor)
        d_tutor.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable
            | QDockWidget.DockWidgetClosable
        )
        self.addDockWidget(Qt.RightDockWidgetArea, d_tutor)
        self.tabifyDockWidget(d_props, d_tutor)
        d_props.raise_()

        # Bottom: session log — compact by default, toggleable via View menu.
        self.session_log = SessionLogPanel()
        d_log = QDockWidget("Session Log", self)
        d_log.setObjectName("dock_session_log")
        d_log.setWidget(self.session_log)
        self.addDockWidget(Qt.BottomDockWidgetArea, d_log)
        self.resizeDocks([d_log], [110], Qt.Vertical)

        self._docks = [d_browse, d_search, d_props, d_tutor, d_log]

    def _build_menus(self) -> None:
        mb = self.menuBar()

        m_file = mb.addMenu("&File")
        a_import = QAction("Import SMILES…", self)
        a_import.setShortcut(QKeySequence("Ctrl+I"))
        a_import.triggered.connect(self._on_import_smiles)
        m_file.addAction(a_import)
        m_file.addSeparator()
        a_export_2d = QAction("Export current molecule (2D)…", self)
        a_export_2d.setShortcut(QKeySequence("Ctrl+E"))
        a_export_2d.triggered.connect(self._on_export_2d)
        m_file.addAction(a_export_2d)
        a_screenshot = QAction("Screenshot window…", self)
        a_screenshot.setShortcut(QKeySequence("Ctrl+Shift+P"))
        a_screenshot.triggered.connect(self._on_screenshot)
        m_file.addAction(a_screenshot)
        m_file.addSeparator()
        a_save_session = QAction("Save session…", self)
        a_save_session.setShortcut(QKeySequence("Ctrl+S"))
        a_save_session.triggered.connect(self._on_save_session)
        m_file.addAction(a_save_session)
        a_load_session = QAction("Load session…", self)
        a_load_session.setShortcut(QKeySequence("Ctrl+Shift+O"))
        a_load_session.triggered.connect(self._on_load_session)
        m_file.addAction(a_load_session)
        self._recent_menu = m_file.addMenu("Recent sessions")
        self._rebuild_recent_sessions_menu()
        m_file.addSeparator()
        a_quit = QAction("&Quit", self)
        a_quit.setShortcut(QKeySequence.Quit)
        a_quit.triggered.connect(self.close)
        m_file.addAction(a_quit)

        m_view = mb.addMenu("&View")
        for d in self._docks:
            m_view.addAction(d.toggleViewAction())
        m_view.addSeparator()
        a_reset_layout = QAction("Reset layout to default", self)
        a_reset_layout.setShortcut(QKeySequence("Ctrl+Shift+R"))
        a_reset_layout.setToolTip(
            "Snap every panel and dock back to the pristine layout. "
            "Useful if you've detached something into an odd position."
        )
        a_reset_layout.triggered.connect(self.reset_layout_to_default)
        m_view.addAction(a_reset_layout)
        a_palette = QAction("Command palette…", self)
        a_palette.setShortcut(QKeySequence("Ctrl+K"))
        a_palette.setToolTip(
            "Type a glossary term, reaction, or molecule name and "
            "jump straight to it. Works from anywhere in the app."
        )
        a_palette.triggered.connect(self.open_command_palette)
        m_view.addAction(a_palette)

        a_find = QAction("Find…", self)
        a_find.setShortcut(QKeySequence("Ctrl+F"))
        a_find.setToolTip(
            "Full-text search every molecule / reaction / pathway "
            "/ glossary term / mechanism step (Phase 33b).  "
            "Matches titles AND descriptions, not just names."
        )
        a_find.triggered.connect(self.open_fulltext_search)
        m_view.addAction(a_find)

        m_tools = mb.addMenu("&Tools")
        a_formula = QAction("Empirical / Molecular Formula Calculator…", self)
        a_formula.triggered.connect(self._on_formula_calc)
        m_tools.addAction(a_formula)
        a_hrms = QAction("HRMS formula candidate guesser…", self)
        a_hrms.triggered.connect(self._on_hrms_guesser)
        m_tools.addAction(a_hrms)
        a_ms_frag = QAction("EI-MS fragmentation sketch…", self)
        a_ms_frag.triggered.connect(self._on_ms_fragments)
        m_tools.addAction(a_ms_frag)
        a_retro = QAction("Retrosynthesis…", self)
        a_retro.triggered.connect(self._on_retrosynthesis)
        m_tools.addAction(a_retro)
        a_orbitals = QAction("Orbitals (Hückel / W-H)…", self)
        a_orbitals.triggered.connect(self._on_orbitals)
        m_tools.addAction(a_orbitals)
        a_lab = QAction("Lab techniques…", self)
        a_lab.triggered.connect(self._on_lab_techniques)
        m_tools.addAction(a_lab)
        a_medchem = QAction("Medicinal chemistry (SAR / Bioisosteres)…", self)
        a_medchem.triggered.connect(self._on_medchem)
        m_tools.addAction(a_medchem)
        a_naming = QAction("IUPAC naming rules…", self)
        a_naming.triggered.connect(self._on_naming_rules)
        m_tools.addAction(a_naming)
        a_periodic = QAction("Periodic table…", self)
        a_periodic.setShortcut(QKeySequence("Ctrl+Shift+T"))
        a_periodic.triggered.connect(self._on_periodic_table)
        m_tools.addAction(a_periodic)
        a_spectro = QAction("Spectroscopy (IR / NMR / MS)…", self)
        a_spectro.triggered.connect(self._on_spectroscopy)
        m_tools.addAction(a_spectro)
        a_stereo = QAction("Stereochemistry…", self)
        a_stereo.triggered.connect(self._on_stereo)
        m_tools.addAction(a_stereo)
        a_green = QAction("Green metrics (atom economy)…", self)
        a_green.triggered.connect(self._on_green_metrics)
        m_tools.addAction(a_green)
        m_tools.addSeparator()
        a_script = QAction("Script editor (Python)…", self)
        a_script.setShortcut(QKeySequence("Ctrl+Shift+E"))
        a_script.setToolTip(
            "Open a Python REPL that can drive any registered action "
            "— Phase 32a scripting workbench foundation."
        )
        a_script.triggered.connect(self._on_script_editor)
        m_tools.addAction(a_script)
        a_draw = QAction("Drawing tool…", self)
        a_draw.setShortcut(QKeySequence("Ctrl+Shift+D"))
        a_draw.setToolTip(
            "Open the molecular drawing canvas (Phase 36) — draw a "
            "structure and send it to the Molecule Workspace or "
            "export PNG / SVG / MOL."
        )
        a_draw.triggered.connect(self._on_drawing_tool)
        m_tools.addAction(a_draw)
        m_tools.addSeparator()
        a_prefs = QAction("Preferences…", self)
        a_prefs.setShortcut(QKeySequence("Ctrl+,"))
        a_prefs.setMenuRole(QAction.PreferencesRole)  # macOS App menu
        a_prefs.triggered.connect(self._on_preferences)
        m_tools.addAction(a_prefs)

        m_window = mb.addMenu("&Window")
        a_work = QAction("Workbench…", self)
        a_work.setShortcut(QKeySequence("Ctrl+Shift+B"))
        a_work.setToolTip(
            "Focus the Workbench — scene composer driven by the "
            "Script Editor and the tutor. Detach to a floating "
            "window from its toolbar."
        )
        a_work.triggered.connect(self.open_workbench)
        m_window.addAction(a_work)
        a_macro = QAction("Macromolecules…", self)
        a_macro.setShortcut(QKeySequence("Ctrl+Shift+M"))
        a_macro.setToolTip(
            "Open the Macromolecules window — proteins, carbohydrates, "
            "lipids, and nucleic acids in one place."
        )
        a_macro.triggered.connect(self.open_macromolecules_window)
        m_window.addAction(a_macro)

        m_tutor = mb.addMenu("T&utor")
        a_focus_tutor = QAction("Open chat console", self)
        a_focus_tutor.triggered.connect(lambda: self.tutor.setFocus())
        m_tutor.addAction(a_focus_tutor)

        m_help = mb.addMenu("&Help")
        a_about = QAction("About", self)
        a_about.triggered.connect(self._on_about)
        m_help.addAction(a_about)

    def _build_status(self) -> None:
        sb = QStatusBar()
        self._status_label = QLabel("Ready")
        sb.addWidget(self._status_label)
        self.setStatusBar(sb)

    # ---------------- bus ---------------------------------------------

    def _connect_bus(self) -> None:
        bus().message_posted.connect(self._on_message)
        bus().molecule_selected.connect(self._on_mol_selected)

    def _on_message(self, level: str, text: str) -> None:
        if level in ("ERROR", "CRITICAL"):
            self._status_label.setText(text.splitlines()[0][:120])

    def _on_mol_selected(self, mol_id: int) -> None:
        self._status_label.setText(f"Selected molecule id {mol_id}")
        self.tabs.setCurrentIndex(0)

    # ---------------- windows ----------------------------------------

    def open_macromolecules_window(self, tab_label: Optional[str] = None):
        """Show (and raise) the Macromolecules window. Lazily
        constructs on first call. Optional ``tab_label`` focuses a
        specific inner tab (``"Proteins"`` / ``"Carbohydrates"`` /
        ``"Lipids"`` / ``"Nucleic acids"``). Returns the window so
        callers / agent actions can introspect it."""
        from orgchem.gui.windows.macromolecules_window import (
            MacromoleculesWindow,
        )
        if self._macromolecules_window is None:
            panels = {
                MacromoleculesWindow.TAB_PROTEINS: self.proteins,
                MacromoleculesWindow.TAB_CARBOHYDRATES: self.carbohydrates,
                MacromoleculesWindow.TAB_LIPIDS: self.lipids,
                MacromoleculesWindow.TAB_NUCLEIC_ACIDS: self.nucleic_acids,
            }
            self._macromolecules_window = MacromoleculesWindow(
                panels, parent=self,
            )
        win = self._macromolecules_window
        if tab_label:
            win.switch_to(tab_label)
        win.show()
        win.raise_()
        win.activateWindow()
        return win

    def open_command_palette(self):
        """Show the Ctrl+K command palette (Phase 11b follow-up).
        Lazily imports so the dialog's DB probe only runs when the
        user actually invokes it."""
        from orgchem.gui.dialogs.command_palette import (
            CommandPaletteDialog,
        )
        dlg = CommandPaletteDialog(self)
        dlg.exec()
        return dlg

    def open_fulltext_search(self):
        """Show the Ctrl+F full-text search dialog (Phase 33b).
        Singleton — reopening the dialog brings the existing
        window forward so the user can keep refining a query."""
        from orgchem.gui.dialogs.fulltext_search import (
            FulltextSearchDialog,
        )
        dlg = FulltextSearchDialog.singleton(parent=self)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        dlg._query.setFocus()
        return dlg

    # ---------------- actions -----------------------------------------

    def _on_import_smiles(self) -> None:
        ImportSmilesDialog(self).exec()

    def _on_formula_calc(self) -> None:
        FormulaCalculatorDialog(self).exec()

    def _on_hrms_guesser(self) -> None:
        HRMSGuesserDialog(self).exec()

    def _on_ms_fragments(self) -> None:
        MSFragmentsDialog(self).exec()

    def _on_retrosynthesis(self) -> None:
        RetrosynthesisDialog(self).exec()

    def _on_orbitals(self) -> None:
        OrbitalsDialog(self).exec()

    def _on_lab_techniques(self) -> None:
        LabTechniquesDialog(self).exec()

    def _on_medchem(self) -> None:
        MedChemDialog(self).exec()

    def _on_naming_rules(self) -> None:
        NamingRulesDialog(self).exec()

    def _on_periodic_table(self) -> None:
        PeriodicTableDialog(self).exec()

    def _on_spectroscopy(self) -> None:
        SpectroscopyDialog(self).exec()

    def _on_stereo(self) -> None:
        StereoDialog(self).exec()

    def _on_green_metrics(self) -> None:
        GreenMetricsDialog(self).exec()

    def _on_script_editor(self) -> None:
        """Open the Phase 32a script editor / REPL (singleton, non-modal)."""
        from orgchem.gui.dialogs.script_editor import ScriptEditorDialog

        dlg = ScriptEditorDialog.singleton(parent=self)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def _on_drawing_tool(self) -> None:
        """Open the Phase 36 molecular drawing tool (singleton, modeless)."""
        from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog

        dlg = DrawingToolDialog.singleton(parent=self)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    # ------------------------------------------------------------------
    # Workbench placement (Phase 32b hybrid)

    def _detach_workbench(self) -> None:
        """Move the Workbench widget out of the tabbar and into a
        standalone top-level :class:`WorkbenchWindow`."""
        from orgchem.gui.windows.workbench_window import WorkbenchWindow

        if self._workbench_window is not None:
            # Already detached — just raise it.
            self._workbench_window.raise_()
            self._workbench_window.activateWindow()
            return

        idx = self.tabs.indexOf(self.workbench)
        if idx >= 0:
            self.tabs.removeTab(idx)

        self.workbench.set_mode(detached=True)
        win = WorkbenchWindow(self.workbench, parent=self)
        win.reattach_requested.connect(self._reattach_workbench)
        win.closed_by_user.connect(self._reattach_workbench)
        win.show()
        self._workbench_window = win

    def _reattach_workbench(self) -> None:
        """Pull the Workbench widget back into the main tabbar."""
        if self._workbench_window is None:
            return
        win = self._workbench_window
        self._workbench_window = None
        try:
            win.takeCentralWidget()
        except Exception:
            pass
        self.workbench.setParent(self.tabs)
        # Always re-insert at index 1, i.e. right after Molecule Workspace.
        self.tabs.insertTab(1, self.workbench, "Workbench")
        self.workbench.set_mode(detached=False)
        try:
            win.close()
        except Exception:
            pass
        self.tabs.setCurrentWidget(self.workbench)

    def open_workbench(self) -> None:
        """Focus the Workbench tab (or raise the detached window
        if it's separated)."""
        if self._workbench_window is not None:
            self._workbench_window.raise_()
            self._workbench_window.activateWindow()
            return
        self.tabs.setCurrentWidget(self.workbench)

    def _on_preferences(self) -> None:
        PreferencesDialog(self.cfg, self).exec()

    # ------------------------------------------------------------------
    # Session save / restore (Phase 20d)

    def capture_session_state(self, name: str = "session"):
        """Snapshot the current app state into a SessionState dataclass."""
        from orgchem.core.session_state import SessionState
        active_idx = self.tabs.currentIndex()
        active_tab = self.tabs.tabText(active_idx) if active_idx >= 0 else ""
        pdb = getattr(self.proteins, "_current_pdb", "") or ""
        ligand = self.proteins.ligand_input.text().strip() \
            if hasattr(self, "proteins") else ""
        na_lig = self.proteins.na_ligand_input.text().strip() \
            if hasattr(self, "proteins") else ""
        return SessionState(
            name=name,
            active_tab=active_tab,
            protein_pdb_id=pdb,
            protein_ligand_name=ligand,
            na_ligand_name=na_lig,
        )

    def apply_session_state(self, state) -> None:
        """Best-effort restore of a loaded :class:`SessionState`.

        Silently skips fields whose target widget has vanished (e.g.
        a future reshuffle of tabs).
        """
        if state.active_tab:
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == state.active_tab:
                    self.tabs.setCurrentIndex(i)
                    break
        if state.protein_pdb_id and hasattr(self, "proteins"):
            self.proteins.id_input.setText(state.protein_pdb_id)
        if state.protein_ligand_name and hasattr(self, "proteins"):
            self.proteins.ligand_input.setText(state.protein_ligand_name)
        if state.na_ligand_name and hasattr(self, "proteins"):
            self.proteins.na_ligand_input.setText(state.na_ligand_name)
        bus().message_posted.emit("INFO", f"Loaded session '{state.name}'")

    def _on_save_session(self) -> None:
        from PySide6.QtWidgets import QInputDialog, QFileDialog
        from orgchem.core.session_state import (
            save_session, default_session_path,
        )
        name, ok = QInputDialog.getText(
            self, "Save session", "Session name:", text="session")
        if not ok or not name.strip():
            return
        state = self.capture_session_state(name.strip())
        path = default_session_path(name.strip())
        save_session(state, path)
        self._rebuild_recent_sessions_menu()
        bus().message_posted.emit("INFO", f"Saved session → {path}")

    def _on_load_session(self) -> None:
        from PySide6.QtWidgets import QFileDialog
        from orgchem.core.session_state import load_session, sessions_dir
        path, _ = QFileDialog.getOpenFileName(
            self, "Load session", str(sessions_dir()),
            "Session YAML (*.yaml *.yml)",
        )
        if not path:
            return
        try:
            state = load_session(path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Load session",
                                f"{type(e).__name__}: {e}")
            return
        self.apply_session_state(state)

    def _rebuild_recent_sessions_menu(self) -> None:
        from orgchem.core.session_state import list_sessions
        m = getattr(self, "_recent_menu", None)
        if m is None:
            return
        m.clear()
        rows = list_sessions()
        if not rows:
            placeholder = QAction("(no saved sessions)", self)
            placeholder.setEnabled(False)
            m.addAction(placeholder)
            return
        for row in rows[:10]:
            label = f"{row['name']}  —  {row['saved_at'][:16]}"
            act = QAction(label, self)
            path = row["path"]
            act.triggered.connect(lambda _=False, p=path: self._open_recent(p))
            m.addAction(act)

    def _open_recent(self, path: str) -> None:
        from orgchem.core.session_state import load_session
        try:
            state = load_session(path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Load session",
                                f"{type(e).__name__}: {e}")
            return
        self.apply_session_state(state)

    # ------------------------------------------------------------------
    # Geometry persistence

    def _settings(self) -> QSettings:
        return QSettings("OrgChem", "OrgChem Studio")

    def _restore_geometry(self) -> None:
        s = self._settings()
        geom = s.value("mainwindow/geometry")
        if geom is not None:
            self.restoreGeometry(geom)
        state = s.value("mainwindow/windowState")
        if state is not None:
            self.restoreState(state)

    def closeEvent(self, event) -> None:  # noqa: N802 — Qt override
        s = self._settings()
        s.setValue("mainwindow/geometry", self.saveGeometry())
        s.setValue("mainwindow/windowState", self.saveState())
        super().closeEvent(event)

    # ------------------------------------------------------------------
    # Reset layout (View → Reset layout to default)

    def reset_layout_to_default(self) -> None:
        """Snap all docks / panels back to the pristine layout captured
        at startup, and clear the persisted QSettings overrides so the
        reset survives the next launch."""
        if hasattr(self, "_default_window_state") and self._default_window_state is not None:
            self.restoreState(self._default_window_state)
        if hasattr(self, "_default_geometry") and self._default_geometry is not None:
            # Only reset size, not position — respect the user's monitor choice.
            self.resize(1280, 780)
        # Drop the persisted state so a subsequent launch won't
        # re-apply the old layout.
        s = self._settings()
        s.remove("mainwindow/windowState")
        log.info("Layout reset to default; saved-state cleared.")
        self._status_label.setText("Layout reset to default")

    def _on_about(self) -> None:
        QMessageBox.about(
            self, "About OrgChem Studio",
            "<h3>OrgChem Studio</h3>"
            "<p>An interactive organic chemistry learning & teaching environment.</p>"
            "<p>Built on RDKit, PySide6, and 3Dmol.js. Pluggable LLM tutor "
            "(Anthropic / OpenAI / Ollama).</p>")

    def _on_export_2d(self) -> None:
        from PySide6.QtWidgets import QFileDialog
        from orgchem.render.export import export_molecule_2d
        from orgchem.core.formats import mol_from_smiles
        smiles = getattr(self.viewer_2d, "_current_smiles", None)
        if not smiles:
            QMessageBox.information(self, "Nothing to export",
                                    "Select a molecule before exporting.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export 2D structure", "molecule.png",
            "PNG image (*.png);;SVG vector (*.svg);;JPEG (*.jpg)")
        if not path:
            return
        try:
            export_molecule_2d(mol_from_smiles(smiles), path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Export failed", str(e))

    def _on_screenshot(self) -> None:
        from PySide6.QtWidgets import QFileDialog
        from orgchem.render.screenshot import grab_widget
        path, _ = QFileDialog.getSaveFileName(
            self, "Save screenshot", "orgchem_screenshot.png", "PNG (*.png)")
        if not path:
            return
        try:
            grab_widget(self, path)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "Screenshot failed", str(e))
