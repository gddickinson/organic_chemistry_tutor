"""Fetch PDB structures from RCSB (https://www.rcsb.org) — Phase 24a.

Uses ``urllib`` (already available) with a local-cache-first policy:

1. Check ``~/Library/Caches/OrgChem/pdb/<id>.pdb``.
2. If missing, fetch from ``https://files.rcsb.org/download/<id>.pdb``.
3. Cache response; return the parsed :class:`orgchem.core.protein.Protein`.

No network calls are issued during unit tests — there's a separate
:func:`parse_from_cache_or_string` entry point that accepts a raw
text string so tests don't hit the internet.
"""
from __future__ import annotations
import logging
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Union

from orgchem.core.protein import Protein, parse_pdb_text
from orgchem.utils.paths import cache_dir

log = logging.getLogger(__name__)

#: RCSB PDB download endpoint
RCSB_URL = "https://files.rcsb.org/download/{pdb_id}.pdb"


def _pdb_cache_dir() -> Path:
    d = cache_dir() / "pdb"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cached_pdb_path(pdb_id: str) -> Path:
    """Local cache path for a PDB id (no fetch)."""
    return _pdb_cache_dir() / f"{pdb_id.upper()}.pdb"


def fetch_pdb_text(pdb_id: str, timeout: float = 30.0,
                   use_cache: bool = True) -> str:
    """Return raw PDB text for ``pdb_id``. Cached on first hit.

    Raises ``FileNotFoundError`` if RCSB has no entry for the code;
    raises ``urllib.error.URLError`` on network trouble.
    """
    pid = pdb_id.strip().upper()
    if not pid or len(pid) != 4:
        raise ValueError(f"PDB id must be a 4-character code, got {pdb_id!r}")

    cached = cached_pdb_path(pid)
    if use_cache and cached.exists() and cached.stat().st_size > 0:
        return cached.read_text()

    url = RCSB_URL.format(pdb_id=pid)
    log.info("Fetching %s from RCSB", pid)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "OrgChemStudio/0.1 (educational)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise FileNotFoundError(
                f"PDB entry {pid!r} not found on RCSB"
            ) from e
        raise

    # Cache on success.
    cached.write_text(data)
    log.info("Cached PDB %s to %s (%d bytes)", pid, cached, len(data))
    return data


def fetch_pdb(pdb_id: str, timeout: float = 30.0,
              use_cache: bool = True) -> Protein:
    """Fetch + parse a PDB entry.

    Returns a :class:`~orgchem.core.protein.Protein`. Uses local cache
    first; falls back to RCSB over HTTPS.
    """
    text = fetch_pdb_text(pdb_id, timeout=timeout, use_cache=use_cache)
    return parse_pdb_text(text, pdb_id=pdb_id.upper())


def parse_from_cache_or_string(pdb_id_or_text: str,
                               treat_as_text: bool = False
                               ) -> Optional[Protein]:
    """Helper for tests: pass either a PDB id (cache lookup only, no
    network) or raw PDB text (if ``treat_as_text=True``)."""
    if treat_as_text:
        return parse_pdb_text(pdb_id_or_text)
    cached = cached_pdb_path(pdb_id_or_text)
    if not cached.exists():
        return None
    return parse_pdb_text(cached.read_text(),
                          pdb_id=pdb_id_or_text.upper())


def clear_cache(pdb_id: Union[str, None] = None) -> int:
    """Clear the PDB cache. Returns the number of files removed.

    Pass ``pdb_id=None`` to clear everything; pass a specific id to clear
    just that entry.
    """
    removed = 0
    if pdb_id is None:
        for p in _pdb_cache_dir().iterdir():
            if p.suffix == ".pdb":
                p.unlink()
                removed += 1
    else:
        p = cached_pdb_path(pdb_id)
        if p.exists():
            p.unlink()
            removed = 1
    return removed
