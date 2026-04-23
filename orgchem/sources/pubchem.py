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
        m = Molecule.from_smiles(smi, name=c.iupac_name or f"CID {identifier}")
        m.source = f"PubChem:{identifier}"
        m.properties["cid"] = identifier
        m.properties["synonyms"] = (c.synonyms or [])[:10]
        return m
