"""Agent actions for Phase 29 lipids + nucleic-acids data modules."""
from __future__ import annotations
from typing import Any, Dict, List

from orgchem.agent.actions import action


# ---- Lipids ---------------------------------------------------------


@action(category="lipid")
def list_lipids(family: str = "") -> List[Dict[str, Any]]:
    """Enumerate seeded lipids, optionally filtered by family
    (``fatty-acid`` / ``triglyceride`` / ``phospholipid`` /
    ``sphingolipid`` / ``sterol`` / ``vitamin``)."""
    from orgchem.core.lipids import list_lipids as _list
    return _list(family)


@action(category="lipid")
def get_lipid(lipid_name: str) -> Dict[str, Any]:
    """Full entry by name (case-insensitive)."""
    from orgchem.core.lipids import get_lipid as _get
    l = _get(lipid_name)
    if l is None:
        return {"error": f"Unknown lipid: {lipid_name!r}"}
    return l.to_dict()


@action(category="lipid")
def lipid_families() -> List[str]:
    """The family taxonomy (ordered)."""
    from orgchem.core.lipids import lipid_families as _fams
    return _fams()


# ---- Nucleic acids --------------------------------------------------


@action(category="nucleic-acid")
def list_nucleic_acids(family: str = "") -> List[Dict[str, Any]]:
    """Enumerate seeded nucleic-acid entries, optionally filtered by
    family (``nucleobase`` / ``nucleoside`` / ``nucleotide`` /
    ``oligonucleotide`` / ``pdb-motif``)."""
    from orgchem.core.nucleic_acids import list_nucleic_acids as _list
    return _list(family)


@action(category="nucleic-acid")
def get_nucleic_acid(na_name: str) -> Dict[str, Any]:
    """Full entry by name (case-insensitive)."""
    from orgchem.core.nucleic_acids import get_nucleic_acid as _get
    n = _get(na_name)
    if n is None:
        return {"error": f"Unknown nucleic-acid entry: {na_name!r}"}
    return n.to_dict()


@action(category="nucleic-acid")
def nucleic_acid_families() -> List[str]:
    """The family taxonomy (ordered)."""
    from orgchem.core.nucleic_acids import nucleic_acid_families as _fams
    return _fams()
