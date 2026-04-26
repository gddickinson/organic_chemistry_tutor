"""Phase 38d.2 (round 193) — process-simulator playback dock.

Sibling widget to :class:`gui.dialogs.lab_setup_canvas.CanvasView`.
Drives a :class:`core.process_simulator.ProcessSimulator` via a
``QTimer`` and renders the current stage's label / description /
progress in a docked panel below the canvas.

For round 193 the canvas-side highlight is intentionally minimal
(no per-stage equipment glyph flashing — that's polish for a
later sub-phase if needed).  The dock surfaces:

- **Play / Pause / Reset / Step** buttons.
- **Speed slider** (0.5× to 4×, default 1×).  The simulator's
  per-stage `duration_seconds` × current speed determines how
  long each stage stays on screen before auto-advance.
- **Stage label + description** rendered in a `QLabel` /
  `QTextBrowser` pair.
- **Progress bar** showing `simulator.progress()`.

Signals:

- :pyattr:`stage_changed(stage_id, stage_index)` — fires whenever
  the simulator advances (manually or via timer).
- :pyattr:`finished()` — fires once when the simulator hits
  ``is_complete()``.

The canvas dialog instantiates this dock + binds it via
:meth:`set_simulator`.  When the simulator is ``None`` (no setup
loaded), the controls disable.
"""
from __future__ import annotations
from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QProgressBar, QPushButton, QSlider,
    QTextBrowser, QVBoxLayout, QWidget,
)

from orgchem.core.process_simulator import ProcessSimulator


