"""Agent actions for Phase 19 — medicinal chemistry descriptors."""
from __future__ import annotations
import logging
from typing import Any, Dict

from orgchem.agent.actions import action

log = logging.getLogger(__name__)


@action(category="medchem")
def list_bioisosteres() -> list:
    """Enumerate the Phase 19c bioisostere template catalogue."""
    from orgchem.core.bioisosteres import list_bioisosteres as _list
    return _list()


@action(category="medchem")
def suggest_bioisosteres(smiles: str, template_ids: list = None) -> Dict[str, Any]:
    """Apply every catalogued bioisostere template to a molecule.

    Returns the set of unique SMILES variants produced by swapping one
    functional group for its isosteric equivalent — COOH ↔ tetrazole,
    CH₃ ↔ CF₃, phenyl ↔ thiophene, amide ↔ sulfonamide, etc.
    ``template_ids`` optionally restricts to a subset of the 14
    templates (see `list_bioisosteres`).
    """
    from orgchem.core.bioisosteres import suggest_bioisosteres as _suggest
    return _suggest(smiles, template_ids=template_ids)


@action(category="medchem")
def drug_likeness(smiles: str = "", molecule_id: int = 0) -> Dict[str, Any]:
    """Compute Lipinski / Veber / Ghose / PAINS / QED for a molecule.

    Accepts either a raw SMILES or a DB molecule id. Returns a nested
    dict with per-rule pass/fail flags plus the QED score.
    """
    from orgchem.core.druglike import drug_likeness_report
    smi = smiles
    if not smi and molecule_id:
        from orgchem.db.session import session_scope
        from orgchem.db.models import Molecule as DBMol
        with session_scope() as s:
            row = s.get(DBMol, int(molecule_id))
            if row is None:
                return {"error": f"No molecule id {molecule_id}"}
            smi = row.smiles
            name = row.name
    elif molecule_id:
        name = ""
    else:
        name = ""
    if not smi:
        return {"error": "Supply either smiles= or molecule_id="}
    try:
        report = drug_likeness_report(smi)
    except ValueError as e:
        return {"error": str(e)}
    return {"smiles": smi, "name": name, **report}
