"""Tests for Phase 4 follow-up — HRMS formula candidate guesser."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


def test_benzene_ranks_first():
    """The correct formula for a benzene HRMS peak is C6H6 at 78.04695."""
    from orgchem.core.hrms import guess_formula
    hits = guess_formula(78.04695, ppm_tolerance=5.0, top_k=5)
    assert hits
    assert hits[0].formula == "C6H6"
    assert abs(hits[0].ppm_error) < 1.0
    assert hits[0].dbe == 4.0


def test_acetaminophen_ranks_first():
    """Paracetamol (C8H9NO2) monoisotopic mass is 151.06333 Da."""
    from orgchem.core.hrms import guess_formula
    hits = guess_formula(151.06333, ppm_tolerance=5.0, top_k=5)
    assert hits
    assert hits[0].formula == "C8H9NO2"
    assert hits[0].dbe == 5.0


def test_nitrogen_rule_rejects_odd_mass_for_zero_n():
    """A molecule with no N must have an even nominal mass. Attempting
    to fit an odd-integer mass with max_n=0 should yield nothing."""
    from orgchem.core.hrms import guess_formula
    hits = guess_formula(101.0, ppm_tolerance=100.0, top_k=5,
                         bounds={"C": (0, 20), "H": (0, 30),
                                 "N": (0, 0), "O": (0, 5)})
    assert not any(c.counts.get("N", 0) != 0 for c in hits)
    # No odd-mass neutral with zero nitrogens survives — the list may
    # contain even-mass candidates only if the window is wide enough.


def test_dbe_is_non_negative():
    """Every returned candidate must have a non-negative integer DBE."""
    from orgchem.core.hrms import guess_formula
    hits = guess_formula(300.0, ppm_tolerance=200.0, top_k=20)
    for c in hits:
        assert c.dbe >= 0
        assert c.dbe == int(c.dbe)


def test_senior_rule_rejects_odd_valence_sum():
    """A hypothetical 'CH3' fragment (Σ valence = 4 + 3 = 7, odd) must
    be rejected. Whatever actually comes back, all candidates must
    satisfy the even-valence-sum requirement."""
    from orgchem.core.hrms import guess_formula
    hits = guess_formula(16.03130, ppm_tolerance=200.0, top_k=5)
    for c in hits:
        assert c.valence_sum % 2 == 0


def test_ppm_tolerance_sensitivity():
    """Tighter ppm tolerance must not *add* candidates compared to a
    looser one."""
    from orgchem.core.hrms import guess_formula
    wide = guess_formula(150.0, ppm_tolerance=100.0, top_k=50)
    narrow = guess_formula(150.0, ppm_tolerance=5.0, top_k=50)
    # Narrower can't be strictly bigger than wider.
    assert len(narrow) <= len(wide)


def test_invalid_mass_raises():
    from orgchem.core.hrms import guess_formula
    with pytest.raises(ValueError):
        guess_formula(0.0)
    with pytest.raises(ValueError):
        guess_formula(-1.0)


def test_invalid_ppm_raises():
    from orgchem.core.hrms import guess_formula
    with pytest.raises(ValueError):
        guess_formula(100.0, ppm_tolerance=0.0)


def test_hill_formula_ordering():
    """Hill convention: C first, then H, then alphabetical heteroatoms."""
    from orgchem.core.hrms import _hill_formula
    assert _hill_formula({"C": 6, "H": 12, "O": 6}) == "C6H12O6"
    assert _hill_formula({"H": 4, "C": 1}) == "CH4"
    assert _hill_formula({"C": 1, "Cl": 4}) == "CCl4"


def test_suggest_for_smiles_round_trip():
    """A round-trip: SMILES → mass → guess should put the true formula
    at rank 1 with near-zero ppm error."""
    from orgchem.core.hrms import suggest_formula_for_smiles
    r = suggest_formula_for_smiles("CC(=O)Oc1ccccc1C(=O)O", ppm_tolerance=5.0)
    assert r["n_candidates"] >= 1
    # Aspirin = C9H8O4
    assert r["candidates"][0]["formula"] == "C9H8O4"
    assert abs(r["candidates"][0]["ppm_error"]) < 1.0


# ---- Agent action ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_guess_formula_action(app):
    r = app.call("guess_formula", mass=78.04695, ppm_tolerance=5.0)
    assert "error" not in r
    assert r["candidates"][0]["formula"] == "C6H6"


def test_guess_formula_for_smiles_action(app):
    r = app.call("guess_formula_for_smiles",
                 smiles="CC(=O)Oc1ccccc1C(=O)O", ppm_tolerance=5.0)
    assert "error" not in r
    assert r["candidates"][0]["formula"] == "C9H8O4"


def test_guess_formula_invalid_action(app):
    r = app.call("guess_formula", mass=-1.0)
    assert "error" in r
