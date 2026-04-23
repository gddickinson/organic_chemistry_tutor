"""Agent actions for Phase 14a — simple Hückel MO theory.

Separated from ``library.py`` to keep modules under the 500-line cap.
Registration happens on import via ``orgchem/agent/__init__.py``.
"""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="orbitals")
def huckel_mos(smiles: str) -> Dict[str, Any]:
    """Return Hückel MO energies and HOMO/LUMO info for a conjugated system.

    Handles canonical teaching cases: linear polyenes (ethene, butadiene,
    hexatriene), allyl cation / radical / anion, aromatic rings (benzene,
    pyridine, pyrrole, furan, thiophene, Cp⁻). Energies are in units of β
    (with α = 0 as reference).
    """
    from orgchem.core.huckel import huckel_for_smiles
    try:
        r = huckel_for_smiles(smiles)
    except ValueError as e:
        return {"error": str(e)}
    return {
        "smiles": smiles,
        "n_pi_atoms": r.n_pi_atoms,
        "n_pi_electrons": r.n_pi_electrons,
        "energies_beta": r.energies,
        "occupations": r.occupations,
        "homo_energy": r.homo_energy,
        "lumo_energy": r.lumo_energy,
        "total_pi_energy": r.total_pi_energy,
        "atom_indices": r.atom_indices,
    }


@action(category="orbitals")
def list_wh_rules(family: str = "") -> list:
    """Enumerate Woodward-Hoffmann selection rules (Phase 14b).

    Optionally filter by family: cycloaddition / electrocyclic /
    sigmatropic / general.
    """
    from orgchem.core.wh_rules import list_rules
    return list_rules(family=family)


@action(category="orbitals")
def get_wh_rule(rule_id: str) -> Dict[str, Any]:
    """Return full detail for one Woodward-Hoffmann rule by id."""
    from orgchem.core.wh_rules import get_rule
    return get_rule(rule_id)


@action(category="orbitals")
def check_wh_allowed(kind: str, electron_count: int,
                     regime: str = "thermal") -> Dict[str, Any]:
    """Evaluate a pericyclic step's Woodward-Hoffmann allowed-ness.

    ``kind``: ``"cycloaddition"`` / ``"electrocyclic"`` / ``"sigmatropic"``.
    ``electron_count``: total π electrons in the transition state.
    ``regime``: ``"thermal"`` or ``"photochemical"``.
    """
    from orgchem.core.wh_rules import check_allowed
    return check_allowed(kind, electron_count, regime)


@action(category="orbitals")
def export_mo_diagram(smiles: str, path: str,
                      width: int = 700, height: int = 600) -> Dict[str, Any]:
    """Render the Hückel MO level diagram for a SMILES to PNG or SVG."""
    from orgchem.core.huckel import huckel_for_smiles
    from orgchem.render.draw_mo import export_mo_diagram as _export
    try:
        r = huckel_for_smiles(smiles)
    except ValueError as e:
        return {"error": str(e)}
    out = _export(r, path, width=width, height=height,
                  title=f"π MOs — {smiles}")
    return {"path": str(out), "smiles": smiles,
            "format": Path(out).suffix.lstrip(".").lower(),
            "n_pi_atoms": r.n_pi_atoms,
            "n_pi_electrons": r.n_pi_electrons,
            "size_bytes": out.stat().st_size}
