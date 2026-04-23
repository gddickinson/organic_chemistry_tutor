"""Agent actions for Phase 17e — physical-organic helpers.

Thin wrappers around :mod:`orgchem.core.physical_organic` so the
tutor can fit a Hammett plot or compute a primary KIE in one call.
"""
from __future__ import annotations
from typing import Any, Dict, Mapping

from orgchem.agent.actions import action


@action(category="phys-org")
def hammett_fit(data: Mapping[str, float],
                sigma_type: str = "sigma_p") -> Dict[str, Any]:
    """Fit log(k/k₀) (or log(K/K₀)) against tabulated Hammett σ.

    ``data`` is a mapping ``{substituent_label: log_rel_rate}``;
    keys are strings like ``"NO2"``, ``"OH"``, ``"CH3"``, ``"H"``.
    ``sigma_type`` picks which σ scale to regress against
    (``"sigma_p"`` / ``"sigma_m"`` / ``"sigma_p_minus"`` /
    ``"sigma_p_plus"``). Returns ρ, r², the fit points, and a
    short teaching interpretation.
    """
    from orgchem.core.physical_organic import hammett_fit as _fit
    return _fit(dict(data), sigma_type=sigma_type)


@action(category="phys-org")
def predict_kie(isotope_pair: str = "H/D",
                partner_element: str = "C",
                nu_H_cm1: float = 3000.0,
                temperature_K: float = 298.15) -> Dict[str, Any]:
    """Predict the primary KIE for a C–H (or N–H / O–H) cleavage.

    Uses the Bigeleisen simplification
    ``k_H/k_D ≈ exp((h·ν_H / 2·k_B·T)·(1 − √(μ_H/μ_D)))``. Inputs
    are the isotopologue pair (``"H/D"`` or ``"H/T"``), the heavy
    atom on the other side of the bond (``"C"`` / ``"N"`` /
    ``"O"``), the stretching wavenumber (``3000`` cm⁻¹ default for
    aliphatic C–H), and the temperature (``298.15`` K default).
    """
    from orgchem.core.physical_organic import predict_kie as _kie
    return _kie(isotope_pair=isotope_pair,
                partner_element=partner_element,
                nu_H_cm1=nu_H_cm1, temperature_K=temperature_K)


@action(category="phys-org")
def list_hammett_substituents() -> Dict[str, Any]:
    """Return the tabulated Hammett σ catalogue — which substituent
    labels :func:`hammett_fit` understands, with their σₘ / σₚ /
    σₚ⁻ / σₚ⁺ values."""
    from orgchem.core.physical_organic import (
        list_hammett_substituents as _cat,
    )
    return {"substituents": _cat()}
