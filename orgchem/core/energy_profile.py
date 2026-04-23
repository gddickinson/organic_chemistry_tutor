"""Reaction-coordinate (energy-profile) data model — Phase 13a.

A :class:`ReactionEnergyProfile` is an ordered list of
:class:`StationaryPoint` s along the reaction coordinate. Each point carries
a label, a relative energy (kJ/mol by default), and a flag marking whether
it is a transition state or a minimum (reactant / intermediate / product).

Stored as JSON in the ``Reaction.energy_profile_json`` column — no schema
migration needed when authoring a new profile.

Pedagogical conventions:
- **x** — reaction progress, unitless (0 = starting, 1 = first TS, 2 = first
  intermediate, ...). We auto-assign integer x-values in order so authors
  only have to list points.
- **energy** — relative to the first point (reactants). Units default to
  kJ/mol but are stored as a free-form string field so authors can use
  kcal/mol or eV if they prefer.
- **is_ts** — transition state. Rendered with a ‡ suffix on the label and
  treated as a curve *peak*; minima are plateau-like.
- **smiles** — optional structure shown underneath the x-axis in the
  renderer's "with structures" mode.

Numbers here are *pedagogical*. They're drawn from canonical textbook
tables (Clayden 2nd ed., Carey & Sundberg) and should reproduce the
qualitative shape of the profile — they are not intended for kinetic
prediction.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json
from typing import Any, Dict, List, Optional


@dataclass
class StationaryPoint:
    label: str                         # short display label, e.g. "Reactants", "TS‡", "Carbocation"
    energy: float                      # relative energy; units given by profile.energy_unit
    is_ts: bool = False                # True → rendered as a sharp peak, ‡ suffix
    smiles: Optional[str] = None       # optional structure for the "with structures" mode
    note: str = ""                     # optional short explanatory caption


@dataclass
class ReactionEnergyProfile:
    reaction_id: int = 0
    title: str = ""
    energy_unit: str = "kJ/mol"
    points: List[StationaryPoint] = field(default_factory=list)
    source: str = ""                   # e.g. "Clayden 2e Table 13.2" or "pedagogical estimate"

    # ---------- serialisation ----------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reaction_id": self.reaction_id,
            "title": self.title,
            "energy_unit": self.energy_unit,
            "source": self.source,
            "points": [asdict(p) for p in self.points],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReactionEnergyProfile":
        return cls(
            reaction_id=int(data.get("reaction_id", 0)),
            title=str(data.get("title", "")),
            energy_unit=str(data.get("energy_unit", "kJ/mol")),
            source=str(data.get("source", "")),
            points=[StationaryPoint(**p) for p in data.get("points", [])],
        )

    @classmethod
    def from_json(cls, text: str) -> "ReactionEnergyProfile":
        return cls.from_dict(json.loads(text))

    # ---------- convenience ----------

    def __len__(self) -> int:
        return len(self.points)

    def __getitem__(self, i: int) -> StationaryPoint:
        return self.points[i]

    @property
    def activation_energies(self) -> List[float]:
        """Ea for each TS: energy(TS) − energy(immediately preceding minimum).

        Returns one value per transition-state point, in order. Empty list
        when the profile has no TS.
        """
        out: List[float] = []
        last_min_e: Optional[float] = None
        for p in self.points:
            if p.is_ts:
                if last_min_e is not None:
                    out.append(p.energy - last_min_e)
            else:
                last_min_e = p.energy
        return out

    @property
    def delta_h(self) -> Optional[float]:
        """Overall ΔH: energy(last minimum) − energy(first minimum).

        None if the profile has fewer than two minima.
        """
        minima = [p.energy for p in self.points if not p.is_ts]
        if len(minima) < 2:
            return None
        return minima[-1] - minima[0]
