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
def drug_likeness(smiles: str = "", molecule_id: int = 0,
                  name: str = "") -> Dict[str, Any]:
    """Compute Lipinski / Veber / Ghose / PAINS / QED for a molecule.

    Accepts any one of: a raw SMILES, a DB ``molecule_id``, or a
    ``name`` (resolved via :func:`find_molecule_by_name` so synonyms
    + case-tolerant lookups work — pass ``"aspirin"`` /
    ``"Aspirin"`` / ``"acetylsalicylic acid"``).  Returns a nested
    dict with per-rule pass/fail flags plus the QED score.

    Round 205 — added the ``name`` fallback after a tutor-test
    surfaced the LLM repeatedly passing broken SMILES strings for
    well-known drugs that ARE in the DB by name.
    """
    from orgchem.core.druglike import drug_likeness_report
    smi = smiles
    resolved_name = ""
    if not smi and molecule_id:
        from orgchem.db.session import session_scope
        from orgchem.db.models import Molecule as DBMol
        with session_scope() as s:
            row = s.get(DBMol, int(molecule_id))
            if row is None:
                return {"error": f"No molecule id {molecule_id}"}
            smi = row.smiles
            resolved_name = row.name
    if not smi and name:
        from orgchem.db.queries import find_molecule_by_name
        row = find_molecule_by_name(name)
        if row is None:
            return {"error": f"No molecule matching name {name!r}"}
        smi = row.smiles
        resolved_name = row.name
    if not smi:
        return {"error": "Supply one of smiles=, molecule_id=, "
                         "or name="}
    try:
        report = drug_likeness_report(smi)
    except ValueError as e:
        return {"error": str(e)}
    return {"smiles": smi, "name": resolved_name, **report}
