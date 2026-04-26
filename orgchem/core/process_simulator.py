"""Phase 38d.1 (round 192) — process-simulator headless state
machine.

First sub-phase of the multi-round Phase-38d process simulator.
Ships the **data + state-machine layer** that the upcoming
Phase-38d.2 canvas animation will drive: each Phase-38b setup
maps to an ordered sequence of teaching :class:`Stage` records
(e.g. simple distillation = "heat the pot" → "vapour rises" →
"vapour condenses" → "receiver fills"), and a :class:`ProcessSimulator`
walks them with `current_stage()` / `advance()` / `reset()` /
`progress()` / `is_complete()` accessors.

Pure-headless: no Qt imports, no rendering.  The canvas
animation (38d.2), pedagogical commentary track (38d.3), agent
actions (38d.4), Reactions-tab integration (Phase 38e), and any
animation-polish (38f) ship in subsequent rounds.

Public API:
- :class:`Stage` frozen dataclass — one teaching step
- :class:`ProcessSimulator` — driver
- :func:`simulator_for_setup(setup_id)` — builder pre-loaded
  with stages for the seeded Phase-38b setups
- :func:`available_setups()` — ids of setups that ship a
  simulator script
- :func:`stage_to_dict(stage)` / :func:`simulator_to_dict(sim)`
  — JSON-friendly serialisation for the eventual agent action
  surface
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Stage
# ----------------------------------------------------------------
@dataclass(frozen=True)
class Stage:
    """One teaching step in a process simulation.

    ``id`` is a stable string id for cross-referencing
    (the Phase-38d.2 canvas can map stages to highlight overlays).
    ``label`` is the short button-text label.  ``description`` is
    the longer pedagogical commentary.  ``duration_seconds`` is
    the intended display time at default playback speed (the
    canvas can scale this).  ``parameters`` is a free-form dict
    for stage-specific data the canvas can use (e.g. *temperature
    rises from 25 → 78 °C* for a heating stage).
    """
    id: str
    label: str
    description: str
    duration_seconds: float = 4.0
    parameters: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------
# ProcessSimulator
# ----------------------------------------------------------------
@dataclass
class ProcessSimulator:
    """Linear state-machine driver for a list of teaching stages.

    The current stage index is held in ``_current``; advance with
    :meth:`advance`, rewind with :meth:`reset`, query state with
    :meth:`current_stage` / :meth:`progress` / :meth:`is_complete`.

    Empty-script case: ``stages = ()`` → simulator is immediately
    "complete", `current_stage()` returns None.
    """
    setup_id: str
    stages: Tuple[Stage, ...]
    _current: int = 0

    @property
    def total_stages(self) -> int:
        return len(self.stages)

    def current_stage(self) -> Optional[Stage]:
        if 0 <= self._current < len(self.stages):
            return self.stages[self._current]
        return None

    def current_index(self) -> int:
        return self._current

    def advance(self) -> bool:
        """Move to the next stage.  Returns True if the index
        actually advanced; False if the simulator was already
        at / past the last stage."""
        if self._current < len(self.stages):
            self._current += 1
            return self._current <= len(self.stages)
        return False

    def reset(self) -> None:
        """Rewind to the first stage."""
        self._current = 0

    def jump_to(self, stage_id: str) -> bool:
        """Jump to the named stage.  Returns True on success."""
        for i, s in enumerate(self.stages):
            if s.id == stage_id:
                self._current = i
                return True
        return False

    def is_complete(self) -> bool:
        return self._current >= len(self.stages)

    def progress(self) -> float:
        """Linear progress in [0, 1].  Returns 0.0 for empty
        scripts (avoids ZeroDivisionError)."""
        if not self.stages:
            return 0.0
        return min(1.0, self._current / len(self.stages))


# ----------------------------------------------------------------
# Per-setup stage scripts.  Hand-written for the Phase-38b
# seeded setups.  Each list is ordered for natural display.
# ----------------------------------------------------------------
def _distillation_stages(
        with_column: bool = False) -> Tuple[Stage, ...]:
    """Shared script for simple + fractional distillation.
    Fractional adds a Vigreux-column equilibration stage."""
    stages: List[Stage] = [
        Stage(
            id="charge",
            label="Charge the pot",
            description="Add the liquid to the pot RBF (~ 1/3 - "
                        "1/2 full) with boiling chips or a stir "
                        "bar to prevent bumping.  Connect the "
                        "distillation head + thermometer + "
                        "condenser + receiver.",
            duration_seconds=3.0,
            parameters={"fill_fraction": 0.4},
        ),
        Stage(
            id="cooling-water-on",
            label="Start cooling water",
            description="Turn on the condenser water (in at the "
                        "low end, out at the high end — counter-"
                        "current cooling is more efficient).  "
                        "Verify flow before any heat is applied.",
            duration_seconds=2.5,
            parameters={"flow_rate": "moderate"},
        ),
        Stage(
            id="heat-up",
            label="Apply heat",
            description="Turn on the heating mantle / oil bath.  "
                        "Increase slowly + watch the thermometer "
                        "— rapid heating overshoots the boiling "
                        "point + entrains low-volatility "
                        "contaminants.",
            duration_seconds=4.0,
            parameters={"target_temp_C": 78,
                        "ramp_rate_C_per_min": 5},
        ),
    ]
    if with_column:
        stages.append(Stage(
            id="column-equilibration",
            label="Vigreux equilibration",
            description="Vapour rises through the Vigreux column.  "
                        "Multiple condensation/re-evaporation "
                        "cycles separate components by boiling "
                        "point — each theoretical plate doubles "
                        "the separation factor.  Watch for the "
                        "flooding line (vapour load > stripping "
                        "capacity → entrainment).",
            duration_seconds=4.0,
            parameters={"theoretical_plates": 8},
        ))
    stages.extend([
        Stage(
            id="vapour-rises",
            label="Vapour rises into the head",
            description="The first vapour bubble reaches the "
                        "head; the thermometer climbs to the "
                        "boiling point of the lowest-bp "
                        "component.  Steady-state has been "
                        "reached when the head temperature "
                        "stabilises.",
            duration_seconds=4.0,
        ),
        Stage(
            id="condense",
            label="Condense + collect fraction",
            description="Vapour condenses in the Liebig "
                        "condenser; the liquid drips into the "
                        "receiver RBF.  Collect the main "
                        "fraction at constant head temperature.  "
                        "If the head temperature climbs by > 2 "
                        "°C, switch to a fresh receiver — you've "
                        "moved into the next fraction.",
            duration_seconds=5.0,
        ),
        Stage(
            id="cool-down",
            label="Cool + decommission",
            description="Turn off the heat first, then cooling "
                        "water once everything's at room "
                        "temperature.  Disassemble + clean the "
                        "glassware while the joints are still "
                        "warm (cold + dry joints stick).",
            duration_seconds=3.0,
        ),
    ])
    return tuple(stages)


def _reflux_stages() -> Tuple[Stage, ...]:
    return (
        Stage(
            id="charge",
            label="Charge the RBF",
            description="Combine reactants + solvent + stir bar.  "
                        "Total volume should not exceed half "
                        "the flask.  Attach the Allihn condenser "
                        "vertically.",
            duration_seconds=3.0,
        ),
        Stage(
            id="cooling-water-on",
            label="Start cooling water",
            description="Counter-current water on; verify flow "
                        "before heating.",
            duration_seconds=2.0,
        ),
        Stage(
            id="heat-up",
            label="Heat to gentle reflux",
            description="Heat the bath to ~ 5-10 °C above the "
                        "solvent boiling point.  Vapour should "
                        "rise no more than half-way up the "
                        "condenser.",
            duration_seconds=4.0,
        ),
        Stage(
            id="reflux",
            label="Hold at reflux",
            description="Reflux ring sits 1/3 to 1/2 up the "
                        "condenser.  Let the reaction run for "
                        "the prescribed time (TLC monitors "
                        "conversion).",
            duration_seconds=8.0,
            parameters={"reaction_time_typical_min": 60},
        ),
        Stage(
            id="cool-down",
            label="Cool + work up",
            description="Drop the bath, let cool to room "
                        "temperature, then proceed to workup "
                        "(quench, extraction, drying, "
                        "concentration).",
            duration_seconds=3.0,
        ),
    )


def _vacuum_filtration_stages() -> Tuple[Stage, ...]:
    return (
        Stage(
            id="setup",
            label="Set up Büchner + filter flask",
            description="Place a filter paper of the correct "
                        "diameter on the Büchner plate; wet "
                        "with a few drops of solvent to seal it.",
            duration_seconds=3.0,
        ),
        Stage(
            id="apply-vacuum",
            label="Apply vacuum",
            description="Connect the filter flask to the cold "
                        "trap + aspirator / vacuum pump.  Open "
                        "the vacuum BEFORE pouring the slurry "
                        "to avoid back-pressure.",
            duration_seconds=2.5,
        ),
        Stage(
            id="filter",
            label="Pour + filter",
            description="Pour the slurry onto the filter paper "
                        "in portions.  The filtrate collects "
                        "in the flask; the solid stays on the "
                        "paper.",
            duration_seconds=4.0,
        ),
        Stage(
            id="wash",
            label="Wash the cake",
            description="Rinse the solid with cold solvent in "
                        "small portions, breaking the vacuum "
                        "briefly between rinses to let the wash "
                        "soak through.",
            duration_seconds=3.0,
        ),
        Stage(
            id="dry",
            label="Air-dry under vacuum",
            description="Pull air through the cake for several "
                        "minutes to wick off the wash solvent "
                        "before transferring to a vial.",
            duration_seconds=3.0,
        ),
    )


def _soxhlet_stages() -> Tuple[Stage, ...]:
    return (
        Stage(
            id="charge-thimble",
            label="Charge cellulose thimble",
            description="Place the powdered solid analyte in a "
                        "cellulose thimble, fold the top, and "
                        "drop into the Soxhlet body.  The "
                        "thimble retains the solid while letting "
                        "solvent percolate through.",
            duration_seconds=3.0,
        ),
        Stage(
            id="charge-pot",
            label="Charge solvent in the pot",
            description="Add the extraction solvent to the pot "
                        "RBF (~ 100 mL for a small thimble).  "
                        "Stir bar + boiling chips help avoid "
                        "bumping during reflux.",
            duration_seconds=3.0,
        ),
        Stage(
            id="reflux-fill",
            label="Reflux + thimble fills",
            description="Heat the pot.  Solvent vapour rises "
                        "around the thimble (NOT through the "
                        "siphon arm), condenses on the "
                        "condenser above, and drips back DOWN "
                        "into the thimble — slowly filling the "
                        "Soxhlet body around the thimble.",
            duration_seconds=6.0,
        ),
        Stage(
            id="siphon",
            label="Siphon trips",
            description="Once liquid reaches the top of the "
                        "siphon arm, the **siphon trips** + "
                        "drains the entire thimble + body back "
                        "into the pot in one cycle.  The pot now "
                        "holds the cumulative extract (analyte "
                        "concentrates here as fresh solvent "
                        "keeps recycling).",
            duration_seconds=4.0,
            parameters={"cycles_per_hour": 6},
        ),
        Stage(
            id="repeat",
            label="Repeat cycles (4-24 h)",
            description="Each siphon = one extraction cycle.  "
                        "Run for hours to days; the cumulative "
                        "extract in the pot reaches near-"
                        "complete recovery from the analyte.  "
                        "TLC monitors the colourful natural-"
                        "product extracts.",
            duration_seconds=5.0,
        ),
        Stage(
            id="cool-recover",
            label="Cool + recover",
            description="Stop heating.  Cool the pot.  Decant the "
                        "extract; rotovap to remove solvent + "
                        "yield the crude.",
            duration_seconds=3.0,
        ),
    )


def _liquid_liquid_extraction_stages() -> Tuple[Stage, ...]:
    return (
        Stage(
            id="combine",
            label="Combine phases in sep funnel",
            description="Pour the aqueous + organic phases into "
                        "the separating funnel (do NOT exceed "
                        "2/3 capacity).  Stopper the top.",
            duration_seconds=3.0,
        ),
        Stage(
            id="invert",
            label="Invert + vent",
            description="Invert the funnel, point the stem AWAY "
                        "from your face + people, and **open "
                        "the stopcock to vent** built-up "
                        "pressure (volatile solvents like ether "
                        "/ DCM build pressure fast).",
            duration_seconds=2.5,
        ),
        Stage(
            id="shake",
            label="Shake gently",
            description="Shake gently for 10 - 30 s, venting "
                        "again every few shakes for the first "
                        "minute.  Vigorous shaking forms an "
                        "emulsion that can take hours to break.",
            duration_seconds=4.0,
        ),
        Stage(
            id="settle",
            label="Settle into two phases",
            description="Place upright in the ring stand.  The "
                        "phases separate by density (organic "
                        "above for low-density solvents like "
                        "ether; below for chlorinated solvents "
                        "like DCM).  Wait for a sharp interface.",
            duration_seconds=4.0,
        ),
        Stage(
            id="drain",
            label="Drain lower phase",
            description="Open the stopcock + drain the lower "
                        "phase into a clean Erlenmeyer.  Stop "
                        "JUST as the interface reaches the "
                        "stopcock — leave a thin lower-phase "
                        "buffer rather than risk contamination.",
            duration_seconds=3.0,
        ),
        Stage(
            id="repeat",
            label="Wash again (3 ×)",
            description="Add fresh extracting solvent to the "
                        "remaining phase + repeat 2-3 times for "
                        "near-complete recovery.  Combine the "
                        "extracts; dry over MgSO₄ or Na₂SO₄; "
                        "filter; concentrate.",
            duration_seconds=4.0,
        ),
    )


def _reflux_with_addition_stages() -> Tuple[Stage, ...]:
    return (
        Stage(
            id="charge",
            label="Charge substrate + solvent",
            description="Combine the substrate + solvent + stir "
                        "bar in the 3-neck RBF.  Attach the "
                        "Allihn condenser (centre neck), "
                        "thermometer (one side), addition funnel "
                        "(other side).",
            duration_seconds=3.0,
        ),
        Stage(
            id="charge-funnel",
            label="Charge addition funnel",
            description="Load the limiting reagent (or the more "
                        "reactive partner) into the addition "
                        "funnel.  Cap with a stopper or a "
                        "drying tube.",
            duration_seconds=2.5,
        ),
        Stage(
            id="cooling-water-on",
            label="Start cooling water + heat",
            description="Counter-current water on the condenser; "
                        "heat to the target temperature (often "
                        "0 - 5 °C for exothermic additions, or "
                        "room temperature for slow additions).",
            duration_seconds=3.0,
        ),
        Stage(
            id="dropwise",
            label="Add dropwise",
            description="Open the addition-funnel stopcock + add "
                        "the reagent **dropwise**.  Watch the "
                        "thermometer — exotherm > 10 °C above "
                        "the target means slow the addition.  "
                        "The drip rate sets the reaction rate.",
            duration_seconds=8.0,
            parameters={"drops_per_second": 1},
        ),
        Stage(
            id="reflux-hold",
            label="Hold at reflux",
            description="After complete addition, heat to gentle "
                        "reflux + hold for the prescribed time "
                        "(TLC monitors).  Reflux ring 1/3 to 1/2 "
                        "up the condenser.",
            duration_seconds=6.0,
        ),
        Stage(
            id="cool-down",
            label="Cool + work up",
            description="Drop the heat, let cool to room "
                        "temperature, quench (if applicable), "
                        "then proceed to extraction / drying / "
                        "concentration.",
            duration_seconds=3.0,
        ),
    )


def _recrystallisation_stages() -> Tuple[Stage, ...]:
    return (
        Stage(
            id="dissolve-hot",
            label="Dissolve in hot solvent",
            description="Add solvent in small portions while "
                        "heating (gently — the solvent is "
                        "volatile).  Stop adding when the solid "
                        "JUST dissolves — minimum hot solvent "
                        "= maximum recovery on cooling.",
            duration_seconds=4.0,
        ),
        Stage(
            id="hot-filter",
            label="Hot filter (optional)",
            description="If the hot solution has insoluble "
                        "impurities (dust, decomposition "
                        "products), filter through a heated "
                        "fluted funnel before cooling.",
            duration_seconds=3.0,
        ),
        Stage(
            id="cool-slowly",
            label="Cool slowly",
            description="Let the flask cool to room temperature "
                        "uninterrupted, then to ice-bath "
                        "temperature.  Slow cooling = larger, "
                        "purer crystals.  Fast cooling = small "
                        "crystals that occlude impurities.",
            duration_seconds=6.0,
        ),
        Stage(
            id="collect",
            label="Vacuum-filter + wash + dry",
            description="Collect the crystals on a Büchner; "
                        "wash with a few mL of COLD solvent to "
                        "remove the supernatant impurities; "
                        "air-dry under vacuum.",
            duration_seconds=4.0,
        ),
    )


# Lookup table — setup id → stage tuple.
_SCRIPTS: Dict[str, Tuple[Stage, ...]] = {
    "simple_distillation": _distillation_stages(False),
    "fractional_distillation": _distillation_stages(True),
    "reflux": _reflux_stages(),
    "reflux_with_addition": _reflux_with_addition_stages(),
    "vacuum_filtration": _vacuum_filtration_stages(),
    "soxhlet_extraction": _soxhlet_stages(),
    "liquid_liquid_extraction":
        _liquid_liquid_extraction_stages(),
    "recrystallisation": _recrystallisation_stages(),
}


# ----------------------------------------------------------------
# Public API
# ----------------------------------------------------------------
def available_setups() -> List[str]:
    """Setup ids that ship a simulator script."""
    return sorted(_SCRIPTS.keys())


def simulator_for_setup(setup_id: str
                        ) -> Optional[ProcessSimulator]:
    """Return a fresh :class:`ProcessSimulator` pre-loaded with
    the setup's teaching stages.  Returns ``None`` for setups
    that don't yet have a script (covered in 38d.2 follow-ups).
    """
    stages = _SCRIPTS.get(setup_id)
    if stages is None:
        return None
    return ProcessSimulator(setup_id=setup_id, stages=stages)


def stage_to_dict(stage: Stage) -> Dict[str, Any]:
    return {
        "id": stage.id,
        "label": stage.label,
        "description": stage.description,
        "duration_seconds": stage.duration_seconds,
        "parameters": dict(stage.parameters),
    }


def simulator_to_dict(sim: ProcessSimulator) -> Dict[str, Any]:
    return {
        "setup_id": sim.setup_id,
        "total_stages": sim.total_stages,
        "current_index": sim.current_index(),
        "is_complete": sim.is_complete(),
        "progress": sim.progress(),
        "stages": [stage_to_dict(s) for s in sim.stages],
    }
