"""Tests for Phase 16d — RNase A mechanism seeding (round 30)."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


def test_rnase_a_builder_returns_two_steps():
    from orgchem.db.seed_mechanisms import _rnase_a
    mech = _rnase_a()
    assert len(mech) == 2
    titles = [s.title for s in mech.steps]
    assert "Step 1" in titles[0]
    assert "Step 2" in titles[1]


def test_rnase_a_step1_uses_lone_pair_and_bond_midpoint():
    """Step 1 (transphosphorylation) must showcase both Phase 13c
    features: the 2'-oxide attacker gets lone-pair dots, and the
    P-O(5') cleavage arrow starts at a bond midpoint."""
    from orgchem.db.seed_mechanisms import _rnase_a
    mech = _rnase_a()
    s = mech.steps[0]
    assert s.lone_pairs, "Step 1 should flag the 2'-oxygen attacker"
    assert any(a.from_bond is not None for a in s.arrows), \
        "Step 1 should have a bond-midpoint arrow for P-O(5') cleavage"


def test_rnase_a_step2_uses_bond_midpoint():
    """Step 2 (hydrolysis) also has a bond-midpoint arrow."""
    from orgchem.db.seed_mechanisms import _rnase_a
    mech = _rnase_a()
    s = mech.steps[1]
    assert s.lone_pairs, "Step 2 should flag the water O attacker"
    assert any(a.from_bond is not None for a in s.arrows), \
        "Step 2 should have a bond-midpoint arrow for P-O(2') cleavage"


def test_rnase_a_json_round_trip():
    from orgchem.core.mechanism import Mechanism
    from orgchem.db.seed_mechanisms import _rnase_a
    text = _rnase_a().to_json()
    back = Mechanism.from_json(text)
    assert len(back) == 2
    # Tuples survive the JSON round-trip.
    for step in back.steps:
        for a in step.arrows:
            if a.from_bond is not None:
                assert isinstance(a.from_bond, tuple)


def test_rnase_a_reaction_seeded():
    from orgchem.db.seed_reactions import _STARTER
    names = [row[0] for row in _STARTER]
    assert any("RNase A" in n for n in names)


def test_seed_version_bumped_to_seven():
    from orgchem.db.seed_mechanisms import SEED_VERSION
    assert SEED_VERSION >= 7


def test_mech_map_contains_rnase_a():
    from orgchem.db.seed_mechanisms import _MECH_MAP
    assert "RNase A" in _MECH_MAP
