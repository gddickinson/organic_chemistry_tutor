"""Round 81 — ``get_mechanism_details`` action tests.

Action-surface gap from round 67 closed: LLM-generated scripts can
now read the full arrow + lone-pair JSON for any seeded mechanism,
not just the summary exposed by ``list_mechanisms`` /
``open_mechanism``.
"""
from __future__ import annotations

import pytest

from orgchem.agent.headless import HeadlessApp


@pytest.fixture(scope="module")
def _app():
    with HeadlessApp() as app:
        yield app


def test_returns_full_mechanism_json_for_diels_alder(_app):
    r = _app.call("get_mechanism_details", name_or_id="Diels-Alder")
    assert "error" not in r, r
    assert r["name"].startswith("Diels-Alder")
    assert "category" in r
    assert "description" in r
    # Full mechanism JSON must include every step's data.
    mech = r["mechanism"]
    assert "steps" in mech and mech["steps"], "empty steps"
    step0 = mech["steps"][0]
    assert "title" in step0
    assert "description" in step0
    assert "smiles" in step0
    assert "arrows" in step0
    assert "lone_pairs" in step0
    # DA step 1 should have multiple curly arrows.
    assert len(step0["arrows"]) >= 2
    for a in step0["arrows"]:
        # Every arrow carries the expected keys.
        assert "from_atom" in a
        assert "to_atom" in a
        assert "kind" in a


def test_returns_error_for_unknown_name(_app):
    r = _app.call(
        "get_mechanism_details",
        name_or_id="Mechanism-That-Does-Not-Exist-XYZ",
    )
    assert "error" in r


def test_lookup_by_id(_app):
    # First use list_mechanisms to grab a real id, then hand it
    # back as a string to prove the isdigit() path works.
    listing = _app.call("list_mechanisms")
    assert listing, "no seeded mechanisms"
    a_row = listing[0]
    r = _app.call("get_mechanism_details",
                  name_or_id=str(a_row["id"]))
    assert "error" not in r, r
    assert r["id"] == a_row["id"]
    assert r["name"] == a_row["name"]


def test_phase_13c_features_exposed_for_hiv_protease(_app):
    """HIV protease mechanism exercises Phase 13c: bond-midpoint
    arrows + lone-pair dots.  The action must surface both fields."""
    r = _app.call("get_mechanism_details", name_or_id="HIV protease")
    assert "error" not in r, r
    mech = r["mechanism"]
    # At least one step must carry lone-pair dots.
    assert any(step.get("lone_pairs") for step in mech["steps"]), (
        "expected HIV protease to expose lone_pairs; "
        f"got {[s.get('lone_pairs') for s in mech['steps']]}")
    # At least one arrow must carry from_bond or to_bond.
    has_bond_arrow = any(
        a.get("from_bond") is not None or a.get("to_bond") is not None
        for step in mech["steps"]
        for a in step.get("arrows", [])
    )
    assert has_bond_arrow, "expected a bond-midpoint arrow"


def test_distinct_from_open_mechanism_return_shape(_app):
    """``open_mechanism`` returns just a summary (id / name / steps-
    count).  ``get_mechanism_details`` MUST return the full step list."""
    open_r = _app.call("open_mechanism", name_or_id="Diels-Alder")
    details_r = _app.call("get_mechanism_details",
                          name_or_id="Diels-Alder")

    # open_mechanism's "steps" is an int (count), not a list.
    assert isinstance(open_r.get("steps"), int)
    # get_mechanism_details carries the real list under mechanism.steps.
    assert isinstance(details_r["mechanism"]["steps"], list)
    # And the count matches.
    assert len(details_r["mechanism"]["steps"]) == open_r["steps"]
