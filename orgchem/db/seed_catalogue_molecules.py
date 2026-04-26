"""Phase 49b (round 177) — backfill the Molecule DB with
catalogue entries that aren't already represented.

The Phase-29 Lipid / Carbohydrate / Nucleic-acid catalogues
and the Phase-31k SAR series each carry many entries with
parseable SMILES.  Round 58's `seed_synonyms` already adds
**catalogue names as aliases** to molecule rows that match by
InChIKey — but it does NOT create new rows for catalogue
molecules that aren't already in the DB.

Round 177 closes that gap: every catalogue molecule with a
parseable SMILES becomes a first-class Molecule row, tagged
with a ``source`` indicating which catalogue it came from
(``carbohydrate-catalogue`` / ``lipid-catalogue`` /
``nucleic-acid-catalogue`` / ``sar-<series-id>``).  This
makes catalogue molecules discoverable via the molecule
browser, addressable by `find_molecule_by_name`, and
available as substrates for downstream features
(retrosynthesis, descriptors, conformers).

Idempotent: re-running adds nothing new because the
InChIKey-uniqueness check skips any molecule already in the
DB.
"""
from __future__ import annotations
import json
import logging
from typing import Dict, List, Tuple

from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope
from orgchem.core.molecule import Molecule as ChemMol

log = logging.getLogger(__name__)


def _gather_catalogue_entries() -> List[Tuple[str, str, str]]:
    """Return ``[(source_tag, name, smiles), ...]`` for every
    catalogue entry with a non-empty SMILES.  Catalogue
    imports are guarded so a stripped-down environment
    doesn't crash the seeder."""
    out: List[Tuple[str, str, str]] = []

    try:
        from orgchem.core.carbohydrates import CARBOHYDRATES
        for c in CARBOHYDRATES:
            if c.smiles:
                out.append(("carbohydrate-catalogue", c.name,
                            c.smiles))
    except Exception:
        log.warning("could not import carbohydrate catalogue")

    try:
        from orgchem.core.lipids import LIPIDS
        for l in LIPIDS:
            if l.smiles:
                out.append(("lipid-catalogue", l.name,
                            l.smiles))
    except Exception:
        log.warning("could not import lipid catalogue")

    try:
        from orgchem.core.nucleic_acids import NUCLEIC_ACIDS
        for na in NUCLEIC_ACIDS:
            if na.smiles:
                out.append(("nucleic-acid-catalogue", na.name,
                            na.smiles))
    except Exception:
        log.warning("could not import nucleic-acid catalogue")

    try:
        from orgchem.core.sar import SAR_LIBRARY
        for s in SAR_LIBRARY:
            for v in s.variants:
                if v.smiles:
                    out.append((f"sar-{s.id}", v.name,
                                v.smiles))
    except Exception:
        log.warning("could not import SAR library")

    return out


def seed_catalogue_molecules_if_needed() -> int:
    """Insert any catalogue molecule whose InChIKey isn't
    already in the Molecule DB.  Returns the number of new
    rows added.  Idempotent."""
    entries = _gather_catalogue_entries()
    if not entries:
        return 0

    # Build lookup of existing molecule InChIKeys + names so
    # we can skip duplicates.
    with session_scope() as s:
        existing_keys = set()
        existing_names = set()
        for row in s.query(DBMol.inchikey, DBMol.name).all():
            if row.inchikey:
                existing_keys.add(row.inchikey)
            existing_names.add(row.name.lower())

    # Compute each catalogue entry's InChIKey via the same
    # `Molecule.from_smiles` path the seeder uses, so we avoid
    # adding duplicates that differ in canonicalisation.
    to_add: List[Tuple[str, str, ChemMol]] = []
    seen_keys_this_run: set = set()
    seen_names_this_run: set = set()
    for source, name, smiles in entries:
        try:
            m = ChemMol.from_smiles(smiles, name=name,
                                    generate_3d=False)
            m.ensure_properties()
        except Exception as e:
            log.warning("Skipping catalogue entry %r: %s",
                        name, e)
            continue
        if not m.inchikey:
            continue
        # Skip if already in DB or already queued in this run.
        if m.inchikey in existing_keys:
            continue
        if m.inchikey in seen_keys_this_run:
            continue
        # Skip if a different InChIKey but same name (defensive
        # — shouldn't happen given the canonical-name pre-check
        # in seed_synonyms, but cheap to guard).
        nl = name.lower()
        if nl in existing_names or nl in seen_names_this_run:
            continue
        to_add.append((source, name, m))
        seen_keys_this_run.add(m.inchikey)
        seen_names_this_run.add(nl)

    if not to_add:
        log.info(
            "All %d catalogue molecules already in the DB.",
            len(entries))
        return 0

    log.info(
        "Backfilling %d catalogue molecules into the DB.",
        len(to_add))
    added = 0
    with session_scope() as s:
        for source, name, m in to_add:
            s.add(DBMol(
                name=m.name, smiles=m.smiles,
                inchi=m.inchi, inchikey=m.inchikey,
                formula=m.formula,
                properties_json=json.dumps(m.properties),
                source=source,
            ))
            added += 1
    log.info(
        "Seeded %d catalogue molecules (round 177).", added)
    return added
