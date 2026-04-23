"""Agent actions for Phase 20d session save/restore and Phase 4 EI-MS
fragmentation sketch.

Kept together in one module so the registry cleanup is easier — both
sets of actions are small and share the same spectroscopy / session
teaching flow.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Session state (Phase 20d)

@action(category="session")
def list_sessions() -> List[Dict[str, Any]]:
    """Enumerate saved sessions under the per-user config dir."""
    from orgchem.core.session_state import list_sessions as _list
    return _list()


@action(category="session")
def save_session_state(session_name: str = "session",
                       active_tab: str = "",
                       current_molecule_smiles: str = "",
                       protein_pdb_id: str = "",
                       protein_ligand_name: str = "",
                       hrms_mass: Optional[float] = None,
                       hrms_ppm_tolerance: Optional[float] = None,
                       notes: str = "",
                       ) -> Dict[str, Any]:
    """Write a minimal session state to the default sessions directory."""
    from orgchem.core.session_state import (
        SessionState, save_session, default_session_path,
    )
    state = SessionState(
        name=session_name,
        active_tab=active_tab,
        current_molecule_smiles=current_molecule_smiles,
        protein_pdb_id=protein_pdb_id,
        protein_ligand_name=protein_ligand_name,
        hrms_mass=hrms_mass,
        hrms_ppm_tolerance=hrms_ppm_tolerance,
        notes=notes,
    )
    path = default_session_path(session_name)
    save_session(state, path)
    return {"path": str(path), "name": state.name,
            "saved_at": state.saved_at}


@action(category="session")
def load_session_state(path: str) -> Dict[str, Any]:
    """Load a session YAML file by path; returns the state as a dict."""
    from dataclasses import asdict
    from orgchem.core.session_state import load_session
    p = Path(path)
    if not p.exists():
        return {"error": f"No session at {path!r}"}
    state = load_session(p)
    return asdict(state)


# ---------------------------------------------------------------------
# EI-MS fragmentation (Phase 4 follow-up)

@action(category="spectroscopy")
def predict_ms_fragments(smiles: str,
                         min_mz: float = 20.0) -> Dict[str, Any]:
    """Predict common EI-MS fragment peaks for ``smiles``.

    Returns the molecular ion plus every neutral-loss candidate whose
    SMARTS precondition matches the molecule (M−15 methyl, M−18 H₂O,
    M−28 CO, M−43 acetyl, etc.). m/z assumes z = +1.
    """
    from orgchem.core.ms_fragments import predict_fragments
    try:
        report = predict_fragments(smiles, min_mz=min_mz)
    except ValueError as e:
        return {"error": str(e)}
    return report.summary()