class SimulationDock(QWidget):
    """Playback dock for a :class:`ProcessSimulator`."""

    #: Emitted whenever the current stage changes (manual or
    #: timer-driven advance).  Carries (stage_id, stage_index).
    stage_changed = Signal(str, int)

    #: Emitted once when the simulator hits is_complete().
    finished = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._sim: Optional[ProcessSimulator] = None
        self._speed: float = 1.0
        self._elapsed_ms_in_stage: int = 0
        self._build_ui()
        self._timer = QTimer(self)
        self._timer.setInterval(100)   # 10 Hz
        self._timer.timeout.connect(self._on_tick)
        self._refresh()

    # ---- Public API ------------------------------------------
    def set_simulator(self, sim: Optional[ProcessSimulator]
                      ) -> None:
        """Bind a simulator (or pass ``None`` to clear)."""
        self.pause()
        self._sim = sim
        self._elapsed_ms_in_stage = 0
        self._refresh()
        if sim is not None:
            self._emit_stage()

    def simulator(self) -> Optional[ProcessSimulator]:
        return self._sim

    def speed(self) -> float:
        return self._speed

    # ---- Playback controls -----------------------------------
    def play(self) -> None:
        if self._sim is None or self._sim.is_complete():
            return
        if not self._timer.isActive():
            self._timer.start()
        self._refresh()

    def pause(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
        self._refresh()

    def is_playing(self) -> bool:
        return self._timer.isActive()

    def step(self) -> None:
        """Advance one stage manually (for click-through study)."""
        if self._sim is None:
            return
        self._sim.advance()
        self._elapsed_ms_in_stage = 0
        self._emit_stage()
        if self._sim.is_complete():
            self.pause()
            self.finished.emit()
        self._refresh()

    def reset(self) -> None:
        self.pause()
        if self._sim is not None:
            self._sim.reset()
        self._elapsed_ms_in_stage = 0
        if self._sim is not None:
            self._emit_stage()
        self._refresh()

    # ---- Internals -------------------------------------------
    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        # Top row: stage label + progress bar.
        top = QHBoxLayout()
        self._stage_label = QLabel("(no simulator loaded)")
        self._stage_label.setStyleSheet("font-weight: bold;")
        top.addWidget(self._stage_label, 1)
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(True)
        self._progress.setFormat("Stage %v / %m")
        top.addWidget(self._progress)
        layout.addLayout(top)
        # Description text.
        self._desc = QTextBrowser()
        self._desc.setMinimumHeight(80)
        self._desc.setOpenLinks(False)
        layout.addWidget(self._desc)
        # Controls row.
        controls = QHBoxLayout()
        self._play_btn = QPushButton("▶ Play")
        self._play_btn.clicked.connect(self._on_play_clicked)
        controls.addWidget(self._play_btn)
        self._step_btn = QPushButton("⏭ Step")
        self._step_btn.clicked.connect(self.step)
        controls.addWidget(self._step_btn)
        self._reset_btn = QPushButton("⟲ Reset")
        self._reset_btn.clicked.connect(self.reset)
        controls.addWidget(self._reset_btn)
        controls.addSpacing(20)
        controls.addWidget(QLabel("Speed:"))
        self._speed_slider = QSlider(Qt.Horizontal)
        self._speed_slider.setRange(50, 400)   # 0.5× to 4×
        self._speed_slider.setValue(100)
        self._speed_slider.setMaximumWidth(160)
        self._speed_slider.valueChanged.connect(
            self._on_speed_changed)
        controls.addWidget(self._speed_slider)
        self._speed_label = QLabel("1.0×")
        controls.addWidget(self._speed_label)
        controls.addStretch(1)
        layout.addLayout(controls)

    def _on_play_clicked(self) -> None:
        if self.is_playing():
            self.pause()
        else:
            self.play()

    def _on_speed_changed(self, value: int) -> None:
        self._speed = value / 100.0
        self._speed_label.setText(f"{self._speed:.1f}×")

    def _on_tick(self) -> None:
        if self._sim is None:
            self.pause()
            return
        stage = self._sim.current_stage()
        if stage is None:
            self.pause()
            self.finished.emit()
            return
        self._elapsed_ms_in_stage += self._timer.interval()
        # Stage duration scales by speed (faster = shorter
        # display window).
        stage_ms = max(50, int(
            stage.duration_seconds * 1000.0 / self._speed))
        if self._elapsed_ms_in_stage >= stage_ms:
            self._elapsed_ms_in_stage = 0
            self._sim.advance()
            self._emit_stage()
            if self._sim.is_complete():
                self.pause()
                self.finished.emit()
        self._refresh()

    def _emit_stage(self) -> None:
        if self._sim is None:
            return
        stage = self._sim.current_stage()
        if stage is not None:
            self.stage_changed.emit(
                stage.id, self._sim.current_index())

    def _refresh(self) -> None:
        has_sim = self._sim is not None
        self._play_btn.setEnabled(
            has_sim and not self._sim.is_complete())
        self._step_btn.setEnabled(
            has_sim and not self._sim.is_complete())
        self._reset_btn.setEnabled(has_sim)
        if not has_sim:
            self._stage_label.setText("(no simulator loaded)")
            self._desc.setHtml("")
            self._progress.setRange(0, 100)
            self._progress.setValue(0)
            return
        self._progress.setRange(0, max(1, self._sim.total_stages))
        self._progress.setValue(self._sim.current_index())
        stage = self._sim.current_stage()
        if stage is None:
            self._stage_label.setText(
                f"✓ Complete ({self._sim.total_stages} stages)")
            self._desc.setHtml(
                "<i>The process has finished.  "
                "Reset to play again.</i>"
            )
        else:
            idx = self._sim.current_index() + 1
            self._stage_label.setText(
                f"Stage {idx} / {self._sim.total_stages}: "
                f"{stage.label}")
            self._desc.setHtml(
                f"<p>{stage.description}</p>"
                f"<p style='color: #888'>Duration: "
                f"{stage.duration_seconds:.1f}s @ "
                f"{self._speed:.1f}× speed</p>"
            )
        # Play button label reflects state.
        self._play_btn.setText(
            "⏸ Pause" if self.is_playing() else "▶ Play")
