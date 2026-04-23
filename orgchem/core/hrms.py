"""HRMS molecular-formula candidate guesser — Phase 4 follow-up.

Given a measured monoisotopic mass (e.g. from an HRMS spectrum) and a
ppm tolerance, enumerate the molecular formulas whose *theoretical*
monoisotopic mass falls inside the window. Candidates are filtered by
classical organic-chem heuristics before ranking:

- **Nitrogen rule** — an odd number of nitrogens ⇒ odd nominal mass,
  and vice-versa. Discards ~50 % of random hits for free.
- **Degree of unsaturation** (DBE) must be ≥ 0 and an integer (half-
  integers mean the formula is non-physical).
- **Senior's rules** — the sum of atomic valences must be even, and
  at least 2·(atoms − 1); otherwise the formula cannot correspond to
  any connected covalent structure.

Ranking: ascending |ppm error|, with a small tie-breaker penalty for
less common heteroatom combinations so vanilla C/H/N/O candidates
appear before exotic ones.

The enumeration is brute-force over user-supplied elemental bounds,
which is fine up to ~m/z 2000 for standard organic-molecule limits
(C ≤ 100, H ≤ 200, N ≤ 10, O ≤ 10, S ≤ 5, P ≤ 3, halogens ≤ 5).
The hot loop lives in :func:`_enumerate` and short-circuits as soon
as the minimum achievable mass exceeds the upper window — this cuts
total iterations by 2-3 orders of magnitude on typical searches.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

from orgchem.core.ms import ISOTOPES


# ---------------------------------------------------------------------

#: Monoisotopic mass of the most-abundant isotope for each element.
MONOISOTOPIC: Dict[str, float] = {
    elem: iso_list[0][0] for elem, iso_list in ISOTOPES.items()
}


#: Typical covalent valence. Used by Senior's rule + DBE.
VALENCE: Dict[str, int] = {
    "C": 4, "N": 3, "O": 2, "H": 1, "F": 1, "Cl": 1, "Br": 1, "I": 1,
    "P": 3, "S": 2,
}


#: Default elemental bounds for a "standard" organic-chem search.
DEFAULT_BOUNDS: Dict[str, Tuple[int, int]] = {
    "C":  (0, 50),
    "H":  (0, 100),
    "N":  (0, 10),
    "O":  (0, 10),
    "S":  (0, 3),
    "P":  (0, 2),
    "F":  (0, 6),
    "Cl": (0, 6),
    "Br": (0, 4),
    "I":  (0, 2),
}

#: Element order for enumeration (heaviest → lightest so pruning wins
#: earliest). H is placed last so it acts as the "rounding" dimension.
_ENUM_ORDER: Tuple[str, ...] = ("I", "Br", "Cl", "S", "P", "F", "C", "N", "O", "H")


# ---------------------------------------------------------------------

@dataclass(frozen=True)
class FormulaCandidate:
    formula: str                   # Hill-ordered formula string, e.g. "C8H9NO2"
    counts: Dict[str, int] = field(hash=False, compare=False,
                                   default_factory=dict)
    theoretical_mass: float = 0.0
    ppm_error: float = 0.0         # signed, measured-over-theoretical
    dbe: float = 0.0               # degree of unsaturation
    valence_sum: int = 0

    def as_dict(self) -> Dict[str, object]:
        return {
            "formula": self.formula,
            "counts": dict(self.counts),
            "theoretical_mass": round(self.theoretical_mass, 5),
            "ppm_error": round(self.ppm_error, 2),
            "dbe": self.dbe,
            "valence_sum": self.valence_sum,
        }


# ---------------------------------------------------------------------
# Public API

def guess_formula(mass: float, ppm_tolerance: float = 5.0,
                  bounds: Optional[Dict[str, Tuple[int, int]]] = None,
                  top_k: int = 20,
                  apply_nitrogen_rule: bool = True,
                  apply_senior_rule: bool = True,
                  ) -> List[FormulaCandidate]:
    """Return the top-K candidate molecular formulas for ``mass``.

    ``ppm_tolerance`` defines the +/- window. Candidates are filtered
    by the nitrogen rule and Senior's rule, then ranked by
    |ppm error|. A bounded search (``bounds``) keeps the hot loop
    small — default bounds cover standard drug-like space up to
    ~m/z 1500.
    """
    if mass <= 0:
        raise ValueError(f"mass must be positive, got {mass!r}")
    if ppm_tolerance <= 0:
        raise ValueError(f"ppm_tolerance must be positive, "
                         f"got {ppm_tolerance!r}")

    bounds = _merge_bounds(bounds or {})
    window = mass * ppm_tolerance / 1e6
    lo, hi = mass - window, mass + window

    candidates: List[FormulaCandidate] = []
    for counts, theo in _enumerate(bounds, lo, hi):
        if apply_nitrogen_rule and not _passes_nitrogen_rule(counts, mass):
            continue
        dbe = _degree_of_unsaturation(counts)
        if dbe < 0 or not _is_integer(dbe):
            continue
        vsum = _valence_sum(counts)
        if apply_senior_rule and not _passes_senior(counts, vsum):
            continue
        ppm = (mass - theo) / theo * 1e6
        candidates.append(FormulaCandidate(
            formula=_hill_formula(counts),
            counts=dict(counts),
            theoretical_mass=theo,
            ppm_error=ppm,
            dbe=dbe,
            valence_sum=vsum,
        ))

    # Sort: |ppm| ascending, then light-heteroatom preference
    candidates.sort(key=lambda c: (abs(c.ppm_error),
                                   _heteroatom_penalty(c.counts)))
    return candidates[:top_k]


def suggest_formula_for_smiles(smiles: str, ppm_tolerance: float = 5.0,
                               **kwargs) -> Dict[str, object]:
    """Round-trip helper: compute the monoisotopic mass of ``smiles``
    (via Phase-4 :func:`monoisotopic_mass`), then call
    :func:`guess_formula` on that mass.  Handy sanity check: the
    correct formula should rank first with ppm ≈ 0.
    """
    from orgchem.core.ms import monoisotopic_mass
    mass = monoisotopic_mass(smiles)
    if mass is None:
        return {"error": f"Could not compute mass for {smiles!r}"}
    hits = guess_formula(mass, ppm_tolerance=ppm_tolerance, **kwargs)
    return {
        "input_smiles": smiles,
        "measured_mass": round(mass, 5),
        "ppm_tolerance": ppm_tolerance,
        "n_candidates": len(hits),
        "candidates": [c.as_dict() for c in hits],
    }


# ---------------------------------------------------------------------
# Internals

def _merge_bounds(user: Dict[str, Tuple[int, int]]
                  ) -> Dict[str, Tuple[int, int]]:
    merged = dict(DEFAULT_BOUNDS)
    merged.update(user)
    return merged


def _enumerate(bounds: Dict[str, Tuple[int, int]],
               lo: float, hi: float
               ) -> Iterator[Tuple[Dict[str, int], float]]:
    """Yield (counts, theoretical_mass) for formulas in the window.

    Uses a per-element for-loop with an early cutoff: once the
    accumulated mass plus the *minimum* remaining contribution
    exceeds ``hi``, skip deeper nesting. The final "H" dimension
    snaps to the unique count whose mass lands inside [lo, hi].
    """
    elements = tuple(e for e in _ENUM_ORDER
                     if bounds.get(e, (0, 0))[1] > 0)
    iso_mass = {e: MONOISOTOPIC[e] for e in elements}
    elem_counts: Dict[str, int] = {e: 0 for e in elements}

    def recurse(idx: int, mass_so_far: float
                ) -> Iterator[Tuple[Dict[str, int], float]]:
        if idx == len(elements):
            if lo <= mass_so_far <= hi:
                yield dict(elem_counts), mass_so_far
            return
        elem = elements[idx]
        low, high = bounds[elem]
        m = iso_mass[elem]

        # For the last element, snap directly.
        if idx == len(elements) - 1:
            n_lo = max(low, int((lo - mass_so_far) / m))
            n_hi = min(high, int((hi - mass_so_far) / m) + 1)
            for n in range(n_lo, n_hi + 1):
                new_mass = mass_so_far + n * m
                if lo <= new_mass <= hi:
                    elem_counts[elem] = n
                    yield dict(elem_counts), new_mass
            return

        for n in range(low, high + 1):
            new_mass = mass_so_far + n * m
            if new_mass > hi:
                break
            elem_counts[elem] = n
            yield from recurse(idx + 1, new_mass)
        elem_counts[elem] = 0

    yield from recurse(0, 0.0)


def _degree_of_unsaturation(counts: Dict[str, int]) -> float:
    """DBE = 1 + (Σᵢ nᵢ(vᵢ − 2)) / 2"""
    acc = 0.0
    for elem, n in counts.items():
        v = VALENCE.get(elem)
        if v is None:
            continue
        acc += n * (v - 2)
    return 1.0 + acc / 2.0


def _is_integer(x: float, eps: float = 1e-9) -> bool:
    return abs(x - round(x)) < eps


def _passes_nitrogen_rule(counts: Dict[str, int], mass: float) -> bool:
    """Odd N → odd nominal mass (and vice-versa) for neutral molecules."""
    n_n = counts.get("N", 0)
    nominal = round(mass)
    # Parity of nominal mass must equal parity of nitrogen count.
    return (nominal % 2) == (n_n % 2)


def _valence_sum(counts: Dict[str, int]) -> int:
    return sum(counts.get(e, 0) * VALENCE[e] for e in VALENCE)


def _passes_senior(counts: Dict[str, int], valence_sum: int) -> bool:
    """Senior's rules: Σ valence is even, and ≥ 2·(atoms - 1).

    The second clause guarantees the formula can correspond to a
    connected graph. Chemists sometimes call this the "degree-sum"
    test.
    """
    if valence_sum % 2 != 0:
        return False
    n_atoms = sum(counts.get(e, 0) for e in VALENCE)
    if n_atoms <= 1:
        return True
    return valence_sum >= 2 * (n_atoms - 1)


def _heteroatom_penalty(counts: Dict[str, int]) -> float:
    """Tie-breaker score: plain C/H/N/O wins over exotic halogens."""
    penalty = 0.0
    for elem, n in counts.items():
        if elem in ("C", "H", "N", "O"):
            continue
        if n == 0:
            continue
        if elem == "S":
            penalty += 0.1 * n
        elif elem == "P":
            penalty += 0.2 * n
        elif elem in ("F", "Cl"):
            penalty += 0.3 * n
        else:
            penalty += 0.5 * n
    return penalty


_HILL_PRIORITY = ["C", "H", "N", "O", "S", "P",
                  "F", "Cl", "Br", "I"]


def _hill_formula(counts: Dict[str, int]) -> str:
    parts: List[str] = []
    for e in _HILL_PRIORITY:
        n = counts.get(e, 0)
        if n > 0:
            parts.append(e if n == 1 else f"{e}{n}")
    # Any element not in the priority list (none by default) trails.
    for e in sorted(counts):
        if e in _HILL_PRIORITY:
            continue
        n = counts[e]
        if n > 0:
            parts.append(e if n == 1 else f"{e}{n}")
    return "".join(parts)
