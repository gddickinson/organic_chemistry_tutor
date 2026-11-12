"""Regression: a database seeded by an older release is brought up to date on the next launch.

Seeding is additive by name and reactions / pathways are only seeded into an empty DB, so before the startup migration
(`db/seed_corrections.py` + `db/seed_corrections_rxn.py`) an existing user DB kept wrong structures forever. This test
builds an old-format DB holding the pre-fix rows (plus look-alike rows a user made), runs the app's startup seeding
and checks that the seeded rows are corrected or renamed exactly once and the user's rows are untouched.
"""
import pytest

from orgchem.core.molecule import Molecule


@pytest.fixture
def old_db(tmp_path):
    from orgchem.config import AppConfig
    from orgchem.db import session as dbsession
    prev = (dbsession._engine, dbsession._SessionLocal)
    dbsession.init_db(AppConfig(db_path=tmp_path / "old.sqlite", log_dir=tmp_path, cache_dir=tmp_path))
    yield dbsession
    dbsession._engine.dispose()
    dbsession._engine, dbsession._SessionLocal = prev


def _mol_row(DBMol, name, smiles):
    m = Molecule.from_smiles(smiles, generate_3d=False)
    return DBMol(name=name, smiles=m.smiles, inchi=m.inchi, inchikey=m.inchikey, formula=m.formula,
                 molblock_2d="stale", functional_group_tags_json='["ketone", "__v1__"]')


def test_old_database_is_migrated(old_db):
    from orgchem.db.models import Molecule as DBMol, Reaction, SynthesisPathway, SynthesisStep
    from orgchem.db.seed import seed_if_empty
    from orgchem.db.seed_corrections import RENAMES
    from orgchem.db.seed_corrections_rxn import PATHWAY_CORRECTIONS, REACTION_CORRECTIONS

    asp_name, asp_old_target, asp_new_target, asp_steps = PATHWAY_CORRECTIONS[0]
    with old_db.session_scope() as s:
        s.add(_mol_row(DBMol, "Limonene", "CC(=C)[C@@H]1CC=C(C)CC1"))
        s.add(_mol_row(DBMol, "Acetyl ester (generic)", "CC(C)=O"))
        s.add(_mol_row(DBMol, "My limonene", "CC(=C)[C@@H]1CC=C(C)CC1"))  # user's own row: same old key, other name
        for name, old, _new in REACTION_CORRECTIONS:
            s.add(Reaction(name=name, reaction_smarts=old, category="old"))
        s.add(Reaction(name="My CBS copy", reaction_smarts=REACTION_CORRECTIONS[2][1], category="user"))
        p = SynthesisPathway(name=asp_name, target_name="Aspartame", target_smiles=asp_old_target)
        s.add(p)
        s.flush()
        s.add(SynthesisStep(pathway_id=p.id, step_index=0, reaction_smiles="kept as is"))
        for idx, old, _new in asp_steps:
            s.add(SynthesisStep(pathway_id=p.id, step_index=idx, reaction_smiles=old))

    seed_if_empty(None)

    with old_db.session_scope() as s:
        names = [r.name for r in s.query(DBMol)]
        for old_name, _key, new_name, smiles, _src in RENAMES:
            assert old_name not in names
            assert names.count(new_name) == 1, new_name  # renamed, not seeded a second time
        lim = s.query(DBMol).filter_by(name="(R)-(+)-Limonene").one()
        assert lim.inchikey == "XMGQYMWWDOXHJM-JTQLQIEISA-N" and lim.molblock_2d != "stale"
        ester = s.query(DBMol).filter_by(name="Methyl acetate (representative acetyl ester)").one()
        assert "ester" in ester.functional_group_tags_json and "ketone" not in ester.functional_group_tags_json
        user = s.query(DBMol).filter_by(name="My limonene").one()
        assert user.inchikey == "XMGQYMWWDOXHJM-SNVBAGLBSA-N" and user.molblock_2d == "stale"
        rx = {r.name: r.reaction_smarts for r in s.query(Reaction)}
        for name, _old, new in REACTION_CORRECTIONS:
            assert rx[name] == new, name
        assert rx["My CBS copy"] == REACTION_CORRECTIONS[2][1]
        p = s.query(SynthesisPathway).filter_by(name=asp_name).one()
        assert p.target_smiles == asp_new_target
        steps = {st.step_index: st.reaction_smiles for st in s.query(SynthesisStep).filter_by(pathway_id=p.id)}
        assert steps[0] == "kept as is"
        for idx, _old, new in asp_steps:
            assert steps[idx] == new


def test_correction_tables_match_current_seeds():
    """The migration must write exactly what a fresh install seeds."""
    from orgchem.db.seed_corrections_rxn import PATHWAY_CORRECTIONS, REACTION_CORRECTIONS
    from orgchem.db.seed_pathways import _STARTER as PATHS
    from orgchem.db.seed_reactions import _STARTER as RXNS
    rx = {r[0]: r[3] for r in RXNS}
    for name, old, new in REACTION_CORRECTIONS:
        assert rx[name] == new and old != new
    paths = {p[0]: p for p in PATHS}
    for name, _old, new_target, steps in PATHWAY_CORRECTIONS:
        assert paths[name][2] == new_target
        for idx, _old_step, new in steps:
            assert paths[name][6][idx]["reaction_smiles"] == new
