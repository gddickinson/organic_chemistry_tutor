"""Regression: every seeded molecule's stereochemistry must be physically possible.

Before the fix the seed SMILES of Camphor, Codeine and Oxycodone carried stereo descriptors that no 3D geometry can
satisfy (e.g. camphor's two bridgeheads were written R and S, but a bicyclo[2.2.1] bridge forces 1R,4R or 1S,4S), so
RDKit could not embed them and the app had no 3D model. They now use the isomeric SMILES of their PubChem records:

* Camphor -> (+)-camphor, (1R,4R): PubChem CID 159055, ChEBI:15396 (the seed name does not say which enantiomer;
  (+)-camphor is the common natural form).
* Codeine -> PubChem CID 5284371, ChEBI:16714.
* Oxycodone -> PubChem CID 5284603, ChEBI:7852.

A scan of all seeded molecules against PubChem (same session) found 78 more rows whose structure or stereochemistry
disagreed with their name (e.g. most L-amino acids were seeded as the D enantiomer); they were corrected and
their PubChem InChIKeys are pinned in tests/fixtures/seed_pubchem_keys.json.

The InChIKeys were taken from those PubChem records (fetched 2026-11-12); the tests never call PubChem.
"""
import json
from pathlib import Path

import pytest
from rdkit import Chem, RDLogger

from orgchem.core.molecule import Molecule

RDLogger.DisableLog("rdApp.*")

EXPECTED = {  # seeded name -> InChIKey of the PubChem record
    "Camphor": "DSSYKIVIOFKYAU-XCBNKYQSSA-N",
    "Codeine": "OROGSEYTTFOCAN-DNJOTXNNSA-N",
    "Oxycodone (OxyContin)": "BRUQQQPBMZOVGD-XFKAJCMBSA-N",
}

# Seeded molecules with stereocentres that are allowed to have no 3D model, with the reason. Keep empty unless a
# structure is genuinely impossible to embed with RDKit for a reason other than wrong stereo.
EMBED_ALLOW_LIST: dict = {}


@pytest.fixture(scope="module")
def seeded():
    from orgchem.web.chemdata import snapshot  # seeds a private temp DB with the app's own seeders
    return {m["name"]: m for m in snapshot()["molecules"]}


def _stereo_preserved_3d(smiles: str):
    """Return (embedded, stereo_kept): does Molecule.generate_3d give a conformer whose specified stereo matches?"""
    mol = Chem.MolFromSmiles(smiles)
    m = Molecule.from_smiles(smiles, generate_3d=True)
    if not m.molblock_3d:
        return False, False
    m3 = Chem.RemoveHs(Chem.MolFromMolBlock(m.molblock_3d, removeHs=False))
    Chem.AssignStereochemistryFrom3D(m3)
    want = Chem.FindMolChiralCenters(mol, includeUnassigned=False, useLegacyImplementation=False)
    got = dict(Chem.FindMolChiralCenters(m3, includeUnassigned=True, useLegacyImplementation=False))
    kept = all(got.get(i) == label for i, label in want)
    for b in mol.GetBonds():
        if b.GetStereo() in (Chem.BondStereo.STEREOE, Chem.BondStereo.STEREOZ):
            kept = kept and m3.GetBondBetweenAtoms(b.GetBeginAtomIdx(), b.GetEndAtomIdx()).GetStereo() == b.GetStereo()
    return True, kept


def _has_stereo(smiles: str) -> bool:
    mol = Chem.MolFromSmiles(smiles)
    return bool(Chem.FindMolChiralCenters(mol, includeUnassigned=False, useLegacyImplementation=False)) or any(
        b.GetStereo() != Chem.BondStereo.STEREONONE for b in mol.GetBonds())


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_named_molecules_match_pubchem_and_embed(seeded, name):
    row = seeded[name]
    assert row["inchikey"] == EXPECTED[name]
    assert Chem.MolToInchiKey(Chem.MolFromSmiles(row["smiles"])) == EXPECTED[name]
    embedded, kept = _stereo_preserved_3d(row["smiles"])
    assert embedded and kept, f"{name}: no 3D model with the seeded stereochemistry"


