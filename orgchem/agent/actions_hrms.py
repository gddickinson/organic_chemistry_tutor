"""Agent actions for the HRMS formula-candidate guesser — Phase 4 follow-up."""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="spectroscopy")
def guess_formula(mass: float, ppm_tolerance: float = 5.0,
                  top_k: int = 10,
                  max_c: Optional[int] = None,
                  max_n: Optional[int] = None,
                  max_o: Optional[int] = None,
                  max_s: Optional[int] = None,
                  max_halogens: Optional[int] = None,
                  ) -> Dict[str, Any]:
    """Enumerate plausible molecular formulas for an HRMS peak.

    ``mass`` is the measured monoisotopic mass in Da.
    ``ppm_tolerance`` sets the +/- window.
    Optional ``max_*`` kwargs override the default elemental bounds
    (C:50, N:10, O:10, S:3, each halogen:6). Returns the top-K
    candidates ranked by absolute ppm error with a light penalty for
    unusual heteroatom combinations.
    """
    from orgchem.core.hrms import DEFAULT_BOUNDS, guess_formula as _guess

    bounds = dict(DEFAULT_BOUNDS)
    if max_c is not None:
        bounds["C"] = (0, max_c)
    if max_n is not None:
        bounds["N"] = (0, max_n)
    if max_o is not None:
        bounds["O"] = (0, max_o)
    if max_s is not None:
        bounds["S"] = (0, max_s)
    if max_halogens is not None:
        for elem in ("F", "Cl", "Br", "I"):
            bounds[elem] = (0, max_halogens)
    try:
        hits = _guess(mass, ppm_tolerance=ppm_tolerance,
                      top_k=top_k, bounds=bounds)
    except ValueError as e:
        return {"error": str(e)}
    return {
        "measured_mass": mass,
        "ppm_tolerance": ppm_tolerance,
        "n_candidates": len(hits),
        "candidates": [c.as_dict() for c in hits],
    }


@action(category="spectroscopy")
def guess_formula_for_smiles(smiles: str, ppm_tolerance: float = 5.0,
                             top_k: int = 10) -> Dict[str, Any]:
    """Round-trip: compute the monoisotopic mass for ``smiles``, then
    enumerate formula candidates. Useful sanity check — the correct
    formula should land at rank #1 with ppm ≈ 0."""
    from orgchem.core.hrms import suggest_formula_for_smiles as _suggest
    result = _suggest(smiles, ppm_tolerance=ppm_tolerance, top_k=top_k)
    return result
