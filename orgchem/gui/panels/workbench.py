"""Phase 32b — Workbench panel.

Standalone ``QWidget`` that hosts a 3Dmol.js ``QWebEngineView`` plus
a right-side tracks list and a toolbar.  Reparentable between the
main-tabbar (default) and a detached ``QMainWindow``
(``WorkbenchWindow``) via the Detach / Reattach buttons.

Listens to ``orgchem.scene.current_scene()`` for mutations; any
script that calls ``viewer.add_molecule(...)`` updates this panel
automatically.  The page rebuild is stateless — every scene
mutation regenerates the full HTML document.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMessageBox, QPushButton, QSplitter, QToolBar, QVBoxLayout, QWidget,
)

from orgchem.gui.panels.workbench_track_row import TrackRow
from orgchem.scene import Scene, SceneEvent, Track, current_scene
from orgchem.scene.html import build_scene_html

log = logging.getLogger(__name__)


class WorkbenchWidget(QWidget):
    """Workbench view + track list.  Reparentable: tab in the main
    window by default, detachable to a standalone
    :class:`WorkbenchWindow` via the toolbar button.

    Signals:
        detach_requested()  — emitted when the user clicks "Detach".
        reattach_requested() — emitted when the user clicks
                               "Reattach" (only meaningful while
                               inside a WorkbenchWindow).
    """

    detach_requested = Signal()
    reattach_requested = Signal()

    #: Internal signal used to marshal Scene events from a worker
    #: thread (e.g. the Script Editor's ``_RunWorker``) back onto
    #: the GUI thread.  Connected with ``Qt.QueuedConnection`` so
    #: emissions from any thread are automatically queued onto the
    #: main-thread event loop before the slot runs.  **Crucial** —
    #: without this, scripts that call ``viewer.add_molecule(...)``
    #: from their worker thread crash the app with SIGTRAP when the
    #: slot tries to touch Qt widgets (reported by the user 2026-
    #: 04-23 round 67 after demo 02 crashed).  Same class of bug as
    #: the NSWindow fix in rounds 55-57.
    _scene_event_queued = Signal(object, object)

    #: A burst of scene events (e.g. a script that adds six molecules
    #: in a row) used to thrash Chromium: each ``setHtml`` torn down
    #: and rebuilt a WebGL context, which on macOS tripped the Metal
    #: compositor into "returned null texture" → SIGTRAP.  We debounce
    #: rebuilds so a rapid burst of SceneEvents coalesces into a
    #: single HTML load after this quiet period (ms).  50 ms is
    #: imperceptible in interactive use but is long enough for a
    #: tight ``for _ in …: viewer.add_molecule(…)`` loop to complete.
    _REBUILD_DEBOUNCE_MS = 50

    #: Optional instrumentation — tests can watch this counter to
    #: verify debouncing actually collapsed a burst of events.
    rebuild_count: int = 0

    def __init__(self, scene: Optional[Scene] = None,
                 parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._scene = scene or current_scene()
        self._view: Optional[QWebEngineView] = None
        self._tracks_list: Optional[QListWidget] = None
        self._status: Optional[QLabel] = None
        self._detach_action: Optional[QAction] = None
        self._reattach_action: Optional[QAction] = None
        self._rebuild_pending: bool = False
        self._rebuild_timer: Optional[QTimer] = None
        #: Dark / light scene background — toggled by the toolbar
        #: button; fed into ``build_scene_html(background=…)``.
        self._background: str = "#1e1e1e"

        self._build_ui()
        # Thread-safe scene → GUI bridge. The listener runs on
        # whichever thread emitted the event; the slot always runs
        # on the GUI thread because of Qt.QueuedConnection.
        self._scene_event_queued.connect(
            self._handle_scene_event_main,
            Qt.QueuedConnection,
        )
        self._unsubscribe = self._scene.listen(self._on_scene_event)
        # Prime the view — initial state is always rendered, never
        # debounced, so a freshly-opened Workbench always shows
        # whatever was already in the Scene.
        self._do_rebuild()
        self._refresh_tracks_list()

    # ---- public hooks for reparenting ---------------------------
    def set_mode(self, *, detached: bool) -> None:
        """Toggle which toolbar action is visible: Detach (when
        attached to the main tabbar) vs Reattach (when hosted in
        :class:`WorkbenchWindow`)."""
        if self._detach_action is not None:
            self._detach_action.setVisible(not detached)
        if self._reattach_action is not None:
            self._reattach_action.setVisible(detached)

    def scene(self) -> Scene:
        return self._scene

    def grab_png(self, path: Path) -> Path:
        """Snapshot-to-PNG entrypoint used by ``scene.snapshot(path)``.

        Uses :py:meth:`QWidget.grab` — works with Qt's offscreen
        platform and doesn't require the widget to be visible.
        """
        path = Path(path)
        pix: QPixmap = self.grab()
        path.parent.mkdir(parents=True, exist_ok=True)
        ok = pix.save(str(path), "PNG")
        if not ok:
            raise RuntimeError(f"failed to write snapshot: {path}")
        return path

    # ---- UI construction ----------------------------------------
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Toolbar
        tb = QToolBar(self)
        tb.setIconSize(QSize(16, 16))

        self._detach_action = QAction("Detach as window", self)
        self._detach_action.setToolTip(
            "Move the Workbench into its own top-level window "
            "(keeps the same Scene; Script Editor still drives it)."
        )
        self._detach_action.triggered.connect(self.detach_requested.emit)
        tb.addAction(self._detach_action)

        self._reattach_action = QAction("Reattach as tab", self)
        self._reattach_action.setToolTip(
            "Close the detached window and put the Workbench back "
            "into the main tabbar."
        )
        self._reattach_action.triggered.connect(self.reattach_requested.emit)
        self._reattach_action.setVisible(False)
        tb.addAction(self._reattach_action)

        tb.addSeparator()

        a_fit = QAction("Fit to view", self)
        a_fit.setToolTip(
            "Re-zoom the camera so every visible track fits in view "
            "— useful after adding or hiding tracks.")
        a_fit.triggered.connect(self._on_fit_clicked)
        tb.addAction(a_fit)

        a_bg = QAction("Toggle bg", self)
        a_bg.setToolTip(
            "Swap the scene background between dark (#1e1e1e) and "
            "light (#ffffff).  Useful for screenshot contrast.")
        a_bg.triggered.connect(self._on_toggle_background)
        tb.addAction(a_bg)

        tb.addSeparator()

        a_clear = QAction("Clear scene", self)
        a_clear.setToolTip("Remove every track from the scene.")
        a_clear.triggered.connect(self._on_clear_clicked)
        tb.addAction(a_clear)

        a_snap = QAction("Snapshot PNG…", self)
        a_snap.setToolTip("Save the current view as a PNG file.")
        a_snap.triggered.connect(self._on_snapshot_clicked)
        tb.addAction(a_snap)

        a_export = QAction("Export HTML…", self)
        a_export.setToolTip(
            "Save the current scene as a standalone .html file — "
            "shareable, works in any browser (3Dmol.js is inlined).")
        a_export.triggered.connect(self._on_export_html_clicked)
        tb.addAction(a_export)

        root.addWidget(tb)

        # Main body: web view (left) + tracks list (right)
        split = QSplitter(Qt.Horizontal, self)
        self._view = QWebEngineView(self)
        split.addWidget(self._view)

        right = QWidget(self)
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(6, 6, 6, 6)
        right_lay.addWidget(QLabel("Tracks:"))
        self._tracks_list = QListWidget(right)
        # Each row uses a custom TrackRow widget with inline
        # checkbox / style combo / remove button — double-click to
        # remove stays as a backup gesture.
        self._tracks_list.itemDoubleClicked.connect(
            self._on_track_double_clicked)
        right_lay.addWidget(self._tracks_list, 1)
        hint = QLabel(
            "<small>Per-row: ☑︎ toggle visibility, style combo "
            "restyles, ✕ removes.<br>"
            "Drive the scene from "
            "<b>Tools → Script editor…</b> (Ctrl+Shift+E):<br>"
            "<tt>viewer.add_molecule('CCO')</tt></small>")
        hint.setWordWrap(True)
        right_lay.addWidget(hint)
        split.addWidget(right)
        split.setSizes([700, 260])
        root.addWidget(split, 1)

        # Status strip
        self._status = QLabel("")
        self._status.setStyleSheet("color: #666; padding: 2px 6px;")
        root.addWidget(self._status)

    # ---- scene events -------------------------------------------
    def _on_scene_event(self, ev: SceneEvent,
                        track: Optional[Track]) -> None:
        """Scene-listener callback — may run on ANY thread.

        We do zero Qt work here.  Instead we emit the
        ``_scene_event_queued`` signal, which Qt hands off to the
        main-thread event loop via its ``QueuedConnection``.  The
        actual widget updates happen in
        :meth:`_handle_scene_event_main` — always on the GUI thread,
        regardless of which worker thread mutated the Scene.
        """
        self._scene_event_queued.emit(ev, track)

    def _handle_scene_event_main(self, ev: SceneEvent,
                                 track: Optional[Track]) -> None:
        """Slot — always runs on the main / GUI thread."""
        # Tracks list + status label are Qt-only and cheap — update
        # them on every event so the right-side panel stays in sync.
        self._refresh_tracks_list()
        n = len(self._scene.tracks())
        plural = "" if n == 1 else "s"
        self._status.setText(f"{n} track{plural}")
        # The expensive part (rebuilding the whole 3Dmol.js HTML
        # page + spinning up a new WebGL context) gets debounced so
        # burst scripts don't thrash the Metal / Graphite compositor.
        self._schedule_rebuild()

    def _schedule_rebuild(self) -> None:
        """Coalesce rapid scene events into a single `_do_rebuild`.

        Uses a single-shot QTimer with ``_REBUILD_DEBOUNCE_MS``
        so subsequent events before the timer fires just extend
        the quiet window rather than piling up.
        """
        if self._view is None:
            return
        if self._rebuild_pending and self._rebuild_timer is not None:
            # Already scheduled — restart the timer to include the
            # latest event in the same rebuild.
            self._rebuild_timer.start(self._REBUILD_DEBOUNCE_MS)
            return
        self._rebuild_pending = True
        t = QTimer(self)
        t.setSingleShot(True)
        t.timeout.connect(self._do_rebuild)
        self._rebuild_timer = t
        t.start(self._REBUILD_DEBOUNCE_MS)

    def _do_rebuild(self) -> None:
        """Re-render the 3Dmol.js page from the current scene.

        Called by the debounce timer (or immediately at widget
        construction).  Guards against a null ``_view`` so it stays
        safe to call during teardown.
        """
        self._rebuild_pending = False
        self._rebuild_timer = None
        if self._view is None:
            return
        html = build_scene_html(self._scene, background=self._background)
        self._view.setHtml(html)
        WorkbenchWidget.rebuild_count += 1

    # Public shim retained for callers (tests, future 32c code) that
    # still reach for ``_rebuild``; now routes through the debouncer
    # so even direct calls from user scripts can't thrash.
    def _rebuild(self) -> None:
        self._schedule_rebuild()

    def _refresh_tracks_list(self) -> None:
        """Rebuild the right-side tracks list with one
        :class:`TrackRow` widget per track.  Rebuilds the whole
        list on every event — cheap for < 100 tracks, and much
        simpler than diffing."""
        if self._tracks_list is None:
            return
        self._tracks_list.clear()
        for t in self._scene.tracks():
            row = TrackRow(t, self._tracks_list)
            row.visibility_toggled.connect(self._on_row_visibility)
            row.style_changed.connect(self._on_row_style_changed)
            row.colour_changed.connect(self._on_row_colour_changed)
            row.opacity_changed.connect(self._on_row_opacity_changed)
            row.remove_clicked.connect(self._on_row_remove)
            item = QListWidgetItem(self._tracks_list)
            item.setData(Qt.UserRole, t.name)
            item.setSizeHint(row.sizeHint())
            self._tracks_list.addItem(item)
            self._tracks_list.setItemWidget(item, row)

    # ---- track-row signal forwarders ----------------------------
    def _on_row_visibility(self, track_name: str, visible: bool) -> None:
        try:
            self._scene.set_visible(track_name, visible)
        except KeyError:
            pass    # track vanished while the UI caught up — ignore

    def _on_row_style_changed(self, track_name: str,
                              new_style: str) -> None:
        try:
            self._scene.set_style(track_name, style=new_style)
        except KeyError:
            pass

    def _on_row_colour_changed(self, track_name: str,
                               new_colour: str) -> None:
        try:
            self._scene.set_style(track_name, colour=new_colour)
        except KeyError:
            pass

    def _on_row_opacity_changed(self, track_name: str,
                                new_opacity: float) -> None:
        try:
            self._scene.set_style(track_name, opacity=new_opacity)
        except KeyError:
            pass

    def _on_row_remove(self, track_name: str) -> None:
        self._scene.remove(track_name)

    # ---- toolbar handlers ---------------------------------------
    def _on_clear_clicked(self) -> None:
        if not self._scene.tracks():
            return
        self._scene.clear()

    def _on_fit_clicked(self) -> None:
        """Ask 3Dmol.js to re-zoom so every visible track fits in
        view.  Rebuilding the HTML page is the simplest path (it
        ends with ``v.zoomTo(); v.render();`` anyway)."""
        self._schedule_rebuild()
        self._status.setText("fit to view")

    def _on_toggle_background(self) -> None:
        """Flip the scene background between dark and light."""
        if self._background == "#1e1e1e":
            self._background = "#ffffff"
            label = "light"
        else:
            self._background = "#1e1e1e"
            label = "dark"
        self._schedule_rebuild()
        self._status.setText(f"background: {label}")

    def _on_export_html_clicked(self) -> None:
        """Save the current scene as a standalone HTML document —
        3Dmol.js inlined, no server needed.  Opens in any browser."""
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self, "Export scene HTML",
            str(Path.home() / "workbench_scene.html"),
            "HTML documents (*.html)")
        if not path:
            return
        try:
            html = build_scene_html(self._scene,
                                    background=self._background)
            Path(path).write_text(html, encoding="utf-8")
        except Exception as e:    # pragma: no cover - user-facing
            QMessageBox.critical(self, "Export failed", str(e))
            return
        self._status.setText(f"exported → {Path(path).name}")

    def _on_snapshot_clicked(self) -> None:
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Workbench snapshot",
            str(Path.home() / "workbench.png"),
            "PNG images (*.png)")
        if not path:
            return
        try:
            out = self.grab_png(Path(path))
        except Exception as e:      # pragma: no cover - user-facing
            QMessageBox.critical(self, "Snapshot failed", str(e))
            return
        self._status.setText(f"snapshot → {out.name}")

    def _on_track_double_clicked(self, item: QListWidgetItem) -> None:
        name = item.data(Qt.UserRole)
        if isinstance(name, str):
            self._scene.remove(name)

    # ---- cleanup ------------------------------------------------
    def closeEvent(self, event) -> None:   # noqa: N802 - Qt API
        try:
            self._unsubscribe()
        except Exception:
            pass
        super().closeEvent(event)
