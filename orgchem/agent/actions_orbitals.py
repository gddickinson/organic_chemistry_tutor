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
def show_molecular_orbital(smiles: str, index: int = -1) -> Dict[str, Any]:
    """Describe one molecular orbital from the Hückel calculation.

    ``index``: 0-based MO index from the lowest-energy (most bonding)
    end. Pass ``-1`` (default) for HOMO, ``-2`` for HOMO-1, ...; pass
    the literal strings ``"HOMO"`` / ``"LUMO"`` by setting ``index``
    via the energy list length (HOMO → n_occupied-1, LUMO →
    n_occupied). Returns the picked MO's energy, occupation, and a
    short interpretation relative to the HOMO / LUMO window.
    """
    from orgchem.core.huckel import huckel_for_smiles
    try:
        r = huckel_for_smiles(smiles)
    except ValueError as e:
        return {"error": str(e)}
    n = r.n_pi_atoms
    if n == 0:
        return {"error": "No π system — nothing to plot."}
    n_occ = sum(1 for o in r.occupations if o > 0)
    homo_idx = n_occ - 1
    lumo_idx = n_occ
    # Accept -1 as alias for HOMO (the common call convention).
    idx = homo_idx if index == -1 else int(index)
    if idx < 0 or idx >= n:
        return {"error": f"MO index {idx} out of range [0, {n - 1}]"}
    energy = r.energies[idx]
    occ = r.occupations[idx]
    if idx == homo_idx:
        role = "HOMO"
    elif idx == lumo_idx:
        role = "LUMO"
    elif idx < homo_idx:
        role = f"HOMO-{homo_idx - idx}"
    else:
        role = f"LUMO+{idx - lumo_idx}"
    return {
        "smiles": smiles,
        "index": idx,
        "role": role,
        "energy_beta": energy,
        "occupation": occ,
        "n_pi_atoms": n,
        "n_pi_electrons": r.n_pi_electrons,
        "homo_index": homo_idx,
        "lumo_index": lumo_idx,
        "homo_energy": r.homo_energy,
        "lumo_energy": r.lumo_energy,
    }


@action(category="orbitals")
def explain_wh(reaction_name_or_id: str) -> Dict[str, Any]:
    """Look up the Woodward-Hoffmann rule that governs a seeded
    named reaction (Phase 14b follow-up).

    Accepts either a reaction DB id (integer string) or a substring
    of the reaction's name (e.g. ``"Diels-Alder"``, ``"Claisen"``,
    ``"[3,3]"``). Returns the matched rule's full WH entry plus the
    originating reaction name.
    """
    from orgchem.core.wh_rules import find_wh_rule_for_reaction, get_rule
    reaction_name: str = ""
    # Try DB lookup first.
    try:
        rxn_id = int(reaction_name_or_id)
        from orgchem.db.models import Reaction as DBRxn
        from orgchem.db.session import session_scope
        with session_scope() as s:
            row = s.query(DBRxn).filter(DBRxn.id == rxn_id).one_or_none()
            if row is not None:
                reaction_name = row.name
    except (ValueError, TypeError):
        reaction_name = reaction_name_or_id
    if not reaction_name:
        return {"error": f"No reaction matching {reaction_name_or_id!r}"}
    rule_id = find_wh_rule_for_reaction(reaction_name)
    if rule_id is None:
        return {
            "reaction": reaction_name,
            "matched": False,
            "note": ("No pericyclic WH rule maps to this reaction — "
                     "it's likely ionic / radical / catalytic, not "
                     "governed by orbital-symmetry rules."),
        }
    rule = get_rule(rule_id)
    return {
        "reaction": reaction_name,
        "matched": True,
        "rule_id": rule_id,
        "rule": rule,
    }


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
