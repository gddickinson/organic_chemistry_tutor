"""Database engine and transactional session management."""
from __future__ import annotations
from contextlib import contextmanager
from typing import Iterator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from orgchem.config import AppConfig
from orgchem.db.models import Base

_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None


def init_db(cfg: AppConfig) -> None:
    """Create the engine and schema; call once at startup.

    Also applies any lightweight additive migrations — small enough to live
    here rather than pull in Alembic. Each migration is a single ALTER
    TABLE guarded by an "is this column already there?" check.
    """
    global _engine, _SessionLocal
    cfg.db_path.parent.mkdir(parents=True, exist_ok=True)
    _engine = create_engine(f"sqlite:///{cfg.db_path}", future=True)
    Base.metadata.create_all(_engine)
    _apply_additive_migrations(_engine)
    _SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False, future=True)


def _apply_additive_migrations(engine) -> None:
    """Add columns introduced after a database was first created."""
    import logging
    from sqlalchemy import text
    log = logging.getLogger(__name__)
    with engine.begin() as conn:
        cols = {r[1] for r in conn.exec_driver_sql(
            "PRAGMA table_info(reactions)"
        ).fetchall()}
        if "reaction_smarts_mapped" not in cols:
            conn.exec_driver_sql(
                "ALTER TABLE reactions ADD COLUMN reaction_smarts_mapped TEXT"
            )
            log.info("Migrated: added reactions.reaction_smarts_mapped")
        if "energy_profile_json" not in cols:
            conn.exec_driver_sql(
                "ALTER TABLE reactions ADD COLUMN energy_profile_json TEXT"
            )
            log.info("Migrated: added reactions.energy_profile_json")

        # Phase 26a — glossary figure columns.
        gloss_cols = {r[1] for r in conn.exec_driver_sql(
            "PRAGMA table_info(glossary_terms)"
        ).fetchall()}
        if gloss_cols and "example_smiles" not in gloss_cols:
            conn.exec_driver_sql(
                "ALTER TABLE glossary_terms ADD COLUMN "
                "example_smiles VARCHAR(500)"
            )
            log.info("Migrated: added glossary_terms.example_smiles")
        if gloss_cols and "example_figure_path" not in gloss_cols:
            conn.exec_driver_sql(
                "ALTER TABLE glossary_terms ADD COLUMN "
                "example_figure_path VARCHAR(500)"
            )
            log.info("Migrated: added glossary_terms.example_figure_path")

        # Phase 28a — Molecule multi-category filter columns.
        mol_cols = {r[1] for r in conn.exec_driver_sql(
            "PRAGMA table_info(molecules)"
        ).fetchall()}
        if mol_cols:
            additions = [
                ("source_tags_json", "TEXT"),
                ("functional_group_tags_json", "TEXT"),
                ("heavy_atom_count", "INTEGER"),
                ("formal_charge", "INTEGER"),
                ("n_rings", "INTEGER"),
                ("has_stereo", "BOOLEAN"),
                # Round 58 — common-name synonyms for DB-name
                # reconciliation (Retinol ↔ Vitamin A, etc.).
                ("synonyms_json", "TEXT"),
            ]
            for col_name, col_type in additions:
                if col_name not in mol_cols:
                    conn.exec_driver_sql(
                        f"ALTER TABLE molecules ADD COLUMN "
                        f"{col_name} {col_type}"
                    )
                    log.info("Migrated: added molecules.%s", col_name)


@contextmanager
def session_scope() -> Iterator[Session]:
    if _SessionLocal is None:
        raise RuntimeError("Database not initialised — call init_db() first")
    s = _SessionLocal()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()
