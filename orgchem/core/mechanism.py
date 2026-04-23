"""Mechanism data model.

A :class:`Mechanism` is an ordered list of :class:`MechanismStep` s. Each
step carries a molecule state (SMILES) and a list of curved arrows between
atom indices. Stored as JSON in the ``Reaction.mechanism_json`` column so
authoring a mechanism is just writing JSON — no schema migration needed.

Pedagogical conventions for arrows:
- **curly**    — 2-electron flow (standard arrow-pushing).
- **fishhook** — 1-electron flow (radical mechanisms).
- ``from_atom`` / ``to_atom`` are indices into the SMILES as parsed by RDKit
  (``Chem.MolFromSmiles``). Because SMILES atom order is deterministic per
  string, these indices are stable.

Arrows always represent *net electron flow*. An arrow from a lone-pair-bearing
atom A to an electrophilic atom B means "electrons move from A toward B".
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Arrow:
    from_atom: int
    to_atom: int
    kind: str = "curly"   # "curly" (2e⁻) or "fishhook" (1e⁻)
    bend: float = 0.35    # perpendicular offset factor for the bezier control point
    label: str = ""       # optional short annotation shown near the arrow
    # Phase 13c follow-up: bond-midpoint arrows.
    # When set, the arrow starts (from_bond) or ends (to_bond) at the
    # midpoint of the named bond instead of at the atom centre. Use a
    # (atomA, atomB) tuple of atom indices; overrides from_atom/to_atom
    # for the corresponding endpoint.
    from_bond: Optional[Tuple[int, int]] = None
    to_bond: Optional[Tuple[int, int]] = None


@dataclass
class MechanismStep:
    title: str
    description: str
    smiles: str
    arrows: List[Arrow] = field(default_factory=list)
    # Phase 13c follow-up: lone-pair dot decorations.
    # Atom indices that should get a pair of dots drawn near them to
    # emphasise the electrons involved in the arrow flow.
    lone_pairs: List[int] = field(default_factory=list)


@dataclass
class Mechanism:
    reaction_id: int = 0
    steps: List[MechanismStep] = field(default_factory=list)

    # ---------- serialisation ----------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reaction_id": self.reaction_id,
            "steps": [
                {
                    "title": s.title,
                    "description": s.description,
                    "smiles": s.smiles,
                    "arrows": [asdict(a) for a in s.arrows],
                    "lone_pairs": list(s.lone_pairs),
                }
                for s in self.steps
            ],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Mechanism":
        return cls(
            reaction_id=int(data.get("reaction_id", 0)),
            steps=[
                MechanismStep(
                    title=s["title"],
                    description=s["description"],
                    smiles=s["smiles"],
                    arrows=[_arrow_from_dict(a) for a in s.get("arrows", [])],
                    lone_pairs=list(s.get("lone_pairs", [])),
                )
                for s in data.get("steps", [])
            ],
        )

    @classmethod
    def from_json(cls, text: str) -> "Mechanism":
        return cls.from_dict(json.loads(text))

    # ---------- convenience ----------

    def __len__(self) -> int:
        return len(self.steps)

    def __getitem__(self, i: int) -> MechanismStep:
        return self.steps[i]


def _arrow_from_dict(d: Dict[str, Any]) -> Arrow:
    """Build an :class:`Arrow` from a dict, coercing bond fields back to
    tuples (JSON serialises tuples as lists)."""
    d = dict(d)  # don't mutate the caller's dict
    for key in ("from_bond", "to_bond"):
        val = d.get(key)
        if val is not None and not isinstance(val, tuple):
            d[key] = tuple(val)
    return Arrow(**d)
