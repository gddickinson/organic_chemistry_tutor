"""Agent actions for Phase 8d — retrosynthesis template matcher."""
from __future__ import annotations
import logging
from typing import Any, Dict

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="synthesis")
def find_retrosynthesis(target_smiles: str,
                        max_templates: int = 0) -> Dict[str, Any]:
    """Apply the 8 seeded retrosynthesis templates to a target SMILES.

    Returns every proposed one-step disconnection: ester / amide /
    biaryl-Suzuki / Williamson ether / aldol / Diels-Alder retro /
    nitration / reductive amination. Each proposal gives a label,
    description, the forward reaction it corresponds to, and the
    precursor SMILES.
    """
    from orgchem.core.retrosynthesis import find_retrosynthesis as _find
    return _find(target_smiles, max_templates=max_templates)


@action(category="synthesis")
def list_retro_templates() -> list:
    """Enumerate the retrosynthesis template catalogue."""
    from orgchem.core.retrosynthesis import list_templates
    return list_templates()


@action(category="synthesis")
def find_multi_step_retrosynthesis(target_smiles: str,
                                   max_depth: int = 3,
                                   max_branches: int = 3,
                                   top_paths: int = 10) -> Dict[str, Any]:
    """Recursive retrosynthesis (Phase 8d follow-up).

    Walk the retro-template catalogue to ``max_depth`` disconnections,
    stopping on each precursor that is either ≤8 heavy atoms, already
    in the molecule DB, or has no disconnectable handles. Returns the
    full tree plus the top-``top_paths`` shortest linear routes.
    """
    from orgchem.core.retrosynthesis import find_multi_step_retrosynthesis as _find
    return _find(target_smiles, max_depth=max_depth,
                 max_branches=max_branches, top_paths=top_paths)
