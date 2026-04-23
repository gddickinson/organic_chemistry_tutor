"""Molecular identity — canonical SMILES, InChI, InChIKey, and
the utilities that let every catalogue in the app agree on
*which compound* a row represents.

User-reported bug (2026-04-23): adding Retinol via PubChem stored
it as ``"(2E,4E,6E,8E)-3,7-dimethyl-9-(2,6,6-trimethyl..."`` in
the Molecule DB while the Lipids catalogue already had it as
``"Retinol (vitamin A)"``. The SMILES strings looked different but
canonicalise to the same string and share an InChIKey — so it's
one molecule, stored twice under two names, with no
cross-reference. Searching "retinol" in the Molecule workspace
missed the long-IUPAC entry entirely.

This module gives every caller a single source of truth for
identity comparison:

- :func:`canonical_smiles` — RDKit canonical SMILES (order-
  invariant, stereochemistry-aware).
- :func:`inchikey` — RDKit InChIKey. Gold-standard identity
  fingerprint; two molecules are *the same* iff their InChIKeys
  match.
- :func:`same_molecule` — safe wrapper; either SMILES may be
  unparseable and we return False rather than raising.
- :func:`normalise_name` — casefold + strip common suffixes like
  ``" (vitamin A)"`` so name-level lookups are more forgiving.
"""
from __future__ import annotations
import re
from typing import Optional

from rdkit import Chem


# Parenthetical suffix at the end of a name — "(vitamin A)",
# "(α-form)", etc. Stripped from display names for matching.
_PARENS_TAIL_RX = re.compile(r"\s*\([^()]*\)\s*$")


def canonical_smiles(smiles: str) -> Optional[str]:
    """Return the RDKit canonical SMILES for ``smiles`` (order-
    invariant, stereo-preserving) or ``None`` if it can't parse."""
    if not smiles:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        return Chem.MolToSmiles(mol, canonical=True)
    except Exception:  # noqa: BLE001
        return None


def inchikey(smiles: str) -> Optional[str]:
    """Return the InChIKey (27-char hash) for ``smiles`` or
    ``None`` on failure. Two molecules are the same compound iff
    their InChIKeys match — this is the canonical identity test."""
    if not smiles:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        key = Chem.MolToInchiKey(mol)
        return key or None
    except Exception:  # noqa: BLE001
        return None


def same_molecule(a: Optional[str], b: Optional[str]) -> bool:
    """True iff both SMILES parse and produce the same InChIKey."""
    if not a or not b:
        return False
    ka, kb = inchikey(a), inchikey(b)
    return bool(ka and kb and ka == kb)


def normalise_name(name: str) -> str:
    """Return a lowercase, whitespace-normalised form of ``name``
    with any trailing parenthetical suffix stripped.

    "Retinol (vitamin A)"  →  "retinol"
    "α-D-Glucopyranose"    →  "α-d-glucopyranose"
    "  N-acetyl  "         →  "n-acetyl"
    """
    if not name:
        return ""
    s = _PARENS_TAIL_RX.sub("", name).strip()
    return s.lower()
