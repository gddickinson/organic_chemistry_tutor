"""Round 58 — seed common synonyms onto the Molecule DB.

Two kinds of enrichment happen here:

1. **Hand-curated list** of common / trivial names for the seeded
   molecules (``"Ethanol" → ["Ethyl alcohol", "EtOH"]``). Run on
   DB init so every user sees the benefit on next launch.

2. **Cross-catalogue reconciliation** — for every entry in the
   Lipids / Carbohydrates / Nucleic-acids Python catalogues,
   find the DB row with the same InChIKey and add the catalogue's
   canonical name as a synonym on that row. Fixes the reported
   bug (Retinol in Lipids vs the IUPAC name in Molecule DB).

Both steps are idempotent: re-running the seeder adds nothing.
"""
from __future__ import annotations
import json
import logging
from typing import Dict, List, Optional

from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


# Canonical name → list of synonyms. Curated, not exhaustive.
_CURATED: Dict[str, List[str]] = {
    "Water": ["H2O", "Dihydrogen monoxide"],
    "Ethanol": ["Ethyl alcohol", "EtOH", "Grain alcohol"],
    "Methanol": ["Methyl alcohol", "MeOH", "Wood alcohol"],
    "Acetic acid": ["Ethanoic acid", "AcOH", "Vinegar acid"],
    "Acetone": ["Propan-2-one", "Propanone", "Dimethyl ketone"],
    "Benzene": ["Benzol"],
    "Toluene": ["Methylbenzene", "Phenylmethane"],
    "Phenol": ["Carbolic acid", "Hydroxybenzene"],
    "Aniline": ["Aminobenzene", "Phenylamine"],
    "Formaldehyde": ["Methanal"],
    "Acetaldehyde": ["Ethanal"],
    "Aspirin": ["Acetylsalicylic acid", "ASA", "2-Acetoxybenzoic acid"],
    "Ibuprofen": ["2-(4-isobutylphenyl)propanoic acid"],
    "Caffeine": ["1,3,7-Trimethylxanthine", "Theine"],
    "Nicotine": ["(S)-3-(1-Methylpyrrolidin-2-yl)pyridine"],
    "Paracetamol": ["Acetaminophen", "N-(4-Hydroxyphenyl)acetamide",
                    "APAP"],
    "Acetaminophen": ["Paracetamol", "APAP",
                      "N-(4-Hydroxyphenyl)acetamide"],
    "Cholesterol": ["Cholest-5-en-3β-ol"],
    "D-Glucose (β-pyranose)": ["β-D-Glucose", "beta-D-Glucose",
                               "β-D-Glucopyranose"],
    "D-Glucose (α-pyranose)": ["α-D-Glucose", "alpha-D-Glucose",
                               "α-D-Glucopyranose"],
    "Glycerol": ["Glycerine", "Propane-1,2,3-triol", "1,2,3-Propanetriol"],
    "Urea": ["Carbamide", "Carbonyldiamide"],
    "Vitamin C": ["L-Ascorbic acid", "Ascorbic acid"],
    "Ascorbic acid": ["Vitamin C", "L-Ascorbic acid"],
    "Bisphenol-A": ["BPA", "4,4'-(propane-2,2-diyl)diphenol"],
    "Methylene blue": ["Methylthioninium chloride"],
    "Indigo": ["Indigotin"],
    # Hormones / vitamins that the Lipids catalogue also lists.
    "Testosterone": ["17β-Hydroxyandrost-4-en-3-one"],
    "Estradiol": ["17β-Estradiol", "E2", "Oestradiol"],
    "Progesterone": ["Pregn-4-ene-3,20-dione", "P4"],
    "Cortisol": ["Hydrocortisone"],
    "Vitamin D3": ["Cholecalciferol", "Colecalciferol"],
    "Retinol (vitamin A)": ["Retinol", "Vitamin A", "all-trans-Retinol"],
}


