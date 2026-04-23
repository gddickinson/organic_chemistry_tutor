"""Empirical and molecular formula calculator.

Inspired by Verma, Singh & Passey (2024), *Rasayan J. Chem.* 17(4), 1460–1472,
`refs/4325_pdf.pdf`. The paper's algorithm (normalise ratios, then try
``k = 1, 2, 3, …`` until every normalised ratio is within a fixed tolerance
of an integer) only works cleanly if the atomic masses are whole numbers —
because with real masses (H = 1.008, C = 12.011, …) the absolute error in a
normalised ratio *grows with the number of atoms of that element*. Cholesterol
has 46 hydrogens, so the 0.8 % error in using H = 1.008 vs 1 inflates to
~0.35 atoms, pushing the paper's tolerance past ``k = 1`` and producing a
wildly wrong empirical formula.

We use a simpler algorithm that benefits from knowing the molar mass:

    atoms(X) = ( %X / 100 ) × molar_mass / atomic_mass(X)

Round to the nearest integer; empirical formula = molecular / GCD.

This is robust against the rounding pathology above because we never
normalise or iterate over scale factors — we compute each element's count
directly from the one quantity a student always has: the molar mass.

Default atomic masses are IUPAC 2019 values. Pass
``masses=ATOMIC_MASSES_INTEGER`` to reproduce the paper's exact numbers.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import reduce
from math import gcd
from typing import Dict, List

#: IUPAC 2019 standard atomic weights (g/mol). The default mass table.
ATOMIC_MASSES: Dict[str, float] = {
    "H": 1.008, "He": 4.003, "Li": 6.94, "Be": 9.012, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Br": 79.904, "I": 126.904,
}

#: Whole-number masses matching Verma et al. 2024 for reproducing their
#: Table 1 exactly. Pass via the ``masses=`` keyword of :func:`compute_formula`.
ATOMIC_MASSES_INTEGER: Dict[str, float] = {
    "H": 1, "He": 4, "Li": 7, "Be": 9, "B": 11,
    "C": 12, "N": 14, "O": 16, "F": 19, "Ne": 20,
    "Na": 23, "Mg": 24, "Al": 27, "Si": 28, "P": 31,
    "S": 32, "Cl": 35.5, "Ar": 40, "K": 39, "Ca": 40,
    "Fe": 56, "Cu": 63.5, "Zn": 65, "Br": 79.9, "I": 126.9,
}


@dataclass
class FormulaResult:
    empirical_formula: str
    molecular_formula: str
    empirical_mass: float
    scale_factor: int
    empirical_counts: Dict[str, int]
    molecular_counts: Dict[str, int]
    #: Maximum |raw_atoms − rounded_atoms| across all elements. Useful for
    #: flagging inconsistent input (e.g. %s that don't sum to ~100 given MW).
    max_residual: float = 0.0
    #: Element with the worst residual (diagnostic only).
    worst_element: str = ""


def compute_formula(percentages: Dict[str, float], molar_mass: float,
                    tol: float = 0.4,
                    masses: Dict[str, float] | None = None) -> FormulaResult:
    """Compute empirical and molecular formulas from mass percentages + molar mass.

    Parameters
    ----------
    percentages : dict[str, float]
        Element symbol → mass percentage (should sum to ~100).
    molar_mass : float
        Compound's molar mass in g/mol.
    tol : float
        Maximum allowed |raw_atoms − rounded_atoms| for any element. The
        direct algorithm rounds each element's computed atom count to the
        nearest integer; if the pre-rounding residual exceeds *tol* the
        inputs are probably inconsistent and we raise. Default 0.4 accepts
        all typical textbook and lab-analysis inputs.
    masses : dict[str, float], optional
        Atomic mass table. Defaults to IUPAC 2019 masses
        (:data:`ATOMIC_MASSES`). Pass :data:`ATOMIC_MASSES_INTEGER` to
        reproduce Verma et al. 2024 exactly.

    Returns
    -------
    FormulaResult
        Includes both the empirical (reduced) and molecular formulas,
        plus the largest rounding residual for diagnostics.
    """
    table = masses if masses is not None else ATOMIC_MASSES
    if not percentages:
        raise ValueError("Need at least one element")
    unknown = [el for el in percentages if el not in table]
    if unknown:
        raise ValueError(f"Unknown element symbols: {unknown}")
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive")
    if any(v < 0 for v in percentages.values()):
        raise ValueError("All percentages must be non-negative")

    # Direct count: atoms(X) = (pct/100) × MW / atomic_mass(X)
    molecular_counts: Dict[str, int] = {}
    worst_residual = 0.0
    worst_element = ""
    for el, pct in percentages.items():
        if pct == 0:
            continue
        mass_of_el = (pct / 100.0) * molar_mass
        raw_atoms = mass_of_el / table[el]
        rounded = int(round(raw_atoms))
        if rounded < 1:
            # Present but sub-atomic → either trace impurity or bad inputs.
            if raw_atoms > 0.5:
                rounded = 1
            else:
                continue
        residual = abs(raw_atoms - rounded)
        if residual > worst_residual:
            worst_residual = residual
            worst_element = el
        molecular_counts[el] = rounded

    if not molecular_counts:
        raise ValueError("No element yielded ≥1 atom — check percentages / molar mass")
    if worst_residual > tol:
        raise ValueError(
            f"Element {worst_element!r} does not round to an integer atom count "
            f"within ±{tol} (residual {worst_residual:.3f}). "
            f"Check that the percentages sum to ~100 and the molar mass is correct."
        )

    # Empirical = molecular / GCD of all counts.
    g = reduce(gcd, molecular_counts.values())
    empirical_counts = {el: n // g for el, n in molecular_counts.items()}
    empirical_mass = sum(table[el] * n for el, n in empirical_counts.items())

    return FormulaResult(
        empirical_formula=_format(empirical_counts),
        molecular_formula=_format(molecular_counts),
        empirical_mass=empirical_mass,
        scale_factor=g,
        empirical_counts=empirical_counts,
        molecular_counts=molecular_counts,
        max_residual=worst_residual,
        worst_element=worst_element,
    )


def _format(counts: Dict[str, int]) -> str:
    """Render counts into a Hill-ordered formula (C, H, then alphabetical)."""
    parts: List[str] = []
    remaining = dict(counts)
    for el in ("C", "H"):
        if el in remaining:
            n = remaining.pop(el)
            parts.append(el if n == 1 else f"{el}{n}")
    for el in sorted(remaining):
        n = remaining[el]
        parts.append(el if n == 1 else f"{el}{n}")
    return "".join(parts)