def test_every_seeded_stereo_molecule_embeds(seeded):
    bad = []
    for name, row in seeded.items():
        if name in EMBED_ALLOW_LIST or not _has_stereo(row["smiles"]):
            continue
        embedded, kept = _stereo_preserved_3d(row["smiles"])
        if not (embedded and kept):
            bad.append((name, row["smiles"], "no conformer" if not embedded else "stereo lost"))
    assert not bad, json.dumps(bad, indent=1)


def test_corrected_molecules_match_pubchem():
    from orgchem.web.chemdata import snapshot
    rows = snapshot()["molecules"]
    data = json.loads((Path(__file__).parent / "fixtures" / "seed_pubchem_keys.json").read_text())
    bad = []
    for ref in data["molecules"]:
        keys = [r["inchikey"] for r in rows if r["name"] == ref["name"]]
        if not keys:
            bad.append((ref["name"], "not seeded"))
        elif "inchikey" in ref and ref["inchikey"] not in keys:
            bad.append((ref["name"], keys, ref["inchikey"], ref["cid"]))
        elif "inchikey_skeleton" in ref and not any(k[:14] == ref["inchikey_skeleton"] for k in keys):
            bad.append((ref["name"], keys, ref["inchikey_skeleton"], ref["cid"]))
    assert not bad, bad


def test_corrections_table_matches_seeders():
    """The in-place DB corrections must write exactly what a fresh seed produces."""
    from orgchem.db.seed_corrections import CORRECTIONS, RENAMES
    from orgchem.web.chemdata import snapshot
    rows = snapshot()["molecules"]
    for name, _old, smiles, _src in CORRECTIONS + [(r[2], r[1], r[3], r[4]) for r in RENAMES]:
        key = Chem.MolToInchiKey(Chem.MolFromSmiles(smiles))
        assert key in [r["inchikey"] for r in rows if r["name"] == name], name


def test_allow_list_entries_exist(seeded):
    assert set(EMBED_ALLOW_LIST) <= set(seeded), "stale allow-list entry"


def test_existing_db_rows_are_corrected(tmp_path):
    """A DB seeded before the fix (seeding is additive by name) gets the corrected structures on next launch."""
    from orgchem.config import AppConfig
    from orgchem.db import session as dbsession
    from orgchem.db.models import Molecule as DBMol
    from orgchem.db.seed_corrections import apply_seed_corrections

    old = {"Camphor": "CC1(C)[C@@H]2CC[C@]1(C)C(=O)C2",
           "Codeine": "COc1ccc2C[C@H]3[C@@H]4C=C[C@@H](O)[C@H]5Oc1c2[C@]45CCN3C",
           "Oxycodone (OxyContin)": "CN1CC[C@@]23c4c5ccc(OC)c4O[C@H]2C(=O)CC[C@@]3(O)[C@H]1C5",
           "L-Alanine": "C[C@@H](N)C(=O)O"}  # was seeded as D-alanine
    prev = (dbsession._engine, dbsession._SessionLocal)
    dbsession.init_db(AppConfig(db_path=tmp_path / "old.sqlite", log_dir=tmp_path, cache_dir=tmp_path))
    try:
        with dbsession.session_scope() as s:
            for name, smi in old.items():
                m = Molecule.from_smiles(smi, name=name, generate_3d=False)
                s.add(DBMol(name=name, smiles=m.smiles, inchikey=m.inchikey, formula=m.formula, molblock_2d="stale"))
        s_user = DBMol(name="D-Alanine", smiles="C[C@@H](N)C(=O)O",
                       inchikey=Molecule.from_smiles("C[C@@H](N)C(=O)O", generate_3d=False).inchikey)
        with dbsession.session_scope() as s:
            s.add(s_user)  # a user's own row with an old key but another name must be left alone
        assert apply_seed_corrections() == 4
        assert apply_seed_corrections() == 0  # idempotent
        with dbsession.session_scope() as s:
            got = {r.name: (r.inchikey, r.molblock_2d) for r in s.query(DBMol)}
        user = got.pop("D-Alanine")
        assert user[0] == "QNAYBMKLOCPYGJ-UWTATZPHSA-N"  # untouched D-alanine
        assert {k: v[0] for k, v in got.items()} == {**EXPECTED, "L-Alanine": "QNAYBMKLOCPYGJ-REOHCLBHSA-N"}
        assert all(v[1] is None for v in got.values())  # stale 2D layout cleared for the backfill
    finally:
        dbsession._engine.dispose()
        dbsession._engine, dbsession._SessionLocal = prev
