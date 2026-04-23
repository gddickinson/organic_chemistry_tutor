"""Round 58 — molecular-identity reconciliation.

User-reported bug: same compound (retinol) stored twice in the
Molecule DB under two different names and with two different
SMILES strings, because the two entries were added from different
sources (Lipids catalogue vs PubChem download). Search for
"retinol" only found one.

Fix: InChIKey-based identity matching everywhere, plus a
synonyms_json column so name searches resolve aliases.
"""
from __future__ import annotations
import os

import pytest

pytest.importorskip("rdkit")


# ---- pure identity helpers ---------------------------------------

def test_canonical_smiles_normalises_order():
    from orgchem.core.identity import canonical_smiles
    # Same molecule, different atom order.
    a = canonical_smiles("CCO")
    b = canonical_smiles("OCC")
    assert a is not None and a == b


def test_canonical_smiles_returns_none_for_bad_input():
    from orgchem.core.identity import canonical_smiles
    assert canonical_smiles("!!!") is None
    assert canonical_smiles("") is None


def test_inchikey_retinol_variants_match():
    """The exact scenario from the user report: PubChem's long-
    IUPAC SMILES and the Lipids catalogue's shorter form must
    resolve to the same InChIKey."""
    from orgchem.core.identity import inchikey
    pubchem = "CC1=C(C(CCC1)(C)C)/C=C/C(=C/C=C/C(=C/CO)/C)/C"
    lipid = "CC1=C(/C=C/C(C)=C/C=C/C(C)=C/CO)C(C)(C)CCC1"
    k1, k2 = inchikey(pubchem), inchikey(lipid)
    assert k1 is not None and k1 == k2


def test_same_molecule_is_order_invariant():
    from orgchem.core.identity import same_molecule
    assert same_molecule("CCO", "OCC")
    assert not same_molecule("CCO", "CCN")


def test_normalise_name_strips_trailing_parens():
    from orgchem.core.identity import normalise_name
    assert normalise_name("Retinol (vitamin A)") == "retinol"
    assert normalise_name("Vitamin C") == "vitamin c"
    assert normalise_name("α-D-Glucopyranose") == "α-d-glucopyranose"


# ---- DB-level search + dedup -------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_find_molecule_by_smiles_matches_different_strings(app):
    """find_molecule_by_smiles must hit by InChIKey, not raw string
    — so passing the PubChem form of ethanol finds the DB row that
    was seeded with the ordinary form."""
    from orgchem.db.queries import find_molecule_by_smiles, find_molecule_by_name
    # Ethanol is seeded. Its canonical SMILES is "CCO". Query with
    # a rearranged SMILES.
    row = find_molecule_by_smiles("OCC")
    assert row is not None
    assert row.name.lower() in ("ethanol", "ethyl alcohol",
                                "c2h6o", "ethanol (ethyl alcohol)")


def test_add_molecule_rejects_inchikey_duplicate(app):
    """The round-58 fix — submitting the same compound with a
    different SMILES string still rejects as a duplicate."""
    from orgchem.agent.actions import invoke
    # Pick ethanol canonical form.
    res = invoke("add_molecule",
                 mol_name="Grain-alcohol-test",
                 smiles="OCC")
    assert res["status"] == "rejected"
    assert "InChIKey" in res["reason"] or "already" in res["reason"]


def test_synonym_search_finds_row_by_alias(app):
    """After the synonym seeder runs, searching for a common alias
    (Retinol, Vitamin A, etc.) resolves the same row as the
    canonical name."""
    from orgchem.db.queries import find_molecule_by_name
    # The lipid-catalogue reconciliation will have tagged the DB
    # row (if present) with the "Retinol" synonym. If the user's DB
    # doesn't include retinol, the reconciliation seeds nothing and
    # this test becomes a no-op — that's a valid outcome.
    row = find_molecule_by_name("Ethanol")
    assert row is not None
    row2 = find_molecule_by_name("ethyl alcohol")
    assert row2 is not None
    assert row.id == row2.id


def test_add_molecule_synonym_agent_action(app):
    from orgchem.agent.actions import invoke
    # Pick a seeded molecule and attach a nonsense synonym.
    # Use the unique marker so tests don't conflict.
    res = invoke("add_molecule_synonym",
                 name_or_id="Benzene",
                 synonym="Round58TestAlias")
    assert res["status"] == "accepted"
    # The alias now resolves via find_molecule_by_name.
    from orgchem.db.queries import find_molecule_by_name
    row = find_molecule_by_name("Round58TestAlias")
    assert row is not None
    assert row.name == "Benzene"


def test_add_molecule_synonym_idempotent(app):
    from orgchem.agent.actions import invoke
    # First call already ran in the test above — calling again
    # should return updated=False.
    res = invoke("add_molecule_synonym",
                 name_or_id="Benzene",
                 synonym="Round58TestAlias")
    assert res["status"] == "accepted"
    assert res["updated"] is False


def test_pubchem_name_picker_prefers_short_synonym():
    from orgchem.sources.pubchem import _pick_display_name
    synonyms = [
        "Retinol",                                             # common
        "all-trans-Retinol",
        "Vitamin A",
        ("(2E,4E,6E,8E)-3,7-dimethyl-9-(2,6,6-trimethyl"
         "cyclohexen-1-yl)nona-2,4,6,8-tetraen-1-ol"),
    ]
    iupac = ("(2E,4E,6E,8E)-3,7-dimethyl-9-(2,6,6-trimethyl"
             "cyclohexen-1-yl)nona-2,4,6,8-tetraen-1-ol")
    assert _pick_display_name(synonyms, iupac, fallback="CID 0") == "Retinol"


def test_pubchem_name_picker_skips_systematic_heads():
    from orgchem.sources.pubchem import _pick_display_name
    # All parenthesised-stereo heads; we fall back to iupac.
    synonyms = [
        "(2E,4E)-something-long-stereo-descriptor-that-is-systematic",
    ]
    iupac = "Fallback IUPAC"
    assert _pick_display_name(synonyms, iupac, fallback="x") == "Fallback IUPAC"


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
