"""Tests for Phase 16e — HIV protease mechanism seeding."""
from __future__ import annotations
import json
import pytest

pytest.importorskip("rdkit")


def test_hiv_protease_builder_returns_three_steps():
    from orgchem.db.seed_mechanisms import _hiv_protease
    mech = _hiv_protease()
    assert len(mech) == 3
    titles = [s.title for s in mech.steps]
    assert "Step 1" in titles[0]
    assert "Step 2" in titles[1]
    assert "Step 3" in titles[2]


def test_hiv_protease_uses_lone_pairs():
    """Phase 13c follow-up: the step-1 water oxygen gets a lone-pair pair."""
    from orgchem.db.seed_mechanisms import _hiv_protease
    mech = _hiv_protease()
    assert mech.steps[0].lone_pairs, \
        "Step 1 should flag the attacking water as a lone-pair bearer"


def test_hiv_protease_uses_bond_midpoint_arrow():
    """Phase 13c follow-up: the step-2 C-N heterolysis arrow starts at a
    bond midpoint."""
    from orgchem.db.seed_mechanisms import _hiv_protease
    mech = _hiv_protease()
    step2 = mech.steps[1]
    assert any(a.from_bond is not None for a in step2.arrows), \
        "Step 2 should have a bond-midpoint arrow for σ-bond cleavage"


def test_hiv_protease_roundtrips_json():
    """Full round-trip through the JSON serialisation exercised by the
    seeder — tuples must survive."""
    from orgchem.core.mechanism import Mechanism
    from orgchem.db.seed_mechanisms import _hiv_protease
    mech = _hiv_protease()
    text = mech.to_json()
    back = Mechanism.from_json(text)
    s2 = back.steps[1]
    fb = s2.arrows[0].from_bond
    assert fb is not None
    assert isinstance(fb, tuple)
    assert len(fb) == 2


def test_seed_version_bumped():
    """Bumping SEED_VERSION forces existing DBs to pick up the new mechanism."""
    from orgchem.db.seed_mechanisms import SEED_VERSION
    assert SEED_VERSION >= 6


def test_hiv_protease_reaction_in_starter_set():
    """The matching reaction row must exist so the mechanism can attach."""
    from orgchem.db.seed_reactions import _STARTER
    names = [row[0] for row in _STARTER]
    assert any("HIV protease" in n for n in names)
