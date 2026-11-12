"""Read-only snapshot of the seeded OrgChem content for the web interface.

The desktop app seeds a SQLite DB on first launch (orgchem/db/seed.py). The web app runs that same seeding into a
private temporary DB (never the user's own ~/Library/Application Support/OrgChem DB) and keeps plain-dict copies of
the rows it serves: molecules, reactions (+ mechanisms and energy profiles), synthesis pathways and glossary terms.
Nothing here is invented: every field comes from the seed modules or the repo's own chemistry code.
"""
from __future__ import annotations

import json
import logging
import tempfile
from functools import lru_cache
from pathlib import Path

log = logging.getLogger(__name__)

# Molecule "source" tags shown as browse groups, in display order; anything else falls under "other".
SOURCE_LABELS = {
    "basics": "Basics", "reference-set": "Verma et al. 2024 reference set", "amino-acid": "Amino acids",
    "drug": "Drugs", "solvent": "Solvents", "natural-product": "Natural products", "reagent": "Reagents",
    "biomolecule": "Biomolecules", "dye": "Dyes", "pah": "PAHs", "heterocycle": "Heterocycles",
    "terpene": "Terpenes", "intermediate": "Reactive intermediates",
}


def _loads(text, default):
    try:
        return json.loads(text) if text else default
    except (TypeError, ValueError):
        return default


@lru_cache(maxsize=1)
def snapshot() -> dict:
    """Seed a throw-away DB with the app's own seeders and return its rows as dicts (cached per process)."""
    from orgchem.config import AppConfig
    from orgchem.db import session as dbsession
    from orgchem.db.models import GlossaryTerm, Molecule, Reaction, SynthesisPathway, SynthesisStep
    from orgchem.db.seed import seed_if_empty

    tmp = Path(tempfile.mkdtemp(prefix="orgchem-web-"))
    logging.getLogger("orgchem").setLevel(logging.WARNING)
    prev = (dbsession._engine, dbsession._SessionLocal)
    dbsession.init_db(AppConfig(db_path=tmp / "web.sqlite", log_dir=tmp, cache_dir=tmp))
    try:
        seed_if_empty(None)
        with dbsession.session_scope() as s:
            mols = [_molecule(m) for m in s.query(Molecule).order_by(Molecule.id)]
            rxns = [_reaction(r) for r in s.query(Reaction).order_by(Reaction.id)]
            paths = []
            for p in s.query(SynthesisPathway).order_by(SynthesisPathway.id):
                steps = (s.query(SynthesisStep).filter_by(pathway_id=p.id)
                         .order_by(SynthesisStep.step_index).all())
                paths.append({
                    "id": p.id, "name": p.name, "target_name": p.target_name, "target_smiles": p.target_smiles,
                    "category": p.category, "source": p.source, "description": p.description,
                    "steps": [{"reaction_smiles": st.reaction_smiles, "reagents": st.reagents,
                               "conditions": st.conditions, "yield_pct": st.yield_pct, "notes": st.notes}
                              for st in steps],
                })
            gloss = [{"term": g.term, "aliases": _loads(g.aliases_json, []), "category": g.category,
                      "see_also": _loads(g.see_also_json, []), "definition_md": g.definition_md,
                      "example_smiles": g.example_smiles}
                     for g in s.query(GlossaryTerm).order_by(GlossaryTerm.term)]
    finally:
        if dbsession._engine is not None:
            dbsession._engine.dispose()
        dbsession._engine, dbsession._SessionLocal = prev
    return {"molecules": mols, "reactions": rxns, "pathways": paths, "glossary": gloss}


def _molecule(m) -> dict:
    fg = [t for t in _loads(m.functional_group_tags_json, []) if not t.startswith("__")]
    src = [t for t in _loads(m.source_tags_json, []) if not t.startswith("__")]
    return {
        "id": m.id, "name": m.name, "smiles": m.smiles, "formula": m.formula, "inchikey": m.inchikey,
        "source": m.source, "properties": _loads(m.properties_json, {}), "tags": fg, "source_tags": src,
        "synonyms": _loads(m.synonyms_json, []), "heavy_atom_count": m.heavy_atom_count,
        "formal_charge": m.formal_charge, "n_rings": m.n_rings, "has_stereo": m.has_stereo,
        "molblock_2d": m.molblock_2d,
    }


def _reaction(r) -> dict:
    from orgchem.core.energy_profile import ReactionEnergyProfile
    prof = _loads(r.energy_profile_json, None)
    if prof:
        p = ReactionEnergyProfile.from_dict(prof)
        prof = dict(p.to_dict(), activation_energies=p.activation_energies, delta_h=p.delta_h)
    mech = _loads(r.mechanism_json, None)
    return {
        "id": r.id, "name": r.name, "category": r.category, "description": r.description,
        "reaction_smiles": r.reaction_smarts, "mechanism": mech, "energy_profile": prof,
    }


def molecule(mid: int):
    return next((m for m in snapshot()["molecules"] if m["id"] == mid), None)


def reaction(rid: int):
    return next((r for r in snapshot()["reactions"] if r["id"] == rid), None)


def pathway(pid: int):
    return next((p for p in snapshot()["pathways"] if p["id"] == pid), None)
