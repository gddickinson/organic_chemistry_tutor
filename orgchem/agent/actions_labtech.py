"""Agent actions for Phase 15 — practical laboratory techniques."""
from __future__ import annotations
import logging
from typing import Any, Dict, List

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="lab")
def predict_tlc(smiles_list: List[str],
                solvent: str = "hexane:ethyl_acetate:1:1") -> Dict[str, Any]:
    """Predict TLC Rf for a mixture of compounds in one mobile phase.

    Uses a teaching-grade logP-based sigmoid — qualitatively correct, not
    quantitatively so. Accepts solvent names or simple mixtures like
    ``"hexane:ethyl_acetate:3:1"``.
    """
    from orgchem.core.chromatography import simulate_tlc
    return simulate_tlc(list(smiles_list), solvent=solvent)


@action(category="lab")
def predict_rf(smiles: str,
               solvent: str = "hexane:ethyl_acetate:1:1") -> Dict[str, Any]:
    """Predict TLC Rf for a single molecule in a given mobile phase."""
    from orgchem.core.chromatography import predict_rf as _predict
    return _predict(smiles, solvent=solvent)


@action(category="lab")
def recrystallisation_yield(s_hot: float, s_cold: float,
                            m_crude_g: float,
                            solvent_volume_ml: float,
                            purity_hot: float = 1.0) -> Dict[str, Any]:
    """Predict recrystallisation yield (g crystals + %) for a single-solvent system.

    Inputs: solubilities g/100 mL at hot and cold temperatures, crude mass,
    hot-solvent volume, and the crude's purity (0-1).
    """
    from orgchem.core.lab_techniques import recrystallisation_yield as _ry
    return _ry(s_hot, s_cold, m_crude_g, solvent_volume_ml, purity_hot)


@action(category="lab")
def distillation_plan(component_a: str, component_b: str) -> Dict[str, Any]:
    """Recommend simple / fractional / non-distillation for a two-component mixture.

    Components are DB molecule names (bp values are tabulated for the
    common teaching set — Water, Ethanol, Acetone, Toluene, …).
    """
    from orgchem.core.lab_techniques import distillation_plan as _plan
    return _plan((component_a, component_b))


@action(category="lab")
def extraction_plan(pka: float, ph: float, is_acid: bool = True,
                    smiles: str = "") -> Dict[str, Any]:
    """Henderson-Hasselbalch partition: organic vs aqueous at a given pH.

    Returns fractions of neutral / ionised form and whether the
    molecule will sit in the organic or aqueous phase. Provide ``smiles``
    to get logP alongside for extra context.
    """
    from orgchem.core.lab_techniques import extraction_plan as _ep, logp_of
    logp = None
    if smiles:
        try:
            logp = logp_of(smiles)
        except ValueError as e:
            return {"error": str(e)}
    return _ep(pka=pka, ph=ph, is_acid=is_acid, logp_neutral=logp)
