"""Phase 6f.1/6f.2 — resolve a SMILES fragment to its canonical DB copy.

Any panel / renderer that draws a molecule can call :func:`resolve` here
to get back a triple ``(canonical_smiles, rdkit_mol_with_db_coords,
db_row_or_none)``. When the fragment is in the molecule DB, its cached
``molblock_2d`` is used to hydrate the Mol so the 2D layout is the *same
one students saw in the Molecule Workspace*. When the fragment is new,
it's canonicalised + 2D-coords-computed in the same way the DB backfill
does, so subsequent seedings line up trivially.

The lookup key is the InChIKey — it's robust to tautomer variations in
writing but not robust to stereochemistry loss (which is what we want
for cross-referencing the DB). If a fragment has no assigned stereo and
the DB row does, or vice versa, the InChIKey still matches on the
*constitution*; the renderer then uses whichever stereo came in. That's
the right compromise for teaching consistency.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Optional, Tuple

from rdkit import Chem
from rdkit.Chem import rdDepictor

log = logging.getLogger(__name__)


# Use the "new" CoordGen layout globally for pretty aromatic rings.
try:
    rdDepictor.SetPreferCoordGen(True)
except Exception:  # some older RDKits don't expose it
    pass


@dataclass
class ResolvedFragment:
    smiles: str                  # canonical SMILES (DB's if a match, else roundtripped)
    mol: Chem.Mol                # RDKit Mol, with 2D coords set (from DB if available)
    db_id: Optional[int] = None  # Molecule.id if found
    db_name: Optional[str] = None
    from_db: bool = False        # True when coords came from the DB cache


def canonical_smiles(smiles: str) -> str:
    """SMILES → canonical SMILES. Empty if unparseable."""
    if not smiles:
        return ""
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return ""
    return Chem.MolToSmiles(m)


def _inchikey_of(mol: Chem.Mol) -> Optional[str]:
    try:
        inchi = Chem.MolToInchi(mol)
        if not inchi:
            return None
        return Chem.InchiToInchiKey(inchi)
    except Exception:
        return None


def resolve(smiles: str) -> Optional[ResolvedFragment]:
    """Resolve a SMILES fragment: look up in the molecule DB by InChIKey,
    hydrate a Mol with the DB's cached 2D coords if found, else compute
    fresh coords.

    Returns ``None`` only if ``smiles`` is unparseable.
    """
    if not smiles:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        log.warning("resolve: unparseable SMILES %r", smiles)
        return None

    canon = Chem.MolToSmiles(mol)
    inchi_key = _inchikey_of(mol)

    # Cheap short-circuit if the DB is not initialised yet (e.g. in a
    # unit test that only imports core/).
    from orgchem.db import session as _session_mod
    if _session_mod._SessionLocal is None:  # type: ignore[attr-defined]
        return _compute_fresh(canon, mol, inchi_key)

    from orgchem.db.session import session_scope
    from orgchem.db.models import Molecule as DBMol
    from sqlalchemy import select

    if inchi_key:
        with session_scope() as s:
            row = s.scalars(
                select(DBMol).where(DBMol.inchikey == inchi_key)
            ).first()
            if row is not None:
                db_canon = row.smiles
                molblock = row.molblock_2d
                db_id = row.id
                db_name = row.name
        if row is not None:
            rebuilt = Chem.MolFromSmiles(db_canon)
            if molblock:
                try:
                    mb_mol = Chem.MolFromMolBlock(molblock, sanitize=True)
                except Exception:
                    mb_mol = None
                if mb_mol is not None and mb_mol.GetNumAtoms() == rebuilt.GetNumAtoms():
                    rebuilt = mb_mol
            else:
                # DB row exists but has no cached coords — compute once.
                rdDepictor.Compute2DCoords(rebuilt)
            return ResolvedFragment(
                smiles=db_canon, mol=rebuilt,
                db_id=db_id, db_name=db_name, from_db=True,
            )

    return _compute_fresh(canon, mol, inchi_key)


def _compute_fresh(canon: str, mol: Chem.Mol,
                   inchi_key: Optional[str]) -> ResolvedFragment:
    fresh = Chem.MolFromSmiles(canon) if canon else mol
    try:
        rdDepictor.Compute2DCoords(fresh)
    except Exception as e:  # noqa: BLE001
        log.debug("Compute2DCoords failed for %r: %s", canon, e)
    return ResolvedFragment(
        smiles=canon or Chem.MolToSmiles(mol),
        mol=fresh,
        db_id=None, db_name=None, from_db=False,
    )


def split_reaction_fragments(reaction_smiles: str) -> Tuple[list, list]:
    """Split ``A.B>>C.D`` (or ``A.B>reagents>C.D``) into reactant / product lists."""
    s = reaction_smiles.strip()
    if ">" not in s:
        return [], []
    parts = s.split(">")
    if len(parts) == 3:
        lhs = [f for f in (parts[0] + "." + parts[1]).split(".") if f]
        rhs = [f for f in parts[2].split(".") if f]
        return lhs, rhs
    if len(parts) == 2:
        lhs = [f for f in parts[0].split(".") if f]
        rhs = [f for f in parts[1].split(".") if f]
        return lhs, rhs
    return [], []


def canonical_reaction_smiles(reaction_smiles: str) -> str:
    """Return the reaction SMILES with every fragment replaced by its DB-canonical form.

    Falls back to the fresh canonical form when a fragment is not in the
    DB. This gives deterministic, consistent SMILES for rendering —
    a given molecule always appears the same way in a reaction string.
    """
    lhs, rhs = split_reaction_fragments(reaction_smiles)
    if not lhs and not rhs:
        return reaction_smiles
    lhs_canon = []
    for f in lhs:
        r = resolve(f)
        lhs_canon.append(r.smiles if r is not None else f)
    rhs_canon = []
    for f in rhs:
        r = resolve(f)
        rhs_canon.append(r.smiles if r is not None else f)
    return ".".join(lhs_canon) + ">>" + ".".join(rhs_canon)


def audit_reaction(reaction_smiles: str) -> dict:
    """Return a dict describing which fragments of a reaction are in the DB.

    Used by Phase 6f.4 consistency tests.
    """
    lhs, rhs = split_reaction_fragments(reaction_smiles)
    found = []
    missing = []
    for f in lhs + rhs:
        r = resolve(f)
        if r is None:
            missing.append({"fragment": f, "reason": "unparseable"})
        elif r.from_db:
            found.append({"fragment": f, "db_id": r.db_id,
                          "db_name": r.db_name, "canonical": r.smiles})
        else:
            missing.append({"fragment": f, "canonical": r.smiles,
                            "reason": "not in DB"})
    return {"n_fragments": len(lhs) + len(rhs),
            "n_in_db": len(found),
            "n_missing": len(missing),
            "found": found, "missing": missing}
