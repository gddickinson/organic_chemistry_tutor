"""Phase 49b (round 177) — molecule-DB canonicalisation
audit.

Locks in that **every catalogue molecule with a parseable
SMILES is also a Molecule row in the DB** (matched by
InChIKey).  The Phase-29 lipid / carbohydrate / nucleic-acid
catalogues + the Phase-31k SAR series variants + the
Phase-43 cell-component cross-references + the Phase-47
biochemistry-by-kingdom topic cross-references should all
resolve to a real DB row that the user can inspect via the
molecule browser, address via `find_molecule_by_name`, and
use as a substrate for descriptors / retrosynthesis /
conformer generation.

Generalises the per-catalogue cross-reference tests added
in round 151 (Phase-43) + round 166 (Phase-47) into a
project-wide audit.
"""
from __future__ import annotations
import os

import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


# ==================================================================
# gather_catalogue_molecule_references — public API
# ==================================================================

def test_gather_returns_at_least_100_references():
    """Round-177 audit collects ≥ 100 catalogue molecule
    references across all walked sources."""
    from orgchem.core.glossary_audit import (
        gather_catalogue_molecule_references,
    )
    refs = gather_catalogue_molecule_references()
    assert len(refs) >= 100


def test_gather_covers_all_four_smiles_sources():
    """The walker must cover all 4 SMILES-bearing sources:
    carbohydrate / lipid / nucleic-acid / sar-*."""
    from orgchem.core.glossary_audit import (
        gather_catalogue_molecule_references,
    )
    refs = gather_catalogue_molecule_references()
    sources = {r[0] for r in refs}
    assert "carbohydrate" in sources
    assert "lipid" in sources
    assert "nucleic-acid" in sources
    assert any(s.startswith("sar-") for s in sources)


# ==================================================================
# Resolution audit — every SMILES-carrying ref hits a DB row
# ==================================================================

def test_every_smiles_ref_resolves_by_inchikey(app):
    """Every catalogue molecule with a parseable SMILES
    must match a Molecule DB row — either by full InChIKey
    or, if the catalogue carries a stereo variant of an
    already-named compound, by name + matching skeleton
    (InChIKey block 1).  The round-177
    `seed_catalogue_molecules.py` backfill closes any
    historical gaps; this test guards against new ones."""
    from rdkit import Chem
    from orgchem.core.glossary_audit import (
        gather_catalogue_molecule_references,
    )
    from orgchem.db.queries import list_molecules

    # Build lookup tables for the entire seeded molecule DB.
    ikeys_in_db = set()
    name_to_skeleton = {}   # lowercased name → InChIKey block 1
    for m in list_molecules():
        if m.inchikey:
            ikeys_in_db.add(m.inchikey)
            if m.name:
                name_to_skeleton[m.name.lower()] = m.inchikey.split("-")[0]

    refs = gather_catalogue_molecule_references()
    failed = []
    for source, name, smiles in refs:
        if not smiles:
            continue   # name-only refs handled by Phase-43 + 47
                       # tests already
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                failed.append((source, name, "unparseable"))
                continue
            ikey = Chem.MolToInchiKey(mol)
            if ikey in ikeys_in_db:
                continue
            # Stereo-variant fallback: same name + matching
            # skeleton block.  The seeder deliberately skips
            # adding a second row for an existing name even
            # when the catalogue's stereo specification differs
            # — those still "resolve" for the user's purposes
            # because the name lookup hits the seed-set row.
            skel = ikey.split("-")[0]
            if name_to_skeleton.get(name.lower()) == skel:
                continue
            failed.append((source, name, ikey))
        except Exception as e:
            failed.append((source, name, str(e)[:50]))
    assert not failed, (
        f"{len(failed)} catalogue molecules don't resolve to "
        f"a Molecule DB row by InChIKey.  First 10:\n"
        + "\n".join(f"  [{s}] {n} → {k}"
                    for s, n, k in failed[:10])
    )


def test_every_name_ref_resolves(app):
    """Every name-only cross-reference (Phase-43
    `cross_reference_molecule_name` + Phase-47
    `cross_reference_molecule_names`) must match a real
    Molecule row by name lookup."""
    from orgchem.core.glossary_audit import (
        gather_catalogue_molecule_references,
    )
    from orgchem.db.queries import find_molecule_by_name

    refs = gather_catalogue_molecule_references()
    failed = []
    for source, name, smiles in refs:
        if smiles:
            continue   # SMILES refs handled above
        if find_molecule_by_name(name) is None:
            failed.append((source, name))
    assert not failed, (
        f"{len(failed)} name-only cross-references don't "
        f"resolve to a Molecule row.  First 10:\n"
        + "\n".join(f"  [{s}] {n}" for s, n in failed[:10])
    )


# ==================================================================
# Backfill mechanism + idempotency
# ==================================================================

def test_seed_catalogue_molecules_idempotent(app):
    """Running `seed_catalogue_molecules_if_needed` twice
    in a row must not add duplicate rows."""
    from orgchem.db.seed_catalogue_molecules import (
        seed_catalogue_molecules_if_needed,
    )
    # First run — may add 0 (already done by seed_if_empty).
    first = seed_catalogue_molecules_if_needed()
    second = seed_catalogue_molecules_if_needed()
    assert second == 0, \
        f"second run added {second} rows — expected 0 " \
        f"(idempotency violation)"
    # First-run delta should be ≥ 0 (0 if pre-seeded by
    # init_db, > 0 in a fresh-DB test environment).
    assert first >= 0


def test_at_least_some_catalogue_molecules_added(app):
    """After round-177 the molecule DB should contain at
    least 50 of the catalogue-sourced molecules — a
    floor that proves the backfill actually ran."""
    from orgchem.db.queries import list_molecules
    catalogue_sources = (
        "carbohydrate-catalogue", "lipid-catalogue",
        "nucleic-acid-catalogue",
    )
    n = sum(
        1 for m in list_molecules()
        if m.source and any(m.source.startswith(s)
                            for s in catalogue_sources)
        or (m.source and m.source.startswith("sar-"))
    )
    assert n >= 50, \
        f"only {n} catalogue-sourced molecules in DB; " \
        f"expected ≥ 50 after the round-177 backfill"
