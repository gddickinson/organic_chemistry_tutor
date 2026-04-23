"""Common read/write helpers for the molecule / reaction tables."""
from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select, or_

from orgchem.db.session import session_scope
from orgchem.db.models import Molecule as DBMol, Reaction as DBRxn


def list_molecules(limit: int = 500, query: Optional[str] = None) -> List[DBMol]:
    with session_scope() as s:
        stmt = select(DBMol)
        if query:
            q = f"%{query}%"
            # Round 58 — search also hits the synonyms column so e.g.
            # "retinol" resolves the row stored under its IUPAC name.
            # SQLite's ilike on TEXT works even when the value is a
            # JSON-encoded list: ``"Retinol"`` appears as a substring
            # of ``'["Retinol", "Vitamin A"]'``.
            stmt = stmt.where(or_(
                DBMol.name.ilike(q),
                DBMol.smiles.ilike(q),
                DBMol.formula.ilike(q),
                DBMol.synonyms_json.ilike(q),
            ))
        stmt = stmt.order_by(DBMol.name).limit(limit)
        rows = list(s.scalars(stmt))
    return rows


def get_molecule(mol_id: int) -> Optional[DBMol]:
    with session_scope() as s:
        return s.get(DBMol, mol_id)


def find_molecule_by_name(name: str) -> Optional[DBMol]:
    """Return the first ``Molecule`` whose ``name`` or any entry in
    its ``synonyms_json`` list matches ``name`` (case-insensitive,
    whitespace + trailing-parenthetical tolerant)."""
    from orgchem.core.identity import normalise_name
    needle_raw = (name or "").strip()
    if not needle_raw:
        return None
    needle = normalise_name(needle_raw)
    import json
    with session_scope() as s:
        # Fast path: exact-ish name match.
        stmt = select(DBMol).where(DBMol.name.ilike(needle_raw)).limit(1)
        row = s.scalars(stmt).first()
        if row is not None:
            return row
        # Synonym path: JSON substring match, then Python-side filter.
        q = f'%"{needle_raw}"%'
        stmt = (select(DBMol)
                .where(DBMol.synonyms_json.ilike(q))
                .limit(20))
        for cand in s.scalars(stmt):
            if not cand.synonyms_json:
                continue
            try:
                alts = json.loads(cand.synonyms_json) or []
            except Exception:  # noqa: BLE001
                alts = []
            for alt in alts:
                if normalise_name(str(alt)) == needle:
                    return cand
        # Last resort: normalised-name match over the whole table
        # (small; only ~400 rows).
        for cand in s.scalars(select(DBMol).limit(2000)):
            if normalise_name(cand.name) == needle:
                return cand
    return None


def find_molecule_by_smiles(smiles: str) -> Optional[DBMol]:
    """Return the first ``Molecule`` whose canonical identity matches
    ``smiles``. Uses InChIKey for order-invariant comparison — two
    SMILES strings that encode the same compound (one Kekulé, one
    aromatic; different atom order) resolve to the same row."""
    from orgchem.core.identity import inchikey, canonical_smiles
    key = inchikey(smiles)
    if key is None:
        return None
    with session_scope() as s:
        # Fast path: indexed InChIKey match.
        row = s.scalars(
            select(DBMol).where(DBMol.inchikey == key).limit(1)
        ).first()
        if row is not None:
            return row
        # Fallback: some rows lack an InChIKey — derive on the fly.
        for cand in s.scalars(select(DBMol).limit(2000)):
            if cand.inchikey == key:
                return cand
            cand_key = inchikey(cand.smiles)
            if cand_key == key:
                return cand
    return None


def add_molecule(m: DBMol) -> int:
    with session_scope() as s:
        s.add(m)
        s.flush()
        return m.id


def count_molecules() -> int:
    with session_scope() as s:
        return s.query(DBMol).count()


# ---------------------------------------------------------------------
# Phase 28d — multi-category tag-aware filter.

