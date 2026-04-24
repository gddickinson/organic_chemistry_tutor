"""PubChem data source via ``pubchempy``."""
from __future__ import annotations
import logging
from typing import List

from orgchem.core.molecule import Molecule
from orgchem.sources.base import DataSource
from orgchem.messaging.errors import NetworkError

log = logging.getLogger(__name__)


class PubChemSource(DataSource):
    name = "PubChem"

    def search(self, query: str, limit: int = 10) -> List[dict]:
        try:
            import pubchempy as pcp
        except ImportError as e:
            raise NetworkError("pubchempy not installed — pip install pubchempy") from e
        try:
            compounds = pcp.get_compounds(query, namespace="name", listkey_count=limit)
        except Exception as e:
            raise NetworkError(f"PubChem search failed: {e}") from e
        out: List[dict] = []
        for c in compounds[:limit]:
            out.append({
                "id": str(c.cid),
                "name": c.iupac_name or query,
                "formula": c.molecular_formula or "",
            })
        return out

    def fetch(self, identifier: str) -> Molecule:
        try:
            import pubchempy as pcp
        except ImportError as e:
            raise NetworkError("pubchempy not installed") from e
        try:
            c = pcp.Compound.from_cid(int(identifier))
        except Exception as e:
            raise NetworkError(f"PubChem fetch failed: {e}") from e
        smi = c.canonical_smiles
        if not smi:
            raise NetworkError(f"CID {identifier} has no canonical SMILES")
        # Round 58 — prefer a common-name ("title") for display over
        # the long systematic IUPAC name. PubChem's "synonyms" list
        # is ordered by usage; its first entry is usually the
        # recognised trivial name (e.g. "Retinol" rather than
        # "(2E,4E,6E,8E)-3,7-dimethyl-9-(…)nona-2,4,6,8-tetraen-1-ol").
        synonyms = list(c.synonyms or [])
        primary = _pick_display_name(synonyms, c.iupac_name,
                                     fallback=f"CID {identifier}")
        m = Molecule.from_smiles(smi, name=primary)
        m.source = f"PubChem:{identifier}"
        m.properties["cid"] = identifier
        m.properties["iupac_name"] = c.iupac_name or ""
        m.properties["synonyms"] = synonyms[:10]
        return m


def fetch_synonyms_by_inchikey(inchikey: str,
                               limit: int = 10) -> List[str]:
    """Phase 35b — best-effort PubChem synonym lookup by InChIKey.

    Returns a list of up to *limit* natural-language synonyms on
    success; returns an empty list on any failure (missing
    ``pubchempy``, network error, compound not found).  Never
    raises — callers use this purely to decorate a DB row, not
    to gate the insert.
    """
    key = (inchikey or "").strip()
    if not key:
        return []
    try:
        import pubchempy as pcp
    except ImportError:
        return []
    try:
        hits = pcp.get_compounds(key, namespace="inchikey")
    except Exception:  # noqa: BLE001 — network / HTTP / parse errors
        return []
    for c in hits or []:
        try:
            syns = list(c.synonyms or [])
        except Exception:  # noqa: BLE001
            continue
        if syns:
            return syns[:limit]
    return []


def _pick_display_name(synonyms, iupac_name, fallback):
    """Choose a friendly display name from PubChem output.

    Prefers the first short synonym (≤ 40 chars, no trailing
    stereochemistry-heavy IUPAC descriptors) over the raw
    ``iupac_name`` field — PubChem's synonym list is ordered by
    usage frequency, so the head of the list is almost always the
    trivial name. Falls back to ``iupac_name`` then to ``fallback``
    (typically the CID).
    """
    for syn in synonyms or []:
        if not syn or len(syn) > 40:
            continue
        # Skip obvious systematic forms (any parenthesised stereo
        # prefix like "(2E,4E,…)" or bracketed numeric prefixes).
        if syn.startswith("(") and "," in syn[:20]:
            continue
        if syn[:1].isdigit():
            continue
        return syn
    return iupac_name or fallback