def _add_syn(row: DBMol, new: List[str]) -> int:
    """Merge ``new`` into ``row.synonyms_json`` (case-insensitive).
    Returns the number of *added* synonyms."""
    from orgchem.core.identity import normalise_name
    try:
        existing = (json.loads(row.synonyms_json)
                    if row.synonyms_json else [])
    except Exception:  # noqa: BLE001
        existing = []
    existing_norm = {normalise_name(s) for s in existing}
    existing_norm.add(normalise_name(row.name))
    added = 0
    for s in new:
        if not s:
            continue
        if normalise_name(s) in existing_norm:
            continue
        existing.append(s)
        existing_norm.add(normalise_name(s))
        added += 1
    if added:
        row.synonyms_json = json.dumps(existing)
    return added


def _backfill_inchikey(rows) -> int:
    """Fill in the ``inchikey`` column on any row where it's NULL,
    so the InChIKey-based reconciliation below can index on it.
    Returns the number of rows updated."""
    from orgchem.core.identity import inchikey as _key
    updated = 0
    for row in rows:
        if row.inchikey:
            continue
        k = _key(row.smiles)
        if k:
            row.inchikey = k
            updated += 1
    return updated


def _reconcile_with_lipids_catalogue(s) -> int:
    """For every Lipid entry with a parseable SMILES, find the DB
    row with the same InChIKey and tag the catalogue name + any
    parenthetical short form as synonyms."""
    try:
        from orgchem.core.lipids import LIPIDS
    except ImportError:
        return 0
    from orgchem.core.identity import inchikey as _key
    added = 0
    by_key: Dict[str, DBMol] = {}
    for row in s.query(DBMol).all():
        if row.inchikey:
            by_key[row.inchikey] = row
    for l in LIPIDS:
        if not l.smiles:
            continue
        k = _key(l.smiles)
        if not k or k not in by_key:
            continue
        row = by_key[k]
        # Catalogue form + trivial alias from the parenthetical.
        syns = [l.name]
        if "(" in l.name and l.name.endswith(")"):
            short = l.name.split("(", 1)[0].strip()
            tail = l.name.split("(", 1)[1].rstrip(")").strip()
            if short:
                syns.append(short)
            if tail:
                syns.append(tail)
        added += _add_syn(row, syns)
    return added


def _reconcile_with_carbs_and_na(s) -> int:
    """Same treatment for Carbohydrates and Nucleic-acids catalogues."""
    from orgchem.core.identity import inchikey as _key
    by_key: Dict[str, DBMol] = {
        row.inchikey: row for row in s.query(DBMol).all()
        if row.inchikey
    }
    added = 0
    for mod_name in ("orgchem.core.carbohydrates",
                     "orgchem.core.nucleic_acids"):
        try:
            mod = __import__(mod_name, fromlist=["*"])
        except ImportError:
            continue
        # Both catalogues use "CARBOHYDRATES" / "NUCLEIC_ACIDS" constants.
        rows = (getattr(mod, "CARBOHYDRATES", None)
                or getattr(mod, "NUCLEIC_ACIDS", None) or [])
        for entry in rows:
            smi = getattr(entry, "smiles", "") or ""
            name = getattr(entry, "name", "") or ""
            if not smi or not name:
                continue
            k = _key(smi)
            if not k or k not in by_key:
                continue
            added += _add_syn(by_key[k], [name])
    return added


def seed_synonyms_if_needed() -> int:
    """Populate ``Molecule.synonyms_json`` with curated + cross-
    catalogue synonyms. Idempotent — re-running adds nothing new.
    Returns the total count of synonym entries added this run."""
    total = 0
    with session_scope() as s:
        rows = list(s.query(DBMol).all())
        total += _backfill_inchikey(rows)
        by_name: Dict[str, DBMol] = {}
        for row in rows:
            by_name[row.name.lower()] = row
        for canonical, synonyms in _CURATED.items():
            row = by_name.get(canonical.lower())
            if row is None:
                continue
            total += _add_syn(row, synonyms)
        total += _reconcile_with_lipids_catalogue(s)
        total += _reconcile_with_carbs_and_na(s)
    if total:
        log.info(
            "Seeded / reconciled %d molecule synonyms (round 58)",
            total,
        )
    return total