def query_by_tags(axis_a: Optional[str] = None,
                  value_a: Optional[str] = None,
                  axis_b: Optional[str] = None,
                  value_b: Optional[str] = None,
                  text_query: Optional[str] = None,
                  limit: int = 500) -> List[DBMol]:
    """AND-filter molecules by up to two tag axes + an optional
    free-text substring (matching name / smiles / formula).

    Axis values (from :mod:`orgchem.core.molecule_tags.FILTER_AXES`):

    - ``functional_group`` — JSON-array membership check on
      ``functional_group_tags_json``.
    - ``composition`` — membership check on ``source_tags_json``
      (currently unused auto-tag) **or** a secondary test on the
      computed flag list. We fall back to a substring match inside
      ``functional_group_tags_json`` so the filter keeps working
      even when the composition list lives alongside.
    - ``charge`` — one of ``neutral`` / ``cation`` / ``anion`` /
      ``zwitterion``. Resolved against ``formal_charge`` and
      a JSON-string substring (``"zwitterion"`` is stored as a
      functional-group-ish tag by the auto-tagger, when detected).
    - ``size`` — ``small`` / ``medium`` / ``large`` band check
      against ``heavy_atom_count``.
    - ``ring_count`` — ``acyclic`` / ``one_to_two`` /
      ``three_plus`` band check against ``n_rings``.
    - ``has_stereo`` — ``yes`` / ``no`` check against the
      ``has_stereo`` column.
    """
    with session_scope() as s:
        stmt = select(DBMol)
        for axis, value in ((axis_a, value_a), (axis_b, value_b)):
            if not axis or not value:
                continue
            stmt = _apply_axis_filter(stmt, axis, value)
        if text_query:
            q = f"%{text_query}%"
            stmt = stmt.where(or_(
                DBMol.name.ilike(q),
                DBMol.smiles.ilike(q),
                DBMol.formula.ilike(q),
            ))
        stmt = stmt.order_by(DBMol.name).limit(limit)
        return list(s.scalars(stmt))


def _apply_axis_filter(stmt, axis: str, value: str):
    axis = axis.strip().lower()
    value = value.strip()
    if not value:
        return stmt
    if axis == "functional_group":
        return stmt.where(
            DBMol.functional_group_tags_json.ilike(f'%"{value}"%'))
    if axis in ("composition", "source"):
        # Composition flags land in the auto-tag array; curated
        # source / drug-class tags land in source_tags_json. Both
        # axes accept either — a broad substring match on each.
        return stmt.where(
            DBMol.functional_group_tags_json.ilike(f'%"{value}"%')
            | DBMol.source_tags_json.ilike(f'%"{value}"%'))
    if axis == "charge":
        if value == "neutral":
            return stmt.where(DBMol.formal_charge == 0)
        if value == "cation":
            return stmt.where(DBMol.formal_charge > 0)
        if value == "anion":
            return stmt.where(DBMol.formal_charge < 0)
        if value == "zwitterion":
            # Zwitterion detection was tagged by the auto-tagger into
            # the functional-group column as the string "zwitterion".
            return stmt.where(
                DBMol.functional_group_tags_json.ilike(
                    f'%"zwitterion"%'))
    if axis == "size":
        if value == "small":
            return stmt.where(DBMol.heavy_atom_count <= 12)
        if value == "medium":
            return stmt.where(
                DBMol.heavy_atom_count >= 13,
                DBMol.heavy_atom_count <= 30)
        if value == "large":
            return stmt.where(DBMol.heavy_atom_count >= 31)
    if axis == "ring_count":
        if value == "acyclic":
            return stmt.where(DBMol.n_rings == 0)
        if value == "one_to_two":
            return stmt.where(DBMol.n_rings.in_((1, 2)))
        if value == "three_plus":
            return stmt.where(DBMol.n_rings >= 3)
    if axis == "has_stereo":
        return stmt.where(DBMol.has_stereo == (value == "yes"))
    return stmt


def list_molecule_category_values() -> dict:
    """Thin wrapper re-exporting the Phase 28c taxonomy for the GUI /
    agent layer so callers don't have to import from core."""
    from orgchem.core.molecule_tags import list_filter_axes
    return list_filter_axes()


def list_reactions(limit: int = 200, query: Optional[str] = None) -> List[DBRxn]:
    with session_scope() as s:
        stmt = select(DBRxn)
        if query:
            q = f"%{query}%"
            stmt = stmt.where(or_(DBRxn.name.ilike(q), DBRxn.category.ilike(q)))
        stmt = stmt.order_by(DBRxn.name).limit(limit)
        return list(s.scalars(stmt))
