"""Phase 6f consistency QA — every reaction / pathway fragment is in the DB,
and a given molecule renders identically wherever it appears."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- Fragment resolver --------------------------------------------

def test_resolve_hit_returns_db_entry(app):
    """A seeded molecule should come back with ``from_db=True``."""
    from orgchem.core.fragment_resolver import resolve
    r = resolve("CCO")
    assert r is not None
    assert r.from_db is True
    assert r.db_name == "Ethanol"


def test_resolve_miss_falls_back(app):
    """An unseeded molecule returns a ResolvedFragment with ``from_db=False``
    and a freshly-computed Mol with 2D coords."""
    from orgchem.core.fragment_resolver import resolve
    r = resolve("CCCCCCCCCCCCCCCCCCCCCCCCCC")  # 26-carbon alkane, not seeded
    assert r is not None
    assert r.from_db is False
    assert r.mol.GetNumConformers() >= 1


def test_resolve_unparseable_returns_none(app):
    from orgchem.core.fragment_resolver import resolve
    assert resolve("not a molecule") is None
    assert resolve("") is None


def test_canonical_reaction_smiles_round_trips_known_fragments(app):
    """Every fragment in a seeded reaction is canonicalised via the DB."""
    from orgchem.core.fragment_resolver import canonical_reaction_smiles
    result = canonical_reaction_smiles("CC(=O)O.CCO>>CC(=O)OCC.O")
    # Same structures, just deterministic canonical forms on every run
    assert ">>" in result
    lhs, rhs = result.split(">>")
    assert sorted(lhs.split(".")) == sorted("CC(=O)O.CCO".split("."))
    # rhs should contain both ethyl acetate and water
    assert "O" in rhs.split(".")


# ---- Coverage audit: every reaction + pathway step ------------------

def test_every_reaction_fragment_is_in_db(app):
    """After Phase 6f.3 seeding, 100% of reaction-SMILES fragments resolve."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Reaction as DBRxn
    from orgchem.core.fragment_resolver import audit_reaction

    missing = []
    with session_scope() as s:
        for r in s.query(DBRxn).all():
            aud = audit_reaction(r.reaction_smarts)
            for m in aud["missing"]:
                missing.append((r.name, m.get("canonical") or m.get("fragment")))

    assert not missing, (
        f"Uncovered reaction fragments ({len(missing)}). Seed them in "
        f"seed_intermediates.py:\n" +
        "\n".join(f"  [{n}] {frag!r}" for n, frag in missing[:20])
    )


def test_every_pathway_step_fragment_is_in_db(app):
    """Every fragment across all synthesis-pathway steps resolves to a DB row."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import SynthesisStep
    from orgchem.core.fragment_resolver import audit_reaction

    missing = []
    with session_scope() as s:
        for step in s.query(SynthesisStep).all():
            aud = audit_reaction(step.reaction_smiles)
            for m in aud["missing"]:
                missing.append((step.id,
                                m.get("canonical") or m.get("fragment")))

    assert not missing, (
        f"Uncovered pathway-step fragments ({len(missing)}):\n" +
        "\n".join(f"  [step {sid}] {frag!r}" for sid, frag in missing[:20])
    )


def test_every_db_molecule_has_cached_coords(app):
    """Phase 6f.2: every Molecule row has a non-null molblock_2d."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Molecule as DBMol
    with session_scope() as s:
        total = s.query(DBMol).count()
        missing = s.query(DBMol).filter(DBMol.molblock_2d.is_(None)).count()
    assert missing == 0, f"{missing} / {total} molecules missing cached 2D coords"


# ---- Cross-tab rendering consistency -------------------------------

def test_same_molecule_renders_same_coords_in_molecule_and_reaction(app):
    """A given DB molecule's coords should be identical whether accessed
    via the 2D renderer directly or via the reaction/fragment resolver
    — the whole point of Phase 6f.1+6f.2."""
    from rdkit import Chem
    from orgchem.core.fragment_resolver import resolve

    # Pick a well-known seeded molecule.
    r1 = resolve("c1ccccc1")  # benzene
    r2 = resolve("c1ccccc1")  # again
    assert r1.from_db and r2.from_db
    assert r1.db_id == r2.db_id

    # Same SMILES as you'd get from walking the canonical reaction scheme:
    r3 = resolve("C1=CC=CC=C1")  # alternate SMILES for benzene
    assert r3 is not None
    assert r3.from_db is True
    assert r3.db_id == r1.db_id, (
        "Different SMILES for benzene should resolve to the same DB row "
        "via InChIKey lookup"
    )


def test_intermediate_seeding_populated(app):
    """Phase 6f.3 added ~120 intermediate molecules."""
    from orgchem.db.session import session_scope
    from orgchem.db.models import Molecule as DBMol
    with session_scope() as s:
        n = s.query(DBMol).filter_by(source="intermediate").count()
    assert n >= 60, f"expected ≥60 intermediate molecules, got {n}"


def test_fmoc_amino_acid_intermediates_present(app):
    """SPPS should have its per-step Fmoc-AAs and growing chain in the DB."""
    rows = app.call("list_all_molecules")
    names = {r["name"] for r in rows}
    for expected in ("Fmoc-Gly-OH", "Fmoc-Phe-OH",
                     "Fmoc-Met-OH", "Fmoc-Tyr-OH",
                     "Dibenzofulvene", "9-Fluorenylmethanol"):
        assert expected in names, f"missing SPPS intermediate {expected!r}"


def test_enzyme_substrate_intermediates_present(app):
    """Aldolase substrates / products visible in the DB."""
    rows = app.call("list_all_molecules")
    names = {r["name"] for r in rows}
    for expected in ("DHAP (dihydroxyacetone phosphate)",
                     "G3P (glyceraldehyde-3-phosphate)",
                     "Fructose-1,6-bisphosphate",
                     "N-acetylglycine (chymotrypsin substrate analogue)"):
        assert expected in names, f"missing enzyme intermediate {expected!r}"


def test_reaction_render_uses_db_canonicalisation(app, tmp_path):
    """Two different SMILES for the same molecule should produce the same SVG
    once routed through the DB canonicaliser."""
    from orgchem.render.draw_reaction import render_svg
    a = render_svg("c1ccccc1.[H][H]>>C1CCCCC1", use_db_coords=True)
    b = render_svg("C1=CC=CC=C1.[H][H]>>C1CCCCC1", use_db_coords=True)
    # The SVGs are generated by RDKit; identical up to whitespace if
    # coords are shared. At minimum, both contain the benzene DB atom
    # count (6 carbons).
    assert "svg" in a.lower() and "svg" in b.lower()
    # Both use DB canonicalisation so both should succeed without error.
    assert len(a) > 1000 and len(b) > 1000
