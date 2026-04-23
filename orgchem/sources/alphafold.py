"""Fetch AlphaFold-predicted structures from EBI — Phase 24b.

The EBI AlphaFold DB (https://alphafold.ebi.ac.uk/) provides predicted
structures for most of UniProt. Endpoint pattern:

    https://alphafold.ebi.ac.uk/files/AF-<UNIPROT>-F1-model_v4.pdb

The AlphaFold PDB format uses the **B-factor column to encode pLDDT**
(per-residue confidence, 0–100). We parse exactly like a regular PDB
but surface the pLDDT values directly so teaching materials can show
the classic blue→orange confidence colouring.

Cache: ``~/Library/Caches/OrgChem/alphafold/AF-<UNIPROT>-F1.pdb``.
``parse_from_cache_or_string`` mirrors the sources/pdb.py test-friendly
entry point.
"""
from __future__ import annotations
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from orgchem.core.protein import Protein, parse_pdb_text
from orgchem.utils.paths import cache_dir

log = logging.getLogger(__name__)

AFDB_URL = "https://alphafold.ebi.ac.uk/files/AF-{uniprot}-F1-model_v{version}.pdb"
DEFAULT_VERSION = 4


@dataclass
class AlphaFoldResult:
    uniprot_id: str
    version: int
    protein: Protein
    #: Per-residue pLDDT values keyed by (chain, seq_id) → mean B-factor
    plddt_by_residue: Dict[tuple, float] = field(default_factory=dict)

    @property
    def mean_plddt(self) -> float:
        vals = list(self.plddt_by_residue.values())
        return sum(vals) / len(vals) if vals else 0.0

    @property
    def confidence_bucket(self) -> str:
        """AlphaFold DB convention for colouring:
        pLDDT > 90  → very high (dark blue)
        70-90 → confident (cyan)
        50-70 → low confidence (yellow)
        <50   → very low (orange)
        """
        m = self.mean_plddt
        if m > 90:
            return "very high"
        if m > 70:
            return "confident"
        if m > 50:
            return "low"
        return "very low"

    def summary(self) -> Dict[str, object]:
        s = self.protein.summary()
        s["uniprot_id"] = self.uniprot_id
        s["version"] = self.version
        s["mean_plddt"] = round(self.mean_plddt, 2)
        s["confidence_bucket"] = self.confidence_bucket
        s["source"] = "AlphaFold DB (EBI)"
        return s


def _af_cache_dir() -> Path:
    d = cache_dir() / "alphafold"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cached_af_path(uniprot_id: str, version: int = DEFAULT_VERSION) -> Path:
    return _af_cache_dir() / f"AF-{uniprot_id.upper()}-F1-v{version}.pdb"


def _compute_plddt_by_residue(protein: Protein) -> Dict[tuple, float]:
    out: Dict[tuple, float] = {}
    for chain in protein.chains:
        for res in chain.residues:
            if not res.atoms:
                continue
            # Use the CA atom's B-factor when present (AlphaFold reports
            # per-residue pLDDT, but it's written on every atom of the
            # residue identically).
            ca = next((a for a in res.atoms if a.name == "CA"),
                      res.atoms[0])
            out[(chain.id, res.seq_id)] = ca.b_factor
    return out


def fetch_alphafold_text(uniprot_id: str,
                         version: int = DEFAULT_VERSION,
                         timeout: float = 30.0,
                         use_cache: bool = True) -> str:
    """Return raw PDB text for an AlphaFold model; cached on first hit."""
    uid = uniprot_id.strip().upper()
    if not uid:
        raise ValueError("uniprot_id must be a non-empty UniProt accession")
    cached = cached_af_path(uid, version)
    if use_cache and cached.exists() and cached.stat().st_size > 0:
        return cached.read_text()
    url = AFDB_URL.format(uniprot=uid, version=version)
    log.info("Fetching AlphaFold %s (v%d) from EBI", uid, version)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "OrgChemStudio/0.1 (educational)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise FileNotFoundError(
                f"No AlphaFold entry for {uid!r} (v{version})"
            ) from e
        raise
    cached.write_text(data)
    log.info("Cached AlphaFold %s → %s (%d bytes)", uid, cached, len(data))
    return data


def fetch_alphafold(uniprot_id: str,
                    version: int = DEFAULT_VERSION,
                    timeout: float = 30.0,
                    use_cache: bool = True) -> AlphaFoldResult:
    """Fetch + parse an AlphaFold model into an :class:`AlphaFoldResult`."""
    text = fetch_alphafold_text(uniprot_id, version=version,
                                timeout=timeout, use_cache=use_cache)
    protein = parse_pdb_text(text, pdb_id=f"AF-{uniprot_id.upper()}")
    plddt = _compute_plddt_by_residue(protein)
    return AlphaFoldResult(
        uniprot_id=uniprot_id.upper(),
        version=version,
        protein=protein,
        plddt_by_residue=plddt,
    )


def parse_from_cache_or_string(uniprot_id_or_text: str,
                               treat_as_text: bool = False,
                               version: int = DEFAULT_VERSION
                               ) -> Optional[AlphaFoldResult]:
    """Test-friendly path: no network, accept raw text directly."""
    if treat_as_text:
        protein = parse_pdb_text(uniprot_id_or_text, pdb_id="AF-TEST")
        return AlphaFoldResult(
            uniprot_id="TEST", version=version,
            protein=protein,
            plddt_by_residue=_compute_plddt_by_residue(protein),
        )
    path = cached_af_path(uniprot_id_or_text, version)
    if not path.exists():
        return None
    protein = parse_pdb_text(
        path.read_text(), pdb_id=f"AF-{uniprot_id_or_text.upper()}")
    return AlphaFoldResult(
        uniprot_id=uniprot_id_or_text.upper(), version=version,
        protein=protein,
        plddt_by_residue=_compute_plddt_by_residue(protein),
    )
