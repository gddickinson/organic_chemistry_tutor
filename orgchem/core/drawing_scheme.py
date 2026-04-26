"""Phase 36f.1 (round 131) — reaction-scheme data core.

Pure-Python dataclass + helpers that bundle two
:class:`orgchem.core.drawing.Structure` halves into a *reaction
scheme* — the LHS (reactants), the RHS (products), an arrow type
(``"forward"`` ``→`` or ``"reversible"`` ``⇌``), and an optional
free-text reagents / conditions string.

The headless surface here is what the Phase-36f GUI (round 132)
will hook into — the canvas will let users mark "this is the
LHS" / "this is the RHS", populate a :class:`Scheme`, and ship
the resulting reaction SMILES string off to the Reactions tab
or the agent layer.

No Qt imports; no `Mol` imports at module load (RDKit is lazy
so the dataclass is usable in environments where RDKit isn't
installed yet).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from orgchem.core.drawing import (
    Structure,
    structure_from_smiles,
    structure_to_smiles,
)


#: Arrow types we recognise in a scheme.  The strings round-trip
#: through :meth:`Scheme.to_dict` / :meth:`Scheme.from_dict`.
_VALID_ARROWS = ("forward", "reversible")


@dataclass
class Scheme:
    """A single reaction scheme: LHS structure(s), an arrow, RHS
    structure(s), plus optional reagents / conditions text.

    ``lhs`` and ``rhs`` are lists of :class:`Structure` so the
    scheme can carry multi-component reactants / products
    (e.g. nucleophile + substrate → product + leaving group).
    The convenience constructor :meth:`from_smiles_pair` is the
    expected GUI entry point — pass two SMILES strings, get a
    valid scheme.
    """
    lhs: List[Structure] = field(default_factory=list)
    rhs: List[Structure] = field(default_factory=list)
    arrow: str = "forward"
    reagents: str = ""

    def __post_init__(self) -> None:
        if self.arrow not in _VALID_ARROWS:
            self.arrow = "forward"

    # ---- introspection -------------------------------------

    @property
    def is_empty(self) -> bool:
        """A scheme is empty when both halves carry no atoms."""
        return all(s.is_empty for s in self.lhs) \
            and all(s.is_empty for s in self.rhs)

    @property
    def n_lhs_atoms(self) -> int:
        return sum(s.n_atoms for s in self.lhs)

    @property
    def n_rhs_atoms(self) -> int:
        return sum(s.n_atoms for s in self.rhs)

    # ---- SMILES round-trip ---------------------------------

    @classmethod
    def from_smiles_pair(
        cls,
        lhs_smiles: str,
        rhs_smiles: str,
        *,
        arrow: str = "forward",
        reagents: str = "",
    ) -> Optional["Scheme"]:
        """Build a scheme from two SMILES strings.  Each side is
        passed through :func:`structure_from_smiles`; ``None`` is
        returned if either side fails to parse so GUI callers can
        surface a clean error message instead of half-constructed
        data.

        ``"."``-separated SMILES on either side are exploded into
        per-component :class:`Structure`s so a multi-substrate
        scheme like ``"CC(=O)Cl.NC"`` lands as two LHS structures.
        """
        lhs = _split_and_parse(lhs_smiles)
        rhs = _split_and_parse(rhs_smiles)
        if lhs is None or rhs is None:
            return None
        return cls(lhs=lhs, rhs=rhs, arrow=arrow, reagents=reagents)

    @classmethod
    def from_reaction_smiles(
        cls, rxn_smiles: str,
    ) -> Optional["Scheme"]:
        """Parse a ``LHS>reagents>RHS`` reaction SMILES into a
        :class:`Scheme`.  Returns ``None`` on parse failure.

        The agents segment between the two ``>`` is preserved
        verbatim in :attr:`Scheme.reagents` so the round-trip is
        lossless for reagent strings already encoded in SMILES
        form (e.g. ``">[Pd]>"``).
        """
        if not rxn_smiles or not isinstance(rxn_smiles, str):
            return None
        parts = rxn_smiles.split(">")
        if len(parts) != 3:
            return None
        lhs_str, reagents, rhs_str = parts
        scheme = cls.from_smiles_pair(
            lhs_str, rhs_str, reagents=reagents.strip(),
        )
        return scheme

    def to_reaction_smiles(self) -> Optional[str]:
        """Bundle the scheme into a ``LHS>reagents>RHS`` reaction
        SMILES.  Returns ``None`` if either side has at least one
        atom yet fails the structure-to-SMILES conversion (RDKit
        sanitisation issue), so callers can surface the failure
        rather than emit a malformed string.

        Empty halves serialise as the empty string — i.e. an
        all-empty scheme renders as ``">>"``, a synthesis target
        with no specified products renders as ``"CCO>>"``, etc.
        That mirrors RDKit's convention so the value round-trips.
        """
        lhs_smiles_parts: List[str] = []
        for s in self.lhs:
            if s.is_empty:
                continue
            smi = structure_to_smiles(s)
            if smi is None:
                return None
            lhs_smiles_parts.append(smi)
        rhs_smiles_parts: List[str] = []
        for s in self.rhs:
            if s.is_empty:
                continue
            smi = structure_to_smiles(s)
            if smi is None:
                return None
            rhs_smiles_parts.append(smi)
        lhs_str = ".".join(lhs_smiles_parts)
        rhs_str = ".".join(rhs_smiles_parts)
        return f"{lhs_str}>{self.reagents}>{rhs_str}"

    # ---- per-side SMILES ----------------------------------

    def lhs_smiles(self) -> str:
        """Return the LHS as a single ``"."``-joined SMILES
        string.  Empty when no LHS atoms."""
        parts: List[str] = []
        for s in self.lhs:
            if s.is_empty:
                continue
            smi = structure_to_smiles(s)
            if smi:
                parts.append(smi)
        return ".".join(parts)

    def rhs_smiles(self) -> str:
        """Return the RHS as a single ``"."``-joined SMILES
        string.  Empty when no RHS atoms."""
        parts: List[str] = []
        for s in self.rhs:
            if s.is_empty:
                continue
            smi = structure_to_smiles(s)
            if smi:
                parts.append(smi)
        return ".".join(parts)

    # ---- JSON-friendly serialisation ----------------------

    def to_dict(self) -> dict:
        return {
            "lhs": self.lhs_smiles(),
            "rhs": self.rhs_smiles(),
            "arrow": self.arrow,
            "reagents": self.reagents,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> Optional["Scheme"]:
        if not isinstance(payload, dict):
            return None
        return cls.from_smiles_pair(
            payload.get("lhs", ""),
            payload.get("rhs", ""),
            arrow=payload.get("arrow", "forward"),
            reagents=payload.get("reagents", ""),
        )


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _split_and_parse(smi: str) -> Optional[List[Structure]]:
    """Split a ``"."``-separated SMILES string into per-component
    :class:`Structure`s.  Returns ``None`` if any component fails
    to parse so the caller can flag the bad input atomically.
    Empty / whitespace input becomes an empty list (a valid
    "no component" half of a scheme).
    """
    if smi is None:
        return None
    text = smi.strip()
    if not text:
        return []
    out: List[Structure] = []
    for part in text.split("."):
        part = part.strip()
        if not part:
            continue
        s = structure_from_smiles(part)
        if s is None:
            return None
        out.append(s)
    return out


def is_balanced_atom_counts(scheme: Scheme) -> bool:
    """Crude atom-count check — same number of heavy atoms on
    each side.  Real reaction balancing is a graph-isomorphism
    problem; this is the cheap "did the user remember to include
    the leaving group?" sanity hint a future GUI can surface
    inline.
    """
    if scheme.is_empty:
        return True
    return scheme.n_lhs_atoms == scheme.n_rhs_atoms
